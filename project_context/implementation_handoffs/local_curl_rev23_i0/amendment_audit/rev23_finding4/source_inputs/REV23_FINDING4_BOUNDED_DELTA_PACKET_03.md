# REV23 Finding 4 — Bounded Delta Packet 03

## 1. Exact inputs and application order

This packet applies only after these exact inputs, in this order:

1. base amendment SHA-256 `3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563`;
2. first correction-packet SHA-256 `b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9`;
3. Delta Packet 02 SHA-256 `184da5779afc301255cd6532e456727380f14e4f0f32bad30f2b4bd010bb76c2`.

The packet changes only the exact clauses identified below. It does not restate or replace any other role-matrix row, snapshot rule, fence rule, finalization rule, test, traceability row, or authorization boundary.

---

## 2. Exact object-role and path insertions

### 2.1 Insert these two paths in base §4.6 immediately after the two `bound_payload_intent` paths

```text
<capture_root>/commit_fence_history/<20d>/bound_snapshot_claim_semantic.json          [snapshot-bearing FENCE_ACQUIRED only]
<capture_root>/commit_fence_history/<20d>/bound_snapshot_claim_semantic.sha256        [snapshot-bearing FENCE_ACQUIRED only]
```

“Snapshot-bearing `FENCE_ACQUIRED`” means an acquisition whose exact `bound_payload_event_kind` is one of:

```text
CAPTURE_SNAPSHOT_COMMITTED
CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED
CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED
```

For every other fence-unit branch, both paths are prohibited. The JSON and sidecar are members of the same atomic fence-history directory as `FENCE_UNIT.json`, `fence_event.json`, and `bound_payload_intent.json`. They may not be published, recovered, or selected independently of that directory.

### 2.2 Insert these two values in the exact base §5.1 closed `object_role` domain immediately after `BOUND_PAYLOAD_INTENT_SIDECAR`

```text
BOUND_SNAPSHOT_CLAIM_SEMANTIC
BOUND_SNAPSHOT_CLAIM_SEMANTIC_SIDECAR
```

The two role/cardinality rows and their logical-hash nullability previously inserted by Delta Packet 02 §4.1 remain governing and are not restated. After this insertion, those rows are members of the closed role domain rather than unreachable matrix values.

---

## 3. Separate acquisition-race scope from prepared claim scope

### 3.1 Insert new §5.4A immediately after effective §5.4

### 5.4A `acquisition_race_scope_sha256`

`acquisition_race_scope_sha256` is a derived validation digest used only to determine whether independently valid prepared `FENCE_ACQUIRED` contenders participated in the same no-replace acquisition race. It is not a replacement for `claim_scope_sha256`, is not a semantic-adoption identity, and is not independently caller supplied.

Its exact typed projection, in this exact order, is:

```text
schema_version                         STRING = local_curl_acquisition_race_scope.v23
spec_revision                          UINT = 23
run_id                                 STRING /^run_[0-9a-f]{64}$/
fence_sequence                         UINT
canonical_acquisition_target_path      STRING
expected_predecessor_commit_sha256     SHA256 or NULL
```

`canonical_acquisition_target_path` is the normalized run-relative final directory path, without a trailing slash, for the exact acquisition sequence:

```text
<capture_root>/commit_fence_history/<fence_sequence_20d>
```

It is derived from the contender’s registered fence-history target path and must be identical to the parent directory of every canonical fence-unit member target claimed by that contender. A contender with member targets resolving to more than one directory has no valid acquisition race scope.

`expected_predecessor_commit_sha256` is null exactly for `fence_sequence=0`; otherwise it is the exact complete-file SHA-256 of the unique valid canonical `fence_unit_manifest_v23` at `fence_sequence-1`. The value is read from and checked against the contender’s persisted claim scope and canonical predecessor bytes; it is not inferred from timestamps or from another contender.

Construct one canonical typed row using the effective typed-cell contract and compute:

