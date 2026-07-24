# Sentinel Scope Acceptance Decision — REV23 Finding 4 I0A Revision 10

Decision: **APPROVE**

## Accepted scope identity

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- accepted base: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- accepted submission: `REV23_FINDING4_I0A_SCOPE_REVISION_10_CANDIDATE_11.zip`
- accepted submission SHA-256: `8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`
- accepted member count: `15`
- Sentinel acceptance date: `2026-07-24`
- canonical review and installation base: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`
- proposed immutable canonical copy: `accepted_scope_revision_10/`
- preserved implementation checkpoint: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- preserved payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`

The 15-member `accepted_scope_revision_10/` directory is an exact member-for-member copy of the accepted Candidate 11 archive. The inner files retain their submitted `NOT_ACCEPTED` wording as immutable submission evidence; this outer Sentinel decision supplies canonical specification acceptance. Their non-authorization clauses remain controlling.

## Decision basis

Revision 10 resolves the material contract contradictions discovered after Revision 09 while preserving the closed twelve-path boundary:

- T107 now reaches `ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH` through a grammar-valid partition descriptor whose first remaining fault is the same-ordinal descriptor/claim partition mismatch;
- T153 now reaches `ERR_CANONICAL_TARGET_DUPLICATE` through two individually grammar-valid partition descriptors that intentionally share one canonical target;
- public-function result inventories are closed, internally consistent, and disjoint across included and excluded codes;
- T166–T230, the 169-ID resolved fixture namespace, 23 caller–callee edges, assurances, precedence, typed seams, and hash contracts close without unresolved references or fixture collisions;
- the exact twelve-path future-impact matrix is identical across all eight declared representations;
- the historical Revision 09 start `8b8e9320...` is separated from the canonically preserved but unaccepted `fcf406c4...` checkpoint; and
- Revision 10 selects no implementation starting SHA and creates no rollback, restore, overwrite, promotion, or continuation instruction.

## Supersession boundary

Revision 10 supersedes Revision 09 for the complete Finding 4 I0A specification surface materialized in the accepted package. Revision 09 and Revision 08 remain immutable historical accepted evidence. The Revision 09 R1 authorization and its source gate do not carry forward to Revision 10.

The preserved checkpoint remains evidence only:

- preservation state: `CANONICALLY_PRESERVED`;
- acceptance state: `NOT_ACCEPTED`;
- authorization effect: `NONE`;
- controlling implementation: `false`;
- Revision 10 implementation starting point: `NOT_AUTHORIZED_AND_NOT_YET_SELECTED`.

## File and authorization boundary

The accepted future-impact inventory remains exactly twelve source/test paths. It is planning evidence only. Scope acceptance does not activate any path and does not authorize implementation.

No Revision 10 implementation authorization is active. The completed Revision 09 R1 one-file source-resume record is historical evidence and cannot be reused as authority for another edit.

Still unauthorized:

- source synchronization or source/test authoring;
- rollback, restoration, overwrite, or checkpoint promotion;
- test discovery, collection, or execution;
- project imports or execution;
- compilation, lint, typing, coverage, or CI;
- research-data or empirical-artifact access;
- API, RPC, curl, Dune, vendor, or general network activity;
- Claude Git writes;
- R2, P1, P2, P3, scoring, probe execution, or gate changes.

## Canonical installation boundary

This decision is included in a documentation-only installation package based on `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`. Revision 10 becomes the verified canonical controlling scope only after Gustavo manually commits the exact package and Sentinel verifies the resulting commit, exact member bytes, checksums, path boundary, preservation of historical scopes and the `fcf406c4...` payload, and absence of live source/test changes.

## Next boundary

1. Gustavo manually installs and commits only the exact documented files.
2. Gustavo returns the full commit SHA to Sentinel.
3. Sentinel verifies the installation commit.
4. Any implementation-start selection, source/test authoring, or test execution requires a later separate specification-conformance decision, Gustavo authorization, and Sentinel handoff.
