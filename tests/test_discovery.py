"""Discovery tests — fake Gamma + Data API, no network."""
from __future__ import annotations

import urllib.parse

from pm_research.data.backfill import Backfiller
from pm_research.data.discovery import (DiscoveryConfig, discover,
                                        fetch_top_markets, wallet_stats)
from pm_research.data.store import Store
from tests.helpers import make_trades, ts

JAN1 = 1735689600
HOUR = 3600
CID_A = "0x" + "0a" * 32
CID_B = "0x" + "0b" * 32
CID_C = "0x" + "0c" * 32
M1 = "0x" + "01" * 32
M2 = "0x" + "02" * 32


def _print(i: int, wallet: str, cid: str, *, n_per_tx: int = 0,
           size: float = 100.0, ts_unix: int | None = None) -> dict:
    return {"proxyWallet": wallet, "timestamp": ts_unix or (JAN1 + i * HOUR),
            "conditionId": cid, "outcome": "Yes", "outcomeIndex": 0,
            "side": "BUY", "price": 0.5, "size": size, "usdcSize": size * 0.5,
            "transactionHash": f"0x{cid}-{wallet}-{i}", "asset": "1"}


def _fake_fetcher(markets_pages: dict, prints_by_market: dict):
    """Serves gamma /markets (keyed by closed flag + offset) and data /trades."""
    def fetch(url: str):
        p = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(p.query)
        if p.path.startswith("/markets"):
            key = (qs["closed"][0], int(qs.get("offset", ["0"])[0]))
            return markets_pages.get(key, [])
        if p.path.startswith("/trades"):
            cid = qs.get("market", [None])[0]
            offset = int(qs.get("offset", ["0"])[0])
            rows = prints_by_market.get(cid, [])
            limit = int(qs.get("limit", ["500"])[0])
            return rows[offset:offset + limit]
        return []
    return fetch


def _bf(markets_pages, prints_by_market, page_size: int = 500) -> Backfiller:
    import tempfile
    return Backfiller(Store(tempfile.mkdtemp()),
                      fetcher=_fake_fetcher(markets_pages, prints_by_market),
                      rate_limit_sleep=0.0, page_size=page_size)


def test_fetch_top_markets_pages_and_dedups():
    pages = {("false", 0): [{"conditionId": CID_A}, {"conditionId": CID_B}],
             ("false", 3): [{"conditionId": CID_B}, {"conditionId": CID_C}]}
    bf = _bf(pages, {})
    # limit param mirrors min(n,100)=3 → second page at offset 3
    cids = fetch_top_markets(bf, 3, closed=False)
    assert cids == [CID_A, CID_B, CID_C]


def test_wallet_stats_aggregates_per_wallet():
    trades = make_trades([
        {"wallet": "A", "condition_id": "m1", "size_usdc": 100.0,
         "traded_at": ts("2025-01-01")},
        {"wallet": "A", "condition_id": "m2", "size_usdc": 300.0,
         "traded_at": ts("2025-01-11")},
        {"wallet": "B", "condition_id": "m1", "size_usdc": 50.0,
         "traded_at": ts("2025-01-05")}])
    s = wallet_stats(trades).set_index("wallet")
    assert s.loc["A", "n_trades"] == 2
    assert abs(s.loc["A", "volume_usdc"] - 400.0) < 1e-9
    assert s.loc["A", "n_markets"] == 2
    assert abs(s.loc["A", "trades_per_day"] - 0.2) < 1e-9   # 2 trades / 10 days


def test_discover_filters_dust_and_bots_and_ranks_by_volume():
    markets_pages = {("false", 0): [{"conditionId": M1}],
                     ("true", 0): [{"conditionId": M2}]}
    prints = {
        M1:
            # WHALE: 20 trades, big size, spread over ~20h... span < 1 day →
            # trades_per_day uses 1-day floor → 20/day, under bot cutoff
            [_print(i, "WHALE", M1, size=1000.0) for i in range(20)]
            # DUST: 2 trades only
            + [_print(i, "DUST", M1, ts_unix=JAN1 + i) for i in range(2)],
        M2:
            # BOT: 600 trades within ~2 days → ~300/day > 200 cutoff
            [_print(i, "BOT", M2, size=50.0,
                    ts_unix=JAN1 + i * 300) for i in range(600)]
            # MID: 15 trades over 15 days
            + [_print(i, "MID", M2, size=200.0,
                      ts_unix=JAN1 + i * 86400) for i in range(15)],
    }
    cfg = DiscoveryConfig(top_markets=2, per_market_pages=5, min_trades=10,
                          min_volume_usdc=1000.0, max_trades_per_day=200.0,
                          top_n=10)
    cand = discover(_bf(markets_pages, prints), cfg)
    wallets = cand["wallet"].tolist()
    assert wallets == ["WHALE", "MID"]          # ranked by volume
    assert "DUST" not in wallets and "BOT" not in wallets


def test_discover_respects_per_market_page_bound():
    markets_pages = {("false", 0): [{"conditionId": M1}], ("true", 0): []}
    prints = {M1: [_print(i, f"W{i % 5}", M1, size=500.0)
                       for i in range(50)]}
    cfg = DiscoveryConfig(top_markets=2, per_market_pages=1, min_trades=1,
                          min_volume_usdc=0.0, top_n=10)
    cand = discover(_bf(markets_pages, prints, page_size=10), cfg)
    # only 1 page x 10 rows fetched → 10 prints across 5 wallets, 2 each
    assert int(cand["n_trades"].sum()) == 10


def test_discover_survives_per_market_failures_and_skips_bad_cids():
    from pm_research.data.backfill import ApiError
    good = "0x" + "aa" * 32
    bad = "0x" + "bb" * 32
    markets_pages = {("false", 0): [{"conditionId": good},
                                    {"conditionId": ""},          # invalid: dropped
                                    {"conditionId": "0xshort"}],  # invalid: dropped
                     ("true", 0): [{"conditionId": bad}]}
    def fetch(url):
        import urllib.parse as up
        p = up.urlparse(url)
        qs = up.parse_qs(p.query)
        if p.path.startswith("/markets"):
            return markets_pages.get((qs["closed"][0], int(qs.get("offset", ["0"])[0])), [])
        cid = qs.get("market", [None])[0]
        if cid == bad:
            raise ApiError(400, url, '{"error":"boom"}')   # one market fails
        if int(qs.get("offset", ["0"])[0]) > 0:
            return []
        return [_print(i, "W", good, size=500.0) for i in range(12)]
    import tempfile
    bf = Backfiller(Store(tempfile.mkdtemp()), fetcher=fetch, rate_limit_sleep=0.0)
    cfg = DiscoveryConfig(top_markets=2, per_market_pages=2, min_trades=1,
                          min_volume_usdc=0.0, top_n=10)
    cand = discover(bf, cfg)                   # must not raise
    assert cand["wallet"].tolist() == ["W"]    # good market still harvested
