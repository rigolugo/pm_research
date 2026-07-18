# ACTIVE CLAUDE HANDOFF — REV23 Finding 4 I0A Implementation Authoring

Use the pm-research-implementing Skill. Skill invocation does not expand the authorization below.

## Governing identity

- canonical repository: `rigolugo/pm_research`
- accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- accepted scope SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`
- verified pre-authorization commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- active package: `project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/`

Do not begin until Sentinel has verified the canonical commit containing this
active package. Record that exact commit as the source-gated local HEAD.

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

Read root `START_HERE.md`, `project_context/START_HERE.md`, the full canonical read order, accepted contract, accepted Revision 08 scope, and the active authorization package. Verify local HEAD, clean worktree, create-only path absence, hashes, file matrix, activity matrix, and governing bytes. Apply the exact ordered halt domain.

## Deliverable

Return one implementation review ZIP conforming to `IMPLEMENTATION_ZIP_LAYOUT_CONTRACT.md`. Include the exact twelve authored files, package-only static conformance report(s), and one `SHA256SUMS.txt` covering every other member exactly once. Record the governing hashes, scope-review anchor, active authorization identity, source-gated local HEAD, and final worktree/diff state.

Do not update canonical project-context files in the repo. If a canonical update is needed, return a finding only. Stop rather than infer permission on any ambiguity or required scope expansion.
