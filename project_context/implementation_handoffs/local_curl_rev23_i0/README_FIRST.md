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
- remediation installation state: `INSTALLED_AND_SENTINEL_VERIFIED`;
- remediation installation commit: `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`;
- conditional source-authorization package: `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`;
- authorization-package installation commit: `71061065d91fc391e934d7e79a29eefc898cfe82`;
- authorization package status: `INSTALLED_AND_SENTINEL_VERIFIED_BUT_NOT_ACTIVATED`;
- installed source-gate result: `STOP_REV10_REMEDIATION_SOURCE_GATE_FAILED`;
- accepted worktree-capture finding: `ACCEPT FINDING — CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`;
- worktree-capture source ZIP SHA-256: `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`;
- worktree-capture installation verification: `INSTALLED_AND_SENTINEL_VERIFIED`;
- worktree-capture installation commit: `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`;
- active implementation authorization: `NONE`;
- active source-gated commit: `NOT_SELECTED`.

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
18. `remediation_scope/SENTINEL_INSTALLATION_VERIFICATION.md`
19. `remediation_scope/ACCEPTED_REMEDIATION_SCOPE_MANIFEST.json`
20. the complete remediation-scope read order declared in `remediation_scope/README_FIRST.md`
21. `provenance_audit/rev23_finding4_i0a_current_twelve_path_worktree_capture_01/README_FIRST.md`
22. `provenance_audit/rev23_finding4_i0a_current_twelve_path_worktree_capture_01/SENTINEL_INSTALLATION_VERIFICATION.md`
23. the complete provenance-capture read order declared there
24. `authorization_audit/rev23_finding4_i0a_revision10_remediation_source_01/README_FIRST.md`
25. the complete authorization-package read order declared there
26. `HANDOFF_INVENTORY.md`
27. `HANDOFF_REVISION_10_STATIC_CONFORMANCE_SHA256SUMS.txt`
28. `HANDOFF_REVISION_10_REMEDIATION_SCOPE_SHA256SUMS.txt`
29. `HANDOFF_REVISION_10_REMEDIATION_SOURCE_AUTHORIZATION_SHA256SUMS.txt`
30. `HANDOFF_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_SHA256SUMS.txt`
31. `HANDOFF_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_VERIFICATION_SHA256SUMS.txt`

## Checkpoint and provenance findings

The checkpoint preserves only `pm_research/local_curl_per_side/prepared_evidence.py`, while Revision 10 requires mandatory source changes in `canonical.py`, `finding4_registry.py`, and `prepared_evidence.py`. The observed checkpoint payload retains superseded result mappings, path parsing, private reducer ownership, selected-payload ordering, and unit-wrapper bypass behavior.

T107 and T153 are resolved at the specification layer.

The independently reviewed twelve-path provenance capture closes:

`CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`

It preserves eleven baseline-matching files and checkpoint-modified `prepared_evidence.py` as untracked workspace evidence. It does not accept or promote those bytes.

The following provenance gap remains open:

`MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`

That gap is separate from the verified implementation-conformance block.

## Accepted remediation scope

The accepted remediation scope defines a future atomic three-source implementation candidate and a separately gated four-test-source candidate. It closes no implementation defect by itself and does not unblock execution.

Conditional package `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01` was installed and Sentinel-verified at `71061065d91fc391e934d7e79a29eefc898cfe82`, but its canonical-worktree source gate failed because the expected live twelve-path tree was absent. The accepted provenance capture records Claude's separate untracked workspace; it does not satisfy or activate that failed gate. No historical authorization carries forward and no active Claude implementation prompt exists.

## Non-authorization

No implementation, source/test edit, test execution, rollback, restoration, overwrite, promotion, project execution, data/network access, subprocess, artifact production outside this documentation/evidence package, Git write by Claude, R2, P1/P2/P3, scoring, probe execution, or gate change is authorized.

The current permitted next action is SPEC-ONLY Professor finalization of Candidate 02 using the accepted and verified capture finding at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`. No source edit is permitted before a separately accepted amendment, Gustavo authorization, and active Sentinel handoff.
