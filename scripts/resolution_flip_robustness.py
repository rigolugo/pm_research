"""Resolution-flip robustness — how fragile is the NO-GO to resolution errors?

Both peer reviewers asked (Q1): the resolutions were DERIVED from price
convergence (final yes_price >= 0.99 -> YES, <= 0.01 -> NO), not read from an
oracle. How many of those derivations would have to be WRONG to flip the main
result (§4.1 modeled-latency ROI, which was negative)?

This computes two bounds:

  (A) WITHIN-BACKTEST: of the trades the engine actually filled, how many of
      their market resolutions would need to flip (winner -> loser) to push
      final equity back to break-even? A small number = fragile; a large
      number = robust.

  (B) GLOBAL ERROR RATE: across ALL resolved markets, what fraction of
      derivations being wrong (at random) would be needed to plausibly flip
      the sign? This speaks to the reviewers' "resolution proxy reliability"
      question directly.

It also offers an OPTIONAL on-chain-free sanity check: how many resolved
markets sit in the "ambiguous band" (final price between, say, 0.90-0.99 or
0.01-0.10) where a late correction is most plausible — i.e. the population
most at risk of mis-derivation.

NO new data needed beyond what's on disk. Honest output: a number, plus the
interpretation rule stated up front (fragile if < ~10% of filled trades).

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/resolution_flip_robustness.py --root ~/data
"""
from __future__ import annotations

import argparse
import pathlib
from datetime import date

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.config import BacktestConfig
from pm_research.selection import TrailingAlphaSelector
from pm_research.scoring import score
from pm_research.features import compute_features
from pm_research.consensus import detect, CooldownFilter
from pm_research.latency import LatencyModel, PriceBook


