# REV23 Finding 4 — Bounded Delta Packet 04

## 1. Exact inputs and application order

Apply this packet only after these exact inputs, in this order:

1. base amendment SHA-256 `3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563`;
2. Correction Packet 01 SHA-256 `b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9`;
3. Delta Packet 02 SHA-256 `184da5779afc301255cd6532e456727380f14e4f0f32bad30f2b4bd010bb76c2`;
4. Delta Packet 03 SHA-256 `4bb5b24561dc2afc378dd36c0a69bfd178b18287e4783bcb14bde18740e1382c`;
5. this Delta Packet 04.

A byte mismatch in any prerequisite prevents application. This packet creates no independent classification-registry artifact.

---

## 2. Exact replacement for Delta Packet 03 §5.2

Replace Delta Packet 03 §5.2 in full with the following text.

### 5.2 Deterministic normal-inventory path classification from registered governing evidence

Each normal-inventory entry uses the already declared `artifact_inventory_entry` row schema and adds no field. For one unique normalized included path, derive exactly one `(artifact_role,producer_stage)` pair from persisted governing evidence by the following ordered procedure.

#### 5.2.1 Normalization and candidate collection

The candidate path is the exact normalized run-relative or package-relative path already required by the governing path contract. A path containing an absolute prefix, `.` segment, `..` segment, empty segment, backslash, duplicate slash, symlink traversal, or non-normalized UTF-8 form is invalid and produces `STOP_FINALIZATION_INVENTORY_INVALID`.

Collect candidates in these four precedence classes, from highest to lowest:

1. **Exact canonical target/path registration.** Match the normalized path to an exact accepted governing-package entry or exact/dynamic accepted artifact-catalog target after substituting only its registered path variables. For an accepted artifact-catalog target, derive `artifact_role` as the exact registered `schema_ref` and `producer_stage` as the exact registered `producer` string. For an accepted governing-package entry, derive `artifact_role` as the exact manifest `role` and `producer_stage="GOVERNING_PACKAGE"`.
2. **Registered prepared structural-member path.** Match exactly one of the eight structural members under `prepared_evidence/<unit_kind>/<prepared_unit_id>/` after reopening and validating the committed prepared directory, its plan, and descriptor. The exact role mapping is:

   | Exact structural member | `artifact_role` |
   |---|---|
   | `CLAIM_SCOPE.json` | `PREPARED_CLAIM_SCOPE` |
   | `CLAIM_SCOPE.sha256` | `PREPARED_CLAIM_SCOPE_SIDECAR` |
   | `CLAIM_SEMANTIC.json` | `PREPARED_CLAIM_SEMANTIC` |
   | `CLAIM_SEMANTIC.sha256` | `PREPARED_CLAIM_SEMANTIC_SIDECAR` |
   | `PREPARATION_PLAN.json` | `PREPARATION_PLAN` |
   | `PREPARATION_PLAN.sha256` | `PREPARATION_PLAN_SIDECAR` |
   | `PREPARED_UNIT.json` | `PREPARED_UNIT_DESCRIPTOR` |
   | `PREPARED_UNIT.sha256` | `PREPARED_UNIT_DESCRIPTOR_SIDECAR` |

   `producer_stage` is derived only from the validated `unit_kind` by §5.2.2.
3. **Validated prepared object member.** Match exactly `prepared_evidence/<unit_kind>/<prepared_unit_id>/objects/<object_ordinal_10d>.bin`, reopen the validated `prepared_evidence_object_v23` entry at that ordinal, and require the path, ordinal, size, complete-file hash, publication mode, canonical target, sidecar pairing, and logical-hash nullability to reconcile. Derive `artifact_role` as that entry's exact closed `object_role`; derive `producer_stage` only from the validated `unit_kind` by §5.2.2.
4. **Registered immutable recovery source.** This class applies only when the path is named as a durable immutable recovery source by a readable validated owner or prepared descriptor and classes 1–3 do not classify the path. Reopen the exact registered owner and derive the pair as follows:

   | Registered immutable owner | `artifact_role` | `producer_stage` |
   |---|---|---|
   | governing-package entry | exact entry `role` | `GOVERNING_PACKAGE` |
   | accepted artifact-catalog entry | exact entry `schema_ref` | exact entry `producer` |
   | prepared-plan object whose source is its committed private `objects/<ordinal>.bin` | exact validated `prepared_evidence_object_v23.object_role` | §5.2.2 mapping for its `unit_kind` |
   | snapshot history or current-view owner | exact registered snapshot object role | §5.2.2 `SNAPSHOT_PUBLICATION` family branch |
   | fence-unit owner | exact registered fence object role | §5.2.2 mapping for the owning fence `unit_kind` |
   | authorization-use relation-version owner | `AUTHORIZATION_USE_ROW_BATCH` or its exact paired sidecar role | `V7 authorization-use ledger` |
   | capture relation-version owner | `CAPTURE_ROW_BATCH` or its exact paired sidecar role | `V7 capture runner` |
   | normal-finalization owner | exact registered normal-finalization object role | `V10 normal finalizer` |
   | conflict-finalization owner | exact registered conflict-finalization object role | `V10 conflict finalizer` |

