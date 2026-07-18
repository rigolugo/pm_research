# REV23 Snapshot, Partition, and Cancellation-Proof Amendment — Complete Replacement Draft

**Filename:** `REV23_SNAPSHOT_PARTITION_CANCELLATION_AMENDMENT_DRAFT.md`  
**Status:** `DRAFT_FOR_SENTINEL_REVIEW`  
**Role:** Professor specification draft  
**Scope:** Revision 23 Finding 4 only: audit-snapshot history, detached partitions, durable row persistence, capture-fence serialization, reservation-cancellation proof, CONTINUATION freshness, recovery, and finalization  
**Accepted-contract commit:** `fad41de515572ca30b4440b060a69dd6bfc57e2b`  
**Current canonical project-state commit inspected:** `f6cb60df66c2bbcdfb6d797119ed25ad79e06a11`  
**Existing Amendment 03 I0 authorization-anchor commit:** `d737aa9e12cbfa584b275e128c8624e01af72f61`  
**Effect if accepted and materialized:** supersedes only incomplete Revision 23 snapshot/partition/cancellation-proof rules and explicitly deactivates the existing Amendment 03 I0 implementation-authorization package. No implementation authorization carries forward.

---

## 1. Objective and governing safety property

This amendment closes Revision 23 Finding 4 by defining one total, deterministic, self-contained contract for:

1. audit-snapshot sequence origin, monotonicity, uniqueness, predecessor chains, forks, cycles, latest/final derivation, and historical/current reconciliation;
2. detached partition ordinals, canonical keys, ranges, logical hashes, immutable reuse, and complete historical inventories;
3. concurrency-safe publication through durable prepared-object units and atomic directory promotion;
4. physical persistence of authorization-use and capture rows as immutable, hash-bound row batches;
5. a durable capture-fence history that orders reservation, STARTED, terminal, checkpoint, cancellation, and CONTINUATION evidence;
6. exact no-start proof, derived unproven handling, contradiction handling, and CONTINUATION freshness;
7. distinct replay/clean-stop finalization and conflict-stop finalization; and
8. complete recovery, resume, immutability, stop, traceability, and test requirements.

The governing safety property is:

> A request cannot become CONTINUATION-eligible from a claimed no-start cancellation unless a uniquely resolved, structurally valid, immutable capture snapshot reconstructs the complete committed capture-row relation through a durable fence checkpoint; independently derives zero matching STARTED rows and zero matching terminal rows; is bound to the cancellation authorization-use row by one committed fence payload unit under an exclusive durable fence; and remains contradiction-free through a separately fenced CONTINUATION activation and every later continuation reservation validation.

No missing, stale, partial, contradictory, forked, unreadable, cyclic, pending, caller-asserted, or non-durable evidence is negative evidence or continuation-unblocking evidence.

---

## 2. Authority, precedence, non-objectives, and baseline identity

### 2.1 Narrow precedence

If this amendment conflicts with an earlier Revision 23 sentence on snapshot history, snapshot publication, detached partitions, physical authorization/capture row persistence, cancellation interval proof, capture-fence ordering, CONTINUATION freshness, recovery, or finalization of those artifacts, this amendment governs that narrow subject.

All unrelated accepted Revision 23 behavior remains unchanged.

### 2.2 Explicit non-objectives

This amendment does **not** change:

- token-manifest relocation or provenance;
- the accepted `600 / 496 / 496` token-manifest, request-manifest, and request-plan populations;
- pre-run identity or the twelve-field `run_id` identity;
- request identity, request ordering, URL serialization, transport, or effective argv;
- typed-cell tags or the exact null cell `{"n":"<field>","t":"NULL","v":null}`;
- the seven-field `partition_id` projection or its three-value partition-family domain;
- the sole HTTP reconciliation schema version, raw Base64 stdout evidence, retained header-parser binding, twelve HTTP reconciliation combinations, or completed-capture HTTP lifecycle;
- compatibility/strict analysis, selected-attempt ordering, fixed denominators, thresholds, result labels, or result ordering;
- P1/P2/P3/probe gates or `named_binary_probe_blocked = true`.

No Revision 22 text, hidden fallback, old chat, or superseded local copy supplies a missing rule in this amendment.

### 2.3 Exact accepted-contract baseline

A later materialization may proceed only from accepted-contract bytes whose hashes equal:

```text
GOVERNING_PACKAGE_MANIFEST_REV23.json
  b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa

governing_package_manifest_semantic_sha256
  6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b

SPEC_local_curl_per_side_price_dataset_verification_REV23.md
  d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9

SCHEMA_REGISTRY_REV23.json
  e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19
```

Any mismatch is a material baseline change and requires renewed Sentinel review. This draft does not authorize materialization.

---

## 3. Closed vocabulary and governing persistence primitives

### 3.1 Snapshot families

The partition/snapshot family domain remains exactly:

```text
capture
analysis_compatibility
analysis_strict
```

The broader global audit-family enum remains unchanged and is not accepted in partition identities.

### 3.2 Existing schemas retained and amended

The following existing Revision 23 schemas remain governing and receive the invariants defined here:

- `json:audit_snapshot_manifest` — `local_curl_audit_snapshot_manifest.v23`;
- `json:snapshot_partition_entry` — embedded closed object;
- `table:snapshot_partition` — `local_curl_snapshot_partition.v23`;
- `table:capture_events` — `local_curl_capture_event.v23`;
- `table:authorization_use_events` — `local_curl_authorization_use_event.v23`;
- `json:authorized_request_set_v23` and `json:network_authorization_record_v23` — membership and identity remain unchanged.

The existing `reservation_start_proof_state` enum remains byte-for-byte unchanged. This amendment changes only state-specific reachability and validation behavior; it does not add or remove an enum lexeme.

### 3.3 New narrow support schemas

Acceptance requires these support schemas:

1. `json:prepared_evidence_object_v23`;
2. `json:prepared_claim_scope_v23`;
3. `json:snapshot_publication_claim_semantic_v23`;
4. `json:capture_payload_intent_v23`;
5. `json:fence_unit_claim_semantic_v23`;
6. `json:normal_finalization_claim_semantic_v23`;
7. `json:prepared_evidence_plan_v23`;
8. `json:prepared_evidence_unit_v23`;
9. `json:snapshot_publication_commit_v23`;
10. `json:snapshot_current_view_commit_v23`;
11. `json:fence_unit_manifest_v23`;
12. `json:fence_event_v23`;
13. `json:immutable_row_batch_v23`;
14. `json:capture_fence_continuation_entry_v23`;
15. `json:conflict_inventory_entry_v23`;
16. `json:conflict_group_v23`;
17. `json:conflict_stop_inventory_v23`;
18. `json:conflict_stop_marker_v23`.

They are evidence, claim, publication, recovery, and lifecycle schemas only. They do not change request counts, empirical outputs, authorization modes, denominators, thresholds, or result labels.

### 3.4 Canonical JSON

Every new JSON artifact uses the accepted Revision 23 canonical JSON contract:

- UTF-8, no BOM;
- closed objects with every nullable field present;
- lexicographic Unicode code-point object-key order;
- compact separators;
- JSON integers, never numeric strings or floats, for integer fields;
- NFC strings where the scalar type is `STRING`;
- no leading/trailing whitespace and no final LF.

An "exact field order" list defines closed schema membership and, where a logical-hash projection says to use the displayed order, the ordered typed-cell projection. It does not override canonical JSON object serialization: stored JSON object keys remain lexicographic Unicode code-point order. Arrays retain their separately registered order.

### 3.5 Sidecar rule: no sidecar-first commit

The accepted sidecar object remains exactly:

```json
{"target_file_sha256":"<64-lowercase-hex>","target_path":"<exact registered relative path>"}
```

A sidecar is never a commit point. This amendment permits only three sidecar publication modes:

1. **Atomic-bundle member.** The target and its sidecar are members of the same fully prepared directory, and the entire directory is committed by one same-filesystem atomic no-replace directory rename. Neither member is visible as committed before the directory commit point.
2. **Deterministic authoritative-file sidecar.** One immutable standalone target is committed first by `ATOMIC_SINGLE_FILE_PROMOTION` under §3.7. The target alone is authoritative. A registered sidecar is then derived from the reopened target bytes and promoted by atomic no-replace file rename. Process loss after target commit but before sidecar commit leaves an authoritative target with one deterministically recoverable derivative sidecar; it does not roll back or duplicate the target commit.
3. **Deterministic derived-view sidecar.** This mode is permitted only for the replaceable legacy current mirrors, which are never a commit point or historical authority. A producer atomically replaces the target from one exact committed current-view generation, reopens the target, computes its SHA-256, constructs the sole valid sidecar, and atomically replaces the sidecar only while the same generation remains the unique head. Consumers never accept the two paths by directory co-presence: they must apply the stable mirror-read protocol in §7.4. A crash or concurrent head advance may leave a physically stale mirror component, but no target/sidecar pair is accepted unless both resolve to one generation and one stable target hash.

For modes 2 and 3, a producer must recheck the target immediately before sidecar promotion and again after promotion. An existing byte-identical sidecar is duplicate retry success. A differing immutable sidecar is a collision and is never overwritten; a differing replaceable mirror sidecar is replaced only from the currently validated generation and is not accepted until the stable mirror-read protocol passes. Sidecar-first publication, two independent file renames claimed as an atomic commit, and any validation protocol that can accept one producer's target with another producer's sidecar are prohibited.

### 3.6 Atomic directory promotion

`ATOMIC_DIRECTORY_PROMOTION` means all of the following:

1. source and target parent are on the same filesystem;
2. the complete source directory is created under a hidden sibling staging name;
3. every member file is closed and durably flushed;
4. the source directory and its parent are durably flushed;
5. the source directory is renamed to the exact final directory by one atomic no-replace operation;
6. the final parent directory is durably flushed;
7. if the final directory already exists, no member is overwritten or merged;
8. an existing final directory is accepted as duplicate success only if its complete recursive path set, file sizes, and file SHA-256 values equal the prepared unit exactly.

Unsupported no-replace directory promotion is not silently weakened to per-file writes.

### 3.7 Atomic single-authoritative-file promotion

`ATOMIC_SINGLE_FILE_PROMOTION` means all of the following:

1. create the complete target bytes under a hidden sibling file on the same filesystem;
2. close and durably flush the file;
3. durably flush the parent directory;
4. atomically no-replace rename the file to the exact final path;
5. durably flush the parent directory;
6. reopen and verify exact size and SHA-256;
7. accept an existing byte-identical target as duplicate success and classify any differing target as a collision.

The target-file rename is the sole commit point. A sidecar, later marker, or consumer cannot make uncommitted target bytes authoritative. Unsupported no-replace promotion is never weakened to overwrite, merge, or check-then-write.

---

## 4. Exact artifact topology

### 4.1 Roots

```text
<run_root> = artifacts/local_curl_per_side/runs/<run_id>

capture family:
<run_root>/capture

analysis_compatibility family:
<run_root>/analysis/compatibility

analysis_strict family:
<run_root>/strict
```

Let `<family_root>` mean the applicable family path and `<capture_root>` mean `<run_root>/capture`.

### 4.2 Sequence component

For unsigned `s` in `0..UINT64_MAX`:

```text
sequence_component(s) = unsigned base-10 s, left-padded with ASCII "0" to 20 digits
```

No sign, whitespace, exponent, separator, non-ASCII digit, or non-20-digit path component is permitted.

### 4.3 Durable prepared units

```text
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SCOPE.json
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SCOPE.sha256
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SEMANTIC.json
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SEMANTIC.sha256
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARATION_PLAN.json
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARATION_PLAN.sha256
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARED_UNIT.json
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARED_UNIT.sha256
<run_root>/prepared_evidence/<unit_kind>/<prepared_unit_id>/objects/<object_ordinal_10d>.bin
```

`CLAIM_SCOPE.json` and `CLAIM_SEMANTIC.json` are canonical JSON structural members, each paired with its bundled sidecar. Their complete bytes are the independently recoverable source of the claim hashes persisted in the plan and descriptor. A committed prepared-unit directory is immutable and retained through the applicable terminal inventory. It is not temporary staging.

Transient pre-commit staging exists only under:

```text
<run_root>/.preparing/<producer_nonce>/
```

A transient directory that never became a prepared-unit directory is not evidence and may be discarded. A committed prepared-unit path is derived from exact plan bytes and may never be caller-selected.

### 4.4 Snapshot history and current views

For snapshot sequence `s`:

```text
<family_root>/audit_snapshot_history/<20d>/audit_snapshot_manifest.json
<family_root>/audit_snapshot_history/<20d>/audit_snapshot_manifest.sha256
<family_root>/audit_snapshot_history/<20d>/snapshot_partitions.parquet
<family_root>/audit_snapshot_history/<20d>/PUBLICATION_COMMITTED.json
<family_root>/audit_snapshot_history/<20d>/PUBLICATION_COMMITTED.sha256
```

The whole `<20d>/` directory is one atomic immutable history bundle.

Current-view generation:

```text
<family_root>/current_view_generations/<20d>/audit_snapshot_manifest.json
<family_root>/current_view_generations/<20d>/audit_snapshot_manifest.sha256
<family_root>/current_view_generations/<20d>/snapshot_partitions.parquet
<family_root>/current_view_generations/<20d>/CURRENT_VIEW_COMMITTED.json
<family_root>/current_view_generations/<20d>/CURRENT_VIEW_COMMITTED.sha256
```

The generation directory is atomically promoted. Existing Revision 23 current paths remain required mirrors:

```text
<family_root>/audit_snapshot_manifest.json
<family_root>/audit_snapshot_manifest.sha256
<family_root>/snapshot_partitions.parquet
```

The mirrors are replaceable, non-authoritative views. Only the unique committed head's generation and mirrors may reconcile as current.

### 4.5 Immutable partitions

```text
<family_root>/partitions/<partition_id>.parquet
```

Partition files are immutable single-authoritative-file objects. They have no independent commit sidecar. Their complete-file hash and size are bound by the prepared unit, history manifest entry, and snapshot index row.

### 4.6 Fence history and row batches

For capture-fence sequence `q`:

```text
<capture_root>/commit_fence_history/<20d>/FENCE_UNIT.json
<capture_root>/commit_fence_history/<20d>/FENCE_UNIT.sha256
<capture_root>/commit_fence_history/<20d>/fence_event.json
<capture_root>/commit_fence_history/<20d>/fence_event.sha256
<capture_root>/commit_fence_history/<20d>/bound_payload_intent.json                   [FENCE_ACQUIRED only]
<capture_root>/commit_fence_history/<20d>/bound_payload_intent.sha256                 [FENCE_ACQUIRED only]
<capture_root>/commit_fence_history/<20d>/rows/authorization_use_events.parquet        [conditional]
<capture_root>/commit_fence_history/<20d>/rows/authorization_use_events.sha256        [conditional]
<capture_root>/commit_fence_history/<20d>/rows/capture_events.parquet                  [conditional]
<capture_root>/commit_fence_history/<20d>/rows/capture_events.sha256                  [conditional]
```

The entire `<20d>/` directory is one atomic immutable fence unit. Row-batch files and their sidecars are committed with the fence event, never before or after it. Every `FENCE_ACQUIRED` unit also commits exactly one immutable `bound_payload_intent.json` and its bundled sidecar. No other fence-unit kind contains that object.

### 4.7 Aggregate relation views

Existing paths remain:

```text
<run_root>/authorization/authorization_use_events.parquet
<capture_root>/capture_events.parquet
```

They are replaceable aggregate views derived exclusively from committed fence-unit row batches. They are not primary evidence and cannot make a pending row committed.

### 4.8 Conflict-stop terminal bundle

```text
<run_root>/CONFLICT_STOP_FINALIZED/CONFLICT_STOP.json
<run_root>/CONFLICT_STOP_FINALIZED/CONFLICT_STOP.sha256
<run_root>/CONFLICT_STOP_FINALIZED/CONFLICT_INVENTORY.json
<run_root>/CONFLICT_STOP_FINALIZED/CONFLICT_INVENTORY.sha256
```

The whole `CONFLICT_STOP_FINALIZED/` directory is atomically promoted and is mutually exclusive with either normal finalized marker.

### 4.9 Normal terminal artifacts

The accepted Revision 23 normal paths remain exact:

```text
<run_root>/finalization/final_artifact_inventory.json      [replay only]
<run_root>/finalization/stop_artifact_inventory.json       [clean stop only]
<run_root>/finalization/REPLAY_FINALIZED.json               [replay only]
<run_root>/finalization/STOP_FINALIZED.json                 [clean stop only]
```

Any sidecar required by the effective registry is at its registered sibling path and is derivative under §3.5 mode 2. The phrase `FINALIZED.marker` in accepted Revision 23 text means exactly the existence of one valid `REPLAY_FINALIZED.json` or one valid `STOP_FINALIZED.json`; it does not name an additional file.

The inventory and marker are independent immutable standalone files. Before either target commits, their exact bytes and any registered derivative sidecars are committed in one `NORMAL_FINALIZATION` prepared unit under §5. The accepted marker schema is narrowly amended to include `normal_finalization_prepared_unit_id`; it is required for `REPLAY_FINALIZED` and `STOP_FINALIZED` and null for every other marker kind. The inventory target commits first under §3.7 and does not finalize the run. The applicable marker target commits last under §3.7 and is the sole normal terminal commit point.

The amended `local_curl_finalization_marker.v23` field order is exactly:

```text
schema_version
spec_revision
marker_kind
pre_run_attempt_id
run_id
stop_code
result_label
inventory_file_sha256
normal_finalization_prepared_unit_id
created_at_ns
```

`normal_finalization_prepared_unit_id` is nullable `STRING /^prep_[0-9a-f]{64}$/`. It is non-null for `REPLAY_FINALIZED` and `STOP_FINALIZED`; it is null for pre-run markers and finalization-failure markers. It is included in the marker semantic projection immediately before `created_at_ns`. The exact inventory path is not a new marker field: it is the one registered path determined by `marker_kind` and `run_id`; `inventory_file_sha256` must equal those exact bytes.

---

## 5. Durable prepared-object, claim, and canonical-winner contract

### 5.1 `prepared_evidence_object_v23`

`object_role` is closed to:

```text
PARTITION_PAYLOAD
HISTORY_MANIFEST
HISTORY_MANIFEST_SIDECAR
HISTORY_INDEX
PUBLICATION_MARKER
PUBLICATION_MARKER_SIDECAR
CURRENT_GENERATION_MANIFEST
CURRENT_GENERATION_MANIFEST_SIDECAR
CURRENT_GENERATION_INDEX
CURRENT_GENERATION_MARKER
CURRENT_GENERATION_MARKER_SIDECAR
LEGACY_CURRENT_MANIFEST
LEGACY_CURRENT_MANIFEST_SIDECAR
LEGACY_CURRENT_INDEX
BOUND_PAYLOAD_INTENT
BOUND_PAYLOAD_INTENT_SIDECAR
FENCE_UNIT_MANIFEST
FENCE_UNIT_MANIFEST_SIDECAR
FENCE_EVENT
FENCE_EVENT_SIDECAR
AUTHORIZATION_USE_ROW_BATCH
AUTHORIZATION_USE_ROW_BATCH_SIDECAR
CAPTURE_ROW_BATCH
CAPTURE_ROW_BATCH_SIDECAR
NORMAL_FINAL_INVENTORY
NORMAL_FINAL_INVENTORY_SIDECAR
NORMAL_FINAL_MARKER
NORMAL_FINAL_MARKER_SIDECAR
```

Exact field order:

```text
object_ordinal                  UINT32
object_role                     STRING
content_schema_id               STRING
publication_mode                STRING {ATOMIC_BUNDLE_MEMBER, SINGLE_AUTHORITATIVE_FILE, REUSE_IMMUTABLE_SOURCE, DERIVED_VIEW_TARGET}
durable_source_path             STRING
canonical_target_path           STRING
file_size_bytes                 UINT64
file_sha256                     SHA256
logical_sha256                  nullable SHA256
sidecar_of_object_ordinal       nullable UINT32
```

Let `M=len(objects)`. The `objects` array is stored in increasing numeric `object_ordinal` and its ordinal set is exactly `0..M-1` (`{}` when `M=0`). Duplicate, missing, negative, overflowed, string-valued, or reordered ordinals are invalid.

Both paths are normalized slash-separated UTF-8 paths relative to `<run_root>`. A valid path:

- is nonempty;
- has no leading slash, drive prefix, backslash, empty component, `.` component, `..` component, NUL, or non-NFC component;
- remains below `<run_root>` after component-wise resolution;
- has no symbolic-link component in any existing ancestor; and
- equals the registered role-specific path form.

`durable_source_path` must exist as a readable regular file and no component, including its final component, may be a symlink. `canonical_target_path` must have a symlink-free existing ancestor chain; its final component must be absent before no-replace promotion or an existing readable regular file/bundle member being evaluated as the canonical winner.

Every `canonical_target_path` is unique in the unit. Two descriptors may not claim one target. A hash without readable durable source bytes at `durable_source_path` is invalid.

Exact source-path form by publication mode:

| Publication mode | Exact `durable_source_path` | Additional rule |
|---|---|---|
| `ATOMIC_BUNDLE_MEMBER` | `prepared_evidence/<unit_kind>/<prepared_unit_id>/objects/<object_ordinal_10d>.bin` | target is a member of the one atomically promoted final directory registered for the unit |
| `SINGLE_AUTHORITATIVE_FILE` | same exact prepared-object path | target commits by §3.7 and source bytes remain immutable through terminal inventory |
| `DERIVED_VIEW_TARGET` | same exact prepared-object path | target is a replaceable derivative and never a commit point |
| `REUSE_IMMUTABLE_SOURCE` | exactly equal to `canonical_target_path` | target must already be the validated immutable canonical object; no copy, alias, hard link, or alternate source path is permitted |

`object_ordinal_10d` is the unsigned decimal ordinal left-padded to exactly ten ASCII digits. For non-`REUSE_IMMUTABLE_SOURCE`, the prepared-object file is inside the already committed prepared-unit directory and its bytes, size, and hashes equal the descriptor. For `REUSE_IMMUTABLE_SOURCE`, reopening the target must prove exact size/file hash and registered logical equivalence before the descriptor is valid.

The exact typed object-entry projection is the ten cells below in this order:

```text
object_ordinal                  UINT
object_role                     STRING
content_schema_id               STRING
publication_mode                STRING
durable_source_path             STRING
canonical_target_path           STRING
file_size_bytes                 UINT
file_sha256                     SHA256
logical_sha256                  SHA256 or NULL
sidecar_of_object_ordinal       UINT or NULL
```

### 5.2 Total prepared-object role, sidecar, logical-hash, and cardinality matrix

The descriptor `logical_sha256` is non-null for every non-sidecar role and null for every sidecar role. A sidecar has no independent semantic projection; its bytes are determined by its paired target path and physical target hash.

| Object role | Permitted unit kind | Exact cardinality | Publication mode | Required pairing | `logical_sha256` |
|---|---|---:|---|---|---|
| `PARTITION_PAYLOAD` | `SNAPSHOT_PUBLICATION` | exactly `len(snapshot_claim.partition_entries)` | `SINGLE_AUTHORITATIVE_FILE` or `REUSE_IMMUTABLE_SOURCE` | none | non-null |
| `HISTORY_MANIFEST` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | one history-manifest sidecar | non-null |
| `HISTORY_MANIFEST_SIDECAR` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | points to history manifest | null |
| `HISTORY_INDEX` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | none | non-null |
| `PUBLICATION_MARKER` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | one publication-marker sidecar | non-null |
| `PUBLICATION_MARKER_SIDECAR` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | points to publication marker | null |
| `CURRENT_GENERATION_MANIFEST` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | one current-generation-manifest sidecar | non-null |
| `CURRENT_GENERATION_MANIFEST_SIDECAR` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | points to current-generation manifest | null |
| `CURRENT_GENERATION_INDEX` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | none | non-null |
| `CURRENT_GENERATION_MARKER` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | one current-generation-marker sidecar | non-null |
| `CURRENT_GENERATION_MARKER_SIDECAR` | `SNAPSHOT_PUBLICATION` | 1 | `ATOMIC_BUNDLE_MEMBER` | points to current-generation marker | null |
| `LEGACY_CURRENT_MANIFEST` | `SNAPSHOT_PUBLICATION` | 1 | `DERIVED_VIEW_TARGET` | one legacy-manifest sidecar | non-null |
| `LEGACY_CURRENT_MANIFEST_SIDECAR` | `SNAPSHOT_PUBLICATION` | 1 | `DERIVED_VIEW_TARGET` | points to legacy manifest | null |
| `LEGACY_CURRENT_INDEX` | `SNAPSHOT_PUBLICATION` | 1 | `DERIVED_VIEW_TARGET` | none | non-null |
| `BOUND_PAYLOAD_INTENT` | `FENCE_ACQUIRED` | 1 | `ATOMIC_BUNDLE_MEMBER` | one intent sidecar | non-null |
| `BOUND_PAYLOAD_INTENT_SIDECAR` | `FENCE_ACQUIRED` | 1 | `ATOMIC_BUNDLE_MEMBER` | points to intent | null |
| `FENCE_UNIT_MANIFEST` | every fence unit kind | 1 | `ATOMIC_BUNDLE_MEMBER` | one manifest sidecar | non-null |
| `FENCE_UNIT_MANIFEST_SIDECAR` | every fence unit kind | 1 | `ATOMIC_BUNDLE_MEMBER` | points to fence manifest | null |
| `FENCE_EVENT` | every fence unit kind | 1 | `ATOMIC_BUNDLE_MEMBER` | one event sidecar | non-null |
| `FENCE_EVENT_SIDECAR` | every fence unit kind | 1 | `ATOMIC_BUNDLE_MEMBER` | points to fence event | null |
| `AUTHORIZATION_USE_ROW_BATCH` | §17.8 authorization payload kinds | 1 when required, otherwise 0 | `ATOMIC_BUNDLE_MEMBER` | one batch sidecar when present | non-null when present |
| `AUTHORIZATION_USE_ROW_BATCH_SIDECAR` | paired unit | 1 when batch present, otherwise 0 | `ATOMIC_BUNDLE_MEMBER` | points to authorization batch | null |
| `CAPTURE_ROW_BATCH` | §17.8 capture payload kinds | 1 when required, otherwise 0 | `ATOMIC_BUNDLE_MEMBER` | one batch sidecar when present | non-null when present |
| `CAPTURE_ROW_BATCH_SIDECAR` | paired unit | 1 when batch present, otherwise 0 | `ATOMIC_BUNDLE_MEMBER` | points to capture batch | null |
| `NORMAL_FINAL_INVENTORY` | `NORMAL_FINALIZATION` | 1 | `SINGLE_AUTHORITATIVE_FILE` | one inventory sidecar | non-null |
| `NORMAL_FINAL_INVENTORY_SIDECAR` | `NORMAL_FINALIZATION` | 1 | `SINGLE_AUTHORITATIVE_FILE` | points to inventory | null |
| `NORMAL_FINAL_MARKER` | `NORMAL_FINALIZATION` | 1 | `SINGLE_AUTHORITATIVE_FILE` | one marker sidecar | non-null |
| `NORMAL_FINAL_MARKER_SIDECAR` | `NORMAL_FINALIZATION` | 1 | `SINGLE_AUTHORITATIVE_FILE` | points to marker | null |

For a snapshot unit, the ordered `PARTITION_PAYLOAD` descriptors are one-to-one with `snapshot_claim.partition_entries` by `partition_ordinal`; no extra object and no missing object is permitted. This cardinality is derived only as `len(snapshot_claim.partition_entries)` and no independent partition-count field exists.

Sidecar rules are exact:

1. a sidecar's `sidecar_of_object_ordinal` is non-null and resolves to one non-sidecar object in the same unit;
2. every target requiring a sidecar has exactly one paired sidecar and no second descriptor points to that target;
3. every non-sidecar has null `sidecar_of_object_ordinal`;
4. sidecar payload `target_path` equals the paired target's exact `canonical_target_path`, and `target_file_sha256` equals its exact physical `file_sha256`;
5. a sidecar cannot pair with another sidecar, an object outside the unit, or a different producer's object; and
6. the pair and every role cardinality validate before prepared-directory commit.

Unit-kind batch/intent cardinality is total:

| Unit kind | Bound-intent pair | Authorization batch pair | Capture batch pair |
|---|---:|---:|---:|
| `FENCE_ACQUIRED` | 1 | 0 | 0 |
| `AUTHORIZATION_USE_EVENT_COMMITTED` | 0 | 1 | 0 |
| `REQUEST_RESERVED_COMMITTED` | 0 | 1 | 0 |
| `CAPTURE_STARTED_COMMITTED` | 0 | 0 | 1 |
| `CAPTURE_TERMINAL_COMMITTED` | 0 | 0 | 1 |
| `CAPTURE_SNAPSHOT_COMMITTED` | 0 | 0 | 0 |
| `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED` | 0 | 1 | 0 |
| `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` | 0 | 1 | 0 |
| `FENCE_RELEASED` | 0 | 0 | 0 |

Every prepared unit also contains this exact structural-member set, outside `objects[]`:

| Structural member | Cardinality | Sidecar | Logical-hash rule |
|---|---:|---|---|
| `CLAIM_SCOPE.json` | 1 | exactly one bundled `CLAIM_SCOPE.sha256` | §5.4 `claim_scope_sha256` |
| `CLAIM_SEMANTIC.json` | 1 | exactly one bundled `CLAIM_SEMANTIC.sha256` | role-specific §5.5 claim digest |
| `PREPARATION_PLAN.json` | 1 | exactly one bundled `PREPARATION_PLAN.sha256` | complete-file SHA-256 is prepared-unit ID input |
| `PREPARED_UNIT.json` | 1 | exactly one bundled `PREPARED_UNIT.sha256` | descriptor logical projection excludes no object metadata and complete-file hash is external |

A prepared directory with any extra/missing structural member or mismatched structural sidecar is invalid.

### 5.3 Logical semantics versus physical file bytes

No canonical Parquet byte encoding is introduced. For every Parquet role—partition payload, history/current/legacy index, authorization-use batch, and capture batch—physical SHA-256 identifies one encoding. Semantic equality is independently derived from:

1. exact registered table schema and nullability;
2. exact row-key uniqueness and registered row order;
3. canonical destination-excluded typed-row bytes for every ordered row;
4. exact row count and first/last key; and
5. the recomputed ordered-relation logical hash defined in §5.5.1.

Different physical Parquet bytes may represent identical semantic bytes. The first valid no-replace target is the canonical physical object. Physical inequality alone is never `STOP_SEMANTIC_ID_COLLISION`.

Canonical JSON roles have one canonical byte encoding. A JSON difference is adoptable only through the exact role-specific normalization whitelist in §5.7; after those substitutions and required dependent-hash recomputations, canonical typed claim semantics must be equal.

`STOP_SEMANTIC_ID_COLLISION` is limited to one registered semantic identity mapping to different canonical claim-semantic bytes. It does not cover semantically equal Parquet encodings, producer timestamps, prepared source paths, physical file hashes/sizes, or deterministic sidecar differences allowed by §5.7.

### 5.4 `prepared_claim_scope_v23` and `claim_scope_sha256`

The claim scope identifies the canonical target namespace, not semantic payload contents or the physical publication method. Exact object field order:

```text
schema_version                       STRING = local_curl_prepared_claim_scope.v23
spec_revision                        UINT16 = 23
run_id                               STRING /^run_[0-9a-f]{64}$/
unit_kind                            STRING
subject_family                       nullable STRING in partition-family domain
subject_sequence                     UINT64
expected_predecessor_commit_sha256   nullable SHA256
object_claims                        ARRAY[prepared_claim_object_v23]
object_claims_logical_sha256         SHA256
```

Each `prepared_claim_object_v23` has exact field order:

```text
object_ordinal                       UINT32
object_role                          STRING
content_schema_id                    STRING
canonical_target_path                STRING
```

Its exact typed projection uses logical tags `UINT,STRING,STRING,STRING`. Publication mode is intentionally excluded from claim scope so a recovery unit may use `REUSE_IMMUTABLE_SOURCE` for the same canonical target claimed originally by `SINGLE_AUTHORITATIVE_FILE`. `object_claims` is ordered by ordinal `0..len(object_claims)-1`; its logical hash is SHA-256 of LF-joined canonical typed object-claim bytes, no trailing LF, and SHA-256 of empty bytes when empty.

`claim_scope_sha256` is not a caller value. Its exact logical projection is:

```text
schema_version                       STRING
spec_revision                        UINT
run_id                               STRING
unit_kind                            STRING
subject_family                       STRING or NULL
subject_sequence                     UINT
expected_predecessor_commit_sha256   SHA256 or NULL
object_claims_logical_sha256         SHA256
```

The raw `object_claims` array is validated against its aggregate but is not hashed a second time. `claim_scope_sha256 = SHA256(exact canonical typed-row bytes of the eight cells above)`.

Unit-kind scope semantics are exact and total:

| Unit kind | `subject_family` | `subject_sequence` | `expected_predecessor_commit_sha256` | Required claim-semantic schema |
|---|---|---:|---|---|
| `SNAPSHOT_PUBLICATION` | non-null and equal to the snapshot claim's `audit_family` | exact `snapshot_sequence` | null at sequence 0; otherwise exact prior sequence `snapshot_publication_commit_v23` complete-file SHA-256 | `local_curl_snapshot_publication_claim_semantic.v23` |
| every fence unit kind from `FENCE_ACQUIRED` through `FENCE_RELEASED` | null | exact `fence_sequence` | null at sequence 0; otherwise exact prior `fence_unit_manifest_v23` complete-file SHA-256 | `local_curl_fence_unit_claim_semantic.v23` |
| `NORMAL_FINALIZATION` | null | exactly `0` | null | `local_curl_normal_finalization_claim_semantic.v23` |

No other combination is valid. A normal finalization claim cannot use a runtime head sequence as `subject_sequence`; its singleton scope is fixed at zero. A fence scope cannot carry an audit family. A snapshot scope cannot omit its family. Scope predecessor values are physical commit-chain hashes and are not inferred from timestamps, aliases, or semantic digests.

The hexadecimal digest is persisted in `prepared_evidence_plan_v23` and `prepared_evidence_unit_v23`. Recomputed scope bytes must match it. Different scope bytes under one digest are `STOP_SEMANTIC_ID_COLLISION`; different scopes are ordinary different claims and do not collide. Changing only publication mode while preserving role/schema/target does not change scope.

### 5.5 Closed claim-semantic schemas and ordered-relation hashes

#### 5.5.1 Ordered relation formula

For any registered relation `R`, obtain rows in its registered canonical key order. For each row, construct the exact registered destination-excluded canonical typed-row bytes. Then:

```text
ordered_relation_logical_sha256(R) =
  SHA256(LF-join(row_typed_bytes in canonical row order), no trailing LF)
```

For zero rows it is SHA-256 of empty bytes. The relation formula never hashes physical Parquet bytes, row-group metadata, compression, dictionary order, file path, file size, or a destination row-hash cell. It is total only after schema, nullability, row-hash, uniqueness, and order validation.

#### 5.5.2 `snapshot_publication_claim_semantic_v23`

Exact field order:

```text
schema_version                              STRING = local_curl_snapshot_publication_claim_semantic.v23
spec_revision                               UINT16 = 23
run_id                                      STRING
audit_family                                STRING in partition-family domain
snapshot_sequence                           UINT64
previous_snapshot_file_sha256               nullable SHA256
previous_publication_commit_file_sha256     nullable SHA256
total_row_count                             UINT64
duplicate_key_count                         UINT64 = 0
first_key_canonical_json                    nullable STRING
last_key_canonical_json                     nullable STRING
partition_entries                           ARRAY[snapshot_claim_partition_entry_v23]
partition_entries_semantic_logical_sha256   SHA256
ordered_relation_logical_sha256             SHA256
capture_coverage_state                      STRING {NOT_CAPTURE, CAPTURE_EMPTY_PREFIX_ORIGIN, CAPTURE_THROUGH_FENCE_SEQUENCE}
covered_through_fence_sequence              nullable UINT64
capture_coverage_relation_logical_sha256    nullable SHA256
```

Each semantic partition entry has exact field order:

```text
partition_ordinal               UINT32
partition_id                    STRING /^part_[0-9a-f]{64}$/
partition_path                  STRING
partition_logical_sha256        SHA256
row_count                       UINT64
first_key_canonical_json        nullable STRING
last_key_canonical_json         nullable STRING
```

Entry bytes use these exact typed cells. The entry array is ordinal ordered; its logical hash is LF-joined entry bytes, no trailing LF, or SHA-256 empty for zero entries. No independent partition-count value exists: every count requirement uses `len(partition_entries)`.

The relation named by `ordered_relation_logical_sha256` is the exact concatenation of the decoded partition rows in partition-ordinal and registered row-key order. Its row count equals `total_row_count`.

Capture coverage is exact:

| Family/coverage | State | `covered_through_fence_sequence` | `capture_coverage_relation_logical_sha256` |
|---|---|---|---|
| non-capture | `NOT_CAPTURE` | null | null |
| capture first empty prefix before fence sequence 0 | `CAPTURE_EMPTY_PREFIX_ORIGIN` | null | non-null and equal to `ordered_relation_logical_sha256` (therefore SHA-256 empty) |
| capture through a committed boundary | `CAPTURE_THROUGH_FENCE_SEQUENCE` | non-null | non-null and equal to `ordered_relation_logical_sha256` |

A capture snapshot claim proves that the reconstructed capture relation equals the authoritative committed capture-batch prefix at that exact boundary. No additional snapshot-relation or capture-snapshot-relation digest field exists.

The exact snapshot claim logical projection is:

```text
schema_version                              STRING
spec_revision                               UINT
run_id                                      STRING
audit_family                                STRING
snapshot_sequence                           UINT
previous_snapshot_file_sha256               SHA256 or NULL
previous_publication_commit_file_sha256     SHA256 or NULL
total_row_count                             UINT
duplicate_key_count                         UINT
first_key_canonical_json                    STRING or NULL
last_key_canonical_json                     STRING or NULL
partition_entries_semantic_logical_sha256   SHA256
ordered_relation_logical_sha256             SHA256
capture_coverage_state                      STRING
covered_through_fence_sequence              UINT or NULL
capture_coverage_relation_logical_sha256    SHA256 or NULL
```

The raw partition array is validated against its aggregate and is not hashed again. `snapshot_claim_semantic_sha256` is SHA-256 of the exact sixteen-cell typed row above.

#### 5.5.3 `fence_unit_claim_semantic_v23`

Exact field order:

```text
schema_version                              STRING = local_curl_fence_unit_claim_semantic.v23
spec_revision                               UINT16 = 23
run_id                                      STRING
fence_sequence                              UINT64
previous_fence_unit_file_sha256             nullable SHA256
event_kind                                  STRING
fence_epoch                                 UINT64
fence_token_sha256                          SHA256
acquire_fence_sequence                      UINT64
covered_through_fence_sequence              nullable UINT64
bound_payload_event_kind                    nullable STRING
bound_payload_intent_file_sha256            nullable SHA256
bound_payload_intent_semantic_sha256        nullable SHA256
payload_intent_semantic_sha256              nullable SHA256
authorization_use_batches_logical_sha256    SHA256
capture_batches_logical_sha256              SHA256
snapshot_claim_semantic_sha256              nullable SHA256
capture_ordered_relation_logical_sha256     nullable SHA256
reservation_fence_sequence                  nullable UINT64
reservation_fence_unit_file_sha256          nullable SHA256
reservation_event_row_sha256                nullable SHA256
cancellation_event_row_sha256               nullable SHA256
continuation_activation_event_row_sha256    nullable SHA256
continuation_validation_entries_logical_sha256 nullable SHA256
selected_continuation_validation_entry_sha256 nullable SHA256
payload_fence_sequence                      nullable UINT64
payload_fence_unit_file_sha256              nullable SHA256
release_outcome                             nullable STRING
```

Batch-list hashes are computed from ordered `immutable_row_batch_v23` semantic descriptors, not physical file hashes. An absent batch list hashes as SHA-256 empty. The exact event-specific nullability matrix is §17.5. The claim-semantic digest is SHA-256 of these exact typed cells and excludes physical current-unit hashes/sizes, prepared-unit identifiers, and `event_ts_ns`.

#### 5.5.4 `normal_finalization_claim_semantic_v23`

Exact field order:

```text
schema_version                         STRING = local_curl_normal_finalization_claim_semantic.v23
spec_revision                          UINT16 = 23
pre_run_attempt_id                     nullable STRING /^pra_[0-9a-f]{64}$/
run_id                                 STRING /^run_[0-9a-f]{64}$/
marker_kind                            STRING {REPLAY_FINALIZED, STOP_FINALIZED}
primary_stop_code                      nullable REV23_STOP_CODE
result_label                           nullable STRING in accepted result-label domain
inventory_schema_id                    STRING {local_curl_final_inventory.v23, local_curl_stop_inventory.v23}
inventory_logical_sha256               SHA256
inventory_entry_count                  UINT64
inventory_entries_logical_sha256       SHA256
```

This schema governs run-level V10 finalization only, so `pre_run_attempt_id` is always null. Conditional values are exact:

| `marker_kind` | `inventory_schema_id` | `primary_stop_code` | `result_label` |
|---|---|---|---|
| `REPLAY_FINALIZED` | `local_curl_final_inventory.v23` | null | non-null accepted result label |
| `STOP_FINALIZED` | `local_curl_stop_inventory.v23` | non-null exact governing `REV23_STOP_CODE` and equal to the bound stop state | null |

Reopen the exact canonical inventory JSON and validate its accepted closed schema. `inventory_entry_count=len(inventory.artifacts)`. `inventory_entries_logical_sha256` equals the inventory's recomputed accepted `inventory_semantic_sha256`: SHA-256 of LF-joined accepted artifact-inventory-entry typed rows in accepted artifact-path order, no trailing LF, or SHA-256 empty for zero entries. `inventory_logical_sha256` is SHA-256 of the exact accepted canonical closed-object semantic bytes using that inventory schema's registered `CANONICAL_CLOSED_OBJECT` field order; because the accepted inventory has no destination field in that projection, this is also the SHA-256 of its exact canonical JSON bytes. The registered V10 exclusion rules—inventory target, applicable normal marker and sidecars, and selected normal-finalization prepared subtree as specified in §23.4—are validation invariants and are not represented by an independent pseudo-field in this claim.

