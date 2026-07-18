# REV23 Finding 4 — Bounded Delta Packet 02

## 1. Exact inputs, application order, and scope

This packet applies only after both exact inputs below have been verified:

```text
Base amendment:
REV23_SNAPSHOT_PARTITION_CANCELLATION_AMENDMENT_DRAFT-3.md
SHA-256 3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563

First correction packet:
REV23_FINDING4_BOUNDED_CORRECTION_PACKET.md
SHA-256 b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9
```

Application order is exact:

1. begin with the exact base amendment;
2. apply the first correction packet in full; and
3. apply this second delta packet last.

This packet does not replace or restate the full amendment or the first packet. It contains only the exact clauses changed by the four remaining integration defects and synchronized schema, recovery, finalization, test, traceability, and cross-reference text.

## 2. Defect-to-clause mapping

| Integration defect | Exact clauses replaced or inserted by this packet |
|---|---|
| reachable, noncontradictory `UNSELECTED_CANONICAL_RACE_LOSER` | first-packet §§3.1, 3.3, 4.2, 4.5, 5.1–5.5, 8.1, 8.5–8.7, 9; base §§8.5–8.6 |
| total post-acquisition capture recovery | base §5.2; first-packet §§4.1–4.5, 8.3, 8.5, 9 |
| sidecar and `CONFLICT_STOP_FINALIZED/` adoption integration | base §3.5; first-packet §§3.1, 3.3, 8.1, 8.2, 8.6–8.7, 9 |
| stale final-snapshot and inventory closure | base §§8.5–8.6; first-packet §§5.1–5.5, 8.6–8.7, 9, 10 |

---

## 3. Exact replacement clauses: contention and target adoption

### 3.1 Replace the `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` row in the first packet’s replacement §3.6 table with the following row

| `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` | physical bytes differ and either **(a)** the ordinary adoption requirements in §5.7 hold, including equal claim scope, equal normalized role-specific claim semantics, whitelist-only substitutions, and complete dependent-hash recomputation, or **(b)** the target is exactly `CONFLICT_STOP_FINALIZED/` and the closed exception in §5.7 holds | adopt the existing canonical winner without rewriting any target member; derive a prepared-candidate disposition only for branch (a), because branch (b) is terminal-directory retry resolution rather than prepared-claim supersession |

### 3.2 Replace the paragraph immediately following the first packet’s replacement §3.6 target-result table that begins “A different-intent prepared `FENCE_ACQUIRED` contender” with the following

Before §3.6 target-equivalence resolution is attempted, a prepared `FENCE_ACQUIRED` contender that lost the no-replace race may withdraw as `UNSELECTED_CANONICAL_RACE_LOSER` only under every §5.7 conjunct. Withdrawal means the contender abandons its attempted canonical publication after proving one unique canonical acquisition winner for the same claim scope, sequence, canonical target, and predecessor. The winner is not asserted to satisfy the loser’s different payload intent, so no semantic-adoption result is derived for the loser.

The loser’s own immutable prepared-unit directory is permitted and required evidence; it is expressly excluded from “canonical operational output.” Terminal normal or conflict inventories are permitted and required to reference that directory and its members. No other canonical artifact may operationally reference the loser. A contender that fails any withdrawal conjunct proceeds to ordinary §3.6 resolution and reaches `CONFLICT` unless byte-identical duplication or ordinary semantic adoption is independently proven.

### 3.3 Replace base §3.5’s final paragraph, beginning “For modes 2 and 3,” with the following exact paragraph

For modes 2 and 3, the canonical target is resolved first under §3.7. Sidecar disposition is then derived only from that validated paired canonical target; a candidate sidecar never selects, replaces, or semantically substitutes for the target winner. Reopen the winner target, compute its exact complete-file SHA-256, and derive the sole permitted sidecar bytes from the winner’s registered target path and physical hash. If the sidecar is absent, publish those derived bytes under the applicable mode. If the existing sidecar is byte-identical to those derived bytes, sidecar recovery succeeds. If an immutable mode-2 sidecar exists with different bytes, the sidecar path is `CONFLICT` and maps to the applicable family, fence, or terminal-publication stop, while the already validated target remains the canonical target and is not rewritten. A mode-3 replaceable mirror sidecar may be replaced only from the currently validated generation and is accepted only after the stable mirror-read protocol passes. Sidecar-first publication, independent target/sidecar winner selection, and acceptance of one producer’s target with another producer’s non-derived sidecar are prohibited.

### 3.4 Replace the `UNSELECTED_CANONICAL_RACE_LOSER` subclause in the first packet’s replacement §5.7, from the sentence introducing that disposition through the paragraph ending with “valid but unselected acquisition proposal,” with the following

