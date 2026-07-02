"""Backfill + parser tests against REALISTIC API payloads (verified shapes:
unix-seconds timestamps, camelCase conditionId, no per-fill id field)."""
from __future__ import annotations

import tempfile
import pathlib
import urllib.parse
from datetime import date

import pandas as pd

from pm_research.data import schemas
from pm_research.data.backfill import (Backfiller, build_prices_from_trades,
                                       parse_markets, parse_price_history,
                                       parse_trades)
from pm_research.data.store import Store

JAN1 = 1735689600  # 2025-01-01 00:00 UTC
DAY = 86400
CID = "0x" + "c1" * 32


def _raw_trade(i: int, ts_unix: int, *, outcome: str = "Yes",
               price: float = 0.42, size: float = 100.0,
               wallet: str = "0xw1") -> dict:
    """Shape of a real data-api /trades row (no `id`, unix int timestamp)."""
    return {"proxyWallet": wallet, "timestamp": ts_unix,
            "conditionId": CID, "outcome": outcome, "outcomeIndex": 0,
            "side": "BUY", "price": price, "size": size,
            "usdcSize": size * price, "transactionHash": f"0xtx{i}",
            "asset": "1234567890"}


def _fake_api(routes: dict):
    """routes: prefix -> {offset: payload}. Matches by path prefix."""
    def fetch(url: str):
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        offset = int(qs.get("offset", ["0"])[0])
        for prefix, pages in routes.items():
            if parsed.path.startswith(prefix):
                if callable(pages):
                    return pages(qs)
                return pages.get(offset, [])
        return []
    return fetch


# ----------------------------- parse_trades --------------------------------

def test_parse_trades_handles_unix_timestamp_and_camelcase_keys():
    df = parse_trades([_raw_trade(0, JAN1)], wallet="0xw1")
    row = df.iloc[0]
    assert row["condition_id"] == CID               # conditionId, not condition_id
    assert row["traded_at"] == pd.Timestamp("2025-01-01", tz="UTC")
    assert row["outcome"] == "YES"
    assert abs(row["size_usdc"] - 42.0) < 1e-9         # usdcSize preferred


def test_parse_trades_composite_id_is_stable_and_distinguishes_fills():
    a = _raw_trade(0, JAN1)
    b = _raw_trade(0, JAN1)            # identical fill seen twice → same id
    c = _raw_trade(0, JAN1, size=50.0)  # different size → different fill
    ids = parse_trades([a, b, c], "0xw1")["trade_id"]
    assert ids.iloc[0] == ids.iloc[1]
    assert ids.iloc[0] != ids.iloc[2]


def test_parse_trades_keeps_proxywallet_for_market_wide_fetches():
    df = parse_trades([_raw_trade(0, JAN1, wallet="0xother")], wallet=None)
    assert df.iloc[0]["wallet"] == "0xother"


# ---- join-key persistence (tx_hash / token_id) for future OrderFilled join ----

def test_parse_trades_persists_tx_hash_from_transaction_hash():
    df = parse_trades([_raw_trade(0, JAN1)], wallet="0xw1")
    # _raw_trade sets transactionHash = f"0xtx{i}" -> "0xtx0"
    assert df.iloc[0]["tx_hash"] == "0xtx0"


def test_parse_trades_persists_token_id_from_asset():
    df = parse_trades([_raw_trade(0, JAN1)], wallet="0xw1")
    assert df.iloc[0]["token_id"] == "1234567890"   # _raw_trade asset


def test_trades_cols_includes_join_keys_and_keeps_required_cols():
    for c in ("tx_hash", "token_id"):
        assert c in schemas.TRADES_COLS
    # the original required columns are all still present and unchanged
    for c in ("trade_id", "wallet", "condition_id", "outcome", "side",
              "price", "size_usdc", "traded_at"):
        assert c in schemas.TRADES_COLS


