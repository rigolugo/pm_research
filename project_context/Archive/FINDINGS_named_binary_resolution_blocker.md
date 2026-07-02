# Findings — Named-Binary Semantics Run + Resolution-Data Blocker

Status: semantics layer COMPLETE and sound. Named-binary probe BLOCKED by data
availability (not by code). No probe was run. This memo proposes DECISION_LOG /
PROJECT_STATE updates and a next-step fork for you to decide.

---

## What ran

`audit_named_binary_semantics.py` over the full dataset (16,505,185 trades /
288,684 conditions, 250 shards, ~3 min). Gate returned
`BLOCKED_BY_RESOLUTION_MAPPING`. Three read-only diagnostics then isolated the
cause exactly.

## Established facts (counts, not samples)

1. **Semantics layer is sound.**
   - token_id coverage 0.99601, outcome_index coverage 0.99601 (matches the
     project's known ~99.6% key coverage).
   - orientation_correctness_rate 1.0 across all eligible conditions.
   - Eligible (cleanly two-token mapped) named-binary conditions: 105,561.
   - Subclass mix: YES_NO 65,603 / UP_DOWN 22,013 / NAMED_OTHER 16,905 /
     OVER_UNDER 1,039 (label-pair census, seed lexicon, zero hand-rules needed).

2. **`resolutions.parquet` is YES/NO-framed and partial.**
   - 22,019 resolution rows total; `winning_outcome` takes ONLY values
     `NO` (16,920) and `YES` (5,099). No team / UP-DOWN / OVER-UNDER winner
     value appears anywhere.
   - Of 105,561 eligible conditions, only 10,923 have a resolution row at all.

3. **Named-binary is structurally unresolvable against this file.**
   Of eligible conditions that HAVE a resolution row, winner-maps-to-a-side:
   - YES_NO:      8,521 / 8,521   (100%)
   - NAMED_OTHER:     0 / 1,814   (0%)
   - OVER_UNDER:      0 /    53   (0%)
   - UP_DOWN:         0 /   535   (0%)
   The 2,402 non-YES/NO "with-resolution" rows resolve to `YES`/`NO`, which match
   neither named side. They are join coincidences, not usable outcomes.

## Two separate issues (do not conflate)

- **Issue A — schema-audit threshold bug (mine, fixable).**
  `determine_schema` requires one interpretation to clear 99% across the whole
  mixed-subclass eligible set, then applies it globally. The 0%-mapping
  named-binary majority drags the label interpretation below 99%, so
  `chosen_schema=None` and the gate reports `resolution_mapping_success_rate=0.0`
  for everything — masking a perfect 8,521/8,521 YES/NO result. Fix: choose the
  schema on the cleanly-mappable subset and report the true per-condition rate.
  **Effect of fixing: recovers the YES/NO universe only. Does NOT make
  named-binary testable.**

- **Issue B — resolution data does not cover named-binary (data, not code).**
  No fix in code. The realized outcomes needed to score team/UP-DOWN/OVER-UNDER
  predictions are absent from `resolutions.parquet`. This blocks the named-binary
  PROBE that the rewrite was built to enable.

## What this does NOT change

- The semantics layer (classification contract, canonical_side_price/oriented_
  price, orientation-by-identity, audit gate) is validated and stays.
- The audit gate behaved correctly: it refused to certify a universe it could not
  resolve, BEFORE any probe ran. A naive probe would have scored 105k markets
  against a YES/NO winner and produced plausible-looking garbage.
- `nb_contract_version` / classification contract is intact for Chat2 to consume.

## Proposed DECISION_LOG entry

> **Named-binary realized outcomes are not present in local resolutions.parquet
> (settled, data-availability).** `winning_outcome` is YES/NO-only (22,019 rows,
> values {NO:16920, YES:5099}). Eligible named-binary conditions: 105,561; with
> any resolution row: 10,923; non-YES/NO conditions whose winner maps to a side:
> 0 / 2,402. The yes_price/canonical_side_price semantics layer is validated
> (orientation 1.0, coverage 0.996, YES/NO resolution 8,521/8,521). The
> named-binary PROBE is blocked pending a resolution source that adjudicates
> team/UP-DOWN/OVER-UNDER outcomes. Caught at the audit gate; no probe run.

## Proposed PROJECT_STATE update

- Named-binary yes_price rewrite: semantics layer DONE and gated.
- Named-binary probe: BLOCKED — needs non-YES/NO realized outcomes (likely a
  Dune market-resolution pull keyed by condition_id, mapping winner -> token /
  outcome_index). Until then, no named-binary probe is runnable.

## Next-step fork (YOUR decision — I will not assume)

1. **Source named-binary resolutions from Dune** (market resolution / payout
   events keyed by condition_id, normalized to a winning token_id/outcome_index).
   This is the only path that makes the named-binary probe possible. Spec-first,
   honoring the varchar-cast/precision lessons. Biggest scope, but it's the
   actual unlock.

2. **Fix Issue A and re-baseline on YES/NO only.** Quick. Gives a clean
   `CLEAR*`-gated YES/NO semantics result and confirms the layer end-to-end on
   real outcomes — but it's the universe Rank 1A already closed negative, so it's
   a validation pass, not new ground.

3. **Pause the branch.** Record the finding; do not invest further until a
   resolution source is decided.

My recommendation: **fix Issue A regardless** (it's small and the 0% is actively
misleading sitting in the artifacts), then decide between (1) and (3). Do NOT run
any named-binary probe — there is nothing to score against. (2) alone is low value
because it re-enters the closed Rank 1A universe.

## Guardrails

No probe was run and none is authorized by this memo. No PnL, no wallet logic, no
copy-trading. The diagnostics are read-only. A `CLEAR*` gate (even after the
Issue-A fix) still would not authorize a probe — that remains a separate explicit
decision, and for named-binary it is moot until outcomes exist.

## Files (diagnostics, read-only — place in scripts\)

- `scripts/diag_resolution_mapping.py`
- `scripts/diag_resolution_coverage.py`
- `scripts/diag_named_binary_resolvable.py`
