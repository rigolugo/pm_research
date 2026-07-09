# ARTIFACT INDEX

*What exists and where. Paths are in the local repo `C:/b1/pm_research` unless noted.*

---

## Artifacts (`artifacts/`)

Recommended subfolder organization (currently flat — reorganize when convenient):

### `artifacts/rank1a/`

- `forecast_vs_price_rank1a.json` + `.md` report + `_splits.csv` + `_conditions.csv` — Rank 1A probe (NEGATIVE).
- `rank1a_price_bucket_diagnostic.json` + `.md` + `.csv` — NO_ACTIONABLE_BUCKET.

### `artifacts/audits/`

- `probe_fast_gate.*` — data gate result CLEAR_WITH_WARNINGS_FOR_RANK1A.
- (audit_market_structure outputs, if retained.)

### `artifacts/rank2_ordersmatched/`

- `ordersmatched_economic_role_expanded.json` + `.md` + `.csv` — Rank 2 final distribution (117 trades, 96 wallets, 71T/46M).
- `ordersmatched_maker_pairing_validation.json` + `.md` + `.csv` — MAKER_PAIRING_VALIDATED.
- `ordersmatched_economic_role.{json,md,csv}` — the pre-expansion probe.
- `ordersmatched_expanded_dune_query.sql` (varchar-cast, 150-tx) and `ordersmatched_expanded_dune_tx_list.txt`.
- `orderfilled_operator_filtered_semantic.*` — event-role recovery + operator filter.
- `orderfilled_fee_role_diagnostic.*` — fee diagnostic (SUPERSEDED, preserved).

### `artifacts/named_binary/`

- `named_binary_audit_gate.json` + `.md` — default/local-only named-binary semantics audit gate: legacy pooled-all gate BLOCKED_BY_RESOLUTION_MAPPING; schema_chosen=label; YES/NO resolves 8,521/8,521 where local resolution rows exist; non-YES/NO unresolved locally. When run with `--resolution-source`, the same gate artifact also includes Stage 4 non-YES/NO branch fields.
- `named_binary_resolution_mapping_coverage.csv` — per-subclass coverage table. In the local-only audit it reports eligible / with-resolution / winner-maps / rate; after Stage 3/4 it extends this with source_rows, resolved_single_winner, conflicts-by-type, exact_winner_rate, and coverage_rate.
- `named_binary_classification_contract.json` + `.md` — per-condition subclass + eligibility; carries `nb_contract_version` (`nb-contract-2026-06-28.1`). **Chat2 consumes this and asserts version equality.**
- `named_binary_semantics_report.md` — narrative summary.
- `named_binary_label_pair_census.csv` — frequency-ranked label-pair census.
- `named_binary_resolution_source_rows.parquet` — Stage 3 normalized winners (condition_id, subclass, resolved_winning_token_id/outcome_index/label, resolved_at, source_table, status, nb_contract_version); string-safe token fields; RESOLVED_SINGLE_WINNER rows only.
- `named_binary_resolution_conflicts.csv` — Stage 3 excluded conflicts with status + payout vector.
- `named_binary_resolutions_source_audit.json` + `.md` — Stage 3 build audit.

### `artifacts/named_binary_probe/`

- `p0_preflight.json` — Stage P0 preflight result (machine-readable): `p0_state` (P0_CLEAR), `authorized_scope` (P0_PREFLIGHT_ONLY), `probe_execution_authorized` (false), `named_binary_probe_blocked_observed` (true), contract/resolution-source versions, `gate_snapshot`, `counts_pooled`, `counts_by_subclass`, `excluded_counts`, `reconciliation`, notes. Accepted real-data figures: contract_eligible 39,957 / resolved_single_winner 39,693 / ambiguous_multiple_winners 253 / source_rows 39,946 / missing_source_rows 11 / final_p0_eligible 39,693.
- `p0_preflight.md` — Stage P0 narrative report.
- `p0_excluded_counts.csv` — per-subclass tally.
- `price_input_s0_inspection.txt` — read-only S0 price-input inspection evidence. Records price provenance, the YES/NO-only / named-binary-unsafe meaning of `yes_price`, the absence of any local per-side/per-token price artifact, and a non-YES/NO price sample.

### `artifacts/named_binary_probe/price_source_option_d_temporal_inrange/`

Option D temporal in-range precheck artifacts (user-run, ACCEPTED; result `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`). Local-only/read-only timing-feasibility artifacts only — **no vendor data and no price series is persisted**.

Accepted result:
- status `COMPLETED`; `halt_code = null`
- exact P0 reconciliation: expected 39,693 / observed 39,693; UP_DOWN 22,012; OVER_UNDER 1,003; NAMED_OTHER 16,678
- no missing first-trade anchors; no missing `resolved_at`
- PMXT v2 pooled temporal coverage: 18,137 / 39,693 = 0.456932
- Telonex L2 pooled temporal coverage: 37,749 / 39,693 = 0.951024
- Telonex L2 by subclass: UP_DOWN 0.974696; OVER_UNDER 0.979063; NAMED_OTHER 0.918096
- PMXT v2 is closed/deprioritized for broad full-P0 Option D coverage on timing grounds
- Telonex L2 is plausible only for a later separately authorized SPEC ONLY vendor-coverage review
- no vendor fetch, account/API key/paid action, price computation, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis follows; `named_binary_probe_blocked` remains true

Artifact set:
- `option_d_temporal_inrange_precheck.json` — machine-readable temporal in-range result and self-attestation.
- `option_d_temporal_inrange_precheck.md` — narrative temporal in-range result report.

### `artifacts/named_binary_probe/price_source_s1/`

