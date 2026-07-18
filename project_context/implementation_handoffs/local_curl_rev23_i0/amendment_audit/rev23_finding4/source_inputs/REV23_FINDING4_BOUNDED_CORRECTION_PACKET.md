# REV23 Finding 4 — Bounded Correction Packet

## 1. Base binding and packet scope

This packet applies only to:

```text
REV23_SNAPSHOT_PARTITION_CANCELLATION_AMENDMENT_DRAFT-3.md
```

Base SHA-256:

```text
3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563
```

This is not a complete replacement amendment. It contains only complete replacement text for the clauses affected by the five localized Sentinel blockers, together with synchronized recovery/finalization classifications, tests, traceability rows, and cross-reference updates.

## 2. Blocker-to-section mapping

| Blocker | Base clauses replaced | Synchronized clauses |
|---|---|---|
| ordinary different-intent acquisition race loser | §§5.7–5.8, 7.5, 17.6, 17.10 | §§21.2–21.4.4, 23.1, 23.3, 24.3, 24.10, 24.14–24.15, 29 |
| no durable pre-acquisition capture snapshot claim | §§7.1–7.3, 17.8 | §§7.5, 17.10, 23.3, 24.6, 29 |
| exact existing-target result trichotomy | §§3.6–3.7, 5.7, 7.2, 7.5 | §§17.6, 24.3–24.4, 29 |
| split `FENCE_RELEASED` nullability and predecessor rules | §§17.5, 17.7, 17.10 | §§24.9–24.10, 24.15, 29 |
| total `primary_stop_code` selection | §21.4.1, §22.2 | §§21.4.7–21.4.8 by reference, 24.14–24.15, 29 |

---

## 3. Exact replacement clauses

### 3.1 Replace base §3.6 in full with the following

### 3.6 Atomic directory promotion and existing-target resolution

`ATOMIC_DIRECTORY_PROMOTION` means all of the following:

1. source and target parent are on the same filesystem;
2. the complete source directory is created under a hidden sibling staging name;
3. every member file is closed and durably flushed;
4. the source directory and its parent are durably flushed;
5. the source directory is renamed to the exact final directory by one atomic no-replace operation;
6. the final parent directory is durably flushed;
7. if the final directory already exists, no member is overwritten, merged, deleted, or replaced; and
8. the producer reopens the existing directory and resolves the attempted target through exactly one result below.

| Existing-target result | Exact condition | Effect |
|---|---|---|
| `BYTE_IDENTICAL_DUPLICATE_SUCCESS` | the complete recursive relative-path set is identical and every corresponding member has equal file size and complete-file SHA-256 | the existing target satisfies the attempted publication; no new canonical bytes are written |
| `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` | physical bytes differ, but the existing target is a fully valid canonical winner, claim scope and role-specific claim semantics are equal after applying only the exact §5.7 substitution whitelist, every differing member role is whitelist-eligible, and all dependent hashes are recomputed from the winner | adopt the existing canonical winner; derive the candidate disposition under §5.7; no target member is rewritten |
| `CONFLICT` | neither of the two conditions above is proven, including invalid/unreadable canonical bytes, a non-whitelisted difference, unequal canonical semantics, ambiguous target membership, incompatible canonical commits, or missing recovery sources | emit the applicable family, fence, semantic-ID, or V10 stop under §§22.1–22.2; preserve all durable evidence |

These three values are the complete existing-directory-target result domain. Physical inequality alone is never sufficient for `CONFLICT`. Semantic adoption is permitted only through the exact role whitelist in §5.7.

A different-intent prepared `FENCE_ACQUIRED` contender that satisfies `UNSELECTED_CANONICAL_RACE_LOSER` under §5.7 does not claim that the existing target satisfies its intent and therefore does not create a fourth existing-target result. It withdraws its unselected prepared claim after independently validating the canonical winner.

Unsupported no-replace directory promotion is not silently weakened to per-file writes and maps to the stage-specific stop in §22.1.

### 3.2 Replace base §3.7 in full with the following

### 3.7 Atomic single-authoritative-file promotion and existing-target resolution

`ATOMIC_SINGLE_FILE_PROMOTION` means all of the following:

1. create the complete target bytes under a hidden sibling file on the same filesystem;
2. close and durably flush the file;
3. durably flush the parent directory;
4. atomically no-replace rename the file to the exact final path;
5. durably flush the parent directory;
6. reopen and verify exact size and complete-file SHA-256; and
7. if the final path already exists, do not overwrite it and resolve it through exactly one result below.

| Existing-target result | Exact condition | Effect |
|---|---|---|
| `BYTE_IDENTICAL_DUPLICATE_SUCCESS` | existing target size and complete-file SHA-256 equal the candidate | the existing target satisfies the attempted publication |
| `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` | bytes differ, but both objects independently validate their registered schemas and logical projections, their role-specific claim semantics are equal after only the §5.7 whitelist substitutions, and every dependent hash is recomputed from the existing winner | adopt the existing target without rewriting it; derive the candidate disposition under §5.7 |
| `CONFLICT` | neither condition above is proven | emit the applicable typed stop; preserve candidate and canonical bytes |

These three values are the complete existing-file-target result domain. A role for which §5.7 permits no substitution can reach semantic adoption only when its registered semantic projection is still equal without changing a prohibited field; otherwise the result is `CONFLICT`. Different valid Parquet physical bytes are not a collision when their exact registered ordered logical rows and all semantic identity fields are equal.

The target-file rename is the sole commit point. A sidecar, later marker, or consumer cannot make uncommitted target bytes authoritative. Unsupported no-replace promotion is never weakened to overwrite, merge, or check-then-write and maps to the stage-specific stop in §22.1.

### 3.3 Replace base §5.7 in full with the following

### 5.7 Canonical-winner adoption, candidate disposition, and exact substitution whitelist

An existing canonical target is resolved only through the three §3.6/§3.7 target results. Candidate disposition is a separate derived classification and cannot add a fourth target result.

A candidate that reaches `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` is `SUPERSEDED_BY_CANONICAL_WINNER` only if claim scope and claim-semantic digests recompute equal and every differing field validates under this exact whitelist. Fields not listed for that role must be typed-equal before and after normalization.