`UNSELECTED_CANONICAL_RACE_LOSER` is a separate, closed, nonblocking withdrawal disposition. It is evaluated before target-equivalence adoption and is permitted only for one committed prepared `FENCE_ACQUIRED` contender satisfying every conjunct below:

1. exactly one canonical `FENCE_ACQUIRED` winner is committed at the attempted canonical fence target and fully validates;
2. loser and winner have equal recomputed `claim_scope_sha256`;
3. loser and winner have the same `run_id`, `fence_sequence`, canonical target path, and identical nullable `expected_predecessor_commit_sha256`;
4. the common predecessor is the unique valid committed fence head immediately before the race;
5. loser preparation plan, claim-scope bytes, claim-semantic bytes, bound payload-intent bytes, every conditional bundled object, every sidecar, descriptor, and every durable prepared source independently validate;
6. the loser may bind a different valid payload intent and therefore may have different claim-semantic bytes; no semantic-adoption equality is asserted and the winner never satisfies or inherits the loser intent;
7. the loser has no **canonical operational output**. Canonical operational output means any canonical fence directory, payload or release, row batch, authorization-use or capture row, snapshot partition, history/current-view object, aggregate view, cancellation or CONTINUATION object, or normal terminal marker whose provenance selects the loser. The loser’s own immutable prepared-unit directory and its members are not canonical operational output;
8. no operational artifact references the loser `prepared_unit_id`, preparation-plan hash, claim-semantic hash, payload-intent file hash, or payload-intent semantic hash. Terminal inventory entries are not operational references: every applicable normal or conflict terminal inventory must reference and preserve the loser prepared directory and every member exactly once;
9. no semantic identity digest identifies different semantic byte strings in winner, loser, or any referenced object;
10. the loser remains immutable and readable through terminal validation; and
11. no second canonical acquisition, canonical fork, incompatible predecessor, ambiguous winner, or canonical path selected from loser bytes exists.

A qualifying loser is withdrawn before §3.6/§3.7 target-equivalence adoption. It is neither `SUPERSEDED_BY_CANONICAL_WINNER` nor `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED`; the canonical winner does not satisfy the loser’s different intent. The disposition creates no fence ownership, payload permission, cancellation proof, CONTINUATION evidence, snapshot claim, or result evidence.

A transient uncommitted contender may be discarded after independently proving the same unique canonical winner, claim scope, target, sequence, and predecessor; it creates no durable disposition and no inventory entry.

Conflict remains mandatory for a second canonical acquisition, any loser canonical operational output, any prohibited operational reference, an incompatible predecessor, unequal claim scope, invalid or unreadable loser bytes, ambiguous canonical winner, or different semantic bytes under one semantic identity digest. Terminal inventory reference to the loser is required evidence and is never itself a conflict.

### 3.5 Insert the following closed `CONFLICT_STOP_FINALIZED/` exception immediately after the substitution-whitelist table in the first packet’s replacement §5.7

`CONFLICT_STOP_FINALIZED/` has one closed semantic-adoption exception because it is a terminal directory committed without a prepared claim-scope object. An existing canonical `CONFLICT_STOP_FINALIZED/` directory may reach `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` only when all conditions below hold:

1. candidate and winner each contain exactly the four registered paths and no extra member, symlink, or subdirectory;
2. candidate and winner `CONFLICT_INVENTORY.json` bytes are byte-identical, and their inventory sidecars independently derive from their own inventory target bytes and the same registered target path;
3. both marker objects independently validate `conflict_stop_marker_v23` and have equal §21.4.8 marker semantic projections;
4. the only permitted marker-object difference is `created_at_ns`; because that field and the destination field are excluded from the §21.4.8 projection, `conflict_stop_marker_semantic_sha256` must remain equal; every semantic-projection field is equal;
5. after adoption, the canonical winner marker and both winner sidecars are reopened and revalidated against the winner’s physical target hashes;
6. terminal mutual exclusion and all inventory-closure rules validate; and
7. no second incompatible conflict terminal directory or normal terminal marker exists.

For this exception, prepared `claim_scope_sha256` equality is inapplicable and must be null/absent because no prepared claim owns the conflict terminal directory. The exception derives no `SUPERSEDED_BY_CANONICAL_WINNER` prepared disposition. Any inventory-byte difference, marker-semantic difference, member-set difference, invalid sidecar, or terminal-exclusion failure is `CONFLICT`. Physical marker inequality caused solely by the excluded `created_at_ns` field is not a semantic-identity collision.

### 3.6 Replace the first packet’s replacement §17.6 paragraphs governing acquisition contention with the following exact text

For payload and release sequences, a semantically equivalent candidate may be adopted only under ordinary §5.7 whitelist rules. A candidate differing from the acquisition-bound intent cannot be adopted and is `CONFLICT` if it publishes or claims the canonical payload or release target.

