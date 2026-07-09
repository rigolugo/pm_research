# SPEC — Option C C1A-F2 follow-up after C1A-F1 mixed diagnostic evidence — SPEC ONLY

**Decision posture:** DEFER pending artifact review for any additional run; proceed only with a no-run / artifact-review-only F2 shape.

**Status:** Proposed for Orchestrator review. This document is not acceptance, not implementation authorization, and not data-run authorization.

**Scope:** Decide whether a second bounded diagnostic is justified after accepted C1A-F1 mixed evidence, and define the safest SPEC ONLY shape if any follow-up is allowed.

**Canonical source:** `rigolugo/pm_research`. Read order followed from `START_HERE.md` and `project_context/START_HERE.md`, including `PROJECT_STATE.md`, `ARTIFACT_INDEX.md`, `GUARDRAILS.md`, `SPEC_price_source_option_c_onchain.md`, `SPEC_price_source_option_c_onchain_C1R_addendum.md`, `SPEC_price_source_option_c_c1a_followup.md`, and `HANDOFF_orchestrator_option_c_c1a_f1_canary_REVIEW.md`.

**Hard boundary:** This is a document-only specification. No implementation, code, tests, SQL generation, SQL modification, Dune/API/RPC/network call, Dune run, local data run, artifact mutation, cap increase, row truncation, C1B, C2, P1/P2/P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, price artifact, local-tx-hash Dune filtering, Dune count scouting, winner/outcome/PnL/score field use, `yes_price`, `1 - price`, `1 - yes_price`, or side synthesis is authorized or proposed here.

---

## 1. Standing accepted state

Named-binary P1 remains blocked on the absence of an accepted per-side/token-identity decision-time price source. `named_binary_probe_blocked` remains `true`. Option C is not marked viable.

The original C1A bounded canary is accepted as a valid halt:

- outcome: `C1_ROW_EXPLOSION`;
- one condition returned `2001` rows against `per_condition_row_cap = 2000`;
- the `cap + 1` behavior proved cap exceedance rather than silent truncation;
- no price was computed or persisted.

C1A-F1 then executed and is accepted as reviewable mixed coverage/trust evidence:

- outcome: `C1_CANARY_EXECUTED_NEEDS_REVIEW`;
- total Dune rows in fixed windows: `133`;
- no row explosion;
- no unresolved side rows;
- total Dune-only tx hashes: `34`;
- `NAMED_OTHER`: `104` Dune rows, `27` Dune-only tx hashes, `2` overlap tx hashes, `0` local-only tx hashes, `0` unresolved side rows;
- `UP_DOWN`: `29` Dune rows, `7` Dune-only tx hashes, `4` overlap tx hashes, `0` local-only tx hashes, `0` unresolved side rows;
- `OVER_UNDER`: `0` Dune rows, `0` Dune-only tx hashes, `0` overlap tx hashes, `2` local-only tx hashes, `0` unresolved side rows;
- no price was computed or persisted;
- this is not `C1_CANARY_DESIGN_CLEAR`.

C1A-F1 is diagnostic evidence only. It does not unblock P1, does not authorize C1B/C2/P1/P2/P3/probe, and does not justify a price artifact.

---

## 2. Exact uncertainty remaining after C1A-F1

C1A-F1 answered only a narrow mechanism question: the fixed, subclass-balanced, low-density selector produced a readable bounded diagnostic without row explosion. It did not answer whether decoded `OrderFilled` tables are a usable per-side/token-identity price source.

The remaining uncertainties are:

1. **Subclass consistency.** `NAMED_OTHER` and `UP_DOWN` showed Dune-only tx hashes in the fixed windows, but `OVER_UNDER` returned zero Dune rows despite two local-only tx hashes. The source behavior is therefore not uniform across the selected subclasses.
2. **OVER_UNDER zero-source ambiguity.** From aggregate counts alone, the `OVER_UNDER` result cannot be assigned to one cause. It may reflect a selector/window artifact, a source-table coverage issue, a local/Dune identity mismatch, a source-table/contract selection mismatch, a timestamp/window-boundary issue, or some local artifact not visible in the aggregate report.
3. **Token-side evidence scope.** Zero unresolved side rows supports token-side tagging only for rows returned by Dune. It says nothing about side identity for rows that Dune did not return, especially the `OVER_UNDER` local-only rows.
4. **Coverage-vs-trust separation.** Dune-only tx hashes show that the decoded source can surface rows absent from local for two selected conditions. They do not prove decision-time both-side price coverage, source completeness, ordering completeness, or production viability.
5. **F1 artifact sufficiency.** It remains unknown whether the existing C1A-F1 artifacts are sufficient to classify the `OVER_UNDER` zero-row observation without running anything else.

