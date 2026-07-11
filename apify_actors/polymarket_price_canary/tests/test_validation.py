"""
Pure-logic tests for src/validation.py.

No network access, no Apify SDK dependency. These import validation.py
directly by path so they can run in any bare Python 3.10+ environment
(matching the project's existing style of network-free, apify/pandas-free
test suites for spec-review artifacts).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import validation as v  # noqa: E402


# ---------------------------------------------------------------------------
# is_string_safe_decimal
# ---------------------------------------------------------------------------

def test_accepts_plain_digit_string():
    assert v.is_string_safe_decimal("123456789012345678901234567890") is True


def test_rejects_non_string():
    assert v.is_string_safe_decimal(123456) is False
    assert v.is_string_safe_decimal(None) is False
    assert v.is_string_safe_decimal(1.5) is False


def test_rejects_empty_string():
    assert v.is_string_safe_decimal("") is False


def test_rejects_scientific_notation():
    assert v.is_string_safe_decimal("1e10") is False
    assert v.is_string_safe_decimal("1E10") is False
    assert v.is_string_safe_decimal("1.5e+20") is False


def test_rejects_decimal_point_and_signs():
    assert v.is_string_safe_decimal("123.456") is False
    assert v.is_string_safe_decimal("-123456") is False
    assert v.is_string_safe_decimal("+123456") is False


def test_rejects_too_long():
    assert v.is_string_safe_decimal("1" * 101) is False


def test_accepts_typical_78_digit_token_id():
    token_id = "1" * 78
    assert v.is_string_safe_decimal(token_id) is True


# ---------------------------------------------------------------------------
# is_iso8601_utc
# ---------------------------------------------------------------------------

def test_accepts_z_suffix():
    assert v.is_iso8601_utc("2026-01-01T00:00:00Z") is True


def test_accepts_explicit_offset():
    assert v.is_iso8601_utc("2026-01-01T00:00:00+00:00") is True


def test_rejects_naive_timestamp():
    assert v.is_iso8601_utc("2026-01-01T00:00:00") is False


def test_rejects_garbage_timestamp():
    assert v.is_iso8601_utc("not-a-timestamp") is False
    assert v.is_iso8601_utc(None) is False
    assert v.is_iso8601_utc("") is False


# ---------------------------------------------------------------------------
# validate_condition
# ---------------------------------------------------------------------------

def _valid_condition(**overrides):
    cond = {
        "condition_id": "0xcondition0001",
        "nb_subclass": "UP_DOWN",
        "decision_ts": "2026-01-01T01:00:00Z",
        "side_0_token_id": "1" * 78,
        "side_1_token_id": "2" * 78,
        "slug": "example-slug",
    }
    cond.update(overrides)
    return cond


def test_valid_condition_no_errors():
    errs = v.validate_condition(_valid_condition())
    assert errs == []


def test_missing_condition_id():
    errs = v.validate_condition(_valid_condition(condition_id=""))
    assert any("condition_id" in e for e in errs)


def test_bad_nb_subclass():
    errs = v.validate_condition(_valid_condition(nb_subclass="YES_NO"))
    assert any("nb_subclass" in e for e in errs)


def test_bad_decision_ts():
    errs = v.validate_condition(_valid_condition(decision_ts="garbage"))
    assert any("decision_ts" in e for e in errs)


def test_bad_token_ids():
    errs = v.validate_condition(_valid_condition(side_0_token_id="1e10", side_1_token_id="abc"))
    assert any("side_0_token_id" in e for e in errs)
    assert any("side_1_token_id" in e for e in errs)


def test_slug_optional_but_typed():
    errs = v.validate_condition(_valid_condition(slug=None))
    assert errs == []
    errs2 = v.validate_condition(_valid_condition(slug=123))
    assert any("slug" in e for e in errs2)


def test_non_dict_condition():
    errs = v.validate_condition("not a dict")
    assert errs == ["condition is not a JSON object"]


# ---------------------------------------------------------------------------
# build_request_plan — manifest-level guardrails
# ---------------------------------------------------------------------------

def test_missing_conditions_key_raises():
    try:
        v.build_request_plan({})
        assert False, "expected CanaryValidationError"
    except v.CanaryValidationError as exc:
        assert "conditions" in str(exc)


def test_empty_conditions_list_raises():
    try:
        v.build_request_plan({"conditions": []})
        assert False, "expected CanaryValidationError"
    except v.CanaryValidationError:
        pass


def test_condition_cap_exceeded_raises():
    conditions = [_valid_condition(condition_id=f"0xc{i}") for i in range(6)]
    try:
        v.build_request_plan({"conditions": conditions})
        assert False, "expected CanaryValidationError"
    except v.CanaryValidationError as exc:
        assert "APIFY_GUARDRAIL_CONDITION_CAP_EXCEEDED" in str(exc)


def test_max_conditions_cannot_exceed_hard_cap():
    # Even if max_conditions in input claims a higher cap, hard 5 wins.
    conditions = [_valid_condition(condition_id=f"0xc{i}") for i in range(6)]
    try:
        v.build_request_plan({"conditions": conditions, "max_conditions": 100})
        assert False, "expected CanaryValidationError"
    except v.CanaryValidationError as exc:
        assert "APIFY_GUARDRAIL_CONDITION_CAP_EXCEEDED" in str(exc)


def test_at_cap_five_conditions_does_not_raise_cap_error():
    conditions = [
        _valid_condition(condition_id=f"0xc{i}", nb_subclass="NAMED_OTHER")
        for i in range(5)
    ]
    plan_rows, error_rows = v.build_request_plan(
        {"conditions": conditions, "fetch_gamma_metadata": False, "fetch_clob_book_shape": False}
    )
    assert error_rows == []
    # 2 prices_history rows per condition x 5 conditions
    assert len(plan_rows) == 10


# ---------------------------------------------------------------------------
# build_request_plan — per-condition row counts
# ---------------------------------------------------------------------------

def test_full_plan_row_count_single_condition():
    conditions = [_valid_condition()]
    plan_rows, error_rows = v.build_request_plan({"conditions": conditions})
    assert error_rows == []
    # 1 gamma + 2 prices_history + (2 sides x 4 book-shape endpoints = 8) = 11
    assert len(plan_rows) == 11
    sources = sorted(row.source for row in plan_rows)
    assert sources.count("gamma_metadata") == 1
    assert sources.count("clob_prices_history") == 2
    assert sources.count("clob_book") == 2
    assert sources.count("clob_price") == 2
    assert sources.count("clob_midpoint") == 2
    assert sources.count("clob_spread") == 2


def test_plan_without_gamma_and_book_shape():
    conditions = [_valid_condition()]
    plan_rows, error_rows = v.build_request_plan(
        {"conditions": conditions, "fetch_gamma_metadata": False, "fetch_clob_book_shape": False}
    )
    assert error_rows == []
    assert len(plan_rows) == 2
    assert all(row.source == "clob_prices_history" for row in plan_rows)


def test_no_slug_skips_gamma_even_if_enabled():
    conditions = [_valid_condition(slug=None)]
    plan_rows, error_rows = v.build_request_plan(
        {"conditions": conditions, "fetch_clob_book_shape": False}
    )
    assert error_rows == []
    assert all(row.source != "gamma_metadata" for row in plan_rows)


def test_invalid_condition_becomes_error_row_and_is_excluded():
    good = _valid_condition(condition_id="0xgood")
    bad = _valid_condition(condition_id="0xbad", side_0_token_id="1e10")
    plan_rows, error_rows = v.build_request_plan(
        {"conditions": [good, bad], "fetch_gamma_metadata": False, "fetch_clob_book_shape": False}
    )
    assert len(error_rows) == 1
    assert error_rows[0].condition_id == "0xbad"
    assert error_rows[0].classification == "APIFY_INPUT_SCHEMA_INVALID"
    # only the good condition contributes plan rows
    assert all(row.condition_id == "0xgood" for row in plan_rows)
    assert len(plan_rows) == 2


def test_global_request_cap_exceeded_raises():
    conditions = [
        _valid_condition(condition_id=f"0xc{i}", nb_subclass="OVER_UNDER")
        for i in range(5)
    ]
    # 11 rows/condition x 5 = 55 > default cap 50
    try:
        v.build_request_plan({"conditions": conditions})
        assert False, "expected CanaryValidationError"
    except v.CanaryValidationError as exc:
        assert "APIFY_GLOBAL_REQUEST_CAP_EXCEEDED" in str(exc)


# ---------------------------------------------------------------------------
# build_request_plan — structural safety guarantees
# ---------------------------------------------------------------------------

FORBIDDEN_URL_SUBSTRINGS = [
    "leaderboard",
    "positions",
    "profile",
    "activity",
    "comments",
    "wallet",
    "batch-prices-history",
]


def test_no_forbidden_endpoint_substrings_in_any_planned_url():
    conditions = [_valid_condition()]
    plan_rows, _ = v.build_request_plan({"conditions": conditions})
    for row in plan_rows:
        if row.planned_url is None:
            continue
        lowered = row.planned_url.lower()
        for forbidden in FORBIDDEN_URL_SUBSTRINGS:
            assert forbidden not in lowered, f"forbidden substring {forbidden!r} in {row.planned_url}"


def test_prices_history_url_uses_single_market_form_only():
    conditions = [_valid_condition()]
    plan_rows, _ = v.build_request_plan(
        {"conditions": conditions, "fetch_gamma_metadata": False, "fetch_clob_book_shape": False}
    )
    for row in plan_rows:
        assert row.source == "clob_prices_history"
        assert "/prices-history?" in row.planned_url
        assert "market=" in row.planned_url
        assert "startTs=" in row.planned_url
        assert "endTs=" in row.planned_url


def test_all_rows_carry_dry_run_true_and_disclaimer():
    conditions = [_valid_condition()]
    plan_rows, _ = v.build_request_plan({"conditions": conditions})
    for row in plan_rows:
        assert row.dry_run is True
        assert row.disclaimer == "APIFY_CANARY_NOT_COVERAGE_EVIDENCE"


def test_no_price_fields_anywhere_on_row():
    # Structural guarantee: RequestPlanRow has no field that could carry a
    # computed/synthesized price. This test breaks loudly if anyone adds one.
    field_names = {f for f in v.RequestPlanRow.__dataclass_fields__}
    forbidden_fields = {"price", "yes_price", "side_0_price", "side_1_price", "canonical_side_price"}
    assert field_names.isdisjoint(forbidden_fields)
