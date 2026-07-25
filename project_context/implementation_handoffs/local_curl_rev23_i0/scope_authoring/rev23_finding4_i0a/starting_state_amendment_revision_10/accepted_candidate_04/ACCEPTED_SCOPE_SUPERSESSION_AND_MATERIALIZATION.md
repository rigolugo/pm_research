# Accepted-Scope Clause Amendment and Supersession Table — Candidate 04

## 1. Status

`AMENDMENT CANDIDATE — NOT ACCEPTED — AUTHORIZATION EFFECT NONE`

Candidate 04 amends only the accepted remediation scope's starting-state and later materialization clauses. It does not amend Revision 10 implementation behavior.

## 2. Definitions

- **Workspace member:** a regular file under an isolated non-Git staging root outside every repository checkout. Instantiating it is not creation of a repository file.
- **Repository file:** a path in the canonical Git tree, index, or worktree.
- **Edit:** any byte, path, identity, or metadata change to an existing workspace/repository member. Exact-byte creation at an absent canonical target is not an edit of the captured source bytes.
- **Materialization:** a separately authorized manual canonical installation that creates an exact declared absent target from previously accepted bytes.

## 3. Governing rule

Candidate 03 remains blocked, unaccepted, and non-controlling. Candidate 04 incorporates the exact Candidate 03 supersession text without redesign. The retained `C03_*` provision identifiers are stable semantic identifiers only; they do not confer authority on Candidate 03. If Sentinel accepts Candidate 04, Candidate 04 is the controlling amendment that gives those retained provisions effect.

Candidate 04 controls only where the table below expressly says `SUPERSEDED`, `NARROWLY_SUPERSEDED`, or names a retained `C03_*` provision incorporated by Candidate 04. In every other case, the accepted remediation scope remains controlling.

## 4. Exact clause-level table

| Clause ID | Accepted source and rule | Workspace preparation | Source authoring | Test authoring | Source materialization | Test materialization | Retained provision incorporated by Candidate 04 |
|---|---|---|---|---|---|---|---|
| `RSC_AFM_ALLOWED_NEW_FILES_NONE` | accepted_remediation_scope_candidate_01/AUTHORIZED_FILE_MATRIX.md#Allowed-new-files: Future implementation/test scope allowed new files is NONE. | REMAINS_CONTROLLING_FOR_REPOSITORY_FILES; workspace-member instantiation is outside the repository and does not create a repository file. | REMAINS_CONTROLLING; no new workspace member or repository file. | REMAINS_CONTROLLING; no new workspace member or repository file. | NARROWLY_SUPERSEDED_BY_C03_MAT_SOURCE_01 for exactly six absent source targets. | NARROWLY_SUPERSEDED_BY_C03_MAT_TEST_01 for exactly six absent test targets. | `C03_SUP_01, C03_MAT_SOURCE_01, C03_MAT_TEST_01` |
| `RSC_ABS_MANDATORY_FILES_AVAILABLE` | accepted_remediation_scope_candidate_01/ACTIVITY_BOUNDARIES_AND_STOPS.md#Source-authoring-preconditions: All mandatory files must be available before source authoring. | REMAINS_CONTROLLING_AS_CLEAR_CONDITION; no authoring may begin until all twelve exact workspace members, including all mandatory files, are present and verified. | REMAINS_CONTROLLING without exception. | REMAINS_CONTROLLING; all six final source members and six test starts must be present before test authoring. | SUPERSEDED_ONLY_FOR_TARGET_EXISTENCE: all six canonical source targets must be absent before exact-byte creation. | SUPERSEDED_ONLY_FOR_TARGET_EXISTENCE: all six canonical test targets must be absent before exact-byte creation. | `C03_WS_04, C03_SRC_02, C03_TWS_04, C03_MAT_SOURCE_02, C03_MAT_TEST_02` |
| `RSC_ABS_MISSING_AUTHORIZED_PATH_HALT` | accepted_remediation_scope_candidate_01/ACTIVITY_BOUNDARIES_AND_STOPS.md#Mandatory-halts: Halt if any authorized path is missing. | REMAINS_CONTROLLING_AS FINAL CLEAR PREDICATE; partial rehydration halts and cannot activate authoring. | REMAINS CONTROLLING. | REMAINS CONTROLLING. | NARROW TARGET-ABSENCE EXCEPTION controls before creation; after creation, any missing target halts verification. | NARROW TARGET-ABSENCE EXCEPTION controls before creation; after creation, any missing target halts verification. | `C03_WS_08, C03_SRC_03, C03_TWS_08, C03_MAT_SOURCE_03, C03_MAT_TEST_03` |
| `RSC_AFM_FIVE_NOT_IMPLICATED_PROHIBITED` | accepted_remediation_scope_candidate_01/AUTHORIZED_FILE_MATRIX.md#Exact-twelve-path-closure-and-Global-prohibition: The five non-implicated paths are prohibited from implementation or test editing. | REMAINS CONTROLLING FOR EDITS; exact-byte instantiation into an empty non-repository workspace is not an edit. | REMAINS CONTROLLING; all five are read-only exact bytes. | REMAINS CONTROLLING; all five are read-only exact bytes. | NARROWLY SUPERSEDED ONLY FOR exact-byte CREATE of __init__.py, claim_hashes.py, and governing_package.py; content modification remains prohibited. | NARROWLY SUPERSEDED ONLY FOR exact-byte CREATE of test_claim_hashes_i0a.py and test_governing_package_i0a.py; content modification remains prohibited. | `C03_SUPPORT_01, C03_MAT_SOURCE_04, C03_MAT_TEST_04` |
| `RSC_ABS_NEW_FILE_REQUIRED_HALT` | accepted_remediation_scope_candidate_01/ACTIVITY_BOUNDARIES_AND_STOPS.md#Mandatory-halts: Halt if implementation requires a new file. | REMAINS CONTROLLING FOR REPOSITORY FILES and for any thirteenth workspace member. | REMAINS CONTROLLING. | REMAINS CONTROLLING. | NARROWLY SUPERSEDED for the exact six declared source CREATE actions only. | NARROWLY SUPERSEDED for the exact six declared test CREATE actions only. | `C03_SUP_02, C03_MAT_SOURCE_01, C03_MAT_TEST_01` |

