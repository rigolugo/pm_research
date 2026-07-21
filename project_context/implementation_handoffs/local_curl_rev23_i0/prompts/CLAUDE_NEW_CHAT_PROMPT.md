# INACTIVE CLAUDE HANDOFF — REV23 Finding 4 I0A Revision 09

Status: **STOP_IMPLEMENTATION_NOT_AUTHORIZED**

Revision 09 was Sentinel-accepted on `2026-07-20` as a narrow SPEC-ONLY correction. This file is not an active implementation prompt. The Revision 08 authorization text below is retained verbatim for historical audit evidence and MUST NOT be executed for Revision 09.

Do not synchronize sources, author implementation or test source, invoke the implementing skill, execute tests or project code, access research data, use network/vendor services, create empirical artifacts, or write Git. A later separate Gustavo authorization and Sentinel handoff are mandatory.

---

## Historical Revision 08 prompt — preserved verbatim and non-operative

# ACTIVE CLAUDE HANDOFF — REV23 Finding 4 I0A Implementation Authoring

Use the pm-research-implementing Skill. Skill invocation does not expand the authorization below.

## Governing identity

- canonical repository: `rigolugo/pm_research`
- accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- accepted scope SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`
- accepted-scope canonical commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- authorization-package installation commit: `b22e30a35f24d4af8b134925ed338a9dd4c2a3b0`
- active package: `project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/`
- source-gated implementation HEAD: the later canonical commit containing both this corrected handoff and the restored complete `HANDOFF_SHA256SUMS.txt`, after Sentinel verifies that commit

Neither `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff` nor
`b22e30a35f24d4af8b134925ed338a9dd4c2a3b0` is the source-gated implementation
HEAD. Do not begin until Sentinel verifies the later activation-correction commit
and supplies its exact full SHA. Record that SHA and require local HEAD to equal it.

## Authorized stage

Author implementation source and unexecuted test source only.

### Authorized source files

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/canonical.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `pm_research/local_curl_per_side/finding4_registry.py`
- `pm_research/local_curl_per_side/prepared_evidence.py`
- `pm_research/local_curl_per_side/claim_hashes.py`

### Authorized test-source files

- `tests/local_curl_per_side/test_canonical_i0a.py`
- `tests/local_curl_per_side/test_governing_package_i0a.py`
- `tests/local_curl_per_side/test_finding4_registry_i0a.py`
- `tests/local_curl_per_side/test_prepared_evidence_i0a.py`
- `tests/local_curl_per_side/test_claim_hashes_i0a.py`
- `tests/local_curl_per_side/test_i0a_public_contract.py`

No other path may be created, edited, deleted, renamed, or generated. All twelve paths are create-only.

## Activity boundaries

- Source synchronization: authorized read-only to the Sentinel-verified source-gated HEAD.
- Test-source authoring: authorized for the six exact test files.
- Test execution: not authorized.
- Project imports/execution: not authorized.
- Local research-data reads: not authorized.
- Network: only read-only Git/GitHub source synchronization; no API/RPC/vendor/Dune/curl/general browsing.
- Subprocess: only git status/diff, file listing/comparison, checksums, and ZIP packaging.
- Artifact production: implementation review ZIP, static report, and SHA256SUMS only.
- Git writes: local working-tree writes to the exact twelve paths only; no commit, branch, push, PR, merge, or remote write.

## Preconditions

Read root `START_HERE.md`, `project_context/START_HERE.md`, the full canonical read order, accepted contract, accepted Revision 08 scope, and the active authorization package. Obtain the exact Sentinel-verified activation-correction commit SHA. Verify local HEAD equals that SHA, the worktree is clean, every create-only path is absent, all governing hashes and checksum inventories match, and the file/activity matrices are exact. Apply the accepted ordered halt domain before writing any source file.

## Deliverable

Return one implementation review ZIP conforming to `IMPLEMENTATION_ZIP_LAYOUT_CONTRACT.md`. Include the exact twelve authored files, package-only static conformance report(s), and one `SHA256SUMS.txt` covering every other member exactly once. Record the governing hashes, scope-review anchor, active authorization identity, source-gated local HEAD, and final worktree/diff state.

Do not update canonical project-context files in the repo. If a canonical update is needed, return a finding only. Stop rather than infer permission on any ambiguity or required scope expansion.
