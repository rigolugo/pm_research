# REV23 Finding 4 — Bounded Delta Packet 06

## 1. Exact inputs and application order

Apply this packet only after these exact inputs, in this order:

1. base amendment SHA-256 `3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563`;
2. Correction Packet 01 SHA-256 `b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9`;
3. Delta Packet 02 SHA-256 `184da5779afc301255cd6532e456727380f14e4f0f32bad30f2b4bd010bb76c2`;
4. Delta Packet 03 SHA-256 `4bb5b24561dc2afc378dd36c0a69bfd178b18287e4783bcb14bde18740e1382c`;
5. Delta Packet 04 SHA-256 `b942b67f688ee4b06d479ee8afa47193802d2969f116a7c4b1edcd247d80f433`;
6. Delta Packet 05 SHA-256 `5bf5788f2298267c881b1c2a0d612617ce0a470d07cef62310752ded43d74fa1`;
7. this Delta Packet 06.

A byte mismatch in any prerequisite prevents application.

---

## 2. Exact replacement rows in Delta Packet 05 §5.2.1 producer-stage table

In the `producer_stage_for(selected_owner)` table in Delta Packet 05 §5.2.1, replace only the following five rows. Every unlisted row remains byte-for-byte unchanged.

| Selected `owner_kind` | Exact `producer_stage` derivation |
|---|---|
| `CONFLICT_FINALIZATION_OBJECT` | no valid normal-inventory value. Conflict-terminal self paths are excluded from normal inventory, and a conflict-terminal profile is mutually exclusive with normal finalization. Selection of this owner kind for a proposed normal-inventory row produces `STOP_FINALIZATION_INVENTORY_INVALID`. |
| `NORMAL_FINALIZATION_OBJECT` | no valid normal-inventory value. The normal inventory, its marker and derivative sidecars, and the selected `NORMAL_FINALIZATION` prepared-unit subtree are the closed normal-finalization self-exclusions. Selection of this owner kind for a proposed normal-inventory row produces `STOP_FINALIZATION_INVENTORY_INVALID`. |
| `FENCE_UNIT_OBJECT` | reopen the exact canonical `fence_unit_manifest_v23` selected by the owner claim; read its persisted `event_kind`; resolve the exact linked prepared plan using the manifest's `preparation_plan_file_sha256` and `prepared_unit_id`; require the plan bytes and sidecar to validate, require `plan.unit_kind == manifest.event_kind`, and then use the unchanged effective §5.2.2 `unit_kind → producer_stage` row for that exact event kind. The manifest has no `unit_kind` field. Missing or unreadable manifest/plan bytes, a hash or prepared-unit-ID mismatch, unsupported `event_kind`, or unequal `plan.unit_kind` produces `STOP_FINALIZATION_INVENTORY_INVALID`. |
| `SNAPSHOT_CURRENT_VIEW_OBJECT` | reopen the exact canonical `snapshot_current_view_commit_v23` that owns the path; read its persisted `audit_family`; require `audit_family` to be exactly one partition-family value; resolve and validate the linked prepared plan from `preparation_plan_file_sha256` and `prepared_unit_id`; require `plan.unit_kind=SNAPSHOT_PUBLICATION` and `plan.subject_family == audit_family`; then derive the exact stage from the closed audit-family table in §2.1. Missing, unreadable, non-domain, or unequal evidence produces `STOP_FINALIZATION_INVENTORY_INVALID`. |
| `SNAPSHOT_HISTORY_OBJECT` | resolve the selected history owner to the sequence's exact canonical `snapshot_publication_commit_v23`, including when the selected path is a manifest, index, sidecar, marker, or referenced partition; read that commit object's persisted `audit_family`; require `audit_family` to be exactly one partition-family value; resolve and validate the linked prepared plan from `preparation_plan_file_sha256` and `prepared_unit_id`; require `plan.unit_kind=SNAPSHOT_PUBLICATION` and `plan.subject_family == audit_family`; then derive the exact stage from the closed audit-family table in §2.1. Missing, unreadable, non-domain, or unequal evidence produces `STOP_FINALIZATION_INVENTORY_INVALID`. |

### 2.1 Closed snapshot-owner `audit_family → producer_stage` mapping

This table is complete and is the sole stage mapping for selected `SNAPSHOT_HISTORY_OBJECT` and `SNAPSHOT_CURRENT_VIEW_OBJECT` owners:

| Canonical owner `audit_family` | Exact `producer_stage` |
|---|---|
| `capture` | `V7 capture snapshot finalizer` |
| `analysis_compatibility` | `V8 compatibility snapshot finalizer` |
| `analysis_strict` | `V8 strict snapshot finalizer` |

