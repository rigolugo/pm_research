# DECISION LOG

*Corrected history and settled decisions. Do not re-litigate settled items
without new authoritative evidence.*

---

## Settled semantic and data decisions

### Rank 1A decision timestamp

`first_price_after_warmup` is retained because fixed-lead-before-resolution
would leak outcome information when resolution time is derived from price
convergence.

### OrderFilled topic order

Settled and Dune-verified:

`topic1 = orderHash`, `topic2 = maker`, `topic3 = taker`.

The earlier 217/0 and 10/0 all-taker outputs were artifacts caused by an invalid
join/topic reversal and uint256 CSV precision loss. They are not findings.

### Asset-ID precision

Dune uint256 values must be cast to varchar, loaded as strings, canonicalized as
integers, and rejected on scientific notation. The validated OrdersMatched
maker-pairing result is retained.

### Data hygiene

- null or blank `condition_id` rows are dropped at analysis load;
- trade-ID deduplication prefers rows with populated semantic keys;
- all-one-role or all-one-direction output is a diagnostic warning, not a result.

---

## Named-binary decisions

### Semantics and realized outcomes

Named-binary orientation is accepted and must not be re-derived.

The local resolution store is YES/NO-only. Non-YES/NO outcomes are accepted from
the Dune payout-vector pipeline:

- resolved single winners: `39,693`;
- ambiguous multiple-winner exclusions: `253`;
- non-YES/NO branch: `CLEAR_WITH_WARNINGS`;
- legacy pooled-all gate: `BLOCKED_BY_RESOLUTION_MAPPING`.

The source is usable for outcome mapping but does not authorize a probe.

`named_binary_probe_blocked = true`.

### P0

P0 is accepted as `P0_CLEAR` with final eligible count `39,693`.

The representativeness audit is accepted as
`P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`. The excluded tail is
compositionally skewed but too small to materially change the impact-weighted
pre-resolution-versus-final-P0 comparison.

Neither result authorizes P1, pricing, scoring, wallet work, or probe execution.

### P1 price input

P1 remains blocked on a two-side price source.

`yes_price`, `1 - price`, and `1 - yes_price` are prohibited as named-binary
unblock paths.

---

## Price-source decisions

### S1

Accepted sampled result: `S1_SOURCE_NOT_VIABLE`.

Do not reopen the sampled negative or silently escalate to Pass 2.

### S1-ALT

Accepted sampled result: `S1ALT_SOURCE_NOT_VIABLE`.

Do not synthesize the missing side.

### Option B

Corrected B0 is accepted as `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.

The original artifact-missing defect is superseded by the corrected diagnostic.
B1 remains unauthorized.

### Option C

- Revision 3 spec and C1R design are accepted as historical/spec context.
- Original C1A halt `C1_ROW_EXPLOSION` is accepted.
- C1A-F1 is mixed diagnostic evidence only.
- C1A-F2 result is `C1F2_ARTIFACTS_INSUFFICIENT`.
- Option C is not accepted as viable.
- C1 is not design-clear.
- No further canary, C1B, C2, price artifact, or downstream phase is authorized.

### Option D

The L2 archive coverage methodology is accepted as SPEC ONLY.

Accepted temporal results:

- PMXT v2 pooled `0.456932`;
- Telonex L2 pooled `0.951024`;
- Telonex NAMED_OTHER `0.918096`.

PMXT v2 is deprioritized for broad P0 coverage. Telonex L2 may only progress
through a separately authorized SPEC-ONLY vendor-coverage review.

Timing feasibility is not vendor availability, token/side coverage, price
quality, mechanical trust, or P1 viability.

---

## Revision 23 lifecycle decisions

### Amendment 03

Revision 23 with Amendments 01–03 was previously accepted. Its earlier bounded
I0 authorization later became stale relative to Finding 4.

The accepted-contract commit and authorization-anchor commit were distinct:

- accepted Amendment 03 contract: `fad41de515572ca30b4440b060a69dd6bfc57e2b`;
- first Amendment 03 authorization anchor:
  `d737aa9e12cbfa584b275e128c8624e01af72f61`.

Claude's `STOP_CANONICAL_SOURCE_UNAVAILABLE` was valid.

### Finding 4 specification and materialization

Finding 4 was approved as the exact ordered stack:

1. base amendment draft;
2. bounded correction packet;
3. delta packets 02 through 08.

The distributed specification was frozen before materialization.

The materialization preflight was accepted only after it proved:

- all 18 support schemas;
- the exact 30-role matrix;
- eight structural prepared members;
- separate descriptor-selected prepared object payloads;
- complete path grammar;
- zero unresolved references;
- all twelve materialization obligations represented concretely.

The final package was accepted with archive SHA-256:

`9ec22f611a1f6b8a598725e0b60b7591503fd6271ae79eb366359e7e312099f8`.

### Finding 4 canonical installation

The Phase A installation is accepted.

Authorized base:

`f6cb60df66c2bbcdfb6d797119ed25ad79e06a11`

Linear commits:

- `3f8cc54dc12a5335472f00f5ffcf5c0d56d8d1ba`
- `c394b9ab5eb5dc07f8d716818e02507994ce41d7`
- `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Finding 4 installation commit:

`e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Verified installed hashes:

- specification: `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`;
- schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`;
- request/authorization contract: `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`;
- governing manifest: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`;
- governing semantic hash: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`;
- accepted checksum inventory: `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`.

All 109 changed files were confined to:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

No implementation, test, dependency, CLI/runtime, empirical, or research-data
path changed.

### Finding 4 I0A scope acceptance

Revision 08 is accepted as the bounded implementation-authoring scope.

- decision: `APPROVE`;
- review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`;
- archive: `REV23_FINDING4_I0A_SCOPE_REVISION_08.zip`;
- archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`;
- accepted member count: `14`;
- maximum candidate matrix: six source paths and six test-source paths;
- implementation authorization: not active;
- test execution: unauthorized.

The scope acceptance closed the then-current revision loop. A later concrete
material contradiction reopened the private reducer contract and produced
Revision 09.

### Finding 4 I0A implementation-authoring authorization

On `2026-07-18`, Gustavo explicitly authorized the bounded Finding 4 I0A
implementation-authoring stage. Sentinel approved authorization ID
`REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01` pinned to verified accepted-scope
commit `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`.

Authorized after canonical installation and Sentinel verification of the active
package:

- read-only source sync to the source-gated HEAD;
- exact six implementation-source paths;
- exact six unexecuted test-source paths;
- static inspection, checksums, and implementation review packaging.

Test execution, project imports/execution, research data, general network/API/curl,
empirical work, dependencies/CLI/config, additional paths, Git history/remote
writes, P1/P2/P3, scoring, probe execution, and gate changes remained unauthorized.

This authorization is historical and inactive under Revision 10.

### Finding 4 I0A Revision 09 scope correction

A concrete material contradiction reopened the accepted Revision 08 scope. The
private helper `_validate_descriptor_set_invariants` was required to emit
`PRIVATE_DESCRIPTOR_SET_LOGICAL_HASH_NULLABILITY_INVALID` and
`PRIVATE_DESCRIPTOR_SET_PARTITION_BINDING_INVALID`, but its closed
`_DescriptorSetInvariantInput` and `_DescriptorSetInvariantSummary` exposed
neither logical-hash values nor partition-entry/binding information. Those
outcomes were impossible to determine through the accepted private interface.

Sentinel accepted `REV23_FINDING4_I0A_SCOPE_REVISION_09` on `2026-07-20` as the
narrow SPEC-ONLY correction:

- accepted archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`;
- accepted member count: `14`;
- canonical installation base: `1e963bb6e8387aff071d697a416fa558956e571e`;
- `_validate_descriptor_set_invariants` is narrowed to role cardinality, ordinal
  sequence, canonical-target uniqueness, sidecar relation, then valid;
- logical-hash-nullability validation belongs to
  `validate_prepared_object_descriptor`;
- same-ordinal partition-entry binding belongs to
  `validate_prepared_descriptor_set`.

Revision 09 superseded Revision 08 only for that private descriptor-set invariant
contract. Revision 08 remains immutable historical accepted evidence. All public
result codes, public assurances, public interfaces, precedence, fixtures, hashes,
role rows, frozen bindings, T001–T165 identities, and the maximum twelve-path
matrix remained preserved except for directly required private traceability
reconciliation.

#### Historical pre-R1 authorization state

Before the later R1 authorization, the Revision 08 implementation authorization
`REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01` did not automatically carry
forward. Revision 09 implementation, source/test authoring, source
synchronization, and an active Claude implementation prompt were unauthorized.

### Finding 4 I0A Revision 09 R1 source-resume authorization

On `2026-07-21`, Gustavo explicitly authorized Claude's implementation resume and
Sentinel accepted only authorization ID
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

The sole writable path was:

`pm_research/local_curl_per_side/prepared_evidence.py`

Required starting SHA-256:

`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

