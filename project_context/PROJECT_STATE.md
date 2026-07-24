# PROJECT STATE

*Current objective, environment, active blockers, and authorization state.*

---

## Current objective

### Controlling Revision 10 verified-installation objective

Revision 10 is accepted, canonically installed, and Sentinel-verified at
`3d6fbe5eda504c32d94fed72be99adb9485fe1b1`. Its accepted source archive SHA-256 is `8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`.

The immediate decision-bearing objective is static implementation-conformance
review of preserved checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4...` against
the installed Revision 10 contract and the remaining provenance evidence.

No implementation start, source/test edit, test execution, rollback, promotion,
R2, or downstream activity is selected or authorized.

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
- inactive Revision 10 specification-installation handoff; no implementation authorization.

No `pm_research/`, `tests/`, dependency, CLI/runtime, research-data, or empirical
path changed during documentation installation.

---

## Revision 23 Finding 4 I0A scope state

### Controlling Revision 10 scope

- decision: `APPROVE`
- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- accepted source: Candidate 11
- archive SHA-256: `8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`
- member count: `15`
- acceptance date: `2026-07-24`
- canonical installation base: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`
- verified canonical installation commit: `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- immutable installed directory: `accepted_scope_revision_10/`
- implementation authorization: `NONE`
- implementation starting SHA: `NOT_AUTHORIZED_AND_NOT_YET_SELECTED`

Revision 10 supersedes Revision 09 for the complete Finding 4 I0A specification
package. Revision 09 and Revision 08 remain immutable historical accepted evidence.

### Historical Revision 09 scope state

- accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
- verified installation commit: `c4e8b1011c51272042decac4bc89e762d767a72a`
- historical R1 source-gated commit: `1e1afb29791f42c286b45d3b576f74926add8dce`
- authorization carries forward: `false`

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

### Controlling Revision 10 authorization state

`STOP_IMPLEMENTATION_NOT_AUTHORIZED`

No Revision 10 implementation authorization, source gate, writable path set, test-source stage, test execution, project execution, data/network activity, or Git write is active.

The historical Revision 09 R1 authorization and Revision 08 implementation authorization do not carry forward. The `fcf406c4...` checkpoint is evidence only and must not be restored, overwritten, promoted, or used as a continuation start without a later explicit decision.

### Preserved unreviewed R1 implementation checkpoint

Checkpoint ID:

`REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`

Exact recovered payload:

- intended target path: `pm_research/local_curl_per_side/prepared_evidence.py`
- evidence-only payload path: `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/payload_exact/pm_research/local_curl_per_side/prepared_evidence.py`
- SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes
- preservation state: `CANONICALLY_PRESERVED`
- canonical installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- verified installation commit: `58acbac493840c45d84c6b7e33c583d722f4d559`
- conformance state: `BLOCKED_PENDING_PROVENANCE_AND_REVISION10_IMPLEMENTATION_CONFORMANCE_REVIEW`
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`

The checkpoint preserves exact bytes against chat/session loss. It does not
promote those bytes to the executable source tree. Revision 10 resolves the
former T107/T153/Candidate 09 specification blockers. Remaining blockers are
incomplete multi-round activity lineage, absence of an independently captured
current twelve-path worktree inventory, and implementation-conformance review
against the verified canonical Revision 10 package.

### Historical Revision 08 authorization state at installation base

The historical Revision 08 and Revision 09 R1 implementation-authoring records
remain audit evidence only. Revision 10 supersedes them for current authority.
They do not authorize source synchronization, source/test authoring, rollback,
restoration, overwrite, promotion, tests, execution, data/network access, Git
writes, or any downstream phase.

## Environment

- Local execution environment: Windows / Miniconda.
- Project path: `C:/b1/pm_research`.
- Data path: `C:/b1/data`.
- Artifacts path: `C:/b1/pm_research/artifacts`.
- Local research data remains unavailable to agents unless separately authorized.

---

## Next possible step

### Controlling Revision 10 next step

Sentinel statically reviews preserved checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` against the
installed Revision 10 contract at verified installation commit `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`.
The review must separate specification conformance from incomplete provenance and
must not execute tests, project code, data reads, network activity, or modify any
file.

No promotion, source/test edit, rollback, R2, or downstream stage follows
automatically.

### Historical Revision 08 next step at installation base

No current action is authorized from the historical Revision 08 package. Any
future implementation stage must be newly authorized under Revision 10 and may
not reuse the historical Revision 08 or Revision 09 source gates.
