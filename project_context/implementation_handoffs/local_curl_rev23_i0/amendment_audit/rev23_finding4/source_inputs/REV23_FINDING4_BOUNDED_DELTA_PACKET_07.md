# REV23 Finding 4 — Bounded Delta Packet 07

## 1. Exact inputs and application order

Apply this packet only after these exact inputs, in this order:

1. base amendment SHA-256 `3bbaea364c9ac6aab977347e4c2753d5c57ceea564a36a939f8fb4352cf65563`;
2. Correction Packet 01 SHA-256 `b58229624ba5df3bc9266748059d757fb12a6e8730f0bc288bb77e77a34b86a9`;
3. Delta Packet 02 SHA-256 `184da5779afc301255cd6532e456727380f14e4f0f32bad30f2b4bd010bb76c2`;
4. Delta Packet 03 SHA-256 `4bb5b24561dc2afc378dd36c0a69bfd178b18287e4783bcb14bde18740e1382c`;
5. Delta Packet 04 SHA-256 `b942b67f688ee4b06d479ee8afa47193802d2969f116a7c4b1edcd247d80f433`;
6. Delta Packet 05 SHA-256 `5bf5788f2298267c881b1c2a0d612617ce0a470d07cef62310752ded43d74fa1`;
7. Delta Packet 06 SHA-256 `7d1e396655455b411f6a2e0bedf70eae0dc235458ec4469046ede92f5381c945`;
8. this Delta Packet 07.

A byte mismatch in any prerequisite prevents application. This packet changes only selected-owner-kind multiplicity, deterministic representative selection, and the directly dependent materialization, test, and traceability text.

---

## 2. Exact replacements in effective Delta Packet 05 §5.2.1

Apply the following replacements to Delta Packet 05 §5.2.1 after applying Delta Packet 06.

### 2.1 Replace the paragraph beginning `After identical-discovery collapse`

Replace that paragraph in full with:

After identical-discovery collapse, let `selected_owner_kind` be the highest-precedence nonempty owner kind under effective base §21.4.2. Collect **every** remaining distinct claim of that owner kind into one `selected_owner_kind_claim_cohort`. Mere multiplicity in this cohort is not an error. A selected `UNREGISTERED_DURABLE_OBJECT`, `NORMAL_FINALIZATION_OBJECT`, or `CONFLICT_FINALIZATION_OBJECT` remains invalid for a normal-inventory row under Delta Packet 06 and produces `STOP_FINALIZATION_INVENTORY_INVALID`.

Every claim in `selected_owner_kind_claim_cohort` must first validate independently against its own immutable owner-registry bytes, complete-file hash, owner-entry key, owner-entry logical hash, owner-kind-specific key grammar, and every owner-kind-specific linked object required by the effective contract. The cohort is compatible if and only if all of the following are true:

1. every claim names the exact same normalized included `(path_root,path)` as the candidate inventory row;
2. every claim resolves to the same effective `content_schema_id`;
3. every claim resolves to the same exact `registered_object_role`;
4. every claim's owner-kind-specific registered semantic-identity projection is valid and byte-identical to the projection of every other cohort claim;
5. every claim resolves to the same target logical semantics and the same target logical hash under the registered schema;
6. every claim resolves to one unique canonical object identity for the included path; the canonical object's normalized path, complete-file bytes, complete-file SHA-256, and size are unique, while a claim's different expected physical object is permitted only when the existing canonical-winner/adoption rules independently validate the claim, prove equal registered semantic identity and equal target logical semantics, and bind that claim to the same canonical physical winner;
7. every claim derives the same exact `artifact_role` and the same exact `producer_stage` under effective §§5.2.1–5.2.2 as amended through Delta Packet 06; and
8. every owner-registry path, owner-registry file hash, owner-entry key, owner-entry logical hash, sequence, ordinal, or other owner-specific relationship coordinate is valid for that claim. Such relationship coordinates may differ between compatible claims when the governing owner schema permits different immutable owners to reference the same canonical object; those differences do not by themselves change target semantics or create a second inventory row.