Sentinel independently verified implementation-review archive SHA-256
`e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`,
all internal archive checksum entries, and the exact twelve-path composite
baseline SHA-256
`061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`.

The other eleven previously authored source/test paths remained read-only. The
stage permitted canonical Revision 09 reads, static AST/source/JSON/text/bytes/hash
inspection, Git status/diff/path inventory/checksums, and one R1 source-only
checkpoint. It did not authorize test-source editing, test collection or
execution, project imports/execution, compilation, lint, type checking, coverage,
CI, another source edit, dependencies/CLI/config/generated files,
implementation ZIP reconstruction, research data, empirical artifacts,
API/RPC/vendor/Dune/curl/general network use, Claude Git history/remote writes,
R2, P1/P2/P3, scoring, probe execution, or gate changes.

Revision 08 authorization remains historical evidence. It does not enlarge the
Revision 09 R1 authorization.

### Finding 4 I0A Revision 09 R1 activation and Claude handoff

On `2026-07-24`, Sentinel verified the exact authorization-installation commit
`1e1afb29791f42c286b45d3b576f74926add8dce` and accepted the one-file R1 stage
as active. Gustavo then explicitly authorized the R1 handoff to Claude.

The exact source-gated local `HEAD` was
`1e1afb29791f42c286b45d3b576f74926add8dce`. Only
`pm_research/local_curl_per_side/prepared_evidence.py` could change, from starting
SHA-256 `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`.
The other eleven baseline paths remained byte-identical.

This activation did not authorize tests, test-source editing, R2, another source
edit, project execution, research data, network activity, empirical work,
P1/P2/P3, scoring, probe execution, or a gate change.

---

### Canonical evidence-only implementation checkpoint system

On `2026-07-24`, Sentinel approved a canonical progress-preservation mechanism for
unaccepted implementation work. Exact submitted bytes are stored under the
relevant handoff's `implementation_checkpoints/` directory, mirrored under
`payload_exact/` rather than written to the executable source path.

The first prepared checkpoint is:

- checkpoint ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- intended target: `pm_research/local_curl_per_side/prepared_evidence.py`
- exact payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- payload size: `112338` bytes
- governing scope at creation: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- source-gated commit: `1e1afb29791f42c286b45d3b576f74926add8dce`
- preservation state: `CANONICALLY_PRESERVED`
- canonical installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- verified installation commit: `58acbac493840c45d84c6b7e33c583d722f4d559`
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`

Checkpoint preservation and implementation promotion are separate decisions.
Presence of newer bytes does not make them controlling, accepted, executable, or
authorized. The checkpoint does not authorize rollback, another source edit,
tests, project execution, network/data access, Git writes by Claude, R2,
P1/P2/P3, scoring, probe execution, or a gate change.

### Checkpoint installation verification

On `2026-07-24`, Sentinel verified canonical commit
`58acbac493840c45d84c6b7e33c583d722f4d559` as exactly one linear
documentation/evidence-only commit after
`80430225af793b10864ef2b43486d718c9872dee`.

The commit changed exactly the declared `19` `project_context/` paths: eight
canonical documentation replacements and eleven new checkpoint files. It changed
no live `pm_research/` source path, no `tests/` path, and no accepted scope,
authorization, data, artifact, dependency, or runtime path.

The preserved payload is byte-identical to the recovered submission:

- evidence path:
  `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/payload_exact/pm_research/local_curl_per_side/prepared_evidence.py`
- SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes
- Git blob SHA: `d25a0fe58e84db526e6d68b4d14e764c59f6d46c`

Sentinel verified the checkpoint manifest, index, latest-preserved pointer,
accepted-checkpoint-null pointer, nested checksum inventory, and non-authorization
labels. The checkpoint is therefore `CANONICALLY_PRESERVED` and
`INSTALLED_AND_SENTINEL_VERIFIED`, but remains `NOT_ACCEPTED` with authorization
effect `NONE`.

---

### Finding 4 I0A Revision 10 scope acceptance

On `2026-07-24`, Sentinel accepted Candidate 11 as
`REV23_FINDING4_I0A_SCOPE_REVISION_10`.

- accepted archive: `REV23_FINDING4_I0A_SCOPE_REVISION_10_CANDIDATE_11.zip`
- accepted archive SHA-256: `8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`
- accepted member count: `15`
- canonical review/install base: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`
- controlling accepted base: `REV23_FINDING4_I0A_SCOPE_REVISION_09`

