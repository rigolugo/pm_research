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