def test_trade_id_unchanged_by_join_key_persistence():
    # trade_id is hashed from the RAW api dict, not the frame, so adding columns
    # must not move it. Pin a stable value for a representative fixture.
    raw = _raw_trade(0, JAN1)
    tid = parse_trades([raw], "0xw1")["trade_id"].iloc[0]
    # recompute from a second identical parse -> identical id (stability)
    tid2 = parse_trades([dict(raw)], "0xw1")["trade_id"].iloc[0]
    assert tid == tid2
    # and the id still depends on transactionHash/asset (changing asset changes id)
    raw_diff = dict(raw); raw_diff["asset"] = "9999999999"
    tid_diff = parse_trades([raw_diff], "0xw1")["trade_id"].iloc[0]
    assert tid_diff != tid


def test_parse_trades_missing_transaction_hash_is_empty_string():
    raw = _raw_trade(0, JAN1)
    del raw["transactionHash"]
    df = parse_trades([raw], "0xw1")
    assert df.iloc[0]["tx_hash"] == ""          # parser convention: missing -> ""


def test_parse_trades_missing_asset_is_empty_string():
    raw = _raw_trade(0, JAN1)
    del raw["asset"]
    df = parse_trades([raw], "0xw1")
    assert df.iloc[0]["token_id"] == ""


def test_validate_fills_missing_join_keys_for_old_frames():
    # an OLD stored frame predating the join-key columns must NOT crash validate;
    # the additive columns are filled with NA instead.
    old = pd.DataFrame({
        "trade_id": ["t1"], "wallet": ["0xw"], "condition_id": [CID],
        "outcome": ["YES"], "side": ["BUY"], "price": [0.5],
        "size_usdc": [10.0], "traded_at": [pd.Timestamp("2025-01-01", tz="UTC")],
    })  # note: NO tx_hash / token_id
    out = schemas.validate(old, schemas.TRADES_COLS, "trades")
    assert "tx_hash" in out.columns and "token_id" in out.columns
    assert out["tx_hash"].isna().all() and out["token_id"].isna().all()


def test_validate_still_raises_on_genuinely_missing_required_column():
    # backward-compat fill must NOT weaken strictness for real required columns
    broken = pd.DataFrame({"trade_id": ["t1"]})   # missing almost everything
    try:
        schemas.validate(broken, schemas.TRADES_COLS, "trades")
        assert False, "expected ValueError for missing required columns"
    except ValueError as e:
        # the error names a hard-missing required column, not the fillable ones
        assert "wallet" in str(e) or "condition_id" in str(e)
        assert "tx_hash" not in str(e) and "token_id" not in str(e)


# ---- outcome_index persistence + named-outcome semantics ---------------------

def test_parse_trades_persists_outcome_index():
    df = parse_trades([_raw_trade(0, JAN1)], wallet="0xw1")
    # _raw_trade sets outcomeIndex = 0
    assert df.iloc[0]["outcome_index"] == 0


def test_trades_cols_includes_outcome_index():
    assert "outcome_index" in schemas.TRADES_COLS


def test_parse_trades_missing_outcome_index_is_none():
    raw = _raw_trade(0, JAN1)
    del raw["outcomeIndex"]
    df = parse_trades([raw], "0xw1")
    # int field: missing -> None/NA, NOT "" (which would corrupt dtype)
    assert pd.isna(df.iloc[0]["outcome_index"])


def test_parse_trades_preserves_named_outcome_label_not_coerced():
    # a multi-outcome market label must be kept (uppercased), NOT coerced to YES/NO
    df = parse_trades([_raw_trade(0, JAN1, outcome="Lakers")], "0xw1")
    assert df.iloc[0]["outcome"] == "LAKERS"        # preserved (uppercased)
    assert df.iloc[0]["outcome"] not in ("YES", "NO")


def test_outcome_index_independent_of_outcome_label():
    # named outcome can carry any index; index is NOT derived from the label
    raw = _raw_trade(0, JAN1, outcome="Zverev")
    raw["outcomeIndex"] = 3
    df = parse_trades([raw], "0xw1")
    assert df.iloc[0]["outcome"] == "ZVEREV"
    assert df.iloc[0]["outcome_index"] == 3


