Use the pm-research-implementing Skill. Skill invocation does not expand the authorization below.

# S2 Candidate 08 — Bounded Implementation-Source Authoring Sentinel Handoff Record Candidate 01

## 1. Status and activation condition

| Field | Exact value |
|---|---|
| Record ID | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORING_BOUNDED_SENTINEL_HANDOFF_RECORD_CANDIDATE_01` |
| Status | `BOUNDED_IMPLEMENTATION_SOURCE_HANDOFF_REVIEW_CANDIDATE` |
| Actor | `CLAUDE` |
| Run ID | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORING_RUN_01` |
| Canonical base | `fc16e9124acb8acb490975c7289d8199b84f2c25` |
| Stage | `IMPLEMENTATION_SOURCE` |
| Package-preparation authorization effect | `NONE` |
| Future activity effect after activation | `IMPLEMENTATION_ONLY` |

This handoff is not active from draft or review-package presence. It becomes
consumable only after the exact package containing it is:

1. accepted by Sentinel;
2. separately authorized by Gustavo for canonical installation;
3. canonically installed without byte drift; and
4. independently verified by Sentinel at its exact installation commit.

No step follows automatically.

## 2. Exact controlling identities

| Item | Path | Bytes | SHA-256 | Additional identity |
|---|---|---:|---|---|
| K011 | `nodes/K011/artifact.json` | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | accepted Candidate-08 prerequisite |
| A010 | `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md` | `135500` | `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950` | rank `1115`; predecessor `[K011]` |
| K013 | `nodes/K013/artifact.json` | `3099` | `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c` | predecessors `[K011, A010]` |
| K012 | `nodes/K012/artifact.json` | `3449` | `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c` | Git blob `796a4d1af1f5765890544f029e51b7b27878d24d`; predecessors `[K011, A010, K013]` |
| K014 | `nodes/K014/artifact.json` | `4302` | `7d54c1cabd1be53abc677425e5b7ce781d362bef2918c31bd844a0fa316b9fc2` | Git blob `cc35df982377286e0940c9dddd5cee01a51e4ace`; predecessors `[K011, A010, K013, K012]` |
| accepted K008 | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md` | `776003` | `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63` | accepted specification |
| accepted Amendment 01 | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md` | `24599` | `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63` | accepted and canonically installed |

K014 exact contract fields:

- schema/profile: `pm_research.s2.activity_root.v1` / `activity_root.v1`;
- rank/role: `1140` / `implementation_source_activity_root`;
- embedded contract commit: `0b755fb71175370638ec87175aee85cf4710f54d`;
- canonical installation commit: `fc16e9124acb8acb490975c7289d8199b84f2c25`;
- `created_at_utc_ms`: `1785598380000`;
- run ID: `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORING_RUN_01`.

A mismatch in any path, byte length, hash, blob, ordering, role, schema, profile,
rank, commit, or installation state requires a stop.

## 3. Already completed administrative access

The bounded administrative access under
`S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_READ_ONLY_REPOSITORY_ACCESS_GUSTAVO_AUTHORIZATION_01` is complete.

It covered one read-only clone/fetch pinned to `fc16e9124acb8acb490975c7289d8199b84f2c25`, verification
of `HEAD`, `origin/main`, clean-tree state, exact bytes and hashes, and bounded
read-only text inspection. It produced no source files, changed no existing
files, and left the workspace clean.

This completed access is an antecedent administrative action. It is not part of
implementation-source execution, need not be repeated, and must not be treated
as continuing network or subprocess authorization.

## 4. Future implementation activity

After the activation condition in §1 is satisfied, Claude MAY:

1. author exactly the fourteen source files in §5;
2. compute their exact byte lengths and SHA-256 values using non-executing file
   operations;
3. perform static text, literal, schema, path, and identity inspection that does
   not import or execute project code;
4. materialize K015 only after all fourteen final source byte objects exist;
5. materialize K016 only after valid final K015 bytes exist;
6. return the fourteen source files, exact identities, K015, K016, and a concise
   conformance report to Sentinel.