S1 Pass 1 **coverage-only** artifacts (user-run, ACCEPTED; verdict `S1_SOURCE_NOT_VIABLE`). Coverage diagnostics only — **no price series is persisted**.

- `price_source_s1_coverage.json` — machine-readable Pass-1 result.
- `price_source_s1_coverage.md` — narrative summary.
- `price_source_s1_coverage_by_condition.csv` — per-condition coverage ledger. **No price values.**
- `price_source_s1_excluded.csv` — excluded conditions with reasons.
- `price_source_s1_endpoint_shape.md` — documented-vs-observed endpoint shape.

### `artifacts/named_binary_probe/price_source_s1_alt/`

S1-ALT Pass 1 (Option A local trade-print) **coverage-only** artifacts (user-run, ACCEPTED; verdict `S1ALT_SOURCE_NOT_VIABLE`). Local-only; reuses the exact accepted S1 Pass-1 300-condition sample. Coverage diagnostics only — **no price series is persisted**.

- `price_source_s1_alt_coverage.json` — machine-readable Pass-1 result.
- `price_source_s1_alt_coverage.md` — narrative summary.
- `price_source_s1_alt_coverage_by_condition.csv` — per-condition coverage ledger. **No price values.**
- `price_source_s1_alt_excluded.csv` — excluded conditions with reasons.
- `price_source_s1_alt_source_shape.md` — observed local `Store.load_trades()` column shape.

### `artifacts/named_binary_probe/price_source_option_b_b0/`

B0 Data API `/trades` mechanical-trust pilot artifacts. Historical state: the original B0 run halted at `STOP_API_LOCAL_MISMATCH`, then local-only artifact inspection halted at `STOP_API_ARTIFACT_MISSING` because only `option_b_b0_manifest.json` had been persisted. This defect motivated the corrected B0 diagnostic harness.

- `option_b_b0_manifest.json` — fixed 10-condition B0 manifest; this was the only confirmed persisted B0 file from the original local artifact inspection.

### `artifacts/named_binary_probe/price_source_option_b_b0_diag/`

Corrected Option B B0 diagnostic artifacts (user-run, ACCEPTED; result `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`). Diagnostic/trust artifacts only — **no price series is persisted**.

Accepted result:

- `artifact_status = API_ARTIFACT_COMPLETE`
- `halt_code = null`
- `manifest_conditions = 10`
- `api_rows_primary = 13,009`
- `api_rows_total_all_query_modes = 17,853`
- `local_rows = 1,346`
- `mismatches = 14,355`
- classifications: `OVERLAP_API_LOCAL_MISMATCH = 7`, `OVERLAP_PAGINATION_PARTIAL = 3`, `OVERLAP_MATCHED = 0`, `NO_TEMPORAL_OVERLAP = 0`
- mismatches: `API_ONLY = 11,829`, `LOCAL_ONLY = 145`, `TX_HASH_AMBIGUOUS = 2,381`
- pagination: `COMPLETE_SHORT_FINAL_PAGE = 7`, `PARTIAL_RETRIEVAL = 3`

Expected artifact set:

- `manifest_attested.json` — fixed 10-condition manifest copy plus run constants/provenance.
- `api_rows.csv` — bounded normalized API row ledger.
- `api_raw_pages.jsonl` — bounded raw page evidence with metadata.
- `api_raw_rows.jsonl` — bounded raw row evidence preserving original row payloads/string forms.
- `local_rows.csv` — local comparison rows as consumed by the reconciler.
- `mismatches.csv` — full mismatch ledger (`API_ONLY`, `LOCAL_ONLY`, `TX_HASH_AMBIGUOUS`).
- `by_condition.csv` — per-condition pagination, temporal bounds, and overlap classifications.
- `schema_errors.csv` — schema/precision deviation ledger, if any.
- `local_load_provenance.json` — local load provenance.
- `reconciliation.json` — run summary and artifact-completeness self-attestation.
- `offline_recompute_summary.json` — offline recompute summary.
- `summary.md` — narrative report.

Decision impact: corrected B0 did **not** establish Data API `/trades` mechanical trust. B1 remains not authorized. Option B must not proceed to B1/full Pass 1/S2/P1/P2/P3/probe. P1 remains blocked on the absence of an accepted per-side/token-identity price source. `named_binary_probe_blocked` stays `true`.

Metadata caveat: `reconciliation.json` reports `takeronly_probe_conditions = 3`, while `offline_recompute_summary.json` reports `takeronly_probe_conditions = 10`. Core `artifact_status`, `halt_code`, counts, `mismatch_counts`, `pagination_counts`, and `classification_counts` match. This is a metadata/recompute inconsistency only and does not change the B0 negative finding.

### `artifacts/named_binary_probe/price_source_option_c_c1a/`

C1A selector manifest + bounded canary artifacts (user-run, ACCEPTED VALID HALT; result `C1_ROW_EXPLOSION`). Coverage/trust diagnostics only — **no price series is persisted**.

Accepted result:

- manifest `resolved_count = 5`, `excluded_count = 0`
- canary outcome `C1_ROW_EXPLOSION`
- halt detail: condition `0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e` returned 2001 rows, exceeding `per_condition_row_cap = 2000`
- cap behavior: generated SQL intentionally uses `LIMIT per_condition_row_cap + 1` so cap exceedance is detected rather than silently truncated
- diagnostic counts: `0x00e0...fc8e` — 2001 Dune rows, 794 Dune-only tx hashes, 136 local-only, 24 overlap, 0 unresolved side rows; `0x0cb2...61c2` — 705 Dune rows, 248 Dune-only, 0 local-only, 44 overlap, 0 unresolved side rows; three other candidates returned 0 Dune rows and local-only tx hashes

Artifact set:

