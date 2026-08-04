# S2 Candidate 08 C10 Working Paper 01 — Execution Closure State Machine — Candidate 03

## 1. Status

| Field | Exact value |
|---|---|
| Working-paper ID | `S2_CANDIDATE_08_C10_WORKING_PAPER_01_EXECUTION_CLOSURE_STATE_MACHINE_CANDIDATE_03` |
| Status | `REVIEW_CANDIDATE_WORKING_PAPER_NOT_ACCEPTED` |
| Authoring mode | `AMEND` |
| Classification | `EXECUTION_CLOSURE_STATE_MACHINE_SPECIFICATION_WORKING_PAPER_CORRECTION_ONLY` |
| Prepared by | `Professor` |
| Independent reviewer and decision owner | `Sentinel` |
| Canonical repository | `rigolugo/pm_research` |
| Exact required canonical main | `2ba8766893407cb92616dd75b9e15a77ad0c865c` |
| Canonical verification | `MATCH — main identical to required commit; ahead 0 / behind 0` |
| Blocked predecessor | `S2_CANDIDATE_08_C10_WORKING_PAPER_01_EXECUTION_CLOSURE_STATE_MACHINE_CANDIDATE_02.md` |
| Blocked predecessor identity | `296608 bytes / eb6df0ff290e8c30a7f52a5f66cf11bed3be17dacc39eea01b6ed8b156d7858d` |
| Blocked predecessor disposition | `BLOCKED_REVIEW_ONLY_NON_CONTROLLING` |
| Authorization effect | `NONE` |

**Purpose.** Correct only `EXECUTION_CLOSURE_STATE_MACHINE_WORKING_PAPER_CANDIDATE_02_STAGE1_DOMAIN_AND_ROLLBACK_NOT_ATTEMPTED_STATE_NOT_CLOSED` while preserving Candidate 02's accepted four-stage factual-classification design.

**Checkable completion sentence.** Sentinel can mechanically verify that all schema-valid raw documents either stop in exactly one dependency-ordered Stage-1 group or produce the exact fifteen-field normalized object; every Stage-2-valid partial-output vector with `rollback_state = NOT_ATTEMPTED` reduces through exactly one of three dominant factual states; and no state has an acceptance effect.

## 2. Source precedence and evidence classification

| Source | Classification | Treatment |
|---|---|---|
| Canonical repository at the pinned commit | `CANONICAL` | Controls project state, guardrails, and settled authorization boundaries. |
| Candidate 02 exact bytes and matching sidecar | `OBSERVED` | Historical correction input only; blocked and non-controlling. |
| Sentinel Candidate-02 correction direction supplied with this task | `SUBMITTED` | Decision-bearing correction scope for this working paper; does not replace canonical project state. |
| Candidate 01, Candidate 09, and their review history | `SUBMITTED / BLOCKED HISTORICAL` | Context only; no blocked bytes become normative. |
| This Candidate 03 working paper | `SUBMITTED REVIEW CANDIDATE` | Not accepted, installed, executable, or implementation-authorizing. |

Candidates 01–09 remain blocked and non-controlling except as historical design evidence. No RECALLED claim is normative.

## 3. Scope

### 3.1 In scope

1. Make Stage 1 total over missing fields, wrong JSON primitive types, and value-level lexical/range validation through four dependency-ordered groups.
2. Replace the undefined parser category `INTEGER` with exact JSON `NUMBER` token semantics and deterministic mathematical signed-Int32 normalization.
3. Add three dominant factual closure states for partial output where rollback was not attempted and final presence is `PRESENT`, `UNAVAILABLE`, or `ABSENT`.
4. Reconcile normative prose, machine-readable rules, counts, examples, and self-attack evidence.

### 3.2 Out of scope

This paper MUST NOT define or imply closure acceptance, registered-evidence eligibility, K199 readiness or bindings, task-envelope scope, interpreter/module boundaries, registry integration, governance identities, final authorization sequencing, Candidate-10 integration, Working Paper 02, implementation, execution, tests, data access, network access, subprocess execution, Git activity, or downstream phase authority.

## 4. Preserved four-stage architecture

```text
raw_document_bytes
    ↓
Stage 1: parse_and_shape_validate
    ↓ only PARSE_AND_SHAPE_VALID
Stage 2: validate_normalized_inputs
    ↓ only NORMALIZED_INPUT_VALID
Stage 3: reduce_execution_closure
    ↓ expected_closure_state
Stage 4: verify_emitted_closure
```

The stages are strictly separated:

- Stage 1 owns bytes, JSON syntax, duplicate keys, exact field shape, primitive types, lexical forms, enum membership, and exit-code range.
- Stage 2 owns cross-field contradictions in the exact normalized object.
- Stage 3 owns one primary factual closure-state classification.
- Stage 4 owns equality between the reducer output and `emitted_closure_state`.
- No Stage-1 rejection enters Stage 2. No Stage-2 rejection enters Stage 3. Stage 4 is not a reducer precondition and does not call itself.

## 5. Stage 1 — `parse_and_shape_validate`

### 5.1 Exact JSON primitive domain

The only JSON primitive-type classifications used by this specification are:

`NULL`, `BOOLEAN`, `NUMBER`, `STRING`, `ARRAY`, and `OBJECT`.

There is no JSON or parser-native type named `INTEGER`. JSON booleans are not numbers.

### 5.2 Exact outputs

Stage 1 MUST return exactly one of:

```text
PARSE_AND_SHAPE_VALID(normalized_candidate_object, ordered_parsing_evidence)
PARSE_AND_SHAPE_REJECTED(primary_stop, matched_rule_ids, complete_ordered_diagnostics, retained_parsing_evidence)
```

A rejected document MUST NOT enter Stage 2. No normalized value may be synthesized after rejection.

### 5.3 Group execution contract

| Group | Name | Evaluation mode | Prerequisite | Failure behavior | Later groups after failure |
|---|---|---|---|---|---|
| `A` | `BYTE_AND_PARSER_GATES` | `SEQUENTIAL_FIRST_FAILURE` | raw_document_bytes supplied | PARSE_AND_SHAPE_REJECTED(primary_stop,[matched_rule_id],[single_diagnostic]) | `false` |
| `B` | `TOP_LEVEL_SHAPE_GATES` | `EVALUATE_ALL_ELIGIBLE_RULES` | Group A cleared | PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics) | `false` |
| `C` | `FIELD_REPRESENTATION_AND_JSON_TYPE_GATES` | `EVALUATE_ALL_ELIGIBLE_RULES` | Groups A and B cleared | PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics) | `false` |
| `D` | `VALUE_LEXICAL_MEMBERSHIP_AND_RANGE_GATES` | `EVALUATE_ALL_RULES_WITH_SATISFIED_PER_FIELD_PREREQUISITES` | Groups A, B, and C cleared | PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics) | `false` |

Group A evaluates sequentially and stops at its first failure. Groups B, C, and D evaluate every eligible rule in the current group, sort matches by integer priority and then Unicode code-point rule ID, retain all matched diagnostics, select the first matched rule's typed stop as `primary_stop`, and prohibit every later group when the current group has any match.

### 5.4 Stage-1 rule inventory

| Rule | Group | Priority | Prerequisites | Predicate | Typed stop | Diagnostic | Evidence retained |
|---|---:|---:|---|---|---|---|---|
| `S1-A-001` | `A` | 10 | raw_document_bytes supplied | `STRICT_UTF8_DECODE(raw_document_bytes) FAILS` | `STOP_CLOSURE_UTF8_INVALID` | `CLOSURE_UTF8_DECODE_ERROR` | raw_byte_length, raw_sha256, decoder_error_byte_offset, decoder_error_reason |
| `S1-A-002` | `A` | 20 | S1-A-001 did not match | `DECODED_TEXT IS_NOT_EXACTLY_ONE_COMPLETE_JSON_VALUE` | `STOP_CLOSURE_JSON_PARSE_INVALID` | `CLOSURE_JSON_SYNTAX_OR_CARDINALITY_ERROR` | raw_byte_length, raw_sha256, parser_error_byte_offset, parser_error_code, trailing_non_whitespace_span_if_any |
| `S1-A-003` | `A` | 30 | S1-A-001 and S1-A-002 did not match; parser retained ordered object-member pairs and source spans before map construction | `ANY_OBJECT_CONTAINS_DUPLICATE_DECODED_KEY` | `STOP_CLOSURE_DUPLICATE_JSON_KEY` | `CLOSURE_DUPLICATE_JSON_KEY` | raw_byte_length, raw_sha256, json_pointer_to_object, decoded_key, occurrence_ordinals, source_byte_spans |
| `S1-A-004` | `A` | 40 | S1-A-001 through S1-A-003 did not match | `PARSED_ROOT_JSON_PRIMITIVE_TYPE != OBJECT` | `STOP_CLOSURE_TOP_LEVEL_OBJECT_REQUIRED` | `CLOSURE_TOP_LEVEL_TYPE_INVALID` | raw_byte_length, raw_sha256, observed_root_json_primitive_type |
| `S1-B-001` | `B` | 50 | Group A cleared; top-level object member names available | `MISSING_REQUIRED_FIELDS != []` | `STOP_CLOSURE_REQUIRED_FIELD_MISSING` | `CLOSURE_REQUIRED_FIELD_MISSING` | raw_byte_length, raw_sha256, ordered_missing_field_names |
| `S1-B-002` | `B` | 60 | Group A cleared; top-level object member names available | `UNEXPECTED_FIELDS != []` | `STOP_CLOSURE_UNEXPECTED_FIELD` | `CLOSURE_UNEXPECTED_FIELD` | raw_byte_length, raw_sha256, ordered_unexpected_field_names |
| `S1-B-003` | `B` | 70 | Group A cleared; duplicate keys already rejected; top-level object member count available | `TOP_LEVEL_MEMBER_COUNT != 15` | `STOP_CLOSURE_FIELD_CARDINALITY_INVALID` | `CLOSURE_FIELD_CARDINALITY_INVALID` | raw_byte_length, raw_sha256, expected_member_count, observed_member_count |
| `S1-C-001` | `C` | 80 | Groups A and B cleared; all fifteen required fields present exactly once | `ANY_NON_NULLABLE_FIELD_VALUE JSON_PRIMITIVE_TYPE == NULL` | `STOP_CLOSURE_NULL_REPRESENTATION_INVALID` | `CLOSURE_NON_NULLABLE_FIELD_IS_NULL` | raw_byte_length, raw_sha256, ordered_json_pointers |
| `S1-C-002` | `C` | 90 | Groups A and B cleared; all enum fields present exactly once | `ANY_ENUM_FIELD JSON_PRIMITIVE_TYPE != STRING` | `STOP_CLOSURE_ENUM_JSON_TYPE_INVALID` | `CLOSURE_ENUM_FIELD_NOT_STRING` | raw_byte_length, raw_sha256, ordered_field_type_diagnostics |
| `S1-C-003` | `C` | 100 | Groups A and B cleared; process_exit_code present exactly once | `process_exit_code JSON_PRIMITIVE_TYPE NOT_IN [NULL,NUMBER]` | `STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` | `CLOSURE_EXIT_CODE_NOT_NULL_OR_NUMBER` | raw_byte_length, raw_sha256, observed_json_primitive_type, source_byte_span |
| `S1-D-001` | `D` | 110 | Groups A, B, and C cleared; for each inspected enum field: JSON primitive type is STRING | `ANY_ENUM_STRING DOES_NOT_MATCH ^[A-Z][A-Z0-9_]*$` | `STOP_CLOSURE_ENUM_TOKEN_LEXICAL_INVALID` | `CLOSURE_ENUM_TOKEN_LEXICAL_INVALID` | raw_byte_length, raw_sha256, ordered_field_token_diagnostics |
| `S1-D-002` | `D` | 120 | Groups A, B, and C cleared; for each inspected enum field: JSON primitive type is STRING; S1-D-001 did not match for that field | `ANY_LEXICALLY_VALID_ENUM_STRING NOT_IN DECLARED_FIELD_ENUM` | `STOP_CLOSURE_ENUM_TOKEN_UNREGISTERED` | `CLOSURE_ENUM_TOKEN_UNREGISTERED` | raw_byte_length, raw_sha256, field_name, observed_token, allowed_tokens |
| `S1-D-003` | `D` | 130 | Groups A, B, and C cleared; process_exit_code JSON primitive type is NUMBER | `ORIGINAL_PROCESS_EXIT_CODE_NUMBER_TOKEN DOES_NOT_MATCH ^-?(0\|[1-9][0-9]*)$` | `STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` | `CLOSURE_EXIT_CODE_INTEGER_NUMBER_LEXICAL_INVALID` | raw_byte_length, raw_sha256, original_number_token, source_byte_span |
| `S1-D-004` | `D` | 140 | Groups A, B, and C cleared; process_exit_code JSON primitive type is NUMBER; S1-D-003 did not match; token parsed as an unbounded mathematical integer | `MATHEMATICAL_INTEGER_VALUE NOT_IN [-2147483648,2147483647]` | `STOP_CLOSURE_EXIT_CODE_RANGE_INVALID` | `CLOSURE_EXIT_CODE_OUT_OF_SIGNED_INT32_RANGE` | raw_byte_length, raw_sha256, original_number_token, unbounded_mathematical_integer_value |

### 5.5 Dependency rules

| Dependency | Normative requirement | Mechanical enforcement |
|---|---|---|
| `S1-DEP-001` | Group B MUST NOT execute unless every Group-A rule cleared. | A Group-A match returns PARSE_AND_SHAPE_REJECTED immediately. |
| `S1-DEP-002` | Groups C and D MUST NOT execute when Group B has one or more matches. | Group-B matched rules are sorted; one primary stop and all diagnostics are returned. |
| `S1-DEP-003` | Group D MUST NOT execute when Group C has one or more matches. | Group-C matched rules are sorted; one primary stop and all diagnostics are returned. |
| `S1-DEP-004` | S1-D-001 and S1-D-002 inspect only present enum fields whose JSON primitive type is STRING. | Group-B and Group-C clearance are explicit prerequisites. |
| `S1-DEP-005` | S1-D-002 evaluates a field only after S1-D-001 cleared for that field. | Lexically invalid enum tokens cannot also yield membership diagnostics. |
| `S1-DEP-006` | S1-D-003 inspects process_exit_code only when its JSON primitive type is NUMBER. | NULL bypasses D-003 and D-004; BOOLEAN, STRING, ARRAY, and OBJECT are rejected in Group C. |
| `S1-DEP-007` | S1-D-004 evaluates only after S1-D-003 accepts the exact original number token. | Fractions and exponents cannot reach range validation; native numeric overflow cannot control classification. |
| `S1-DEP-008` | No later group or dependent rule may synthesize a value for a missing, null-forbidden, or wrong-type field. | No normalization occurs after any Stage-1 rejection. |

### 5.6 Exact `process_exit_code` number-token semantics

1. `process_exit_code` passes Group C only when its JSON primitive type is `NULL` or `NUMBER`.
2. `NULL` normalizes to null and bypasses number-token lexical and range rules.
3. For `NUMBER`, Stage 1 MUST retain and inspect the exact original JSON number token.
4. The accepted integer-number grammar is `^-?(0|[1-9][0-9]*)$`.
5. Fractions and exponent forms are rejected, including `1.0`, `1e0`, `1E0`, and `-2.5`.
6. A plus sign and JSON-invalid leading-zero forms fail Group A JSON parsing.
7. After lexical acceptance, the token is parsed as an unbounded mathematical integer; implementation-native number width is non-authoritative.
8. The accepted range is inclusive `-2147483648` through `2147483647`.
9. `-0` normalizes to mathematical integer zero while the exact source token `-0` remains retained parsing evidence.

| Source token/value | Stage-1 result | Normalized value or stop |
|---|---|---|
| `0` | `VALID` | `0` |
| `-0` | `VALID; source token retained` | `0` |
| `1` | `VALID` | `1` |
| `-1` | `VALID` | `-1` |
| `2147483647` | `VALID` | `2147483647` |
| `-2147483648` | `VALID` | `-2147483648` |
| `2147483648` | `REJECTED` | `STOP_CLOSURE_EXIT_CODE_RANGE_INVALID` |
| `-2147483649` | `REJECTED` | `STOP_CLOSURE_EXIT_CODE_RANGE_INVALID` |
| `1.0` | `REJECTED` | `STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` |
| `1e0` | `REJECTED` | `STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` |
| `true` | `REJECTED in Group C` | `STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` |
| `"1"` | `REJECTED in Group C` | `STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` |
| `null` | `VALID Stage-1 representation` | `null` |

## 6. Normalized input schema

The normalized object has exactly fifteen fields, no additional fields, and does not contain `emitted_closure_state`.

| Field | Type | Allowed values / range | Observer | Null rule |
|---|---|---|---|---|
| `execution_attempt_state` | `ClosedEnum<ExecutionAttemptStateV1>` | ["NOT_ATTEMPTED","EXACTLY_ONE","MULTIPLE","UNAVAILABLE"] | `OUTER_EXECUTION_CONTROLLER` | NEVER; forbidden: ALWAYS |
| `process_launch_state` | `ClosedEnum<ProcessLaunchStateV1>` | ["NOT_ATTEMPTED","LAUNCH_FAILED","LAUNCHED","UNAVAILABLE"] | `OUTER_EXECUTION_OBSERVER` | NEVER; forbidden: ALWAYS |
| `process_exit_state` | `ClosedEnum<ProcessExitStateV1>` | ["NOT_APPLICABLE","EXIT_OBSERVED","EXIT_NOT_OBSERVED","UNAVAILABLE"] | `OUTER_EXECUTION_OBSERVER` | NEVER; forbidden: ALWAYS |
| `process_exit_code` | `Nullable<MathematicalSignedInt32>` | [-2147483648,2147483647] | `OUTER_EXECUTION_OBSERVER` | process_exit_state != EXIT_OBSERVED; forbidden: process_exit_state == EXIT_OBSERVED |
| `output_creation_state` | `ClosedEnum<OutputCreationStateV1>` | ["NOT_CREATED","PARTIAL_CREATED","COMPLETE_CREATED","UNAVAILABLE"] | `OUTER_OUTPUT_OBSERVER` | NEVER; forbidden: ALWAYS |
| `output_commit_state` | `ClosedEnum<OutputCommitStateV1>` | ["NOT_ATTEMPTED","COMMIT_FAILED","COMMITTED","UNAVAILABLE"] | `OUTER_OUTPUT_OBSERVER` | NEVER; forbidden: ALWAYS |
| `raw_artifact_presence` | `ClosedEnum<RawArtifactPresenceV1>` | ["ABSENT","PRESENT","UNAVAILABLE"] | `OUTER_OUTPUT_OBSERVER` | NEVER; forbidden: ALWAYS |
| `raw_artifact_identity_state` | `ClosedEnum<RawArtifactIdentityStateV1>` | ["NOT_APPLICABLE","MATCH","MISMATCH","UNAVAILABLE"] | `OUTER_RAW_IDENTITY_VALIDATOR` | NEVER; use NOT_APPLICABLE or UNAVAILABLE; forbidden: ALWAYS |
| `raw_artifact_schema_state` | `ClosedEnum<RawArtifactSchemaStateV1>` | ["NOT_APPLICABLE","VALID","INVALID","UNAVAILABLE"] | `OUTER_RAW_SCHEMA_VALIDATOR` | NEVER; use NOT_APPLICABLE or UNAVAILABLE; forbidden: ALWAYS |
| `raw_result_state` | `ClosedEnum<RawResultStateV1>` | ["NOT_APPLICABLE","COMPLETE","BLOCKING","INDETERMINATE","INVALID_LITERAL","UNAVAILABLE"] | `OUTER_RAW_SCHEMA_VALIDATOR` | NEVER; use NOT_APPLICABLE or UNAVAILABLE; forbidden: ALWAYS |
| `raw_branch_consistency_state` | `ClosedEnum<RawBranchConsistencyStateV1>` | ["NOT_APPLICABLE","CONSISTENT","CONTRADICTORY","UNAVAILABLE"] | `STATIC_RAW_BRANCH_VALIDATOR` | NEVER; use NOT_APPLICABLE or UNAVAILABLE; forbidden: ALWAYS |
| `rollback_state` | `ClosedEnum<RollbackStateV1>` | ["NOT_REQUIRED","NOT_ATTEMPTED","PARTIAL_OUTPUT_REMOVED","ROLLBACK_FAILED_RESIDUE_PRESENT","ROLLBACK_RESULT_UNAVAILABLE"] | `OUTER_OUTPUT_OBSERVER` | NEVER; forbidden: ALWAYS |
| `authorization_valid_at_start` | `ClosedEnum<AuthorizationValidityAtStartV1>` | ["VALID","INVALID","UNAVAILABLE"] | `OUTER_AUTHORIZATION_CONTROLLER` | NEVER; forbidden: ALWAYS |
| `authorization_valid_at_completion` | `ClosedEnum<AuthorizationValidityAtCompletionV1>` | ["NOT_APPLICABLE","VALID","EXPIRED","INVALID","UNAVAILABLE"] | `OUTER_AUTHORIZATION_CONTROLLER` | NEVER; forbidden: ALWAYS |
| `authorization_consumption_state` | `ClosedEnum<AuthorizationConsumptionStateV1>` | ["NOT_APPLICABLE","CONSUMED","CONSUMPTION_FAILED","UNAVAILABLE"] | `OUTER_AUTHORIZATION_CONTROLLER` | NEVER; forbidden: ALWAYS |

Outer authorities, not the child program, own authorization, attempt, launch, exit, output, commit, presence, identity, schema, and rollback facts. `NOT_APPLICABLE`, `ABSENT`, and `UNAVAILABLE` are explicit semantic values, not aliases for null.

## 7. Stage 2 — `validate_normalized_inputs`

### 7.1 Deterministic rejection algorithm

```text
matched_rule_ids =
    every Stage-2 rule whose predicate evaluates true,
    sorted by explicit integer priority and then code-point rule ID

if matched_rule_ids is empty:
    return NORMALIZED_INPUT_VALID

primary_stop = typed stop of matched_rule_ids[0]
return NORMALIZED_INPUT_REJECTED(
    primary_stop,
    matched_rule_ids,
    complete_ordered_diagnostics
)
```

Every matched rule is retained. Exactly one primary stop is selected mechanically. Source enumeration order and reviewer discretion MUST NOT affect the result.

### 7.2 Rollback `NOT_ATTEMPTED` valid domain

A Stage-2-valid `rollback_state = NOT_ATTEMPTED` combination MUST have:

- `output_creation_state = PARTIAL_CREATED`;
- `output_commit_state ∈ {NOT_ATTEMPTED, COMMIT_FAILED}`;
- `raw_artifact_presence ∈ {PRESENT, ABSENT, UNAVAILABLE}`; and
- all presence-dependent raw identity, schema, result, and branch fields satisfying the ordinary raw-presence rules.

A raw result literal, including `COMPLETE`, does not imply a successful output commit. Only the explicit fact `output_commit_state = COMMITTED` denotes successful commit.

### 7.3 Complete Stage-2 rule inventory