The claim-semantic digest is SHA-256 of the exact eleven-cell typed projection above. Physical marker hash/size, prepared ID, sidecars, and `created_at_ns` are excluded. The inventory bytes themselves remain durably prepared and are bound by the prepared object descriptor.

### 5.6 `prepared_evidence_plan_v23` and `prepared_evidence_unit_v23`

`unit_kind` is closed to:

```text
SNAPSHOT_PUBLICATION
FENCE_ACQUIRED
AUTHORIZATION_USE_EVENT_COMMITTED
REQUEST_RESERVED_COMMITTED
CAPTURE_STARTED_COMMITTED
CAPTURE_TERMINAL_COMMITTED
CAPTURE_SNAPSHOT_COMMITTED
CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED
CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED
FENCE_RELEASED
NORMAL_FINALIZATION
```

Preparation-plan exact field order:

```text
schema_version                       STRING = local_curl_prepared_evidence_plan.v23
spec_revision                        UINT16 = 23
run_id                               STRING /^run_[0-9a-f]{64}$/
unit_kind                            STRING
subject_sequence                     UINT64
subject_family                       nullable STRING in partition-family domain
expected_predecessor_commit_sha256   nullable SHA256
claim_scope_file_sha256              SHA256
claim_scope_sha256                   SHA256
claim_semantic_schema_id             STRING
claim_semantic_file_sha256           SHA256
claim_semantic_sha256                SHA256
planned_objects                      ARRAY[prepared_planned_object_v23]
planned_objects_logical_sha256       SHA256
```

Each `prepared_planned_object_v23` exact field order is:

```text
object_ordinal                       UINT32
object_role                          STRING
content_schema_id                    STRING
publication_mode                     STRING
canonical_target_path                STRING
```

Its logical projection uses `UINT,STRING,STRING,STRING,STRING`; ordinals are exact `0..len(planned_objects)-1`.

`claim_scope_file_sha256` equals the complete canonical `CLAIM_SCOPE.json` bytes, and `claim_scope_sha256` equals its §5.4 typed semantic projection. The scope object is reconstructed from plan metadata and `planned_objects` by dropping only `publication_mode` from each planned tuple. `object_claims_logical_sha256` and `planned_objects_logical_sha256` are separately recomputed and are not required to equal. `claim_semantic_schema_id` is exactly one of:

```text
local_curl_snapshot_publication_claim_semantic.v23
local_curl_fence_unit_claim_semantic.v23
local_curl_normal_finalization_claim_semantic.v23
```

`claim_semantic_file_sha256` equals complete canonical `CLAIM_SEMANTIC.json` bytes and `claim_semantic_sha256` equals its registered typed semantic projection. Both claim files and sidecars exist inside the prepared unit before the plan/descriptor are considered recoverable.

The plan excludes physical hashes/sizes, durable source paths, sidecar hashes, prepared-unit ID, descriptor hash, producer nonce, process ID, hostname, and clock reading.

```text
preparation_plan_file_sha256 = SHA256(exact PREPARATION_PLAN.json bytes)
prepared_unit_id = "prep_" + lowercase_hex(preparation_plan_file_sha256)
```

Prepared-unit descriptor exact field order:

```text
schema_version                       STRING = local_curl_prepared_evidence_unit.v23
spec_revision                        UINT16 = 23
run_id                               STRING
prepared_unit_id                     STRING /^prep_[0-9a-f]{64}$/
preparation_plan_file_sha256         SHA256
unit_kind                            STRING
subject_sequence                     UINT64
subject_family                       nullable STRING
expected_predecessor_commit_sha256   nullable SHA256
claim_scope_file_sha256              SHA256
claim_scope_sha256                   SHA256
claim_semantic_schema_id             STRING
claim_semantic_file_sha256           SHA256
claim_semantic_sha256                SHA256
objects                              ARRAY[prepared_evidence_object_v23]
objects_logical_sha256               SHA256
```

Unit metadata is typed-equal to the plan. The descriptor reopens both structural claim files, validates their bundled sidecars, complete-file hashes, schema IDs, and logical hashes. `objects_logical_sha256` hashes LF-joined exact §5.1 object-entry bytes in ordinal order, no final LF. The descriptor binds finalized source/target physical metadata. Final target objects may bind the plan hash/ID but never the descriptor hash; the acyclic graph is `claim semantics → plan → prepared source/final bytes → descriptor`.

### 5.7 Canonical-winner adoption and exact substitution whitelist

A canonical target winner is the first fully valid object or atomic bundle committed by no-replace promotion. A losing candidate is `SUPERSEDED_BY_CANONICAL_WINNER` only if claim scope and claim-semantic digests recompute equal and every role validates under this exact whitelist. Fields not listed for that role must be typed-equal before and after normalization.

| Exact object role(s) | Sole permitted winner substitutions | Required recomputation |
|---|---|---|
| `PARTITION_PAYLOAD` | descriptor `durable_source_path`, `file_size_bytes`, `file_sha256` | none; `logical_sha256`, partition ID, rows, bounds, and target path remain equal |
| `HISTORY_INDEX`, `CURRENT_GENERATION_INDEX`, `LEGACY_CURRENT_INDEX` | descriptor physical source/size/hash; decoded row fields `size_bytes`, `file_sha256`, and destination `snapshot_partition_row_sha256` only where the row references an adopted partition physical variant | recompute every affected row hash and the index ordered-relation logical hash; all semantic partition fields remain equal |
| `AUTHORIZATION_USE_ROW_BATCH`, `CAPTURE_ROW_BATCH` | descriptor physical source/size/hash and paired sidecar bytes/hash | none; complete decoded rows, row hashes, batch logical hash, count, and bounds remain equal |
| `HISTORY_MANIFEST`, `CURRENT_GENERATION_MANIFEST`, `LEGACY_CURRENT_MANIFEST` | `created_at_ns`; `partition_entries[*].size_bytes`; `partition_entries[*].file_sha256`; `partition_entries_logical_sha256` | recompute `partition_entries_logical_sha256` from the winner-bound physical entries; all predecessor, ID, path, logical-hash, row-count, key, total, and coverage fields remain equal |
| `PUBLICATION_MARKER` (`snapshot_publication_commit_v23`) | `preparation_plan_file_sha256`, `prepared_unit_id`, `manifest_file_size_bytes`, `manifest_file_sha256`, `history_index_file_size_bytes`, `history_index_file_sha256`, `committed_at_ns`, destination semantic hash | recompute destination semantic hash; all claim-scope/claim-semantic, run/family/sequence/predecessor, relation, and capture-binding fields remain equal |
| `CURRENT_GENERATION_MARKER` (`snapshot_current_view_commit_v23`) | `preparation_plan_file_sha256`, `prepared_unit_id`, current manifest/index physical sizes/hashes, `committed_at_ns`, destination semantic hash | recompute destination semantic hash; head sequence/history hash/claim semantics remain equal |
| `BOUND_PAYLOAD_INTENT` | none | byte equality required |
| `FENCE_UNIT_MANIFEST`, `FENCE_EVENT` | `preparation_plan_file_sha256`, `prepared_unit_id`, child physical file hashes/sizes already proven equivalent, `event_ts_ns`, destination logical/row hashes that include only those whitelisted physical fields | recompute affected destination hashes; sequence/predecessor/event/epoch/token, intent hashes, logical batch/snapshot hashes, identities, and release outcome remain equal |
| `NORMAL_FINAL_INVENTORY` | none | exact canonical inventory byte equality required; by V10 every selected canonical physical object is already fixed, so differing inventory physical metadata is a different normal-finalization claim |
| `NORMAL_FINAL_MARKER` | `normal_finalization_prepared_unit_id`, `created_at_ns`, destination semantic hash | recompute marker semantic hash; marker kind, stop/result, `inventory_file_sha256`, and the normal-finalization claim's inventory schema/logical/count fields remain equal |
| every sidecar role | complete sidecar bytes and sidecar physical hash, only as deterministic function of the paired winner's unchanged target path and winner target physical hash | recompute sidecar bytes/hash; paired ordinal/path remain equal |

No field omitted from the table may be substituted. In particular, `content_schema_id`, canonical target path, claim-scope hash, claim-semantic hash, logical row/relation hashes, semantic identities, sequence/predecessor values, bound payload intent, authorization/reservation identity, and release outcome may never differ.

For every whitelisted replacement, all dependent physical-reference fields and physical aggregate hashes must be recomputed from the winner; no stale candidate-derived hash may remain. The normalized interpreted objects must then produce equal exact claim-semantic bytes.

Adoption requirements are all mandatory:

1. winner is fully committed, readable, structurally valid, and recoverable;
2. candidate and winner have equal recomputed `claim_scope_sha256`;
3. candidate and winner have equal recomputed claim-semantic schema and digest;
4. every Parquet variant independently validates §5.3;
5. sidecars validate only with their own producer target; no cross-pair is read as valid;
6. predecessor, run/family/sequence, semantic identities, counts, bounds, and domains agree;
7. no canonical artifact selects the loser as a second winner;
8. winner source bytes and every transitive recovery source remain durable; and
9. any committed loser remains immutable and enters terminal inventory.

A transient uncommitted loser may be discarded. A committed loser is nonblocking only after the classification is independently rederived. It cannot publish, overwrite, merge, form a second head, or supply a different payload to an acquired fence.

A fork/collision stop is reserved for incompatible canonical commits, different semantic bytes under one semantic identity, unequal claim semantics under one claim scope, invalid winner bytes, ambiguous winner assignment, or missing winner recovery sources. Physical Parquet inequality with equal ordered-relation bytes is not a conflict.

### 5.8 Prepared-unit commit, retention, and recovery

The producer constructs exact claim-scope bytes, claim-semantic bytes, their sidecars, plan, exact object-source bytes, plan sidecar, descriptor, and descriptor sidecar under transient staging, closes and flushes all members, and atomically no-replace promotes the complete prepared directory. That directory rename is the sole prepared-unit commit point.

A committed prepared candidate is finalization-neutral only after it is selected as the canonical producer or validly `SUPERSEDED_BY_CANONICAL_WINNER`. Every other committed candidate is pending/conflicting and blocks normal finalization. Hash-only intent, absent source bytes, invalid source path, symlink source, ambiguous target, or unrecoverable transitive source is not recovery evidence.

Every selected and superseded prepared unit, including its plan, plan sidecar, descriptor, descriptor sidecar, and all `objects/<ordinal>.bin` bytes, remains immutable through the applicable terminal inventory. A recovery unit may use `REUSE_IMMUTABLE_SOURCE` only under the exact source-equals-target rule in §5.1.

## 6. Snapshot sequence, predecessor chain, transitions, and cycles

### 6.1 Origin, uniqueness, and contiguity

Snapshot sequence is scoped by exact `(run_id,audit_family)`.

- The first committed sequence is `0`.
- Committed sequences are exactly `0..N` with no gap.
- A sequence number identifies at most one canonical history directory.
- The manifest `snapshot_sequence`, history path component, publication marker sequence, and prepared unit subject sequence are typed-equal.
- A byte-identical manifest at a second history path is a duplicate and invalid; equality of content does not permit duplicate sequence identities.

### 6.2 Predecessor construction

For sequence `0`:

```text
previous_snapshot_file_sha256 = null
previous_publication_commit_file_sha256 = null
```

For sequence `s>0`:

```text
previous_snapshot_file_sha256 = SHA256(complete stored historical manifest bytes at s-1)
previous_publication_commit_file_sha256 = SHA256(complete stored PUBLICATION_COMMITTED.json bytes at s-1)
```

The predecessor hashes bind exact stored bytes, not parsed/re-serialized objects, current aliases, sidecars, partition files, or directory names.

### 6.3 Permitted transitions

A successor may:

- append new family rows;
- publish a no-change checkpoint with the same logical relation;
- repartition the same or expanded logical relation into different immutable partitions.

It may not remove or mutate a previously committed family row. Monotonicity is validated at the family row-key and exact typed-row-byte level, not by requiring partition-entry prefix extension.

### 6.4 Fork, duplicate, missing predecessor, rollback, stale, out-of-order, and cycle handling

Reject and preserve evidence for:

- two distinct committed candidates for one sequence;
- one predecessor with two different committed successors;
- missing sequence or predecessor bytes;
- predecessor hash mismatch;
- sequence rollback or reuse;
- successor `created_at_ns <= predecessor.created_at_ns`;
- path/field sequence disagreement;
- self-edge, forward edge, disconnected component, two-node cycle, or longer cycle;
- current view claiming a non-head sequence.

Validation builds a directed graph from exact predecessor hashes, verifies one origin, indegree/outdegree constraints, contiguity, and then performs a visited/active-stack traversal before selecting a head. A cycle or fork never yields a latest snapshot.

### 6.5 Committed snapshot definition

For `analysis_compatibility` and `analysis_strict`, a snapshot is committed when its complete history directory is atomically promoted and validates.

For `capture`, a prepared snapshot candidate may exist before fence acquisition, but no canonical capture history directory may be promoted before an exclusive capture fence is durably acquired. Under one and the same open acquisition:

1. derive the committed capture-row prefix boundary (`null` at acquisition sequence 0, otherwise `A-1`);
2. independently reconstruct and validate the complete authoritative capture prefix;
3. prove the prepared snapshot's logical relation equals that prefix exactly;
4. validate predecessor/head identity and every partition object;
5. before promotion, validate the acquisition's immutable payload-intent bytes and prove their snapshot claim/ordered-relation/coverage and authorization-reservation identity equal this candidate;
6. atomically promote the exact canonical capture history directory;
7. commit at `A+1` exactly the payload kind and logical identities bound by that intent; and
8. durably commit the matching release.

The snapshot becomes committed only at the binding payload's fence-unit commit. The later release controls fence closure and downstream use. A promoted capture history directory without its payload remains recoverable only under the same still-open fence; no later proof-relevant commit can make it stale. A capture history directory promoted without a matching open acquisition is invalid and maps to `STOP_CAPTURE_SNAPSHOT_INVALID`.

## 7. Snapshot publication and recovery

### 7.1 Snapshot prepared unit

The snapshot prepared unit contains or durably references every byte required to recover every new/reused partition, history bundle, current-generation bundle, and legacy mirror target. It obeys the total §5.2 matrix. Every object has exact source path, target path, size, physical hash, and required logical hash.

For `capture`, preparation may precede acquisition. Canonical partition reuse/promotion may also precede acquisition because partition objects are immutable and unreferenced until a history bundle commits. Before acquisition, the exact §5.5.2 snapshot claim and §17.4 payload intent must already be derivable. Canonical **capture history-directory** promotion, prefix validation, the payload matching the acquisition-bound intent, and release must all occur under one open fence as specified in §§6.5 and 17.8.

### 7.2 Immutable partition publication and physical-object adoption

For each partition candidate:

1. validate the durable source bytes and registered logical projection;
2. if the canonical target is absent, atomically no-replace promote the candidate file and reopen it;
3. if the target exists and physical bytes are equal, treat as idempotent success;
4. if physical bytes differ, independently decode both files and apply §5.3;
5. when semantic bytes, `partition_id`, row count, key bounds, schema, ordering, and partition logical hash are equal, adopt the existing canonical physical object and classify the losing candidate or prepared unit `SUPERSEDED_BY_CANONICAL_WINNER` as applicable;
6. when the same `partition_id` maps to different semantic bytes, emit `STOP_SEMANTIC_ID_COLLISION`;
7. when target path/identity or structure is invalid without a semantic-ID collision, emit the applicable family snapshot stop.

The first valid no-replace physical object remains immutable. No producer rewrites it to obtain byte equality. A later history manifest/index must bind the canonical winner's actual file hash and size. If an earlier prepared manifest referenced the losing physical hash, that prepared unit cannot publish; a recovery prepared unit may reuse the canonical winner and the earlier unit becomes superseded.

### 7.3 Atomic history-directory publication

For analysis families, the producer builds the exact five-member history bundle, validates it, and atomically no-replace promotes it. A pre-existing valid canonical directory may be adopted under §5.6; differing canonical JSON semantics or a genuine sequence claim conflict triggers the applicable family snapshot stop.

For `capture`, the same operation is permitted only after fence acquisition and successful prefix/predecessor validation under that acquisition. Exact order is:

```text
FENCE_ACQUIRED committed with exact immutable payload intent
→ capture prefix and the exact bound snapshot claim validated under the open fence
→ exact history directory atomically promoted/adopted
→ only the payload matching the bound intent committed at A+1
→ FENCE_RELEASED committed
```

No capture history target is promoted before acquisition. If validation fails before promotion, the acquisition closes with `ABORTED_NO_OUTPUT`. If atomic history promotion is unsupported or irrecoverably fails, emit `STOP_CAPTURE_SNAPSHOT_INVALID`; if no payload committed, close the fence with the exact aborted release when that release remains structurally possible. If the history directory commits and process loss occurs before the payload, the still-open fence prevents later capture/authorization commits and recovery resumes only the payload named by the acquisition's immutable intent bytes or conflict-stops. No stale-residue race state exists.

`PUBLICATION_COMMITTED.json` is `local_curl_snapshot_publication_commit.v23` with exact field order:

```text
schema_version                           STRING
spec_revision                            UINT16
run_id                                   STRING
audit_family                             STRING
snapshot_sequence                        UINT64
previous_publication_commit_file_sha256  nullable SHA256
preparation_plan_file_sha256             SHA256
prepared_unit_id                         STRING
claim_scope_sha256                       SHA256
snapshot_claim_semantic_sha256           SHA256
manifest_path                            STRING
manifest_file_size_bytes                 UINT64
manifest_file_sha256                     SHA256
history_index_path                       STRING
history_index_file_size_bytes            UINT64
history_index_file_sha256                SHA256
partition_entries_semantic_logical_sha256 SHA256
ordered_relation_logical_sha256          SHA256
capture_fence_binding_required           BOOL
committed_at_ns                          UTC_NS
publication_commit_semantic_sha256       SHA256
```

Its semantic projection excludes only destination `publication_commit_semantic_sha256` and uses the displayed order. For capture, `capture_fence_binding_required=true`; for analysis families it is false. For capture it is canonical history residue until the matching bound payload commits; it is not a snapshot head before that payload.

### 7.4 Current-view generation and legacy mirrors

After a unique committed head exists, the producer atomically promotes or adopts the exact head current-view generation. `CURRENT_VIEW_COMMITTED.json` is `local_curl_snapshot_current_view_commit.v23` with exact field order:

```text
schema_version                           STRING
spec_revision                            UINT16
run_id                                   STRING
audit_family                             STRING
snapshot_sequence                        UINT64
history_publication_commit_file_sha256   SHA256
snapshot_claim_semantic_sha256           SHA256
preparation_plan_file_sha256             SHA256
prepared_unit_id                         STRING
current_manifest_path                    STRING
current_manifest_file_size_bytes         UINT64
current_manifest_file_sha256             SHA256
current_index_path                       STRING
current_index_file_size_bytes            UINT64
current_index_file_sha256                SHA256
committed_at_ns                          UTC_NS
current_view_commit_semantic_sha256      SHA256
```

The semantic projection excludes only its destination. Physical Parquet variation is accepted only through §5.3 and §5.7. The generation is authoritative for current-view validation.

Legacy mirrors are repaired only from that generation using the accepted stable mirror-read protocol. A missing, stale, cross-generation, unstable, or mismatched mirror is `CURRENT_VIEW_REPAIRABLE`; it does not alter history or head derivation.

### 7.5 Complete snapshot recovery and contention classification

| Durable state | Classification | Exact handling | Normal-finalization eligible after handling |
|---|---|---|---:|
| transient staging only; no committed prepared unit | `TRANSIENT_ONLY` | discard or restart | yes |
| one valid prepared unit; no canonical target | `PREPARED_READY` | resume exact unit | after completion |
| existing valid canonical target; candidate semantically equal under §5.6 | `SUPERSEDED_BY_CANONICAL_WINNER` | adopt winner; retain committed loser in inventory | yes |
| valid canonical Parquet target with different physical bytes but equal logical bytes | `CANONICAL_PHYSICAL_OBJECT_ADOPTED` | bind winner hash/size in a recovery unit; supersede loser | yes |
| strict subset of exact partitions promoted | `PARTITION_PROMOTION_PARTIAL_RECOVERABLE` | promote/adopt remaining exact partitions | after completion |
| analysis history directory absent | `HISTORY_DIRECTORY_PENDING_RECOVERABLE` | promote/adopt exact directory if predecessor remains head | after completion |
| capture prepared candidate; no fence acquired | `CAPTURE_FENCE_ACQUISITION_REQUIRED` | acquire fence before any history promotion | no |
| capture history promoted under open fence; binding payload absent; prepared payload valid | `CAPTURE_BINDING_PENDING_RECOVERABLE` | commit exact payload and release under same acquisition | after completion |
| capture history promoted but no matching open acquisition exists | `CAPTURE_HISTORY_PROMOTED_OUTSIDE_FENCE` | `STOP_CAPTURE_SNAPSHOT_INVALID`; preserve evidence | no |
| valid committed head; current generation/mirrors missing or stale | `CURRENT_VIEW_REPAIRABLE` | reconstruct from head | after repair |
| committed candidate cannot prove equality to canonical winner | `CONFLICTING_SEMANTIC_CLAIM` | family stop or semantic-ID collision as applicable | no |
| two different canonical committed sequence claims | `PUBLICATION_FORK_CONFLICT` | applicable family snapshot stop | no |
| committed target lacks required durable source bytes | `RECOVERY_SOURCE_MISSING` | applicable family snapshot stop | no |