- `c1a_selector_manifest.json` — fixed 5-condition selector manifest; full string-safe side-token identities; no outcome-conditioned selector source.
- `c1a_selector_manifest.csv` — CSV form of the selector manifest.
- `c1a_dune_query.sql` — generated decoded-OrderFilled query; uses fixed windows/tokens and cap+1 over-fetch; historical artifact only, not authorization for another Dune run.
- `c1a_canary_result.json` — machine-readable canary result with halt code and counts.
- `c1a_canary_result.md` — narrative canary result report.
- `c1a_canary_by_condition.csv` — per-condition canary ledger.
- `option_c_c1a_raw_rows_sample.csv` — raw-row evidence sample.
- `option_c_c1a_tagged_rows.csv` — tagged event rows including token-side match and tx-hash relation diagnostics.

Decision impact: C1A halted validly on row explosion. This is not a price-source viability verdict and does not unblock P1. C1B/C2/P1/P2/P3/probe remain unauthorized. `named_binary_probe_blocked` stays `true`.

Parser-fix note: the C1A user-run exposed two local parser issues that were patched before result acceptance — manifest timestamp parsing needed datetime-like / pandas `Timestamp` support; canary parsing needed Dune timestamp strings (`YYYY-MM-DD HH:MM:SS.fff UTC`) and UTF-8 BOM-tolerant CSV header handling. These were local parser fixes only, not evidence of source viability.

Follow-up spec note: `SPEC_price_source_option_c_c1a_followup.md` is ACCEPTED / SPEC ONLY. It accepts the C1A-F1 selector-policy shape in principle after the accepted C1A `C1_ROW_EXPLOSION` halt. It does not add artifacts to this folder and does not authorize implementation, tests, SQL/query generation, a Dune/API/RPC/network run, a bounded user-run, cap increases, row truncation, C1B/C2/P1/P2/P3/probe, scoring/backfill/wallet/`log_index`/PnL, a price artifact, or side synthesis.

### `artifacts/named_binary_probe/price_source_option_c_c1a_f1/`

C1A-F1 selector + bounded canary artifacts (selector/prep accepted; user-run executed and ACCEPTED as reviewable mixed evidence; result `C1_CANARY_EXECUTED_NEEDS_REVIEW`). Coverage/trust diagnostics only — **no price series is persisted**.

Accepted selector/prep context:

- selector universe was bounded to the accepted small S1/S1-ALT eligible / C1A-compatible measured pool; no full ~288K universe scan/profile and no reusable volume-profiling artifact.
- selected conditions = 3, one per subclass: `OVER_UNDER`, `NAMED_OTHER`, `UP_DOWN`.
- cap constants preserved: `per_condition_row_cap = 2000`, per-condition Dune query `LIMIT = 2001` (`cap+1` over-fetch), `global_row_cap = 6000`.
- generated SQL used decoded `OrderFilled` tables only, fixed token pairs/windows, subquery-wrapped branch limits, and no local `tx_hash` filter.
- selector/prep artifacts authorize no run by themselves.

Accepted C1A-F1 post-run result:

- canary outcome `C1_CANARY_EXECUTED_NEEDS_REVIEW`
- total Dune rows in fixed windows = 133
- no row explosion
- no unresolved side rows
- Dune-only tx hashes found = 34 total
- `NAMED_OTHER`: 104 Dune rows, 27 Dune-only tx hashes, 2 overlap tx hashes, 0 local-only tx hashes, 0 unresolved side rows
- `UP_DOWN`: 29 Dune rows, 7 Dune-only tx hashes, 4 overlap tx hashes, 0 local-only tx hashes, 0 unresolved side rows
- `OVER_UNDER`: 0 Dune rows, 0 Dune-only tx hashes, 0 overlap tx hashes, 2 local-only tx hashes, 0 unresolved side rows
- no price was computed or persisted
- this is **not** `C1_CANARY_DESIGN_CLEAR`

Artifact set:

- `c1a_f1_windows.json` — deterministic windows input derived from bounded local/static inputs.
- `c1a_f1_windows.json.provenance.json` — windows provenance; records local-trades bounded-pool source, no Dune/API/RPC/network, no SQL, no price artifact, no full-universe scan.
- `c1a_f1_selector_provenance.json` — selector provenance; records selected/rejected conditions, density source, caps, guardrail fields, and no Dune count scout / no local-tx-hash filter / no winner/outcome/price/score/PnL fields.
- `c1a_f1_selected_conditions.csv` — accepted selected 3-condition manifest source with side token identities and selector diagnostics.
- `c1a_f1_selector_excluded.csv` — selector exclusions.
- `c1a_f1_canary_manifest.json` — JSON manifest consumed by `scripts/price_source_option_c_c1a_canary.py`, with `conditions[]`, side token IDs, windows, and caps.
- `c1a_f1_dune_query.sql` — prepared decoded-OrderFilled SQL text; historical artifact only and not authorization to execute or rerun.
- `c1a_f1_dune_export.csv` — raw Dune export used by the accepted C1A-F1 bounded canary; historical evidence only, not authorization to rerun, modify SQL, or use as price input.
- `c1a_canary_result.json` — machine-readable C1A-F1 canary result.
- `c1a_canary_result.md` — narrative C1A-F1 canary result report.
- `c1a_canary_by_condition.csv` — per-condition C1A-F1 canary ledger.
- `option_c_c1a_raw_rows_sample.csv` — bounded raw-row evidence as ingested from the user-provided Dune CSV export.
- `option_c_c1a_tagged_rows.csv` — tagged rows with raw token-side match and tx-hash relation diagnostics.