| Rule | Priority | Predicate | Typed stop | Diagnostic | Evidence retained | Standard closure artifact |
|---|---:|---|---|---|---|---|
| `S2-001` | 100 | `execution_attempt_state == NOT_ATTEMPTED AND process_launch_state != NOT_ATTEMPTED` | `STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID` | `ATTEMPT_NOT_ATTEMPTED_BUT_LAUNCH_NOT_NOT_ATTEMPTED` | execution_attempt_ledger, process_launch_observation | `false` |
| `S2-002` | 110 | `execution_attempt_state != NOT_ATTEMPTED AND process_launch_state == NOT_ATTEMPTED` | `STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID` | `ATTEMPT_PRESENT_BUT_LAUNCH_NOT_ATTEMPTED` | execution_attempt_ledger, process_launch_observation | `false` |
| `S2-003` | 120 | `process_launch_state IN [NOT_ATTEMPTED,LAUNCH_FAILED] AND process_exit_state != NOT_APPLICABLE` | `STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS` | `EXIT_STATE_REPORTED_WITHOUT_LAUNCHED_PROCESS` | process_launch_observation, process_exit_observation | `false` |
| `S2-004` | 130 | `process_launch_state == UNAVAILABLE AND process_exit_state != UNAVAILABLE` | `STOP_CLOSURE_LAUNCH_RESULT_EXIT_RELATION_INVALID` | `LAUNCH_UNAVAILABLE_REQUIRES_EXIT_UNAVAILABLE` | process_launch_observation, process_exit_observation | `false` |
| `S2-005` | 140 | `process_launch_state == LAUNCHED AND process_exit_state == NOT_APPLICABLE` | `STOP_CLOSURE_LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE` | `LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE` | process_launch_observation, process_exit_observation | `false` |
| `S2-006` | 150 | `(process_exit_state == EXIT_OBSERVED AND process_exit_code IS_NULL) OR (process_exit_state != EXIT_OBSERVED AND process_exit_code IS_NOT_NULL)` | `STOP_CLOSURE_EXIT_CODE_NULLABILITY_INVALID` | `EXIT_CODE_NULLABILITY_RELATION_INVALID` | process_exit_observation, process_exit_code_observation | `false` |
| `S2-007` | 200 | `execution_attempt_state == NOT_ATTEMPTED AND output_creation_state != NOT_CREATED` | `STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID` | `NO_ATTEMPT_WITH_OUTPUT_CREATION` | execution_attempt_ledger, output_creation_observation | `false` |
| `S2-008` | 210 | `execution_attempt_state == NOT_ATTEMPTED AND output_commit_state != NOT_ATTEMPTED` | `STOP_CLOSURE_NO_ATTEMPT_OUTPUT_COMMIT_INVALID` | `NO_ATTEMPT_WITH_OUTPUT_COMMIT_ACTIVITY` | execution_attempt_ledger, output_commit_observation | `false` |
| `S2-009` | 220 | `execution_attempt_state == NOT_ATTEMPTED AND raw_artifact_presence != ABSENT` | `STOP_CLOSURE_NO_ATTEMPT_RAW_ARTIFACT_INVALID` | `NO_ATTEMPT_WITH_NONABSENT_RAW_ARTIFACT` | execution_attempt_ledger, raw_presence_observation | `false` |
| `S2-010` | 230 | `execution_attempt_state == NOT_ATTEMPTED AND rollback_state != NOT_REQUIRED` | `STOP_CLOSURE_NO_ATTEMPT_ROLLBACK_INVALID` | `NO_ATTEMPT_WITH_ROLLBACK_ACTIVITY` | execution_attempt_ledger, rollback_observation | `false` |
| `S2-011` | 300 | `output_commit_state == COMMITTED AND output_creation_state != COMPLETE_CREATED` | `STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID` | `COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION` | output_creation_observation, output_commit_observation | `false` |
| `S2-012` | 310 | `output_commit_state == COMMITTED AND raw_artifact_presence != PRESENT` | `STOP_CLOSURE_COMMITTED_RAW_ARTIFACT_STATE_INVALID` | `COMMITTED_OUTPUT_REQUIRES_PRESENT_RAW_ARTIFACT` | output_commit_observation, raw_presence_observation | `false` |
| `S2-013` | 320 | `output_creation_state == PARTIAL_CREATED AND output_commit_state == COMMITTED` | `STOP_CLOSURE_PARTIAL_OUTPUT_COMMITTED` | `PARTIAL_OUTPUT_CANNOT_BE_COMMITTED` | output_creation_observation, output_commit_observation | `false` |
| `S2-014` | 330 | `raw_artifact_presence == PRESENT AND output_creation_state == NOT_CREATED` | `STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION` | `RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION` | raw_presence_observation, output_creation_observation | `false` |
| `S2-015` | 400 | `rollback_state == PARTIAL_OUTPUT_REMOVED AND output_creation_state != PARTIAL_CREATED` | `STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID` | `PARTIAL_REMOVAL_REQUIRES_PARTIAL_CREATION` | rollback_observation, output_creation_observation | `false` |
| `S2-016` | 410 | `rollback_state == PARTIAL_OUTPUT_REMOVED AND output_commit_state NOT_IN [NOT_ATTEMPTED,COMMIT_FAILED]` | `STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID` | `PARTIAL_REMOVAL_REQUIRES_NO_COMMIT` | rollback_observation, output_commit_observation | `false` |
| `S2-017` | 420 | `rollback_state == PARTIAL_OUTPUT_REMOVED AND raw_artifact_presence != ABSENT` | `STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID` | `PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE` | rollback_observation, raw_presence_observation | `false` |
| `S2-018` | 430 | `rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT AND output_creation_state != PARTIAL_CREATED` | `STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID` | `ROLLBACK_RESIDUE_REQUIRES_PARTIAL_CREATION` | rollback_observation, output_creation_observation | `false` |
| `S2-019` | 440 | `rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT AND output_commit_state NOT_IN [NOT_ATTEMPTED,COMMIT_FAILED]` | `STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID` | `ROLLBACK_RESIDUE_REQUIRES_NO_COMMIT` | rollback_observation, output_commit_observation | `false` |
| `S2-020` | 450 | `rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT AND raw_artifact_presence != PRESENT` | `STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID` | `ROLLBACK_RESIDUE_REQUIRES_FINAL_PRESENCE` | rollback_observation, raw_presence_observation | `false` |
| `S2-021` | 460 | `rollback_state == ROLLBACK_RESULT_UNAVAILABLE AND output_creation_state != PARTIAL_CREATED` | `STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID` | `ROLLBACK_UNAVAILABLE_REQUIRES_PARTIAL_CREATION` | rollback_observation, output_creation_observation | `false` |
| `S2-022` | 470 | `rollback_state == ROLLBACK_RESULT_UNAVAILABLE AND raw_artifact_presence != UNAVAILABLE` | `STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID` | `ROLLBACK_UNAVAILABLE_REQUIRES_FINAL_PRESENCE_UNAVAILABLE` | rollback_observation, raw_presence_observation | `false` |
| `S2-023` | 480 | `output_creation_state == PARTIAL_CREATED AND rollback_state == NOT_REQUIRED` | `STOP_CLOSURE_PARTIAL_OUTPUT_ROLLBACK_NOT_REQUIRED` | `PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED` | output_creation_observation, rollback_observation | `false` |
| `S2-024` | 490 | `rollback_state == NOT_ATTEMPTED AND output_creation_state != PARTIAL_CREATED` | `STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_STATE_INVALID` | `ROLLBACK_NOT_ATTEMPTED_REQUIRES_PARTIAL_OUTPUT` | rollback_observation, output_creation_observation | `false` |
| `S2-049` | 495 | `rollback_state == NOT_ATTEMPTED AND output_commit_state NOT_IN [NOT_ATTEMPTED,COMMIT_FAILED]` | `STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_COMMIT_STATE_INVALID` | `ROLLBACK_NOT_ATTEMPTED_REQUIRES_NO_SUCCESSFUL_OR_UNAVAILABLE_COMMIT` | output_creation_observation, output_commit_observation, rollback_observation, final_raw_presence_observation | `false` |
| `S2-025` | 500 | `raw_artifact_presence == ABSENT AND raw_artifact_identity_state != NOT_APPLICABLE` | `STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT` | `RAW_ABSENCE_REQUIRES_IDENTITY_NOT_APPLICABLE` | raw_presence_observation, raw_artifact_identity_state_observation | `false` |
| `S2-026` | 510 | `raw_artifact_presence == ABSENT AND raw_artifact_schema_state != NOT_APPLICABLE` | `STOP_CLOSURE_RAW_SCHEMA_WITHOUT_ARTIFACT` | `RAW_ABSENCE_REQUIRES_SCHEMA_NOT_APPLICABLE` | raw_presence_observation, raw_artifact_schema_state_observation | `false` |
| `S2-027` | 520 | `raw_artifact_presence == ABSENT AND raw_result_state != NOT_APPLICABLE` | `STOP_CLOSURE_RAW_RESULT_WITHOUT_ARTIFACT` | `RAW_ABSENCE_REQUIRES_RESULT_NOT_APPLICABLE` | raw_presence_observation, raw_result_state_observation | `false` |
| `S2-028` | 530 | `raw_artifact_presence == ABSENT AND raw_branch_consistency_state != NOT_APPLICABLE` | `STOP_CLOSURE_RAW_BRANCH_WITHOUT_ARTIFACT` | `RAW_ABSENCE_REQUIRES_BRANCH_NOT_APPLICABLE` | raw_presence_observation, raw_branch_consistency_state_observation | `false` |
| `S2-029` | 540 | `raw_artifact_presence == UNAVAILABLE AND raw_artifact_identity_state != UNAVAILABLE` | `STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` | `RAW_UNAVAILABLE_REQUIRES_IDENTITY_UNAVAILABLE` | raw_presence_observation, raw_artifact_identity_state_observation | `false` |
| `S2-030` | 550 | `raw_artifact_presence == UNAVAILABLE AND raw_artifact_schema_state != UNAVAILABLE` | `STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` | `RAW_UNAVAILABLE_REQUIRES_SCHEMA_UNAVAILABLE` | raw_presence_observation, raw_artifact_schema_state_observation | `false` |
| `S2-031` | 560 | `raw_artifact_presence == UNAVAILABLE AND raw_result_state != UNAVAILABLE` | `STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` | `RAW_UNAVAILABLE_REQUIRES_RESULT_UNAVAILABLE` | raw_presence_observation, raw_result_state_observation | `false` |
| `S2-032` | 570 | `raw_artifact_presence == UNAVAILABLE AND raw_branch_consistency_state != UNAVAILABLE` | `STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` | `RAW_UNAVAILABLE_REQUIRES_BRANCH_UNAVAILABLE` | raw_presence_observation, raw_branch_consistency_state_observation | `false` |
| `S2-033` | 580 | `raw_artifact_presence == PRESENT AND raw_artifact_identity_state == NOT_APPLICABLE` | `STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` | `RAW_PRESENT_FORBIDS_IDENTITY_NOT_APPLICABLE` | raw_presence_observation, raw_artifact_identity_state_observation | `false` |
| `S2-034` | 590 | `raw_artifact_presence == PRESENT AND raw_artifact_schema_state == NOT_APPLICABLE` | `STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` | `RAW_PRESENT_FORBIDS_SCHEMA_NOT_APPLICABLE` | raw_presence_observation, raw_artifact_schema_state_observation | `false` |
| `S2-035` | 600 | `raw_artifact_presence == PRESENT AND raw_result_state == NOT_APPLICABLE` | `STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` | `RAW_PRESENT_FORBIDS_RESULT_NOT_APPLICABLE` | raw_presence_observation, raw_result_state_observation | `false` |
| `S2-036` | 610 | `raw_artifact_presence == PRESENT AND raw_branch_consistency_state == NOT_APPLICABLE` | `STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` | `RAW_PRESENT_FORBIDS_BRANCH_NOT_APPLICABLE` | raw_presence_observation, raw_branch_consistency_state_observation | `false` |
| `S2-037` | 620 | `raw_artifact_schema_state == INVALID AND raw_result_state IN [COMPLETE,BLOCKING,INDETERMINATE]` | `STOP_CLOSURE_RAW_RESULT_WITH_INVALID_SCHEMA` | `INVALID_SCHEMA_WITH_VALID_RESULT_LITERAL` | raw_schema_diagnostics, raw_result_observation | `false` |
| `S2-038` | 630 | `raw_result_state == INVALID_LITERAL AND raw_artifact_schema_state != INVALID` | `STOP_CLOSURE_INVALID_LITERAL_SCHEMA_RELATION_INVALID` | `INVALID_LITERAL_REQUIRES_INVALID_SCHEMA` | raw_schema_diagnostics, raw_result_observation | `false` |
| `S2-039` | 640 | `raw_result_state IN [COMPLETE,BLOCKING,INDETERMINATE] AND raw_artifact_schema_state != VALID` | `STOP_CLOSURE_VALID_RESULT_WITHOUT_VALID_SCHEMA` | `VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA` | raw_schema_diagnostics, raw_result_observation | `false` |
| `S2-040` | 650 | `raw_branch_consistency_state IN [CONSISTENT,CONTRADICTORY] AND raw_artifact_schema_state != VALID` | `STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID` | `BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA` | raw_schema_diagnostics, raw_branch_validation_record | `false` |
| `S2-041` | 660 | `raw_artifact_schema_state == INVALID AND raw_branch_consistency_state != UNAVAILABLE` | `STOP_CLOSURE_INVALID_SCHEMA_BRANCH_STATE_INVALID` | `INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE` | raw_schema_diagnostics, raw_branch_validation_record | `false` |
| `S2-042` | 700 | `execution_attempt_state == NOT_ATTEMPTED AND authorization_valid_at_completion != NOT_APPLICABLE` | `STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID` | `NO_ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_NOT_APPLICABLE` | execution_attempt_ledger, authorization_completion_ledger | `false` |
| `S2-043` | 710 | `execution_attempt_state != NOT_ATTEMPTED AND authorization_valid_at_completion == NOT_APPLICABLE` | `STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID` | `ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_APPLICABLE` | execution_attempt_ledger, authorization_completion_ledger | `false` |
| `S2-044` | 720 | `execution_attempt_state == NOT_ATTEMPTED AND authorization_consumption_state == CONSUMED` | `STOP_CLOSURE_AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT` | `AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT` | execution_attempt_ledger, authorization_consumption_ledger | `false` |
| `S2-045` | 730 | `execution_attempt_state == NOT_ATTEMPTED AND authorization_consumption_state IN [CONSUMPTION_FAILED,UNAVAILABLE]` | `STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID` | `NO_ATTEMPT_REQUIRES_CONSUMPTION_NOT_APPLICABLE` | execution_attempt_ledger, authorization_consumption_ledger | `false` |
| `S2-046` | 740 | `execution_attempt_state != NOT_ATTEMPTED AND authorization_consumption_state == NOT_APPLICABLE` | `STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID` | `ATTEMPT_REQUIRES_CONSUMPTION_APPLICABLE` | execution_attempt_ledger, authorization_consumption_ledger | `false` |
| `S2-047` | 800 | `process_launch_state == LAUNCH_FAILED AND output_commit_state == COMMITTED` | `STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW` | `LAUNCH_FAILED_WITH_COMMITTED_OUTPUT` | process_launch_observation, output_commit_observation | `false` |
| `S2-048` | 810 | `process_launch_state == LAUNCH_FAILED AND raw_result_state == COMPLETE` | `STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW` | `LAUNCH_FAILED_WITH_RAW_COMPLETE_RESULT` | process_launch_observation, raw_result_observation | `false` |

### 7.4 Stop precedence

The exact stop precedence is the Stage-2 rule table sorted by `(priority ascending, rule_id Unicode code-point ascending)`. Equal priorities are permitted only when rule-ID ordering resolves them; this candidate uses unique priorities for all forty-nine rules.

## 8. Stage 3 — `reduce_execution_closure`

### 8.1 Precondition and meaning

The reducer MUST receive only `NORMALIZED_INPUT_VALID`. It MUST NOT repair or reinterpret a rejected vector. The output label is the primary factual classification; the complete normalized object remains mandatory evidence. No label means accepted, approved, clear, ready, authorized, or implementation-eligible.

### 8.2 Closure-state inventory

| State | Factual description | Acceptance effect |
|---|---|---|
| `CLOSURE_ROLLBACK_RESIDUE_PRESENT` | A partial output remains after rollback failed; residue is the dominant primary factual classification. | `NONE` |
| `CLOSURE_ROLLBACK_RESULT_UNAVAILABLE` | The cleanup result and final residue disposition cannot be established. | `NONE` |
| `CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` | A partial output was created, no successful commit occurred, rollback was not attempted, and residue is present at the exact output path. | `NONE` |
| `CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE` | A partial output was created, no successful commit occurred, rollback was not attempted, and final residue presence is unavailable. | `NONE` |
| `CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` | A partial output was created, no successful commit occurred, rollback was not attempted, and the final output path is absent; the state does not attribute absence to authorized cleanup. | `NONE` |
| `CLOSURE_AUTHORIZATION_INVALID_AT_START` | The outer authority controller established that authority was invalid at the execution-start boundary. | `NONE` |
| `CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE` | The outer authority controller could not establish authority validity at the execution-start boundary. | `NONE` |
| `CLOSURE_EXECUTION_ATTEMPT_MULTIPLE` | The outer attempt ledger establishes more than one execution attempt under the single-use boundary. | `NONE` |
| `CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE` | The outer attempt ledger cannot establish whether exactly one attempt occurred. | `NONE` |
| `CLOSURE_EXECUTION_NOT_ATTEMPTED` | No execution attempt occurred. | `NONE` |
| `CLOSURE_PROCESS_LAUNCH_FAILED` | An execution attempt was recorded but process launch failed. | `NONE` |
| `CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE` | An execution attempt was recorded but launch disposition is unavailable. | `NONE` |
| `CLOSURE_PROCESS_EXIT_UNAVAILABLE` | The process was launched but a terminal exit observation is absent or unavailable. | `NONE` |
| `CLOSURE_PROCESS_EXIT_NONZERO` | The process exit was observed with a nonzero signed exit code. | `NONE` |
| `CLOSURE_OUTPUT_STATE_UNAVAILABLE` | Creation, commit, or final raw-presence state is unavailable outside the exact rollback-unavailable pattern. | `NONE` |
| `CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH` | Present raw bytes do not match the expected raw-artifact identity. | `NONE` |
| `CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE` | Raw identity, schema, or branch-consistency validation is unavailable. | `NONE` |
| `CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID` | A present raw artifact fails the exact raw-evidence schema. | `NONE` |
| `CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION` | A schema-valid raw artifact contradicts the sealed-script branch crosswalk. | `NONE` |
| `CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION` | Authority was valid at start and expired before execution closure. | `NONE` |
| `CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION` | Authority was valid at start but is invalid, other than simple expiry, at completion. | `NONE` |
| `CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE` | Authority validity at completion is unavailable. | `NONE` |
| `CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED` | The outer controller failed to record the required authorization consumption. | `NONE` |
| `CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE` | The outer controller cannot establish authorization-consumption disposition. | `NONE` |
| `CLOSURE_PARTIAL_OUTPUT_REMOVED` | A partial output was not committed and was successfully removed. | `NONE` |
| `CLOSURE_PROCESS_EXITED_NO_OUTPUT` | The process exited with code zero, no output was created, and no raw artifact exists. | `NONE` |
| `CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT` | Terminal execution closure exists but no committed complete valid raw artifact exists. | `NONE` |
| `CLOSURE_VALID_RAW_BLOCKING_REPORTED` | A committed, identity-matching, schema-valid, branch-consistent raw artifact reports BLOCKING. | `NONE` |
| `CLOSURE_VALID_RAW_INDETERMINATE_REPORTED` | A committed, identity-matching, schema-valid, branch-consistent raw artifact reports INDETERMINATE. | `NONE` |
| `CLOSURE_VALID_RAW_COMPLETE_REPORTED` | A committed, identity-matching, schema-valid, branch-consistent raw artifact reports COMPLETE; this remains factual only. | `NONE` |
| `CLOSURE_EXECUTION_RESULT_INDETERMINATE` | No prior factual rule applies; the closed final rule classifies the remaining valid vector as indeterminate. | `NONE` |

### 8.3 Ordered first-match reducer

| Rule | Priority | Predicate | Closure state |
|---|---:|---|---|
| `S3-001` | 1 | `rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT` | `CLOSURE_ROLLBACK_RESIDUE_PRESENT` |
| `S3-002` | 2 | `rollback_state == ROLLBACK_RESULT_UNAVAILABLE` | `CLOSURE_ROLLBACK_RESULT_UNAVAILABLE` |
| `S3-003` | 3 | `rollback_state == NOT_ATTEMPTED AND output_creation_state == PARTIAL_CREATED AND output_commit_state IN [NOT_ATTEMPTED,COMMIT_FAILED] AND raw_artifact_presence == PRESENT` | `CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-004` | 4 | `rollback_state == NOT_ATTEMPTED AND output_creation_state == PARTIAL_CREATED AND output_commit_state IN [NOT_ATTEMPTED,COMMIT_FAILED] AND raw_artifact_presence == UNAVAILABLE` | `CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE` |
| `S3-005` | 5 | `rollback_state == NOT_ATTEMPTED AND output_creation_state == PARTIAL_CREATED AND output_commit_state IN [NOT_ATTEMPTED,COMMIT_FAILED] AND raw_artifact_presence == ABSENT` | `CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` |
| `S3-006` | 6 | `authorization_valid_at_start == INVALID` | `CLOSURE_AUTHORIZATION_INVALID_AT_START` |
| `S3-007` | 7 | `authorization_valid_at_start == UNAVAILABLE` | `CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE` |
| `S3-008` | 8 | `execution_attempt_state == MULTIPLE` | `CLOSURE_EXECUTION_ATTEMPT_MULTIPLE` |
| `S3-009` | 9 | `execution_attempt_state == UNAVAILABLE` | `CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE` |
| `S3-010` | 10 | `execution_attempt_state == NOT_ATTEMPTED` | `CLOSURE_EXECUTION_NOT_ATTEMPTED` |
| `S3-011` | 11 | `process_launch_state == LAUNCH_FAILED` | `CLOSURE_PROCESS_LAUNCH_FAILED` |
| `S3-012` | 12 | `process_launch_state == UNAVAILABLE` | `CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE` |
| `S3-013` | 13 | `process_exit_state IN [EXIT_NOT_OBSERVED,UNAVAILABLE]` | `CLOSURE_PROCESS_EXIT_UNAVAILABLE` |
| `S3-014` | 14 | `process_exit_state == EXIT_OBSERVED AND process_exit_code != 0` | `CLOSURE_PROCESS_EXIT_NONZERO` |
| `S3-015` | 15 | `output_creation_state == UNAVAILABLE OR output_commit_state == UNAVAILABLE OR raw_artifact_presence == UNAVAILABLE` | `CLOSURE_OUTPUT_STATE_UNAVAILABLE` |
| `S3-016` | 16 | `raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MISMATCH` | `CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH` |
| `S3-017` | 17 | `raw_artifact_presence == PRESENT AND raw_artifact_identity_state == UNAVAILABLE` | `CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE` |
| `S3-018` | 18 | `raw_artifact_presence == PRESENT AND raw_artifact_schema_state == INVALID` | `CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID` |
| `S3-019` | 19 | `raw_artifact_presence == PRESENT AND raw_artifact_schema_state == UNAVAILABLE` | `CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE` |
| `S3-020` | 20 | `raw_artifact_presence == PRESENT AND raw_branch_consistency_state == CONTRADICTORY` | `CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION` |
| `S3-021` | 21 | `raw_artifact_presence == PRESENT AND raw_branch_consistency_state == UNAVAILABLE` | `CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE` |
| `S3-022` | 22 | `authorization_valid_at_completion == EXPIRED` | `CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION` |
| `S3-023` | 23 | `authorization_valid_at_completion == INVALID` | `CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION` |
| `S3-024` | 24 | `authorization_valid_at_completion == UNAVAILABLE` | `CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE` |
| `S3-025` | 25 | `authorization_consumption_state == CONSUMPTION_FAILED` | `CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED` |
| `S3-026` | 26 | `authorization_consumption_state == UNAVAILABLE` | `CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE` |
| `S3-027` | 27 | `rollback_state == PARTIAL_OUTPUT_REMOVED` | `CLOSURE_PARTIAL_OUTPUT_REMOVED` |
| `S3-028` | 28 | `process_exit_state == EXIT_OBSERVED AND process_exit_code == 0 AND output_creation_state == NOT_CREATED AND raw_artifact_presence == ABSENT` | `CLOSURE_PROCESS_EXITED_NO_OUTPUT` |
| `S3-029` | 29 | `raw_artifact_presence == ABSENT OR output_creation_state != COMPLETE_CREATED OR output_commit_state != COMMITTED` | `CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT` |
| `S3-030` | 30 | `output_creation_state == COMPLETE_CREATED AND output_commit_state == COMMITTED AND raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MATCH AND raw_artifact_schema_state == VALID AND raw_branch_consistency_state == CONSISTENT AND raw_result_state == BLOCKING` | `CLOSURE_VALID_RAW_BLOCKING_REPORTED` |
| `S3-031` | 31 | `output_creation_state == COMPLETE_CREATED AND output_commit_state == COMMITTED AND raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MATCH AND raw_artifact_schema_state == VALID AND raw_branch_consistency_state == CONSISTENT AND raw_result_state == INDETERMINATE` | `CLOSURE_VALID_RAW_INDETERMINATE_REPORTED` |
| `S3-032` | 32 | `output_creation_state == COMPLETE_CREATED AND output_commit_state == COMMITTED AND raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MATCH AND raw_artifact_schema_state == VALID AND raw_branch_consistency_state == CONSISTENT AND raw_result_state == COMPLETE` | `CLOSURE_VALID_RAW_COMPLETE_REPORTED` |
| `S3-033` | 33 | `TRUE` | `CLOSURE_EXECUTION_RESULT_INDETERMINATE` |

