"""Edge half-life + niche finder — honest version.

Answers two questions against the data already on disk:

  1. How fast does a selected wallet's edge decay after they trade?
     (the "edge half-life" — the latency budget for any live system)

  2. Is there a market SEGMENT, defined by a mechanism stated in advance,
     where the edge half-life is long enough that the strategy survives
     realistic entry delay?

ANTI-OVERFITTING DISCIPLINE (read this before trusting any output):
  - Segments are defined by MECHANISMS chosen up front (time-to-resolution
    bucket, market activity/liquidity tier), NOT by slicing 22k markets
    until something looks green.
  - Every segment is scored on a TRAIN window and then re-scored on a
    held-out TEST window it played no part in choosing. A segment that is
    only positive in-sample is reported as OVERFIT, not as a win.
  - The unfiltered baseline is always printed alongside, so a filter that
    does nothing can't masquerade as a discovery.

This script only MEASURES. It does not change the strategy. A negative
result here is the honest answer, same as the backtest.

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/edge_halflife.py --root ~/data
"""
from __future__ import annotations

import argparse
import pathlib
from datetime import date

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.selection import TrailingAlphaSelector
from pm_research.config import SelectionConfig


# delays at which we measure the entry edge (the decay curve x-axis)
DELAYS = [
    ("0 (instant)", pd.Timedelta(0)),
    ("5 min", pd.Timedelta(minutes=5)),
    ("30 min", pd.Timedelta(minutes=30)),
    ("2 h", pd.Timedelta(hours=2)),
    ("12 h", pd.Timedelta(hours=12)),
    ("48 h", pd.Timedelta(hours=48)),
]


def _price_at(series: pd.Series, ts: pd.Timestamp) -> float | None:
    """As-of (last price at or before ts) from an hourly yes_price series."""
    if series is None or len(series) == 0:
        return None
    idx = series.index.searchsorted(ts, side="right") - 1
    if idx < 0:
        return None
    return float(series.iloc[idx])


def load_price_series(prices_root: pathlib.Path, cid: str) -> pd.Series | None:
    p = prices_root / "prices" / cid
    for ext in (".parquet", ".pkl"):
        fp = p.with_suffix(ext)
        if fp.exists():
            df = pd.read_parquet(fp) if ext == ".parquet" else pd.read_pickle(fp)
            if df.empty:
                return None
            return df.set_index("ts")["yes_price"].sort_index()
    return None


