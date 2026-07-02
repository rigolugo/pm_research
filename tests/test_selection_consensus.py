"""Selection + consensus tests.

The selection no-lookahead test is THE methodological test of phase 1:
appending future data must not change the universe chosen as of T.
"""
from __future__ import annotations

import pandas as pd

from pm_research.config import ConsensusConfig, SelectionConfig
from pm_research.consensus import CooldownFilter, detect
from pm_research.features import compute_features
from pm_research.scoring import score
from pm_research.selection import TrailingAlphaSelector
from tests.helpers import make_resolutions, make_trades, small_world, ts


def _sel_cfg(**kw) -> SelectionConfig:
    base = dict(universe_size=10, lookback_days=90,
                min_resolved_trades=5, min_volume_usdc=100.0)
    base.update(kw)
    return SelectionConfig(**base)


def test_selector_prefers_skilled_wallets_on_synthetic_world():
    w = small_world()
    sel = TrailingAlphaSelector(_sel_cfg())
    as_of = w.trades["traded_at"].max()  # by the end, plenty of resolutions
    chosen = sel.select(w.trades, w.resolutions, as_of)
    assert chosen, "selector returned empty universe"
    skilled_hits = sum(1 for x in chosen if x in w.skilled_wallets)
    # >=60% of the chosen universe should be genuinely skilled wallets;
    # a random pick of 10 from this pool would average ~29% skilled, so 60%
    # is a strong signal while leaving headroom for percentile-rank noise.
    assert skilled_hits / len(chosen) >= 0.6, (skilled_hits, len(chosen), chosen)


def test_selector_no_lookahead_future_data_does_not_change_past_selection():
    w = small_world()
    sel = TrailingAlphaSelector(_sel_cfg())
    mid = w.trades["traded_at"].min() + (w.trades["traded_at"].max()
                                         - w.trades["traded_at"].min()) / 2
    past_trades = w.trades[w.trades["traded_at"] <= mid]
    past_res = w.resolutions[w.resolutions["resolved_at"] <= mid]
    chosen_truncated = sel.select(past_trades, past_res, mid)
    chosen_full = sel.select(w.trades, w.resolutions, mid)  # future rows present
    assert chosen_truncated == chosen_full


def test_selector_respects_min_resolved_trades_gate():
    trades = make_trades([
        {"wallet": "A", "condition_id": "m1", "outcome": "YES", "price": 0.5,
         "size_usdc": 1000.0, "traded_at": ts("2025-06-01")}])
    res = make_resolutions([
        {"condition_id": "m1", "winning_outcome": "YES", "resolved_at": ts("2025-06-02")}])
    sel = TrailingAlphaSelector(_sel_cfg(min_resolved_trades=5))
    assert sel.select(trades, res, ts("2025-06-30")) == []


# ---------------------------- consensus ----------------------------------

def _scores_for(wallets: list[str], alpha: float = 0.9) -> pd.DataFrame:
    return pd.DataFrame({"wallet": wallets, "alpha_score": [alpha] * len(wallets)})


def test_consensus_detected_with_three_traders_same_outcome():
    base = ts("2025-06-01 00:00")
    trades = make_trades([
        {"wallet": f"w{i}", "condition_id": "mX", "outcome": "YES",
         "price": 0.40 + i * 0.01, "traded_at": base + pd.Timedelta(hours=i)}
        for i in range(3)])
    cfg = ConsensusConfig(window_hours=48, min_unique_traders=3, min_weighted_score=0.5)
    sigs = detect(trades, [f"w{i}" for i in range(3)], _scores_for([f"w{i}" for i in range(3)]),
                  as_of=base + pd.Timedelta(hours=10), cfg=cfg)
    assert len(sigs) == 1
    s = sigs[0]
    assert s.condition_id == "mX" and s.outcome == "YES" and s.n_traders == 3
    assert abs(s.leaders_avg_entry - 0.41) < 1e-9
    assert s.detected_at == base + pd.Timedelta(hours=2)


def test_consensus_not_detected_below_min_traders_or_outside_window():
    base = ts("2025-06-01 00:00")
    trades = make_trades([
        {"wallet": "w0", "condition_id": "mX", "outcome": "YES", "traded_at": base},
        {"wallet": "w1", "condition_id": "mX", "outcome": "YES", "traded_at": base},
        # third trader is 80h later — outside the 48h window
        {"wallet": "w2", "condition_id": "mX", "outcome": "YES",
         "traded_at": base + pd.Timedelta(hours=80)}])
    cfg = ConsensusConfig(window_hours=48, min_unique_traders=3, min_weighted_score=0.0)
    sigs = detect(trades, ["w0", "w1", "w2"], _scores_for(["w0", "w1", "w2"]),
                  as_of=base + pd.Timedelta(hours=81), cfg=cfg)
    assert sigs == []  # at as_of, only w2's trade is inside the window


def test_consensus_ignores_non_universe_and_sell_trades():
    base = ts("2025-06-01 00:00")
    trades = make_trades([
        {"wallet": "w0", "condition_id": "mX", "outcome": "YES", "traded_at": base},
        {"wallet": "w1", "condition_id": "mX", "outcome": "YES", "traded_at": base},
        {"wallet": "OUTSIDER", "condition_id": "mX", "outcome": "YES", "traded_at": base},
        {"wallet": "w2", "condition_id": "mX", "outcome": "YES", "side": "SELL",
         "traded_at": base}])
    cfg = ConsensusConfig(min_unique_traders=3, min_weighted_score=0.0)
    sigs = detect(trades, ["w0", "w1", "w2"], _scores_for(["w0", "w1", "w2"]),
                  as_of=base + pd.Timedelta(hours=1), cfg=cfg)
    assert sigs == []


def test_consensus_weighted_score_threshold():
    base = ts("2025-06-01 00:00")
    trades = make_trades([
        {"wallet": f"w{i}", "condition_id": "mX", "outcome": "YES", "traded_at": base}
        for i in range(3)])
    cfg = ConsensusConfig(min_unique_traders=3, min_weighted_score=0.5)
    weak = _scores_for(["w0", "w1", "w2"], alpha=0.2)
    assert detect(trades, ["w0", "w1", "w2"], weak, base + pd.Timedelta(hours=1), cfg) == []
    strong = _scores_for(["w0", "w1", "w2"], alpha=0.8)
    assert len(detect(trades, ["w0", "w1", "w2"], strong, base + pd.Timedelta(hours=1), cfg)) == 1


def test_cooldown_filter_suppresses_repeats():
    base = ts("2025-06-01 00:00")
    trades = make_trades([
        {"wallet": f"w{i}", "condition_id": "mX", "outcome": "YES", "traded_at": base}
        for i in range(3)])
    cfg = ConsensusConfig(min_unique_traders=3, min_weighted_score=0.0,
                          cooldown_hours_per_market=24)
    scores = _scores_for(["w0", "w1", "w2"])
    cd = CooldownFilter(cfg.cooldown_hours_per_market)
    s1 = detect(trades, ["w0", "w1", "w2"], scores, base + pd.Timedelta(hours=1), cfg)[0]
    s2 = detect(trades, ["w0", "w1", "w2"], scores, base + pd.Timedelta(hours=5), cfg)[0]
    assert cd.admit(s1) is True
    assert cd.admit(s2) is False   # same market, inside cooldown