The first five factual priorities are exactly rollback failure with residue, rollback result unavailable, rollback not attempted with residue present, rollback not attempted with presence unavailable, and rollback not attempted with final absence. These dominate authority, multiplicity, launch, exit, raw validation, authorization completion, consumption, and raw result literals.

This precedence prevents an unperformed or unresolved cleanup from being hidden by apparently complete evidence or by another factual defect. `CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` records only final absence; it does not claim that authorized rollback caused the absence.

### 8.4 Formal properties

- **Coverage:** the final rule `S3-033` has predicate `TRUE`, so every Stage-2-valid vector maps.
- **Uniqueness:** ordered first-match semantics returns at the first true predicate and evaluates no later return.
- **Determinism:** predicates are pure functions of the exact normalized object and fixed rule order.
- **Termination:** the finite list contains thirty-three rules and an unconditional final rule.
- **No reviewer discretion:** no rule contains a judgment field, reviewer choice, or qualitative fallback.

## 9. Stage 4 — `verify_emitted_closure`

`emitted_closure_state` is a Stage-4-only field and is not one of the fifteen normalized execution facts.

```text
expected_closure_state = reduce_execution_closure(normalized_inputs)

if emitted_closure_state != expected_closure_state:
    POST_REDUCTION_REJECTED(
        STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH,
        expected_closure_state,
        emitted_closure_state,
        reducer_trace
    )
else:
    POST_REDUCTION_VERIFIED
```

| Rule | Priority | Predicate | Result | Typed stop |
|---|---:|---|---|---|
| `S4-001` | 10 | `emitted_closure_state != expected_closure_state` | `POST_REDUCTION_REJECTED` | `STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH` |
| `S4-002` | 20 | `emitted_closure_state == expected_closure_state` | `POST_REDUCTION_VERIFIED` | `null` |

Stage 4 verifies conformance only. `POST_REDUCTION_VERIFIED` has `acceptance_effect = NONE`.

## 10. Example-vector reconciliation

The appendix contains exactly 137 vectors: 32 Stage-1 vectors, 54 Stage-2 vectors, 46 Stage-3 vectors, and 5 Stage-4 vectors.

Every Stage-2 rule has at least one target vector. Every closure state has at least one Stage-2-valid reducer vector. Required rollback conflicts cover invalid authority at start, multiple attempts, launch failure, nonzero exit, raw identity mismatch, invalid raw schema, raw `COMPLETE`, authority expiry, and consumption failure.

| Example | Stage | Description | Expected result |
|---|---:|---|---|
| `S1-EX-A001` | 1 | Invalid UTF-8 stops Group A immediately | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_UTF8_INVALID` |
| `S1-EX-A002` | 1 | Truncated JSON stops before duplicate and shape inspection | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_JSON_PARSE_INVALID` |
| `S1-EX-A003` | 1 | Duplicate key detected before object construction | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_DUPLICATE_JSON_KEY` |
| `S1-EX-A004` | 1 | Top-level array rejected | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_TOP_LEVEL_OBJECT_REQUIRED` |
| `S1-EX-A005` | 1 | Plus-prefixed number is invalid JSON and never reaches number-token rules | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_JSON_PARSE_INVALID` |
| `S1-EX-A006` | 1 | Leading-zero number is invalid JSON and never reaches number-token rules | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_JSON_PARSE_INVALID` |
| `S1-EX-B001` | 1 | process_exit_code missing; no type, lexical, or range rule evaluates | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_REQUIRED_FIELD_MISSING` |
| `S1-EX-B002` | 1 | Unexpected field and excess cardinality retained together | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_UNEXPECTED_FIELD` |
| `S1-EX-B003` | 1 | Missing and unexpected fields together with unchanged member count | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_REQUIRED_FIELD_MISSING` |
| `S1-EX-B004` | 1 | Enum field missing; Group D cannot inspect it | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_REQUIRED_FIELD_MISSING` |
| `S1-EX-C001` | 1 | process_exit_code string rejected before number lexical/range inspection | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` |
| `S1-EX-C002` | 1 | process_exit_code array rejected before number lexical/range inspection | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` |
| `S1-EX-C003` | 1 | process_exit_code object rejected before number lexical/range inspection | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` |
| `S1-EX-C004` | 1 | process_exit_code boolean rejected before number lexical/range inspection | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID` |
| `S1-EX-C005` | 1 | Enum field null matches both non-null and enum-type rules; deterministic primary stop | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_NULL_REPRESENTATION_INVALID` |
| `S1-EX-C006` | 1 | Enum field integer rejected; lexical and membership rules do not evaluate | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_ENUM_JSON_TYPE_INVALID` |
| `S1-EX-C007` | 1 | Wrong-type array containing a lexically invalid-looking token is rejected only by Group C | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_ENUM_JSON_TYPE_INVALID` |
| `S1-EX-D001` | 1 | Enum lexical form invalid | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_ENUM_TOKEN_LEXICAL_INVALID` |
| `S1-EX-D002` | 1 | Lexically valid but unregistered enum token | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_ENUM_TOKEN_UNREGISTERED` |
| `S1-EX-N001` | 1 | Exact process_exit_code token 0 | `PARSE_AND_SHAPE_VALID` |
| `S1-EX-N002` | 1 | Exact process_exit_code token -0 | `PARSE_AND_SHAPE_VALID` |
| `S1-EX-N003` | 1 | Exact process_exit_code token 1 | `PARSE_AND_SHAPE_VALID` |
| `S1-EX-N004` | 1 | Exact process_exit_code token -1 | `PARSE_AND_SHAPE_VALID` |
| `S1-EX-N005` | 1 | Exact process_exit_code token 2147483647 | `PARSE_AND_SHAPE_VALID` |
| `S1-EX-N006` | 1 | Exact process_exit_code token -2147483648 | `PARSE_AND_SHAPE_VALID` |
| `S1-EX-N007` | 1 | Exact process_exit_code token 2147483648 | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_RANGE_INVALID` |
| `S1-EX-N008` | 1 | Exact process_exit_code token -2147483649 | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_RANGE_INVALID` |
| `S1-EX-N009` | 1 | Exact process_exit_code token 1.0 | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` |
| `S1-EX-N010` | 1 | Exact process_exit_code token 1e0 | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` |
| `S1-EX-N011` | 1 | Exact process_exit_code token 1E0 | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` |
| `S1-EX-N012` | 1 | Exact process_exit_code token -2.5 | `PARSE_AND_SHAPE_REJECTED / STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID` |
| `S1-EX-N013` | 1 | JSON null is a valid Stage-1 representation for process_exit_code | `PARSE_AND_SHAPE_VALID` |
| `S2-EX-001` | 2 | Witness for S2-001: ATTEMPT_NOT_ATTEMPTED_BUT_LAUNCH_NOT_NOT_ATTEMPTED | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID` |
| `S2-EX-002` | 2 | Witness for S2-002: ATTEMPT_PRESENT_BUT_LAUNCH_NOT_ATTEMPTED | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID` |
| `S2-EX-003` | 2 | Witness for S2-003: EXIT_STATE_REPORTED_WITHOUT_LAUNCHED_PROCESS | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS` |
| `S2-EX-004` | 2 | Witness for S2-004: LAUNCH_UNAVAILABLE_REQUIRES_EXIT_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_LAUNCH_RESULT_EXIT_RELATION_INVALID` |
| `S2-EX-005` | 2 | Witness for S2-005: LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE` |
| `S2-EX-006` | 2 | Witness for S2-006: EXIT_CODE_NULLABILITY_RELATION_INVALID | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_EXIT_CODE_NULLABILITY_INVALID` |
| `S2-EX-007` | 2 | Witness for S2-007: NO_ATTEMPT_WITH_OUTPUT_CREATION | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID` |
| `S2-EX-008` | 2 | Witness for S2-008: NO_ATTEMPT_WITH_OUTPUT_COMMIT_ACTIVITY | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_NO_ATTEMPT_OUTPUT_COMMIT_INVALID` |
| `S2-EX-009` | 2 | Witness for S2-009: NO_ATTEMPT_WITH_NONABSENT_RAW_ARTIFACT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_NO_ATTEMPT_RAW_ARTIFACT_INVALID` |
| `S2-EX-010` | 2 | Witness for S2-010: NO_ATTEMPT_WITH_ROLLBACK_ACTIVITY | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID` |
| `S2-EX-011` | 2 | Witness for S2-011: COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID` |
| `S2-EX-012` | 2 | Witness for S2-012: COMMITTED_OUTPUT_REQUIRES_PRESENT_RAW_ARTIFACT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_COMMITTED_RAW_ARTIFACT_STATE_INVALID` |
| `S2-EX-013` | 2 | Witness for S2-013: PARTIAL_OUTPUT_CANNOT_BE_COMMITTED | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID` |
| `S2-EX-014` | 2 | Witness for S2-014: RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION` |
| `S2-EX-015` | 2 | Witness for S2-015: PARTIAL_REMOVAL_REQUIRES_PARTIAL_CREATION | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID` |
| `S2-EX-016` | 2 | Witness for S2-016: PARTIAL_REMOVAL_REQUIRES_NO_COMMIT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID` |
| `S2-EX-017` | 2 | Witness for S2-017: PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID` |
| `S2-EX-018` | 2 | Witness for S2-018: ROLLBACK_RESIDUE_REQUIRES_PARTIAL_CREATION | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID` |
| `S2-EX-019` | 2 | Witness for S2-019: ROLLBACK_RESIDUE_REQUIRES_NO_COMMIT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID` |
| `S2-EX-020` | 2 | Witness for S2-020: ROLLBACK_RESIDUE_REQUIRES_FINAL_PRESENCE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID` |
| `S2-EX-021` | 2 | Witness for S2-021: ROLLBACK_UNAVAILABLE_REQUIRES_PARTIAL_CREATION | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID` |
| `S2-EX-022` | 2 | Witness for S2-022: ROLLBACK_UNAVAILABLE_REQUIRES_FINAL_PRESENCE_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID` |
| `S2-EX-023` | 2 | Witness for S2-023: PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_PARTIAL_OUTPUT_ROLLBACK_NOT_REQUIRED` |
| `S2-EX-024` | 2 | Witness for S2-024: ROLLBACK_NOT_ATTEMPTED_REQUIRES_PARTIAL_OUTPUT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_STATE_INVALID` |
| `S2-EX-025` | 2 | Witness for S2-025: RAW_ABSENCE_REQUIRES_IDENTITY_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT` |
| `S2-EX-026` | 2 | Witness for S2-026: RAW_ABSENCE_REQUIRES_SCHEMA_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_SCHEMA_WITHOUT_ARTIFACT` |
| `S2-EX-027` | 2 | Witness for S2-027: RAW_ABSENCE_REQUIRES_RESULT_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_RESULT_WITHOUT_ARTIFACT` |
| `S2-EX-028` | 2 | Witness for S2-028: RAW_ABSENCE_REQUIRES_BRANCH_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_BRANCH_WITHOUT_ARTIFACT` |
| `S2-EX-029` | 2 | Witness for S2-029: RAW_UNAVAILABLE_REQUIRES_IDENTITY_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` |
| `S2-EX-030` | 2 | Witness for S2-030: RAW_UNAVAILABLE_REQUIRES_SCHEMA_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` |
| `S2-EX-031` | 2 | Witness for S2-031: RAW_UNAVAILABLE_REQUIRES_RESULT_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` |
| `S2-EX-032` | 2 | Witness for S2-032: RAW_UNAVAILABLE_REQUIRES_BRANCH_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID` |
| `S2-EX-033` | 2 | Witness for S2-033: RAW_PRESENT_FORBIDS_IDENTITY_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` |
| `S2-EX-034` | 2 | Witness for S2-034: RAW_PRESENT_FORBIDS_SCHEMA_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` |
| `S2-EX-035` | 2 | Witness for S2-035: RAW_PRESENT_FORBIDS_RESULT_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` |
| `S2-EX-036` | 2 | Witness for S2-036: RAW_PRESENT_FORBIDS_BRANCH_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` |
| `S2-EX-037` | 2 | Witness for S2-037: INVALID_SCHEMA_WITH_VALID_RESULT_LITERAL | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_RESULT_WITH_INVALID_SCHEMA` |
| `S2-EX-038` | 2 | Witness for S2-038: INVALID_LITERAL_REQUIRES_INVALID_SCHEMA | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_INVALID_LITERAL_SCHEMA_RELATION_INVALID` |
| `S2-EX-039` | 2 | Witness for S2-039: VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_VALID_RESULT_WITHOUT_VALID_SCHEMA` |
| `S2-EX-040` | 2 | Witness for S2-040: BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID` |
| `S2-EX-041` | 2 | Witness for S2-041: INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID` |
| `S2-EX-042` | 2 | Witness for S2-042: NO_ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID` |
| `S2-EX-043` | 2 | Witness for S2-043: ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID` |
| `S2-EX-044` | 2 | Witness for S2-044: AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT` |
| `S2-EX-045` | 2 | Witness for S2-045: NO_ATTEMPT_REQUIRES_CONSUMPTION_NOT_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID` |
| `S2-EX-046` | 2 | Witness for S2-046: ATTEMPT_REQUIRES_CONSUMPTION_APPLICABLE | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID` |
| `S2-EX-047` | 2 | Witness for S2-047: LAUNCH_FAILED_WITH_COMMITTED_OUTPUT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW` |
| `S2-EX-048` | 2 | Witness for S2-048: LAUNCH_FAILED_WITH_RAW_COMPLETE_RESULT | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION` |
| `S2-OVERLAP-01` | 2 | Overlapping normalized contradictions with deterministic primary-stop selection | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS` |
| `S2-OVERLAP-02` | 2 | Overlapping normalized contradictions with deterministic primary-stop selection | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT` |
| `S2-OVERLAP-03` | 2 | Overlapping normalized contradictions with deterministic primary-stop selection | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID` |
| `S2-OVERLAP-04` | 2 | Overlapping normalized contradictions with deterministic primary-stop selection | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID` |
| `S2-OVERLAP-05` | 2 | Overlapping normalized contradictions with deterministic primary-stop selection | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE` |
| `S2-EX-054` | 2 | Witness for S2-049: rollback NOT_ATTEMPTED permits only NOT_ATTEMPTED or COMMIT_FAILED commit states | `NORMALIZED_INPUT_REJECTED / STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_COMMIT_STATE_INVALID` |
| `S3-STATE-CLOSURE_ROLLBACK_RESIDUE_PRESENT` | 3 | Representative normalized-valid vector for CLOSURE_ROLLBACK_RESIDUE_PRESENT | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESIDUE_PRESENT` |
| `S3-STATE-CLOSURE_ROLLBACK_RESULT_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_ROLLBACK_RESULT_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESULT_UNAVAILABLE` |
| `S3-STATE-CLOSURE_AUTHORIZATION_INVALID_AT_START` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_INVALID_AT_START | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_INVALID_AT_START` |
| `S3-STATE-CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE` |
| `S3-STATE-CLOSURE_EXECUTION_ATTEMPT_MULTIPLE` | 3 | Representative normalized-valid vector for CLOSURE_EXECUTION_ATTEMPT_MULTIPLE | `CLOSURE_STATE_REDUCED / CLOSURE_EXECUTION_ATTEMPT_MULTIPLE` |
| `S3-STATE-CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE` |
| `S3-STATE-CLOSURE_EXECUTION_NOT_ATTEMPTED` | 3 | Representative normalized-valid vector for CLOSURE_EXECUTION_NOT_ATTEMPTED | `CLOSURE_STATE_REDUCED / CLOSURE_EXECUTION_NOT_ATTEMPTED` |
| `S3-STATE-CLOSURE_PROCESS_LAUNCH_FAILED` | 3 | Representative normalized-valid vector for CLOSURE_PROCESS_LAUNCH_FAILED | `CLOSURE_STATE_REDUCED / CLOSURE_PROCESS_LAUNCH_FAILED` |
| `S3-STATE-CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE` |
| `S3-STATE-CLOSURE_PROCESS_EXIT_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_PROCESS_EXIT_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_PROCESS_EXIT_UNAVAILABLE` |
| `S3-STATE-CLOSURE_PROCESS_EXIT_NONZERO` | 3 | Representative normalized-valid vector for CLOSURE_PROCESS_EXIT_NONZERO | `CLOSURE_STATE_REDUCED / CLOSURE_PROCESS_EXIT_NONZERO` |
| `S3-STATE-CLOSURE_OUTPUT_STATE_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_OUTPUT_STATE_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_OUTPUT_STATE_UNAVAILABLE` |
| `S3-STATE-CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH` | 3 | Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH | `CLOSURE_STATE_REDUCED / CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH` |
| `S3-STATE-CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE` |
| `S3-STATE-CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID` | 3 | Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID | `CLOSURE_STATE_REDUCED / CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID` |
| `S3-STATE-CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION` | 3 | Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION | `CLOSURE_STATE_REDUCED / CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION` |
| `S3-STATE-CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION` |
| `S3-STATE-CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION` |
| `S3-STATE-CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE` |
| `S3-STATE-CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED` |
| `S3-STATE-CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE` | 3 | Representative normalized-valid vector for CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE` |
| `S3-STATE-CLOSURE_PARTIAL_OUTPUT_REMOVED` | 3 | Representative normalized-valid vector for CLOSURE_PARTIAL_OUTPUT_REMOVED | `CLOSURE_STATE_REDUCED / CLOSURE_PARTIAL_OUTPUT_REMOVED` |
| `S3-STATE-CLOSURE_PROCESS_EXITED_NO_OUTPUT` | 3 | Representative normalized-valid vector for CLOSURE_PROCESS_EXITED_NO_OUTPUT | `CLOSURE_STATE_REDUCED / CLOSURE_PROCESS_EXITED_NO_OUTPUT` |
| `S3-STATE-CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT` | 3 | Representative normalized-valid vector for CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT | `CLOSURE_STATE_REDUCED / CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT` |
| `S3-STATE-CLOSURE_VALID_RAW_BLOCKING_REPORTED` | 3 | Representative normalized-valid vector for CLOSURE_VALID_RAW_BLOCKING_REPORTED | `CLOSURE_STATE_REDUCED / CLOSURE_VALID_RAW_BLOCKING_REPORTED` |
| `S3-STATE-CLOSURE_VALID_RAW_INDETERMINATE_REPORTED` | 3 | Representative normalized-valid vector for CLOSURE_VALID_RAW_INDETERMINATE_REPORTED | `CLOSURE_STATE_REDUCED / CLOSURE_VALID_RAW_INDETERMINATE_REPORTED` |
| `S3-STATE-CLOSURE_VALID_RAW_COMPLETE_REPORTED` | 3 | Representative normalized-valid vector for CLOSURE_VALID_RAW_COMPLETE_REPORTED | `CLOSURE_STATE_REDUCED / CLOSURE_VALID_RAW_COMPLETE_REPORTED` |
| `S3-STATE-CLOSURE_EXECUTION_RESULT_INDETERMINATE` | 3 | Representative normalized-valid vector for CLOSURE_EXECUTION_RESULT_INDETERMINATE | `CLOSURE_STATE_REDUCED / CLOSURE_EXECUTION_RESULT_INDETERMINATE` |
| `S3-CONFLICT-RESIDUE-AUTH-INVALID` | 3 | Precedence-conflict or final-fallback vector | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESIDUE_PRESENT` |
| `S3-CONFLICT-RESIDUE-MULTIPLE` | 3 | Precedence-conflict or final-fallback vector | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESIDUE_PRESENT` |
| `S3-CONFLICT-RESIDUE-LAUNCH-FAILED` | 3 | Precedence-conflict or final-fallback vector | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESIDUE_PRESENT` |
| `S3-CONFLICT-RESIDUE-COMPLETE-RAW` | 3 | Precedence-conflict or final-fallback vector | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESIDUE_PRESENT` |
| `S3-CONFLICT-ROLLBACK-UNAVAILABLE-CHILD-COMPLETE-ECHO` | 3 | Precedence-conflict or final-fallback vector | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_RESULT_UNAVAILABLE` |
| `S3-FINAL-INDETERMINATE` | 3 | Precedence-conflict or final-fallback vector | `CLOSURE_STATE_REDUCED / CLOSURE_EXECUTION_RESULT_INDETERMINATE` |
| `S3-STATE-CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` | 3 | Representative Stage-2-valid vector for CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-STATE-CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE` | 3 | Representative Stage-2-valid vector for CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE` |
| `S3-STATE-CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` | 3 | Representative Stage-2-valid vector for CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` |
| `S3-C03-CONFLICT-001` | 3 | rollback NOT_ATTEMPTED residue present dominates invalid authority at start | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-C03-CONFLICT-002` | 3 | rollback NOT_ATTEMPTED residue unavailable dominates multiple attempts | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE` |
| `S3-C03-CONFLICT-003` | 3 | rollback NOT_ATTEMPTED final absence dominates launch failure | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` |
| `S3-C03-CONFLICT-004` | 3 | rollback NOT_ATTEMPTED residue present dominates nonzero exit | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-C03-CONFLICT-005` | 3 | rollback NOT_ATTEMPTED residue present dominates raw identity mismatch | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-C03-CONFLICT-006` | 3 | rollback NOT_ATTEMPTED residue present dominates invalid raw schema | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-C03-CONFLICT-007` | 3 | rollback NOT_ATTEMPTED residue present dominates apparently COMPLETE raw result | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT` |
| `S3-C03-CONFLICT-008` | 3 | rollback NOT_ATTEMPTED residue unavailable dominates authority expiry | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE` |
| `S3-C03-CONFLICT-009` | 3 | rollback NOT_ATTEMPTED final absence dominates consumption failure | `CLOSURE_STATE_REDUCED / CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE` |
| `S4-EX-001` | 4 | Emitted state exactly equals reducer output | `POST_REDUCTION_VERIFIED` |
| `S4-EX-002` | 4 | Emitted state differs from reducer output | `POST_REDUCTION_REJECTED / STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH` |
| `S4-EX-003` | 4 | Complete-looking emitted state while attempt multiplicity is unavailable | `POST_REDUCTION_REJECTED / STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH` |
| `S4-EX-004` | 4 | Blocking emitted state while reducer returns rollback residue | `POST_REDUCTION_REJECTED / STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH` |
| `S4-C03-EX-005` | 4 | Complete-looking emitted state cannot override rollback NOT_ATTEMPTED residue-present classification | `POST_REDUCTION_REJECTED / STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH` |