| Exact object role(s) | Sole permitted winner substitutions | Required recomputation |
|---|---|---|
| `PARTITION_PAYLOAD` | descriptor `durable_source_path`, `file_size_bytes`, `file_sha256` | none; `logical_sha256`, partition ID, rows, bounds, and target path remain equal |
| `HISTORY_INDEX`, `CURRENT_GENERATION_INDEX`, `LEGACY_CURRENT_INDEX` | descriptor physical source/size/hash; decoded row fields `size_bytes`, `file_sha256`, and destination `snapshot_partition_row_sha256` only where the row references an adopted partition physical variant | recompute every affected row hash and the index ordered-relation logical hash; all semantic partition fields remain equal |
| `AUTHORIZATION_USE_ROW_BATCH`, `CAPTURE_ROW_BATCH` | descriptor physical source/size/hash and paired sidecar bytes/hash | none; complete decoded rows, row hashes, batch logical hash, count, and bounds remain equal |
| `HISTORY_MANIFEST`, `CURRENT_GENERATION_MANIFEST`, `LEGACY_CURRENT_MANIFEST` | `created_at_ns`; `partition_entries[*].size_bytes`; `partition_entries[*].file_sha256`; `partition_entries_logical_sha256` | recompute `partition_entries_logical_sha256` from winner-bound physical entries; all predecessor, ID, path, logical-hash, row-count, key, total, and coverage fields remain equal |
| `PUBLICATION_MARKER` (`snapshot_publication_commit_v23`) | `preparation_plan_file_sha256`, `prepared_unit_id`, `manifest_file_size_bytes`, `manifest_file_sha256`, `history_index_file_size_bytes`, `history_index_file_sha256`, `committed_at_ns`, destination semantic hash | recompute destination semantic hash; all claim-scope/claim-semantic, run/family/sequence/predecessor, relation, and capture-binding fields remain equal |
| `CURRENT_GENERATION_MARKER` (`snapshot_current_view_commit_v23`) | `preparation_plan_file_sha256`, `prepared_unit_id`, current manifest/index physical sizes/hashes, `committed_at_ns`, destination semantic hash | recompute destination semantic hash; head sequence/history hash/claim semantics remain equal |
| `BOUND_PAYLOAD_INTENT` | none | byte equality required for semantic adoption |
| `FENCE_UNIT_MANIFEST`, `FENCE_EVENT` | `preparation_plan_file_sha256`, `prepared_unit_id`, child physical file hashes/sizes already proven equivalent, `event_ts_ns`, destination logical/row hashes that include only those whitelisted physical fields | recompute affected destination hashes; sequence/predecessor/event/epoch/token, intent hashes, logical batch/snapshot hashes, identities, and release outcome remain equal |
| `NORMAL_FINAL_INVENTORY` | none | exact canonical inventory byte equality required |
| `NORMAL_FINAL_MARKER` | `normal_finalization_prepared_unit_id`, `created_at_ns`, destination semantic hash | recompute marker semantic hash; marker kind, stop/result, inventory hash, and inventory schema/logical/count fields remain equal |
| every sidecar role | complete sidecar bytes and sidecar physical hash, only as deterministic function of the paired winner's unchanged target path and winner target physical hash | recompute sidecar bytes/hash; paired ordinal/path remain equal |

No field omitted from the table may be substituted. `content_schema_id`, canonical target path, claim-scope hash, claim-semantic hash, logical row/relation hashes, semantic identities, sequence/predecessor values, bound payload intent, authorization/reservation identity, and release outcome may never differ during semantic adoption.

For every whitelisted replacement, all dependent physical-reference fields and physical aggregate hashes are recomputed from the winner; no stale candidate-derived hash may remain. The normalized interpreted objects must then produce equal exact claim-semantic bytes.

Adoption requirements are all mandatory:

1. winner is fully committed, readable, structurally valid, and recoverable;
2. candidate and winner have equal recomputed `claim_scope_sha256`;
3. candidate and winner have equal recomputed claim-semantic schema and digest;
4. every Parquet variant independently validates §5.3;
5. sidecars validate only with their own producer target;
6. predecessor, run/family/sequence, semantic identities, counts, bounds, and domains agree;
7. no canonical artifact selects the loser as a second winner;
8. winner source bytes and every transitive recovery source remain durable; and
9. every committed loser remains immutable and enters terminal inventory.

`UNSELECTED_CANONICAL_RACE_LOSER` is a separate, closed, nonblocking disposition. It is permitted only for a prepared `FENCE_ACQUIRED` contender and requires all of the following:

1. one unique canonical `FENCE_ACQUIRED` winner is already committed and fully validates;
2. loser and winner claim the same `(run_id,fence_sequence,canonical target path)` and have identical non-null or null `expected_predecessor_commit_sha256` values;
3. that predecessor is the unique committed fence head immediately before the race;
4. loser preparation plan, claim-scope object, claim-semantic object, payload-intent object, and every prepared source byte independently validate;
5. loser may contain a different valid bound payload intent and therefore may have different claim-semantic bytes; this is not semantic adoption and the loser never supplies its intent to the winner;
6. no loser byte, member, sidecar, row batch, snapshot, partition, history directory, fence event, or fence manifest was promoted to any canonical target;
7. no canonical artifact references the loser `prepared_unit_id`, plan hash, claim-semantic hash, or payload-intent file/semantic hash;
8. loser has no semantic identity digest collision: no one digest identifies two different semantic byte strings;
9. loser remains immutable and is included in every applicable terminal inventory; and
10. no second canonical acquisition, incompatible canonical predecessor, or canonical fork exists.

A transient uncommitted acquisition contender that loses the no-replace race may be discarded after the same canonical-winner and predecessor checks; it creates no durable disposition or inventory entry.

`UNSELECTED_CANONICAL_RACE_LOSER` is not `SUPERSEDED_BY_CANONICAL_WINNER`: the canonical winner does not satisfy the loser's different intent. It is also not `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` and is not a fourth existing-target result. It is the withdrawal of a valid but unselected acquisition proposal after a unique canonical winner is established.

Fork/collision stops remain mandatory for incompatible canonical commits, different semantic bytes under one semantic identity digest, a second canonical acquisition, unequal canonical sequence topology, invalid winner bytes, ambiguous winner assignment, missing winner recovery sources, any canonical output from a purported race loser, or any canonical reference to that loser. Physical Parquet inequality with equal ordered-relation bytes is not a conflict.

### 3.4 Replace base §5.8 in full with the following

### 5.8 Prepared-unit commit, retention, and recovery

Except for the capture-specific acquisition rule below, the producer constructs exact claim-scope bytes, claim-semantic bytes, sidecars, plan, exact object-source bytes, plan sidecar, descriptor, and descriptor sidecar under transient staging, closes and flushes all members, and atomically no-replace promotes the complete prepared directory. That directory rename is the sole prepared-unit commit point.

For `unit_kind=SNAPSHOT_PUBLICATION` with `subject_family=capture`, pre-acquisition work is transient only. No capture snapshot prepared directory may be committed before the exact acquisition-bound payload intent is canonical. Under the same open acquisition, the producer must derive and commit the exact capture snapshot prepared unit whose claim-semantic digest equals the digest named by the acquisition intent, then perform any new partition and history promotion under §§7.1–7.3 and 17.8. The acquisition intent excludes prepared-unit ID and physical target hashes, so this ordering introduces no hash cycle.

A committed prepared candidate is finalization-neutral only after it is one of:

- selected canonical producer;
- `SUPERSEDED_BY_CANONICAL_WINNER`; or
- `UNSELECTED_CANONICAL_RACE_LOSER` satisfying every §5.7 condition.

Every other committed candidate is pending, invalid, or conflicting and blocks normal finalization. A committed capture `SNAPSHOT_PUBLICATION` unit with no matching earlier open acquisition and bound intent is `PRE_ACQUISITION_CAPTURE_PREPARED_PROTOCOL_VIOLATION`; it is not a valid semantic claim, cannot be adopted or reused, remains immutable evidence, and maps to `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` with the applicable capture snapshot stop taking precedence only when canonical capture snapshot bytes were also promoted or invalid.

Every selected, superseded, and unselected-race-loser prepared unit—including its plan, plan sidecar, descriptor, descriptor sidecar, and all `objects/<ordinal>.bin` bytes—remains immutable through the applicable terminal inventory. A recovery unit may use `REUSE_IMMUTABLE_SOURCE` only under the exact source-equals-target rule in §5.1. Hash-only intent, absent source bytes, invalid source path, symlink source, ambiguous target, or unrecoverable transitive source is not recovery evidence.

