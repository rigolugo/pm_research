# REV23 Finding 4 — Bounded Delta Packet 05

## 1. Exact inputs and application order

Apply this packet only after these exact inputs, in this order:

1. base amendment SHA-256 `3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563`;
2. Correction Packet 01 SHA-256 `b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9`;
3. Delta Packet 02 SHA-256 `184da5779afc301255cd6532e456727380f14e4f0f32bad30f2b4bd010bb76c2`;
4. Delta Packet 03 SHA-256 `4bb5b24561dc2afc378dd36c0a69bfd178b18287e4783bcb14bde18740e1382c`;
5. Delta Packet 04 SHA-256 `b942b67f688ee4b06d479ee8afa47193802d2969f116a7c4b1edcd247d80f433`;
6. this Delta Packet 05.

A byte mismatch in any prerequisite prevents application. This packet creates no independent inventory-classification registry, owner array, or undeclared inventory-row field.

---

## 2. Exact replacement for Delta Packet 04 §5.2.1

Replace Delta Packet 04 §5.2.1 in full with the following text. Delta Packet 04 §5.2.2, including its complete `unit_kind → producer_stage` table, remains unchanged.

#### 5.2.1 Normalization, claim collection, authoritative-owner selection, and row derivation

The candidate path is the exact normalized run-relative or package-relative path required by the governing path contract. A path containing an absolute prefix, `.` segment, `..` segment, empty segment, backslash, duplicate slash, symlink traversal, or non-normalized UTF-8 form is invalid and produces `STOP_FINALIZATION_INVENTORY_INVALID`.

For one normalized included path, collect **all** registered owner claims from the effective base §21.4.2 discovery union. This includes, where applicable, simultaneous `GOVERNING_PACKAGE_ENTRY`, `SCHEMA_ARTIFACT_CATALOG_ENTRY`, runtime-owner, prepared-plan, and recovery-source claims. Discovery occurrences that identify the same owner claim collapse only when all of the following are byte-identical: `owner_kind`, `owner_registry_path`, `owner_registry_file_sha256`, `owner_entry_key`, `owner_entry_logical_sha256`, normalized target path, `content_schema_id`, `registered_object_role`, registered semantic identity, and every required expected hash. They are one claim, not multiple candidates.

Select exactly one authoritative owner by the existing effective base §21.4.2 owner-kind precedence, reproduced here only as the governing selection order:

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

Selection is by owner kind, not by discovery class. A governing-package claim and a schema-artifact-catalog claim for the same accepted path therefore coexist: `GOVERNING_PACKAGE_ENTRY` is selected and the catalog claim remains a secondary claim. They are not duplicate candidates merely because they name the same path.

After identical-discovery collapse, the highest-precedence nonempty owner kind must contain exactly one distinct claim. Two or more distinct claims within that selected owner kind are contradictory owner metadata and produce `STOP_FINALIZATION_INVENTORY_INVALID`. A selected `UNREGISTERED_DURABLE_OBJECT` is not valid normal-finalization classification and produces `STOP_FINALIZATION_INVENTORY_INVALID`.

The one normal-inventory row derives its pair only from the selected owner:

```text
artifact_role  = selected_owner.registered_object_role
producer_stage = producer_stage_for(selected_owner)
```

`artifact_role` is never derived from `schema_ref`, `content_schema_id`, a disposition, a secondary owner, or a recovery-source label.

`producer_stage_for(selected_owner)` is total over every registered owner kind that may validly own a normal-inventory path:

| Selected `owner_kind` | Exact `producer_stage` derivation |
|---|---|
| `CONFLICT_FINALIZATION_OBJECT` | exact string `V10 conflict finalizer` |
| `NORMAL_FINALIZATION_OBJECT` | exact string `V10 normal finalizer` |
| `FENCE_UNIT_OBJECT` | reopen the exact owning fence-unit manifest, validate its `unit_kind`, and use the unchanged effective §5.2.2 `unit_kind → producer_stage` mapping |
| `AUTHORIZATION_USE_RELATION_VERSION` | exact string `V7 authorization-use ledger` |
| `CAPTURE_RELATION_VERSION` | exact string `V7 capture runner` |
| `SNAPSHOT_CURRENT_VIEW_OBJECT` | reopen the exact current-view owner, validate its snapshot `subject_family`, and use the matching unchanged §5.2.2 `SNAPSHOT_PUBLICATION` family row |
| `SNAPSHOT_HISTORY_OBJECT` | reopen the exact history owner, validate its snapshot `subject_family`, and use the matching unchanged §5.2.2 `SNAPSHOT_PUBLICATION` family row |
| `DETACHED_PRE_RUN_ATTACHMENT_ENTRY` | exact string `V5A detached pre-run attachment finalizer` |
| `GOVERNING_PACKAGE_ENTRY` | exact string `GOVERNING_PACKAGE` |
| `SCHEMA_ARTIFACT_CATALOG_ENTRY` | exact accepted catalog entry `producer` string after validating that the selected catalog entry uniquely owns the normalized path; null, empty, unreadable, or contradictory producer metadata is invalid |
| `PREPARED_PLAN_OBJECT` | reopen the exact owning prepared plan, validate whether the path is an exact registered structural member or exact object member, validate `unit_kind`, and use the unchanged effective §5.2.2 `unit_kind → producer_stage` mapping |
| `UNREGISTERED_DURABLE_OBJECT` | no valid value; normal finalization stops with `STOP_FINALIZATION_INVENTORY_INVALID` |

