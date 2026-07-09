# SPEC — Option C artifact-enrichment evidence-capture requirements — SPEC ONLY

**Decision posture:** SPEC ONLY. This document defines evidence-capture requirements for a *possible future* Option C / decoded `OrderFilled` diagnostic. It authorizes no implementation, no run, and no downstream continuation.

**Status:** ACCEPTED by Orchestrator as SPEC ONLY. This document is not implementation authorization and not data-run authorization.

**Scope:** Documentation only. Define the minimum evidence-capture requirements — required artifacts, required columns/fields, required labels, and required stop/reject conditions — for any future Option C / decoded `OrderFilled` diagnostic that compares local rows with source rows, so that local-only, Dune-only, and overlap rows can be reviewed without rerunning data or guessing at causes.

**Canonical source:** `rigolugo/pm_research`. Read order followed: `START_HERE.md`, `project_context/START_HERE.md`, `project_context/PROJECT_STATE.md`, `project_context/ARTIFACT_INDEX.md`, `project_context/GUARDRAILS.md`, `project_context/SPEC_price_source_option_c_onchain.md`, `project_context/SPEC_price_source_option_c_onchain_C1R_addendum.md`, `project_context/SPEC_price_source_option_c_c1a_followup.md`, `project_context/HANDOFF_orchestrator_option_c_c1a_f1_canary_REVIEW.md`, `project_context/SPEC_price_source_option_c_c1a_f2_followup.md`, `project_context/HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`, `project_context/HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md`.

**Hard boundary — this document does not:** implement code; write tests; generate SQL; modify SQL; execute SQL; call Dune/API/RPC/network; run local data; inspect new local data; rerun C1A/C1A-F1; create another canary; create a one-condition diagnostic; authorize C1B/C2; authorize P1/P2/P3/probe; create a price artifact; compute prices; use `yes_price`, `1 - price`, `1 - yes_price`, or `1 - p`; synthesize side prices; use winner/outcome/resolution-winner fields; use PnL/score/probe metrics; expand into wallet discovery; use OrdersMatched; use `log_index`; increase caps; truncate rows; modify gates; or flip `named_binary_probe_blocked`.

---

## 0. Standing state preserved

This spec changes nothing about accepted results. It only defines what a future evidence package would have to contain.

- C1A valid halt accepted: `C1_ROW_EXPLOSION`.
- C1A-F1 accepted as reviewable mixed evidence: `C1_CANARY_EXECUTED_NEEDS_REVIEW`.
- C1A-F2 accepted: `C1F2_ARTIFACTS_INSUFFICIENT`.
- Option C is not viable.
- C1 is not design-clear. `C1_CANARY_DESIGN_CLEAR` is not emitted by this document.
- P1 remains `BLOCKED`.
- `named_binary_probe_blocked` remains `true`.
- C1B, C2, P1, P2, P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, and PnL remain unauthorized.

---

## 1. Problem statement

C1A-F2 accepted `C1F2_ARTIFACTS_INSUFFICIENT` (see `HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md`). The exact defect is:

- The C1A-F1 artifacts preserved aggregate by-condition/by-subclass evidence (Dune row counts, Dune-only/overlap/local-only tx-hash counts, unresolved-side-row counts) and Dune-side/tagged evidence (`c1a_canary_by_condition.csv`, `option_c_c1a_raw_rows_sample.csv`, `option_c_c1a_tagged_rows.csv`).
- For `OVER_UNDER`, the local-only evidence contained only enough information to count two local-only tx hashes. `option_c_c1a_tagged_rows.csv` recorded the two `OVER_UNDER` local-only tx hashes but not the local-side fields needed to interpret them.
- It did **not** preserve enough local-side row detail to determine whether the zero-Dune-row `OVER_UNDER` result was caused by a selector/window artifact, a source coverage gap, a local/Dune identity mismatch, a source-table mismatch, a timestamp/window-boundary issue, or another artifact-level cause.

Missing local-side fields, specifically: local timestamp/`traded_at`, local `token_id`, local `outcome_index`, local side-token match, local row identity, and direct evidence of window membership for the two local-only rows.

This is an evidence-capture gap, not a data-run gap. The fix is a schema requirement for future artifacts, not a rerun of C1A-F1.

---

## 2. Design goal

Define an evidence package such that a future reviewer, using only persisted artifacts and no rerun, no new query, and no new local data read, can independently verify:

