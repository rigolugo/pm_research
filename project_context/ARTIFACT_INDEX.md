# ARTIFACT INDEX

*Canonical and proposed identities for the current S2 K014 review boundary.*

---

## Canonical base

- repository: `rigolugo/pm_research`;
- canonical `main`: `0872d4578fd2c0fc5147c77af606b9f807c7bc2b`;
- classification: `K014_DOCUMENTATION_GOVERNANCE_CANDIDATE_PREPARATION_ONLY`;
- candidate-preparation authorization effect: `NONE`.

## Installed controlling artifacts

| Node | Path | Bytes | SHA-256 | Rank | Predecessors | Installation state |
|---|---|---:|---|---:|---|---|
| K011 | `nodes/K011/artifact.json` | 1134 | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | acceptance | accepted chain | canonical |
| A010 | `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md` | 135500 | `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950` | 1115 | `[K011]` | accepted, installed, verified |
| K013 | `nodes/K013/artifact.json` | 3099 | `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c` | 1120 | `[K011, A010]` | installed at `6c891a61e7408f7977b72b2ccf52472412cd7e04`, verified |
| K012 | `nodes/K012/artifact.json` | 3449 | `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c` | 1130 | `[K011, A010, K013]` | installed at `0872d4578fd2c0fc5147c77af606b9f807c7bc2b`, verified |

K012 Git blob: `796a4d1af1f5765890544f029e51b7b27878d24d`.

## Fresh proposed K014

| Field | Value |
|---|---|
| Path | `nodes/K014/artifact.json` |
| Bytes | `4302` |
| SHA-256 | `7d54c1cabd1be53abc677425e5b7ce781d362bef2918c31bd844a0fa316b9fc2` |
| Git blob | `cc35df982377286e0940c9dddd5cee01a51e4ace` |
| Schema/profile | `pm_research.s2.activity_root.v1` / `activity_root.v1` |
| Rank/role | `1140` / `implementation_source_activity_root` |
| Ordered predecessors | `[K011, A010, K013, K012]` |
| Embedded commit | `0b755fb71175370638ec87175aee85cf4710f54d` |
| Timestamp | `1785598380000` |
| Status | `REVIEW_CANDIDATE_NOT_CONSUMABLE` |
| Canonical membership | `NO — proposed package member only` |
| Candidate-preparation effect | `NONE` |

## Proposed canonical package paths

1. `nodes/K014/artifact.json`
2. `project_context/START_HERE.md`
3. `project_context/PROJECT_STATE.md`
4. `project_context/DECISION_LOG.md`
5. `project_context/ARTIFACT_INDEX.md`
6. `project_context/S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_01.json`
7. `project_context/S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_DOCUMENTATION_GOVERNANCE_PACKAGE_SHA256SUMS_CANDIDATE_01.txt`

Review-only members:

1. `review_only/HANDOFF_PROFESSOR_S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_DOCUMENTATION_GOVERNANCE_PACKAGE_CANDIDATE_01.md`
2. `review_only/CHANGED_PATH_MATRIX_S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_DOCUMENTATION_GOVERNANCE_PACKAGE_CANDIDATE_01.csv`

## Exact implementation matrix

| # | Path | Role | Language | Required |
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

## Package identity model

The binding model is `REVIEW_ZIP_EXTERNAL_SIDECAR_V1`. The checksum inventory
hashes five substantive candidates and two review-only files, while excluding
itself and the manifest. The manifest inventories every ZIP member, including
itself. Its own member entry has null byte length, SHA-256, and self-identity;
top-level self-identity is null. The external sidecar binds final ZIP bytes.
No ZIP member contains the final ZIP hash. The graph is acyclic.

## Lifecycle status

K012 is accepted, installed, and verified. K014 review is pending. K014
installation authorization, installation verification, consumability, and the
separate implementation handoff are absent. K015/K016 and implementation source
are absent. Tests, execution, data, network, empirical work, canonical
installation, and Git activity are absent.

Requested Sentinel decision:
`APPROVE — S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_CANDIDATE_01_ACCEPTED`.