## 11. Self-attack

| Attack | Attempt | Counterexample found | Exact result |
|---|---|---|---|
| `SA-01` | Find a missing field inspected by a later lexical rule | `NONE` | Group B rejects and suppresses Groups C and D; `process_exit_code`-missing and enum-missing vectors prove suppression. |
| `SA-02` | Find a wrong-type value inspected by a later range rule | `NONE` | Group C rejects BOOLEAN/STRING/ARRAY/OBJECT; D-003/D-004 prerequisites require NUMBER. |
| `SA-03` | Find two conforming implementations classifying `1.0` differently | `NONE` | The exact original token fails `^-?(0\|[1-9][0-9]*)$` before native conversion. |
| `SA-04` | Make native integer overflow affect classification | `NONE` | The accepted token is parsed as an unbounded mathematical integer before signed-Int32 range comparison. |
| `SA-05` | Find partial output with rollback NOT_ATTEMPTED that reaches a non-rollback primary state | `NONE` | All three presence values match S3-003, S3-004, or S3-005 before every non-rollback rule. |
| `SA-06` | Hide rollback NOT_ATTEMPTED behind authority or raw evidence | `NONE` | Nine conflict vectors retain all facts and select the appropriate dominant rollback state. |
| `SA-07` | Make a parser rejection reach Stage 2 | `NONE` | Every Group failure has `later_groups_execute_after_failure = false` and Stage-1 rejection forbids normalization. |
| `SA-08` | Make a Stage-2 rejection reach Stage 3 | `NONE` | The reducer precondition is exactly `NORMALIZED_INPUT_VALID`. |
| `SA-09` | Make an emitted-state mismatch pass Stage 4 | `NONE` | S4-001 precedes equality and returns `STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH`. |
| `SA-10` | Find a closure state with non-NONE authorization effect | `NONE` | All 31 states mechanically declare `acceptance_effect = NONE`. |

**Strongest alternative design.** Evaluate every Stage-1 rule against a partially constructed object and let inapplicable predicates return false. This is rejected because missing and wrong-type fields would make rule applicability implementation-dependent and could silently suppress diagnostics. Explicit group dependencies are the separating requirement.

## 12. Machine-readable review appendix

The following JSON is review support only. It is not a registry overlay, canonical artifact, executable contract, acceptance predicate, or authorization record.

