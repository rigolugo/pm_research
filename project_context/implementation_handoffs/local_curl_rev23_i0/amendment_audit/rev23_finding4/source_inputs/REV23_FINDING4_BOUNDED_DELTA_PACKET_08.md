# REV23 Finding 4 — Bounded Delta Packet 08

## 1. Exact inputs and application order

Apply this packet only after these exact inputs, in this order:

1. base amendment SHA-256 `3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563`;
2. Correction Packet 01 SHA-256 `b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9`;
3. Delta Packet 02 SHA-256 `184da5779afc301255cd6532e456727380f14e4f0f32bad30f2b4bd010bb76c2`;
4. Delta Packet 03 SHA-256 `4bb5b24561dc2afc378dd36c0a69bfd178b18287e4783bcb14bde18740e1382c`;
5. Delta Packet 04 SHA-256 `b942b67f688ee4b06d479ee8afa47193802d2969f116a7c4b1edcd247d80f433`;
6. Delta Packet 05 SHA-256 `5bf5788f2298267c881b1c2a0d612617ce0a470d07cef62310752ded43d74fa1`;
7. Delta Packet 06 SHA-256 `7d1e396655455b411f6a2e0bedf70eae0dc235458ec4469046ede92f5381c945`;
8. Delta Packet 07 SHA-256 `7a61f87979818994480c9b20c25d6906377839734c70f47a0d6635af104f4d64`;
9. this Delta Packet 08.

A byte mismatch in any prerequisite prevents application. This packet changes only the undeclared normal-inventory owner-metadata serialization introduced by Delta Packet 07 and its directly dependent materialization, tests, and traceability.

---

## 2. Exact replacements in effective §5.2.1

### 2.1 Replace the Delta Packet 07 text beginning `Select one deterministic selected_owner_representative`

Replace that paragraph, its tuple block, and the following paragraph ending `alternative (artifact_role,producer_stage) pair` in full with:

No owner-claim representative participates in normal-inventory row production. After the complete `selected_owner_kind_claim_cohort` has independently validated and satisfied every compatible-cohort requirement in this section, all same-kind cohort claims and all compatible lower-precedence claims remain external finalization-closure evidence. Their owner-registry paths, owner-registry file hashes, owner-entry keys, owner-entry logical hashes, sequences, ordinals, and other owner-specific coordinates are validated by reopening the exact immutable governing bytes, but none of those owner metadata values is serialized into `artifact_inventory_entry`.

The accepted closed `artifact_inventory_entry` schema remains exactly these six fields and no others:

```text
artifact_role
file_sha256
logical_sha256
path
producer_stage
size_bytes
```

Fields named `owner_kind`, `owner_registry_path`, `owner_registry_file_sha256`, `owner_entry_key`, or `owner_entry_logical_sha256` are not members of `artifact_inventory_entry`. Any occurrence of any such field, any owner array, or any other undeclared field in a normal-inventory row is `STOP_FINALIZATION_INVENTORY_INVALID`.

A validator may traverse owner claims in a fixed internal order solely to make validation diagnostics reproducible. If the four-component unsigned UTF-8 tuple `(owner_entry_key,owner_registry_path,owner_registry_file_sha256,owner_entry_logical_sha256)` is used for that purpose, it is validation-process ordering only. It creates no artifact, selected representative, persisted field, semantic input, or owner disposition and has no effect on inventory row bytes, inventory row order, row logical hashes, inventory semantic hashes, `artifact_role`, `producer_stage`, canonical-object selection, or finalization outcome. Permuting claim discovery or traversal order must produce byte-identical six-field inventory rows and identical validation results.

### 2.2 Replace the Delta Packet 07 paragraph and projection beginning `The one normal-inventory row derives its pair`

Replace that paragraph, its projection, and the following explanatory paragraph in full with:

Exactly one normal-inventory row is derived for the unique normalized included path from the validated compatible selected-owner-kind cohort and the unique canonical included object:

```text
path             = unique normalized included path
size_bytes       = exact byte size of the unique canonical included object
file_sha256      = SHA256(exact bytes of the unique canonical included object)
logical_sha256   = common validated target logical SHA-256, or null exactly when the existing registered role-specific nullability rule requires null
artifact_role    = common exact registered_object_role of every selected-owner-kind cohort claim
producer_stage   = common exact validated producer stage of every selected-owner-kind cohort claim
```

For `logical_sha256`, if the existing role-specific rule requires a non-null logical hash, every applicable claim must recompute the same lowercase SHA-256 value and that value is stored. If the existing role-specific rule requires null, every applicable claim must validate that null is required and the row stores null. Mixed null/non-null requirements or unequal non-null values are `STOP_FINALIZATION_INVENTORY_INVALID`.

The unique canonical included object determines only `path`, `size_bytes`, and `file_sha256`. Cohort consensus determines only `logical_sha256`, `artifact_role`, and `producer_stage` under the rules above. No owner metadata field is copied into the row, and `artifact_role` is never derived from `schema_ref`, `content_schema_id`, disposition, recovery-source label, claim discovery order, or traversal order.

