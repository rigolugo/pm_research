# ARTIFACT INDEX

*Canonical and proposed identities for the current S2 K012 review boundary.*

---

## Canonical base

- repository: `rigolugo/pm_research`;
- canonical `main` inspected: `6c891a61e7408f7977b72b2ccf52472412cd7e04`;
- candidate-preparation classification:
  `K012_DOCUMENTATION_GOVERNANCE_CANDIDATE_PREPARATION_ONLY`;
- candidate-preparation authorization effect: `NONE`.

## Installed controlling artifacts

| Node | Logical path | Bytes | SHA-256 | Direct predecessors |
|---|---|---:|---|---|
| `K011` | `nodes/K011/artifact.json` | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | accepted specification chain |
| `A010` | `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md` | `135500` | `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950` | `[K011]` |
| `K013` | `nodes/K013/artifact.json` | `3099` | `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c` | `[K011, A010]` |

K013 canonical installation commit: `6c891a61e7408f7977b72b2ccf52472412cd7e04`.

## Fresh proposed K012

| Field | Value |
|---|---|
| Path | `nodes/K012/artifact.json` |
| Bytes | `3449` |
| SHA-256 | `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c` |
| Schema | `pm_research.s2.sentinel_authorization.v1` |
| Profile | `sentinel_authorization.v1` |
| Rank | `1130` |
| Semantic role | `sentinel_implementation_source_authorization` |
| Ordered direct predecessors | `[K011, A010, K013]` |
| Status | `REVIEW_CANDIDATE_NOT_CONSUMABLE` |
| Canonical membership | `NO — proposed package member only` |
| Authorization effect of preparation | `NONE` |

## Proposed canonical package paths

1. `nodes/K012/artifact.json` — new substantive candidate.
2. `project_context/START_HERE.md` — complete replacement.
3. `project_context/PROJECT_STATE.md` — complete replacement.
4. `project_context/DECISION_LOG.md` — complete replacement.
5. `project_context/ARTIFACT_INDEX.md` — complete replacement.
6. `project_context/S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_02.json` — new package control.
7. `project_context/S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_SHA256SUMS_CANDIDATE_02.txt` — new acyclic checksum control.

Review-only members:

1. `review_only/HANDOFF_PROFESSOR_S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_CANDIDATE_02.md`;
2. `review_only/CHANGED_PATH_MATRIX_S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_CANDIDATE_02.csv`.

The review ZIP contains no K014, K015, K016, implementation source, test source,
test result, imported project output, local research data, raw network response,
empirical evidence, research artifact, Git object, repository metadata, or
canonical installation action.

## Exact preserved implementation matrix

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

Binding model: `REVIEW_ZIP_EXTERNAL_SIDECAR_V1`.

1. The checksum inventory hashes all five substantive candidate files and both
   review-only files.
2. The checksum inventory excludes itself and the canonical package manifest.
3. The canonical package manifest inventories every ZIP member, including
   itself.
4. The manifest's own member entry has `byte_length = null`, `sha256 = null`,
   and `self_identity = null`; it is a membership declaration and not a
   self-hash.
5. The canonical package manifest's top-level `self_identity` remains `null`.
6. The external `.zip.sha256` sidecar binds the final sealed ZIP bytes.
7. No ZIP member contains the final ZIP hash.
8. The identity graph remains acyclic because the manifest carries no raw
   identity for itself and the checksum inventory excludes both controls.

This produces an acyclic identity chain:

```text
substantive files + changed-path matrix
  -> review handoff
  -> checksum inventory
  -> package manifest inventory of all ZIP members
     (manifest self-entry has null identity fields)
  -> ZIP
  -> external SHA-256 sidecar
```

## Lifecycle status

- K012 Sentinel review: pending.
- K012 canonical installation authorization: absent.
- K012 installation and verification: absent.
- K012 consumability: absent.
- K014/K015/K016: absent.
- implementation source: absent.
- test source and execution: absent.
- project/research artifact generation: absent.
- Git activity: absent.

Requested Sentinel decision:
`APPROVE — S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_CANDIDATE_01_ACCEPTED`.
