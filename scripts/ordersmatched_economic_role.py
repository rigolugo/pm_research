"""OrdersMatched economic-role probe (Dune-sourced, research only).

OrdersMatched fires ONCE per trade and carries `takerordermaker` = the wallet
that owned the TAKER (aggressor) order. So:
  wallet == takerordermaker            -> ECONOMIC_TAKER_CONFIRMED (direct)
  wallet is a confirmed maker-leg party -> ECONOMIC_MAKER_CONFIRMED (paired)

Per Copilot: economic MAKER is NEVER assigned by mere exclusion. A wallet is
ECONOMIC_MAKER_CONFIRMED only if it is positively present as the maker side of a
paired OrderFilled leg for that same trade (matched on tx + token/asset +
amount), AND it is not the takerordermaker.

Two phases:
  Phase 1 (no --dune-csv): sample tx, write tx-list + the exact Dune query.
  Phase 2 (--dune-csv given): ingest Dune OrdersMatched rows, optionally pair
    against OrderFilled legs (--rpc-url or --orderfilled-csv) to confirm maker
    side, classify economic role, report recoverability.

Data source for OrdersMatched is DUNE (path B) — NOT RPC self-decode (avoids
re-deriving the OrdersMatched ABI). OrderFilled legs, used only to confirm the
maker side, may come from RPC (reusing the validated decoder) or a prior CSV.

No indexer. No log_index backfill. No PnL. No strategy claim. No trading.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import time

import pandas as pd

from pm_research.data.store import Store

_ofj_spec = importlib.util.spec_from_file_location(
    "orderfilled_sample_join",
    str(pathlib.Path(__file__).resolve().parent / "orderfilled_sample_join.py"))
_ofj = importlib.util.module_from_spec(_ofj_spec)
_ofj_spec.loader.exec_module(_ofj)

_op_spec = importlib.util.spec_from_file_location(
    "orderfilled_operator_filtered_semantic",
    str(pathlib.Path(__file__).resolve().parent /
        "orderfilled_operator_filtered_semantic.py"))
_op = importlib.util.module_from_spec(_op_spec)
_op_spec.loader.exec_module(_op)

KNOWN_EXCHANGE = _op.KNOWN_EXCHANGE_CONTRACTS


def _read_csv_tolerant(path: str) -> pd.DataFrame:
    """Read a CSV that may be UTF-8-BOM, UTF-16, or latin-1 (Dune/Excel exports
    vary). Tries encodings in order; utf-8-sig strips a BOM if present. Asset/
    amount columns are read as str (dtype) so 78-digit ids are not floated."""
    str_cols = {"makerassetid", "takerassetid", "makeramountfilled",
                "takeramountfilled", "takerordermaker", "takerorderhash",
                "evt_tx_hash", "contract_address"}
    # pandas applies dtype by column name; unknown cols are ignored safely
    dtype_map = {c: str for c in str_cols}
    for enc in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc, dtype=dtype_map)
        except (UnicodeDecodeError, UnicodeError):
            continue
        except ValueError:
            # dtype map mismatch (e.g. different casing) -> read without dtype
            try:
                return pd.read_csv(path, encoding=enc)
            except (UnicodeDecodeError, UnicodeError):
                continue
    import io
    raw = pathlib.Path(path).read_bytes()
    return pd.read_csv(io.StringIO(raw.decode("utf-8", errors="replace")))

DUNE_QUERY_TEMPLATE = """\
-- OrdersMatched economic-role export (paste tx_hash list where indicated).
-- takerordermaker = wallet that owned the TAKER (aggressor) order.
-- uint256 asset/amount fields CAST TO VARCHAR so 78-digit token ids export at
-- full precision (numeric export -> float/scientific notation loses precision
-- and breaks maker-side asset matching).
select 'pm_polygon.ctf' as src, evt_tx_hash, evt_index, contract_address,
       takerorderhash, takerordermaker,
       cast(makerassetid as varchar) as makerassetid,
       cast(takerassetid as varchar) as takerassetid,
       cast(makeramountfilled as varchar) as makeramountfilled,
       cast(takeramountfilled as varchar) as takeramountfilled
