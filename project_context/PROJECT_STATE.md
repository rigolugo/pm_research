# PROJECT STATE

*Current objective, environment, active blockers, and authorization state.*

---

## Current objective

The current authorized activity is preparation of the documentation-only
post-installation verification package:

`S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_POST_INSTALLATION_VERIFICATION_DOCUMENTATION_PACKAGE_CANDIDATE_01`

Exact package-authoring base and verified canonical `main`:

`a34636a89ec6ba557764cb32cbb0deed5b46df94`

The package proposes exactly seven canonical documentation paths: one new
post-installation verification record, four complete documentation
replacements, and two new package-control files. The sealed review ZIP contains
exactly ten members: those seven canonical candidates plus one Professor
handoff, one changed-path matrix, and one root review manifest. It contains no
`nodes/A010/artifact.json`.

Candidate-04 specification acceptance, documentation-installation-package
acceptance, temporary branch creation, the exact eight-path branch commit,
temporary-branch push and Sentinel branch verification, consumed Gustavo merge
authorization, and ordinary one-commit fast-forward installation into canonical
`main` are complete. The canonical Git installation commit is
`a34636a89ec6ba557764cb32cbb0deed5b46df94`, directly above
`90c0059c0e86b7afd44fcf9f17223d68eab1a9e0`.

The bounded Git finding is
`CANDIDATE_04_CANONICAL_GIT_INSTALLATION_COMPLETE`. This post-installation
verification package remains a review candidate. It requests, but does not
issue:

`ACCEPT FINDING — A010_CANONICAL_INSTALLATION_VERIFIED`

A010 downstream graph consumption remains blocked until Sentinel accepts this
package and later verifies its exact canonical installation. Fresh K013
preparation and K012/K014/K015/K016 remain unauthorized and unmaterialized.

Authorization effect:

`NONE`

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

Candidate 08 remains accepted but not implemented. No S2 Candidate 08 implementation source, S2 implementation candidate, S2 test source, executed S2 tests, accepted per-token price artifact, or downstream phase exists. The separately accepted P0 CLOB Candidate 03 diagnostic source package is not S2 implementation source and does not change this state. S2 implementation authorization is `NONE`.

### S2 Candidate 08 Implementation-Source Amendment 01

Amendment 01 is accepted and canonically installed as a SPEC-only amendment.

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

Candidate 04 is accepted SPEC-only and canonically installed at
`a34636a89ec6ba557764cb32cbb0deed5b46df94`. The exact installed Markdown is
the A010 raw governance artifact. Formal downstream consumption remains blocked
until Sentinel accepts the post-installation verification package and later
verifies that package's exact canonical installation. The future authorization
chain does not currently exist and MUST be:

```text
accepted K011
  + accepted installed Implementation-Source Amendment 01
  + accepted and canonically verified A010
  -> fresh K013
  -> fresh K012
  -> fresh K014
  -> K015/K016
```

No stale pre-A010, pre-amendment, chat-only, or matrix-mismatched K013, K012,
or K014 may be reused.

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

### S2 Candidate 08 Authorization-Graph Amendment 01 Candidate 04

Sentinel accepted Candidate 04 as SPEC-only:

`APPROVE — S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04_ACCEPTED_SPEC_ONLY`

Exact accepted Markdown identity:

- canonical path: `project_context/S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04.md`;
- byte length: `135500`;
- SHA-256: `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950`;
- serialization: UTF-8, LF-only, no BOM, final newline;
- authorization effect: `NONE`.

The accepted governance design is exactly one A010 node at rank `1115` under
closed `amendment_governance.v1`. A010's direct predecessor set is exactly
`[K011]`. The accepted installed Amendment-01 identity and installation commit
`e675a47ec2c8f6cd769c2673afc16d96e5622ccd` are closed non-edge governance data.
No `nodes/A010/artifact.json` is required or permitted by this package.

Effective-registry identities remain:

- immutable base: `479463` / `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`;
- exact overlay: `45347` / `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a`;
- effective bundle: `1266` / `075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67`;
- reducer projection: `66232` / `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`;
- effective graph: `167` nodes / `683` direct edges;
- K127 ordered-evidence population: `60`.

Canonical Git installation of the exact Candidate-04 Markdown is complete at
`a34636a89ec6ba557764cb32cbb0deed5b46df94`; the bounded finding is
`CANDIDATE_04_CANONICAL_GIT_INSTALLATION_COMPLETE`. The post-installation
verification package requests
`ACCEPT FINDING — A010_CANONICAL_INSTALLATION_VERIFIED` but does not approve
itself. A010 downstream consumption, fresh K013, K012, K014, K015, and K016
remain blocked, unauthorized, or unmaterialized until Sentinel accepts the
package and later verifies its exact canonical installation. S2
implementation-source authorization remains `NONE`; no S2 implementation or
test source exists or is accepted.

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

### P0 CLOB canary and network-sensitivity state

Accepted dry-run reconciliation:

| Field | Count |
|---|---:|
| `final_p0_rows_loaded` | `39,693` |
| `token_pair_clear_conditions` | `39,693` |
| `request_eligible_conditions` | `18,624` |
| `request_eligible_token_sides` | `37,248` |
| `INVALID_DECISION_WINDOW` | `21,069` |
| `REQUEST_ELIGIBLE` | `18,624` |
| `executed_requests` | `0` |

Invariant: `21,069 + 18,624 = 39,693`.

Accepted first bounded canary:

- script SHA-256: `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00`;
- executed requests: `100`;
- HTTP 200 / 500 / NONE: `17 / 73 / 10`;
- transport OK / HTTP error / connection error / timeout: `17 / 73 / 9 / 1`;
- `SERIES_PRESENT = 17`;
- `in_window_present_sides = 17`;
- `condition_both_sides_present = 0`;
- source viability: `NOT ESTABLISHED`.

Accepted repeat bounded canary on a new network:

- canonical base verified: `true`;
- canonical commit: `e675a47ec2c8f6cd769c2673afc16d96e5622ccd`;
- same script SHA-256: `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00`;
- executed requests: `100`;
- `HTTP 200 = 100`;
- `TRANSPORT_OK = 100`;
- `SERIES_PRESENT = 100`;
- `IN_WINDOW_PRESENT = 100`;
- `condition_both_sides_present = 50`;
- `error_response_count = 0`;
- `malformed_response_count = 0`.

Accepted interpretation:

- the repeat canary supports network/environment sensitivity of the first failure pattern;
- the CLOB route is not dead;
- P0-scale source viability remains `NOT ESTABLISHED`;
- only `100 / 37,248` request-eligible token sides were tested;
- the result does not authorize a full diagnostic or any further network activity.

Candidate 02 failure-characterization design is accepted as SPEC-only with authorization effect `NONE`.

### P0 CLOB Candidate 03 source-installation state

#### Historical empirical evidence remains separately attributed

The earlier accepted dry run and two earlier 100-request canaries remain historical evidence from:

| Historical item | Bytes | SHA-256 |
|---|---:|---|
| diagnostic script | `66241` | `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00` |
| compatibility Store | `8788` | `7fa3078e78c2ba993ba3a825c2f6042dd33445d0079592aba3cde86e09b7dc92` |
| `schemas.py` | `4878` | `75ec05646f458d72d2fba7481ee8a78c67a3099d4025eb9826af3ad9ac30396c` |

Historical repository base:

`e675a47ec2c8f6cd769c2673afc16d96e5622ccd`

The earlier network-sensitivity documentation package installed no source and did not contain Candidate 03. Candidate 03 MUST NOT be credited with producing those historical runs.

#### Candidate 03 accepted external package and canonical installation

External provenance package:

`P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALL_CANDIDATE_03.zip`

- bytes: `20023`;
- SHA-256: `7a6d63d804a85bcbdf20917b2bc067fe08ae1f4fd77a69c7d1a1f46ed0b45b94`;
- repository membership: `NO`;
- static-review state: `STATIC_REVIEW_ACCEPTED`.

Canonical source-installation anchor:

| Field | Exact value |
|---|---|
| commit | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| parent | `ed045a6ce0130c1c245e4a5bee98fe1b09be83cb` |
| tree | `d8a530b598735fc9d98294698a21d4d072162414` |
| message | `Install Candidate 03 P0 CLOB diagnostic source and canonical validation record` |
| installation finding | `CANONICAL_REMOTE_INSTALLATION_VERIFIED` |
| installation method | one local commit; ordinary non-force fast-forward push to `origin/main`; no merge, amend, or tag |
| remote verification | local `HEAD`, `origin/main`, and direct `refs/heads/main` resolved to the same exact commit; local status clean |

Installed source identities:

| Path | Bytes | SHA-256 | Git blob SHA |
|---|---:|---|---|
| `.gitignore` | `2328` | `0790b0f98f1367195ff5142e4e1de0f651a73b160465f13ef25313945d41522f` | `b4d26e15ac1b3de27af48d38d5024fd2c4cc830c` |
| `scripts/p0_per_token_price_source_scale_diagnostic_01.py` | `63237` | `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006` | `c72a6b582e6523fcffc1cf64ce0a25ab114154a9` |
| `pm_research/data/__init__.py` | `0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `pm_research/data/store.py` | `5079` | `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95` | `711052cdb3ff2644758f0b138016fceaca3c3169` |

The installed `.gitignore` exception is exactly:

`!scripts/p0_per_token_price_source_scale_diagnostic_01.py`

Candidate 03 removes the permanent exact-Git-HEAD runtime gate and obsolete canonical-base override path; narrows `Store` to read-only trade loading without directory creation, save/write methods, prices, markets, resolutions, coverage API, or `schemas.py`; contains no `yes_price` or complement-price semantics; excludes `schemas.py`; and preserves independent token-side acquisition.

#### Accepted Candidate 03 local non-network validation

Exact validated source:

- script SHA-256 `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006`;
- Store SHA-256 `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95`.

Controls: `dry_run = true`, `execute_network = false`, `save_raw = false`, `executed_requests = 0`, no raw directory, no request-results JSONL, no condition or subclass filters, and no maximum-condition or maximum-request restriction.

Accepted reconciliation:

- `final_p0_rows_loaded = 39693`;
- `token_pair_clear_conditions = 39693`;
- `request_eligible_conditions = 18624`;
- `request_eligible_token_sides = 37248`;
- `INVALID_DECISION_WINDOW = 21069`;
- `REQUEST_ELIGIBLE = 18624`;
- request-manifest rows `= 37248`;
- `failed = []`.

Accepted finding:

`LOCAL_NON_NETWORK_VALIDATION_CLEAR`

This finding establishes local planning and reconciliation equivalence only. No dry-run output-file identity is asserted.

#### Accepted Candidate 03 bounded network canary

Run interval:

- started `2026-07-30T09:15:13Z`;
- completed `2026-07-30T09:25:28Z`.

Controls included endpoint `https://clob.polymarket.com/prices-history`, `execute_network = true`, `dry_run = false`, `save_raw = false`, `max_requests = 100`, `max_conditions = null`, no condition or subclass filters, `resume = false`, `retry_count = 0`, `fidelity = 1`, interval omitted, timeout `30`, sleep `0`, independent token-specific acquisition, no complement synthesis, and no winner-based token enumeration.

