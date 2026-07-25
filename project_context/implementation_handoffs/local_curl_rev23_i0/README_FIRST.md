# Local Curl REV23 I0 — Read First

## Current controlling state

- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- scope installation: `INSTALLED_AND_SENTINEL_VERIFIED`
- scope installation commit: `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- checkpoint static-conformance decision:
  `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`
- static review base: `3cf0871ae97d112324031190822756379d1236e8`
- implementation authorization: `NONE`
- implementation starting SHA: `NOT_AUTHORIZED_AND_NOT_SELECTED`

The preserved checkpoint remains exact, recoverable, evidence-only,
`NOT_ACCEPTED`, non-controlling, and authorization effect `NONE`.

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
15. `HANDOFF_INVENTORY.md`
16. `HANDOFF_REVISION_10_STATIC_CONFORMANCE_SHA256SUMS.txt`

## Checkpoint finding

The checkpoint preserves only
`pm_research/local_curl_per_side/prepared_evidence.py`, while Revision 10
requires mandatory source changes in `canonical.py`, `finding4_registry.py`, and
`prepared_evidence.py`. The observed payload also retains superseded result
mappings, path parsing, private reducer ownership, selected-payload ordering, and
unit-wrapper bypass behavior.

T107 and T153 are resolved at the specification layer. Two provenance gaps
remain open:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

Those gaps are separate from the verified implementation-conformance block.

## Non-authorization

No implementation, source/test edit, test execution, rollback, restoration,
overwrite, promotion, project execution, data/network access, subprocess,
artifact production, Git write by Claude, R2, P1/P2/P3, scoring, probe
execution, or gate change is authorized.

The only permitted immediate action from this package is Gustavo's manual
installation of the documentation-only canonical review record at the exact
base stated above, followed by Sentinel installation verification.
