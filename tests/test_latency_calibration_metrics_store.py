"""Latency, calibration, metrics, store tests."""
from __future__ import annotations

import tempfile
from datetime import date

import numpy as np
import pandas as pd

from pm_research.calibration import IsotonicCalibrator
from pm_research.config import LatencyConfig
from pm_research.data import schemas
from pm_research.data.store import Store, _spans_cover
from pm_research.latency import ZERO_LATENCY, LatencyModel, PriceBook
from pm_research.metrics import max_drawdown, profit_factor, sharpe, summarize
from tests.helpers import make_trades, ts


# ---------------------------- latency ------------------------------------

def _book(prices_by_hour: list[float], cid: str = "m1",
          liquidity: float = 10_000.0) -> PriceBook:
    t0 = ts("2025-06-01 00:00")
    prices = pd.DataFrame({
        "condition_id": cid,
        "ts": [t0 + pd.Timedelta(hours=h) for h in range(len(prices_by_hour))],
        "yes_price": prices_by_hour})
    markets = pd.DataFrame({"condition_id": [cid], "category": ["OTHER"],
                            "liquidity_usdc": [liquidity],
                            "created_at": [t0], "resolution_at": [t0 + pd.Timedelta(days=7)]})
    return PriceBook(schemas.validate(prices, schemas.PRICES_COLS, "prices"),
                     schemas.validate(markets, schemas.MARKETS_COLS, "markets"))


def test_latency_fill_is_worse_than_leader_entry():
    book = _book([0.40, 0.45, 0.50])
    lm = LatencyModel(LatencyConfig(detection_delay_seconds=3600, impact_k=0.5,
                                    impact_cap=0.03, max_chase=0.50,
                                    intrabar_fill_policy="close"))
    fill = lm.apply(condition_id="m1", outcome="YES",
                    detected_at=ts("2025-06-01 00:00"),
                    leaders_avg_entry=0.40, size_usdc=200.0, book=book)
    assert fill.filled
    # one hour later price is 0.45, plus impact 0.5*200/10000 = 0.01
    assert abs(fill.fill_price - 0.46) < 1e-9
    assert fill.fill_price > 0.40


def test_latency_abandons_when_price_chased_beyond_max():
    book = _book([0.40, 0.60])
    lm = LatencyModel(LatencyConfig(detection_delay_seconds=3600, impact_k=0.0,
                                    impact_cap=0.0, max_chase=0.04,
                                    intrabar_fill_policy="close"))
    fill = lm.apply(condition_id="m1", outcome="YES",
                    detected_at=ts("2025-06-01 00:00"),
                    leaders_avg_entry=0.40, size_usdc=100.0, book=book)
    assert not fill.filled and "chase" in fill.reason


def test_latency_impact_is_capped():
    book = _book([0.40], liquidity=100.0)   # tiny liquidity → huge raw impact
    lm = LatencyModel(LatencyConfig(detection_delay_seconds=0, impact_k=0.5,
                                    impact_cap=0.03, max_chase=1.0,
                                    intrabar_fill_policy="close"))
    fill = lm.apply(condition_id="m1", outcome="YES",
                    detected_at=ts("2025-06-01 00:00"),
                    leaders_avg_entry=0.40, size_usdc=10_000.0, book=book)
    assert abs(fill.fill_price - 0.43) < 1e-9


def test_zero_latency_config_fills_at_leader_price():
    book = _book([0.40, 0.99])
    lm = LatencyModel(ZERO_LATENCY)
    fill = lm.apply(condition_id="m1", outcome="YES",
                    detected_at=ts("2025-06-01 00:00"),
                    leaders_avg_entry=0.40, size_usdc=100.0, book=book)
    assert fill.filled and abs(fill.fill_price - 0.40) < 1e-9


def test_pricebook_no_outcome_inversion():
    book = _book([0.30])
    assert abs(book.price_at("m1", "NO", ts("2025-06-01 00:30")) - 0.70) < 1e-9


# -------------------------- calibration ----------------------------------

def test_calibration_refuses_small_samples():
    c = IsotonicCalibrator(min_samples=200)
    try:
        c.fit(np.random.rand(50), np.random.randint(0, 2, 50))
        raise AssertionError("should have refused")
    except ValueError as e:
        assert "bootstrap" in str(e)


def test_calibration_corrects_overconfidence_and_is_monotone():
    rng = np.random.default_rng(0)
    n = 4000
    raw = rng.uniform(0.4, 1.0, n)
    true_p = 0.5 + (raw - 0.4) * 0.5      # raw 1.0 → only 80% real win prob
    y = (rng.random(n) < true_p).astype(float)
    c = IsotonicCalibrator(min_samples=200).fit(raw, y)
    cal = c.apply(np.array([0.5, 0.7, 0.9, 1.0]))
    assert all(np.diff(cal) >= -1e-12)                 # monotone
    assert c.apply(0.95) < 0.92                        # overconfidence shrunk
    assert c.brier(c.apply(raw), y) <= c.brier(raw, y) # brier improves
    # round-trips through JSON
    c2 = IsotonicCalibrator.from_json(c.to_json())
    assert abs(float(c2.apply(0.8)) - float(c.apply(0.8))) < 1e-12


# ---------------------------- metrics -------------------------------------

def test_max_drawdown_known_curve():
    eq = pd.Series([100.0, 120.0, 90.0, 110.0])
    assert abs(max_drawdown(eq) - 0.25) < 1e-9          # 120 → 90