```text
acquisition_race_scope_sha256 =
    SHA256(canonical_typed_row_json_bytes)
```

There is no trailing LF. The digest is recomputed independently for every contender from its persisted bytes.

Two `FENCE_ACQUIRED` contenders are in the same acquisition race if and only if their recomputed `acquisition_race_scope_sha256` values are equal. Their event kinds, conditional object sets, bound payload intents, bound snapshot-claim objects, full `object_claims` arrays, and `claim_scope_sha256` values may differ. Equal acquisition race scope never establishes ordinary semantic equivalence.

Full `claim_scope_sha256` equality remains mandatory for every ordinary `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` decision under §§3.6–3.7 and 5.7. It is not required for `UNSELECTED_CANONICAL_RACE_LOSER` withdrawal.

Different run ID, fence sequence, canonical acquisition target path, or nullable predecessor value means a different race and cannot qualify for withdrawal against that winner.

### 3.2 Replace Delta Packet 02 §3.2 in full with the following

Before §3.6 target-equivalence resolution is attempted, a committed prepared `FENCE_ACQUIRED` contender that lost the no-replace directory race may withdraw as `UNSELECTED_CANONICAL_RACE_LOSER` only under every effective §5.7 conjunct. Withdrawal requires one unique fully valid canonical acquisition winner with equal recomputed `acquisition_race_scope_sha256`. It does not require equal `claim_scope_sha256`, because different valid event kinds and conditional object sets may participate in one acquisition race.

The loser abandons its attempted acquisition proposal before target-equivalence adoption. The winner is not asserted to satisfy the loser’s bound event kind, payload intent, conditional object set, claim scope, or claim-semantic bytes. Therefore no `BYTE_IDENTICAL_DUPLICATE_SUCCESS`, `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED`, or `SUPERSEDED_BY_CANONICAL_WINNER` result is derived for that loser.

The loser’s own immutable prepared-unit directory and every member remain permitted and required evidence; those paths are excluded from “canonical operational output.” Terminal normal or conflict inventories are permitted and required to reference those paths. No snapshot, fence, row, cancellation, CONTINUATION, current-view, aggregate, or other operational artifact may reference or select the loser.

A contender that fails withdrawal qualification proceeds to ordinary target resolution only when it actually asserts an existing canonical target. Conflict remains mandatory for a second canonical acquisition, unequal acquisition race scope, incompatible predecessor, invalid or unreadable loser bytes, loser canonical operational output, prohibited operational reference, ambiguous winner, or semantic-identity collision.

### 3.3 Replace the `UNSELECTED_CANONICAL_RACE_LOSER` subclause supplied by Delta Packet 02 §3.4 in full with the following

`UNSELECTED_CANONICAL_RACE_LOSER` is a separate, closed, nonblocking withdrawal disposition evaluated before target-equivalence adoption. It is permitted only for one committed prepared `FENCE_ACQUIRED` contender satisfying every conjunct below:

1. exactly one canonical `FENCE_ACQUIRED` winner is committed at the attempted canonical acquisition directory and fully validates;
2. loser and winner have equal independently recomputed `acquisition_race_scope_sha256` under §5.4A;
3. the shared race scope proves the same `run_id`, `fence_sequence`, normalized canonical acquisition target directory, and identical nullable `expected_predecessor_commit_sha256`;
4. the shared predecessor is null only for sequence 0 and otherwise is the unique valid committed fence head immediately before the race;
5. the loser’s preparation plan, claim-scope bytes, role-specific claim-semantic bytes, bound payload-intent bytes, any conditional bound snapshot-claim bytes, every sidecar, descriptor, and every durable prepared source independently validate;
6. loser and winner may bind different event kinds, conditional object sets, payload intents, claim scopes, and claim-semantic bytes; none of those differences is adopted by the winner;
7. the loser has no canonical operational output. Its own immutable prepared-unit directory and members are expressly excluded from canonical operational output;
8. no operational artifact references the loser `prepared_unit_id`, preparation-plan hash, claim-scope hash, claim-semantic hash, payload-intent file hash, payload-intent semantic hash, or bound snapshot-claim hash. Required terminal inventory rows are expressly permitted and are not operational references;
9. no semantic identity digest identifies different semantic bytes;
10. the loser remains immutable and readable through terminal validation and every applicable terminal inventory includes every loser path exactly once under the normal one-row-per-path rule in §8.6;
11. there is no second canonical acquisition, incompatible canonical predecessor, canonical fork, ambiguous canonical winner, or canonical path selected from loser bytes.

