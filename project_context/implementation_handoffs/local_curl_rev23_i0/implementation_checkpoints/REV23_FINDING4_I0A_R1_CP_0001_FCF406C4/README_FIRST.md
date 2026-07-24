# REV23_FINDING4_I0A_R1_CP_0001_FCF406C4

## Status

- authority class: `EVIDENCE_ONLY`
- preservation state: `CANONICALLY_PRESERVED`
- canonical installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- verified checkpoint installation commit: `58acbac493840c45d84c6b7e33c583d722f4d559`
- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- controlling specification installation commit: `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- conformance state: `BLOCKED_PENDING_PROVENANCE_AND_REVISION10_IMPLEMENTATION_CONFORMANCE_REVIEW`
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`

This checkpoint preserves the exact recovered implementation bytes. It is not the
live source path and must not be treated as accepted, executable, or selected as
a Revision 10 implementation start.

## Exact payload

- evidence path:
  `payload_exact/pm_research/local_curl_per_side/prepared_evidence.py`
- intended executable target:
  `pm_research/local_curl_per_side/prepared_evidence.py`
- SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes

## Governing context

Revision 10 resolves the former T107, T153, and Candidate 09 specification-layer
blockers. Historical Revision 09 R1 authorization identity and source-gate fields
remain provenance only and are not reusable under Revision 10.

## Remaining review boundary

Implementation acceptance remains blocked on:

- incomplete multi-round activity lineage;
- absence of an independently captured current twelve-path worktree inventory;
- static implementation-conformance review against installed Revision 10.

Read the existing checkpoint installation verification for byte-preservation
history and the Revision 10 scope installation verification for current contract
status. No rollback, promotion, additional edit, test, execution, or downstream
stage is authorized by this checkpoint.
