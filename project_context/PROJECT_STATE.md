# PROJECT STATE

*Current objective, environment, active blockers, and authorization state.*

---

## Current objective

The current S2 objective is documentation-only canonical installation of the accepted S2 Candidate 08 Implementation-Source Amendment 01. The exact canonical base for this package is:

`ddf41003fb16aa091c2a899d7c17754e89341cc7`

This package is prepared under Gustavo authorization:

`S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_DOCUMENTATION_ONLY_INSTALLATION_PREPARATION_GUSTAVO_AUTHORIZATION_01`

It responds to Candidate 03 being blocked as:

`BLOCK — package manifest recorded SHA mismatch for its proposed canonical manifest`

Candidate 03 preserves Candidate 03's complete documentation-authority coverage and corrects only the package-integrity manifest/sidecar contradiction.

- `project_context/START_HERE.md`;
- `project_context/PROJECT_STATE.md`;
- `project_context/DECISION_LOG.md`;
- `project_context/ARTIFACT_INDEX.md`.

It also installs the accepted amendment text and a documentation-only installation record.


Candidate 05 package-integrity state:

- prior Candidate 04 block: `BLOCK — package incomplete because required external ZIP SHA-256 sidecar was not supplied, and proposed canonical files still refer to blocked Candidate 03 as the operative package/binding identity`;
- root ZIP SHA-256 sidecar is external, supplied outside the ZIP, and binds the final sealed Candidate 05 ZIP bytes;
- root manifest `self_identity = null`;
- root manifest member inventory lists every actual ZIP member except the root manifest exactly;
- no final ZIP hash is stored inside a ZIP member;
- proposed canonical manifest self-identity: `null`;
- proposed canonical sidecar/inventory scope: six canonical documentation payload files only;
- proposed canonical manifest and proposed canonical sidecar are externally bound control files through Candidate 05 and later Sentinel installation verification;
- no manifest or sidecar raw SHA-256 is embedded in its own bytes;
- Candidate 03 and Candidate 04 remain blocked historical predecessor evidence only and are not operative package identities.


---

## S2 per-token price-artifact specification state

Sentinel accepted `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08` as the controlling executable-level S2 specification.

Accepted documentation identities:

- K008 specification: `776003` bytes, SHA-256 `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63`;
- K009 Professor review handoff: `13549` bytes, SHA-256 `720f2f081fa1f127fadc980702dd072f52a3714a14f7db418489862d14a609f1`;
- K010 Sentinel review: `1504` bytes, SHA-256 `e34ddcf51b8b908570de9b4cd4af520114e46bc848cfc00110bf4874dfafa17b`;
- K011 specification acceptance: `1134` bytes, SHA-256 `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f264`.

Accepted prerequisite architecture:

- path: `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md`;
- byte length: `5854`;
- SHA-256: `87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c`.

Candidate 08 remains accepted but not implemented. No implementation source, implementation candidate, test source, executed tests, empirical artifacts, accepted per-token price artifact, or downstream phase exists. Implementation authorization is `NONE`.

### S2 Candidate 08 Implementation-Source Amendment 01

Amendment 01 is accepted as a SPEC-only amendment after this documentation installation.

Accepted amendment identity:

- canonical path: `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
- byte length: `24599`;
- SHA-256: `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63`;
- Sentinel decision: `APPROVE — S2 Candidate 08 Implementation-Source Amendment 01 accepted as a SPEC-only amendment`;
- authorization effect: `NONE`.

The amendment resolves only:

- package-layout/path-boundary defect;
- registry-provenance ambiguity;
- K015 ordering ambiguity;
- K016 self-identity ambiguity;
- incorrect Appendix-A matrix citation.

Accepted Amendment 01 implementation-source facts:

- selected future implementation package: `pm_research.named_binary_probe_s2`;
- selected future repository directory: `pm_research/named_binary_probe_s2/`;
- future implementation-source matrix: exactly fourteen files under that directory;
- `src/` layout forbidden;
- namespace package behavior forbidden;
- `pyproject.toml` changes forbidden for this stage;
- K016 `/payload/self_identity = null`;
- accepted Candidate-08 §23 JCS: `479463` bytes / `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`;
- reducer projection: `66232` bytes / `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`.

Future source authoring requires a fresh post-installation chain:

`K011 + accepted installed amendment → fresh K013 → fresh K012 → fresh K014 → K015/K016`

No stale, pre-amendment, or chat-only K013/K012/K014 may be reused.

Exact future implementation-source matrix:

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

---

## Named-binary research state

### Semantics and realized outcomes

- Named-binary semantics/orientation: accepted and must not be re-derived.
- Orientation correctness: `1.0`.
- Token identity coverage: `0.99601`.
- YES/NO local resolutions: `8,521 / 8,521`.
- Non-YES/NO realized outcomes: accepted Dune payout-vector source.
- Resolved single-winner rows: `39,693`.
- Ambiguous multiple-winner exclusions: `253`.
- Non-YES/NO branch gate: `CLEAR_WITH_WARNINGS`.
- Legacy pooled-all gate: `BLOCKED_BY_RESOLUTION_MAPPING`.
- `named_binary_probe_blocked = true`.

### P0 and P1

- P0 preflight: `P0_CLEAR`.
- Final P0 eligible universe: `39,693`.
- Subclasses: UP_DOWN `22,012`; OVER_UNDER `1,003`; NAMED_OTHER `16,678`.
- P0 representativeness result: `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`.
- P1 remains blocked because no accepted per-side/token-identity decision-time price artifact exists.
- `yes_price`, `1 - price`, and `1 - yes_price` are prohibited as named-binary unblock paths.

---

## Price-source candidate state

### S1 — CLOB `/prices-history`

Historical `interval=max`, fidelity-omitted method remains `S1_SOURCE_NOT_VIABLE`.

The revised reviewed EC2 method used one independently queried token ID per side, `startTs = decision_lower_ts - 1`, `endTs = resolved_at_ts`, `fidelity=1`, `interval` omitted, zero retries, no side synthesis, and the unchanged half-open evaluation window `decision_lower_ts <= t < resolved_at_ts`.

The revised method establishes `S1_SOURCE_VIABLE` only for the existing stratified Pass-1 sample and reviewed EC2 route: UP_DOWN `50/50`, OVER_UNDER `98/98`, NAMED_OTHER `100/100`, combined `248/248`. This is not full-universe validation and is not price-artifact acceptance.

No S2/Pass 2, full-universe request, price-artifact construction, P1/P2/P3, scoring, probe execution, further networking, local-data execution, implementation, test, or gate change is authorized.

### S1-ALT, Option B, Option C, Option D

- S1-ALT local trade prints: `S1ALT_SOURCE_NOT_VIABLE`.
- Option B corrected B0: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`; B1 unauthorized.
- Option C: original C1A halt `C1_ROW_EXPLOSION` accepted; C1A-F1 mixed diagnostic evidence only; C1A-F2 `C1F2_ARTIFACTS_INSUFFICIENT`; C1B/C2 unauthorized.
- Option D temporal in-range precheck accepted; Telonex L2 may only proceed through a separately authorized SPEC-only vendor-coverage review.

---

## Revision 23 Finding 4 contract state

Revision 23 with Amendments 01–03 and Finding 4 is accepted and installed. The installed contract and Finding 4 audit trail live under:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

Revision 10 is accepted and Sentinel-verified. Historical Revision 08 and Revision 09 implementation authorizations remain inactive and do not carry forward.

The recovered R1 checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` remains evidence-only, `NOT_ACCEPTED`, non-controlling, and non-authorizing.

Static checkpoint conformance remains:

`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`

---

## Implementation authorization state

Implementation authorization remains `NONE` for S2 Candidate 08 and Amendment 01.

This documentation package authorizes no implementation-source authoring, test-source authoring, test execution, project imports or execution, compilation, linting, type checking, coverage, local research-data reads, network/API/RPC/vendor/Dune/curl/endpoint activity, dependency or packaging changes, acquisition, construction, alignment, rebuild, audit, transition, empirical work, P1/P2/P3, scoring, probe execution, gate changes, Git commit, push, merge, branch, tag, release, ref update, or canonical installation itself.

---

## Working discipline

- Verify exact paths, bytes, hashes, schemas, and authorization boundaries.
- Passing tests do not prove correctness when tests encode the wrong contract.
- Specification acceptance does not authorize implementation.
- Implementation acceptance does not authorize tests or execution.
- Canonical project-document changes are prepared as complete files and uploaded manually by Gustavo.
- Never silently reverse a settled decision or reactivate superseded material.
