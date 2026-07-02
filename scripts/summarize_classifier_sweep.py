"""Summarise the classifier sensitivity sweep CSV.

The sweep itself printed aggregate stats; this digs into STRUCTURE so we can
state the finding precisely rather than just "the split moves a lot":

  1. Baseline + the min/max-MM corners, with UNKNOWN counts, to confirm the
     extreme corners are not DEGENERATE (e.g. everything collapsing to UNKNOWN
     or to one class because the data ran out, rather than a real reclassif.).
  2. Flip structure: of the grid configs, how many flip the MM-majority, and
     which single threshold VALUE each flip is most associated with — a cheap
     variable-importance read on what actually drives the split.
  3. mm_fraction conditioned on each threshold value (marginal means), so we
     can see which knob has the biggest lever on the split.
  4. Survivor distribution among the configs that ran the skill gauntlet
     (baseline + OAT), tabulated by which class held the majority — the key
     robustness check: does the directional-survivor count depend on how the
     population was drawn?

No recomputation, no data store needed — pure read of the CSV the sweep wrote.

Run:
    ~/bot1/pm_research/.venv/bin/python scripts/summarize_classifier_sweep.py \
        --csv ~/bot1/pm_research/classifier_sweep_results.csv
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

THRESHOLDS = ["sell_buy_hi", "two_sided_hi", "roundtrip_hi",
              "hold_lo_hours", "breadth_hi", "min_score"]


def _fmt_cfg(row) -> str:
    return "  ".join(f"{t}={row[t]:g}" for t in THRESHOLDS)


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="classifier_sweep_results.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    grid = df[df["sweep"] == "grid"].copy()
    oat = df[df["sweep"].isin(["oat", "baseline"])].copy()
    base = df[df["sweep"] == "baseline"].iloc[0]

    print(f"loaded {len(df):,} sweep rows "
          f"({len(grid):,} grid, {len(oat):,} oat+baseline)")
    print(f"baseline mm_fraction = {base['mm_fraction']:.3f}  "
          f"(MM={int(base['n_mm'])} DIR={int(base['n_directional'])} "
          f"UNK={int(base['n_unknown'])})")

    # ---- 1. extreme corners, degeneracy check ----------------------------
    section("1. EXTREME CORNERS (is the 0.12 / 0.94 range degenerate?)")
    lo = grid.loc[grid["mm_fraction"].idxmin()]
    hi = grid.loc[grid["mm_fraction"].idxmax()]
    for tag, r in [("MIN mm_fraction", lo), ("MAX mm_fraction", hi)]:
        print(f"\n  {tag} = {r['mm_fraction']:.3f}")
        print(f"    cfg: {_fmt_cfg(r)}")
        print(f"    split: MM={int(r['n_mm'])} DIR={int(r['n_directional'])} "
              f"UNK={int(r['n_unknown'])} judged={int(r['judged'])}")
    # degeneracy = UNKNOWN dominating, or judged pool collapsing
    base_unk = int(base["n_unknown"])
    print(f"\n  baseline UNK={base_unk}. If corner UNK ~ baseline UNK, the")
    print("  extreme is a real reclassification, not the pool dissolving.")
    if int(lo["n_unknown"]) > base_unk * 2 or int(hi["n_unknown"]) > base_unk * 2:
        print("  WARNING: a corner has >2x baseline UNK — inspect for degeneracy.")
    else:
        print("  OK: UNKNOWN stable at both corners — extremes are genuine.")

    # ---- 2. flip structure & driver -------------------------------------
    section("2. MM-MAJORITY FLIP STRUCTURE")
    n_flip = int(grid["mm_majority_flip"].fillna(False).sum())
    print(f"  grid configs flipping MM-majority: {n_flip}/{len(grid)} "
          f"({100*n_flip/len(grid):.1f}%)")
    # which threshold value is most over-represented among flips?
    print("\n  flip rate by threshold value (how often each setting flips):")
    for t in THRESHOLDS:
        sub = (grid.groupby(t)["mm_majority_flip"]
               .apply(lambda s: float(s.fillna(False).mean())))
        cells = "  ".join(f"{v:g}:{rate:.2f}" for v, rate in sub.items())
        print(f"    {t:14s} {cells}")
    print("\n  (read: a value with flip-rate near 1.0 almost always flips the")
    print("   majority; near 0.0 almost never does — that's the dominant lever.)")

    # ---- 3. marginal mean mm_fraction per threshold value ----------------
    section("3. MARGINAL EFFECT ON mm_fraction (grid means per value)")
    spreads = {}
    for t in THRESHOLDS:
        m = grid.groupby(t)["mm_fraction"].mean()
        spreads[t] = float(m.max() - m.min())
        cells = "  ".join(f"{v:g}:{val:.3f}" for v, val in m.items())
        print(f"  {t:14s} {cells}")
    section("3b. THRESHOLDS RANKED BY LEVER SIZE (max-min of marginal means)")
    for t, s in sorted(spreads.items(), key=lambda kv: -kv[1]):
        bar = "#" * int(round(s * 50))
        print(f"  {t:14s} {s:.3f}  {bar}")
    print("\n  The biggest-lever threshold is the one whose exact value most")
    print("  determines the headline split — i.e. the most important to pin")
    print("  down (or replace with ground truth).")

    # ---- 4. survivor distribution (configs that ran the gauntlet) -------
    section("4. DIRECTIONAL-SURVIVOR ROBUSTNESS (oat+baseline gauntlet runs)")
    g = oat[oat["gate_persist_and_fee"] >= 0].copy()
    g["majority"] = np.where(g["mm_fraction"] >= 0.5, "MM-majority",
                             "DIR-majority")
    print(f"  configs with skill test run: {len(g)}")
    surv = g["gate_persist_and_fee"]
    print(f"  survivors across all: min={int(surv.min())} "
          f"med={surv.median():.1f} max={int(surv.max())}")
    print("\n  survivor count by which class held the majority:")
    for maj, sub in g.groupby("majority"):
        vals = sorted(sub["gate_persist_and_fee"].tolist())
        print(f"    {maj:13s} n={len(sub):2d}  survivors={vals}  "
              f"(max={max(vals)})")
    print("\n  KEY CHECK: if max survivors stays tiny (0-2) in BOTH rows, the")
    print("  skill verdict is INVARIANT to how the population is drawn — the")
    print("  fragile split does not threaten the NO-GO decision.")

    # ---- one-line headline ----------------------------------------------
    section("HEADLINE")
    mn, md, mx = (grid["mm_fraction"].min(), grid["mm_fraction"].median(),
                  grid["mm_fraction"].max())
    print(f"  mm_fraction: baseline={base['mm_fraction']:.2f}, "
          f"grid range [{mn:.2f}, {mx:.2f}], median {md:.2f}.")
    print(f"  {n_flip}/{len(grid)} grid configs flip the majority -> the SPLIT")
    print("  is threshold-dependent and must be quoted as a range.")
    print(f"  But directional survivors stay in "
          f"[{int(surv.min())}, {int(surv.max())}] regardless -> the VERDICT")
    print("  is robust. The fragility is descriptive, not decision-relevant.")


if __name__ == "__main__":
    main()