These are evidence-quality and source-trust questions, not price-computation questions.

---

## 3. Interpretation of the `OVER_UNDER` zero-Dune-row / local-only result

The current correct classification is:

> `OVER_UNDER_ZERO_DUNE_ROWS_UNRESOLVED_FROM_AGGREGATE_COUNTS`.

More specific classifications are possible only after no-run artifact review, and only if the existing artifacts support them.

### 3.1 Selector/window artifact — plausible, not established

A selector/window artifact is plausible if existing artifacts show any of the following:

- the fixed window for the `OVER_UNDER` condition differs from the local evidence window in a way that could exclude the local tx hashes;
- the window was constructed from a boundary rule that can produce a non-comparable Dune `block_time` range for this subclass;
- token-pair identity was valid locally but not aligned with the decoded table's `makerAssetId` / `takerAssetId` representation for that condition;
- the condition was selected from a low-density band that had enough local evidence for comparison but was too near-empty to make a zero-source observation informative.

This cannot be assumed. It must be shown from existing artifact fields.

### 3.2 Source-table coverage issue — plausible, not established

A source-table coverage issue is plausible if existing artifacts show that:

- the `OVER_UNDER` local-only tx hashes should have been present under the same decoded `OrderFilled` table/window/token filter, yet no source rows were returned;
- the selected decoded table/source version is missing rows for this contract or market class;
- the selected condition may require a source table variant not covered by the C1A-F1 fixed source-table rule.

This would remain a trust diagnostic, not a price-source viability verdict.

### 3.3 Local/Dune tx-hash mismatch issue — plausible, not established

A local/Dune tx-hash mismatch issue is plausible if existing artifacts show that:

- tx-hash normalization or precision handling differs between local and Dune artifacts;
- the local-only rows are not comparable to Dune `tx_hash` values under the full composite identity discipline;
- local rows represent records that cannot map cleanly to decoded `OrderFilled` event rows under the C1A-F1 comparison model.

No Dune query filtered by local tx hashes may be used to test this. That would recreate the blocked local-`tx_hash` scoping trap.

### 3.4 Current conclusion

Until existing artifacts are reviewed, the `OVER_UNDER` result remains unresolved. It should not be called likely selector/window artifact, likely source-table coverage issue, or likely local/Dune tx-hash mismatch without artifact-specific evidence.

---

## 4. Is a second bounded diagnostic justified?

A second Dune canary is **not justified now**.

A no-run F2 artifact review is justified because it tests a different uncertainty than C1A-F1 execution: whether the mixed evidence can be explained from already-persisted artifacts before requesting any new implementation or run. This preserves the falsification discipline and avoids converting one mixed subclass observation into a post-hoc new sample.

The safe F2 shape is therefore:

> **C1A-F2 = no-run / artifact-review-only diagnostic review of the existing C1A-F1 artifacts, focused on classifying the `OVER_UNDER` zero-Dune-row / local-only observation and validating that the F1 artifacts are sufficient, complete, and non-leaky.**

F2 must not be a second Dune run, not a selector run, not a new SQL package, not a C1B sample, and not a price-source test.

---

## 5. Alternatives evaluated

### 5.1 No-run / artifact-review-only — recommended

Recommended.

This is the only shape that directly addresses the remaining uncertainty without adding new source observations. It can inspect whether the existing C1A-F1 artifacts support one of the allowed classifications in §9, or whether the correct conclusion is simply unresolved.

It remains SPEC/document-review work only. It does not touch data, run code, generate SQL, or create price artifacts.

### 5.2 Selector-only F2 — rejected for now

Rejected.