`UNREGISTERED_DURABLE_OBJECT` is not a registered immutable recovery-source classification. A recovery source that cannot be classified by one row above produces `STOP_FINALIZATION_INVENTORY_INVALID`.

#### 5.2.2 Complete closed `unit_kind → producer_stage` mapping

The following table is complete for every effective `prepared_evidence_plan_v23.unit_kind`. The strings in the right column are the exact normal-inventory `producer_stage` values for prepared structural members and prepared object members.

| Effective `unit_kind` | Additional discriminator | Exact `producer_stage` |
|---|---|---|
| `SNAPSHOT_PUBLICATION` | `subject_family=capture` | `V7 capture snapshot finalizer` |
| `SNAPSHOT_PUBLICATION` | `subject_family=analysis_compatibility` | `V8 compatibility snapshot finalizer` |
| `SNAPSHOT_PUBLICATION` | `subject_family=analysis_strict` | `V8 strict snapshot finalizer` |
| `FENCE_ACQUIRED` | none | `V7 authorization/capture fence coordinator` |
| `AUTHORIZATION_USE_EVENT_COMMITTED` | none | `V7 authorization-use ledger` |
| `REQUEST_RESERVED_COMMITTED` | none | `V7 authorization-use ledger` |
| `CAPTURE_STARTED_COMMITTED` | none | `V7 capture runner` |
| `CAPTURE_TERMINAL_COMMITTED` | none | `V7 capture runner` |
| `CAPTURE_SNAPSHOT_COMMITTED` | none | `V7 capture snapshot finalizer` |
| `CANCELLATION_CHECKPOINT_AND_ROW_COMMITTED` | none | `V7 authorization-use ledger` |
| `CONTINUATION_CHECKPOINT_AND_ACTIVATION_COMMITTED` | none | `V7 authorization-use ledger` |
| `FENCE_RELEASED` | none | `V7 authorization/capture fence coordinator` |
| `NORMAL_FINALIZATION` | none | `V10 normal finalizer` |

No other `unit_kind`, snapshot family, or producer-stage value is valid for prepared structural or object-member classification. A `SNAPSHOT_PUBLICATION` unit with null or non-domain `subject_family` is unclassifiable and produces `STOP_FINALIZATION_INVENTORY_INVALID`.

#### 5.2.3 Total precedence and contradiction handling

Classification is total and deterministic:

1. Within each precedence class, zero or one candidate is permitted. More than one candidate in one class produces `STOP_FINALIZATION_INVENTORY_INVALID`.
2. Select the first nonempty class in the order 1 → 2 → 3 → 4.
3. A lower-precedence recovery or relationship reference may coexist with the selected class only when it independently derives the identical `(artifact_role,producer_stage)` pair and identical normalized path. It does not create another inventory row.
4. A path matching both the prepared structural-member grammar and the prepared object-member grammar is invalid even if the proposed pair is textually equal; the grammars are disjoint by contract. This produces `STOP_FINALIZATION_INVENTORY_INVALID`.
5. A structural-path classification that disagrees with the embedded object's role or unit-derived stage produces `STOP_FINALIZATION_INVENTORY_INVALID`.
6. An exact canonical registration that disagrees with any lower-precedence owner/recovery classification produces `STOP_FINALIZATION_INVENTORY_INVALID`; precedence never suppresses contradictory governing evidence.
7. No candidate in all four classes produces `STOP_FINALIZATION_INVENTORY_INVALID`.
8. A selected, `SUPERSEDED_BY_CANONICAL_WINNER`, or `UNSELECTED_CANONICAL_RACE_LOSER` disposition never changes a canonical path's role or stage. Disposition and secondary ownership are validation relationships, not row-classification inputs.

