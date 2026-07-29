# S2 Candidate 08 Implementation-Source Amendment 01 — Canonical Installation Record

## 1. Status

| Field | Value |
|---|---|
| Record ID | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_CANONICAL_INSTALLATION_RECORD` |
| Status | `DOCUMENTATION_ONLY_CANONICAL_INSTALLATION_RECORD_CANDIDATE_05` |
| Authoring mode | `MATERIALIZE` |
| Prepared by | Professor |
| Reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Installation package base | `ddf41003fb16aa091c2a899d7c17754e89341cc7` |
| Authorization | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_DOCUMENTATION_ONLY_INSTALLATION_PREPARATION_GUSTAVO_AUTHORIZATION_01` |
| Sentinel decision recorded | `APPROVE — S2 Candidate 08 Implementation-Source Amendment 01 accepted as a SPEC-only amendment` |
| Authorization effect | `NONE` |

This record is a proposed canonical documentation record for the accepted S2 Candidate 08 Implementation-Source Amendment 01. It is not an implementation authorization and does not create or activate K013, K012, K014, K015, K016, source files, tests, execution, data access, network/vendor activity, Git activity, P1/P2/P3, scoring, probe execution, or gate changes.

**Checkable completion sentence:** Sentinel can verify that the accepted amendment file is canonically installed with exact identity `24599 / 8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63`, that the documentation authority set references it consistently, and that implementation authorization remains `NONE`.

## 2. Installed accepted amendment identity

| Field | Exact value |
|---|---|
| Canonical proposed path | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md` |
| Accepted package source path | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md` |
| Byte length | `24599` |
| SHA-256 | `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63` |
| Accepted decision | `APPROVE — S2 Candidate 08 Implementation-Source Amendment 01 accepted as a SPEC-only amendment` |
| Authorization effect | `NONE` |

## 3. Accepted amendment effect

The amendment resolves only the accepted implementation-source authorization blocker:

`ACCEPT FINDING — S2_IMPLEMENTATION_SOURCE_AUTHORIZATION_BLOCKED_BY_PATH_LAYOUT_AND_REGISTRY_PROVENANCE`

Resolved defects:

1. package-layout/path-boundary defect;
2. registry-provenance ambiguity;
3. K015 ordering ambiguity;
4. K016 self-identity ambiguity;
5. incorrect Appendix-A matrix citation.

## 4. Preserved S2 identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| accepted K008 specification | `776003` | `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63` |
| accepted K009 Professor handoff | `13549` | `720f2f081fa1f127fadc980702dd072f52a3714a14f7db418489862d14a609f1` |
| K010 Sentinel review | `1504` | `e34ddcf51b8b908570de9b4cd4af520114e46bc848cfc00110bf4874dfafa17b` |
| K011 acceptance | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f264` |
| A002 accepted architecture prerequisite | `5854` | `87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c` |
| accepted Candidate-08 §23 JCS | `479463` | `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff` |
| reducer projection | `66232` | `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c` |

## 5. Future implementation-source model after this documentation installation

| Field | Accepted value |
|---|---|
| Future implementation package | `pm_research.named_binary_probe_s2` |
| Future repository directory | `pm_research/named_binary_probe_s2/` |
| Future source matrix count | `14` |
| `src/` layout | forbidden |
| namespace package behavior | forbidden |
| `pyproject.toml` changes | forbidden for this stage |
| K016 `/payload/self_identity` | `null` |
| Current implementation authorization | `NONE` |

Exact future source matrix:

| # | Path | Role |
|---:|---|---|
| 1 | `pm_research/named_binary_probe_s2/__init__.py` | `package_export` |
| 2 | `pm_research/named_binary_probe_s2/acquisition.py` | `independent_token_acquisition_and_raw_closure` |
| 3 | `pm_research/named_binary_probe_s2/alignment.py` | `accepted_policy_alignment` |
| 4 | `pm_research/named_binary_probe_s2/audit.py` | `nineteen_audit_closures_and_gate` |
| 5 | `pm_research/named_binary_probe_s2/construction.py` | `scientific_construction_and_deduplication` |
| 6 | `pm_research/named_binary_probe_s2/prices_history_contract.py` | `endpoint_response_terminal_and_retry_contract` |
| 7 | `pm_research/named_binary_probe_s2/rebuild.py` | `isolated_rebuild_and_byte_comparison` |
| 8 | `pm_research/named_binary_probe_s2/request_plan.py` | `deterministic_request_plan` |
| 9 | `pm_research/named_binary_probe_s2/s4_inputs.py` | `s4_input_parsers_and_reconciliation` |
| 10 | `pm_research/named_binary_probe_s2/safe_span.py` | `safe_span_classifier_and_reducer` |
| 11 | `pm_research/named_binary_probe_s2/schema_registry.py` | `schema_registry_and_edge_derivation` |
| 12 | `pm_research/named_binary_probe_s2/state_reducers.py` | `global_condition_transition_state_reducers` |
| 13 | `pm_research/named_binary_probe_s2/transition.py` | `stage10_transition_reconciliation` |
| 14 | `pm_research/named_binary_probe_s2/types.py` | `closed_types_and_jcs` |

A future source-authoring chain must be fresh and post-installation:

`K011 + accepted installed amendment → fresh K013 → fresh K012 → fresh K014 → K015/K016`

No stale, pre-amendment, chat-only, or matrix-mismatched K013/K012/K014 may be reused.

## 6. Documentation package scope

This documentation package proposes adding or replacing only the following canonical documentation files:

1. `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
2. `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_CANONICAL_INSTALLATION_RECORD.md`;
3. `project_context/START_HERE.md`;
4. `project_context/PROJECT_STATE.md`;
5. `project_context/DECISION_LOG.md`;
6. `project_context/ARTIFACT_INDEX.md`.