Any failure of items 1–8 is an incompatible same-kind cohort and produces `STOP_FINALIZATION_INVENTORY_INVALID`. Physical-byte inequality between an unselected physical candidate and the canonical winner is not by itself a contradiction, but it is never accepted without the complete existing semantic-adoption proof. No precedence rule, representative choice, or disposition may suppress an actual cohort contradiction.

For multiple `SNAPSHOT_HISTORY_OBJECT` claims on one reused immutable partition, different snapshot sequences, `owner_entry_key` values, `owner_registry_path` values, owner-registry file hashes, owner-entry logical hashes, and partition ordinals are expressly permitted. Every owning snapshot publication commit must nevertheless validate independently and resolve to the same exact `audit_family`; every claim must register the same partition object role and content schema, resolve to the same canonical partition identity and partition logical semantics, and derive the same producer stage from that common `audit_family`. A different `audit_family`, producer stage, semantic identity, partition logical hash, incompatible canonical-object claim, or unproved physical-winner difference produces `STOP_FINALIZATION_INVENTORY_INVALID`.

Select one deterministic `selected_owner_representative` from the compatible cohort by ascending component-wise unsigned UTF-8 byte order over this exact tuple:

```text
(
  owner_entry_key,
  owner_registry_path,
  owner_registry_file_sha256,
  owner_entry_logical_sha256
)
```

All four tuple components are non-null for every owner kind that may validly classify a normal-inventory row. SHA-256 components are their registered lowercase hexadecimal strings. Compare the first component; if equal, compare the second; then the third; then the fourth. No discovery ordinal, filesystem enumeration order, insertion order, timestamp, process identity, or implementation map order participates. Failure to obtain one unique first tuple after identical-discovery collapse is `STOP_FINALIZATION_INVENTORY_INVALID`.

The representative supplies only the normal-inventory row's top-level owner encoding metadata: `owner_kind`, `owner_registry_path`, `owner_registry_file_sha256`, `owner_entry_key`, and `owner_entry_logical_sha256`. It does not erase, supersede, or relax validation of any other same-kind claim. Every nonrepresentative compatible same-kind claim remains retained secondary ownership evidence and must be validated during finalization closure. It emits no additional inventory row and no alternative `(artifact_role,producer_stage)` pair.

### 2.2 Replace the paragraph and projection beginning `The one normal-inventory row derives its pair`

Replace that paragraph and its following projection in full with:

The one normal-inventory row derives its pair from the validated compatible selected-owner-kind cohort, using the deterministic representative only for top-level owner encoding metadata:

```text
selected_owner = selected_owner_representative
artifact_role  = common validated selected_owner_kind_claim_cohort registered_object_role
producer_stage = common validated producer_stage_for every selected_owner_kind_claim_cohort member
```

`selected_owner.registered_object_role` must equal the cohort's common validated `registered_object_role`; the row therefore remains equivalent to `artifact_role = selected_owner.registered_object_role` after cohort validation. `artifact_role` is never derived from `schema_ref`, `content_schema_id`, a disposition, a lower-precedence claim, or a recovery-source label. The representative cannot select a role or stage that differs from any compatible cohort member.

### 2.3 Replace the paragraph beginning `Every nonselected claim`

Replace that paragraph in full with:

Every claim not used as the top-level encoding representative is validated secondary ownership evidence of exactly one of these two kinds:

1. a **compatible nonrepresentative same-kind claim**, which must satisfy the complete selected-owner-kind cohort rules above; or
2. a **compatible lower-precedence claim**, which must satisfy the five lower-precedence compatibility dimensions already specified in this section.

Neither kind emits, replaces, or votes on the selected inventory row's `(artifact_role,producer_stage)` pair. Every compatible nonrepresentative same-kind claim remains part of the retained ownership proof and every compatible lower-precedence claim remains part of the retained secondary-provenance proof. A nonrepresentative claim is not discarded merely because it did not win the deterministic representative ordering.