Decision impact: C1A-F1 is accepted as executed and reviewable mixed coverage/trust evidence. It does **not** mark Option C viable, does **not** mark C1 design-clear, does **not** unblock P1, and does **not** authorize C1B/C2/P1/P2/P3/probe/scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, cap increases, truncation, additional canaries, or any price artifact. `named_binary_probe_blocked` stays `true`.

C1A-F2 artifact review impact: `project_context/HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md` is accepted with result `C1F2_ARTIFACTS_INSUFFICIENT`. The C1A-F1 artifacts confirm the mixed summary and safe selector/query/cap discipline, but the `OVER_UNDER` local-only evidence is too thin for safe causal classification: the two local-only rows lack local-side timestamp/token/outcome_index/side-match/row-identity/window-membership fields. No likely-cause label is accepted; no one-condition diagnostic is recommended. This does not mark Option C viable, does not mark C1 design-clear, does not unblock P1, and does not authorize any downstream work.

---

## Scripts (`scripts/`)

### Rank 1A

- `forecast_vs_price.py` — pooled YES/NO forecast-vs-price probe.
- `rank1a_price_bucket_diagnostic.py` — price-bucket segmentation diagnostic.

### Audit / gate

- `audit_market_structure.py` — streaming market-structure audit.
- `probe_fast_gate.py` — overlap/concentration data gate.

### Rank 2 (OrdersMatched / OrderFilled)

- `orderfilled_sample_join.py` — validated decoder (topic2=maker, topic3=taker; canonical-int helpers live here / in the OrdersMatched module).
- `ordersmatched_economic_role.py` — economic-role probe (taker via takerordermaker; maker via pairing). Contains `canonical_int`, `DataExportPrecisionLoss`, varchar Dune query template.
- `ordersmatched_economic_role_expanded.py` — stratified 150-tx expansion + per-wallet/contract/time/fill breakdowns.
- `ordersmatched_maker_pairing_validation.py` — known-maker-case validation harness.

### Named-binary semantics

- `audit_named_binary_semantics.py` — orchestration entry point; streams sharded trades, runs mapping/classification/resolution/orientation/gate, writes named-binary artifacts. Stage 4 optional `--resolution-source <rows.parquet>` overlays Stage 3 winners onto non-YES/NO subclasses. CLEAR_WITH_WARNINGS means the outcome source/audit is usable and never authorizes a probe (`named_binary_probe_blocked` stays True).
- `named_binary_label_census.py` — frequency-ranked label-pair census feeding the lexicon.
- `diag_resolution_mapping.py`, `diag_resolution_coverage.py`, `diag_named_binary_resolvable.py` — read-only diagnostics that isolated the YES/NO-only resolutions finding.
- `inspect_named_binary_resolution_dune_schema.py` — Stage 0 read-only Dune schema inspection.
- `export_contract_for_dune.py` — exports the classification contract to a Dune-upload CSV.
- `build_named_binary_resolution_source.py` — Stage 3 bulk builder.

### Named-binary probe (Stage P0 only)

- `named_binary_probe_p0_preflight.py` — Stage P0 preflight (ACCEPTED, P0_CLEAR). Read-only except for its three `artifacts/named_binary_probe/` outputs. Counts only; no trades/prices, no decision timestamps, no canonical_side_price, no scoring, no Dune/network, no log_index, no wallet logic.

### Named-binary probe (price-source diagnostics — coverage/trust only, user-run when explicitly authorized)

- `price_source_s1_coverage.py` — S1 Pass 1 CLOB `/prices-history` coverage test (ACCEPTED run; verdict `S1_SOURCE_NOT_VIABLE`). Coverage-only: no `yes_price` / `1 - yes_price` / `1 - price` / `1 - p` synthesis; no writes to `prices/`; no scoring/backfill; `named_binary_probe_blocked` never flipped.
- `price_source_s1_alt_pass1_coverage.py` — S1-ALT Pass 1 local trade-print coverage test (ACCEPTED run; verdict `S1ALT_SOURCE_NOT_VIABLE`). Local-only; reuses accepted S1 sample; no price series persisted.
- `price_source_option_b_b0_failure_diagnostic.py` — corrected Option B B0 diagnostic harness. It was code/test authorized separately, then user-run; accepted result `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`. Diagnostic/trust artifacts only; no price series, no B1/full Pass 1/S2/P1/P2/P3/probe authorization, no gate change.
- `price_source_option_c_c1a_f1_selector.py` — C1A-F1 selector helper; local-only selector/windows preparation over the bounded accepted pool. Historical after accepted selector artifacts; no Dune/API/RPC/network, no SQL execution, no price artifact, no full-universe profiling.
- `price_source_option_c_c1a_f1_prepare_canary.py` — C1A-F1 prep-only SQL/manifest generator from accepted selected conditions and windows. Historical after accepted C1A-F1 prep; no Dune/API/RPC/network path and no SQL execution.
- `price_source_option_d_temporal_inrange_precheck.py` — Option D local-only/read-only temporal in-range precheck. User-run completed and accepted with result `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`; timing-feasibility only, no vendor data, no price series, no P1/probe/scoring/gate authorization.

### Named-binary probe (read-only inspection scripts — no code/gate/probe changes)

- `inspect_named_binary_probe_data_contracts.py` — read-only inspector for exact schemas/API surfaces.
- `inspect_oriented_price_formula.py` — read-only inspector for price/orientation callables.

---

## Tests (`tests/`)

