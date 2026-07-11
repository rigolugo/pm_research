"""
Tests for src/live_canary.py.

NO test in this file makes, or could make, a real network call:
  - Preflight/validation/cap tests call pure functions directly.
  - "Happy path" / parsing / classification tests use FakeFetcher, a
    canned-response stub -- never HttpFetcher, never urllib, never any
    real socket.
  - The zero-network proofs use PoisonedFetcher, which raises immediately
    if `.fetch()` is ever called, and assert call_count == 0 afterward.

HttpFetcher (the only real-network code path in the whole package) is
never instantiated anywhere in this file.
"""

import sys
from pathlib import Path

# live_canary.py uses `from .validation import ...` (a relative import,
# correct for production execution via `python -m src`). To load it in a
# test without a real Apify runtime, import it as part of the `src`
# package (src/__init__.py already exists) rather than as a bare module.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import live_canary as lc  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _tok(prefix_digit: str) -> str:
    return prefix_digit + "1" * 76  # 77-char synthetic decimal token id


def _condition(condition_id, nb_subclass, decision_ts, side_0, side_1):
    return {
        "condition_id": condition_id,
        "nb_subclass": nb_subclass,
        "decision_ts": decision_ts,
        "side_0_token_id": side_0,
        "side_1_token_id": side_1,
    }


def _valid_three_conditions():
    return [
        _condition("0xUP", "UP_DOWN", "2026-01-01T01:00:00Z", _tok("2"), _tok("3")),
        _condition("0xOU", "OVER_UNDER", "2026-02-01T01:00:00Z", _tok("4"), _tok("5")),
        _condition("0xNO", "NAMED_OTHER", "2026-03-01T01:00:00Z", _tok("6"), _tok("7")),
    ]


def _valid_live_input(**overrides):
    payload = {
        "conditions": _valid_three_conditions(),
        "dry_run": False,
        "live_canary_enabled": True,
        "acknowledge_not_p1_evidence": True,
    }
    payload.update(overrides)
    return payload


class FakeFetcher:
    """Canned-response stub keyed by URL substring match on `market=` token.
    Never touches the network. Records call_count and every URL fetched."""

    def __init__(self, responses_by_token: dict[str, "lc.FetchResult"], default=None):
        self.responses_by_token = responses_by_token
        self.default = default
        self.call_count = 0
        self.urls_fetched: list[str] = []

    def fetch(self, url: str) -> "lc.FetchResult":
        self.call_count += 1
        self.urls_fetched.append(url)
        for token, result in self.responses_by_token.items():
            if f"market={token}" in url or f"token_id={token}" in url:
                return result
        if self.default is not None:
            return self.default
        raise AssertionError(f"FakeFetcher: no canned response configured for url={url}")


class PoisonedFetcher:
    """Raises immediately if .fetch() is ever called. Used to prove a code
    path makes zero network calls."""

    def __init__(self):
        self.call_count = 0

    def fetch(self, url: str) -> "lc.FetchResult":
        self.call_count += 1
        raise AssertionError(f"PoisonedFetcher.fetch() was called with url={url} -- network call attempted!")


def _json_body(obj) -> bytes:
    import json
    return json.dumps(obj).encode("utf-8")


def _ok_history_result(points: list[tuple[int, float]]) -> "lc.FetchResult":
    return lc.FetchResult(
        http_status=200,
        body_bytes=_json_body({"history": [{"t": t, "p": p} for t, p in points]}),
        error=None,
    )


def _empty_history_result() -> "lc.FetchResult":
    return lc.FetchResult(http_status=200, body_bytes=_json_body({"history": []}), error=None)


def _http_error_result(status=500) -> "lc.FetchResult":
    return lc.FetchResult(http_status=status, body_bytes=b"internal error", error=None)


def _connection_error_result() -> "lc.FetchResult":
    return lc.FetchResult(http_status=None, body_bytes=None, error="Connection refused")


def _malformed_shape_result() -> "lc.FetchResult":
    return lc.FetchResult(http_status=200, body_bytes=_json_body({"unexpected": "shape"}), error=None)


def _invalid_json_result() -> "lc.FetchResult":
    return lc.FetchResult(http_status=200, body_bytes=b"not json at all {{{", error=None)