### 3.5 Replace base §7.1 in full with the following

### 7.1 Snapshot preparation timing

For analysis families, a committed snapshot prepared unit may precede canonical publication and must contain or durably reference every byte required to recover every new/reused partition, history bundle, current-generation bundle, and legacy mirror target under the total §5.2 matrix.

For `capture`, only transient staging may precede acquisition. Before acquisition, a producer may derive transient partition bytes, exact snapshot claim bytes, and exact payload-intent bytes, but it must not:

- atomically commit a capture `SNAPSHOT_PUBLICATION` prepared unit;
- promote a new canonical capture partition;
- promote a capture history directory; or
- create any canonical reference to the transient bytes.

The canonical `FENCE_ACQUIRED` unit binds the exact payload-intent semantic hash, including snapshot sequence, snapshot claim semantic hash, capture ordered-relation logical hash, coverage, event kind, and relevant authorization/reservation identity. Only while that acquisition remains the unique open fence may the producer:

1. rederive the authoritative capture prefix under the fence;
2. prove exact equality with the bound snapshot claim;
3. commit the exact capture `SNAPSHOT_PUBLICATION` prepared unit;
4. promote or adopt every new/reused partition under §7.2;
5. promote or adopt the exact history directory under §7.3;
6. commit only the bound payload at `A+1`; and
7. commit the matching release.

A process loss before acquisition leaves only transient staging, which may be discarded or rederived and has no semantic-claim or inventory status. A process loss after acquisition uses only the acquisition-bound prepared unit and recovery rules in §§7.5 and 17.10.

### 3.6 Replace base §7.2 in full with the following

### 7.2 Immutable partition publication and physical-object adoption

For each partition candidate:

1. validate durable source bytes and the registered logical projection;
2. for `capture`, require the matching open acquisition and exact bound snapshot intent before any new canonical partition promotion or adoption attempt;
3. if the canonical target is absent, atomically no-replace promote the candidate file and reopen it;
4. if the target exists, resolve it through exactly the §3.7 trichotomy;
5. `BYTE_IDENTICAL_DUPLICATE_SUCCESS` binds the existing physical hash and size;
6. `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` requires independent decoding of both Parquet files, equal schema, exact ordered typed rows, `partition_id`, row count, key bounds, ordering, and partition logical hash, followed by winner-bound recomputation under §5.7;
7. when the same `partition_id` maps to different semantic bytes, emit `STOP_SEMANTIC_ID_COLLISION`; and
8. every other `CONFLICT` emits the applicable family snapshot stop.

The first valid no-replace physical object remains immutable. No producer rewrites it to obtain byte equality. A later history manifest/index binds the canonical winner's actual file hash and size. If an earlier analysis prepared manifest referenced a losing physical hash, a recovery prepared unit may reuse the canonical winner and the earlier unit becomes `SUPERSEDED_BY_CANONICAL_WINNER`. For capture, the winner-bound capture prepared unit itself is committed only under the acquisition; no pre-acquisition committed prepared manifest may be repaired or reused.

### 3.7 Replace base §7.3 paragraphs preceding `PUBLICATION_COMMITTED.json` with the following

### 7.3 Atomic history-directory publication

For analysis families, the producer builds the exact five-member history bundle, validates it, and atomically no-replace promotes it. A pre-existing target is resolved only through §3.6: byte-identical duplicate success, whitelist-limited semantic winner adoption, or conflict.

For `capture`, history publication is permitted only after all of these are true under one open acquisition:

```text
FENCE_ACQUIRED committed with exact immutable payload intent
→ authoritative capture prefix and exact bound snapshot claim validated
→ exact capture SNAPSHOT_PUBLICATION prepared unit committed under that acquisition
→ every new/reused canonical partition promoted or adopted under that acquisition
→ exact history directory atomically promoted or adopted
→ only the payload matching the bound intent committed at A+1
→ branch-correct FENCE_RELEASED committed
```

No capture snapshot prepared unit, new capture partition target, or capture history target is committed before acquisition. If validation fails before any canonical output, the acquisition may close with `ABORTED_NO_OUTPUT`. If atomic partition/history promotion is unsupported or irrecoverably fails, emit `STOP_CAPTURE_SNAPSHOT_INVALID`; an aborted release is allowed only when no canonical output named by the intent was committed. If canonical output commits and process loss occurs before the payload, the still-open fence prevents later proof-relevant commits and recovery resumes only the exact acquisition-bound prepared unit, payload, and release. No alternate snapshot claim or prepared unit may be substituted.

### 3.8 Replace base §7.5 in full with the following

### 7.5 Complete snapshot recovery and contention classification

| Durable state | Classification | Exact handling | Normal-finalization eligible after handling |
|---|---|---|---:|
| transient analysis staging only; no committed prepared unit | `TRANSIENT_ONLY` | discard or restart | yes |
| transient capture staging; no acquisition | `TRANSIENT_CAPTURE_PREPARATION` | discard or rederive; it is not a durable claim | yes |
| one valid analysis prepared unit; no canonical target | `PREPARED_READY` | resume exact unit | after completion |
| acquisition committed with bound capture snapshot intent; capture prepared unit absent | `BOUND_CAPTURE_PREPARATION_REQUIRED` | derive and commit exactly the bound capture prepared unit under the open acquisition | after completion |
| exact bound capture prepared unit committed under the open acquisition; no canonical capture output | `BOUND_CAPTURE_PREPARED_RECOVERABLE` | promote/adopt exact partitions and history under that acquisition | after completion |
| committed capture prepared unit exists without a matching earlier open acquisition/bound intent | `PRE_ACQUISITION_CAPTURE_PREPARED_PROTOCOL_VIOLATION` | preserve; no adoption or reuse; authorization/capture stop | no |
| existing target is byte-identical | `BYTE_IDENTICAL_DUPLICATE_SUCCESS` | use existing target | after completion |
| existing target is semantically equivalent under exact §5.7 whitelist | `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` | adopt winner; derive `SUPERSEDED_BY_CANONICAL_WINNER`; inventory committed loser | yes |
| valid canonical acquisition winner; different-intent prepared acquisition contender satisfies every §5.7 race-loser rule | `UNSELECTED_CANONICAL_RACE_LOSER` | withdraw contender; retain committed prepared bytes in inventory; no canonical output/reference | yes |
| strict subset of exact analysis partitions promoted | `PARTITION_PROMOTION_PARTIAL_RECOVERABLE` | promote/adopt remaining exact partitions | after completion |
| analysis history directory absent | `HISTORY_DIRECTORY_PENDING_RECOVERABLE` | promote/adopt exact directory if predecessor remains head | after completion |
| capture history promoted under open fence; binding payload absent; exact bound prepared unit valid | `CAPTURE_BINDING_PENDING_RECOVERABLE` | commit exact payload and branch-correct release under same acquisition | after completion |
| capture canonical output promoted but no matching open acquisition exists | `CAPTURE_OUTPUT_PROMOTED_OUTSIDE_FENCE` | applicable capture snapshot/auth-capture stop; preserve evidence | no |
| valid committed head; current generation/mirrors missing or stale | `CURRENT_VIEW_REPAIRABLE` | reconstruct from head | after repair |
| existing target fails byte equality and whitelist-limited semantic equivalence | `CONFLICT` | applicable family or semantic-ID stop | no |
| two different canonical committed sequence claims | `PUBLICATION_FORK_CONFLICT` | applicable family snapshot stop | no |
| committed target lacks required durable source bytes | `RECOVERY_SOURCE_MISSING` | applicable family snapshot stop | no |