- `test_forecast_vs_price.py`, `test_orderfilled_sample_join.py`, `test_ordersmatched_economic_role.py`, plus existing store/audit/backfill suites.
- `test_named_binary_semantics.py` — named-binary suite.
- `test_named_binary_resolution_source.py` — Stage 2 suite.
- `test_build_named_binary_resolution_source.py` — Stage 3 builder suite.
- `test_named_binary_stage4_gate.py` — Stage 4 suite.
- `test_named_binary_probe_p0_preflight.py` — Stage P0 preflight suite.
- `test_price_source_s1_coverage.py` — S1 Pass 1 coverage suite.
- `test_price_source_option_b_b0_failure_diagnostic.py` — corrected Option B B0 diagnostic harness suite; covers artifact persistence, offline recompute, cap enforcement, Windows-safe writing, schema-blocked classification, and takerOnly incompleteness behavior.
- `test_price_source_option_c_c1a_f1_selector.py` — C1A-F1 selector helper suite; local-only guardrails for bounded selector/windows generation.
- `test_price_source_option_c_c1a_f1_canary_prep.py` — C1A-F1 prep suite; verifies exact accepted 3-condition set, caps, manifest/SQL consistency, no local-tx-hash filter, no forbidden winner/outcome/PnL/score fields, and no network/SQL execution path.
- `test_price_source_option_d_temporal_inrange_precheck.py` — Option D temporal in-range precheck fixture suite; local fixture tests accepted with 53 passed.

---

## Core package (`pm_research/`)

- `data/store.py` — flat parquet store; `load_trades` applies hygiene (drop null condition_id, key-preferring dedup); `load_prices`, `load_resolutions`, `load_markets`.
- `data/schemas.py` — TRADES_COLS (11; no log_index), PRICES_COLS `[condition_id, ts, yes_price]`, RESOLUTIONS_COLS `[condition_id, winning_outcome, resolved_at]`, MARKETS_COLS.
- `semantics/` — named-binary semantics layer: `lexicon.py`, `mapping_audit.py`, `resolution_schema.py`, `resolution_source.py`, `named_binary.py`, `__init__.py`.
- `splits.py` — `rolling_train_test_splits`.
- `calibration.py` — `IsotonicCalibrator`.

---

## Specs & handoffs (repo root or specs folder)