Revision 10 resolves the T107 and T153 reachability contradictions, closes public
result inventories, materializes T166–T230 and the 169-ID fixture namespace,
closes all 23 caller–callee edges, and makes the twelve-path future-impact matrix
identical across all eight declared representations.

Revision 10 selects no implementation starting SHA. The historical Revision 09
start `8b8e9320...` is not current. The preserved `fcf406c4...` checkpoint remains
`NOT_ACCEPTED`, non-controlling, and authorization effect `NONE`. No rollback,
restore, overwrite, promotion, implementation, tests, execution, data/network
activity, Git write, R2, P1/P2/P3, scoring, probe execution, or gate change is
authorized.

Revision 10 supersedes Revision 09 for the complete Finding 4 I0A specification
package. Revision 09 and Revision 08 remain immutable historical accepted evidence.
Their implementation authorizations do not carry forward.

---

### Finding 4 I0A Revision 10 canonical installation verification

On `2026-07-24`, Sentinel verified commit
`3d6fbe5eda504c32d94fed72be99adb9485fe1b1` as the exact documentation-only
installation of `REV23_FINDING4_I0A_SCOPE_REVISION_10`.

- parent/install base: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`
- changed paths: `32`, all under `project_context/`
- accepted source archive SHA-256: `8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`
- accepted member count: `15`
- live source/test changes: `0`
- checkpoint payload changed: `false`
- implementation authorization effect: `NONE`

Revision 10 is now the controlling accepted and canonically installed Finding 4
I0A specification. T107, T153, and Candidate 09 are no longer open
specification-layer blockers for checkpoint review. They are removed from the
checkpoint blocker list without implying implementation conformance.

The checkpoint remains `NOT_ACCEPTED`, non-controlling, and authorization effect
`NONE`. At that point, remaining blockers were incomplete multi-round activity
lineage, absence of an independently captured current twelve-path worktree
inventory, and static implementation-conformance review against Revision 10.

No implementation start, rollback, restoration, overwrite, promotion, source or
test edit, test execution, project execution, data/network activity, Git write,
R2, P1/P2/P3, scoring, probe execution, or gate change was authorized.

---

### Revision 10 checkpoint static-conformance decision

On `2026-07-24`, Sentinel independently reviewed preserved checkpoint
`REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` against the installed Revision 10
contract at canonical review base
`3cf0871ae97d112324031190822756379d1236e8`.

Decision:

`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`

Verified material defects:

1. Revision 10 requires mandatory source changes in `canonical.py`,
   `finding4_registry.py`, and `prepared_evidence.py`; the checkpoint preserves
   only `prepared_evidence.py`.
2. The checkpoint does not materialize `ERR_UNIT_CONTEXT_INVALID`,
   `ERR_SEMANTIC_FAMILY_BINDING_MISMATCH`, `ERR_RUN_ID_BINDING_MISMATCH`, or
   `ERR_REUSE_SOURCE_TARGET_MISMATCH`.
3. Closed UnitContext validation is missing.
4. Registry-owned path decomposition and typed binding outputs are missing;
   private string/suffix parsing remains in `prepared_evidence.py`.
5. Descriptor pre-binding and global path/reuse/family/run reduction helpers are
   missing.
6. The private descriptor-set reducer retains the superseded ordinal result and
   `expected_role_counts` input.
7. `validate_selected_json_payload` retains the old predicate order and direct
   old `BindingQuery` construction; `_project_selected_binding_query` is absent.
8. `validate_prepared_unit_structure` bypasses
   `validate_selected_json_payload`, preventing required selected-wrapper
   propagation.

Resolved/non-blocking specification areas:

- T107 reachability is resolved by Revision 10.
- T153 reachability is resolved by Revision 10.
- Candidate 09 is non-controlling.
- The exact checkpoint payload remains recoverable and useful as historical
  Revision 09 progress.

Open provenance gaps remain separate:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

The checkpoint remains `NOT_ACCEPTED`, non-controlling, and authorization effect
`NONE`. No implementation starting SHA is selected. No remediation, implementation,
tests, rollback, promotion, data/network access, Git write by Claude, R2,
P1/P2/P3, scoring, probe execution, or gate change is authorized.

The only immediate next action is Gustavo's manual installation of the complete
documentation-only review record package at the exact review base, followed by
Sentinel verification of the resulting commit.

---

### Revision 10 local-curl remediation-scope acceptance

On `2026-07-24`, Sentinel accepted
`REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01` as the narrow
implementation-remediation planning contract.

- decision: `APPROVE — REV10_LOCAL_CURL_REMEDIATION_SCOPE_ACCEPTED`;
- submitted ZIP SHA-256:
  `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`;
- accepted candidate member count: `11`;
- implementation authorization effect: `NONE`;
- implementation starting SHA selected: `false`.

The accepted source-stage design is one atomic candidate across exactly:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

Test-source authoring remains a separate later boundary across exactly:

- `tests/local_curl_per_side/test_canonical_i0a.py`;
- `tests/local_curl_per_side/test_finding4_registry_i0a.py`;
- `tests/local_curl_per_side/test_i0a_public_contract.py`;
- `tests/local_curl_per_side/test_prepared_evidence_i0a.py`.

Binding Sentinel determinations:

1. selected-member iteration is sidecars first, then non-sidecars, with ascending
   numeric `object_ordinal` within each class;
2. `UnitContext` is exact, closed, and non-coercing; `bool` is excluded from
   `subject_sequence`, which is bounded to `0..2^64-1`;
3. the candidate checksum inventory excludes self-reference and the detached ZIP
   SHA-256 identifies the complete submitted archive.

The remediation-scope acceptance did not close either provenance gap at that time.
A later independently captured worktree finding closes only
`CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`; it does not promote or
accept the preserved `fcf406c4...` checkpoint.

### Revision 10 remediation-scope canonical installation verification

On `2026-07-24`, Sentinel verified canonical commit
`ee4a639f9a9429e642391f1fb1e0ab356a6f965a` as the exact documentation-only
installation of the accepted remediation scope.

- parent/install base: `cc2964840d197a40d1c4ef567b42eda762c0be0a`;
- installation package ZIP SHA-256:
  `5c4594a01b6210b1b8865815d4617447c2470720e540ac03d4144836de48a72c`;
- changed paths: `17`;
- replacements: `1`;
- new documentation files: `16`;
- live implementation-source changes: `0`;
- test-source changes: `0`;
- local `HEAD` and fetched `origin/main`: exact match;
- final worktree status entries: `0`.

The accepted remediation scope is therefore `INSTALLED_AND_SENTINEL_VERIFIED`.
Its authorization effect remains `NONE`; no implementation starting SHA,
source-gated commit, Claude implementation prompt, test stage, execution stage,
network/data activity, or downstream phase is active.

---

### Revision 10 remediation source-authoring authorization package

On `2026-07-24`, Gustavo approved conditional authorization package `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01` after Sentinel described the exact three-source atomic boundary and separate test-source/test-execution gates.

Sentinel decision:

`APPROVE — REV10_REMEDIATION_SOURCE_AUTHORIZATION_PACKAGE_ACCEPTED`

- package-preparation base: `a4fb0e64056b58a229da481664e4234e3215cd91`;
- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- accepted remediation package: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- writable paths after activation: exactly `canonical.py`, `finding4_registry.py`, and `prepared_evidence.py`;
- allowed new repository files: `NONE`;
- exact twelve-path expected baseline: pinned in `TWELVE_PATH_STARTING_SHA256SUMS.txt`;
- currently active: `false`;
- activation requires canonical installation verification plus Sentinel acceptance of a local twelve-path source gate;
- test-source authoring and test execution: unauthorized;
- project execution, research data, network, Git history writes by Claude, checkpoint promotion, and downstream stages: unauthorized.

This package does not reuse the historical Revision 09 authorization or promote the preserved checkpoint. A failed source gate is a valid halt and must not be repaired by restoring historical bytes.

### Current twelve-path worktree capture acceptance and installation verification

On `2026-07-25`, Sentinel accepted the independently captured current twelve-path Claude workspace as:

`ACCEPT FINDING — CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`

- source archive SHA-256: `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`;
- source archive size: `487764` bytes;
- archive members: `17`;
- captured source/test paths: `12`;
- all twelve paths: untracked at detached local HEAD `1e1afb29791f42c286b45d3b576f74926add8dce`;
- historical baseline matches: `11`;
- checkpoint-modified `prepared_evidence.py`: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`, `112338` bytes.