---

## 3. Exact replacements in effective Delta Packet 05 §5.2.3

Apply these replacements after Delta Packet 06 §3.2.

### 3.1 Replace item 4

Replace item 4 in full with:

4. Form the complete `selected_owner_kind_claim_cohort` from every distinct claim in the highest-precedence nonempty owner kind; independently validate every cohort claim; require cohort compatibility under effective §5.2.1; reject `UNREGISTERED_DURABLE_OBJECT`, `NORMAL_FINALIZATION_OBJECT`, and `CONFLICT_FINALIZATION_OBJECT` as normal-inventory owners; and select exactly one top-level encoding representative by the fixed four-component unsigned UTF-8 tuple order. Cohort multiplicity alone is not invalid.

### 3.2 Replace item 6

Replace item 6 in full with:

6. Validate every nonrepresentative compatible same-kind claim as retained secondary ownership evidence under the complete cohort rules, and validate every lower-precedence claim under the five lower-precedence compatibility dimensions in §5.2.1. No nonrepresentative or lower-precedence claim emits another inventory row or an alternative role/stage pair. Representative selection changes encoding metadata only and never removes a claim from closure validation.

### 3.3 Replace item 8 as amended by Delta Packet 06

Replace item 8 in full with:

8. An incompatible selected-owner-kind cohort; a same-kind claim whose normalized path, schema, registered role, registered semantic identity, target logical hash, canonical-object identity, or producer stage disagrees; a same-kind physical-object difference lacking the complete existing canonical-winner/adoption proof; a `SNAPSHOT_HISTORY_OBJECT` cohort whose owning publications resolve to different or non-domain `audit_family` values or different producer stages; no registered claim; unreadable selected-owner metadata without independently bound expected metadata; no unique deterministic representative; representative choice dependent on discovery order or any nonregistered ordering input; structural/member grammar contradiction; a fence owner with missing, unreadable, unsupported, or mismatched `event_kind`/linked-plan evidence; a snapshot owner with missing, unreadable, non-domain, or plan-unequal `audit_family`; selection of `NORMAL_FINALIZATION_OBJECT`, `CONFLICT_FINALIZATION_OBJECT`, or `UNREGISTERED_DURABLE_OBJECT`; selected-owner role/stage derivation failure; incompatible lower-precedence claim; nonrepresentative same-kind claim omitted from validation; secondary claim emitting another role/stage pair; duplicate inventory output row; disposition-derived role/stage; owner array; or undeclared row field produces `STOP_FINALIZATION_INVENTORY_INVALID`. Multiple compatible claims in the selected owner kind do not produce a stop.

---

## 4. Directly affected materialization replacement

Replace Delta Packet 06 §4.1 in full with the following text.

### 4.1 Replacement for effective base §26 item 11

