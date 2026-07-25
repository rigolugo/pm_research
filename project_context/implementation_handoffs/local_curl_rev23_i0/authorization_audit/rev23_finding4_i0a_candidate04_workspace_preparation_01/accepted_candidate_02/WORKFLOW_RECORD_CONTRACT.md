# Workflow Success and Halt Record Contract

## Controlling identities

The future workspace-preparation run MUST emit exactly one record:

- first predicate failure: a halt record conforming to
  `WORKFLOW_HALT_RECORD.schema.json`, SHA-256
  `6b73d32258c90173a3164e107d1b91a09ac30faa12b81327dadf4a1b5855a2f2`;
- all 18 predicates true: a success record conforming to
  `WORKFLOW_SUCCESS_RECORD.schema.json`, SHA-256
  `688b32a1635d9562c28a618b5f4b8d1fd3492469d0048c95d93ac0e35b58cb88`.

Every record MUST additionally satisfy:

- `WORKFLOW_DOMAIN.json`, SHA-256
  `ea08b160f77670807b4190df276e57be9917261be434370cb1d9fd1077dead8c`;
- `WORKFLOW_RECORD_CROSS_FIELD_RULES.md`, SHA-256
  `7df2c220f53cdc95fd8f0efd6a5b7aa55a25ad1cfd67f8b7c85e999e7ec69a6d`.

All paths are relative to the accepted Candidate 04 directory identified in
`README_FIRST.md`.

## Halt record

The record MUST select stage `WORKSPACE_PREPARATION`, the exact failed
predicate ID and ordinal, and the exact applicability-row stop code, decision
owner, retry eligibility, and retry owner. It MUST use authorization effect
`NONE`, bind expected and observed evidence exactly as required by the accepted
schema and cross-field rules, compute exact affected paths, and compute
`evidence_sha256` using the accepted RFC 8785 projection.

Only the first failed predicate is recorded. No later predicate is evaluated.
An invalid record changes no state and authorizes no retry or repair.

## Success record

The record MUST contain:

- `schema_id`: `rev10_candidate04_workflow_success.v1`
- `record_kind`: `SUCCESS`
- `stage`: `WORKSPACE_PREPARATION`
- `from_state`: `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED`
- `to_state`: `C04_SOURCE_WORKSPACE_READY`
- `success_code`: `CLEAR_C04_SOURCE_WORKSPACE_PREPARED`
- `predicate_count`: `18`
- `completed_predicate_ids`: the exact 18 IDs in accepted predicate order
- `decision_owner`: `SENTINEL`
- `authorization_effect`: `NONE`
- `affected_paths`: the exact accepted twelve paths in accepted ordering
- `authoring_started`: `false`
- `git_write_observed`: `false`
- `execution_activity_observed`: `false`

Expected/observed evidence, timestamps, ordering, unique keys, nullability, and
`evidence_sha256` MUST satisfy the accepted schema and cross-field rules
exactly. This package does not invent a sample record or a new record field.
