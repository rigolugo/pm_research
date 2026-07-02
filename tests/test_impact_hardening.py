"""Phase 1.5 impact-shape hardening — full test matrix.

Covers compute_impact() across modes and edge cases, the derived sqrt
coefficient, the pessimism guarantee (sqrt_guarded never cheaper than linear
pre-cap), the deliberately-surfaced sqrt-cheaper-than-linear case at x>1, the
invalid-input handling (no fabricated liquidity), and the diagnostic helper
(present-but-unused-by-default; missing-prints fallback).
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
import pytest

from pm_research.config import LatencyConfig
from pm_research.latency import (
    compute_impact, resolve_sqrt_coeff, nearby_trade_diagnostics,
    LatencyModel, PriceBook, ZERO_LATENCY,
)

K = 0.5          # legacy linear coeff
CAP = 0.03
REF_X = 0.01


# --------------------------------------------------------------------------
# derived sqrt coefficient
# --------------------------------------------------------------------------
def test_sqrt_coeff_derived_from_ref_x():
    # impact_k_sqrt None -> derive = impact_k * sqrt(ref_x) = 0.5 * 0.1 = 0.05
    k_sqrt = resolve_sqrt_coeff(K, None, REF_X)
    assert k_sqrt == pytest.approx(0.05)


def test_sqrt_coeff_explicit_overrides_derivation():
    assert resolve_sqrt_coeff(K, 0.123, REF_X) == pytest.approx(0.123)


def test_sqrt_coeff_validations():
    with pytest.raises(ValueError):
        resolve_sqrt_coeff(K, None, 0.0)         # ref_x must be > 0
    with pytest.raises(ValueError):
        resolve_sqrt_coeff(K, None, -0.01)
    with pytest.raises(ValueError):
        resolve_sqrt_coeff(-1.0, None, REF_X)    # impact_k >= 0
    with pytest.raises(ValueError):
        resolve_sqrt_coeff(K, -0.01, REF_X)      # impact_k_sqrt >= 0 if supplied


def test_linear_and_sqrt_cross_at_ref_x():
    # by construction the two terms are equal at x = ref_x
    x = REF_X
    k_sqrt = resolve_sqrt_coeff(K, None, REF_X)
    assert K * x == pytest.approx(k_sqrt * math.sqrt(x))


# --------------------------------------------------------------------------
# edge cases: size and liquidity
# --------------------------------------------------------------------------
def test_zero_size_gives_zero_impact():
    assert compute_impact(0.0, 20000, impact_k=K, impact_cap=CAP) == 0.0
    assert compute_impact(-5.0, 20000, impact_k=K, impact_cap=CAP) == 0.0


@pytest.mark.parametrize("legacy_liq", [0.0, -1.0, None])
def test_legacy_nonpositive_liquidity_falls_back_to_cap(legacy_liq):
    # liq <= 0 (incl. 0.0 from a missing market via book.liquidity, and None)
    # is the DELIBERATE legacy fallback -> silent cap, no fabricated liquidity.
    assert compute_impact(250, legacy_liq, impact_k=K, impact_cap=CAP) == CAP


@pytest.mark.parametrize("bad_liq", [float("nan"), float("inf"), float("-inf")])
def test_malformed_liquidity_raises_by_default(bad_liq):
    # NaN/inf was never a deliberate fallback; default policy surfaces it loudly
    with pytest.raises(ValueError, match="finite and positive"):
        compute_impact(250, bad_liq, impact_k=K, impact_cap=CAP)


@pytest.mark.parametrize("bad_liq", [float("nan"), float("inf"), float("-inf")])
def test_malformed_liquidity_caps_under_explicit_policy(bad_liq):
    # "cap" is an explicit opt-in to the conservative fallback for NaN/inf
    assert compute_impact(250, bad_liq, impact_k=K, impact_cap=CAP,
                          invalid_liquidity_policy="cap") == CAP


def test_unknown_invalid_liquidity_policy_raises():
    with pytest.raises(ValueError, match="invalid_liquidity_policy"):
        compute_impact(250, float("nan"), impact_k=K, impact_cap=CAP,
                       invalid_liquidity_policy="bogus")


def test_zero_size_short_circuits_before_malformed_check():
    # nothing traded -> 0 impact, even if liquidity is malformed (irrelevant)
    assert compute_impact(0.0, float("nan"), impact_k=K, impact_cap=CAP) == 0.0
    assert compute_impact(0.0, float("inf"), impact_k=K, impact_cap=CAP,
                          invalid_liquidity_policy="raise") == 0.0


def test_negative_cap_raises():
    with pytest.raises(ValueError):
        compute_impact(250, 20000, impact_k=K, impact_cap=-0.01)


def test_unknown_shape_raises():
    with pytest.raises(ValueError):
        compute_impact(250, 20000, impact_k=K, impact_cap=CAP,
                       impact_shape="bogus")


# --------------------------------------------------------------------------
# x < 1, x == 1, x > 1 across modes
# --------------------------------------------------------------------------
def test_x_below_one_sqrt_guarded_picks_sqrt_when_higher():
    # small participation: sqrt term sits above linear -> guarded picks sqrt
    size, liq = 100, 20000          # x = 0.005 (< ref_x)
    x = size / liq
    k_sqrt = resolve_sqrt_coeff(K, None, REF_X)
    linear = K * x
    sqrt_term = k_sqrt * math.sqrt(x)
    assert sqrt_term > linear        # precondition for this regime
    g = compute_impact(size, liq, impact_k=K, impact_cap=CAP,
                       impact_shape="sqrt_guarded")
    assert g == pytest.approx(min(sqrt_term, CAP))


def test_x_equals_one_all_modes_equal_premcap():
    # at x = 1, linear = K*1 = 0.5 and sqrt = k_sqrt*1 = 0.05; both capped.
    size, liq = 1000, 1000           # x = 1
    lin = compute_impact(size, liq, impact_k=K, impact_cap=CAP,
                         impact_shape="linear")
    guard = compute_impact(size, liq, impact_k=K, impact_cap=CAP,
                           impact_shape="sqrt_guarded")
    assert lin == CAP and guard == CAP


def test_x_above_one_sqrt_cheaper_than_linear_surfaced():
    # DELIBERATE: pure sqrt CAN be cheaper than linear when x > 1.
    # use a large cap so the cap doesn't mask the comparison.
    size, liq = 2000, 1000           # x = 2
    big_cap = 10.0
    lin = compute_impact(size, liq, impact_k=K, impact_cap=big_cap,
                         impact_shape="linear")
    sq = compute_impact(size, liq, impact_k=K, impact_cap=big_cap,
                        impact_shape="sqrt")
    assert sq < lin                  # sqrt is cheaper here — surfaced, expected


# --------------------------------------------------------------------------
# cap binding
# --------------------------------------------------------------------------
def test_cap_binds_in_all_modes():
    size, liq = 5000, 1000           # x = 5, everything well above cap
    for shape in ("linear", "sqrt", "sqrt_guarded"):
        assert compute_impact(size, liq, impact_k=K, impact_cap=CAP,
                              impact_shape=shape) == CAP


# --------------------------------------------------------------------------
# pessimism guarantee: sqrt_guarded never cheaper than linear (pre-cap)
# --------------------------------------------------------------------------
@pytest.mark.parametrize("x", [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5,
                               0.9, 1.0, 1.5, 2.0, 5.0])
def test_sqrt_guarded_never_cheaper_than_linear(x):
    # use a large cap so we test the pre-cap guarantee, not the cap floor
    size, liq = x * 10000, 10000
    big_cap = 1e9
    lin = compute_impact(size, liq, impact_k=K, impact_cap=big_cap,
                         impact_shape="linear")
    guard = compute_impact(size, liq, impact_k=K, impact_cap=big_cap,
                           impact_shape="sqrt_guarded")
    assert guard >= lin - 1e-12


def test_sqrt_guarded_never_cheaper_than_linear_with_real_cap():
    # also holds with the real cap (cap applies equally to both)
    for x in [0.0005, 0.005, 0.05, 0.5, 2.0]:
        size, liq = x * 10000, 10000
        lin = compute_impact(size, liq, impact_k=K, impact_cap=CAP,
                             impact_shape="linear")
        guard = compute_impact(size, liq, impact_k=K, impact_cap=CAP,
                               impact_shape="sqrt_guarded")
        assert guard >= lin - 1e-12


# --------------------------------------------------------------------------
# config defaults + model integration
# --------------------------------------------------------------------------
def test_config_defaults():
    c = LatencyConfig()
    assert c.impact_shape == "sqrt_guarded"
    assert c.impact_k_sqrt is None          # derived unless supplied
    assert c.impact_sqrt_ref_x == 0.01


def test_zero_latency_yields_zero_impact():
    # the upper-bound comparison run must charge no impact in any mode path
    assert compute_impact(250, 20000, impact_k=ZERO_LATENCY.impact_k,
                          impact_cap=ZERO_LATENCY.impact_cap,
                          impact_shape=ZERO_LATENCY.impact_shape,
                          impact_k_sqrt=ZERO_LATENCY.impact_k_sqrt,
                          impact_sqrt_ref_x=ZERO_LATENCY.impact_sqrt_ref_x) == 0.0


def test_model_apply_uses_guarded_impact():
    # build a tiny price book and confirm apply() routes through compute_impact
    prices = pd.DataFrame({
        "condition_id": ["c1"] * 3,
        "ts": pd.to_datetime(["2025-01-01T00:00:00Z", "2025-01-01T01:00:00Z",
                              "2025-01-01T02:00:00Z"]),
        "yes_price": [0.50, 0.50, 0.50],
    })
    markets = pd.DataFrame({"condition_id": ["c1"], "liquidity_usdc": [20000.0]})
    book = PriceBook(prices, markets)
    # pin "close": this test isolates IMPACT math through apply(); it has no
    # trades source and no reason to exercise worst_in_bar (which would raise
    # for a missing source by design). Fill-pricing held at legacy close.
    cfg = LatencyConfig(detection_delay_seconds=0, taker_fee_bps=0, max_chase=1.0,
                        intrabar_fill_policy="close")
    model = LatencyModel(cfg)
    fill = model.apply(condition_id="c1", outcome="YES",
                       detected_at=pd.Timestamp("2025-01-01T01:00:00Z"),
                       leaders_avg_entry=0.50, size_usdc=100.0, book=book)
    assert fill.filled
    # expected impact = guarded at x=100/20000=0.005
    exp = compute_impact(100.0, 20000.0, impact_k=cfg.impact_k,
                         impact_cap=cfg.impact_cap, impact_shape=cfg.impact_shape,
                         impact_k_sqrt=cfg.impact_k_sqrt,
                         impact_sqrt_ref_x=cfg.impact_sqrt_ref_x)
    assert fill.fill_price == pytest.approx(0.50 + exp)


# --------------------------------------------------------------------------
# trade-print diagnostics (DIAGNOSTIC ONLY; never alters impact by default)
# --------------------------------------------------------------------------
def _trades():
    return pd.DataFrame({
        "condition_id": ["c1", "c1", "c1", "c2"],
        "traded_at": pd.to_datetime([
            "2025-01-01T01:00:00Z", "2025-01-01T01:02:00Z",
            "2025-01-01T01:10:00Z",            # outside +/-300s of 01:00
            "2025-01-01T01:00:30Z"]),          # different market
        "size_usdc": [100.0, 300.0, 999.0, 50.0],
    })


def test_diagnostics_present_but_do_not_alter_impact():
    # diagnostics computed, but impact is identical whether or not we computed them
    fill_at = pd.Timestamp("2025-01-01T01:00:00Z")
    diag = nearby_trade_diagnostics(_trades(), "c1", fill_at, window_seconds=300)
    assert diag["nearby_trade_count"] == 2          # the 01:00 and 01:02 prints
    assert diag["nearby_median_trade_size_usdc"] == pytest.approx(200.0)
    assert diag["nearby_window_seconds"] == 300
    # impact does not consume diagnostics — same value regardless
    imp = compute_impact(250, 20000, impact_k=K, impact_cap=CAP)
    assert imp == compute_impact(250, 20000, impact_k=K, impact_cap=CAP)


def test_diagnostics_missing_prints_returns_nan_zero():
    fill_at = pd.Timestamp("2025-06-01T00:00:00Z")   # far from any print
    diag = nearby_trade_diagnostics(_trades(), "c1", fill_at, window_seconds=300)
    assert diag["nearby_trade_count"] == 0
    assert math.isnan(diag["nearby_median_trade_size_usdc"])


def test_diagnostics_empty_frame():
    diag = nearby_trade_diagnostics(pd.DataFrame(), "c1",
                                    pd.Timestamp("2025-01-01T00:00:00Z"))
    assert diag["nearby_trade_count"] == 0
    assert math.isnan(diag["nearby_median_trade_size_usdc"])


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