def build_copy_events(store: Store, root: pathlib.Path,
                      start: date, end: date) -> pd.DataFrame:
    """For each trade a SELECTED wallet made in [start, end] on a market that
    later resolved, record what entering at delay Δ would have returned.

    Edge at delay Δ = (resolution payout) − (price you'd pay entering Δ later).
    Payout is 1.0 if the wallet's chosen outcome won, else 0.0.
    Positive mean edge = profitable on average BEFORE impact/fees.
    """
    trades = store.load_trades()
    res = store.load_resolutions()
    winner = dict(zip(res["condition_id"], res["winning_outcome"]))
    res_at = dict(zip(res["condition_id"], res["resolved_at"]))

    sel = TrailingAlphaSelector(SelectionConfig())

    s = pd.Timestamp(start, tz="UTC")
    e = pd.Timestamp(end, tz="UTC")
    win = trades[(trades["traded_at"] >= s) & (trades["traded_at"] < e)]

    # Select the universe AS OF the window start, using only history that
    # precedes the window. This is point-in-time honest (no lookahead into
    # the period we're about to measure) and avoids picking wallets using
    # the very trades whose edge we're scoring.
    universe = set(sel.select(trades, res, s))
    if not universe:
        # fall back: widen as-of slightly if the exact boundary is too sparse
        universe = set(sel.select(trades, res, s + pd.Timedelta(days=1)))
    win = win[win["wallet"].isin(universe)]
    # only markets that actually resolved (we know the payout) and have prices
    win = win[win["condition_id"].isin(winner)]

    rows = []
    series_cache: dict[str, pd.Series | None] = {}
    cids = win["condition_id"].unique()
    for j, cid in enumerate(cids, 1):
        if cid not in series_cache:
            series_cache[cid] = load_price_series(root, cid)
        series = series_cache[cid]
        if series is None:
            continue
        won_outcome = winner[cid]
        resolved_at = pd.Timestamp(res_at[cid])
        sub = win[win["condition_id"] == cid]
        for _, t in sub.iterrows():
            t0 = t["traded_at"]
            outcome = t["outcome"]
            payout = 1.0 if outcome == won_outcome else 0.0
            ttr_hours = (resolved_at - t0).total_seconds() / 3600.0
            if ttr_hours <= 0:
                continue  # traded at/after resolution; skip
            rec = {"condition_id": cid, "wallet": t["wallet"],
                   "outcome": outcome, "traded_at": t0,
                   "ttr_hours": ttr_hours, "size_usdc": t["size_usdc"],
                   "n_price_obs": len(series)}
            for label, dt in DELAYS:
                entry_ts = t0 + dt
                if entry_ts >= resolved_at:
                    rec[label] = np.nan       # delay would miss resolution
                    continue
                yes_p = _price_at(series, entry_ts)
                if yes_p is None:
                    rec[label] = np.nan
                    continue
                entry_price = yes_p if outcome == "YES" else 1.0 - yes_p
                rec[label] = payout - entry_price   # edge in [−1, 1]
            rows.append(rec)
        if j % 200 == 0:
            print(f"  scanned {j}/{len(cids)} markets, {len(rows)} copy events")
    return pd.DataFrame(rows)


def decay_table(ev: pd.DataFrame) -> pd.DataFrame:
    """Mean edge at each delay, plus the half-life readout."""
    out = []
    base = None
    for label, _ in DELAYS:
        col = ev[label].dropna()
        m = col.mean() if len(col) else np.nan
        if base is None:
            base = m
        frac = (m / base) if (base and base != 0) else np.nan
        out.append({"delay": label, "mean_edge": m, "n": len(col),
                    "frac_of_instant": frac})
    return pd.DataFrame(out)


def summarize_segment(ev: pd.DataFrame, name: str) -> dict:
    """One-line health readout for a segment, at instant vs 2h delay."""
    inst = ev["0 (instant)"].dropna()
    d2h = ev["2 h"].dropna()
    return {"segment": name, "events": len(ev),
            "edge_instant": inst.mean() if len(inst) else np.nan,
            "edge_2h": d2h.mean() if len(d2h) else np.nan,
            "win_rate": (inst > 0).mean() if len(inst) else np.nan}


