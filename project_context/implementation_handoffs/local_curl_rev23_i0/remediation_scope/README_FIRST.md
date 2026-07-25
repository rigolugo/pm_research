# Revision 10 Local-Curl Remediation Scope — Read First

## Current status

- accepted remediation-scope source: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- submitted ZIP SHA-256: `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`;
- Sentinel decision: `APPROVE — REV10_LOCAL_CURL_REMEDIATION_SCOPE_ACCEPTED`;
- Gustavo documentation-only installation authorization: **GRANTED** on `2026-07-24`;
- canonical installation base: `cc2964840d197a40d1c4ef567b42eda762c0be0a`;
- installation state: `INSTALLED_AND_SENTINEL_VERIFIED`;
- verified installation commit: `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`;
- implementation authorization: **NONE**;
- implementation starting SHA: `NOT_AUTHORIZED_AND_NOT_SELECTED`;
- test-source authoring: **UNAUTHORIZED**;
- test execution: **UNAUTHORIZED**.

The accepted remediation scope is an implementation-planning contract only. It does not accept, restore, promote, or authorize the preserved `fcf406c4...` checkpoint.

## Read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `SENTINEL_INSTALLATION_AUTHORIZATION.md`
3. `SENTINEL_INSTALLATION_VERIFICATION.md`
4. `ACCEPTED_REMEDIATION_SCOPE_MANIFEST.json`
5. `accepted_remediation_scope_candidate_01/README_FIRST.md`
6. `accepted_remediation_scope_candidate_01/REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01.md`
7. `accepted_remediation_scope_candidate_01/CONTRACT_GAP_TO_CHANGE_MATRIX.md`
8. `accepted_remediation_scope_candidate_01/AUTHORIZED_FILE_MATRIX.md`
9. `accepted_remediation_scope_candidate_01/INTERFACE_AND_RESULT_CODE_MATRIX.md`
10. `accepted_remediation_scope_candidate_01/TEST_OBLIGATION_MATRIX.md`
11. `accepted_remediation_scope_candidate_01/ACTIVITY_BOUNDARIES_AND_STOPS.md`
12. `accepted_remediation_scope_candidate_01/PROVENANCE_GAP_HANDLING.md`
13. `accepted_remediation_scope_candidate_01/SENTINEL_REVIEW_HANDOFF.md`
14. `accepted_remediation_scope_candidate_01/PACKAGE_MANIFEST.json`
15. `accepted_remediation_scope_candidate_01/SHA256SUMS.txt`
16. `REMEDIATION_SCOPE_SHA256SUMS.txt`

## Accepted implementation-stage design

The remediation scope requires a single atomic source-authoring candidate across exactly:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

Test-source authoring is a separate later boundary across exactly:

- `tests/local_curl_per_side/test_canonical_i0a.py`;
- `tests/local_curl_per_side/test_finding4_registry_i0a.py`;
- `tests/local_curl_per_side/test_i0a_public_contract.py`;
- `tests/local_curl_per_side/test_prepared_evidence_i0a.py`.

Acceptance of this documentation package does not authorize either boundary.

## Binding Sentinel determinations

1. Selected-member iteration: wrapper-eligible sidecars first, then wrapper-eligible non-sidecars; ascending numeric `object_ordinal` within each class.
2. `UnitContext`: exact closed type and values only; no mapping lookalikes, aliases, inferred defaults, or coercion; `subject_sequence` requires `type(value) is int`, excludes `bool`, and is bounded to `0..2^64-1`.
3. Checksums: the candidate's internal checksum inventory excludes its own self-reference; the detached ZIP SHA-256 identifies the complete submitted archive.

## Preserved checkpoint and provenance

`REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` remains exact, recoverable, evidence-only, `NOT_ACCEPTED`, non-controlling, and authorization effect `NONE`.

The following provenance gaps remain open:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

They are not resolved by this remediation-scope acceptance or installation.

## Non-authorization

No implementation, source/test edit, test execution, rollback, restoration, overwrite, promotion, project execution, data/network access, subprocess, artifact production, Git write by Claude, R2, P1/P2/P3, scoring, probe execution, or gate change is authorized.

The documentation-only installation is verified at `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`. No Claude implementation prompt is active. A later implementation stage requires separate Gustavo authorization, a Sentinel-approved handoff, and an independently verified starting state.
