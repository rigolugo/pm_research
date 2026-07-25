# Implementation Checkpoints — Read First

This directory preserves exact implementation progress as evidence without
promoting it into the executable source tree.

## Current checkpoint

- ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- exact payload SHA-256:
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes
- preservation: `CANONICALLY_PRESERVED`
- installation: `INSTALLED_AND_SENTINEL_VERIFIED`
- acceptance: `NOT_ACCEPTED`
- authorization effect: `NONE`
- conformance: `REVISION10_STATIC_CONFORMANCE_BLOCKED`

## Required read order

1. `CHECKPOINT_INDEX.json`
2. `LATEST_PRESERVED_CHECKPOINT.json`
3. `LATEST_ACCEPTED_CHECKPOINT.json`
4. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/README_FIRST.md`
5. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/CHECKPOINT_MANIFEST.json`
6. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/BASELINE_AND_LINEAGE.md`
7. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/ACTIVITY_BOUNDARY_STATUS.md`
8. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/KNOWN_FINDINGS.md`
9. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_INSTALLATION_VERIFICATION.md`
10. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md`
11. `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SHA256SUMS.txt`

## Controlling interpretation

Revision 10 resolves the former T107 and T153 specification-layer blockers. The
static checkpoint review is nevertheless blocked because the checkpoint does not
materialize mandatory Revision 10 source and behavioral changes.

The two remaining provenance gaps are open and separately labeled. They do not
soften or replace the verified static-conformance failure.

## Non-authorization

Checkpoint preservation and review do not authorize restoration, overwrite,
promotion, continuation, implementation, source/test edits, tests, execution,
data/network access, artifact production, Git writes by Claude, R2, P1/P2/P3,
scoring, probe execution, or gate changes.