11. synchronize artifact catalog, producer-consumer, lifecycle, resume, finalization, traceability, tests, and authorization supersession; materialize normal final-inventory cardinality as exactly one row per unique normalized included path; collect all effective base §21.4.2 claims and select the highest-precedence nonempty owner kind; form and independently validate the complete same-kind claim cohort; permit multiple same-kind claims only when all applicable normalized-path, content-schema, registered-role, registered-semantic-identity, target-logical-hash, canonical-object, physical-winner, and producer-stage requirements agree; choose one deterministic top-level owner-metadata representative by ascending unsigned UTF-8 `(owner_entry_key,owner_registry_path,owner_registry_file_sha256,owner_entry_logical_sha256)` while retaining and validating every nonrepresentative same-kind claim as secondary ownership evidence; derive `artifact_role` only from the cohort's common exact `registered_object_role`; derive a selected fence cohort's common `producer_stage` from each canonical `fence_unit_manifest_v23.event_kind` only after reopening each exact linked prepared plan and proving `plan.unit_kind == manifest.event_kind`; derive a selected snapshot cohort's common stage from every owning canonical commit's exact `audit_family` using the closed `capture`/`analysis_compatibility`/`analysis_strict` mapping and require each linked plan to prove `unit_kind=SNAPSHOT_PUBLICATION` and `subject_family == audit_family`; permit one immutable partition to have multiple compatible `SNAPSHOT_HISTORY_OBJECT` owners across sequences and ordinals only when every owner resolves to the same audit family, role, schema, canonical partition identity, logical semantics, and producer stage; reject selected normal-terminal, conflict-terminal, or unregistered owners as impossible normal-inventory classifications; preserve the unchanged prepared structural/object `unit_kind → producer_stage` table; permit compatible lower-precedence claims, including governing-package and schema-artifact-catalog claims for one accepted path, without a second row or pair; add no independent classification-registry artifact, owner arrays, alternative role/stage pairs, or undeclared relationship fields; reject absent, unreadable, incompatible same-kind, nondeterministically represented, unregistered, terminal-owner, or otherwise contradictory classifications with `STOP_FINALIZATION_INVENTORY_INVALID`; and validate snapshot, prepared-unit, superseded-unit, race-loser, row-batch, terminal-source, nonrepresentative same-kind, and lower-precedence relationships separately during closure;

---

## 5. Directly affected test replacement

Replace Delta Packet 06 §5 in full with the following text.

Normal-inventory owner-selection tests construct the complete effective base §21.4.2 claim set for each normalized path and exercise every selected owner kind that may validly classify a non-self-excluded normal-inventory path. Positive cases require exactly one inventory row per normalized included path and prove: one immutable partition reused by multiple valid `SNAPSHOT_HISTORY_OBJECT` owners across different snapshot sequences and partition ordinals; all such owners resolving independently to one audit family, one schema, one registered role, one canonical partition identity, one logical hash, and one producer stage; deterministic representative selection by the exact four-component unsigned UTF-8 tuple independent of discovery, filesystem, insertion, and map iteration order; every compatible nonrepresentative same-kind claim retained and validated; no compatible same-kind claim emitting a second inventory row or alternative role/stage pair; governing-package selection with a compatible schema-artifact-catalog lower-precedence claim; schema-artifact-catalog fallback; exact common selected-cohort `registered_object_role` use rather than `schema_ref`; authorization-use and capture relation stages; detached pre-run attachment stage; every prepared structural/object stage that can occur on a non-self-excluded included path; each canonical fence `event_kind` supported by effective §5.2.2 with every applicable exact linked plan proving equal `unit_kind`; snapshot history and current-view ownership for `capture`, `analysis_compatibility`, and `analysis_strict`, each with the exact family stage and every linked `SNAPSHOT_PUBLICATION` plan proving equal `subject_family`; compatible lower-precedence prepared/recovery claims; permitted physical-winner inequality only under the complete existing equal-semantics adoption proof; and disposition-neutral role/stage.

Counterexamples require `STOP_FINALIZATION_INVENTORY_INVALID` for: a same-kind claim naming a different normalized path; same-kind content-schema mismatch; same-kind registered-role mismatch; same-kind registered-semantic-identity disagreement; same-kind target logical-hash disagreement; same-kind canonical-object disagreement; same-kind incompatible or unproved physical-object claims; multiple snapshot-history owners resolving to different or non-domain audit families; multiple same-kind claims deriving different producer stages; an independently invalid same-kind owner entry; a representative chosen differently after claim discovery order is permuted; a representative tuple using a timestamp, discovery ordinal, filesystem order, insertion order, process identity, or implementation map order; a compatible same-kind claim omitted from closure validation; a nonrepresentative same-kind claim emitting another inventory row or alternative role/stage pair; no claim; selected unregistered owner; malformed catalog fallback producer; deriving `artifact_role` from `schema_ref`; structural/member grammar contradiction; a fence manifest read as though it contained `unit_kind`; missing or unreadable fence manifest or linked plan; manifest/plan hash or prepared-unit-ID mismatch; `manifest.event_kind != plan.unit_kind`; unsupported fence `event_kind`; missing, unreadable, or non-domain snapshot `audit_family`; snapshot linked plan with `unit_kind != SNAPSHOT_PUBLICATION`; `plan.subject_family != audit_family`; selected `NORMAL_FINALIZATION_OBJECT`; selected `CONFLICT_FINALIZATION_OBJECT`; unreadable owner metadata without independently bound metadata; incompatible lower-precedence claim; duplicate path row; disposition-derived replacement of role/stage; owner array; undeclared field; or omitted secondary-relationship proof.