Claude MUST NOT create, modify, delete, or rename any other path.

## 5. Exact implementation-source matrix

The package model is the regular Python package
`pm_research.named_binary_probe_s2` at
`pm_research/named_binary_probe_s2/`.

| # | Logical path | Exact role | Language | Required |
|---:|---|---|---|---|
| 1 | `pm_research/named_binary_probe_s2/__init__.py` | `package_export` | `PYTHON` | `true` |
| 2 | `pm_research/named_binary_probe_s2/acquisition.py` | `independent_token_acquisition_and_raw_closure` | `PYTHON` | `true` |
| 3 | `pm_research/named_binary_probe_s2/alignment.py` | `accepted_policy_alignment` | `PYTHON` | `true` |
| 4 | `pm_research/named_binary_probe_s2/audit.py` | `nineteen_audit_closures_and_gate` | `PYTHON` | `true` |
| 5 | `pm_research/named_binary_probe_s2/construction.py` | `scientific_construction_and_deduplication` | `PYTHON` | `true` |
| 6 | `pm_research/named_binary_probe_s2/prices_history_contract.py` | `endpoint_response_terminal_and_retry_contract` | `PYTHON` | `true` |
| 7 | `pm_research/named_binary_probe_s2/rebuild.py` | `isolated_rebuild_and_byte_comparison` | `PYTHON` | `true` |
| 8 | `pm_research/named_binary_probe_s2/request_plan.py` | `deterministic_request_plan` | `PYTHON` | `true` |
| 9 | `pm_research/named_binary_probe_s2/s4_inputs.py` | `s4_input_parsers_and_reconciliation` | `PYTHON` | `true` |
| 10 | `pm_research/named_binary_probe_s2/safe_span.py` | `safe_span_classifier_and_reducer` | `PYTHON` | `true` |
| 11 | `pm_research/named_binary_probe_s2/schema_registry.py` | `schema_registry_and_edge_derivation` | `PYTHON` | `true` |
| 12 | `pm_research/named_binary_probe_s2/state_reducers.py` | `global_condition_transition_state_reducers` | `PYTHON` | `true` |
| 13 | `pm_research/named_binary_probe_s2/transition.py` | `stage10_transition_reconciliation` | `PYTHON` | `true` |
| 14 | `pm_research/named_binary_probe_s2/types.py` | `closed_types_and_jcs` | `PYTHON` | `true` |

### 5.1 Normative matrix authority

The implementation instruction, K015 construction, and K016 handoff MUST use
exactly these two authoritative matrix locations:

1. Candidate 08 §23 top-level `implementation_source_matrix`, as amended by
   accepted Implementation-Source Amendment 01 and accepted A010;
2. Candidate 08 §23
   `nodes.K015.node_specific_constants.exact_source_file_matrix`, as amended by
   accepted Implementation-Source Amendment 01 and accepted A010.

Before source authoring or K015 construction, both authoritative locations MUST
resolve to the same fourteen ordered path-role rows shown in §5. K016 handoff
materialization MUST bind the K015 candidate produced from that exact resolved
matrix.

Appendix A is authoritative only for direct graph edges. Appendix A MUST NOT be
used as the source-file matrix authority.

Any missing citation to either authoritative matrix location, any disagreement
between the two resolved matrix locations, or any substitution of Appendix A
for either matrix location is
`STOP_IMPLEMENTATION_MATRIX_CITATION_INVALID`.

After `STOP_IMPLEMENTATION_MATRIX_CITATION_INVALID`, no source authoring, K015,
or K016 may proceed. Existing evidence MUST be preserved and returned to
Sentinel without widening scope or selecting a fallback matrix.

Closed matrix rules:

- exactly fourteen rows and fourteen files;
- every role remains attached to its listed path;
- rows are emitted in raw UTF-8 `logical_path` ascending order after rejecting
  non-NFC input;
- every K015 row includes actual final `byte_length`, `sha256`, and
  `required=true`;
- no fifteenth file, helper, generated side file, compatibility shim,
  `src/` path, namespace-package design, `pyproject.toml` change, path rename,
  relocation, reduction, or role reassignment;