def test_profit_factor_and_summary():
    pnls = pd.Series([10.0, -5.0, 20.0, -5.0])
    assert abs(profit_factor(pnls) - 3.0) < 1e-9
    eq = pd.Series([100.0, 101.0, 103.0, 102.0],
                   index=pd.date_range("2025-01-01", periods=4))
    s = summarize(eq, pnls)
    assert s["n_trades"] == 4 and abs(s["win_rate"] - 0.5) < 1e-9
    assert s["total_roi"] > 0


def test_sharpe_zero_for_flat_curve():
    eq = pd.Series([100.0] * 10, index=pd.date_range("2025-01-01", periods=10))
    assert sharpe(eq.pct_change().dropna()) == 0.0


# ------------------------------ store -------------------------------------

def test_store_roundtrip_dedup_and_coverage():
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        t1 = make_trades([{"trade_id": "a", "wallet": "w1"},
                          {"trade_id": "b", "wallet": "w1"}])
        store.save_wallet_trades("w1", t1, date(2025, 1, 1), date(2025, 6, 30))
        # overlapping second save: duplicate "b" plus new "c"
        t2 = make_trades([{"trade_id": "b", "wallet": "w1"},
                          {"trade_id": "c", "wallet": "w1"}])
        store.save_wallet_trades("w1", t2, date(2025, 6, 1), date(2025, 12, 31))
        loaded = store.load_trades(["w1"])
        assert sorted(loaded["trade_id"]) == ["a", "b", "c"]
        ok, gaps = store.coverage_ok(["w1"], date(2025, 2, 1), date(2025, 11, 30))
        assert ok and gaps == []
        ok, gaps = store.coverage_ok(["w1", "w2"], date(2025, 2, 1), date(2025, 11, 30))
        assert not ok and gaps == ["w2"]


def test_spans_cover_logic():
    j = date  # brevity
    assert _spans_cover([(j(2025, 1, 1), j(2025, 6, 30)),
                         (j(2025, 6, 1), j(2025, 12, 31))], j(2025, 2, 1), j(2025, 11, 1))
    assert not _spans_cover([(j(2025, 1, 1), j(2025, 3, 1)),
                             (j(2025, 5, 1), j(2025, 12, 31))], j(2025, 2, 1), j(2025, 11, 1))
    assert not _spans_cover([], j(2025, 1, 1), j(2025, 2, 1))


# ---- data-hygiene patches: null condition_id drop + key-aware dedup ----------

def _full_trade(tid, cid, *, tx="0xtx", tok="tok", oi=0, wallet="0xw"):
    return {"trade_id": tid, "wallet": wallet, "condition_id": cid,
            "outcome": "YES", "side": "BUY", "price": 0.5, "size_usdc": 10.0,
            "traded_at": pd.Timestamp("2025-01-01", tz="UTC"),
            "tx_hash": tx, "token_id": tok, "outcome_index": oi}


def test_load_trades_drops_null_condition_id():
    # a row with null condition_id must NOT survive an analysis load
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        good = pd.DataFrame([_full_trade("t1", "0xc1")])
        bad = pd.DataFrame([_full_trade("t2", None)])      # null condition_id
        store.save_wallet_trades("w1", good, date(2025, 1, 1), date(2025, 3, 31))
        store.save_wallet_trades("w2", bad, date(2025, 1, 1), date(2025, 3, 31))
        out = store.load_trades()
        assert set(out["condition_id"]) == {"0xc1"}        # null row dropped
        assert "t2" not in set(out["trade_id"])


def test_load_trades_dedup_prefers_populated_keys():
    # same trade_id in two wallet files; one copy has NA tx_hash/token_id/
    # outcome_index, the other is populated. The populated row must be kept.
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        populated = pd.DataFrame([_full_trade("dup", "0xc1", tx="0xFULL",
                                              tok="tokFULL", oi=1, wallet="wA")])
        missing = pd.DataFrame([{
            "trade_id": "dup", "wallet": "wB", "condition_id": "0xc1",
            "outcome": "YES", "side": "BUY", "price": 0.5, "size_usdc": 10.0,
            "traded_at": pd.Timestamp("2025-01-01", tz="UTC"),
            "tx_hash": None, "token_id": None, "outcome_index": None}])
        store.save_wallet_trades("wA", populated, date(2025, 1, 1), date(2025, 3, 31))
        store.save_wallet_trades("wB", missing, date(2025, 1, 1), date(2025, 3, 31))
        out = store.load_trades()
        row = out[out["trade_id"] == "dup"]
        assert len(row) == 1                               # deduped to one
        assert row.iloc[0]["tx_hash"] == "0xFULL"          # populated kept
        assert row.iloc[0]["token_id"] == "tokFULL"
        assert row.iloc[0]["outcome_index"] == 1


def test_load_trades_identical_duplicates_still_collapse():
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        a = pd.DataFrame([_full_trade("x", "0xc1", wallet="wA")])
        b = pd.DataFrame([_full_trade("x", "0xc1", wallet="wB")])  # same fill, diff wallet
        store.save_wallet_trades("wA", a, date(2025, 1, 1), date(2025, 3, 31))
        store.save_wallet_trades("wB", b, date(2025, 1, 1), date(2025, 3, 31))
        out = store.load_trades()
        assert (out["trade_id"] == "x").sum() == 1         # collapsed to one
