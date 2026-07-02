"""Classifier threshold-sensitivity sweep.

WHY. The headline MM/DIRECTIONAL split (and therefore the "half the pool is
uncopyable" argument) came from ONE fixed set of classifier thresholds. That
point estimate has no error bars. This script perturbs the thresholds and
reports how stable (a) the wallet split and (b) the downstream skill-test
verdict are. If the split swings wildly across plausible thresholds, the
"uncopyable by construction" claim is fragile; if it barely moves, the claim
is robust. Either way we now KNOW instead of assuming.

TWO PASSES (run both, then compare):
  OAT  - One-At-a-Time: vary each threshold alone, others at baseline.
         Fast, readable, isolates which single knob the split is most
         sensitive to. Misses interactions between thresholds.
  GRID - full Cartesian product over all thresholds. Captures interactions
         OAT cannot see. If GRID's spread is much wider than OAT's, that is
         itself the finding: the thresholds interact and no single knob can
         be reported in isolation.

PER CONFIG we record:
  - n_mm / n_directional / n_unknown   (the split)
  - mm_fraction of the judged (non-UNKNOWN) pool
  - mm_majority_flip flag: did the MM share cross 50% relative to baseline?
  - the skill-test single-split gauntlet on the DIRECTIONAL pool:
      wallets tested -> BH survivors -> fee-clearing -> persist+fee on TEST
    i.e. how many directional wallets pass, under THIS population definition.

This reuses the REAL skill-test functions (evaluate_window, benjamini_hochberg,
net_of_fee_pnl) so it cannot drift from the canonical gates. It runs the
single-split portion only (not the K-split hardened verification) — the point
is sensitivity of the split and the first-order verdict, run many times, not a
final tradability claim. A config that produces survivors here should be fed
to the full randomization_skill_test.py for the hardened check.

Run (example, matching your bot layout):
    nohup ~/bot1/pm_research/.venv/bin/python -u \
      ~/bot1/pm_research/scripts/classifier_sensitivity_sweep.py \
      --root ~/data --mode both \
      > ~/bot1/pm_research/classifier_sweep.log 2>&1 & echo "PID: $!"
"""
from __future__ import annotations

import argparse
import itertools
import json
from datetime import date

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.wallet_classifier import classify

# Reuse the REAL skill-test gates so this can never diverge from canon. The
# sibling script imports only pm_research.* and is normally run as a file (not
# as a package), so `import scripts.x` is unreliable depending on invocation.
# Put the repo root on sys.path and import the sibling module by bare name,
# which works whether this is run as `python scripts/foo.py`, `python -m
# scripts.foo`, or under nohup.
import os
import sys
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from randomization_skill_test import (  # noqa: E402  (path set up above)
    evaluate_window, benjamini_hochberg, N_PERM, MIN_RESOLVED_TRADES, SEED,
)


# ---- baseline thresholds (the ones FINDINGS used) -------------------------
BASELINE = dict(sell_buy_hi=0.4, two_sided_hi=0.15, roundtrip_hi=0.4,
                hold_lo_hours=48.0, breadth_hi=50, min_score=3)

# ---- perturbation grids (plausible ranges around each baseline) -----------
# Chosen to bracket each baseline value without becoming absurd. min_score is
# the majority cutoff: 2 = lenient (any-two tells), 3 = baseline majority,
# 4 = strict.
GRIDS = {
    "sell_buy_hi":   [0.25, 0.4, 0.55, 0.7],
    "two_sided_hi":  [0.05, 0.10, 0.15, 0.25],
    "roundtrip_hi":  [0.25, 0.4, 0.55, 0.7],
    "hold_lo_hours": [24.0, 48.0, 72.0, 120.0],
    "breadth_hi":    [25, 50, 75, 100],
    "min_score":     [2, 3, 4],
}


def split_counts(cls: pd.DataFrame) -> dict:
    n_mm = int((cls["label"] == "MARKET_MAKER").sum())
    n_dir = int((cls["label"] == "DIRECTIONAL").sum())
    n_unk = int((cls["label"] == "UNKNOWN").sum())
    judged = n_mm + n_dir
    mm_frac = (n_mm / judged) if judged else float("nan")
    return {"n_mm": n_mm, "n_directional": n_dir, "n_unknown": n_unk,
            "judged": judged, "mm_fraction": mm_frac}