`CANONICAL_PHYSICAL_OBJECT_ADOPTED` is removed as a standalone existing-target result; it is a specific instance of `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED`. An unselected different-intent acquisition contender is not a fork and does not adopt the winner's intent. Fork status requires incompatible canonical commits or a genuine semantic-identity collision.

---

## 4. Affected fence schema and nullability replacements

### 4.1 Replace base §17.5 in full with the following

### 17.5 `fence_event_v23` and `fence_unit_manifest_v23`

`fence_event_v23` exact field order remains:

```text
schema_version                              STRING = local_curl_capture_fence_event.v23
spec_revision                               UINT16 = 23
run_id                                      STRING
fence_sequence                              UINT64
event_kind                                  STRING
preparation_plan_file_sha256                SHA256
prepared_unit_id                            STRING
fence_epoch                                 UINT64
fence_token_sha256                          SHA256
acquire_fence_sequence                      UINT64
covered_through_fence_sequence              nullable UINT64
bound_payload_event_kind                    nullable STRING
bound_payload_intent_file_sha256            nullable SHA256
bound_payload_intent_semantic_sha256        nullable SHA256
payload_intent_semantic_sha256               nullable SHA256
payload_fence_sequence                      nullable UINT64
payload_fence_unit_file_sha256               nullable SHA256
release_outcome                             nullable STRING {COMMITTED, ABORTED_NO_OUTPUT}
event_ts_ns                                 UTC_NS
```

Event kinds remain exactly:

```text
FENCE_ACQUIRED
AUTHORIZATION_USE_EVENT_COMMITTED
REQUEST_RESERVED_COMMITTED
CAPTURE_STARTED_COMMITTED
CAPTURE_TERMINAL_COMMITTED
CAPTURE_SNAPSHOT_COMMITTED
CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED
CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED
FENCE_RELEASED
```

`fence_unit_manifest_v23` exact field order remains:

```text
schema_version                           STRING = local_curl_capture_fence_unit_manifest.v23
spec_revision                            UINT16 = 23
run_id                                   STRING
fence_sequence                           UINT64
previous_fence_unit_file_sha256          nullable SHA256
preparation_plan_file_sha256             SHA256
prepared_unit_id                         STRING
fence_event_file_sha256                  SHA256
event_kind                               STRING
fence_epoch                              UINT64
fence_token_sha256                       SHA256
acquire_fence_sequence                   UINT64
covered_through_fence_sequence           nullable UINT64
bound_payload_event_kind                 nullable STRING
bound_payload_intent_file_sha256         nullable SHA256
bound_payload_intent_semantic_sha256     nullable SHA256
payload_intent_semantic_sha256           nullable SHA256
row_batches                              ARRAY[immutable_row_batch_v23]
row_batches_semantic_logical_sha256      SHA256
snapshot_claim_semantic_sha256           nullable SHA256
capture_snapshot_sequence                nullable UINT64
capture_snapshot_manifest_file_sha256    nullable SHA256
snapshot_publication_commit_file_sha256  nullable SHA256
capture_ordered_relation_logical_sha256  nullable SHA256
capture_coverage_state                   nullable STRING
reservation_fence_sequence               nullable UINT64
reservation_fence_unit_file_sha256       nullable SHA256
reservation_event_row_sha256             nullable SHA256
cancellation_event_row_sha256            nullable SHA256
continuation_activation_event_row_sha256 nullable SHA256
continuation_validation_entries          nullable ARRAY[capture_fence_continuation_entry_v23]
continuation_validation_entries_logical_sha256 nullable SHA256
selected_continuation_validation_entry_sha256 nullable SHA256
payload_fence_sequence                   nullable UINT64
payload_fence_unit_file_sha256           nullable SHA256
release_outcome                          nullable STRING
```

`reservation_fence_unit_file_sha256` is directly persisted and is the complete-file hash of the earlier manifest that committed the matched reservation row. It is never inferred.

The total event/nullability matrix is:

| Unit branch | `previous_fence_unit_file_sha256` | Bound event/file/semantic triple | `payload_intent_semantic_sha256` | Snapshot semantic/physical fields | Reservation triple | Cancellation/activation/validation fields | `payload_fence_sequence` / `payload_fence_unit_file_sha256` | `release_outcome` |
|---|---|---|---|---|---|---|---|---|
| sequence-0 `FENCE_ACQUIRED` | null | all non-null; bound event equals intent payload kind; bundled intent validates | null | all null | all null | all null | both null | null |
| later `FENCE_ACQUIRED` | exact prior committed fence manifest hash | all non-null; bound event equals intent payload kind; bundled intent validates | null | all null | all null | all null | both null | null |
| each payload kind | exact acquisition manifest hash | all non-null and typed-equal to acquisition triple; `bound_payload_event_kind=event_kind` | non-null and equal to bound semantic digest | exact §17.4 branch; snapshot fields only for snapshot-bearing payloads | only cancellation: all non-null | exact event-specific groups | both null | null |
| `FENCE_RELEASED` / `ABORTED_NO_OUTPUT` | exact acquisition manifest hash | all null | null | all null | all null | all null | both null | `ABORTED_NO_OUTPUT` |
| `FENCE_RELEASED` / `COMMITTED` | exact payload manifest hash | all null | null | all null | all null | all null | both non-null and equal to that payload sequence and complete-file manifest hash | `COMMITTED` |

For every release branch, `acquire_fence_sequence`, `fence_epoch`, and `fence_token_sha256` remain non-null and typed-equal to the acquisition. Release row batches are empty and `row_batches_semantic_logical_sha256` is SHA-256 of empty bytes.

For the three snapshot-bearing payloads, `(snapshot_claim_semantic_sha256,capture_ordered_relation_logical_sha256)` is non-null and resolves to the exact promoted capture snapshot. The physical snapshot triple `(capture_snapshot_sequence,capture_snapshot_manifest_file_sha256,snapshot_publication_commit_file_sha256)` is also all non-null. Partial groups are invalid.

For cancellation, `(reservation_fence_sequence,reservation_fence_unit_file_sha256,reservation_event_row_sha256)` is all non-null and resolves exactly; for every other event it is all null.

The acquisition's intent file hash is SHA-256 of exact canonical intent bytes and its semantic hash recomputes from §17.4. A payload unit directly persists the acquisition's exact bound event/file/semantic triple and validates it against the reopened acquisition. A release persists no bound-intent triple.

An `ABORTED_NO_OUTPUT` release proves that no payload or canonical output occurred and therefore must not contain a payload reference. A `COMMITTED` release proves durable closure after one canonical payload and therefore must contain the exact payload sequence/hash. A release with the wrong predecessor, wrong payload-reference nullability, or a payload reference inconsistent with predecessor bytes is invalid.

The manifest's claim-semantic projection remains exactly §5.5.3. Physical row-batch and snapshot file hashes remain evidence fields but do not replace logical semantic bindings.

### 4.2 Replace base §17.6 in full with the following

### 17.6 Atomic fence-unit commit, acquisition contention, and bound-payload exclusivity