- internal imports are explicit relative imports within
  `pm_research.named_binary_probe_s2` or absolute imports beginning with that
  package name.

## 6. Exact registry and reducer materialization contract

### 6.1 Immutable accepted base registry

- JCS bytes: `479463`;
- SHA-256: `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`;
- source: exact first fenced JSON object under accepted K008 §23;
- runtime Markdown parsing or runtime K008 reading: forbidden.

### 6.2 Accepted A010 overlay

- JCS bytes: `45347`;
- SHA-256: `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a`;
- operation count: `27`;
- immutable-base materializer: exactly one verified working copy and one
  operation-engine invocation;
- a flattened third hand-edited registry literal: forbidden.

### 6.3 Effective registry bundle

- bytes: `1266`;
- SHA-256: `075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67`;
- effective graph: `167` nodes /
  `683` direct edges;
- K127 evidence population: `60`;
- exposure is atomic only after all base, overlay, graph, reducer, and bundle
  checks pass.

`schema_registry.py` MUST preserve exactly the accepted immutable base literal
and exact A010 overlay literal, verify both identities, materialize one
deep-frozen effective semantic view, and expose no partial result.

### 6.4 Reducer projection

- bytes: `66232`;
- SHA-256: `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`;
- exact keys: complete `condition_state_classes` and `global_state_reducer`;
- `state_reducers.py` derives behavior from the verified immutable effective
  registry and MUST NOT contain a duplicate or hand-edited normative reducer
  literal.

## 7. Exact K015 contract

K015 is created only after the fourteen final source files exist.

| Field | Exact contract |
|---|---|
| node | `K015` |
| rank | `1150` |
| semantic role | `implementation_source_candidate` |
| schema/profile | `pm_research.s2.source_matrix.v1` / `source_matrix.v1` |
| record ID | `S2_CANDIDATE_08_K015_IMPLEMENTATION_SOURCE_CANDIDATE_01` |
| canonical commit | `0b755fb71175370638ec87175aee85cf4710f54d` |
| direct predecessors | exactly `[K014]` |
| typed binding | `/payload/activity_root` → exact K014 |
| top-level status | `REVIEW_CANDIDATE_NOT_CONSUMABLE` |
| creation time | fresh `UtcMs` strictly greater than K014; recorded once |
| `/payload/file_matrix` | exactly fourteen final `SourceFileRow` values from §5 |
| `/payload/matrix_closed` | `true` |
| `/payload/implementation_status` | `CANDIDATE_ONLY` |

Each `SourceFileRow` has exactly:

- `logical_path`;
- `role`;
- `language = PYTHON`;
- `required = true`;
- actual final `byte_length`;
- actual final `sha256`.

K015 JCS serialization is RFC 8785 UTF-8, no BOM, no trailing newline.
`dependencies` is derived exactly from the K014 typed reference and is not an
independent source of edges. K015 MUST NOT exist before the complete source
matrix validates.

## 8. Exact K016 contract

K016 is created only after valid final K015 bytes exist.

| Field | Exact contract |
|---|---|
| node | `K016` |
| rank | `1160` |
| semantic role | `implementation_source_handoff` |
| schema/profile | `pm_research.s2.handoff.v1` / `handoff.v1` |
| record ID and handoff ID | `S2_CANDIDATE_08_K016_IMPLEMENTATION_SOURCE_HANDOFF_CANDIDATE_01` |
| canonical commit | `0b755fb71175370638ec87175aee85cf4710f54d` |
| direct predecessors | exactly `[K013, K012, K014, K015]` |
| control refs | exactly `[K013, K012, K014]` |
| deliverable refs | exactly `[K015]` |
| evidence refs | exactly `[]` |
| stage code | `IMPLEMENTATION_SOURCE` |
| top-level status | `REVIEW_CANDIDATE_NOT_CONSUMABLE` |
| creation time | fresh `UtcMs` strictly greater than K015 |
| `/payload/self_identity` | exactly `null` |
| `/payload/authorization_effect` | exactly `NONE` |

