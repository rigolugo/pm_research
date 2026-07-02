"""Expanded OrdersMatched economic-role probe (research only).

Stabilizes the economic-role distribution on a larger STRATIFIED sample
(default 150 tx across wallets, time periods, and single- vs multi-fill tx).
Reuses the VALIDATED machinery unchanged: classify_trade (taker via
takerordermaker; maker only by positive OrderFilled pairing, never exclusion),
canonical_int asset matching, and the Dune-API CSV path with varchar casts.

Adds breakdowns: role distribution by wallet, by contract, by time bucket, and
single- vs multi-fill. Labels the distribution's stability/shape.

No PnL. No log_index. No indexer. No strategy claim. No trading.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import time

import pandas as pd

from pm_research.data.store import Store

_om_spec = importlib.util.spec_from_file_location(
    "ordersmatched_economic_role",
    str(pathlib.Path(__file__).resolve().parent / "ordersmatched_economic_role.py"))
_om = importlib.util.module_from_spec(_om_spec)
_om_spec.loader.exec_module(_om)
_ofj = _om._ofj

MIN_COVERAGE_WALLETS = 5         # need role data across >= this many wallets
MIN_TRADES_FOR_STABLE = 60       # need >= this many classified trades to call stable


def stratified_sample(t: pd.DataFrame, n_tx: int, seed: int) -> pd.DataFrame:
    """Stratify tx across wallet, time bucket, and fill-multiplicity.

    Allocates the tx budget across (wallet x time-quartile) cells, drawing a mix
    of single-fill and multi-fill tx within each cell where available."""
    import numpy as np
    rng = np.random.default_rng(seed)
    t = t.copy()
    t["traded_at"] = pd.to_datetime(t["traded_at"], utc=True, errors="coerce")
    # time buckets = quartiles of trade time
    try:
        t["time_bucket"] = pd.qcut(t["traded_at"].astype("int64"), 4,
                                   labels=["q1", "q2", "q3", "q4"], duplicates="drop")
    except (ValueError, TypeError):
        t["time_bucket"] = "q1"
    per_tx = t.groupby("tx_hash").size()
    multi_set = set(per_tx[per_tx > 1].index)
    # build per-tx frame with strata keys (first wallet/time/bucket per tx)
    tx_meta = (t.groupby("tx_hash")
               .agg(wallet=("wallet", "first"),
                    time_bucket=("time_bucket", "first")).reset_index())
    tx_meta["is_multi"] = tx_meta["tx_hash"].isin(multi_set)
    wallets = tx_meta["wallet"].unique().tolist()
    buckets = ["q1", "q2", "q3", "q4"]
    picked = []
    # round-robin across wallet x bucket cells, alternating multi/single
    cells = [(w, b) for w in wallets for b in buckets]
    rng.shuffle(cells)
    per_cell = max(1, n_tx // max(1, len(cells)))
    prefer_multi = True
    for (w, b) in cells:
        if len(picked) >= n_tx:
            break
        cell = tx_meta[(tx_meta["wallet"] == w) & (tx_meta["time_bucket"] == b)]
        if len(cell) == 0:
            continue
        pool_multi = cell[cell["is_multi"]]["tx_hash"].tolist()
        pool_single = cell[~cell["is_multi"]]["tx_hash"].tolist()
        order = ([pool_multi, pool_single] if prefer_multi
                 else [pool_single, pool_multi])
        prefer_multi = not prefer_multi
        take = []
        for pool in order:
            avail = [x for x in pool if x not in picked]
            if avail:
                k = min(per_cell - len(take), len(avail))
                take += list(rng.choice(avail, k, replace=False))
            if len(take) >= per_cell:
                break
        picked += take
    # top up randomly if under budget
    if len(picked) < n_tx:
        rest = [x for x in tx_meta["tx_hash"].tolist() if x not in picked]
        if rest:
            k = min(n_tx - len(picked), len(rest))
            picked += list(rng.choice(rest, k, replace=False))
    picked = list(dict.fromkeys(picked))[:n_tx]
    return t[t["tx_hash"].isin(picked)], multi_set


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--dune-csv", default=None)
    ap.add_argument("--rpc-url", default=None)
    ap.add_argument("--n-tx", type=int, default=150)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    store = Store(args.root)
    trades = store.load_trades()
    t = trades[trades["tx_hash"].astype(str).str.startswith("0x")].copy()
    t["tx_hash"] = t["tx_hash"].astype(str)
    samp, multi_set = stratified_sample(t, args.n_tx, args.seed)

    # ---- PHASE 1: emit tx-list + query ------------------------------------
    if not args.dune_csv:
        tx_list = list(dict.fromkeys(samp["tx_hash"].tolist()))
        (out_dir / "ordersmatched_expanded_dune_tx_list.txt").write_text(
            "\n".join(tx_list))
        txlist_sql = ",\n".join(f"  {tx}" for tx in tx_list)
        (out_dir / "ordersmatched_expanded_dune_query.sql").write_text(
            _om.DUNE_QUERY_TEMPLATE.replace("{TXLIST}", txlist_sql))
        print("=" * 64)
        print(f"PHASE 1 (expanded) — {len(tx_list)} stratified tx emitted")
        print("=" * 64)
        print(f"  wallets covered: {samp['wallet'].nunique()} | "
              f"time buckets: {samp['time_bucket'].nunique()}")
        print(f"  -> {out_dir}/ordersmatched_expanded_dune_query.sql")
        print(f"  -> {out_dir}/ordersmatched_expanded_dune_tx_list.txt")
        print("  Run on Dune (API CSV path), then re-run with --dune-csv.")
        return 0

    # ---- PHASE 2: classify -------------------------------------------------
    dune = _om._read_csv_tolerant(args.dune_csv)
    dune.columns = [c.lower() for c in dune.columns]
    dune["evt_tx_hash"] = dune["evt_tx_hash"].astype(str).str.lower()

    # OrderFilled legs for maker-side pairing
    of_by_tx = {}
    sampled = set(samp["tx_hash"].str.lower())
    target = sorted(sampled & set(dune["evt_tx_hash"]))
    if args.rpc_url:
        topic = _ofj.resolve_topic0()
        if topic.get("method") != "NO_KECCAK_LIB":
            import requests
            sess = requests.Session()
            for i, tx in enumerate(target, 1):
                try:
                    rcpt = _ofj.fetch_receipt(args.rpc_url, tx, session=sess)
                except _ofj.RpcLimited:
                    print(f"  RPC limited at {i}/{len(target)}; partial pairing")
                    break
                of_by_tx[tx] = [d for lg in (rcpt or {}).get("logs", [])
                                if (d := _ofj.decode_orderfilled(lg))]
                if i % 25 == 0:
                    print(f"  legs {i}/{len(target)}")
                time.sleep(args.sleep)

    # time bucket per tx for breakdown
    tb_by_tx = dict(zip(samp["tx_hash"].str.lower(), samp["time_bucket"].astype(str)))
    rows = []
    precision_loss = 0
    for _, om in dune.iterrows():
        tx = om["evt_tx_hash"]
        wallets = set(str(w).lower()
                      for w in samp[samp["tx_hash"].str.lower() == tx]["wallet"])
        legs = of_by_tx.get(tx)
        try:
            res = _om.classify_trade(om.to_dict(), wallets, legs)
        except _om.DataExportPrecisionLoss as e:
            precision_loss += 1
            res = {"economic_role": "UNDECODED_OR_UNMATCHED",
                   "takerordermaker": str(om.get("takerordermaker", "")).lower(),
                   "confirmed_by": f"PRECISION_LOSS:{e}"}
        # which monitored wallet is implicated (for per-wallet breakdown)
        tom = str(om.get("takerordermaker", "")).lower()
        impl_wallet = tom if tom in wallets else (
            "|".join(sorted(wallets)) if wallets else "")
        rows.append({
            "tx_hash": tx, "evt_index": om.get("evt_index"), "src": om.get("src"),
            "contract_address": str(om.get("contract_address", "")).lower(),
            "economic_role": res["economic_role"],
            "implicated_wallet": impl_wallet,
            "time_bucket": tb_by_tx.get(tx, "?"),
            "is_multi_fill": tx in {m.lower() for m in multi_set},
        })
    rj = pd.DataFrame(rows)
    if precision_loss:
        print(f"  !! DATA_EXPORT_PRECISION_LOSS on {precision_loss} rows — re-export "
              f"with cast(... as varchar) / use the Dune API CSV path.")

    n = len(rj)
    def cnt(r): return int((rj["economic_role"] == r).sum()) if n else 0
    taker = cnt("ECONOMIC_TAKER_CONFIRMED")
    maker = cnt("ECONOMIC_MAKER_CONFIRMED")
    not_in = cnt("WALLET_NOT_IN_MATCH")
    ambig = cnt("AMBIGUOUS")
    operator = cnt("OPERATOR_OR_INTERNAL_LEG")
    confirmed = taker + maker
    wallet_involved = confirmed + ambig
    role_recoverable_rate = confirmed / wallet_involved if wallet_involved else 0.0
    ambiguity_rate = ambig / wallet_involved if wallet_involved else 0.0
    taker_share = taker / confirmed if confirmed else 0.0
    maker_share = maker / confirmed if confirmed else 0.0

    def dist_by(col):
        out = {}
        sub = rj[rj["economic_role"].isin(
            ["ECONOMIC_TAKER_CONFIRMED", "ECONOMIC_MAKER_CONFIRMED"])]
        for key, g in sub.groupby(col):
            tk = int((g["economic_role"] == "ECONOMIC_TAKER_CONFIRMED").sum())
            mk = int((g["economic_role"] == "ECONOMIC_MAKER_CONFIRMED").sum())
            tot = tk + mk
            out[str(key)] = {"taker": tk, "maker": mk, "n": tot,
                             "taker_share": tk / tot if tot else None}
        return out

    role_by_wallet = dist_by("implicated_wallet")
    role_by_contract = dist_by("contract_address")
    role_by_time = dist_by("time_bucket")
    role_by_fill = dist_by("is_multi_fill")
    wallets_covered = len([w for w in role_by_wallet
                           if role_by_wallet[w]["n"] > 0])

    # ---- label -------------------------------------------------------------
    if n == 0:
        label = "NEED_MORE_SAMPLE"
    elif precision_loss > 0:
        label = "BLOCKED_BY_PAIRING_FAILURE"
    elif ambiguity_rate > 0.3:
        label = "BLOCKED_BY_AMBIGUITY"
    elif confirmed < MIN_TRADES_FOR_STABLE or wallets_covered < MIN_COVERAGE_WALLETS:
        label = "NEED_MORE_SAMPLE"
    elif taker_share >= 0.65:
        label = "ROLE_DISTRIBUTION_STABLE_TAKER_HEAVY"
    elif maker_share >= 0.65:
        label = "ROLE_DISTRIBUTION_STABLE_MAKER_HEAVY"
    else:
        label = "ROLE_DISTRIBUTION_STABLE_MIXED"

    metrics = {
        "total_sampled_tx": int(samp["tx_hash"].nunique()),
        "ordersmatched_rows_returned": int(n),
        "tx_with_ordersmatched": int(rj["tx_hash"].nunique()) if n else 0,
        "ECONOMIC_TAKER_CONFIRMED": taker, "ECONOMIC_MAKER_CONFIRMED": maker,
        "WALLET_NOT_IN_MATCH": not_in, "AMBIGUOUS": ambig,
        "OPERATOR_OR_INTERNAL_LEG": operator,
        "role_recoverable_rate": role_recoverable_rate,
        "ambiguity_rate": ambiguity_rate,
        "taker_share": taker_share, "maker_share": maker_share,
        "wallets_covered": wallets_covered,
        "role_distribution_by_wallet": role_by_wallet,
        "role_distribution_by_contract": role_by_contract,
        "role_distribution_by_time_bucket": role_by_time,
        "single_fill_vs_multi_fill_role_distribution": role_by_fill,
        "decision_label": label,
    }
    out = {**metrics, "guardrails": [
        "distribution NOT a finding unless coverage broad across wallets/time",
        "maker confirmed by pairing, never exclusion; canonical-int asset match",
        "no PnL, no log_index, no indexer, no strategy claim, no trading"]}
    (out_dir / "ordersmatched_economic_role_expanded.json").write_text(
        json.dumps(out, indent=2, default=str))
    rj.to_csv(out_dir / "ordersmatched_economic_role_expanded.csv", index=False)
    _write_md(out, out_dir / "ordersmatched_economic_role_expanded.md")

    print("=" * 64)
    print("EXPANDED OrdersMatched ECONOMIC-ROLE (research only)")
    print("=" * 64)
    print(f"  sampled tx: {metrics['total_sampled_tx']} | OM rows: {n} | "
          f"wallets covered: {wallets_covered}")
    print(f"  ECONOMIC_TAKER: {taker} | ECONOMIC_MAKER: {maker} | "
          f"AMBIGUOUS: {ambig} | OPERATOR: {operator}")
    print(f"  taker_share: {taker_share:.3f} | maker_share: {maker_share:.3f}")
    print(f"  role_recoverable_rate: {role_recoverable_rate:.3f} | "
          f"ambiguity_rate: {ambiguity_rate:.3f}")
    print(f"  >>> DECISION LABEL: {label}")
    print(f"  wrote {out_dir}/ordersmatched_economic_role_expanded.json (+ md, csv)")
    return 0


def _write_md(out, path):
    L = ["# Expanded OrdersMatched Economic-Role Distribution (research only)", "",
         f"**Decision label: `{out['decision_label']}`**", "",
         "## Headline",
         f"- sampled tx: {out['total_sampled_tx']} | OM rows: "
         f"{out['ordersmatched_rows_returned']} | wallets covered: "
         f"{out['wallets_covered']}",
         f"- ECONOMIC_TAKER: {out['ECONOMIC_TAKER_CONFIRMED']} | "
         f"ECONOMIC_MAKER: {out['ECONOMIC_MAKER_CONFIRMED']}",
         f"- taker_share: {out['taker_share']:.3f} | "
         f"maker_share: {out['maker_share']:.3f}",
         f"- role_recoverable_rate: {out['role_recoverable_rate']:.3f} | "
         f"ambiguity_rate: {out['ambiguity_rate']:.3f}", "",
         "## Role by wallet"]
    for w, d in out["role_distribution_by_wallet"].items():
        L.append(f"- {w[:16]}..: taker {d['taker']} / maker {d['maker']} "
                 f"(n={d['n']}, taker_share={d['taker_share']})")
    L += ["", "## Role by contract"]
    for c, d in out["role_distribution_by_contract"].items():
        L.append(f"- {c[:16]}..: taker {d['taker']} / maker {d['maker']} (n={d['n']})")
    L += ["", "## Role by time bucket"]
    for b, d in out["role_distribution_by_time_bucket"].items():
        L.append(f"- {b}: taker {d['taker']} / maker {d['maker']} (n={d['n']})")
    L += ["", "## Single vs multi-fill"]
    for f, d in out["single_fill_vs_multi_fill_role_distribution"].items():
        L.append(f"- multi={f}: taker {d['taker']} / maker {d['maker']} (n={d['n']})")
    L += ["", "## Interpretation rules",
          "- NOT a finding unless coverage is broad across wallets/time.",
          "- taker-heavy broadly -> liquidity-provider H1 weakens.",
          "- mixed/wallet-specific -> recommend per-wallet role analysis.",
          "- maker-heavy -> assess whether PnL-by-role is justified.", "",
          "## Guardrails"]
    L += [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
