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

## P0 CLOB Candidate 03 source-installation decisions

### Static source candidate accepted

Sentinel accepted the external provenance package:

`P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALL_CANDIDATE_03.zip`

Exact identity:

- bytes: `20023`;
- SHA-256: `7a6d63d804a85bcbdf20917b2bc067fe08ae1f4fd77a69c7d1a1f46ed0b45b94`;
- disposition: `STATIC_REVIEW_ACCEPTED`;
- authorization effect: `NONE`;
- repository membership: `NO`.

Accepted payload identities:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `.gitignore` | `2328` | `0790b0f98f1367195ff5142e4e1de0f651a73b160465f13ef25313945d41522f` |
| `scripts/p0_per_token_price_source_scale_diagnostic_01.py` | `63237` | `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006` |
| `pm_research/data/__init__.py` | `0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `pm_research/data/store.py` | `5079` | `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95` |

The accepted corrections remove the permanent exact-Git-HEAD runtime gate and obsolete canonical-base override; narrow Store to read-only trade loading with no directory creation, save/write methods, prices, markets, resolutions, coverage API, or `schemas.py`; exclude `schemas.py`; retain no `yes_price` or complement-price semantics; and add one narrow `.gitignore` exception.

### Historical source attribution preserved

The historical dry run and historical two 100-request canaries remain attributed to:

- script: `66241` bytes / `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00`;
- compatibility Store: `8788` bytes / `7fa3078e78c2ba993ba3a825c2f6042dd33445d0079592aba3cde86e09b7dc92`;
- historical `schemas.py`: `4878` bytes / `75ec05646f458d72d2fba7481ee8a78c67a3099d4025eb9826af3ad9ac30396c`;
- repository base: `e675a47ec2c8f6cd769c2673afc16d96e5622ccd`.

Candidate 03 does not retroactively own or replace those historical evidence identities. The earlier network-sensitivity documentation package installed no source and did not contain Candidate 03.

### Candidate 03 local non-network validation accepted

Exact source identities:

- script SHA-256 `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006`;
- Store SHA-256 `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95`.

The dry-run controls established no network execution and no raw/result output. Reconciliation remained:

- final P0 rows `39693`;
- token-pair-clear conditions `39693`;
- request-eligible conditions `18624`;
- request-eligible token sides and request-manifest rows `37248`;
- invalid decision windows `21069`;
- request-eligible disposition `18624`;
- executed requests `0`;
- `failed = []`.

Accepted finding:

`LOCAL_NON_NETWORK_VALIDATION_CLEAR`

This proves local planning and reconciliation equivalence only. No dry-run output-file identity is accepted or invented.

### Candidate 03 bounded network canary accepted

The separately authorized deterministic bounded run used the exact Candidate 03 script and Store identities, independent token-specific requests, no complement synthesis, no winner-derived token enumeration, `fidelity = 1`, interval omitted, zero retries, `save_raw = false`, and a maximum of `100` requests.

Accepted result:

- `100 / 100` HTTP 200 and `TRANSPORT_OK`;
- `100` series present and in-window-present sides;
- `50` conditions with both sides present;
- all one-side, neither-side, not-measurable, error, malformed, and resumed-skip counts `0`;
- `condition_incomplete_bounded_run = 18574`;
- planning reconciliation remained unchanged;
- `failed = []`.

Accepted finding:

`BOUNDED_100_REQUEST_NETWORK_CANARY_CLEAR`

This finding establishes bounded end-to-end endpoint behavior only. It does not establish full `37248`-request viability, long-run transport stability, full-universe acquisition, immutable raw-evidence closure, S2 artifact acceptability, price-artifact acceptance, P1 readiness, scoring readiness, probe readiness, or any gate change.

### Canonical remote installation verified

Accepted installation finding:

`CANONICAL_REMOTE_INSTALLATION_VERIFIED`

Source-installation anchor:

| Field | Exact value |
|---|---|
| commit | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| parent | `ed045a6ce0130c1c245e4a5bee98fe1b09be83cb` |
| tree | `d8a530b598735fc9d98294698a21d4d072162414` |
| message | `Install Candidate 03 P0 CLOB diagnostic source and canonical validation record` |
| changed paths | exactly `9` |
| push | ordinary non-force fast-forward to `origin/main` |
| prohibited mechanisms absent | no force push, merge, amend, or tag |
| ref convergence | local `HEAD`, `origin/main`, and direct `refs/heads/main` resolved to `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| local status | clean after push |

The exact nine committed paths and their Git blob identities are recorded in the post-installation verification record. The external Candidate 03 ZIP is provenance and is not a repository member.

### Lifecycle separation after installation

The following boundaries remain separate:

1. source candidate static acceptance — complete;
2. local non-network validation — complete;
3. bounded network canary — complete;
4. canonical remote source installation — verified;
5. this post-installation documentation package — review candidate only;
6. any future documentation installation commit — not created or authorized by this package;
7. further empirical execution — unauthorized;
8. S2 construction, price-artifact acceptance, P1/P2/P3, scoring, probe execution, and gate changes — unauthorized.

The execution authorization used for the local non-network validation and bounded canary is consumed. Source installation creates no new execution authority.

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

Documentation acceptance, specification acceptance, amendment acceptance, source-candidate static acceptance, bounded validation acceptance, package preparation, checksum validation, or canonical documentation installation authorizes no source installation, local commit, exact commit review, push, merge, remote verification, further source/test authoring, tests, project imports or execution, local research-data reads, network/API/RPC/vendor/Dune/curl/endpoint activity, raw-response access or saving, another dry run or canary, a full diagnostic, empirical artifacts, dependency or packaging changes, S2 artifact construction, P1/P2/P3, scoring, probe execution, gate changes, Git writes, or downstream stages unless a later exact Gustavo authorization and Sentinel stage authorization explicitly create that scope.