def test_trade_id_stable_with_outcome_index_persisted():
    # _trade_id already hashed outcomeIndex from the raw dict; persisting it as a
    # column must not move the id. Pin stability and index-dependence.
    raw = _raw_trade(0, JAN1)
    tid = parse_trades([raw], "0xw1")["trade_id"].iloc[0]
    tid2 = parse_trades([dict(raw)], "0xw1")["trade_id"].iloc[0]
    assert tid == tid2
    # changing the index changes the id (it is part of the composite hash)
    raw_diff = dict(raw); raw_diff["outcomeIndex"] = 1
    assert parse_trades([raw_diff], "0xw1")["trade_id"].iloc[0] != tid


def test_validate_fills_missing_outcome_index_for_old_frames():
    # OLD frame predating outcome_index must NOT crash validate -> filled NA
    old = pd.DataFrame({
        "trade_id": ["t1"], "wallet": ["0xw"], "condition_id": [CID],
        "outcome": ["YES"], "side": ["BUY"], "price": [0.5],
        "size_usdc": [10.0], "traded_at": [pd.Timestamp("2025-01-01", tz="UTC")],
        "tx_hash": ["0xtx"], "token_id": ["tok"],
    })  # note: NO outcome_index
    out = schemas.validate(old, schemas.TRADES_COLS, "trades")
    assert "outcome_index" in out.columns
    assert out["outcome_index"].isna().all()


def test_yes_price_conversion_unchanged_by_this_patch():
    # GUARD: this patch must NOT touch the yes_price conversion. Confirm the
    # legacy binary behavior still stands (outcome=="YES" -> price; else 1-price).
    src = (pathlib.Path(__file__).resolve().parents[1]
           / "pm_research" / "data" / "backfill.py").read_text()
    assert 't["outcome"] == "YES", 1.0 - t["price"]' in src


# ----------------------------- parse_markets -------------------------------

def _raw_market(closed: bool = True, winner_idx: int = 0) -> dict:
    prices = ["0", "0"]
    prices[winner_idx] = "1"
    return {"conditionId": CID, "category": "Politics",
            "liquidityNum": 12345.6, "createdAt": "2025-01-01T00:00:00Z",
            "endDate": "2025-02-01T00:00:00Z", "closed": closed,
            "outcomes": '["Yes","No"]',
            "outcomePrices": f'["{prices[0]}","{prices[1]}"]',
            "closedTime": "2025-02-01 12:00:00+00" if closed else None}


def test_parse_markets_extracts_metadata_and_resolution():
    markets, res = parse_markets([_raw_market(closed=True, winner_idx=1)])
    assert markets.iloc[0]["condition_id"] == CID
    assert abs(markets.iloc[0]["liquidity_usdc"] - 12345.6) < 1e-9
    assert len(res) == 1 and res.iloc[0]["winning_outcome"] == "NO"


def test_parse_markets_open_market_yields_no_resolution():
    _, res = parse_markets([_raw_market(closed=False)])
    assert len(res) == 0


def test_parse_markets_unresolved_prices_yield_no_resolution():
    m = _raw_market(closed=True)
    m["outcomePrices"] = '["0.55","0.45"]'   # closed but no >=0.99 winner
    _, res = parse_markets([m])
    assert len(res) == 0


# ------------------------- prices from prints / clob ------------------------

def test_build_prices_from_trades_inverts_no_and_resamples_hourly():
    trades = parse_trades([
        _raw_trade(0, JAN1, outcome="Yes", price=0.40),
        _raw_trade(1, JAN1 + 600, outcome="No", price=0.55),   # YES = 0.45
        _raw_trade(2, JAN1 + 3 * 3600, outcome="Yes", price=0.50),
    ], "0xw1")
    prices = build_prices_from_trades(trades, freq="1h")
    s = prices.set_index("ts")["yes_price"]
    assert abs(s[pd.Timestamp("2025-01-01 00:00", tz="UTC")] - 0.45) < 1e-9  # last print in hour
    assert abs(s[pd.Timestamp("2025-01-01 01:00", tz="UTC")] - 0.45) < 1e-9  # ffill gap
    assert abs(s[pd.Timestamp("2025-01-01 03:00", tz="UTC")] - 0.50) < 1e-9


