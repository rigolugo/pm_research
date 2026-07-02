"""A0 — OrderFilled semantic-validation mini-pass (research only).

Question: can ECONOMIC passive/aggressive role be recovered from CTF Exchange V2
/ NegRisk Exchange OrderFilled events, order hashes, or paired logs — or is the
maker/taker field just order-owner/operator (the "wrong instrument")?

Method: take 10-20 representative tx (mix of single-fill and multi-fill), fully
decode EVERY OrderFilled log, dump all fields raw, pair the logs within each tx,
and compare maker/taker to the wallet on the matching trade row. Emit evidence,
not just a count. Proposes a decision label; a human + Dune cross-check confirm.

NOT an indexer. NO log_index backfill. NO trading. Reuses the sample-join
decoder so field semantics are identical.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time

import pandas as pd

from pm_research.data.store import Store

# reuse the decoder + RPC + topic resolution from the sample-join probe
import importlib.util
_ofj_spec = importlib.util.spec_from_file_location(
    "orderfilled_sample_join",
    str(pathlib.Path(__file__).resolve().parent / "orderfilled_sample_join.py"))
_ofj = importlib.util.module_from_spec(_ofj_spec)
_ofj_spec.loader.exec_module(_ofj)


def analyze_tx(tx, raw_logs, trade_rows) -> dict:
    """Fully decode the OrderFilled logs in one tx and assemble evidence about
    what maker/taker actually are."""
    fills = []
    for lg in raw_logs:
        d = _ofj.decode_orderfilled(lg)
        if d is not None:
            fills.append(d)
    # which addresses appear as maker vs taker across ALL fills in this tx?
    makers = [f["maker"] for f in fills]
    takers = [f["taker"] for f in fills]
    # the trade rows' wallets for this tx (our monitored wallets)
    wallets = sorted(set(str(w).lower() for w in trade_rows["wallet"]))
    # a repeated taker address across many fills in one tx is the tell of an
    # operator/matcher (one counterparty filling many resting orders)
    taker_counts = pd.Series(takers).value_counts().to_dict() if takers else {}
    maker_counts = pd.Series(makers).value_counts().to_dict() if makers else {}
    repeated_taker = max(taker_counts.values()) if taker_counts else 0
    distinct_makers = len(set(makers))
    # do our wallets appear as maker, taker, both, or neither?
    wallet_as_maker = sum(1 for f in fills if f["maker"] in wallets)
    wallet_as_taker = sum(1 for f in fills if f["taker"] in wallets)
    return {
        "tx_hash": tx,
        "n_orderfilled_logs": len(fills),
        "n_trade_rows": int(len(trade_rows)),
        "monitored_wallets_in_tx": wallets,
        "distinct_makers": distinct_makers,
        "distinct_takers": len(set(takers)),
        "max_repeated_taker_count": repeated_taker,
        "wallet_appears_as_maker": wallet_as_maker,
        "wallet_appears_as_taker": wallet_as_taker,
        "contracts": sorted(set(f["contract_address"] for f in fills)),
        # raw per-fill dump for human/Dune inspection
        "fills": [
            {"log_index": f["log_index"], "contract": f["contract_address"],
             "order_hash": f["order_hash"], "maker": f["maker"],
             "taker": f["taker"], "maker_asset_id": str(f["maker_asset_id"]),
             "taker_asset_id": str(f["taker_asset_id"]),
             "maker_amount": f["maker_amount_filled"],
             "taker_amount": f["taker_amount_filled"], "fee": f["fee"]}
            for f in fills],
    }


def propose_label(tx_analyses: list[dict]) -> tuple[str, dict]:
    """Propose a decision label from the assembled evidence. Conservative:
    only claims recoverability if the events actually distinguish roles."""
    if not tx_analyses:
        return "INCONCLUSIVE", {}
    total_fills = sum(a["n_orderfilled_logs"] for a in tx_analyses)
    if total_fills == 0:
        return "NEED_ABI_DISCOVERY", {"reason": "no OrderFilled logs decoded"}

    # Evidence 1: do monitored wallets EVER appear as taker?
    any_wallet_taker = any(a["wallet_appears_as_taker"] > 0 for a in tx_analyses)
    total_wallet_maker = sum(a["wallet_appears_as_maker"] for a in tx_analyses)
    total_wallet_taker = sum(a["wallet_appears_as_taker"] for a in tx_analyses)

    # Evidence 2: in multi-fill tx, is there ONE repeated taker (operator tell)?
    multi = [a for a in tx_analyses if a["n_orderfilled_logs"] > 1]
    operator_pattern = sum(
        1 for a in multi
        if a["max_repeated_taker_count"] >= max(2, a["n_orderfilled_logs"] - 1)
        and a["distinct_makers"] >= a["n_orderfilled_logs"] - 1)
    operator_tell = (len(multi) > 0 and operator_pattern >= max(1, len(multi) // 2))

    # Evidence 3: order_hash present? (could pair to an order book / CLOB lookup)
    has_order_hash = any(
        f["order_hash"] for a in tx_analyses for f in a["fills"])

    evidence = {
        "total_fills_decoded": total_fills,
        "wallet_as_maker_total": total_wallet_maker,
        "wallet_as_taker_total": total_wallet_taker,
        "any_wallet_appears_taker": any_wallet_taker,
        "multi_fill_tx": len(multi),
        "operator_pattern_tx": operator_pattern,
        "operator_tell": operator_tell,
        "order_hash_present": has_order_hash,
    }

    # Decision logic:
    # - if wallets appear ONLY as maker AND multi-fill tx show the one-repeated-
    #   taker operator pattern -> maker/taker is owner/operator -> WRONG INSTRUMENT
    # - if wallets appear as BOTH maker and taker across fills -> the field DOES
    #   carry directional role -> potentially RECOVERABLE
    # - if neither but order_hash present -> need CLOB/order data to resolve
    if total_wallet_maker > 0 and total_wallet_taker == 0 and operator_tell:
        label = "ORDERFILLED_WRONG_INSTRUMENT"
    elif total_wallet_maker > 0 and total_wallet_taker > 0:
        label = "ECONOMIC_ROLE_RECOVERABLE_FROM_EVENTS"
    elif has_order_hash and not any_wallet_taker:
        label = "NEED_ORDER_HASH_OR_CLOB_DATA"
    else:
        label = "INCONCLUSIVE"
    return label, evidence


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--rpc-url", default=None)
    ap.add_argument("--logs-json", default=None,
                    help="public-dataset fallback (e.g. Dune export) keyed by tx_hash")
    ap.add_argument("--n-tx", type=int, default=15)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.2)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    topic = _ofj.resolve_topic0()
    if topic.get("method") == "NO_KECCAK_LIB":
        out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "orderfilled_semantic_validation.json").write_text(json.dumps(
            {"decision_label": "NEED_ABI_DISCOVERY", "topic0": topic}, indent=2))
        print("NEED_ABI_DISCOVERY —", topic["warning"]); return 0

    store = Store(args.root)
    trades = store.load_trades()
    t = trades[trades["tx_hash"].astype(str).str.startswith("0x")].copy()
    per_tx = t.groupby("tx_hash").size()
    single = list(per_tx[per_tx == 1].index)
    multi = list(per_tx[per_tx > 1].index)
    import numpy as np
    rng = np.random.default_rng(args.seed)
    n_multi = min(len(multi), max(2, args.n_tx // 2))
    n_single = min(len(single), args.n_tx - n_multi)
    pick = (list(rng.choice(single, n_single, replace=False)) if single else []) + \
           (list(rng.choice(multi, n_multi, replace=False)) if multi else [])

    # fetch logs
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
                print("  RPC limited; stopping fetch early"); break
            print(f"  fetched {i}/{len(pick)}: {tx[:14]}.. "
                  f"({len(logs_by_tx.get(tx, []))} logs)")
            time.sleep(args.sleep)
    else:
        print("ERROR: provide --rpc-url or --logs-json"); return 2

    analyses = []
    for tx in pick:
        if tx not in logs_by_tx:
            continue
        rows = t[t["tx_hash"] == tx]
        analyses.append(analyze_tx(tx, logs_by_tx[tx], rows))

    label, evidence = propose_label(analyses)

    out = {
        "validation": "orderfilled_semantic_A0",
        "n_tx_analyzed": len(analyses),
        "topic0": topic,
        "known_contracts": _ofj.KNOWN_EXCHANGES,
        "decision_label": label,
        "evidence": evidence,
        "dune_crosscheck_table": "polymarket_polygon.ctfexchange_evt_orderfilled",
        "dune_crosscheck_note": (
            "cross-check decoded maker/taker/order_hash/amounts for these tx_hash "
            "against Dune's table; if Dune's maker/taker agree with this decode, "
            "the field semantics are confirmed (not a decode bug)."),
        "per_tx": analyses,
        "guardrails": ["semantic validation only", "no indexer",
                       "no log_index backfill", "no trading"],
    }
    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "orderfilled_semantic_validation.json").write_text(
        json.dumps(out, indent=2, default=str))
    # flat CSV: one row per decoded fill
    fill_rows = []
    for a in analyses:
        for f in a["fills"]:
            fill_rows.append({"tx_hash": a["tx_hash"], **f,
                              "monitored_wallets": "|".join(a["monitored_wallets_in_tx"]),
                              "wallet_is_maker": f["maker"] in a["monitored_wallets_in_tx"],
                              "wallet_is_taker": f["taker"] in a["monitored_wallets_in_tx"]})
    pd.DataFrame(fill_rows or [{"tx_hash": "(none)"}]).to_csv(
        out_dir / "orderfilled_semantic_validation.csv", index=False)
    _write_md(out, out_dir / "orderfilled_semantic_validation.md")

    print("=" * 64)
    print("A0 — OrderFilled SEMANTIC VALIDATION (research only)")
    print("=" * 64)
    print(f"  tx analyzed: {len(analyses)} | fills decoded: {evidence.get('total_fills_decoded', 0)}")
    print(f"  wallet-as-maker: {evidence.get('wallet_as_maker_total')} | "
          f"wallet-as-taker: {evidence.get('wallet_as_taker_total')}")
    print(f"  operator pattern in {evidence.get('operator_pattern_tx')}/"
          f"{evidence.get('multi_fill_tx')} multi-fill tx | "
          f"order_hash present: {evidence.get('order_hash_present')}")
    print(f"  >>> DECISION LABEL: {label}")
    print(f"  (cross-check tx against Dune ctfexchange_evt_orderfilled)")
    print(f"  wrote {out_dir}/orderfilled_semantic_validation.json (+ md, csv)")
    return 0


def _write_md(out, path):
    e = out["evidence"]
    L = ["# A0 — OrderFilled Semantic Validation (research only)", "",
         f"**Decision label: `{out['decision_label']}`**", "",
         f"- tx analyzed: {out['n_tx_analyzed']}",
         f"- total fills decoded: {e.get('total_fills_decoded', 0)}",
         f"- wallet appears as maker: {e.get('wallet_as_maker_total')}",
         f"- wallet appears as taker: {e.get('wallet_as_taker_total')}",
         f"- any wallet ever a taker: {e.get('any_wallet_appears_taker')}",
         f"- operator-pattern tx (one repeated taker + many distinct makers): "
         f"{e.get('operator_pattern_tx')}/{e.get('multi_fill_tx')}",
         f"- order_hash present in logs: {e.get('order_hash_present')}", "",
         "## What the label means", ""]
    meanings = {
        "ORDERFILLED_WRONG_INSTRUMENT":
            "wallets appear ONLY as maker, and multi-fill tx show one repeated "
            "taker against many distinct makers — i.e. taker = operator/matcher, "
            "maker = order owner. The field does NOT encode economic passive/"
            "aggressive role. Stop the OrderFilled-maker/taker branch.",
        "ECONOMIC_ROLE_RECOVERABLE_FROM_EVENTS":
            "wallets appear as BOTH maker and taker across fills — the field "
            "carries directional role. A minimal log_index/sample re-test is "
            "justified.",
        "NEED_ORDER_HASH_OR_CLOB_DATA":
            "role not separable from the event alone, but order_hash is present "
            "— pairing to CLOB/order data could resolve it.",
        "NEED_ABI_DISCOVERY": "no OrderFilled logs decoded; ABI/contract unresolved.",
        "INCONCLUSIVE": "evidence insufficient to decide; widen the sample.",
    }
    L.append(meanings.get(out["decision_label"], ""))
    L += ["", "## Dune cross-check",
          f"- table: `{out['dune_crosscheck_table']}`",
          f"- {out['dune_crosscheck_note']}", "",
          "## Recommendation by label", "",
          "- `ECONOMIC_ROLE_RECOVERABLE_FROM_EVENTS` -> minimal log_index/sample re-test.",
          "- `ORDERFILLED_WRONG_INSTRUMENT` -> stop this branch; choose: economic "
          "price-improvement proxy / yes_price rewrite (named-binary) / Phase-1 "
          "revalidation on corrected dataset.",
          "- `NEED_ORDER_HASH_OR_CLOB_DATA` -> investigate CLOB/order-hash lookup.",
          "", "## Guardrails"]
    L += [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
