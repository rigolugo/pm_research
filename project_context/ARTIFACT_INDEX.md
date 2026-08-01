# ARTIFACT INDEX

*Canonical and proposed artifact identities. Repository paths are relative to `rigolugo/pm_research`.*

---

## Fresh K013 Candidate 01 review package

### Proposed canonical node

- path: `nodes/K013/artifact.json`;
- node ID: `K013`;
- record ID: `S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_CANDIDATE_01`;
- byte length: `3099`;
- SHA-256: `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c`;
- schema/profile: `pm_research.s2.gustavo_authorization.v1` / `gustavo_authorization.v1`;
- rank: `1120`;
- semantic role: `gustavo_implementation_source_authorization`;
- direct predecessors: exactly `[K011, A010]`;
- status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`;
- canonical repository membership: `NO`;
- authorization effect of preparation: `NONE`.

The proposed node is fresh after exact A010 verification. No pre-A010, stale, reply-only, chat-only, or historical K013 artifact was reused.

### Proposed documentation/governance package

Package ID:

`S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_CANDIDATE_01`

Exactly seven proposed canonical paths:

1. `nodes/K013/artifact.json` — NEW.
2. `project_context/START_HERE.md` — COMPLETE REPLACEMENT from base blob `a02d2b3252e8c0f299fd925753829384c2eb9cdf`.
3. `project_context/PROJECT_STATE.md` — COMPLETE REPLACEMENT from base blob `77aae48dd9760d31dc0e13e249e77e5e1de226e1`.
4. `project_context/DECISION_LOG.md` — COMPLETE REPLACEMENT from base blob `e77b3f0f99a54fe90f4a5c4d38a67988947f106a`.
5. `project_context/ARTIFACT_INDEX.md` — COMPLETE REPLACEMENT from base blob `2ed5cb2061d7391e6fa7c53fa9a490d1e0ba0ebf`.
6. `project_context/S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_MANIFEST_CANDIDATE_01.json` — NEW package control.
7. `project_context/S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_DOCUMENTATION_GOVERNANCE_PACKAGE_SHA256SUMS_CANDIDATE_01.txt` — NEW package control.

The sealed review ZIP contains exactly these seven canonical candidates plus three review-only members. The binding model is `REVIEW_ZIP_EXTERNAL_SIDECAR_V1`. The external sidecar binds the final sealed ZIP bytes.

The proposed canonical package manifest has `self_identity = null`. The checksum record excludes itself and the canonical package manifest and verifies exactly the five substantive canonical payloads.

Candidate preparation, manifest generation, checksum generation, ZIP sealing, and sidecar generation have authorization effect `NONE`.

---

## K011 prerequisite identity

- node: `K011`;
- path: `nodes/K011/artifact.json`;
- byte length: `1134`;
- SHA-256: `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`;
- state: authoritative accepted Candidate-08 acceptance node.

---

## A010 prerequisite identity

- logical path: `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md`;
- byte length: `135500`;
- SHA-256: `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950`;
- profile: `amendment_governance.v1`;
- rank: `1115`;
- direct predecessors: exactly `[K011]`;
- canonical installation commit: `a34636a89ec6ba557764cb32cbb0deed5b46df94`;
- canonical verification commit: `0b755fb71175370638ec87175aee85cf4710f54d`;
- accepted finding: `A010_CANONICAL_INSTALLATION_VERIFIED`;
- separate `nodes/A010/artifact.json`: absent and not required;
- authorization effect: `NONE`.

---

## Exact future implementation-source matrix

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

Package restrictions remain exact:

- regular package under `pm_research/named_binary_probe_s2`;
- no `src/` layout;
- no namespace-package redesign;
- no `pyproject.toml` modification;
- no additional implementation path;
- no matrix reduction, expansion, or role reassignment.

No listed implementation file exists as a result of this package.

---

## Candidate-04 and Candidate-08 canonical layer

Accepted Candidate-08 identities:

- K008 specification: `776003` / `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63`;
- K009 handoff: `13549` / `720f2f081fa1f127fadc980702dd072f52a3714a14f7db418489862d14a609f1`;
- K010 review: `1504` / `e34ddcf51b8b908570de9b4cd4af520114e46bc848cfc00110bf4874dfafa17b`;
- K011 acceptance: `1134` / `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`.

Accepted Implementation-Source Amendment 01:

- path: `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
- byte length: `24599`;
- SHA-256: `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63`;
- authorization effect: `NONE`.

Candidate-04 effective-registry contract:

- immutable base registry: `479463` / `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`;
- exact overlay: `45347` / `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a`;
- effective bundle: `1266` / `075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67`;
- reducer projection: `66232` / `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`;
- effective graph: `167 / 683`;
- K127 population: `60`.

---

## Research artifacts and gates

Canonical named-binary research artifacts remain under:

- `artifacts/named_binary/`;
- `artifacts/named_binary_probe/`.

Accepted state remains:

- P0: `P0_CLEAR`;
- final P0 eligible: `39,693`;
- P0 representativeness: `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`;
- accepted per-token price artifact: `NONE`;
- P1: `BLOCKED`;
- P2 and P3: `UNAUTHORIZED`;
- scoring and probe execution: `UNAUTHORIZED`;
- `named_binary_probe_blocked = true`;
- complement-price synthesis: prohibited.

Historical and bounded P0/S1 evidence remains evidence only unless a separate acceptance record says otherwise.

---

## Lifecycle and authorization boundary

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

K013's proposed future implementation-source scope has no independently consumable effect until Sentinel acceptance, separately authorized installation, exact installed identity verification, fresh K012, fresh K014, and every remaining activity boundary.

No source ZIP, implementation source, test source, `.gitignore` change, runtime/dependency change, local research data, empirical output, raw response, Git object, repository metadata, or generated research artifact is a member of this documentation/governance package.

Requested Sentinel decision: APPROVE — S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_CANDIDATE_01_ACCEPTED