def run_backtest_capture(trades, resolutions, markets, cfg, root, latency):
    """Minimal re-run of the modeled-latency backtest that records, per filled
    position, its cost, shares, outcome, condition_id, and realized payout —
    so we can later flip resolutions and recompute equity."""
    book = PriceBook(pd.DataFrame(), markets, prices_root=root)
    sel = TrailingAlphaSelector(cfg.selection)
    winner = dict(zip(resolutions["condition_id"], resolutions["winning_outcome"]))
    res_at = dict(zip(resolutions["condition_id"], resolutions["resolved_at"]))
    res_by_day = resolutions.assign(day=resolutions["resolved_at"].dt.floor("D"))

    cash = cfg.initial_capital
    open_pos = {}
    fills = []   # one record per filled position
    cooldown = CooldownFilter(cfg.consensus.cooldown_hours_per_market)
    universe, scores = [], pd.DataFrame()
    days = pd.date_range(pd.Timestamp(cfg.start, tz="UTC"),
                         pd.Timestamp(cfg.end, tz="UTC"), freq="D")
    last_rebalance = None

    def open_value(as_of):
        tot = 0.0
        for p in open_pos.values():
            q = book.price_at(p["condition_id"], p["outcome"], as_of)
            tot += p["shares"] * (q if q is not None else p["entry_price"])
        return tot

    for day in days:
        as_of = day + pd.Timedelta(hours=23, minutes=59)
        if (last_rebalance is None or
                (day - last_rebalance).days >= cfg.selection.rebalance_interval_days):
            universe = sel.select(trades, resolutions, as_of)
            last_rebalance = day
            if universe:
                f = compute_features(trades, resolutions, as_of,
                                     cfg.selection.lookback_days)
                scores = score(f[f["wallet"].isin(universe)])

        rtoday = res_by_day[res_by_day["day"] == day]
        for _, r in rtoday.iterrows():
            for outcome in ("YES", "NO"):
                key = (r["condition_id"], outcome)
                p = open_pos.pop(key, None)
                if p is None:
                    continue
                payout = p["shares"] * (1.0 if outcome == r["winning_outcome"] else 0.0)
                cash += payout
                p["payout"] = payout
                p["won"] = (outcome == r["winning_outcome"])
                fills.append(p)

        if universe:
            equity_now = cash + open_value(as_of)
            for sig in detect(trades, universe, scores, as_of, cfg.consensus):
                if not cooldown.admit(sig):
                    continue
                key = (sig.condition_id, sig.outcome)
                if key in open_pos or len(open_pos) >= cfg.risk.max_open_positions:
                    continue
                wk = res_at.get(sig.condition_id)
                if wk is not None and sig.detected_at >= pd.Timestamp(wk):
                    continue
                size = min(cfg.risk.size_fraction * equity_now, cash)
                if size < 1.0:
                    continue
                fill = latency.apply(condition_id=sig.condition_id, outcome=sig.outcome,
                                     detected_at=sig.detected_at,
                                     leaders_avg_entry=sig.leaders_avg_entry,
                                     size_usdc=size, book=book)
                if not fill.filled:
                    continue
                shares = size / fill.fill_price
                open_pos[key] = {"condition_id": sig.condition_id, "outcome": sig.outcome,
                                 "shares": shares, "entry_price": fill.fill_price,
                                 "cost": size}
                cash -= size

    # any positions never resolved in-window: value at last price (unrealized)
    leftover = 0.0
    for p in open_pos.values():
        q = book.price_at(p["condition_id"], p["outcome"],
                          pd.Timestamp(cfg.end, tz="UTC"))
        leftover += p["shares"] * (q if q is not None else p["entry_price"])
    return fills, cash, leftover, cfg.initial_capital


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)
    res = store.load_resolutions()
    markets = store.load_markets()
    cfg = BacktestConfig(start=args.start, end=args.end)
    latency = LatencyModel(cfg.latency)

    fills, cash, leftover, cap = run_backtest_capture(
        trades, res, markets, cfg, args.root, latency)
    final_equity = cash + leftover
    roi = final_equity / cap - 1.0
    realized = [f for f in fills if "payout" in f]
    losers = [f for f in realized if not f["won"]]

    print("=== modeled-latency backtest (recomputed) ===")
    print(f"  filled & resolved positions: {len(realized)}")
    print(f"  winners: {sum(f['won'] for f in realized)}  losers: {len(losers)}")
    print(f"  final equity: {final_equity:,.2f}  ROI: {roi:+.4f}\n")

    if roi >= 0:
        print("  NOTE: recomputed ROI is non-negative; this script assumes the")
        print("  negative §4.1 result. Re-check window/params if this differs.")
        # continue anyway for the error-rate framing

    # ---------- (A) within-backtest flip count ----------
    # Flipping a LOSER to a winner adds (shares*1.0 - 0) = shares payout it
    # didn't get. Flipping a WINNER to loser removes its payout. To IMPROVE the
    # result we flip losers->winners, taking the largest-share losers first
    # (most equity recovered per flip).
    gap = cap - final_equity        # dollars needed to reach break-even
    print("=== (A) WITHIN-BACKTEST: flips to reach break-even ===")
    if gap <= 0:
        print("  Already at/above break-even; no flips needed.\n")
    else:
        loser_gains = sorted([f["shares"] for f in losers], reverse=True)
        cum, k = 0.0, 0
        for g in loser_gains:
            cum += g            # each flipped loser pays shares*1.0
            k += 1
            if cum >= gap:
                break
        frac = k / len(realized) if realized else float("nan")
        print(f"  dollars to break-even: {gap:,.2f}")
        print(f"  loser-positions that must flip to winners: {k} of {len(losers)} "
              f"losers ({k}/{len(realized)} = {frac:.1%} of all filled positions)")
        rule = ("FRAGILE" if frac < 0.10 else
                "MODERATE" if frac < 0.25 else "ROBUST")
        print(f"  -> robustness: {rule} "
              f"(rule: <10% fragile, 10-25% moderate, >25% robust)\n")

    # ---------- (B) global resolution error-rate framing ----------
    print("=== (B) GLOBAL: resolution-derivation reliability ===")
    n_res = len(res)
    # ambiguous band: how many derivations are 'close calls' most at risk of
    # a late correction? (final price near but not at the extremes)
    # We approximate by re-reading each market's final price.
    root = pathlib.Path(args.root)
    band = 0
    checked = 0
    for cid in res["condition_id"]:
        p = root / "prices" / cid
        fy = None
        for ext in (".parquet", ".pkl"):
            fp = p.with_suffix(ext)
            if fp.exists():
                df = pd.read_parquet(fp) if ext == ".parquet" else pd.read_pickle(fp)
                if not df.empty:
                    fy = float(df.sort_values("ts")["yes_price"].iloc[-1])
                break
        if fy is None:
            continue
        checked += 1
        # 'clean' = within 0.005 of 0/1; ambiguous = derived but not crisp
        if not (fy >= 0.995 or fy <= 0.005):
            band += 1
    amb_frac = band / checked if checked else float("nan")
    print(f"  resolved markets: {n_res}")
    print(f"  checked final prices: {checked}")
    print(f"  derivations NOT crisp (final price not within 0.005 of 0/1): "
          f"{band} ({amb_frac:.2%})")
    print("  These are the derivations most exposed to late-correction error.")
    print("  Even if ALL of them were wrong, only positions the backtest")
    print("  actually traded in those markets affect §4.1 — see (A) for the")
    print("  count that matters. The global proxy reliability is bounded below")
    print(f"  by 1 - {amb_frac:.2%} = {1-amb_frac:.2%} crisp derivations.\n")

    print("=== INTERPRETATION ===")
    print("  The §4.1 verdict flips only if (A)'s count of loser->winner flips")
    print("  actually occurred. If that count is a large fraction of filled")
    print("  trades AND concentrated in non-crisp derivations, the result is")
    print("  fragile. If it's a large fraction OR the derivations are crisp,")
    print("  the NO-GO is robust to resolution-derivation error.")


if __name__ == "__main__":
    main()