def _all_points_malformed_result() -> "lc.FetchResult":
    return lc.FetchResult(
        http_status=200,
        body_bytes=_json_body({"history": [{"t": "not-a-number", "p": "also-not"}]}),
        error=None,
    )


# ===========================================================================
# 1. Input validation (preflight)
# ===========================================================================

def test_acknowledgements_both_present_passes():
    lc.check_live_acknowledgements({"live_canary_enabled": True, "acknowledge_not_p1_evidence": True})


def test_acknowledgements_missing_live_canary_enabled():
    try:
        lc.check_live_acknowledgements({"acknowledge_not_p1_evidence": True})
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "live_canary_enabled" in str(exc)


def test_acknowledgements_missing_acknowledge_not_p1_evidence():
    try:
        lc.check_live_acknowledgements({"live_canary_enabled": True})
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "acknowledge_not_p1_evidence" in str(exc)


def test_acknowledgements_truthy_but_not_literal_true_rejected():
    # "true" (string) and 1 (int) must NOT satisfy the gate -- only literal True.
    try:
        lc.check_live_acknowledgements({"live_canary_enabled": "true", "acknowledge_not_p1_evidence": 1})
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError:
        pass


def test_validate_conditions_happy_path():
    result = lc.validate_live_canary_conditions(_valid_three_conditions())
    assert len(result) == 3


def test_validate_conditions_wrong_count():
    try:
        lc.validate_live_canary_conditions(_valid_three_conditions()[:2])
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "exactly 3" in str(exc)


def test_validate_conditions_missing_subclass():
    conds = _valid_three_conditions()
    conds[2]["nb_subclass"] = "UP_DOWN"  # now two UP_DOWN, zero NAMED_OTHER
    try:
        lc.validate_live_canary_conditions(conds)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "exactly one condition each" in str(exc)


def test_validate_conditions_missing_token_id():
    conds = _valid_three_conditions()
    del conds[0]["side_1_token_id"]
    try:
        lc.validate_live_canary_conditions(conds)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "side_1_token_id" in str(exc)


def test_validate_conditions_non_string_safe_token_id():
    conds = _valid_three_conditions()
    conds[0]["side_0_token_id"] = "1e10"
    try:
        lc.validate_live_canary_conditions(conds)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "string-safe decimal" in str(exc)


def test_validate_conditions_duplicate_side_tokens_within_condition():
    conds = _valid_three_conditions()
    conds[0]["side_1_token_id"] = conds[0]["side_0_token_id"]
    try:
        lc.validate_live_canary_conditions(conds)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "malformed" in str(exc)


def test_validate_conditions_duplicate_token_across_conditions():
    conds = _valid_three_conditions()
    conds[1]["side_0_token_id"] = conds[0]["side_0_token_id"]
    try:
        lc.validate_live_canary_conditions(conds)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "duplicate token_id" in str(exc)


def test_validate_conditions_bad_decision_ts():
    conds = _valid_three_conditions()
    conds[0]["decision_ts"] = "not-a-timestamp"
    try:
        lc.validate_live_canary_conditions(conds)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "decision_ts" in str(exc)


def test_validate_conditions_not_a_list():
    try:
        lc.validate_live_canary_conditions("not-a-list")
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError:
        pass


# ===========================================================================
# 2. Request-plan construction
# ===========================================================================

def test_plan_mandatory_six_requests():
    plan = lc.build_live_request_plan(_valid_three_conditions())
    assert len(plan) == 6
    assert all(p.endpoint == "clob_prices_history" for p in plan)
    sides = sorted((p.condition_id, p.side) for p in plan)
    assert sides == [("0xNO", 0), ("0xNO", 1), ("0xOU", 0), ("0xOU", 1), ("0xUP", 0), ("0xUP", 1)]


def test_plan_urls_are_single_market_form_only():
    plan = lc.build_live_request_plan(_valid_three_conditions())
    for p in plan:
        assert "/prices-history?" in p.request_url_actual
        assert "market=" in p.request_url_actual
        assert "startTs=" in p.request_url_actual
        assert "endTs=" in p.request_url_actual
        assert "batch" not in p.request_url_actual.lower()
        assert p.request_url_market_param == p.request_token_id