An unselected or losing candidate is not itself a fork. Fork status requires incompatible canonical sequence topology or a genuine conflicting semantic claim. Every committed superseded prepared unit is retained and included in final inventory closure.

## 8. Historical reconciliation, latest/final derivation, and inventories

### 8.1 Historical own-entry reconciliation

Every committed historical manifest reconciles only against:

- its own ordered `partition_entries`;
- the immutable partition files named by those entries;
- its own history index;
- its own prepared unit and publication marker;
- its own predecessor links.

A historical manifest is never compared to the current alias, current-view generation, or current `snapshot_partitions.parquet` mirror.

### 8.2 Unique head and current reconciliation

The unique head is the sole committed snapshot with no committed successor after chain/fork/cycle validation. Only that head reconciles against:

- `current_view_generations/<head>/...`;
- `<family_root>/audit_snapshot_manifest.json` and sidecar;
- `<family_root>/snapshot_partitions.parquet`.

All must be byte-/field-equal to the head's prepared current-view objects. A stale or missing current view is repairable; a current view cannot change historical validity or head selection.

### 8.3 Successor repartition

A successor may replace predecessor partitions with a different partitioning if:

- predecessor history still validates against its original immutable partitions;
- successor history validates against its own partitions;
- row-level monotonicity and family relation rules hold;
- every partition referenced by either sequence remains immutable and inventoried.

Example: S0 references P0/P1; S1 references P2/P3 for the same expanded relation. S0 is validated only with P0/P1. S1 and the current view are validated with P2/P3. Comparing S0 to the S1 index is forbidden.

### 8.4 Latest and timestamp-bounded snapshot

After complete chain validation:

- `latest_snapshot` is the unique head.
- For a capture fence boundary `F`, `latest_capture_snapshot_at_F` is the committed capture snapshot with greatest snapshot sequence whose bound `covered_through_fence_sequence` is null only for the empty origin or is `<=F`.
- A pending, forked, cyclic, invalid, or unbound snapshot is excluded.

### 8.5 Final snapshot

A family final snapshot exists only when:

1. one unique committed head exists;
2. every committed prepared candidate is selected or validly `SUPERSEDED_BY_CANONICAL_WINNER`, and no unresolved prepared unit, open-fence capture binding, or publication conflict remains for that family;
3. current generation and legacy mirrors equal the head;
4. final inventory closure holds;
5. the applicable normal finalization marker commits.

Conflict-stop finalization does not create a family final snapshot.

### 8.6 Complete inventories

A normal replay or clean-stop final inventory contains:

- the complete history chain from sequence 0 through head;
- every history manifest sidecar;
- every history index;
- every publication marker sidecar;
- every prepared snapshot unit used by committed sequences and every committed snapshot candidate validly `SUPERSEDED_BY_CANONICAL_WINNER`, including each plan, descriptor, structural sidecar, and object payload;
- every committed current-view generation from sequence 0 through the head, and the exact head generation;
- legacy current mirrors;
- the union of every immutable partition referenced by every committed historical sequence;
- every prepared fence unit used by committed fence sequences and every committed fence candidate validly `SUPERSEDED_BY_CANONICAL_WINNER`, including each plan, descriptor, structural sidecar, and object payload;
- complete fence history and all bundled sidecars;
- every immutable authorization/capture row batch;
- final aggregate relation views.

The normal inventory excludes itself, its future normal marker and derivative sidecars, and the selected `NORMAL_FINALIZATION` prepared-unit subtree because that subtree contains the inventory's own source bytes. This is a closed finalization-self exclusion, not a general omission. The normal marker binds `normal_finalization_prepared_unit_id`; terminal validation resolves that exact immutable prepared unit and verifies its plan, descriptor, inventory source bytes, marker source bytes, and sidecar sources against the committed targets.

A conflict-stop inventory additionally contains every readable pending prepared unit, committed superseded unit, promoted residue, conflicting target, open fence unit, incomplete current view, and unresolved competing semantic claim. It must not claim superseded or conflicting objects are canonical committed evidence.

---

## 9. Partition ordinal origin, uniqueness, contiguity, and missing ordinals

For each snapshot manifest independently, let `P=len(partition_entries)`.

```text
ordinal set = {}                  when P = 0
ordinal set = {0,1,...,P-1}       when P > 0
```

Within each manifest:

- every ordinal occurs exactly once;
- entries are stored in numeric ordinal order;
- partition IDs and paths are unique;
- an ordinal gap, duplicate, negative, overflow, string encoding, or coercion is invalid;
- missing ordinals are never compressed, renumbered, inferred from paths, or borrowed from another sequence.

For the unique head only, the current generation and current mirror ordinal sets and row orders must equal the head manifest. Historical manifests have no dependency on current indexes.

---

## 10. Partition key canonicalization and comparison

### 10.1 Canonical key bytes

For each key field in registered key order, encode one typed cell:

```json
{"n":"<field>","t":"<registered logical tag>","v":<logical value>}
```

Serialize the outer array under Revision 23 canonical typed-row rules: compact UTF-8, exact key-field order, NFC strings, exact integer semantics, no BOM, no final LF. Null is prohibited in family keys.

Capture key:

```json
[{"n":"request_id","t":"STRING","v":"req_<64-lowercase-hex>"},{"n":"attempt_number","t":"UINT","v":1},{"n":"capture_event_ordinal","t":"UINT","v":0}]
```

Compatibility/strict key:

```json
[{"n":"request_id","t":"STRING","v":"req_<64-lowercase-hex>"},{"n":"attempt_number","t":"UINT","v":1}]
```

### 10.2 Comparison

Decode canonical key arrays and compare tuples lexicographically:

- `STRING`: unsigned UTF-8 byte order of the NFC string;
- `UINT` or `INT`: mathematical integer order;
- tuple: first unequal field decides.

Raw JSON text order, locale collation, filesystem order, Parquet dictionary order, signed reinterpretation, and caller-supplied comparators are forbidden.

---

## 11. First/last keys and empty partitions

### 11.1 Nonempty partition

For `row_count>0`:

- rows are schema-valid, row-hash-valid, unique by key, and persisted in registered key order;
- `first_key_canonical_json` and `last_key_canonical_json` are non-null and equal the minimum and maximum reconstructed keys;
- `first_key <= last_key`;
- equality is valid only for exactly one unique row.

### 11.2 Empty partition

For `row_count=0`:

```text
first_key_canonical_json = null
last_key_canonical_json  = null
partition logical bytes  = empty byte string
logical_sha256            = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The `partition_id` projection uses `t:"NULL",v:null` for both key-bound cells. The partition file must still be a readable zero-row relation with the exact family schema. A missing, zero-byte, malformed, or schema-less file is not an empty partition.

For `manifest.total_row_count=0`, manifest first/last keys are null. Otherwise both are non-null and equal the global minimum/maximum over nonempty partitions.

---

## 12. Inverted, overlapping, duplicate, adjacent, and missing ranges

Process entries by ordinal.

- **Inverted:** nonempty `first_key > last_key` is invalid.
- **Duplicate:** any duplicate row key within or across partitions is invalid; independently derived `duplicate_key_count` must be zero.
- **Overlap:** for consecutive nonempty partitions, require `previous.last_key < current.first_key`. Equality is overlap.
- **Adjacent:** means only strict ordered non-overlap. Keys are sparse tuples; no immediate-successor rule exists.
- **Missing evidence:** exists only from a missing ordinal/entry/file, a family row committed at the snapshot fence but absent from reconstruction, a total/bound mismatch, or a canonical partition outside committed-history union and every valid prepared unit. A lexical/numeric gap in tuple space is not missing evidence.
- **Global order:** concatenating rows in partition ordinal order must equal the complete family relation in registered key order. Set equality after resorting is insufficient.

---

## 13. Partition, index-row, and entry hash projections

### 13.1 Partition logical hash

For each partition:

1. validate each row's registered destination-excluded row-hash projection;
2. encode exact canonical typed-row bytes;
3. sort by registered family key;
4. LF-join with no trailing LF; and
5. SHA-256 the resulting bytes.

Physical Parquet bytes are independently bound by `file_sha256` and `size_bytes`.

### 13.2 Existing seven-field `partition_id`

Exact ordered cells remain:

| Field | Logical tag when non-null | Null rule |
|---|---|---|
| `run_id` | `STRING` | prohibited |
| `audit_family` | `STRING` | prohibited |
| `partition_ordinal` | `UINT` | prohibited |
| `row_count` | `UINT` | prohibited |
| `first_key_canonical_json` | `STRING` | `NULL` |
| `last_key_canonical_json` | `STRING` | `NULL` |
| `partition_logical_sha256` | `SHA256` | prohibited |

```text
partition_id = "part_" + lowercase_hex(SHA256(exact seven-cell typed-row bytes))
```

No path, file hash, size, manifest hash, snapshot sequence, or index-row hash is included.

### 13.3 `table:snapshot_partition` row hash

Exact destination-excluded projection:

```text
schema_version                  STRING
spec_revision                   UINT
partition_ordinal               UINT
partition_id                    STRING
partition_path                  STRING
row_count                       UINT
size_bytes                      UINT
file_sha256                     SHA256
logical_sha256                  SHA256
first_key_canonical_json        STRING or NULL
last_key_canonical_json         STRING or NULL
```

### 13.4 Embedded partition-entry bytes and aggregate

Exact entry projection:

```text
file_sha256                     SHA256
first_key_canonical_json        STRING or NULL
last_key_canonical_json         STRING or NULL
logical_sha256                  SHA256
partition_id                    STRING
partition_ordinal               UINT
partition_path                  STRING
row_count                       UINT
size_bytes                      UINT
```

`partition_entry_logical_sha256` is SHA-256 of one entry's exact nine-cell bytes and is validation-only. `partition_entries_logical_sha256` is SHA-256 of ordinal-ordered LF-joined entry bytes with no final LF. Zero entries use SHA-256 of empty bytes.

---

## 14. Snapshot canonical bytes, file hashes, sidecars, and interpreted equality

The existing manifest field set remains closed and unchanged:

```text
audit_family
created_at_ns
duplicate_key_count
first_key_canonical_json
last_key_canonical_json
partition_entries
partition_entries_logical_sha256
previous_snapshot_file_sha256
run_id
schema_version
snapshot_sequence
spec_revision
total_row_count
```

Every nullable field is present with JSON null when null. Exact canonical bytes are rederived from the interpreted object and must equal stored bytes. The complete-file hash is SHA-256 of those exact bytes and is external to the manifest.

Historical manifest and sidecar commit together only as members of the atomic history directory. Current mirror sidecars follow the deterministic target-first repair rule in §3.5.

Two manifests are interpreted-equal only with exact typed recursive equality and identical ordered entries. Current generation and legacy alias require both interpreted equality and byte equality with the unique head. A predecessor link always uses exact stored historical bytes, never reserialized bytes.

---

## 15. Per-snapshot count and relation reconciliation

For every committed historical sequence `s`, derive from its own entries and partitions:

```text
P_s = len(S[s].partition_entries)
R_s = sum(entry.row_count)
K_s = number of distinct reconstructed keys
```

Require:

```text
ordinals = 0..P_s-1
R_s = S[s].total_row_count
K_s = S[s].total_row_count
S[s].duplicate_key_count = 0
```

For each entry, independently validate canonical path, immutable readable bytes, size, file hash, family table schema, actual row count, row hashes, logical hash, first/last keys, and `partition_id`.

For the unique head only, current generation and mirror index rows must equal the head entries field-for-field. No historical sequence is compared to a current index.

The reconstructed relation must equal the authoritative family relation at that snapshot's committed publication/fence boundary. Summary fields are not substitutes for partition reads.

---

## 16. Physical persistence of authorization-use and capture rows

### 16.1 Primary evidence is immutable row batches

A row is committed only when its exact bytes occur in one immutable row-batch file inside one atomically committed fence-unit directory. A row hash, aggregate Parquet row, prepared object, or caller assertion is insufficient.

The accepted row schemas and row-hash projections remain unchanged. The batch file contains complete accepted table rows, including destination row hashes.

### 16.2 `immutable_row_batch_v23`

Each fence-unit manifest contains one descriptor per row batch with exact field order:

```text
schema_version                   STRING = local_curl_immutable_row_batch.v23
spec_revision                    UINT16 = 23
run_id                           STRING
fence_sequence                   UINT64
relation_name                    STRING {authorization_use_events, capture_events}
batch_relative_path              STRING
batch_sidecar_relative_path      STRING
schema_id                        STRING
row_count                        UINT64
first_key_canonical_json         nullable STRING
last_key_canonical_json          nullable STRING
file_size_bytes                  UINT64
file_sha256                      SHA256
logical_sha256                   SHA256
ordered_row_sha256s              ARRAY[SHA256]
ordered_row_sha256s_logical_sha256 SHA256
```

Rules:

- `run_id` and `fence_sequence` equal the containing fence unit.
- `ordered_row_sha256s` exactly equals physical rows in registered relation order.
- `ordered_row_sha256s_logical_sha256` is SHA-256 of LF-joined canonical typed cells `{"n":"row_sha256","t":"SHA256","v":"<digest>"}` in list order, no trailing LF, or SHA-256 empty when the list is empty.
- `row_count` equals list length and physical row count.
- first/last keys are null only for zero rows; otherwise they are canonical accepted table keys.
- batch logical hash is SHA-256 of LF-joined canonical destination-excluded row bytes with no trailing LF.
- file hash/size bind exact Parquet bytes.
- sidecar bytes are bundled in the same fence directory and bind the batch final path/hash.
- the physical descriptor row-hash projection uses the exact listed field order, with the raw array validated against `ordered_row_sha256s_logical_sha256`;
- the batch claim-semantic projection excludes physical path/sidecar path/size/file hash and raw array, and is exactly:

```text
relation_name                         STRING
schema_id                             STRING
row_count                             UINT
first_key_canonical_json              STRING or NULL
last_key_canonical_json               STRING or NULL
logical_sha256                        SHA256
ordered_row_sha256s_logical_sha256    SHA256
```

`authorization_use_batches_logical_sha256` and `capture_batches_logical_sha256` in §5.5.3 are SHA-256 of LF-joined canonical batch claim-semantic rows for the applicable relation in batch order; absent lists hash as SHA-256 empty.

### 16.3 One-to-one row provenance

The validator requires:

- every committed authorization/capture row appears in exactly one committed row batch;
- every committed row batch belongs to exactly one committed fence unit;
- no row hash occurs in two batches;
- no fence unit claims a row absent from its batch;
- no batch contains an unclaimed row;
- relation name, row schema, row key, tuple identities, row hashes, and batch descriptors reconcile exactly.

### 16.4 Aggregate views

Aggregate views are rebuilt by:

1. traversing the valid committed fence chain in sequence order;
2. selecting every batch of the requested relation;
3. validating each batch;
4. concatenating rows;
5. rejecting duplicate relation keys or row hashes;
6. sorting by the accepted table ordering;
7. writing the complete aggregate Parquet relation.

The aggregate logical hash is derived from all ordered rows. The existing aggregate paths are atomically replaced as single authoritative view files. They are not historical authority. A missing/stale aggregate view is repairable from committed row batches; an aggregate view containing an extra, missing, or different row is invalid as a view but cannot rewrite row history.

---

## 17. Durable capture-fence history and acquisition-bound payload intent

### 17.1 Purpose

The fence history is the sole durable serialization authority for proof-relevant commits. Every committed reservation, capture STARTED/terminal row, capture snapshot binding, no-start cancellation row, CONTINUATION activation row, and CONTINUATION reservation validation is contained or referenced by exactly one committed fence payload unit.

A fence acquisition is never generic. It commits one exact immutable payload intent. Only the event and semantics named by that intent may occupy the immediately following payload position.

### 17.2 Fence-unit chain

`fence_sequence` is scoped by `run_id`, begins at 0, is unique and contiguous, and uses exact 20-digit directories. Each `FENCE_UNIT.json` binds the exact previous manifest file hash, null only at sequence 0. The graph has one origin, one unique head, no gap, duplicate canonical unit, fork, rollback, disconnected component, self-edge, forward edge, or cycle.

A noncanonical prepared candidate does not enter the chain. It may be superseded only under §5.7. Two incompatible canonical directories or different fence claim-semantic bytes under one fence identity are structural conflicts.

### 17.3 Fence token, nullable origin, and first acquisition

For `FENCE_ACQUIRED`:

```text
fence_token_sha256 = SHA256(canonical typed cells:
  run_id                                  STRING
  fence_epoch                             UINT
  acquire_fence_sequence                  UINT
  previous_fence_unit_file_sha256         SHA256 or NULL
  bound_payload_intent_semantic_sha256    SHA256)
```

At the first acquisition:

```text
acquire_fence_sequence = 0
fence_epoch = 0
previous_fence_unit_file_sha256 = null
covered_through_fence_sequence = null
```

Null means the committed prefix before acquisition is empty. It is never encoded as `-1`, `UINT64_MAX`, zero, or text. For acquisition `A>0`, `covered_through_fence_sequence=A-1`. Epoch increments by exactly one per acquisition.

### 17.4 `capture_payload_intent_v23`

The exact intent is committed as `bound_payload_intent.json` inside the acquisition directory. Field order:

```text
schema_version                                  STRING = local_curl_capture_payload_intent.v23
spec_revision                                   UINT16 = 23
run_id                                          STRING
acquire_fence_sequence                          UINT64
expected_payload_fence_sequence                 UINT64
payload_event_kind                              STRING
expected_previous_fence_unit_file_sha256        nullable SHA256
authorization_id                                nullable STRING
authorization_mode                              nullable STRING in accepted authorization-mode domain
reservation_id                                  nullable STRING
request_id                                      nullable STRING
attempt_number                                  nullable UINT32
authorization_use_batch_logical_sha256          nullable SHA256
authorization_use_row_sha256                    nullable SHA256
capture_batch_logical_sha256                    nullable SHA256
capture_row_sha256                              nullable SHA256
capture_event_state                             nullable STRING
capture_snapshot_sequence                       nullable UINT64
capture_snapshot_claim_semantic_sha256          nullable SHA256
capture_ordered_relation_logical_sha256         nullable SHA256
capture_coverage_state                          nullable STRING in §5.5.2 capture-state domain
covered_through_fence_sequence                  nullable UINT64
reservation_fence_sequence                      nullable UINT64
reservation_fence_unit_file_sha256              nullable SHA256
reservation_event_row_sha256                    nullable SHA256
continuation_validation_entries_logical_sha256  nullable SHA256
selected_continuation_validation_entry_sha256   nullable SHA256
```

Always require:

```text
expected_payload_fence_sequence = acquire_fence_sequence + 1
```

with no UINT64 overflow, and `expected_previous_fence_unit_file_sha256` equal to the acquisition unit's predecessor hash, not the future acquisition hash. This avoids a cycle.

The intent semantic digest is SHA-256 of the exact canonical typed fields above. It excludes prepared IDs, physical files/hashes/sizes of future objects, future payload-unit hash, event timestamps, process ID, and release hash.

Event-specific intent nullability is total:

| Intended payload | Required non-null intent fields beyond common sequence fields | All other payload fields |
|---|---|---|
| `AUTHORIZATION_USE_EVENT_COMMITTED` | authorization identity, authorization batch logical hash, authorization row hash | null |
| `REQUEST_RESERVED_COMMITTED` | authorization/reservation/request/attempt identity, authorization batch logical hash, reservation row hash; selected validation hash additionally required for CONTINUATION | null |
| `CAPTURE_STARTED_COMMITTED` | authorization/reservation/request/attempt identity, capture batch logical hash, capture row hash, `capture_event_state=STARTED` | null |
| `CAPTURE_TERMINAL_COMMITTED` | same identity, capture batch logical hash, capture row hash, event state `INTERRUPTED` or `COMPLETED` | null |
| `CAPTURE_SNAPSHOT_COMMITTED` | snapshot sequence, snapshot claim-semantic hash, capture ordered-relation hash, capture coverage state/boundary | null |
| `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED` | snapshot fields; authorization/reservation/request/attempt identity; authorization batch logical hash; cancellation row hash; reservation sequence/unit hash/row hash | null |
| `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` | snapshot fields; authorization/request identity; authorization batch logical hash; activation row hash; validation entries logical hash | null except selected validation hash remains null at activation |

For capture snapshot fields, `capture_snapshot_claim_semantic_sha256` resolves the exact §5.5.2 claim. Its `ordered_relation_logical_sha256` equals `capture_ordered_relation_logical_sha256`, and coverage state/boundary are typed-equal. No physical partition/manifest hash is an intent identity input.

### 17.5 `fence_event_v23` and `fence_unit_manifest_v23`

`fence_event_v23` exact field order:

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
payload_intent_semantic_sha256              nullable SHA256
payload_fence_sequence                      nullable UINT64
payload_fence_unit_file_sha256              nullable SHA256
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

`fence_unit_manifest_v23` exact field order:

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

Total event matrix:

| Unit kind | Bound event/file/semantic triple | Payload-intent semantic field | Snapshot semantic/physical fields | Reservation triple | Cancellation hash | Activation hash | Validation array/hash | Payload ref/release |
|---|---|---|---|---|---|---|---|---|
| `FENCE_ACQUIRED` | all non-null; event kind equals intent payload kind; intent file is bundled and validates | null | all null | all null | null | null | both null | all null |
| each payload kind | all non-null and exactly equal to the acquisition triple; `bound_payload_event_kind=event_kind` | non-null and equal to bound semantic digest | exact §17.4 branch fields; snapshot fields only for three snapshot-bearing payloads | only cancellation: all non-null | only cancellation non-null | only continuation activation non-null | only continuation activation both non-null | all null |
| `FENCE_RELEASED` | all null | null | all null | all null | null | null | both null | payload sequence/hash and release outcome non-null |

For the three snapshot-bearing payloads, the semantic snapshot pair `(snapshot_claim_semantic_sha256,capture_ordered_relation_logical_sha256)` is non-null and resolves to the exact promoted capture snapshot. The existing physical snapshot triple `(capture_snapshot_sequence,capture_snapshot_manifest_file_sha256,snapshot_publication_commit_file_sha256)` is also all non-null. Partial semantic or physical groups are invalid.

For cancellation, the reservation triple `(reservation_fence_sequence,reservation_fence_unit_file_sha256,reservation_event_row_sha256)` is all non-null and resolves exactly as previously accepted; for every other event it is all null.

The acquisition's intent file hash is SHA-256 of exact canonical intent bytes; its semantic hash recomputes from §17.4. The payload unit directly persists the acquisition's exact bound event/file/semantic triple, reopens that exact acquisition directory, verifies the intent file and sidecar, recomputes the semantic hash, and requires both bound and payload-intent semantic fields to equal it. A caller-supplied digest without the intent bytes is invalid.

The manifest's claim-semantic projection is exactly §5.5.3. Physical row-batch and snapshot file hashes remain evidence fields but do not replace their logical semantic bindings.

### 17.6 Atomic fence-unit commit, contention, and bound-payload exclusivity

Every fence sequence is one atomic directory containing the exact manifest/event pairs and §5.2 conditional objects. The directory rename is the sole commit point.

A canonical acquisition winner includes the exact immutable payload intent. A losing acquisition candidate is adoptable only if claim scope, fence claim semantics, and intent canonical bytes are equal. Different bound intents at the same canonical acquisition sequence are a genuine fence semantic conflict, not a legitimate loser.

Only the intent bound at acquisition `A` may occupy sequence `A+1`. A payload unit must prove:

1. `fence_sequence=A+1`;
2. event kind equals `bound_payload_event_kind`;
3. its recomputed payload intent digest equals the acquisition digest;
4. all actual logical row/snapshot/validation hashes and identities equal the intent;
5. predecessor is the exact acquisition manifest file hash; and
6. no other payload/release already occupies `A+1`.

A semantically equal no-replace loser may be superseded under §5.7. Incompatible canonical units, different semantic bytes under one fence identity, invalid target bytes, missing intent/source bytes, or a payload that differs from the bound intent trigger `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, with `STOP_SEMANTIC_ID_COLLISION` taking precedence only for its exact condition.

