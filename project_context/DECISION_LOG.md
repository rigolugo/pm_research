# DECISION LOG

*Corrected history and settled decisions. Do not re-litigate settled items without new authoritative evidence.*

---

## S2 Candidate 08 specification decisions

Sentinel accepted `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08` as the controlling executable-level S2 specification.

Exact accepted identities:

- K008: `776003` bytes / `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63`;
- K009: `13549` bytes / `720f2f081fa1f127fadc980702dd072f52a3714a14f7db418489862d14a609f1`;
- K010: `1504` bytes / `e34ddcf51b8b908570de9b4cd4af520114e46bc848cfc00110bf4874dfafa17b`;
- K011: `1134` bytes / `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`.

Specification acceptance had authorization effect `NONE`.

### Implementation-Source Amendment 01

Sentinel accepted and canonical installation completed for the SPEC-only amendment:

- path: `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
- byte length: `24599`;
- SHA-256: `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63`;
- authorization effect: `NONE`.

The amendment settled the regular-package directory `pm_research/named_binary_probe_s2`, prohibited a `src/` layout, namespace-package behavior, and `pyproject.toml` changes, fixed K015 ordering, fixed K016 self-identity, and preserved the exact fourteen-file matrix.

---

## Candidate-04 authorization-graph decisions

Sentinel accepted:

`APPROVE — S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_ACCEPTED_SPEC_ONLY`

Exact Candidate-04 identity:

- path: `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md`;
- byte length: `135500`;
- SHA-256: `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950`;
- profile: `amendment_governance.v1`;
- authorization effect: `NONE`.

Settled graph behavior:

1. A010 is the exact installed Candidate-04 Markdown raw governance artifact.
2. A010 rank is `1115`.
3. A010 direct predecessors are exactly `[K011]`.
4. The accepted installed Implementation-Source Amendment 01 is closed non-edge governance data.
5. K013 direct predecessors are exactly `[K011, A010]`.
6. K012 will bind `[K011, A010, K013]` only after exact K013 bytes exist.
7. K014 will bind `[K011, A010, K013, K012]` only after exact K013 and K012 bytes exist.
8. K015 depends directly only on K014.
9. K016 retains the accepted direct predecessors and `/payload/self_identity = null`.
10. The effective graph remains `167` nodes / `683` direct edges with K127 population `60`.
11. The reducer projection and exact fourteen-file implementation matrix remain unchanged.

### Canonical installation and A010 verification

Candidate-04 canonical installation completed at:

`a34636a89ec6ba557764cb32cbb0deed5b46df94`

Sentinel accepted the finding:

`A010_CANONICAL_INSTALLATION_VERIFIED`

Exact canonical verification commit:

`0b755fb71175370638ec87175aee85cf4710f54d`

This accepted finding satisfies the A010 prerequisite for preparing fresh K013 bytes. It is not implementation authorization.

No `nodes/A010/artifact.json` is required or permitted.

---

## Fresh K013 Candidate 01 preparation decision boundary

Fresh K013 Candidate 01 has been prepared under:

`DOCUMENTATION_GOVERNANCE_CANDIDATE_PREPARATION_ONLY`

Exact proposed identity:

- path: `nodes/K013/artifact.json`;
- byte length: `3099`;
- SHA-256: `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c`;
- schema/profile: `pm_research.s2.gustavo_authorization.v1` / `gustavo_authorization.v1`;
- rank: `1120`;
- semantic role: `gustavo_implementation_source_authorization`;
- direct predecessors: exactly `[K011, A010]`;
- top-level status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`.

This is a candidate-preparation fact, not an acceptance decision. K013 is not accepted, installed, verified, effective, consumed, or independently implementation-authorizing.

The future proposed K013 scope is limited to implementation-source authoring for the exact fourteen-file matrix. It excludes test-source authoring, tests, project imports, local research-data reads, subprocesses, network/API/RPC/vendor/Polymarket activity, empirical runs, artifact generation, canonical installation, Git writes, P1/P2/P3, scoring, probes, and automatic gate changes.

The strongest alternative interpretation—that existence of candidate bytes activates implementation—is rejected. Candidate bytes are inert review material until all accepted lifecycle prerequisites are separately completed.

K013 has no independently consumable implementation effect until:

1. Sentinel accepts the exact K013 candidate;
2. Gustavo separately authorizes canonical installation where required;
3. exact installed K013 identity is canonically verified;
4. fresh K012 is created after exact K013 bytes exist;
5. fresh K014 binds K011, A010, K013, and K012;
6. every remaining activity boundary is separately authorized.

K012, K014, K015, and K016 remain unmaterialized and unauthorized.

Requested Sentinel decision: APPROVE — S2_CANDIDATE_08_K013_GUSTAVO_IMPLEMENTATION_SOURCE_AUTHORIZATION_CANDIDATE_01_ACCEPTED

Professor does not issue that decision.

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

The matrix is exact. No source path may be added, omitted, renamed, relocated, or reclassified by this candidate.

---

## P0 CLOB and price-source decisions

Accepted P0 dry-run reconciliation remains:

- final P0 rows: `39,693`;
- token-pair-clear conditions: `39,693`;
- request-eligible conditions: `18,624`;
- request-eligible token sides: `37,248`;
- invalid decision windows: `21,069`;
- executed requests in the dry run: `0`.

The accepted bounded P0 canary findings do not establish full-universe viability, accept a price artifact, or unblock P1.

Historical S1 CLOB `/prices-history` with `interval=max` and fidelity omitted remains `S1_SOURCE_NOT_VIABLE`.

The revised `fidelity=1`, interval-omitted method remains `S1_SOURCE_VIABLE` only for the reviewed 248-condition stratified sample and reviewed EC2 route. It is not full-universe validation and does not accept a price artifact.

---

## Settled named-binary decisions

- P0: `P0_CLEAR`.
- Final P0 eligible universe: `39,693`.
- P0 representativeness: `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`.
- P1: blocked.
- P2 and P3: unauthorized.
- Scoring: unauthorized.
- Probe execution: unauthorized.
- `named_binary_probe_blocked = true`.
- `yes_price`, `1 - price`, `1 - yes_price`, and complement synthesis are prohibited unblock paths.

---

## Revision 23 lifecycle decisions

Revision 23 with Amendments 01–03 and Finding 4 remains accepted and installed under:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

Revision 10 remains controlling. Historical Revision 08 and Revision 09 authorizations are inactive and do not carry forward.

The preserved R1 checkpoint remains evidence-only, `NOT_ACCEPTED`, and non-authorizing.

Static checkpoint conformance remains:

`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`

---

## Standing non-authorization rule

Documentation acceptance, specification acceptance, amendment acceptance, candidate preparation, package preparation, checksum validation, canonical documentation installation, or existence of a proposed authorization node does not itself authorize source authoring, test authoring, tests, project imports or execution, local research-data access, subprocesses, network/API/RPC/vendor activity, empirical work, artifact construction, P1/P2/P3, scoring, probe execution, gate changes, or Git activity.

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
