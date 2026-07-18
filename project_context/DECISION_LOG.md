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

---

## Self-correction discipline

One row, one all-one output, one incomplete artifact set, one passing test suite,
or one unverified hash is never sufficient to conclude. Verify authoritative
bytes and contracts before accepting a finding.
