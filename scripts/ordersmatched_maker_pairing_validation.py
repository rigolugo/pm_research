"""Maker-pairing validation (research only) — is the 0-maker result real or a bug?

The OrdersMatched probe returned 10 ECONOMIC_TAKER_CONFIRMED / 0 ECONOMIC_MAKER
with pairing AVAILABLE. Before trusting that split, prove the pairing logic CAN
classify a known maker. This harness:
  1. finds candidate cases: a Dune OrdersMatched row where our wallet is NOT the
     takerordermaker, but our wallet IS present as the event-maker of an
     OrderFilled leg in the same tx;
  2. dumps the EXACT values classify_trade compares (RPC asset ids vs Dune asset
     ids) so a format mismatch is visible;
  3. runs the real classify_trade and reports VALIDATED / BROKEN / NO_CASE.

No sample expansion. No log_index work. No PnL. No indexer. No behavioral claim.
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


def find_candidates(dune: pd.DataFrame, trades: pd.DataFrame,
                    of_by_tx: dict) -> list[dict]:
    """A candidate = OM row where wallet != takerordermaker, but wallet is the
    event-maker of some OrderFilled leg in the same tx (hand-verifiable maker)."""
    candidates = []
    for _, om in dune.iterrows():
        tx = str(om["evt_tx_hash"]).lower()
        wallets = set(str(w).lower()
                      for w in trades[trades["tx_hash"].str.lower() == tx]["wallet"])
        taker_owner = str(om.get("takerordermaker", "")).lower()
        if taker_owner in wallets:
            continue                      # this is a taker case, skip
        if taker_owner in _om.KNOWN_EXCHANGE:
            continue                      # operator leg, skip
        legs = of_by_tx.get(tx, [])
        for f in legs:
            if f["maker"] in wallets and f["maker"] != taker_owner:
                candidates.append({
                    "tx_hash": tx, "om_evt_index": om.get("evt_index"),
                    "takerordermaker": taker_owner,
                    "wallet": f["maker"],
                    "of_log_index": f["log_index"],
                    "of_maker": f["maker"], "of_taker": f["taker"],
                    "of_maker_asset_id": str(f["maker_asset_id"]),
                    "of_taker_asset_id": str(f["taker_asset_id"]),
                    "om_makerassetid": str(om.get("makerassetid")),
                    "om_takerassetid": str(om.get("takerassetid")),
                    "om_row": om.to_dict(), "legs": legs, "wallets": wallets,
                })
    return candidates


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--dune-csv", required=True)
    ap.add_argument("--rpc-url", default=None)
    ap.add_argument("--n-tx", type=int, default=18)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.3)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    store = Store(args.root)
    trades = store.load_trades()
    t = trades[trades["tx_hash"].astype(str).str.startswith("0x")].copy()
    t["tx_hash"] = t["tx_hash"].astype(str)

    # reproduce the SAME sample as the probe (same seed/n-tx) so tx align
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

    dune = _om._read_csv_tolerant(args.dune_csv)
    dune.columns = [c.lower() for c in dune.columns]
    dune["evt_tx_hash"] = dune["evt_tx_hash"].astype(str).str.lower()

    # fetch OrderFilled legs (same as probe phase 2)
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
                    print("  RPC limited; partial"); break
                legs = [d for lg in (rcpt or {}).get("logs", [])
                        if (d := _ofj.decode_orderfilled(lg))]
                of_by_tx[tx] = legs
                print(f"  legs {i}/{len(target)}: {tx[:12]}.. ({len(legs)})")
                time.sleep(args.sleep)

    candidates = find_candidates(dune, t, of_by_tx)

    # run the REAL classify_trade on each candidate + dump the compared values
    results = []
    for c in candidates:
        res = _om.classify_trade(c["om_row"], c["wallets"], c["legs"])
        # explicitly compute the same_asset comparison so we can SEE it
        of_ids = {c["of_maker_asset_id"], c["of_taker_asset_id"]}
        om_ids = {c["om_makerassetid"], c["om_takerassetid"]}
        asset_overlap = bool(of_ids & om_ids)
        results.append({
            "tx_hash": c["tx_hash"], "om_evt_index": c["om_evt_index"],
            "wallet": c["wallet"], "takerordermaker": c["takerordermaker"],
            "of_log_index": c["of_log_index"],
            "of_maker_asset_id": c["of_maker_asset_id"],
            "of_taker_asset_id": c["of_taker_asset_id"],
            "om_makerassetid": c["om_makerassetid"],
            "om_takerassetid": c["om_takerassetid"],
            "asset_ids_overlap": asset_overlap,
            "classify_result": res["economic_role"],
            "confirmed_by": res.get("confirmed_by"),
        })

    n_cases = len(results)
    correct = [r for r in results if r["classify_result"] == "ECONOMIC_MAKER_CONFIRMED"]
    # a case where wallet is a real maker leg but classify failed AND the reason
    # looks like an asset-format mismatch -> BROKEN
    broken = [r for r in results
              if r["classify_result"] != "ECONOMIC_MAKER_CONFIRMED"]

    if n_cases == 0:
        label = "NO_KNOWN_MAKER_CASE_FOUND"
        failure = ("no OM row where wallet != takerordermaker AND wallet is an "
                   "event-maker leg in the same tx (within this sample)")
    elif len(correct) >= 1:
        label = "MAKER_PAIRING_VALIDATED"
        failure = None
    else:
        label = "MAKER_PAIRING_BROKEN"
        # diagnose: did asset overlap exist but classify still failed?
        any_overlap = any(r["asset_ids_overlap"] for r in results)
        failure = ("hand-verified maker case(s) exist but classify_trade did NOT "
                   "return ECONOMIC_MAKER_CONFIRMED. "
                   + ("asset_ids DO overlap in raw set-comparison but the in-code "
                      "same_asset check failed -> format/type mismatch between RPC "
                      "asset ids and Dune asset ids."
                      if any_overlap else
                      "asset ids do not overlap even in raw comparison -> the OM "
                      "asset ids and OrderFilled asset ids differ in representation "
                      "(hex vs dec, scientific notation, or scaling)."))

    out = {
        "validation_label": label,
        "candidates_checked": n_cases,
        "maker_cases_found": n_cases,
        "maker_cases_correctly_classified": len(correct),
        "failure_reason": failure,
        "split_now_interpretable": label == "MAKER_PAIRING_VALIDATED",
        "cases": results,
        "guardrails": ["validation only", "no sample expansion", "no log_index",
                       "no PnL", "no indexer", "no behavioral claim"],
    }
    (out_dir / "ordersmatched_maker_pairing_validation.json").write_text(
        json.dumps(out, indent=2, default=str))
    pd.DataFrame(results or [{"note": "no candidates"}]).to_csv(
        out_dir / "ordersmatched_maker_pairing_validation.csv", index=False)
    _write_md(out, out_dir / "ordersmatched_maker_pairing_validation.md")

    print("=" * 64)
    print("MAKER-PAIRING VALIDATION (research only)")
    print("=" * 64)
    print(f"  candidates (known maker-side cases): {n_cases}")
    print(f"  correctly classified ECONOMIC_MAKER_CONFIRMED: {len(correct)}")
    for r in results[:5]:
        print(f"   - {r['tx_hash'][:12]}.. of_ids=({r['of_maker_asset_id'][:12]}..,"
              f"{r['of_taker_asset_id'][:12]}..) om_ids=({r['om_makerassetid'][:12]}..,"
              f"{r['om_takerassetid'][:12]}..) overlap={r['asset_ids_overlap']} "
              f"-> {r['classify_result']}")
    print(f"  >>> VALIDATION LABEL: {label}")
    if failure:
        print(f"  failure_reason: {failure}")
    print(f"  split_now_interpretable: {out['split_now_interpretable']}")
    print(f"  wrote {out_dir}/ordersmatched_maker_pairing_validation.json (+ md, csv)")
    return 0


def _write_md(out, path):
    L = ["# Maker-Pairing Validation (research only)", "",
         f"**Validation label: `{out['validation_label']}`**", "",
         f"- candidates checked: {out['candidates_checked']}",
         f"- maker cases found: {out['maker_cases_found']}",
         f"- correctly classified ECONOMIC_MAKER_CONFIRMED: "
         f"{out['maker_cases_correctly_classified']}",
         f"- failure_reason: {out['failure_reason']}",
         f"- 10/0 split now interpretable: {out['split_now_interpretable']}", "",
         "## Cases (raw values compared by the pairing logic)", "",
         "| tx | wallet | of_maker_asset | om_makerassetid | overlap | result |",
         "|---|---|---|---|---|---|"]
    for r in out["cases"]:
        L.append(f"| {r['tx_hash'][:10]}.. | {r['wallet'][:8]}.. | "
                 f"{r['of_maker_asset_id'][:14]}.. | {r['om_makerassetid'][:14]}.. | "
                 f"{r['asset_ids_overlap']} | {r['classify_result']} |")
    L += ["", "## Interpretation",
          "- `MAKER_PAIRING_VALIDATED`: the logic CAN detect a maker -> the 0-maker "
          "result in the probe is a REAL all-taker finding, now interpretable.",
          "- `MAKER_PAIRING_BROKEN`: a real maker case was misclassified -> the "
          "0-maker result is an ARTIFACT; fix asset-id matching and re-run.",
          "- `NO_KNOWN_MAKER_CASE_FOUND`: no maker case in this sample -> cannot "
          "validate; widen sample (but the 10/0 may simply reflect a taker-heavy "
          "sample).", "", "## Guardrails"]
    L += [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
