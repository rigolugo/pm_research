# ARTIFACT INDEX

*Canonical and proposed identities for the K014 post-installation and bounded
implementation-handoff canonicalization boundary.*

---

## Canonical base

- repository: `rigolugo/pm_research`;
- canonical `main`: `fc16e9124acb8acb490975c7289d8199b84f2c25`;
- task classification: `K014_POST_INSTALLATION_VERIFICATION_AND_IMPLEMENTATION_HANDOFF_CANONICALIZATION_CANDIDATE_PREPARATION_ONLY`;
- package-preparation authorization effect: `NONE`.

## Installed controlling artifacts

| Item | Path | Bytes | SHA-256 | State |
|---|---|---:|---|---|
| K011 | `nodes/K011/artifact.json` | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | accepted |
| A010 | `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md` | `135500` | `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950` | accepted, installed, verified |
| K013 | `nodes/K013/artifact.json` | `3099` | `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c` | accepted, installed, verified |
| K012 | `nodes/K012/artifact.json` | `3449` | `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c` | accepted, installed, verified |
| K014 | `nodes/K014/artifact.json` | `4302` | `7d54c1cabd1be53abc677425e5b7ce781d362bef2918c31bd844a0fa316b9fc2` | accepted, installed at `fc16e9124acb8acb490975c7289d8199b84f2c25`, verified |
| K008 | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md` | `776003` | `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63` | accepted |
| Amendment 01 | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md` | `24599` | `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63` | accepted, installed |

K014 Git blob: `cc35df982377286e0940c9dddd5cee01a51e4ace`.

## Proposed canonical package paths

Exactly eight proposed canonical paths:

1. `project_context/S2_CANDIDATE_08_K014_POST_INSTALLATION_VERIFICATION_RECORD_CANDIDATE_01.md`
2. `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORING_BOUNDED_SENTINEL_HANDOFF_RECORD_CANDIDATE_01.md`
3. `project_context/START_HERE.md`
4. `project_context/PROJECT_STATE.md`
5. `project_context/DECISION_LOG.md`
6. `project_context/ARTIFACT_INDEX.md`
7. `project_context/S2_CANDIDATE_08_K014_POST_INSTALLATION_VERIFICATION_AND_IMPLEMENTATION_SOURCE_HANDOFF_CANONICALIZATION_PACKAGE_MANIFEST_CANDIDATE_01.json`
8. `project_context/S2_CANDIDATE_08_K014_POST_INSTALLATION_VERIFICATION_AND_IMPLEMENTATION_SOURCE_HANDOFF_CANONICALIZATION_PACKAGE_SHA256SUMS_CANDIDATE_01.txt`

Review-only paths:

1. `review_only/HANDOFF_PROFESSOR_S2_CANDIDATE_08_K014_POST_INSTALLATION_VERIFICATION_AND_IMPLEMENTATION_SOURCE_HANDOFF_CANONICALIZATION_PACKAGE_CANDIDATE_02.md`
2. `review_only/CHANGED_PATH_MATRIX_S2_CANDIDATE_08_K014_POST_INSTALLATION_VERIFICATION_AND_IMPLEMENTATION_SOURCE_HANDOFF_CANONICALIZATION_PACKAGE_CANDIDATE_02.csv`

No source file, K015, K016, test, runtime artifact, Git metadata, or research
data is a package member.

## Proposed lifecycle

- verification record: candidate until separately installed;
- bounded Sentinel handoff: candidate until separately installed;
- implementation remains blocked until package acceptance, installation, and
  independent verification;
- after those boundaries, only exact fourteen-file source authoring and bounded
  K015/K016 completion become consumable;
- K015/K016 currently absent;
- implementation source currently absent.

## Exact future source matrix

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

1. The canonical manifest inventories all ten ZIP members, including itself.
2. Its own member entry has null byte length, null SHA-256, and null
   self-identity.
3. Top-level manifest self-identity is null.
4. The checksum inventory excludes itself and the manifest.
5. The checksum inventory covers the six substantive documentation files and
   both review-only files.
6. The external `.zip.sha256` sidecar binds final sealed ZIP bytes.
7. No ZIP member contains the final ZIP hash.
8. The identity graph is acyclic.

## Preserved gates

P0 remains accepted at `39,693`; P1 remains blocked; P2/P3 remain
unauthorized; `named_binary_probe_blocked = true`; tests, imports, data,
execution, network, subprocess, Git writes, scoring, probes, gate changes, and
complement synthesis remain unauthorized.

Requested Sentinel decision:
`APPROVE — S2_CANDIDATE_08_K014_POST_INSTALLATION_VERIFICATION_AND_IMPLEMENTATION_SOURCE_HANDOFF_CANONICALIZATION_PACKAGE_CANDIDATE_02_ACCEPTED`.
