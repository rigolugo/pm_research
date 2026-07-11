"""
Live price-source canary logic for the Polymarket Price Canary Actor.

Implements SPEC_apify_live_price_source_canary.md (accepted, branch
apify-price-canary-dry-run). THIS MODULE IS NOT EXECUTED AGAINST LIVE
NETWORK IN THIS DELIVERY. Per the current authorization ("AUTHORIZE
IMPLEMENTATION PACKAGE REVIEW ONLY"):
  - no Apify run
  - no build/deploy
  - no network call
  - no live dataset produced

Structural safety, not just a flag:
  - HttpFetcher.fetch() (the only code path that touches the network) is
    instantiated in exactly one place in this whole codebase:
    run_live_canary_from_actor_input(), in this file.
  - run_live_canary_from_actor_input() calls check_live_acknowledgements()
    FIRST, before touching conditions, before building any request plan,
    before HttpFetcher is ever constructed. Missing/false acknowledgements
    raise LiveCanaryValidationError there, before HttpFetcher exists at all.
  - main.py only calls run_live_canary_from_actor_input() when
    raw_input.get("dry_run", True) is the literal Python value False (a
    JSON boolean `false`, not a truthy default, not a string). Any other
    value takes the pre-existing, unchanged dry-run path in main.py, which
    has no dependency on this module at all.
  - Every function in this module that builds a request plan
    (build_live_request_plan) or checks it (check_request_cap) is pure
    computation -- no I/O, callable and tested with zero network access.
  - The actual per-request work (run_live_canary) takes a `fetcher` object
    as an explicit parameter. Tests always pass a fake/mock fetcher; only
    run_live_canary_from_actor_input ever passes a real HttpFetcher.

Guardrails encoded here (see the spec for full rationale):
  - Exactly 3 conditions, one per subclass (UP_DOWN, OVER_UNDER,
    NAMED_OTHER), read verbatim from Actor input -- never hardcoded, never
    re-selected.
  - Mandatory fetch: CLOB GET /prices-history, single-market form only
    (POST /batch-prices-history is never used).
  - Optional, bounded current-endpoint schema comparison (/book only, one
    side per condition) -- current-state data, never historical, never
    contributes to a parsed_side_candidate_row.
  - No Gamma.
  - Hard global request cap <= 12, enforced as pure computation before any
    fetch.
  - No yes_price / 1-price / 1-yes_price / side synthesis, no
    canonical_side_price, no scoring. None of these concepts appear
    anywhere in this module's data model.
  - Every output row carries disclaimer_label =
    "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE". P1/P2/P3/probe/gate terms
    (including named_binary_probe_blocked) appear only in that disclaimer
    string and in comments/docstrings -- never read, modified, computed,
    or used as operational state anywhere in this module.
"""

from __future__ import annotations

import datetime as _dt
import json
import uuid
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode

from .validation import DEFAULT_CLOB_BASE_URL, is_iso8601_utc, is_string_safe_decimal

HARD_REQUEST_CAP = 12
REQUIRED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
DISCLAIMER_LABEL = "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE"
POINT_SELECTION_METHOD = "nearest_ts_prefer_earlier_on_tie"
RAW_EXCERPT_MAX_BYTES = 500

# Defensive top-level JSON keys that, if present in a /prices-history
# response and equal to a string, are treated as a possible echoed token
# identity. The documented shape does not require or promise this field;
# its absence is normal, not an error (see token_identity_basis rules).
RESPONSE_BODY_ID_KEYS = ("market", "token_id", "asset_id")


class LiveCanaryValidationError(Exception):
    """Raised for any preflight hard-stop. Every raise site in this module
    that can be reached before HttpFetcher is constructed guarantees zero
    network calls occurred for this run."""


# ---------------------------------------------------------------------------
# Preflight: acknowledgements (checked FIRST, before anything else)
# ---------------------------------------------------------------------------