A selector-only F2 would choose new candidates after seeing that `OVER_UNDER` was the mixed subclass. Even if deterministic, it would be driven by the previous result and would not answer whether the existing F1 observation is explainable. It risks becoming a disguised attempt to find a cleaner `OVER_UNDER` condition.

### 5.3 One-condition targeted diagnostic — deferred, not authorized

Deferred.

A one-condition targeted diagnostic could be considered only after no-run artifact review proves that a single, specific, non-result hypothesis cannot be resolved from existing artifacts and that testing it would not require cap changes, window changes, SQL modification, Dune count scouting, local-tx-hash filtering, or outcome-conditioned selection.

Even then, it would require a separate SPEC-only document and separate Orchestrator review before any implementation or run could be considered. It must not be authorized by this F2 spec.

### 5.4 Three-condition subclass-balanced diagnostic — rejected

Rejected.

A second three-condition subclass-balanced canary would substantially repeat F1. It would add another small sample after observing mixed evidence and would drift toward C1B full sampled coverage without satisfying C1B authorization or design requirements.

### 5.5 Reject all F2 — not recommended

Not recommended.

Stopping all F2 work would leave the `OVER_UNDER` mixed evidence unclassified even though existing artifacts may be sufficient to identify a defect, non-result, or unresolved classification. A no-run artifact review is a safer intermediate step than either running again or abandoning the evidence unexamined.

---

## 6. F2 artifact-review-only design

### 6.1 Purpose

C1A-F2 artifact review asks:

> Do the existing C1A-F1 artifacts allow a non-run classification of the `OVER_UNDER` zero-Dune-row / local-only observation, and do they preserve the guardrails required for interpreting C1A-F1 as mixed diagnostic evidence only?

It does not ask whether Option C is viable.

### 6.2 Allowed inputs

F2 may review only already-persisted C1A-F1 artifacts listed in `ARTIFACT_INDEX.md`, including:

- `c1a_f1_windows.json`;
- `c1a_f1_windows.json.provenance.json`;
- `c1a_f1_selector_provenance.json`;
- `c1a_f1_selected_conditions.csv`;
- `c1a_f1_selector_excluded.csv`;
- `c1a_f1_canary_manifest.json`;
- `c1a_f1_dune_query.sql` as historical evidence only, not for editing or rerun;
- `c1a_canary_result.json`;
- `c1a_canary_result.md`;
- `c1a_canary_by_condition.csv`;
- `option_c_c1a_raw_rows_sample.csv`;
- `option_c_c1a_tagged_rows.csv`.

If an expected artifact is missing, incomplete, internally inconsistent, or insufficient to support review, F2 must stop with `C1F2_ARTIFACTS_INSUFFICIENT`.

### 6.3 Forbidden inputs

F2 must not use:

