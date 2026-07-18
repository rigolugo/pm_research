# ARTIFACT INDEX

*What exists and where. Local paths are relative to `C:/b1/pm_research` unless
otherwise stated.*

---

## Core research artifacts

### `artifacts/named_binary/`

- `named_binary_audit_gate.json` and `.md`
- `named_binary_resolution_mapping_coverage.csv`
- `named_binary_classification_contract.json` and `.md`
- `named_binary_semantics_report.md`
- `named_binary_label_pair_census.csv`
- `named_binary_resolution_source_rows.parquet`
- `named_binary_resolution_conflicts.csv`
- `named_binary_resolutions_source_audit.json` and `.md`

Stage 4 retains the legacy pooled-all
`BLOCKED_BY_RESOLUTION_MAPPING` state and the separate non-YES/NO
`CLEAR_WITH_WARNINGS` branch. `named_binary_probe_blocked` remains true.

### `artifacts/named_binary_probe/`

- `p0_preflight.json`
- `p0_preflight.md`
- `p0_excluded_counts.csv`
- `price_input_s0_inspection.txt`

Accepted P0 figures:

- contract eligible: `39,957`
- resolved single winner: `39,693`
- ambiguous multiple winners: `253`
- source rows: `39,946`
- missing source rows: `11`
- final P0 eligible: `39,693`

### `artifacts/named_binary_probe/p0_representativeness_quality/`

- `p0_representativeness_quality_audit.json`
- `p0_representativeness_quality_audit.md`
- `p0_representativeness_by_condition.csv`

Accepted result:
`P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`.

### `artifacts/named_binary_probe/price_source_s1/`

Accepted coverage-only result: `S1_SOURCE_NOT_VIABLE`.

- `price_source_s1_coverage.json`
- `price_source_s1_coverage.md`
- `price_source_s1_coverage_by_condition.csv`
- `price_source_s1_excluded.csv`
- `price_source_s1_endpoint_shape.md`

No price series is persisted.

### `artifacts/named_binary_probe/price_source_s1_alt/`

Accepted coverage-only result: `S1ALT_SOURCE_NOT_VIABLE`.

- `price_source_s1_alt_coverage.json`
- `price_source_s1_alt_coverage.md`
- `price_source_s1_alt_coverage_by_condition.csv`
- `price_source_s1_alt_excluded.csv`
- `price_source_s1_alt_source_shape.md`

No price series is persisted.

### `artifacts/named_binary_probe/price_source_option_b_b0_diag/`

Accepted result: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.

Expected persisted diagnostic set includes:

- `manifest_attested.json`
- `api_rows.csv`
- `api_raw_pages.jsonl`
- `api_raw_rows.jsonl`
- `local_rows.csv`
- `mismatches.csv`
- `by_condition.csv`
- `schema_errors.csv`
- `local_load_provenance.json`
- `reconciliation.json`
- `offline_recompute_summary.json`
- `summary.md`

No price series is persisted. B1 remains unauthorized.

### `artifacts/named_binary_probe/price_source_option_c_c1a/`

Accepted valid halt: `C1_ROW_EXPLOSION`.

Contains selector manifest, bounded SQL, result summaries, condition ledger, raw
sample, and tagged rows. Historical evidence only.

### `artifacts/named_binary_probe/price_source_option_c_c1a_f1/`

Accepted mixed diagnostic result:
`C1_CANARY_EXECUTED_NEEDS_REVIEW`.

Contains windows, selector provenance, selected/excluded conditions, canary
manifest, bounded SQL, Dune export, result summaries, condition ledger, raw
sample, and tagged rows.

C1A-F2 review result: `C1F2_ARTIFACTS_INSUFFICIENT`.

### `artifacts/named_binary_probe/price_source_option_d_temporal_inrange/`

Accepted result:
`OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`.

- `option_d_temporal_inrange_precheck.json`
- `option_d_temporal_inrange_precheck.md`

Timing feasibility only; no vendor data or price series.

---

