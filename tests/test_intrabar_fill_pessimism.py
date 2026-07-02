"""Phase 1.5 intra-bar fill pessimism — SIDE-AWARE test matrix.

build_prices_from_trades collapses each hourly bar to its LAST (close) print.
Pricing a fill at that close is optimistic when the bar traded through a worse
level. PriceBook.fill_price_at(..., side, intrabar_fill_policy="worst_in_bar")
prices a FILL at the side+outcome-ADVERSE extreme among the REAL prints in the
bar, when raw trades are available — falling back to close otherwise.

  outcome=YES, side=buy  -> max yes_price    outcome=YES, side=sell -> min yes_price
  outcome=NO,  side=buy  -> min yes_price    outcome=NO,  side=sell -> max yes_price

price_at() is the NEUTRAL mark/as-of lookup (no side, no policy) and is tested
separately to confirm it stays close-only.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pm_research.config import LatencyConfig
from pm_research.latency import PriceBook, LatencyModel


def _prices(rows):
    return pd.DataFrame({
        "condition_id": [r[0] for r in rows],
        "ts": pd.to_datetime([r[1] for r in rows]),
        "yes_price": [r[2] for r in rows],
    })


def _trades(rows):
    return pd.DataFrame({
        "condition_id": [r[0] for r in rows],
        "traded_at": pd.to_datetime([r[1] for r in rows]),
        "outcome": [r[2] for r in rows],
        "price": [r[3] for r in rows],
    })


# A single bar at 01:00 whose CLOSE (last print) is 0.50, which traded through
# 0.60 (high) and 0.40 (low) earlier in the hour.
PRICES = _prices([("c1", "2025-01-01T01:00:00Z", 0.50)])
TRADES = _trades([
    ("c1", "2025-01-01T01:05:00Z", "YES", 0.60),   # high within bar
    ("c1", "2025-01-01T01:20:00Z", "YES", 0.40),   # low within bar
    ("c1", "2025-01-01T01:55:00Z", "YES", 0.50),   # last -> matches close
])
MARKETS = pd.DataFrame({"condition_id": ["c1"], "liquidity_usdc": [20000.0]})
FILL_TS = pd.Timestamp("2025-01-01T01:30:00Z")     # falls in the 01:00 bar
WIB = "worst_in_bar"


# --------------------------------------------------------------------------
# neutral price_at(): mark/as-of only, no side, no policy
# --------------------------------------------------------------------------
def test_price_at_is_neutral_close_yes():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    assert book.price_at("c1", "YES", FILL_TS) == 0.50


def test_price_at_is_neutral_close_no():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    assert book.price_at("c1", "NO", FILL_TS) == 0.50    # 1 - 0.50


def test_price_at_takes_no_policy_or_side():
    # price_at must NOT accept intrabar_fill_policy/side anymore (neutral lookup)
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    with pytest.raises(TypeError):
        book.price_at("c1", "YES", FILL_TS, intrabar_fill_policy=WIB)


def test_price_at_unknown_outcome_raises():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    with pytest.raises(ValueError, match="unknown outcome"):
        book.price_at("c1", "MAYBE", FILL_TS)


# --------------------------------------------------------------------------
# fill_price_at(): side-aware adverse matrix
# --------------------------------------------------------------------------
def test_fill_close_policy_matches_legacy_value():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    # close policy is side-independent -> the close value
    assert book.fill_price_at("c1", "YES", FILL_TS, side="buy",
                              intrabar_fill_policy="close") == 0.50
    assert book.fill_price_at("c1", "YES", FILL_TS, side="sell",
                              intrabar_fill_policy="close") == 0.50
    # default policy is close
    assert book.fill_price_at("c1", "YES", FILL_TS, side="buy") == 0.50


def test_buy_yes_uses_bar_high():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    p = book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.60)            # max yes; buyer pays the high
    assert p > 0.50                            # worse than close for a buyer


def test_sell_yes_uses_bar_low():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    p = book.fill_price_at("c1", "YES", FILL_TS, side="sell", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.40)            # min yes; seller sells at the low
    assert p < 0.50                            # worse than close for a seller


def test_buy_no_uses_bar_low_yes():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    # NO buy: adverse = min yes (0.40) -> NO price = 1 - 0.40 = 0.60
    p = book.fill_price_at("c1", "NO", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.60)
    assert p > 0.50                            # worse than close NO (0.50) for a buyer


def test_sell_no_uses_bar_high_yes():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    # NO sell: adverse = max yes (0.60) -> NO price = 1 - 0.60 = 0.40
    p = book.fill_price_at("c1", "NO", FILL_TS, side="sell", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.40)
    assert p < 0.50                            # worse than close NO (0.50) for a seller


def test_buy_and_sell_are_opposite_extremes():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    buy_yes = book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    sell_yes = book.fill_price_at("c1", "YES", FILL_TS, side="sell", intrabar_fill_policy=WIB)
    assert buy_yes > sell_yes                  # buyer pays more than seller receives


# --------------------------------------------------------------------------
# NO-trade yes_price conversion before min/max
# --------------------------------------------------------------------------
def test_no_trades_convert_to_yes_before_extremes():
    # prints recorded as NO trades; their yes_price = 1 - price. A NO print at
    # 0.30 is yes_price 0.70; at 0.55 is yes_price 0.45. For a YES buyer the
    # adverse is max yes = 0.70.
    prices = _prices([("c2", "2025-01-01T01:00:00Z", 0.50)])
    trades = _trades([
        ("c2", "2025-01-01T01:05:00Z", "NO", 0.30),   # yes_price 0.70
        ("c2", "2025-01-01T01:25:00Z", "NO", 0.55),   # yes_price 0.45
    ])
    markets = pd.DataFrame({"condition_id": ["c2"], "liquidity_usdc": [20000.0]})
    book = PriceBook(prices, markets, trades=trades)
    p = book.fill_price_at("c2", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.70)            # max of {0.70, 0.45}


# --------------------------------------------------------------------------
# real-timestamp bucketing, no invention
# --------------------------------------------------------------------------
def test_prints_in_other_bars_are_not_used():
    prices = _prices([
        ("c1", "2025-01-01T01:00:00Z", 0.50),
        ("c1", "2025-01-01T02:00:00Z", 0.95),
    ])
    trades = _trades([
        ("c1", "2025-01-01T01:05:00Z", "YES", 0.60),   # 01:00 bar
        ("c1", "2025-01-01T02:10:00Z", "YES", 0.95),   # 02:00 bar, must be ignored
    ])
    book = PriceBook(prices, MARKETS, trades=trades)
    p = book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.60)


def test_worst_in_bar_returns_a_real_print():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    observed_yes = set(TRADES["price"].tolist())   # YES prints == yes_price
    p = book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    assert p in observed_yes


# --------------------------------------------------------------------------
# determinism: single / equal-price buckets
# --------------------------------------------------------------------------
def test_single_print_bar_equals_that_print():
    prices = _prices([("c1", "2025-01-01T01:00:00Z", 0.42)])
    trades = _trades([("c1", "2025-01-01T01:30:00Z", "YES", 0.42)])
    book = PriceBook(prices, MARKETS, trades=trades)
    for side in ("buy", "sell"):
        assert book.fill_price_at("c1", "YES", FILL_TS, side=side,
                                  intrabar_fill_policy=WIB) == pytest.approx(0.42)


def test_equal_price_bar_is_deterministic():
    prices = _prices([("c1", "2025-01-01T01:00:00Z", 0.42)])
    trades = _trades([
        ("c1", "2025-01-01T01:05:00Z", "YES", 0.42),
        ("c1", "2025-01-01T01:45:00Z", "YES", 0.42),
    ])
    book = PriceBook(prices, MARKETS, trades=trades)
    for side in ("buy", "sell"):
        assert book.fill_price_at("c1", "YES", FILL_TS, side=side,
                                  intrabar_fill_policy=WIB) == pytest.approx(0.42)


# --------------------------------------------------------------------------
# four-way source/bucket distinction + validation
# --------------------------------------------------------------------------
def test_no_trades_source_raises_under_worst_in_bar():
    book = PriceBook(PRICES, MARKETS)          # trades=None -> no source
    with pytest.raises(ValueError, match="requires raw trades"):
        book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)


def test_no_trades_source_close_is_fine():
    book = PriceBook(PRICES, MARKETS)          # trades=None
    assert book.fill_price_at("c1", "YES", FILL_TS, side="buy",
                              intrabar_fill_policy="close") == 0.50
    assert book.fill_price_at("c1", "YES", FILL_TS, side="buy") == 0.50   # default


def test_source_present_but_market_absent_falls_back_to_close():
    other = _trades([("cOTHER", "2025-01-01T01:05:00Z", "YES", 0.6)])
    book = PriceBook(PRICES, MARKETS, trades=other)
    p = book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.50)            # close, no raise


def test_sparse_bucket_falls_back_to_close():
    prices = _prices([
        ("c1", "2025-01-01T01:00:00Z", 0.50),
        ("c1", "2025-01-01T03:00:00Z", 0.50),
    ])
    trades = _trades([("c1", "2025-01-01T01:05:00Z", "YES", 0.60)])
    book = PriceBook(prices, MARKETS, trades=trades)
    # fill at 03:30 -> 03:00 bar has no prints -> close 0.50
    p = book.fill_price_at("c1", "YES", pd.Timestamp("2025-01-01T03:30:00Z"),
                           side="buy", intrabar_fill_policy=WIB)
    assert p == pytest.approx(0.50)


def test_unknown_policy_raises():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    with pytest.raises(ValueError, match="intrabar_fill_policy"):
        book.fill_price_at("c1", "YES", FILL_TS, side="buy", intrabar_fill_policy="bogus")


def test_unknown_side_raises():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    with pytest.raises(ValueError, match="unknown side"):
        book.fill_price_at("c1", "YES", FILL_TS, side="hodl", intrabar_fill_policy=WIB)


def test_unknown_outcome_raises_in_fill():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    with pytest.raises(ValueError, match="unknown outcome"):
        book.fill_price_at("c1", "MAYBE", FILL_TS, side="buy", intrabar_fill_policy=WIB)


# --------------------------------------------------------------------------
# config default + LatencyModel integration (entry = buy)
# --------------------------------------------------------------------------
def test_config_default_is_worst_in_bar():
    assert LatencyConfig().intrabar_fill_policy == "worst_in_bar"


def test_model_apply_entry_uses_side_buy():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    cfg = LatencyConfig(detection_delay_seconds=0, taker_fee_bps=0, max_chase=1.0,
                        intrabar_fill_policy="worst_in_bar", impact_k=0.0,
                        impact_k_sqrt=0.0)
    model = LatencyModel(cfg)
    fill = model.apply(condition_id="c1", outcome="YES", detected_at=FILL_TS,
                       leaders_avg_entry=0.60, size_usdc=100.0, book=book)
    assert fill.filled
    # entry buy YES -> bar high 0.60, zero impact/fee
    assert fill.fill_price == pytest.approx(0.60)


def test_model_apply_close_policy_matches_legacy():
    book = PriceBook(PRICES, MARKETS, trades=TRADES)
    cfg = LatencyConfig(detection_delay_seconds=0, taker_fee_bps=0, max_chase=1.0,
                        intrabar_fill_policy="close", impact_k=0.0, impact_k_sqrt=0.0)
    model = LatencyModel(cfg)
    fill = model.apply(condition_id="c1", outcome="YES", detected_at=FILL_TS,
                       leaders_avg_entry=0.60, size_usdc=100.0, book=book)
    assert fill.fill_price == pytest.approx(0.50)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