- `SPEC_named_binary_resolution_source.md` — spec for sourcing non-YES/NO realized outcomes from Dune; IMPLEMENTED + ACCEPTED across Stages 0–4.
- `PLAN_named_binary_resolution_source_implementation.md` — staged implementation plan (Stages 0–4).
- `HANDOFF_orchestrator_named_binary_taskAB.md` — orchestrator handoff: Issue-A fix + spec, with real-data before/after.
- `FINDINGS_named_binary_resolution_blocker.md` — dated finding: YES/NO-only resolutions block the named-binary probe (superseded by the Dune source).
- Stage 0 — `SCHEMA_INSPECTION_named_binary_resolution_source.md`.
- Stage 1 — `DUNE_SQL_named_binary_resolution_stage1.sql` + `STAGE1_named_binary_resolution_query_plan.md` + `FINDINGS_stage1_named_binary_resolution_coverage.md`.
- Stage 2 — `HANDOFF_orchestrator_stage2_resolution_source.md`.
- Stage 3 — `HANDOFF_orchestrator_stage3_resolution_builder.md`.
- Stage 4 — `HANDOFF_orchestrator_stage4_gate_integration.md`.
- `REVIEW_nautilus_scavenge_named_binary_resolution.md` — file-based review of the NautilusTrader bundle (engineering shapes only; LGPL — no code copied; not a canonical source).
- `SPEC_named_binary_probe.md` — ACCEPTED spec-only document for a future offline historical non-YES/NO named-binary forecast-vs-price probe. Authorizes no implementation, no data run, and no probe execution.
- `HANDOFF_orchestrator_named_binary_probe_p0.md` — Stage P0 preflight handoff (ACCEPTED, P0_CLEAR).
- `HANDOFF_orchestrator_named_binary_probe_p1_REVIEW.md` — Stage P1 review memo (PAUSED/BLOCKED). Superseded by DATA_CONTRACTS + PRICE_INPUT_CONTRACT; P1 stays blocked.
- `DATA_CONTRACTS_named_binary_probe.md` — ACCEPTED reference contract.
- `PRICE_INPUT_CONTRACT_named_binary_probe.md` — ACCEPTED S0 finding. P1 remains BLOCKED on price input.
- `SPEC_price_source_s1_coverage.md` — ACCEPTED / SPEC ONLY / coverage-only. Authorizes no implementation, no S1 run, no network/data fetch, no backfill, no scoring, no S2, no P1/P2/P3, no probe execution. Forbids `yes_price` / `1 - yes_price` / `1 - p` side-synthesis.
- `HANDOFF_orchestrator_s1_pass1_RESULT.md` — S1 Pass 1 sampled coverage RESULT (ACCEPTED): `S1_SOURCE_NOT_VIABLE`. Pass 1 sampled coverage only; P1 stays blocked.
- `HANDOFF_orchestrator_s1_alt_pass1_RESULT.md` — S1-ALT Pass 1 sampled coverage RESULT (ACCEPTED): `S1ALT_SOURCE_NOT_VIABLE`. Pass 1 sampled coverage only; P1 stays blocked.
- `SPEC_price_source_option_b_data_api_review.md` — ACCEPTED Option B Data API `/trades` spec context; historical after corrected B0 negative.
- `HANDOFF_orchestrator_option_b_spec_s1_1_patch.md` — docs-only Option B wording patch to avoid over-closing all candidate sources.
- `HANDOFF_orchestrator_option_b_b0_RESULT.md` — docs-only handoff recording the original B0 state: halted at `STOP_API_LOCAL_MISMATCH`, then local-only artifact inspection halted at `STOP_API_ARTIFACT_MISSING`; now superseded by the corrected B0 diagnostic result.
- `SPEC_option_b_b0_failure_diagnostic.md` — ACCEPTED / SPEC ONLY. Pessimistic, falsification-minded design for the corrected B0 diagnostic; defined D1–D9 evidence persistence, locked constants (`τ = 120 seconds`, `σ = 24 hours`, primary API row-ledger cap 25,000 rows total), typed classifications, and locked `OVERLAP_MATCHED` clean bar.
- `HANDOFF_orchestrator_option_b_b0_failure_diagnostic.md` — Claude-to-Orchestrator handoff recording the accepted failure-diagnostic spec locks.
- `README_option_b_b0_failure_diagnostic.md` — implementation/run-instructions README for the corrected B0 diagnostic harness. Historical now that corrected B0 has completed; no further B0 run is authorized by this README.
- `HANDOFF_claude_option_b_b0_failure_diagnostic_IMPLEMENTATION.md` — Claude-to-Orchestrator implementation handoff for the corrected B0 diagnostic harness. Code/test handoff only; did not authorize a run by itself.
- `HANDOFF_orchestrator_option_b_b0_corrected_diagnostic_RESULT.md` — docs-only handoff recording the accepted corrected B0 diagnostic result: artifact-complete/no-halt run, but Data API `/trades` mechanical trust not established (`OVERLAP_API_LOCAL_MISMATCH = 7`, `OVERLAP_PAGINATION_PARTIAL = 3`, `OVERLAP_MATCHED = 0`). B1/P1/downstream remain blocked; `named_binary_probe_blocked` remains true.
- `SPEC_price_source_option_c_onchain.md` — ACCEPTED / SPEC ONLY (Revision 3). Third per-side/token-identity price-source candidate review (after Option A/S1-ALT and Option B, both closed negative): bounded decoded Dune/vendor OrderFilled event tables. C0 (candidate/source-interface selection) is accepted, spec-only, no run — this remains current. At Revision 3, C1 (bounded coverage/trust pilot) was guardrail-blocked (local-`tx_hash` scoping likely reproduces S1-ALT and cannot test missing coverage by construction; independent condition/time-window event querying risks indexer-shaped work under "No full indexer"). That pre-C1R block is superseded by the separately accepted C1R addendum below.
- `HANDOFF_orchestrator_option_c_onchain_spec.md` — Claude-to-Orchestrator handoff recording the ACCEPT FINDING for the Option C Revision 3 spec: C0 accepted scope, C1 guardrail block (as it stood at Revision 3), files patched, and confirmation that no state/gate/probe authorization changed.
- `SPEC_price_source_option_c_onchain_C1R_addendum.md` — ACCEPTED / SPEC ONLY. C1R (C1 Revised) design addendum: resolves the Revision-3 C1 guardrail block via fixed selector manifest (outcome-independent, never reads winner/outcome fields), subquery-wrapped SQL with per-condition `cap+1` over-fetch, hard row-cap enforcement (fail-fast), empty-export detection (`C1_SOURCE_EMPTY`), row-level evidence artifacts, and source-table validation against the two decoded OrderFilled tables only. Pure-logic tests: 50 passing. No execution.
- `HANDOFF_orchestrator_option_c_c1r_design_addendum.md` — Claude-to-Orchestrator handoff for C1R design acceptance: how the design resolves the Revision-3 scoping trap, 50 tests passing, no run/execution, all guardrails preserved.
- `README_price_source_option_c_c1a.md` — C1A implementation runbook: manifest builder + bounded canary reconciliation (pure code/test-only, 50 tests, no network). Historical runbook for the now-completed C1A user-run; does not authorize another run by itself. Accepted result: valid `C1_ROW_EXPLOSION` halt. C1B/C2/P1/P2/P3 remain NOT authorized.
- `scripts/price_source_option_c_c1a_manifest.py` — C1A selector manifest builder (local-only, no network). Validates candidates (3–5 conditions, `RESOLVED_SINGLE_WINNER` status, oriented subclasses only), enumerates token pairs (S1 discipline, never reading outcome/winner fields), validates `source_table_version` against a strict regex + two-table allowlist, and renders the Dune SQL query text (subquery-wrapped, `cap+1` over-fetch — never executed by this script). 29 tests, all passing.
- `scripts/price_source_option_c_c1a_canary.py` — C1A bounded canary reconciliation (Dune CSV consumer, local-only, no network). Enforces hard per-condition/global row caps with fail-fast (`C1_ROW_EXPLOSION`), halts on empty export (`C1_SOURCE_EMPTY`), tags rows by raw token match (no interpretation), compares tx_hash coverage against the local store, persists row-level evidence (`option_c_c1a_raw_rows_sample.csv`, `option_c_c1a_tagged_rows.csv`) even on a halt, and reports `C1_CANARY_EXECUTED_NEEDS_REVIEW` on a clean run — never auto-emits `C1_CANARY_DESIGN_CLEAR` (that label is Orchestrator-applied only, after manual review). 21 tests, all passing.
- `tests/test_price_source_option_c_c1a_manifest.py` — C1A manifest builder test suite (29 tests, all passing in a bare Python environment; no pandas/Store dependency exercised).
- `tests/test_price_source_option_c_c1a_canary.py` — C1A canary reconciliation test suite (21 tests, all passing; covers cap+1 explosion, exactly-at-cap non-explosion, global cap+1 explosion, empty-export halt, non-halt `EXECUTED_NEEDS_REVIEW` status, row-level artifact writer including `LOCAL_ONLY` synthetic rows, and invalid/non-allowlisted `source_table_version` rejection).
- `HANDOFF_orchestrator_option_c_c1a_IMPLEMENTATION.md` — Claude-to-Orchestrator handoff for C1A implementation completion: all prior BLOCK rounds closed, 50 tests passing, C1A authorized for user-run only (not Claude execution), next step is user-run per README with results returned to orchestrator for review before any C1B/C2/P1 discussion.
- `HANDOFF_orchestrator_option_c_c1a_timestamp_fix.md` — local parser fix handoff: manifest timestamp parser now accepts datetime-like / pandas `Timestamp` values from `Store.load_trades().traded_at`; parser fix only, no source-viability evidence.
- `HANDOFF_orchestrator_option_c_c1a_canary_parser_fix.md` — local parser fix handoff: canary parser now accepts Dune timestamp strings with `UTC` suffix and tolerates UTF-8 BOM CSV headers; parser fix only, no source-viability evidence.
- `HANDOFF_orchestrator_option_c_c1a_RESULT.md` — Claude-to-Orchestrator handoff recording accepted C1A result: user-run manifest resolved 5/excluded 0 and canary halted validly on `C1_ROW_EXPLOSION`; no C1B/C2/P1/probe authorization follows.
- `SPEC_price_source_option_c_c1a_followup.md` — ACCEPTED / SPEC ONLY. C1A-F1 selector-policy shape accepted in principle after the accepted C1A `C1_ROW_EXPLOSION` halt. It defines a deterministic, outcome-independent, local-density / subclass-balanced selector-policy shape with an explicit default selector pool limited to the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool unless broader local-only computation is separately authorized. It rejects hand-picking, winner/outcome leakage, local-`tx_hash` Dune filtering, Dune count scouting, cap increases, truncation, full-universe scanning/profiling, reusable volume-profiling artifacts, and treating local density as a guaranteed predictor. It authorizes no implementation, no code/tests, no SQL/query generation, no Dune/API/RPC/network run, no bounded user-run, no C1B/C2/P1/P2/P3/probe, no scoring/backfill/wallet/`log_index`/PnL, no price artifact, and no side synthesis.
- `HANDOFF_orchestrator_option_c_c1a_followup_SPEC.md` — Claude-to-Orchestrator handoff for the accepted C1A-F1 follow-up selector-policy SPEC. Documentation-only; records that no code, tests, artifacts, query, implementation, or run are authorized.
- `README_price_source_option_c_c1a_f1_canary_prep.md` — C1A-F1 prep-only runbook. Historical after the C1A-F1 user-run; not authorization for rerun or downstream work.
- `HANDOFF_orchestrator_option_c_c1a_f1_canary_PREP.md` — prep-only handoff for C1A-F1 SQL/manifest package; no execution authorized by the handoff itself.
- `HANDOFF_orchestrator_option_c_c1a_f1_canary_REVIEW.md` — docs-only post-run handoff recording the accepted C1A-F1 mixed evidence result: `C1_CANARY_EXECUTED_NEEDS_REVIEW`, 133 total Dune rows, 34 total Dune-only tx hashes, no row explosion, no unresolved side rows, no price artifact, and no P1/C1B/C2/probe authorization.
- `SPEC_price_source_option_c_c1a_f2_followup.md` — ACCEPTED / SPEC ONLY. C1A-F2 no-run / artifact-review-only follow-up after accepted C1A-F1 mixed evidence. Rejects another canary, selector-only F2, SQL generation/modification, Dune/API/RPC/network calls, local data runs, cap changes, truncation, local-`tx_hash` Dune filtering, Dune count scouting, C1B/C2/P1/P2/P3/probe, scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, price artifacts, gate changes, and side synthesis.
- `HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md` — docs-only handoff accompanying the accepted F2 SPEC; records that F2 may proceed only as no-run / artifact-review-only and authorizes no implementation or run.
- `HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md` — accepted C1A-F2 review-only artifact memo; result `C1F2_ARTIFACTS_INSUFFICIENT` because the `OVER_UNDER` local-only evidence lacks local-side row detail needed for causal classification. No P1 unblock, no Option C viability, no C1 design-clear, no further canary, no price artifact.
- `SPEC_price_source_option_c_artifact_enrichment.md` — ACCEPTED / SPEC ONLY. Defines minimum evidence-capture requirements for any possible future Option C / decoded `OrderFilled` diagnostic so local-only, Dune-only, and overlap rows can be reviewed without rerunning or guessing. Defines required future artifacts (`local_comparison_rows.csv`, `source_orderfilled_rows.csv`, `comparison_tagged_rows.csv`, `comparison_by_condition.csv`, `comparison_reconciliation.json`, `artifact_schema.md`), required columns, reconciliation checks, stop/reject labels, and guardrail flags. Authorizes no implementation, no tests, no local data reads, no Dune/API/RPC/network, no SQL generation/modification/execution, no additional canary, no one-condition diagnostic, no C1B/C2/P1/P2/P3/probe, no scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, no price artifact, no gate change, no cap change, no row truncation, and no side synthesis.
- `HANDOFF_orchestrator_option_c_artifact_enrichment_SPEC.md` — docs-only handoff accompanying the accepted artifact-enrichment SPEC; records `ARTIFACT_ENRICHMENT_SPEC_ONLY` and preserves all standing blocks.
- `SPEC_price_source_option_d_l2_archive.md` — ACCEPTED / SPEC ONLY. Option D L2 order-book vendor archive coverage-feasibility spec for PMXT v2 and Telonex L2 order-book/quote archives. Candidate scope: PMXT v2 only from `2026-04-13T19:00:00Z`; Telonex L2 order-book/quote history from `2025-10-11T00:00:00Z`. PMXT v1 and Telonex on-chain fills are out of scope for L2 book coverage unless separately reviewed. Accepted channel-mismatch guards: `VENDOR_HISTORY_NOT_L2_BOOK_RELEVANT` and `STOP_VENDOR_HISTORY_CHANNEL_MISMATCH`. Authorizes no implementation, tests, local temporal precheck, vendor fetch, account/API/paid action, Pass 1, Pass 2, price artifact, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis. P1 remains blocked; `named_binary_probe_blocked` remains true.
- `SPEC_price_source_option_d_temporal_inrange_precheck.md` — ACCEPTED / SPEC ONLY. Option D local-only/read-only temporal in-range precheck design. The authorized local-only run later completed and is accepted as `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`.
- `README_price_source_option_d_temporal_inrange_precheck.md` — implementation/runbook for the Option D temporal precheck. Historical after accepted local run; does not authorize rerun or downstream work by itself.
- `HANDOFF_orchestrator_option_d_temporal_inrange_precheck_IMPLEMENTATION_PATCH.md` — implementation patch handoff; fixture tests accepted with 53 passed before the user-run.
- `HANDOFF_orchestrator_option_d_temporal_inrange_precheck_RESULT.md` — accepted result handoff: PMXT v2 temporal coverage 0.456932 (closed/deprioritized for broad full-P0 coverage); Telonex L2 temporal coverage 0.951024 pooled but NAMED_OTHER 0.918096, so only a later SPEC ONLY vendor-coverage review is plausible. P1 remains blocked; `named_binary_probe_blocked` remains true.