## Scripts and tests

Relevant scripts include:

- `scripts/audit_named_binary_semantics.py`
- `scripts/build_named_binary_resolution_source.py`
- `scripts/named_binary_probe_p0_preflight.py`
- `scripts/p0_representativeness_quality_audit.py`
- `scripts/price_source_s1_coverage.py`
- `scripts/price_source_s1_alt_pass1_coverage.py`
- `scripts/price_source_option_b_b0_failure_diagnostic.py`
- `scripts/price_source_option_c_c1a_manifest.py`
- `scripts/price_source_option_c_c1a_canary.py`
- `scripts/price_source_option_c_c1a_f1_selector.py`
- `scripts/price_source_option_c_c1a_f1_prepare_canary.py`
- `scripts/price_source_option_d_temporal_inrange_precheck.py`

Relevant tests remain historical evidence of authorized stages. No current test
execution is authorized.

---

## Revision 23 Finding 4 canonical handoff

Canonical directory:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

Finding 4 installation commit:

`e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Installation commits:

- `3f8cc54dc12a5335472f00f5ffcf5c0d56d8d1ba`
- `c394b9ab5eb5dc07f8d716818e02507994ce41d7`
- `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

### Controlling handoff files

- `README_FIRST.md`
- `SENTINEL_ACCEPTANCE_DECISION.md`
- `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
- `HANDOFF_INVENTORY.md`
- `HANDOFF_SHA256SUMS.txt`
- `CANONICAL_REPOSITORY_POINTER.md`
- `prompts/CLAUDE_NEW_CHAT_PROMPT.md`
- `prompts/SENTINEL_NEW_CHAT_PROMPT.md`

Current implementation scope:
`DEFER — NOT AUTHORIZED`.

### `accepted_contract/`

Complete effective Finding 4 contract.

Primary hashes:

- `SPEC_local_curl_per_side_price_dataset_verification_REV23.md`
  `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`
- `SCHEMA_REGISTRY_REV23.json`
  `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`
- `REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`
  `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`
- `GOVERNING_PACKAGE_MANIFEST_REV23.json`
  `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- governing semantic hash
  `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`
- `ACCEPTED_CONTRACT_SHA256SUMS.txt`
  `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`

The accepted contract also includes the retained contracts/policies and
`REV23_SNAPSHOT_PARTITION_CANCELLATION_AMENDMENT.md`.

### `amendment_audit/rev23_finding4/`

Complete accepted Finding 4 materialization package, including:

- source inputs;
- approved preflight artifacts;
- materialized accepted-contract copy;
- complete replacements;
- RFC 6902 schema patch;
- transformation manifest;
- baseline-target integrity;
- package manifest;
- package-level `SHA256SUMS.txt`;
- source-input checksum inventory;
- static consistency report;
- traceability, stop, change-ledger, handoff, and authorization records.

### `authorization_audit/rev23_finding4/`

- `SENTINEL_ACCEPTANCE_DECISION_REV23_FINDING4.md`
- `AUTHORIZATION_SUPERSESSION_REV23_FINDING4.md`
- `CANONICAL_INSTALL_STATUS.md`

### Historical Amendment 03 authorization audit

`authorization_audit/rev23_amendment_03_i0/` remains preserved for history.

Its implementation authorization is superseded. Its source-sync status records
that no Claude synchronization or authoring is currently authorized.

---

## Canonical documentation

Pinned canonical files:

- `START_HERE.md`
- `PROJECT_STATE.md`
- `GUARDRAILS.md`
- `DECISION_LOG.md`
- `CLOSED_FINDINGS.md`
- `ARTIFACT_INDEX.md`
- `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`
- `DATA_CONTRACTS_named_binary_probe.md`
- `PRICE_INPUT_CONTRACT_named_binary_probe.md`
- `CLAUDE_PROJECT_SETTINGS.md`
- `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`
- `implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md`

Keep canonical repository files and the Claude Project Files panel synchronized.
The private repository remains authoritative.
