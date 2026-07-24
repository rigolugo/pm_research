# REV23 Finding 4 Canonical Handoff — Revision 09 R1 Active

## Revision 09 controlling state

Revision 09 is canonically installed and Sentinel-verified at
`c4e8b1011c51272042decac4bc89e762d767a72a`. Gustavo explicitly authorized and Sentinel accepted the narrow
R1 source-resume authorization `REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

Sentinel verified the authorization-installation commit
`1e1afb29791f42c286b45d3b576f74926add8dce`, and Gustavo explicitly authorized the R1 handoff to Claude
on `2026-07-24`. The R1 one-file source stage is **ACTIVE**.

- accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- Sentinel acceptance date: `2026-07-20`
- accepted archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
- accepted member count: `14`
- verified Revision 09 installation commit: `c4e8b1011c51272042decac4bc89e762d767a72a`
- verified R1 source-gated commit: `1e1afb29791f42c286b45d3b576f74926add8dce`
- immutable installed directory: `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_09/`
- historical Revision 08 directory: unchanged
- active authorization: `REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`
- sole writable path: `pm_research/local_curl_per_side/prepared_evidence.py`
- required starting SHA-256: `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`
- test-source authoring and test execution: **NOT AUTHORIZED**

## Revision 09 read order

1. `authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/README_FIRST.md`
2. `authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/SENTINEL_ACTIVATION_VERIFICATION.md`
3. the remaining files in that authorization directory read order
4. `scope_authoring/rev23_finding4_i0a/README_FIRST.md`
5. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
6. `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json`
7. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_09/README_FIRST.md`
8. the remaining Revision 09 members in their own read order
9. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION_REVISION_08.md`
10. `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST_REVISION_08.json`
11. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_08/README_FIRST.md`
12. `scope_authoring/rev23_finding4_i0a/SCOPE_SHA256SUMS.txt`
13. `implementation_checkpoints/README_FIRST.md`
14. `implementation_checkpoints/CHECKPOINT_INDEX.json`
15. `implementation_checkpoints/LATEST_PRESERVED_CHECKPOINT.json`
16. `implementation_checkpoints/LATEST_ACCEPTED_CHECKPOINT.json`
17. `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/README_FIRST.md`
18. `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/CHECKPOINT_MANIFEST.json`
19. `HANDOFF_REVISION_09_INSTALL_SHA256SUMS.txt`
20. `HANDOFF_REVISION_09_R1_AUTHORIZATION_SHA256SUMS.txt`
21. `HANDOFF_SHA256SUMS.txt`

## Active Revision 09 R1 boundary

Claude may synchronize read-only to exact local `HEAD`
`1e1afb29791f42c286b45d3b576f74926add8dce` and edit only
`pm_research/local_curl_per_side/prepared_evidence.py`, then return one
source-only checkpoint. The source gate requires exactly twelve authorized
untracked paths, exact equality with the immutable twelve-path baseline, and no
thirteenth or other changed path. The other eleven authored paths are read-only.

The edited existing `prepared_evidence.py` is the only submitted source file.
Claude returns static reports, path inventory, diff summary, and checksums as
chat text and does not create canonical repository files. After Sentinel review,
ChatGPT may prepare an evidence-only checkpoint under `implementation_checkpoints/`
for Gustavo's manual commit. Test-source editing, tests,
project imports/execution, another source edit, implementation ZIP
reconstruction, research data, empirical work, general network/vendor activity,
Git history/remote writes, R2, and downstream phases remain unauthorized.


## Preserved unreviewed implementation evidence

Checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` preserves exact recovered bytes for the sole R1
writable target without changing the executable source path.

- evidence payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- evidence payload size: `112338` bytes
- preservation state: `PAYLOAD_VERIFIED_PRE_INSTALL`
- canonical installation state: `PENDING_GUSTAVO_COMMIT_AND_SENTINEL_VERIFICATION`
- conformance state: `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`

Read the checkpoint only after the governing scope and authorization package.
Do not use it as a new edit base, do not roll back to it, and do not promote it
to `pm_research/` without a later Sentinel decision and Gustavo authorization.

---

## Historical canonical handoff at installation base — preserved verbatim

# REV23 Finding 4 Canonical Handoff — I0A Authoring Authorized

## Current canonical state

Finding 4 and accepted I0A Scope Revision 08 are canonically installed and
verified. Gustavo authorized bounded I0A implementation-source and unexecuted
test-source authoring; Sentinel approved the exact twelve-path boundary.

- verified accepted-scope commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- Finding 4 installation commit: `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`
- accepted Finding 4 package SHA-256: `9ec22f611a1f6b8a598725e0b60b7591503fd6271ae79eb366359e7e312099f8`
- accepted I0A scope archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`

The active authorization becomes usable only after Sentinel verifies the
canonical commit containing `authorization_audit/rev23_finding4_i0a/`.

## Required read order

1. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
2. `authorization_audit/rev23_finding4_i0a/README_FIRST.md`
3. `authorization_audit/rev23_finding4_i0a/SENTINEL_IMPLEMENTATION_AUTHORIZATION.md`
4. `authorization_audit/rev23_finding4_i0a/AUTHORIZATION_MANIFEST.json`
5. `authorization_audit/rev23_finding4_i0a/AUTHORIZED_FILE_MATRIX.md`
6. `authorization_audit/rev23_finding4_i0a/ACTIVITY_BOUNDARIES.md`
7. `authorization_audit/rev23_finding4_i0a/SOURCE_GATE.md`
8. `scope_authoring/rev23_finding4_i0a/README_FIRST.md`
9. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_08/README_FIRST.md`
10. the remaining accepted-scope files in their own read order
11. `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
12. `accepted_contract/ACCEPTED_CONTRACT_SHA256SUMS.txt`
13. root `START_HERE.md`, then `project_context/START_HERE.md`

## Authorization boundary

Authorized: read-only source sync to source-gated HEAD, exact six source files,
exact six unexecuted test-source files, static packaging/report/checksum work.

Unauthorized: tests, project imports/execution, research data, empirical work,
general network/API/curl, dependencies/CLI/config, additional paths, Git history
or remote writes, downstream research phases, and gate changes.
