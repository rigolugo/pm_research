"""Wallet behavioral classifier — market maker vs directional trader.

WHY. The exit-mirror backtest proved the volume-ranked wallets make money by
liquidity provision (market-making), which a latency-bound copier cannot
capture. But that population was selected by raw VOLUME, which over-selects
exactly those market makers. The untested hypothesis is whether the
DIRECTIONAL traders in the data — the ones making genuine forward bets and
holding them — carry information a slower strategy could use.

This module classifies each wallet by behavioral MECHANISM (stated up front,
not fit to an outcome), so downstream experiments can split the population.
It is a TOOL, not a strategy. It produces no PnL claim.

The five tells (each a structural difference between the two roles):
  sell_buy_ratio      MMs cycle inventory constantly        -> high for MM
  two_sided_rate      MMs quote BOTH sides of a market       -> high for MM
  roundtrip_rate      MMs exit before resolution             -> high for MM
  median_hold_hours   MMs flip fast                          -> low for MM
  market_breadth      MMs spread thin across many markets    -> high for MM

A wallet is flagged MARKET_MAKER if it shows the MM signature on a majority
of these. DIRECTIONAL otherwise. The threshold is explicit and tunable; the
point is a transparent rule, not a black box.

HONESTY NOTES:
  - This classifies BEHAVIOUR, not skill. A market maker can be highly
    skilled; the point is only that their skill is uncopyable by a taker.
  - 'two_sided_rate' needs SELLs and both-outcome trades to be meaningful;
    if the data is BUY-only or single-sided, that tell degrades gracefully
    and the function says so rather than inventing a value.
  - No outcome/resolution data is used. Classification is purely from trade
    BEHAVIOUR, so it cannot leak lookahead into any downstream test.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


CLASSIFIER_COLS = ["wallet", "n_trades", "sell_buy_ratio", "two_sided_rate",
                   "roundtrip_rate", "median_hold_hours", "market_breadth",
                   "mm_score", "label"]


def _wallet_behavior(g: pd.DataFrame) -> dict:
    """Behavioral tells for one wallet's trades (no outcome data used)."""
    n = len(g)
    n_buy = int((g["side"] == "BUY").sum())
    n_sell = int((g["side"] == "SELL").sum())
    sell_buy = (n_sell / n_buy) if n_buy else (np.nan if n_sell == 0 else np.inf)

    # two-sided: markets where the wallet traded BOTH YES and NO
    per_mkt_sides = g.groupby("condition_id")["outcome"].nunique()
    two_sided_rate = float((per_mkt_sides >= 2).mean()) if len(per_mkt_sides) else 0.0

    # round-trips and hold duration: per (market, outcome), pair buys with
    # later sells. A position is 'round-tripped' if it has >=1 buy and >=1
    # sell. Hold = time from first buy to first sell.
    rt_flags, holds = [], []
    for (_cid, _oc), h in g.groupby(["condition_id", "outcome"]):
        buys = h[h["side"] == "BUY"]
        sells = h[h["side"] == "SELL"]
        if len(buys) and len(sells):
            rt_flags.append(1)
            first_buy = buys["traded_at"].min()
            first_sell = sells["traded_at"].min()
            if first_sell > first_buy:
                holds.append((first_sell - first_buy).total_seconds() / 3600.0)
        elif len(buys):
            rt_flags.append(0)
    roundtrip_rate = float(np.mean(rt_flags)) if rt_flags else 0.0
    median_hold = float(np.median(holds)) if holds else np.nan

    market_breadth = int(g["condition_id"].nunique())

    return {"n_trades": n, "sell_buy_ratio": sell_buy,
            "two_sided_rate": two_sided_rate, "roundtrip_rate": roundtrip_rate,
            "median_hold_hours": median_hold, "market_breadth": market_breadth}


