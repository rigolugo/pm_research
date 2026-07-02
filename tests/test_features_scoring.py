"""Features + scoring tests: hand-computed values and the no-lookahead guard."""
from __future__ import annotations

import pandas as pd

from pm_research.features import compute_features
from pm_research.scoring import score
from tests.helpers import make_resolutions, make_trades, ts


def test_features_hand_computed_roi_and_win_rate():
    trades = make_trades([
        # wallet A: wins a 0.50 buy (roi +1.0), loses a 0.25 buy (roi -1.0)
        {"wallet": "A", "condition_id": "m1", "outcome": "YES", "price": 0.50,
         "size_usdc": 100.0, "traded_at": ts("2025-06-01")},
        {"wallet": "A", "condition_id": "m2", "outcome": "YES", "price": 0.25,
         "size_usdc": 100.0, "traded_at": ts("2025-06-02")},
    ])
    res = make_resolutions([
        {"condition_id": "m1", "winning_outcome": "YES", "resolved_at": ts("2025-06-05")},
        {"condition_id": "m2", "winning_outcome": "NO", "resolved_at": ts("2025-06-06")},
    ])
    f = compute_features(trades, res, as_of=ts("2025-06-30"), lookback_days=90)
    row = f[f["wallet"] == "A"].iloc[0]
    assert row["resolved_trades"] == 2
    assert abs(row["win_rate"] - 0.5) < 1e-9
    # equal sizes: roi = mean(+1.0 for m1, -1.0 for m2) = 0
    assert abs(row["roi"] - 0.0) < 1e-9


def test_features_exclude_unresolved_from_roi():
    trades = make_trades([
        {"wallet": "A", "condition_id": "m1", "outcome": "YES", "price": 0.5,
         "traded_at": ts("2025-06-01")},
        {"wallet": "A", "condition_id": "m9", "outcome": "YES", "price": 0.5,
         "traded_at": ts("2025-06-02")},   # never resolves
    ])
    res = make_resolutions([
        {"condition_id": "m1", "winning_outcome": "YES", "resolved_at": ts("2025-06-05")}])
    f = compute_features(trades, res, ts("2025-06-30"))
    row = f.iloc[0]
    assert row["resolved_trades"] == 1 and row["total_trades"] == 2
    assert abs(row["roi"] - 1.0) < 1e-9     # only the resolved winner counts


def test_features_no_lookahead():
    """A resolution AFTER as_of must not affect features as of that date."""
    trades = make_trades([
        {"wallet": "A", "condition_id": "m1", "outcome": "YES", "price": 0.5,
         "traded_at": ts("2025-06-01")}])
    res_future = make_resolutions([
        {"condition_id": "m1", "winning_outcome": "YES", "resolved_at": ts("2025-07-01")}])
    f = compute_features(trades, res_future, as_of=ts("2025-06-15"))
    assert f.iloc[0]["resolved_trades"] == 0
    assert pd.isna(f.iloc[0]["roi"])


def test_features_lookback_window_excludes_old_trades():
    trades = make_trades([
        {"wallet": "A", "condition_id": "m1", "traded_at": ts("2025-01-01")},
        {"wallet": "A", "condition_id": "m2", "traded_at": ts("2025-06-01")}])
    f = compute_features(trades, make_resolutions([]), ts("2025-06-15"), lookback_days=30)
    assert f.iloc[0]["total_trades"] == 1


def test_scoring_ranks_better_roi_higher():
    trades = make_trades([
        {"wallet": "GOOD", "condition_id": "m1", "outcome": "YES", "price": 0.4,
         "traded_at": ts("2025-06-01")},
        {"wallet": "BAD", "condition_id": "m1", "outcome": "NO", "price": 0.6,
         "traded_at": ts("2025-06-01")}])
    res = make_resolutions([
        {"condition_id": "m1", "winning_outcome": "YES", "resolved_at": ts("2025-06-05")}])
    s = score(compute_features(trades, res, ts("2025-06-30")))
    assert s.iloc[0]["wallet"] == "GOOD"
    good = s.loc[s["wallet"] == "GOOD", "alpha_score"].iloc[0]
    bad = s.loc[s["wallet"] == "BAD", "alpha_score"].iloc[0]
    assert good > bad
    assert 0.0 <= bad <= good <= 1.0


def test_scoring_empty_frame_is_safe():
    out = score(compute_features(make_trades([]), make_resolutions([]),
                                 ts("2025-06-30")))
    assert len(out) == 0 and "alpha_score" in out.columns
