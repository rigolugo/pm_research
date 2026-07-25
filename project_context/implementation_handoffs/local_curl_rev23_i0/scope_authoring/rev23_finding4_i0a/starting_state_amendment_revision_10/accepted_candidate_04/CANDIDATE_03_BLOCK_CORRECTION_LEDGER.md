# Candidate 03 Sentinel-Block Correction Ledger

## Status

`CANDIDATE 04 REVIEW EVIDENCE — SPEC ONLY — AUTHORIZATION EFFECT NONE`

Candidate 03 remains blocked, unaccepted, non-controlling, and unsuitable as an implementation contract.

Candidate 04 preserves Candidate 03's architecture and corrects exactly two submitted Sentinel block defects.

| Block defect | Candidate 03 defect | Candidate 04 correction | Primary evidence |
|---|---|---|---|
| Closed typed record schemas | Candidate 03 described halt and success records but did not provide complete closed schemas or a complete normative equivalent. | Adds two closed Draft 2020-12 JSON Schemas with exact types, required fields, enums/consts, nullability, integer ranges, SHA/timestamp/path grammars, ordered arrays, closed expected/observed evidence, and normative stage-row cross-field validation. | `WORKFLOW_HALT_RECORD.schema.json`; `WORKFLOW_SUCCESS_RECORD.schema.json`; `WORKFLOW_RECORD_CROSS_FIELD_RULES.md` |
| Commit/review/push/remote separation | Candidate 03 combined local materialization commit creation and later installation verification without separately representing local commit review, separate push authorization, exact push gate, non-force push, and remote verification. | Replaces each source/test materialization delivery with five distinct stages. Push is never implied by commit authorization or Sentinel local-commit approval. Remote advancement halts without push or repair. | `DELIVERY_COMMIT_PUSH_REMOTE_BOUNDARIES.md`; `WORKFLOW_DOMAIN.json`; `WORKFLOW_DOMAIN.md` |

## Preserved Candidate 03 architecture

Candidate 04 preserves without redesign:

- exact accepted-scope supersession text and retained `C03_*` semantic provision IDs;
- exact twelve path, size, and SHA-256 rows;
- eleven baseline matches and one checkpoint-modified start;
- isolated non-Git Windows workspace;
- three writable source paths and nine protected source-stage paths;
- four writable test paths and eight protected test-stage paths;
- five baseline-support edit prohibitions;
- separate source/test authoring and materialization;
- failed-gate non-repair;
- open `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- authorization effect `NONE`.

## Workflow count change

Candidate 03:

- states: `15`;
- stages: `14`;
- stop codes: `48`;
- success codes: `14`;
- predicates: `146`.

Candidate 04:

- states: `21`;
- stages: `20`;
- stop codes: `70`;
- success codes: `20`;
- predicates: `205`.

The increase is limited to schema review closure and the two five-stage source/test delivery sequences.