Accepted outcome:

- `executed_requests = 100`;
- `HTTP 200 = 100`;
- `TRANSPORT_OK = 100`;
- `SERIES_PRESENT = 100`;
- `in_window_present_sides = 100`;
- `in_window_empty_sides = 0`;
- `condition_both_sides_present = 50`;
- one-side, neither-side, and not-measurable counts `= 0`;
- error and malformed-response counts `= 0`;
- `skipped_resumed_rows = 0`;
- `condition_incomplete_bounded_run = 18574`;
- planning reconciliation remained `39693 / 18624 / 37248 / 21069 / 18624`;
- `failed = []`.

Accepted finding:

`BOUNDED_100_REQUEST_NETWORK_CANARY_CLEAR`

The local evidence identities remain non-canonical local evidence only. They are recorded in the installation and post-installation verification records. `request_results.jsonl` is not immutable raw-response evidence because `save_raw = false` and no raw directory existed.

#### Candidate 03 current lifecycle

| Lifecycle boundary | Current state |
|---|---|
| source candidate | `STATIC_REVIEW_ACCEPTED` |
| local non-network validation | `LOCAL_NON_NETWORK_VALIDATION_CLEAR` |
| bounded 100-request network canary | `BOUNDED_100_REQUEST_NETWORK_CANARY_CLEAR` |
| canonical remote installation | `CANONICAL_REMOTE_INSTALLATION_VERIFIED` |
| source-installation anchor commit | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| validation execution authorization | `CONSUMED` |
| further execution authorization | `NONE` |
| accepted per-token price artifact | `NONE` |
| P1 | `BLOCKED` |

A future documentation-installation commit may descend from the source-installation anchor. This document MUST NOT describe `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` as permanently the repository's latest commit.

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

Candidate 03 source authoring, the local non-network validation, the bounded network canary, and the exact canonical source installation are complete at their accepted boundaries. Canonical remote installation is verified at source-installation anchor commit `1a19e1ef715ceca7aef9d55f7aa2446961e13c35`.

The validation execution authorization is consumed. Source installation does not authorize another diagnostic, endpoint request, test run, local-data read, full diagnostic, S2 artifact construction, P1/P2/P3, scoring, probe execution, or gate change.

S2 Candidate 08 implementation authorization remains `NONE`. Candidate 02 remains SPEC-only with authorization effect `NONE`. Candidate 04 is accepted SPEC-only and canonically installed at `a34636a89ec6ba557764cb32cbb0deed5b46df94`; `CANDIDATE_04_CANONICAL_GIT_INSTALLATION_COMPLETE` is established. The requested `A010_CANONICAL_INSTALLATION_VERIFIED` finding, A010 downstream consumption, fresh K013, and K012/K014/K015/K016 remain absent, blocked, or unauthorized pending Sentinel acceptance and later exact installation verification of this documentation package.

This documentation package authorizes no source or test edit, `.gitignore` change, staging, local commit, push, merge, amend, branch, tag, reset, ref update, test execution, project import or execution, compilation, linting, type checking, coverage, local research-data read, network/API/RPC/vendor/Dune/curl/endpoint activity, raw-response access or copying, raw saving, diagnostic execution, another dry run or canary, full diagnostic, dependency or packaging change, acquisition, S2 artifact construction, price-artifact construction or acceptance, P1/P2/P3, scoring, probe execution, or gate change.

---

## Working discipline

- Verify exact paths, bytes, hashes, schemas, and authorization boundaries.
- Passing tests do not prove correctness when tests encode the wrong contract.
- Specification acceptance does not authorize implementation.
- Implementation acceptance does not authorize tests or execution.
- Canonical project-document changes are prepared as complete files and uploaded manually by Gustavo.
- Never silently reverse a settled decision or reactivate superseded material.