def test_parse_price_history_clob_shape():
    raw = {"history": [{"t": JAN1, "p": 0.61}, {"t": JAN1 + 3600, "p": 0.62}]}
    df = parse_price_history(raw, CID, token_is_yes=False)
    assert len(df) == 2
    assert abs(df.iloc[0]["yes_price"] - 0.39) < 1e-9   # NO token inverted


# ------------------------------ Backfiller ---------------------------------

def test_backfill_wallet_paginates_filters_and_records_coverage():
    pages = {0: [_raw_trade(i, JAN1 + i * DAY) for i in range(3)], 3: []}
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=_fake_api({"/trades": pages}),
                        rate_limit_sleep=0.0, page_size=3)
        n = bf.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 12, 31))
        assert n == 3
        assert len(store.load_trades(["0xw1"])) == 3
        ok, _ = store.coverage_ok(["0xw1"], date(2025, 2, 1), date(2025, 11, 1))
        assert ok


def test_backfill_idempotent_on_rerun_without_fill_ids():
    pages = {0: [_raw_trade(0, JAN1)]}
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=_fake_api({"/trades": pages}),
                        rate_limit_sleep=0.0)
        bf.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 3, 31))
        bf.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 3, 31))
        assert len(store.load_trades(["0xw1"])) == 1   # composite hash dedup


def test_resume_skips_wallets_already_covered():
    """`resume=True` must skip wallets whose stored coverage already spans
    [start, end], including bot-skip markers — without re-hitting the API."""
    calls = {"n": 0}
    pages = {0: [_raw_trade(0, JAN1)]}

    def fetch(url):
        calls["n"] += 1
        return _fake_api({"/trades": pages})(url)

    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=fetch, rate_limit_sleep=0.0)
        start, end = date(2025, 1, 1), date(2025, 3, 31)

        # first run: both wallets backfilled normally
        out1 = bf.backfill(["0xw1", "0xw2"], start, end)
        assert set(out1) == {"0xw1", "0xw2"}
        calls_after_first = calls["n"]
        assert calls_after_first > 0

        # second run with resume: both already covered -> NO new fetches,
        # NOT even attempted
        out2 = bf.backfill(["0xw1", "0xw2"], start, end, resume=True)
        assert out2 == {}
        assert calls["n"] == calls_after_first

        # a brand-new wallet (no coverage yet) is still backfilled under resume
        out3 = bf.backfill(["0xw1", "0xw3"], start, end, resume=True)
        assert set(out3) == {"0xw3"}
        assert calls["n"] > calls_after_first


def test_resume_skips_bot_marked_wallets():
    """A wallet that was recorded as a bot (0 trades saved, but coverage
    written) must also be skipped on resume — not re-walked."""
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        start, end = date(2025, 1, 1), date(2025, 3, 31)
        store.save_wallet_trades("0xbot", schemas.empty(schemas.TRADES_COLS),
                                 start, end)

        def fetch(url):
            raise AssertionError("should not be called for a resumed bot wallet")

        bf = Backfiller(store, fetcher=fetch, rate_limit_sleep=0.0)
        out = bf.backfill(["0xbot"], start, end, resume=True)
        assert out == {}


def test_backfill_full_assembles_all_four_frames():
    def trades_route(qs):
        # same payload whether queried by user or by market
        return [_raw_trade(0, JAN1, price=0.40),
                _raw_trade(1, JAN1 + 3600, outcome="No", price=0.55)]
    routes = {"/trades": trades_route,
              "/markets": {0: [_raw_market(closed=True, winner_idx=0)]}}
    # gamma route keyed differently: handle via callable too
    def gamma_route(qs):
        return [_raw_market(closed=True, winner_idx=0)]
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=_fake_api({"/trades": trades_route,
                                                  "/markets": gamma_route}),
                        rate_limit_sleep=0.0)
        rep = bf.backfill_full(["0xw1"], date(2025, 1, 1), date(2025, 12, 31))
        assert rep["markets"] == 1 and rep["resolutions"] == 1
        assert rep["price_rows"] >= 1
        assert not store.load_markets().empty
        assert not store.load_resolutions().empty
        assert not store.load_prices().empty