Every fence sequence is one atomic directory containing the exact manifest/event pair and §5.2 conditional objects. The directory rename is the sole commit point. Any pre-existing canonical target is resolved only through the §3.6 trichotomy.

For payload and release sequences, a semantically equivalent candidate may be adopted only under §5.7. A candidate that differs from the acquisition-bound intent cannot be adopted and is `CONFLICT` if it attempts to claim or publish that canonical payload/release target.

For `FENCE_ACQUIRED` only, multiple prepared contenders may legitimately bind different valid payload intents while racing from the same unique predecessor to the same next sequence. The first fully valid no-replace canonical directory is the acquisition winner. A different-intent losing prepared contender is nonblocking only as `UNSELECTED_CANONICAL_RACE_LOSER` under every §5.7 condition. It does not adopt the winner, does not publish an alternative intent, and grants no fence or payload permission.

Only the intent bound at acquisition `A` may occupy sequence `A+1`. A payload unit must prove:

1. `fence_sequence=A+1`;
2. event kind equals `bound_payload_event_kind`;
3. its recomputed payload intent digest equals the acquisition digest;
4. all actual logical row/snapshot/validation hashes and identities equal the intent;
5. predecessor is the exact acquisition manifest complete-file hash; and
6. no other payload or release occupies `A+1`.

Incompatible canonical units, a second canonical acquisition, different semantic bytes under one semantic identity, invalid target bytes, missing intent/source bytes, canonical output from a purported race loser, canonical reference to a loser, or a payload differing from the bound intent triggers `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, with `STOP_SEMANTIC_ID_COLLISION` taking precedence only for its exact condition.

Unsupported or failed fence-directory promotion maps to `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, not a V10 stop.

### 4.3 Replace base §17.7 in full with the following

### 17.7 Closed fence transitions

Let `A` be a committed acquisition. Permitted forms are exactly:

```text
A:   FENCE_ACQUIRED with one exact bound payload intent
A+1: FENCE_RELEASED with ABORTED_NO_OUTPUT
```

For this branch:

- the release predecessor is the acquisition manifest complete-file hash;
- `payload_fence_sequence` and `payload_fence_unit_file_sha256` are null;
- no payload or canonical output named by the intent exists; and
- no payload reference is asserted.

Or:

```text
A:   FENCE_ACQUIRED with one exact bound payload intent
A+1: exactly the bound payload event
A+2: FENCE_RELEASED with COMMITTED
```

For this branch:

- the payload predecessor is the acquisition manifest hash;
- the release predecessor is the payload manifest hash;
- `payload_fence_sequence=A+1`;
- `payload_fence_unit_file_sha256` equals the exact canonical payload manifest complete-file hash; and
- the release outcome is `COMMITTED`.

No nested acquisition, different payload, second payload, gap, token/epoch change, later proof-relevant commit, or new acquisition may intervene. An acquisition or payload without release is a durable open fence. No blanket rule requires an aborted release to reference a payload.

### 4.4 Replace base §17.8 text following its payload table with the following

For every snapshot-bearing payload:

1. only transient snapshot/partition/intent derivation may exist before acquisition;
2. acquisition commits the exact payload-intent bytes/hash naming snapshot sequence, claim-semantic hash, ordered capture relation hash, coverage state/boundary, and relevant authorization/reservation identity;
3. no committed capture `SNAPSHOT_PUBLICATION` prepared unit and no new canonical capture partition/history target exists before acquisition;
4. under the same open fence, reconstruct the authoritative prefix and validate exact equality with the bound claim;
5. under that fence, commit the exact bound capture snapshot prepared unit;
6. under that fence, promote/adopt only the partitions and history directory matching the bound claim;
7. commit at `A+1` only the payload matching the bound intent; and
8. commit the branch-correct release under §17.7.

A crash after canonical output promotion but before payload leaves a recoverable binding only if the same open acquisition, exact intent file, exact committed bound prepared unit, exact prepared sources, and exact promoted targets all validate. Recovery cannot substitute another snapshot, event kind, row hash, validation set, authorization identity, or prepared unit. A purported capture prepared unit committed before acquisition is invalid evidence, never a reusable candidate.

### 4.5 Replace base §17.10 in full with the following

### 17.10 Fence recovery classification

| Durable state | Classification | Exact handling |
|---|---|---|
| transient acquisition staging; no committed prepared unit | `TRANSIENT_ACQUISITION_CONTENDER` | discard or retry from current canonical head |
| unique canonical acquisition winner; transient loser | `TRANSIENT_CANONICAL_RACE_LOSER` | validate winner/predecessor; discard loser; no inventory entry |
| unique canonical acquisition winner; committed different-intent prepared loser meeting §5.7 | `UNSELECTED_CANONICAL_RACE_LOSER` | retain loser in terminal inventory; no stop and no canonical reference/output |
| acquisition and exact intent committed; no payload and no canonical output | `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT` | commit exactly bound payload, or commit `ABORTED_NO_OUTPUT` release with null payload refs and acquisition predecessor |
| acquisition committed; exact bound capture prepared unit absent | `BOUND_CAPTURE_PREPARATION_REQUIRED` | commit only the exact acquisition-bound capture prepared unit |
| exact payload prepared; canonical payload absent | `BOUND_PAYLOAD_PREPARED_RECOVERABLE` | verify intent equality, then commit/adopt exact payload |
| canonical payload committed; release absent | `RELEASE_PENDING_RECOVERABLE` | commit `COMMITTED` release with payload predecessor and non-null exact payload refs |
| STARTED payload committed; release absent | `STARTED_RELEASE_PENDING_NO_LAUNCH` | commit exact `COMMITTED` release before process creation |
| exact capture history/partitions promoted under current open acquisition; binding absent | `CAPTURE_BINDING_PENDING_RECOVERABLE` | validate exact bound prepared unit, commit exact payload, then `COMMITTED` release |
| semantically equal existing fence target under whitelist | `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` | adopt winner; derive `SUPERSEDED_BY_CANONICAL_WINNER` |
| byte-identical existing fence target | `BYTE_IDENTICAL_DUPLICATE_SUCCESS` | use existing target |
| missing/wrong intent bytes, alternate canonical payload, second canonical acquisition, canonical output/reference from race loser, incompatible predecessor, semantic conflict, wrong token/epoch, missing recovery bytes, or invalid release branch | `CONFLICT` | authorization/capture stop; preserve evidence |

An aborted release is prohibited after any canonical row-containing payload, capture prepared unit, partition, or history target named by the bound intent has been committed. `ABORTED_NO_OUTPUT` never references a payload. `COMMITTED` always references the exact canonical payload. Recovery never substitutes a different intent or prepared snapshot claim.

---

## 5. Affected recovery and finalization classification replacements

### 5.1 Replace base §21.2 in full with the following

### 21.2 Replay and clean-stop preconditions and commit protocol

Replay or clean-stop finalization requires:

- every snapshot and fence chain valid and cycle-free;
- every committed prepared candidate classified as selected canonical producer, `SUPERSEDED_BY_CANONICAL_WINNER`, or `UNSELECTED_CANONICAL_RACE_LOSER`;
- every race loser satisfying the exact winner, predecessor, no-output, no-reference, immutability, and inventory conditions in §5.7;
- no unresolved prepared claim, pre-acquisition committed capture snapshot unit, promoted unbound capture output, open fence, conflicting canonical target, or semantic collision;
- every superseded and unselected committed prepared unit fully retained and inventoried;
- current views and aggregate views equal committed sources; and
- complete normal final inventory closure.