def check_live_acknowledgements(raw_input: dict) -> None:
    """Hard-stop unless BOTH acknowledgements are explicitly the literal
    value `True` (a JSON boolean `true`, not a truthy string or 1).
    Nothing about conditions, request plans, or fetchers is touched before
    this check runs and passes."""
    if raw_input.get("live_canary_enabled") is not True:
        raise LiveCanaryValidationError(
            "live_canary_enabled must be explicitly true to run the live "
            "canary; missing or false -> hard-stop before any request"
        )
    if raw_input.get("acknowledge_not_p1_evidence") is not True:
        raise LiveCanaryValidationError(
            "acknowledge_not_p1_evidence must be explicitly true to run "
            "the live canary; missing or false -> hard-stop before any request"
        )


# ---------------------------------------------------------------------------
# Preflight: strict whole-manifest condition validation (no per-condition
# tolerance -- unlike the dry-run planner in validation.py, ANY problem
# here aborts the WHOLE run, per SPEC §5.1)
# ---------------------------------------------------------------------------

def validate_live_canary_conditions(conditions: Any) -> list[dict]:
    """Return the validated conditions list unchanged on success. Raise
    LiveCanaryValidationError, aborting the whole run before any request,
    on any problem."""
    if not isinstance(conditions, list):
        raise LiveCanaryValidationError("input.conditions must be a list")
    if len(conditions) != 3:
        raise LiveCanaryValidationError(
            f"exactly 3 conditions are required for the live canary, got {len(conditions)}"
        )

    seen_subclasses: list[str] = []
    seen_token_ids: set[str] = set()

    for cond in conditions:
        if not isinstance(cond, dict):
            raise LiveCanaryValidationError("each condition must be a JSON object")

        for required_field in (
            "condition_id", "nb_subclass", "decision_ts",
            "side_0_token_id", "side_1_token_id",
        ):
            if required_field not in cond or cond[required_field] in (None, ""):
                raise LiveCanaryValidationError(
                    f"condition missing required field: {required_field}"
                )

        condition_id = cond["condition_id"]
        nb_subclass = cond["nb_subclass"]
        if nb_subclass not in REQUIRED_SUBCLASSES:
            raise LiveCanaryValidationError(
                f"condition {condition_id}: nb_subclass must be one of "
                f"{REQUIRED_SUBCLASSES}, got {nb_subclass!r}"
            )
        seen_subclasses.append(nb_subclass)

        if not is_iso8601_utc(cond["decision_ts"]):
            raise LiveCanaryValidationError(
                f"condition {condition_id}: decision_ts is not a "
                f"timezone-aware ISO8601 string (got {cond['decision_ts']!r})"
            )

        side_0 = cond["side_0_token_id"]
        side_1 = cond["side_1_token_id"]
        if not is_string_safe_decimal(side_0):
            raise LiveCanaryValidationError(
                f"condition {condition_id}: side_0_token_id is not a "
                f"string-safe decimal id (got {side_0!r})"
            )
        if not is_string_safe_decimal(side_1):
            raise LiveCanaryValidationError(
                f"condition {condition_id}: side_1_token_id is not a "
                f"string-safe decimal id (got {side_1!r})"
            )
        if side_0 == side_1:
            raise LiveCanaryValidationError(
                f"condition {condition_id}: side_0_token_id == side_1_token_id "
                "(malformed -- both sides cannot share one token)"
            )
        for token_id in (side_0, side_1):
            if token_id in seen_token_ids:
                raise LiveCanaryValidationError(
                    f"duplicate token_id across manifest: {token_id!r} "
                    "(malformed -- each side token must be unique across the whole manifest)"
                )
            seen_token_ids.add(token_id)

    if sorted(seen_subclasses) != sorted(REQUIRED_SUBCLASSES):
        raise LiveCanaryValidationError(
            f"must have exactly one condition each of {sorted(REQUIRED_SUBCLASSES)}, "
            f"got {seen_subclasses}"
        )

    return conditions


# ---------------------------------------------------------------------------
# Request plan construction (pure computation, no I/O)
# ---------------------------------------------------------------------------

@dataclass
class PlannedLiveRequest:
    condition_id: str
    nb_subclass: str
    decision_ts: str
    side: int
    endpoint: str  # "clob_prices_history" | "clob_book"
    request_token_id: str
    request_url_market_param: str
    request_url_actual: str
    window_start_ts: int | None = None
    window_end_ts: int | None = None
    fidelity: str | None = None