## 5. Candidate 04 controlling provisions

- **`C03_SUP_01`:** During workspace preparation, source authoring, test-workspace preparation, and test authoring, `allowed new repository files = NONE` remains controlling. Exact instantiation of declared workspace members outside every repository is not a repository-file exception.
- **`C03_SUP_02`:** A thirteenth workspace member or any undeclared repository path remains prohibited and selects `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED`.
- **`C03_WS_04`:** Workspace preparation is clear only after all twelve exact members exist and match path, regular-file type, size, and SHA-256.
- **`C03_WS_08`:** Partial workspace rehydration is a halt. Missing members are not permitted authoring starts.
- **`C03_SRC_02`:** Source authoring begins only from all twelve exact available members.
- **`C03_SRC_03`:** Any missing source-stage member after activation is a halt; no restoration or synthesis is permitted.
- **`C03_TWS_04`:** Test workspace preparation requires six Sentinel-verified final source members and six exact captured test starts.
- **`C03_TWS_08`:** Any missing test-workspace member is a halt.
- **`C03_SUPPORT_01`:** The five baseline-support paths are edit-prohibited in every authoring and review stage. Their only later exception is exact-byte CREATE at an absent canonical target under the matching materialization authorization.
- **`C03_MAT_SOURCE_01`:** A separately authorized source materialization MAY create exactly the six declared source paths and no others.
- **`C03_MAT_SOURCE_02`:** Before source materialization, all six canonical source targets MUST be absent. This target-absence predicate supersedes the accepted mandatory-file-availability predicate only for the materialization target location.
- **`C03_MAT_SOURCE_03`:** After source materialization, all six paths MUST exist with exact accepted bytes; a missing path halts installation verification.
- **`C03_MAT_SOURCE_04`:** The three support source paths MUST be created byte-identical to the accepted capture and MUST NOT be edited.
- **`C03_MAT_TEST_01`:** A separately authorized test materialization MAY create exactly the six declared test paths and no others.
- **`C03_MAT_TEST_02`:** Before test materialization, all six canonical test targets MUST be absent. This target-absence predicate supersedes mandatory-file availability only for the materialization target location.
- **`C03_MAT_TEST_03`:** After test materialization, all six test paths MUST exist with exact accepted bytes; a missing path halts verification.
- **`C03_MAT_TEST_04`:** The two support test paths MUST be created byte-identical to the accepted capture and MUST NOT be edited.

## 6. Five baseline-support paths

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/claim_hashes.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `tests/local_curl_per_side/test_claim_hashes_i0a.py`
- `tests/local_curl_per_side/test_governing_package_i0a.py`

They remain prohibited from editing. Candidate 04 permits only exact-byte instantiation as a non-repository workspace member and, later, exact-byte creation at an absent canonical target in the matching materialization stage.

## 7. Conflict precedence

| Context | Controlling rule | Candidate 04 effect |
|---|---|---|
| `WORKSPACE_PREPARATION_OR_SOURCE_OR_TEST_AUTHORING` | `ACCEPTED_REMEDIATION_SCOPE` | Adds exact location and identity interpretation only; creates no repository new-file exception and no edit exception. |
| `SOURCE_MATERIALIZATION` | `CANDIDATE03_C03_MAT_SOURCE_01_THROUGH_04` | Permits exact-byte creation of exactly six absent source targets under separate authorization; every other accepted-scope prohibition remains controlling. |
| `TEST_MATERIALIZATION` | `CANDIDATE03_C03_MAT_TEST_01_THROUGH_04` | Permits exact-byte creation of exactly six absent test targets under separate authorization; every other accepted-scope prohibition remains controlling. |
| `ALL_OTHER_CONTEXTS` | `ACCEPTED_REMEDIATION_SCOPE` | NONE. |

## 8. No implicit authority

This amendment text does not activate any exception. Each materialization exception requires its own Sentinel-accepted installation contract, separate Gustavo authorization, exact absence gate, manual installation, and Sentinel verification.