```json
{
  "stage_1_groups": [
    {
      "group_id": "A",
      "name": "BYTE_AND_PARSER_GATES",
      "evaluation_mode": "SEQUENTIAL_FIRST_FAILURE",
      "prerequisite": "raw_document_bytes supplied",
      "ordered_rule_ids": [
        "S1-A-001",
        "S1-A-002",
        "S1-A-003",
        "S1-A-004"
      ],
      "diagnostic_order": [
        "rule priority ascending",
        "rule_id Unicode code-point order"
      ],
      "failure_result": "PARSE_AND_SHAPE_REJECTED(primary_stop,[matched_rule_id],[single_diagnostic])",
      "later_groups_execute_after_failure": false,
      "normalization_permitted_after_failure": false
    },
    {
      "group_id": "B",
      "name": "TOP_LEVEL_SHAPE_GATES",
      "evaluation_mode": "EVALUATE_ALL_ELIGIBLE_RULES",
      "prerequisite": "Group A cleared",
      "ordered_rule_ids": [
        "S1-B-001",
        "S1-B-002",
        "S1-B-003"
      ],
      "diagnostic_order": [
        "priority ascending",
        "rule_id Unicode code-point order",
        "field name Unicode code-point order"
      ],
      "failure_result": "PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics)",
      "primary_stop": "typed_stop of first ordered matched rule",
      "later_groups_execute_after_failure": false,
      "normalization_permitted_after_failure": false
    },
    {
      "group_id": "C",
      "name": "FIELD_REPRESENTATION_AND_JSON_TYPE_GATES",
      "evaluation_mode": "EVALUATE_ALL_ELIGIBLE_RULES",
      "prerequisite": "Groups A and B cleared",
      "ordered_rule_ids": [
        "S1-C-001",
        "S1-C-002",
        "S1-C-003"
      ],
      "diagnostic_order": [
        "priority ascending",
        "rule_id Unicode code-point order",
        "field name Unicode code-point order"
      ],
      "failure_result": "PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics)",
      "primary_stop": "typed_stop of first ordered matched rule",
      "later_groups_execute_after_failure": false,
      "normalization_permitted_after_failure": false
    },
    {
      "group_id": "D",
      "name": "VALUE_LEXICAL_MEMBERSHIP_AND_RANGE_GATES",
      "evaluation_mode": "EVALUATE_ALL_RULES_WITH_SATISFIED_PER_FIELD_PREREQUISITES",
      "prerequisite": "Groups A, B, and C cleared",
      "ordered_rule_ids": [
        "S1-D-001",
        "S1-D-002",
        "S1-D-003",
        "S1-D-004"
      ],
      "diagnostic_order": [
        "priority ascending",
        "rule_id Unicode code-point order",
        "field name Unicode code-point order"
      ],
      "failure_result": "PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics)",
      "primary_stop": "typed_stop of first ordered matched rule",
      "later_groups_execute_after_failure": false,
      "normalization_permitted_after_failure": false
    }
  ],
  "stage_1_parse_and_shape_rules": [
    {
      "rule_id": "S1-A-001",
      "group": "A",
      "priority": 10,
      "prerequisites": [
        "raw_document_bytes supplied"
      ],
      "predicate": "STRICT_UTF8_DECODE(raw_document_bytes) FAILS",
      "typed_stop": "STOP_CLOSURE_UTF8_INVALID",
      "diagnostic_code": "CLOSURE_UTF8_DECODE_ERROR",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "decoder_error_byte_offset",
        "decoder_error_reason"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-A-002",
      "group": "A",
      "priority": 20,
      "prerequisites": [
        "S1-A-001 did not match"
      ],
      "predicate": "DECODED_TEXT IS_NOT_EXACTLY_ONE_COMPLETE_JSON_VALUE",
      "typed_stop": "STOP_CLOSURE_JSON_PARSE_INVALID",
      "diagnostic_code": "CLOSURE_JSON_SYNTAX_OR_CARDINALITY_ERROR",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "parser_error_byte_offset",
        "parser_error_code",
        "trailing_non_whitespace_span_if_any"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-A-003",
      "group": "A",
      "priority": 30,
      "prerequisites": [
        "S1-A-001 and S1-A-002 did not match",
        "parser retained ordered object-member pairs and source spans before map construction"
      ],
      "predicate": "ANY_OBJECT_CONTAINS_DUPLICATE_DECODED_KEY",
      "typed_stop": "STOP_CLOSURE_DUPLICATE_JSON_KEY",
      "diagnostic_code": "CLOSURE_DUPLICATE_JSON_KEY",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "json_pointer_to_object",
        "decoded_key",
        "occurrence_ordinals",
        "source_byte_spans"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-A-004",
      "group": "A",
      "priority": 40,
      "prerequisites": [
        "S1-A-001 through S1-A-003 did not match"
      ],
      "predicate": "PARSED_ROOT_JSON_PRIMITIVE_TYPE != OBJECT",
      "typed_stop": "STOP_CLOSURE_TOP_LEVEL_OBJECT_REQUIRED",
      "diagnostic_code": "CLOSURE_TOP_LEVEL_TYPE_INVALID",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "observed_root_json_primitive_type"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-B-001",
      "group": "B",
      "priority": 50,
      "prerequisites": [
        "Group A cleared",
        "top-level object member names available"
      ],
      "predicate": "MISSING_REQUIRED_FIELDS != []",
      "typed_stop": "STOP_CLOSURE_REQUIRED_FIELD_MISSING",
      "diagnostic_code": "CLOSURE_REQUIRED_FIELD_MISSING",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "ordered_missing_field_names"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-B-002",
      "group": "B",
      "priority": 60,
      "prerequisites": [
        "Group A cleared",
        "top-level object member names available"
      ],
      "predicate": "UNEXPECTED_FIELDS != []",
      "typed_stop": "STOP_CLOSURE_UNEXPECTED_FIELD",
      "diagnostic_code": "CLOSURE_UNEXPECTED_FIELD",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "ordered_unexpected_field_names"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-B-003",
      "group": "B",
      "priority": 70,
      "prerequisites": [
        "Group A cleared",
        "duplicate keys already rejected",
        "top-level object member count available"
      ],
      "predicate": "TOP_LEVEL_MEMBER_COUNT != 15",
      "typed_stop": "STOP_CLOSURE_FIELD_CARDINALITY_INVALID",
      "diagnostic_code": "CLOSURE_FIELD_CARDINALITY_INVALID",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "expected_member_count",
        "observed_member_count"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-C-001",
      "group": "C",
      "priority": 80,
      "prerequisites": [
        "Groups A and B cleared",
        "all fifteen required fields present exactly once"
      ],
      "predicate": "ANY_NON_NULLABLE_FIELD_VALUE JSON_PRIMITIVE_TYPE == NULL",
      "typed_stop": "STOP_CLOSURE_NULL_REPRESENTATION_INVALID",
      "diagnostic_code": "CLOSURE_NON_NULLABLE_FIELD_IS_NULL",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "ordered_json_pointers"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-C-002",
      "group": "C",
      "priority": 90,
      "prerequisites": [
        "Groups A and B cleared",
        "all enum fields present exactly once"
      ],
      "predicate": "ANY_ENUM_FIELD JSON_PRIMITIVE_TYPE != STRING",
      "typed_stop": "STOP_CLOSURE_ENUM_JSON_TYPE_INVALID",
      "diagnostic_code": "CLOSURE_ENUM_FIELD_NOT_STRING",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "ordered_field_type_diagnostics"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-C-003",
      "group": "C",
      "priority": 100,
      "prerequisites": [
        "Groups A and B cleared",
        "process_exit_code present exactly once"
      ],
      "predicate": "process_exit_code JSON_PRIMITIVE_TYPE NOT_IN [NULL,NUMBER]",
      "typed_stop": "STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID",
      "diagnostic_code": "CLOSURE_EXIT_CODE_NOT_NULL_OR_NUMBER",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "observed_json_primitive_type",
        "source_byte_span"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-D-001",
      "group": "D",
      "priority": 110,
      "prerequisites": [
        "Groups A, B, and C cleared",
        "for each inspected enum field: JSON primitive type is STRING"
      ],
      "predicate": "ANY_ENUM_STRING DOES_NOT_MATCH ^[A-Z][A-Z0-9_]*$",
      "typed_stop": "STOP_CLOSURE_ENUM_TOKEN_LEXICAL_INVALID",
      "diagnostic_code": "CLOSURE_ENUM_TOKEN_LEXICAL_INVALID",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "ordered_field_token_diagnostics"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-D-002",
      "group": "D",
      "priority": 120,
      "prerequisites": [
        "Groups A, B, and C cleared",
        "for each inspected enum field: JSON primitive type is STRING",
        "S1-D-001 did not match for that field"
      ],
      "predicate": "ANY_LEXICALLY_VALID_ENUM_STRING NOT_IN DECLARED_FIELD_ENUM",
      "typed_stop": "STOP_CLOSURE_ENUM_TOKEN_UNREGISTERED",
      "diagnostic_code": "CLOSURE_ENUM_TOKEN_UNREGISTERED",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "field_name",
        "observed_token",
        "allowed_tokens"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-D-003",
      "group": "D",
      "priority": 130,
      "prerequisites": [
        "Groups A, B, and C cleared",
        "process_exit_code JSON primitive type is NUMBER"
      ],
      "predicate": "ORIGINAL_PROCESS_EXIT_CODE_NUMBER_TOKEN DOES_NOT_MATCH ^-?(0|[1-9][0-9]*)$",
      "typed_stop": "STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID",
      "diagnostic_code": "CLOSURE_EXIT_CODE_INTEGER_NUMBER_LEXICAL_INVALID",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "original_number_token",
        "source_byte_span"
      ],
      "later_groups_execute_after_failure": false
    },
    {
      "rule_id": "S1-D-004",
      "group": "D",
      "priority": 140,
      "prerequisites": [
        "Groups A, B, and C cleared",
        "process_exit_code JSON primitive type is NUMBER",
        "S1-D-003 did not match",
        "token parsed as an unbounded mathematical integer"
      ],
      "predicate": "MATHEMATICAL_INTEGER_VALUE NOT_IN [-2147483648,2147483647]",
      "typed_stop": "STOP_CLOSURE_EXIT_CODE_RANGE_INVALID",
      "diagnostic_code": "CLOSURE_EXIT_CODE_OUT_OF_SIGNED_INT32_RANGE",
      "evidence_retained": [
        "raw_byte_length",
        "raw_sha256",
        "original_number_token",
        "unbounded_mathematical_integer_value"
      ],
      "later_groups_execute_after_failure": false
    }
  ],
  "stage_1_dependency_rules": [
    {
      "dependency_id": "S1-DEP-001",
      "requirement": "Group B MUST NOT execute unless every Group-A rule cleared.",
      "enforcement": "A Group-A match returns PARSE_AND_SHAPE_REJECTED immediately."
    },
    {
      "dependency_id": "S1-DEP-002",
      "requirement": "Groups C and D MUST NOT execute when Group B has one or more matches.",
      "enforcement": "Group-B matched rules are sorted; one primary stop and all diagnostics are returned."
    },
    {
      "dependency_id": "S1-DEP-003",
      "requirement": "Group D MUST NOT execute when Group C has one or more matches.",
      "enforcement": "Group-C matched rules are sorted; one primary stop and all diagnostics are returned."
    },
    {
      "dependency_id": "S1-DEP-004",
      "requirement": "S1-D-001 and S1-D-002 inspect only present enum fields whose JSON primitive type is STRING.",
      "enforcement": "Group-B and Group-C clearance are explicit prerequisites."
    },
    {
      "dependency_id": "S1-DEP-005",
      "requirement": "S1-D-002 evaluates a field only after S1-D-001 cleared for that field.",
      "enforcement": "Lexically invalid enum tokens cannot also yield membership diagnostics."
    },
    {
      "dependency_id": "S1-DEP-006",
      "requirement": "S1-D-003 inspects process_exit_code only when its JSON primitive type is NUMBER.",
      "enforcement": "NULL bypasses D-003 and D-004; BOOLEAN, STRING, ARRAY, and OBJECT are rejected in Group C."
    },
    {
      "dependency_id": "S1-DEP-007",
      "requirement": "S1-D-004 evaluates only after S1-D-003 accepts the exact original number token.",
      "enforcement": "Fractions and exponents cannot reach range validation; native numeric overflow cannot control classification."
    },
    {
      "dependency_id": "S1-DEP-008",
      "requirement": "No later group or dependent rule may synthesize a value for a missing, null-forbidden, or wrong-type field.",
      "enforcement": "No normalization occurs after any Stage-1 rejection."
    }
  ],
  "normalized_input_schema": {
    "schema_id": "execution_closure_normalized_inputs.v3",
    "exact_allowed_field_count": 15,
    "exact_allowed_fields_in_order": [
      "execution_attempt_state",
      "process_launch_state",
      "process_exit_state",
      "process_exit_code",
      "output_creation_state",
      "output_commit_state",
      "raw_artifact_presence",
      "raw_artifact_identity_state",
      "raw_artifact_schema_state",
      "raw_result_state",
      "raw_branch_consistency_state",
      "rollback_state",
      "authorization_valid_at_start",
      "authorization_valid_at_completion",
      "authorization_consumption_state"
    ],
    "additional_fields": false,
    "fields": {
      "execution_attempt_state": {
        "type": "ClosedEnum<ExecutionAttemptStateV1>",
        "enum_values": [
          "NOT_ATTEMPTED",
          "EXACTLY_ONE",
          "MULTIPLE",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after the outer execution controller reconciles all attempt-ledger entries for the authorization",
        "observing_authority": "OUTER_EXECUTION_CONTROLLER",
        "provenance": "DETERMINISTIC_DERIVATION_FROM_OUTER_ATTEMPT_LEDGER",
        "copied_or_measured": "DERIVED_BY_OUTER_CONTROLLER",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "process_launch_state": {
        "type": "ClosedEnum<ProcessLaunchStateV1>",
        "enum_values": [
          "NOT_ATTEMPTED",
          "LAUNCH_FAILED",
          "LAUNCHED",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after the outer execution interface declines launch, reports launch failure, confirms launch, or cannot expose the launch disposition",
        "observing_authority": "OUTER_EXECUTION_OBSERVER",
        "provenance": "MEASURED_OUTER_EXECUTION_FACT",
        "copied_or_measured": "MEASURED",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "process_exit_state": {
        "type": "ClosedEnum<ProcessExitStateV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "EXIT_OBSERVED",
          "EXIT_NOT_OBSERVED",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after process-launch disposition is known or is itself unavailable",
        "observing_authority": "OUTER_EXECUTION_OBSERVER",
        "provenance": "MEASURED_OUTER_EXECUTION_FACT",
        "copied_or_measured": "MEASURED",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "process_exit_code": {
        "type": "Nullable<MathematicalSignedInt32>",
        "source_json_primitive_types": [
          "NULL",
          "NUMBER"
        ],
        "nullable": true,
        "observable_when": "only when process_exit_state is EXIT_OBSERVED and the outer execution interface exposes an exit code",
        "observing_authority": "OUTER_EXECUTION_OBSERVER",
        "provenance": "MEASURED_OUTER_EXECUTION_FACT_PARSED_FROM_EXACT_JSON_NUMBER_TOKEN",
        "copied_or_measured": "MEASURED_AND_DETERMINISTICALLY_PARSED",
        "null_mandatory_when": "process_exit_state != EXIT_OBSERVED",
        "null_forbidden_when": "process_exit_state == EXIT_OBSERVED",
        "accepted_number_token_grammar": "^-?(0|[1-9][0-9]*)$",
        "mathematical_integer_range_inclusive": [
          -2147483648,
          2147483647
        ],
        "negative_zero_normalization": {
          "normalized_value": 0,
          "original_token_retained_as_stage_1_parsing_evidence": true
        },
        "native_number_behavior_authoritative": false
      },
      "output_creation_state": {
        "type": "ClosedEnum<OutputCreationStateV1>",
        "enum_values": [
          "NOT_CREATED",
          "PARTIAL_CREATED",
          "COMPLETE_CREATED",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after the execution attempt and any cleanup attempt finish or become unavailable",
        "observing_authority": "OUTER_OUTPUT_OBSERVER",
        "provenance": "MEASURED_OUTER_FILESYSTEM_FACT",
        "copied_or_measured": "MEASURED",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "output_commit_state": {
        "type": "ClosedEnum<OutputCommitStateV1>",
        "enum_values": [
          "NOT_ATTEMPTED",
          "COMMIT_FAILED",
          "COMMITTED",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after exclusive output creation and commit logic finishes or becomes unavailable",
        "observing_authority": "OUTER_OUTPUT_OBSERVER",
        "provenance": "MEASURED_OUTER_FILESYSTEM_FACT",
        "copied_or_measured": "MEASURED",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "raw_artifact_presence": {
        "type": "ClosedEnum<RawArtifactPresenceV1>",
        "enum_values": [
          "ABSENT",
          "PRESENT",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "at the closure snapshot of the exact raw-output path",
        "observing_authority": "OUTER_OUTPUT_OBSERVER",
        "provenance": "MEASURED_OUTER_FILESYSTEM_FACT",
        "copied_or_measured": "MEASURED",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "raw_artifact_identity_state": {
        "type": "ClosedEnum<RawArtifactIdentityStateV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "MATCH",
          "MISMATCH",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after raw presence is established and exact raw bytes can or cannot be hashed",
        "observing_authority": "OUTER_RAW_IDENTITY_VALIDATOR",
        "provenance": "DETERMINISTIC_DERIVATION_FROM_RAW_BYTES_AND_EXPECTED_IDENTITY",
        "copied_or_measured": "DERIVED_BY_OUTER_VALIDATOR",
        "null_mandatory_when": "NEVER; use NOT_APPLICABLE or UNAVAILABLE",
        "null_forbidden_when": "ALWAYS"
      },
      "raw_artifact_schema_state": {
        "type": "ClosedEnum<RawArtifactSchemaStateV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "VALID",
          "INVALID",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after raw presence and readable bytes are established",
        "observing_authority": "OUTER_RAW_SCHEMA_VALIDATOR",
        "provenance": "DETERMINISTIC_SCHEMA_VALIDATION",
        "copied_or_measured": "DERIVED_BY_OUTER_VALIDATOR",
        "null_mandatory_when": "NEVER; use NOT_APPLICABLE or UNAVAILABLE",
        "null_forbidden_when": "ALWAYS"
      },
      "raw_result_state": {
        "type": "ClosedEnum<RawResultStateV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "COMPLETE",
          "BLOCKING",
          "INDETERMINATE",
          "INVALID_LITERAL",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after the raw artifact is parsed or parsing is impossible",
        "observing_authority": "OUTER_RAW_SCHEMA_VALIDATOR",
        "provenance": "COPIED_FROM_RAW_ARTIFACT_OR_DETERMINISTIC_INVALID_LITERAL_CLASSIFICATION",
        "copied_or_measured": "COPIED_OR_DERIVED_BY_OUTER_VALIDATOR",
        "null_mandatory_when": "NEVER; use NOT_APPLICABLE or UNAVAILABLE",
        "null_forbidden_when": "ALWAYS"
      },
      "raw_branch_consistency_state": {
        "type": "ClosedEnum<RawBranchConsistencyStateV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "CONSISTENT",
          "CONTRADICTORY",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after schema-valid raw fields can be compared with the accepted sealed-script branch crosswalk",
        "observing_authority": "STATIC_RAW_BRANCH_VALIDATOR",
        "provenance": "DETERMINISTIC_DERIVATION_FROM_RAW_FIELDS_AND_SEALED_SCRIPT_CONTRACT",
        "copied_or_measured": "DERIVED_BY_STATIC_VALIDATOR",
        "null_mandatory_when": "NEVER; use NOT_APPLICABLE or UNAVAILABLE",
        "null_forbidden_when": "ALWAYS"
      },
      "rollback_state": {
        "type": "ClosedEnum<RollbackStateV1>",
        "enum_values": [
          "NOT_REQUIRED",
          "NOT_ATTEMPTED",
          "PARTIAL_OUTPUT_REMOVED",
          "ROLLBACK_FAILED_RESIDUE_PRESENT",
          "ROLLBACK_RESULT_UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after cleanup is not required, not attempted, completed, failed with residue, or becomes unavailable",
        "observing_authority": "OUTER_OUTPUT_OBSERVER",
        "provenance": "MEASURED_OUTER_FILESYSTEM_AND_CLEANUP_FACT",
        "copied_or_measured": "MEASURED",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "authorization_valid_at_start": {
        "type": "ClosedEnum<AuthorizationValidityAtStartV1>",
        "enum_values": [
          "VALID",
          "INVALID",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "immediately before the outer execution-attempt decision",
        "observing_authority": "OUTER_AUTHORIZATION_CONTROLLER",
        "provenance": "COPIED_AUTHORITY_LEDGER_FACT",
        "copied_or_measured": "COPIED_FROM_AUTHORITY_LEDGER",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "authorization_valid_at_completion": {
        "type": "ClosedEnum<AuthorizationValidityAtCompletionV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "VALID",
          "EXPIRED",
          "INVALID",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "at execution-attempt closure time; NOT_APPLICABLE only when no attempt occurred",
        "observing_authority": "OUTER_AUTHORIZATION_CONTROLLER",
        "provenance": "COPIED_AUTHORITY_LEDGER_FACT",
        "copied_or_measured": "COPIED_FROM_AUTHORITY_LEDGER",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      },
      "authorization_consumption_state": {
        "type": "ClosedEnum<AuthorizationConsumptionStateV1>",
        "enum_values": [
          "NOT_APPLICABLE",
          "CONSUMED",
          "CONSUMPTION_FAILED",
          "UNAVAILABLE"
        ],
        "nullable": false,
        "observable_when": "after the outer authorization controller records or fails to record attempt consumption",
        "observing_authority": "OUTER_AUTHORIZATION_CONTROLLER",
        "provenance": "COPIED_AUTHORITY_LEDGER_FACT",
        "copied_or_measured": "COPIED_FROM_AUTHORITY_LEDGER",
        "null_mandatory_when": "NEVER",
        "null_forbidden_when": "ALWAYS"
      }
    },
    "duplicate_key_equality": "EXACT_DECODED_UNICODE_SCALAR_SEQUENCE_WITHOUT_NORMALIZATION",
    "normalization_serialization_order": [
      "execution_attempt_state",
      "process_launch_state",
      "process_exit_state",
      "process_exit_code",
      "output_creation_state",
      "output_commit_state",
      "raw_artifact_presence",
      "raw_artifact_identity_state",
      "raw_artifact_schema_state",
      "raw_result_state",
      "raw_branch_consistency_state",
      "rollback_state",
      "authorization_valid_at_start",
      "authorization_valid_at_completion",
      "authorization_consumption_state"
    ],
    "stage_1_output_contract": {
      "valid": "PARSE_AND_SHAPE_VALID(normalized_candidate_object,ordered_parsing_evidence)",
      "rejected": "PARSE_AND_SHAPE_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics,retained_parsing_evidence)",
      "rejected_document_enters_stage_2": false
    },
    "stage_1_rule_evaluation": {
      "groups_in_order": [
        "A",
        "B",
        "C",
        "D"
      ],
      "group_A": "sequential first failure; immediate rejection",
      "groups_B_C_D": "evaluate all eligible rules within current group; sort by priority then code-point rule ID then field/source order; reject before later groups when any match",
      "dependent_value_rules": "evaluate only when declared prerequisites are satisfied",
      "primary_stop": "typed_stop of first ordered matched rule",
      "normalization_after_rejection": false
    },
    "stage_2_validation_algorithm": {
      "matched_rule_ids": "all Stage-2 rules whose predicates are true",
      "sort": [
        "priority_ascending",
        "rule_id_code_point"
      ],
      "primary_stop": "typed_stop of matched_rule_ids[0]",
      "empty_result": "NORMALIZED_INPUT_VALID",
      "nonempty_result": "NORMALIZED_INPUT_REJECTED(primary_stop,matched_rule_ids,complete_ordered_diagnostics)",
      "source_enumeration_order_affects_result": false
    },
    "stage_3_precondition": "NORMALIZED_INPUT_VALID",
    "rule_counts": {
      "stage_1_groups": 4,
      "stage_1_parse_and_shape_rules": 14,
      "stage_1_dependency_rules": 8,
      "stage_2_validation_rules": 49,
      "closure_states": 31,
      "stage_3_reducer_rules": 33,
      "stage_4_conformance_rules": 2,
      "example_vectors": 137
    },
    "json_primitive_type_inventory": [
      "NULL",
      "BOOLEAN",
      "NUMBER",
      "STRING",
      "ARRAY",
      "OBJECT"
    ],
    "rollback_not_attempted_valid_domain": {
      "required": {
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": [
          "NOT_ATTEMPTED",
          "COMMIT_FAILED"
        ],
        "rollback_state": "NOT_ATTEMPTED"
      },
      "permitted_raw_artifact_presence": [
        "PRESENT",
        "ABSENT",
        "UNAVAILABLE"
      ],
      "presence_dependent_raw_fields": "must satisfy all Stage-2 raw presence, identity, schema, result, and branch-consistency rules",
      "commit_non_implication": "raw_result_state does not imply output_commit_state; only explicit output_commit_state == COMMITTED denotes a successful commit"
    }
  },
  "stage_2_validation_rules": [
    {
      "rule_id": "S2-001",
      "priority": 100,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND process_launch_state != NOT_ATTEMPTED",
      "typed_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID",
      "diagnostic_code": "ATTEMPT_NOT_ATTEMPTED_BUT_LAUNCH_NOT_NOT_ATTEMPTED",
      "evidence_retained": [
        "execution_attempt_ledger",
        "process_launch_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "process_launch_state"
      ]
    },
    {
      "rule_id": "S2-002",
      "priority": 110,
      "predicate": "execution_attempt_state != NOT_ATTEMPTED AND process_launch_state == NOT_ATTEMPTED",
      "typed_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID",
      "diagnostic_code": "ATTEMPT_PRESENT_BUT_LAUNCH_NOT_ATTEMPTED",
      "evidence_retained": [
        "execution_attempt_ledger",
        "process_launch_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "process_launch_state"
      ]
    },
    {
      "rule_id": "S2-003",
      "priority": 120,
      "predicate": "process_launch_state IN [NOT_ATTEMPTED,LAUNCH_FAILED] AND process_exit_state != NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS",
      "diagnostic_code": "EXIT_STATE_REPORTED_WITHOUT_LAUNCHED_PROCESS",
      "evidence_retained": [
        "process_launch_observation",
        "process_exit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "process_launch_state",
        "process_exit_state"
      ]
    },
    {
      "rule_id": "S2-004",
      "priority": 130,
      "predicate": "process_launch_state == UNAVAILABLE AND process_exit_state != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_LAUNCH_RESULT_EXIT_RELATION_INVALID",
      "diagnostic_code": "LAUNCH_UNAVAILABLE_REQUIRES_EXIT_UNAVAILABLE",
      "evidence_retained": [
        "process_launch_observation",
        "process_exit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "process_launch_state",
        "process_exit_state"
      ]
    },
    {
      "rule_id": "S2-005",
      "priority": 140,
      "predicate": "process_launch_state == LAUNCHED AND process_exit_state == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE",
      "diagnostic_code": "LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE",
      "evidence_retained": [
        "process_launch_observation",
        "process_exit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "process_launch_state",
        "process_exit_state"
      ]
    },
    {
      "rule_id": "S2-006",
      "priority": 150,
      "predicate": "(process_exit_state == EXIT_OBSERVED AND process_exit_code IS_NULL) OR (process_exit_state != EXIT_OBSERVED AND process_exit_code IS_NOT_NULL)",
      "typed_stop": "STOP_CLOSURE_EXIT_CODE_NULLABILITY_INVALID",
      "diagnostic_code": "EXIT_CODE_NULLABILITY_RELATION_INVALID",
      "evidence_retained": [
        "process_exit_observation",
        "process_exit_code_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "process_exit_state",
        "process_exit_code"
      ]
    },
    {
      "rule_id": "S2-007",
      "priority": 200,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND output_creation_state != NOT_CREATED",
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID",
      "diagnostic_code": "NO_ATTEMPT_WITH_OUTPUT_CREATION",
      "evidence_retained": [
        "execution_attempt_ledger",
        "output_creation_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-008",
      "priority": 210,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND output_commit_state != NOT_ATTEMPTED",
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_COMMIT_INVALID",
      "diagnostic_code": "NO_ATTEMPT_WITH_OUTPUT_COMMIT_ACTIVITY",
      "evidence_retained": [
        "execution_attempt_ledger",
        "output_commit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "output_commit_state"
      ]
    },
    {
      "rule_id": "S2-009",
      "priority": 220,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND raw_artifact_presence != ABSENT",
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_RAW_ARTIFACT_INVALID",
      "diagnostic_code": "NO_ATTEMPT_WITH_NONABSENT_RAW_ARTIFACT",
      "evidence_retained": [
        "execution_attempt_ledger",
        "raw_presence_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "raw_artifact_presence"
      ]
    },
    {
      "rule_id": "S2-010",
      "priority": 230,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND rollback_state != NOT_REQUIRED",
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_ROLLBACK_INVALID",
      "diagnostic_code": "NO_ATTEMPT_WITH_ROLLBACK_ACTIVITY",
      "evidence_retained": [
        "execution_attempt_ledger",
        "rollback_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "rollback_state"
      ]
    },
    {
      "rule_id": "S2-011",
      "priority": 300,
      "predicate": "output_commit_state == COMMITTED AND output_creation_state != COMPLETE_CREATED",
      "typed_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID",
      "diagnostic_code": "COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
      "evidence_retained": [
        "output_creation_observation",
        "output_commit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "output_commit_state",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-012",
      "priority": 310,
      "predicate": "output_commit_state == COMMITTED AND raw_artifact_presence != PRESENT",
      "typed_stop": "STOP_CLOSURE_COMMITTED_RAW_ARTIFACT_STATE_INVALID",
      "diagnostic_code": "COMMITTED_OUTPUT_REQUIRES_PRESENT_RAW_ARTIFACT",
      "evidence_retained": [
        "output_commit_observation",
        "raw_presence_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "output_commit_state",
        "raw_artifact_presence"
      ]
    },
    {
      "rule_id": "S2-013",
      "priority": 320,
      "predicate": "output_creation_state == PARTIAL_CREATED AND output_commit_state == COMMITTED",
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_COMMITTED",
      "diagnostic_code": "PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
      "evidence_retained": [
        "output_creation_observation",
        "output_commit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "output_creation_state",
        "output_commit_state"
      ]
    },
    {
      "rule_id": "S2-014",
      "priority": 330,
      "predicate": "raw_artifact_presence == PRESENT AND output_creation_state == NOT_CREATED",
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION",
      "diagnostic_code": "RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION",
      "evidence_retained": [
        "raw_presence_observation",
        "output_creation_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-015",
      "priority": 400,
      "predicate": "rollback_state == PARTIAL_OUTPUT_REMOVED AND output_creation_state != PARTIAL_CREATED",
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID",
      "diagnostic_code": "PARTIAL_REMOVAL_REQUIRES_PARTIAL_CREATION",
      "evidence_retained": [
        "rollback_observation",
        "output_creation_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-016",
      "priority": 410,
      "predicate": "rollback_state == PARTIAL_OUTPUT_REMOVED AND output_commit_state NOT_IN [NOT_ATTEMPTED,COMMIT_FAILED]",
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID",
      "diagnostic_code": "PARTIAL_REMOVAL_REQUIRES_NO_COMMIT",
      "evidence_retained": [
        "rollback_observation",
        "output_commit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_commit_state"
      ]
    },
    {
      "rule_id": "S2-017",
      "priority": 420,
      "predicate": "rollback_state == PARTIAL_OUTPUT_REMOVED AND raw_artifact_presence != ABSENT",
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID",
      "diagnostic_code": "PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE",
      "evidence_retained": [
        "rollback_observation",
        "raw_presence_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "raw_artifact_presence"
      ]
    },
    {
      "rule_id": "S2-018",
      "priority": 430,
      "predicate": "rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT AND output_creation_state != PARTIAL_CREATED",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_RESIDUE_REQUIRES_PARTIAL_CREATION",
      "evidence_retained": [
        "rollback_observation",
        "output_creation_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-019",
      "priority": 440,
      "predicate": "rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT AND output_commit_state NOT_IN [NOT_ATTEMPTED,COMMIT_FAILED]",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_RESIDUE_REQUIRES_NO_COMMIT",
      "evidence_retained": [
        "rollback_observation",
        "output_commit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_commit_state"
      ]
    },
    {
      "rule_id": "S2-020",
      "priority": 450,
      "predicate": "rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT AND raw_artifact_presence != PRESENT",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_RESIDUE_REQUIRES_FINAL_PRESENCE",
      "evidence_retained": [
        "rollback_observation",
        "raw_presence_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "raw_artifact_presence"
      ]
    },
    {
      "rule_id": "S2-021",
      "priority": 460,
      "predicate": "rollback_state == ROLLBACK_RESULT_UNAVAILABLE AND output_creation_state != PARTIAL_CREATED",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_UNAVAILABLE_REQUIRES_PARTIAL_CREATION",
      "evidence_retained": [
        "rollback_observation",
        "output_creation_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-022",
      "priority": 470,
      "predicate": "rollback_state == ROLLBACK_RESULT_UNAVAILABLE AND raw_artifact_presence != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_UNAVAILABLE_REQUIRES_FINAL_PRESENCE_UNAVAILABLE",
      "evidence_retained": [
        "rollback_observation",
        "raw_presence_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "raw_artifact_presence"
      ]
    },
    {
      "rule_id": "S2-023",
      "priority": 480,
      "predicate": "output_creation_state == PARTIAL_CREATED AND rollback_state == NOT_REQUIRED",
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_ROLLBACK_NOT_REQUIRED",
      "diagnostic_code": "PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED",
      "evidence_retained": [
        "output_creation_observation",
        "rollback_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "output_creation_state",
        "rollback_state"
      ]
    },
    {
      "rule_id": "S2-024",
      "priority": 490,
      "predicate": "rollback_state == NOT_ATTEMPTED AND output_creation_state != PARTIAL_CREATED",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_NOT_ATTEMPTED_REQUIRES_PARTIAL_OUTPUT",
      "evidence_retained": [
        "rollback_observation",
        "output_creation_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_creation_state"
      ]
    },
    {
      "rule_id": "S2-049",
      "priority": 495,
      "predicate": "rollback_state == NOT_ATTEMPTED AND output_commit_state NOT_IN [NOT_ATTEMPTED,COMMIT_FAILED]",
      "typed_stop": "STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_COMMIT_STATE_INVALID",
      "diagnostic_code": "ROLLBACK_NOT_ATTEMPTED_REQUIRES_NO_SUCCESSFUL_OR_UNAVAILABLE_COMMIT",
      "evidence_retained": [
        "output_creation_observation",
        "output_commit_observation",
        "rollback_observation",
        "final_raw_presence_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "rollback_state",
        "output_commit_state"
      ]
    },
    {
      "rule_id": "S2-025",
      "priority": 500,
      "predicate": "raw_artifact_presence == ABSENT AND raw_artifact_identity_state != NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT",
      "diagnostic_code": "RAW_ABSENCE_REQUIRES_IDENTITY_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_artifact_identity_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_identity_state"
      ]
    },
    {
      "rule_id": "S2-026",
      "priority": 510,
      "predicate": "raw_artifact_presence == ABSENT AND raw_artifact_schema_state != NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_SCHEMA_WITHOUT_ARTIFACT",
      "diagnostic_code": "RAW_ABSENCE_REQUIRES_SCHEMA_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_artifact_schema_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_schema_state"
      ]
    },
    {
      "rule_id": "S2-027",
      "priority": 520,
      "predicate": "raw_artifact_presence == ABSENT AND raw_result_state != NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_RESULT_WITHOUT_ARTIFACT",
      "diagnostic_code": "RAW_ABSENCE_REQUIRES_RESULT_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_result_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_result_state"
      ]
    },
    {
      "rule_id": "S2-028",
      "priority": 530,
      "predicate": "raw_artifact_presence == ABSENT AND raw_branch_consistency_state != NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_BRANCH_WITHOUT_ARTIFACT",
      "diagnostic_code": "RAW_ABSENCE_REQUIRES_BRANCH_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_branch_consistency_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_branch_consistency_state"
      ]
    },
    {
      "rule_id": "S2-029",
      "priority": 540,
      "predicate": "raw_artifact_presence == UNAVAILABLE AND raw_artifact_identity_state != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
      "diagnostic_code": "RAW_UNAVAILABLE_REQUIRES_IDENTITY_UNAVAILABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_artifact_identity_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_identity_state"
      ]
    },
    {
      "rule_id": "S2-030",
      "priority": 550,
      "predicate": "raw_artifact_presence == UNAVAILABLE AND raw_artifact_schema_state != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
      "diagnostic_code": "RAW_UNAVAILABLE_REQUIRES_SCHEMA_UNAVAILABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_artifact_schema_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_schema_state"
      ]
    },
    {
      "rule_id": "S2-031",
      "priority": 560,
      "predicate": "raw_artifact_presence == UNAVAILABLE AND raw_result_state != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
      "diagnostic_code": "RAW_UNAVAILABLE_REQUIRES_RESULT_UNAVAILABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_result_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_result_state"
      ]
    },
    {
      "rule_id": "S2-032",
      "priority": 570,
      "predicate": "raw_artifact_presence == UNAVAILABLE AND raw_branch_consistency_state != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
      "diagnostic_code": "RAW_UNAVAILABLE_REQUIRES_BRANCH_UNAVAILABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_branch_consistency_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_branch_consistency_state"
      ]
    },
    {
      "rule_id": "S2-033",
      "priority": 580,
      "predicate": "raw_artifact_presence == PRESENT AND raw_artifact_identity_state == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
      "diagnostic_code": "RAW_PRESENT_FORBIDS_IDENTITY_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_artifact_identity_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_identity_state"
      ]
    },
    {
      "rule_id": "S2-034",
      "priority": 590,
      "predicate": "raw_artifact_presence == PRESENT AND raw_artifact_schema_state == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
      "diagnostic_code": "RAW_PRESENT_FORBIDS_SCHEMA_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_artifact_schema_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_schema_state"
      ]
    },
    {
      "rule_id": "S2-035",
      "priority": 600,
      "predicate": "raw_artifact_presence == PRESENT AND raw_result_state == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
      "diagnostic_code": "RAW_PRESENT_FORBIDS_RESULT_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_result_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_result_state"
      ]
    },
    {
      "rule_id": "S2-036",
      "priority": 610,
      "predicate": "raw_artifact_presence == PRESENT AND raw_branch_consistency_state == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
      "diagnostic_code": "RAW_PRESENT_FORBIDS_BRANCH_NOT_APPLICABLE",
      "evidence_retained": [
        "raw_presence_observation",
        "raw_branch_consistency_state_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_branch_consistency_state"
      ]
    },
    {
      "rule_id": "S2-037",
      "priority": 620,
      "predicate": "raw_artifact_schema_state == INVALID AND raw_result_state IN [COMPLETE,BLOCKING,INDETERMINATE]",
      "typed_stop": "STOP_CLOSURE_RAW_RESULT_WITH_INVALID_SCHEMA",
      "diagnostic_code": "INVALID_SCHEMA_WITH_VALID_RESULT_LITERAL",
      "evidence_retained": [
        "raw_schema_diagnostics",
        "raw_result_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_schema_state",
        "raw_result_state"
      ]
    },
    {
      "rule_id": "S2-038",
      "priority": 630,
      "predicate": "raw_result_state == INVALID_LITERAL AND raw_artifact_schema_state != INVALID",
      "typed_stop": "STOP_CLOSURE_INVALID_LITERAL_SCHEMA_RELATION_INVALID",
      "diagnostic_code": "INVALID_LITERAL_REQUIRES_INVALID_SCHEMA",
      "evidence_retained": [
        "raw_schema_diagnostics",
        "raw_result_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_result_state",
        "raw_artifact_schema_state"
      ]
    },
    {
      "rule_id": "S2-039",
      "priority": 640,
      "predicate": "raw_result_state IN [COMPLETE,BLOCKING,INDETERMINATE] AND raw_artifact_schema_state != VALID",
      "typed_stop": "STOP_CLOSURE_VALID_RESULT_WITHOUT_VALID_SCHEMA",
      "diagnostic_code": "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA",
      "evidence_retained": [
        "raw_schema_diagnostics",
        "raw_result_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_result_state",
        "raw_artifact_schema_state"
      ]
    },
    {
      "rule_id": "S2-040",
      "priority": 650,
      "predicate": "raw_branch_consistency_state IN [CONSISTENT,CONTRADICTORY] AND raw_artifact_schema_state != VALID",
      "typed_stop": "STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID",
      "diagnostic_code": "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA",
      "evidence_retained": [
        "raw_schema_diagnostics",
        "raw_branch_validation_record"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_branch_consistency_state",
        "raw_artifact_schema_state"
      ]
    },
    {
      "rule_id": "S2-041",
      "priority": 660,
      "predicate": "raw_artifact_schema_state == INVALID AND raw_branch_consistency_state != UNAVAILABLE",
      "typed_stop": "STOP_CLOSURE_INVALID_SCHEMA_BRANCH_STATE_INVALID",
      "diagnostic_code": "INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE",
      "evidence_retained": [
        "raw_schema_diagnostics",
        "raw_branch_validation_record"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "raw_artifact_schema_state",
        "raw_branch_consistency_state"
      ]
    },
    {
      "rule_id": "S2-042",
      "priority": 700,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND authorization_valid_at_completion != NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID",
      "diagnostic_code": "NO_ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_NOT_APPLICABLE",
      "evidence_retained": [
        "execution_attempt_ledger",
        "authorization_completion_ledger"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "authorization_valid_at_completion"
      ]
    },
    {
      "rule_id": "S2-043",
      "priority": 710,
      "predicate": "execution_attempt_state != NOT_ATTEMPTED AND authorization_valid_at_completion == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID",
      "diagnostic_code": "ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_APPLICABLE",
      "evidence_retained": [
        "execution_attempt_ledger",
        "authorization_completion_ledger"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "authorization_valid_at_completion"
      ]
    },
    {
      "rule_id": "S2-044",
      "priority": 720,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND authorization_consumption_state == CONSUMED",
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT",
      "diagnostic_code": "AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT",
      "evidence_retained": [
        "execution_attempt_ledger",
        "authorization_consumption_ledger"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "authorization_consumption_state"
      ]
    },
    {
      "rule_id": "S2-045",
      "priority": 730,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED AND authorization_consumption_state IN [CONSUMPTION_FAILED,UNAVAILABLE]",
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID",
      "diagnostic_code": "NO_ATTEMPT_REQUIRES_CONSUMPTION_NOT_APPLICABLE",
      "evidence_retained": [
        "execution_attempt_ledger",
        "authorization_consumption_ledger"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "authorization_consumption_state"
      ]
    },
    {
      "rule_id": "S2-046",
      "priority": 740,
      "predicate": "execution_attempt_state != NOT_ATTEMPTED AND authorization_consumption_state == NOT_APPLICABLE",
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID",
      "diagnostic_code": "ATTEMPT_REQUIRES_CONSUMPTION_APPLICABLE",
      "evidence_retained": [
        "execution_attempt_ledger",
        "authorization_consumption_ledger"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "execution_attempt_state",
        "authorization_consumption_state"
      ]
    },
    {
      "rule_id": "S2-047",
      "priority": 800,
      "predicate": "process_launch_state == LAUNCH_FAILED AND output_commit_state == COMMITTED",
      "typed_stop": "STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW",
      "diagnostic_code": "LAUNCH_FAILED_WITH_COMMITTED_OUTPUT",
      "evidence_retained": [
        "process_launch_observation",
        "output_commit_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "process_launch_state",
        "output_commit_state"
      ]
    },
    {
      "rule_id": "S2-048",
      "priority": 810,
      "predicate": "process_launch_state == LAUNCH_FAILED AND raw_result_state == COMPLETE",
      "typed_stop": "STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW",
      "diagnostic_code": "LAUNCH_FAILED_WITH_RAW_COMPLETE_RESULT",
      "evidence_retained": [
        "process_launch_observation",
        "raw_result_observation"
      ],
      "standard_closure_artifact_may_materialize": false,
      "referenced_fields": [
        "process_launch_state",
        "raw_result_state"
      ]
    }
  ],
  "stage_2_stop_precedence": [
    {
      "ordinal": 1,
      "rule_id": "S2-001",
      "priority": 100,
      "typed_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID"
    },
    {
      "ordinal": 2,
      "rule_id": "S2-002",
      "priority": 110,
      "typed_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID"
    },
    {
      "ordinal": 3,
      "rule_id": "S2-003",
      "priority": 120,
      "typed_stop": "STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS"
    },
    {
      "ordinal": 4,
      "rule_id": "S2-004",
      "priority": 130,
      "typed_stop": "STOP_CLOSURE_LAUNCH_RESULT_EXIT_RELATION_INVALID"
    },
    {
      "ordinal": 5,
      "rule_id": "S2-005",
      "priority": 140,
      "typed_stop": "STOP_CLOSURE_LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE"
    },
    {
      "ordinal": 6,
      "rule_id": "S2-006",
      "priority": 150,
      "typed_stop": "STOP_CLOSURE_EXIT_CODE_NULLABILITY_INVALID"
    },
    {
      "ordinal": 7,
      "rule_id": "S2-007",
      "priority": 200,
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID"
    },
    {
      "ordinal": 8,
      "rule_id": "S2-008",
      "priority": 210,
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_COMMIT_INVALID"
    },
    {
      "ordinal": 9,
      "rule_id": "S2-009",
      "priority": 220,
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_RAW_ARTIFACT_INVALID"
    },
    {
      "ordinal": 10,
      "rule_id": "S2-010",
      "priority": 230,
      "typed_stop": "STOP_CLOSURE_NO_ATTEMPT_ROLLBACK_INVALID"
    },
    {
      "ordinal": 11,
      "rule_id": "S2-011",
      "priority": 300,
      "typed_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID"
    },
    {
      "ordinal": 12,
      "rule_id": "S2-012",
      "priority": 310,
      "typed_stop": "STOP_CLOSURE_COMMITTED_RAW_ARTIFACT_STATE_INVALID"
    },
    {
      "ordinal": 13,
      "rule_id": "S2-013",
      "priority": 320,
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_COMMITTED"
    },
    {
      "ordinal": 14,
      "rule_id": "S2-014",
      "priority": 330,
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION"
    },
    {
      "ordinal": 15,
      "rule_id": "S2-015",
      "priority": 400,
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID"
    },
    {
      "ordinal": 16,
      "rule_id": "S2-016",
      "priority": 410,
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID"
    },
    {
      "ordinal": 17,
      "rule_id": "S2-017",
      "priority": 420,
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID"
    },
    {
      "ordinal": 18,
      "rule_id": "S2-018",
      "priority": 430,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID"
    },
    {
      "ordinal": 19,
      "rule_id": "S2-019",
      "priority": 440,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID"
    },
    {
      "ordinal": 20,
      "rule_id": "S2-020",
      "priority": 450,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID"
    },
    {
      "ordinal": 21,
      "rule_id": "S2-021",
      "priority": 460,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID"
    },
    {
      "ordinal": 22,
      "rule_id": "S2-022",
      "priority": 470,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID"
    },
    {
      "ordinal": 23,
      "rule_id": "S2-023",
      "priority": 480,
      "typed_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_ROLLBACK_NOT_REQUIRED"
    },
    {
      "ordinal": 24,
      "rule_id": "S2-024",
      "priority": 490,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_STATE_INVALID"
    },
    {
      "ordinal": 25,
      "rule_id": "S2-049",
      "priority": 495,
      "typed_stop": "STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_COMMIT_STATE_INVALID"
    },
    {
      "ordinal": 26,
      "rule_id": "S2-025",
      "priority": 500,
      "typed_stop": "STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT"
    },
    {
      "ordinal": 27,
      "rule_id": "S2-026",
      "priority": 510,
      "typed_stop": "STOP_CLOSURE_RAW_SCHEMA_WITHOUT_ARTIFACT"
    },
    {
      "ordinal": 28,
      "rule_id": "S2-027",
      "priority": 520,
      "typed_stop": "STOP_CLOSURE_RAW_RESULT_WITHOUT_ARTIFACT"
    },
    {
      "ordinal": 29,
      "rule_id": "S2-028",
      "priority": 530,
      "typed_stop": "STOP_CLOSURE_RAW_BRANCH_WITHOUT_ARTIFACT"
    },
    {
      "ordinal": 30,
      "rule_id": "S2-029",
      "priority": 540,
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID"
    },
    {
      "ordinal": 31,
      "rule_id": "S2-030",
      "priority": 550,
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID"
    },
    {
      "ordinal": 32,
      "rule_id": "S2-031",
      "priority": 560,
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID"
    },
    {
      "ordinal": 33,
      "rule_id": "S2-032",
      "priority": 570,
      "typed_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID"
    },
    {
      "ordinal": 34,
      "rule_id": "S2-033",
      "priority": 580,
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE"
    },
    {
      "ordinal": 35,
      "rule_id": "S2-034",
      "priority": 590,
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE"
    },
    {
      "ordinal": 36,
      "rule_id": "S2-035",
      "priority": 600,
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE"
    },
    {
      "ordinal": 37,
      "rule_id": "S2-036",
      "priority": 610,
      "typed_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE"
    },
    {
      "ordinal": 38,
      "rule_id": "S2-037",
      "priority": 620,
      "typed_stop": "STOP_CLOSURE_RAW_RESULT_WITH_INVALID_SCHEMA"
    },
    {
      "ordinal": 39,
      "rule_id": "S2-038",
      "priority": 630,
      "typed_stop": "STOP_CLOSURE_INVALID_LITERAL_SCHEMA_RELATION_INVALID"
    },
    {
      "ordinal": 40,
      "rule_id": "S2-039",
      "priority": 640,
      "typed_stop": "STOP_CLOSURE_VALID_RESULT_WITHOUT_VALID_SCHEMA"
    },
    {
      "ordinal": 41,
      "rule_id": "S2-040",
      "priority": 650,
      "typed_stop": "STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID"
    },
    {
      "ordinal": 42,
      "rule_id": "S2-041",
      "priority": 660,
      "typed_stop": "STOP_CLOSURE_INVALID_SCHEMA_BRANCH_STATE_INVALID"
    },
    {
      "ordinal": 43,
      "rule_id": "S2-042",
      "priority": 700,
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID"
    },
    {
      "ordinal": 44,
      "rule_id": "S2-043",
      "priority": 710,
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID"
    },
    {
      "ordinal": 45,
      "rule_id": "S2-044",
      "priority": 720,
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT"
    },
    {
      "ordinal": 46,
      "rule_id": "S2-045",
      "priority": 730,
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID"
    },
    {
      "ordinal": 47,
      "rule_id": "S2-046",
      "priority": 740,
      "typed_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID"
    },
    {
      "ordinal": 48,
      "rule_id": "S2-047",
      "priority": 800,
      "typed_stop": "STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW"
    },
    {
      "ordinal": 49,
      "rule_id": "S2-048",
      "priority": 810,
      "typed_stop": "STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW"
    }
  ],
  "closure_states": [
    {
      "state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
      "description": "A partial output remains after rollback failed; residue is the dominant primary factual classification.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_ROLLBACK_RESULT_UNAVAILABLE",
      "description": "The cleanup result and final residue disposition cannot be established.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
      "description": "A partial output was created, no successful commit occurred, rollback was not attempted, and residue is present at the exact output path.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
      "description": "A partial output was created, no successful commit occurred, rollback was not attempted, and final residue presence is unavailable.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
      "description": "A partial output was created, no successful commit occurred, rollback was not attempted, and the final output path is absent; the state does not attribute absence to authorized cleanup.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_INVALID_AT_START",
      "description": "The outer authority controller established that authority was invalid at the execution-start boundary.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE",
      "description": "The outer authority controller could not establish authority validity at the execution-start boundary.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLE",
      "description": "The outer attempt ledger establishes more than one execution attempt under the single-use boundary.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE",
      "description": "The outer attempt ledger cannot establish whether exactly one attempt occurred.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_EXECUTION_NOT_ATTEMPTED",
      "description": "No execution attempt occurred.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_PROCESS_LAUNCH_FAILED",
      "description": "An execution attempt was recorded but process launch failed.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE",
      "description": "An execution attempt was recorded but launch disposition is unavailable.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_PROCESS_EXIT_UNAVAILABLE",
      "description": "The process was launched but a terminal exit observation is absent or unavailable.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_PROCESS_EXIT_NONZERO",
      "description": "The process exit was observed with a nonzero signed exit code.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_OUTPUT_STATE_UNAVAILABLE",
      "description": "Creation, commit, or final raw-presence state is unavailable outside the exact rollback-unavailable pattern.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH",
      "description": "Present raw bytes do not match the expected raw-artifact identity.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
      "description": "Raw identity, schema, or branch-consistency validation is unavailable.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID",
      "description": "A present raw artifact fails the exact raw-evidence schema.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION",
      "description": "A schema-valid raw artifact contradicts the sealed-script branch crosswalk.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION",
      "description": "Authority was valid at start and expired before execution closure.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION",
      "description": "Authority was valid at start but is invalid, other than simple expiry, at completion.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE",
      "description": "Authority validity at completion is unavailable.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED",
      "description": "The outer controller failed to record the required authorization consumption.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE",
      "description": "The outer controller cannot establish authorization-consumption disposition.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_PARTIAL_OUTPUT_REMOVED",
      "description": "A partial output was not committed and was successfully removed.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_PROCESS_EXITED_NO_OUTPUT",
      "description": "The process exited with code zero, no output was created, and no raw artifact exists.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT",
      "description": "Terminal execution closure exists but no committed complete valid raw artifact exists.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
      "description": "A committed, identity-matching, schema-valid, branch-consistent raw artifact reports BLOCKING.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_VALID_RAW_INDETERMINATE_REPORTED",
      "description": "A committed, identity-matching, schema-valid, branch-consistent raw artifact reports INDETERMINATE.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "description": "A committed, identity-matching, schema-valid, branch-consistent raw artifact reports COMPLETE; this remains factual only.",
      "acceptance_effect": "NONE"
    },
    {
      "state": "CLOSURE_EXECUTION_RESULT_INDETERMINATE",
      "description": "No prior factual rule applies; the closed final rule classifies the remaining valid vector as indeterminate.",
      "acceptance_effect": "NONE"
    }
  ],
  "stage_3_reducer_rules": [
    {
      "rule_id": "S3-001",
      "priority": 1,
      "predicate": "rollback_state == ROLLBACK_FAILED_RESIDUE_PRESENT",
      "closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
      "referenced_fields": [
        "rollback_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-002",
      "priority": 2,
      "predicate": "rollback_state == ROLLBACK_RESULT_UNAVAILABLE",
      "closure_state": "CLOSURE_ROLLBACK_RESULT_UNAVAILABLE",
      "referenced_fields": [
        "rollback_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-003",
      "priority": 3,
      "predicate": "rollback_state == NOT_ATTEMPTED AND output_creation_state == PARTIAL_CREATED AND output_commit_state IN [NOT_ATTEMPTED,COMMIT_FAILED] AND raw_artifact_presence == PRESENT",
      "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
      "referenced_fields": [
        "rollback_state",
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-004",
      "priority": 4,
      "predicate": "rollback_state == NOT_ATTEMPTED AND output_creation_state == PARTIAL_CREATED AND output_commit_state IN [NOT_ATTEMPTED,COMMIT_FAILED] AND raw_artifact_presence == UNAVAILABLE",
      "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
      "referenced_fields": [
        "rollback_state",
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-005",
      "priority": 5,
      "predicate": "rollback_state == NOT_ATTEMPTED AND output_creation_state == PARTIAL_CREATED AND output_commit_state IN [NOT_ATTEMPTED,COMMIT_FAILED] AND raw_artifact_presence == ABSENT",
      "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
      "referenced_fields": [
        "rollback_state",
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-006",
      "priority": 6,
      "predicate": "authorization_valid_at_start == INVALID",
      "closure_state": "CLOSURE_AUTHORIZATION_INVALID_AT_START",
      "referenced_fields": [
        "authorization_valid_at_start"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-007",
      "priority": 7,
      "predicate": "authorization_valid_at_start == UNAVAILABLE",
      "closure_state": "CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE",
      "referenced_fields": [
        "authorization_valid_at_start"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-008",
      "priority": 8,
      "predicate": "execution_attempt_state == MULTIPLE",
      "closure_state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLE",
      "referenced_fields": [
        "execution_attempt_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-009",
      "priority": 9,
      "predicate": "execution_attempt_state == UNAVAILABLE",
      "closure_state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE",
      "referenced_fields": [
        "execution_attempt_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-010",
      "priority": 10,
      "predicate": "execution_attempt_state == NOT_ATTEMPTED",
      "closure_state": "CLOSURE_EXECUTION_NOT_ATTEMPTED",
      "referenced_fields": [
        "execution_attempt_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-011",
      "priority": 11,
      "predicate": "process_launch_state == LAUNCH_FAILED",
      "closure_state": "CLOSURE_PROCESS_LAUNCH_FAILED",
      "referenced_fields": [
        "process_launch_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-012",
      "priority": 12,
      "predicate": "process_launch_state == UNAVAILABLE",
      "closure_state": "CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE",
      "referenced_fields": [
        "process_launch_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-013",
      "priority": 13,
      "predicate": "process_exit_state IN [EXIT_NOT_OBSERVED,UNAVAILABLE]",
      "closure_state": "CLOSURE_PROCESS_EXIT_UNAVAILABLE",
      "referenced_fields": [
        "process_exit_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-014",
      "priority": 14,
      "predicate": "process_exit_state == EXIT_OBSERVED AND process_exit_code != 0",
      "closure_state": "CLOSURE_PROCESS_EXIT_NONZERO",
      "referenced_fields": [
        "process_exit_state",
        "process_exit_code"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-015",
      "priority": 15,
      "predicate": "output_creation_state == UNAVAILABLE OR output_commit_state == UNAVAILABLE OR raw_artifact_presence == UNAVAILABLE",
      "closure_state": "CLOSURE_OUTPUT_STATE_UNAVAILABLE",
      "referenced_fields": [
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-016",
      "priority": 16,
      "predicate": "raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MISMATCH",
      "closure_state": "CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH",
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_identity_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-017",
      "priority": 17,
      "predicate": "raw_artifact_presence == PRESENT AND raw_artifact_identity_state == UNAVAILABLE",
      "closure_state": "CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_identity_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-018",
      "priority": 18,
      "predicate": "raw_artifact_presence == PRESENT AND raw_artifact_schema_state == INVALID",
      "closure_state": "CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID",
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_schema_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-019",
      "priority": 19,
      "predicate": "raw_artifact_presence == PRESENT AND raw_artifact_schema_state == UNAVAILABLE",
      "closure_state": "CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_artifact_schema_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-020",
      "priority": 20,
      "predicate": "raw_artifact_presence == PRESENT AND raw_branch_consistency_state == CONTRADICTORY",
      "closure_state": "CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION",
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_branch_consistency_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-021",
      "priority": 21,
      "predicate": "raw_artifact_presence == PRESENT AND raw_branch_consistency_state == UNAVAILABLE",
      "closure_state": "CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
      "referenced_fields": [
        "raw_artifact_presence",
        "raw_branch_consistency_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-022",
      "priority": 22,
      "predicate": "authorization_valid_at_completion == EXPIRED",
      "closure_state": "CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION",
      "referenced_fields": [
        "authorization_valid_at_completion"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-023",
      "priority": 23,
      "predicate": "authorization_valid_at_completion == INVALID",
      "closure_state": "CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION",
      "referenced_fields": [
        "authorization_valid_at_completion"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-024",
      "priority": 24,
      "predicate": "authorization_valid_at_completion == UNAVAILABLE",
      "closure_state": "CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE",
      "referenced_fields": [
        "authorization_valid_at_completion"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-025",
      "priority": 25,
      "predicate": "authorization_consumption_state == CONSUMPTION_FAILED",
      "closure_state": "CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED",
      "referenced_fields": [
        "authorization_consumption_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-026",
      "priority": 26,
      "predicate": "authorization_consumption_state == UNAVAILABLE",
      "closure_state": "CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE",
      "referenced_fields": [
        "authorization_consumption_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-027",
      "priority": 27,
      "predicate": "rollback_state == PARTIAL_OUTPUT_REMOVED",
      "closure_state": "CLOSURE_PARTIAL_OUTPUT_REMOVED",
      "referenced_fields": [
        "rollback_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-028",
      "priority": 28,
      "predicate": "process_exit_state == EXIT_OBSERVED AND process_exit_code == 0 AND output_creation_state == NOT_CREATED AND raw_artifact_presence == ABSENT",
      "closure_state": "CLOSURE_PROCESS_EXITED_NO_OUTPUT",
      "referenced_fields": [
        "process_exit_state",
        "process_exit_code",
        "output_creation_state",
        "raw_artifact_presence"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-029",
      "priority": 29,
      "predicate": "raw_artifact_presence == ABSENT OR output_creation_state != COMPLETE_CREATED OR output_commit_state != COMMITTED",
      "closure_state": "CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT",
      "referenced_fields": [
        "raw_artifact_presence",
        "output_creation_state",
        "output_commit_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-030",
      "priority": 30,
      "predicate": "output_creation_state == COMPLETE_CREATED AND output_commit_state == COMMITTED AND raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MATCH AND raw_artifact_schema_state == VALID AND raw_branch_consistency_state == CONSISTENT AND raw_result_state == BLOCKING",
      "closure_state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
      "referenced_fields": [
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence",
        "raw_artifact_identity_state",
        "raw_artifact_schema_state",
        "raw_branch_consistency_state",
        "raw_result_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-031",
      "priority": 31,
      "predicate": "output_creation_state == COMPLETE_CREATED AND output_commit_state == COMMITTED AND raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MATCH AND raw_artifact_schema_state == VALID AND raw_branch_consistency_state == CONSISTENT AND raw_result_state == INDETERMINATE",
      "closure_state": "CLOSURE_VALID_RAW_INDETERMINATE_REPORTED",
      "referenced_fields": [
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence",
        "raw_artifact_identity_state",
        "raw_artifact_schema_state",
        "raw_branch_consistency_state",
        "raw_result_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-032",
      "priority": 32,
      "predicate": "output_creation_state == COMPLETE_CREATED AND output_commit_state == COMMITTED AND raw_artifact_presence == PRESENT AND raw_artifact_identity_state == MATCH AND raw_artifact_schema_state == VALID AND raw_branch_consistency_state == CONSISTENT AND raw_result_state == COMPLETE",
      "closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "referenced_fields": [
        "output_creation_state",
        "output_commit_state",
        "raw_artifact_presence",
        "raw_artifact_identity_state",
        "raw_artifact_schema_state",
        "raw_branch_consistency_state",
        "raw_result_state"
      ],
      "semantics": "FIRST_MATCH_RETURN"
    },
    {
      "rule_id": "S3-033",
      "priority": 33,
      "predicate": "TRUE",
      "closure_state": "CLOSURE_EXECUTION_RESULT_INDETERMINATE",
      "referenced_fields": [],
      "semantics": "FIRST_MATCH_RETURN"
    }
  ],
  "stage_4_conformance_rules": [
    {
      "rule_id": "S4-001",
      "priority": 10,
      "predicate": "emitted_closure_state != expected_closure_state",
      "result": "POST_REDUCTION_REJECTED",
      "typed_stop": "STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH",
      "diagnostic_code": "EMITTED_CLOSURE_STATE_DIFFERS_FROM_REDUCER_OUTPUT",
      "evidence_retained": [
        "normalized_inputs",
        "expected_closure_state",
        "emitted_closure_state",
        "reducer_trace"
      ],
      "referenced_fields": [
        "emitted_closure_state",
        "expected_closure_state"
      ],
      "input_contract": {
        "normalized_inputs": "exact Stage-2-valid normalized object",
        "expected_closure_state": "output of reduce_execution_closure(normalized_inputs)",
        "emitted_closure_state": {
          "field_name": "emitted_closure_state",
          "type": "ClosedEnum<ExecutionClosureStateV3>",
          "nullable": false,
          "stage": "STAGE_4_ONLY",
          "not_in_normalized_input_schema": true,
          "observer": "CLOSURE_ARTIFACT_MATERIALIZER_OR_VERIFIER",
          "acceptance_effect": "NONE"
        }
      }
    },
    {
      "rule_id": "S4-002",
      "priority": 20,
      "predicate": "emitted_closure_state == expected_closure_state",
      "result": "POST_REDUCTION_VERIFIED",
      "typed_stop": null,
      "diagnostic_code": "EMITTED_CLOSURE_STATE_MATCHES_REDUCER_OUTPUT",
      "evidence_retained": [
        "normalized_inputs",
        "expected_closure_state",
        "emitted_closure_state",
        "reducer_trace"
      ],
      "referenced_fields": [
        "emitted_closure_state",
        "expected_closure_state"
      ],
      "input_contract": {
        "normalized_inputs": "exact Stage-2-valid normalized object",
        "expected_closure_state": "output of reduce_execution_closure(normalized_inputs)",
        "emitted_closure_state": {
          "field_name": "emitted_closure_state",
          "type": "ClosedEnum<ExecutionClosureStateV3>",
          "nullable": false,
          "stage": "STAGE_4_ONLY",
          "not_in_normalized_input_schema": true,
          "observer": "CLOSURE_ARTIFACT_MATERIALIZER_OR_VERIFIER",
          "acceptance_effect": "NONE"
        }
      }
    }
  ],
  "example_vectors": [
    {
      "example_id": "S1-EX-A001",
      "stage": 1,
      "description": "Invalid UTF-8 stops Group A immediately",
      "input": {
        "raw_document_base64": "/w=="
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "A",
        "primary_stop": "STOP_CLOSURE_UTF8_INVALID",
        "matched_rule_ids": [
          "S1-A-001"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-A002",
      "stage": 1,
      "description": "Truncated JSON stops before duplicate and shape inspection",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "A",
        "primary_stop": "STOP_CLOSURE_JSON_PARSE_INVALID",
        "matched_rule_ids": [
          "S1-A-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-A003",
      "stage": 1,
      "description": "Duplicate key detected before object construction",
      "input": {
        "raw_document_text": "{\"x\":1,\"x\":2}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "A",
        "primary_stop": "STOP_CLOSURE_DUPLICATE_JSON_KEY",
        "matched_rule_ids": [
          "S1-A-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-A004",
      "stage": 1,
      "description": "Top-level array rejected",
      "input": {
        "raw_document_text": "[]"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "A",
        "primary_stop": "STOP_CLOSURE_TOP_LEVEL_OBJECT_REQUIRED",
        "matched_rule_ids": [
          "S1-A-004"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-A005",
      "stage": 1,
      "description": "Plus-prefixed number is invalid JSON and never reaches number-token rules",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":+1,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "A",
        "primary_stop": "STOP_CLOSURE_JSON_PARSE_INVALID",
        "matched_rule_ids": [
          "S1-A-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-A006",
      "stage": 1,
      "description": "Leading-zero number is invalid JSON and never reaches number-token rules",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":01,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "A",
        "primary_stop": "STOP_CLOSURE_JSON_PARSE_INVALID",
        "matched_rule_ids": [
          "S1-A-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-B001",
      "stage": 1,
      "description": "process_exit_code missing; no type, lexical, or range rule evaluates",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "B",
        "primary_stop": "STOP_CLOSURE_REQUIRED_FIELD_MISSING",
        "matched_rule_ids": [
          "S1-B-001",
          "S1-B-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-B002",
      "stage": 1,
      "description": "Unexpected field and excess cardinality retained together",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\",\"unexpected_field\":\"X\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "B",
        "primary_stop": "STOP_CLOSURE_UNEXPECTED_FIELD",
        "matched_rule_ids": [
          "S1-B-002",
          "S1-B-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-B003",
      "stage": 1,
      "description": "Missing and unexpected fields together with unchanged member count",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\",\"unexpected_field\":\"X\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "B",
        "primary_stop": "STOP_CLOSURE_REQUIRED_FIELD_MISSING",
        "matched_rule_ids": [
          "S1-B-001",
          "S1-B-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-B004",
      "stage": 1,
      "description": "Enum field missing; Group D cannot inspect it",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "B",
        "primary_stop": "STOP_CLOSURE_REQUIRED_FIELD_MISSING",
        "matched_rule_ids": [
          "S1-B-001",
          "S1-B-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C001",
      "stage": 1,
      "description": "process_exit_code string rejected before number lexical/range inspection",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":\"1\",\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID",
        "matched_rule_ids": [
          "S1-C-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C002",
      "stage": 1,
      "description": "process_exit_code array rejected before number lexical/range inspection",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":[],\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID",
        "matched_rule_ids": [
          "S1-C-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C003",
      "stage": 1,
      "description": "process_exit_code object rejected before number lexical/range inspection",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":{},\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID",
        "matched_rule_ids": [
          "S1-C-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C004",
      "stage": 1,
      "description": "process_exit_code boolean rejected before number lexical/range inspection",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":true,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_JSON_TYPE_INVALID",
        "matched_rule_ids": [
          "S1-C-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C005",
      "stage": 1,
      "description": "Enum field null matches both non-null and enum-type rules; deterministic primary stop",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":null,\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_NULL_REPRESENTATION_INVALID",
        "matched_rule_ids": [
          "S1-C-001",
          "S1-C-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C006",
      "stage": 1,
      "description": "Enum field integer rejected; lexical and membership rules do not evaluate",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":7,\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_ENUM_JSON_TYPE_INVALID",
        "matched_rule_ids": [
          "S1-C-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-C007",
      "stage": 1,
      "description": "Wrong-type array containing a lexically invalid-looking token is rejected only by Group C",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":[\"bad-token\"],\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "C",
        "primary_stop": "STOP_CLOSURE_ENUM_JSON_TYPE_INVALID",
        "matched_rule_ids": [
          "S1-C-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-D001",
      "stage": 1,
      "description": "Enum lexical form invalid",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"bad-token\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_ENUM_TOKEN_LEXICAL_INVALID",
        "matched_rule_ids": [
          "S1-D-001"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-D002",
      "stage": 1,
      "description": "Lexically valid but unregistered enum token",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"UNKNOWN\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_ENUM_TOKEN_UNREGISTERED",
        "matched_rule_ids": [
          "S1-D-002"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N001",
      "stage": 1,
      "description": "Exact process_exit_code token 0",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "original_number_token": "0",
        "normalized_process_exit_code": 0,
        "matched_rule_ids": [],
        "parsing_evidence_retains_original_token": true
      }
    },
    {
      "example_id": "S1-EX-N002",
      "stage": 1,
      "description": "Exact process_exit_code token -0",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":-0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "original_number_token": "-0",
        "normalized_process_exit_code": 0,
        "matched_rule_ids": [],
        "parsing_evidence_retains_original_token": true
      }
    },
    {
      "example_id": "S1-EX-N003",
      "stage": 1,
      "description": "Exact process_exit_code token 1",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":1,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "original_number_token": "1",
        "normalized_process_exit_code": 1,
        "matched_rule_ids": [],
        "parsing_evidence_retains_original_token": true
      }
    },
    {
      "example_id": "S1-EX-N004",
      "stage": 1,
      "description": "Exact process_exit_code token -1",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":-1,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "original_number_token": "-1",
        "normalized_process_exit_code": -1,
        "matched_rule_ids": [],
        "parsing_evidence_retains_original_token": true
      }
    },
    {
      "example_id": "S1-EX-N005",
      "stage": 1,
      "description": "Exact process_exit_code token 2147483647",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":2147483647,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "original_number_token": "2147483647",
        "normalized_process_exit_code": 2147483647,
        "matched_rule_ids": [],
        "parsing_evidence_retains_original_token": true
      }
    },
    {
      "example_id": "S1-EX-N006",
      "stage": 1,
      "description": "Exact process_exit_code token -2147483648",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":-2147483648,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "original_number_token": "-2147483648",
        "normalized_process_exit_code": -2147483648,
        "matched_rule_ids": [],
        "parsing_evidence_retains_original_token": true
      }
    },
    {
      "example_id": "S1-EX-N007",
      "stage": 1,
      "description": "Exact process_exit_code token 2147483648",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":2147483648,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "original_number_token": "2147483648",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_RANGE_INVALID",
        "matched_rule_ids": [
          "S1-D-004"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N008",
      "stage": 1,
      "description": "Exact process_exit_code token -2147483649",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":-2147483649,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "original_number_token": "-2147483649",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_RANGE_INVALID",
        "matched_rule_ids": [
          "S1-D-004"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N009",
      "stage": 1,
      "description": "Exact process_exit_code token 1.0",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":1.0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "original_number_token": "1.0",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID",
        "matched_rule_ids": [
          "S1-D-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N010",
      "stage": 1,
      "description": "Exact process_exit_code token 1e0",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":1e0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "original_number_token": "1e0",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID",
        "matched_rule_ids": [
          "S1-D-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N011",
      "stage": 1,
      "description": "Exact process_exit_code token 1E0",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":1E0,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "original_number_token": "1E0",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID",
        "matched_rule_ids": [
          "S1-D-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N012",
      "stage": 1,
      "description": "Exact process_exit_code token -2.5",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_OBSERVED\",\"process_exit_code\":-2.5,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_REJECTED",
        "original_number_token": "-2.5",
        "group": "D",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_INTEGER_LEXICAL_INVALID",
        "matched_rule_ids": [
          "S1-D-003"
        ],
        "later_groups_evaluated": []
      }
    },
    {
      "example_id": "S1-EX-N013",
      "stage": 1,
      "description": "JSON null is a valid Stage-1 representation for process_exit_code",
      "input": {
        "raw_document_text": "{\"execution_attempt_state\":\"EXACTLY_ONE\",\"process_launch_state\":\"LAUNCHED\",\"process_exit_state\":\"EXIT_NOT_OBSERVED\",\"process_exit_code\":null,\"output_creation_state\":\"COMPLETE_CREATED\",\"output_commit_state\":\"COMMITTED\",\"raw_artifact_presence\":\"PRESENT\",\"raw_artifact_identity_state\":\"MATCH\",\"raw_artifact_schema_state\":\"VALID\",\"raw_result_state\":\"COMPLETE\",\"raw_branch_consistency_state\":\"CONSISTENT\",\"rollback_state\":\"NOT_REQUIRED\",\"authorization_valid_at_start\":\"VALID\",\"authorization_valid_at_completion\":\"VALID\",\"authorization_consumption_state\":\"CONSUMED\"}"
      },
      "expected": {
        "result": "PARSE_AND_SHAPE_VALID",
        "normalized_process_exit_code": null,
        "matched_rule_ids": []
      }
    },
    {
      "example_id": "S2-EX-001",
      "stage": 2,
      "description": "Witness for S2-001: ATTEMPT_NOT_ATTEMPTED_BUT_LAUNCH_NOT_NOT_ATTEMPTED",
      "target_rule_id": "S2-001",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-001"
        ],
        "complete_ordered_diagnostics": [
          "ATTEMPT_NOT_ATTEMPTED_BUT_LAUNCH_NOT_NOT_ATTEMPTED"
        ]
      }
    },
    {
      "example_id": "S2-EX-002",
      "stage": 2,
      "description": "Witness for S2-002: ATTEMPT_PRESENT_BUT_LAUNCH_NOT_ATTEMPTED",
      "target_rule_id": "S2-002",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-002"
        ],
        "complete_ordered_diagnostics": [
          "ATTEMPT_PRESENT_BUT_LAUNCH_NOT_ATTEMPTED"
        ]
      }
    },
    {
      "example_id": "S2-EX-003",
      "stage": 2,
      "description": "Witness for S2-003: EXIT_STATE_REPORTED_WITHOUT_LAUNCHED_PROCESS",
      "target_rule_id": "S2-003",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS",
        "matched_rule_ids": [
          "S2-003"
        ],
        "complete_ordered_diagnostics": [
          "EXIT_STATE_REPORTED_WITHOUT_LAUNCHED_PROCESS"
        ]
      }
    },
    {
      "example_id": "S2-EX-004",
      "stage": 2,
      "description": "Witness for S2-004: LAUNCH_UNAVAILABLE_REQUIRES_EXIT_UNAVAILABLE",
      "target_rule_id": "S2-004",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "UNAVAILABLE",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_LAUNCH_RESULT_EXIT_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-004"
        ],
        "complete_ordered_diagnostics": [
          "LAUNCH_UNAVAILABLE_REQUIRES_EXIT_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-005",
      "stage": 2,
      "description": "Witness for S2-005: LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE",
      "target_rule_id": "S2-005",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE",
        "matched_rule_ids": [
          "S2-005"
        ],
        "complete_ordered_diagnostics": [
          "LAUNCHED_PROCESS_EXIT_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-006",
      "stage": 2,
      "description": "Witness for S2-006: EXIT_CODE_NULLABILITY_RELATION_INVALID",
      "target_rule_id": "S2-006",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": null,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_EXIT_CODE_NULLABILITY_INVALID",
        "matched_rule_ids": [
          "S2-006"
        ],
        "complete_ordered_diagnostics": [
          "EXIT_CODE_NULLABILITY_RELATION_INVALID"
        ]
      }
    },
    {
      "example_id": "S2-EX-007",
      "stage": 2,
      "description": "Witness for S2-007: NO_ATTEMPT_WITH_OUTPUT_CREATION",
      "target_rule_id": "S2-007",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-007"
        ],
        "complete_ordered_diagnostics": [
          "NO_ATTEMPT_WITH_OUTPUT_CREATION"
        ]
      }
    },
    {
      "example_id": "S2-EX-008",
      "stage": 2,
      "description": "Witness for S2-008: NO_ATTEMPT_WITH_OUTPUT_COMMIT_ACTIVITY",
      "target_rule_id": "S2-008",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_COMMIT_INVALID",
        "matched_rule_ids": [
          "S2-008"
        ],
        "complete_ordered_diagnostics": [
          "NO_ATTEMPT_WITH_OUTPUT_COMMIT_ACTIVITY"
        ]
      }
    },
    {
      "example_id": "S2-EX-009",
      "stage": 2,
      "description": "Witness for S2-009: NO_ATTEMPT_WITH_NONABSENT_RAW_ARTIFACT",
      "target_rule_id": "S2-009",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_NO_ATTEMPT_RAW_ARTIFACT_INVALID",
        "matched_rule_ids": [
          "S2-009",
          "S2-014"
        ],
        "complete_ordered_diagnostics": [
          "NO_ATTEMPT_WITH_NONABSENT_RAW_ARTIFACT",
          "RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION"
        ]
      }
    },
    {
      "example_id": "S2-EX-010",
      "stage": 2,
      "description": "Witness for S2-010: NO_ATTEMPT_WITH_ROLLBACK_ACTIVITY",
      "target_rule_id": "S2-010",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_NO_ATTEMPT_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-007",
          "S2-010"
        ],
        "complete_ordered_diagnostics": [
          "NO_ATTEMPT_WITH_OUTPUT_CREATION",
          "NO_ATTEMPT_WITH_ROLLBACK_ACTIVITY"
        ]
      }
    },
    {
      "example_id": "S2-EX-011",
      "stage": 2,
      "description": "Witness for S2-011: COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
      "target_rule_id": "S2-011",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-011",
          "S2-013",
          "S2-023"
        ],
        "complete_ordered_diagnostics": [
          "COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
          "PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
          "PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED"
        ]
      }
    },
    {
      "example_id": "S2-EX-012",
      "stage": 2,
      "description": "Witness for S2-012: COMMITTED_OUTPUT_REQUIRES_PRESENT_RAW_ARTIFACT",
      "target_rule_id": "S2-012",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_COMMITTED_RAW_ARTIFACT_STATE_INVALID",
        "matched_rule_ids": [
          "S2-012"
        ],
        "complete_ordered_diagnostics": [
          "COMMITTED_OUTPUT_REQUIRES_PRESENT_RAW_ARTIFACT"
        ]
      }
    },
    {
      "example_id": "S2-EX-013",
      "stage": 2,
      "description": "Witness for S2-013: PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
      "target_rule_id": "S2-013",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-011",
          "S2-013",
          "S2-023"
        ],
        "complete_ordered_diagnostics": [
          "COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
          "PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
          "PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED"
        ]
      }
    },
    {
      "example_id": "S2-EX-014",
      "stage": 2,
      "description": "Witness for S2-014: RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION",
      "target_rule_id": "S2-014",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION",
        "matched_rule_ids": [
          "S2-014"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION"
        ]
      }
    },
    {
      "example_id": "S2-EX-015",
      "stage": 2,
      "description": "Witness for S2-015: PARTIAL_REMOVAL_REQUIRES_PARTIAL_CREATION",
      "target_rule_id": "S2-015",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "PARTIAL_OUTPUT_REMOVED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID",
        "matched_rule_ids": [
          "S2-015"
        ],
        "complete_ordered_diagnostics": [
          "PARTIAL_REMOVAL_REQUIRES_PARTIAL_CREATION"
        ]
      }
    },
    {
      "example_id": "S2-EX-016",
      "stage": 2,
      "description": "Witness for S2-016: PARTIAL_REMOVAL_REQUIRES_NO_COMMIT",
      "target_rule_id": "S2-016",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "PARTIAL_OUTPUT_REMOVED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-011",
          "S2-013",
          "S2-016",
          "S2-017"
        ],
        "complete_ordered_diagnostics": [
          "COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
          "PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
          "PARTIAL_REMOVAL_REQUIRES_NO_COMMIT",
          "PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE"
        ]
      }
    },
    {
      "example_id": "S2-EX-017",
      "stage": 2,
      "description": "Witness for S2-017: PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE",
      "target_rule_id": "S2-017",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "PARTIAL_OUTPUT_REMOVED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_REMOVAL_STATE_INVALID",
        "matched_rule_ids": [
          "S2-017"
        ],
        "complete_ordered_diagnostics": [
          "PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE"
        ]
      }
    },
    {
      "example_id": "S2-EX-018",
      "stage": 2,
      "description": "Witness for S2-018: ROLLBACK_RESIDUE_REQUIRES_PARTIAL_CREATION",
      "target_rule_id": "S2-018",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID",
        "matched_rule_ids": [
          "S2-018"
        ],
        "complete_ordered_diagnostics": [
          "ROLLBACK_RESIDUE_REQUIRES_PARTIAL_CREATION"
        ]
      }
    },
    {
      "example_id": "S2-EX-019",
      "stage": 2,
      "description": "Witness for S2-019: ROLLBACK_RESIDUE_REQUIRES_NO_COMMIT",
      "target_rule_id": "S2-019",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-011",
          "S2-013",
          "S2-019"
        ],
        "complete_ordered_diagnostics": [
          "COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
          "PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
          "ROLLBACK_RESIDUE_REQUIRES_NO_COMMIT"
        ]
      }
    },
    {
      "example_id": "S2-EX-020",
      "stage": 2,
      "description": "Witness for S2-020: ROLLBACK_RESIDUE_REQUIRES_FINAL_PRESENCE",
      "target_rule_id": "S2-020",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ROLLBACK_RESIDUE_STATE_INVALID",
        "matched_rule_ids": [
          "S2-020"
        ],
        "complete_ordered_diagnostics": [
          "ROLLBACK_RESIDUE_REQUIRES_FINAL_PRESENCE"
        ]
      }
    },
    {
      "example_id": "S2-EX-021",
      "stage": 2,
      "description": "Witness for S2-021: ROLLBACK_UNAVAILABLE_REQUIRES_PARTIAL_CREATION",
      "target_rule_id": "S2-021",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_RESULT_UNAVAILABLE",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID",
        "matched_rule_ids": [
          "S2-021"
        ],
        "complete_ordered_diagnostics": [
          "ROLLBACK_UNAVAILABLE_REQUIRES_PARTIAL_CREATION"
        ]
      }
    },
    {
      "example_id": "S2-EX-022",
      "stage": 2,
      "description": "Witness for S2-022: ROLLBACK_UNAVAILABLE_REQUIRES_FINAL_PRESENCE_UNAVAILABLE",
      "target_rule_id": "S2-022",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "ROLLBACK_RESULT_UNAVAILABLE",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ROLLBACK_RESULT_UNAVAILABLE_STATE_INVALID",
        "matched_rule_ids": [
          "S2-022"
        ],
        "complete_ordered_diagnostics": [
          "ROLLBACK_UNAVAILABLE_REQUIRES_FINAL_PRESENCE_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-023",
      "stage": 2,
      "description": "Witness for S2-023: PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED",
      "target_rule_id": "S2-023",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_PARTIAL_OUTPUT_ROLLBACK_NOT_REQUIRED",
        "matched_rule_ids": [
          "S2-023"
        ],
        "complete_ordered_diagnostics": [
          "PARTIAL_OUTPUT_CANNOT_MARK_ROLLBACK_NOT_REQUIRED"
        ]
      }
    },
    {
      "example_id": "S2-EX-024",
      "stage": 2,
      "description": "Witness for S2-024: ROLLBACK_NOT_ATTEMPTED_REQUIRES_PARTIAL_OUTPUT",
      "target_rule_id": "S2-024",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_STATE_INVALID",
        "matched_rule_ids": [
          "S2-024",
          "S2-049"
        ],
        "complete_ordered_diagnostics": [
          "ROLLBACK_NOT_ATTEMPTED_REQUIRES_PARTIAL_OUTPUT",
          "ROLLBACK_NOT_ATTEMPTED_REQUIRES_NO_SUCCESSFUL_OR_UNAVAILABLE_COMMIT"
        ]
      }
    },
    {
      "example_id": "S2-EX-025",
      "stage": 2,
      "description": "Witness for S2-025: RAW_ABSENCE_REQUIRES_IDENTITY_NOT_APPLICABLE",
      "target_rule_id": "S2-025",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT",
        "matched_rule_ids": [
          "S2-025"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ABSENCE_REQUIRES_IDENTITY_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-026",
      "stage": 2,
      "description": "Witness for S2-026: RAW_ABSENCE_REQUIRES_SCHEMA_NOT_APPLICABLE",
      "target_rule_id": "S2-026",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_SCHEMA_WITHOUT_ARTIFACT",
        "matched_rule_ids": [
          "S2-026"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ABSENCE_REQUIRES_SCHEMA_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-027",
      "stage": 2,
      "description": "Witness for S2-027: RAW_ABSENCE_REQUIRES_RESULT_NOT_APPLICABLE",
      "target_rule_id": "S2-027",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_RESULT_WITHOUT_ARTIFACT",
        "matched_rule_ids": [
          "S2-027",
          "S2-039"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ABSENCE_REQUIRES_RESULT_NOT_APPLICABLE",
          "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-028",
      "stage": 2,
      "description": "Witness for S2-028: RAW_ABSENCE_REQUIRES_BRANCH_NOT_APPLICABLE",
      "target_rule_id": "S2-028",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_BRANCH_WITHOUT_ARTIFACT",
        "matched_rule_ids": [
          "S2-028",
          "S2-040"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ABSENCE_REQUIRES_BRANCH_NOT_APPLICABLE",
          "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-029",
      "stage": 2,
      "description": "Witness for S2-029: RAW_UNAVAILABLE_REQUIRES_IDENTITY_UNAVAILABLE",
      "target_rule_id": "S2-029",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "UNAVAILABLE",
        "process_exit_state": "UNAVAILABLE",
        "process_exit_code": null,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-029"
        ],
        "complete_ordered_diagnostics": [
          "RAW_UNAVAILABLE_REQUIRES_IDENTITY_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-030",
      "stage": 2,
      "description": "Witness for S2-030: RAW_UNAVAILABLE_REQUIRES_SCHEMA_UNAVAILABLE",
      "target_rule_id": "S2-030",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "UNAVAILABLE",
        "process_exit_state": "UNAVAILABLE",
        "process_exit_code": null,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-030"
        ],
        "complete_ordered_diagnostics": [
          "RAW_UNAVAILABLE_REQUIRES_SCHEMA_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-031",
      "stage": 2,
      "description": "Witness for S2-031: RAW_UNAVAILABLE_REQUIRES_RESULT_UNAVAILABLE",
      "target_rule_id": "S2-031",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "UNAVAILABLE",
        "process_exit_state": "UNAVAILABLE",
        "process_exit_code": null,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-031",
          "S2-039"
        ],
        "complete_ordered_diagnostics": [
          "RAW_UNAVAILABLE_REQUIRES_RESULT_UNAVAILABLE",
          "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-032",
      "stage": 2,
      "description": "Witness for S2-032: RAW_UNAVAILABLE_REQUIRES_BRANCH_UNAVAILABLE",
      "target_rule_id": "S2-032",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "UNAVAILABLE",
        "process_exit_state": "UNAVAILABLE",
        "process_exit_code": null,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_UNAVAILABLE_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-032",
          "S2-040"
        ],
        "complete_ordered_diagnostics": [
          "RAW_UNAVAILABLE_REQUIRES_BRANCH_UNAVAILABLE",
          "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-033",
      "stage": 2,
      "description": "Witness for S2-033: RAW_PRESENT_FORBIDS_IDENTITY_NOT_APPLICABLE",
      "target_rule_id": "S2-033",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
        "matched_rule_ids": [
          "S2-033"
        ],
        "complete_ordered_diagnostics": [
          "RAW_PRESENT_FORBIDS_IDENTITY_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-034",
      "stage": 2,
      "description": "Witness for S2-034: RAW_PRESENT_FORBIDS_SCHEMA_NOT_APPLICABLE",
      "target_rule_id": "S2-034",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
        "matched_rule_ids": [
          "S2-034",
          "S2-039",
          "S2-040"
        ],
        "complete_ordered_diagnostics": [
          "RAW_PRESENT_FORBIDS_SCHEMA_NOT_APPLICABLE",
          "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA",
          "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-035",
      "stage": 2,
      "description": "Witness for S2-035: RAW_PRESENT_FORBIDS_RESULT_NOT_APPLICABLE",
      "target_rule_id": "S2-035",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
        "matched_rule_ids": [
          "S2-035"
        ],
        "complete_ordered_diagnostics": [
          "RAW_PRESENT_FORBIDS_RESULT_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-036",
      "stage": 2,
      "description": "Witness for S2-036: RAW_PRESENT_FORBIDS_BRANCH_NOT_APPLICABLE",
      "target_rule_id": "S2-036",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
        "matched_rule_ids": [
          "S2-036"
        ],
        "complete_ordered_diagnostics": [
          "RAW_PRESENT_FORBIDS_BRANCH_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-037",
      "stage": 2,
      "description": "Witness for S2-037: INVALID_SCHEMA_WITH_VALID_RESULT_LITERAL",
      "target_rule_id": "S2-037",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_RESULT_WITH_INVALID_SCHEMA",
        "matched_rule_ids": [
          "S2-037",
          "S2-039"
        ],
        "complete_ordered_diagnostics": [
          "INVALID_SCHEMA_WITH_VALID_RESULT_LITERAL",
          "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-038",
      "stage": 2,
      "description": "Witness for S2-038: INVALID_LITERAL_REQUIRES_INVALID_SCHEMA",
      "target_rule_id": "S2-038",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_INVALID_LITERAL_SCHEMA_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-038"
        ],
        "complete_ordered_diagnostics": [
          "INVALID_LITERAL_REQUIRES_INVALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-039",
      "stage": 2,
      "description": "Witness for S2-039: VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA",
      "target_rule_id": "S2-039",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_VALID_RESULT_WITHOUT_VALID_SCHEMA",
        "matched_rule_ids": [
          "S2-039"
        ],
        "complete_ordered_diagnostics": [
          "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA"
        ]
      }
    },
    {
      "example_id": "S2-EX-040",
      "stage": 2,
      "description": "Witness for S2-040: BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA",
      "target_rule_id": "S2-040",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-040",
          "S2-041"
        ],
        "complete_ordered_diagnostics": [
          "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA",
          "INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-041",
      "stage": 2,
      "description": "Witness for S2-041: INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE",
      "target_rule_id": "S2-041",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_BRANCH_VALIDATION_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-040",
          "S2-041"
        ],
        "complete_ordered_diagnostics": [
          "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA",
          "INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-042",
      "stage": 2,
      "description": "Witness for S2-042: NO_ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_NOT_APPLICABLE",
      "target_rule_id": "S2-042",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID",
        "matched_rule_ids": [
          "S2-042"
        ],
        "complete_ordered_diagnostics": [
          "NO_ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-043",
      "stage": 2,
      "description": "Witness for S2-043: ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_APPLICABLE",
      "target_rule_id": "S2-043",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_AUTHORIZATION_COMPLETION_APPLICABILITY_INVALID",
        "matched_rule_ids": [
          "S2-043"
        ],
        "complete_ordered_diagnostics": [
          "ATTEMPT_REQUIRES_COMPLETION_AUTHORITY_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-044",
      "stage": 2,
      "description": "Witness for S2-044: AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT",
      "target_rule_id": "S2-044",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT",
        "matched_rule_ids": [
          "S2-044"
        ],
        "complete_ordered_diagnostics": [
          "AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT"
        ]
      }
    },
    {
      "example_id": "S2-EX-045",
      "stage": 2,
      "description": "Witness for S2-045: NO_ATTEMPT_REQUIRES_CONSUMPTION_NOT_APPLICABLE",
      "target_rule_id": "S2-045",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID",
        "matched_rule_ids": [
          "S2-045"
        ],
        "complete_ordered_diagnostics": [
          "NO_ATTEMPT_REQUIRES_CONSUMPTION_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-046",
      "stage": 2,
      "description": "Witness for S2-046: ATTEMPT_REQUIRES_CONSUMPTION_APPLICABLE",
      "target_rule_id": "S2-046",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_AUTHORIZATION_CONSUMPTION_APPLICABILITY_INVALID",
        "matched_rule_ids": [
          "S2-046"
        ],
        "complete_ordered_diagnostics": [
          "ATTEMPT_REQUIRES_CONSUMPTION_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-047",
      "stage": 2,
      "description": "Witness for S2-047: LAUNCH_FAILED_WITH_COMMITTED_OUTPUT",
      "target_rule_id": "S2-047",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "BLOCKING",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_LAUNCH_FAILED_WITH_COMMITTED_OR_COMPLETE_RAW",
        "matched_rule_ids": [
          "S2-047"
        ],
        "complete_ordered_diagnostics": [
          "LAUNCH_FAILED_WITH_COMMITTED_OUTPUT"
        ]
      }
    },
    {
      "example_id": "S2-EX-048",
      "stage": 2,
      "description": "Witness for S2-048: LAUNCH_FAILED_WITH_RAW_COMPLETE_RESULT",
      "target_rule_id": "S2-048",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_WITHOUT_OUTPUT_CREATION",
        "matched_rule_ids": [
          "S2-014",
          "S2-048"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ARTIFACT_PRESENT_WITHOUT_OUTPUT_CREATION",
          "LAUNCH_FAILED_WITH_RAW_COMPLETE_RESULT"
        ]
      }
    },
    {
      "example_id": "S2-OVERLAP-01",
      "stage": 2,
      "description": "Overlapping normalized contradictions with deterministic primary-stop selection",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_PROCESS_EXIT_WITHOUT_LAUNCHED_PROCESS",
        "matched_rule_ids": [
          "S2-003",
          "S2-047",
          "S2-048"
        ],
        "complete_ordered_diagnostics": [
          "EXIT_STATE_REPORTED_WITHOUT_LAUNCHED_PROCESS",
          "LAUNCH_FAILED_WITH_COMMITTED_OUTPUT",
          "LAUNCH_FAILED_WITH_RAW_COMPLETE_RESULT"
        ]
      }
    },
    {
      "example_id": "S2-OVERLAP-02",
      "stage": 2,
      "description": "Overlapping normalized contradictions with deterministic primary-stop selection",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_IDENTITY_WITHOUT_ARTIFACT",
        "matched_rule_ids": [
          "S2-025",
          "S2-026"
        ],
        "complete_ordered_diagnostics": [
          "RAW_ABSENCE_REQUIRES_IDENTITY_NOT_APPLICABLE",
          "RAW_ABSENCE_REQUIRES_SCHEMA_NOT_APPLICABLE"
        ]
      }
    },
    {
      "example_id": "S2-OVERLAP-03",
      "stage": 2,
      "description": "Overlapping normalized contradictions with deterministic primary-stop selection",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "PARTIAL_OUTPUT_REMOVED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_COMMITTED_OUTPUT_CREATION_INVALID",
        "matched_rule_ids": [
          "S2-011",
          "S2-013",
          "S2-016",
          "S2-017"
        ],
        "complete_ordered_diagnostics": [
          "COMMITTED_OUTPUT_REQUIRES_COMPLETE_CREATION",
          "PARTIAL_OUTPUT_CANNOT_BE_COMMITTED",
          "PARTIAL_REMOVAL_REQUIRES_NO_COMMIT",
          "PARTIAL_REMOVAL_REQUIRES_FINAL_ABSENCE"
        ]
      }
    },
    {
      "example_id": "S2-OVERLAP-04",
      "stage": 2,
      "description": "Overlapping normalized contradictions with deterministic primary-stop selection",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ATTEMPT_LAUNCH_RELATION_INVALID",
        "matched_rule_ids": [
          "S2-001",
          "S2-044"
        ],
        "complete_ordered_diagnostics": [
          "ATTEMPT_NOT_ATTEMPTED_BUT_LAUNCH_NOT_NOT_ATTEMPTED",
          "AUTHORIZATION_CONSUMED_WITHOUT_ATTEMPT"
        ]
      }
    },
    {
      "example_id": "S2-OVERLAP-05",
      "stage": 2,
      "description": "Overlapping normalized contradictions with deterministic primary-stop selection",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_RAW_PRESENT_VALIDATION_NOT_APPLICABLE",
        "matched_rule_ids": [
          "S2-033",
          "S2-037",
          "S2-039",
          "S2-040",
          "S2-041"
        ],
        "complete_ordered_diagnostics": [
          "RAW_PRESENT_FORBIDS_IDENTITY_NOT_APPLICABLE",
          "INVALID_SCHEMA_WITH_VALID_RESULT_LITERAL",
          "VALID_RESULT_LITERAL_REQUIRES_VALID_SCHEMA",
          "BRANCH_CLASSIFICATION_REQUIRES_VALID_SCHEMA",
          "INVALID_SCHEMA_REQUIRES_BRANCH_UNAVAILABLE"
        ]
      }
    },
    {
      "example_id": "S2-EX-054",
      "stage": 2,
      "description": "Witness for S2-049: rollback NOT_ATTEMPTED permits only NOT_ATTEMPTED or COMMIT_FAILED commit states",
      "target_rule_id": "S2-049",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "NORMALIZED_INPUT_REJECTED",
        "primary_stop": "STOP_CLOSURE_ROLLBACK_NOT_ATTEMPTED_COMMIT_STATE_INVALID",
        "matched_rule_ids": [
          "S2-049"
        ],
        "complete_ordered_diagnostics": [
          "ROLLBACK_NOT_ATTEMPTED_REQUIRES_NO_SUCCESSFUL_OR_UNAVAILABLE_COMMIT"
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_ROLLBACK_RESIDUE_PRESENT",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_ROLLBACK_RESIDUE_PRESENT",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-001",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_ROLLBACK_RESULT_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_ROLLBACK_RESULT_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_RESULT_UNAVAILABLE",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESULT_UNAVAILABLE",
        "first_matched_rule_id": "S3-002",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_INVALID_AT_START",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_INVALID_AT_START",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "INVALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_INVALID_AT_START",
        "first_matched_rule_id": "S3-006",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "UNAVAILABLE",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_START_VALIDITY_UNAVAILABLE",
        "first_matched_rule_id": "S3-007",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_EXECUTION_ATTEMPT_MULTIPLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_EXECUTION_ATTEMPT_MULTIPLE",
      "normalized_inputs": {
        "execution_attempt_state": "MULTIPLE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLE",
        "first_matched_rule_id": "S3-008",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "UNAVAILABLE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE",
        "first_matched_rule_id": "S3-009",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_EXECUTION_NOT_ATTEMPTED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_EXECUTION_NOT_ATTEMPTED",
      "normalized_inputs": {
        "execution_attempt_state": "NOT_ATTEMPTED",
        "process_launch_state": "NOT_ATTEMPTED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "NOT_APPLICABLE",
        "authorization_consumption_state": "NOT_APPLICABLE"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_EXECUTION_NOT_ATTEMPTED",
        "first_matched_rule_id": "S3-010",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_PROCESS_LAUNCH_FAILED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_PROCESS_LAUNCH_FAILED",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_PROCESS_LAUNCH_FAILED",
        "first_matched_rule_id": "S3-011",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "UNAVAILABLE",
        "process_exit_state": "UNAVAILABLE",
        "process_exit_code": null,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_PROCESS_LAUNCH_RESULT_UNAVAILABLE",
        "first_matched_rule_id": "S3-012",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_PROCESS_EXIT_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_PROCESS_EXIT_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_NOT_OBSERVED",
        "process_exit_code": null,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_PROCESS_EXIT_UNAVAILABLE",
        "first_matched_rule_id": "S3-013",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_PROCESS_EXIT_NONZERO",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_PROCESS_EXIT_NONZERO",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 7,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_PROCESS_EXIT_NONZERO",
        "first_matched_rule_id": "S3-014",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_OUTPUT_STATE_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_OUTPUT_STATE_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "UNAVAILABLE",
        "output_commit_state": "UNAVAILABLE",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_OUTPUT_STATE_UNAVAILABLE",
        "first_matched_rule_id": "S3-015",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_RAW_ARTIFACT_IDENTITY_MISMATCH",
        "first_matched_rule_id": "S3-016",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_RAW_ARTIFACT_VALIDATION_UNAVAILABLE",
        "first_matched_rule_id": "S3-017",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_RAW_ARTIFACT_SCHEMA_INVALID",
        "first_matched_rule_id": "S3-018",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONTRADICTORY",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_RAW_ARTIFACT_BRANCH_CONTRADICTION",
        "first_matched_rule_id": "S3-020",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "EXPIRED",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_EXPIRED_DURING_EXECUTION",
        "first_matched_rule_id": "S3-022",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "INVALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_INVALID_AT_COMPLETION",
        "first_matched_rule_id": "S3-023",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "UNAVAILABLE",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_COMPLETION_VALIDITY_UNAVAILABLE",
        "first_matched_rule_id": "S3-024",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMPTION_FAILED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_CONSUMPTION_FAILED",
        "first_matched_rule_id": "S3-025",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "UNAVAILABLE"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_AUTHORIZATION_CONSUMPTION_UNAVAILABLE",
        "first_matched_rule_id": "S3-026",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_PARTIAL_OUTPUT_REMOVED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_PARTIAL_OUTPUT_REMOVED",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "PARTIAL_OUTPUT_REMOVED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_PARTIAL_OUTPUT_REMOVED",
        "first_matched_rule_id": "S3-027",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_PROCESS_EXITED_NO_OUTPUT",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_PROCESS_EXITED_NO_OUTPUT",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "NOT_CREATED",
        "output_commit_state": "NOT_ATTEMPTED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_PROCESS_EXITED_NO_OUTPUT",
        "first_matched_rule_id": "S3-028",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_COMPLETED_NO_VALID_RAW_ARTIFACT",
        "first_matched_rule_id": "S3-029",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_VALID_RAW_BLOCKING_REPORTED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_VALID_RAW_BLOCKING_REPORTED",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "BLOCKING",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
        "first_matched_rule_id": "S3-030",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_VALID_RAW_INDETERMINATE_REPORTED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_VALID_RAW_INDETERMINATE_REPORTED",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "INDETERMINATE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_VALID_RAW_INDETERMINATE_REPORTED",
        "first_matched_rule_id": "S3-031",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": false
          },
          {
            "rule_id": "S3-031",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
        "first_matched_rule_id": "S3-032",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": false
          },
          {
            "rule_id": "S3-031",
            "matched": false
          },
          {
            "rule_id": "S3-032",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_EXECUTION_RESULT_INDETERMINATE",
      "stage": 3,
      "description": "Representative normalized-valid vector for CLOSURE_EXECUTION_RESULT_INDETERMINATE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_EXECUTION_RESULT_INDETERMINATE",
        "first_matched_rule_id": "S3-033",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": false
          },
          {
            "rule_id": "S3-031",
            "matched": false
          },
          {
            "rule_id": "S3-032",
            "matched": false
          },
          {
            "rule_id": "S3-033",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-CONFLICT-RESIDUE-AUTH-INVALID",
      "stage": 3,
      "description": "Precedence-conflict or final-fallback vector",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "INVALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-001",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-CONFLICT-RESIDUE-MULTIPLE",
      "stage": 3,
      "description": "Precedence-conflict or final-fallback vector",
      "normalized_inputs": {
        "execution_attempt_state": "MULTIPLE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-001",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-CONFLICT-RESIDUE-LAUNCH-FAILED",
      "stage": 3,
      "description": "Precedence-conflict or final-fallback vector",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-001",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-CONFLICT-RESIDUE-COMPLETE-RAW",
      "stage": 3,
      "description": "Precedence-conflict or final-fallback vector",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-001",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-CONFLICT-ROLLBACK-UNAVAILABLE-CHILD-COMPLETE-ECHO",
      "stage": 3,
      "description": "Precedence-conflict or final-fallback vector",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_RESULT_UNAVAILABLE",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_RESULT_UNAVAILABLE",
        "first_matched_rule_id": "S3-002",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": true
          }
        ]
      },
      "non_authoritative_context": {
        "child_echo": "COMPLETE",
        "treatment": "NOT_A_NORMALIZED_EXECUTION_FACT; outer raw presence and validation remain UNAVAILABLE"
      }
    },
    {
      "example_id": "S3-FINAL-INDETERMINATE",
      "stage": 3,
      "description": "Precedence-conflict or final-fallback vector",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_EXECUTION_RESULT_INDETERMINATE",
        "first_matched_rule_id": "S3-033",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": false
          },
          {
            "rule_id": "S3-031",
            "matched": false
          },
          {
            "rule_id": "S3-032",
            "matched": false
          },
          {
            "rule_id": "S3-033",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
      "stage": 3,
      "description": "Representative Stage-2-valid vector for CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-003",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
      "stage": 3,
      "description": "Representative Stage-2-valid vector for CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
        "first_matched_rule_id": "S3-004",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-STATE-CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
      "stage": 3,
      "description": "Representative Stage-2-valid vector for CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
        "first_matched_rule_id": "S3-005",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-001",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue present dominates invalid authority at start",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "INVALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-003",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-002",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue unavailable dominates multiple attempts",
      "normalized_inputs": {
        "execution_attempt_state": "MULTIPLE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
        "first_matched_rule_id": "S3-004",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-003",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED final absence dominates launch failure",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCH_FAILED",
        "process_exit_state": "NOT_APPLICABLE",
        "process_exit_code": null,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
        "first_matched_rule_id": "S3-005",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-004",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue present dominates nonzero exit",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 7,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-003",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-005",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue present dominates raw identity mismatch",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-003",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-006",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue present dominates invalid raw schema",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-003",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-007",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue present dominates apparently COMPLETE raw result",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "first_matched_rule_id": "S3-003",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-008",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED residue unavailable dominates authority expiry",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "UNAVAILABLE",
        "raw_artifact_identity_state": "UNAVAILABLE",
        "raw_artifact_schema_state": "UNAVAILABLE",
        "raw_result_state": "UNAVAILABLE",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "EXPIRED",
        "authorization_consumption_state": "CONSUMED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_UNAVAILABLE",
        "first_matched_rule_id": "S3-004",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S3-C03-CONFLICT-009",
      "stage": 3,
      "description": "rollback NOT_ATTEMPTED final absence dominates consumption failure",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "ABSENT",
        "raw_artifact_identity_state": "NOT_APPLICABLE",
        "raw_artifact_schema_state": "NOT_APPLICABLE",
        "raw_result_state": "NOT_APPLICABLE",
        "raw_branch_consistency_state": "NOT_APPLICABLE",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMPTION_FAILED"
      },
      "expected": {
        "result": "CLOSURE_STATE_REDUCED",
        "closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_FINAL_ABSENCE",
        "first_matched_rule_id": "S3-005",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S4-EX-001",
      "stage": 4,
      "description": "Emitted state exactly equals reducer output",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "emitted_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "expected": {
        "result": "POST_REDUCTION_VERIFIED",
        "expected_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
        "emitted_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": false
          },
          {
            "rule_id": "S3-031",
            "matched": false
          },
          {
            "rule_id": "S3-032",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S4-EX-002",
      "stage": 4,
      "description": "Emitted state differs from reducer output",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "emitted_closure_state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
      "expected": {
        "result": "POST_REDUCTION_REJECTED",
        "typed_stop": "STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH",
        "expected_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
        "emitted_closure_state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": false
          },
          {
            "rule_id": "S3-010",
            "matched": false
          },
          {
            "rule_id": "S3-011",
            "matched": false
          },
          {
            "rule_id": "S3-012",
            "matched": false
          },
          {
            "rule_id": "S3-013",
            "matched": false
          },
          {
            "rule_id": "S3-014",
            "matched": false
          },
          {
            "rule_id": "S3-015",
            "matched": false
          },
          {
            "rule_id": "S3-016",
            "matched": false
          },
          {
            "rule_id": "S3-017",
            "matched": false
          },
          {
            "rule_id": "S3-018",
            "matched": false
          },
          {
            "rule_id": "S3-019",
            "matched": false
          },
          {
            "rule_id": "S3-020",
            "matched": false
          },
          {
            "rule_id": "S3-021",
            "matched": false
          },
          {
            "rule_id": "S3-022",
            "matched": false
          },
          {
            "rule_id": "S3-023",
            "matched": false
          },
          {
            "rule_id": "S3-024",
            "matched": false
          },
          {
            "rule_id": "S3-025",
            "matched": false
          },
          {
            "rule_id": "S3-026",
            "matched": false
          },
          {
            "rule_id": "S3-027",
            "matched": false
          },
          {
            "rule_id": "S3-028",
            "matched": false
          },
          {
            "rule_id": "S3-029",
            "matched": false
          },
          {
            "rule_id": "S3-030",
            "matched": false
          },
          {
            "rule_id": "S3-031",
            "matched": false
          },
          {
            "rule_id": "S3-032",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S4-EX-003",
      "stage": 4,
      "description": "Complete-looking emitted state while attempt multiplicity is unavailable",
      "normalized_inputs": {
        "execution_attempt_state": "UNAVAILABLE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "COMPLETE_CREATED",
        "output_commit_state": "COMMITTED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_REQUIRED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "emitted_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "expected": {
        "result": "POST_REDUCTION_REJECTED",
        "typed_stop": "STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH",
        "expected_closure_state": "CLOSURE_EXECUTION_ATTEMPT_MULTIPLICITY_UNAVAILABLE",
        "emitted_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": false
          },
          {
            "rule_id": "S3-004",
            "matched": false
          },
          {
            "rule_id": "S3-005",
            "matched": false
          },
          {
            "rule_id": "S3-006",
            "matched": false
          },
          {
            "rule_id": "S3-007",
            "matched": false
          },
          {
            "rule_id": "S3-008",
            "matched": false
          },
          {
            "rule_id": "S3-009",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S4-EX-004",
      "stage": 4,
      "description": "Blocking emitted state while reducer returns rollback residue",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MISMATCH",
        "raw_artifact_schema_state": "INVALID",
        "raw_result_state": "INVALID_LITERAL",
        "raw_branch_consistency_state": "UNAVAILABLE",
        "rollback_state": "ROLLBACK_FAILED_RESIDUE_PRESENT",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "emitted_closure_state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
      "expected": {
        "result": "POST_REDUCTION_REJECTED",
        "typed_stop": "STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH",
        "expected_closure_state": "CLOSURE_ROLLBACK_RESIDUE_PRESENT",
        "emitted_closure_state": "CLOSURE_VALID_RAW_BLOCKING_REPORTED",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": true
          }
        ]
      }
    },
    {
      "example_id": "S4-C03-EX-005",
      "stage": 4,
      "description": "Complete-looking emitted state cannot override rollback NOT_ATTEMPTED residue-present classification",
      "normalized_inputs": {
        "execution_attempt_state": "EXACTLY_ONE",
        "process_launch_state": "LAUNCHED",
        "process_exit_state": "EXIT_OBSERVED",
        "process_exit_code": 0,
        "output_creation_state": "PARTIAL_CREATED",
        "output_commit_state": "COMMIT_FAILED",
        "raw_artifact_presence": "PRESENT",
        "raw_artifact_identity_state": "MATCH",
        "raw_artifact_schema_state": "VALID",
        "raw_result_state": "COMPLETE",
        "raw_branch_consistency_state": "CONSISTENT",
        "rollback_state": "NOT_ATTEMPTED",
        "authorization_valid_at_start": "VALID",
        "authorization_valid_at_completion": "VALID",
        "authorization_consumption_state": "CONSUMED"
      },
      "emitted_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
      "expected": {
        "result": "POST_REDUCTION_REJECTED",
        "typed_stop": "STOP_CLOSURE_REDUCER_OUTPUT_MISMATCH",
        "expected_closure_state": "CLOSURE_ROLLBACK_NOT_ATTEMPTED_RESIDUE_PRESENT",
        "emitted_closure_state": "CLOSURE_VALID_RAW_COMPLETE_REPORTED",
        "reducer_trace": [
          {
            "rule_id": "S3-001",
            "matched": false
          },
          {
            "rule_id": "S3-002",
            "matched": false
          },
          {
            "rule_id": "S3-003",
            "matched": true
          }
        ]
      }
    }
  ]
}
```