def _prices_history_url(base_url: str, token_id: str, start_ts: int, end_ts: int, fidelity: str) -> str:
    # GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...
    # Single-market form only. POST /batch-prices-history is never built here.
    params = {"market": token_id, "startTs": start_ts, "endTs": end_ts, "fidelity": fidelity}
    return f"{base_url}/prices-history?{urlencode(params)}"


def _book_url(base_url: str, token_id: str) -> str:
    params = {"token_id": token_id}
    return f"{base_url}/book?{urlencode(params)}"


def build_live_request_plan(
    conditions: list[dict],
    include_current_endpoint_check: bool = False,
    clob_base_url: str = DEFAULT_CLOB_BASE_URL,
    price_history_window_seconds: int = 3600,
    fidelity: str = "1",
) -> list[PlannedLiveRequest]:
    """Build the planned request list. Pure computation -- no network call.
    Mandatory: 2 requests/condition (clob_prices_history) = 6 for 3
    conditions. Optional (+3, one per condition, side_0 only, /book) if
    include_current_endpoint_check is True -- 9 total. Never exceeds 12 by
    construction for exactly 3 conditions; check_request_cap is still
    called by run_live_canary as a defensive, explicit gate."""
    plan: list[PlannedLiveRequest] = []

    for cond in conditions:
        decision_ts = cond["decision_ts"]
        parsed_ts = _dt.datetime.fromisoformat(decision_ts.replace("Z", "+00:00"))
        start_ts = int(parsed_ts.timestamp()) - price_history_window_seconds
        end_ts = int(parsed_ts.timestamp()) + price_history_window_seconds

        for side, token_field in ((0, "side_0_token_id"), (1, "side_1_token_id")):
            token_id = cond[token_field]
            plan.append(
                PlannedLiveRequest(
                    condition_id=cond["condition_id"],
                    nb_subclass=cond["nb_subclass"],
                    decision_ts=decision_ts,
                    side=side,
                    endpoint="clob_prices_history",
                    request_token_id=token_id,
                    request_url_market_param=token_id,
                    request_url_actual=_prices_history_url(
                        clob_base_url, token_id, start_ts, end_ts, fidelity
                    ),
                    window_start_ts=start_ts,
                    window_end_ts=end_ts,
                    fidelity=fidelity,
                )
            )

    if include_current_endpoint_check:
        for cond in conditions:
            token_id = cond["side_0_token_id"]
            plan.append(
                PlannedLiveRequest(
                    condition_id=cond["condition_id"],
                    nb_subclass=cond["nb_subclass"],
                    decision_ts=cond["decision_ts"],
                    side=0,
                    endpoint="clob_book",
                    request_token_id=token_id,
                    request_url_market_param=token_id,
                    request_url_actual=_book_url(clob_base_url, token_id),
                )
            )

    return plan


def check_request_cap(plan: list[PlannedLiveRequest], cap: int = HARD_REQUEST_CAP) -> None:
    """Hard-stop, before any request, if the plan exceeds the cap. Pure
    computation -- this runs after the plan is built but before any
    fetcher call is made anywhere in the pipeline."""
    if len(plan) > cap:
        raise LiveCanaryValidationError(
            f"request plan has {len(plan)} requests, which exceeds the hard "
            f"cap of {cap}; refusing to start (zero requests made)"
        )


# ---------------------------------------------------------------------------
# HTTP fetch abstraction
# ---------------------------------------------------------------------------

@dataclass
class FetchResult:
    http_status: int | None
    body_bytes: bytes | None
    error: str | None  # non-None only for connection/timeout-level failures


