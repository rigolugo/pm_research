"""Operator-filtered OrderFilled semantic pass (research only).

Topic order CONFIRMED (exact-index Dune match, both contracts):
  topic1=orderHash, topic2=maker, topic3=taker.

This pass classifies each decoded fill and reports the wallet's EVENT role
(event_maker / event_taker) on REAL-COUNTERPARTY fills only, after excluding
OPERATOR_LEG fills (taker == a known exchange/operator contract).

STRICT TERMINOLOGY: event_maker / event_taker / operator_leg /
real_counterparty_fill / ambiguous_fill. NOT passive/aggressive — event role is
NOT yet justified as economic passive/aggressive role.

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

# Known exchange/operator contracts (lowercased). A fill whose TAKER is one of
# these is an operator_leg (settlement side), not a real counterparty fill.
KNOWN_EXCHANGE_CONTRACTS = {
    "0x4bfb41d5b3570defd03c39a9a4d8de6bd8b8982e",   # old CTF Exchange
    "0xc5d563a36ae78145c45a50134d48a1215220f80a",   # old NegRisk Exchange
    "0xe111180000d2663c0091e4f400237545b87b996b",   # current CTF Exchange V2
    "0xe2222d279d744050d28e00520010520000310f59",   # current NegRisk CTF V2
}


def classify_fill(decoded: dict, wallets: set) -> dict:
    """Classify one decoded fill. event_maker=topic2, event_taker=topic3 (per
    confirmed topic order). fill_class = OPERATOR_LEG if taker is an exchange
    contract, else REAL_COUNTERPARTY_FILL. wallet_role from the wallet's side."""
    maker = decoded["maker"]
    taker = decoded["taker"]
    is_operator = taker in KNOWN_EXCHANGE_CONTRACTS
    fill_class = "OPERATOR_LEG" if is_operator else "REAL_COUNTERPARTY_FILL"
    if maker in wallets and taker in wallets:
        wallet_role = "AMBIGUOUS"           # wallet on both sides (shouldn't happen)
    elif maker in wallets:
        wallet_role = "EVENT_MAKER"
    elif taker in wallets:
        wallet_role = "EVENT_TAKER"
    else:
        wallet_role = "WALLET_NOT_IN_FILL"
    return {"fill_class": fill_class, "wallet_role": wallet_role,
            "event_maker": maker, "event_taker": taker,
            "is_operator_leg": is_operator}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--rpc-url", default=None)
    ap.add_argument("--logs-json", default=None)
    ap.add_argument("--n-tx", type=int, default=18)
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

    # token_id per trade for the tokenId/side columns (best-effort, per tx)
    rows = []
    contract_counts = {}
    multi_candidate_tx = 0
    for tx in pick:
        raw_logs = logs_by_tx.get(tx, [])
        trade_rows = t[t["tx_hash"] == tx]
        wallets = set(str(w).lower() for w in trade_rows["wallet"])
        # token_id / side from the trade row(s) for this tx (may be >1)
        tok_side = {}
        for _, tr in trade_rows.iterrows():
            tok_side.setdefault(str(tr.get("token_id", "")), (tr.get("side"),))
        decoded_fills = []
        for lg in raw_logs:
            if not lg.get("topics") or lg["topics"][0].lower() not in _ofj.KNOWN_TOPICS:
                continue
            d = _ofj.decode_orderfilled(lg)
            if d is None:
                continue
            decoded_fills.append(d)
            contract_counts[d["contract_address"]] = \
                contract_counts.get(d["contract_address"], 0) + 1
        # count tx that have multiple REAL-counterparty candidate logs touching
        # our wallets (the log_index-disambiguation risk)
        real_wallet_logs = [
            d for d in decoded_fills
            if d["taker"] not in KNOWN_EXCHANGE_CONTRACTS
            and (d["maker"] in wallets or d["taker"] in wallets)]
        if len(real_wallet_logs) > 1:
            multi_candidate_tx += 1
        for d in decoded_fills:
            c = classify_fill(d, wallets)
            # match a token_id/side from trade rows where the fill's asset matches
            tok = None
            for k in tok_side:
                if k and (k == str(d["maker_asset_id"]) or k == str(d["taker_asset_id"])):
                    tok = k; break
            rows.append({
                "tx_hash": tx, "log_index": d["log_index"],
                "emitting_contract": d["contract_address"],
                "orderHash": d["order_hash"],
                "maker": d["maker"], "taker": d["taker"],
                "tokenId": tok, "side": (tok_side.get(tok, (None,))[0] if tok else None),
                "makerAmountFilled": d["maker_amount_filled"],
                "takerAmountFilled": d["taker_amount_filled"],
                "wallet": "|".join(sorted(wallets)),
                "wallet_role": c["wallet_role"],
                "fill_class": c["fill_class"],
            })
    rj = pd.DataFrame(rows)

    # --- metrics ---
    total = int(len(rj))
    operator = rj[rj["fill_class"] == "OPERATOR_LEG"]
    real = rj[rj["fill_class"] == "REAL_COUNTERPARTY_FILL"]
    # role distribution EXCLUDING operator legs, and only where wallet is in fill
    real_wallet = real[real["wallet_role"].isin(["EVENT_MAKER", "EVENT_TAKER"])]
    w_maker = int((real_wallet["wallet_role"] == "EVENT_MAKER").sum())
    w_taker = int((real_wallet["wallet_role"] == "EVENT_TAKER").sum())
    ambiguous = int((rj["wallet_role"] == "AMBIGUOUS").sum())

    metrics = {
        "total_decoded_fills": total,
        "operator_leg_count": int(len(operator)),
        "real_counterparty_fill_count": int(len(real)),
        "wallet_as_event_maker_count": w_maker,
        "wallet_as_event_taker_count": w_taker,
        "wallet_role_distribution_excluding_operator_legs": {
            "EVENT_MAKER": w_maker, "EVENT_TAKER": w_taker,
            "total_wallet_involving_real_fills": w_maker + w_taker},
        "ambiguous_fill_count": ambiguous,
        "tx_with_multiple_candidate_logs_count": multi_candidate_tx,
        "emitting_contract_counts": contract_counts,
        "topic_order": "topic1=orderHash, topic2=maker, topic3=taker (confirmed)",
    }

    # --- decision label (per the specified rules) ---
    wallet_real = w_maker + w_taker
    both_roles = w_maker > 0 and w_taker > 0
    # of tx that have any real wallet fill, how many are multi-candidate (ambiguous)?
    if total == 0:
        label = "INCONCLUSIVE"
    elif wallet_real == 0:
        # nearly all wallet-involving fills are operator legs
        label = "ORDERFILLED_WRONG_INSTRUMENT"
    elif both_roles and multi_candidate_tx > 0 and \
            multi_candidate_tx >= max(1, len(pick) // 2):
        label = "NEED_LOG_INDEX_DISAMBIGUATION"
    elif both_roles:
        # event role recoverable, but passive/aggressive NOT proven
        label = "EVENT_ROLE_RECOVERABLE_BUT_PASSIVE_AGGRESSIVE_UNPROVEN"
    else:
        label = "INCONCLUSIVE"
    metrics["decision_label"] = label

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    out = {**metrics, "guardrails": [
        "event_maker/event_taker terminology — NOT passive/aggressive",
        "operator legs classified and reported, not silently dropped",
        "no indexer, no log_index backfill, no trading, no strategy claim"]}
    (out_dir / "orderfilled_operator_filtered_semantic.json").write_text(
        json.dumps(out, indent=2, default=str))
    rj.to_csv(out_dir / "orderfilled_operator_filtered_semantic.csv", index=False)
    _write_md(out, out_dir / "orderfilled_operator_filtered_semantic.md")

    print("=" * 64)
    print("OPERATOR-FILTERED SEMANTIC PASS (research only)")
    print("=" * 64)
    print(f"  total decoded fills: {total}")
    print(f"  operator_leg: {len(operator)} | real_counterparty: {len(real)}")
    print(f"  wallet EVENT_MAKER: {w_maker} | EVENT_TAKER: {w_taker} "
          f"(operator legs excluded)")
    print(f"  ambiguous: {ambiguous} | "
          f"tx w/ multiple candidate logs: {multi_candidate_tx}")
    print(f"  contracts: {list(contract_counts.keys())}")
    print(f"  >>> DECISION LABEL: {label}")
    print(f"  wrote {out_dir}/orderfilled_operator_filtered_semantic.json (+ md, csv)")
    return 0


def _write_md(out, path):
    L = ["# Operator-Filtered OrderFilled Semantic Pass (research only)", "",
         f"**Decision label: `{out['decision_label']}`**", "",
         "Topic order confirmed: `topic1=orderHash, topic2=maker, topic3=taker` "
         "(exact-index Dune match, both contracts).", "",
         "## Metrics",
         f"- total decoded fills: {out['total_decoded_fills']}",
         f"- operator_leg_count: {out['operator_leg_count']}",
         f"- real_counterparty_fill_count: {out['real_counterparty_fill_count']}",
         f"- wallet_as_event_maker_count: {out['wallet_as_event_maker_count']}",
         f"- wallet_as_event_taker_count: {out['wallet_as_event_taker_count']}",
         f"- ambiguous_fill_count: {out['ambiguous_fill_count']}",
         f"- tx_with_multiple_candidate_logs_count: "
         f"{out['tx_with_multiple_candidate_logs_count']}", "",
         "## Wallet role distribution (operator legs EXCLUDED)",
         f"- EVENT_MAKER: {out['wallet_as_event_maker_count']}",
         f"- EVENT_TAKER: {out['wallet_as_event_taker_count']}", "",
         "## Terminology guard",
         "- `event_maker`/`event_taker` are the OrderFilled event roles. They "
         "are NOT claimed to be economic passive/aggressive roles — that needs "
         "order-book / OrdersMatched context not present here.", "",
         "## Label meaning"]
    meanings = {
        "EVENT_ROLE_RECOVERABLE_BUT_PASSIVE_AGGRESSIVE_UNPROVEN":
            "Real-counterparty fills remain after operator filtering, and wallets "
            "appear as BOTH event_maker and event_taker. Event role is recoverable; "
            "economic passive/aggressive interpretation is NOT yet proven.",
        "NEED_LOG_INDEX_DISAMBIGUATION":
            "Real-counterparty fills remain but most tx have multiple candidate "
            "logs touching our wallets; without per-trade log_index, role can't be "
            "pinned per trade.",
        "ORDERFILLED_WRONG_INSTRUMENT":
            "Nearly all wallet-involving fills are operator legs; OrderFilled does "
            "not carry usable counterparty role for these wallets.",
        "ECONOMIC_ROLE_RECOVERABLE_FROM_EVENTS":
            "Event role cleanly recoverable AND order semantics justify event "
            "maker/taker as economic maker/taker.",
        "INCONCLUSIVE": "Insufficient evidence; widen the sample.",
    }
    L.append(meanings.get(out["decision_label"], ""))
    L += ["", "## Guardrails"] + [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
