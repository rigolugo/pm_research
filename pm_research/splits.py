"""Rolling train/test split construction — SHARED by the market-structure audit
and the future forecast_vs_price probe so they count signals identically.

A "split" is a (train_window, test_window) pair: the calibrator is fit on the
train window and scored on the test window that immediately follows it. Splits
advance across the data span. This is DELIBERATELY different from
walk_forward_backtest.py's single-window design — the forecast probe needs a
fit-then-score structure, so train precedes test within each split.

The audit and the probe MUST use this same function, or the audit's
signal-count gate (>=100 train, >=50 test per split, >=4/5 splits) would be
measuring a different partition than the probe actually runs. One source of
truth on purpose.
"""
from __future__ import annotations

from datetime import date, timedelta


def rolling_train_test_splits(span_start: date, span_end: date,
                              n_splits: int = 5,
                              train_frac: float = 0.6):
    """Return a list of (train_start, train_end, test_start, test_end) tuples.

    The span [span_start, span_end) is divided into n_splits overlapping
    segments advancing by a fixed step. Within each segment the first
    `train_frac` is train and the remainder is test (test immediately follows
    train, no gap, no overlap between this split's train and test).

    Segments overlap across splits (like walk-forward), so splits are NOT
    independent — this is a stability/power design, not an independence claim,
    and the probe must state that caveat exactly as walk_forward_backtest.py does.
    """
    if n_splits < 1:
        raise ValueError(f"n_splits must be >= 1, got {n_splits}")
    if not (0.0 < train_frac < 1.0):
        raise ValueError(f"train_frac must be in (0,1), got {train_frac}")
    total_days = (span_end - span_start).days
    if total_days <= 0:
        raise ValueError("span_end must be after span_start")

    # Each segment is sized so n_splits segments tile the span with a uniform
    # step; segments overlap when n_splits>1. Segment length is chosen so the
    # last segment ends at span_end.
    if n_splits == 1:
        seg_len = total_days
        step = 0
    else:
        # segment length = total / (1 + (n_splits-1)*(1-overlap)); we use a
        # simple, explicit construction: step = total/(n_splits+1), seg = 2*step
        # so consecutive segments overlap by ~50% and the last ends at span_end.
        step = total_days // (n_splits + 1)
        seg_len = total_days - step * (n_splits - 1)

    splits = []
    for i in range(n_splits):
        seg_start = span_start + timedelta(days=step * i)
        seg_end = seg_start + timedelta(days=seg_len)
        if seg_end > span_end:
            seg_end = span_end
        train_days = int((seg_end - seg_start).days * train_frac)
        train_start = seg_start
        train_end = seg_start + timedelta(days=train_days)
        test_start = train_end
        test_end = seg_end
        splits.append((train_start, train_end, test_start, test_end))
    return splits
