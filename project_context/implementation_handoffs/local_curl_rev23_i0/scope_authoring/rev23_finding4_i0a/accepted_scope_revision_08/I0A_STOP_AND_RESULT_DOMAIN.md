# I0A Stop and Result Domains — Revision 08

## A. Ordered authoring/workflow halt domain

These labels are workflow outcomes only. They are not persisted research artifacts and do not extend `REV23_STOP_CODE`.

Evaluate one ordered `if / else-if` chain. The first true predicate is the sole outcome. The mapping is total and mutually exclusive.

| Order | Halt label | Exact trigger after all prior predicates are false | Zero requests | Artifact behavior | Downstream effect |
|---:|---|---|---:|---|---|
| 1 | `STOP_IMPLEMENTATION_NOT_AUTHORIZED` | explicit current Gustavo implementation authorization is absent, regardless of any package presence, identity, or local state | yes | inactive review text only | no authoring |
| 2 | `STOP_ACTIVE_AUTHORIZATION_PACKAGE_MISSING` | authorization exists but no Sentinel-installed active package exists | yes | no implementation artifact | active package required |
| 3 | `STOP_SCOPE_ANCHOR_MISMATCH` | active package exists but its required scope anchor is not `88362521fe9ef247708e4d7b5f90753784b8b88e` | yes | no changes | renewed review |
| 4 | `STOP_ACTIVE_AUTHORIZATION_PACKAGE_MISMATCH` | anchor matches but active package hash, identity, file matrix, activity matrix, or governing hashes differ from the authorized package | yes | no changes | corrected package required |
| 5 | `STOP_SOURCE_SYNC_NOT_AUTHORIZED` | valid active package requires source synchronization that lacks separate authorization | yes | no synchronization | authoring blocked |
| 6 | `STOP_LOCAL_HEAD_MISMATCH` | source synchronization is authorized/completed but local HEAD is not the exact source-gated HEAD | yes | no source changes | source gate closed |
| 7 | `STOP_WORKTREE_NOT_CLEAN` | HEAD matches but worktree violates the active clean-state gate | yes | no source changes | clean state required |
| 8 | `STOP_AUTHORIZED_PATH_ALREADY_EXISTS` | an authorized create-only path already exists | yes | preserve bytes | renewed review |
| 9 | `STOP_GOVERNING_PACKAGE_BYTES_MISMATCH` | accepted governing bytes differ from active package hashes | yes | no source changes | governing correction required |
| 10 | `STOP_DEPENDENCY_OR_CLI_SCOPE_EXPANSION` | work requires a dependency, CLI, config, generated code, filesystem adapter, reverse import, duplicated grammar authority, or existing-module edit outside the accepted matrix | yes | report only | new scope review |
| 11 | `STOP_AUTHORIZED_FILE_MATRIX_EXPANSION` | any additional repository path is required | yes | report only | new authorization |
| 12 | `STOP_SCOPE_AMBIGUITY` | a material contract question remains after applying the exact accepted files | yes | report only | Professor/Sentinel amendment |
| 13 | `STOP_UNAUTHORIZED_EXECUTION_REQUIRED` | completion requires tests, project imports/execution, local reads, artifact recovery, network/curl/subprocess, replay, empirical work, or another unauthorized action | yes | report only | separate authorization |
| 14 | `AUTHORING_PRECONDITIONS_CLEAR` | every prior predicate is false | yes until separately authorized execution | no implicit artifact | only the separately authorized action may proceed |

Current state resolves at order 1: `STOP_IMPLEMENTATION_NOT_AUTHORIZED`.

## B. Pure I0A typed stop-state table

These are in-memory `I0AResultCode` values, not persisted REV23 stops.

| Stop code | Exact trigger | Stage | Zero requests | Artifact behavior | Downstream effect |
|---|---|---|---:|---|---|
| `STOP_UNIT_KIND_NOT_ACCEPTED_I0A` | directly or transitively supplied unit kind is not `SNAPSHOT_PUBLICATION` | first gate on every applicable surface | yes | typed result only | no later input is evaluated |
| `STOP_SCHEMA_REFERENCE_UNRESOLVED` | a `json:`/`table:` ID is absent from the complete pinned accepted-registry index | after unit/package/query/path checks | yes | typed result only | no binding/schema validation |
| `STOP_CONTENT_SCHEMA_TARGET_BINDING_INVALID` | accepted ID exists but compatible frozen binding count is zero or greater than one | after membership | yes | typed result only | no selected-schema validation |
| `STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A` | accepted and uniquely compatible selected schema is outside the implemented I0A schema set | after binding and prior structural/physical checks | yes | typed result only | inconclusive; never a negative finding |
| `STOP_PAYLOAD_LOGICAL_VALIDATION_OUT_OF_SCOPE` | required logical rows, decoder, or logical evidence is outside I0A | after applicable structural/schema checks | yes | typed result only | no A4/A6 claim |
| `STOP_FILESYSTEM_FACTS_OUT_OF_SCOPE` | requested result requires independent filesystem/reopen/reuse/durability facts | after unit-kind gate where applicable | yes | typed result only | A5/A7/A8 remain unreachable |

Every stop returns `established_assurances=()`.

## C. Ordered success/result-label decision table

Success is evaluated only after every function-specific ordered error/stop predicate is false.

