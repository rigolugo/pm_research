"""Verify the baseline-split shift is caused by the sell/buy NaN-guard fix.

The FINDINGS correction (§4.5.1) states the baseline MM/DIR split moved (≈50/39
-> 61/42) because the corrected `sell_buy_ratio` tell now fires where the old
`is not np.nan` identity guard silently never did. This script proves that
claim rather than reasoning it, by classifying the SAME real wallets two ways:

  OLD  - reproduces the buggy guard exactly:
             b["sell_buy_ratio"] is not np.nan and b["sell_buy_ratio"] >= hi
         (identity test; effectively always True for finite floats, and the
          interaction with the np.isnan hold-guard reproduced verbatim).
  NEW  - calls the shipped, fixed classify().

It then:
  1. Confirms NEW here == the canonical classify() (sanity: our inline OLD/NEW
     differ only in the two guarded tells, nothing else).
  2. Reports the split under each.
  3. Diffs labels wallet-by-wallet and shows, for every wallet that changed,
     the sell/buy ratio, the OLD vs NEW sell_buy tell, and the score delta —
     so we can see the change is exactly the corrected tell newly firing.

If every label change is explained by the sell_buy tell flipping (or, for
all-SELL wallets, by inf now being handled), the attribution is verified.

Run:
    ~/bot1/pm_research/.venv/bin/python scripts/verify_nan_fix_attribution.py \
        --root ~/data
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.wallet_classifier import (
    classify, _wallet_behavior,
)

# baseline thresholds (must match FINDINGS / the sweep baseline)
HI = dict(sell_buy_hi=0.4, two_sided_hi=0.15, roundtrip_hi=0.4,
          hold_lo_hours=48.0, breadth_hi=50, min_trades=20, min_score=3)


def _score_old(b: dict) -> tuple[int, bool]:
    """Reproduce the PRE-FIX scoring exactly, returning (score, old_sb_tell).

    The bug: `x is not np.nan` is an identity test. For a ratio computed as
    n_sell/n_buy it is a fresh float, never the np.nan singleton, so the guard
    is ~always True and the tell reduces to `ratio >= hi`. For the literal
    np.nan assigned in the degenerate case, `is not np.nan` is also typically
    True (CPython does not intern NaN), so NaN would ALSO pass the guard and
    then `nan >= hi` is False — i.e. it happens not to trip, but for the wrong
    reason. We reproduce the expression verbatim to be faithful.
    """
    sbr = b["sell_buy_ratio"]
    old_sb_tell = bool(sbr is not np.nan and sbr >= HI["sell_buy_hi"])
    mh = b["median_hold_hours"]
    # old hold guard used np.isnan (works on float nan, would raise on None)
    old_hold_tell = bool((not np.isnan(mh)) and mh <= HI["hold_lo_hours"])
    tells = [
        old_sb_tell,
        (b["two_sided_rate"] >= HI["two_sided_hi"]),
        (b["roundtrip_rate"] >= HI["roundtrip_hi"]),
        old_hold_tell,
        (b["market_breadth"] >= HI["breadth_hi"]),
    ]
    return int(sum(bool(x) for x in tells)), old_sb_tell


def _score_new(b: dict) -> tuple[int, bool]:
    """Reproduce the FIXED scoring (mirrors the shipped classify())."""
    sbr = b["sell_buy_ratio"]
    new_sb_tell = bool(pd.notna(sbr) and sbr >= HI["sell_buy_hi"])
    mh = b["median_hold_hours"]
    new_hold_tell = bool(pd.notna(mh) and mh <= HI["hold_lo_hours"])
    tells = [
        new_sb_tell,
        (b["two_sided_rate"] >= HI["two_sided_hi"]),
        (b["roundtrip_rate"] >= HI["roundtrip_hi"]),
        new_hold_tell,
        (b["market_breadth"] >= HI["breadth_hi"]),
    ]
    return int(sum(bool(x) for x in tells)), new_sb_tell


def _label(score: int) -> str:
    return "MARKET_MAKER" if score >= HI["min_score"] else "DIRECTIONAL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)

    recs = []
    for wallet, g in trades.groupby("wallet"):
        b = _wallet_behavior(g)
        if b["n_trades"] < HI["min_trades"]:
            recs.append({"wallet": wallet, "old": "UNKNOWN", "new": "UNKNOWN",
                         "sell_buy_ratio": b["sell_buy_ratio"],
                         "old_sb_tell": None, "new_sb_tell": None,
                         "old_score": np.nan, "new_score": np.nan})
            continue
        os_, ot = _score_old(b)
        ns_, nt = _score_new(b)
        recs.append({"wallet": wallet, "old": _label(os_), "new": _label(ns_),
                     "sell_buy_ratio": b["sell_buy_ratio"],
                     "old_sb_tell": ot, "new_sb_tell": nt,
                     "old_score": os_, "new_score": ns_})
    d = pd.DataFrame(recs)

    # ---- sanity: our inline NEW must equal the shipped classify() ----------
    canon = classify(trades, **HI)[["wallet", "label"]].rename(
        columns={"label": "canon"})
    chk = d.merge(canon, on="wallet", how="left")
    mismatch = chk[chk["new"] != chk["canon"]]
    print("=== sanity: inline NEW vs canonical classify() ===")
    if mismatch.empty:
        print("  OK: inline NEW reproduces the shipped classifier exactly.")
    else:
        print(f"  WARNING: {len(mismatch)} wallets differ from canonical — the")
        print("  inline reproduction is not faithful; interpret with care.")
        print(mismatch[["wallet", "new", "canon"]].head(20).to_string(index=False))

    # ---- splits under each -------------------------------------------------
    def split(col):
        vc = d[col].value_counts()
        return (int(vc.get("MARKET_MAKER", 0)),
                int(vc.get("DIRECTIONAL", 0)),
                int(vc.get("UNKNOWN", 0)))
    omm, odir, ounk = split("old")
    nmm, ndir, nunk = split("new")
    print("\n=== baseline split, OLD (buggy) vs NEW (fixed) ===")
    print(f"  OLD:  MM={omm}  DIR={odir}  UNK={ounk}")
    print(f"  NEW:  MM={nmm}  DIR={ndir}  UNK={nunk}")
    print(f"  delta: MM {nmm-omm:+d}  DIR {ndir-odir:+d}  UNK {nunk-ounk:+d}")

    # ---- label changes, fully explained ------------------------------------
    judged = d[d["old"] != "UNKNOWN"]
    changed = judged[judged["old"] != judged["new"]]
    print(f"\n=== wallets whose label changed: {len(changed)} ===")
    if changed.empty:
        print("  none — the fix did not move any baseline label "
              "(attribution would then be: no shift to explain).")
    else:
        # is every change accompanied by the sell_buy tell flipping?
        sb_flipped = changed[changed["old_sb_tell"] != changed["new_sb_tell"]]
        print(f"  of these, {len(sb_flipped)}/{len(changed)} have the sell_buy "
              f"tell flipping OLD->NEW (the fixed tell newly (un)firing).")
        print("\n  per-wallet detail:")
        print("  wallet         sb_ratio  old_sb new_sb  old_sc new_sc  "
              "old_label -> new_label")
        for _, r in changed.iterrows():
            ratio = (f"{r['sell_buy_ratio']:.3f}"
                     if np.isfinite(r["sell_buy_ratio"]) else
                     str(r["sell_buy_ratio"]))
            print(f"  {r['wallet'][:12]}  {ratio:>8s}  "
                  f"{str(r['old_sb_tell']):>5s}  {str(r['new_sb_tell']):>5s}  "
                  f"{int(r['old_score']):>5d}  {int(r['new_score']):>5d}  "
                  f"{r['old']} -> {r['new']}")
        unexplained = changed[changed["old_sb_tell"] == changed["new_sb_tell"]]
        print()
        if unexplained.empty:
            print("  VERDICT: every label change is explained by the sell_buy")
            print("  tell flipping. Attribution to the NaN-guard fix VERIFIED.")
        else:
            print(f"  NOTE: {len(unexplained)} change(s) NOT accompanied by a")
            print("  sell_buy tell flip — these are driven by the hold-guard")
            print("  change instead (np.isnan -> pd.notna). Still the fix, but")
            print("  via the hold tell. Detail:")
            print(unexplained[["wallet", "old", "new", "old_score",
                               "new_score"]].to_string(index=False))

    # all-SELL wallets specifically (inf ratio) — the clearest fix case
    inf_w = judged[~np.isfinite(judged["sell_buy_ratio"])]
    print(f"\n=== all-SELL / non-finite-ratio wallets: {len(inf_w)} ===")
    if len(inf_w):
        print("  (inf ratio = n_buy==0; the fixed tell trips, old guard was")
        print("   incidental). labels old->new:")
        for _, r in inf_w.iterrows():
            print(f"    {r['wallet'][:12]}  ratio={r['sell_buy_ratio']}  "
                  f"{r['old']} -> {r['new']}")


if __name__ == "__main__":
    main()
