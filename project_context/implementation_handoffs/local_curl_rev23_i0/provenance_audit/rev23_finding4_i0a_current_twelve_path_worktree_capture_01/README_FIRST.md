# Current Twelve-Path Worktree Capture — Read First

## Status

- capture ID: `REV23_FINDING4_I0A_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_01`;
- Sentinel decision: `ACCEPT FINDING — CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`;
- source artifact: `REV23_FINDING4_I0A_PROVENANCE_CAPTURE.zip`;
- source artifact SHA-256: `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`;
- source artifact size: `487764` bytes;
- source artifact members: `17`;
- captured source/test payload paths: `12`;
- missing captured paths: `0`;
- unresolved-provenance labels inside the capture: `0`;
- canonical installation base: `71061065d91fc391e934d7e79a29eefc898cfe82`;
- canonical installation verification: `PENDING_SENTINEL_VERIFICATION`.

## Decision boundary

This record accepts the uploaded archive as a sufficient independent read-only capture of the exact twelve-path Claude worktree state. It closes only:

`CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`

It does not accept implementation conformance, the preserved checkpoint, any historical corrective round, or any executable-source materialization. It does not select implementation starting bytes and does not activate the conditional Revision 10 source authorization.

`MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE` remains open.

## Required read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `PROVENANCE_CAPTURE_MANIFEST.json`
3. `SOURCE_ARTIFACT_IDENTITY.md`
4. `CAPTURED_GIT_STATE.txt`
5. `CAPTURED_FILE_INVENTORY.json`
6. `CAPTURED_TWELVE_PATH_SHA256SUMS.txt`
7. `CAPTURED_PACKAGE_MANIFEST.json`
8. `CAPTURED_PROVENANCE_NOTES.md`
9. `ACTIVITY_BOUNDARIES.md`
10. `SENTINEL_INSTALLATION_SCOPE.md`
11. `SHA256SUMS.txt`
12. `evidence_exact/REV23_FINDING4_I0A_PROVENANCE_CAPTURE.zip`

## Accepted observed composition

- eleven paths are byte-identical to the historical twelve-path baseline manifest;
- `pm_research/local_curl_per_side/prepared_evidence.py` is checkpoint-modified at SHA-256 `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`, size `112338` bytes;
- all twelve paths were untracked at detached local HEAD `1e1afb29791f42c286b45d3b576f74926add8dce`;
- requested canonical commit `71061065d91fc391e934d7e79a29eefc898cfe82` was not present in Claude's local object store, and the capture did not move HEAD;
- the original `prepared_evidence.py` R1 baseline bytes for SHA-256 `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` were not found in the captured local tree.

## Non-authorization

This record authorizes no source/test edit, materialization, restoration, checkpoint promotion, test execution, import, compilation, lint, typing, coverage, project execution, data/network access, artifact production beyond this documentation package, Git write by Claude, R2, P1/P2/P3, scoring, probe execution, or gate change.
