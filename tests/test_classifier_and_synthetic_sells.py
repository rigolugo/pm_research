"""Tests for two Phase-1 fixes:

1. wallet_classifier: the sell_buy_ratio / median_hold_hours tells used a
   broken `is not np.nan` IDENTITY guard. These tests pin the corrected
   pd.notna()-based behaviour, including the inf (all-SELL) and NaN
   (never-round-tripped) edge cases.

2. synthetic: the generator gained an OPTIONAL market-maker population that
   injects SELLs. These tests assert (a) the default world is unchanged
   (still BUY-only, same row count for a fixed seed) and (b) MM mode produces
   SELLs that the classifier actually labels MARKET_MAKER.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pm_research.data.synthetic import WorldConfig, generate
from pm_research.wallet_classifier import classify, _wallet_behavior


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _ts(h: int) -> pd.Timestamp:
    return pd.Timestamp("2025-06-01", tz="UTC") + pd.Timedelta(hours=h)


def _mk_trades(rows: list[dict]) -> pd.DataFrame:
    """rows: list of (wallet, condition_id, outcome, side, price, hours)."""
    out = []
    for i, r in enumerate(rows):
        out.append({
            "trade_id": f"t{i:05d}", "wallet": r["wallet"],
            "condition_id": r["cid"], "outcome": r["outcome"],
            "side": r["side"], "price": r["price"],
            "size_usdc": r.get("size", 100.0), "traded_at": _ts(r["h"])})
    return pd.DataFrame(out)


# --------------------------------------------------------------------------
# 1. classifier NaN / inf edge cases
# --------------------------------------------------------------------------
def test_all_sell_wallet_trips_sell_buy_tell():
    """An all-SELL wallet has sell_buy_ratio == inf. The old `is not np.nan`
    guard happened to let inf through, but for the wrong reason; the fixed
    pd.notna() guard must still treat inf as a tripped MM tell."""
    rows = [{"wallet": "0xmaker", "cid": f"0xc{m:02d}", "outcome": "YES",
             "side": "SELL", "price": 0.5, "h": m} for m in range(25)]
    b = _wallet_behavior(_mk_trades(rows))
    assert np.isinf(b["sell_buy_ratio"])  # inf, not NaN
    # the tell itself: pd.notna(inf) is True and inf >= 0.4 is True
    assert bool(pd.notna(b["sell_buy_ratio"]) and b["sell_buy_ratio"] >= 0.4)


def test_never_roundtripped_wallet_does_not_trip_hold_tell():
    """A wallet that only ever BUYs has median_hold_hours == NaN. A NaN hold
    must NOT trip the 'holds briefly' MM tell (the bug would have raised or
    mis-fired). Pure buy-and-hold should land DIRECTIONAL, not MARKET_MAKER."""
    rows = [{"wallet": "0xhodler", "cid": f"0xc{m:02d}", "outcome": "YES",
             "side": "BUY", "price": 0.5, "h": m} for m in range(25)]
    b = _wallet_behavior(_mk_trades(rows))
    assert np.isnan(b["median_hold_hours"])
    df = classify(_mk_trades(rows))
    label = df.loc[df["wallet"] == "0xhodler", "label"].iloc[0]
    assert label == "DIRECTIONAL"


def test_fast_two_sided_roundtripper_is_market_maker():
    """A wallet that buys and sells both outcomes quickly across many markets
    should trip a majority of tells and classify MARKET_MAKER."""
    rows = []
    for m in range(60):  # wide breadth
        cid = f"0xc{m:03d}"
        for oc in ("YES", "NO"):  # two-sided
            rows.append({"wallet": "0xmm", "cid": cid, "outcome": oc,
                         "side": "BUY", "price": 0.5, "h": m * 10})
            rows.append({"wallet": "0xmm", "cid": cid, "outcome": oc,
                         "side": "SELL", "price": 0.5, "h": m * 10 + 1})  # 1h hold
    df = classify(_mk_trades(rows))
    row = df.loc[df["wallet"] == "0xmm"].iloc[0]
    assert row["label"] == "MARKET_MAKER"
    assert row["mm_score"] >= 3


def test_below_min_trades_is_unknown():
    rows = [{"wallet": "0xtiny", "cid": "0xc00", "outcome": "YES",
             "side": "BUY", "price": 0.5, "h": 1}]
    df = classify(_mk_trades(rows))
    assert df.loc[df["wallet"] == "0xtiny", "label"].iloc[0] == "UNKNOWN"


# --------------------------------------------------------------------------
# 2. synthetic SELL injection
# --------------------------------------------------------------------------
def test_default_world_is_buy_only_and_stable():
    """With n_market_makers == 0 the world must be BUY-only and identical
    across runs for a fixed seed (the property the engine tests depend on)."""
    w1 = generate(WorldConfig(n_markets=40, n_skilled=5, n_random=10,
                              trades_per_trader=20, seed=7))
    w2 = generate(WorldConfig(n_markets=40, n_skilled=5, n_random=10,
                              trades_per_trader=20, seed=7))
    assert (w1.trades["side"] == "BUY").all()
    assert len(w1.trades) == len(w2.trades)
    assert w1.market_maker_wallets == []
    # full row-for-row stability
    pd.testing.assert_frame_equal(w1.trades, w2.trades)


def test_mm_mode_injects_sells_and_classifies():
    """With n_market_makers > 0 the world gains SELLs, and the injected MM
    wallets are detectable by the classifier."""
    w = generate(WorldConfig(n_markets=60, n_skilled=5, n_random=10,
                             trades_per_trader=20, n_market_makers=4,
                             mm_trades_per_trader=50, seed=7))
    sell_frac = (w.trades["side"] == "SELL").mean()
    assert sell_frac > 0.0
    assert len(w.market_maker_wallets) == 4
    df = classify(w.trades)
    mm_labels = df[df["wallet"].isin(w.market_maker_wallets)]["label"]
    # at least a majority of injected MMs should be caught as MARKET_MAKER
    assert (mm_labels == "MARKET_MAKER").sum() >= 3


def test_mm_mode_leaves_directional_population_intact():
    """Injecting MMs must not relabel the skilled/random buy-and-hold wallets
    as market makers."""
    w = generate(WorldConfig(n_markets=60, n_skilled=6, n_random=12,
                             trades_per_trader=30, n_market_makers=3,
                             mm_trades_per_trader=50, seed=11))
    df = classify(w.trades)
    skilled_labels = df[df["wallet"].isin(w.skilled_wallets)]["label"]
    # buy-and-hold skilled traders should not be MM
    assert (skilled_labels == "MARKET_MAKER").sum() == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
