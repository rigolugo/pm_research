"""Strict OrderFilled topic-order validation (research only, NO assumptions).

Prior error: a topic-order "fix" was based on comparing local log_index 1227 to
Dune evt_index 1229 — DIFFERENT logs in a multi-fill tx. Invalid. This script
makes NO global topic-order assumption. It dumps, per EXACT (tx_hash, contract,
log_index): raw topics[0:4], both candidate decodings (A: topic2=maker/topic3=
taker ; B: topic2=taker/topic3=maker), and the monitored wallet — so the correct
order is READ OFF the data per contract, cross-checked against the matching Dune
evt_index (same log_index), not a neighboring one.

Handles each emitting contract SEPARATELY. Does not assume V2 ABI applies to
older/unknown contracts. NO indexer, NO log_index backfill, NO redirect.
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

# Canonical current contracts (per Copilot / Polymarket docs), lowercased.
CONTRACT_LABELS = {
    "0xe111180000d2663c0091e4f400237545b87b996b": "CTF_Exchange_V2",
    "0xe2222d279d744050d28e00520010520000310f59": "NegRisk_CTF_Exchange_V2",
    # older/unknown emitters observed in our sample — DO NOT assume V2 ABI:
    "0xc5d563a36ae78145c45a50134d48a1215220f80a": "UNKNOWN_or_OLD_negrisk_like",
    "0x4bfb41d5b3570defd03c39a9a4d8de6bd8b8982e": "UNKNOWN_or_OLD_ctf_like",
}


def _addr(topic):
    return ("0x" + topic[-40:]).lower() if topic else None


def both_decodings(log: dict) -> dict:
    """Return raw topics + BOTH candidate address decodings, no assumption."""
    topics = log.get("topics", [])
    t = (topics + [None] * 4)[:4]
    return {
        "topic0": t[0], "topic1_orderHash": t[1],
        "topic2_addr": _addr(t[2]), "topic3_addr": _addr(t[3]),
        # candidate A: topic2=maker, topic3=taker (V2 source order per Copilot)
        "A_maker": _addr(t[2]), "A_taker": _addr(t[3]),
        # candidate B: topic2=taker, topic3=maker (my earlier reversed guess)
        "B_taker": _addr(t[2]), "B_maker": _addr(t[3]),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--rpc-url", default=None)
    ap.add_argument("--logs-json", default=None)
    ap.add_argument("--dune-csv", default=None,
                    help="optional Dune export with columns: evt_tx_hash, "
                         "evt_index, contract_address, maker, taker (for exact "
                         "log-index cross-check)")
    ap.add_argument("--n-tx", type=int, default=15)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    topic = _ofj.resolve_topic0()
    if topic.get("method") == "NO_KECCAK_LIB":
        print("NEED_CONTRACT_ABI_DISCOVERY — no keccak lib:", topic["warning"])
        return 0

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

    # fetch raw logs per tx
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

    # optional Dune export for EXACT (tx, log_index) cross-check
    dune = None
    if args.dune_csv and pathlib.Path(args.dune_csv).exists():
        dune = pd.read_csv(args.dune_csv)
        dune.columns = [c.lower() for c in dune.columns]
        dune["evt_tx_hash"] = dune["evt_tx_hash"].astype(str).str.lower()

    rows = []
    for tx in pick:
        raw_logs = logs_by_tx.get(tx, [])
        wallets = set(str(w).lower() for w in t[t["tx_hash"] == tx]["wallet"])
        for lg in raw_logs:
            if not lg.get("topics") or lg["topics"][0].lower() not in _ofj.KNOWN_TOPICS:
                continue
            contract = (lg.get("address") or "").lower()
            li = _ofj._hexint(lg.get("logIndex"))
            dec = both_decodings(lg)
            # EXACT Dune match: same tx AND same evt_index == log_index
            dune_maker = dune_taker = None
            if dune is not None:
                m = dune[(dune["evt_tx_hash"] == tx.lower())
                         & (dune["evt_index"] == li)]
                if len(m) == 1:
                    dune_maker = str(m.iloc[0].get("maker", "")).lower() or None
                    dune_taker = str(m.iloc[0].get("taker", "")).lower() or None
            # which candidate matches Dune (if Dune present)?
            matches = None
            if dune_maker:
                if dec["A_maker"] == dune_maker and dec["A_taker"] == dune_taker:
                    matches = "A(topic2=maker)"
                elif dec["B_maker"] == dune_maker and dec["B_taker"] == dune_taker:
                    matches = "B(topic2=taker)"
                else:
                    matches = "NEITHER"
            wallet_at_topic2 = dec["topic2_addr"] in wallets
            wallet_at_topic3 = dec["topic3_addr"] in wallets
            rows.append({
                "tx_hash": tx, "contract_address": contract,
                "contract_label": CONTRACT_LABELS.get(contract, "UNKNOWN"),
                "log_index": li,
                "topic2_addr": dec["topic2_addr"], "topic3_addr": dec["topic3_addr"],
                "wallet_at_topic2": wallet_at_topic2,
                "wallet_at_topic3": wallet_at_topic3,
                "dune_maker": dune_maker, "dune_taker": dune_taker,
                "dune_match_candidate": matches,
                "monitored_wallets": "|".join(sorted(wallets)),
            })
    rj = pd.DataFrame(rows)

    # per-contract conclusion (only where we have Dune to anchor truth)
    per_contract = {}
    for contract, g in (rj.groupby("contract_address") if len(rj) else []):
        anchored = g[g["dune_match_candidate"].isin(["A(topic2=maker)",
                                                     "B(topic2=taker)"])]
        cand = anchored["dune_match_candidate"].value_counts().to_dict()
        neither = int((g["dune_match_candidate"] == "NEITHER").sum())
        if len(anchored) == 0:
            order = "UNDETERMINED_no_dune_anchor"
        elif len(cand) == 1:
            order = list(cand)[0]
        else:
            order = "CONFLICTING"
        per_contract[contract] = {
            "label": CONTRACT_LABELS.get(contract, "UNKNOWN"),
            "n_logs": int(len(g)),
            "dune_anchored_logs": int(len(anchored)),
            "candidate_counts": cand, "neither_count": neither,
            "resolved_topic_order": order,
        }

    # overall label
    if len(rj) == 0:
        label = "NEED_CONTRACT_ABI_DISCOVERY"
    elif dune is None:
        label = "INCONCLUSIVE"   # raw topics dumped, but no Dune anchor to confirm
    elif any(c["resolved_topic_order"] == "CONFLICTING"
             for c in per_contract.values()):
        label = "TOPIC_ORDER_MISMATCH"
    elif any(c["neither_count"] > 0 and c["dune_anchored_logs"] == 0
             for c in per_contract.values()):
        label = "DUNE_LOG_MISMATCH"
    elif all(c["resolved_topic_order"].startswith(("A(", "B("))
             for c in per_contract.values() if c["dune_anchored_logs"]):
        label = "TOPIC_ORDER_CONFIRMED_PER_CONTRACT"
    else:
        label = "INCONCLUSIVE"

    out = {
        "validation": "orderfilled_topic_order_strict",
        "topic0": topic,
        "decision_label": label,
        "per_contract": per_contract,
        "n_logs": int(len(rj)),
        "dune_provided": dune is not None,
        "notes": [
            "NO global topic order assumed; raw topics dumped per log.",
            "Dune cross-check requires EXACT same log_index (evt_index), not a "
            "neighboring log in the same multi-fill tx.",
            "each emitting contract resolved separately; V2 ABI NOT assumed for "
            "older/unknown contracts.",
        ],
    }
    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "orderfilled_topic_order_validation.json").write_text(
        json.dumps(out, indent=2, default=str))
    rj.to_csv(out_dir / "orderfilled_topic_order_validation.csv", index=False)
    _write_md(out, rj, out_dir / "orderfilled_topic_order_validation.md")

    print("=" * 64)
    print("STRICT TOPIC-ORDER VALIDATION (no assumptions)")
    print("=" * 64)
    print(f"  logs examined: {len(rj)} | dune provided: {dune is not None}")
    for c, info in per_contract.items():
        print(f"  [{info['label']}] {c[:10]}.. logs={info['n_logs']} "
              f"dune_anchored={info['dune_anchored_logs']} "
              f"-> {info['resolved_topic_order']}")
    print(f"  >>> LABEL: {label}")
    if dune is None:
        print("  (no --dune-csv: raw topics dumped to CSV; provide Dune export "
              "with exact evt_index to resolve topic order)")
    print(f"  wrote {out_dir}/orderfilled_topic_order_validation.json (+ md, csv)")
    return 0


def _write_md(out, rj, path):
    L = ["# Strict OrderFilled Topic-Order Validation (no assumptions)", "",
         f"**Label: `{out['decision_label']}`**", "",
         "Prior error corrected: comparison must use the EXACT same log_index "
         "(evt_index), not a neighboring log in a multi-fill tx. No global topic "
         "order is assumed; each emitting contract is resolved separately.", "",
         "## Per-contract", "",
         "| contract | label | logs | dune-anchored | resolved order |",
         "|---|---|---|---|---|"]
    for c, info in out["per_contract"].items():
        L.append(f"| {c} | {info['label']} | {info['n_logs']} | "
                 f"{info['dune_anchored_logs']} | {info['resolved_topic_order']} |")
    L += ["", "## How to read",
          "- `A(topic2=maker)` = the V2-source order (orderHash, maker, taker).",
          "- `B(topic2=taker)` = the reversed order.",
          "- resolution requires a Dune row with the SAME evt_index to anchor "
          "which candidate is correct, PER CONTRACT.",
          "", "## Notes"]
    L += [f"- {n}" for n in out["notes"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
