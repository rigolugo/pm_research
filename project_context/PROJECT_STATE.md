# PROJECT STATE

*Current objective, environment, active blockers, and authorization state.*

---

## Current objective

### Controlling Revision 09 installation objective

Stay Polymarket-native and preserve the accepted research-only guardrails. The immediate objective is Sentinel static review of the documentation-only Revision 09 canonical installation package, followed only on approval by Gustavo's manual documentation commit and Sentinel verification of the resulting commit. No Revision 09 implementation activity is authorized.

### Historical Revision 08 objective at installation base

Stay Polymarket-native and preserve the accepted research-only guardrails.

The immediate project objective is to install and verify the active Finding 4
I0A authorization package, then complete bounded implementation-source and
unexecuted test-source authoring under Revision 08. The accepted-scope commit
`2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff` is verified.

---

## Named-binary research state

### Semantics and realized outcomes

- Named-binary semantics/orientation: implemented, tested, and audit-gated.
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
- P0 representativeness result:
  `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`.
- P1 remains blocked because the accepted orientation contract requires two
  independently sourced per-side prices, while the local price store exposes only
  `[condition_id, ts, yes_price]`.
- `yes_price` is YES/NO-only and unsafe for UP_DOWN, OVER_UNDER, and NAMED_OTHER.
- No local per-side/per-token decision-time price artifact is accepted.

---

## Price-source candidate state

### S1 — CLOB `/prices-history`

Accepted sampled result: `S1_SOURCE_NOT_VIABLE`.

Both-side Level-B coverage cleared `0.95` in no subclass:

- UP_DOWN: `19 / 50 = 0.38`
- OVER_UNDER: `51 / 98 ≈ 0.5204`
- NAMED_OTHER: `65 / 100 = 0.65`

No Pass 2 or downstream phase is authorized.

### S1-ALT — local trade prints

Accepted sampled result: `S1ALT_SOURCE_NOT_VIABLE`.

- UP_DOWN: `13 / 50 = 0.26`
- OVER_UNDER: `40 / 98 ≈ 0.4082`
- NAMED_OTHER: `71 / 100 = 0.71`

No side synthesis or downstream phase is authorized.

### Option B — Data API `/trades`

Accepted corrected B0 result: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.

- primary API rows: `13,009`
- total API rows across query modes: `17,853`
- local rows: `1,346`
- mismatches: `14,355`
- overlap matched: `0`
- overlap API/local mismatch: `7`
- overlap pagination partial: `3`

B1 remains unauthorized.

### Option C — decoded on-chain OrderFilled tables

- Original C1A accepted valid halt: `C1_ROW_EXPLOSION`.
- C1A-F1: reviewable mixed evidence only.
- C1A-F2: `C1F2_ARTIFACTS_INSUFFICIENT`.
- Option C is not accepted as viable.
- C1 is not design-clear.
- C1B, C2, P1/P2/P3, and probe execution remain unauthorized.

### Option D — L2 archive candidates

Accepted temporal in-range result:

- PMXT v2 pooled: `18,137 / 39,693 = 0.456932`
- Telonex L2 pooled: `37,749 / 39,693 = 0.951024`
- Telonex NAMED_OTHER: `0.918096`

PMXT v2 is closed/deprioritized for broad full-P0 coverage on timing grounds.
Telonex L2 may only proceed through a separately authorized SPEC-ONLY
vendor-coverage review. No vendor fetch or paid action is authorized.

---

## Revision 23 Finding 4 contract state

Revision 23 with Amendments 01–03 and Finding 4 is accepted and installed.

Installation base:

`f6cb60df66c2bbcdfb6d797119ed25ad79e06a11`

Linear installation commits:

1. `3f8cc54dc12a5335472f00f5ffcf5c0d56d8d1ba`
2. `c394b9ab5eb5dc07f8d716818e02507994ce41d7`
3. `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Finding 4 installation commit:

`e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Installed effective hashes:

- specification: `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`
- schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`
- request/authorization contract: `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`
- governing manifest: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- governing semantic hash: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`
- accepted checksum inventory: `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`

Installed path:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

The installed tree includes:

- complete effective accepted contract;
- complete Finding 4 materialization/audit trail;
- preflight evidence;
- replacements and transformation evidence;
- authorization supersession record;
- disabled Claude implementation prompt.

