"""Walk-forward backtest — turn one fragile point estimate into a distribution.

THE PROBLEM (from the resolution-flip robustness check). The single modeled-
latency backtest (§4.1) filled only 36 trades and ended at -6.26% ROI — one
resolution flip from break-even. That is statistically underpowered: the true
modeled-latency ROI could be modestly negative OR modestly positive and 36
trades cannot tell them apart.

THE FIX (no new data, no strategy change). Run the SAME engine on many rolling
windows across the full data span and look at the DISTRIBUTION of ROIs, not a
single point. This uses the existing data more completely and answers the real
question:

  - If most windows are clearly negative -> the -6% was not a fluke; the NO-GO
    is robust and the single-split fragility was just small-sample noise around
    a genuinely negative mean.
  - If windows straddle zero widely -> the data genuinely CANNOT distinguish
    positive from negative. That is also a valid, honest answer: it means the
    backtest leg (§4.1) is underpowered on this dataset regardless of slicing,
    and the verdict must rest on the other, non-trade-count-fragile legs
    (§4.2 edge-at-instant, §4.4 exit-mirror).

WHAT THIS DOES NOT DO. It does not change any gate, threshold, or the strategy.
It does not manufacture trades by loosening rejection rules (that would test a
different strategy). It only re-runs the identical strategy over more windows.
Windows overlap, so the per-window results are NOT independent — this is a
power/stability diagnostic, not a significance test. Stated plainly so no one
over-reads it.

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/walk_forward_backtest.py --root ~/data
"""
from __future__ import annotations

