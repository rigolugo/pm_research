# Revision 10 Remediation Source Authorization — Read First

## Status

- authorization ID: `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`;
- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- accepted remediation scope: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- canonical package-preparation base: `a4fb0e64056b58a229da481664e4234e3215cd91`;
- Gustavo source-authoring authorization: **GRANTED** on `2026-07-24`;
- Sentinel package decision: `APPROVE — REV10_REMEDIATION_SOURCE_AUTHORIZATION_PACKAGE_ACCEPTED`;
- package installation state: `NOT_YET_INSTALLED`;
- activation state: `PENDING_CANONICAL_INSTALLATION_AND_LOCAL_SOURCE_GATE`;
- source-authoring paths after activation: exactly `3`;
- allowed new repository files during implementation: `NONE`;
- test-source authoring: **UNAUTHORIZED**;
- test execution: **UNAUTHORIZED**;
- project execution and research-data/network access: **UNAUTHORIZED**.

This package is conditional. It does not authorize Claude to edit source until Sentinel verifies the canonical documentation-installation commit and separately accepts a local source-gate report proving the exact twelve-path starting state.

## Read order

1. `GUSTAVO_AUTHORIZATION_RECORD.md`
2. `SENTINEL_IMPLEMENTATION_AUTHORIZATION.md`
3. `AUTHORIZATION_MANIFEST.json`
4. `AUTHORIZED_FILE_MATRIX.md`
5. `ACTIVITY_BOUNDARIES.md`
6. `SOURCE_GATE.md`
7. `TWELVE_PATH_STARTING_SHA256SUMS.txt`
8. `IMPLEMENTATION_REVIEW_DELIVERABLES.md`
9. `CLAUDE_HANDOFF_INACTIVE.md`
10. `SHA256SUMS.txt`

Then read the complete accepted Revision 10 and remediation-scope read orders.

## No checkpoint promotion

The preserved checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` remains `NOT_ACCEPTED`, non-controlling, and authorization effect `NONE`. Its `fcf406c4...` bytes must not be restored, copied, promoted, or used as the starting version of `prepared_evidence.py`.