def classify(trades: pd.DataFrame,
             sell_buy_hi: float = 0.4,
             two_sided_hi: float = 0.15,
             roundtrip_hi: float = 0.4,
             hold_lo_hours: float = 48.0,
             breadth_hi: int = 50,
             min_trades: int = 20,
             min_score: int = 3) -> pd.DataFrame:
    """Classify each wallet as MARKET_MAKER or DIRECTIONAL.

    Thresholds are explicit and stated in advance. A wallet scores one MM
    point per tell it trips; reaching `min_score` of the 5 tells (default 3,
    a majority) -> MARKET_MAKER. Wallets below `min_trades` are labeled
    UNKNOWN (too little behaviour to judge).
    """
    rows = []
    for wallet, g in trades.groupby("wallet"):
        b = _wallet_behavior(g)
        b["wallet"] = wallet
        if b["n_trades"] < min_trades:
            b["mm_score"] = np.nan
            b["label"] = "UNKNOWN"
            rows.append(b)
            continue
        # sell_buy_ratio is a float when n_buy>0, np.inf for an all-SELL
        # wallet (n_buy==0, n_sell>0 -> maximally MM-like, trips the tell),
        # or np.nan only in the degenerate no-trade case. The previous guard
        # used `is not np.nan`, an IDENTITY test that is unreliable for NaN
        # (fresh float NaNs are not the np.nan singleton) and so never
        # actually fired. pd.notna() handles NaN correctly; inf passes the
        # >= comparison as intended.
        sbr = b["sell_buy_ratio"]
        sbr_tell = bool(pd.notna(sbr) and sbr >= sell_buy_hi)
        # median_hold_hours is NaN when the wallet never round-tripped a
        # position (no buy->sell pair). A wallet that never closes is NOT
        # behaving like a fast-flipping MM, so a NaN hold must NOT trip the
        # "holds briefly" tell. pd.notna() guards that.
        mh = b["median_hold_hours"]
        hold_tell = bool(pd.notna(mh) and mh <= hold_lo_hours)
        tells = [
            sbr_tell,
            (b["two_sided_rate"] >= two_sided_hi),
            (b["roundtrip_rate"] >= roundtrip_hi),
            hold_tell,
            (b["market_breadth"] >= breadth_hi),
        ]
        score = int(sum(bool(x) for x in tells))
        b["mm_score"] = score
        b["label"] = "MARKET_MAKER" if score >= min_score else "DIRECTIONAL"
        rows.append(b)
    df = pd.DataFrame(rows, columns=CLASSIFIER_COLS)
    return df


def main() -> None:
    import argparse
    from datetime import date
    from pm_research.data.store import Store

    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=None)
    ap.add_argument("--end", type=date.fromisoformat, default=None)
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades()
    if args.start:
        trades = trades[trades["traded_at"] >= pd.Timestamp(args.start, tz="UTC")]
    if args.end:
        trades = trades[trades["traded_at"] < pd.Timestamp(args.end, tz="UTC")]

    # honesty gate: is there enough SELL/two-sided behaviour to classify?
    sell_frac = (trades["side"] == "SELL").mean() if len(trades) else 0.0
    print(f"=== data check: {len(trades)} trades, SELL fraction {sell_frac:.3f} ===")
    if sell_frac < 0.01:
        print("  WARNING: near BUY-only data. sell_buy_ratio, roundtrip_rate and")
        print("  hold-duration tells will be degenerate. Classification will lean")
        print("  on two_sided_rate and breadth only — interpret with caution.\n")

    df = classify(trades)
    counts = df["label"].value_counts()
    print("=== wallet classification ===")
    print(counts.to_string())
    print()
    judged = df[df["label"] != "UNKNOWN"]
    if len(judged):
        print("  by label, median behavioral tells:")
        summary = judged.groupby("label")[
            ["sell_buy_ratio", "two_sided_rate", "roundtrip_rate",
             "median_hold_hours", "market_breadth"]].median()
        print(summary.to_string())
    print(f"\n  DIRECTIONAL wallets: {int((df['label']=='DIRECTIONAL').sum())}")
    print("  These are the untested population: traders who mostly buy and")
    print("  hold, NOT liquidity providers. The next experiment asks whether")
    print("  THEIR consensus is informative out-of-sample.")


if __name__ == "__main__":
    main()