The same fixtures must prove that mere selected-owner-kind multiplicity is not a stop: two or more independently valid compatible claims pass, the deterministic representative is stable, all claims remain validated, and exactly one inventory row is emitted. No positive normal-inventory test may construct a row selected by `NORMAL_FINALIZATION_OBJECT` or `CONFLICT_FINALIZATION_OBJECT`. Independent tests for normal/conflict terminal publication and mutual exclusion remain unchanged. If the unchanged `NORMAL_FINALIZATION` row in the prepared-unit mapping is tested, it is tested only as a prepared-plan schema/stage derivation outside a normal-inventory included-row claim because the selected normal-finalization prepared subtree remains self-excluded.

---

## 6. Directly affected traceability replacement

Replace Delta Packet 06 §6.1 in full with the following text.

### 6.1 Replacement traceability row immediately after `final snapshot and complete loser inventory closure`

| Requirement | Section | Schema/invariant | Stop/decision | Proposed tests |
|---|---|---|---|---|
| normal-inventory same-owner-kind cohort validation, deterministic representative selection, stage derivation, and one-row-per-path closure | §§5.2, 8.6, 17.5, 21.2, 21.4.2, 26–27 | collect all registered claims; select highest-precedence nonempty owner kind; independently validate every distinct same-kind claim; compatible cohort requires equal normalized path, schema, registered role, semantic identity, target logical hash, canonical-object identity, permitted physical-winner proof, and producer stage; deterministic representative is minimum unsigned UTF-8 `(owner_entry_key,owner_registry_path,owner_registry_file_sha256,owner_entry_logical_sha256)` and supplies encoding metadata only; all nonrepresentative same-kind claims remain validated secondary evidence; multiple snapshot-history owners may reference one reused partition only with one audit family and stage; compatible lower-precedence claims emit no second pair; terminal/unregistered owner kinds remain invalid; one unique normalized-path row | `STOP_FINALIZATION_INVENTORY_INVALID` for incompatible same-kind cohort, path/schema/role/semantic/logical/canonical-object/stage disagreement, unproved physical difference, mixed snapshot families, invalid cohort member, absent/unregistered/terminal owner, nondeterministic representative, omitted same-kind validation, incompatible lower-precedence claim, duplicate row, or undeclared field; compatible same-kind multiplicity continues | effective §§24.14–24.15 normal-inventory tests as replaced by this packet §5; independent terminal-publication tests unchanged |

---

## 7. Unchanged-text and authorization statement

Except for the exact replacements in this packet, every byte of the base amendment, Correction Packet 01, Delta Packets 02–06, and their effective application remains unchanged. In particular, Delta Packet 04 §5.2.2 and its complete `unit_kind → producer_stage` mapping, Delta Packet 06 fence/snapshot producer-stage corrections and terminal-owner exclusions, all independent terminal-publication rules, and all authorization boundaries remain unchanged.

This packet creates no new schema, artifact, owner kind, inventory field, owner array, registry, stop code, or authorization. It authorizes nothing. It does not authorize communication with Claude, materialization, source synchronization, implementation, test authoring, test execution, repository edits, local reads, subprocesses, network activity, replay, empirical work, P1/P2/P3, probe execution, or gate changes.
