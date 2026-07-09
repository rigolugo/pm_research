# HANDOFF — Orchestrator Option C C1A-F2 artifact review

**Primary decision label:** `C1F2_ARTIFACTS_INSUFFICIENT`

**Scope:** Review-only / documentation-only F2 artifact memo for C1A-F2. No code, tests, SQL generation, SQL edits, Dune/API/RPC/network calls, local data processing, rerun, new canary, price artifact, probe/scoring/backfill/wallet/OrdersMatched/`log_index`/PnL work, cap change, row truncation, or gate change was performed.

---

## 1. Reviewed / attempted artifact list

The review attempted to inspect the C1A-F1 artifacts listed in `ARTIFACT_INDEX.md` under:

`artifacts/named_binary_probe/price_source_option_c_c1a_f1/`

Expected C1A-F1 artifact set:

1. `c1a_f1_windows.json`
2. `c1a_f1_windows.json.provenance.json`
3. `c1a_f1_selector_provenance.json`
4. `c1a_f1_selected_conditions.csv`
5. `c1a_f1_selector_excluded.csv`
6. `c1a_f1_canary_manifest.json`
7. `c1a_f1_dune_query.sql` — historical evidence only, not for edit or rerun
8. `c1a_canary_result.json`
9. `c1a_canary_result.md`
10. `c1a_canary_by_condition.csv`
11. `option_c_c1a_raw_rows_sample.csv`
12. `option_c_c1a_tagged_rows.csv`

Also checked, by exact canonical path, the two F2 context files named in the task:

1. `project_context/SPEC_price_source_option_c_c1a_f2_followup.md`
2. `project_context/HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`

---

## 2. Artifact completeness finding

The F2 artifact review cannot be completed from the canonical GitHub repo state inspected for this memo.

Findings:

- `ARTIFACT_INDEX.md` documents the expected C1A-F1 artifact set and records the accepted C1A-F1 result as reviewable mixed coverage/trust evidence.
- The exact C1A-F1 artifact paths listed above were not retrievable from the canonical repo by exact path during this review.
- Repository search found documentation references to `price_source_option_c_c1a_f1`, but did not surface the listed persisted C1A-F1 artifact files themselves.
- The two required F2 source documents named in the task, `SPEC_price_source_option_c_c1a_f2_followup.md` and `HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`, were also not retrievable from the canonical repo by exact path.

Because the actual F1 artifacts were not available for direct inspection, this memo cannot verify manifest integrity, window comparability, token-pair comparability, source-table provenance, cap discipline, or local-only evidence shape from artifact contents. Documentation summaries alone are insufficient for the requested F2 artifact review.

Decision consequence: use `C1F2_ARTIFACTS_INSUFFICIENT`, not a likely-cause label.

---

## 3. `OVER_UNDER` evidence summary

Accepted summary evidence from the already-recorded C1A-F1 result says:

- `OVER_UNDER`: `0` Dune rows
- `OVER_UNDER`: `0` Dune-only tx hashes
- `OVER_UNDER`: `0` overlap tx hashes
- `OVER_UNDER`: `2` local-only tx hashes
- `OVER_UNDER`: `0` unresolved side rows

This is sufficient to state that the accepted C1A-F1 result was mixed and that `OVER_UNDER` was the zero-Dune-row subclass in the selected 3-condition canary.

It is not sufficient for F2 to assign a specific cause. Without the actual windows, manifest, SQL text, selected-condition ledger, by-condition ledger, and tagged-row evidence, this review cannot determine whether the `OVER_UNDER` zero is more likely:

- a selector/window artifact;
- a source coverage gap;
- a local/Dune identity mismatch; or
- some other unresolved artifact-level explanation.

No “likely” label is supported by directly inspected artifact contents.

---

## 4. Selector / window / token / source-table / local-only evidence review

### Selector provenance

Not verifiable from artifact contents. The required selector provenance file was not available for direct inspection.

Therefore this review cannot independently confirm from the artifact that the `OVER_UNDER` condition was selected only by the accepted deterministic, outcome-independent policy and not by result-aware edits, Dune counts, local-tx-hash filtering, or winner/outcome fields.

### Manifest integrity

Not verifiable from artifact contents. The required canary manifest file was not available for direct inspection.

