# HANDOFF — Orchestrator Option C C1A-F2 follow-up SPEC

**Decision posture:** DEFER pending artifact review for any implementation/run; proceed only with a no-run / artifact-review-only F2 spec shape.

**Scope of this handoff:** SPEC ONLY. This handoff accompanies `SPEC_price_source_option_c_c1a_f2_followup.md` and records the recommended next decision boundary after accepted C1A-F1 mixed evidence.

---

## 1. What was drafted

Drafted:

1. `SPEC_price_source_option_c_c1a_f2_followup.md`
2. `HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`

The SPEC defines C1A-F2 as a no-run / artifact-review-only follow-up focused on the existing C1A-F1 artifacts, especially the `OVER_UNDER` result with zero Dune rows and two local-only tx hashes.

---

## 2. Standing accepted state preserved

The SPEC preserves the current accepted state:

- Named-binary P1 remains blocked on the absence of an accepted per-side/token-identity decision-time price source.
- `named_binary_probe_blocked` remains `true`.
- Option C is not marked viable.
- Original C1A remains an accepted valid halt: `C1_ROW_EXPLOSION`, one condition returned `2001` rows against `per_condition_row_cap = 2000`.
- C1A-F1 remains accepted as reviewable mixed evidence: `C1_CANARY_EXECUTED_NEEDS_REVIEW`, 133 total Dune rows, no row explosion, no unresolved side rows, 34 Dune-only tx hashes, and a mixed `OVER_UNDER` observation.
- No price was computed or persisted.
- C1A-F1 is not `C1_CANARY_DESIGN_CLEAR`.
- C1B/C2/P1/P2/P3/probe remain unauthorized.

---

## 3. Exact uncertainty identified

The remaining uncertainty is not whether to run a larger sample. It is whether the existing F1 artifacts can explain the `OVER_UNDER` zero-Dune-row / local-only result.

From aggregate counts alone, the SPEC classifies that result as:

`OVER_UNDER_ZERO_DUNE_ROWS_UNRESOLVED_FROM_AGGREGATE_COUNTS`

Possible explanations are explicitly left unproven until artifact review:

- selector/window artifact;
- source-table coverage issue;
- local/Dune tx-hash or composite-identity mismatch;
- source-table/contract mismatch;
- timestamp/window-boundary issue;
- unresolved.

---

## 4. Recommended F2 shape

Recommended:

> Proceed with F2 only as no-run / artifact-review-only.

The SPEC recommends reviewing only already-persisted C1A-F1 artifacts listed in `ARTIFACT_INDEX.md`, including windows/provenance, selector provenance, selected conditions, canary manifest, historical Dune query text, canary results, by-condition ledger, raw-row sample, and tagged rows.

This is designed to test a different uncertainty than another canary: artifact sufficiency and classification of the mixed `OVER_UNDER` evidence, not source coverage at a new condition.

---

## 5. What is rejected or deferred

Rejected now:

- selector-only F2;
- three-condition subclass-balanced diagnostic;
- any second Dune canary under this SPEC;
- any SQL generation or SQL modification;
- any Dune/API/RPC/network call;
- any local data run;
- any cap increase or row truncation;
- any local-tx-hash Dune filtering;
- any Dune count scouting;
- any use of winner/outcome/PnL/score/price/probe fields;
- any price artifact;
- any direct downstream continuation.

Deferred, not authorized:

- one-condition targeted diagnostic. It could be considered only after accepted artifact review identifies a narrowly testable unresolved hypothesis and only through a separate SPEC-only document.

---

## 6. Proposed F2 artifact-review labels

The SPEC defines these allowed labels for any future artifact-review memo:

- `C1F2_ARTIFACT_REVIEW_NOT_STARTED`
- `C1F2_ARTIFACTS_INSUFFICIENT`
- `C1F2_F1_ARTIFACT_DEFECT`
- `C1F2_OVER_UNDER_ZERO_LIKELY_SELECTOR_WINDOW_ARTIFACT`
- `C1F2_OVER_UNDER_ZERO_LIKELY_SOURCE_COVERAGE_GAP`
- `C1F2_OVER_UNDER_ZERO_LIKELY_LOCAL_DUNE_IDENTITY_MISMATCH`
- `C1F2_OVER_UNDER_ZERO_UNRESOLVED`
- `C1F2_REJECT_FURTHER_CANARY`
- `C1F2_ONE_CONDITION_DIAGNOSTIC_SPEC_REQUIRED`

None of these labels may imply source viability, design-clear, P1 unblock, C1B/C2 authorization, probe authorization, price artifact creation, or a gate change.

---

## 7. Explicit authorization boundary

SPEC ONLY.

No implementation authorization.

No run authorization.

No downstream authorization.

No SQL generation or SQL modification authorization.

No Dune/API/RPC/network authorization.

No local data-run authorization.

No C1B/C2/P1/P2/P3/probe/scoring/backfill/wallet/OrdersMatched/`log_index`/PnL authorization.

No price artifact authorization.

Do not mark Option C viable.

Do not mark `C1_CANARY_DESIGN_CLEAR`.

Do not flip `named_binary_probe_blocked`.

---

## 8. Recommended orchestrator decision

Recommended decision:

> **DEFER pending artifact review for any implementation/run; proceed with F2 only as a no-run / artifact-review-only spec shape.**

Operationally, that means:

1. Accept or patch the F2 SPEC shape if the Orchestrator agrees.
2. Do not authorize code, tests, SQL, Dune, local runs, or a second canary.
3. If the user later wants to continue, the next safe request would be a review-only task over existing C1A-F1 artifacts, producing an F2 artifact-review memo with one of the allowed labels.

---

## 9. P1 unblock statement

No F2 outcome can unblock P1 directly.

F2 is coverage/trust diagnostic review only. A future P1 unblock would require a separate accepted price-source spec and accepted evidence for usable per-side/token-identity decision-time prices. F2 does not compute, persist, or validate such prices.