The normal inventory continues to contain exactly one row per unique normalized included path. Snapshot-sequence membership, current-head membership, prepared-unit membership, semantic supersession, race-loser withdrawal, row-batch ownership, and terminal-source relationships are validated separately by reopening their governing bytes. No owner array, secondary-role array, or other undeclared field is added to the inventory row.

---

## 3. Directly dependent materialization clause

Replace Delta Packet 03 §6.4 in full with the following text.

### 6.4 Replacement for base §26 item 11

11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; materialize normal final-inventory cardinality as exactly one row per unique normalized included path; derive each row's canonical `(artifact_role,producer_stage)` only through effective §5.2's four-class precedence and complete `unit_kind → producer_stage` table; add no independent classification-registry artifact and no owner arrays or undeclared relationship fields; reject absent, ambiguous, overlapping, or contradictory classifications with `STOP_FINALIZATION_INVENTORY_INVALID`; and validate snapshot, prepared-unit, superseded-unit, race-loser, row-batch, and terminal-source relationships separately during closure;

---

## 4. Directly dependent producer-consumer row

Replace Delta Packet 03 §6.8 in full with the following text.

### 6.8 Replacement row in base §27 immediately after `normal V10 inventory/marker`

| Artifact | Producer | Consumer | Cardinality | Lifecycle |
|---|---|---|---|---|
| normal inventory path entry | V10 normal finalizer applying effective §5.2 to registered governing bytes | terminal validator, Sentinel | exactly one row per unique normalized included path | immutable within committed inventory; role/stage derived without a new registry artifact; secondary relationships validated externally without extra fields |

---

## 5. Directly dependent tests

In Delta Packet 03 §7.5, replace only the paragraph beginning `Normal-inventory tests construct paths` with the following text.

Normal-inventory classification tests enumerate all four effective §5.2 precedence classes and every row of the complete `unit_kind → producer_stage` table. Positive cases require exactly one row per normalized included path and prove: exact artifact-catalog and governing-package extraction; all eight prepared structural roles; prepared object role extraction at exact ordinal; each snapshot-family stage branch; every fence/finalization unit kind; registered immutable recovery-source classification; compatible lower-priority relationship references; and disposition-neutral canonical role/stage. Counterexamples require `STOP_FINALIZATION_INVENTORY_INVALID` for: no match; two matches within one class; two exact canonical registrations; structural/member grammar overlap; structural role or stage disagreeing with the embedded object; canonical and recovery-owner disagreement; unknown `unit_kind`; invalid snapshot family; recovery source without registered canonical classification; duplicate path row; disposition-derived replacement of role/stage; owner array; undeclared field; or omitted secondary relationship proof. No test may read or depend on an independent inventory-classification registry artifact.

---

## 6. Directly dependent traceability row

Replace Delta Packet 03 §8.4 in full with the following text.

### 8.4 Replacement traceability row immediately after `final snapshot and complete loser inventory closure`

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| normal inventory one-row-per-path classification closure | §§5.2, 8.6, 21.2, 26–27 | four-class evidence precedence; complete unit-kind/family stage mapping; one unique normalized path row; no independent registry; compatible secondary relationships validated outside row schema | `STOP_FINALIZATION_INVENTORY_INVALID` for absent, duplicate, overlapping, ambiguous, unregistered, or contradictory role/stage derivation, undeclared fields, or missing relationship proof | §§24.14–24.15 as replaced by Delta Packet 03 §7.5 and this packet §5 |

---

## 7. Exact cross-reference update

Replace Delta Packet 03 §9 item 8 with the following text:

8. In base §26, replace only items 3, 5, and 8 with Delta Packet 03 §§6.1–6.3, and replace item 11 with this packet §3. Do not renumber any item. In base §27, apply Delta Packet 03 §§6.5–6.7 and replace Delta Packet 03 §6.8 with this packet §4. Apply only the normal-inventory test paragraph and traceability-row replacements in this packet §§5–6.

---

## 8. Unchanged-text and authorization statement

Except for the exact replacements in this packet, every byte of the base amendment, Correction Packet 01, Delta Packet 02, and Delta Packet 03 remains unchanged and continues to govern in the stated application order.

This packet authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
