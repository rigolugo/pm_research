# HANDOFF — Orchestrator Option C artifact-enrichment evidence-capture SPEC

**Primary decision label:** `ARTIFACT_ENRICHMENT_SPEC_ONLY`

**Scope:** Documentation-only handoff for the newly drafted `SPEC_price_source_option_c_artifact_enrichment.md`. No code, tests, SQL generation, SQL edits, Dune/API/RPC/network calls, local data processing, rerun, new canary, one-condition diagnostic, price artifact, or probe/scoring/backfill/wallet/OrdersMatched/`log_index`/PnL work was performed. No gate was changed.

---

## 1. What was drafted

`project_context/SPEC_price_source_option_c_artifact_enrichment.md` — a SPEC-only document defining the minimum evidence-capture requirements for any *future* Option C / decoded `OrderFilled` diagnostic that compares local rows with source rows. It specifies six required artifacts (`local_comparison_rows.csv`, `source_orderfilled_rows.csv`, `comparison_tagged_rows.csv`, `comparison_by_condition.csv`, `comparison_reconciliation.json`, `artifact_schema.md`), their required columns, nine allowed readiness labels, explicit stop/reject conditions, and explicit non-goals.

---

## 2. Why this spec exists

C1A-F2 accepted `C1F2_ARTIFACTS_INSUFFICIENT` (`HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md`). The C1A-F1 artifacts confirmed the mixed by-subclass summary and safe selector/query/cap discipline, but the two `OVER_UNDER` local-only tx hashes lacked local-side timestamp, token, `outcome_index`, side-match, row-identity, and window-membership fields. That gap made it impossible to distinguish, from artifacts alone, a selector/window artifact from a source coverage gap, a local/Dune identity mismatch, a source-table mismatch, or a timestamp/window-boundary issue.

`HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md` §10 and `project_context/START_HERE.md` both name a doc-only artifact-enrichment review specification as the only safe next step if this specific unresolved gap is to be pursued later. This document is that spec.

---

## 3. What artifact weakness it fixes (prospectively, not retroactively)

This spec does **not** repair or reinterpret the existing C1A-F1 artifacts. It defines what a future artifact set would need to contain so that a future reviewer could, from persisted files alone:

- confirm local and source row membership in the fixed condition/window/token pair;
- confirm side-token matching on both the local and source sides;
- classify every row as overlap, local-only, Dune-only, unresolved-side, out-of-window, or parse-blocked;
- reconcile row-level ledgers exactly against by-condition summaries;
- confirm cap discipline;
- confirm the absence of price/winner/PnL/score/probe leakage.

The existing `OVER_UNDER` zero-Dune-row observation remains unresolved and is not reclassified by this document.

---

## 4. What it does not authorize

This spec and this handoff do not authorize:

- implementation, code, or tests;
- SQL generation, modification, or execution;
- any Dune/API/RPC/network call;
- any local data run or inspection of new local data;
- a rerun of C1A or C1A-F1;
- another canary;
- a one-condition diagnostic;
- C1B or C2;
- P1, P2, P3, or probe execution;
- scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, or PnL;
- a price artifact, `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis;
- any gate change or flip of `named_binary_probe_blocked`.

---

## 5. Standing state unchanged

- C1A valid halt accepted: `C1_ROW_EXPLOSION`.
- C1A-F1 accepted as reviewable mixed evidence: `C1_CANARY_EXECUTED_NEEDS_REVIEW`.
- C1A-F2 accepted: `C1F2_ARTIFACTS_INSUFFICIENT`.
- Option C is not viable. C1 is not design-clear. `C1_CANARY_DESIGN_CLEAR` is not emitted.
- P1 remains `BLOCKED`. `named_binary_probe_blocked` remains `true`.
- C1B, C2, P1, P2, P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, and PnL remain unauthorized.
- No files other than the two listed below were created or modified.

---

## 6. Files delivered this task

1. `project_context/SPEC_price_source_option_c_artifact_enrichment.md`
2. `project_context/HANDOFF_orchestrator_option_c_artifact_enrichment_SPEC.md` (this file)

Delivery does not equal acceptance or authorization. Both files await Orchestrator review before any commit or reliance.

---

## 7. Recommended orchestrator decision

Recommended: review and, if acceptable, mark `ARTIFACT_ENRICHMENT_SPEC_ONLY` accepted / spec-only in `PROJECT_STATE.md` and `ARTIFACT_INDEX.md`. This acceptance would still not authorize generating any of the six required artifacts, running C1A/C1A-F1 again, or proceeding to C1B/C2/P1/P2/P3/probe. Any future step that would actually produce these artifacts requires separate, explicit authorization and remains bounded by all standing guardrails.