For prepared structural-member and prepared object-member paths, the unchanged Delta Packet 04 §5.2.2 table remains the sole `unit_kind → producer_stage` mapping. The exact structural-member role table and validated `prepared_evidence_object_v23.object_role` rules remain unchanged; they supply `registered_object_role` to the selected `PREPARED_PLAN_OBJECT` claim and never bypass owner selection.

Every nonselected claim is a compatible secondary claim or a contradiction. A secondary claim does not emit, replace, or vote on the selected `(artifact_role,producer_stage)` pair. Validate each secondary claim only for its applicable registered dimensions:

1. its normalized target path is identical to the selected owner's normalized target path;
2. its effective `content_schema_id` is byte-identical to the selected owner's effective `content_schema_id` after resolving any catalog/template reference through the immutable owner entry;
3. its `registered_object_role` is byte-identical to the selected owner's `registered_object_role`;
4. every required owner-registry hash, owner-entry hash, target complete-file hash, logical hash, and registered semantic identity recomputes and agrees with the selected canonical object; and
5. a different expected physical file hash is permitted only when the effective §5.3/§5.7 canonical-winner rules independently prove permitted physical-winner variation, identical registered semantic identity, and equal canonical logical semantics. Physical inequality alone is neither compatibility nor conflict.

The expected accepted case in which one governing-package entry and one schema-artifact-catalog entry register the same path is valid only when the path, effective schema ID, registered role, required hashes, and semantic identity satisfy the five checks above. The governing-package owner supplies the inventory pair; the catalog claim supplies secondary schema/producer provenance only.

A genuine disagreement in normalized path, effective `content_schema_id`, `registered_object_role`, required hash, semantic identity, or permitted physical-winner proof produces `STOP_FINALIZATION_INVENTORY_INVALID`. Precedence determines the deterministic selected-owner fields; it never suppresses contradictory evidence.

---

## 3. Exact replacement for Delta Packet 04 §5.2.3

Replace Delta Packet 04 §5.2.3 in full with the following text.

#### 5.2.3 Total owner-selection and contradiction handling

Normal-inventory classification is total and deterministic:

1. Normalize the included path and collect all claims exactly under §5.2.1.
2. Collapse only identical discovery occurrences of one claim under the exact equality rule in §5.2.1.
3. Select the highest-precedence nonempty owner kind using effective base §21.4.2.
4. Require exactly one distinct claim in that selected owner kind and reject `UNREGISTERED_DURABLE_OBJECT` as a normal-finalization owner.
5. Derive `artifact_role` solely from the selected owner's exact `registered_object_role` and derive `producer_stage` solely from the selected-owner table in §5.2.1, using unchanged §5.2.2 where that table delegates by `unit_kind` or snapshot family.
6. Validate every nonselected claim only as a secondary claim under the five compatibility dimensions in §5.2.1. A compatible secondary claim emits no inventory row and no alternative role/stage pair.
7. A governing-package claim and schema-artifact-catalog claim for one accepted path are expected compatible secondary-owner evidence, not a duplicate-owner error. Any disagreement in their normalized path, effective schema ID, registered role, required hash, or semantic identity is `STOP_FINALIZATION_INVENTORY_INVALID`.
8. Two distinct claims in the selected owner kind; no registered claim; unreadable selected-owner metadata without independently bound expected metadata; structural/member grammar contradiction; unknown or invalid `unit_kind`; invalid snapshot family; selected-owner role/stage derivation failure; secondary-owner incompatibility; duplicate inventory output row; disposition-derived role/stage; owner array; or undeclared row field produces `STOP_FINALIZATION_INVENTORY_INVALID`.
9. A selected, `SUPERSEDED_BY_CANONICAL_WINNER`, or `UNSELECTED_CANONICAL_RACE_LOSER` disposition never changes a canonical path's selected owner, `artifact_role`, or `producer_stage`. Disposition and secondary relationships are validated outside the row schema.