A legitimate semantically superseded loser or acquisition race loser does not block finalization. An unvalidated loser, missing/invalid canonical winner, canonical loser output/reference, invalid pre-acquisition capture unit, or unresolved semantic claim does.

Normal V10 publication remains marker-last under the unchanged §5.5.4 claim semantics and §3.5 sidecar rules. `STOP_FINALIZATION_ATOMICITY_UNSUPPORTED` and `STOP_FINALIZATION_ATOMICITY_FAILURE` apply only to V10 terminal inventory/marker operations or the V10 conflict-directory operation.

### 5.2 Replace base §21.3 in full with the following

### 21.3 Conflict-stop trigger

Conflict-stop finalization is required only when the run must terminate while preserving an unresolved structural conflict, including:

- incompatible canonical snapshot/fence claims or a second canonical acquisition;
- different semantic bytes under one semantic identity;
- an unrecoverable open fence;
- a committed candidate that cannot be validated as selected, `SUPERSEDED_BY_CANONICAL_WINNER`, or `UNSELECTED_CANONICAL_RACE_LOSER`;
- canonical output or a canonical reference from a purported race loser;
- a committed pre-acquisition capture snapshot prepared unit;
- contradictory immutable cancellation/activation evidence;
- unrecoverable publication residue after the applicable family or authorization/capture stop; or
- V10 terminal publication conflict.

A valid no-replace winner plus a semantically equivalent loser is not a conflict. A valid canonical acquisition winner plus a different-intent prepared contender satisfying `UNSELECTED_CANONICAL_RACE_LOSER` is also not a conflict. A recoverable ordinary interruption remains recovery-required and is not conflict-finalized absent separate authority.

### 5.3 Replace the `classification` domain block in base §21.4.3 with the following

`classification` is closed to:

```text
CANONICAL_COMMITTED
DERIVED_VIEW_VALID
SELECTED_PREPARED_WINNER
SUPERSEDED_BY_CANONICAL_WINNER
UNSELECTED_CANONICAL_RACE_LOSER
RECOVERY_SOURCE_VALID
TERMINAL_EVIDENCE_VALID
CONTEXT_VALID
PROMOTED_PENDING_UNDER_OPEN_FENCE
FINALIZATION_RESIDUE
EXPECTED_MISSING
UNREADABLE
CORRUPT
CONTRADICTORY_OWNER_METADATA
UNREGISTERED_DURABLE_PATH
```

### 5.4 Replace the `PRESENT_VALID` role-class table and the prepared-disposition paragraph in base §21.4.4 with the following

For `PRESENT_VALID`, classification is determined by role class and, for `PREPARED_SUPERSEDED`, the independently derived prepared disposition:

| Role class | Exact classification |
|---|---|
| `CANONICAL_REQUIRED` | `CANONICAL_COMMITTED` |
| `DERIVED_REQUIRED` | `DERIVED_VIEW_VALID` |
| `PREPARED_SELECTED` | `SELECTED_PREPARED_WINNER` |
| `PREPARED_SUPERSEDED` with §5.7 semantic adoption | `SUPERSEDED_BY_CANONICAL_WINNER` |
| `PREPARED_SUPERSEDED` with §5.7 acquisition-race withdrawal | `UNSELECTED_CANONICAL_RACE_LOSER` |
| `RECOVERY_SOURCE` | `RECOVERY_SOURCE_VALID` |
| `TERMINAL_EVIDENCE` | `TERMINAL_EVIDENCE_VALID` |
| `CONTEXT_ONLY` | `CONTEXT_VALID` |
| `UNREGISTERED` | invalid combination → `CONTRADICTORY_OWNER_METADATA` |

`prepared_unit_id` and `claim_scope_sha256` remain non-null exactly for paths owned by or selected/superseded/unselected from one prepared plan. For `UNSELECTED_CANONICAL_RACE_LOSER`, the inventory validator must additionally resolve the unique canonical acquisition winner, identical race predecessor, absence of loser canonical output/reference, immutable loser bytes, and absence of conflict groups. A purported race-loser entry with any conflict-group membership is `CONTRADICTORY_OWNER_METADATA` unless a separately detected unrelated conflict affects the same physical path.

### 5.5 Replace the sentence at the end of base §21.4.6 that states a validated superseded loser normally has no group with the following

A validated `SUPERSEDED_BY_CANONICAL_WINNER` or `UNSELECTED_CANONICAL_RACE_LOSER` entry normally has no conflict group. A conflict group is required only when independent conflicting canonical or semantic evidence exists; losing an acquisition no-replace race is not itself a conflict kind.

---

## 6. Total `primary_stop_code` selection replacement

### 6.1 Replace the `primary_stop_code` derivation paragraph in base §21.4.1 with the following

`primary_stop_code` is derived and total over every member of the exact closed `REV23_STOP_CODE` enum above.

**Authoritative committed-stop-state branch.** First inspect the registered zero-or-one path:

```text
stop/stop_state.json
```

A committed stop state is authoritative only when all of the following validate:

1. exact `local_curl_stop_state.v23` closed schema;
2. exact run ID and spec revision;
3. complete-file bytes and registered hash/inventory binding;
4. `stop_code` is one exact `REV23_STOP_CODE` member permitted by that schema;
5. `stage` is one exact `stop_stage` value and is compatible with the effective stop-table row for that code;
6. evidence paths and hashes resolve to the still-applicable trigger; and
7. no second committed stop-state target or incompatible canonical stop-state claim exists.

When that valid committed stop state exists, `primary_stop_code` equals its `stop_code`, and the conflict inventory and marker bind that exact stop-state path and complete-file hash through their ordinary inventory entries. No later local ranking replaces it.

**Derived branch when no valid committed stop state exists.** Construct the set of every still-applicable unresolved stop candidate. Each candidate is exactly `(stop_code,actual_detection_stage,evidence_identity)` where:

- `stop_code` is one enum member;
- `actual_detection_stage` is the concrete producer/detection stage established by persisted evidence, not `ANY` and not a caller default;
- the stage is compatible with every stage listed for that code in the effective `STOP_STATE_TABLE_REV23.md`; for an `ANY` row, any concrete stage in the global order below is compatible; and
- duplicate discoveries of the same code/stage/evidence identity collapse.

Global stage precedence is exactly:

```text
V0 < V1 < V2 < V3 < V4 < V5A < V5B < V5C < V6 < V6A
   < V7 < V8C < V8S < V8D < V9 < V10
```

Select the candidate at the earliest stage. Within that stage, precedence is the exact ordinal of `stop_code` in the complete 71-member `REV23_STOP_CODE` enum printed in this subsection: lower enum ordinal wins. This is the explicit complete within-stage precedence for every code, including codes unrelated to Finding 4. If duplicate candidates have the same stage and code, they yield the same `primary_stop_code`; evidence order does not affect selection.

A multi-stage stop uses the actual persisted detection stage, not the earliest stage named in its allowed-stage set. If an actual stage cannot be proven, the evidence is structurally invalid and contributes the applicable schema/finalization stop rather than an invented stage. A valid `SUPERSEDED_BY_CANONICAL_WINNER` or `UNSELECTED_CANONICAL_RACE_LOSER` contributes no stop.

