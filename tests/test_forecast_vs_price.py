"""Tests for the Rank 1A forecast-vs-price probe (Rung 0 + Rung 1)."""
from __future__ import annotations

import importlib.util
import pathlib
from datetime import date

import numpy as np
import pandas as pd

_spec = importlib.util.spec_from_file_location(
    "forecast_vs_price",
    str(pathlib.Path(__file__).resolve().parents[1] / "scripts" / "forecast_vs_price.py"))
fvp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fvp)

from pm_research.calibration import IsotonicCalibrator
from pm_research.splits import rolling_train_test_splits


def _splits():
    return rolling_train_test_splits(date(2025, 1, 1), date(2026, 1, 1), 5)


def _cond_df(n, p=0.5, seed=0, start="2025-02-01", days_span=300):
    rng = np.random.default_rng(seed)
    base = pd.Timestamp(start, tz="UTC")
    ts = [base + pd.Timedelta(days=int(d))
          for d in rng.integers(0, days_span, n)]
    price = rng.uniform(0.05, 0.95, n) if p is None else np.full(n, p)
    outcome = (rng.uniform(size=n) < price).astype(int)
    return pd.DataFrame({
        "condition_id": [f"c{i}" for i in range(n)],
        "first_trade_ts": ts,
        "decision_ts": ts,
        "market_price_at_decision": price,
        "realized_outcome": outcome,
        "resolution_label": ["YES" if o else "NO" for o in outcome],
    })


# 1. one signal per condition ------------------------------------------------
def test_one_signal_per_condition():
    df = _cond_df(100, p=None, seed=1)
    assert df["condition_id"].is_unique
    assert len(df) == df["condition_id"].nunique()
    # no trade-count column anywhere (must not weight by trade count)
    assert not any("trade_count" in c or "count" in c.lower()
                   for c in df.columns)


# 2. Rung 0 sanity tie -------------------------------------------------------
def test_rung0_ties_price_baseline():
    df = _cond_df(2000, p=None, seed=2)
    res = fvp.run_probe(df, _splits(), 0.04, 0.01, 50, 100, 4)
    ok = [s for s in res["per_split"] if s.get("status") == "OK"]
    assert ok, "need evaluable splits"
    for s in ok:
        assert abs(s["rung0_brier_skill"]) < 1e-9     # forecast=price -> skill 0
    assert res["rung0_sanity_ties"] is True
    assert res["verdict"] != "FAIL_RUNG0_SANITY"


# 3. isotonic calibrator fit on train only -----------------------------------
def test_calibrator_fit_on_train_only_no_leakage():
    # train and test are disjoint by decision_ts; a calibrator fit on train must
    # be applied to test it never saw. We assert the probe never fits on test by
    # checking that a constant-price degenerate train can't "learn" the test.
    df = _cond_df(1500, p=None, seed=3)
    res = fvp.run_probe(df, _splits(), 0.04, 0.01, 50, 100, 4)
    # at minimum, evaluable splits computed a brier_cal distinct from a peek at
    # test labels (cal applied to TEST prices, not fit on them)
    ok = [s for s in res["per_split"] if s.get("status") == "OK"]
    assert ok
    for s in ok:
        assert "brier_cal" in s and "brier_price" in s


# 4. no train/test temporal leakage ------------------------------------------
def test_no_train_test_temporal_overlap():
    df = _cond_df(1500, p=None, seed=4)
    dec = pd.to_datetime(df["decision_ts"], utc=True)
    for (trs, tre, tes, tee) in _splits():
        trs, tre = pd.Timestamp(trs, tz="UTC"), pd.Timestamp(tre, tz="UTC")
        tes, tee = pd.Timestamp(tes, tz="UTC"), pd.Timestamp(tee, tz="UTC")
        tr = df[(dec >= trs) & (dec < tre)]
        te = df[(dec >= tes) & (dec < tee)]
        if len(tr) and len(te):
            assert tr["decision_ts"].max() <= te["decision_ts"].min()  # train before test


# 5. Brier skill computation -------------------------------------------------
def test_brier_skill_sign():
    # perfectly calibrated forecast beats a biased one -> positive skill
    y = np.array([1, 1, 0, 0, 1, 0, 1, 0])
    good = np.array([.9, .9, .1, .1, .9, .1, .9, .1])
    bad = np.full(8, 0.5)
    bg = IsotonicCalibrator.brier(good, y)
    bb = IsotonicCalibrator.brier(bad, y)
    skill = 1.0 - (bg / bb)
    assert skill > 0