- new local data reads;
- Dune/API/RPC/network calls;
- Dune count scouts;
- regenerated SQL;
- modified SQL;
- local tx-hash Dune filters;
- winner/outcome/resolution winner columns;
- price, PnL, score, forecast, calibration, Brier/log-loss, or probe fields;
- `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis;
- manual web/source checks of tx hashes;
- any unlisted artifact unless a separate doc-only authorization explicitly adds it to the review input set.

### 6.4 Review checks

A future F2 artifact-review memo, if separately requested, should check only the following:

1. **Artifact completeness:** all expected F1 artifacts exist and carry the expected scope/provenance fields.
2. **Manifest integrity:** the `OVER_UNDER` condition has exactly two string-safe side token IDs, fixed window bounds, subclass label, caps, and source-table/version fields.
3. **Selector provenance:** the `OVER_UNDER` condition was selected by the accepted deterministic policy, not by result-aware edits, Dune counts, local-tx-hash filtering, or winner/outcome fields.
4. **Window comparability:** the fixed window recorded for the `OVER_UNDER` condition is internally consistent across windows, manifest, query artifact, canary result, and by-condition ledger.
5. **Token-pair comparability:** token IDs in the selected condition, manifest, query artifact, and tagged rows are string-safe and consistent. If there are no Dune rows, the review may only validate the query-side token pair as recorded; it cannot infer source-side token behavior for missing rows.
6. **Source-table provenance:** the historical query artifact and result metadata name the expected decoded `OrderFilled` source table(s) and do not imply an arbitrary table substitution.
7. **Local-only evidence shape:** the `OVER_UNDER` local-only tx hashes are represented in the by-condition/tagged evidence sufficiently to know that they belong to the fixed condition/window/token-pair comparison. No tx-hash lookup or Dune requery is allowed.
8. **No price leakage:** no artifact includes or consumes price, canonical-side price, winner fields, PnL, score, or probe metrics for the F1 selector or F2 review.
9. **No hidden cap manipulation:** caps remain `per_condition_row_cap <= 2000`, `global_row_cap <= 6000`, with no truncation or changed branch limits.
10. **Interpretation discipline:** the review does not convert a non-halt F1 execution into `C1_CANARY_DESIGN_CLEAR`, a viability verdict, or a P1 unblock.

---

## 7. Avoiding hand-picking, leakage, and scope creep

F2 must preserve these rules:

1. Do not choose a new condition because `OVER_UNDER` returned zero Dune rows.
2. Do not drop, replace, or retry the `OVER_UNDER` condition.
3. Do not expand from one mixed subclass into another subclass-balanced sample.
4. Do not run repeated small canaries until a clean result appears.
5. Do not use C1A-F1 Dune row counts as selector input for any future manifest.
6. Do not use local tx hashes as Dune query filters.
7. Do not perform Dune count scouting.
8. Do not modify windows after observing Dune results.
9. Do not increase caps, truncate rows, or reinterpret capped rows as complete.
10. Do not use winner/outcome/resolution-winner/PnL/score fields.
11. Do not use `yes_price`, `1 - price`, `1 - yes_price`, or side synthesis.
12. Do not build reusable volume-profiling artifacts.
13. Do not scan/profile the full approximately 288K-condition universe.
14. Do not treat this as C1B, C2, P1, P2, P3, or probe preparation.

---

## 8. Stop conditions and rejection criteria

### 8.1 F2 artifact-review stop labels

A future F2 artifact-review memo may use only these diagnostic labels:

- `C1F2_ARTIFACT_REVIEW_NOT_STARTED` — this spec exists but no artifact review has occurred.
- `C1F2_ARTIFACTS_INSUFFICIENT` — required existing artifacts are missing, incomplete, inconsistent, or too thin to classify the `OVER_UNDER` observation.
- `C1F2_F1_ARTIFACT_DEFECT` — existing artifacts show a defect in F1 selection, manifest construction, windowing, provenance, cap handling, or evidence persistence. This invalidates or weakens F1 interpretation; it does not authorize a rerun.
- `C1F2_OVER_UNDER_ZERO_LIKELY_SELECTOR_WINDOW_ARTIFACT` — existing artifacts support this explanation without new data.
- `C1F2_OVER_UNDER_ZERO_LIKELY_SOURCE_COVERAGE_GAP` — existing artifacts support this explanation without new data.
- `C1F2_OVER_UNDER_ZERO_LIKELY_LOCAL_DUNE_IDENTITY_MISMATCH` — existing artifacts support this explanation without new data.
- `C1F2_OVER_UNDER_ZERO_UNRESOLVED` — artifacts are complete enough to review but do not support a more specific explanation.
- `C1F2_REJECT_FURTHER_CANARY` — artifact review indicates that another canary would be unsafe, duplicative, or not useful.
- `C1F2_ONE_CONDITION_DIAGNOSTIC_SPEC_REQUIRED` — artifact review identifies a narrowly testable unresolved hypothesis, but any test requires a separate SPEC-only document before implementation/run can even be discussed.

### 8.2 Rejection criteria

Reject any F2 proposal that:

1. includes implementation, code, tests, commands, SQL generation, SQL modification, local data reads, or any Dune/API/RPC/network call;
2. proposes a Dune run or a local run;
3. changes caps or permits cap increases;
4. truncates rows or treats a capped branch as complete;
5. filters by local tx hashes;
6. performs Dune count scouting;
7. selects conditions from winner/outcome/PnL/score/price/probe fields;
8. uses `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis;
9. chooses a new `OVER_UNDER` condition simply because the prior one returned zero Dune rows;
10. repeats a three-condition subclass-balanced canary;
11. expands to C1B/C2/P1/P2/P3/probe;
12. computes or persists any price artifact;
13. marks Option C viable;
14. marks `C1_CANARY_DESIGN_CLEAR` or `C1F_DESIGN_READABLE_ACCEPTED_BY_REVIEW` automatically;
15. flips `named_binary_probe_blocked`.