from polymarket_polygon.ctfexchange_evt_ordersmatched
where evt_tx_hash in (
{TXLIST}
)
union all
select 'pm_polygon.negrisk' as src, evt_tx_hash, evt_index, contract_address,
       takerorderhash, takerordermaker,
       cast(makerassetid as varchar) as makerassetid,
       cast(takerassetid as varchar) as takerassetid,
       cast(makeramountfilled as varchar) as makeramountfilled,
       cast(takeramountfilled as varchar) as takeramountfilled
from polymarket_polygon.negriskctfexchange_evt_ordersmatched
where evt_tx_hash in (
{TXLIST}
)
order by evt_tx_hash, evt_index
"""

import re as _re
_SCI_RE = _re.compile(r"^[+-]?\d+\.?\d*[eE][+-]?\d+$")


class DataExportPrecisionLoss(Exception):
    """A token/asset id arrived in scientific notation — precision already lost;
    cannot recover the exact integer. Re-export with cast(... as varchar)."""


def canonical_int(value):
    """Normalize an asset/amount id to a canonical int.
      "0"->0 ; "0.0"->0 ; "  123 "->123 ; 123->123
    Scientific notation ("5.20896e+76") RAISES DataExportPrecisionLoss (NOT
    recoverable). None/blank/non-numeric -> None."""
    if value is None:
        return None
    if isinstance(value, int):
        return int(value)
    s = str(value).strip()
    if s == "" or s.lower() in ("nan", "none"):
        return None
    if _SCI_RE.match(s):
        raise DataExportPrecisionLoss(
            f"asset id in scientific notation: {s!r} — re-export Dune CSV with "
            f"cast(... as varchar); precision lost, cannot recover.")
    if s.isdigit() or (s and s[0] in "+-" and s[1:].isdigit()):
        return int(s)
    try:
        f = float(s)
        if f.is_integer():
            return int(f)
    except (ValueError, OverflowError):
        pass
    return None


def write_phase1(samp: pd.DataFrame, out_dir: pathlib.Path) -> list[str]:
    """Emit the tx-list and the Dune query for the user to run."""
    tx_list = list(dict.fromkeys(samp["tx_hash"].tolist()))
    (out_dir / "ordersmatched_dune_tx_list.txt").write_text(
        "\n".join(tx_list))
    txlist_sql = ",\n".join(f"  {tx}" for tx in tx_list)  # 0x literals, no quotes
    query = DUNE_QUERY_TEMPLATE.replace("{TXLIST}", txlist_sql)
    (out_dir / "ordersmatched_dune_query.sql").write_text(query)
    return tx_list


def classify_trade(om_row: dict, wallets: set,
                   of_legs: list[dict] | None) -> dict:
    """Classify the wallet's economic role for one OrdersMatched trade.

    om_row: a Dune OrdersMatched row (takerordermaker, asset ids, amounts).
    of_legs: decoded OrderFilled fills in the same tx (for maker-side pairing),
             or None if unavailable.
    """
    taker_owner = str(om_row.get("takerordermaker", "")).lower()
    contract = str(om_row.get("contract_address", "")).lower()
    # operator/internal: the matched "taker" owner is an exchange contract
    if taker_owner in KNOWN_EXCHANGE:
        return {"economic_role": "OPERATOR_OR_INTERNAL_LEG",
                "takerordermaker": taker_owner, "confirmed_by": "exchange_taker"}
    # ECONOMIC_TAKER: our wallet owns the taker (aggressor) order — DIRECT
    wallet_is_taker = taker_owner in wallets
    if wallet_is_taker:
        return {"economic_role": "ECONOMIC_TAKER_CONFIRMED",
                "takerordermaker": taker_owner, "confirmed_by": "takerordermaker"}
    # otherwise, our wallet may be a MAKER — but ONLY if positively paired.
    # require an OrderFilled leg in the same tx where our wallet is the event
    # maker (topic2) AND not the taker owner. Never by exclusion.
    if of_legs:
        # normalize the OM asset ids once (raises DataExportPrecisionLoss if the
        # CSV still has scientific notation -> caller surfaces it loudly)
        om_ids = set()
        for k in ("makerassetid", "takerassetid"):
            ci = canonical_int(om_row.get(k))
            if ci is not None:
                om_ids.add(ci)
        for f in of_legs:
            if f["maker"] in wallets and f["maker"] != taker_owner:
                of_ids = {canonical_int(f["maker_asset_id"]),
                          canonical_int(f["taker_asset_id"])} - {None}
                same_asset = bool(of_ids & om_ids)
                if same_asset:
                    return {"economic_role": "ECONOMIC_MAKER_CONFIRMED",
                            "takerordermaker": taker_owner,
                            "confirmed_by": "paired_orderfilled_maker_leg",
                            "maker_leg_log_index": f["log_index"]}
        # wallet appears in tx but not positively confirmable as maker here
        wallet_in_any = any(f["maker"] in wallets or f["taker"] in wallets
                            for f in of_legs)
        if wallet_in_any:
            return {"economic_role": "AMBIGUOUS",
                    "takerordermaker": taker_owner,
                    "confirmed_by": "wallet_in_tx_but_maker_side_unconfirmed"}
        return {"economic_role": "WALLET_NOT_IN_MATCH",
                "takerordermaker": taker_owner, "confirmed_by": "not_in_legs"}
    # no OrderFilled legs available to confirm maker side
    return {"economic_role": "NEED_PAIRING",
            "takerordermaker": taker_owner,
            "confirmed_by": "no_orderfilled_legs_available"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--dune-csv", default=None,
                    help="Dune OrdersMatched export (phase 2). If absent, phase 1 "
                         "writes the tx-list + query and exits.")
    ap.add_argument("--orderfilled-csv", default=None,
                    help="optional prior OrderFilled decode CSV for maker-side "
                         "pairing (else --rpc-url fetches legs)")
    ap.add_argument("--rpc-url", default=None,
                    help="optional: fetch OrderFilled legs to confirm maker side")
    ap.add_argument("--n-tx", type=int, default=18)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    store = Store(args.root)
    trades = store.load_trades()
    t = trades[trades["tx_hash"].astype(str).str.startswith("0x")].copy()

    # ----- sample: prefer tx known to have wallet-involved OrderFilled logs --
    per_tx = t.groupby("tx_hash").size()
    import numpy as np
    rng = np.random.default_rng(args.seed)
    multi = list(per_tx[per_tx > 1].index)
    single = list(per_tx[per_tx == 1].index)
    n_multi = min(len(multi), max(2, args.n_tx // 2))
    n_single = min(len(single), args.n_tx - n_multi)
    pick = (list(rng.choice(multi, n_multi, replace=False)) if multi else []) + \
           (list(rng.choice(single, n_single, replace=False)) if single else [])
    samp = t[t["tx_hash"].isin(pick)]

    # ----- PHASE 1: no Dune CSV yet -> emit tx-list + query and stop ---------
    if not args.dune_csv:
        tx_list = write_phase1(samp, out_dir)
        print("=" * 64)
        print("PHASE 1 — OrdersMatched tx-list + Dune query emitted")
        print("=" * 64)
        print(f"  sampled {len(tx_list)} tx")
        print(f"  -> {out_dir}/ordersmatched_dune_tx_list.txt")
        print(f"  -> {out_dir}/ordersmatched_dune_query.sql")
        print("  Run the .sql on Dune, export CSV, then re-run with --dune-csv.")
        return 0

    # ----- PHASE 2: ingest Dune OrdersMatched CSV ---------------------------
    dune = _read_csv_tolerant(args.dune_csv)
    dune.columns = [c.lower() for c in dune.columns]
    dune["evt_tx_hash"] = dune["evt_tx_hash"].astype(str).str.lower()

    # OrderFilled legs for maker-side pairing (optional but needed to CONFIRM
    # maker side rather than infer by exclusion)
    of_by_tx = {}
    sampled_tx = set(samp["tx_hash"].str.lower())
    dune_tx = set(dune["evt_tx_hash"])
    target_tx = sorted(sampled_tx & dune_tx)
    if args.orderfilled_csv and pathlib.Path(args.orderfilled_csv).exists():
        ofc = pd.read_csv(args.orderfilled_csv)
        ofc["tx_hash"] = ofc["tx_hash"].astype(str).str.lower()
        for tx, g in ofc.groupby("tx_hash"):
            of_by_tx[tx] = [
                {"maker": str(r["maker"]).lower(), "taker": str(r["taker"]).lower(),
                 "maker_asset_id": r.get("makerAmountFilled"),  # placeholder
                 "taker_asset_id": None, "log_index": r.get("log_index")}
                for _, r in g.iterrows()]
    elif args.rpc_url:
        topic = _ofj.resolve_topic0()
        if topic.get("method") != "NO_KECCAK_LIB":
            import requests
            sess = requests.Session()
            for i, tx in enumerate(target_tx, 1):
                try:
                    rcpt = _ofj.fetch_receipt(args.rpc_url, tx, session=sess)
                except _ofj.RpcLimited:
                    print("  RPC limited during leg fetch; continuing with partial")
                    break
                legs = []
                for lg in (rcpt or {}).get("logs", []):
                    d = _ofj.decode_orderfilled(lg)
                    if d:
                        legs.append(d)
                of_by_tx[tx] = legs
                time.sleep(args.sleep)

    # classify per OrdersMatched row
    rows = []
    precision_loss = 0
    for _, om in dune.iterrows():
        tx = om["evt_tx_hash"]
        wallets = set(str(w).lower() for w in samp[samp["tx_hash"].str.lower() == tx]["wallet"])
        legs = of_by_tx.get(tx)
        try:
            res = classify_trade(om.to_dict(), wallets, legs)
        except DataExportPrecisionLoss as e:
            precision_loss += 1
            res = {"economic_role": "UNDECODED_OR_UNMATCHED",
                   "takerordermaker": str(om.get("takerordermaker", "")).lower(),
                   "confirmed_by": f"DATA_EXPORT_PRECISION_LOSS: {e}"}
        rows.append({
            "tx_hash": tx, "evt_index": om.get("evt_index"),
            "src": om.get("src"), "contract_address": om.get("contract_address"),
            "takerordermaker": res["takerordermaker"],
            "economic_role": res["economic_role"],
            "confirmed_by": res["confirmed_by"],
            "monitored_wallets": "|".join(sorted(wallets)),
        })
    rj = pd.DataFrame(rows)
    if precision_loss:
        print(f"  !! DATA_EXPORT_PRECISION_LOSS on {precision_loss} rows — the "
              f"CSV still has scientific-notation asset ids. Re-export the Dune "
              f"query with cast(... as varchar).")

    n = len(rj)
    def cnt(role): return int((rj["economic_role"] == role).sum()) if n else 0
    taker_c = cnt("ECONOMIC_TAKER_CONFIRMED")
    maker_c = cnt("ECONOMIC_MAKER_CONFIRMED")
    not_in = cnt("WALLET_NOT_IN_MATCH")
    ambig = cnt("AMBIGUOUS")
    operator = cnt("OPERATOR_OR_INTERNAL_LEG")
    need_pair = cnt("NEED_PAIRING")
    confirmed = taker_c + maker_c
    wallet_involved = confirmed + ambig + need_pair  # excludes not-in / operator
    role_recoverable_rate = (confirmed / wallet_involved) if wallet_involved else 0.0
    ambiguity_rate = (ambig / wallet_involved) if wallet_involved else 0.0

    # ----- gate -------------------------------------------------------------
    tables = sorted(rj["src"].dropna().unique().tolist())
    if n == 0:
        label = "ORDERSMATCHED_NOT_AVAILABLE"
    elif wallet_involved < 10:
        label = "NEED_MORE_SAMPLE"
    elif taker_c > 0 and maker_c == 0 and need_pair + ambig > 0:
        # taker side recoverable; maker side NOT confirmed (no/insufficient pairing)
        label = "NEED_ORDERFILLED_PAIRING_FOR_MAKER_SIDE"
    elif taker_c > 0 and maker_c > 0 and role_recoverable_rate >= 0.6 \
            and ambiguity_rate <= 0.3:
        # taker direct + maker confirmed by pairing (not exclusion) + enough + clean
        label = "ECONOMIC_ROLE_RECOVERABLE_VIA_ORDERSMATCHED"
    elif confirmed == 0:
        label = "ORDERSMATCHED_NOT_ENOUGH_FOR_ROLE"
    else:
        label = "INCONCLUSIVE"

    metrics = {
        "total_sampled_tx": len(set(samp["tx_hash"])),
        "ordersmatched_rows_returned": int(n),
        "tx_with_ordersmatched": int(rj["tx_hash"].nunique()) if n else 0,
        "ECONOMIC_TAKER_CONFIRMED": taker_c,
        "ECONOMIC_MAKER_CONFIRMED": maker_c,
        "WALLET_NOT_IN_MATCH": not_in,
        "AMBIGUOUS": ambig,
        "OPERATOR_OR_INTERNAL_LEG": operator,
        "NEED_PAIRING": need_pair,
        "role_recoverable_rate": role_recoverable_rate,
        "ambiguity_rate": ambiguity_rate,
        "tables_represented": tables,
        "maker_side_pairing_available": bool(of_by_tx),
        "decision_label": label,
    }
    out = {**metrics, "guardrails": [
        "economic MAKER confirmed by pairing, never by exclusion",
        "OrdersMatched sourced from Dune (path B), not RPC self-decode",
        "no indexer, no log_index backfill, no PnL, no strategy claim, no trading"]}
    (out_dir / "ordersmatched_economic_role.json").write_text(
        json.dumps(out, indent=2, default=str))
    rj.to_csv(out_dir / "ordersmatched_economic_role.csv", index=False)
    _write_md(out, out_dir / "ordersmatched_economic_role_report.md")

    print("=" * 64)
    print("PHASE 2 — OrdersMatched ECONOMIC-ROLE CLASSIFICATION")
    print("=" * 64)
    print(f"  OrdersMatched rows: {n} | tx with OM: {metrics['tx_with_ordersmatched']}")
    print(f"  ECONOMIC_TAKER_CONFIRMED: {taker_c}")
    print(f"  ECONOMIC_MAKER_CONFIRMED: {maker_c} "
          f"(pairing available: {bool(of_by_tx)})")
    print(f"  AMBIGUOUS: {ambig} | NEED_PAIRING: {need_pair} | "
          f"WALLET_NOT_IN_MATCH: {not_in} | OPERATOR: {operator}")
    print(f"  role_recoverable_rate: {role_recoverable_rate:.3f} | "
          f"ambiguity_rate: {ambiguity_rate:.3f}")
    print(f"  tables: {tables}")
    print(f"  >>> DECISION LABEL: {label}")
    print(f"  wrote {out_dir}/ordersmatched_economic_role.json (+ report, csv)")
    return 0


def _write_md(out, path):
    L = ["# OrdersMatched Economic-Role Probe (Dune-sourced, research only)", "",
         f"**Decision label: `{out['decision_label']}`**", "",
         "## Metrics",
         f"- total sampled tx: {out['total_sampled_tx']}",
         f"- OrdersMatched rows returned: {out['ordersmatched_rows_returned']}",
         f"- tx with OrdersMatched: {out['tx_with_ordersmatched']}",
         f"- ECONOMIC_TAKER_CONFIRMED: {out['ECONOMIC_TAKER_CONFIRMED']}",
         f"- ECONOMIC_MAKER_CONFIRMED: {out['ECONOMIC_MAKER_CONFIRMED']}",
         f"- WALLET_NOT_IN_MATCH: {out['WALLET_NOT_IN_MATCH']}",
         f"- AMBIGUOUS: {out['AMBIGUOUS']}",
         f"- OPERATOR_OR_INTERNAL_LEG: {out['OPERATOR_OR_INTERNAL_LEG']}",
         f"- NEED_PAIRING (maker side unconfirmed): {out['NEED_PAIRING']}",
         f"- role_recoverable_rate: {out['role_recoverable_rate']:.3f}",
         f"- ambiguity_rate: {out['ambiguity_rate']:.3f}",
         f"- tables represented: {out['tables_represented']}",
         f"- maker-side pairing available: {out['maker_side_pairing_available']}", "",
         "## Classification rules",
         "- `ECONOMIC_TAKER_CONFIRMED`: wallet == takerordermaker (direct).",
         "- `ECONOMIC_MAKER_CONFIRMED`: wallet positively present as the maker "
         "side of a paired OrderFilled leg (same tx + asset context), AND not the "
         "takerordermaker. NEVER by exclusion.",
         "- `OPERATOR_OR_INTERNAL_LEG`: takerordermaker is an exchange contract.",
         "- `AMBIGUOUS`: wallet in tx but maker side not positively confirmable.",
         "- `NEED_PAIRING`: no OrderFilled legs available to confirm maker side.",
         "- `WALLET_NOT_IN_MATCH`: wallet not present in the matched trade.", "",
         "## Guardrails"]
    L += [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
