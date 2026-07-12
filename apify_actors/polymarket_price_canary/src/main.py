"""
Polymarket Price Canary Actor — entry point.

DRY-RUN BY DEFAULT. Live-canary and transport-isolation-canary capability
exist behind explicit, multi-flag gating (see below) and are NOT executed
as part of this delivery -- no Apify run, no build/deploy, no network
call, no live dataset, no curl invocation. Per
SPEC_apify_live_price_source_canary.md and
SPEC_apify_transport_isolation_canary.md (both accepted, branch
apify-price-canary-dry-run) and the current "implementation package only"
authorization for the transport-isolation route.

Three code paths:

1. DEFAULT / dry_run path (raw_input.get("dry_run", True) is not the
   literal value False): completely unchanged from the prior dry-run-only
   build. Uses src/validation.py only. Makes ZERO network calls -- no
   HTTP client is imported by that path at all. This is the path taken
   whenever `dry_run` is absent, `true`, or anything other than the exact
   JSON boolean `false`.

2. LIVE-CANARY path (dry_run is exactly False, and
   transport_isolation_canary_enabled is not exactly True): dispatches to
   src/live_canary.py's run_live_canary_from_actor_input(), unchanged from
   the prior accepted revision -- see that module for its own gating.

3. TRANSPORT-ISOLATION path (dry_run is exactly False, and
   transport_isolation_canary_enabled is exactly True): dispatches to
   src/transport_isolation_canary.py's
   run_transport_isolation_from_actor_input(), which:
     - checks transport_isolation_canary_enabled == true and
       acknowledge_transport_isolation_not_p1_evidence == true FIRST;
     - re-checks mode ambiguity (defense-in-depth; already checked at the
       dispatch level below);
     - rejects the optional current-endpoint flag and any conflicting
       runtime override (clob_base_url / price_history_window_seconds /
       fidelity) before anything else;
     - reconciles raw_input["conditions"] EXACTLY against the fixed
       identity manifest at
       artifacts/named_binary_probe/apify_price_canary_real_condition_input.json
       -- no normalization, order-sensitive, string-exact;
     - only after all of the above passes does it run a zero-network curl
       provenance preflight (`curl --version`, not a data request), and
       only after THAT passes does it construct a real SubprocessCurlRunner
       and make requests.
   Mode ambiguity (both transport_isolation_canary_enabled=true and
   live_canary_enabled=true) is rejected at the dispatch level in main(),
   before either sub-path's own gating even runs, with zero rows written
   to either path.
   This Actor build does not have the transport-isolation mode invoked
   against a real run, and no curl subprocess is invoked, as part of this
   delivery -- see the implementation handoff's self-attestation.

Standing guardrails enforced across all three paths:
  - No wallet/profile/leaderboard/comments/positions/activity endpoint is
    reachable: only known-safe endpoint families are ever addressed, and
    no user-supplied path is used verbatim.
  - No yes_price / 1-price / 1-yes_price / side synthesis, no price
    computation beyond diagnostic candidate extraction, no
    canonical_side_price, no scoring.
  - P1/P2/P3/probe/gate terms (including named_binary_probe_blocked)
    appear only in guardrail/disclaimer language and are never read,
    modified, computed, or used as operational state anywhere in this
    Actor.
  - Does not claim S1_SOURCE_NOT_VIABLE has changed; every row from any
    path carries its own disclaimer, and the transport-isolation
    disclaimer is never blended with the live-canary disclaimer.
  - /batch-prices-history is intentionally not used anywhere (see
    validation.py, live_canary.py, transport_isolation_canary.py).
"""

from __future__ import annotations

import datetime as _dt
import uuid

from apify import Actor

from .live_canary import LiveCanaryValidationError, run_live_canary_from_actor_input
from .transport_isolation_canary import (
    DISCLAIMER_LABEL as TRANSPORT_DISCLAIMER,
    TransportIsolationValidationError,
    run_transport_isolation_from_actor_input,
)
from .validation import CanaryValidationError, RequestPlanRow, build_request_plan

SCHEMA_VERSION = "apify-canary-plan-1.0"
DISCLAIMER = "APIFY_CANARY_NOT_COVERAGE_EVIDENCE"
LIVE_DISCLAIMER = "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE"
MODE_AMBIGUOUS_MESSAGE = (
    "STOP_APIFY_TRANSPORT_MODE_AMBIGUOUS: transport_isolation_canary_enabled and "
    "live_canary_enabled cannot both be true in the same run"
)