# ---- segment definitions: MECHANISMS chosen in advance, not green-hunted ---
def segment_by_ttr(ev: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Time-to-resolution buckets — available for ALL resolved markets.
    Hypothesis stated in advance: longer-dated markets diffuse information
    more slowly, so the edge should survive entry delay better."""
    return {
        "ttr <24h (fast)":   ev[ev["ttr_hours"] < 24],
        "ttr 1-7d":          ev[(ev["ttr_hours"] >= 24) & (ev["ttr_hours"] < 168)],
        "ttr 7-30d":         ev[(ev["ttr_hours"] >= 168) & (ev["ttr_hours"] < 720)],
        "ttr >30d (slow)":   ev[ev["ttr_hours"] >= 720],
    }


def segment_by_activity(ev: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Price-observation count as a liquidity/attention proxy — available for
    ALL markets (it's just the length of the price series). Hypothesis stated
    in advance: thinly-traded markets carry more durable private edge (but
    watch impact)."""
    q = ev["n_price_obs"]
    if q.empty:
        return {}
    lo, hi = q.quantile(0.33), q.quantile(0.66)
    return {
        "thin (low activity)":   ev[ev["n_price_obs"] <= lo],
        "mid":                   ev[(ev["n_price_obs"] > lo) & (ev["n_price_obs"] <= hi)],
        "thick (high activity)": ev[ev["n_price_obs"] > hi],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    store = Store(str(root))

    # Honest train/test split: choose any favorable segment on TRAIN, then
    # confirm on TEST which had no role in the choice.
    mid = pd.Timestamp(args.start, tz="UTC") + (
        pd.Timestamp(args.end, tz="UTC") - pd.Timestamp(args.start, tz="UTC")) / 2
    mid_date = mid.date()

    print(f"=== TRAIN window {args.start} .. {mid_date} ===")
    ev_train = build_copy_events(store, root, args.start, mid_date)
    print(f"  {len(ev_train)} copy events on train\n")

    print(f"=== TEST window {mid_date} .. {args.end} (held out) ===")
    ev_test = build_copy_events(store, root, mid_date, args.end)
    print(f"  {len(ev_test)} copy events on test\n")

    if ev_train.empty or ev_test.empty:
        print("Not enough copy events to analyse. Edge undefined on this data.")
        return

    print("=== OVERALL EDGE DECAY (train) ===")
    print(decay_table(ev_train).to_string(index=False))
    print("\n  half-life readout: the delay where frac_of_instant first")
    print("  drops below 0.5 is your latency budget. If mean_edge is already")
    print("  <= 0 at instant, there is no edge to decay.\n")

    print("=== BASELINE (no filter) ===")
    base_tr = summarize_segment(ev_train, "ALL (train)")
    base_te = summarize_segment(ev_test, "ALL (test)")
    print(pd.DataFrame([base_tr, base_te]).to_string(index=False))
    print()

    for seg_name, seg_fn in [("TIME-TO-RESOLUTION", segment_by_ttr),
                             ("ACTIVITY/LIQUIDITY PROXY", segment_by_activity)]:
        print(f"=== SEGMENT: {seg_name} ===")
        tr_segs = seg_fn(ev_train)
        te_segs = seg_fn(ev_test)
        rows = []
        for k in tr_segs:
            tr = summarize_segment(tr_segs[k], k + " [train]")
            te = summarize_segment(te_segs.get(k, ev_test.iloc[0:0]), k + " [test]")
            rows.append(tr)
            rows.append(te)
        tbl = pd.DataFrame(rows)
        print(tbl.to_string(index=False))

        # honest verdict per segment: positive on BOTH train and test 2h-delay
        print("\n  verdict (edge_2h must be > 0 on BOTH train and test):")
        for k in tr_segs:
            tr2 = summarize_segment(tr_segs[k], k)["edge_2h"]
            te2 = summarize_segment(te_segs.get(k, ev_test.iloc[0:0]), k)["edge_2h"]
            if pd.notna(tr2) and pd.notna(te2) and tr2 > 0 and te2 > 0:
                tag = "SURVIVES (candidate niche)"
            elif pd.notna(tr2) and tr2 > 0 and (pd.isna(te2) or te2 <= 0):
                tag = "OVERFIT (train-only, do NOT trust)"
            else:
                tag = "no edge at 2h delay"
            print(f"    {k:28s} train_2h={tr2: .4f}  test_2h={te2 if pd.notna(te2) else float('nan'): .4f}  -> {tag}")
        print()

    print("=== HOW TO READ THIS ===")
    print("  edge_instant  : avg profit per $1 if you entered at the leader's price")
    print("  edge_2h       : same, entering 2h later (realistic detection lag)")
    print("  A niche is real ONLY if edge_2h > 0 on the held-out TEST window.")
    print("  Train-only positives are overfitting and are flagged as such.")
    print("  If nothing survives on test, the honest answer is: no tradable")
    print("  niche in this data. That is a valid, valuable result.")


if __name__ == "__main__":
    main()
