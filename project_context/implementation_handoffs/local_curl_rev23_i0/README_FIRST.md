# Local Curl REV23 I0 — Read First

## Current controlling state

- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- specification installation: `INSTALLED_AND_SENTINEL_VERIFIED`;
- specification installation commit: `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`;
- preserved-checkpoint static-conformance decision: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`;
- accepted remediation scope: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- remediation-scope Sentinel decision: `APPROVE — REV10_LOCAL_CURL_REMEDIATION_SCOPE_ACCEPTED`;
- remediation candidate ZIP SHA-256: `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`;
- remediation installation base: `cc2964840d197a40d1c4ef567b42eda762c0be0a`;
- remediation installation state after this package is committed: `INSTALLED_PENDING_SENTINEL_VERIFICATION`;
- implementation authorization: `NONE`;
- implementation starting SHA: `NOT_AUTHORIZED_AND_NOT_SELECTED`.

The preserved `fcf406c4...` checkpoint remains exact, recoverable, evidence-only, `NOT_ACCEPTED`, non-controlling, and authorization effect `NONE`.

## Required read order

1. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
2. `SENTINEL_ACCEPTANCE_DECISION.md`
3. `scope_authoring/rev23_finding4_i0a/README_FIRST.md`
4. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
5. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_INSTALLATION_VERIFICATION_REVISION_10.md`
6. `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json`
7. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_10/README_FIRST.md`
8. the complete Revision 10 read order declared there
9. `implementation_checkpoints/README_FIRST.md`
10. `implementation_checkpoints/CHECKPOINT_INDEX.json`
11. `implementation_checkpoints/LATEST_PRESERVED_CHECKPOINT.json`
12. `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/README_FIRST.md`
13. `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/CHECKPOINT_MANIFEST.json`
14. `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md`
15. `remediation_scope/README_FIRST.md`
16. `remediation_scope/SENTINEL_ACCEPTANCE_DECISION.md`
17. `remediation_scope/SENTINEL_INSTALLATION_AUTHORIZATION.md`
18. `remediation_scope/ACCEPTED_REMEDIATION_SCOPE_MANIFEST.json`
19. the complete remediation-scope read order declared in `remediation_scope/README_FIRST.md`
20. `HANDOFF_INVENTORY.md`
21. `HANDOFF_REVISION_10_STATIC_CONFORMANCE_SHA256SUMS.txt`

## Checkpoint finding

The checkpoint preserves only `pm_research/local_curl_per_side/prepared_evidence.py`, while Revision 10 requires mandatory source changes in `canonical.py`, `finding4_registry.py`, and `prepared_evidence.py`. The observed payload also retains superseded result mappings, path parsing, private reducer ownership, selected-payload ordering, and unit-wrapper bypass behavior.

T107 and T153 are resolved at the specification layer. Two provenance gaps remain open:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

Those gaps are separate from the verified implementation-conformance block.

## Accepted remediation scope

The accepted remediation scope defines a future atomic three-source implementation candidate and a separately gated four-test-source candidate. It closes no implementation defect by itself and does not unblock execution.

No implementation starting SHA is selected. No historical authorization carries forward. No Claude implementation prompt is active.

## Non-authorization

No implementation, source/test edit, test execution, rollback, restoration, overwrite, promotion, project execution, data/network access, subprocess, artifact production, Git write by Claude, R2, P1/P2/P3, scoring, probe execution, or gate change is authorized.

The only permitted immediate action from this package is Gustavo's manual documentation installation at exact base `cc2964840d197a40d1c4ef567b42eda762c0be0a`, followed by Sentinel verification of the resulting commit.