A qualifying loser is neither `SUPERSEDED_BY_CANONICAL_WINNER` nor an ordinary semantic-adoption result. It creates no fence ownership, payload permission, cancellation proof, CONTINUATION evidence, snapshot claim, current-view permission, or result evidence.

A transient uncommitted contender may be discarded after proving the same unique canonical winner and equal acquisition race scope; it creates no durable disposition and no inventory entry.

Conflict remains mandatory for different race scope, a second canonical acquisition, incompatible predecessor, invalid or unreadable loser bytes, loser operational output, prohibited operational reference, ambiguous winner, or semantic-identity collision. Different `claim_scope_sha256` values alone are not conflict when the contender qualifies under this subclause.

### 3.4 Replace the acquisition-contention paragraphs supplied by Delta Packet 02 §3.6 with the following

For payload and release sequences, semantic adoption remains governed only by ordinary §5.7 equality and the exact role whitelist. A payload or release candidate differing from the canonical acquisition-bound intent is `CONFLICT` if it claims or publishes the canonical target.

For `FENCE_ACQUIRED` only, multiple independently valid prepared contenders may race from the same unique predecessor to the same next sequence and canonical acquisition directory while binding different event kinds, conditional object sets, payload intents, claim scopes, and claim-semantic bytes. The first fully valid atomic no-replace canonical directory is the unique acquisition winner.

A committed losing contender is evaluated for `UNSELECTED_CANONICAL_RACE_LOSER` before any target-equivalence adoption. Qualification requires equal recomputed `acquisition_race_scope_sha256`, independently valid loser bytes, no loser canonical operational output, no prohibited operational reference, immutable retention, and exact terminal inventory inclusion. Ordinary `claim_scope_sha256` equality is neither required nor sufficient for this withdrawal; it remains required for ordinary semantic adoption.