class HttpFetcher:
    """The ONLY code path in this codebase that can make a real network
    call. Instantiated in exactly one place: run_live_canary_from_actor_input.
    Never instantiated anywhere in this delivery's tests, and never invoked
    during implementation/verification of this package -- see the handoff's
    self-attestation."""

    def __init__(self, timeout_s: int = 15):
        self.timeout_s = timeout_s

    def fetch(self, url: str) -> FetchResult:  # pragma: no cover (never exercised in this delivery)
        import urllib.error
        import urllib.request

        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                return FetchResult(http_status=resp.status, body_bytes=resp.read(), error=None)
        except urllib.error.HTTPError as exc:
            try:
                body = exc.read()
            except Exception:  # noqa: BLE001
                body = None
            return FetchResult(http_status=exc.code, body_bytes=body, error=None)
        except Exception as exc:  # noqa: BLE001 - any connection/timeout/DNS/etc failure
            return FetchResult(http_status=None, body_bytes=None, error=str(exc))


# ---------------------------------------------------------------------------
# Response parsing (pure computation given a FetchResult -- no I/O)
# ---------------------------------------------------------------------------

def _try_parse_json(body_bytes: bytes | None) -> tuple[Any, bool]:
    if body_bytes is None:
        return None, False
    try:
        return json.loads(body_bytes.decode("utf-8")), True
    except Exception:  # noqa: BLE001
        return None, False


def _extract_response_body_token_id(parsed_json: Any) -> str | None:
    if not isinstance(parsed_json, dict):
        return None
    for key in RESPONSE_BODY_ID_KEYS:
        val = parsed_json.get(key)
        if isinstance(val, str) and val:
            return val
    return None


def _extract_valid_points(history_list: list) -> list[tuple[int, float]]:
    """Return [(ts:int, price:float), ...] for items whose t/p both parse
    and whose price is in [0, 1]. Malformed items are skipped, not raised
    on individually -- a request is only PARSE_BLOCKED if NO valid points
    remain after this filtering."""
    points: list[tuple[int, float]] = []
    for item in history_list:
        if not isinstance(item, dict):
            continue
        try:
            t_val = int(item.get("t"))
        except (TypeError, ValueError):
            continue
        try:
            p_val = float(item.get("p"))
        except (TypeError, ValueError):
            continue
        if not (0.0 <= p_val <= 1.0):
            continue
        points.append((t_val, p_val))
    return points


def select_nearest_point(points: list[tuple[int, float]], decision_ts_unix: int) -> tuple[int, float] | None:
    """Select the point nearest decision_ts_unix (minimizing absolute time
    difference). Ties are broken by preferring the EARLIER timestamp,
    regardless of input order. Diagnostic selection only -- see
    POINT_SELECTION_METHOD and the spec's §4."""
    if not points:
        return None
    best: tuple[int, float] | None = None
    best_gap: int | None = None
    for ts, price in points:
        gap = abs(ts - decision_ts_unix)
        if best is None or gap < best_gap or (gap == best_gap and ts < best[0]):
            best = (ts, price)
            best_gap = gap
    return best


