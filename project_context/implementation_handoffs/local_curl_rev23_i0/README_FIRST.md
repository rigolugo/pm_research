# REV23 Finding 4 Canonical Handoff — Revision 09 R1 Authorization Installation

## Revision 09 controlling installation state

Revision 09 is canonically installed and Sentinel-verified at
`c4e8b1011c51272042decac4bc89e762d767a72a`. Gustavo explicitly authorized and
Sentinel accepted the narrow R1 source-resume authorization
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`. That authorization remains
inactive until Gustavo manually commits this exact documentation package and
Sentinel verifies the resulting commit.

- accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- Sentinel acceptance date: `2026-07-20`
- accepted archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
- accepted member count: `14`
- installation base: `1e963bb6e8387aff071d697a416fa558956e571e`
- verified canonical installation commit:
  `c4e8b1011c51272042decac4bc89e762d767a72a`
- immutable installed directory:
  `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_09/`
- historical Revision 08 directory: unchanged
- active-after-verification authorization: `REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`
- sole writable path after activation: `pm_research/local_curl_per_side/prepared_evidence.py`
- required starting SHA-256: `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`
- test-source authoring and test execution: **NOT AUTHORIZED**

## Revision 09 read order

1. `authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/README_FIRST.md`
2. the remaining files in that authorization directory read order
3. `scope_authoring/rev23_finding4_i0a/README_FIRST.md`
4. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
5. `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json`
6. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_09/README_FIRST.md`
7. the remaining Revision 09 members in their own read order
8. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION_REVISION_08.md`
9. `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST_REVISION_08.json`
10. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_08/README_FIRST.md`
11. `scope_authoring/rev23_finding4_i0a/SCOPE_SHA256SUMS.txt`
12. `HANDOFF_REVISION_09_INSTALL_SHA256SUMS.txt`
13. `HANDOFF_REVISION_09_R1_AUTHORIZATION_SHA256SUMS.txt`
14. `HANDOFF_SHA256SUMS.txt`

## Revision 09 R1 authorization boundary

After authorization-installation-commit verification, Claude may synchronize
read-only to the Sentinel-verified commit and edit only
`pm_research/local_curl_per_side/prepared_evidence.py`, then return one
source-only checkpoint. The source gate requires exactly twelve authorized
untracked paths, exact equality with the immutable twelve-path baseline, and no
thirteenth or other changed path. The other eleven authored paths are read-only.

The edited existing `prepared_evidence.py` is the only submitted source file.
Static source report, exact path inventory, diff summary, and checksums are chat
text and MUST NOT be created as repository files. Test-source editing, tests,
project imports/execution, another source edit, implementation ZIP
reconstruction, research data, empirical work, general network/vendor activity,
Git history/remote writes, R2, and downstream phases remain unauthorized.

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