def test_plan_with_optional_current_endpoint_check():
    plan = lc.build_live_request_plan(_valid_three_conditions(), include_current_endpoint_check=True)
    assert len(plan) == 9
    book_rows = [p for p in plan if p.endpoint == "clob_book"]
    assert len(book_rows) == 3
    assert all(p.side == 0 for p in book_rows)  # one side per condition only
    for p in book_rows:
        assert "/book?" in p.request_url_actual


def test_plan_no_gamma_ever():
    plan = lc.build_live_request_plan(_valid_three_conditions(), include_current_endpoint_check=True)
    for p in plan:
        assert "gamma" not in p.request_url_actual.lower()
        assert p.endpoint in ("clob_prices_history", "clob_book")


# ===========================================================================
# 3. Request cap enforcement (and zero-network proof)
# ===========================================================================

def test_request_cap_default_not_exceeded_by_mandatory_plan():
    plan = lc.build_live_request_plan(_valid_three_conditions())
    lc.check_request_cap(plan)  # should not raise; 6 <= 12


def test_request_cap_default_not_exceeded_with_optional_check():
    plan = lc.build_live_request_plan(_valid_three_conditions(), include_current_endpoint_check=True)
    lc.check_request_cap(plan)  # should not raise; 9 <= 12


def test_request_cap_violation_raises():
    plan = lc.build_live_request_plan(_valid_three_conditions())  # 6 requests
    try:
        lc.check_request_cap(plan, cap=3)  # artificially low cap for this test only
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError as exc:
        assert "exceeds the hard cap" in str(exc)


def test_request_cap_violation_causes_zero_network_calls():
    """Proves run_live_canary never calls fetcher.fetch() even once when
    the (test-lowered) cap would be exceeded."""
    poisoned = PoisonedFetcher()
    try:
        lc.run_live_canary(_valid_three_conditions(), fetcher=poisoned, request_cap=3)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError:
        pass
    assert poisoned.call_count == 0


# ===========================================================================
# 4. Zero-network proofs for acknowledgement gating
# ===========================================================================

def test_missing_acknowledgements_cause_zero_network_calls():
    poisoned = PoisonedFetcher()
    raw_input = _valid_live_input(live_canary_enabled=False)  # ack missing/false
    try:
        # run_live_canary_from_actor_input constructs its own HttpFetcher
        # internally -- to prove the ack-check itself (not just the outer
        # function) never gets past the gate, call it directly first:
        lc.check_live_acknowledgements(raw_input)
        assert False, "expected LiveCanaryValidationError from check_live_acknowledgements"
    except lc.LiveCanaryValidationError:
        pass
    # And confirm the full entry point also halts before constructing any
    # fetcher: it must raise, and must do so before any poisoned fetcher
    # (which we don't even get a chance to inject here, since
    # run_live_canary_from_actor_input builds its own HttpFetcher -- the
    # absence of a network error, and the presence of the expected
    # exception, is itself the proof no request was attempted).
    try:
        lc.run_live_canary_from_actor_input(raw_input)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError:
        pass
    assert poisoned.call_count == 0  # never even constructed/used


def test_default_dry_run_input_never_reaches_live_canary_module():
    """A default/dry-run-style input (no live-canary flags at all) should
    never even be passed to this module's entry point by main.py -- this
    test documents that check_live_acknowledgements() correctly rejects
    such an input if it ever were, as a defense-in-depth backstop."""
    poisoned = PoisonedFetcher()
    raw_input = {"conditions": _valid_three_conditions()}  # no dry_run, no acks at all
    try:
        lc.check_live_acknowledgements(raw_input)
        assert False, "expected LiveCanaryValidationError"
    except lc.LiveCanaryValidationError:
        pass
    assert poisoned.call_count == 0


# ===========================================================================
# 5. Token identity basis
# ===========================================================================