def classify_and_parse_prices_history(
    fetch_result: FetchResult,
    request_token_id: str,
    request_url_market_param: str,
    decision_ts_iso: str,
) -> dict:
    """Derive request_classification, side_status, token identity fields,
    and (if usable) the candidate point, from a single /prices-history
    FetchResult. Pure function -- no I/O."""
    result: dict = {
        "request_classification": None,
        "side_status": None,
        "response_body_token_id": None,
        "token_identity_basis": "REQUEST_URL",
        "raw_point_count": 0,
        "candidate_price": None,
        "candidate_source_ts_iso": None,
        "signed_gap_seconds": None,
        "schema_matches_documented": False,
        "price_in_range_0_1": False,
        "timestamp_parseable": False,
    }

    if fetch_result.error is not None or fetch_result.http_status is None or fetch_result.http_status >= 400:
        result["request_classification"] = "APIFY_LIVE_CANARY_ENDPOINT_ERROR"
        result["side_status"] = "ERROR"
        return result

    parsed_json, is_valid_json = _try_parse_json(fetch_result.body_bytes)
    if not is_valid_json:
        # Per spec §7.1: a response that isn't valid JSON at all -> ENDPOINT_ERROR.
        result["request_classification"] = "APIFY_LIVE_CANARY_ENDPOINT_ERROR"
        result["side_status"] = "ERROR"
        return result

    response_body_token_id = _extract_response_body_token_id(parsed_json)
    result["response_body_token_id"] = response_body_token_id
    if response_body_token_id is not None:
        if response_body_token_id == request_token_id:
            result["token_identity_basis"] = "RESPONSE_BODY"
        else:
            # Present but conflicts with the requested token -> genuinely ambiguous.
            result["token_identity_basis"] = "UNCONFIRMED"
    if request_url_market_param != request_token_id:
        # Defensive: should be structurally impossible given how the plan is
        # built, but if it ever happened, identity cannot be trusted.
        result["token_identity_basis"] = "UNCONFIRMED"

    if not isinstance(parsed_json, dict) or not isinstance(parsed_json.get("history"), list):
        result["request_classification"] = "APIFY_LIVE_CANARY_PARSE_BLOCKED"
        result["side_status"] = "PARSE_BLOCKED"
        return result

    result["schema_matches_documented"] = True
    history = parsed_json["history"]
    result["raw_point_count"] = len(history)

    if len(history) == 0:
        result["request_classification"] = "APIFY_LIVE_CANARY_EMPTY_HISTORY"
        result["side_status"] = "EMPTY"
        return result

    valid_points = _extract_valid_points(history)
    if not valid_points:
        result["request_classification"] = "APIFY_LIVE_CANARY_PARSE_BLOCKED"
        result["side_status"] = "PARSE_BLOCKED"
        return result

    decision_ts_unix = int(_dt.datetime.fromisoformat(decision_ts_iso.replace("Z", "+00:00")).timestamp())
    nearest = select_nearest_point(valid_points, decision_ts_unix)
    candidate_ts, candidate_price = nearest  # type: ignore[misc]

    result["timestamp_parseable"] = True
    result["price_in_range_0_1"] = True
    result["candidate_price"] = candidate_price
    result["candidate_source_ts_iso"] = (
        _dt.datetime.fromtimestamp(candidate_ts, tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    result["signed_gap_seconds"] = candidate_ts - decision_ts_unix
    result["request_classification"] = "APIFY_LIVE_CANARY_USABLE_SHAPE"
    result["side_status"] = (
        "UNCONFIRMED_TOKEN_ID" if result["token_identity_basis"] == "UNCONFIRMED" else "PRESENT"
    )
    return result


def classify_current_endpoint(fetch_result: FetchResult) -> dict:
    """Classification for the optional current-endpoint schema-comparison
    call. Never contributes a parsed_side_candidate_row."""
    if fetch_result.error is not None or fetch_result.http_status is None or fetch_result.http_status >= 400:
        return {
            "request_classification": "APIFY_LIVE_CANARY_ENDPOINT_ERROR",
            "raw_point_count": 0,
            "response_body_token_id": None,
            "token_identity_basis": "REQUEST_URL",
        }

    parsed_json, is_valid_json = _try_parse_json(fetch_result.body_bytes)
    if not is_valid_json:
        return {
            "request_classification": "APIFY_LIVE_CANARY_ENDPOINT_ERROR",
            "raw_point_count": 0,
            "response_body_token_id": None,
            "token_identity_basis": "REQUEST_URL",
        }

    raw_point_count = 0
    if isinstance(parsed_json, dict):
        for key in ("bids", "asks"):
            val = parsed_json.get(key)
            if isinstance(val, list):
                raw_point_count += len(val)

    return {
        "request_classification": "APIFY_LIVE_CANARY_CURRENT_ONLY_NOT_HISTORICAL",
        "raw_point_count": raw_point_count,
        "response_body_token_id": _extract_response_body_token_id(parsed_json),
        "token_identity_basis": "REQUEST_URL",
    }


def _bounded_excerpt(body_bytes: bytes | None, max_bytes: int = RAW_EXCERPT_MAX_BYTES) -> str | None:
    if body_bytes is None:
        return None
    try:
        text = body_bytes.decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return None
    return text[:max_bytes]


# ---------------------------------------------------------------------------
# Row builders (pure, no I/O)
# ---------------------------------------------------------------------------

def _raw_request_summary_row(
    run_id: str, generated_at: str, planned: PlannedLiveRequest,
    fetch_result: FetchResult, derived: dict,
) -> dict:
    return {
        "row_type": "raw_request_summary_row",
        "run_id": run_id,
        "request_id": str(uuid.uuid4()),
        "condition_id": planned.condition_id,
        "nb_subclass": planned.nb_subclass,
        "side": planned.side,
        "endpoint": planned.endpoint,
        "request_token_id": planned.request_token_id,
        "request_url_market_param": planned.request_url_market_param,
        "request_url_actual": planned.request_url_actual,
        "window_start_ts": planned.window_start_ts,
        "window_end_ts": planned.window_end_ts,
        "fidelity": planned.fidelity,
        "http_status": fetch_result.http_status,
        "response_byte_length": len(fetch_result.body_bytes) if fetch_result.body_bytes else 0,
        "raw_point_count": derived.get("raw_point_count", 0),
        "raw_response_excerpt": _bounded_excerpt(fetch_result.body_bytes),
        "response_body_token_id": derived.get("response_body_token_id"),
        "token_identity_basis": derived.get("token_identity_basis", "REQUEST_URL"),
        "fetched_at": generated_at,
        "request_classification": derived["request_classification"],
        "disclaimer_label": DISCLAIMER_LABEL,
    }


def _parsed_side_candidate_row(run_id: str, planned: PlannedLiveRequest, derived: dict) -> dict:
    return {
        "row_type": "parsed_side_candidate_row",
        "run_id": run_id,
        "condition_id": planned.condition_id,
        "nb_subclass": planned.nb_subclass,
        "side": planned.side,
        "token_id": planned.request_token_id,
        "decision_ts": planned.decision_ts,
        "candidate_price": derived["candidate_price"],
        "candidate_source_ts": derived["candidate_source_ts_iso"],
        "signed_gap_seconds": derived["signed_gap_seconds"],
        "point_selection_method": POINT_SELECTION_METHOD,
        "side_status": derived["side_status"],
        "schema_matches_documented": derived["schema_matches_documented"],
        "price_in_range_0_1": derived["price_in_range_0_1"],
        "timestamp_parseable": derived["timestamp_parseable"],
        "is_synthesized": False,
        "disclaimer_label": DISCLAIMER_LABEL,
    }


def _condition_pair_summary_rows(
    conditions: list[dict],
    side_status_map: dict[tuple[str, int], str],
    candidate_map: dict[tuple[str, int], tuple[float, str]],
    run_id: str,
    generated_at: str,
) -> list[dict]:
    rows = []
    for cond in conditions:
        cid = cond["condition_id"]
        s0_status = side_status_map.get((cid, 0), "ERROR")
        s1_status = side_status_map.get((cid, 1), "ERROR")
        s0_price, s0_ts = candidate_map.get((cid, 0), (None, None))
        s1_price, s1_ts = candidate_map.get((cid, 1), (None, None))

        present_count = sum(1 for s in (s0_status, s1_status) if s == "PRESENT")
        if present_count == 2:
            pair_status = "BOTH_SIDES_PRESENT"
        elif present_count == 1:
            pair_status = "ONE_SIDED_ONLY"
        else:
            pair_status = "BOTH_SIDES_MISSING_OR_BLOCKED"

        rows.append({
            "row_type": "condition_pair_summary_row",
            "run_id": run_id,
            "condition_id": cid,
            "nb_subclass": cond["nb_subclass"],
            "side_0_token_id": cond["side_0_token_id"],
            "side_1_token_id": cond["side_1_token_id"],
            "side_0_price_candidate": s0_price,
            "side_1_price_candidate": s1_price,
            "side_0_source_ts": s0_ts,
            "side_1_source_ts": s1_ts,
            "side_0_status": s0_status,
            "side_1_status": s1_status,
            "condition_pair_status": pair_status,
            "disclaimer_label": DISCLAIMER_LABEL,
            "generated_at": generated_at,
        })
    return rows


# ---------------------------------------------------------------------------
# Orchestration (testable with any fetcher; production only ever gets a real
# HttpFetcher via run_live_canary_from_actor_input, never directly)
# ---------------------------------------------------------------------------

def run_live_canary(
    conditions: list[dict],
    fetcher: Any,
    include_current_endpoint_check: bool = False,
    request_cap: int = HARD_REQUEST_CAP,
    clob_base_url: str = DEFAULT_CLOB_BASE_URL,
    price_history_window_seconds: int = 3600,
    fidelity: str = "1",
    run_id: str | None = None,
) -> list[dict]:
    """Build the plan, enforce the cap (zero fetches if it fails), then run
    every planned request through `fetcher.fetch(url)`, and return the full
    list of output rows (raw_request_summary_row + parsed_side_candidate_row
    + condition_pair_summary_row). `conditions` must already have passed
    validate_live_canary_conditions -- this function does not re-validate
    manifest shape, only builds/executes/classifies the plan."""
    plan = build_live_request_plan(
        conditions, include_current_endpoint_check, clob_base_url,
        price_history_window_seconds, fidelity,
    )
    check_request_cap(plan, request_cap)  # raises before ANY fetch call

    if run_id is None:
        run_id = str(uuid.uuid4())
    generated_at = _dt.datetime.now(_dt.timezone.utc).isoformat()

    raw_rows: list[dict] = []
    candidate_rows: list[dict] = []
    side_status_map: dict[tuple[str, int], str] = {}
    candidate_map: dict[tuple[str, int], tuple[float, str]] = {}

    for planned in plan:
        fetch_result = fetcher.fetch(planned.request_url_actual)

        if planned.endpoint == "clob_prices_history":
            derived = classify_and_parse_prices_history(
                fetch_result, planned.request_token_id,
                planned.request_url_market_param, planned.decision_ts,
            )
            raw_rows.append(_raw_request_summary_row(run_id, generated_at, planned, fetch_result, derived))
            side_status_map[(planned.condition_id, planned.side)] = derived["side_status"]
            if derived["side_status"] in ("PRESENT", "UNCONFIRMED_TOKEN_ID"):
                candidate_rows.append(_parsed_side_candidate_row(run_id, planned, derived))
                candidate_map[(planned.condition_id, planned.side)] = (
                    derived["candidate_price"], derived["candidate_source_ts_iso"],
                )
        else:  # clob_book -- current-endpoint schema comparison only
            derived = classify_current_endpoint(fetch_result)
            raw_rows.append(_raw_request_summary_row(run_id, generated_at, planned, fetch_result, derived))

    pair_rows = _condition_pair_summary_rows(conditions, side_status_map, candidate_map, run_id, generated_at)

    return raw_rows + candidate_rows + pair_rows


def run_live_canary_from_actor_input(raw_input: dict) -> list[dict]:
    """The ONLY function in this codebase that constructs a real
    HttpFetcher. Called from main.py only when raw_input.get("dry_run",
    True) is the literal value False. Checks acknowledgements FIRST -- if
    either is missing, LiveCanaryValidationError is raised before anything
    else in this function runs, including before `conditions` is even read
    from raw_input."""
    check_live_acknowledgements(raw_input)

    conditions = validate_live_canary_conditions(raw_input.get("conditions"))

    include_current = raw_input.get("live_include_current_endpoint_check", False) is True
    clob_base_url = raw_input.get("clob_base_url", DEFAULT_CLOB_BASE_URL)
    if not isinstance(clob_base_url, str) or not clob_base_url:
        clob_base_url = DEFAULT_CLOB_BASE_URL

    price_history_window_seconds = raw_input.get("price_history_window_seconds", 3600)
    if not isinstance(price_history_window_seconds, int) or price_history_window_seconds <= 0:
        price_history_window_seconds = 3600

    fidelity = raw_input.get("fidelity", "1")
    if not isinstance(fidelity, str) or not fidelity:
        fidelity = "1"

    fetcher = HttpFetcher()  # the only construction site in the whole codebase
    return run_live_canary(
        conditions, fetcher,
        include_current_endpoint_check=include_current,
        request_cap=HARD_REQUEST_CAP,
        clob_base_url=clob_base_url,
        price_history_window_seconds=price_history_window_seconds,
        fidelity=fidelity,
    )
