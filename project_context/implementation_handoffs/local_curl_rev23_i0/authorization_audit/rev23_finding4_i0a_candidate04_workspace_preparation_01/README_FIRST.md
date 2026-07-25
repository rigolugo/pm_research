# Candidate 04 Workspace Preparation — Read First

## Status

`ACCEPTED DOCUMENTATION PACKAGE — CANONICAL INSTALLATION PENDING SENTINEL VERIFICATION — EXECUTION NOT AUTHORIZED`

## Identity

- package: `REV23_FINDING4_I0A_CANDIDATE04_WORKSPACE_PREPARATION_PACKAGE_CANDIDATE_02`;
- Sentinel decision: `APPROVE — CANDIDATE_04_WORKSPACE_PREPARATION_PACKAGE_CANDIDATE_02_ACCEPTED`;
- submitted ZIP SHA-256: `77c70fec832b97f2d2b78c9fb7886f1fe8f3b1aa03739a73a6213684d8c89601`;
- submitted ZIP size: `13495` bytes;
- submitted archive members: `9`;
- accepted payload documentation files: `8`;
- canonical installation base: `689e546e588d557c96f28bc722c3f159d635f2c1`;
- proposed exact Windows staging root: `C:\b1\rev23_candidate04_source_workspace_01`;
- Candidate 01 status: `BLOCKED_NOT_ACCEPTED_NON_CONTROLLING`.

## Current authority

Gustavo authorized preparation of the documentation-only canonical installation package. This authorization does not authorize workspace creation, archive extraction, file copying, permission changes, workspace verification execution, source/test authoring, tests, project execution, data/network activity, or Git writes by Claude.

Canonical installation of this package does not execute `WORKSPACE_PREPARATION`. A future run still requires a distinct Gustavo `WORKSPACE_PREPARATION_ONLY` authorization and an active Sentinel handoff naming the exact installed package, canonical HEAD, staging root, capture identity, and result contract.

## Read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `ACCEPTED_WORKSPACE_PREPARATION_PACKAGE_MANIFEST.json`
3. `accepted_candidate_02/README_FIRST.md`
4. `accepted_candidate_02/GUSTAVO_PACKAGE_AUTHORING_AUTHORIZATION.md`
5. `accepted_candidate_02/WORKSPACE_PREPARATION_CONTRACT.md`
6. `accepted_candidate_02/WORKFLOW_RECORD_CONTRACT.md`
7. `accepted_candidate_02/ACTIVITY_BOUNDARIES.md`
8. `accepted_candidate_02/CENTRAL_DOCUMENT_REPLACEMENTS.md`
9. `accepted_candidate_02/SENTINEL_REVIEW_HANDOFF.md`
10. `accepted_candidate_02/PACKAGE_MANIFEST.json`
11. `accepted_candidate_02/SHA256SUMS.txt`
12. `SHA256SUMS.txt`

## Controlling stage

Candidate 04 remains the controlling specification. The current workflow state is:

`C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED`

This package defines the exact future transition:

`C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED` → `WORKSPACE_PREPARATION` → `C04_SOURCE_WORKSPACE_READY`

The transition occurs only after a separately authorized run produces a valid record and Sentinel accepts that result. Package acceptance and installation do not change the workflow state.

## Non-authorization

- workspace execution authorization: `NONE`;
- active workspace-execution handoff: `NONE`;
- source authoring authorization: `NONE`;
- test-source authoring and test execution: unauthorized;
- implementation starting commit: `NOT_SELECTED`;
- active Claude implementation prompt: `false`;
- local commit, push, merge, remote write, P1/P2/P3, scoring, probe, and gate changes: unauthorized.
