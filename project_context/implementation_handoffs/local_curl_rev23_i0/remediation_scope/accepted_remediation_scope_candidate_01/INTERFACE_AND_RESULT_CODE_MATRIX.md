# Interface and Result-Code Matrix

Canonical repository: `rigolugo/pm_research`  
Canonical base inspected: `cc2964840d197a40d1c4ef567b42eda762c0be0a`  
Controlling accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`  
Preserved checkpoint evidence: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`  
Checkpoint state: `NOT_ACCEPTED`; authorization effect: `NONE`; static result: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`.


## 1. Public result codes

| Code | Canonical inventory owner | Trigger owner/surfaces | Exact trigger | Immediate predecessor/successor | Older mapping replaced or forbidden | Return shape |
|---|---|---|---|---|---|---|
| `ERR_UNIT_CONTEXT_INVALID` | `canonical.py` | applicable wrappers in `prepared_evidence.py` | Accepted unit kind, but family or sequence violates closed context domain. | after `STOP_UNIT_KIND_NOT_ACCEPTED_I0A`; before every parse/registry/descriptor/physical/delegate predicate | Any later path/schema/cross-member result MUST NOT mask invalid context. | `ValidationResult(code=..., established_assurances=())` |
| `ERR_REUSE_SOURCE_TARGET_MISMATCH` | `canonical.py` | descriptor pre-binding/reduction | Reuse binding, both fields lexical/grammar valid under selected target grammar, exact strings/UTF-8 bytes unequal. | after global lexical and grammar; before family/run/nullability | `ERR_ROLE_DISPOSITION_INVALID` forbidden for post-path inequality. | same, no extra fields |
| `ERR_SEMANTIC_FAMILY_BINDING_MISMATCH` | `canonical.py` | single descriptor and descriptor-set family stages | Grammar-valid family differs among UnitContext, schema family when specific, target parsed family, and claim family on set surface. | after reuse; before run/nullability | path errors forbidden for grammar-valid wrong family; ad hoc cross-member class forbidden. | same |
| `ERR_RUN_ID_BINDING_MISMATCH` | `canonical.py` | descriptor-set run reduction and transitive callers | Grammar-valid claim, target, and durable-source run IDs are not all equal for any descriptor. | after family; before nullability | `ERR_PATH_GRAMMAR_MISMATCH` and `ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH` forbidden for this condition. | same |

Every non-success result retains empty assurances. Existing success and error domains not named here remain unchanged.

## 2. UnitContext

| Field | Type/domain | Nullable | Invalid examples | Decision |
|---|---|---:|---|---|
| `unit_kind` | existing `PreparedUnitKind`; I0A accepts `SNAPSHOT_PUBLICATION` | no | unknown/non-enum/unsupported | unsupported accepted discriminant -> unit-kind stop before context; malformed context value -> context error according to existing constructor/type boundary |
| `subject_family` | exact semantic value `capture`, `analysis_compatibility`, `analysis_strict` | no | null, `analysis/compatibility`, semantic alias `strict`, unknown string | `ERR_UNIT_CONTEXT_INVALID` |
| `subject_sequence` | `type(value) is int`, not bool; `0..2^64-1` inclusive | no | null, bool, float, string, negative, `2^64` | `ERR_UNIT_CONTEXT_INVALID` |

No coercion, normalization, or inferred default is allowed.

## 3. Registry path interface

### `_FrozenPathBindings`

Closed typed fields:

- `grammar_id: FrozenPathGrammarId`, non-null;
- `run_id: str`, non-null;
- `semantic_family: Literal[capture,analysis_compatibility,analysis_strict] | None`, null iff grammar has no family root;
- `snapshot_sequence: int | None`, null iff absent placeholder;
- `partition_id: str | None`;
- `fence_sequence: int | None`;
- `unit_kind: PreparedUnitKind | None`;
- `prepared_unit_id: str | None`;
- `object_ordinal: int | None`.

### `_PathMatchResult`

Closed fields `code` and `bindings`; lexical and grammar failures have null bindings; success has complete bindings. No exceptions or caller grammar are added by this scope.

## 4. SchemaBinding

Frozen fields: `binding_id:str`, `role:PreparedObjectRole`, `unit_kind:PreparedUnitKind`, `publication_mode:PublicationMode`, `target_grammar_id:FrozenPathGrammarId`, `content_schema_id:str`, `logical_sha256_nullability:str`, `sidecar_rule:str`.

Selection key: `tuple[PreparedObjectRole, PreparedUnitKind, PublicationMode, str]` from role, UnitContext kind, mode, schema ID. Actual logical-hash nullability, target/source paths, file size/hash, and sidecar ordinal are excluded.

## 5. Descriptor pre-binding and reduction

| Type | Closed fields / values | Nullability |
|---|---|---|
| `_DescriptorPreBindingCode` | valid, lexical, grammar, reuse, family | closed enum |
| `_DescriptorPreBindingResult` | code, object ordinal, selected binding, target match, source match | all outer fields non-null; nested match bindings follow outcome |
| `_DescriptorPreBindingFaultEvidence` | object ordinal, path field, source code | path field null only for reuse/family |
| `_DescriptorPreBindingReductionCode` | valid, lexical, grammar, reuse, family reduction codes | closed enum |
| `_DescriptorPreBindingReductionResult` | code, fault evidence, ordered results | failure: evidence non-empty/results null; success: evidence null/results exact tuple |

Total mapping: lexical -> public lexical; grammar -> public grammar; reuse -> new reuse; family -> new family; valid -> continue.

## 6. Private descriptor-set reducer

Input fields: `summaries`, `expected_fixed_role_counts`. `PARTITION_PAYLOAD` is forbidden in the fixed map.

Result domain/order: role cardinality, duplicate target, sidecar relation, valid. Failures have `summaries=None`; success has full summaries. `PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID` and `expected_role_counts` are superseded and MUST be absent.

## 7. Selected BindingQuery projection

`_project_selected_binding_query(unit_context, selected_descriptor, paired_descriptor)` returns a frozen `_SelectedBindingQueryProjectionResult` with only code `PRIVATE_SELECTED_BINDING_QUERY_PROJECTION_VALID` and non-null exact `BindingQuery` under preconditions.

Projection copies selected values and computes booleans using Python identity; paired role/schema/path are all populated from the validated paired descriptor for sidecars or all null for non-sidecars. The helper establishes no public assurance and has no public failure result.

## 8. Public interface applicability

| Public interface | UnitContext | Reuse | Family | Run | Selected wrapper |
|---|---:|---:|---:|---:|---:|
| `validate_prepared_object_descriptor` | direct | yes | yes | no claim run input | no |
| `validate_prepared_descriptor_set` | direct | yes | yes | yes | no |
| `validate_structural_json_member` | direct | no | no complete set | no | no |
| `validate_selected_json_payload` | direct/transitive | yes via set | yes via set | yes via set | owner |
| `validate_prepared_unit_structure` | direct/transitive | propagated | propagated | propagated | MUST delegate |
| `dispatch_i0a_unit_validation` | direct/transitive | propagated | propagated | propagated | propagated |
| `validate_full_prepared_object` / `validate_full_prepared_unit` | excluded before filesystem stop | no | no | no | no |

## 9. Total precedence summary

Descriptor set: unit kind; context; claim canonical/schema/predecessor/coverage/digest; descriptor closed fields; binding; global lexical; global grammar; reuse; family; run; nullability; public ordinal; variable partition cardinality; private fixed cardinality; uniqueness; sidecar relation; same-ordinal binding; success.

Selected wrapper: the exact 19 predicates in the primary scope. Unit validator: unit kind; context; member set; registry; structural members; descriptor set; selected wrapper iteration; success.