def run_skill_gates(trades, winner, directional_pool, start, end, fee_rate):
    """The skill-test SINGLE-SPLIT gauntlet on a given directional pool.

    Returns counts at each gate. Reuses the canonical evaluate_window / BH so
    results are directly comparable to randomization_skill_test.py. This is
    deliberately the single mid-split version (not the K-split hardened test):
    we are measuring how the first-order verdict moves with the population
    definition, run once per config, not issuing a final verdict.
    """
    out = {"pool_size": len(directional_pool), "tested": 0, "bh_survivors": 0,
           "fee_clearing": 0, "persist_and_fee": 0, "note": ""}
    if not directional_pool:
        out["note"] = "empty directional pool"
        return out

    s = pd.Timestamp(start, tz="UTC")
    e = pd.Timestamp(end, tz="UTC")
    mid = s + (e - s) / 2
    tr_tr = trades[(trades["traded_at"] >= s) & (trades["traded_at"] < mid)]
    tr_te = trades[(trades["traded_at"] >= mid) & (trades["traded_at"] < e)]

    rng = np.random.default_rng(SEED)
    train = evaluate_window(tr_tr, winner, directional_pool, rng, fee_rate)
    if train.empty:
        out["note"] = "no wallets with enough resolved TRAIN trades"
        return out
    out["tested"] = int(len(train))
    train = train.sort_values("p_value").reset_index(drop=True)
    train["bh_pass"] = benjamini_hochberg(train["p_value"].tolist(), alpha=0.05)
    bh = train[train["bh_pass"]]
    out["bh_survivors"] = int(len(bh))
    if bh.empty:
        return out
    out["fee_clearing"] = int((bh["net_fee_pnl"] > 0).sum())

    cand = list(bh["wallet"])
    rng2 = np.random.default_rng(SEED + 1)
    test = evaluate_window(tr_te, winner, cand, rng2, fee_rate)
    if test.empty:
        out["note"] = "survivors lack resolved TEST trades (persistence INCONCLUSIVE)"
        return out
    test["persist_pass"] = test["p_value"] <= 0.05
    test["fee_pass"] = test["net_fee_pnl"] > 0
    out["persist_and_fee"] = int((test["persist_pass"] & test["fee_pass"]).sum())
    return out


