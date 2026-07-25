# Checkpoint REV23_FINDING4_I0A_R1_CP_0001_FCF406C4

## Identity

- intended executable target:
  `pm_research/local_curl_per_side/prepared_evidence.py`
- evidence-only payload:
  `payload_exact/pm_research/local_curl_per_side/prepared_evidence.py`
- SHA-256:
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes
- preservation: `CANONICALLY_PRESERVED`
- acceptance: `NOT_ACCEPTED`
- authorization effect: `NONE`
- conformance: `REVISION10_STATIC_CONFORMANCE_BLOCKED`

## Read order

1. `CHECKPOINT_MANIFEST.json`
2. `BASELINE_AND_LINEAGE.md`
3. `ACTIVITY_BOUNDARY_STATUS.md`
4. `KNOWN_FINDINGS.md`
5. `SENTINEL_INSTALLATION_VERIFICATION.md`
6. `SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md`
7. `SHA256SUMS.txt`
8. the exact payload only when static source inspection is required

## Static review result

The payload is useful historical Revision 09 progress but fails the installed
Revision 10 contract. The decisive failures are recorded in
`SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md`.

T107 and T153 are resolved as specification-layer matters. The following
provenance gaps remain open:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

## Preservation rule

The exact payload is not replaced, restored to the executable path, overwritten,
promoted, or selected as a continuation start by this record.

No implementation starting SHA is selected.

## Non-authorization

This checkpoint and its review authorize no implementation, source/test edit,
test execution, rollback, restoration, overwrite, promotion, project execution,
data/network access, artifact production, Git write by Claude, R2, P1/P2/P3,
scoring, probe execution, or gate change.