No `pm_research/`, `tests/`, dependency, CLI/runtime, research-data, or empirical
path changed during installation.

---

## Revision 23 Finding 4 I0A scope state

### Controlling Revision 09 scope

Revision 09 is Sentinel-accepted as the narrow controlling correction, pending canonical installation and Sentinel verification of the resulting manual commit.

- Sentinel acceptance date: `2026-07-20`
- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- accepted archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
- accepted member count: `14`
- canonical installation base: `1e963bb6e8387aff071d697a416fa558956e571e`
- proposed immutable directory: `accepted_scope_revision_09/`
- Revision 08 directory: immutable historical accepted evidence
- supersession boundary: private descriptor-set invariant contract only
- Revision 09 implementation authoring: **NOT AUTHORIZED**
- Revision 09 test-source authoring and test execution: **NOT AUTHORIZED**

### Historical Revision 08 scope state at installation base

Revision 08 is accepted as the bounded implementation-authoring scope.

- Sentinel decision: `APPROVE`
- review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- accepted archive: `REV23_FINDING4_I0A_SCOPE_REVISION_08.zip`
- accepted archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- accepted member count: `14`
- canonical scope path:
  `project_context/implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/`
- accepted maximum candidate matrix: six source paths and six test-source paths
- accepted-scope commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff` — verified
- implementation authoring: **AUTHORIZED AFTER ACTIVE-PACKAGE INSTALL VERIFICATION**
- unexecuted test-source authoring: **AUTHORIZED AFTER ACTIVE-PACKAGE INSTALL VERIFICATION**
- test execution: **NOT AUTHORIZED**
- authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`

The accepted scope contains exact API, schema, grammar, assurance, result,
return-payload, hash, fixture, and static-contract obligations. No Revision 09
follows for optional polish. A later amendment requires a concrete material
contradiction that cannot be resolved from Revision 08.

---

## Authorization state

### Controlling Revision 09 authorization state

Revision 09 implementation is not authorized. The Revision 08 authorization ID `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01` remains historical and does not automatically carry forward. No active Revision 09 Claude prompt, source synchronization, implementation-source authoring, or test-source authoring is authorized. The only current activity is documentation/checksum installation review and, after Sentinel approval, Gustavo's manual canonical commit.

### Historical Revision 08 authorization state at installation base

Gustavo has explicitly authorized bounded Finding 4 I0A implementation authoring.
Sentinel has approved the exact twelve-path activity matrix. Activation requires
manual installation and Sentinel verification of the authorization package.

Authorized after activation:

- read-only source synchronization to the source-gated HEAD;
- implementation-source authoring in exactly six paths;
- unexecuted test-source authoring in exactly six paths;
- static file/JSON/hash/package validation within the active boundary;
- implementation review ZIP, report, and checksum production.

Still unauthorized:

- test execution, lint, type checking, coverage, CI, compilation, or project imports;
- local research-data or empirical-artifact reads;
- API, RPC, vendor, Dune, curl, or general network use;
- replay, scoring, P1/P2/P3, probe execution, or gate changes;
- dependencies, CLI/config, generated code, additional paths, caches, or bytecode;
- Git commit, branch/ref, push, PR, merge, or other history/remote write.

The active authorization ID is `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`.

---

## Environment

- Local execution environment: Windows / Miniconda.
- Project path: `C:/b1/pm_research`.
- Data path: `C:/b1/data`.
- Artifacts path: `C:/b1/pm_research/artifacts`.
- Local research data remains unavailable to agents unless separately authorized.

---

## Next possible step

### Controlling Revision 09 next step

Sentinel statically reviews the Revision 09 documentation-only installation package. On approval, Gustavo manually uploads the exact package files and commits them. Gustavo then returns the full commit SHA to Sentinel for exact path, byte, checksum, Revision 08 preservation, and no-source/test-change verification. Any Revision 09 implementation stage requires a later separate Gustavo authorization and Sentinel handoff.

### Historical Revision 08 next step at installation base

Manually upload and commit the active I0A authorization package, then return the
commit SHA to Sentinel for verification.

After verification, Claude may begin only the bounded implementation-source and
unexecuted test-source authoring stage. Test execution remains a separate future
decision.
