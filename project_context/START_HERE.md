# START HERE

*First file to read in every new project chat.*

---

## Rule 0 — canonical source

The private canonical repository is `rigolugo/pm_research`. Canonical repository bytes,
accepted specifications, Sentinel decisions, authorization records, manifests,
and verification records control over chat history, memory, archives, uploaded
duplicates, and public mirrors.

## Required read order

Read these before doing anything:

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
    - after exact K013 installation verification, the proposed K012 review material:
      - `../nodes/K012/artifact.json`
      - `S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_02.json`
      - `S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_SHA256SUMS_CANDIDATE_02.txt`
12. For Revision 23 / Finding 4, enter through
    `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md` and follow
    every nested accepted read order.
13. Follow every additional canonical read order referenced by the governing
    entry points.

## Current S2 Candidate 08 authorization state

Canonical `main` inspected for this candidate:

`6c891a61e7408f7977b72b2ccf52472412cd7e04`

Exact installed prerequisites:

| Node | Path | Bytes | SHA-256 | State |
|---|---|---:|---|---|
| `K011` | `nodes/K011/artifact.json` | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | accepted |
| `A010` | `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md` | `135500` | `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950` | accepted, installed, Sentinel-verified |
| `K013` | `nodes/K013/artifact.json` | `3099` | `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c` | accepted, installed at `6c891a61e7408f7977b72b2ccf52472412cd7e04`, exact installation identity independently verified |

Fresh proposed K012 Candidate 01:

- path: `nodes/K012/artifact.json`;
- byte length: `3449`;
- SHA-256: `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c`;
- schema/profile: `pm_research.s2.sentinel_authorization.v1` /
  `sentinel_authorization.v1`;
- rank: `1130`;
- semantic role: `sentinel_implementation_source_authorization`;
- ordered direct predecessors: exactly `[K011, A010, K013]`;
- created after exact K013 bytes;
- status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`;
- candidate-preparation authorization effect: `NONE`.

K012 is not accepted, canonically installed, canonically verified, effective, or
consumable. Its payload cannot be used without independent Sentinel acceptance
and every required installation and verification boundary. K014, K015, and K016
remain unmaterialized. Implementation-source authoring has not begun.

## Exact implementation-source matrix preserved by proposed K012

The package model remains the regular package at
`pm_research/named_binary_probe_s2`. A `src/` layout, namespace-package
redesign, `pyproject.toml` modification, additional path, removed path, renamed
path, relocated path, or role reassignment is forbidden.

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

## Required lifecycle order

```text
accepted K011
  -> accepted and canonically verified A010
  -> exact accepted, installed, and verified K013
  -> fresh K012 review candidate
  -> Sentinel acceptance and any required K012 installation/verification
  -> separately prepared K014
  -> K015/K016
```

This package stops before K014. It contains no implementation source.

## Preserved research and authorization gates

- P0 remains accepted with final eligible universe `39,693`.
- P1 remains blocked on an accepted per-side token-identity decision-time price artifact.
- P2 and P3 remain unauthorized.
- `named_binary_probe_blocked = true`.
- Scoring and probe execution remain unauthorized.
- `yes_price`, `1 - price`, `1 - yes_price`, and complement synthesis remain prohibited.
- No S2 per-token price artifact is accepted.
- Test source, tests, imports, local research-data access, subprocess execution,
  networking, empirical activity, research-artifact generation, canonical
  installation, and Git activity remain unauthorized by this candidate package.

## Working discipline

- Verify exact paths, bytes, hashes, schemas, ranks, roles, ordering, and authorization boundaries.
- Candidate preparation is not Sentinel acceptance.
- A stage-authorization candidate is not an activity root.
- K014 is required before implementation-source activity can begin.
- Professor does not approve its own work.
- Claude receives only Sentinel-accepted and Gustavo-authorized scope.

Requested Sentinel decision:
`APPROVE — S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_CANDIDATE_01_ACCEPTED`
