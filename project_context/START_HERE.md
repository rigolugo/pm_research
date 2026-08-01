# START HERE

*First file to read in every new project chat.*

---

## Rule 0 — canonical source

The private canonical repository is:

`rigolugo/pm_research`

Old chats, memory, uploaded duplicates, archived files, and public mirrors are non-authoritative. Exact canonical paths, bytes, hashes, schemas, decisions, and authorization records control.

---

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
10. The accepted price-source specifications and result handoffs relevant to the task.
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
    - `../nodes/K013/artifact.json` only after the exact Candidate-04 and A010 verification material above.
12. For Revision 23 / Finding 4, enter through `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md` and follow every nested accepted read order.
13. Follow every additional handoff, accepted-scope, checkpoint, remediation, provenance-capture, starting-state, workspace-preparation, and authorization read order referenced by the governing entry points.

---

## Current S2 Candidate 08 authorization state

Candidate 08 is accepted through K011. The installed Implementation-Source Amendment 01 remains SPEC-only. Candidate-04 is accepted SPEC-only and canonically installed at:

`a34636a89ec6ba557764cb32cbb0deed5b46df94`

The exact installed Candidate-04 Markdown is the A010 raw governance artifact:

- path: `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md`;
- byte length: `135500`;
- SHA-256: `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950`;
- profile: `amendment_governance.v1`;
- rank: `1115`;
- direct predecessors: exactly `[K011]`;
- separate `nodes/A010/artifact.json`: prohibited and absent.

Sentinel accepted `A010_CANONICAL_INSTALLATION_VERIFIED` at exact canonical verification commit:

`0b755fb71175370638ec87175aee85cf4710f54d`

The authoritative K011 identity is:

- path: `nodes/K011/artifact.json`;
- byte length: `1134`;
- SHA-256: `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`.

Fresh proposed K013 Candidate 01 now exists only as a sealed review-package member:

- path: `nodes/K013/artifact.json`;
- byte length: `3099`;
- SHA-256: `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c`;
- profile: `gustavo_authorization.v1`;
- rank: `1120`;
- semantic role: `gustavo_implementation_source_authorization`;
- exact direct predecessors: `[K011, A010]`;
- status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`;
- authorization effect of candidate preparation: `NONE`.

K013's proposed future scope is implementation-source authoring only for the exact accepted fourteen-file matrix. Candidate preparation itself does not activate that scope.

K013 has no independently consumable implementation effect until all of the following occur:

1. Sentinel accepts the exact K013 bytes;
2. Gustavo separately authorizes canonical installation where required;
3. the exact installed K013 identity is canonically verified;
4. fresh K012 is created after the exact K013 bytes exist;
5. fresh K014 binds K011, A010, K013, and K012;
6. every remaining activity boundary is separately authorized.

K012, K014, K015, and K016 remain unmaterialized and unauthorized.

---

## Exact future implementation-source matrix

The package model remains a regular package at `pm_research/named_binary_probe_s2`. A `src/` layout, namespace-package redesign, `pyproject.toml` modification, additional implementation path, or matrix reduction is forbidden.

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

---

## Required lifecycle state

1. Candidate-04 specification acceptance is complete.
2. Candidate-04 canonical installation at `a34636a89ec6ba557764cb32cbb0deed5b46df94` is complete.
3. Sentinel's accepted finding `A010_CANONICAL_INSTALLATION_VERIFIED` is bound to exact canonical verification commit `0b755fb71175370638ec87175aee85cf4710f54d`.
4. Fresh K013 Candidate 01 has been prepared only as a review candidate.
5. K013 is not accepted, canonically installed, canonically verified, effective, consumable, or independently implementation-authorizing.
6. K012, K014, K015, and K016 remain unmaterialized and unauthorized.
7. Implementation-source authoring has not begun and is not authorized by candidate preparation.
8. Test-source authoring, tests, project imports, local research-data access, subprocess execution, networking, vendor/API/RPC/Polymarket access, empirical execution, artifact generation, and canonical or Git activity remain unauthorized.
9. The exact fourteen-file implementation matrix and all accepted architectural restrictions remain unchanged.
10. `named_binary_probe_blocked = true`.
11. P1 remains blocked.
12. P2 and P3 remain unauthorized.
13. `yes_price`, `1 - price`, `1 - yes_price`, and any complement synthesis remain prohibited.

---

## Current research gates

- P0 preflight: **ACCEPTED — `P0_CLEAR`**.
- Final P0 eligible universe: `39,693`.
- P0 representativeness: **ACCEPTED — `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`**.
- P1: **BLOCKED** on an accepted per-side, token-identity decision-time price artifact.
- P2 and P3: **UNAUTHORIZED**.
- Scoring and probe execution: **UNAUTHORIZED**.
- `named_binary_probe_blocked = true`.
- `yes_price`, `1 - price`, `1 - yes_price`, and complement synthesis are prohibited.
- Historical S1 `interval=max`, fidelity-omitted method: `S1_SOURCE_NOT_VIABLE`.
- Revised `fidelity=1`, interval-omitted method: `S1_SOURCE_VIABLE` only for the existing stratified Pass-1 sample and reviewed EC2 route; not full-universe validation and not price-artifact acceptance.
- No S2 per-token price artifact is accepted.

---

## Working discipline

- Verify exact paths, bytes, hashes, schemas, and authorization boundaries.
- Candidate preparation, package sealing, checksum validation, specification acceptance, or documentation installation does not authorize implementation.
- Implementation-source authorization does not authorize tests, imports, data access, networking, execution, or downstream stages.
- Canonical changes are prepared as complete candidate files for Sentinel review and Gustavo-controlled installation.
- Professor does not approve its own work.
- Claude receives only Sentinel-accepted and Gustavo-authorized scope.
- Never silently reverse a settled decision or reopen a closed finding.

Requested Sentinel decision: APPROVE — S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_CANDIDATE_01_ACCEPTED