def _row_to_dict(row: RequestPlanRow, run_id: str, generated_at: str) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "condition_id": row.condition_id,
        "nb_subclass": row.nb_subclass,
        "side": row.side,
        "token_id": row.token_id,
        "source": row.source,
        "planned_url": row.planned_url,
        "dry_run": row.dry_run,
        "disclaimer": row.disclaimer,
        "classification": row.classification,
        "errors": row.errors or None,
        "generated_at": generated_at,
    }


async def _run_dry_run_path(raw_input: dict, run_id: str, generated_at: str) -> None:
    """Unchanged from the prior dry-run-only build. Zero network calls."""
    try:
        plan_rows, error_rows = build_request_plan(raw_input)
    except CanaryValidationError as exc:
        Actor.log.error(f"Run halted before any planning: {exc}")
        await Actor.push_data(
            {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "condition_id": None,
                "nb_subclass": None,
                "side": None,
                "token_id": None,
                "source": "manifest_validation",
                "planned_url": None,
                "dry_run": True,
                "disclaimer": DISCLAIMER,
                "classification": str(exc).split(":", 1)[0],
                "errors": [str(exc)],
                "generated_at": generated_at,
            }
        )
        await Actor.fail(status_message=str(exc))
        return

    for row in error_rows:
        await Actor.push_data(_row_to_dict(row, run_id, generated_at))

    for row in plan_rows:
        await Actor.push_data(_row_to_dict(row, run_id, generated_at))

    Actor.log.info(
        f"Dry-run complete. {len(plan_rows)} planned request rows, "
        f"{len(error_rows)} per-condition validation errors emitted. "
        "Zero network calls were made to Polymarket/Gamma/CLOB. "
        f"{DISCLAIMER} — this run does not update S1_SOURCE_NOT_VIABLE "
        "and does not by itself authorize S2/P1/probe/any gate change."
    )


async def _run_live_canary_path(raw_input: dict, run_id: str, generated_at: str) -> None:
    """Gated live-canary path. See src/live_canary.py for the full
    acknowledgement/validation/cap gating -- every hard-stop below is
    raised before any network call in this run."""
    Actor.log.warning(
        "dry_run=false was requested. Checking live-canary gating "
        "acknowledgements and manifest validity before considering any "
        "network call."
    )
    try:
        rows = run_live_canary_from_actor_input(raw_input)
    except LiveCanaryValidationError as exc:
        Actor.log.error(f"Live canary preflight halted before any request: {exc}")
        await Actor.push_data(
            {
                "row_type": "raw_request_summary_row",
                "run_id": run_id,
                "request_id": None,
                "condition_id": None,
                "nb_subclass": None,
                "side": None,
                "endpoint": None,
                "request_token_id": None,
                "request_url_market_param": None,
                "request_url_actual": None,
                "window_start_ts": None,
                "window_end_ts": None,
                "fidelity": None,
                "http_status": None,
                "response_byte_length": 0,
                "raw_point_count": 0,
                "raw_response_excerpt": None,
                "response_body_token_id": None,
                "token_identity_basis": None,
                "fetched_at": generated_at,
                "request_classification": "PREFLIGHT_HARD_STOP",
                "disclaimer_label": LIVE_DISCLAIMER,
                "errors": [str(exc)],
            }
        )
        await Actor.fail(status_message=str(exc))
        return

    for row in rows:
        await Actor.push_data(row)

    Actor.log.info(
        f"Live canary complete. {len(rows)} rows emitted across "
        "raw_request_summary_row / parsed_side_candidate_row / "
        "condition_pair_summary_row. "
        f"{LIVE_DISCLAIMER} — this run does not establish coverage, does "
        "not update S1_SOURCE_NOT_VIABLE, and does not unblock P1."
    )


_KNOWN_TRANSPORT_STOP_PREFIXES = (
    "STOP_APIFY_TRANSPORT_MODE_AMBIGUOUS",
    "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID",
    "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE",
)


def _classify_transport_stop_message(message: str) -> str:
    """Map a validation-exception message to its exact accepted stop
    classification when the message begins with one of the three known
    STOP_* labels; otherwise PREFLIGHT_HARD_STOP (acknowledgement,
    optional-endpoint, runtime-override, and request-count failures have
    no single dedicated label in the accepted spec)."""
    for prefix in _KNOWN_TRANSPORT_STOP_PREFIXES:
        if message.startswith(prefix):
            return prefix
    return "PREFLIGHT_HARD_STOP"


