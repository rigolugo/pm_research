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

Accepted Revision 10 remediation-scope installation commit:

`ee4a639f9a9429e642391f1fb1e0ab356a6f965a`

Installation commits:

- `3f8cc54dc12a5335472f00f5ffcf5c0d56d8d1ba`
- `c394b9ab5eb5dc07f8d716818e02507994ce41d7`
- `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

### Controlling handoff files

- `README_FIRST.md`
- `SENTINEL_ACCEPTANCE_DECISION.md`
- `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
- `HANDOFF_INVENTORY.md`
- `HANDOFF_SHA256SUMS.txt` — historical complete inventory through the Revision 10 installation-verification state.
- `HANDOFF_REVISION_09_INSTALL_SHA256SUMS.txt` — historical focused Revision 09 scope-installation inventory.
- `HANDOFF_REVISION_10_INSTALL_SHA256SUMS.txt` — historical focused verified Revision 10 scope-installation inventory.
- `HANDOFF_REVISION_10_STATIC_CONFORMANCE_SHA256SUMS.txt` — focused inventory for the documentation-only `REVISION10_STATIC_CONFORMANCE_BLOCKED` record.
- `HANDOFF_REVISION_09_R1_AUTHORIZATION_SHA256SUMS.txt` — historical Revision 09 R1 authorization inventory; inactive under Revision 10.
- `CANONICAL_REPOSITORY_POINTER.md`
- `prompts/CLAUDE_NEW_CHAT_PROMPT.md` — inactive stop notice only; not an implementation prompt.
- `prompts/SENTINEL_NEW_CHAT_PROMPT.md`
- `scope_authoring/rev23_finding4_i0a/README_FIRST.md`
- `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
- `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_INSTALLATION_VERIFICATION_REVISION_10.md`
- `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json`
- `remediation_scope/README_FIRST.md`
- `remediation_scope/SENTINEL_ACCEPTANCE_DECISION.md`
- `remediation_scope/SENTINEL_INSTALLATION_AUTHORIZATION.md`
- `remediation_scope/SENTINEL_INSTALLATION_VERIFICATION.md`
- `remediation_scope/ACCEPTED_REMEDIATION_SCOPE_MANIFEST.json`
- `remediation_scope/REMEDIATION_SCOPE_SHA256SUMS.txt`
- `HANDOFF_REVISION_10_REMEDIATION_SCOPE_SHA256SUMS.txt`

Current implementation state:

`STOP_REV10_REMEDIATION_SOURCE_AUTHORIZATION_NOT_ACTIVATED`

Current static-conformance state:

`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`

Revision 10 remains the controlling accepted specification, installed and
Sentinel-verified at `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`. The current
twelve-path worktree capture is accepted and verified at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`. No implementation
starting SHA, source-gated commit, writable source/test path, test stage, rollback,
promotion, or downstream stage is selected or authorized.
Revision 09 R1 and Revision 08 authorizations are historical and do not carry
forward.

### `implementation_checkpoints/`

Evidence-only canonical preservation area for exact unaccepted implementation
progress. Checkpoint presence is not implementation acceptance and authorizes
nothing.

Controlling index files:

- `README_FIRST.md`
- `CHECKPOINT_INDEX.json`
- `LATEST_PRESERVED_CHECKPOINT.json`
- `LATEST_ACCEPTED_CHECKPOINT.json`

Current preserved checkpoint:

- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/README_FIRST.md`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/CHECKPOINT_MANIFEST.json`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/BASELINE_AND_LINEAGE.md`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/ACTIVITY_BOUNDARY_STATUS.md`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/KNOWN_FINDINGS.md`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_INSTALLATION_VERIFICATION.md`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SHA256SUMS.txt`
- `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/payload_exact/pm_research/local_curl_per_side/prepared_evidence.py`

Exact payload identity:

- SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes
- preservation state: `CANONICALLY_PRESERVED`
- installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- acceptance state: `NOT_ACCEPTED`
- controlling implementation: `false`
- authorization effect: `NONE`
- static-conformance state: `REVISION10_STATIC_CONFORMANCE_BLOCKED`
- static review base: `3cf0871ae97d112324031190822756379d1236e8`

The exact payload remains unchanged and is not included as replacement content in
the documentation-only static-conformance installation package.

Provenance state:

- closed by accepted and verified worktree capture: `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`
- still open: `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`

Resolved specification-layer matters:

- `T107_FIXTURE_REACHABILITY_CONTRADICTION`
- `T153_FIXTURE_REACHABILITY_CONTRADICTION`
- `CANDIDATE_09_NOT_ACCEPTED`

The immutable Sentinel review record identifies the failed Revision 10 contract
areas. It does not select remediation, an implementation start, or a Claude
implementation handoff.

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

Complete accepted Finding 4 materialization package, including source inputs,
approved preflight artifacts, the materialized accepted-contract copy,
replacements, RFC 6902 schema patch, transformation manifest, baseline-target
integrity, package manifest, checksum inventories, static consistency report,
traceability, stop, change-ledger, handoff, and authorization records.

### `authorization_audit/rev23_finding4/`

- `SENTINEL_ACCEPTANCE_DECISION_REV23_FINDING4.md`
- `AUTHORIZATION_SUPERSESSION_REV23_FINDING4.md`
- `CANONICAL_INSTALL_STATUS.md`

### `scope_authoring/rev23_finding4_i0a/`

Accepted bounded implementation-authoring scope history and current controlling
specification.

- `README_FIRST.md`
- `SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
- `SENTINEL_SCOPE_INSTALLATION_VERIFICATION_REVISION_10.md`
- `ACCEPTED_SCOPE_MANIFEST.json`
- `SCOPE_SHA256SUMS.txt`
- `accepted_scope_revision_08/` — immutable exact 14-member historical package
- `accepted_scope_revision_09/` — immutable exact 14-member historical package
- `accepted_scope_revision_10/` — immutable exact 15-member controlling package
- `ACCEPTED_SCOPE_MANIFEST_REVISION_09.json`
- `SENTINEL_SCOPE_ACCEPTANCE_DECISION_REVISION_09.md`
- `ACCEPTED_SCOPE_MANIFEST_REVISION_08.json`
- `SENTINEL_SCOPE_ACCEPTANCE_DECISION_REVISION_08.md`

Revision 10 accepted source archive SHA-256:

`8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`

Revision 10 supersedes Revision 09 for the complete Finding 4 I0A specification
package. Revision 09 and Revision 08 remain immutable historical evidence. No
implementation authorization follows.

### `remediation_scope/`

Accepted and Sentinel-verified Revision 10 implementation-remediation planning
record.

- accepted candidate:
  `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`
- submitted candidate ZIP SHA-256:
  `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`
- installation package ZIP SHA-256:
  `5c4594a01b6210b1b8865815d4617447c2470720e540ac03d4144836de48a72c`
- installation base: `cc2964840d197a40d1c4ef567b42eda762c0be0a`
- verified installation commit: `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`
- installation changed paths: `17`, documentation only
- implementation authorization: `NONE`
- implementation starting SHA: `NOT_AUTHORIZED_AND_NOT_SELECTED`

The scope defines a future atomic three-source candidate and a separately gated
four-test-source candidate. It contains no implementation or test code and does
not activate either stage. The preserved checkpoint remains `NOT_ACCEPTED` and
non-authorizing. The current twelve-path capture closes the worktree-capture gap;
`MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE` remains open.

Controlling records:

- `README_FIRST.md`
- `SENTINEL_ACCEPTANCE_DECISION.md`
- `SENTINEL_INSTALLATION_AUTHORIZATION.md`
- `SENTINEL_INSTALLATION_VERIFICATION.md`
- `ACCEPTED_REMEDIATION_SCOPE_MANIFEST.json`
- `REMEDIATION_SCOPE_SHA256SUMS.txt`
- `accepted_remediation_scope_candidate_01/`

### `authorization_audit/rev23_finding4_i0a_revision10_remediation_source_01/`

Conditional Revision 10 remediation source-authoring authorization package.

- authorization ID: `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`;
- package-preparation base: `a4fb0e64056b58a229da481664e4234e3215cd91`;
- Gustavo authorization: recorded;
- Sentinel package decision: `APPROVE`;
- canonical installation: `INSTALLED_AND_SENTINEL_VERIFIED` at `71061065d91fc391e934d7e79a29eefc898cfe82`;
- canonical-worktree source gate: `STOP_REV10_REMEDIATION_SOURCE_GATE_FAILED`;
- activation: `false`;
- writable after activation: exactly three source files;
- test-source authoring and test execution: unauthorized;
- allowed new repository files: none.

Controlling files:

- `README_FIRST.md`
- `GUSTAVO_AUTHORIZATION_RECORD.md`
- `SENTINEL_IMPLEMENTATION_AUTHORIZATION.md`
- `AUTHORIZATION_MANIFEST.json`
- `AUTHORIZED_FILE_MATRIX.md`
- `ACTIVITY_BOUNDARIES.md`
- `SOURCE_GATE.md`
- `TWELVE_PATH_STARTING_SHA256SUMS.txt`
- `IMPLEMENTATION_REVIEW_DELIVERABLES.md`
- `CLAUDE_HANDOFF_INACTIVE.md`
- `SHA256SUMS.txt`

The package is not an active Claude handoff. Its source gate failed before edits, and the accepted provenance capture does not repair or reactivate it.

### `provenance_audit/rev23_finding4_i0a_current_twelve_path_worktree_capture_01/`

Accepted and Sentinel-verified read-only provenance capture.

- decision: `ACCEPT FINDING — CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`;
- verified installation commit: `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`;
- installation parent: `71061065d91fc391e934d7e79a29eefc898cfe82`;
- source archive SHA-256: `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`;
- source archive size: `487764` bytes;
- source archive members: `17`;
- captured source/test paths: `12`;
- baseline-matching paths: `11`;
- checkpoint-modified paths: `1`;
- closed gap: `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`;
- still-open gap: `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- checkpoint acceptance: `NOT_ACCEPTED`;
- authorization effect: `NONE`.

Controlling records:

- `README_FIRST.md`
- `SENTINEL_ACCEPTANCE_DECISION.md`
- `SENTINEL_INSTALLATION_VERIFICATION.md`
- `PROVENANCE_CAPTURE_MANIFEST.json`
- `SOURCE_ARTIFACT_IDENTITY.md`
- `CAPTURED_GIT_STATE.txt`
- `CAPTURED_FILE_INVENTORY.json`
- `CAPTURED_TWELVE_PATH_SHA256SUMS.txt`
- `CAPTURED_PACKAGE_MANIFEST.json`
- `CAPTURED_PROVENANCE_NOTES.md`
- `ACTIVITY_BOUNDARIES.md`
- `SENTINEL_INSTALLATION_SCOPE.md`
- `SHA256SUMS.txt` — historical acceptance-package inventory
- `evidence_exact/REV23_FINDING4_I0A_PROVENANCE_CAPTURE.zip`
- `HANDOFF_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_SHA256SUMS.txt`
- `HANDOFF_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_VERIFICATION_SHA256SUMS.txt`

### `authorization_audit/rev23_finding4_i0a/`

Historical bounded Revision 08 authoring package:

- `README_FIRST.md`
- `GUSTAVO_AUTHORIZATION_RECORD.md`
- `SENTINEL_IMPLEMENTATION_AUTHORIZATION.md`
- `AUTHORIZATION_MANIFEST.json`
- `AUTHORIZED_FILE_MATRIX.md`
- `ACTIVITY_BOUNDARIES.md`
- `SOURCE_GATE.md`
- `SHA256SUMS.txt`

Authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`. The package
is specific to Revision 08 and is inactive under Revision 10.

### `authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/`

Historical, non-reusable authorization record for
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

- `README_FIRST.md`
- `GUSTAVO_AUTHORIZATION_RECORD.md`
- `SENTINEL_AUTHORIZATION_DECISION.md`
- `SENTINEL_ACTIVATION_VERIFICATION.md`
- `AUTHORIZED_FILE_MATRIX.md`
- `ACTIVITY_BOUNDARIES.md`
- `SOURCE_GATE.md`
- `AUTHORIZATION_MANIFEST.json`
- `REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt`
- `SHA256SUMS.txt`

Baseline provenance:

- `REV23_FINDING4_I0A_IMPLEMENTATION_REVIEW.zip` SHA-256
  `e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`
- twelve-path baseline composite SHA-256
  `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`
- later historical `prepared_evidence.py` starting SHA-256
  `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

The package was historically activated at source-gated commit
`1e1afb29791f42c286b45d3b576f74926add8dce`. It cannot authorize another edit,
rollback, restoration, overwrite, promotion, test stage, execution stage, R2,
or downstream activity.

### `authorization_audit/rev23_amendment_03_i0/`

Preserved historical authorization evidence. Its implementation authorization is
superseded and its source-sync status authorizes no current Claude activity.

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
- `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/README_FIRST.md`
- `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`

Keep canonical repository files and the Claude Project Files panel synchronized.
Preserve material unaccepted implementation progress through
`implementation_checkpoints/`; do not use chat-only state as the sole recovery
source. The private repository remains authoritative.