Unsupported or failed fence-directory promotion maps to `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, not a V10 stop.

### 17.7 Closed fence transitions

Let `A` be a committed acquisition. Permitted forms are exactly:

```text
A:   FENCE_ACQUIRED with one exact bound payload intent
A+1: FENCE_RELEASED with ABORTED_NO_OUTPUT and no payload
```

or:

```text
A:   FENCE_ACQUIRED with one exact bound payload intent
A+1: exactly the bound payload event
A+2: FENCE_RELEASED with COMMITTED
```

The release references the exact payload sequence and canonical payload manifest hash. No nested acquisition, different payload, second payload, gap, token/epoch change, later proof-relevant commit, or new acquisition may intervene. An acquisition or payload without release is a durable open fence.

### 17.8 Payload cardinality and capture snapshot promotion under fence

| Payload | Required evidence | Prohibited co-members |
|---|---|---|
| `AUTHORIZATION_USE_EVENT_COMMITTED` | exact bound intent and one authorization row batch/row | capture rows/snapshot |
| `REQUEST_RESERVED_COMMITTED` | exact bound intent and one reservation row | capture rows/snapshot/cancellation/activation |
| `CAPTURE_STARTED_COMMITTED` | exact bound intent and one STARTED row | terminal/auth row |
| `CAPTURE_TERMINAL_COMMITTED` | exact bound intent and one terminal row | STARTED/auth row |
| `CAPTURE_SNAPSHOT_COMMITTED` | exact bound intent and one semantic+physical snapshot binding | every row batch |
| `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED` | exact bound intent, snapshot binding, reservation triple, one cancellation row | capture rows/activation |
| `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` | exact bound intent, snapshot binding, one activation row, complete validation array/hash | capture rows/reservation/cancellation |

For every snapshot-bearing payload:

1. exact snapshot claim and all prepared snapshot source bytes may exist before acquisition;
2. acquisition commits the exact payload-intent bytes/hash that name snapshot sequence, claim-semantic hash, ordered capture relation hash, coverage state/boundary, and relevant authorization/reservation identity;
3. no canonical capture history directory is promoted before acquisition;
4. under the same open fence, reconstruct the authoritative prefix and validate exact equality with the bound claim;
5. under that fence, promote/adopt only the history directory matching the bound claim;
6. commit at `A+1` only the payload matching the bound intent; and
7. commit the matching release.

A crash after promotion but before payload leaves a recoverable binding only if the same open acquisition, exact intent file, exact prepared sources, and exact promoted directory all validate. Recovery cannot substitute another snapshot, event kind, row hash, validation set, or authorization identity. Otherwise preserve evidence and stop under `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` or the applicable capture snapshot stop by §22 precedence.

### 17.9 Capture launch ordering

Process creation is permitted only after:

1. one canonical `CAPTURE_STARTED_COMMITTED` unit exactly matching the acquisition-bound STARTED intent;
2. the immediately following canonical `FENCE_RELEASED(COMMITTED)` unit;
3. release binding to the STARTED payload sequence and canonical manifest hash; and
4. reconciliation of request/reservation/attempt/effective-argv fields.

Transient, prepared, or promoted-but-uncommitted STARTED bytes grant no permission. A STARTED payload without durable release grants no permission. Terminal evidence requires a later acquisition with a different terminal intent and later payload/release. STARTED and terminal cannot share a prepared unit, fence sequence, payload, batch, or release.

### 17.10 Fence recovery classification

| Durable state | Classification | Exact handling |
|---|---|---|
| acquisition and exact intent committed; no payload | `OPEN_FENCE_BOUND_INTENT_NO_OUTPUT` | either commit exactly bound payload or exact aborted release if no canonical output was promoted |
| exact payload prepared; canonical payload absent | `BOUND_PAYLOAD_PREPARED_RECOVERABLE` | verify intent equality then commit/adopt exact payload |
| canonical payload committed; release absent | `RELEASE_PENDING_RECOVERABLE` | commit exact release |
| STARTED payload committed; release absent | `STARTED_RELEASE_PENDING_NO_LAUNCH` | release before any process creation |
| exact capture history promoted under current open acquisition; binding absent | `CAPTURE_BINDING_PENDING_RECOVERABLE` | commit exact bound payload then release |
| valid canonical winner and equal candidate | `SUPERSEDED_BY_CANONICAL_WINNER` | adopt winner; inventory committed loser |
| missing/wrong intent bytes, different candidate payload, incompatible canonical unit, semantic conflict, wrong token/epoch, or missing recovery bytes | `FENCE_CONFLICT` | authorization/capture stop; preserve evidence |

An aborted release is prohibited after any canonical history directory or row-containing payload target named by the bound intent has been promoted. No stale-residue classification is permitted, and recovery never substitutes a different intent.

## 18. Reservation cancellation proof

### 18.1 Exact interval boundaries

Let:

- `R` be the fence payload sequence committing the exact `REQUEST_RESERVED` row;
- `A` be the later cancellation `FENCE_ACQUIRED` sequence;
- `C=A+1` be `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED`;
- `D=A+2` be the matching `FENCE_RELEASED(COMMITTED)`.

Require:

```text
R < A < C < D
A >= 1
covered_through_fence_sequence = A - 1
```

Cancellation at first acquisition `A=0` is impossible because no prior reservation sequence can satisfy `R<A`.

The proof interval is `(R,C]`. The checkpoint relation covers all committed capture row batches through `A-1`. The exclusive fence permits no competing payload between acquisition and cancellation payload.

### 18.2 Reservation-before-checkpoint witness

The cancellation payload directly persists and binds in `FENCE_UNIT.json`:

```text
reservation_fence_sequence
reservation_fence_unit_file_sha256
reservation_event_row_sha256
```

The row batch and row resolve to the same run, authorization, authorized request set, reservation, request, execution ordinal, and attempt as the cancellation row. The chain proves reservation commit precedes checkpoint without timestamps.

### 18.3 Complete capture relation at checkpoint

Construct authoritative capture relation `CapturePrefix(A)` from every valid committed `capture_events` row batch in fence payload units with sequence `<=A-1`.

The capture snapshot bound by `C` must:

- have `covered_through_fence_sequence=A-1`;
- reconstruct exactly `CapturePrefix(A)`;
- contain no missing, extra, duplicate, malformed, or differently hashed row;
- validate against its own manifest entries and immutable partitions;
- be a valid successor/checkpoint of the previous committed capture snapshot;
- have its promoted history bundle and publication marker bound by the cancellation fence unit.

Current aliases, aggregate-view files, directory listings, summary counts, and timestamps are not substitutes for row-batch reconstruction.

### 18.4 No capture commit before cancellation

Because `C` is the sole payload immediately after acquisition `A`, and every capture row requires a committed fence payload, no capture row can commit between the coverage boundary `A-1` and cancellation commit `C`.

The cancellation row and checkpoint reference commit atomically as members/references of the same fence-unit directory. A promoted capture snapshot without the fence unit remains pending and cannot prove cancellation.

### 18.5 Independently derived zero counts

Filter `CapturePrefix(A)` by exact typed equality on:

```text
run_id
authorization_id
authorization_record_file_sha256
authorized_request_set_file_sha256
reservation_id
request_id
execution_ordinal
attempt_number
```

Derive:

```text
derived_started = count(capture_event_state=STARTED and capture_event_ordinal=0)
derived_terminal = count(capture_event_state in {INTERRUPTED,COMPLETED} and capture_event_ordinal=1)
```

Every matching row must first satisfy the closed capture schema and physical row-batch provenance.

Positive proof requires:

```text
derived_started = 0
stored capture_started_row_count = 0
derived_terminal = 0
stored terminal_capture_row_count = 0
reservation_irrevocably_closed = true
old_authorization_reservation_usable = false
reason_code = POSITIVE_PROOF_NO_START
reservation_start_proof_state = POSITIVE_PROOF_NO_START
```

Stored zeroes are reconciliation assertions, not evidence.

### 18.6 No-launch conclusion

The accepted rule remains that process creation is permitted only after a committed STARTED payload and its durable COMMITTED release. Complete checkpoint coverage plus `derived_started=0` proves no permitted launch for the old reservation through cancellation.

---

## 19. Derived unproven result and contradictory immutable rows

### 19.1 Persisted enum behavior

The accepted `reservation_start_proof_state` enum remains unchanged. State-specific reachability is:

- `NOT_APPLICABLE` for states that do not carry start proof;
- `START_EVIDENCE_PRESENT` for start-confirmed, start-ambiguous, or terminal states as already accepted;
- `POSITIVE_PROOF_NO_START` only for a valid committed cancellation row;
- `RESERVATION_START_STATUS_UNPROVEN` is prohibited in every persisted authorization-use row.

Encountering the defensive lexeme in a persisted row is `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`.

### 19.2 Derived validation result

Validators derive, but do not persist in `reservation_start_proof_state`:

```text
reservation_start_validation_result ∈
  {PROVEN_NO_START, START_EVIDENCE_PRESENT, RESERVATION_START_STATUS_UNPROVEN}
