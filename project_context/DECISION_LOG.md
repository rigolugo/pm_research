# DECISION LOG

*Corrected history and settled decisions. Do not re-litigate settled items without new authoritative evidence.*

---

## P0 CLOB canary and network-sensitivity decisions

### Dry-run reconciliation accepted

The documentation record preserves the accepted dry-run state:

- `final_p0_rows_loaded = 39,693`;
- `token_pair_clear_conditions = 39,693`;
- `request_eligible_conditions = 18,624`;
- `request_eligible_token_sides = 37,248`;
- `INVALID_DECISION_WINDOW = 21,069`;
- `REQUEST_ELIGIBLE = 18,624`;
- `executed_requests = 0`.

The reconciliation invariant is:

`21,069 + 18,624 = 39,693`

The dry-run did not execute network requests, construct an S2 artifact, or change any gate.

### First bounded 100-request canary accepted

Exact script identity:

`4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00`

Accepted result:

- executed requests: `100`;
- HTTP 200: `17`;
- HTTP 500: `73`;
- HTTP NONE: `10`;
- `TRANSPORT_OK = 17`;
- `TRANSPORT_HTTP_ERROR = 73`;
- `TRANSPORT_CONNECTION_ERROR = 9`;
- `TRANSPORT_TIMEOUT = 1`;
- `SERIES_PRESENT = 17`;
- `in_window_present_sides = 17`;
- `condition_both_sides_present = 0`;
- source viability: `NOT ESTABLISHED`.

### Repeat bounded 100-request canary on a new network accepted

The repeat verified canonical base `e675a47ec2c8f6cd769c2673afc16d96e5622ccd` and used the same script SHA-256.

Accepted result:

- executed requests: `100`;
- `HTTP 200 = 100`;
- `TRANSPORT_OK = 100`;
- `SERIES_PRESENT = 100`;
- `IN_WINDOW_PRESENT = 100`;
- `condition_both_sides_present = 50`;
- `error_response_count = 0`;
- `malformed_response_count = 0`.

### Accepted finding and limitation

The repeat canary supports network/environment sensitivity of the first failure pattern. The CLOB route is not dead.

P0-scale source viability remains `NOT ESTABLISHED`. Only `100 / 37,248` request-eligible token sides were tested. No inference from the repeat canary may widen the tested denominator, establish full-universe coverage, accept a price artifact, unblock P1, or clear an S2 gate.

### Candidate 02 failure-characterization design

The Candidate 02 failure-characterization design is accepted as SPEC-only.

Authorization effect:

`NONE`

Its acceptance does not authorize implementation-source authoring, test-source authoring, tests, project imports, local-data reads, network execution, raw-save activity, a full diagnostic, Git writes, S2 artifact construction, P1/P2/P3, scoring, probe execution, or gate changes.

---

## S2 Candidate 08 decisions

### Candidate 08 specification acceptance

Sentinel accepted `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08` as the controlling executable-level S2 specification.

Accepted identities:

- K008 specification: `776003` bytes, SHA-256 `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63`;
- K009 Professor review handoff: `13549` bytes, SHA-256 `720f2f081fa1f127fadc980702dd072f52a3714a14f7db418489862d14a609f1`;
- K010 Sentinel review: `1504` bytes, SHA-256 `e34ddcf51b8b908570de9b4cd4af520114e46bc848cfc00110bf4874dfafa17b`;
- K011 specification acceptance: `1134` bytes, SHA-256 `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f264`;
- A002 prerequisite: `5854` bytes, SHA-256 `87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c`.

Authorization effect remained `NONE`. Specification acceptance did not authorize implementation, tests, execution, data access, networking, Git activity, P1/P2/P3, scoring, probe execution, or gate changes.

### S2 Candidate 08 Implementation-Source Amendment 01 acceptance

Sentinel decision:

`APPROVE — S2 Candidate 08 Implementation-Source Amendment 01 accepted as a SPEC-only amendment`

Accepted amendment identity:

- canonical path after installation: `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
- submitted package path: `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
- byte length: `24599`;
- SHA-256: `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63`;
- authorization effect: `NONE`.

The amendment resolves the accepted finding:

`ACCEPT FINDING — S2_IMPLEMENTATION_SOURCE_AUTHORIZATION_BLOCKED_BY_PATH_LAYOUT_AND_REGISTRY_PROVENANCE`

Resolved defects:

1. package-layout/path-boundary defect;
2. registry-provenance ambiguity;
3. K015 ordering ambiguity;
4. K016 self-identity ambiguity;
5. incorrect Appendix-A matrix citation.

Accepted Amendment 01 facts:

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

No stale, pre-amendment, chat-only, or matrix-mismatched K013/K012/K014 may be reused.

Authorization effect: `NONE`.

---

## Settled named-binary decisions

### Semantics and realized outcomes

Named-binary orientation is accepted and must not be re-derived.

The local resolution store is YES/NO-only. Non-YES/NO outcomes are accepted from the Dune payout-vector pipeline:

- resolved single winners: `39,693`;
- ambiguous multiple-winner exclusions: `253`;
- non-YES/NO branch: `CLEAR_WITH_WARNINGS`;
- legacy pooled-all gate: `BLOCKED_BY_RESOLUTION_MAPPING`.

The source is usable for outcome mapping but does not authorize a probe.

`named_binary_probe_blocked = true`.

### P0 and P1

P0 is accepted as `P0_CLEAR` with final eligible count `39,693`.

The representativeness audit is accepted as `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`.

Neither result authorizes P1, pricing, scoring, wallet work, or probe execution.

P1 remains blocked on a two-side price source. `yes_price`, `1 - price`, and `1 - yes_price` are prohibited as named-binary unblock paths.

---

## Price-source decisions

### S1 CLOB `/prices-history`

Historical accepted sampled result for `interval=max` with fidelity omitted:

`S1_SOURCE_NOT_VIABLE`

The revised reviewed EC2 method using `fidelity=1` with interval omitted is `S1_SOURCE_VIABLE` only for the existing stratified Pass-1 sample and reviewed EC2 route. It is not full-universe validation and does not accept a price artifact.

### Other source decisions

- S1-ALT local trade prints: `S1ALT_SOURCE_NOT_VIABLE`.
- Option B corrected B0: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`; B1 remains unauthorized.
- Option C is not accepted as viable; C1B/C2 remain unauthorized.
- Option D temporal feasibility is accepted only as timing evidence; vendor coverage requires separate SPEC-only review.

---

## Revision 23 lifecycle decisions

Revision 23 with Amendments 01–03 and Finding 4 is accepted and installed under:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

Revision 10 remains the controlling accepted scope. Historical Revision 08 and Revision 09 implementation authorizations are inactive and do not carry forward.

The preserved checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` remains evidence-only and non-authorizing.

---

## Non-authorization standing rule

Documentation acceptance, specification acceptance, amendment acceptance, package preparation, checksum validation, static review, or canonical documentation installation authorizes no implementation-source authoring, test-source authoring, tests, project imports or execution, local research-data reads, network/API/RPC/vendor/Dune/curl/endpoint activity, raw-response saving, a full diagnostic, empirical artifacts, dependency or packaging changes, P1/P2/P3, scoring, probe execution, gate changes, Git writes, or downstream stages unless a later exact Gustavo authorization and Sentinel stage authorization explicitly create that scope.