def _transport_isolation_stop_row(run_id: str, generated_at: str, error_message: str) -> dict:
    """A raw_request_summary_row-shaped stop row for any transport-isolation
    hard-stop (mode ambiguity, acknowledgement, manifest, curl-unavailable).
    Exactly the pinned 34 fields -- no extra 'errors' field. Detailed
    error text is available via Actor logging and
    Actor.fail(status_message=...), not stored on the row itself.
    execution_origin/transport are fixed values on every transport-route
    row, including stop rows -- they describe the route, not the outcome."""
    return {
        "row_type": "raw_request_summary_row",
        "run_id": run_id,
        "request_id": None,
        "condition_id": None,
        "nb_subclass": None,
        "side": None,
        "endpoint": None,
        "request_token_id": None,
        "request_url_market_param": None,
        "request_url_actual": None,
        "window_start_ts": None,
        "window_end_ts": None,
        "fidelity": None,
        "http_status": None,
        "response_byte_length": 0,
        "raw_point_count": 0,
        "raw_response_excerpt": None,
        "response_body_token_id": None,
        "token_identity_basis": None,
        "fetched_at": generated_at,
        "request_classification": _classify_transport_stop_message(error_message),
        "disclaimer_label": TRANSPORT_DISCLAIMER,
        "execution_origin": "APIFY_CURL_LIBCURL",
        "transport": "CURL",
        "curl_executable_path": None,
        "curl_version": None,
        "libcurl_version": None,
        "tls_backend": None,
        "curl_supported_protocols": None,
        "curl_version_output": None,
        "curl_version_exit_code": None,
        "curl_exit_code": None,
        "curl_stderr_excerpt": None,
        "response_headers_excerpt": None,
    }


async def _push_transport_mode_ambiguous_stop(run_id: str, generated_at: str) -> None:
    """Zero-process halt when both transport_isolation_canary_enabled and
    live_canary_enabled are true. Checked at the dispatch level in main(),
    before either sub-path's own gating runs."""
    Actor.log.error(MODE_AMBIGUOUS_MESSAGE)
    await Actor.push_data(_transport_isolation_stop_row(run_id, generated_at, MODE_AMBIGUOUS_MESSAGE))
    await Actor.fail(status_message=MODE_AMBIGUOUS_MESSAGE)


async def _run_transport_isolation_path(raw_input: dict, run_id: str, generated_at: str) -> None:
    """Gated transport-isolation path. See src/transport_isolation_canary.py
    for the full acknowledgement/manifest/curl-preflight gating -- every
    hard-stop below is raised before any curl subprocess in this run."""
    Actor.log.warning(
        "transport_isolation_canary_enabled=true was requested. Checking "
        "acknowledgement, manifest reconciliation, and curl provenance "
        "preflight gates before considering any curl process."
    )
    try:
        rows = run_transport_isolation_from_actor_input(raw_input)
    except TransportIsolationValidationError as exc:
        Actor.log.error(f"Transport-isolation preflight halted before any curl process: {exc}")
        await Actor.push_data(_transport_isolation_stop_row(run_id, generated_at, str(exc)))
        await Actor.fail(status_message=str(exc))
        return

    for row in rows:
        await Actor.push_data(row)

    Actor.log.info(
        f"Transport-isolation canary complete. {len(rows)} rows emitted across "
        "raw_request_summary_row / parsed_side_candidate_row / "
        "condition_pair_summary_row. "
        f"{TRANSPORT_DISCLAIMER} — this run does not establish coverage, does "
        "not update S1_SOURCE_NOT_VIABLE, and does not unblock P1."
    )


async def main() -> None:
    async with Actor:
        raw_input = await Actor.get_input() or {}

        run_id = str(uuid.uuid4())
        generated_at = _dt.datetime.now(_dt.timezone.utc).isoformat()

        if raw_input.get("dry_run", True) is not False:
            await _run_dry_run_path(raw_input, run_id, generated_at)
            return

        transport_requested = raw_input.get("transport_isolation_canary_enabled") is True
        live_requested = raw_input.get("live_canary_enabled") is True

        if transport_requested and live_requested:
            # Zero-process halt, before dispatching to either sub-path's own gating.
            await _push_transport_mode_ambiguous_stop(run_id, generated_at)
            return

        if transport_requested:
            await _run_transport_isolation_path(raw_input, run_id, generated_at)
        else:
            await _run_live_canary_path(raw_input, run_id, generated_at)
