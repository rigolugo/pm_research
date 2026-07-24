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

The scope acceptance closes the revision loop. No Revision 09 should be opened
for optional polish. A later scope amendment requires a concrete material
contradiction that cannot be resolved from the accepted Revision 08 contract.

The commit containing the accepted-scope canonical installation must be returned
to Sentinel for verification before any implementation authorization.

### Finding 4 I0A implementation-authoring authorization

On `2026-07-18`, Gustavo explicitly authorized the bounded Finding 4 I0A
implementation-authoring stage. Sentinel approves authorization ID
`REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01` pinned to verified accepted-scope commit `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`.

Authorized after canonical installation and Sentinel verification of the active
package:

- read-only source sync to the source-gated HEAD;
- exact six implementation-source paths;
- exact six unexecuted test-source paths;
- static inspection, checksums, and implementation review packaging.

Test execution, project imports/execution, research data, general network/API/curl,
empirical work, dependencies/CLI/config, additional paths, Git history/remote
writes, P1/P2/P3, scoring, probe execution, and gate changes remain unauthorized.

The earlier Amendment 03 I0 authorization remains superseded. Revision 08 remains
the accepted scope; no Revision 09 follows for optional polish.

### Finding 4 I0A Revision 09 scope correction

A concrete material contradiction reopened the accepted Revision 08 scope. The
private helper `_validate_descriptor_set_invariants` was required to emit
`PRIVATE_DESCRIPTOR_SET_LOGICAL_HASH_NULLABILITY_INVALID` and
`PRIVATE_DESCRIPTOR_SET_PARTITION_BINDING_INVALID`, but its closed
`_DescriptorSetInvariantInput` and `_DescriptorSetInvariantSummary` exposed
neither logical-hash values nor partition-entry/binding information. Those
outcomes were impossible to determine through the accepted private interface.

Sentinel accepted `REV23_FINDING4_I0A_SCOPE_REVISION_09` on
`2026-07-20` as the narrow SPEC-ONLY correction:

- accepted archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`;
- accepted member count: `14`;
- canonical installation base: `1e963bb6e8387aff071d697a416fa558956e571e`;
- `_validate_descriptor_set_invariants` is narrowed to role cardinality, ordinal
  sequence, canonical-target uniqueness, sidecar relation, then valid;
- logical-hash-nullability validation belongs to
  `validate_prepared_object_descriptor`;
- same-ordinal partition-entry binding belongs to
  `validate_prepared_descriptor_set`.

Revision 09 supersedes Revision 08 only for that private descriptor-set
invariant contract. Revision 08 remains immutable historical accepted evidence.
All public result codes, public assurances, public interfaces, precedence,
fixtures, hashes, role rows, frozen bindings, T001–T165 identities, and the
maximum twelve-path matrix remain preserved except for directly required private
traceability reconciliation.

#### Historical pre-R1 authorization state

Before the later R1 authorization, the Revision 08 implementation authorization
`REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01` did not automatically carry
forward. At that pre-R1 point, Revision 09 implementation, source/test authoring,
source synchronization, and an active Claude implementation prompt were
unauthorized. That paragraph is retained as historical state only.

### Finding 4 I0A Revision 09 R1 source-resume authorization

On `2026-07-21`, Gustavo explicitly authorized Claude's implementation resume and
Sentinel accepted only authorization ID
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

The sole writable path is:

`pm_research/local_curl_per_side/prepared_evidence.py`

Required starting SHA-256:

`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

Sentinel independently verified implementation-review archive SHA-256
`e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`, all internal archive checksum entries, and the exact
twelve-path composite baseline SHA-256 `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`.

The other eleven previously authored source/test paths remain read-only. The
stage permits canonical Revision 09 reads, static AST/source/JSON/text/bytes/hash
inspection, Git status/diff/path inventory/checksums, and one R1 source-only
checkpoint. It does not authorize test-source editing, test collection or
execution, project imports/execution, compilation, lint, type checking,
coverage, CI, another source edit, dependencies/CLI/config/generated files,
implementation ZIP reconstruction, research data, empirical artifacts,
API/RPC/vendor/Dune/curl/general network use, Claude Git history/remote writes,
R2, P1/P2/P3, scoring, probe execution, or gate changes.

Revision 08 authorization remains historical evidence. It does not enlarge the
Revision 09 R1 authorization.

### Finding 4 I0A Revision 09 R1 activation and Claude handoff

On `2026-07-24`, Sentinel verified the exact authorization-installation commit
`1e1afb29791f42c286b45d3b576f74926add8dce` and accepted the one-file R1 stage as active. Gustavo then
explicitly authorized the R1 handoff to Claude.

The exact source-gated local `HEAD` is `1e1afb29791f42c286b45d3b576f74926add8dce`. Only
`pm_research/local_curl_per_side/prepared_evidence.py` may change, from starting
SHA-256 `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`. The other eleven baseline paths remain byte-identical.

This activation does not authorize tests, test-source editing, R2, another
source edit, project execution, research data, network activity, empirical work,
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
- governing scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- source-gated commit: `1e1afb29791f42c286b45d3b576f74926add8dce`
- preservation state: `CANONICALLY_PRESERVED`
- canonical installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- verified installation commit: `58acbac493840c45d84c6b7e33c583d722f4d559`
- conformance state: `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`

Checkpoint preservation and implementation promotion are separate decisions.
Presence of newer bytes does not make them controlling, accepted, executable, or
authorized. Candidate 09 remains non-authoritative until Sentinel decides it.
The checkpoint does not authorize rollback, another source edit, tests, project
execution, network/data access, Git writes by Claude, R2, P1/P2/P3, scoring,
probe execution, or a gate change.

### Checkpoint installation verification

On `2026-07-24`, Sentinel verified canonical commit
`58acbac493840c45d84c6b7e33c583d722f4d559` as exactly one linear documentation/evidence-only commit after
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
- Revision 09 private descriptor-set invariant correction, absent new authoritative evidence.
- Revision 09 R1 one-file source-resume boundary, absent a later Gustavo authorization and Sentinel decision.

---

## Self-correction discipline

One row, one all-one output, one incomplete artifact set, one passing test suite,
or one unverified hash is never sufficient to conclude. Verify authoritative
bytes and contracts before accepting a finding.