1. local row membership in the fixed condition/window/token pair;
2. source row membership in the fixed condition/window/token pair;
3. side-token matching, on both the local side and the source side;
4. overlap / local-only / Dune-only classification, at the row level and reconciled to the by-condition summary;
5. count reconciliation from row-level ledgers up to by-condition summaries;
6. cap discipline (per-condition cap, global cap, cap-exceeded flags);
7. the absence of any price/winner/PnL/score/probe leakage in the artifact set itself.

An artifact set that cannot support all seven checks from persisted data alone is insufficient, regardless of how complete the aggregate summary looks.

---

## 3. Required future artifact set

The following artifacts are required for any future diagnostic that compares local rows with decoded `OrderFilled` rows. This section defines schema requirements only; it does not authorize generating these files now.

### A. `local_comparison_rows.csv`

One row per local trade row within the fixed condition/window scope (not deduplicated by tx hash).

Required columns:

- `condition_id`
- `nb_subclass`
- `tx_hash`
- `local_traded_at_raw`
- `local_traded_at_utc`
- `local_traded_at_epoch`
- `window_start_utc`
- `window_end_utc`
- `inside_window`
- `seconds_from_window_start`
- `seconds_to_window_end`
- `local_token_id`
- `local_outcome_index`
- `side_0_token_id`
- `side_1_token_id`
- `local_matched_side`
- `local_token_match_status`
- `local_row_ordinal`
- `local_row_identity_key`
- `local_quantity_fields_present`
- optional raw non-price quantity fields, only if already present in the local trade schema and needed for identity review
- `local_schema_version_or_source`
- `local_row_parse_status`
- `local_row_parse_error`

Excluded from this artifact: wallet-selection fields, PnL, score, resolution winner, inferred canonical price, `yes_price`, and any side-synthesized price field.

### B. `source_orderfilled_rows.csv`

One row per decoded `OrderFilled` row returned within the fixed condition/window/token scope.

Required columns:

- `condition_id`
- `nb_subclass`
- `tx_hash`
- `source_table`
- `block_time_raw`
- `block_time_utc`
- `block_time_epoch`
- `window_start_utc`
- `window_end_utc`
- `inside_window`
- `makerAssetId`
- `takerAssetId`
- `makerAmountFilled`
- `takerAmountFilled`
- `side_0_token_id`
- `side_1_token_id`
- `source_matched_side`
- `source_token_match_status`
- `source_row_ordinal`
- `source_row_identity_key`
- `source_parse_status`
- `source_parse_error`

Excluded from this artifact: maker/taker wallet-address analysis, OrdersMatched fields, `log_index`, PnL, score, and any price field.

### C. `comparison_tagged_rows.csv`

Row-level join/comparison ledger carrying enough identity from both A and B to classify each row without recomputation.

Required columns:

- all row identity keys needed to join or compare (from A and B)
- `condition_id`
- `nb_subclass`
- `tx_hash`
- `row_origin` — allowed values: `LOCAL`, `SOURCE`, `BOTH`
- `tx_hash_relation` — allowed values: `OVERLAP`, `LOCAL_ONLY`, `DUNE_ONLY`, `UNRESOLVED_SIDE`, `OUT_OF_WINDOW`, `PARSE_BLOCKED`
- `local_row_identity_key`
- `source_row_identity_key`
- `local_matched_side`
- `source_matched_side`
- `local_token_match_status`
- `source_token_match_status`
- `local_inside_window`
- `source_inside_window`
- `classification_reason_code`
- `classification_detail`

This is the artifact that C1A-F1's `option_c_c1a_tagged_rows.csv` did not carry enough local-side fields to support for the `OVER_UNDER` local-only rows. This spec requires that any future version of this artifact carry the full local-side and source-side identity columns above for every row, including rows classified `LOCAL_ONLY` or `DUNE_ONLY`.

### D. `comparison_by_condition.csv`

Per-condition summary, required to reconcile exactly against the row-level ledgers in A/B/C.

Required columns:

- `condition_id`
- `nb_subclass`
- `local_rows_in_window`
- `source_rows_in_window`
- `local_distinct_tx_hash_count`
- `source_distinct_tx_hash_count`
- `overlap_tx_hash_count`
- `local_only_tx_hash_count`
- `dune_only_tx_hash_count`
- `unresolved_side_rows`
- `out_of_window_rows`
- `parse_blocked_rows`
- `cap_exceeded`
- `per_condition_row_cap`
- `dune_query_limit`
- `global_row_cap`
- `artifact_completeness_status`

Every count in this file must be independently recomputable from A, B, and C. A future reconciliation step (E) must show that recomputed counts match these summary counts exactly.

### E. `comparison_reconciliation.json`

Machine-readable self-attestation of artifact completeness and guardrail compliance.

Required fields:

- artifact list with existence flags
- row counts by artifact
- recomputed counts from ledgers (A/B/C recomputation of D)
- equality checks between row ledgers and summaries
- cap checks
- empty-export checks
- parse-error counts
- schema/version fields
- guardrail flags:
  - `no_price_artifact`
  - `no_yes_price`
  - `no_side_synthesis`
  - `no_winner_fields`
  - `no_pnl_score_probe_fields`
  - `no_wallet_discovery`
  - `no_ordersmatched`
  - `no_log_index`
  - `named_binary_probe_blocked_observed_true`
- final artifact completeness label (§4)

### F. `artifact_schema.md`

Human-readable companion explaining:

- data sources used;
- columns preserved;
- columns deliberately excluded, and why;
- why each retained field is needed for future review;
- an explicit statement that this schema authorizes no downstream run, no C1B/C2/P1/P2/P3/probe, and no price artifact.

---

## 4. Required labels

Allowed artifact-readiness labels for any future artifact-enrichment evidence package:

- `ARTIFACT_ENRICHMENT_SPEC_ONLY`
- `ARTIFACT_SCHEMA_READY_FOR_REVIEW`
- `ARTIFACT_SCHEMA_INSUFFICIENT_LOCAL_SIDE`
- `ARTIFACT_SCHEMA_INSUFFICIENT_SOURCE_SIDE`
- `ARTIFACT_SCHEMA_REJECT_PRICE_LEAKAGE`
- `ARTIFACT_SCHEMA_REJECT_WINNER_OUTCOME_LEAKAGE`
- `ARTIFACT_SCHEMA_REJECT_WALLET_OR_LOG_INDEX_SCOPE`
- `ARTIFACT_SCHEMA_REJECT_DOWNSTREAM_AUTHORIZATION`
- `ARTIFACT_RECONCILIATION_FAILED`

This document itself ends with: **`ARTIFACT_ENRICHMENT_SPEC_ONLY`**.

---

## 5. Stop/reject conditions

A future evidence-capture attempt built against this spec must stop (and must not self-label `ARTIFACT_SCHEMA_READY_FOR_REVIEW`) if any of the following hold:

1. local-only rows lack local timestamp/token/outcome_index/side-match/window-membership fields;
2. source rows lack source-table/`block_time`/token-side evidence;
3. row ledgers (A/B/C) cannot reproduce the by-condition summary (D) exactly;
4. artifacts include price, winner, PnL, score, or probe fields;
5. artifacts include wallet discovery, OrdersMatched, or `log_index` expansion;
6. any artifact implies P1/C1B/C2/probe authorization;
7. caps are raised, or truncation is used to self-clear a capped or incomplete result;
8. Dune or local tx-hash filters are used to force overlap;
9. a one-condition diagnostic or an additional canary is embedded inside the evidence-capture step itself.

Any of these conditions requires the label `ARTIFACT_RECONCILIATION_FAILED` or the relevant `ARTIFACT_SCHEMA_REJECT_*` label, not `ARTIFACT_SCHEMA_READY_FOR_REVIEW`.

---

## 6. Explicit non-goals

This spec does not:

- classify the current `OVER_UNDER` zero-Dune result;
- make Option C viable;
- mark C1 design-clear;
- unblock P1;
- authorize implementation;
- authorize tests;
- authorize local data reads;
- authorize Dune/API/RPC/network calls;
- authorize SQL generation or modification;
- authorize another canary;
- authorize a one-condition diagnostic;
- authorize C1B or C2;
- authorize P1, P2, P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, or PnL;
- create a price artifact.

The `OVER_UNDER` zero-Dune-row / local-only observation from C1A-F1 remains exactly as classified in `HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md`: unresolved from existing artifacts. This spec defines what a future evidence package would need in order to resolve it; it does not resolve it.

---

## 7. Guardrails preserved

Research only. This SPEC authorizes no implementation, no code, no tests, no SQL generation or modification, no Dune/API/RPC/network call, no local data run, no inspection of new local data, no rerun of C1A/C1A-F1, no additional canary, no one-condition diagnostic, no C1B, no C2, no P1/P2/P3, no probe execution, no scoring, no backfill, no wallet discovery, no OrdersMatched expansion, no `log_index`, no PnL, no cap increase, no row truncation, no gate modification, no price artifact, no `yes_price`/`1 - price`/`1 - yes_price`/`1 - p`, and no side synthesis.

`named_binary_probe_blocked` remains `true`. P1 remains `BLOCKED`. Option C remains not viable. C1 remains not design-clear.

**`ARTIFACT_ENRICHMENT_SPEC_ONLY`**