### 2.3 Replace the Delta Packet 07 paragraph beginning `Every claim not used as the top-level encoding representative`

Replace that paragraph in full with:

Every compatible same-kind claim and every compatible lower-precedence claim remains external finalization-closure evidence. Each claim must be reopened and validated against its immutable owner-registry bytes, complete-file hash, entry key, entry logical hash, linked canonical object, registered semantic identity, registered role, applicable logical hash, and owner-specific relationship rules. No claim emits an additional inventory row, an alternative `(artifact_role,producer_stage)` pair, or any owner metadata field. Removing, changing, making unreadable, or failing to validate any required external owner claim produces `STOP_FINALIZATION_INVENTORY_INVALID` even though that claim's owner metadata is not serialized into the six-field row.

---

## 3. Exact replacements in effective §5.2.3

### 3.1 Replace item 4 supplied by Delta Packet 07

Replace item 4 in full with:

4. Form the complete `selected_owner_kind_claim_cohort` from every distinct claim in the highest-precedence nonempty owner kind; independently validate every cohort claim; require cohort compatibility under effective §5.2.1; and reject `UNREGISTERED_DURABLE_OBJECT`, `NORMAL_FINALIZATION_OBJECT`, and `CONFLICT_FINALIZATION_OBJECT` as normal-inventory owners. Cohort multiplicity alone is not invalid. No representative is selected and no owner metadata is serialized into the inventory row.

### 3.2 Replace item 6 supplied by Delta Packet 07

Replace item 6 in full with:

6. Validate every compatible same-kind claim as retained external ownership evidence under the complete cohort rules and validate every lower-precedence claim under the applicable lower-precedence compatibility dimensions in §5.2.1. No same-kind or lower-precedence claim emits another inventory row, an alternative role/stage pair, or any owner metadata field. Claim traversal order is validation-process-only and cannot affect any of the six persisted row fields or any inventory hash.

### 3.3 Replace item 8 supplied by Delta Packet 07 and amended through Delta Packet 06

Replace item 8 in full with:

8. An incompatible selected-owner-kind cohort; a same-kind claim whose normalized path, schema, registered role, registered semantic identity, target logical hash, canonical-object identity, or producer stage disagrees; a same-kind physical-object difference lacking the complete existing canonical-winner/adoption proof; a `SNAPSHOT_HISTORY_OBJECT` cohort whose owning publications resolve to different or non-domain `audit_family` values or different producer stages; no registered claim; unreadable required owner metadata without independently bound expected metadata; structural/member grammar contradiction; a fence owner with missing, unreadable, unsupported, or mismatched `event_kind`/linked-plan evidence; a snapshot owner with missing, unreadable, non-domain, or plan-unequal `audit_family`; selection of `NORMAL_FINALIZATION_OBJECT`, `CONFLICT_FINALIZATION_OBJECT`, or `UNREGISTERED_DURABLE_OBJECT`; selected-owner-kind role/stage derivation failure; incompatible lower-precedence claim; any required same-kind or lower-precedence claim omitted from external closure validation; any secondary claim emitting another role/stage pair; any owner metadata field, owner array, or other undeclared field added to `artifact_inventory_entry`; claim discovery or traversal order changing any of the six persisted row fields or any inventory hash; duplicate inventory output row; or disposition-derived role/stage produces `STOP_FINALIZATION_INVENTORY_INVALID`. Multiple compatible claims in the selected owner kind do not produce a stop.

---

## 4. Directly affected materialization replacement

Replace the base §26 item 11 text supplied by Delta Packet 07 §4 in full with:

11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; preserve the exact closed six-field `artifact_inventory_entry` schema `(artifact_role,file_sha256,logical_sha256,path,producer_stage,size_bytes)` and materialize exactly one row per unique normalized included path; collect all effective base §21.4.2 claims and select the highest-precedence nonempty owner kind; form and independently validate the complete same-kind claim cohort; permit multiple same-kind claims only when all applicable normalized-path, content-schema, registered-role, registered-semantic-identity, target-logical-hash, canonical-object, physical-winner, and producer-stage requirements agree; derive `path`, `size_bytes`, and `file_sha256` from the unique canonical included object; derive `logical_sha256`, `artifact_role`, and `producer_stage` from the cohort's common validated values under the existing logical-hash nullability rule; serialize no owner metadata, owner array, alternative role/stage pair, or undeclared relationship field; retain and validate every compatible same-kind and lower-precedence claim as external closure evidence by reopening its immutable governing bytes; ensure claim discovery or traversal order cannot affect row bytes, row order, logical hashes, semantic hashes, role, stage, or disposition; preserve the unchanged fence, snapshot-family, prepared structural/object, reused-partition, terminal-owner rejection, physical-winner, and disposition-neutral derivation rules from Delta Packets 05–07; and reject absent, unreadable, incompatible, unregistered, terminal-owner, undeclared-field, order-dependent, or otherwise contradictory classifications with `STOP_FINALIZATION_INVENTORY_INVALID`;

