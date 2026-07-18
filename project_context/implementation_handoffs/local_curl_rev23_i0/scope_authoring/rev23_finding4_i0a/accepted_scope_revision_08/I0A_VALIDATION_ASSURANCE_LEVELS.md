# I0A Validation Assurance Levels — Revision 08

The assurance domain is closed. Assurance exists only in the exact `established_assurances: tuple[AssuranceLevel, ...]` returned with a public `I0AResultCode`. Private helper outcomes carry no assurance tuple.

| Level | Exact claim | Reachable | Does not establish |
|---|---|---:|---|
| `A0_NONE` | no validation assurance; deterministic byte/digest construction only | yes | any validity |
| `A1_LEXICAL_PATH_SHAPE` | one supplied path is normalized and matches one immutable frozen grammar and its exact placeholder domains | yes | registry binding, descriptor validity, bytes, filesystem |
| `A1_REGISTRY_BINDING_RESOLVED` | the selected schema is in the complete pinned accepted-registry index and exactly one immutable production binding matches | yes | descriptor/set validity, bytes, filesystem |
| `A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS` | one complete descriptor satisfies closed fields, types, role-local mode/path/hash syntax, and logical-hash nullability | yes | unit cardinality, ordinal completeness, target uniqueness, complete sidecar graph |
| `A2_DESCRIPTOR_SET_COMPLETE` | the complete descriptor set satisfies exact ordinals, claim-derived role cardinalities, target uniqueness, and the complete same-unit sidecar graph | yes | payload bytes, selected schema, filesystem |
| `A3_EXACT_LENGTH_AND_SHA256_RECONCILED` | supplied bytes equal an explicit expected exact length and expected complete-file SHA-256 | yes | descriptor, binding, logical schema, filesystem |
| `A3_PINNED_GOVERNING_SHA256_VALIDATED` | fixed governing bytes equal the accepted pinned complete-file SHA-256 | yes | generic caller-selected length proof, descriptor, filesystem |
| `A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED` | a fixed structural sidecar and independently supplied paired-target bytes each reconcile physically, and the sidecar values equal the independently derived paired path and observed target hash | yes | decoded logical rows, A4, A6, descriptor set, selected schema, filesystem |
| `A4_DECODED_LOGICAL_ROWS_VALIDATED` | supplied decoded logical content satisfies the implemented closed relation, ordering, uniqueness, nullability, and recomputed logical hash | yes | physical bytes unless separately listed, Parquet decoding, filesystem |
| `A5_FILESYSTEM_FACTS_VALIDATED` | independent filesystem, reopen, symlink, reuse, and durability facts | no | — |
| `A6_STRUCTURAL_SCHEMA_COMPLETE` | one fixed structural JSON-object schema completes after exact physical and logical checks | yes on declared branches | descriptor-selected A6, filesystem, A7/A8 |
| `A6_DESCRIPTOR_SELECTED_SCHEMA_COMPLETE` | one descriptor-selected schema completes after exact A2 set, A1 binding, selected A3, paired-target A3 when required, and schema checks | yes only for `json:sha256_sidecar` | other selected schemas, filesystem, A7/A8 |
| `A7_PREPARED_OBJECT_FULL` | complete prepared object including independent filesystem facts | no | — |
| `A8_PREPARED_UNIT_FULL` | complete prepared unit including all selected schemas and independent filesystem facts | no | — |

## Global success-code mapping

Every success code has exactly one tuple globally. Function-local alternatives are forbidden.

| Success code | Exact `established_assurances` tuple |
|---|---|
| `I0A_BYTES_CONSTRUCTED_A0` | `()` |
| `I0A_DIGEST_CONSTRUCTED_A0` | `()` |
| `I0A_VALID_A1_PATH` | `(A1_LEXICAL_PATH_SHAPE,)` |
| `I0A_BINDING_RESOLVED_A1` | `(A1_LEXICAL_PATH_SHAPE, A1_REGISTRY_BINDING_RESOLVED)` |
| `I0A_VALID_A2_SINGLE` | `(A1_LEXICAL_PATH_SHAPE, A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS)` |
| `I0A_VALID_A2_SET` | `(A1_LEXICAL_PATH_SHAPE, A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS, A2_DESCRIPTOR_SET_COMPLETE)` |
| `I0A_VALID_A3_EXACT` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED,)` |
| `I0A_PINNED_GOVERNING_BYTES_VALIDATED_A3H` | `(A3_PINNED_GOVERNING_SHA256_VALIDATED,)` |
| `I0A_REGISTRY_INDEX_MATERIALIZED_A3H` | `(A3_PINNED_GOVERNING_SHA256_VALIDATED,)` |
| `I0A_VALID_A3_STRUCTURAL_SIDECAR` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)` |
| `I0A_VALID_A4_INTERNAL_RELATION` | `(A4_DECODED_LOGICAL_ROWS_VALIDATED,)` |
| `I0A_VALID_A3_A4_STRUCTURAL_OBJECT` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A4_DECODED_LOGICAL_ROWS_VALIDATED)` |
| `I0A_VALID_A6_STRUCTURAL` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A6_STRUCTURAL_SCHEMA_COMPLETE)` |
| `I0A_VALID_A6_SELECTED` | `(A1_LEXICAL_PATH_SHAPE, A1_REGISTRY_BINDING_RESOLVED, A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS, A2_DESCRIPTOR_SET_COMPLETE, A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A6_DESCRIPTOR_SELECTED_SCHEMA_COMPLETE)` |

Every error or stop returns `()`.

## Result-payload invariants

1. `CanonicalBytesResult` has non-null exact bytes only on `I0A_BYTES_CONSTRUCTED_A0`; every non-success has `value=null`.
2. `DigestResult` has one exact lowercase SHA-256 only on `I0A_DIGEST_CONSTRUCTED_A0`; every non-success has `digest_sha256=null`.
3. `RegistryDefinitionIndexResult` has a fully populated index only on `I0A_REGISTRY_INDEX_MATERIALIZED_A3H`; otherwise `index=null`.
4. `BindingResolutionResult` has the exact frozen production binding only on `I0A_BINDING_RESOLVED_A1`; otherwise `binding=null`.
5. `PhysicalPayloadResult` reports both actual observed size and actual observed SHA-256 on success, size mismatch, and SHA mismatch. Invalid expectations stop before observation and return both fields null.
6. No result reuses stale or partially computed values after a non-success decision.
7. `_resolve_compatible_binding_set` and `_validate_descriptor_set_invariants` return private outcome types, not public I0A successes or assurance tuples.
8. A5, A7, and A8 remain unreachable.