Sentinel verified canonical installation commit `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1` as one linear documentation/evidence-only commit after `71061065d91fc391e934d7e79a29eefc898cfe82`. The commit changed exactly `17` paths under `project_context/`, changed no live source/test path, and preserved the exact evidence ZIP.

This closes only `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.
`MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE` remains open. The checkpoint remains `NOT_ACCEPTED`, non-controlling, and authorization effect `NONE`. The accepted capture does not repair the failed source gate, select implementation starting bytes, or authorize implementation, tests, execution, data/network access, or Git writes by Claude.

At that point, Professor was permitted to finalize the SPEC-ONLY starting-state amendment for Sentinel review.

### Revision 10 starting-state amendment Candidate 04 acceptance

On `2026-07-25`, Sentinel accepted `REV23_FINDING4_I0A_REVISION_10_STARTING_STATE_AMENDMENT_CANDIDATE_04` as:

`APPROVE — REV10_STARTING_STATE_AMENDMENT_CANDIDATE_04_ACCEPTED`

- canonical review and installation base: `bc957fe05096b790052d0515773b9e0a2dc88a60`;
- submitted ZIP SHA-256: `9b6e05ff09e916b02b990556ee1ef6a37e3bc044a83c317ecfcc60fa65a63193`;
- submitted ZIP size: `74507` bytes;
- accepted member count: `19`;
- Candidate 03 status: `BLOCKED_NOT_ACCEPTED_NON_CONTROLLING`;
- selected model: `ISOLATED_CAPTURED_PAYLOAD_WORKSPACE_MODEL_V2`;
- exact starting paths: `12`;
- source authoring boundary: `3` writable and `9` protected;
- test authoring boundary: `4` writable and `8` protected;
- baseline-support edit prohibitions: `5`;
- workflow closure: `21` states, `20` stages, `70` stop codes, `20` success codes, and `205` ordered predicate applications.

Candidate 04 resolves the Candidate 03 record-schema and delivery-boundary defects. Halt and success records are structurally closed and cross-field bound to exact workflow rows. Source and test delivery each separate local commit creation, Sentinel local review, separate Gustavo push authorization, one non-force fast-forward push, and Sentinel remote installation verification.

The accepted amendment does not repair or reactivate `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`, accept or promote checkpoint `fcf406c4...`, close `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`, or authorize implementation, tests, execution, data/network activity, or Git writes by Claude.

Canonical installation is documentation-only and remains `PENDING_SENTINEL_VERIFICATION` until the exact commit is returned and verified. Candidate 04 acceptance alone creates no active Claude handoff.

---

## DO NOT REOPEN unless explicitly requested with new evidence

- Rank 1A recalibration.
- OrderFilled topic order.
- The 217/0 and 10/0 artifacts.
- Fee-field diagnostic.
- Named-binary orientation and outcome-source derivation.
- S1 and S1-ALT sampled negatives.
- Option B corrected B0 negative.
- Option C old unsafe C1 designs or a false `C1_CANARY_DESIGN_CLEAR`.
- Option D temporal interpretation.
- P0 representativeness result.
- Amendment 03 versus authorization-anchor distinction.
- Finding 4 approved source stack and accepted materialization.
- The superseded Amendment 03 I0 implementation authorization.
- Revision 08 I0A scope, absent a concrete material contract contradiction.
- Revision 09 private descriptor-set invariant correction, now historical under accepted Revision 10.
- Revision 09 R1 one-file source-resume boundary, now historical and non-reusable under Revision 10.
- Revision 10 T107/T153 reachability, result-domain closure, T166–T230, fixture namespace, call-edge closure, and twelve-path matrix, absent new authoritative evidence.
- The `REVISION10_STATIC_CONFORMANCE_BLOCKED` finding for checkpoint
  `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`, absent new implementation bytes or
  authoritative evidence that changes the reviewed payload or controlling contract.
- The accepted Revision 10 remediation-scope identity, binding Sentinel determinations,
  and verified documentation-only installation at `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`,
  absent new authoritative evidence or a formally accepted amendment.
- The accepted current twelve-path worktree-capture identity and verified installation
  at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`, absent new authoritative evidence that changes the captured bytes or scope.
- The accepted Candidate 04 starting-state amendment identity, closed record domains, exact path boundaries, and commit/review/push/remote-verification separation, absent a concrete contract contradiction or formally accepted later amendment.

---

## Self-correction discipline

One row, one all-one output, one incomplete artifact set, one passing test suite,
or one unverified hash is never sufficient to conclude. Verify authoritative
bytes and contracts before accepting a finding.