```

Any failed positive-proof conjunct yields derived `RESERVATION_START_STATUS_UNPROVEN` and `continuation_eligible=false`.

### 19.3 Before a cancellation row exists

If proof is omitted, stale, partial, unreadable, forked, cyclic, physically unbound, contradictory, nonzero, or unrecoverable:

- no cancellation row commits;
- last valid state remains `REQUEST_RESERVED`;
- stored proof state remains its existing non-proof value;
- derived result is `RESERVATION_START_STATUS_UNPROVEN`;
- the applicable structural stop precedes `STOP_RESERVATION_NO_START_PROOF_INVALID`;
- request is not CONTINUATION-eligible.

### 19.4 After an immutable contradictory cancellation row exists

If later validation finds a contradiction:

- retain the immutable cancellation row with stored `POSITIVE_PROOF_NO_START`;
- derive `RESERVATION_START_STATUS_UNPROVEN` for current validation;
- emit the first applicable structural/proof stop;
- invalidate any continuation activation or eligibility based on it;
- commit no further reservation under the affected continuation authorization;
- emit no empirical replay label;
- preserve the contradictory row, its row batch, fence unit, snapshot, and prepared sources in the terminal inventory.

The row is contradictory evidence; it is never mutated or silently ignored.

### 19.5 Closed unproven causes

Unproven includes: missing/unresolved prepared source; invalid atomic directory; wrong run/family; stale or pre-reservation checkpoint; partial publication; fork, duplicate, gap, rollback, cycle, or out-of-order chain; invalid partition/index; missing row batch; aggregate-only row; open/conflicting fence; STARTED without release; incomplete checkpoint relation; nonzero derived count; stored/derived mismatch; tuple/hash mismatch; later matching old-reservation row; or incorrect closure/usability booleans.

---

## 20. CONTINUATION freshness

### 20.1 Authorization identity remains unchanged

The existing CONTINUATION authorized-request-set and authorization-ID construction remain unchanged. No new field enters either semantic identity. Freshness is bound in fence-unit evidence.

### 20.2 `capture_fence_continuation_entry_v23`

Each validation entry has exact field order:

```text
request_id                                      STRING
execution_ordinal                               UINT16
validation_basis                                STRING {CANCELLED_NO_START, NEVER_RESERVED_NEVER_STARTED}
source_authorization_id                         nullable STRING
source_reservation_id                           nullable STRING
source_attempt_number                           nullable UINT32
source_cancellation_event_row_sha256            nullable SHA256
source_cancellation_fence_unit_file_sha256      nullable SHA256
source_capture_snapshot_manifest_file_sha256    nullable SHA256
validation_capture_snapshot_manifest_file_sha256 SHA256
validation_covered_through_fence_sequence       nullable UINT64
derived_started_row_count                       UINT64 = 0
derived_terminal_row_count                      UINT64 = 0
continuation_eligible                           BOOL = true
continuation_validation_entry_sha256            SHA256
```

The row hash excludes only its destination field and uses the listed projection. Entries are ordered by execution ordinal and request ID. The array logical hash is LF-joined entry bytes with no trailing LF.

For `CANCELLED_NO_START`, all source fields are non-null and resolve exactly to the prior cancellation row, fence unit, and capture snapshot. For `NEVER_RESERVED_NEVER_STARTED`, all source fields are null. Null/non-null mixing is invalid.

### 20.3 Fenced activation

Before CONTINUATION activation:

1. validate authorization record and request set;
2. acquire a new exclusive capture fence at `A2`;
3. derive the committed prefix boundary as null only for `A2=0`, otherwise `A2-1`;
4. build and commit a fresh capture checkpoint from all committed row batches through that boundary;
5. validate every request-set entry and construct the exact complete ordered validation array;
6. commit one `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` payload at `A2+1`, containing the checkpoint binding, array/logical hash, and exactly one `ACTIVATED` row;
7. commit `FENCE_RELEASED(COMMITTED)` at `A2+2`.

Activation is valid only after the release is durable. Prepared or payload-only activation is not active.

### 20.4 Cancelled-reservation entries

For `CANCELLED_NO_START`, require the exact prior cancellation row batch, cancellation fence unit, cancellation snapshot, currently valid original proof, fresh zero matching STARTED/terminal rows, no later old-reservation capture row, and closed/unusable old reservation.

### 20.5 Never-reserved entries

For `NEVER_RESERVED_NEVER_STARTED`, require the complete committed authorization-use row-batch prefix to contain no reservation for that request under relevant prior authorizations, and the fresh capture checkpoint to contain no capture row for the claimed attempt.

### 20.6 Validation before each continuation reservation

Before committing `REQUEST_RESERVED` under a CONTINUATION authorization:

1. acquire a new exclusive fence at `A3`;
2. derive complete authorization/capture row-batch prefixes through `covered_through_fence_sequence` (`A3-1`; null is impossible for a valid CONTINUATION reservation);
3. validate the activation payload and its COMMITTED release;
4. revalidate the selected request's exact activation entry against the fresh prefixes;
5. require no matching old-reservation capture row, no new reservation for a `NEVER_RESERVED` basis, and no contradictory cancellation;
6. commit the new `REQUEST_RESERVED` row at `A3+1` with exactly one selected validation-entry hash bound in `FENCE_UNIT.json`;
7. commit `FENCE_RELEASED(COMMITTED)` at `A3+2`.

No fork, cycle, missing row batch, stale aggregate-only claim, or open/conflicting fence may exist. A contradiction blocks reservation before commit. The external authorization record remains immutable but unusable.

## 21. Replay finalization, clean-stop finalization, and conflict-stop finalization

### 21.1 Terminal profiles are mutually exclusive

Exactly one terminal profile may exist:

1. `FINALIZED_REPLAY` — one valid `finalization/REPLAY_FINALIZED.json`;
2. `FINALIZED_STOP_CLEAN` — one valid `finalization/STOP_FINALIZED.json`;
3. `FINALIZED_CONFLICT_STOP` — one valid `CONFLICT_STOP_FINALIZED/` directory, with neither normal marker.

Both marker families existing is `STOP_FINALIZATION_INVENTORY_INVALID` and yields no valid terminal profile. Here the two marker families are the normal-marker family and the conflict-stop directory family. Within the normal-marker family, both normal markers existing is the same stop.

### 21.2 Replay and clean-stop preconditions and commit protocol

Replay or clean-stop finalization requires:

- every snapshot and fence chain valid and cycle-free;
- every committed prepared candidate selected or validly `SUPERSEDED_BY_CANONICAL_WINNER`;
- no unresolved prepared claim, promoted unbound capture history, open fence, conflicting canonical target, or semantic collision;
- every superseded committed prepared unit fully retained and inventoried;
- current views and aggregate views equal committed sources; and
- complete normal final inventory closure.

A legitimate superseded loser does not block finalization. An unvalidated loser, missing canonical winner, or unresolved semantic claim does.

Normal V10 publication remains marker-last: persist the exact §5.4 claim scope and §5.5.4 normal-finalization claim semantics, prepare exact inventory and marker bytes, commit the immutable prepared source, atomically commit the inventory target, revalidate, then atomically commit the marker target as the sole normal terminal point. Registered sidecars are deterministic post-target derivatives or bundled members under §3.5. `STOP_FINALIZATION_ATOMICITY_UNSUPPORTED` and `STOP_FINALIZATION_ATOMICITY_FAILURE` apply only to these V10 terminal inventory/marker operations or the V10 conflict-directory operation.

### 21.3 Conflict-stop trigger

Conflict-stop finalization is required only when the run must terminate while preserving an unresolved structural conflict, including:

- incompatible canonical snapshot/fence claims;
- different semantic bytes under one semantic identity;
- an unrecoverable open fence;
- a committed candidate that cannot be validated as selected or `SUPERSEDED_BY_CANONICAL_WINNER`;
- contradictory immutable cancellation/activation evidence;
- unrecoverable publication residue after the applicable family or authorization/capture stop; or
- V10 terminal publication conflict.

A valid no-replace winner plus semantically equivalent loser is not a conflict. A recoverable ordinary interruption remains recovery-required and is not conflict-finalized absent separate authority.

### 21.4 `conflict_stop_inventory_v23` and terminal bundle

#### 21.4.1 Governing `REV23_STOP_CODE` type and top-level inventory schema

`REV23_STOP_CODE` is the following exact closed enum, synchronized with the effective schema registry; no unregistered string is permitted:

```text
STOP_CANONICAL_INPUT_MISSING
STOP_SOURCE_B_SCHEMA_INVALID
STOP_SOURCE_B_COUNT_INVALID
STOP_SOURCE_B_OVERLAP_INVALID
STOP_SOURCE_B_REASON_INVALID
STOP_SOURCE_B_NORMALIZATION_INVALID
STOP_SOURCE_D_INPUT_INVALID
STOP_SOURCE_D_P0_INVALID
STOP_SOURCE_D_CONTRACT_INVALID
STOP_SOURCE_D_RESOLUTION_INVALID
STOP_SOURCE_D_TRADE_TIMESTAMP_INVALID
STOP_SOURCE_D_PRECISION_LOSS
STOP_SOURCE_D_TOKEN_ENUMERATION_UNRELIABLE
STOP_SOURCE_D_SAMPLE_INVALID
STOP_SOURCE_D_OUTPUT_COUNT_INVALID
STOP_SOURCE_D_ISOLATION_INVALID
STOP_SOURCE_D_PROVENANCE_INVALID
STOP_SOURCE_D_SOURCE_B_ORDER_INVALID
STOP_SOURCE_B_SOURCE_D_RECONCILIATION_INVALID
STOP_MANIFEST_COUNT_OR_HASH_INVALID
STOP_REQUEST_EXECUTION_ORDER_INVALID
STOP_ENDPOINT_SHAPE_EVIDENCE_INVALID
STOP_ACCEPTED_FIDELITY_UNRESOLVED
STOP_POLICY_OBSERVATION_INVALID
STOP_POLICY_RESOLUTION_INVALID
STOP_POLICY_NOT_ESTABLISHED
STOP_URL_POLICY_INVALID
STOP_TRANSPORT_POLICY_INVALID
STOP_CURL_SUBPROCESS_CONTRACT_INVALID
STOP_TOKEN_NOT_FOUND_REGISTRY_INVALID
STOP_REQUEST_PLAN_INVALID
STOP_RESPONSE_HEADER_EXTRACTION_CONTRACT_INVALID
STOP_REQUESTS_JSON_EQUIVALENCE_CONTRACT_INVALID
STOP_CURL_PROVENANCE_INVALID
STOP_HTTP_PROTOCOL_POLICY_VIOLATION
STOP_FINGERPRINT_INVALID
STOP_PRE_V7_FREEZE_INVALID
STOP_NETWORK_AUTHORIZATION_INVALID
STOP_AUTHORIZATION_USE_CONFLICT
STOP_CAPTURE_EVENT_SCHEMA_INVALID
STOP_CAPTURE_ATTEMPT_RECONCILIATION_INVALID
STOP_CAPTURE_SNAPSHOT_INVALID
STOP_REQUEST_DISPOSITION_INVALID
STOP_REQUEST_POPULATION_INCOMPLETE
STOP_ANALYSIS_SCHEMA_INVALID
STOP_ANALYSIS_CAPTURE_RECONCILIATION_INVALID
STOP_ANALYSIS_SNAPSHOT_INVALID
STOP_PAIR_RECONCILIATION_INVALID
STOP_ALL_ONE_VECTOR_STRUCTURAL_INVALID
STOP_THRESHOLD_RECONCILIATION_INVALID
STOP_RESULT_LOGIC_INVALID
STOP_ROW_HASH_PROJECTION_INVALID
STOP_LOGICAL_HASH_MISMATCH
STOP_SEMANTIC_ID_COLLISION
STOP_SCHEMA_REGISTRY_USAGE_INVALID
STOP_FINALIZATION_INVENTORY_INVALID
STOP_FINALIZATION_ATOMICITY_UNSUPPORTED
STOP_FINALIZATION_ATOMICITY_FAILURE
STOP_GOVERNING_PACKAGE_MANIFEST_INVALID
STOP_PRE_RUN_ID_COLLISION
STOP_DETACHED_PRE_RUN_ATTACHMENT_INVALID
STOP_RUN_ESTABLISHMENT_FAILED
STOP_AUTHORIZATION_NAMESPACE_INVALID
STOP_AUTHORIZATION_REQUEST_SET_CROSS_FILE_INVALID
STOP_AUTHORIZED_REQUEST_SET_INVALID
STOP_RESERVATION_NO_START_PROOF_INVALID
STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED
STOP_EFFECTIVE_ARGV_MISMATCH
STOP_HTTP_WRITEOUT_INVALID
STOP_HTTP_STATUS_EVIDENCE_MISMATCH
STOP_SCHEMA_RECONCILIATION_FAILED
```

`CONFLICT_INVENTORY.json` exact field order:

```text
schema_version                          STRING = local_curl_conflict_stop_inventory.v23
spec_revision                           UINT16 = 23
run_id                                  STRING /^run_[0-9a-f]{64}$/
accepted_contract_manifest_file_sha256  SHA256
governing_schema_registry_file_sha256   SHA256
primary_stop_code                       REV23_STOP_CODE
conflict_groups                         ARRAY[conflict_group_v23]
conflict_group_count                    UINT64
conflict_groups_logical_sha256          SHA256
entries                                 ARRAY[conflict_inventory_entry_v23]
entry_count                             UINT64
entries_logical_sha256                  SHA256
excluded_self_paths                     STRING_LIST
excluded_self_paths_logical_sha256      SHA256
inventory_logical_sha256                SHA256
```

The two governing hashes equal the accepted baseline in §2.3. `conflict_group_count=len(conflict_groups)` and `entry_count=len(entries)`; these stored counts are independently reconciled and are not claim-scope inputs.

`primary_stop_code` is derived, never caller-selected. It is the first still-applicable unresolved stop by §22.2 precedence. When two detected stops occupy the same precedence rank, choose the one appearing earlier in the exact `REV23_STOP_CODE` enum order above. A valid superseded candidate contributes no stop. A V10 publication failure cannot be recorded in a successfully committed conflict inventory because that inventory/marker did not commit; it remains preserved unfinalized residue under §21.5.

#### 21.4.2 Complete owner/schema metadata

Every durable accepted-contract artifact is representable without enumerating all role lexemes by binding its exact registered owner. `owner_kind` is closed to:

```text
GOVERNING_PACKAGE_ENTRY
SCHEMA_ARTIFACT_CATALOG_ENTRY
DETACHED_PRE_RUN_ATTACHMENT_ENTRY
PREPARED_PLAN_OBJECT
SNAPSHOT_HISTORY_OBJECT
SNAPSHOT_CURRENT_VIEW_OBJECT
FENCE_UNIT_OBJECT
AUTHORIZATION_USE_RELATION_VERSION
CAPTURE_RELATION_VERSION
NORMAL_FINALIZATION_OBJECT
CONFLICT_FINALIZATION_OBJECT
UNREGISTERED_DURABLE_OBJECT
```

Path roots are exactly:

```text
ACCEPTED_CONTRACT_ROOT
PRE_RUN_ROOT
RUN_ROOT
```

The discovery set is closed and exhaustive. Before classification, construct the set union below and normalize every path under §5.1:

1. every package path in the accepted governing-package manifest under `ACCEPTED_CONTRACT_ROOT`;
2. every accepted schema-registry artifact-catalog target and every registered retained-contract/policy target under its registered root;
3. every detached pre-run attachment manifest entry and detached pre-run inventory target under `PRE_RUN_ROOT`;
4. every prepared unit structural member, prepared source object, and registered canonical target reachable from a valid or unresolved immutable preparation plan under `PRE_RUN_ROOT` or `RUN_ROOT` as registered;
5. every object referenced by every snapshot history sequence, every current generation, every legacy/current aggregate view, every fence unit, every authorization-use/capture row batch, and every relation-version/aggregate-view catalog entry under `RUN_ROOT`;
6. every normal-finalization prepared object, residue, inventory, sidecar, and marker target under `RUN_ROOT`;
7. every physically present regular file, symlink, non-regular filesystem object, or directory entry below the three roots that is not already claimed by items 1–6, represented as `UNREGISTERED_DURABLE_OBJECT`; and
8. the four fixed conflict-terminal self paths, which are the only paths omitted from `entries[]` and appear exactly in `excluded_self_paths` under §21.4.7.

Discovery is by registered inventories/catalogs plus a complete root walk for unregistered residue; absence from a current alias, latest manifest, or aggregate view does not remove a historical or prepared object from the set. Every discovered `(path_root,path)` is accounted for exactly once after §21.4.4 duplicate reconciliation. A durable path outside this union is impossible by construction; an unwalkable root or incomplete traversal is `STOP_FINALIZATION_INVENTORY_INVALID` and conflict finalization cannot commit.

Every registered entry carries:

```text
owner_kind
owner_registry_path
owner_registry_file_sha256
owner_entry_key
owner_entry_logical_sha256
content_schema_id
registered_object_role
conflict_inventory_role_class
```

`owner_registry_path` is encoded exactly as `<PATH_ROOT>:<normalized-relative-path>` and points to the immutable owner file. For `UNREGISTERED_DURABLE_OBJECT`, the four owner-registry fields are null, `content_schema_id="opaque:unregistered"`, `registered_object_role="UNREGISTERED_DURABLE_OBJECT"`, and `conflict_inventory_role_class=UNREGISTERED`. For every other owner kind, all owner-registry fields are non-null and resolve to exact immutable bytes and one unique owner entry. Missing or unreadable target bytes never erase or replace owner metadata; they preserve the expected registered role/schema and owner entry.

Every registered owner entry also persists one `conflict_inventory_role_class` from the §21.4.3 role-class domain. The inventory entry's `role_class` must equal it, except a `PREPARED_PLAN_OBJECT` is deterministically refined to `PREPARED_SELECTED` or `PREPARED_SUPERSEDED` after disposition validation; an unresolved prepared object retains registered `RECOVERY_SOURCE`. No caller-selected role class is accepted.

Owner selection is deterministic. Collect every registered claim for the normalized target path. Select the first claim in this precedence order:

```text
CONFLICT_FINALIZATION_OBJECT
NORMAL_FINALIZATION_OBJECT
FENCE_UNIT_OBJECT
AUTHORIZATION_USE_RELATION_VERSION
CAPTURE_RELATION_VERSION
SNAPSHOT_CURRENT_VIEW_OBJECT
SNAPSHOT_HISTORY_OBJECT
DETACHED_PRE_RUN_ATTACHMENT_ENTRY
GOVERNING_PACKAGE_ENTRY
SCHEMA_ARTIFACT_CATALOG_ENTRY
PREPARED_PLAN_OBJECT
UNREGISTERED_DURABLE_OBJECT
```

A more specific immutable runtime owner therefore governs over a generic catalog template, while a prepared plan remains the owner of its private prepared-source path and a secondary provenance claim for a reused canonical target. All claims for one path must agree on normalized target path, `content_schema_id`, and `registered_object_role`. Different expected physical hashes are permitted only where §5.3/§5.7 independently proves equal logical semantics and canonical-winner adoption; a secondary `PREPARED_PLAN_OBJECT` may retain `RECOVERY_SOURCE` while the selected canonical owner has its registered canonical/derived/terminal role class. Every other role-class or semantic-identity disagreement is contradictory owner metadata.

If claims contradict, the top-level owner fields retain the first claim by the fixed order solely for deterministic encoding; they do not validate or suppress the contradiction. The conflict group must include the target path entry and the inventory entry for every non-null `owner_registry_path` participating in the contradiction. Thus all claimant owner bytes, or their missing/unreadable classifications and expected hashes, remain physically represented without creating a second row for the target path.

If the selected owner registry is missing or unreadable, its expected path, file hash, entry key, entry logical hash, schema, role, and role class must remain derivable from an independently readable parent owner or prepared plan. Otherwise classification is `CONTRADICTORY_OWNER_METADATA` plus the applicable missing/unreadable recovery-source group; the validator may not replace the missing owner's metadata with an unregistered role.

Owner sources are exact:

| Owner kind | Authoritative owner entry |
|---|---|
| `GOVERNING_PACKAGE_ENTRY` | exact entry in accepted `GOVERNING_PACKAGE_MANIFEST_REV23.json` |
| `SCHEMA_ARTIFACT_CATALOG_ENTRY` | exact artifact-catalog/schema-binding entry in accepted `SCHEMA_REGISTRY_REV23.json`, including registered conflict-inventory role class |
| `DETACHED_PRE_RUN_ATTACHMENT_ENTRY` | exact detached attachment manifest entry bound into `run_id` |
| `PREPARED_PLAN_OBJECT` | exact planned-object tuple in immutable `PREPARATION_PLAN.json` |
| `SNAPSHOT_HISTORY_OBJECT` | exact history manifest/publication-marker entry or partition entry for one sequence |
| `SNAPSHOT_CURRENT_VIEW_OBJECT` | exact unique-head current-generation commit entry |
| `FENCE_UNIT_OBJECT` | exact object/event/batch entry in one immutable fence manifest |
| `AUTHORIZATION_USE_RELATION_VERSION` | exact authorization batch descriptor in one fence unit |
| `CAPTURE_RELATION_VERSION` | exact capture batch descriptor in one fence unit |
| `NORMAL_FINALIZATION_OBJECT` | exact normal-finalization prepared-plan object |
| `CONFLICT_FINALIZATION_OBJECT` | fixed schema/path registration in this §21.4; self paths remain excluded from inventory rows |

`owner_entry_key` has this exact owner-specific form:

| Owner kind | Exact `owner_entry_key` |
|---|---|
| `GOVERNING_PACKAGE_ENTRY` | accepted package path |
| `SCHEMA_ARTIFACT_CATALOG_ENTRY` | exact schema-registry artifact path template |
| `DETACHED_PRE_RUN_ATTACHMENT_ENTRY` | exact attachment-relative path |
| `PREPARED_PLAN_OBJECT` | `object_ordinal_10d` |
| `SNAPSHOT_HISTORY_OBJECT` | `snapshot_sequence_20d + ":" + registered_object_role + ":" + optional partition_ordinal_10d` |
| `SNAPSHOT_CURRENT_VIEW_OBJECT` | `snapshot_sequence_20d + ":" + registered_object_role` |
| `FENCE_UNIT_OBJECT` | `fence_sequence_20d + ":" + registered_object_role + ":" + optional batch_ordinal_10d` |
| `AUTHORIZATION_USE_RELATION_VERSION` | `fence_sequence_20d + ":authorization_use_events"` |
| `CAPTURE_RELATION_VERSION` | `fence_sequence_20d + ":capture_events"` |
| `NORMAL_FINALIZATION_OBJECT` | exact prepared object role |
| `CONFLICT_FINALIZATION_OBJECT` | exact fixed conflict-bundle relative path |

`owner_entry_logical_sha256` hashes the exact canonical typed owner-entry projection registered for that owner. It is not the target file hash. Any owner key that does not match this table is contradictory metadata.

#### 21.4.3 Entry schema

Each `conflict_inventory_entry_v23` exact field order:

```text
path_root                            STRING
path                                 STRING
owner_kind                           STRING
owner_registry_path                  nullable STRING
owner_registry_file_sha256           nullable SHA256
owner_entry_key                      nullable STRING
owner_entry_logical_sha256           nullable SHA256
content_schema_id                    STRING
registered_object_role               STRING
role_class                           STRING
observation_state                    STRING
classification                       STRING
size_bytes                           nullable UINT64
file_sha256                          nullable SHA256
logical_sha256                       nullable SHA256
read_error_code                      nullable STRING
prepared_unit_id                     nullable STRING /^prep_[0-9a-f]{64}$/
claim_scope_sha256                    nullable SHA256
committed_sequence                   nullable UINT64
conflict_group_ids                   STRING_LIST
conflict_group_ids_logical_sha256    SHA256
```

`path` is normalized relative to `path_root` under §5.1 path rules. The key `(path_root,path)` is unique. Entries are ordered first by path-root enum order shown above, then unsigned UTF-8 `path` bytes.

`role_class` is typed-equal to the owner's `conflict_inventory_role_class`, subject only to the prepared disposition refinement above. It is closed to:

```text
CANONICAL_REQUIRED
DERIVED_REQUIRED
PREPARED_SELECTED
PREPARED_SUPERSEDED
RECOVERY_SOURCE
TERMINAL_EVIDENCE
CONTEXT_ONLY
UNREGISTERED
```

`observation_state` is closed to:

```text
PRESENT_VALID
PRESENT_INVALID
PRESENT_PENDING_OPEN_FENCE
PRESENT_FINALIZATION_RESIDUE
EXPECTED_MISSING
EXPECTED_UNREADABLE
UNREGISTERED_PRESENT
```

`classification` is closed to:

```text
CANONICAL_COMMITTED
DERIVED_VIEW_VALID
SELECTED_PREPARED_WINNER
SUPERSEDED_BY_CANONICAL_WINNER
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

`read_error_code`, when non-null, is exactly one of:

```text
PATH_NOT_FOUND
PERMISSION_DENIED
SYMLINK_FORBIDDEN
NON_REGULAR_FILE
IS_DIRECTORY
SIZE_READ_FAILED
HASH_READ_FAILED
IO_ERROR
```

#### 21.4.4 Total role/state-to-classification matrix and precedence

For `PRESENT_VALID`, classification is determined by role class:

| Role class | Exact classification |
|---|---|
| `CANONICAL_REQUIRED` | `CANONICAL_COMMITTED` |
| `DERIVED_REQUIRED` | `DERIVED_VIEW_VALID` |
| `PREPARED_SELECTED` | `SELECTED_PREPARED_WINNER` |
| `PREPARED_SUPERSEDED` | `SUPERSEDED_BY_CANONICAL_WINNER` |
| `RECOVERY_SOURCE` | `RECOVERY_SOURCE_VALID` |
| `TERMINAL_EVIDENCE` | `TERMINAL_EVIDENCE_VALID` |
| `CONTEXT_ONLY` | `CONTEXT_VALID` |
| `UNREGISTERED` | invalid combination → `CONTRADICTORY_OWNER_METADATA` |

Every other observation state maps as follows, irrespective of registered role class unless the validity column says otherwise:

| Observation state | Permitted role class | Classification |
|---|---|---|
| `PRESENT_INVALID` | any registered class | `CORRUPT` |
| `PRESENT_PENDING_OPEN_FENCE` | `CANONICAL_REQUIRED`, `RECOVERY_SOURCE`, or `CONTEXT_ONLY` | `PROMOTED_PENDING_UNDER_OPEN_FENCE` |
| `PRESENT_FINALIZATION_RESIDUE` | `TERMINAL_EVIDENCE`, `RECOVERY_SOURCE`, or `CONTEXT_ONLY` | `FINALIZATION_RESIDUE` |
| `EXPECTED_MISSING` | any registered class | `EXPECTED_MISSING` |
| `EXPECTED_UNREADABLE` | any registered class | `UNREADABLE` |
| `UNREGISTERED_PRESENT` | `UNREGISTERED` only | `UNREGISTERED_DURABLE_PATH` |

Any state/role combination not permitted by these two tables is `CONTRADICTORY_OWNER_METADATA`.

Classification precedence for one path is exact:

1. contradictory owner/path metadata;
2. expected missing or unreadable;
3. present but structurally/semantically invalid;
4. unregistered present path;
5. pending-open-fence state;
6. finalization residue;
7. valid role-class classification.

Readable registered regular files have non-null size/file hash and null read error. Missing/unreadable registered paths have null size/file/logical hashes and the exact read error (`PATH_NOT_FOUND` for missing; a non-`PATH_NOT_FOUND` value for unreadable). Present invalid readable regular files retain size/file hash but have null logical hash. `logical_sha256` is non-null exactly when a registered logical projection validates; sidecars and opaque bytes have null logical hash.

For `UNREGISTERED_PRESENT`, nullability is also total: a readable regular unregistered file has non-null size/file hash, null logical hash, and null read error; an unregistered symlink, directory, or other non-regular object has null size/file/logical hashes and respectively `SYMLINK_FORBIDDEN`, `IS_DIRECTORY`, or `NON_REGULAR_FILE`. No unregistered object is treated as semantically valid merely because its bytes are readable.

`prepared_unit_id` and `claim_scope_sha256` are both non-null exactly for a path owned by or selected/superseded from one prepared plan; they must resolve to that plan's exact §5.4 claim. They are both null otherwise. Ambiguous prepared ownership is contradictory metadata.

`committed_sequence` is non-null only for snapshot/fence sequence objects and row batches owned by that sequence. `conflict_group_ids` is sorted unsigned UTF-8, unique, and may be empty for valid context or superseded entries.

Discovery duplicates with identical complete claim metadata collapse before owner selection. Different discoveries for one `(path_root,path)` produce one entry using the fixed owner-selection and classification precedence. For contradictory claims, the deterministic group contains the target entry key plus every participating owner-registry entry key as required by §21.4.2. Duplicate output rows or an owner-registry member absent from `entries[]` are forbidden.

The exact entry logical projection excludes raw `conflict_group_ids` and uses these cells in displayed schema order, replacing the raw list with `conflict_group_ids_logical_sha256`:

```text
path_root STRING
path STRING
owner_kind STRING
owner_registry_path STRING or NULL
owner_registry_file_sha256 SHA256 or NULL
owner_entry_key STRING or NULL
owner_entry_logical_sha256 SHA256 or NULL
content_schema_id STRING
registered_object_role STRING
role_class STRING
observation_state STRING
classification STRING
size_bytes UINT or NULL
file_sha256 SHA256 or NULL
logical_sha256 SHA256 or NULL
read_error_code STRING or NULL
prepared_unit_id STRING or NULL
claim_scope_sha256 SHA256 or NULL
committed_sequence UINT or NULL
conflict_group_ids_logical_sha256 SHA256
```