`STOP_FINALIZATION_ATOMICITY_UNSUPPORTED` and `STOP_FINALIZATION_ATOMICITY_FAILURE` remain members of the total derived ordering at `V10`, but a failed V10 conflict-directory commit cannot retroactively create a successfully committed inventory/marker. Its computed primary code applies only to preserved unfinalized V10 residue.

### 6.2 Replace base §22.2 in full with the following

### 22.2 Global primary-stop selection and Finding 4 validator precedence

Global `primary_stop_code` selection is exclusively the two-branch algorithm in §21.4.1:

1. valid committed `stop/stop_state.json`, when present; otherwise
2. earliest concrete global stage, then exact `REV23_STOP_CODE` enum ordinal within that stage.

The global algorithm is total over all 71 stop codes and ranks unrelated V0–V10 stops. The Finding 4 local validator order below does not select `primary_stop_code` across stages or unrelated validators. It only determines which Finding 4 defect a single amended validator emits first when the same validation operation simultaneously observes multiple local defects:

1. `STOP_ROW_HASH_PROJECTION_INVALID`;
2. `STOP_LOGICAL_HASH_MISMATCH`;
3. `STOP_SEMANTIC_ID_COLLISION` only for one semantic identity mapping to different semantic bytes;
4. applicable family snapshot stop;
5. `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`;
6. `STOP_RESERVATION_NO_START_PROOF_INVALID`; and
7. V10 inventory/finalization atomicity stop only while attempting the corresponding terminal publication.

After local detection, the emitted candidate enters the global algorithm with its concrete detection stage. A validated `SUPERSEDED_BY_CANONICAL_WINNER` or `UNSELECTED_CANONICAL_RACE_LOSER` produces no stop. Missing evidence never becomes a zero-count proof.

---

## 7. Producer, resume, and finalization cross-clause replacements

### 7.1 Replace the first three rows of the producer-consumer matrix in base §23.1 with the following rows

| Artifact | Sole producer class | Required consumers |
|---|---|---|
| prepared evidence unit | snapshot publisher, fence coordinator, or V10 normal finalizer by unit kind; capture snapshot unit only under its open acquisition | publication/adoption validator, recovery, inventories, Sentinel |
| semantically superseded prepared candidate | original producer; classification derived by validator | winner-adoption validator, normal/conflict inventory, Sentinel |
| unselected acquisition race-loser prepared candidate | original acquisition contender; classification derived only after unique canonical winner validation | race/predecessor/no-output/no-reference validator, normal/conflict inventory, Sentinel |

All remaining rows in base §23.1 remain byte-for-byte unchanged.

### 7.2 Replace base §23.3 in full with the following

### 23.3 Resume order

Resume must:

1. validate mutually exclusive terminal profiles;
2. validate every committed prepared plan, descriptor, source byte, target scope, and §5.2 role/cardinality rule;
3. identify canonical no-replace winners and rederive every `SUPERSEDED_BY_CANONICAL_WINNER` and `UNSELECTED_CANONICAL_RACE_LOSER` classification before treating candidates as nonblocking;
4. for each acquisition race loser, prove the unique canonical winner, identical race predecessor, no loser canonical output/reference, and immutable retention;
5. reject any committed pre-acquisition capture `SNAPSHOT_PUBLICATION` unit as a protocol violation; transient pre-acquisition capture staging may be discarded;
6. validate snapshot and fence graphs including cycles before selecting heads;
7. identify at most one durable open fence;
8. for capture, commit the exact bound snapshot prepared unit and promote partitions/history only under that open acquisition;
9. classify snapshot publication under §7.5 and fence recovery under §17.10;
10. complete only exact prepared/adopted winner bytes or emit the applicable family or authorization/capture stop;
11. for release recovery, enforce the `ABORTED_NO_OUTPUT` null-payload branch or the `COMMITTED` non-null-payload branch exactly;
12. repair current generations, mirrors, and aggregate views only from committed canonical sources;
13. validate V10 pending normal inventory/marker state only after all non-V10 recovery is closed; and
14. revalidate cancellation and CONTINUATION freshness before any reservation.

No resume path may convert a different-intent acquisition race loser into the canonical winner's semantic claim, reuse a pre-acquisition committed capture prepared unit, or treat physical inequality alone as conflict.

---

## 8. Affected test replacements

### 8.1 Replace base §24.3 in full with the following

### 24.3 Claim-scope, claim-semantic, canonical-winner, and race-loser tests

Positive tests must:

- recompute exact claim-scope bytes/hash for snapshot, fence, and normal finalization;
- prove equal logical Parquet variants reach `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED` and derive `SUPERSEDED_BY_CANONICAL_WINNER` only through the whitelist;
- prove byte-identical existing targets reach `BYTE_IDENTICAL_DUPLICATE_SUCCESS`;
- prove every non-equivalent existing target reaches `CONFLICT`;
- construct two valid prepared `FENCE_ACQUIRED` contenders with different intents, identical sequence/target/predecessor, and one unique canonical winner; prove the committed loser is `UNSELECTED_CANONICAL_RACE_LOSER`, has no canonical output/reference, is retained in terminal inventory, has no conflict group, and does not block normal finalization; and
- prove a transient losing contender may be discarded only after winner/predecessor validation.

Reject a fourth existing-target result, physical inequality treated as collision, non-whitelisted semantic adoption, stale dependent hash, ambiguous winner, different predecessor, second canonical acquisition, canonical output/reference from a race loser, missing loser prepared bytes, race loser omitted from inventory, race loser placed in a conflict group without an independent conflict, or same semantic identity digest mapped to different bytes.

### 8.2 Replace base §24.4 in full with the following

### 24.4 Parquet physical/semantic distinction and target-trichotomy tests

Positive: different valid Parquet bytes with equal schema, exact ordered typed rows, counts, bounds, and logical hash reach `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED`; the first target remains canonical and the candidate becomes `SUPERSEDED_BY_CANONICAL_WINNER`.

Reject physical inequality alone as `CONFLICT`, equal row count with different rows/order/hash, winner rewrite, or semantic adoption outside the exact role whitelist.

### 8.3 Replace base §24.6 in full with the following

### 24.6 Acquisition-bound capture preparation and promotion tests

Positive order is exact:

1. derive transient snapshot claim and payload-intent bytes;
2. commit acquisition with immutable intent file/hash;
3. reconstruct and validate the exact capture prefix under that acquisition;
4. commit the exact capture `SNAPSHOT_PUBLICATION` prepared unit under that acquisition;
5. promote/adopt exact partitions and history under the same acquisition;
6. commit at `A+1` only the bound payload; and
7. commit the branch-correct release.

Crash tests cover each boundary. Before acquisition, only transient staging may exist and may be discarded. After acquisition, recovery uses only the exact bound prepared unit. Reject a committed pre-acquisition capture prepared unit, pre-acquisition partition/history promotion, alternate prepared unit after acquisition, generic acquisition, absent/wrong intent bytes, alternate `A+1` event, promotion after release, prefix validation outside acquisition, different snapshot/row hash, or aborted release after any canonical output.

### 8.4 Replace base §24.9 in full with the following

### 24.9 First fence acquisition and release-nullability tests

Positive sequence-0 acquisition has null predecessor and null coverage. Test both legal closure branches:

