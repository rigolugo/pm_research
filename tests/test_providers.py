"""Provider adapter tests with FAKE library clients — no network, no install.

The fakes duck-type the real libraries: polymarket-apis style (sync client,
Pydantic models with model_dump) and aiopolymarket style (async context
manager clients). Both must land identical canonical frames in the store.
"""
from __future__ import annotations

import tempfile
from datetime import date

from pm_research.data.providers import (AiopolymarketProvider,
                                        PolymarketApisProvider, _dump)
from pm_research.data.store import Store

JAN1 = 1735689600


class _Model:
    """Stands in for a Pydantic v2 model: exposes model_dump(by_alias=True)."""
    def __init__(self, **raw):
        self._raw = raw

    def model_dump(self, by_alias: bool = False):
        return dict(self._raw)


def _raw(i: int, wallet: str = "0xw1") -> dict:
    return {"proxyWallet": wallet, "timestamp": JAN1 + i * 3600,
            "conditionId": "0xc1", "outcome": "Yes", "outcomeIndex": 0,
            "side": "BUY", "price": 0.4 + i * 0.01, "size": 100.0,
            "usdcSize": 40.0, "transactionHash": f"0xtx{i}", "asset": "111"}


_MARKET = {"conditionId": "0xc1", "category": "Other", "liquidityNum": 1000.0,
           "createdAt": "2025-01-01T00:00:00Z", "endDate": "2025-02-01T00:00:00Z",
           "closed": True, "outcomes": '["Yes","No"]',
           "outcomePrices": '["1","0"]', "closedTime": None}


def test_dump_handles_models_dicts_and_objects():
    assert _dump({"a": 1}) == {"a": 1}
    assert _dump(_Model(a=1)) == {"a": 1}
    class Plain:
        def __init__(self):
            self.a = 1
    assert _dump(Plain()) == {"a": 1}


# ---------------------- polymarket-apis style (sync) -----------------------

class FakeDataClient:
    def get_trades(self, limit: int, offset: int, user: str | None = None,
                   condition_id: str | None = None):
        rows = [_Model(**_raw(i)) for i in range(3)]
        return rows[offset:offset + limit]


class FakeGammaClient:
    def get_markets(self, condition_ids: list[str], limit: int):
        return [_Model(**_MARKET)]


def test_polymarket_apis_provider_lands_canonical_frames():
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        p = PolymarketApisProvider(store, data_client=FakeDataClient(),
                                   gamma_client=FakeGammaClient(), page_size=2)
        n = p.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 12, 31))
        assert n == 3                                    # paginated 2 + 1
        nm, nr = p.backfill_markets(["0xc1"])
        assert (nm, nr) == (1, 1)
        assert p.backfill_prices_from_prints(["0xc1"]) >= 1
        trades = store.load_trades(["0xw1"])
        assert list(trades.columns)[:3] == ["trade_id", "wallet", "condition_id"]
        assert not store.load_resolutions().empty


# ---------------------- aiopolymarket style (async) ------------------------

class FakeAsyncDataClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get_trades(self, limit: int, offset: int, user: str | None = None,
                         market: str | None = None):
        rows = [_Model(**_raw(i)) for i in range(3)]
        return rows[offset:offset + limit]


class FakeAsyncGammaClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get_markets(self, condition_ids: list[str], limit: int):
        return [_Model(**_MARKET)]


def test_aiopolymarket_provider_matches_sync_provider_output():
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        sync_store, async_store = Store(d1), Store(d2)
        ps = PolymarketApisProvider(sync_store, data_client=FakeDataClient(),
                                    gamma_client=FakeGammaClient())
        pa = AiopolymarketProvider(async_store,
                                   data_client_factory=FakeAsyncDataClient,
                                   gamma_client_factory=FakeAsyncGammaClient)
        ps.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 12, 31))
        pa.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 12, 31))
        a = sync_store.load_trades(["0xw1"]).reset_index(drop=True)
        b = async_store.load_trades(["0xw1"]).reset_index(drop=True)
        assert a.equals(b)        # same parsers → byte-identical frames
