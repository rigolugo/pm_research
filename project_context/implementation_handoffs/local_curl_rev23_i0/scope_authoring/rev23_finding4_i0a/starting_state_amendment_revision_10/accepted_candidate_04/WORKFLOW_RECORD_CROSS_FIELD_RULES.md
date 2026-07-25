# Workflow Record Cross-Field Validation Rules — Candidate 04

## 1. Status

`NORMATIVE SPECIFICATION CONTRACT — NOT ACCEPTED — AUTHORIZATION EFFECT NONE`

The two Draft 2020-12 JSON Schemas close structural typing. This document closes the relationships that ordinary JSON Schema cannot express compactly, including stage-row lookup, exact predicate applicability, exact transition lookup, lexicographic ordering, unique Fact keys, and evidence-hash computation.

A record is valid only when it passes both its JSON Schema and every applicable rule below.

## 2. Validation order

1. Parse the submitted bytes as UTF-8 JSON. Duplicate object member names are invalid.
2. Select the schema by exact `schema_id` and `record_kind`.
3. Validate against the complete matching Draft 2020-12 schema.
4. Enforce every `x-ordering` and `x-uniqueBy` annotation as normative.
5. Look up the exact stage and applicability or transition row in `WORKFLOW_DOMAIN.json`.
6. Apply the halt or success cross-field rules.
7. Recompute `evidence_sha256`.
8. Accept the record only if every check succeeds.

No normalization, sorting, coercion, default insertion, case folding, path rewriting, field deletion, or in-place repair is permitted.

## 3. Normative ordering

- Fact arrays: ascending by `key` using Unicode code-point order; keys are unique.
- Repository-relative path arrays: ascending by the UTF-8 byte sequence of the complete path; values are unique.
- `STRING_ARRAY`: ascending Unicode code-point order; values are unique.
- `INTEGER_ARRAY`: numeric ascending; values are unique.
- `completed_predicate_ids`: exact stage predicate order by ascending `predicate_ordinal`; not general lexicographic order.

An array with the correct members in the wrong order is invalid.

## 4. Halt-record validation

For a record with `record_kind = HALT`:

1. `stage` MUST select exactly one `stage_specs` member.
2. The pair `(predicate_id, predicate_ordinal)` MUST select exactly one predicate in that stage.
3. `stop_code`, `decision_owner`, `retry_eligibility`, and `retry_owner` MUST exactly equal the selected applicability row.
4. `authorization_effect` MUST be `NONE`.
5. For the first state predicate:
   - `predicate_ordinal` MUST be `1`;
   - `stop_code` MUST be `STOP_C04_STAGE_STATE_MISMATCH`;
   - `state` MUST be a closed `WorkflowState` different from the stage `from_state`.
6. For every other predicate, `state` MUST equal the stage `from_state`.
7. `expected.condition` and `observed.condition` MUST equal the selected predicate's exact `condition_for_success`.
8. `expected.status` MUST equal `EXPECTED`.
9. `observed.status` MUST be exactly one of:
   - `FALSE`;
   - `MISSING`;
   - `MALFORMED`;
   - `AMBIGUOUS`;
   - `STALE`;
   - `CONFLICTING`.
10. `expected.facts` MUST contain these exact keys and values:
    - `condition_for_success` — `STRING`;
    - `predicate_id` — `STRING`;
    - `predicate_ordinal` — `INTEGER`;
    - `stage` — `STRING`.
11. `observed.facts` MUST contain:
    - `authoring_started` — `BOOLEAN`, equal to the top-level field;
    - `execution_activity_observed` — `BOOLEAN`, equal to the top-level field;
    - `git_write_observed` — `BOOLEAN`, equal to the top-level field;
    - `predicate_satisfied` — `BOOLEAN`, exactly `false`.
12. Additional facts MAY appear only through one of the closed Fact variants in the schema.
13. `affected_paths` MUST equal the sorted unique union of all `PATH` and `PATH_ARRAY` values in `observed.facts`.
14. Any mismatch makes the record invalid. The record MUST NOT be reinterpreted as another predicate or stop.

## 5. Success-record validation

For a record with `record_kind = SUCCESS`:

1. `stage` MUST select exactly one `stage_specs` member.
2. `from_state`, `to_state`, `success_code`, and `decision_owner` MUST equal the selected stage row.
3. `predicate_count` MUST equal the exact predicate count for the stage.
4. `completed_predicate_ids` MUST equal the exact ordered predicate-ID list for the stage.
5. `authorization_effect` MUST be `NONE`.
6. Both `expected.condition` and `observed.condition` MUST equal:

   `ALL_STAGE_PREDICATES_TRUE:<stage>`

7. `expected.status` MUST equal `EXPECTED`.
8. `observed.status` MUST equal `SATISFIED`.
9. `expected.facts` MUST contain:
   - `from_state` — `STRING`;
   - `predicate_count` — `INTEGER`;
   - `stage` — `STRING`;
   - `success_code` — `STRING`;
   - `to_state` — `STRING`.
10. `observed.facts` MUST contain:
    - `all_predicates_satisfied` — `BOOLEAN`, exactly `true`;
    - `authoring_started` — `BOOLEAN`;
    - `execution_activity_observed` — `BOOLEAN`;
    - `git_write_observed` — `BOOLEAN`.
11. The three observed booleans and the corresponding top-level booleans MUST equal the stage's exact success values.
12. `affected_paths` MUST equal the stage's exact `success_affected_paths` array.
13. Any mismatch makes the record invalid and prevents the transition.

## 6. Evidence hash

For both record kinds, construct this exact object:

```json
{
  "affected_paths": "<record affected_paths value>",
  "authoring_started": "<record boolean>",
  "execution_activity_observed": "<record boolean>",
  "expected": "<record expected object>",
  "git_write_observed": "<record boolean>",
  "observed": "<record observed object>"
}
```

Serialize it using RFC 8785 JSON Canonicalization Scheme as UTF-8 bytes. `evidence_sha256` MUST be the lowercase 64-character SHA-256 digest of those bytes.

The hash does not include `evidence_sha256`, `created_at_utc`, or the stage-selection fields.

## 7. Invalid-record effect

A schema-invalid or cross-field-invalid record:

- is neither a halt nor a success;
- changes no workflow state;
- authorizes no retry, commit, review, push, repair, or execution;
- MUST NOT be normalized or repaired in place;
- MAY be referenced by Sentinel in a separate review finding using
  `STOP_C04_RECORD_SCHEMA_INVALID` or
  `STOP_C04_RECORD_CROSS_FIELD_MISMATCH`.

## 8. Schema members

- `WORKFLOW_HALT_RECORD.schema.json`
- `WORKFLOW_SUCCESS_RECORD.schema.json`
- `WORKFLOW_DOMAIN.json`

These files are one normative record contract and MUST be reviewed together.
