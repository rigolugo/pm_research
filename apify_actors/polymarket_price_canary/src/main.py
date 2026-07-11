"""
Polymarket Price Canary Actor — entry point.

DRY-RUN ONLY IN THIS BUILD. This module makes ZERO network calls to
Polymarket, Gamma, or any other external host. It only:
  1. Reads Actor input.
  2. Validates it and builds the planned request URLs via
     src/validation.py (pure logic, independently unit-tested).
  3. Pushes one dataset row per planned request (or per validation error)
     to the Actor's default dataset.

It never calls requests/httpx/aiohttp/urllib.request or any other HTTP
client against Polymarket/Gamma. The only outbound traffic this container
performs is the Apify SDK's own calls to the Apify platform for input and
dataset I/O, which are not Polymarket calls and are unrelated to the
guardrails this project cares about.

See project_context/SPEC_apify_polymarket_price_canary.md in
rigolugo/pm_research for the full design and guardrail rationale.
Standing guardrails enforced here:
  - Hard condition cap <= 5 (src/validation.py).
  - No wallet/profile/leaderboard/comments/positions/activity endpoint is
    reachable: only three fixed, known-safe endpoint families are ever
    addressed, and no user-supplied path is used verbatim.
  - No yes_price / 1-price / 1-yes_price / side synthesis, no price
    computation, no canonical_side_price, no scoring.
  - P1/P2/P3/probe/gate terms (including named_binary_probe_blocked)
    appear only in guardrail/disclaimer language (e.g. the DISCLAIMER
    string and log messages below) and are never read, modified,
    computed, or used as operational state anywhere in this Actor.
  - Does not claim S1_SOURCE_NOT_VIABLE has changed; every row carries the
    APIFY_CANARY_NOT_COVERAGE_EVIDENCE disclaimer.
  - /batch-prices-history is intentionally not used (see validation.py).
"""

from __future__ import annotations

import datetime as _dt
import uuid

from apify import Actor

from .validation import CanaryValidationError, RequestPlanRow, build_request_plan

SCHEMA_VERSION = "apify-canary-plan-1.0"
DISCLAIMER = "APIFY_CANARY_NOT_COVERAGE_EVIDENCE"


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


async def main() -> None:
    async with Actor:
        raw_input = await Actor.get_input() or {}

        if raw_input.get("dry_run", True) is False:
            Actor.log.warning(
                "dry_run=false was supplied, but this Actor build is "
                "DRY-RUN ONLY and contains no network-call code path at "
                "all. Forcing dry-run behavior regardless. A live-run mode "
                "would require a separate, explicitly authorized build."
            )

        run_id = str(uuid.uuid4())
        generated_at = _dt.datetime.now(_dt.timezone.utc).isoformat()

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