def test_backfill_full_tolerates_trades_with_missing_condition_id():
    """A real /trades row missing `conditionId` parses to condition_id="".
    That "" must NOT be sent to the Gamma API (it 422s on an empty
    condition_ids param and crashes the whole run) nor to
    fetch_market_trades (which raises on invalid condition ids).

    Canonical contract (Option A): missing condition_id means "not
    analysis-eligible" — the row is still PERSISTED in raw parquet (no data
    loss at storage), but is DROPPED on analysis load (load_trades), because a
    row with no condition cannot be assigned to a market.
    """
    good_row = _raw_trade(0, JAN1, price=0.40)
    bad_row = dict(good_row)
    bad_row.pop("conditionId")          # -> condition_id == "" after parsing
    bad_row["transactionHash"] = "0xtxbad"

    def trades_route(qs):
        return [good_row, bad_row]

    def gamma_route(qs):
        # if "" ever lands here as a condition_ids param, the real API 422s;
        # assert it never appears
        assert "" not in qs.get("condition_ids", [])
        return [_raw_market(closed=True, winner_idx=0)]

    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=_fake_api({"/trades": trades_route,
                                                  "/markets": gamma_route}),
                        rate_limit_sleep=0.0)
        rep = bf.backfill_full(["0xw1"], date(2025, 1, 1), date(2025, 12, 31))
        assert rep["markets"] == 1 and rep["resolutions"] == 1
        assert rep["condition_ids"] == 1   # "" excluded from the count
        # backfill tolerated the missing-condition row without crashing.

        # PERSISTENCE: both rows are still in the raw parquet (no storage loss).
        raw = pd.read_parquet(pathlib.Path(d) / "trades" / "0xw1.parquet")
        assert len(raw) == 2
        assert "" in set(raw["condition_id"].astype(str))   # bad row persisted

        # ANALYSIS LOAD: the missing-condition row is dropped (not eligible).
        loaded = store.load_trades(["0xw1"])
        assert len(loaded) == 1                              # bad row dropped
        assert "" not in set(loaded["condition_id"].astype(str))
        assert "0xtxbad" not in set(loaded["tx_hash"].astype(str))


# ------------------- error transparency & cid validation --------------------

def test_fetch_market_trades_rejects_malformed_condition_id():
    with tempfile.TemporaryDirectory() as d:
        bf = Backfiller(Store(d), fetcher=lambda u: [], rate_limit_sleep=0.0)
        try:
            bf.fetch_market_trades("0xdeadbeef")   # too short — would 400 upstream
            raise AssertionError("should have raised")
        except ValueError as e:
            assert "64 hex" in str(e)


def test_valid_condition_id_passes_validation():
    from pm_research.data.backfill import is_condition_id
    good = "0x" + "ab12" * 16
    assert is_condition_id(good)
    assert not is_condition_id("")
    assert not is_condition_id("0x123")
    assert not is_condition_id("dd22" * 16)    # missing 0x


def test_api_error_carries_url_and_body():
    from pm_research.data.backfill import ApiError
    e = ApiError(400, "https://x/trades?market=bad", '{"error":"invalid market"}')
    assert "400" in str(e) and "invalid market" in str(e) and "/trades" in str(e)


def test_wallet_queries_send_taker_only_false_market_queries_do_not():
    seen = []
    def spy(url):
        seen.append(url)
        return []
    with tempfile.TemporaryDirectory() as d:
        bf = Backfiller(Store(d), fetcher=spy, rate_limit_sleep=0.0)
        bf.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 2, 1))
        bf.fetch_market_trades("0x" + "ab" * 32)
    assert "takerOnly=false" in seen[0]        # wallet history: include maker fills
    assert "takerOnly" not in seen[1]          # market prints: API default


# --------------------- offset cap & deep history walk ----------------------