import argparse
import dataclasses
from datetime import date, timedelta

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.config import BacktestConfig
from pm_research.selection import TrailingAlphaSelector
from pm_research.backtest import BacktestEngine
from pm_research.latency import LatencyModel, ZERO_LATENCY


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--data-start", type=date.fromisoformat, default=date(2025, 3, 1),
                    help="earliest date with backfilled data")
    ap.add_argument("--data-end", type=date.fromisoformat, default=date(2026, 6, 1))
    ap.add_argument("--window-days", type=int, default=180,
                    help="length of each backtest window (test period)")
    ap.add_argument("--step-days", type=int, default=30,
                    help="how far each window start advances")
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)
    res = store.load_resolutions()
    markets = store.load_markets()
    empty_prices = pd.DataFrame(columns=["condition_id", "ts", "yes_price"])

    # build rolling windows
    windows = []
    cur = args.data_start
    while cur + timedelta(days=args.window_days) <= args.data_end:
        windows.append((cur, cur + timedelta(days=args.window_days)))
        cur = cur + timedelta(days=args.step_days)
    print(f"=== walk-forward: {len(windows)} rolling windows "
          f"({args.window_days}d each, step {args.step_days}d) ===")
    print(f"  span {args.data_start} .. {args.data_end}\n")
    if not windows:
        print("  No windows fit in the span. Widen --data-start/--data-end or")
        print("  shrink --window-days. Inconclusive.")
        return

    rows = []
    for i, (ws, we) in enumerate(windows, 1):
        cfg = dataclasses.replace(BacktestConfig(), start=ws, end=we)
        sel = TrailingAlphaSelector(cfg.selection)
        modeled = BacktestEngine(trades, markets, res, empty_prices, sel, cfg,
                                 prices_root=args.root).run()
        sel2 = TrailingAlphaSelector(cfg.selection)
        zero = BacktestEngine(trades, markets, res, empty_prices, sel2, cfg,
                              latency_model=LatencyModel(ZERO_LATENCY),
                              prices_root=args.root).run()
        m, z = modeled.summary, zero.summary
        rows.append({
            "window": f"{ws}..{we}",
            "filled": modeled.n_filled,
            "roi_modeled": m.get("total_roi", float("nan")),
            "roi_zero": z.get("total_roi", float("nan")),
            "sharpe_modeled": m.get("sharpe", float("nan")),
            "n_trades": m.get("n_trades", 0),
        })
        print(f"  [{i}/{len(windows)}] {ws}..{we}  "
              f"filled={modeled.n_filled:3d}  "
              f"roi_modeled={m.get('total_roi', float('nan')):+.4f}  "
              f"roi_zero={z.get('total_roi', float('nan')):+.4f}")

    df = pd.DataFrame(rows)
    mod = df["roi_modeled"].dropna()
    zero = df["roi_zero"].dropna()
    total_filled = int(df["filled"].sum())

    print("\n=== MODELED-LATENCY ROI DISTRIBUTION (the number that counts) ===")
    print(f"  windows: {len(mod)}   total filled trades across windows: {total_filled}")
    if len(mod):
        print(f"  mean   : {mod.mean():+.4f}")
        print(f"  median : {mod.median():+.4f}")
        print(f"  std    : {mod.std():.4f}")
        print(f"  min    : {mod.min():+.4f}    max: {mod.max():+.4f}")
        neg = int((mod < 0).sum())
        pos = int((mod > 0).sum())
        print(f"  windows negative: {neg}/{len(mod)} ({neg/len(mod):.0%})   "
              f"positive: {pos}/{len(mod)} ({pos/len(mod):.0%})")

    print("\n  zero-latency upper bound (for reference):")
    if len(zero):
        print(f"    mean {zero.mean():+.4f}   median {zero.median():+.4f}   "
              f"{int((zero>0).sum())}/{len(zero)} positive")

    print("\n=== VERDICT (pre-stated reading rule) ===")
    if not len(mod):
        print("  No valid windows. Inconclusive.")
        return
    frac_neg = (mod < 0).mean()
    frac_pos = (mod > 0).mean()
    crosses_zero = mod.min() < 0 < mod.max()
    if frac_neg >= 0.80 and mod.mean() < 0:
        print(f"  {frac_neg:.0%} of windows are negative with a negative mean")
        print(f"  ({mod.mean():+.4f}). The single-split -6.26% was NOT a fluke —")
        print("  the modeled-latency edge is robustly negative across the data.")
        print("  §4.1 fragility was small-sample noise around a negative mean;")
        print("  the NO-GO leg is sound.")
    elif frac_pos >= 0.80 and mod.mean() > 0:
        print(f"  {frac_pos:.0%} of windows are POSITIVE with a positive mean")
        print(f"  ({mod.mean():+.4f}). This would CONTRADICT the single-split")
        print("  -6.26% and the §4.1 NO-GO leg. If this appears on real data it")
        print("  is a major finding that must be reconciled against §4.2/§4.4")
        print("  before any conclusion — do NOT celebrate; investigate why the")
        print("  single split disagreed (window choice, trade mix, an error).")
    elif crosses_zero and abs(mod.mean()) < mod.std():
        print(f"  ROIs straddle zero (min {mod.min():+.4f}, max {mod.max():+.4f})")
        print(f"  and the mean ({mod.mean():+.4f}) is within one std ({mod.std():.4f})")
        print("  of zero. The data CANNOT distinguish a modest positive from a")
        print("  modest negative for the backtest leg. This is the honest answer:")
        print("  §4.1 is underpowered on this dataset regardless of slicing. The")
        print("  verdict must rest on the non-trade-count-fragile legs (§4.2")
        print("  edge-at-instant, §4.4 exit-mirror), NOT on the backtest ROI.")
    else:
        print(f"  Mixed: mean {mod.mean():+.4f}, {frac_neg:.0%} negative, "
              f"range [{mod.min():+.4f}, {mod.max():+.4f}].")
        print("  Not a clean verdict in either direction. Report the full")
        print("  distribution honestly; treat §4.1 as suggestive, not decisive,")
        print("  and lean on §4.2/§4.4 for the overall verdict.")

    print("\n  NOTE: windows overlap, so these are NOT independent samples — this")
    print("  is a stability/power diagnostic, not a significance test. It shows")
    print("  whether the backtest ROI is consistently signed or noise around zero.")


if __name__ == "__main__":
    main()