Only the intent bound by canonical acquisition `A` may occupy `A+1`. A different sequence, target, or predecessor, a second canonical acquisition, loser operational output, prohibited operational reference, invalid loser bytes, ambiguous winner, or semantic-identity collision triggers `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, with `STOP_SEMANTIC_ID_COLLISION` taking precedence only for its exact semantic-identity condition.

---

## 4. Capture current-view timing corrections

### 4.1 Replace the final paragraph supplied by Delta Packet 02 §5.1 with the following

A snapshot-bearing acquisition with valid bundled claim bytes is recoverable only to that exact claim and therefore cannot use `ABORTED_NO_OUTPUT`. Once any capture snapshot prepared unit, payload prepared unit, canonical partition, canonical history directory, row-containing payload, or other pre-release canonical output permitted by the bound intent commits, abort is prohibited. A missing, unreadable, invalid, or semantically unequal bound claim object makes the acquisition invalid and reaches `CONFLICT`; it is not an abort path.

Current-view generation directories, legacy current mirrors, and their sidecars are not permitted pre-release canonical outputs. For capture snapshots they may be published, adopted, or repaired only after the exact snapshot payload at `A+1` and its `FENCE_RELEASED(COMMITTED)` unit are both durable and revalidated. Their absence before release is not a capture-binding defect.

### 4.2 Replace these three rows in effective §17.10 with the following rows

| Durable state | Classification | Exact handling |
|---|---|---|
| unique canonical acquisition winner; committed prepared loser with equal `acquisition_race_scope_sha256` satisfying every effective §5.7 conjunct | `UNSELECTED_CANONICAL_RACE_LOSER` | withdraw before target adoption; retain loser prepared directory; require exact terminal inventory rows; no stop and no operational reference/output |
| snapshot-bearing acquisition; exact bound capture prepared unit committed; no payload prepared unit; no canonical capture partition or history-directory output; canonical payload absent | `BOUND_CAPTURE_CANONICAL_PROMOTION_REQUIRED` | under the same open acquisition, promote or adopt only the exact immutable partitions and exact history directory named by the bound prepared unit; do not publish a current generation or legacy mirror; abort prohibited |
| snapshot-bearing acquisition; exact bound capture prepared unit committed; no payload prepared unit; at least one bound canonical capture partition or history-directory output committed; canonical payload absent | `CAPTURE_BINDING_PENDING_RECOVERABLE` | under the same open acquisition, validate and complete only the exact partition/history set, commit the exact bound payload prepared unit and canonical payload, then commit `FENCE_RELEASED(COMMITTED)`; current generation and mirrors remain prohibited until after release |

Replace the two closure paragraphs following the effective §17.10 table with the following exact text:

`OPEN_FENCE_BOUND_INTENT_NO_OUTPUT` is restricted to non-snapshot-bearing acquisitions with no committed payload prepared unit and no canonical output. `BOUND_CAPTURE_PREPARATION_REQUIRED` is restricted to snapshot-bearing acquisitions with valid bundled claim bytes and no capture prepared unit, partition, or history-directory output. They cannot overlap.

`ABORTED_NO_OUTPUT` is legal only from `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT`. It is prohibited for snapshot-bearing acquisitions and after any prepared payload/snapshot unit, partition, history directory, row-containing payload, or other permitted canonical output commits. Capture current generation and legacy mirrors are prohibited until the exact payload and `FENCE_RELEASED(COMMITTED)` are durable. `COMMITTED` always references the exact canonical payload. Recovery never substitutes a different claim, prepared unit, event kind, authorization identity, payload intent, or acquisition race winner.

### 4.3 Insert this paragraph at the beginning of base §7.4, before “After a unique committed head exists”

For the `capture` family, a history sequence does not grant current-view publication permission by itself. Before any current-view generation or legacy mirror is published, adopted, or repaired, the validator must reopen the exact `CAPTURE_SNAPSHOT_COMMITTED`, `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED`, or `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` payload that bound the head history sequence and the exact following `FENCE_RELEASED(COMMITTED)` unit. Both must be durable, chain-valid, and semantically equal to the head snapshot claim. A promoted history directory with an open fence has no current-view generation and no legacy mirror. Analysis families retain the existing head-based timing.

### 4.4 Replace the generic `CURRENT_VIEW_REPAIRABLE` row in effective §7.5 with the following row

| Durable state | Classification | Exact handling | Normal-finalization eligible after handling |
|---|---|---|---:|
| valid committed head; for `capture`, exact bound snapshot payload and following `FENCE_RELEASED(COMMITTED)` both durable; current generation or mirrors missing/stale | `CURRENT_VIEW_REPAIRABLE` | publish or repair only from the validated committed head after the capture release condition, or directly from the committed head for analysis families | after repair |

A capture current-view target present before the required committed release is not `CURRENT_VIEW_REPAIRABLE`; it is prohibited canonical output and maps to `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` while all evidence is preserved.

---

## 5. Normal-inventory one-row-per-path semantics

### 5.1 Replace the opening sentence supplied by Delta Packet 02 §6.2 with the following

A normal replay or clean-stop final inventory contains exactly one entry for every unique normalized included path listed below. The inventory entry count therefore equals the cardinality of the set of included normalized paths after applying only the closed self-exclusions in this section. A path is never duplicated because it participates in more than one validated relationship.

### 5.2 Insert the following immediately after the inventory bullet list supplied by Delta Packet 02 §6.2 and before its self-exclusion paragraph

Each entry uses the already declared normal-inventory row schema and adds no fields. Its existing `artifact_role` and `producer_stage` values are selected deterministically as follows:

1. resolve the normalized path against the effective schema registry’s canonical inventory-classification registry;
2. an exact registered path entry, when present, is the sole match;
3. otherwise exactly one registered dynamic path grammar must match;
4. prepared-unit structural files and prepared object members use the canonical role and producer stage registered for that structural path or `prepared_evidence_object_v23.object_role` under its `unit_kind`;
5. a selected, superseded, or race-loser disposition does not alter the path’s canonical `artifact_role` or `producer_stage`; and
6. zero matches or multiple matches is `STOP_FINALIZATION_INVENTORY_INVALID`.

The registry must therefore assign exactly one canonical `(artifact_role,producer_stage)` pair to every path grammar included by §8.6. The pair is a path classification, not an ownership list.

Snapshot-sequence membership, current-head membership, prepared-unit membership, semantic supersession, race-loser withdrawal, row-batch ownership, and terminal-source relationships are validated during inventory closure by reopening the governing manifests, preparation plans, descriptors, fence units, and disposition evidence. Those secondary relationships do not create additional inventory rows and are not serialized into undeclared inventory fields.

If one immutable path supports multiple compatible relationships, the one row retains only the registry-selected canonical role/stage pair; closure separately proves every required relationship. Contradictory relationships block finalization and do not create duplicate rows.

---

## 6. Synchronized schema, producer-consumer, and materialization clauses

### 6.1 Replace base §26 item 3 with the following

3. materialize the total role/cardinality/sidecar/logical-hash matrix, including partition cardinality as `len(snapshot_claim.partition_entries)`; register `BOUND_SNAPSHOT_CLAIM_SEMANTIC` and `BOUND_SNAPSHOT_CLAIM_SEMANTIC_SIDECAR` in the closed `object_role` domain; register their exact conditional §4.6 paths; and enforce exactly one pair for snapshot-bearing `FENCE_ACQUIRED` and zero pairs for every other branch;

### 6.2 Replace base §26 item 5 with the following

5. materialize the exact role-specific canonical-winner substitution whitelist and semantic/physical distinction; add the exact derived `local_curl_acquisition_race_scope.v23` projection from §5.4A; use acquisition-race equality only for `UNSELECTED_CANONICAL_RACE_LOSER`; and retain full `claim_scope_sha256` equality for ordinary semantic adoption;

### 6.3 Replace base §26 item 8 with the following

8. add `capture_payload_intent_v23`; register acquisition-bound intent objects and the closed bound snapshot-claim object pair; materialize exact fence event/manifest fields, total nullability, cancellation reservation hash, `acquisition_race_scope_sha256` derivation, and the rule that capture current generation/mirrors may publish only after the exact snapshot payload and `FENCE_RELEASED(COMMITTED)` are durable;

### 6.4 Replace base §26 item 11 with the following

11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; materialize normal final-inventory cardinality as exactly one row per unique normalized included path; register exactly one canonical `(artifact_role,producer_stage)` classification for every included exact/dynamic path grammar; prohibit owner arrays or undeclared relationship fields; and validate snapshot, prepared-unit, superseded-unit, and race-loser relationships separately during closure;

### 6.5 Insert this row in base §23.1 immediately after the `prepared evidence unit` row as replaced by the first correction packet

| Artifact | Sole producer class | Required consumers |
|---|---|---|
| acquisition-bound snapshot claim-semantic object and bundled sidecar | fence coordinator, only inside a snapshot-bearing canonical `FENCE_ACQUIRED` atomic directory | acquisition validator, bound capture prepared-unit producer, payload validator, recovery, inventories, Sentinel |

### 6.6 Insert these rows in base §27 immediately after `acquisition-bound payload intent`

| Artifact | Producer | Consumer | Cardinality | Lifecycle |
|---|---|---|---|---|
| acquisition-bound snapshot claim-semantic object and sidecar | fence coordinator | acquisition validator, capture snapshot preparation, payload/recovery validator, Sentinel | exactly one pair per snapshot-bearing `FENCE_ACQUIRED`; zero otherwise | immutable atomic-bundle members; never independent snapshot output |
| derived acquisition race scope | contention validator from persisted contender and predecessor bytes | race-loser classifier, recovery, terminal closure | exactly one recomputed value per valid prepared or canonical acquisition contender | derived only; not a canonical artifact and not semantic-adoption identity |

### 6.7 Replace the `current generation/mirrors` row in base §27 with the following

| Artifact | Producer | Consumer | Cardinality | Lifecycle |
|---|---|---|---|---|
| current generation/mirrors | current-view projector | current readers/finalizer | one head generation; one mirror set | analysis: after unique head; capture: only after exact bound snapshot payload and `FENCE_RELEASED(COMMITTED)`; generation immutable, mirrors replaceable preterminal |

### 6.8 Insert this row in base §27 immediately after `normal V10 inventory/marker`

| Artifact | Producer | Consumer | Cardinality | Lifecycle |
|---|---|---|---|---|
| normal inventory path entry | V10 normal finalizer from canonical inventory-classification registry | terminal validator, Sentinel | exactly one row per unique normalized included path | immutable within committed inventory; secondary relationships validated externally without extra fields |

### 6.9 Replace the race-loser bullet in effective §21.2 with the following

```text
- every race loser satisfying equal recomputed acquisition race scope, unique winner, common sequence/target/predecessor, independently valid bytes, no canonical operational output, no prohibited operational reference, immutability, and terminal inventory inclusion under §5.7;
```

### 6.10 Replace the prepared-disposition paragraph supplied by Delta Packet 02 §6.5 with the following

`prepared_unit_id` and `claim_scope_sha256` are non-null exactly for paths owned by or selected, superseded, or withdrawn from one prepared plan. `claim_scope_sha256` identifies that loser’s own prepared claim; it is not required to equal the canonical acquisition winner’s claim scope. For `UNSELECTED_CANONICAL_RACE_LOSER`, the inventory validator must resolve equal recomputed `acquisition_race_scope_sha256`, one unique canonical acquisition winner, the common run/sequence/target/predecessor, independently valid loser bytes, absence of loser canonical operational output and prohibited operational references, immutable retention, and complete one-row-per-path inventory coverage. The loser’s own prepared-unit directory and terminal inventory references are expressly permitted and required. A valid race loser normally has no conflict group; a group is present only for independently detected conflict evidence affecting the same path.

---

## 7. Affected tests

### 7.1 Append the following to effective §24.2

Positive role-registration tests enumerate the closed `object_role` domain and prove both bound snapshot-claim roles are present. For each snapshot-bearing acquisition, assert exactly one JSON/sidecar pair at the exact §4.6 paths, correct atomic-directory membership, non-null JSON logical hash, null sidecar logical hash, and typed equality with the bound intent. For every other branch, assert cardinality zero and path absence. Reject a matrix role absent from the closed domain, alternate path/case, standalone publication, extra pair, partial pair, or cross-paired sidecar.

### 7.2 Replace the different-intent acquisition-race positive and rejection paragraphs in effective §24.3 with the following

Positive tests construct independently valid `FENCE_ACQUIRED` contenders with the same run, sequence, normalized acquisition target directory, and nullable predecessor but different event kinds, conditional object sets, bound intents, claim scopes, and claim semantics. They recompute equal `acquisition_race_scope_sha256`, commit exactly one canonical winner, classify the committed loser as `UNSELECTED_CANONICAL_RACE_LOSER`, retain and inventory every loser path, and prove no ordinary semantic adoption occurred.

Counterexamples reject different race sequence, target, or predecessor; invalid loser bytes; second canonical acquisition; loser operational output/reference; ambiguous winner; or semantic-identity collision. Unequal `claim_scope_sha256` alone must not reject a qualifying race loser. Ordinary semantic-adoption tests continue to require equal full claim scope and claim semantics.

### 7.3 Replace effective §24.6 with the following

### 24.6 Acquisition-bound capture preparation, promotion, release, and current-view tests

Positive snapshot-bearing order is exact:

1. derive transient payload-intent and complete snapshot claim-semantic bytes;
2. commit one canonical acquisition containing the exact intent pair and bound snapshot-claim pair;
3. reopen and validate both pairs, their physical hashes, semantic digests, event kind, and acquisition race scope;
4. reconstruct and validate the authoritative capture prefix under that acquisition;
5. commit exactly one bound capture `SNAPSHOT_PUBLICATION` prepared unit;
6. under the same acquisition, promote or adopt only the exact immutable partitions and exact history directory;
7. commit at `A+1` only the bound snapshot-bearing payload;
8. commit `FENCE_RELEASED(COMMITTED)`; and
9. only then publish/adopt the current generation and repair legacy mirrors.

Crash recovery tests cover every boundary and reach exactly one effective §17.10 row. Before payload commit, `BOUND_CAPTURE_CANONICAL_PROMOTION_REQUIRED` and `CAPTURE_BINDING_PENDING_RECOVERABLE` may operate only on partitions and the history directory. Missing current generation/mirrors before release is not a binding defect. After payload and release, missing/stale current views reach `CURRENT_VIEW_REPAIRABLE`.

Reject missing/partial/unregistered bound claim roles or paths, alternate claim/prepared unit, generic acquisition, alternate `A+1`, pre-acquisition canonical capture publication, current generation or mirror publication before committed release, promotion after release, prefix validation outside acquisition, snapshot/row/coverage/authorization mismatch, or abort from a snapshot-bearing acquisition.

### 7.4 Replace the contention and capture-recovery paragraphs in effective §24.10 with the following

Contention tests recompute `acquisition_race_scope_sha256` from exact persisted bytes. Positive different-intent contenders share run/sequence/target/predecessor while differing in valid event kind, conditional objects, claim scope, and intent; exactly one canonical acquisition wins and the loser is nonblocking only under all effective §5.7 requirements. Ordinary semantic-adoption tests separately require equal full claim scope and whitelist-valid semantics.

Recovery tests prove that capture binding under an open fence publishes or repairs only exact partitions and history. Current generation and legacy mirrors remain absent until exact payload and `FENCE_RELEASED(COMMITTED)` are durable. Reject any pre-release current-view target, a race loser with different acquisition race scope, a second canonical acquisition, invalid loser bytes, loser operational output/reference, missing loser inventory, or semantic-ID collision.

### 7.5 Replace the first race-loser bullet supplied by Delta Packet 02 §7.5 with the following

```text
- classify a valid different-intent acquisition loser as `UNSELECTED_CANONICAL_RACE_LOSER` only after equal recomputed acquisition race scope, unique winner, common run/sequence/target/predecessor, valid loser bytes, no operational output/reference, immutable retention, and terminal inventory inclusion are proven;
```

Append the following normal-inventory requirements to effective §24.14:

Normal-inventory tests construct paths with multiple compatible secondary relationships and require exactly one row per normalized path. Each row’s existing `artifact_role` and `producer_stage` must equal the unique canonical registry classification. Closure must independently validate every snapshot, prepared-unit, superseded-unit, and race-loser relationship without owner arrays or any undeclared field. Reject duplicate rows, zero/multiple registry matches, a disposition-derived role replacing the canonical path role, an undeclared relationship field, or a relationship omitted from closure merely because the path row is unique.

### 7.6 Replace the normal-finalization sentence supplied by Delta Packet 02 §7.6 with the following

Positive normal finalization proves effective §§8.5–8.6 exactly: selected canonical producers, valid `SUPERSEDED_BY_CANONICAL_WINNER` candidates, and valid `UNSELECTED_CANONICAL_RACE_LOSER` contenders are finalization-neutral only after complete validation and one-row-per-path inventory coverage. A race loser requires equal acquisition race scope, not equal winner claim scope, and supplies no canonical snapshot, fence, cancellation, CONTINUATION, current-view, or result evidence. Reject omission or duplication of a loser path, operational reference to a loser, loser canonical output, invalid acquisition race scope/predecessor, noncanonical inventory role/stage, open fence, overlapping recovery classification, snapshot-bearing abort, pre-release capture current-view publication, or conflict-terminal adoption outside the exact existing exception.

---

## 8. Affected traceability rows

### 8.1 Insert this row immediately after `prepared source/path/ordinal/cardinality closure`

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| bound snapshot-claim role and path closure | §§4.6, 5.1–5.2, 17.5 | closed object roles; exact conditional JSON/sidecar paths; one pair only for snapshot-bearing acquisition | `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` for absent/extra/partial/unregistered pair | §§24.2, 24.6, 24.10 |

### 8.2 Replace the effective `different-intent acquisition race withdrawal` row with the following

| different-intent acquisition race withdrawal | §§3.6, 5.4A, 5.7, 17.6, 17.10, 21.2–21.4.4 | equal acquisition race scope from run/sequence/target/predecessor; unique canonical winner; independently valid loser; no operational output/reference; immutable retention; terminal inventory required; full claim-scope equality not required | nonblocking only as `UNSELECTED_CANONICAL_RACE_LOSER`; otherwise applicable authorization/capture or semantic-ID stop | §§24.3, 24.10, 24.14–24.15 |

### 8.3 Replace the effective `acquisition-bound snapshot claim and total capture recovery` row with the following

| acquisition-bound snapshot claim and total capture recovery | §§4.6, 5.1–5.2, 7.4–7.5, 17.5–17.10 | registered bound claim pair; exact prepared unit; pre-release promotion limited to partitions/history; payload and COMMITTED release precede current generation/mirrors | authorization/capture stop for missing/invalid pair, alternate claim, pre-release current view, or sequencing violation | §§24.2, 24.6, 24.10 |

### 8.4 Insert this row immediately after `final snapshot and complete loser inventory closure`

| normal inventory one-row-per-path closure | §§8.6, 21.2, 26–27 | one unique normalized path row; unique registered canonical artifact role and producer stage; secondary relationships validated outside row schema | `STOP_FINALIZATION_INVENTORY_INVALID` for duplicate path, ambiguous/unregistered classification, undeclared field, or missing relationship proof | §§24.14–24.15 |

---

## 9. Exact cross-reference updates

1. Replace only the race-loser qualification bullet in effective §21.2 with §6.9 of this packet.
2. Replace only the prepared-disposition paragraph originating in Delta Packet 02 §6.5 with §6.10 of this packet.
3. In effective §8.5 condition 3, the existing phrase `validly UNSELECTED_CANONICAL_RACE_LOSER` resolves to effective §5.7 as replaced by §3.3 of this packet; no §8.5 bytes are otherwise replaced.
4. In effective §8.6, replace only the opening sentence and insert only the row-semantics text from §§5.1–5.2 of this packet. The inventory path list and closed self-exclusions remain otherwise unchanged.
5. Replace only the three effective §17.10 rows listed in §4.2 and the two immediately following closure paragraphs quoted there.
6. Replace only the final paragraph originating in Delta Packet 02 §5.1 with §4.1.
7. Insert only the capture timing paragraph in base §7.4 and replace only the effective `CURRENT_VIEW_REPAIRABLE` row as specified in §§4.3–4.4.
8. In base §26, replace only items 3, 5, 8, and 11 with §§6.1–6.4. Do not renumber any item.
9. In base §§23.1 and 27, apply only §§6.5–6.8.
10. Replace only the tests and traceability rows explicitly identified in §§7–8.

---

## 10. Unchanged-text and authorization statement

Except for the exact replacements and insertions in this packet, every byte of the base amendment, the first correction packet, and Delta Packet 02 remains unchanged and continues to govern in the stated application order.

This packet authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