## Stage 4 audit gate fields (in `named_binary_audit_gate.json` when `--resolution-source` is supplied)

- `gate_state` / `base_gate_state` — legacy pooled-all (stays BLOCKED_BY_RESOLUTION_MAPPING; YES/NO sparsity).
- `gate_policy_note` — describes both the legacy gate and the non-YES/NO branch without contradiction.
- `stage4_nonyesno_branch` — `non_yesno_gate_state` (CLEAR_WITH_WARNINGS), `non_yesno_scoreable`, `non_yesno_pooled_map_rate` (0.99339), `pooled_threshold` 0.99, `subclass_threshold` 0.95, `per_subclass_map_rate`, `per_subclass_scoreable`, and `per_subclass_breakdown`.
- `non_yesno_scoreable_from_source`, `source_winner_count` (39,693), `source_conflict_counts`, `per_subclass_source_coverage`.
- `named_binary_probe_blocked` — always true; CLEAR_WITH_WARNINGS does NOT authorize a probe.

---

## Pinned context (this folder, `project_context/`)

Pin all of the following in the Claude Project Files panel (read `START_HERE.md` first):

- `START_HERE.md` — onboarding + required read order + current branch state + "old chats are not source of truth" rule.
- `PROJECT_STATE.md` — current objective / active / blocked.
- `GUARDRAILS.md` — hard constraints.
- `DECISION_LOG.md` — corrected history / settled decisions.
- `CLOSED_FINDINGS.md` — settled negative/complete results.
- `ARTIFACT_INDEX.md` (this file) — what exists and where.
- `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md` — manual canonical-doc update workflow; ChatGPT prepares full replacement files, user uploads manually, Claude does not edit canonical repo files.
- `DATA_CONTRACTS_named_binary_probe.md` — exact inspected schemas/API surfaces for the probe.
- `PRICE_INPUT_CONTRACT_named_binary_probe.md` — accepted S0 price-input finding (why P1 is blocked).
- `CLAUDE_PROJECT_SETTINGS.md` — operational Claude capability settings; does not override the above and authorizes nothing.
- Active specs/handoffs as applicable — `SPEC_named_binary_probe.md`, `SPEC_price_source_s1_coverage.md`, `SPEC_price_source_alt_trade_prints.md`, `SPEC_price_source_option_b_data_api_review.md`, `SPEC_option_b_b0_failure_diagnostic.md`, `SPEC_price_source_option_c_onchain.md`, `SPEC_price_source_option_c_onchain_C1R_addendum.md`, `README_price_source_option_c_c1a.md`, `SPEC_price_source_option_c_c1a_followup.md`, `README_price_source_option_c_c1a_f1_canary_prep.md`, `SPEC_price_source_option_c_c1a_f2_followup.md`, `SPEC_price_source_option_c_artifact_enrichment.md`, `SPEC_price_source_option_d_l2_archive.md`, `SPEC_price_source_option_d_temporal_inrange_precheck.md`, `HANDOFF_orchestrator_named_binary_probe_p0.md`, `HANDOFF_orchestrator_named_binary_probe_p1_REVIEW.md`, `HANDOFF_orchestrator_option_b_spec_s1_1_patch.md`, `HANDOFF_orchestrator_option_b_b0_RESULT.md`, `HANDOFF_orchestrator_option_b_b0_failure_diagnostic.md`, `HANDOFF_orchestrator_option_b_b0_corrected_diagnostic_RESULT.md`, `HANDOFF_orchestrator_option_c_onchain_spec.md`, `HANDOFF_orchestrator_option_c_c1r_design_addendum.md`, `HANDOFF_orchestrator_option_c_c1a_IMPLEMENTATION.md`, `HANDOFF_orchestrator_option_c_c1a_RESULT.md`, `HANDOFF_orchestrator_option_c_c1a_followup_SPEC.md`, `HANDOFF_orchestrator_option_c_c1a_f1_canary_PREP.md`, `HANDOFF_orchestrator_option_c_c1a_f1_canary_REVIEW.md`, `HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`, `HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md`, `HANDOFF_orchestrator_option_c_artifact_enrichment_SPEC.md`.
- `ORCHESTRATOR_LOW_CONTEXT_MODE.md` — reusable low-context review/decision protocol. Documentation only; overrides nothing and authorizes nothing.
- Supporting reference (not overriding): `DUNE_DATA_NOTES.md`.

Keep these version-controlled in the repo AND pinned in the Claude Project Files panel; re-upload when changed so the two stay in sync.