The normal inventory contains exactly one row per unique normalized included path. Snapshot-sequence membership, current-head membership, prepared-unit membership, semantic supersession, race-loser withdrawal, row-batch ownership, terminal-source ownership, and every compatible secondary-owner relationship are validated separately by reopening their governing bytes. No owner array, secondary-role array, alternative-pair field, or other undeclared field is added to the inventory row.

---

## 4. Directly dependent materialization replacement

Replace Delta Packet 04 §6.4 in full with the following text.

### 6.4 Replacement for base §26 item 11

11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; materialize normal final-inventory cardinality as exactly one row per unique normalized included path; collect all effective base §21.4.2 claims, select one authoritative owner by the existing owner-kind precedence, derive `artifact_role` only from the selected owner's `registered_object_role`, and derive `producer_stage` only from the exact owner-specific rules in effective §5.2.1 and unchanged `unit_kind → producer_stage` table in §5.2.2; permit governing-package and schema-artifact-catalog claims for one accepted path to coexist as selected/secondary evidence when all applicable path, schema, role, hash, semantic-identity, and physical-winner checks reconcile; add no independent classification-registry artifact, owner arrays, alternative role/stage pairs, or undeclared relationship fields; reject absent, ambiguous, same-kind duplicate, unreadable, unregistered, or contradictory owner classifications with `STOP_FINALIZATION_INVENTORY_INVALID`; and validate snapshot, prepared-unit, superseded-unit, race-loser, row-batch, terminal-source, and secondary-owner relationships separately during closure;

---

## 5. Directly dependent test replacement

Replace the normal-inventory classification test paragraph supplied by Delta Packet 04 §5 with the following text.

Normal-inventory owner-selection tests construct the complete effective base §21.4.2 claim set for each normalized path and exercise every selected owner kind and every unchanged effective §5.2.2 `unit_kind → producer_stage` row. Positive cases require exactly one inventory row per normalized included path and prove: governing-package selection with a compatible schema-artifact-catalog secondary claim for the same accepted path; schema-artifact-catalog fallback when no higher-precedence owner exists; exact selected-owner `registered_object_role` use rather than `schema_ref`; the owner-specific producer-stage rule for governing-package, catalog fallback, snapshot history, snapshot current view, fence unit, authorization-use relation, capture relation, normal finalization, conflict finalization, detached pre-run attachment, and prepared-plan owners; all eight prepared structural roles; prepared object role extraction at exact ordinal; compatible lower-precedence prepared/recovery claims; permitted physical-winner inequality only under independently proven equal semantics; and disposition-neutral selected role/stage. Counterexamples require `STOP_FINALIZATION_INVENTORY_INVALID` for: no claim; selected unregistered owner; two distinct claims in the selected owner kind; two governing-package entries for one path; malformed catalog fallback producer; deriving `artifact_role` from `schema_ref`; path mismatch; schema mismatch; registered-role mismatch; required-hash mismatch; semantic-identity mismatch; unproved physical-winner difference; structural/member grammar contradiction; unknown `unit_kind`; invalid snapshot family; unreadable selected owner without independently bound metadata; secondary claim emitting another role/stage pair; duplicate path row; disposition-derived replacement of role/stage; owner array; undeclared field; or omitted secondary-relationship proof. One governing-package claim plus one compatible catalog claim must pass and must not be treated as duplicate candidates. No test may read or depend on an independent inventory-classification registry artifact.

---

## 6. Directly dependent traceability replacement

Replace the traceability row supplied by Delta Packet 04 §6 with the following text.

### 8.4 Replacement traceability row immediately after `final snapshot and complete loser inventory closure`

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| normal inventory authoritative-owner selection and one-row-per-path closure | §§5.2, 8.6, 21.2, 21.4.2, 26–27 | collect all registered claims; select one owner by existing owner-kind precedence; `artifact_role=selected_owner.registered_object_role`; exact owner-specific producer stage; compatible secondary claims validate path/schema/role/hash/semantic identity without emitting a second pair; one unique normalized path row; no independent registry or owner arrays | `STOP_FINALIZATION_INVENTORY_INVALID` for absent or unregistered owner, same-kind multiplicity, unreadable selected metadata, role/stage derivation failure, incompatible secondary claim, unproved physical-winner difference, duplicate row, or undeclared field | §§24.14–24.15 as replaced by Delta Packet 03 §7.5, Delta Packet 04 §5, and this packet §5 |

---

## 7. Unchanged-text and authorization statement

Except for the exact replacements in this packet, every byte of the base amendment, Correction Packet 01, Delta Packet 02, Delta Packet 03, and Delta Packet 04 remains unchanged and continues to govern in the stated application order. In particular, Delta Packet 04 §5.2.2 and its complete `unit_kind → producer_stage` table remain byte-for-byte unchanged.

This packet authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