def test_pagination_never_exceeds_offset_cap_and_keeps_partial():
    """Endless fake data: requests must stop at offset 3000, keeping rows."""
    seen_offsets = []
    def fetch(url):
        import urllib.parse as up
        qs = up.parse_qs(up.urlparse(url).query)
        off = int(qs.get("offset", ["0"])[0])
        seen_offsets.append(off)
        lim = int(qs.get("limit", ["500"])[0])
        return [_raw_trade(off + i, JAN1 + (off + i)) for i in range(lim)]
    with tempfile.TemporaryDirectory() as d:
        bf = Backfiller(Store(d), fetcher=fetch, rate_limit_sleep=0.0)
        df = bf._paged_trades({"user": "0xw1"})
        assert max(seen_offsets) <= 3000
        assert len(df) == 3500                      # 7 pages x 500, the cap


def test_mid_pagination_api_error_returns_partial_not_raise():
    from pm_research.data.backfill import ApiError
    def fetch(url):
        import urllib.parse as up
        off = int(up.parse_qs(up.urlparse(url).query).get("offset", ["0"])[0])
        if off >= 1000:
            raise ApiError(400, url, '{"error":"max historical activity offset of 3000 exceeded"}')
        return [_raw_trade(off + i, JAN1 + (off + i)) for i in range(500)]
    with tempfile.TemporaryDirectory() as d:
        bf = Backfiller(Store(d), fetcher=fetch, rate_limit_sleep=0.0)
        df = bf._paged_trades({"user": "0xw1"})     # must not raise
        assert len(df) == 1000


def test_deep_wallet_walk_recovers_history_beyond_cap():
    """8000 trades, one per minute. /trades alone caps at 3500; the windowed
    /activity walk must recover ALL of them within [start, end]."""
    N = 8000
    all_rows = [_raw_trade(i, JAN1 + i * 60) for i in range(N)]   # ascending
    by_ts_desc = sorted(all_rows, key=lambda r: -r["timestamp"])

    def fetch(url):
        import urllib.parse as up
        p = up.urlparse(url)
        qs = up.parse_qs(p.query)
        off = int(qs.get("offset", ["0"])[0])
        lim = int(qs.get("limit", ["500"])[0])
        if off > 3000:
            raise __import__("pm_research.data.backfill", fromlist=["ApiError"]
                             ).ApiError(400, url, '{"error":"max historical activity offset of 3000 exceeded"}')
        if p.path.startswith("/activity"):
            s = int(qs["start"][0]); e = int(qs["end"][0])
            win = [r for r in by_ts_desc if s <= r["timestamp"] < e]
            return win[off:off + lim]
        if p.path.startswith("/trades"):
            return by_ts_desc[off:off + lim]
        return []

    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=fetch, rate_limit_sleep=0.0)
        n = bf.backfill_wallet("0xw1", date(2025, 1, 1), date(2025, 12, 31))
        assert n == N                                # nothing lost to the cap
        assert len(store.load_trades(["0xw1"])) == N


def test_deep_walk_zero_progress_guard_terminates():
    """Pathological: every activity row shares one timestamp. Must terminate."""
    rows = [_raw_trade(i, JAN1) for i in range(600)]
    def fetch(url):
        import urllib.parse as up
        p = up.urlparse(url)
        qs = up.parse_qs(p.query)
        if p.path.startswith("/activity"):
            s = int(qs["start"][0]); e = int(qs["end"][0])
            if not (s <= JAN1 < e):
                return []
            off = int(qs.get("offset", ["0"])[0])
            return rows[off:off + int(qs.get("limit", ["500"])[0])]
        return []
    with tempfile.TemporaryDirectory() as d:
        bf = Backfiller(Store(d), fetcher=fetch, rate_limit_sleep=0.0)
        df = bf.fetch_wallet_trades_deep("0xw1", date(2024, 12, 1), date(2025, 2, 1))
        assert len(df) == 600                        # finished, no infinite loop


