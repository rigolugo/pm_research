"""
Pure validation + request-plan builder for the Polymarket Price Canary Actor.

This module contains NO network calls and NO Apify SDK import, so it can be
unit-tested in isolation, without a live Apify runtime and without network
access. It only builds a *plan* of URLs that a future, separately
authorized live-run mode could call. It never requests any of them.

Guardrails encoded here (see SPEC_apify_polymarket_price_canary.md,
project_context in rigolugo/pm_research):

- Hard condition cap: <= 5, enforced regardless of what `max_conditions`
  claims.
- Required per-condition fields: condition_id, nb_subclass, decision_ts,
  side_0_token_id, side_1_token_id.
- Token ids must be string-safe decimal strings; scientific notation and
  any non-digit character is rejected outright.
- Only three fixed, known-safe endpoint families are ever addressed here:
  Gamma metadata, CLOB GET /prices-history (single-market form only), and
  CLOB current-shape endpoints (/book, /price, /midpoint, /spread). No
  user-supplied path/endpoint is ever used verbatim, so wallet/profile/
  leaderboard/comments/positions/activity endpoints are structurally
  unreachable from this module.
- POST /batch-prices-history is intentionally NOT implemented. Per
  Orchestrator correction: current Polymarket docs clearly confirm
  GET /prices-history?market=TOKEN_ID&startTs=...&endTs=..., but do not
  clearly document /batch-prices-history. Only the single-market form is
  planned.
- No yes_price / 1-price / 1-yes_price / side synthesis, no price
  computation, no canonical_side_price, no scoring: none of those concepts
  appear anywhere in this module's data model.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode

HARD_MAX_CONDITIONS = 5
VALID_SUBCLASSES = {"UP_DOWN", "OVER_UNDER", "NAMED_OTHER"}
MIN_TOKEN_ID_LEN = 1
MAX_TOKEN_ID_LEN = 100

DEFAULT_GAMMA_BASE_URL = "https://gamma-api.polymarket.com"
DEFAULT_CLOB_BASE_URL = "https://clob.polymarket.com"

DISCLAIMER = "APIFY_CANARY_NOT_COVERAGE_EVIDENCE"


class CanaryValidationError(Exception):
    """Raised for manifest-level (not per-condition) validation failures.

    These are failures that make it unsafe or meaningless to build any
    plan at all for the whole run: a missing/malformed conditions list,
    exceeding the hard condition cap, or exceeding the global planned-
    request cap. Per-condition failures do NOT raise this; see
    build_request_plan().
    """


def is_string_safe_decimal(value: Any) -> bool:
    """True iff value is a non-scientific-notation decimal digit string.

    Rejects: non-strings, empty strings, anything containing a non-digit
    character (this alone rejects scientific notation, since 'e'/'E'/'.'/
    '+'/'-' are all non-digits), and anything outside a sane length band.
    """
    if not isinstance(value, str):
        return False
    if not value:
        return False
    if not value.isdigit():
        return False
    if not (MIN_TOKEN_ID_LEN <= len(value) <= MAX_TOKEN_ID_LEN):
        return False
    return True


def is_iso8601_utc(value: Any) -> bool:
    """True iff value is a timezone-aware ISO 8601 timestamp string."""
    if not isinstance(value, str) or not value:
        return False
    candidate = value.replace("Z", "+00:00")
    try:
        parsed = _dt.datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_condition(cond: Any) -> list[str]:
    """Return a list of human-readable error strings; [] means valid."""
    errors: list[str] = []
    if not isinstance(cond, dict):
        return ["condition is not a JSON object"]

    condition_id = cond.get("condition_id")
    if not isinstance(condition_id, str) or not condition_id:
        errors.append("condition_id missing or not a non-empty string")

    nb_subclass = cond.get("nb_subclass")
    if nb_subclass not in VALID_SUBCLASSES:
        errors.append(
            f"nb_subclass must be one of {sorted(VALID_SUBCLASSES)}, got {nb_subclass!r}"
        )

    decision_ts = cond.get("decision_ts")
    if not is_iso8601_utc(decision_ts):
        errors.append(
            "decision_ts missing or not a timezone-aware ISO8601 string "
            f"(got {decision_ts!r})"
        )

    for field_name in ("side_0_token_id", "side_1_token_id"):
        token_id = cond.get(field_name)
        if not is_string_safe_decimal(token_id):
            errors.append(
                f"{field_name} missing or not a string-safe decimal id "
                f"(digits only, no scientific notation): got {token_id!r}"
            )

    slug = cond.get("slug")
    if slug is not None and not isinstance(slug, str):
        errors.append("slug, if present, must be a string")

    return errors


@dataclass
class RequestPlanRow:
    """One planned (never-executed) request, or one validation-error row."""

    condition_id: str | None
    nb_subclass: str | None
    side: int | None
    token_id: str | None
    source: str
    planned_url: str | None
    dry_run: bool = True
    disclaimer: str = DISCLAIMER
    classification: str | None = None
    errors: list[str] = field(default_factory=list)


def _prices_history_url(base_url: str, token_id: str, start_ts: int, end_ts: int, fidelity: str) -> str:
    # GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...
    # This is the ONLY CLOB price-history shape this module builds.
    # /batch-prices-history is intentionally not implemented (see module docstring).
    params = {"market": token_id, "startTs": start_ts, "endTs": end_ts, "fidelity": fidelity}
    return f"{base_url}/prices-history?{urlencode(params)}"


def _gamma_url(base_url: str, slug: str, lookup_type: str) -> str:
    params = {"slug": slug}
    return f"{base_url}/{lookup_type}?{urlencode(params)}"


def _book_shape_url(base_url: str, path: str, token_id: str) -> str:
    params = {"token_id": token_id}
    return f"{base_url}/{path}?{urlencode(params)}"


def build_request_plan(raw_input: dict) -> tuple[list[RequestPlanRow], list[RequestPlanRow]]:
    """
    Validate raw_input and build the planned (never-executed) request rows.

    Returns (plan_rows, error_rows):
      - plan_rows: one row per planned request, for conditions that passed
        per-condition validation.
      - error_rows: one row per condition that FAILED per-condition
        validation (classification=APIFY_INPUT_SCHEMA_INVALID); that
        condition is simply excluded from plan_rows, the run continues for
        the remaining valid conditions.

    Raises CanaryValidationError for manifest-level failures that make it
    unsafe/meaningless to plan the whole run at all:
      - input.conditions missing, not a list, or empty.
      - len(conditions) exceeds the effective cap (min(max_conditions, 5)).
      - the resulting plan would exceed global_request_cap.

    No network call is made anywhere in this function.
    """
    if not isinstance(raw_input, dict):
        raise CanaryValidationError("input is not a JSON object")

    conditions = raw_input.get("conditions")
    if not isinstance(conditions, list) or not conditions:
        raise CanaryValidationError("input.conditions must be a non-empty array")

    max_conditions = raw_input.get("max_conditions", HARD_MAX_CONDITIONS)
    if not isinstance(max_conditions, int) or max_conditions < 1:
        max_conditions = HARD_MAX_CONDITIONS
    effective_cap = min(max_conditions, HARD_MAX_CONDITIONS)

    if len(conditions) > effective_cap:
        raise CanaryValidationError(
            "APIFY_GUARDRAIL_CONDITION_CAP_EXCEEDED: "
            f"{len(conditions)} conditions supplied, hard cap is {HARD_MAX_CONDITIONS} "
            f"(effective cap this run: {effective_cap})"
        )

    fetch_gamma_metadata = bool(raw_input.get("fetch_gamma_metadata", True))
    fetch_clob_book_shape = bool(raw_input.get("fetch_clob_book_shape", True))

    price_history_window_seconds = raw_input.get("price_history_window_seconds", 3600)
    if not isinstance(price_history_window_seconds, int) or price_history_window_seconds <= 0:
        price_history_window_seconds = 3600

    fidelity = raw_input.get("fidelity", "1")
    if not isinstance(fidelity, str) or not fidelity:
        fidelity = "1"

    gamma_lookup_type = raw_input.get("gamma_lookup_type", "markets")
    if gamma_lookup_type not in ("markets", "events"):
        gamma_lookup_type = "markets"

    gamma_base_url = raw_input.get("gamma_base_url", DEFAULT_GAMMA_BASE_URL)
    if not isinstance(gamma_base_url, str) or not gamma_base_url:
        gamma_base_url = DEFAULT_GAMMA_BASE_URL

    clob_base_url = raw_input.get("clob_base_url", DEFAULT_CLOB_BASE_URL)
    if not isinstance(clob_base_url, str) or not clob_base_url:
        clob_base_url = DEFAULT_CLOB_BASE_URL

    plan_rows: list[RequestPlanRow] = []
    error_rows: list[RequestPlanRow] = []

    for cond in conditions:
        errs = validate_condition(cond)
        condition_id = cond.get("condition_id") if isinstance(cond, dict) else None
        nb_subclass = cond.get("nb_subclass") if isinstance(cond, dict) else None

        if errs:
            error_rows.append(
                RequestPlanRow(
                    condition_id=condition_id,
                    nb_subclass=nb_subclass,
                    side=None,
                    token_id=None,
                    source="validation",
                    planned_url=None,
                    classification="APIFY_INPUT_SCHEMA_INVALID",
                    errors=errs,
                )
            )
            continue

        decision_ts = cond["decision_ts"]
        parsed_ts = _dt.datetime.fromisoformat(decision_ts.replace("Z", "+00:00"))
        start_ts = int(parsed_ts.timestamp()) - price_history_window_seconds
        end_ts = int(parsed_ts.timestamp()) + price_history_window_seconds

        slug = cond.get("slug")
        if fetch_gamma_metadata and slug:
            plan_rows.append(
                RequestPlanRow(
                    condition_id=condition_id,
                    nb_subclass=nb_subclass,
                    side=None,
                    token_id=None,
                    source="gamma_metadata",
                    planned_url=_gamma_url(gamma_base_url, slug, gamma_lookup_type),
                )
            )

        for side, token_field in ((0, "side_0_token_id"), (1, "side_1_token_id")):
            token_id = cond[token_field]
            plan_rows.append(
                RequestPlanRow(
                    condition_id=condition_id,
                    nb_subclass=nb_subclass,
                    side=side,
                    token_id=token_id,
                    source="clob_prices_history",
                    planned_url=_prices_history_url(
                        clob_base_url, token_id, start_ts, end_ts, fidelity
                    ),
                )
            )

        if fetch_clob_book_shape:
            for side, token_field in ((0, "side_0_token_id"), (1, "side_1_token_id")):
                token_id = cond[token_field]
                for source, path in (
                    ("clob_book", "book"),
                    ("clob_price", "price"),
                    ("clob_midpoint", "midpoint"),
                    ("clob_spread", "spread"),
                ):
                    plan_rows.append(
                        RequestPlanRow(
                            condition_id=condition_id,
                            nb_subclass=nb_subclass,
                            side=side,
                            token_id=token_id,
                            source=source,
                            planned_url=_book_shape_url(clob_base_url, path, token_id),
                        )
                    )

    global_request_cap = raw_input.get("global_request_cap", 50)
    if not isinstance(global_request_cap, int) or global_request_cap < 1:
        global_request_cap = 50

    if len(plan_rows) > global_request_cap:
        raise CanaryValidationError(
            "APIFY_GLOBAL_REQUEST_CAP_EXCEEDED: "
            f"planned {len(plan_rows)} requests, cap is {global_request_cap}"
        )

    return plan_rows, error_rows