| Exact result | Exact condition | Exact established assurances |
|---|---|---|
| `I0A_BYTES_CONSTRUCTED_A0` | typed byte constructor completes | `()` |
| `I0A_DIGEST_CONSTRUCTED_A0` | digest constructor completes | `()` |
| `I0A_VALID_A1_PATH` | one path matches its selected frozen grammar and placeholders | `(A1_LEXICAL_PATH_SHAPE,)` |
| `I0A_BINDING_RESOLVED_A1` | accepted registry membership and exactly one frozen binding resolve | `(A1_LEXICAL_PATH_SHAPE, A1_REGISTRY_BINDING_RESOLVED)` |
| `I0A_VALID_A2_SINGLE` | one complete descriptor validates | `(A1_LEXICAL_PATH_SHAPE, A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS)` |
| `I0A_VALID_A2_SET` | complete claim-derived descriptor set validates | `(A1_LEXICAL_PATH_SHAPE, A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS, A2_DESCRIPTOR_SET_COMPLETE)` |
| `I0A_VALID_A3_EXACT` | supplied bytes match explicit expected length and complete-file SHA-256 | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED,)` |
| `I0A_PINNED_GOVERNING_BYTES_VALIDATED_A3H` | all fixed governing bytes match their pinned hashes | `(A3_PINNED_GOVERNING_SHA256_VALIDATED,)` |
| `I0A_REGISTRY_INDEX_MATERIALIZED_A3H` | pinned registry bytes parse strictly, reject duplicates/floats/constants, canonical-reserialize identically, and yield the complete definition index | `(A3_PINNED_GOVERNING_SHA256_VALIDATED,)` |
| `I0A_VALID_A3_STRUCTURAL_SIDECAR` | fixed structural sidecar and independently supplied paired-target bytes reconcile and bind to the independently derived paired path/hash | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)` |
| `I0A_VALID_A4_INTERNAL_RELATION` | internal `i0a:` logical relation validates without physical A3 | `(A4_DECODED_LOGICAL_ROWS_VALIDATED,)` |
| `I0A_VALID_A3_A4_STRUCTURAL_OBJECT` | physically reconciled plan or prepared-unit structural JSON validates its implemented decoded relation | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A4_DECODED_LOGICAL_ROWS_VALIDATED)` |
| `I0A_VALID_A6_STRUCTURAL` | fixed structural JSON-object schema completes | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A6_STRUCTURAL_SCHEMA_COMPLETE)` |
| `I0A_VALID_A6_SELECTED` | descriptor-selected `json:sha256_sidecar` completes after A2, binding, selected A3, and paired-target A3 | `(A1_LEXICAL_PATH_SHAPE, A1_REGISTRY_BINDING_RESOLVED, A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS, A2_DESCRIPTOR_SET_COMPLETE, A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A6_DESCRIPTOR_SELECTED_SCHEMA_COMPLETE)` |

## D. Closed pure error domain

The exact error codes are:

```text
ERR_PATH_LEXICAL_INVALID
ERR_PATH_GRAMMAR_MISMATCH
ERR_CANONICAL_TAG_INVALID
ERR_CANONICAL_TYPE_MISMATCH
ERR_CANONICAL_NON_NFC
ERR_CANONICAL_UINT_RANGE
ERR_CANONICAL_SHA256_FORMAT
ERR_CANONICAL_BYTES_FORMAT
ERR_CANONICAL_FIELD_NAME_INVALID
ERR_CANONICAL_FIELD_ORDER_INVALID
ERR_CANONICAL_ROW_ARITY
ERR_DIGEST_INPUT_INVALID
ERR_CANONICAL_JSON_INVALID
ERR_GOVERNING_PACKAGE_BYTES_MISMATCH
ERR_BINDING_QUERY_INVALID
ERR_DESCRIPTOR_CLOSED_FIELD_INVALID
ERR_ROLE_DISPOSITION_INVALID
ERR_ROLE_CARDINALITY_INVALID
ERR_ORDINAL_SEQUENCE_INVALID
ERR_CANONICAL_TARGET_DUPLICATE
ERR_SIDECAR_RELATION_INVALID
ERR_LOGICAL_HASH_NULLABILITY_INVALID
ERR_PHYSICAL_EXPECTATION_INVALID
ERR_PHYSICAL_SIZE_MISMATCH
ERR_PHYSICAL_SHA256_MISMATCH
ERR_LOGICAL_ROWS_INVALID
ERR_LOGICAL_SHA256_MISMATCH
ERR_SELECTED_SCHEMA_INVALID
ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED
ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH
ERR_STRUCTURAL_MEMBER_SET_INVALID
ERR_PREDECESSOR_RULE_INVALID
ERR_COVERAGE_STATE_INVALID
ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH
ERR_PREPARED_UNIT_ID_MISMATCH
ERR_CLAIM_SEMANTIC_SCHEMA_MISMATCH
```

Every error returns `established_assurances=()`. Each public function's exact precedence is materialized in `I0A_PUBLIC_API_CONTRACT.json`; each code has a direct static case in `I0A_STATIC_TEST_CASE_MATRIX.json`.

## E. Persisted REV23 stop domain

Revision 08 does not add, remove, reinterpret, or emit a persisted `REV23_STOP_CODE`. Persisted canonical stops remain governed solely by the accepted Revision 23 contract.

Missing evidence, an unimplemented schema, a parser failure, or an out-of-scope fact cannot become a negative finding, a false unblock, a persisted research stop, or a gate change.