#### 21.4.5 Recovery-source semantic-scope mapping

Every missing, unreadable, corrupt, or conflicting recovery source maps to one exact semantic scope:

| Owner/role | Semantic scope and identity inputs |
|---|---|
| prepared-plan object or prepared source | `PREPARED_CLAIM_SCOPE`; exact `claim_scope_sha256` from §5.4 |
| partition payload with validated `partition_id` | `SEMANTIC_ID`; `content_schema_id`, `partition_id` |
| snapshot history manifest/index/marker/current generation | `SNAPSHOT_SEQUENCE`; run ID, family, sequence |
| fence manifest/event/intent/row batch/relation version | `FENCE_SEQUENCE`; run ID, fence sequence |
| open acquisition or payload | `OPEN_FENCE`; run ID, acquire sequence, fence token, bound payload-intent semantic hash |
| cancellation/continuation proof evidence | `RESERVATION_PROOF`; run, authorization, reservation, request, attempt |
| normal/conflict terminal object | `FINALIZATION_TARGET`; run ID, terminal marker kind, canonical target path |
| governing package, schema catalog, detached attachment, aggregate/derived view, or other registered runtime artifact | `CANONICAL_TARGET`; path root and canonical path |
| contradictory or unregistered path metadata | `PATH`; path root and path |

No recovery-source group may choose a different scope. A missing prepared source without resolvable `claim_scope_sha256` is additionally contradictory owner metadata.

#### 21.4.6 Conflict groups

`conflict_kind` is exactly:

```text
CANONICAL_TARGET_DIVERGENCE
SEMANTIC_ID_COLLISION
SNAPSHOT_SEQUENCE_FORK
FENCE_SEQUENCE_FORK
PREPARED_CLAIM_DIVERGENCE
RECOVERY_SOURCE_MISSING
OPEN_FENCE_CONFLICT
CANCELLATION_CONTRADICTION
FINALIZATION_TARGET_CONFLICT
PATH_METADATA_CONTRADICTION
```

`semantic_scope` is exactly:

```text
CANONICAL_TARGET
SEMANTIC_ID
SNAPSHOT_SEQUENCE
FENCE_SEQUENCE
PREPARED_CLAIM_SCOPE
OPEN_FENCE
RESERVATION_PROOF
FINALIZATION_TARGET
PATH
```

Each `conflict_group_v23` exact field order:

```text
conflict_group_id                   STRING /^cg_[0-9a-f]{64}$/
conflict_kind                       STRING
semantic_scope                      STRING
semantic_identity                   STRING /^si_[0-9a-f]{64}$/
semantic_identity_cells             ARRAY[typed_cell]
semantic_identity_cells_logical_sha256 SHA256
claim_scope_sha256                  nullable SHA256
canonical_target_path_root          nullable STRING
canonical_target_path               nullable STRING
member_entry_keys                   STRING_LIST
member_entry_keys_logical_sha256    SHA256
```

An entry key is `path_root + ":" + path`. The list is sorted unsigned UTF-8 and unique. `member_entry_keys_logical_sha256` is SHA-256 of LF-joined canonical typed cells `{"n":"member_entry_key","t":"STRING","v":"<entry-key>"}` in that exact order, no trailing LF; the empty list hashes as SHA-256 of empty bytes.

`semantic_identity_cells` is the exact ordered typed-cell array from this table; its list hash is SHA-256 of LF-joined canonical typed-cell bytes, no trailing LF. `semantic_identity = "si_" + lowercase_hex(SHA256(exact canonical typed-row bytes of the same ordered cells))` using:

| Scope | Exact identity cells |
|---|---|
| `CANONICAL_TARGET` | `path_root STRING`, `canonical_target_path STRING` |
| `SEMANTIC_ID` | `content_schema_id STRING`, `registered_semantic_id STRING` |
| `SNAPSHOT_SEQUENCE` | `run_id STRING`, `audit_family STRING`, `snapshot_sequence UINT` |
| `FENCE_SEQUENCE` | `run_id STRING`, `fence_sequence UINT` |
| `PREPARED_CLAIM_SCOPE` | `claim_scope_sha256 SHA256` |
| `OPEN_FENCE` | `run_id STRING`, `acquire_fence_sequence UINT`, `fence_token_sha256 SHA256`, `bound_payload_intent_semantic_sha256 SHA256` |
| `RESERVATION_PROOF` | `run_id STRING`, `authorization_id STRING`, `reservation_id STRING`, `request_id STRING`, `attempt_number UINT` |
| `FINALIZATION_TARGET` | `run_id STRING`, `marker_kind STRING`, `path_root STRING`, `canonical_target_path STRING` |
| `PATH` | `path_root STRING`, `path STRING` |

`claim_scope_sha256` is non-null exactly for `PREPARED_CLAIM_SCOPE`; null otherwise. Canonical target path/root are non-null exactly for `CANONICAL_TARGET` and `FINALIZATION_TARGET`; null otherwise.

Conflict-kind/scope pairing is exact: target divergence→canonical target; semantic collision→semantic ID; snapshot fork→snapshot sequence; fence fork→fence sequence; prepared divergence→prepared claim scope; missing recovery source→the §21.4.5 mapped scope; open fence→open fence; cancellation contradiction→reservation proof; finalization target conflict→finalization target; path metadata contradiction→path.

The exact conflict-group logical projection excludes the two raw arrays and uses these cells in order:

```text
conflict_kind                              STRING
semantic_scope                             STRING
semantic_identity                          STRING
semantic_identity_cells_logical_sha256     SHA256
claim_scope_sha256                         SHA256 or NULL
canonical_target_path_root                 STRING or NULL
canonical_target_path                      STRING or NULL
member_entry_keys_logical_sha256            SHA256
```

`conflict_group_id = "cg_" + lowercase_hex(SHA256(exact canonical typed-row bytes of this projection))`. Groups are ordered by unsigned UTF-8 group ID. Entry references must resolve, and every member key must exist. A validated superseded loser normally has no group.

#### 21.4.7 Inventory ordering, self exclusions, and logical hash

`excluded_self_paths` is exactly this order, with `RUN_ROOT:` prefix:

```text
RUN_ROOT:CONFLICT_STOP_FINALIZED/CONFLICT_INVENTORY.json
RUN_ROOT:CONFLICT_STOP_FINALIZED/CONFLICT_INVENTORY.sha256
RUN_ROOT:CONFLICT_STOP_FINALIZED/CONFLICT_STOP.json
RUN_ROOT:CONFLICT_STOP_FINALIZED/CONFLICT_STOP.sha256
```

`excluded_self_paths_logical_sha256` is SHA-256 of LF-joined canonical typed cells `{"n":"excluded_self_path","t":"STRING","v":"<path>"}` in the fixed order above, no trailing LF. Entries hash as LF-joined exact entry typed bytes in entry order. Groups hash analogously. The raw `entries` and `conflict_groups` arrays are independently validated against their counts and aggregate hashes and are represented in the inventory projection only by those count/hash pairs; they are not hashed a second time. `inventory_logical_sha256` excludes its own destination field and hashes these cells exactly in this order:

```text
schema_version                          STRING
spec_revision                           UINT
run_id                                  STRING
accepted_contract_manifest_file_sha256  SHA256
governing_schema_registry_file_sha256   SHA256
primary_stop_code                       STRING
conflict_group_count                    UINT
conflict_groups_logical_sha256          SHA256
entry_count                             UINT
entries_logical_sha256                  SHA256
excluded_self_paths                     STRING_LIST
excluded_self_paths_logical_sha256      SHA256
```

Complete canonical JSON bytes have an independent file hash and bundled sidecar.

#### 21.4.8 Complete `conflict_stop_marker_v23`

`CONFLICT_STOP.json` exact field order:

```text
schema_version                         STRING = local_curl_conflict_stop_marker.v23
spec_revision                          UINT16 = 23
marker_kind                            STRING = CONFLICT_STOP_FINALIZED
run_id                                 STRING /^run_[0-9a-f]{64}$/
terminal_state                         STRING = FINALIZED_CONFLICT_STOP
primary_stop_code                      REV23_STOP_CODE
conflict_inventory_path                STRING = CONFLICT_STOP_FINALIZED/CONFLICT_INVENTORY.json
conflict_inventory_file_size_bytes     UINT64
conflict_inventory_file_sha256         SHA256
conflict_inventory_logical_sha256      SHA256
conflict_group_count                    UINT64
inventory_entry_count                  UINT64
replay_result_emitted                   BOOL = false
continuation_eligible                   BOOL = false
same_run_resume_permitted               BOOL = false
created_at_ns                           UTC_NS
conflict_stop_marker_semantic_sha256    SHA256
```

Nullability: no field is nullable. `primary_stop_code` is the inventory's exact governing enum value. Inventory size/file/logical hashes and both counts equal the reopened inventory bytes/object. The three booleans are always false.

Marker semantic projection excludes only producer-time `created_at_ns` and destination `conflict_stop_marker_semantic_sha256`; every other field remains in displayed order. The destination equals SHA-256 of the exact canonical typed projection. Complete marker JSON independently binds `created_at_ns` through its file SHA-256 and sidecar.

The marker sidecar is exactly:

```json
{"target_file_sha256":"<exact marker complete-file hash>","target_path":"CONFLICT_STOP_FINALIZED/CONFLICT_STOP.json"}
```

The inventory sidecar is exactly:

```json
{"target_file_sha256":"<exact inventory complete-file hash>","target_path":"CONFLICT_STOP_FINALIZED/CONFLICT_INVENTORY.json"}
```

All four files are fully prepared, mutually cross-validated without self-hash cycles, and committed by one §3.6 atomic no-replace directory promotion. The directory contains exactly those four files and no symlink, subdirectory, extra file, or missing member. If a valid canonical conflict directory already exists, a losing finalizer adopts it only when inventory canonical bytes are identical and marker semantic projections are equal; `created_at_ns` may differ, but no other marker field may differ. An incompatible canonical conflict directory is `FINALIZATION_TARGET_CONFLICT`.

Terminal validation requires:

1. inventory and marker canonical schemas and hashes valid;
2. marker/inventory run ID, stop code, logical hash, group count, and entry count equal;
3. both sidecars pair only with their local target;
4. every unresolved durable artifact outside the four self paths is represented by the inventory;
5. no valid `REPLAY_FINALIZED.json`, `STOP_FINALIZED.json`, `RUN_STOP_FINALIZATION_FAILED.json`, or other accepted normal terminal marker exists;
6. no second conflict-stop directory/marker exists; and
7. atomic-directory commit validates.

Normal and conflict terminal markers are mutually exclusive. Coexistence yields `STOP_FINALIZATION_INVENTORY_INVALID` and no valid terminal profile; neither marker is silently preferred. A valid conflict marker is immutable, emits no empirical result, grants no continuation, and permits no same-run resume.

### 21.5 Resume after terminal markers

- `FINALIZED_REPLAY` and `FINALIZED_STOP_CLEAN`: immutable; no replay/resume. A missing registered sidecar may be reconstructed deterministically from the authoritative immutable target; this is metadata repair only.
- `FINALIZED_CONFLICT_STOP`: immutable; no same-run recovery or resume. Later repair requires a separately specified new run/evidence-review process and cannot mutate this run.
- no terminal marker: classify valid pending normal inventory first, then snapshot/fence recovery under §§7.5 and 17.10. A pending normal inventory may be completed only with exact marker bytes derived from it.

## 22. Exact typed stops and precedence

### 22.1 Stop mapping

| Stop | Exact amended trigger | Stage/effect |
|---|---|---|
| `STOP_ROW_HASH_PROJECTION_INVALID` | malformed registered typed projection | first detecting stage; preserve bytes |
| `STOP_LOGICAL_HASH_MISMATCH` | valid projection recomputes to a different logical hash | first detecting stage; preserve bytes |
| `STOP_SEMANTIC_ID_COLLISION` | one semantic identity maps to different semantic bytes; physical Parquet variation with equal logical bytes is excluded | first detecting stage; conflict-stop eligible |
| `STOP_CAPTURE_SNAPSHOT_INVALID` | capture snapshot chain, capture history publication/adoption, partition semantics, own-entry reconciliation, count/coverage, or capture publication atomicity fails | V7; no cancellation/continuation/replay result |
| `STOP_ANALYSIS_SNAPSHOT_INVALID` | compatibility or strict snapshot chain/publication/adoption/partition/count/current-view condition fails | V8C/V8S; no replay result |
| `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` | fence chain/unit publication, no-replace adoption, row-batch provenance, STARTED release, reservation triple including `reservation_fence_unit_file_sha256`, cancellation/activation binding, or one-to-one tuple reconciliation fails | V7/V8; no continuation/replay result |
| `STOP_RESERVATION_NO_START_PROOF_INVALID` | structurally readable evidence fails complete interval, zero-count, closure, or freshness proof | derived unproven; no continuation eligibility |
| `STOP_FINALIZATION_INVENTORY_INVALID` | V10 normal/conflict inventory schema, closure, grouping, self-exclusion, or terminal-profile rule fails | V10 only; no valid terminal profile |
| `STOP_FINALIZATION_ATOMICITY_UNSUPPORTED` | required V10 normal inventory/marker or V10 conflict-directory atomic publication is unsupported | V10 only; halted/unfinalized |
| `STOP_FINALIZATION_ATOMICITY_FAILURE` | attempted V10 normal inventory/marker or V10 conflict-directory publication fails | V10 only; preserve V10 residue |

Snapshot publication atomicity failures never map to a finalization atomicity stop: capture uses `STOP_CAPTURE_SNAPSHOT_INVALID`; compatibility/strict use `STOP_ANALYSIS_SNAPSHOT_INVALID`. Fence publication atomicity failures use `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`. V10 finalization atomicity stops are not global publication stops.

### 22.2 Local precedence

Within one Finding 4 validation pass:

1. `STOP_ROW_HASH_PROJECTION_INVALID`;
2. `STOP_LOGICAL_HASH_MISMATCH`;
3. `STOP_SEMANTIC_ID_COLLISION` only for different semantic bytes under one semantic identity;
4. applicable family snapshot stop;
5. `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`;
6. `STOP_RESERVATION_NO_START_PROOF_INVALID`;
7. V10 inventory or V10 finalization atomicity stop only when a terminal profile is attempted.

A validated `SUPERSEDED_BY_CANONICAL_WINNER` candidate produces no stop and is removed from the unresolved-prepared set. Missing evidence never becomes a zero-count proof.

## 23. Producers, consumers, lifecycle, immutability, and resume

### 23.1 Producer-consumer matrix

| Artifact | Sole producer class | Required consumers |
|---|---|---|
| prepared evidence unit | snapshot publisher, fence coordinator, or V10 normal finalizer by unit kind | publication/adoption validator, recovery, inventories, Sentinel |
| superseded prepared candidate | original producer; classification derived by validator | winner-adoption validator, normal/conflict inventory, Sentinel |
| immutable partition | detached partition writer | every referencing historical validator, adoption validator, finalizer |
| atomic snapshot history directory | family snapshot publisher under family rules; capture publisher under open fence | chain/history validator, capture fence validator, inventory |
| current-view generation and legacy mirrors | current-view projector | ordinary readers, finalizer; never head authority |
| atomic fence-unit directory | capture-fence coordinator | row provenance, cancellation/CONTINUATION validator, finalizer |
| immutable authorization/capture row batch | fence coordinator | relation reconstruction, aggregate projector, proof validator |
| aggregate relation view | aggregate projector | ordinary readers/finalizer; never primary evidence |
| normal V10 inventory/marker | V10 normal finalizer | terminal validator, Sentinel |
| conflict-stop bundle | V10 conflict finalizer | Sentinel and later external evidence review only |

No consumer treats a current mirror, aggregate view, transient candidate, superseded physical object, or unbound capture history directory as canonical historical evidence.

### 23.2 Immutability

After commit, prepared-unit directories, history directories, partitions, fence-unit directories, row batches, normal final inventories, normal final markers, and conflict-stop bundles are immutable. Current generations are immutable by sequence. Legacy current mirrors and aggregate relation views are replaceable only from validated committed sources before terminal finalization. Deterministic repair of a missing registered sidecar from an immutable authoritative target is the sole permitted post-terminal in-run metadata write and cannot change target bytes or terminal state.

### 23.3 Resume order

Resume must:

1. validate mutually exclusive terminal profiles;
2. validate every committed prepared plan, descriptor, source byte, target scope, and §5.2 role/cardinality rule;
3. identify canonical no-replace winners and rederive every `SUPERSEDED_BY_CANONICAL_WINNER` classification before treating candidates as nonblocking;
4. validate snapshot and fence graphs including cycles before selecting heads;
5. identify at most one durable open fence;
6. for capture, prohibit history-directory promotion unless the matching acquisition is open; recover an already promoted unbound directory only by the exact payload/release under that acquisition;
7. classify snapshot publication under §7.5 and fence recovery under §17.10;
8. complete only exact prepared/adopted winner bytes or emit the applicable family or authorization/capture stop;
9. repair current generations, mirrors, and aggregate views only from committed canonical sources;
10. validate V10 pending normal inventory/marker state only after all non-V10 recovery is closed; and
11. revalidate cancellation and CONTINUATION freshness before any reservation.

A valid canonical winner may supersede a losing candidate; the old prohibition on replacing every pending unit is narrowed accordingly. No candidate may replace an incompatible canonical winner or bypass semantic validation.

### 23.4 Hash-cycle prohibition

The dependency graph is acyclic:

- prepared-unit ID is the preparation-plan file hash; the plan excludes future physical object hashes and its own ID;
- prepared descriptor binds final object bytes; final objects bind only the plan hash/ID, never the descriptor hash;
- snapshot manifest hashes only predecessor manifest;
- publication/current markers bind plan and member hashes but exclude their own hashes and descriptor hash;
- capture fence unit binds snapshot publication marker; the snapshot marker does not bind a future fence-unit hash;
- fence unit binds plan, row-batch/event hashes, and predecessor fence-unit hash; event/rows do not bind fence-unit or descriptor hash;
- sidecars bind targets; targets do not bind sidecars;
- normal marker binds already committed inventory and the prepared-unit ID; normal inventory excludes its own target, marker/sidecars, and the selected normal-finalization prepared subtree; the marker restores the one-way binding to that subtree;
- conflict inventory excludes its terminal bundle's four future bytes;
- physical Parquet file hashes bind encodings, while logical hashes bind semantic rows; adoption creates no reverse edge from canonical targets to losing candidate descriptors.

Any reverse edge creating a cycle is nonconforming and requires separate review.

---

## 24. Positive and counterexample test requirements

These are proposed specification acceptance tests only. This draft does not authorize test authoring or execution.

### 24.1 Snapshot chain, historical reconciliation, and cycles

Positive: origin 0, append, no-change checkpoint, successor repartition, strict timestamp increase, unique head, historical manifests reconciled only to their own entries/partitions, and current view reconciled only to head.

Reject: gap, duplicate canonical sequence, fork, wrong predecessor, rollback, stale/equal timestamp, self/two-node/long cycle, forward edge, disconnected component, or historical manifest compared to successor/current index.

### 24.2 Prepared-source, ordinal, path, matrix, and sidecar tests

For every unit, assert canonical `CLAIM_SCOPE.json` and `CLAIM_SEMANTIC.json` bytes/sidecars/file hashes/logical hashes, then `object_ordinal=0..M-1`, exact array order, unique normalized target paths, exact mode-specific source paths, no traversal, no symlink component, source regularity, and source size/hash equality. Assert `REUSE_IMMUTABLE_SOURCE` has source path exactly equal to validated immutable target. For snapshots, assert `PARTITION_PAYLOAD` count equals `len(snapshot_claim.partition_entries)`.

For every role, assert exact unit kind, cardinality, publication mode, sidecar pair, and logical-hash nullability. Reject gap/duplicate ordinal, wrong zero-padding, absolute/backslash/dot-dot path, alternate reuse source, missing source bytes, duplicate target, missing/extra/cross-unit sidecar, non-null sidecar logical hash, null non-sidecar logical hash, or wrong batch/intent cardinality.

### 24.3 Claim-scope, claim-semantic, and canonical-winner tests

Positive:

- recompute exact claim-scope bytes/hash for snapshot, fence, and normal finalization;
- snapshot uses `len(partition_entries)` and exact ordered-relation hash, including zero-row capture-origin coverage;
- equal logical Parquet variants adopt the first canonical physical object;
- every differing JSON field is within the role-specific substitution whitelist and dependent physical hashes are recomputed;
- committed loser becomes `SUPERSEDED_BY_CANONICAL_WINNER`, enters inventory, and does not block normal finalization.

Reject missing claim source bytes, undefined/independent partition count, old relation pseudo-fields, unequal ordered rows, wrong capture coverage state/hash, differing non-whitelisted field, stale dependent hash after substitution, different claim semantics under one scope, missing winner source, cross-producer sidecar, or omitted superseded unit.

### 24.4 Parquet physical/semantic distinction tests

Positive: different valid Parquet bytes with equal schema, exact ordered typed rows, counts, bounds, and logical hash are semantically equal; first target stays canonical.

