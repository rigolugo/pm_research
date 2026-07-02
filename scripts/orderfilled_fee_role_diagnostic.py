"""Fee-field diagnostic — does the OrderFilled `fee` separate economic role?

Cheapest possible test before any log_index / OrdersMatched work: re-fetch (or
reuse) the decoded OrderFilled sample and analyze the `fee` field by event role.
If on real-counterparty fills the fee is consistently attached to one side
(e.g. event_taker pays, event_maker doesn't), then `fee` separates economic
role and event_maker/event_taker can be mapped to economic maker/taker.

STRICT terminology: event_maker / event_taker. "Economic role" claimed ONLY if
fee evidence supports it. No passive/aggressive wording otherwise.

No indexer. No log_index backfill. No trading. No strategy claim.
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
MIN_BUCKET = 20          # min fills per bucket to call a fee pattern meaningful


def _summary(series: pd.Series) -> dict:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) == 0:
        return {"n": 0, "nonzero_rate": None, "median": None, "mean": None}
    return {"n": int(len(s)),
            "nonzero_rate": float((s > 0).mean()),
            "median": float(s.median()), "mean": float(s.mean())}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--rpc-url", default=None)
    ap.add_argument("--logs-json", default=None)
    ap.add_argument("--n-tx", type=int, default=25)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    topic = _ofj.resolve_topic0()
    if topic.get("method") == "NO_KECCAK_LIB":
        print("NEED keccak lib:", topic["warning"]); return 0

    store = Store(args.root)
    trades = store.load_trades()
    t = trades[trades["tx_hash"].astype(str).str.startswith("0x")].copy()
    per_tx = t.groupby("tx_hash").size()
    import numpy as np
    rng = np.random.default_rng(args.seed)
    single = list(per_tx[per_tx == 1].index)
    multi = list(per_tx[per_tx > 1].index)
    n_multi = min(len(multi), max(2, args.n_tx // 2))
    n_single = min(len(single), args.n_tx - n_multi)
    pick = (list(rng.choice(single, n_single, replace=False)) if single else []) + \
           (list(rng.choice(multi, n_multi, replace=False)) if multi else [])

    logs_by_tx = {}
    if args.logs_json:
        logs_by_tx = json.loads(pathlib.Path(args.logs_json).read_text())
    elif args.rpc_url:
        import requests
        sess = requests.Session()
        for i, tx in enumerate(pick, 1):
            try:
                rcpt = _ofj.fetch_receipt(args.rpc_url, tx, session=sess)
                logs_by_tx[tx] = (rcpt or {}).get("logs", [])
            except _ofj.RpcLimited:
                print("  RPC limited; stopping early"); break
            print(f"  fetched {i}/{len(pick)}: {tx[:12]}.. "
                  f"({len(logs_by_tx.get(tx, []))} logs)")
            time.sleep(args.sleep)
    else:
        print("ERROR: provide --rpc-url or --logs-json"); return 2

    rows = []
    for tx in pick:
        raw_logs = logs_by_tx.get(tx, [])
        wallets = set(str(w).lower() for w in t[t["tx_hash"] == tx]["wallet"])
        side_by_tok = {}
        for _, tr in t[t["tx_hash"] == tx].iterrows():
            side_by_tok[str(tr.get("token_id", ""))] = tr.get("side")
        for lg in raw_logs:
            if not lg.get("topics") or lg["topics"][0].lower() not in _ofj.KNOWN_TOPICS:
                continue
            d = _ofj.decode_orderfilled(lg)
            if d is None:
                continue
            c = _op.classify_fill(d, wallets)
            tok = None
            for k in side_by_tok:
                if k and (k == str(d["maker_asset_id"]) or k == str(d["taker_asset_id"])):
                    tok = k; break
            rows.append({
                "tx_hash": tx, "log_index": d["log_index"],
                "emitting_contract": d["contract_address"],
                "fee": d["fee"],
                "maker": d["maker"], "taker": d["taker"],
                "tokenId": tok, "side": side_by_tok.get(tok),
                "wallet_event_role": c["wallet_role"],
                "fill_class": c["fill_class"],
            })
    rj = pd.DataFrame(rows)
    if len(rj) == 0:
        print("no fills decoded"); return 0

    real = rj[rj["fill_class"] == "REAL_COUNTERPARTY_FILL"]
    operator = rj[rj["fill_class"] == "OPERATOR_LEG"]

    # --- fee by event role (ALL fills, and real-counterparty only) ----------
    def by_role(df):
        return {role: _summary(df[df["wallet_event_role"] == role]["fee"])
                for role in ["EVENT_MAKER", "EVENT_TAKER",
                             "WALLET_NOT_IN_FILL", "AMBIGUOUS"]}

    # KEY ANALYSIS: on a real-counterparty fill, the event has ONE maker and ONE
    # taker. Compare fee attached to the maker-side vs taker-side across ALL real
    # fills (not just wallet's) — does fee consistently attach to taker?
    # The OrderFilled `fee` is a single per-event value; we can't split it per
    # side from one field. So we test: is fee nonzero, and does its presence
    # correlate with anything (contract/side)? A single fee field that is uniform
    # cannot separate maker vs taker within one event.
    metrics = {
        "total_fills": int(len(rj)),
        "real_counterparty_fills": int(len(real)),
        "operator_legs": int(len(operator)),
        "fee_summary_all": _summary(rj["fee"]),
        "fee_summary_real_counterparty": _summary(real["fee"]),
        "fee_summary_operator_legs": _summary(operator["fee"]),
        "fee_by_wallet_event_role_all": by_role(rj),
        "fee_by_wallet_event_role_real_only": by_role(real),
        "fee_by_contract": {
            c: _summary(g["fee"]) for c, g in rj.groupby("emitting_contract")},
        "fee_by_side": {
            str(s): _summary(g["fee"]) for s, g in rj.groupby("side", dropna=False)},
        "fee_nonzero_rate_real_counterparty_only":
            float((pd.to_numeric(real["fee"], errors="coerce") > 0).mean())
            if len(real) else None,
        "fee_nonzero_rate_operator_legs":
            float((pd.to_numeric(operator["fee"], errors="coerce") > 0).mean())
            if len(operator) else None,
    }

    # --- decision: does fee separate economic role? -------------------------
    # The OrderFilled event carries ONE fee value per fill, not a per-side fee.
    # So fee can separate economic role ONLY if its presence/magnitude differs
    # systematically by the wallet's event role on real fills AND there is enough
    # sample. Compare nonzero-rate event_maker vs event_taker on real fills.
    em = metrics["fee_by_wallet_event_role_real_only"]["EVENT_MAKER"]
    et = metrics["fee_by_wallet_event_role_real_only"]["EVENT_TAKER"]
    enough = (em["n"] >= MIN_BUCKET and et["n"] >= MIN_BUCKET)
    overall_fee_nonzero = metrics["fee_summary_all"]["nonzero_rate"]

    asymmetric = False
    if em["n"] and et["n"] and em["nonzero_rate"] is not None and et["nonzero_rate"] is not None:
        asymmetric = abs(em["nonzero_rate"] - et["nonzero_rate"]) >= 0.5

    if overall_fee_nonzero == 0.0:
        # fee is zero on every fill -> cannot separate anything
        label = "FEE_DOES_NOT_SEPARATE_ROLE"
        reason = "fee is zero on all decoded fills"
    elif not enough:
        label = "NEED_MORE_SAMPLE"
        reason = f"event_maker n={em['n']}, event_taker n={et['n']} (<{MIN_BUCKET})"
    elif asymmetric:
        label = "FEE_SEPARATES_ECONOMIC_ROLE"
        reason = (f"fee nonzero-rate event_maker={em['nonzero_rate']:.2f} vs "
                  f"event_taker={et['nonzero_rate']:.2f} (asymmetric)")
    else:
        # fee exists but does not differ by event role -> single-field fee can't
        # separate economic maker/taker
        label = "FEE_DOES_NOT_SEPARATE_ROLE"
        reason = ("fee present but symmetric across event_maker/event_taker; a "
                  "single per-event fee value does not separate economic role")
    metrics["decision_label"] = label
    metrics["decision_reason"] = reason
    metrics["fee_is_asymmetric_by_event_role"] = asymmetric

    out = {**metrics, "guardrails": [
        "event_maker/event_taker terminology — economic role claimed ONLY if "
        "fee evidence supports it",
        "no indexer, no log_index backfill, no trading, no strategy claim"]}
    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "orderfilled_fee_role_diagnostic.json").write_text(
        json.dumps(out, indent=2, default=str))
    rj.to_csv(out_dir / "orderfilled_fee_role_diagnostic.csv", index=False)
    _write_md(out, out_dir / "orderfilled_fee_role_diagnostic.md")

    print("=" * 64)
    print("FEE-FIELD ROLE DIAGNOSTIC (research only)")
    print("=" * 64)
    print(f"  total fills: {metrics['total_fills']} | real: {len(real)} | "
          f"operator: {len(operator)}")
    print(f"  fee nonzero-rate ALL: {overall_fee_nonzero}")
    print(f"  fee nonzero-rate real-counterparty: "
          f"{metrics['fee_nonzero_rate_real_counterparty_only']}")
    print(f"  event_maker fee: n={em['n']} nonzero={em['nonzero_rate']} "
          f"median={em['median']}")
    print(f"  event_taker fee: n={et['n']} nonzero={et['nonzero_rate']} "
          f"median={et['median']}")
    print(f"  asymmetric by event role: {asymmetric}")
    print(f"  >>> DECISION LABEL: {label}")
    print(f"  reason: {reason}")
    print(f"  wrote {out_dir}/orderfilled_fee_role_diagnostic.json (+ md, csv)")
    return 0


def _write_md(out, path):
    L = ["# Fee-Field Role Diagnostic (research only)", "",
         f"**Decision label: `{out['decision_label']}`**",
         f"reason: {out['decision_reason']}", "",
         "## Fee summary",
         f"- all fills: {out['fee_summary_all']}",
         f"- real-counterparty: {out['fee_summary_real_counterparty']}",
         f"- operator legs: {out['fee_summary_operator_legs']}", "",
         "## Fee by wallet event role (real-counterparty only)",
         f"- EVENT_MAKER: {out['fee_by_wallet_event_role_real_only']['EVENT_MAKER']}",
         f"- EVENT_TAKER: {out['fee_by_wallet_event_role_real_only']['EVENT_TAKER']}",
         "",
         "## Interpretation",
         "- The OrderFilled event carries ONE `fee` value per fill, not a per-side "
         "fee. It can separate economic role only if its presence/magnitude differs "
         "systematically by the wallet's event role on real fills.",
         "- `event_maker`/`event_taker` are event roles; economic maker/taker is "
         "claimed ONLY under FEE_SEPARATES_ECONOMIC_ROLE.", "",
         "## Guardrails"]
    L += [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
