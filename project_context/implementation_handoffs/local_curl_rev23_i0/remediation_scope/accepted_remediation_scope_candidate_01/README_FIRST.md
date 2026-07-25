# README FIRST — Revision 10 Local-Curl Implementation Remediation

## Status

`REVIEW_CANDIDATE — SPECIFICATION ONLY — NOT ACCEPTED — AUTHORIZATION EFFECT NONE`

Professor drafted this package. Sentinel reviews and decides. Claude may receive implementation scope only after Sentinel acceptance and separate Gustavo authorization.

## Package identity

- package ID: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- candidate number: `01`;
- canonical repository: `rigolugo/pm_research`;
- canonical base: `cc2964840d197a40d1c4ef567b42eda762c0be0a`;
- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- preserved evidence checkpoint: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`;
- preserved payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`.

## Purpose

Define the smallest complete future implementation-remediation boundary capable of addressing all eight verified Revision 10 static-conformance failures without creating a partial or false-unblock state.

## Checkable completion sentence

This candidate is complete when Sentinel can verify that every verified Revision 10 defect is assigned to its correct mandatory source owner, every result and predicate mapping is total and ordered, the exact future source and test boundaries are closed, provenance gaps remain separately classified, and no implementation or execution authority is implied.

## Read order

1. `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01.md`
2. `CONTRACT_GAP_TO_CHANGE_MATRIX.md`
3. `AUTHORIZED_FILE_MATRIX.md`
4. `INTERFACE_AND_RESULT_CODE_MATRIX.md`
5. `TEST_OBLIGATION_MATRIX.md`
6. `ACTIVITY_BOUNDARIES_AND_STOPS.md`
7. `PROVENANCE_GAP_HANDLING.md`
8. `SENTINEL_REVIEW_HANDOFF.md`
9. `PACKAGE_MANIFEST.json`
10. `SHA256SUMS.txt`

## Exact proposed future changed-path boundary

Source-authoring stage, mandatory and atomic:

- `pm_research/local_curl_per_side/canonical.py`
- `pm_research/local_curl_per_side/finding4_registry.py`
- `pm_research/local_curl_per_side/prepared_evidence.py`

Later test-source-authoring stage, separately gated:

- `tests/local_curl_per_side/test_canonical_i0a.py`
- `tests/local_curl_per_side/test_finding4_registry_i0a.py`
- `tests/local_curl_per_side/test_i0a_public_contract.py`
- `tests/local_curl_per_side/test_prepared_evidence_i0a.py`

Allowed new implementation or test files: `NONE`.

## Explicit non-authorization

This package does not select implementation starting bytes or a starting SHA. It does not authorize restoration, promotion, continuation from the checkpoint, source authoring, test-source authoring, test execution, project execution, imports, compilation, lint, typing, coverage, CI, local-data reads, network or subprocess use, artifact production, Git writes, R2, P1, P2, P3, scoring, probe execution, or gate changes.

## Checksum convention

`SHA256SUMS.txt` covers every other package member. It omits its own checksum because an internal file cannot contain its actual final SHA-256 without self-reference. `PACKAGE_MANIFEST.json` lists all members, gives actual SHA-256 values for every non-inventory member, and records the inventory-file self-reference exception explicitly. The detached ZIP SHA-256 covers the complete archive bytes.