---

## 9. Required artifacts before any future implementation/run could be considered

No implementation/run is proposed here. If a future request attempts to move beyond F2 artifact review, the following must exist first:

1. **Accepted F2 artifact-review memo** using only the existing F1 artifacts and one of the labels in §8.1.
2. **Artifact-completeness attestation** confirming the required C1A-F1 artifacts are present, internally consistent, and reviewable.
3. **Explicit classification of the `OVER_UNDER` observation** as likely selector/window artifact, likely source-table coverage gap, likely local/Dune identity mismatch, unresolved, or artifact defect — with artifact references.
4. **Separate SPEC-only document** for any proposed one-condition diagnostic, if and only if F2 review concludes that such a diagnostic is narrowly useful and not a disguised C1B/C2 continuation.
5. **Predeclared condition and hypothesis rule** for any future one-condition diagnostic. It must explain why the condition is diagnostic rather than hand-picked, why using the F1 `OVER_UNDER` condition is legitimate for failure analysis if proposed, and why no new selector search is being performed.
6. **Unchanged caps and boundaries:** `per_condition_row_cap <= 2000`, `global_row_cap <= 6000`, no row truncation, no cap increase, no repeated canary batches.
7. **No SQL generation/modification in the artifact-review step.** Any future query text would require separate authorization and must not be created by this spec.
8. **No downstream authorization language.** Any implementation/run request must explicitly state that it does not authorize C1B/C2/P1/P2/P3/probe/scoring/backfill/wallet/OrdersMatched/`log_index`/PnL/price artifact.

Absent these artifacts and decisions, further F2 execution should be rejected or deferred.

---

## 10. Decision labels after F2 and what they must not imply

Allowed post-F2 labels are listed in §8.1. None of them may imply:

- Option C is viable;
- C1 is design-clear;
- C1B is authorized;
- C2 is authorized;
- P1 is unblocked;
- P2/P3/probe is authorized;
- a price artifact exists;
- Dune-only tx hashes are price input;
- local-only tx hashes prove source failure without artifact support;
- `named_binary_probe_blocked` may be flipped;
- `yes_price`, `1 - price`, or `1 - yes_price` may be used.

The only acceptable interpretation of a completed F2 artifact review is narrower:

> The existing F1 evidence is either classifiable from artifacts, defective, insufficient, or unresolved. No price-source viability verdict follows.

---

## 11. Could any F2 outcome unblock P1 directly?

No.

No F2 outcome can unblock P1 directly. F2 is coverage/trust diagnostic review only. It does not compute per-side prices, does not validate decision-time coverage across the P0 universe, does not build a price series, and does not create a `canonical_side_price` input.

A future P1 unblock would require a separate accepted price-source spec and accepted evidence that a source provides usable per-side/token-identity decision-time prices under the named-binary contract. F2 cannot substitute for that.

---

## 12. Recommendation

Recommended next decision:

> **Proceed with F2 only as no-run / artifact-review-only. Defer any implementation or run pending that artifact review. Reject selector-only, one-condition run, three-condition canary, SQL generation/modification, and any downstream continuation at this stage.**

This preserves the useful part of C1A-F1 — reviewable mixed diagnostic evidence — without turning a single mixed subclass observation into post-hoc sampling or cap-evasion.

---

## 13. Guardrails preserved

Research only. This SPEC authorizes no implementation, no code, no tests, no SQL generation or modification, no Dune/API/RPC/network call, no Dune run, no local data run, no C1B, no C2, no P1/P2/P3, no probe execution, no scoring, no backfill, no wallet discovery, no OrdersMatched expansion, no `log_index`, no PnL, no cap increase, no row truncation, no local-tx-hash Dune filtering, no Dune count scouting, no winner/outcome/PnL/score fields, no price artifact, and no side synthesis.

`named_binary_probe_blocked` remains `true`. P1 remains blocked. Option C remains diagnostic-only and is not marked viable.