Exact `actions_performed`:

1. `IMPLEMENTATION_SOURCE_AUTHORING`;
2. `NON_EXECUTING_SOURCE_BYTE_LENGTH_AND_SHA256_COMPUTATION`;
3. `STATIC_TEXT_SCHEMA_IDENTITY_INSPECTION`;
4. `K015_MATERIALIZATION`;
5. `K016_MATERIALIZATION`.

Exact `actions_not_performed`:

- `NETWORK_ACCESS`;
- `REPOSITORY_CLONE_OR_FETCH`;
- `SUBPROCESS_EXECUTION`;
- `TEST_SOURCE_AUTHORING`;
- `TEST_EXECUTION`;
- `PROJECT_IMPORT`;
- `LOCAL_RESEARCH_DATA_READ`;
- `EMPIRICAL_EXECUTION`;
- `PACKAGE_INSTALLATION`;
- `GIT_ACTIVITY`;
- `CANONICAL_INSTALLATION`;
- `P1`;
- `P2`;
- `P3`;
- `SCORING`;
- `PROBE_EXECUTION`;
- `AUTOMATIC_GATE_CHANGE`.

Because this handoff carries no scientific result effects, `/payload/effects`
is exactly:

```json
{
  "ACTIVE": 0,
  "VALID_EXCLUSION": 0,
  "CLEAR_COMPONENT": 0,
  "LIMITATION": 0,
  "INCOMPLETE_EVIDENCE": 0,
  "BLOCKING_DEFECT": 0,
  "total": 0
}
```

K016 MUST NOT embed its own raw SHA-256 and MUST NOT use a self-excluding
projection. Its later review record or external delivery envelope binds exact
raw K016 path, byte length, and SHA-256.

## 9. Accepted stop conditions

All three accepted inventories below control. A code repeated across
inventories remains one code, not an alternate meaning.

### 9.1 Accepted Candidate-08 base stops

- `STOP_AUTHORIZATION_ORDER_INVALID`
- `STOP_AUTHORIZATION_PROVENANCE_INVALID`
- `AUTHORIZATION_PREREQUISITE_BYTES_MISSING`
- `AUTHORIZATION_SCOPE_EXPANSION`
- `GLOBAL_STATE_INVALID`
- `CONDITION_STATE_INVALID`
- `STOP_CANONICAL_BASE_MISMATCH`
- `STOP_P0_NOT_CLEAR`
- `STOP_STALE_CONTRACT`
- `STOP_INPUT_IDENTITY_MISMATCH`
- `STOP_UNIVERSE_RECONCILIATION_FAILED`
- `STOP_RESOLUTION_BOUNDARY_INVALID`
- `STOP_TRADE_ANCHOR_MISSING`
- `STOP_TOKEN_ENUMERATION_UNRELIABLE`
- `STOP_PRECISION_LOSS`
- `PREFLIGHT_INTEGRITY_FAILURE`
- `PREFLIGHT_INCOMPLETE`
- `NO_SAFE_SPAN`
- `NO_SAFE_SPAN_AFTER_MARGIN`
- `STOP_REQUEST_PLAN_INVALID`
- `STOP_REQUEST_TERMINALS_INCOMPLETE`
- `STOP_RAW_ARCHIVE_INCOMPLETE`
- `STOP_RAW_ARCHIVE_IDENTITY_MISMATCH`
- `STOP_ENDPOINT_SHAPE_UNRECOGNIZED`
- `STOP_FORBIDDEN_SYNTHESIS`
- `DUPLICATE_PRICE_CONFLICT`
- `SCIENTIFIC_PROJECTION_CONFLICT`
- `SCIENTIFIC_RAW_PROJECTION_MISMATCH`
- `ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN`
- `STOP_DETERMINISTIC_BUILD_ID_MISMATCH`
- `STOP_REBUILD_SOURCE_ISOLATION_VIOLATION`
- `STOP_REBUILD_BYTE_MISMATCH`
- `STOP_ALIGNMENT_POLICY_ABSENT`
- `STOP_ALIGNMENT_POLICY_INVALID`
- `STOP_ALIGNMENT_INCOMPLETE`
- `PROVENANCE_EDGE_SET_MISMATCH`
- `STOP_AUDIT_SELF_REFERENCE`
- `STOP_GATE_RECONCILIATION_FAILED`
- `STOP_S9_NOT_APPROVED_CLEAR`
- `STOP_TRANSITION_RECONCILIATION_FAILED`
- `STOP_CANDIDATE_SEAL_PREMATURE`
- `STOP_P1_NOT_SEPARATELY_AUTHORIZED`
- `ARCHITECTURE_CONTROL_SET_INVALID`
- `STOP_DUPLICATE_IDENTITY_CONFLICT`
- `STOP_RESOURCE_BOUND_EXCEEDED`
- `STOP_RESUME_PROVENANCE_INVALID`
- `STOP_RETRY_AFTER_UNIT_INVALID`
- `STOP_ZERO_POPULATION_NOT_PERMITTED`
- `STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED`
- `STOP_UNEXPECTED_DELIVERABLE_PATH`