No other family or stage is valid. This table does not replace or modify Delta Packet 04 §5.2.2. That complete `unit_kind → producer_stage` table remains unchanged for prepared structural-member and prepared object-member paths.

---

## 3. Directly affected totality replacements

### 3.1 Replacement paragraph in Delta Packet 05 §5.2.1

Replace the paragraph beginning `` `producer_stage_for(selected_owner)` is total`` with the following text:

`producer_stage_for(selected_owner)` is total over the complete effective owner-kind domain. A selected `CONFLICT_FINALIZATION_OBJECT`, `NORMAL_FINALIZATION_OBJECT`, or `UNREGISTERED_DURABLE_OBJECT` has no valid normal-inventory producer stage and deterministically produces `STOP_FINALIZATION_INVENTORY_INVALID`. Every other valid selected owner kind derives exactly one stage from the table below, the unchanged effective §5.2.2 table where expressly delegated, and the closed snapshot-family table in this packet §2.1. No field absent from the selected owner's registered schema may be read or inferred.

### 3.2 Replacement items in Delta Packet 05 §5.2.3

In Delta Packet 05 §5.2.3, replace only items 5 and 8 with the following text:

5. Derive `artifact_role` solely from the selected owner's exact `registered_object_role`. Derive `producer_stage` solely from the selected-owner table in effective §5.2.1 as amended by Delta Packet 06 §2. For a selected `FENCE_UNIT_OBJECT`, use the canonical manifest's persisted `event_kind` only after the exact linked prepared plan validates and proves `plan.unit_kind == manifest.event_kind`. For a selected snapshot owner, use the canonical owner commit's persisted `audit_family`, require the exact linked plan to prove `unit_kind=SNAPSHOT_PUBLICATION` and `subject_family == audit_family`, and apply Delta Packet 06 §2.1. A selected terminal owner kind or `UNREGISTERED_DURABLE_OBJECT` has no valid normal-inventory pair and stops.

8. Two distinct claims in the selected owner kind; no registered claim; unreadable selected-owner metadata without independently bound expected metadata; structural/member grammar contradiction; a fence owner with missing, unreadable, unsupported, or mismatched `event_kind`/linked-plan evidence; a snapshot owner with missing, unreadable, non-domain, or plan-unequal `audit_family`; selection of `NORMAL_FINALIZATION_OBJECT`, `CONFLICT_FINALIZATION_OBJECT`, or `UNREGISTERED_DURABLE_OBJECT`; selected-owner role/stage derivation failure; secondary-owner incompatibility; duplicate inventory output row; disposition-derived role/stage; owner array; or undeclared row field produces `STOP_FINALIZATION_INVENTORY_INVALID`.

The independent normal-terminal and conflict-terminal publication, validation, sidecar, marker, and mutual-exclusion rules remain unchanged. This packet changes only whether those terminal owner kinds can classify a row inside a normal inventory; they cannot.

---

## 4. Directly affected materialization replacement

Replace Delta Packet 05 §4 in full with the following text.

### 4.1 Replacement for effective base §26 item 11

11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; materialize normal final-inventory cardinality as exactly one row per unique normalized included path; collect all effective base §21.4.2 claims and select one authoritative owner by the existing owner-kind precedence; derive `artifact_role` only from the selected owner's exact `registered_object_role`; derive a selected fence owner's `producer_stage` from the canonical `fence_unit_manifest_v23.event_kind` only after reopening the exact linked prepared plan and proving `plan.unit_kind == manifest.event_kind`; derive a selected snapshot owner's stage from the canonical owner commit's exact `audit_family` using the closed `capture`/`analysis_compatibility`/`analysis_strict` mapping and require its exact linked plan to prove `unit_kind=SNAPSHOT_PUBLICATION` and `subject_family == audit_family`; reject selected normal-terminal, conflict-terminal, or unregistered owners as impossible normal-inventory classifications; preserve the unchanged prepared structural/object `unit_kind → producer_stage` table; permit governing-package and schema-artifact-catalog claims for one accepted path to coexist as selected/secondary evidence when all applicable path, schema, role, hash, semantic-identity, and physical-winner checks reconcile; add no independent classification-registry artifact, owner arrays, alternative role/stage pairs, or undeclared relationship fields; reject absent, ambiguous, same-kind duplicate, unreadable, unregistered, terminal-owner, or contradictory owner classifications with `STOP_FINALIZATION_INVENTORY_INVALID`; and validate snapshot, prepared-unit, superseded-unit, race-loser, row-batch, terminal-source, and secondary-owner relationships separately during closure;

---

## 5. Directly affected test replacement

Replace the normal-inventory owner-selection test paragraph supplied by Delta Packet 05 §5 with the following text.