## 13. Acceptance boundary

This paper defines factual parsing, validation, reduction, and emitted-state conformance only. It does not define which state is accepted, which state permits registered-evidence transformation, which state permits K199, or any downstream authorization effect. Every closure state has `acceptance_effect = NONE`.

## 14. Acceptance evidence for Sentinel review

| Evidence | Result |
|---|---|
| Canonical base compare | `identical; ahead 0; behind 0` |
| Blocked Candidate-02 identity | `296608 / eb6df0ff290e8c30a7f52a5f66cf11bed3be17dacc39eea01b6ed8b156d7858d; sidecar matched` |
| Normalized field count | `15` |
| Stage-1 group count | `4` |
| Stage-1 rule count | `14` |
| Stage-1 dependency-rule count | `8` |
| Stage-2 rule count | `49` |
| Closure-state count | `31` |
| Stage-3 reducer-rule count | `33` |
| Stage-4 conformance-rule count | `2` |
| Example-vector count | `137` |
| Closure-state example coverage | `100%` |
| Stage-2 rule target coverage | `100%` |
| Non-NONE acceptance effects | `0` |

## 15. Authorization statement

Preparation of this working paper and detached digest has authorization effect `NONE`. No Candidate 10, Working Paper 02, registry overlay, governance replacement, manifest, checksum inventory, ZIP, sealed script, installation, Skill invocation, discovery, execution, implementation, K015/K016/K199/K200/K201/K202 materialization, test, import, data access, network access, subprocess, Git activity, empirical work, P1/P2/P3, scoring, probe, trading, or gate change is authorized or performed.

Requested Sentinel review: EXECUTION_CLOSURE_STATE_MACHINE_WORKING_PAPER_CANDIDATE_03