Therefore this review cannot independently confirm that the `OVER_UNDER` manifest row contains exactly two string-safe side token IDs, fixed window bounds, subclass label, caps, and source-table/version fields.

### Window comparability

Not verifiable from artifact contents. The windows, manifest, SQL, canary result, and by-condition ledger were not available together for direct comparison.

Therefore this review cannot compare the `OVER_UNDER` fixed window across all required evidence surfaces.

### Token-pair comparability

Not verifiable from artifact contents. The selected-condition CSV, manifest, SQL text, and tagged rows were not available together for direct comparison.

Because `OVER_UNDER` had zero Dune rows in the accepted summary, no source-side token behavior can be inferred from returned Dune rows for that subclass. The artifact-level question remains unresolved.

### Source-table provenance

Not verifiable from artifact contents. The historical SQL and result metadata were not available for direct inspection.

Therefore this review cannot independently confirm that the actual historical SQL/result metadata names only the expected decoded `OrderFilled` source table(s), nor can it rule out arbitrary table substitution from artifact contents.

### Local-only evidence shape

Not verifiable from artifact contents. The by-condition ledger and tagged-row evidence were not available for direct inspection.

Therefore this review cannot independently confirm that the two `OVER_UNDER` local-only tx hashes are represented sufficiently to show they belong to the fixed condition/window/token-pair comparison. No tx-hash lookup, Dune requery, source lookup, or count scout was performed.

---

## 5. No price leakage review

Not verifiable from artifact contents. The selector provenance, selected-condition source, manifest, SQL, result, by-condition ledger, and tagged rows were not available for direct inspection.

This review therefore cannot independently confirm from the artifacts that no price, canonical-side price, winner fields, PnL, score, or probe metrics were consumed in selector/review artifacts.

Standing accepted context still says no price was computed or persisted in C1A-F1, and the review does not contradict that. The issue is only that F2 artifact-level verification cannot be completed without the artifacts.

---

## 6. Cap discipline review

Not verifiable from artifact contents. The manifest and SQL were not available for direct inspection.

Accepted documentation says C1A-F1 preserved:

- `per_condition_row_cap = 2000`
- per-condition SQL `LIMIT = 2001` (`cap + 1` over-fetch)
- `global_row_cap = 6000`
- no row explosion
- no truncation

F2 cannot independently confirm those fields across manifest, SQL, and result artifacts without the actual files.

---

## 7. Defects / insufficiencies found

Primary insufficiency:

- The expected F1 artifact files listed in `ARTIFACT_INDEX.md` were not available for direct artifact review from the canonical repo paths inspected here.

Additional context-file insufficiency:

- The required F2 context files named in the task were not available by exact canonical repo path:
  - `project_context/SPEC_price_source_option_c_c1a_f2_followup.md`
  - `project_context/HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`

This is not a finding that the C1A-F1 result is invalid. It is a finding that F2 artifact review cannot substantiate a more specific label from the artifacts currently available to this review.

---

## 8. Interpretation discipline

No F2 outcome unblocks P1.

This memo does not mark Option C viable. It does not mark C1 design-clear. It does not emit or record `C1_CANARY_DESIGN_CLEAR`. It does not authorize C1B, C2, P1, P2, P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, cap increases, truncation, SQL modification, another canary, or any price artifact.

Standing state remains:

- Option C is not viable.
- C1 is not design-clear.
- P1 remains `BLOCKED` on missing accepted per-side/token-identity decision-time price source.
- `named_binary_probe_blocked` remains `true`.
- C1B/C2/P1/P2/P3/probe remain unauthorized.
- No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis may be used to unblock named-binary pricing.

---

## 9. Recommended next action

**Recommended next action:** remain unresolved / stop.

Do not proceed to another canary, C1B, C2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, cap change, row truncation, SQL modification, price artifact, or any implementation task from this memo.

Before any F2 artifact-level conclusion can be made, the exact listed C1A-F1 artifacts and the missing F2 context documents must be made available in the canonical repo, or explicitly supplied as the review input under a new review-only authorization. After that, F2 can be repeated as artifact review only.

No separate one-condition diagnostic spec is recommended from this memo, because the current insufficiency is artifact availability, not a narrowly testable artifact-supported hypothesis.