For `FENCE_ACQUIRED` only, multiple prepared contenders may legitimately bind different valid payload intents while racing from the same unique predecessor to the same next sequence and target. The first fully valid atomic no-replace canonical directory is the unique acquisition winner. A committed different-intent losing prepared contender is evaluated for `UNSELECTED_CANONICAL_RACE_LOSER` before target-equivalence adoption. Qualification requires equal `claim_scope_sha256`, the same sequence/target/predecessor, independently valid loser bytes, no loser canonical operational output, no prohibited operational reference, immutable retention, and terminal inventory inclusion under §5.7. Its own prepared-unit directory is permitted evidence and terminal inventories must reference it.

Only the intent bound by canonical acquisition `A` may occupy `A+1`. A second canonical acquisition, loser operational output, prohibited operational reference, incompatible predecessor, ambiguous canonical winner, or semantic-identity collision triggers `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, with `STOP_SEMANTIC_ID_COLLISION` taking precedence only for different semantic bytes under one semantic identity digest.

---

## 4. Exact schema and cardinality changes for snapshot-bearing acquisitions

### 4.1 Insert these two rows immediately after `BOUND_PAYLOAD_INTENT_SIDECAR` in base §5.2’s prepared-object role matrix

| `BOUND_SNAPSHOT_CLAIM_SEMANTIC` | `FENCE_ACQUIRED` | exactly 1 when `bound_payload_event_kind` is `CAPTURE_SNAPSHOT_COMMITTED`, `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED`, or `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED`; otherwise 0 | `ATOMIC_BUNDLE_MEMBER` | one bound-snapshot-claim sidecar | non-null and equal to the exact snapshot claim-semantic digest named by the bound payload intent |
| `BOUND_SNAPSHOT_CLAIM_SEMANTIC_SIDECAR` | `FENCE_ACQUIRED` | exactly 1 when `BOUND_SNAPSHOT_CLAIM_SEMANTIC` cardinality is 1; otherwise 0 | `ATOMIC_BUNDLE_MEMBER` | points to `BOUND_SNAPSHOT_CLAIM_SEMANTIC` | null |

The canonical fence-unit member paths are exactly:

```text
bound_snapshot_claim_semantic.json
bound_snapshot_claim_semantic.sha256
```

The JSON file contains the complete exact canonical claim-semantic bytes for the snapshot claim named by the acquisition intent. Its complete-file SHA-256 and its registered semantic digest are distinct and both validate. The sidecar is derived only from the exact canonical member path and complete-file hash.

### 4.2 Replace base §5.2’s unit-kind batch/intent cardinality table with the following

| Unit kind | Bound-intent pair | Bound snapshot-claim-semantic pair | Authorization batch pair | Capture batch pair |
|---|---:|---:|---:|---:|
| `FENCE_ACQUIRED` with snapshot-bearing bound event | 1 | 1 | 0 | 0 |
| `FENCE_ACQUIRED` with non-snapshot-bearing bound event | 1 | 0 | 0 | 0 |
| `AUTHORIZATION_USE_EVENT_COMMITTED` | 0 | 0 | 1 | 0 |
| `REQUEST_RESERVED_COMMITTED` | 0 | 0 | 1 | 0 |
| `CAPTURE_STARTED_COMMITTED` | 0 | 0 | 0 | 1 |
| `CAPTURE_TERMINAL_COMMITTED` | 0 | 0 | 0 | 1 |
| `CAPTURE_SNAPSHOT_COMMITTED` | 0 | 0 | 0 | 0 |
| `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED` | 0 | 0 | 1 | 0 |
| `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` | 0 | 0 | 1 | 0 |
| `FENCE_RELEASED` | 0 | 0 | 0 | 0 |

### 4.3 In both exact field-order lists in the first packet’s replacement §17.5, insert these fields immediately after `bound_payload_intent_semantic_sha256`

```text
bound_snapshot_claim_semantic_file_sha256  nullable SHA256
bound_snapshot_claim_semantic_sha256       nullable SHA256
```

For `fence_event_v23` and `fence_unit_manifest_v23`, the two fields are:

- both non-null only for `FENCE_ACQUIRED` whose `bound_payload_event_kind` is one of the three snapshot-bearing event kinds listed in §4.1 of this packet;
- both null for every non-snapshot-bearing acquisition, every payload unit, and every release;
- mechanically derived from the bundled `bound_snapshot_claim_semantic.json` bytes and their registered semantic projection;
- typed-equal to the snapshot claim-semantic digest in the bound payload-intent object; and
- invalid as a partial pair.

### 4.4 Replace the two `FENCE_ACQUIRED` rows and the payload/release rows in the first packet’s replacement §17.5 nullability matrix with the following

| Unit branch | `previous_fence_unit_file_sha256` | Bound event/file/semantic triple | Bound snapshot-claim file/semantic pair | `payload_intent_semantic_sha256` | Snapshot semantic/physical fields | Reservation triple | Cancellation/activation/validation fields | Payload sequence/hash pair | `release_outcome` |
|---|---|---|---|---|---|---|---|---|---|
| sequence-0 snapshot-bearing `FENCE_ACQUIRED` | null | all non-null; bound event equals intent payload kind; bundled intent validates | both non-null; bundled exact claim-semantic bytes validate and equal intent claim digest | null | all payload-output fields null | all null | all null | both null | null |
| later snapshot-bearing `FENCE_ACQUIRED` | exact prior committed fence manifest hash | all non-null; bound event equals intent payload kind; bundled intent validates | both non-null; bundled exact claim-semantic bytes validate and equal intent claim digest | null | all payload-output fields null | all null | all null | both null | null |
| sequence-0 or later non-snapshot-bearing `FENCE_ACQUIRED` | null only at sequence 0, otherwise exact prior committed fence manifest hash | all non-null; bound event equals intent payload kind; bundled intent validates | both null | null | all payload-output fields null | all null | all null | both null | null |
| each payload kind | exact acquisition manifest hash | all non-null and typed-equal to acquisition triple; bound event equals `event_kind` | both null | non-null and equal to bound semantic digest | exact §17.4 payload branch; snapshot fields only for snapshot-bearing payloads | only cancellation: all non-null | exact event-specific groups | both null | null |
| `FENCE_RELEASED` / `ABORTED_NO_OUTPUT` | exact acquisition manifest hash | all null | both null | null | all null | all null | all null | both null | `ABORTED_NO_OUTPUT` |
| `FENCE_RELEASED` / `COMMITTED` | exact payload manifest hash | all null | both null | null | all null | all null | all null | both non-null and equal to exact payload sequence and manifest complete-file hash | `COMMITTED` |

---

## 5. Exact replacement clauses: capture recovery totality

### 5.1 Replace the first packet’s replacement §17.8 post-table text with the following

For every snapshot-bearing payload:

1. before acquisition, only transient derivation of payload-intent and snapshot claim-semantic bytes may exist;
2. canonical acquisition commits the exact payload-intent object and the complete exact `bound_snapshot_claim_semantic.json` bytes plus sidecar in one atomic fence unit;
3. the acquisition’s bound claim file hash, semantic digest, payload event kind, snapshot identity, ordered capture-relation logical hash, coverage, and authorization/reservation identity all reconcile;
4. no committed capture `SNAPSHOT_PUBLICATION` prepared unit and no new canonical capture partition/history target exists before acquisition;
5. under the same open acquisition, reconstruct the authoritative prefix and validate exact equality with the bundled bound claim bytes;
6. commit exactly one capture `SNAPSHOT_PUBLICATION` prepared unit derived from those bundled claim bytes;
7. under the same open acquisition, promote or adopt only the partitions and history directory matching that prepared unit and bound claim;
8. commit at `A+1` only the payload matching the acquisition intent; and
9. commit the branch-correct release.

A snapshot-bearing acquisition with valid bundled claim bytes is always recoverable to the exact claim and therefore cannot use `ABORTED_NO_OUTPUT`. Once any payload prepared unit, capture snapshot prepared unit, partition, history/current-view target, row-containing payload, or other canonical output named by the intent commits, abort is prohibited for every acquisition kind. A missing, unreadable, invalid, or semantically unequal bound claim object makes the acquisition invalid and reaches `CONFLICT`; it is not an abort path.

### 5.2 Replace the first packet’s replacement §17.10 table and its following paragraph with the following mutually exclusive table and closure rules

### 17.10 Fence recovery classification

The rows below are mutually exclusive after event-kind, prepared-unit existence, canonical-output existence, and release existence are evaluated from durable bytes.

| Durable state | Classification | Exact handling |
|---|---|---|
| transient acquisition staging; no committed prepared contender | `TRANSIENT_ACQUISITION_CONTENDER` | discard or retry from current canonical head |
| unique canonical acquisition winner; transient loser | `TRANSIENT_CANONICAL_RACE_LOSER` | validate winner, claim scope, sequence, target, and predecessor; discard loser; no inventory entry |
| unique canonical acquisition winner; committed different-intent prepared loser satisfying every §5.7 conjunct | `UNSELECTED_CANONICAL_RACE_LOSER` | withdraw proposal before target adoption; retain loser prepared directory; require terminal inventory references; no stop and no operational reference/output |
| snapshot-bearing acquisition; bound claim pair missing, partial, unreadable, invalid, or unequal to intent | `CONFLICT` | `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`; preserve evidence |
| snapshot-bearing acquisition; valid bundled claim pair; no capture snapshot prepared unit; no canonical capture output; payload absent | `BOUND_CAPTURE_PREPARATION_REQUIRED` | derive and commit exactly one acquisition-bound capture prepared unit from bundled claim bytes; abort prohibited |
| snapshot-bearing acquisition; exact bound capture prepared unit committed; no payload prepared unit; no canonical capture partition/history/current-view output; canonical payload absent | `BOUND_CAPTURE_CANONICAL_PROMOTION_REQUIRED` | promote or adopt only the exact prepared partitions/history/current generation under the same open acquisition; abort prohibited |
| snapshot-bearing acquisition; exact bound capture prepared unit committed; no payload prepared unit; at least one bound canonical capture partition/history/current-view output committed; canonical payload absent | `CAPTURE_BINDING_PENDING_RECOVERABLE` | validate and complete the exact promoted set, commit the exact bound payload prepared unit and payload, then commit `COMMITTED` release; abort prohibited |
| non-snapshot-bearing acquisition; no payload prepared unit; no canonical output; payload absent | `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT` | either commit exactly the bound payload or commit `ABORTED_NO_OUTPUT` release with acquisition predecessor and null payload refs |
| any acquisition; exact bound payload prepared unit committed; all event-specific prerequisites complete; canonical payload absent | `BOUND_PAYLOAD_PREPARED_RECOVERABLE` | verify exact intent equality and commit or adopt only that payload; abort prohibited |
| canonical `CAPTURE_STARTED_COMMITTED` payload committed; release absent | `STARTED_RELEASE_PENDING_NO_LAUNCH` | commit exact `COMMITTED` release before process creation; launch remains prohibited |
| canonical non-STARTED payload committed; release absent | `RELEASE_PENDING_RECOVERABLE` | commit `COMMITTED` release with payload predecessor and exact non-null payload refs |
| semantically equal existing fence target under ordinary whitelist | `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` | adopt winner and derive `SUPERSEDED_BY_CANONICAL_WINNER` only when ordinary §5.7 claim equality holds |
| byte-identical existing fence target | `BYTE_IDENTICAL_DUPLICATE_SUCCESS` | use existing target |
| second canonical acquisition, incompatible predecessor, loser operational output/reference, alternate payload, semantic-identity collision, invalid target, missing required recovery source, invalid release branch, or any durable state satisfying no row above | `CONFLICT` | applicable authorization/capture or semantic-ID stop; preserve all evidence |

`OPEN_FENCE_BOUND_INTENT_NO_OUTPUT` is restricted to non-snapshot-bearing acquisitions with no committed payload prepared unit and no canonical output. `BOUND_CAPTURE_PREPARATION_REQUIRED` is restricted to snapshot-bearing acquisitions with valid bundled claim bytes and no capture prepared unit or canonical output. They cannot overlap.

`ABORTED_NO_OUTPUT` is legal only from `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT`. It is prohibited for snapshot-bearing acquisitions and after any prepared payload/snapshot unit or canonical output commits. `COMMITTED` always references the exact canonical payload. Recovery never substitutes a different claim, prepared unit, event kind, authorization identity, or payload intent.

---

## 6. Exact replacement clauses: final snapshot and complete inventories

### 6.1 Replace base §8.5 in full with the following

### 8.5 Final snapshot

A family final snapshot exists only when all conditions below hold:

1. one unique valid committed family head exists;
2. every committed prepared candidate that claims a family snapshot/current-view target is either the selected canonical producer or validly `SUPERSEDED_BY_CANONICAL_WINNER`;
3. every committed prepared `FENCE_ACQUIRED` contender whose bound intent names a snapshot claim for the family is either the canonical acquisition winner or validly `UNSELECTED_CANONICAL_RACE_LOSER`;
4. selected canonical producers, valid `SUPERSEDED_BY_CANONICAL_WINNER` candidates, and valid `UNSELECTED_CANONICAL_RACE_LOSER` contenders are all finalization-neutral after their exact validation and inventory obligations are satisfied;
5. no unresolved prepared unit, invalid race loser, open fence, unbound canonical capture output, publication conflict, fork, cycle, semantic collision, or missing recovery source remains for the family;
6. current generation and legacy mirrors equal the unique head;
7. final inventory closure under §8.6 holds; and
8. the applicable normal finalization marker commits.

A valid race loser never becomes a snapshot candidate, history head, partition source, current view, cancellation proof, CONTINUATION proof, or result source. Conflict-stop finalization does not create a family final snapshot.

### 6.2 Replace base §8.6 in full with the following

### 8.6 Complete inventories

A normal replay or clean-stop final inventory contains every path below exactly once unless the same immutable path is referenced by more than one validated relationship, in which case one inventory entry carries all registered owner relationships:

- the complete history chain from sequence 0 through the unique head;
- every history manifest sidecar;
- every history index;
- every publication marker and sidecar;
- every prepared snapshot unit used by a committed sequence;
- every committed snapshot prepared candidate validly `SUPERSEDED_BY_CANONICAL_WINNER`, including its plan, descriptor, structural sidecars, object payloads, and durable sources;
- every committed current-view generation from sequence 0 through the head, including the exact head generation;
- every legacy current mirror and registered mirror sidecar;
- the union of every immutable partition referenced by every committed historical sequence;
- every prepared fence unit used by a committed fence sequence;
- every committed fence prepared candidate validly `SUPERSEDED_BY_CANONICAL_WINNER`, including its plan, descriptor, structural sidecars, conditional objects, object payloads, and durable sources;
- every committed prepared `FENCE_ACQUIRED` contender validly `UNSELECTED_CANONICAL_RACE_LOSER`, including its complete prepared directory, claim scope, claim semantics, bound payload intent, bound snapshot claim-semantic object when present, all sidecars, descriptor, plan, and durable sources;
- complete canonical fence history and all bundled sidecars;
- every immutable authorization-use and capture row batch and sidecar;
- final aggregate relation views; and
- every terminal inventory source needed to revalidate selected, superseded, and race-loser dispositions.

The normal inventory excludes only itself, its future normal marker and deterministic derivative sidecars, and the selected `NORMAL_FINALIZATION` prepared-unit subtree because that subtree contains the inventory’s own source bytes. This is a closed self-exclusion and does not permit omission of any race loser or superseded unit. The normal marker binds the exact normal-finalization prepared unit, and terminal validation resolves its plan, descriptor, inventory source bytes, marker source bytes, and sidecar sources against committed targets.

A conflict-stop inventory additionally contains every readable pending or invalid prepared unit, every valid superseded unit, every valid race loser, promoted residue, conflicting target, open fence unit, incomplete current view, and unresolved competing semantic claim. It must classify valid race losers as nonconflicting unless independent conflict evidence exists, and it must not claim superseded, race-loser, pending, or conflicting objects are canonical committed evidence.

### 6.3 Replace the first packet’s replacement §21.2 in full with the following

### 21.2 Replay and clean-stop preconditions and commit protocol

Replay or clean-stop finalization requires:

- every snapshot and fence chain valid and cycle-free;
- every committed prepared candidate classified as selected canonical producer, `SUPERSEDED_BY_CANONICAL_WINNER`, or `UNSELECTED_CANONICAL_RACE_LOSER`;
- every race loser satisfying equal claim scope, unique winner, common sequence/target/predecessor, independently valid bytes, no canonical operational output, no prohibited operational reference, immutability, and terminal inventory inclusion under §5.7;
- no unresolved prepared claim, invalid pre-acquisition capture unit, promoted unbound capture output, open fence, conflicting canonical target, or semantic collision;
- every superseded and unselected committed prepared unit fully retained and inventoried;
- current views and aggregate views equal committed sources; and
- complete normal final inventory closure under §8.6.

A legitimate semantically superseded loser or acquisition race loser does not block finalization. Terminal inventory references to a valid race loser are required and do not violate the prohibition on operational references. An unvalidated loser, missing or invalid canonical winner, loser canonical operational output, prohibited operational reference, invalid pre-acquisition capture unit, or unresolved semantic claim blocks normal finalization.

Normal V10 publication remains marker-last under unchanged normal-finalization claim semantics and the corrected §3.5 sidecar rule. V10 finalization atomicity stops remain limited to V10 terminal publication.

### 6.4 Replace these two bullets in the first packet’s replacement §21.3

Replace:

```text
- a committed candidate that cannot be validated as selected, SUPERSEDED_BY_CANONICAL_WINNER, or UNSELECTED_CANONICAL_RACE_LOSER;
- canonical output or a canonical reference from a purported race loser;
```

with:

```text
- a committed candidate that cannot be validated as selected canonical producer, SUPERSEDED_BY_CANONICAL_WINNER, or UNSELECTED_CANONICAL_RACE_LOSER;
- canonical operational output or a prohibited operational reference from a purported race loser; required terminal inventory references are excluded from this trigger;
```

### 6.5 Replace the prepared-disposition paragraph in the first packet’s replacement §21.4.4 with the following

`prepared_unit_id` and `claim_scope_sha256` are non-null exactly for paths owned by or selected, superseded, or withdrawn from one prepared plan. For `UNSELECTED_CANONICAL_RACE_LOSER`, the inventory validator must resolve equal claim scope, one unique canonical acquisition winner, the common sequence/target/predecessor, independently valid loser bytes, absence of loser canonical operational output and prohibited operational references, immutable retention, and complete inventory coverage. The loser’s own prepared-unit directory and terminal inventory references are expressly permitted and required. A valid race loser normally has no conflict group; a group is present only for independently detected conflict evidence affecting the same path.

---

## 7. Synchronized tests

### 7.1 Replace the different-intent race-loser positive and rejection requirements in the first packet’s replacement §24.3 with the following

Positive tests construct two independently valid committed prepared `FENCE_ACQUIRED` contenders with equal `claim_scope_sha256`, identical run/sequence/target/predecessor, different valid payload intents, and exactly one canonical no-replace winner. They prove the loser is withdrawn before target-equivalence adoption, its own prepared directory is not canonical operational output, no operational artifact references it, every applicable terminal inventory references it exactly once, and it does not block finalization.

Counterexamples prove conflict for unequal claim scope, different predecessor, second canonical acquisition, invalid loser bytes, loser canonical operational output, prohibited operational reference, missing terminal inventory coverage, ambiguous winner, or semantic-identity collision. A terminal inventory reference alone must never produce conflict.

### 7.2 Append the following positive and counterexample requirements to the first packet’s replacement §24.4

Positive conflict-terminal retry: two `CONFLICT_STOP_FINALIZED/` candidates have byte-identical inventory bytes and equal §21.4.8 marker semantic projections and semantic digests while only `created_at_ns` differs. The first valid canonical directory is adopted under the closed §5.7 exception without prepared claim-scope equality.

Reject conflict-terminal adoption for different inventory bytes, unequal marker semantics, invalid or cross-paired sidecars, extra/missing members, terminal-marker coexistence, or a difference in any marker semantic field other than the already excluded `created_at_ns`.

### 7.3 Replace the first packet’s replacement §24.6 in full with the following

### 24.6 Acquisition-bound capture preparation and promotion tests

Positive snapshot-bearing order is exact:

1. derive transient payload-intent and complete snapshot claim-semantic bytes;
2. commit acquisition containing the exact intent object, exact claim-semantic object, and both sidecars;
3. reopen and validate both hashes and semantic equality;
4. reconstruct and validate the authoritative capture prefix under that acquisition;
5. commit exactly one bound capture `SNAPSHOT_PUBLICATION` prepared unit;
6. promote or adopt exact partitions, history, and current generation under the same acquisition;
7. commit at `A+1` only the bound snapshot-bearing payload; and
8. commit `COMMITTED` release.

Crash recovery tests cover every boundary and must reach exactly one mutually exclusive §17.10 row. A snapshot-bearing acquisition with valid bundled claim bytes and no prepared/canonical output reaches `BOUND_CAPTURE_PREPARATION_REQUIRED`, not `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT`. An exact prepared capture unit with no canonical output reaches `BOUND_CAPTURE_CANONICAL_PROMOTION_REQUIRED`. Any canonical capture output without payload reaches `CAPTURE_BINDING_PENDING_RECOVERABLE`.

Reject missing/partial/invalid bound claim pair, abort from any snapshot-bearing acquisition, abort after any prepared unit or canonical output, committed pre-acquisition capture prepared unit, pre-acquisition partition/history promotion, alternate claim or prepared unit, generic acquisition, alternate `A+1`, promotion after release, prefix validation outside the acquisition, or different snapshot/row/coverage/authorization identity.

### 7.4 Replace the recovery/contention portion of the first packet’s replacement §24.10 with the following

Positive contention tests require equal claim scope, common sequence/target/predecessor, one unique canonical acquisition, independently valid loser bytes, different valid intents, no loser canonical operational output, no prohibited operational reference, immutable retention, and required terminal inventory references. The loser’s prepared directory is expressly allowed and required.

Recovery tests enumerate every §17.10 row and prove mutual exclusivity. Snapshot-bearing acquisitions bundle exact claim-semantic bytes and cannot abort. Non-snapshot-bearing acquisitions may reach `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT` only before any payload prepared unit or canonical output exists. Once any prepared unit or canonical output commits, abort is rejected. STARTED payload release remains mandatory before launch.

Reject a second canonical acquisition, unequal claim scope, incompatible predecessor, invalid loser bytes, loser operational output/reference, missing loser inventory, missing/invalid bound snapshot claim bytes, overlapping recovery classifications, abort from a snapshot-bearing acquisition, abort after preparation/output, semantic-ID collision, invalid release branch, or fence atomicity mapped to V10.

### 7.5 Replace the race-loser and terminal-adoption bullets in the first packet’s replacement §24.14 with the following

- classify a valid different-intent acquisition loser as `UNSELECTED_CANONICAL_RACE_LOSER` only after equal claim scope, unique winner, common sequence/target/predecessor, valid loser bytes, no operational output/reference, immutable retention, and terminal inventory inclusion are proven;
- permit and require terminal inventory references to the loser prepared directory while rejecting every operational reference;
- require no conflict group for the loser absent independently detected conflict;
- include every committed race-loser path exactly once;
- prove `CONFLICT_STOP_FINALIZED/` semantic adoption only with byte-identical inventory and equal §21.4.8 marker semantics under the closed exception; and
- reject cross-paired or independently selected sidecars.

### 7.6 Replace the normal-finalization positive/rejection sentence in the first packet’s replacement §24.15 with the following

Positive normal finalization proves base §8.5 and §8.6 exactly: selected canonical producers, valid `SUPERSEDED_BY_CANONICAL_WINNER` candidates, and valid `UNSELECTED_CANONICAL_RACE_LOSER` contenders are finalization-neutral only after complete validation and inventory coverage; every race loser is present exactly once and supplies no canonical snapshot, fence, cancellation, CONTINUATION, or result evidence. Reject omission of a race loser, operational reference to a loser, loser canonical output, invalid claim scope/predecessor, open fence, overlapping recovery classification, snapshot-bearing abort, or conflict-terminal adoption outside the exact exception.

---

## 8. Synchronized traceability rows

### 8.1 Replace the first packet’s `different-intent acquisition race loser` traceability row with the following

| different-intent acquisition race withdrawal | §§3.6, 5.7, 17.6, 17.10, 21.2–21.4.4 | equal claim scope; same sequence/target/predecessor; unique canonical winner; independently valid loser bytes; no canonical operational output or prohibited operational reference; immutable retention; terminal inventories required and allowed | nonblocking only as `UNSELECTED_CANONICAL_RACE_LOSER`; otherwise applicable authorization/capture or semantic-ID stop | §§24.3, 24.10, 24.14–24.15 |

### 8.2 Replace the first packet’s `acquisition-bound capture preparation and promotion` traceability row with the following

| acquisition-bound snapshot claim and total capture recovery | §§5.2, 17.5–17.10 | snapshot-bearing acquisition bundles exact claim-semantic bytes/hash; exact prepared unit and all canonical promotion occur under same open fence; mutually exclusive recovery states; no snapshot-bearing abort | authorization/capture stop for missing/invalid claim, pre-acquisition commit, alternate claim, or abort violation | §§24.6, 24.10 |

### 8.3 Insert these rows immediately after the ordinary target-resolution traceability row

| authoritative-target-derived sidecar disposition | §§3.5, 3.7, 5.7 | target winner resolved first; sole sidecar derived from winner path/hash; no independent sidecar winner | applicable family/fence/terminal stop for immutable mismatched sidecar | §§24.3–24.4, 24.14 |
| conflict-terminal retry adoption | §§3.6, 5.7, 21.4.8 | byte-identical inventory plus equal marker semantic projection; `created_at_ns` excluded; no prepared claim-scope equality | V10 conflict only for incompatible terminal directory | §§24.4, 24.14–24.15 |

### 8.4 Insert this row immediately after the snapshot-chain finalization row

| final snapshot and complete loser inventory closure | §§8.5–8.6, 21.2 | selected, superseded, and valid race-loser candidates finalization-neutral only after complete validation; every race loser inventoried exactly once and never used operationally | normal finalization blocked on omission, invalid loser, open fence, or unresolved conflict | §§24.14–24.15 |

---

## 9. Exact cross-reference updates

Apply only these exact cross-reference edits after the first packet:

1. Delete first-packet §10 item 7 in full. The complete base §§8.5–8.6 replacements in §§6.1–6.2 of this packet supply the governing text instead.
2. Replace first-packet §10 item 8 in full with: “In base §26 schema-registry amendments, add `UNSELECTED_CANONICAL_RACE_LOSER`; add `BOUND_CAPTURE_CANONICAL_PROMOTION_REQUIRED`; add the two bound snapshot-claim fields and conditional object pair defined in §4 of this packet; retain the split `FENCE_RELEASED` branches; and keep `CANONICAL_PHYSICAL_OBJECT_ADOPTED` absent from the target-result enum.”
3. Replace the first-packet §9 `different-intent acquisition race loser` traceability row only with §8.1 of this packet.
4. Replace the first-packet §9 `acquisition-bound capture preparation and promotion` traceability row only with §8.2 of this packet.
5. Insert the two §8.3 rows and the one §8.4 row at the exact locations stated there.
6. Replace base §§8.5–8.6 only with §§6.1–6.2 of this packet.

---

## 10. Unchanged-text and authorization statement

Every base-amendment byte and every first-correction-packet clause not expressly replaced or inserted by this second delta remains unchanged under the exact application order in §1.

This packet authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local project-data reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