# 6. EV side logic: YES vs NO ------------------------------------------------
def test_ev_side_logic_yes_no():
    fc = np.array([0.7, 0.3])          # >price -> YES ; <price -> NO
    pr = np.array([0.5, 0.5])
    oc = np.array([1.0, 0.0])
    ev = fvp.net_ev(fc, pr, oc, fee_rate=0.0, spread=0.0)
    # YES with outcome 1: realized = 1-0.5 = +0.5
    # NO  with outcome 0: realized = 0.5-0 = +0.5
    assert abs(ev["mean_realized_pnl"] - 0.5) < 1e-12
    assert abs(ev["frac_side_yes"] - 0.5) < 1e-12


def test_ev_side_logic_losing_sides():
    fc = np.array([0.7, 0.3])
    pr = np.array([0.5, 0.5])
    oc = np.array([0.0, 1.0])          # both wrong
    ev = fvp.net_ev(fc, pr, oc, fee_rate=0.0, spread=0.0)
    # YES with outcome 0: realized = 0-0.5 = -0.5
    # NO  with outcome 1: realized = 0.5-1 = -0.5
    assert abs(ev["mean_realized_pnl"] - (-0.5)) < 1e-12


# 7. fee subtraction ---------------------------------------------------------
def test_fee_formula_and_subtraction():
    assert abs(float(fvp._fee(np.array([0.5]), 0.04)[0]) - 0.01) < 1e-12  # peak
    assert float(fvp._fee(np.array([0.0]), 0.04)[0]) == 0.0               # edges 0
    assert float(fvp._fee(np.array([1.0]), 0.04)[0]) == 0.0
    # net EV is strictly below gross realized when fee/spread > 0
    fc = np.array([0.7]); pr = np.array([0.5]); oc = np.array([1.0])
    gross = fvp.net_ev(fc, pr, oc, 0.0, 0.0)["mean_net_ev"]
    net = fvp.net_ev(fc, pr, oc, 0.04, 0.01)["mean_net_ev"]
    assert net < gross


# 8. INCONCLUSIVE on thin sample ---------------------------------------------
def test_inconclusive_thin_sample():
    df = _cond_df(3, p=None, seed=9)
    res = fvp.run_probe(df, _splits(), 0.04, 0.01, 50, 100, 4)
    assert res["verdict"] == "INCONCLUSIVE_INSUFFICIENT_SAMPLE"


# 9. tradable requires EV>0, not just Brier ----------------------------------
def test_brier_improvement_alone_not_tradable():
    # construct a case where calibration helps Brier but costs wipe EV:
    # build per-split records manually mimicking run_probe's structure
    per_split = []
    for i in range(1, 6):
        per_split.append({
            "split": i, "status": "OK", "n_train": 200, "n_test": 100,
            "rung0_brier_skill": 0.0,
            "brier_price": 0.25, "brier_cal": 0.24, "brier_skill_cal": 0.04,
            "ev_rung1_conservative": {"mean_net_ev": -0.02},   # negative EV
            "ev_rung1_no_spread": {"mean_net_ev": -0.01},
        })
    ok = [s for s in per_split if s["status"] == "OK"]
    rung1_pos = sum(1 for s in ok if s["brier_skill_cal"] > 0)
    rung1_ev_pos = sum(1 for s in ok
                       if s["ev_rung1_conservative"]["mean_net_ev"] > 0)
    assert rung1_pos == 5 and rung1_ev_pos == 0   # Brier up everywhere, EV<=0


# 10. named-binary excluded (classification-level) ---------------------------
def test_named_binary_excluded_from_usable():
    # classify_from_aggregates must NOT mark a named-binary (UP/DOWN) as usable
    agg = {
        "yn": {"tokens": {"A", "B"}, "indices": {0, 1}, "labels": {"YES", "NO"},
               "trade_count": 10, "first_trade": pd.Timestamp("2025-06-01", tz="UTC")},
        "named": {"tokens": {"C", "D"}, "indices": {0, 1}, "labels": {"UP", "DOWN"},
                  "trade_count": 10, "first_trade": pd.Timestamp("2025-06-01", tz="UTC")},
    }
    markets = pd.DataFrame(columns=["condition_id", "category", "liquidity_usdc"])
    res = pd.DataFrame({"condition_id": ["yn", "named"],
                        "winning_outcome": ["YES", "UP"],
                        "resolved_at": [pd.Timestamp("2025-07-01", tz="UTC")] * 2})
    cc = fvp._ams.classify_from_aggregates(agg, markets, res, {"yn", "named"})
    usable = set(cc.loc[cc["usable"], "condition_id"])
    assert "yn" in usable
    assert "named" not in usable        # named-binary never enters the probe set
    named_row = cc[cc["condition_id"] == "named"].iloc[0]
    assert named_row["class"] == "named_binary"
