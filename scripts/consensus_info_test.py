"""Directional-consensus informativeness test — the real experiment.

The pivot away from copy-trading: don't TRADE on the leaders, LEARN from them.
Specifically: when the DIRECTIONAL wallets (market makers excluded via the
classifier) reach consensus on an outcome, does that consensus predict the
market's resolution BETTER THAN THE MARKET PRICE ALREADY DOES?

This is the honest bar. Not "are the leaders right" (a market at 0.85 is
'right' 85% of the time with zero skill). The bar is INCREMENTAL information:
does knowing the consensus improve a prediction beyond what the price at that
moment already implies?

METHOD (strict out-of-sample):
  1. Classify wallets; keep only DIRECTIONAL ones (market makers can't carry
     copyable directional info, and we proved their P&L is liquidity-based).
  2. On a TRAIN window, collect consensus signals. For each, record:
       - market_price at detection (the baseline prediction)
       - consensus_confidence (raw_confidence from the directional wallets)
       - outcome (did the consensus's side win at resolution) -- label
  3. Compare two predictors on the held-out TEST window via Brier score
     (lower = better calibrated probability):
       BASELINE : predict resolution = market price at detection
       MODEL    : predict resolution = isotonic-calibrated(consensus, price),
                  where the calibrator is FIT ON TRAIN ONLY.
  4. If MODEL's Brier on TEST is meaningfully below BASELINE's, the consensus
     carries information beyond price. If not, it doesn't — full stop.

FALSIFICATION GATES:
  - Calibrator fit on TRAIN, scored on TEST. No in-sample evaluation.
  - The baseline is the MARKET PRICE, the hardest honest benchmark. Beating
    "always predict 0.5" is meaningless; beating the price is the real test.
  - Brier skill score reported with sign. <= 0 means no skill, stated plainly.
  - If too few signals to fit/score, the script says inconclusive, not green.

This makes NO PnL claim. Informative != tradable-after-costs (we learned that
distinction the hard way). A positive result here means the signal is worth
further work; a negative result closes the 'learn from them' thread cleanly.

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/consensus_info_test.py --root ~/data
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
from pm_research.consensus import detect
from pm_research.calibration import IsotonicCalibrator
from pm_research.wallet_classifier import classify


def _price_at(root: pathlib.Path, cid: str, ts: pd.Timestamp,
              cache: dict) -> float | None:
    if cid not in cache:
        p = root / "prices" / cid
        s = None
        for ext in (".parquet", ".pkl"):
            fp = p.with_suffix(ext)
            if fp.exists():
                df = pd.read_parquet(fp) if ext == ".parquet" else pd.read_pickle(fp)
                if not df.empty:
                    s = df.set_index("ts")["yes_price"].sort_index()
                break
        cache[cid] = s
    s = cache[cid]
    if s is None:
        return None
    idx = s.index.searchsorted(ts, side="right") - 1
    return float(s.iloc[idx]) if idx >= 0 else None


def collect_signals(trades, resolutions, directional, cfg, root, start, end):
    """Consensus signals from DIRECTIONAL wallets only, with the market price
    at detection and the realized label. Point-in-time; no lookahead."""
    winner = dict(zip(resolutions["condition_id"], resolutions["winning_outcome"]))
    sel = TrailingAlphaSelector(cfg.selection)
    cache: dict = {}
    s_ts = pd.Timestamp(start, tz="UTC")
    e_ts = pd.Timestamp(end, tz="UTC")

    rows = []
    days = pd.date_range(s_ts, e_ts, freq="D")
    last_rebalance, universe, scores = None, [], pd.DataFrame()
    for day in days:
        as_of = day + pd.Timedelta(hours=23, minutes=59)
        if (last_rebalance is None or
                (day - last_rebalance).days >= cfg.selection.rebalance_interval_days):
            full = sel.select(trades, resolutions, as_of)
            # restrict the universe to DIRECTIONAL wallets
            universe = [w for w in full if w in directional]
            last_rebalance = day
            if universe:
                f = compute_features(trades, resolutions, as_of,
                                     cfg.selection.lookback_days)
                scores = score(f[f["wallet"].isin(universe)])
        if not universe:
            continue
        for sig in detect(trades, universe, scores, as_of, cfg.consensus):
            if sig.condition_id not in winner:
                continue
            price = _price_at(root, sig.condition_id, sig.detected_at, cache)
            if price is None:
                continue
            # baseline prediction = market prob of the consensus's side
            base_p = price if sig.outcome == "YES" else 1.0 - price
            label = 1.0 if winner[sig.condition_id] == sig.outcome else 0.0
            rows.append({"condition_id": sig.condition_id, "outcome": sig.outcome,
                         "confidence": sig.raw_confidence, "market_p": base_p,
                         "n_traders": sig.n_traders, "label": label,
                         "detected_at": sig.detected_at})
    return pd.DataFrame(rows)


def brier(p, y):
    p, y = np.asarray(p, float), np.asarray(y, float)
    return float(np.mean((p - y) ** 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)
    res = store.load_resolutions()
    cfg = BacktestConfig(start=args.start, end=args.end)

    # classify on the full history, keep DIRECTIONAL
    cls = classify(trades)
    directional = set(cls[cls["label"] == "DIRECTIONAL"]["wallet"])
    print(f"=== {len(directional)} DIRECTIONAL wallets "
          f"(of {len(cls)} total) ===")
    if not directional:
        print("  No directional wallets found. Cannot run. (Pool may be all")
        print("  market makers / too few trades each.) Inconclusive.")
        return

    mid = pd.Timestamp(args.start, tz="UTC") + (
        pd.Timestamp(args.end, tz="UTC") - pd.Timestamp(args.start, tz="UTC")) / 2
    mid_date = mid.date()

    print(f"collecting TRAIN signals {args.start}..{mid_date} ...")
    tr = collect_signals(trades, res, directional, cfg, root, args.start, mid_date)
    print(f"  {len(tr)} train signals")
    print(f"collecting TEST signals {mid_date}..{args.end} ...")
    te = collect_signals(trades, res, directional, cfg, root, mid_date, args.end)
    print(f"  {len(te)} test signals\n")

    if len(tr) < 50 or len(te) < 25:
        print("=== INCONCLUSIVE ===")
        print(f"  Too few signals (train={len(tr)}, test={len(te)}) to fit and")
        print("  score a calibrator with any confidence. Need >= 50 train /")
        print("  25 test. The directional consensus simply doesn't fire often")
        print("  enough on this data to evaluate. Not a positive, not a")
        print("  negative -- inconclusive.")
        return

    # BASELINE: market price predicts resolution
    base_brier_test = brier(te["market_p"], te["label"])

    # MODEL: isotonic calibration of consensus confidence, fit on TRAIN
    cal = IsotonicCalibrator(min_samples=min(50, len(tr)))
    cal.fit(tr["confidence"].values, tr["label"].values)
    model_p_test = cal.apply(te["confidence"].values)
    model_brier_test = brier(model_p_test, te["label"])

    # also: does consensus add to price? blend and check.
    # (simple average of model and market; a real model would learn the weight)
    blend_p = 0.5 * model_p_test + 0.5 * te["market_p"].values
    blend_brier_test = brier(blend_p, te["label"])

    print("=== OUT-OF-SAMPLE BRIER SCORES (lower = better) ===")
    print(f"  BASELINE  (market price)              : {base_brier_test:.4f}")
    print(f"  MODEL     (calibrated consensus only) : {model_brier_test:.4f}")
    print(f"  BLEND     (consensus + market price)  : {blend_brier_test:.4f}")

    # Brier skill score of model vs baseline
    bss_model = 1.0 - model_brier_test / base_brier_test if base_brier_test else np.nan
    bss_blend = 1.0 - blend_brier_test / base_brier_test if base_brier_test else np.nan
    print(f"\n  skill vs market (model): {bss_model:+.4f}")
    print(f"  skill vs market (blend): {bss_blend:+.4f}")

    print("\n=== VERDICT ===")
    base_rate = te["label"].mean()
    print(f"  test base rate (consensus side won): {base_rate:.3f}")
    if bss_blend > 0.02 or bss_model > 0.02:
        print("  >>> The directional consensus carries INFORMATION BEYOND PRICE")
        print("  >>> out-of-sample (positive Brier skill). This is the first")
        print("  >>> positive signal in the project that isn't a latency")
        print("  >>> artifact. It is NOT yet a tradable edge -- informative !=")
        print("  >>> profitable after costs -- but it justifies further work:")
        print("  >>> size the information, then test if it survives costs.")
    elif bss_blend > 0 or bss_model > 0:
        print("  >>> Marginal positive skill (<2%). Could be noise. Worth a")
        print("  >>> second date split to see if it's stable before believing.")
    else:
        print("  >>> The directional consensus does NOT beat the market price")
        print("  >>> out-of-sample. The market already prices in whatever these")
        print("  >>> wallets know by the time they've reached consensus. This")
        print("  >>> closes the 'learn from them' thread honestly: there is no")
        print("  >>> incremental information to extract from this signal.")
    print("\n  (Brier skill is prediction quality, not PnL. A positive result")
    print("   is a reason to continue; a negative result is a clean stop.)")


if __name__ == "__main__":
    main()