- sequence 1 `ABORTED_NO_OUTPUT` release with predecessor equal to acquisition hash and null payload sequence/hash; and
- sequence 1 payload followed by sequence 2 `COMMITTED` release with predecessor equal to payload hash and non-null exact payload sequence/hash.

Reject `-1`, `UINT64_MAX`, zero, or string as origin coverage; aborted release with payload refs; committed release with null payload refs; aborted release whose predecessor is a payload; committed release whose predecessor is the acquisition; and any blanket assertion that all releases reference a payload.

### 8.5 Replace base §24.10 in full with the following

### 24.10 Fence schema, intent, reservation hash, contention, and release tests

Assert exact event/manifest field order, acquisition-bound intent file and semantic hash, total event nullability, and `reservation_fence_unit_file_sha256` cancellation-only behavior.

Positive contention tests include:

- equal-intent candidate reaching byte-identical duplicate or semantic winner adoption as applicable;
- different-intent prepared acquisition contender reaching `UNSELECTED_CANONICAL_RACE_LOSER` only with unique winner, identical predecessor, no canonical loser output/reference, immutable retention, and terminal inventory inclusion; and
- payload/release candidates remaining bound exclusively to the canonical acquisition intent.

Positive release tests assert `ABORTED_NO_OUTPUT` has acquisition predecessor and null payload refs, while `COMMITTED` has payload predecessor and non-null exact payload refs.

Reject incompatible canonical units, second canonical acquisition, semantic-ID conflict, cycle, nested acquisition, two payloads, wrong token/epoch, loser output/reference, missing loser inventory, release mismatch, or fence atomicity mapped to V10.

### 8.6 Replace the positive list and rejection sentence in base §24.14 with the following

Positive conflict-inventory tests must additionally:

- classify valid semantic losers as `SUPERSEDED_BY_CANONICAL_WINNER`;
- classify valid different-intent acquisition losers as `UNSELECTED_CANONICAL_RACE_LOSER`;
- bind both to `PREPARED_SUPERSEDED` owner role while preserving the distinct classification;
- require no conflict group for either absent an independent conflict;
- preserve every committed loser path exactly once; and
- derive `primary_stop_code` from a valid committed stop state when present, otherwise from concrete global stage and complete enum ordinal.

Reject a race loser classified as conflict solely for intent inequality, a race loser with canonical output/reference, a missing race-loser inventory path, an invented actual detection stage, a local Finding 4 rank used against unrelated stage stops, an invalid/multiple stop state treated as authoritative, or a primary code not selected by the exact §21.4.1 algorithm.

All other base §24.14 test requirements remain byte-for-byte unchanged.

### 8.7 Replace base §24.15 in full with the following

### 24.15 Typed-stop and finalization tests

Assert snapshot atomicity failures map to family snapshot stops, fence/intent/payload publication failures map to `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, and V10 atomicity stops occur only for terminal publication.

Primary-stop tests cover all enum members by constructing valid candidate tuples for every permitted concrete stage. Prove:

1. valid committed `stop/stop_state.json` is authoritative;
2. absent valid stop state, earlier global stage wins;
3. same-stage ties use exact full enum ordinal;
4. multi-stage/`ANY` codes use the persisted actual detection stage;
5. invalid, duplicate, or evidence-incompatible stop states do not bind; and
6. Finding 4 local validator precedence never ranks unrelated V0–V10 candidates.

Positive normal finalization includes selected, semantically superseded, and unselected-race-loser prepared units, with no open fence and no invalid pre-acquisition capture prepared unit. Reject both terminal profiles, undefined primary stop, superseded/race loser treated as fork without independent conflict, V10 stop at V7/V8, invalid release nullability, or replay result from conflict stop.

---

## 9. Affected traceability rows

Replace the `no-replace winner adoption` row in base §29 with:

| ordinary target resolution and semantic adoption | §§3.6–3.7, 5.7, 7.2 | exact three-value target result; role whitelist | byte duplicate, semantic adoption, or conflict only | §§24.3–24.4 |

Insert immediately after it:

| different-intent acquisition race loser | §§5.7–5.8, 7.5, 17.6, 17.10 | `UNSELECTED_CANONICAL_RACE_LOSER` with unique winner, identical predecessor, no output/reference, immutable retention | no stop only when every conjunct holds | §§24.3, 24.10, 24.14–24.15 |

Replace the `acquisition-bound capture promotion` row with:

| acquisition-bound capture preparation and promotion | §§7.1–7.3, 17.4–17.8 | transient-only before acquisition; exact prepared unit and all canonical promotion under open fence | capture/auth-capture stop on violation | §24.6 |

Insert immediately after the `reservation fence-unit hash` row:

| split release nullability and predecessor | §§17.5, 17.7, 17.10 | aborted: null payload refs/acquisition predecessor; committed: non-null payload refs/payload predecessor | auth/capture stop | §§24.9–24.10 |

Replace the `stop-family consistency` row with:

| total primary-stop selection and stop-family consistency | §§21.4.1, 22.1–22.2 | valid committed stop state else global stage plus complete enum ordinal | exact `REV23_STOP_CODE`; stage-specific stops preserved | §§24.14–24.15 |

All other base §29 rows remain byte-for-byte unchanged.

---

## 10. Cross-reference updates

Apply these exact cross-reference substitutions wherever the affected base clauses refer to the superseded rule:

1. Replace any statement that an existing target is accepted only when recursively byte-identical with: “resolve through the exact §3.6 or §3.7 three-value target result.”
2. Replace any standalone recovery classification `CANONICAL_PHYSICAL_OBJECT_ADOPTED` with `SEMANTICALLY_EQUIVALENT_CANONICAL_WINNER_ADOPTED`.
3. Replace any statement that different acquisition intents at one prepared no-replace race are automatically a conflict with the §5.7/§17.6 distinction between an unselected prepared contender and incompatible canonical commits.
4. Replace any statement that capture snapshot prepared units or new capture partitions may be durably committed before acquisition with §§5.8 and 7.1 transient-only preparation.
5. Replace any blanket statement that every `FENCE_RELEASED` event references a payload with the two §17.5/§17.7 release branches.
6. Replace every `primary_stop_code` reference to “§22.2 local precedence” with “§21.4.1 global primary-stop selection”; retain §22.2 only for its explicit distinction between global selection and local validator emission.
7. In §§23.4, 25, 26, 27, 28, 30, and 34, interpret “selected/superseded prepared units” as “selected, `SUPERSEDED_BY_CANONICAL_WINNER`, or `UNSELECTED_CANONICAL_RACE_LOSER` prepared units” only where terminal inventory closure is discussed. This substitution does not authorize a race loser to satisfy a canonical semantic claim.
8. In §26 schema-registry amendments, add the `UNSELECTED_CANONICAL_RACE_LOSER` disposition/classification and split `FENCE_RELEASED` nullability branches; remove `CANONICAL_PHYSICAL_OBJECT_ADOPTED` as an independent target-result enum.

---

## 11. Unchanged-base statement and authorization boundary

Every base-draft byte not expressly replaced or cross-referenced by this packet remains byte-for-byte unchanged from base SHA-256:

```text
3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563
```

This packet is a specification correction for Sentinel review only. It authorizes nothing. It does not authorize Claude communication, materialization, source synchronization, implementation, test authoring, testing, repository edits, local project-data reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