### 9.2 Accepted Implementation-Source Amendment-01 stops

- `STOP_CANONICAL_BASE_MISMATCH`
- `STOP_A002_IDENTITY_MISMATCH`
- `STOP_ACCEPTED_K008_IDENTITY_MISMATCH`
- `STOP_AMENDMENT_NOT_ACCEPTED`
- `STOP_AMENDMENT_INSTALLATION_NOT_VERIFIED`
- `STOP_IMPLEMENTATION_MATRIX_CITATION_INVALID`
- `STOP_K015_SOURCE_MATRIX_INVALID`
- `STOP_NAMESPACE_PACKAGE_FORBIDDEN`
- `STOP_PACKAGING_SCOPE_NOT_AUTHORIZED`
- `STOP_REGISTRY_SOURCE_IDENTITY_MISMATCH`
- `STOP_REGISTRY_EXTRACTION_AMBIGUOUS`
- `STOP_REGISTRY_JCS_IDENTITY_MISMATCH`
- `STOP_REDUCER_PROJECTION_IDENTITY_MISMATCH`
- `STOP_GENERATED_LITERAL_DRIFT`
- `STOP_K016_SELF_IDENTITY_INVALID`
- `STOP_AUTHORIZATION_CHAIN_INCOMPLETE`
- `STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED`

### 9.3 Accepted A010 overlay stops

- `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH`
- `STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH`
- `STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID`
- `STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET`
- `STOP_REGISTRY_OVERLAY_TARGET_MISSING`
- `STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE`
- `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED`
- `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH`
- `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH`
- `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH`
- `STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID`

Any required newly expanded network, subprocess, import, project execution,
package installation, data-access, Git-write, or test boundary is
`STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED`. Preserve all completed source bytes and
return to Sentinel; do not silently reuse the completed administrative access.

## 10. Forbidden future activity

This handoff does not authorize:

- additional network access;
- additional repository cloning or fetching;
- subprocess execution;
- test-source authoring or test execution;
- project imports or project-code execution;
- local research-data access;
- empirical activity, price acquisition, or construction;
- package installation;
- Git branch, commit, push, merge, tag, ref update, reset, or rebase;
- canonical installation;
- P1, P2, P3, scoring, probes, or gate changes;
- any source path outside §5.

If the environment cannot author and hash the files without a newly required
network, subprocess, import, or execution boundary, Claude MUST stop and return
to Sentinel.

## 11. Required return to Sentinel

Return:

1. all fourteen final source files;
2. one exact identity table with path, role, byte length, and SHA-256 for
   every source file;
3. exact K015 raw bytes and external identity;
4. exact K016 raw bytes and external identity;
5. static evidence for matrix equality, registry/base/overlay/bundle identities,
   reducer projection identity, prohibited-path absence, prohibited-operation
   absence, and K016 `self_identity = null`;
6. a clear list of actions not performed.

Do not update canonical project-context files. If a canonical documentation
change appears necessary, return a finding to Sentinel.
