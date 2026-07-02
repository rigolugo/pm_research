"""End-to-end backtest tests — the scientific core of phase 1.

Three invariants a correct engine must satisfy:
  1. EDGE EXISTS  → on a synthetic world with skilled traders, modeled-latency
     PnL is positive.
  2. NO EDGE      → with only coin-flip traders, the engine reports ~no profit
     (a profitable result here would mean the engine manufactures edge: the
     worst possible bug).
  3. LATENCY HURTS → zero-latency ROI >= modeled-latency ROI.
"""
from __future__ import annotations

from datetime import date

from pm_research.backtest import BacktestEngine, _kelly_fraction
from pm_research.config import (BacktestConfig, ConsensusConfig, RiskConfig,
                                SelectionConfig)
from pm_research.data.synthetic import WorldConfig, generate
from pm_research.latency import ZERO_LATENCY, LatencyModel
from pm_research.selection import ManualListSelector, TrailingAlphaSelector
from tests.helpers import small_world


def _cfg(world) -> BacktestConfig:
    start = world.trades["traded_at"].min().date()
    end = world.resolutions["resolved_at"].max().date()
    return BacktestConfig(
        start=start, end=end, initial_capital=10_000.0,
        selection=SelectionConfig(universe_size=10, lookback_days=90,
                                  min_resolved_trades=5, min_volume_usdc=100.0,
                                  rebalance_interval_days=7),
        consensus=ConsensusConfig(window_hours=48, min_unique_traders=3,
                                  min_weighted_score=0.4,
                                  cooldown_hours_per_market=24),
        risk=RiskConfig(size_fraction=0.02, max_open_positions=30))


def _run(world, cfg, latency_model=None):
    sel = TrailingAlphaSelector(cfg.selection)
    eng = BacktestEngine(world.trades, world.markets, world.resolutions,
                         world.prices, sel, cfg, latency_model=latency_model)
    return eng.run()


def test_e2e_detects_real_edge_under_modeled_latency():
    w = small_world(seed=7)
    res = _run(w, _cfg(w))
    assert res.n_signals > 0, "no consensus signals at all — pipeline broken"
    assert res.n_filled > 0, "nothing filled — latency model or sizing broken"
    assert res.summary["total_roi"] > 0.005, res.summary
    assert res.summary["win_rate"] > 0.55, res.summary
    assert res.biased_selection is False


def test_e2e_reports_no_edge_when_traders_are_random():
    w = small_world(seed=11, n_skilled=0, n_random=35)
    res = _run(w, _cfg(w))
    # the engine must NOT manufacture profit out of noise
    assert res.summary["total_roi"] < 0.02, res.summary


def test_e2e_zero_latency_is_upper_bound():
    w = small_world(seed=7)
    cfg = _cfg(w)
    modeled = _run(w, cfg)
    zero = _run(w, cfg, latency_model=LatencyModel(ZERO_LATENCY))
    assert zero.summary["total_roi"] >= modeled.summary["total_roi"] - 1e-9
    assert zero.n_lost_to_latency == 0


def test_e2e_manual_selector_is_flagged_biased():
    w = small_world(seed=7)
    cfg = _cfg(w)
    eng = BacktestEngine(w.trades, w.markets, w.resolutions, w.prices,
                         ManualListSelector(w.skilled_wallets), cfg)
    res = eng.run()
    assert res.biased_selection is True


def test_e2e_equity_curve_and_accounting_consistency():
    w = small_world(seed=7)
    res = _run(w, _cfg(w))
    eq = res.equity
    assert abs(eq.iloc[0] - 10_000.0) < 200.0          # starts ~ initial capital
    # final equity == initial + sum of realized pnl (all positions resolve)
    realized = float(res.trade_log["pnl_usdc"].sum()) if len(res.trade_log) else 0.0
    assert abs(eq.iloc[-1] - (10_000.0 + realized)) < 1.0
    assert not eq.isna().any()


def test_kelly_fraction_math():
    # p=0.6 at price 0.5: b=1, f*=0.6-0.4=0.2 → quarter kelly 0.05
    assert abs(_kelly_fraction(0.6, 0.5, 0.25) - 0.05) < 1e-12
    # negative edge clamps to zero
    assert _kelly_fraction(0.4, 0.5, 0.25) == 0.0