No source, test, packaging, runtime, dependency, generated-code, artifact-output, or research-data path is in scope.

## 7. Stop conditions

- `STOP_CANONICAL_BASE_MISMATCH`;
- `STOP_ACCEPTED_AMENDMENT_IDENTITY_MISMATCH`;
- `STOP_DOCUMENTATION_AUTHORITY_SET_INCOMPLETE`;
- `STOP_DOCUMENTATION_STATE_CONTRADICTION`;
- `STOP_SOURCE_TEST_PACKAGE_RUNTIME_PATH_NEEDED`;
- `STOP_IMPLEMENTATION_AUTHORIZATION_ATTEMPTED`;
- `STOP_TEST_AUTHORIZATION_ATTEMPTED`;
- `STOP_GIT_WRITE_REQUIRED`;
- `STOP_STALE_PRE_AMENDMENT_AUTHORIZATION_REUSE`.

## 8. Explicit non-authorization

This record and package authorize no implementation-source authoring, test-source authoring, test execution, project imports or execution, compilation, linting, type checking, coverage, local research-data reads, network/API/RPC/vendor/Dune/curl/endpoint activity, dependency or packaging changes, acquisition, construction, alignment, rebuild, audit, transition, empirical work, P1/P2/P3, scoring, probe execution, gate changes, Git commit, push, merge, branch, tag, release, ref update, or canonical installation itself.

Authorization effect: `NONE`.

---

## 9. Candidate 05 manifest and sidecar self-reference rule

Candidate 05 uses a two-layer external-binding model.

1. The six canonical documentation payload files are:
   - `project_context/START_HERE.md`;
   - `project_context/PROJECT_STATE.md`;
   - `project_context/DECISION_LOG.md`;
   - `project_context/ARTIFACT_INDEX.md`;
   - `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
   - `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_CANONICAL_INSTALLATION_RECORD.md`.
2. The proposed canonical manifest and proposed canonical SHA-256 record are installed control files, not payload-file checksum subjects.
3. The proposed canonical manifest has `self_identity = null`; its raw SHA-256 MUST be bound externally by the Candidate 05 review-package manifest and by any later Sentinel canonical-installation verification.
4. The proposed canonical SHA-256 record inventories only the six payload files above and excludes itself and the proposed canonical manifest to avoid circular self-hash claims.
5. The proposed canonical SHA-256 record's raw identity is also bound externally by the Candidate 05 review-package manifest and by any later Sentinel canonical-installation verification.
6. Any later installed package that records a manifest or sidecar raw identity different from the Candidate 05 review-package manifest MUST stop as `STOP_DOCUMENTATION_PACKAGE_IDENTITY_MISMATCH`.

This rule removes the Candidate 02 contradiction where the proposed canonical manifest recorded a SHA-256 for itself that did not match the ZIP member.

---

## 12. Candidate 05 review-package external sidecar rule

Candidate 05 uses `REVIEW_ZIP_EXTERNAL_SIDECAR_V1`.

1. The Candidate 05 root ZIP SHA-256 sidecar is supplied as a separate file outside the ZIP:
   `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_DOCUMENTATION_INSTALLATION_PACKAGE_CANDIDATE_05.zip.sha256`.
2. The sidecar binds the final sealed Candidate 05 ZIP bytes after archive creation.
3. The root ZIP sidecar is not a ZIP member.
4. The root review-package manifest has `self_identity = null`.
5. The root review-package manifest inventories every actual ZIP member except itself.
6. No final ZIP hash is stored inside a ZIP member.
7. Candidate 03 and Candidate 04 are blocked predecessor packages only and are not operative installed-package identities or active external-binding authorities.

## 13. Candidate 05 canonical manifest and sidecar self-reference rule

Candidate 05 preserves the proposed canonical two-layer external-binding model.

1. The proposed canonical manifest has `self_identity = null`.
2. The proposed canonical SHA-256 record inventories only the six canonical documentation payload files.
3. The proposed canonical SHA-256 record explicitly excludes itself and the proposed canonical manifest.
4. The proposed canonical manifest and proposed canonical sidecar are installed control files externally bound by the Candidate 05 review-package manifest and any later Sentinel canonical-installation verification.
5. No manifest or sidecar raw SHA-256 is embedded in its own bytes.

This rule supersedes blocked Candidate 03 and Candidate 04 package-binding language. Candidate 03 may be cited only as historical blocked predecessor evidence.