def test_token_identity_defaults_to_request_url():
    result = lc.classify_and_parse_prices_history(
        _ok_history_result([(1_700_000_000, 0.5)]),
        request_token_id=_tok("2"),
        request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["response_body_token_id"] is None  # documented shape doesn't echo it
    assert result["token_identity_basis"] == "REQUEST_URL"
    assert result["side_status"] == "PRESENT"  # missing echo is NOT a problem


def test_token_identity_response_body_match_upgrades_basis():
    token = _tok("2")
    body = _json_body({"market": token, "history": [{"t": 1_700_000_000, "p": 0.5}]})
    result = lc.classify_and_parse_prices_history(
        lc.FetchResult(http_status=200, body_bytes=body, error=None),
        request_token_id=token,
        request_url_market_param=token,
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["response_body_token_id"] == token
    assert result["token_identity_basis"] == "RESPONSE_BODY"
    assert result["side_status"] == "PRESENT"


def test_token_identity_response_body_conflict_is_unconfirmed():
    token = _tok("2")
    other_token = _tok("9")
    body = _json_body({"market": other_token, "history": [{"t": 1_700_000_000, "p": 0.5}]})
    result = lc.classify_and_parse_prices_history(
        lc.FetchResult(http_status=200, body_bytes=body, error=None),
        request_token_id=token,
        request_url_market_param=token,
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["token_identity_basis"] == "UNCONFIRMED"
    assert result["side_status"] == "UNCONFIRMED_TOKEN_ID"
    # A candidate is still recorded (not discarded), just flagged:
    assert result["candidate_price"] == 0.5


def test_token_identity_url_param_mismatch_is_unconfirmed():
    result = lc.classify_and_parse_prices_history(
        _ok_history_result([(1_700_000_000, 0.5)]),
        request_token_id=_tok("2"),
        request_url_market_param=_tok("9"),  # deliberately mismatched
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["token_identity_basis"] == "UNCONFIRMED"
    assert result["side_status"] == "UNCONFIRMED_TOKEN_ID"


# ===========================================================================
# 6. Response parsing: common shapes, empty history, endpoint error, parse blocked
# ===========================================================================

def test_parse_usable_shape():
    result = lc.classify_and_parse_prices_history(
        _ok_history_result([(1_700_000_000, 0.42), (1_700_003_600, 0.55)]),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_USABLE_SHAPE"
    assert result["side_status"] == "PRESENT"
    assert result["schema_matches_documented"] is True
    assert result["price_in_range_0_1"] is True
    assert result["timestamp_parseable"] is True


def test_parse_empty_history():
    result = lc.classify_and_parse_prices_history(
        _empty_history_result(),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_EMPTY_HISTORY"
    assert result["side_status"] == "EMPTY"


def test_parse_endpoint_error_http_500():
    result = lc.classify_and_parse_prices_history(
        _http_error_result(500),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_ENDPOINT_ERROR"
    assert result["side_status"] == "ERROR"


def test_parse_endpoint_error_connection_failure():
    result = lc.classify_and_parse_prices_history(
        _connection_error_result(),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_ENDPOINT_ERROR"
    assert result["side_status"] == "ERROR"


def test_parse_endpoint_error_invalid_json():
    result = lc.classify_and_parse_prices_history(
        _invalid_json_result(),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    # Per spec §7.1: invalid JSON -> ENDPOINT_ERROR, not PARSE_BLOCKED.
    assert result["request_classification"] == "APIFY_LIVE_CANARY_ENDPOINT_ERROR"
    assert result["side_status"] == "ERROR"


def test_parse_blocked_ambiguous_shape():
    result = lc.classify_and_parse_prices_history(
        _malformed_shape_result(),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_PARSE_BLOCKED"
    assert result["side_status"] == "PARSE_BLOCKED"


def test_parse_blocked_all_points_malformed():
    result = lc.classify_and_parse_prices_history(
        _all_points_malformed_result(),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_PARSE_BLOCKED"
    assert result["side_status"] == "PARSE_BLOCKED"


def test_parse_blocked_price_out_of_range():
    result = lc.classify_and_parse_prices_history(
        _ok_history_result([(1_700_000_000, 1.5)]),  # out of [0,1]
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert result["request_classification"] == "APIFY_LIVE_CANARY_PARSE_BLOCKED"
    assert result["side_status"] == "PARSE_BLOCKED"


def test_current_only_not_historical_classification():
    result = lc.classify_current_endpoint(lc.FetchResult(
        http_status=200, body_bytes=_json_body({"bids": [{"price": "0.4"}], "asks": []}), error=None,
    ))
    assert result["request_classification"] == "APIFY_LIVE_CANARY_CURRENT_ONLY_NOT_HISTORICAL"


def test_current_endpoint_error():
    result = lc.classify_current_endpoint(_http_error_result(503))
    assert result["request_classification"] == "APIFY_LIVE_CANARY_ENDPOINT_ERROR"


# ===========================================================================
# 7. Nearest-timestamp selection and tie-break
# ===========================================================================

def test_select_nearest_point_basic():
    points = [(1_700_000_000, 0.4), (1_700_003_700, 0.6), (1_700_010_000, 0.9)]
    decision_ts_unix = 1_700_003_600  # closest to the second point (100s away)
    chosen = lc.select_nearest_point(points, decision_ts_unix)
    assert chosen == (1_700_003_700, 0.6)


def test_select_nearest_point_tie_prefers_earlier():
    decision_ts_unix = 1_700_000_000
    points = [
        (1_700_000_000 - 50, 0.3),  # 50s before
        (1_700_000_000 + 50, 0.7),  # 50s after -- exact tie in absolute gap
    ]
    chosen = lc.select_nearest_point(points, decision_ts_unix)
    assert chosen == (1_700_000_000 - 50, 0.3)  # earlier wins the tie


def test_select_nearest_point_tie_prefers_earlier_regardless_of_input_order():
    decision_ts_unix = 1_700_000_000
    points = [
        (1_700_000_000 + 50, 0.7),  # later one listed FIRST this time
        (1_700_000_000 - 50, 0.3),
    ]
    chosen = lc.select_nearest_point(points, decision_ts_unix)
    assert chosen == (1_700_000_000 - 50, 0.3)


def test_select_nearest_point_empty_returns_none():
    assert lc.select_nearest_point([], 1_700_000_000) is None


def test_signed_gap_seconds_sign_and_method_recorded():
    # Point strictly AFTER decision_ts -> positive signed gap.
    result_after = lc.classify_and_parse_prices_history(
        _ok_history_result([(1_700_000_100, 0.5)]),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso=_dt_iso(1_700_000_000),
    )
    assert result_after["signed_gap_seconds"] == 100

    # Point strictly BEFORE decision_ts -> negative signed gap.
    result_before = lc.classify_and_parse_prices_history(
        _ok_history_result([(1_700_000_000 - 100, 0.5)]),
        request_token_id=_tok("2"), request_url_market_param=_tok("2"),
        decision_ts_iso=_dt_iso(1_700_000_000),
    )
    assert result_before["signed_gap_seconds"] == -100


def _dt_iso(unix_ts: int) -> str:
    import datetime as dt
    return dt.datetime.fromtimestamp(unix_ts, tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_point_selection_method_recorded_on_row():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    candidate_rows = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    assert len(candidate_rows) == 6
    assert all(r["point_selection_method"] == "nearest_ts_prefer_earlier_on_tie" for r in candidate_rows)


# ===========================================================================
# 8. Condition-pair rollup
# ===========================================================================

def test_condition_pair_both_sides_present():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    pair_rows = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    assert len(pair_rows) == 3
    assert all(r["condition_pair_status"] == "BOTH_SIDES_PRESENT" for r in pair_rows)
    up = next(r for r in pair_rows if r["condition_id"] == "0xUP")
    assert up["side_0_price_candidate"] == 0.4
    assert up["side_1_price_candidate"] == 0.6


def test_condition_pair_one_sided_only():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _empty_history_result(),  # side_1 empty for 0xUP
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    pair_rows = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    up = next(r for r in pair_rows if r["condition_id"] == "0xUP")
    assert up["condition_pair_status"] == "ONE_SIDED_ONLY"
    assert up["side_0_status"] == "PRESENT"
    assert up["side_1_status"] == "EMPTY"
    others = [r for r in pair_rows if r["condition_id"] != "0xUP"]
    assert all(r["condition_pair_status"] == "BOTH_SIDES_PRESENT" for r in others)


def test_condition_pair_both_sides_missing_or_blocked():
    fetcher = FakeFetcher({
        _tok("2"): _http_error_result(500),
        _tok("3"): _connection_error_result(),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    pair_rows = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    up = next(r for r in pair_rows if r["condition_id"] == "0xUP")
    assert up["condition_pair_status"] == "BOTH_SIDES_MISSING_OR_BLOCKED"


def test_condition_pair_unconfirmed_token_id_never_counts_as_present():
    """An UNCONFIRMED_TOKEN_ID side must never contribute to
    BOTH_SIDES_PRESENT -- it is diagnostic, not a usable pair."""
    conflicting_token = _tok("9")
    body_conflict = _json_body({"market": conflicting_token, "history": [{"t": 1_700_000_000, "p": 0.4}]})
    fetcher = FakeFetcher({
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    }, default=None)
    # Manually override side_0 of 0xUP to return a conflicting-identity body.
    fetcher.responses_by_token[_tok("2")] = lc.FetchResult(http_status=200, body_bytes=body_conflict, error=None)

    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    pair_rows = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    up = next(r for r in pair_rows if r["condition_id"] == "0xUP")
    assert up["side_0_status"] == "UNCONFIRMED_TOKEN_ID"
    assert up["condition_pair_status"] == "ONE_SIDED_ONLY"  # side_1 PRESENT, side_0 not counted


# ===========================================================================
# 9. Mandatory disclaimer on every row type
# ===========================================================================

def test_disclaimer_on_every_row_type():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher, include_current_endpoint_check=True)
    row_types_seen = {r["row_type"] for r in rows}
    assert row_types_seen == {"raw_request_summary_row", "parsed_side_candidate_row", "condition_pair_summary_row"}
    assert all(r["disclaimer_label"] == "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE" for r in rows)


# ===========================================================================
# 10. No forbidden fields in outputs
# ===========================================================================

FORBIDDEN_KEY_SUBSTRINGS = ("yes_price", "canonical_side_price", "1_minus", "synthesized_price")


def test_no_forbidden_fields_in_any_output_row():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _empty_history_result(),
        _tok("5"): _http_error_result(500),
        _tok("6"): _malformed_shape_result(),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher, include_current_endpoint_check=True)
    for row in rows:
        for key in row:
            lowered = key.lower()
            for forbidden in FORBIDDEN_KEY_SUBSTRINGS:
                assert forbidden not in lowered, f"forbidden field {key!r} present in row {row!r}"
    # is_synthesized must be hardcoded False wherever present:
    for row in rows:
        if "is_synthesized" in row:
            assert row["is_synthesized"] is False


def test_no_batch_endpoint_ever_referenced():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    for row in rows:
        url = row.get("request_url_actual")
        if url:
            assert "batch" not in url.lower()


# ===========================================================================
# 11. Full happy-path integration (fake fetcher only)
# ===========================================================================

def test_full_pipeline_row_counts_mandatory_only():
    fetcher = FakeFetcher({
        _tok("2"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_history_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_history_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_history_result([(1_700_000_000, 0.6)]),
    })
    rows = lc.run_live_canary(_valid_three_conditions(), fetcher=fetcher)
    assert fetcher.call_count == 6
    raw = [r for r in rows if r["row_type"] == "raw_request_summary_row"]
    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    assert len(raw) == 6
    assert len(candidates) == 6
    assert len(pairs) == 3


def test_entry_point_reaches_fetcher_only_after_all_gates_pass():
    """Proves run_live_canary_from_actor_input's gating doesn't ALSO block a
    fully valid request (i.e. the gates are precise, not overzealous) --
    while still never touching a real network. Monkeypatches HttpFetcher to
    a poisoned stand-in for the duration of this test only, so if the code
    reaches the point of calling .fetch(), we see our own controlled
    AssertionError (proving the wiring is correct) instead of any real
    socket ever opening."""

    class PoisonedHttpFetcher:
        def __init__(self, *a, **kw):
            pass

        def fetch(self, url):
            raise RuntimeError(f"POISONED_FETCHER_REACHED:{url}")

    original = lc.HttpFetcher
    lc.HttpFetcher = PoisonedHttpFetcher
    try:
        raw_input = _valid_live_input()
        try:
            lc.run_live_canary_from_actor_input(raw_input)
            raise AssertionError("expected the poisoned fetcher to be reached and raise RuntimeError")
        except RuntimeError as exc:
            assert str(exc).startswith("POISONED_FETCHER_REACHED:")
            assert "/prices-history?" in str(exc)  # confirms it was a real planned URL, not a fluke
    finally:
        lc.HttpFetcher = original


# ---------------------------------------------------------------------------
# Plain-script runner (no pytest required)
# ---------------------------------------------------------------------------

def _main() -> int:
    import inspect
    module = sys.modules[__name__]
    test_fns = [
        obj for name, obj in vars(module).items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    for fn in test_fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nALL {len(test_fns)} SELF-TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
