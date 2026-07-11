"""
Polymarket Price Canary Actor — entry point.

DRY-RUN BY DEFAULT. Live-canary capability exists behind explicit,
multi-flag gating (see below) and is NOT executed as part of this
delivery -- no Apify run, no build/deploy, no network call, no live
dataset. Per SPEC_apify_live_price_source_canary.md (accepted, branch
apify-price-canary-dry-run) and the current "implementation package
review only" authorization.

Two code paths:

1. DEFAULT / dry_run path (raw_input.get("dry_run", True) is not the
   literal value False): completely unchanged from the prior dry-run-only
   build. Uses src/validation.py only. Makes ZERO network calls -- no
   HTTP client is imported by that path at all. This is the path taken
   whenever `dry_run` is absent, `true`, or anything other than the exact
   JSON boolean `false`.

2. LIVE-CANARY path (raw_input.get("dry_run", True) is exactly False):
   dispatches to src/live_canary.py's run_live_canary_from_actor_input(),
   which:
     - checks live_canary_enabled == true and acknowledge_not_p1_evidence
       == true FIRST -- if either is missing/false, hard-stops (raises)
       before touching conditions, before building any request plan,
       before an HttpFetcher is ever constructed;
     - then strictly validates the conditions manifest (exactly 3, one
       per subclass, valid string-safe tokens, no duplicates) -- any
       problem hard-stops the WHOLE run before any request;
     - then builds the request plan and enforces the hard cap (<=12)
       BEFORE any request is made;
     - only after all of the above passes does it construct a real
       HttpFetcher and make requests.
   This Actor build does not have live-canary mode invoked against a real
   run as part of its delivery -- see the implementation handoff's
   self-attestation.

Standing guardrails enforced across both paths:
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
  - Does not claim S1_SOURCE_NOT_VIABLE has changed; every row from either
    path carries its own disclaimer.
  - /batch-prices-history is intentionally not used anywhere (see
    validation.py and live_canary.py).
"""

from __future__ import annotations

import datetime as _dt
import uuid

from apify import Actor

from .live_canary import LiveCanaryValidationError, run_live_canary_from_actor_input
from .validation import CanaryValidationError, RequestPlanRow, build_request_plan

SCHEMA_VERSION = "apify-canary-plan-1.0"
DISCLAIMER = "APIFY_CANARY_NOT_COVERAGE_EVIDENCE"
LIVE_DISCLAIMER = "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE"


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


async def main() -> None:
    async with Actor:
        raw_input = await Actor.get_input() or {}

        run_id = str(uuid.uuid4())
        generated_at = _dt.datetime.now(_dt.timezone.utc).isoformat()

        if raw_input.get("dry_run", True) is False:
            await _run_live_canary_path(raw_input, run_id, generated_at)
        else:
            await _run_dry_run_path(raw_input, run_id, generated_at)