Reject physical inequality alone as semantic collision, equal row count with different rows/order/hash, or winner rewrite.

### 24.5 Prepared-source recovery and hash-cycle tests

For every recoverable role, kill after prepared-directory commit and recover from exact persisted source bytes. Reject hash-only intent, missing/wrong/symlink source, future-hash cycle, descriptor hash in target semantics, or descriptor omission. Verify claim semantics precede plan, plan precedes source/target bytes, and descriptor follows them.

### 24.6 Acquisition-bound payload and capture-promotion tests

Positive:

1. prepare exact snapshot claim and payload-intent bytes;
2. acquire fence with immutable intent file/hash;
3. validate exact capture prefix and claim under that acquisition;
4. promote exact history directory;
5. commit at `A+1` only the event/rows/snapshot/validation identities in the bound intent;
6. release.

Crash after promotion resumes only that bound payload. Concurrent acquisition candidates with identical intent may adopt the winner; different intents conflict. Reject generic acquisition, absent intent bytes, wrong intent hash, alternate `A+1` event, promotion before acquisition, promotion after release, prefix validation outside acquisition, different snapshot/row hash, or aborted release after canonical output promotion.

### 24.7 Partition and successor-repartition tests

Test zero/empty/single/multiple partitions, ordinals, key canonicalization, bounds, gaps, overlap, duplicate, inversion, physical adoption, logical collision, and complete historical partition union. Positive successor repartition keeps predecessor partitions immutable and inventoried.

### 24.8 Physical row persistence and aggregate tests

Positive: each row appears in exactly one immutable batch and one canonical fence unit; aggregate rebuild is exact. Reject aggregate-only row, hash without batch bytes, duplicate batch membership, unclaimed row, wrong batch count/hash/key range, or stale aggregate treated as authority.

### 24.9 First fence acquisition and nullable-origin test

Positive sequence 0 acquisition has null predecessor and null coverage, then payload and release. Reject `-1`, `UINT64_MAX`, zero, or string as origin coverage. Cancellation at acquisition 0 is impossible because no prior reservation sequence satisfies `R<0`.

### 24.10 Fence schema, intent, reservation hash, and contention tests

Assert the exact event/manifest field order, acquisition-bound intent file and semantic hash, total event nullability, and `reservation_fence_unit_file_sha256` cancellation-only behavior. The reservation hash resolves exact earlier manifest bytes and sole reservation row. Reject partial groups, inferred hash, aggregate-only reservation, non-cancellation reservation field, payload intent mismatch, or payload event not occupying exactly `A+1`.

Positive canonical-winner adoption requires equal fence claim semantics and byte-identical intent JSON. Reject incompatible canonical units, different bound intents, semantic-ID conflict, cycle, nested acquisition, two payloads, wrong token/epoch, release mismatch, or fence atomicity mapped to V10.

### 24.11 STARTED launch-order tests

Positive: STARTED batch/payload, durable COMMITTED release, then process permission; terminal under later acquisition/payload/release. Reject transient/prepared STARTED launch, launch before release, shared STARTED/terminal unit, or terminal sequence not later.

### 24.12 Positive cancellation and CONTINUATION tests

Construct exact reservation triple including fence-unit hash, later acquisition, exact checkpoint prefix, zero derived STARTED/terminal counts, cancellation payload/release, fresh CONTINUATION activation/release, and reservation-time revalidation. Derive `PROVEN_NO_START` only when every conjunct holds.

### 24.13 Cancellation and freshness counterexamples

Each remains derived `RESERVATION_START_STATUS_UNPROVEN` and ineligible: omitted/stale/partial/forked/cyclic/unreadable history; matching STARTED/terminal row; caller zeroes; wrong reservation fence-unit hash; cancellation outside checkpoint payload; later contradiction; activation before release; stale activation; or reservation after contradiction.

### 24.14 Conflict inventory and marker tests

Positive:

- construct the exact §21.4.2 discovery union, prove every discovered path appears once or is one of the four ordered self-exclusions, and fail on an unwalkable/incompletely traversed root;
- represent every durable path under accepted-contract, detached pre-run, and run roots with exact owner/schema metadata and owner-registered `conflict_inventory_role_class`;
- preserve registered role/owner for missing and unreadable files through an independently readable parent owner/prepared plan;
- apply the fixed owner-selection order, prove legitimate prepared/canonical secondary claims compatible, and require target-plus-all-owner-registry group membership for contradictory claims;
- apply every role/state matrix cell and precedence rule;
- collapse identical discovery duplicates and emit one path row for contradictory claims;
- map every recovery source to the exact semantic scope, including prepared `claim_scope_sha256`;
- validate complete governing `REV23_STOP_CODE` typing and deterministic `primary_stop_code` selection by §22.2 rank then enum ordinal;
- hash entries/groups/semantic-identity cells/self exclusions exactly;
- independently reconstruct every semantic identity and conflict-group ID;
- atomically commit the exact four-file conflict directory;
- validate marker inventory binding, sidecars, false booleans, terminal state, and mutual exclusion.

Reject unregistered stop code, erased owner metadata, fake missing role, duplicate path row, undefined role/state combination accepted as valid, wrong scope, absent prepared claim hash, unresolved group member, wrong order/hash, extra/missing conflict-directory member, marker/inventory mismatch, nullable marker field, normal+conflict coexistence, replay result, continuation eligibility, or same-run resume. Accept a no-replace conflict-directory winner only when inventory bytes and marker semantics match, even if producer timestamp differs.

### 24.15 Typed-stop and finalization tests

Assert snapshot atomicity failures map to family snapshot stops, fence/intent/payload publication failures map to `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED`, and V10 atomicity stops occur only for terminal publication. Positive normal finalization uses exact §5.5.4 claim semantics and includes selected/superseded prepared units with no open fence. Positive conflict finalization validates the full marker schema. Reject V10 stop at V7/V8, superseded candidate treated as fork, both terminal profiles, undefined primary stop, or replay result from conflict stop.

### 24.16 Authorization-supersession tests

After separately authorized acceptance/materialization, assert every project-state, decision, handoff, prompt, source-gate, authorization-audit, inventory, and checksum document marks Amendment 03 I0 `SUPERSEDED_INACTIVE`; no implementation or source-sync authorization survives by implication.

## 25. No-false-continuation-unblock proof

Continuation eligibility from cancellation is the conjunction:

```text
valid committed reservation row batch and exact `reservation_fence_unit_file_sha256`
AND R < A
AND valid acquisition and coverage boundary
AND complete committed capture row-batch prefix through A-1
AND capture history promoted, validated, and bound under the same open fence
AND valid capture snapshot of exactly that prefix
AND independently derived matching STARTED count = 0
AND independently derived matching terminal count = 0
AND cancellation row committed in same payload unit as checkpoint binding
AND COMMITTED release durable
AND valid closure/usability/proof fields
AND no later contradictory old-reservation row
AND fresh fenced CONTINUATION activation and release
AND revalidation before later continuation reservation
```

Every omitted, stale, partial, contradictory, forked, cyclic, unreadable, aggregate-only, pending, unreleased, non-atomic, or mismatched condition makes the conjunction false. False never becomes zero. Prepared bytes are not committed rows. Aggregate views are not primary evidence. A cancellation row cannot commit without its row batch and fence payload. A continuation cannot activate without its release. Therefore no false continuation-unblock path exists.

---

## 26. Exact schema-registry amendments required after acceptance

A separately authorized materialization must:

1. add every support schema in §3.3 with exact fields, types, domains, nullability, and projections;
2. materialize §5.1 source/target path grammar, exact object-entry projection, ordinal `0..M-1`, and source-mode rules;
3. materialize the total role/cardinality/sidecar/logical-hash matrix, including partition cardinality as `len(snapshot_claim.partition_entries)`;
4. add exact claim-scope, snapshot claim-semantic, fence claim-semantic, normal-finalization claim-semantic, and ordered-relation formulas; prohibit the superseded pseudo-fields;
5. materialize the exact role-specific canonical-winner substitution whitelist and semantic/physical distinction;
6. amend snapshot schemas with historical-own-entry reconciliation, capture coverage, acquisition-bound promotion, and §§6–15 partition rules;
7. amend authorization/capture row schemas with immutable row-batch/fence provenance while preserving proof-state enum;
8. add `capture_payload_intent_v23`, intent objects/cardinality, exact fence event/manifest fields, total nullability, and cancellation reservation hash;
9. materialize the closed §21.4.2 discovery set, fixed owner-selection/secondary-claim compatibility rules, `conflict_inventory_role_class` on every registered owner entry, missing-owner parent binding, complete conflict owner metadata, role/state matrix, recovery-scope mapping, entries/groups, governing stop enum reference, inventory, and fully defined marker;
10. restrict finalization atomicity stops to V10 and map snapshot/fence failures as §22 requires;
11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; and
12. preserve every non-Finding-4 schema byte unless an exact affected reference changes.

No field, type, enum, role, path grammar, classification, stop mapping, projection, or marker rule may remain prose-only after materialization. This draft does not authorize materialization.

## 27. Artifact producer-consumer matrix

| Artifact | Producer | Consumer | Cardinality | Lifecycle |
|---|---|---|---|---|
| prepared claim scope/semantic object | family publisher, fence coordinator, or V10 normal finalizer | contention/adoption/recovery validator | exactly one claim scope and one role-specific semantic claim per prepared unit | immutable logical input |
| acquisition-bound payload intent | fence coordinator | exact A+1 payload validator, recovery, Sentinel | exactly one per acquisition | immutable atomic-bundle member |
| selected prepared snapshot/fence unit | family publisher or fence coordinator | canonical publication, recovery, inventory | exactly one selected per canonical claim | immutable |
| superseded prepared candidate | original producer; disposition derived by validator | adoption validator, normal/conflict inventory, Sentinel | zero or more per canonical winner | immutable; nonblocking only after exact validation |
| history sequence directory | family publisher; capture only under open fence | chain/history/final validators | exactly one canonical per committed sequence | immutable |
| immutable partition physical object | partition writer | every referencing snapshot/adoption validator | one canonical physical object per partition target | immutable; physical variants may be superseded |
| current generation/mirrors | current-view projector | current readers/finalizer | one head generation; one mirror set | generation immutable; mirrors replaceable preterminal |
| fence sequence directory | fence coordinator | row/proof/final validators | exactly one canonical per committed fence sequence | immutable |
| immutable row batch | fence coordinator | relation reconstruction, proof, aggregate | total §5.2 cardinality | immutable |
| aggregate relation view | aggregate projector | ordinary readers/finalizer | one per relation | replaceable preterminal; non-authoritative |
| normal V10 inventory/marker | V10 normal finalizer | terminal validator/Sentinel | exactly one selected normal profile | immutable |
| conflict inventory and fully defined marker bundle | V10 conflict finalizer | terminal validator/Sentinel | zero or one, exclusive of every normal marker | immutable terminal |

Every artifact has an exact producer and intended consumer. A losing candidate never becomes a second producer of the canonical target.

## 28. Typed stop-state table

| Trigger | Stop | Stage | Zero requests guaranteed | Artifact behavior | Downstream effect |
|---|---|---|---:|---|---|
| capture snapshot chain/partition/history publication/adoption invalid | `STOP_CAPTURE_SNAPSHOT_INVALID` | V7 | false | preserve selected, superseded, and conflicting bytes | no cancellation/continuation/replay result |
| compatibility/strict snapshot equivalent invalid | `STOP_ANALYSIS_SNAPSHOT_INVALID` | V8C/V8S | false | preserve evidence | no replay result |
| typed projection malformed | `STOP_ROW_HASH_PROJECTION_INVALID` | first detecting stage | false | preserve evidence | no result |
| logical hash mismatch | `STOP_LOGICAL_HASH_MISMATCH` | first detecting stage | false | preserve evidence | no result |
| one semantic ID maps to different semantic bytes | `STOP_SEMANTIC_ID_COLLISION` | first detecting stage | false | preserve all claims | conflict-stop eligible |
| fence publication/chain/bound-intent/A+1 payload/row provenance/launch/reservation-hash/cancellation binding invalid | `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` | V7/V8 | false | preserve evidence/open fence | no continuation/replay result |
| positive no-start/freshness conjunct fails | `STOP_RESERVATION_NO_START_PROOF_INVALID` | V7/V8 | false | retain contradiction; derive unproven | no continuation eligibility |
| V10 inventory/grouping/terminal-profile invalid | `STOP_FINALIZATION_INVENTORY_INVALID` | V10 | false | no valid terminal profile | halted/unfinalized |
| V10 terminal atomic protocol unsupported | `STOP_FINALIZATION_ATOMICITY_UNSUPPORTED` | V10 only | false | preserve V10 prepared bytes | no terminal marker |
| V10 terminal atomic publication fails | `STOP_FINALIZATION_ATOMICITY_FAILURE` | V10 only | false | preserve V10 residue | no terminal marker |

A semantically equal no-replace loser classified `SUPERSEDED_BY_CANONICAL_WINNER` emits no stop.

## 29. Requirements traceability matrix

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| prepared source/path/ordinal/cardinality closure | §§5.1–5.2 | prepared object/unit | row/hash or applicable structural stop | §24.2 |
| exact claim scopes and claim semantics | §§5.4–5.6 | three claim schemas and hashes | collision only for different semantic bytes under one semantic identity | §24.3 |
| no-replace winner adoption | §§5.7–5.8, 7.2, 17.6 | whitelist + `SUPERSEDED_BY_CANONICAL_WINNER` | no stop when fully proven | §24.3 |
| physical Parquet versus semantic bytes | §5.3 | ordered-relation projection | semantic collision excludes equal logical variants | §24.4 |
| acquisition-bound capture promotion | §§7.3, 17.4–17.8 | immutable intent + exact A+1 payload | capture or auth/capture stop | §24.6 |
| reservation fence-unit hash | §§17.5, 18.2 | manifest field/matrix | auth/capture stop | §24.10 |
| conflict inventory and marker closure | §21.4 | owner metadata, role/state matrix, groups, marker | finalization inventory stop | §24.14 |
| stop-family consistency | §22 | typed stop table | stage-specific | §24.15 |
| physical row persistence and launch order | §§16–17 | row batches/fence release | auth/capture stop | §§24.8, 24.11 |
| cancellation/CONTINUATION proof | §§18–20 | exact prefixes and releases | proof/auth stops | §§24.12–24.13 |
| historical own reconciliation and cycles | §§6, 8 | snapshot graph | family stop | §§24.1, 24.7 |
| no false unblock | §25 | closed conjunction | continuation false unless all true | §§24.12–24.13 |
| authorization supersession | §32 | project/handoff synchronization | no implicit authorization | §24.16 |

## 30. Change ledger from the blocked replacement

### 30.1 Corrected in this revision

- defined closed claim-scope and role-specific snapshot/fence/normal-finalization claim-semantic schemas;
- replaced every independent partition-count reference with `len(partition_entries)` and defined exact ordered-relation/capture-coverage hashes;
- added a durable immutable acquisition-bound payload intent whose exact event and logical identities alone may occupy `A+1`;
- completed prepared-object ordinal, normalized path, no-traversal/no-symlink, source-mode, reuse-source, object-projection, and partition-cardinality rules;
- expanded conflict inventory to every durable accepted-contract artifact through exact owner/schema metadata, total role/state classification, recovery-scope mapping, and governing stop typing;
- fully specified `conflict_stop_marker_v23`, its semantic hash, inventory binding, sidecars, atomic terminal validation, and marker mutual exclusion;
- added acceptance/counterexample tests and synchronized schema, artifact, lifecycle, stop, traceability, and supersession references.

### 30.2 Preserved

All non-Finding-4 behavior in §2.2, plus the prior draft's accepted historical-own-entry reconciliation, successor repartition, partition/hash rules, derived unproven handling, cancellation zero-count direction, CONTINUATION freshness direction, cycle handling, and authorization-supersession direction.

---

## 31. Result-label decision impact

The accepted result-label decision table remains mechanically unchanged. Every defect governed here resolves before empirical result-label evaluation. Structural or proof stops emit no empirical label. A conflict-stop terminal profile emits no replay result. Unproven or contradictory cancellation evidence is not a negative finding and not a clear result.

---

## 32. Mandatory supersession of the existing Amendment 03 I0 authorization package

### 32.1 Effective condition

This section takes effect only if Sentinel accepts this amendment and the amended Revision 23 governing package is completely materialized and canonicalized under a separate authorization.

At that moment, the current Amendment 03 I0 implementation-authorization and source-gate package pinned to earlier governing bytes is `SUPERSEDED_INACTIVE`. Its source/test-source authoring permission, source-gate correction, prompts, and source-synchronization status cannot be reused or satisfied to reactivate work.

No implementation authorization carries forward implicitly.

### 32.2 Historical preservation

Existing Gustavo and Sentinel authorization records remain immutable historical audit evidence. A new supersession record must state:

```text
superseded_authorization = REV23_AMENDMENT_03_I0
supersession_reason = GOVERNING_CONTRACT_CHANGED_BY_FINDING4_AMENDMENT
implementation_authoring_authorized = false
source_sync_authorized = false
test_authoring_authorized = false
test_execution_authorized = false
```

### 32.3 Required canonical synchronization set

A separately authorized acceptance/materialization package must update, reconcile, and rehash at minimum:

```text
project_context/PROJECT_STATE.md
project_context/DECISION_LOG.md
project_context/START_HERE.md
project_context/HANDOFF_orchestrator_rev23_amendment_03_ACCEPTED.md
project_context/HANDOFF_orchestrator_rev23_amendment_03_i0_IMPLEMENTATION_AUTHORIZED.md

project_context/implementation_handoffs/local_curl_rev23_i0/README_FIRST.md
project_context/implementation_handoffs/local_curl_rev23_i0/SENTINEL_ACCEPTANCE_DECISION.md
project_context/implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md
project_context/implementation_handoffs/local_curl_rev23_i0/HANDOFF_INVENTORY.md
project_context/implementation_handoffs/local_curl_rev23_i0/HANDOFF_SHA256SUMS.txt

project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/README_FIRST.md
project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SENTINEL_IMPLEMENTATION_AUTHORIZATION_REV23_AMENDMENT_03_I0.md
project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SENTINEL_CANONICAL_SOURCE_GATE_CORRECTION.md
project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SOURCE_SYNC_AUTHORIZATION_STATUS.md
project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SHA256SUMS.txt
project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SENTINEL_SUPERSESSION_REV23_FINDING4.md  [new]

project_context/implementation_handoffs/local_curl_rev23_i0/prompts/CLAUDE_NEW_CHAT_PROMPT.md
project_context/implementation_handoffs/local_curl_rev23_i0/prompts/SENTINEL_NEW_CHAT_PROMPT.md
```

`GUSTAVO_AUTHORIZATION_RECORD.md` remains immutable historical evidence and is referenced by the supersession record. The Claude prompt becomes an inactive no-authoring placeholder. The Sentinel prompt becomes review-only. The source gate states `SUPERSEDED` and cannot authorize synchronization or authoring.

### 32.4 Hash and inventory cascade

A later separately authorized materialization must update affected accepted-contract files, schema registry, governing manifest, semantic hash, complete-file sidecar, accepted-contract checksum inventory, amendment audit, handoff inventories, authorization-audit inventories, prompts, and outer checksums. No-change files receive verified no-change hashes.

Only after new Sentinel acceptance, canonical installation, and a new explicit Gustavo authorization may any implementation scope or Claude prompt be created.

---

## 33. Unresolved questions

None within the authorized Finding 4 specification scope.

The prepared-unit, atomic-directory, row-batch, and conflict-stop artifacts are additive evidence contracts required by the blocked findings. They do not redesign token, request, HTTP, result, denominator, threshold, or downstream gate behavior. Sentinel must independently decide whether this narrow additive architecture is acceptable.

---

## 34. Sentinel handoff

### 34.1 Decision requested

Review this complete replacement as a narrow Revision 23 Finding 4 amendment. Determine independently whether concurrency-safe publication, durable recovery sources, physical row persistence, STARTED/release launch ordering, terminal-row separation, snapshot/fence cycles, cancellation proof, CONTINUATION freshness, terminal-profile separation, inventories, and authorization supersession are complete and compatible with accepted architecture.

Professor does not approve this draft and does not authorize implementation.

### 34.2 Required package if accepted

A later separately authorized static materialization must return the complete amended specification package, Sentinel handoff, change ledger, traceability matrix, typed stop table, result-label no-change record, producer-consumer matrix, unresolved-questions file, exact diffs/replacements, schema patch, manifests, inventories, sidecars, and SHA-256 hashes.

### 34.3 Authorization closing statement

- specification revision only;
- materialization not authorized;
- implementation not authorized;
- source synchronization not authorized;
- test authoring not authorized;
- tests not authorized;
- repository edits not authorized;
- local reads and artifact recovery not authorized;
- deterministic regeneration not authorized;
- subprocesses not authorized;
- network or curl execution not authorized;
- replay and empirical run not authorized;
- full-universe build not authorized;
- P1/P2/P3 continuation not authorized;
- probe execution not authorized;
- P1 remains blocked unless the canonical repository states otherwise;
- `named_binary_probe_blocked` remains true unless separately changed through an accepted and authorized gate decision.