def test_deep_walk_aborts_early_when_over_bot_threshold():
    """A true HFT bot (way more fills than --skip-bots-over) must NOT be
    fully walked just to be discarded afterwards. The walk should stop as
    soon as the running total crosses `abort_over`, leaving most of the
    wallet's history un-fetched (saves memory, time, and API calls on a
    1GB box)."""
    N = 8000
    all_rows = [_raw_trade(i, JAN1 + i * 60) for i in range(N)]   # ascending
    by_ts_desc = sorted(all_rows, key=lambda r: -r["timestamp"])
    calls = {"activity": 0}

    def fetch(url):
        import urllib.parse as up
        p = up.urlparse(url)
        qs = up.parse_qs(p.query)
        off = int(qs.get("offset", ["0"])[0])
        lim = int(qs.get("limit", ["500"])[0])
        if off > 3000:
            from pm_research.data.backfill import ApiError
            raise ApiError(400, url, '{"error":"max historical activity offset of 3000 exceeded"}')
        if p.path.startswith("/activity"):
            calls["activity"] += 1
            s = int(qs["start"][0]); e = int(qs["end"][0])
            win = [r for r in by_ts_desc if s <= r["timestamp"] < e]
            return win[off:off + lim]
        return []

    with tempfile.TemporaryDirectory() as d:
        bf = Backfiller(Store(d), fetcher=fetch, rate_limit_sleep=0.0)
        df = bf.fetch_wallet_trades_deep("0xbot", date(2025, 1, 1), date(2025, 12, 31),
                                         abort_over=1000)
        # one window already exceeds the threshold (3500 rows, offset-capped)
        # -> walk must stop there, NOT recover all 8000
        assert len(df) < N
        assert len(df) >= 1000
        # confirm it didn't even attempt a second window's worth of pages
        # beyond the one that crossed the threshold
        assert calls["activity"] <= 7  # one window's pagination (3000/500 + 1)


def test_backfill_wallet_skips_bot_without_full_deep_walk():
    """End-to-end via backfill_wallet: a wallet over --skip-bots-over is
    marked a bot (0 trades saved) WITHOUT the deep walk recovering its
    entire history first."""
    N = 8000
    all_rows = [_raw_trade(i, JAN1 + i * 60) for i in range(N)]
    by_ts_desc = sorted(all_rows, key=lambda r: -r["timestamp"])

    def fetch(url):
        import urllib.parse as up
        p = up.urlparse(url)
        qs = up.parse_qs(p.query)
        off = int(qs.get("offset", ["0"])[0])
        lim = int(qs.get("limit", ["500"])[0])
        if off > 3000:
            from pm_research.data.backfill import ApiError
            raise ApiError(400, url, '{"error":"max historical activity offset of 3000 exceeded"}')
        if p.path.startswith("/activity"):
            s = int(qs["start"][0]); e = int(qs["end"][0])
            win = [r for r in by_ts_desc if s <= r["timestamp"] < e]
            return win[off:off + lim]
        if p.path.startswith("/trades"):
            return by_ts_desc[off:off + lim]
        return []

    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=fetch, rate_limit_sleep=0.0,
                       max_wallet_trades=1000)
        n = bf.backfill_wallet("0xbot", date(2025, 1, 1), date(2025, 12, 31))
        assert n == 0                                 # skipped as bot
        assert len(store.load_trades(["0xbot"])) == 0


def test_backfill_full_resume_skips_markets_with_existing_prices():
    """The price phase has no per-market coverage record beyond "the file
    exists" -> resume=True must skip markets already on disk (no re-fetch
    of /trades?market=, no recomputation), and must NOT skip them when
    resume=False (a plain re-run still refreshes everything)."""
    calls = {"market_trades": 0}

    def trades_route(qs):
        if "market" in qs:
            calls["market_trades"] += 1
        return [_raw_trade(0, JAN1, price=0.40),
                _raw_trade(1, JAN1 + 3600, outcome="No", price=0.55)]

    def gamma_route(qs):
        return [_raw_market(closed=True, winner_idx=0)]

    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        bf = Backfiller(store, fetcher=_fake_api({"/trades": trades_route,
                                                  "/markets": gamma_route}),
                        rate_limit_sleep=0.0)
        start, end = date(2025, 1, 1), date(2025, 12, 31)

        rep1 = bf.backfill_full(["0xw1"], start, end)
        assert rep1["condition_ids"] == 1
        assert rep1["price_markets_resumed"] == 0
        calls_after_first = calls["market_trades"]
        assert calls_after_first > 0

        # resume=True: the one market's prices already exist -> skip it
        rep2 = bf.backfill_full(["0xw1"], start, end, resume=True)
        assert rep2["price_markets_resumed"] == 1
        assert calls["market_trades"] == calls_after_first   # no new calls

        # resume=False: re-fetches and recomputes as normal
        rep3 = bf.backfill_full(["0xw1"], start, end, resume=False)
        assert rep3["price_markets_resumed"] == 0
        assert calls["market_trades"] > calls_after_first