def evaluate_config(cfg, trades, winner, args, baseline_mm_frac,
                    run_skill=True):
    cls = classify(trades, **cfg)
    sc = split_counts(cls)
    flip = None
    if baseline_mm_frac == baseline_mm_frac and sc["mm_fraction"] == sc["mm_fraction"]:
        # both non-NaN: did the MM share cross 50% vs baseline?
        flip = (sc["mm_fraction"] >= 0.5) != (baseline_mm_frac >= 0.5)
    if not run_skill:
        empty = {f"gate_{k}": (None if k == "note" else -1) for k in
                 ("pool_size", "tested", "bh_survivors", "fee_clearing",
                  "persist_and_fee", "note")}
        return {**cfg, **sc, "mm_majority_flip": flip, **empty}
    pool = list(cls[cls["label"] == "DIRECTIONAL"]["wallet"])
    gates = run_skill_gates(trades, winner, pool, args.start, args.end,
                            args.fee_rate)
    return {**cfg, **sc, "mm_majority_flip": flip, **{f"gate_{k}": v
            for k, v in gates.items()}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    ap.add_argument("--fee-rate", type=float, default=0.05)
    ap.add_argument("--mode", choices=["oat", "grid", "both"], default="both")
    ap.add_argument("--grid-skill-test", action="store_true", default=False,
                    help="Run the full skill-test gauntlet on EVERY grid config "
                         "(SLOW: ~3000 configs x 10k perms = hours). Default off: "
                         "the grid computes only the split + majority-flip flags "
                         "(instant), which is what the sensitivity question needs. "
                         "OAT + baseline always run the full gauntlet regardless.")
    ap.add_argument("--out-csv", default="classifier_sweep_results.csv")
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)
    res = store.load_resolutions()
    winner = dict(zip(res["condition_id"], res["winning_outcome"]))

    print(f"loaded {len(trades):,} trades, {len(winner):,} resolved markets")
    print(f"N_PERM={N_PERM}, fee_rate={args.fee_rate}, "
          f"window {args.start}..{args.end}\n")

    # baseline first — everything is measured relative to this.
    base_cls = classify(trades, **BASELINE)
    base_sc = split_counts(base_cls)
    base_mm_frac = base_sc["mm_fraction"]
    print("=== BASELINE ===")
    print(f"  {BASELINE}")
    print(f"  split: MM={base_sc['n_mm']} DIR={base_sc['n_directional']} "
          f"UNK={base_sc['n_unknown']}  mm_fraction={base_mm_frac:.3f}\n")

    rows = []
    base_row = evaluate_config(BASELINE, trades, winner, args, base_mm_frac)
    base_row["sweep"] = "baseline"; base_row["varied"] = "-"
    rows.append(base_row)

    # ---------------- OAT ----------------
    if args.mode in ("oat", "both"):
        print("=== OAT (one-at-a-time) ===")
        for name, values in GRIDS.items():
            for v in values:
                if v == BASELINE[name]:
                    continue  # already have baseline
                cfg = dict(BASELINE); cfg[name] = v
                r = evaluate_config(cfg, trades, winner, args, base_mm_frac)
                r["sweep"] = "oat"; r["varied"] = name
                rows.append(r)
                flip = "  <-- MM-MAJORITY FLIP" if r["mm_majority_flip"] else ""
                print(f"  {name:14s}={str(v):>6s}  MM={r['n_mm']:3d} "
                      f"DIR={r['n_directional']:3d} mm_frac={r['mm_fraction']:.3f}  "
                      f"dir_survivors={r['gate_persist_and_fee']}{flip}")
        print()

    # ---------------- GRID ----------------
    if args.mode in ("grid", "both"):
        keys = list(GRIDS.keys())
        combos = list(itertools.product(*[GRIDS[k] for k in keys]))
        print(f"=== GRID (full product: {len(combos):,} configs) ===")
        for i, combo in enumerate(combos):
            cfg = dict(zip(keys, combo))
            r = evaluate_config(cfg, trades, winner, args, base_mm_frac,
                                run_skill=args.grid_skill_test)
            r["sweep"] = "grid"; r["varied"] = "all"
            rows.append(r)
            if (i + 1) % 100 == 0:
                print(f"  ...{i+1}/{len(combos)} configs done")
        print(f"  grid complete ({len(combos):,} configs)\n")

    df = pd.DataFrame(rows)
    df.to_csv(args.out_csv, index=False)

    # ---------------- summary ----------------
    print("=== SUMMARY ===")
    for sweep in ("oat", "grid"):
        sub = df[df["sweep"] == sweep]
        if sub.empty:
            continue
        mmf = sub["mm_fraction"].dropna()
        surv = sub["gate_persist_and_fee"]
        surv_real = surv[surv >= 0]  # exclude skipped (-1) configs
        flips = int(sub["mm_majority_flip"].fillna(False).sum())
        print(f"  [{sweep}]  configs={len(sub)}")
        print(f"     mm_fraction: min={mmf.min():.3f} med={mmf.median():.3f} "
              f"max={mmf.max():.3f}  (baseline={base_mm_frac:.3f})")
        if len(surv_real):
            print(f"     directional survivors: min={int(surv_real.min())} "
                  f"med={surv_real.median():.1f} max={int(surv_real.max())} "
                  f"(over {len(surv_real)} configs w/ skill test)")
        else:
            print("     directional survivors: skill test not run for this sweep")
        print(f"     MM-majority flips: {flips}/{len(sub)} configs")
    print(f"\n  full results -> {args.out_csv}")

    # OAT vs GRID comparison: is the grid spread wider (interaction effects)?
    if args.mode == "both":
        oat_mmf = df[df["sweep"] == "oat"]["mm_fraction"].dropna()
        grid_mmf = df[df["sweep"] == "grid"]["mm_fraction"].dropna()
        if len(oat_mmf) and len(grid_mmf):
            oat_range = oat_mmf.max() - oat_mmf.min()
            grid_range = grid_mmf.max() - grid_mmf.min()
            print("\n=== OAT vs GRID ===")
            print(f"  mm_fraction range:  OAT={oat_range:.3f}  GRID={grid_range:.3f}")
            if grid_range > oat_range * 1.25:
                print("  -> GRID spread materially wider than OAT: thresholds")
                print("     INTERACT. No single threshold can be reported alone;")
                print("     the split must be quoted as a range over the grid.")
            else:
                print("  -> GRID spread ~ OAT spread: thresholds act roughly")
                print("     independently; OAT is a fair summary of sensitivity.")


if __name__ == "__main__":
    main()
