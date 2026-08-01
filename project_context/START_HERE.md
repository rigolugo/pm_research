# START HERE

*First file to read in every new project chat.*

---

## Rule 0 — canonical source

The private canonical repository is `rigolugo/pm_research`. Canonical repository bytes,
accepted specifications, Sentinel decisions, authorization records, manifests,
and verification records control over chat history, memory, archives, uploaded
duplicates, and public mirrors.

## Required read order

1. `GUARDRAILS.md`
2. `PROJECT_STATE.md`
3. `DECISION_LOG.md`
4. `CLOSED_FINDINGS.md`
5. `ARTIFACT_INDEX.md`
6. `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`
7. `DATA_CONTRACTS_named_binary_probe.md`
8. `PRICE_INPUT_CONTRACT_named_binary_probe.md`
9. `SPEC_named_binary_probe.md`
10. Accepted price-source specifications and result handoffs relevant to the task.
11. For S2 Candidate 08, read in this exact order:
    - `S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md`
    - `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md`
    - `HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md`
    - `../nodes/K010/artifact.json`
    - `../nodes/K011/artifact.json`
    - `S2_CANDIDATE_08_CANONICAL_INSTALLATION_PACKAGE_MANIFEST_01.json`
    - `S2_CANDIDATE_08_CANONICAL_INSTALLATION_PACKAGE_SHA256SUMS_01.txt`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_CANONICAL_INSTALLATION_RECORD.md`
    - `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_CANONICAL_INSTALLATION_RECORD.md`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_DOCUMENTATION_INSTALLATION_PACKAGE_MANIFEST.json`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_DOCUMENTATION_INSTALLATION_PACKAGE_SHA256SUMS.txt`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_POST_INSTALLATION_VERIFICATION_RECORD_CANDIDATE_01.md`
    - `../nodes/K013/artifact.json`
    - `S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_01.json`
    - `../nodes/K012/artifact.json`
    - `S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_02.json`
    - `S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_SHA256SUMS_CANDIDATE_02.txt`
    - after exact K012 installation verification, the proposed K014 review material:
      - `../nodes/K014/artifact.json`
      - `S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_01.json`
      - `S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_DOCUMENTATION_GOVERNANCE_PACKAGE_SHA256SUMS_CANDIDATE_01.txt`
12. For Revision 23 / Finding 4, enter through
    `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md` and follow
    every nested accepted read order.
13. Follow every additional canonical read order referenced by the governing entry points.

## Current S2 Candidate 08 authorization state

Canonical `main` verified for this candidate: `0872d4578fd2c0fc5147c77af606b9f807c7bc2b`.

| Node | Path | Bytes | SHA-256 | Rank | Ordered direct predecessors | State |
|---|---|---:|---|---:|---|---|
| `K011` | `nodes/K011/artifact.json` | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | acceptance | accepted chain | accepted |
| `A010` | `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md` | `135500` | `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950` | `1115` | `[K011]` | accepted, installed, verified |
| `K013` | `nodes/K013/artifact.json` | `3099` | `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c` | `1120` | `[K011, A010]` | accepted, installed at `6c891a61e7408f7977b72b2ccf52472412cd7e04`, verified |
| `K012` | `nodes/K012/artifact.json` | `3449` | `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c` | `1130` | `[K011, A010, K013]` | accepted, installed at `0872d4578fd2c0fc5147c77af606b9f807c7bc2b`, verified |

K013 and K012 both embed `0b755fb71175370638ec87175aee85cf4710f54d`. `0872d4578fd2c0fc5147c77af606b9f807c7bc2b` identifies repository
installation/preparation state and does not replace that embedded contract commit.

## Fresh proposed K014 Candidate 01

- path: `nodes/K014/artifact.json`;
- bytes: `4302`;
- SHA-256: `7d54c1cabd1be53abc677425e5b7ce781d362bef2918c31bd844a0fa316b9fc2`;
- Git blob: `cc35df982377286e0940c9dddd5cee01a51e4ace`;
- schema/profile: `pm_research.s2.activity_root.v1` / `activity_root.v1`;
- rank: `1140`;
- semantic role: `implementation_source_activity_root`;
- ordered direct predecessors: `[K011, A010, K013, K012]`;
- `created_at_utc_ms`: `1785598380000`;
- embedded `canonical_commit`: `0b755fb71175370638ec87175aee85cf4710f54d`;
- status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`;
- candidate-preparation authorization effect: `NONE`.

K014 is not accepted, installed, verified, effective, or consumable. K015 and
K016 remain unmaterialized. Implementation-source authoring has not begun.

## Exact K014 scope

Input roots:

- `nodes/K011/artifact.json`
- `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md`
- `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md`
- `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`

Output root: `pm_research/named_binary_probe_s2`.

| # | Allowed deliverable | Role | Language | Required |
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

No fifteenth source file, `src/` layout, namespace-package design,
`pyproject.toml` change, path rename, relocation, matrix reduction, or role
reassignment is permitted.

## Required lifecycle order

```text
K011 accepted
  -> A010 accepted, installed, verified
  -> K013 accepted, installed, verified
  -> K012 accepted, installed, verified
  -> K014 review candidate
  -> Sentinel acceptance
  -> separate Gustavo installation authorization
  -> exact installed K014 verification
  -> separate bounded Sentinel implementation handoff
  -> K015/K016
```

Candidate preparation does not activate Claude and does not authorize implementation.

## Preserved research and authorization gates

- P0 remains accepted with final eligible universe `39,693`.
- P1 remains blocked; P2 and P3 remain unauthorized.
- `named_binary_probe_blocked = true`.
- No accepted S2 per-token price artifact exists.
- Scoring and probe execution remain unauthorized.
- Complement synthesis remains prohibited.
- Test source, tests, imports, local research-data access, subprocess execution,
  networking, empirical execution, research-artifact generation, canonical
  installation, and Git activity remain unauthorized by this candidate.

Requested Sentinel decision:
`APPROVE — S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_CANDIDATE_01_ACCEPTED`.