Normal-inventory owner-selection tests construct the complete effective base §21.4.2 claim set for each normalized path and exercise every selected owner kind that may validly classify a non-self-excluded normal-inventory path. Positive cases require exactly one inventory row per normalized included path and prove: governing-package selection with a compatible schema-artifact-catalog secondary claim; schema-artifact-catalog fallback; exact selected-owner `registered_object_role` use rather than `schema_ref`; authorization-use and capture relation stages; detached pre-run attachment stage; every prepared structural/object stage that can occur on a non-self-excluded included path; each canonical fence `event_kind` supported by effective §5.2.2 with an exact linked plan whose `unit_kind` is equal; snapshot history and current-view ownership for `capture`, `analysis_compatibility`, and `analysis_strict`, each with the exact family stage and a linked `SNAPSHOT_PUBLICATION` plan whose `subject_family` is equal; compatible lower-precedence prepared/recovery claims; permitted physical-winner inequality only under independently proven equal semantics; and disposition-neutral selected role/stage.

Counterexamples require `STOP_FINALIZATION_INVENTORY_INVALID` for: no claim; selected unregistered owner; two distinct claims in the selected owner kind; two governing-package entries for one path; malformed catalog fallback producer; deriving `artifact_role` from `schema_ref`; path, schema, registered-role, required-hash, or semantic-identity mismatch; unproved physical-winner difference; structural/member grammar contradiction; a fence manifest read as though it contained `unit_kind`; missing or unreadable fence manifest or linked plan; manifest/plan hash or prepared-unit-ID mismatch; `manifest.event_kind != plan.unit_kind`; unsupported fence `event_kind`; missing, unreadable, or non-domain snapshot `audit_family`; snapshot linked plan with `unit_kind != SNAPSHOT_PUBLICATION`; `plan.subject_family != audit_family`; selected `NORMAL_FINALIZATION_OBJECT`; selected `CONFLICT_FINALIZATION_OBJECT`; unreadable selected owner without independently bound metadata; secondary claim emitting another role/stage pair; duplicate path row; disposition-derived replacement of role/stage; owner array; undeclared field; or omitted secondary-relationship proof. A governing-package claim plus one compatible catalog claim must pass and must not be treated as duplicate candidates.

No positive normal-inventory test may construct a row selected by `NORMAL_FINALIZATION_OBJECT` or `CONFLICT_FINALIZATION_OBJECT`. Independent tests for normal/conflict terminal publication and mutual exclusion remain unchanged. If the unchanged `NORMAL_FINALIZATION` row in the prepared-unit mapping is tested, it is tested only as a prepared-plan schema/stage derivation outside a normal-inventory included-row claim, because the selected normal-finalization prepared subtree remains self-excluded.

---

## 6. Directly affected traceability replacement

Replace the traceability row supplied by Delta Packet 05 §6 with the following text.

### 6.1 Replacement traceability row immediately after `final snapshot and complete loser inventory closure`

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| normal-inventory authoritative-owner stage derivation and terminal-owner exclusion | §§5.2, 8.6, 17.5, 21.2, 21.4.2, 26–27 | collect all registered claims; select one owner by existing owner-kind precedence; `artifact_role=selected_owner.registered_object_role`; fence stage from persisted `fence_unit_manifest_v23.event_kind` plus exact linked-plan equality; snapshot stage from canonical commit `audit_family` plus linked `SNAPSHOT_PUBLICATION`/`subject_family` equality; closed three-family mapping; selected normal/conflict terminal owners invalid for normal-inventory rows; compatible secondary claims emit no second pair; one unique normalized path row | `STOP_FINALIZATION_INVENTORY_INVALID` for absent/unregistered owner, same-kind multiplicity, terminal owner, unreadable or unsupported fence evidence, fence event/plan mismatch, invalid or plan-unequal snapshot family, incompatible secondary claim, unproved physical-winner difference, duplicate row, or undeclared field | effective §§24.14–24.15 normal-inventory tests as replaced by Delta Packet 06 §5; independent terminal-publication tests unchanged |

---

## 7. Unchanged-text and authorization statement

Except for the exact replacements in this packet, every byte of the base amendment, Correction Packet 01, Delta Packet 02, Delta Packet 03, Delta Packet 04, and Delta Packet 05 remains unchanged and continues to govern in the stated application order. In particular:

- Delta Packet 04 §5.2.2 and its complete `unit_kind → producer_stage` table remain unchanged;
- the independent normal-finalization and conflict-finalization publication profiles, self-exclusions, markers, sidecars, and mutual-exclusion rules remain unchanged; and
- this packet creates no new schema, artifact, owner kind, inventory field, or authorization.

This packet authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