# ---- save_wallet_trades merge precedence (fresh rows win on collision) --------

def _trade_row(trade_id, *, tx_hash, token_id, outcome_index,
               traded_at=JAN1, wallet="0xw1", outcome="YES"):
    """One TRADES-shaped row as a dict (all canonical columns present)."""
    return {"trade_id": trade_id, "wallet": wallet, "condition_id": CID,
            "outcome": outcome, "side": "BUY", "price": 0.42, "size_usdc": 42.0,
            "traded_at": pd.Timestamp(traded_at, unit="s", tz="UTC"),
            "tx_hash": tx_hash, "token_id": token_id,
            "outcome_index": outcome_index}


def test_save_wallet_trades_fresh_row_wins_on_trade_id_collision():
    # old stored row: same trade_id, MISSING join keys (NA) — simulates a frame
    # written before the schema-enrichment patches.
    # new fetched row: same trade_id, POPULATED keys.
    # after save, the stored row must carry the populated values.
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        old = pd.DataFrame([_trade_row("tid1", tx_hash=None, token_id="",
                                       outcome_index=None)])
        store.save_wallet_trades("0xw1", old, date(2025, 1, 1), date(2025, 3, 31))

        new = pd.DataFrame([_trade_row("tid1", tx_hash="0xfresh",
                                       token_id="tok123", outcome_index=0)])
        store.save_wallet_trades("0xw1", new, date(2025, 1, 1), date(2025, 3, 31))

        out = store.load_trades(["0xw1"])
        assert len(out) == 1                              # still one row (deduped)
        row = out.iloc[0]
        assert row["tx_hash"] == "0xfresh"                # fresh value won
        assert row["token_id"] == "tok123"
        assert row["outcome_index"] == 0
        assert row["trade_id"] == "tid1"                  # identity preserved


def test_save_wallet_trades_preserves_unrelated_existing_trades():
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        old = pd.DataFrame([
            _trade_row("keepme", tx_hash="0xold", token_id="tokOLD",
                       outcome_index=1, traded_at=JAN1),
            _trade_row("tid1", tx_hash=None, token_id="", outcome_index=None,
                       traded_at=JAN1 + DAY),
        ])
        store.save_wallet_trades("0xw1", old, date(2025, 1, 1), date(2025, 3, 31))
        # re-fetch only tid1 with populated keys
        new = pd.DataFrame([_trade_row("tid1", tx_hash="0xfresh",
                                       token_id="tok123", outcome_index=0,
                                       traded_at=JAN1 + DAY)])
        store.save_wallet_trades("0xw1", new, date(2025, 1, 1), date(2025, 3, 31))

        out = store.load_trades(["0xw1"]).set_index("trade_id")
        assert len(out) == 2                              # unrelated row kept
        assert out.loc["keepme"]["tx_hash"] == "0xold"    # untouched
        assert out.loc["tid1"]["tx_hash"] == "0xfresh"    # updated


def test_save_wallet_trades_dedupes_duplicate_new_rows_by_trade_id():
    with tempfile.TemporaryDirectory() as d:
        store = Store(d)
        # two new rows with the SAME trade_id in one save call -> dedupe to one
        dup = pd.DataFrame([
            _trade_row("tidX", tx_hash="0xa", token_id="tokA", outcome_index=0),
            _trade_row("tidX", tx_hash="0xb", token_id="tokB", outcome_index=1),
        ])
        store.save_wallet_trades("0xw1", dup, date(2025, 1, 1), date(2025, 3, 31))
        out = store.load_trades(["0xw1"])
        assert len(out) == 1                              # deduped by trade_id
        # keep="last" -> the second of the duplicate pair wins
        assert out.iloc[0]["tx_hash"] == "0xb"