---

## 5. Directly affected test replacement

Replace the normal-inventory test text supplied by Delta Packet 07 §5 in full with:

Normal-inventory owner-selection tests construct the complete effective base §21.4.2 claim set for each normalized path and exercise every selected owner kind that may validly classify a non-self-excluded normal-inventory path. Positive cases require exactly one inventory row per normalized included path and prove: the row schema is exactly `(artifact_role,file_sha256,logical_sha256,path,producer_stage,size_bytes)`; `path`, `size_bytes`, and `file_sha256` equal the unique canonical included object; `logical_sha256` follows the existing role-specific nullability rule and equals the cohort's common validated logical semantics when non-null; `artifact_role` equals the cohort's common exact `registered_object_role`; `producer_stage` equals the cohort's common validated producer stage; one immutable partition reused by multiple valid `SNAPSHOT_HISTORY_OBJECT` owners across different sequences and ordinals still emits one row; all compatible same-kind and lower-precedence claims remain reopened and validated as external closure evidence; governing-package and schema-artifact-catalog claims may coexist when compatible; fence and snapshot-family stage derivations remain as amended through Delta Packet 06; permitted physical-winner inequality requires the complete existing equal-semantics adoption proof; and disposition remains role/stage neutral.

Order-independence tests must permute discovery order, filesystem enumeration order, insertion order, map iteration order, and any optional validation traversal order and prove byte-identical values for all six row fields, byte-identical row ordering, byte-identical row logical hashes, and byte-identical inventory semantic hashes. No test fixture may serialize a claim representative or any owner metadata into `artifact_inventory_entry`.

Counterexamples require `STOP_FINALIZATION_INVENTORY_INVALID` for: adding `owner_kind`, `owner_registry_path`, `owner_registry_file_sha256`, `owner_entry_key`, `owner_entry_logical_sha256`, an owner array, or any other undeclared field to `artifact_inventory_entry`; deriving a row field from a representative or claim traversal order; changing claim discovery order and obtaining different row bytes or hashes; removing a required external same-kind or lower-precedence owner claim; changing an external claim's owner-registry path, owner-registry file hash, owner-entry key, owner-entry logical hash, registered role, semantic identity, logical hash, canonical-object binding, audit family, producer stage, or required linked evidence; making required external owner metadata unreadable; same-kind path, schema, role, semantic-identity, logical-hash, canonical-object, physical-winner, audit-family, or producer-stage disagreement; incompatible lower-precedence evidence; duplicate path row; or omitted secondary-relationship proof. Detection of changed, removed, or unreadable owner metadata must occur during external closure validation even though none of that metadata is stored in the six-field row.

Independent normal/conflict terminal-publication tests and their mutual-exclusion rules remain unchanged. No positive normal-inventory test may construct a row selected by `NORMAL_FINALIZATION_OBJECT` or `CONFLICT_FINALIZATION_OBJECT`.

---

## 6. Directly affected traceability replacement

Replace the traceability row supplied by Delta Packet 07 §6 in full with:

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| normal-inventory six-field row derivation from compatible owner cohort with external owner-evidence closure | §§5.2, 8.6, 17.5, 21.2, 21.4.2, 26–27 | exact closed row schema `(artifact_role,file_sha256,logical_sha256,path,producer_stage,size_bytes)`; one unique normalized-path row; unique canonical object supplies path/size/file hash; compatible selected-owner-kind cohort supplies common logical hash under existing nullability, registered role, and producer stage; no representative or owner metadata is serialized; every same-kind and lower-precedence claim remains externally reopened and validated; discovery/traversal order is nonsemantic and cannot affect row or inventory bytes | `STOP_FINALIZATION_INVENTORY_INVALID` for undeclared owner field or array, incompatible cohort or lower-precedence claim, missing/changed/unreadable external owner evidence, order-dependent row production, duplicate row, role/stage disagreement, invalid logical-hash nullability, or omitted closure proof; compatible multiplicity continues with one row | positive six-field derivation, reused-partition one-row case, complete external-claim validation, and order-permutation invariance; counterexamples for every prohibited owner field, changed/removed/unreadable external claim metadata, incompatible cohort dimensions, order-dependent bytes, and duplicate rows |

---

## 7. Unchanged-text and authorization statement

Except for the exact replacements in this packet, every byte of the base amendment, Correction Packet 01, and Delta Packets 02–07 remains unchanged and continues to govern in the stated application order. In particular, all compatible-cohort rules, reused-partition handling, owner-kind precedence, producer-stage mappings, canonical-winner/adoption rules, one-row-per-path cardinality, terminal-profile exclusions, and independent normal/conflict terminal publication rules not expressly replaced above remain unchanged.

This packet authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
