# Total Typed Workflow Domain — Candidate 04

## 1. Status and boundary

`SPEC ONLY — CLOSED WORKFLOW CONTRACT — AUTHORIZATION EFFECT NONE`

Candidate 03 remains blocked and non-controlling. Candidate 04 preserves its architecture and corrects only record-schema closure and commit/review/push/remote-verification separation.

This workflow is not an `I0AResultCode` domain, runtime stop domain, implementation authorization, push authorization, or execution authorization.

## 2. Normative members

- `WORKFLOW_DOMAIN.json` — enums, stages, predicates, transitions, applicability, and success metadata;
- `WORKFLOW_HALT_RECORD.schema.json` — closed Draft 2020-12 halt-record schema;
- `WORKFLOW_SUCCESS_RECORD.schema.json` — closed Draft 2020-12 success-record schema;
- `WORKFLOW_RECORD_CROSS_FIELD_RULES.md` — normative relationships not compactly expressible in JSON Schema;
- `DELIVERY_COMMIT_PUSH_REMOTE_BOUNDARIES.md` — local commit, review, push authorization, push, and remote verification separation.

## 3. Closed enum counts

| Enum | Count | Values |
|---|---:|---|
| `AuthorizationEffect` | 10 | `NONE`; `WORKSPACE_PREPARATION_ONLY`; `SOURCE_AUTHORING_ONLY`; `SOURCE_LOCAL_COMMIT_CREATION_ONLY`; `SOURCE_PUSH_ONLY`; `TEST_WORKSPACE_PREPARATION_ONLY`; `TEST_AUTHORING_ONLY`; `TEST_LOCAL_COMMIT_CREATION_ONLY`; `TEST_PUSH_ONLY`; `EXECUTION_ONLY` |
| `DecisionOwner` | 5 | `SENTINEL`; `GUSTAVO`; `GUSTAVO_MANUAL_INSTALLER`; `CLAUDE`; `NO_OWNER` |
| `ObservationStatus` | 8 | `EXPECTED`; `SATISFIED`; `FALSE`; `MISSING`; `MALFORMED`; `AMBIGUOUS`; `STALE`; `CONFLICTING` |
| `RetryEligibility` | 8 | `SAME_AUTHORIZATION_FRESH_GATE`; `NEW_SENTINEL_DECISION_REQUIRED`; `NEW_GUSTAVO_AUTHORIZATION_REQUIRED`; `NEW_PUSH_AUTHORIZATION_REQUIRED`; `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED`; `MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION`; `NO_RETRY_UNDER_SAME_AUTHORIZATION`; `NOT_APPLICABLE` |
| `ReviewDecision` | 5 | `APPROVE`; `BLOCK`; `DEFER`; `ACCEPT_FINDING`; `NEEDS_VERIFICATION` |
| `WorkflowStage` | 20 | `SPEC_REVIEW`; `SPEC_CANONICAL_INSTALLATION_CONFIRMATION`; `WORKSPACE_PREPARATION`; `SOURCE_AUTHORING`; `SOURCE_STATIC_REVIEW`; `SOURCE_LOCAL_COMMIT_CREATION`; `SOURCE_LOCAL_COMMIT_REVIEW`; `SOURCE_PUSH_AUTHORIZATION`; `SOURCE_FAST_FORWARD_PUSH`; `SOURCE_REMOTE_INSTALLATION_VERIFICATION`; `TEST_SCOPE_REVIEW`; `TEST_WORKSPACE_PREPARATION`; `TEST_AUTHORING`; `TEST_STATIC_REVIEW`; `TEST_LOCAL_COMMIT_CREATION`; `TEST_LOCAL_COMMIT_REVIEW`; `TEST_PUSH_AUTHORIZATION`; `TEST_FAST_FORWARD_PUSH`; `TEST_REMOTE_INSTALLATION_VERIFICATION`; `EXECUTION_AUTHORIZATION` |
| `WorkflowState` | 21 | `C04_DRAFT_NOT_ACCEPTED`; `C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION`; `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED`; `C04_SOURCE_WORKSPACE_READY`; `C04_SOURCE_CANDIDATE_SUBMITTED`; `C04_SOURCE_STATIC_ACCEPTED_NOT_MATERIALIZED`; `C04_SOURCE_LOCAL_COMMIT_CREATED_PENDING_REVIEW`; `C04_SOURCE_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED`; `C04_SOURCE_PUSH_AUTHORIZED_NOT_PUSHED`; `C04_SOURCE_PUSHED_PENDING_REMOTE_VERIFICATION`; `C04_SOURCE_REMOTE_MATERIALIZED_VERIFIED`; `C04_TEST_SCOPE_ACCEPTED_NOT_AUTHORIZED`; `C04_TEST_WORKSPACE_READY`; `C04_TEST_CANDIDATE_SUBMITTED`; `C04_TEST_STATIC_ACCEPTED_NOT_MATERIALIZED`; `C04_TEST_LOCAL_COMMIT_CREATED_PENDING_REVIEW`; `C04_TEST_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED`; `C04_TEST_PUSH_AUTHORIZED_NOT_PUSHED`; `C04_TEST_PUSHED_PENDING_REMOTE_VERIFICATION`; `C04_TEST_REMOTE_MATERIALIZED_VERIFIED`; `C04_EXECUTION_AUTHORIZED_OUTSIDE_C04` |
| `WorkflowStopCode` | 70 | `STOP_C04_ATOMIC_SOURCE_RESULT_UNAVAILABLE`; `STOP_C04_AUTHORIZATION_NOT_ACTIVE`; `STOP_C04_CANONICAL_HEAD_MISMATCH`; `STOP_C04_CAPTURE_BYTE_IDENTITY_MISMATCH`; `STOP_C04_CAPTURE_PACKAGE_IDENTITY_MISMATCH`; `STOP_C04_CAPTURE_PATH_SET_MISMATCH`; `STOP_C04_CONTROLLING_CONTRACT_UNAVAILABLE`; `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE`; `STOP_C04_FAILED_GATE_REPAIR_ATTEMPT`; `STOP_C04_LOCAL_COMMIT_AUTHORIZATION_NOT_ACTIVE`; `STOP_C04_LOCAL_COMMIT_BASE_OR_BRANCH_MISMATCH`; `STOP_C04_LOCAL_COMMIT_IDENTITY_MISMATCH`; `STOP_C04_LOCAL_COMMIT_PARENT_MISMATCH`; `STOP_C04_LOCAL_COMMIT_PROHIBITED_OPERATION`; `STOP_C04_LOCAL_COMMIT_PUSH_OCCURRED`; `STOP_C04_LOCAL_COMMIT_REVIEW_NOT_APPROVED`; `STOP_C04_LOCAL_COMMIT_WORKTREE_NOT_CLEAN`; `STOP_C04_MANDATORY_FILE_UNAVAILABLE`; `STOP_C04_MATERIALIZATION_BYTE_IDENTITY_MISMATCH`; `STOP_C04_MATERIALIZATION_GIT_MODE_INVALID`; `STOP_C04_MATERIALIZATION_PATH_SET_MISMATCH`; `STOP_C04_MATERIALIZATION_TARGET_PRESENT`; `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED`; `STOP_C04_PUSH_AHEAD_BEHIND_MISMATCH`; `STOP_C04_PUSH_AUTHORIZATION_IDENTITY_MISMATCH`; `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE`; `STOP_C04_PUSH_BRANCH_REFSPEC_MISMATCH`; `STOP_C04_PUSH_BYTE_OR_MODE_MISMATCH`; `STOP_C04_PUSH_CHANGED_PATHS_OR_STATUSES_MISMATCH`; `STOP_C04_PUSH_COMMIT_MISMATCH`; `STOP_C04_PUSH_FAILED`; `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT`; `STOP_C04_PUSH_REMOTE_ADVANCED`; `STOP_C04_PUSH_WORKTREE_NOT_CLEAN`; `STOP_C04_READ_ONLY_PATH_MUTATED`; `STOP_C04_RECORD_CROSS_FIELD_MISMATCH`; `STOP_C04_RECORD_SCHEMA_INVALID`; `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH`; `STOP_C04_REMOTE_INSTALLATION_NOT_VERIFIED`; `STOP_C04_SOURCE_CANDIDATE_IDENTITY_MISMATCH`; `STOP_C04_SOURCE_REVIEW_NOT_APPROVED`; `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION`; `STOP_C04_SPEC_CANONICAL_BASE_MISMATCH`; `STOP_C04_SPEC_CANONICAL_INSTALLATION_LIVE_PATH_CHANGE`; `STOP_C04_SPEC_CANONICAL_INSTALLATION_NOT_APPROVED`; `STOP_C04_SPEC_CANONICAL_INSTALLATION_NOT_VERIFIED`; `STOP_C04_SPEC_CANONICAL_INSTALLATION_RECORD_MISSING`; `STOP_C04_SPEC_DELIVERY_MECHANICS_NOT_EXTERNAL`; `STOP_C04_SPEC_PACKAGE_IDENTITY_MISMATCH`; `STOP_C04_SPEC_PRESERVED_CONTRACT_MISMATCH`; `STOP_C04_SPEC_REPRESENTATION_MISMATCH`; `STOP_C04_SPEC_REVIEW_NOT_APPROVED`; `STOP_C04_SPEC_SCOPE_DRIFT`; `STOP_C04_SPEC_SELF_AUTHORIZED_DELIVERY_ATTEMPT`; `STOP_C04_SPEC_SUPERSESSION_INCOMPLETE`; `STOP_C04_SPEC_WORKFLOW_DOMAIN_NOT_TOTAL`; `STOP_C04_STAGE_STATE_MISMATCH`; `STOP_C04_TEST_AUTHORING_RESULT_UNAVAILABLE`; `STOP_C04_TEST_CANDIDATE_IDENTITY_MISMATCH`; `STOP_C04_TEST_REVIEW_NOT_APPROVED`; `STOP_C04_TEST_SCOPE_NOT_APPROVED`; `STOP_C04_TEST_WORKSPACE_SOURCE_IDENTITY_MISMATCH`; `STOP_C04_TRUSTED_MULTI_ROUND_LINEAGE_REQUIRED`; `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY`; `STOP_C04_UNAUTHORIZED_GIT_WRITE`; `STOP_C04_WORKSPACE_ALIAS_OR_LINK_INVALID`; `STOP_C04_WORKSPACE_EXTRA_OR_MISSING_PATH`; `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID`; `STOP_C04_WORKSPACE_NOT_EMPTY`; `STOP_C04_WORKSPACE_ROOT_INVALID` |
| `WorkflowSuccessCode` | 20 | `CLEAR_C04_SPEC_REVIEW_APPROVED`; `CLEAR_C04_SPEC_CANONICAL_INSTALLATION_CONFIRMED`; `CLEAR_C04_SOURCE_WORKSPACE_PREPARED`; `CLEAR_C04_SOURCE_CANDIDATE_SUBMITTED`; `CLEAR_C04_SOURCE_STATIC_REVIEW_APPROVED`; `CLEAR_C04_SOURCE_LOCAL_COMMIT_CREATED`; `CLEAR_C04_SOURCE_LOCAL_COMMIT_REVIEW_APPROVED`; `CLEAR_C04_SOURCE_PUSH_SEPARATELY_AUTHORIZED`; `CLEAR_C04_SOURCE_FAST_FORWARD_PUSH_COMPLETED`; `CLEAR_C04_SOURCE_REMOTE_INSTALLATION_VERIFIED`; `CLEAR_C04_TEST_SCOPE_REVIEW_APPROVED`; `CLEAR_C04_TEST_WORKSPACE_PREPARED`; `CLEAR_C04_TEST_CANDIDATE_SUBMITTED`; `CLEAR_C04_TEST_STATIC_REVIEW_APPROVED`; `CLEAR_C04_TEST_LOCAL_COMMIT_CREATED`; `CLEAR_C04_TEST_LOCAL_COMMIT_REVIEW_APPROVED`; `CLEAR_C04_TEST_PUSH_SEPARATELY_AUTHORIZED`; `CLEAR_C04_TEST_FAST_FORWARD_PUSH_COMPLETED`; `CLEAR_C04_TEST_REMOTE_INSTALLATION_VERIFIED`; `CLEAR_C04_EXECUTION_AUTHORIZATION_RECORDED_OUTSIDE_C04` |

## 4. Aggregate closure

- workflow states: `21`;
- workflow stages: `20`;
- workflow stop codes: `70`;
- workflow success codes: `20`;
- ordered predicate applications: `205`;
- each stage has exactly one declared from-state and one success to-state;
- every predicate maps to exactly one stop applicability row;
- every valid success maps to exactly one transition row.

## 5. Record-validation order

1. Parse JSON as UTF-8 without duplicate object member names.
2. Validate the record against the exact referenced Draft 2020-12 JSON Schema.
3. Validate every x-ordering and x-uniqueBy annotation normatively.
4. Validate the record against the exact WorkflowStage transition or predicate applicability row.
5. Recompute evidence_sha256 from the exact evidence projection and compare lowercase hex.

A record that fails either its JSON Schema or the normative cross-field rules is invalid. It changes no state and authorizes nothing.

## 6. Deterministic stage-selection algorithm

1. Resolve the requested stage as an exact WorkflowStage enum member.
2. Require current WorkflowState to equal that stage's exact from_state; otherwise the stage's first predicate returns STOP_C04_STAGE_STATE_MISMATCH.
3. Evaluate predicates in strictly ascending predicate_ordinal.
4. Treat false, missing, malformed, ambiguous, stale, or conflicting evidence as predicate failure.
5. On first failure, emit exactly one schema-valid halt record bound to the exact applicability row and evaluate no later predicate.
6. If every predicate succeeds, emit exactly one schema-valid success record bound to the exact stage transition row.
7. A halt or success record that fails its JSON Schema or normative cross-field rules is invalid and cannot move state.
8. No halt may trigger repair, fallback, deletion, overwrite, reset, restore, rollback, pull, merge, rebase, force, or automatic repair.

## 7. State-transition table

| Stage | From state | Required authorization effect | Success code | To state | Success decision owner | Success paths | Authoring started | Git write observed | Execution activity observed | Predicate count |
|---|---|---|---|---|---|---|---|---|---|---:|
| `SPEC_REVIEW` | `C04_DRAFT_NOT_ACCEPTED` | `NONE` | `CLEAR_C04_SPEC_REVIEW_APPROVED` | `C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION` | `SENTINEL` | <empty> | `false` | `false` | `false` | 11 |
| `SPEC_CANONICAL_INSTALLATION_CONFIRMATION` | `C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION` | `NONE` | `CLEAR_C04_SPEC_CANONICAL_INSTALLATION_CONFIRMED` | `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED` | `SENTINEL` | <empty> | `false` | `false` | `false` | 7 |
| `WORKSPACE_PREPARATION` | `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED` | `WORKSPACE_PREPARATION_ONLY` | `CLEAR_C04_SOURCE_WORKSPACE_PREPARED` | `C04_SOURCE_WORKSPACE_READY` | `SENTINEL` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py`<br>`tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 18 |
| `SOURCE_AUTHORING` | `C04_SOURCE_WORKSPACE_READY` | `SOURCE_AUTHORING_ONLY` | `CLEAR_C04_SOURCE_CANDIDATE_SUBMITTED` | `C04_SOURCE_CANDIDATE_SUBMITTED` | `SENTINEL` | `pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `true` | `false` | `false` | 12 |
| `SOURCE_STATIC_REVIEW` | `C04_SOURCE_CANDIDATE_SUBMITTED` | `NONE` | `CLEAR_C04_SOURCE_STATIC_REVIEW_APPROVED` | `C04_SOURCE_STATIC_ACCEPTED_NOT_MATERIALIZED` | `SENTINEL` | `pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `false` | `false` | `false` | 8 |
| `SOURCE_LOCAL_COMMIT_CREATION` | `C04_SOURCE_STATIC_ACCEPTED_NOT_MATERIALIZED` | `SOURCE_LOCAL_COMMIT_CREATION_ONLY` | `CLEAR_C04_SOURCE_LOCAL_COMMIT_CREATED` | `C04_SOURCE_LOCAL_COMMIT_CREATED_PENDING_REVIEW` | `GUSTAVO_MANUAL_INSTALLER` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `false` | `true` | `false` | 14 |
| `SOURCE_LOCAL_COMMIT_REVIEW` | `C04_SOURCE_LOCAL_COMMIT_CREATED_PENDING_REVIEW` | `NONE` | `CLEAR_C04_SOURCE_LOCAL_COMMIT_REVIEW_APPROVED` | `C04_SOURCE_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` | `SENTINEL` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `false` | `false` | `false` | 10 |
| `SOURCE_PUSH_AUTHORIZATION` | `C04_SOURCE_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` | `NONE` | `CLEAR_C04_SOURCE_PUSH_SEPARATELY_AUTHORIZED` | `C04_SOURCE_PUSH_AUTHORIZED_NOT_PUSHED` | `SENTINEL` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `false` | `false` | `false` | 7 |
| `SOURCE_FAST_FORWARD_PUSH` | `C04_SOURCE_PUSH_AUTHORIZED_NOT_PUSHED` | `SOURCE_PUSH_ONLY` | `CLEAR_C04_SOURCE_FAST_FORWARD_PUSH_COMPLETED` | `C04_SOURCE_PUSHED_PENDING_REMOTE_VERIFICATION` | `GUSTAVO_MANUAL_INSTALLER` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `false` | `true` | `false` | 13 |
| `SOURCE_REMOTE_INSTALLATION_VERIFICATION` | `C04_SOURCE_PUSHED_PENDING_REMOTE_VERIFICATION` | `NONE` | `CLEAR_C04_SOURCE_REMOTE_INSTALLATION_VERIFIED` | `C04_SOURCE_REMOTE_MATERIALIZED_VERIFIED` | `SENTINEL` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py` | `false` | `false` | `false` | 7 |
| `TEST_SCOPE_REVIEW` | `C04_SOURCE_REMOTE_MATERIALIZED_VERIFIED` | `NONE` | `CLEAR_C04_TEST_SCOPE_REVIEW_APPROVED` | `C04_TEST_SCOPE_ACCEPTED_NOT_AUTHORIZED` | `SENTINEL` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 7 |
| `TEST_WORKSPACE_PREPARATION` | `C04_TEST_SCOPE_ACCEPTED_NOT_AUTHORIZED` | `TEST_WORKSPACE_PREPARATION_ONLY` | `CLEAR_C04_TEST_WORKSPACE_PREPARED` | `C04_TEST_WORKSPACE_READY` | `SENTINEL` | `pm_research/local_curl_per_side/__init__.py`<br>`pm_research/local_curl_per_side/canonical.py`<br>`pm_research/local_curl_per_side/claim_hashes.py`<br>`pm_research/local_curl_per_side/finding4_registry.py`<br>`pm_research/local_curl_per_side/governing_package.py`<br>`pm_research/local_curl_per_side/prepared_evidence.py`<br>`tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 15 |
| `TEST_AUTHORING` | `C04_TEST_WORKSPACE_READY` | `TEST_AUTHORING_ONLY` | `CLEAR_C04_TEST_CANDIDATE_SUBMITTED` | `C04_TEST_CANDIDATE_SUBMITTED` | `SENTINEL` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `true` | `false` | `false` | 10 |
| `TEST_STATIC_REVIEW` | `C04_TEST_CANDIDATE_SUBMITTED` | `NONE` | `CLEAR_C04_TEST_STATIC_REVIEW_APPROVED` | `C04_TEST_STATIC_ACCEPTED_NOT_MATERIALIZED` | `SENTINEL` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 7 |
| `TEST_LOCAL_COMMIT_CREATION` | `C04_TEST_STATIC_ACCEPTED_NOT_MATERIALIZED` | `TEST_LOCAL_COMMIT_CREATION_ONLY` | `CLEAR_C04_TEST_LOCAL_COMMIT_CREATED` | `C04_TEST_LOCAL_COMMIT_CREATED_PENDING_REVIEW` | `GUSTAVO_MANUAL_INSTALLER` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `true` | `false` | 14 |
| `TEST_LOCAL_COMMIT_REVIEW` | `C04_TEST_LOCAL_COMMIT_CREATED_PENDING_REVIEW` | `NONE` | `CLEAR_C04_TEST_LOCAL_COMMIT_REVIEW_APPROVED` | `C04_TEST_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` | `SENTINEL` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 10 |
| `TEST_PUSH_AUTHORIZATION` | `C04_TEST_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` | `NONE` | `CLEAR_C04_TEST_PUSH_SEPARATELY_AUTHORIZED` | `C04_TEST_PUSH_AUTHORIZED_NOT_PUSHED` | `SENTINEL` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 7 |
| `TEST_FAST_FORWARD_PUSH` | `C04_TEST_PUSH_AUTHORIZED_NOT_PUSHED` | `TEST_PUSH_ONLY` | `CLEAR_C04_TEST_FAST_FORWARD_PUSH_COMPLETED` | `C04_TEST_PUSHED_PENDING_REMOTE_VERIFICATION` | `GUSTAVO_MANUAL_INSTALLER` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `true` | `false` | 13 |
| `TEST_REMOTE_INSTALLATION_VERIFICATION` | `C04_TEST_PUSHED_PENDING_REMOTE_VERIFICATION` | `NONE` | `CLEAR_C04_TEST_REMOTE_INSTALLATION_VERIFIED` | `C04_TEST_REMOTE_MATERIALIZED_VERIFIED` | `SENTINEL` | `tests/local_curl_per_side/test_canonical_i0a.py`<br>`tests/local_curl_per_side/test_claim_hashes_i0a.py`<br>`tests/local_curl_per_side/test_finding4_registry_i0a.py`<br>`tests/local_curl_per_side/test_governing_package_i0a.py`<br>`tests/local_curl_per_side/test_i0a_public_contract.py`<br>`tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `false` | `false` | `false` | 7 |
| `EXECUTION_AUTHORIZATION` | `C04_TEST_REMOTE_MATERIALIZED_VERIFIED` | `EXECUTION_ONLY` | `CLEAR_C04_EXECUTION_AUTHORIZATION_RECORDED_OUTSIDE_C04` | `C04_EXECUTION_AUTHORIZED_OUTSIDE_C04` | `SENTINEL` | <empty> | `false` | `false` | `false` | 8 |

## 8. Delivery separation

### 8.1 Source materialization delivery

1. `SOURCE_LOCAL_COMMIT_CREATION`
2. `SOURCE_LOCAL_COMMIT_REVIEW`
3. `SOURCE_PUSH_AUTHORIZATION`
4. `SOURCE_FAST_FORWARD_PUSH`
5. `SOURCE_REMOTE_INSTALLATION_VERIFICATION`

### 8.2 Test materialization delivery

1. `TEST_LOCAL_COMMIT_CREATION`
2. `TEST_LOCAL_COMMIT_REVIEW`
3. `TEST_PUSH_AUTHORIZATION`
4. `TEST_FAST_FORWARD_PUSH`
5. `TEST_REMOTE_INSTALLATION_VERIFICATION`

A local-commit authorization includes no push. Sentinel approval of a local commit includes no push. Push requires a separate exact Gustavo authorization and active Sentinel handoff.

If a fresh fetch shows the remote advanced, `STOP_C04_PUSH_REMOTE_ADVANCED` controls. No push or repair is permitted.

## 9. Candidate 04 documentation-installation boundary

Candidate 04 does not authorize or prescribe its own commit, merge, push, ref update, or remote mutation.

Documentation delivery mechanics are controlled exclusively by `project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`. `SPEC_CANONICAL_INSTALLATION_CONFIRMATION` only confirms the external workflow result.

## 10. Ordered predicates by stage

### 10.1 `SPEC_REVIEW`

From `C04_DRAFT_NOT_ACCEPTED` to `C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION` on `CLEAR_C04_SPEC_REVIEW_APPROVED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SPEC_REVIEW_STATE` | Current workflow state is exactly C04_DRAFT_NOT_ACCEPTED for stage SPEC_REVIEW. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SR01` | Candidate 04 package identity, complete member inventory, member checksums, and detached ZIP identity are exact. | `STOP_C04_SPEC_PACKAGE_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `SR02` | Canonical base is exactly bc957fe05096b790052d0515773b9e0a2dc88a60 and all controlling canonical identities are available. | `STOP_C04_SPEC_CANONICAL_BASE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `SR03` | The Candidate 03 architecture is preserved except for the two expressly authorized Candidate 04 corrections. | `STOP_C04_SPEC_SCOPE_DRIFT` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `SR04` | The accepted-scope supersession contract and exact twelve-path byte matrix are unchanged in substance. | `STOP_C04_SPEC_PRESERVED_CONTRACT_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `SR05` | WORKFLOW_HALT_RECORD.schema.json and WORKFLOW_SUCCESS_RECORD.schema.json are valid closed Draft 2020-12 JSON Schemas. | `STOP_C04_RECORD_SCHEMA_INVALID` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `SR06` | The normative cross-field record rules make any applicability-row or success-transition mismatch invalid. | `STOP_C04_RECORD_CROSS_FIELD_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 8 | `SR07` | The workflow separates local commit creation, Sentinel local review, separate push authorization, one non-force push, and Sentinel remote verification for both source and test materialization. | `STOP_C04_SPEC_WORKFLOW_DOMAIN_NOT_TOTAL` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 9 | `SR08` | Candidate 04 documentation delivery mechanics are deferred exclusively to project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md. | `STOP_C04_SPEC_DELIVERY_MECHANICS_NOT_EXTERNAL` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 10 | `SR09` | Every Markdown and JSON representation agrees on enums, states, stages, stops, successes, predicates, paths, schemas, and authorization fields. | `STOP_C04_SPEC_REPRESENTATION_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 11 | `SR10` | Sentinel decision is exactly APPROVE. | `STOP_C04_SPEC_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.2 `SPEC_CANONICAL_INSTALLATION_CONFIRMATION`

From `C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION` to `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED` on `CLEAR_C04_SPEC_CANONICAL_INSTALLATION_CONFIRMED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SPEC_CANONICAL_INSTALLATION_CONFIRMATION_STATE` | Current workflow state is exactly C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION for stage SPEC_CANONICAL_INSTALLATION_CONFIRMATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SCI01` | The exact Candidate 04 package has a prior Sentinel APPROVE decision. | `STOP_C04_SPEC_CANONICAL_INSTALLATION_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `SCI02` | The controlling project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md was used as the sole delivery-mechanics authority. | `STOP_C04_SPEC_DELIVERY_MECHANICS_NOT_EXTERNAL` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `SCI03` | A canonical installation record identifies the exact accepted Candidate 04 bytes and exact canonical installation commit. | `STOP_C04_SPEC_CANONICAL_INSTALLATION_RECORD_MISSING` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `SCI04` | Candidate 04 itself did not authorize or prescribe its own commit, merge, push, ref update, or remote mutation. | `STOP_C04_SPEC_SELF_AUTHORIZED_DELIVERY_ATTEMPT` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `SCI05` | No live source, test, data, dependency, runtime, or project artifact path changed during documentation installation. | `STOP_C04_SPEC_CANONICAL_INSTALLATION_LIVE_PATH_CHANGE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `SCI06` | Sentinel independently verified the exact documentation-only canonical installation. | `STOP_C04_SPEC_CANONICAL_INSTALLATION_NOT_VERIFIED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.3 `WORKSPACE_PREPARATION`

From `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED` to `C04_SOURCE_WORKSPACE_READY` on `CLEAR_C04_SOURCE_WORKSPACE_PREPARED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `WORKSPACE_PREPARATION_STATE` | Current workflow state is exactly C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED for stage WORKSPACE_PREPARATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `WP01` | A distinct Gustavo workspace-preparation authorization and active Sentinel handoff exist for the exact canonically installed Candidate 04 identity. | `STOP_C04_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `WP02` | Canonical HEAD equals the exact HEAD selected by that active handoff. | `STOP_C04_CANONICAL_HEAD_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 4 | `WP03` | All controlling Revision 10, remediation, capture, Candidate 04, and failed-gate records are exact and readable. | `STOP_C04_CONTROLLING_CONTRACT_UNAVAILABLE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `WP04` | The accepted capture archive identity and acceptance/installation identities are exact. | `STOP_C04_CAPTURE_PACKAGE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 6 | `WP05` | The capture contains exactly the twelve declared relative paths exactly once. | `STOP_C04_CAPTURE_PATH_SET_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 7 | `WP06` | All twelve capture sizes and SHA-256 values match the exact matrix. | `STOP_C04_CAPTURE_BYTE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 8 | `WP07` | The Windows staging root is outside every Git checkout/worktree and contains no Git metadata. | `STOP_C04_WORKSPACE_ROOT_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 9 | `WP08` | The staging root has zero members before instantiation. | `STOP_C04_WORKSPACE_NOT_EMPTY` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 10 | `WP09` | Each instantiated member is a regular file at its exact relative path with exact size and SHA-256. | `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 11 | `WP10` | No member or ancestor is a symlink, junction, reparse-point alias, alternate path alias, or hard-link substitution. | `STOP_C04_WORKSPACE_ALIAS_OR_LINK_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 12 | `WP11` | After instantiation, the workspace has exactly twelve members and no extra or missing path. | `STOP_C04_WORKSPACE_EXTRA_OR_MISSING_PATH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 13 | `WP12` | All three mandatory source files and all nine read-only paths are available with exact identities. | `STOP_C04_MANDATORY_FILE_UNAVAILABLE` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 14 | `WP13` | No thirteenth workspace member or repository file is required. | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 15 | `WP14` | No old failed-gate predicate, result, authorization ID, or inactive handoff is reused or represented as clear. | `STOP_C04_FAILED_GATE_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 16 | `WP15` | No decision depends on trusting incomplete multi-round lineage. | `STOP_C04_TRUSTED_MULTI_ROUND_LINEAGE_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 17 | `WP16` | No Git write occurs. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 18 | `WP17` | No test, import, compilation, project execution, data access, network activity, or project artifact generation occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

### 10.4 `SOURCE_AUTHORING`

From `C04_SOURCE_WORKSPACE_READY` to `C04_SOURCE_CANDIDATE_SUBMITTED` on `CLEAR_C04_SOURCE_CANDIDATE_SUBMITTED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_AUTHORING_STATE` | Current workflow state is exactly C04_SOURCE_WORKSPACE_READY for stage SOURCE_AUTHORING. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SA01` | A distinct source-authoring authorization and active Sentinel handoff name the exact gated workspace. | `STOP_C04_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `SA02` | All twelve workspace members still match the gated starting identities before write opening. | `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 4 | `SA03` | Exactly canonical.py, finding4_registry.py, and prepared_evidence.py are writable. | `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 5 | `SA04` | All nine protected paths remain byte-identical and no baseline-support path is edited. | `STOP_C04_READ_ONLY_PATH_MUTATED` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 6 | `SA05` | No new workspace member, repository file, dependency, configuration, export, fixture, documentation path, or adjacent path is required. | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `SA06` | No source/test boundary violation occurs. | `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 8 | `SA07` | No Git write occurs. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 9 | `SA08` | No test, import, compilation, project execution, data access, network activity, or project artifact generation occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 10 | `SA09` | No implementation choice depends on trusted multi-round lineage. | `STOP_C04_TRUSTED_MULTI_ROUND_LINEAGE_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 11 | `SA10` | All three writable files are returned, each ending hash differs from its start, and all eight remediation defects are addressed atomically. | `STOP_C04_ATOMIC_SOURCE_RESULT_UNAVAILABLE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 12 | `SA11` | The source review package contains exact starts, ends, nine unchanged identities, three payloads, requirement mapping, activity declarations, checksums, and detached archive identity. | `STOP_C04_SOURCE_CANDIDATE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `CLAUDE` |

### 10.5 `SOURCE_STATIC_REVIEW`

From `C04_SOURCE_CANDIDATE_SUBMITTED` to `C04_SOURCE_STATIC_ACCEPTED_NOT_MATERIALIZED` on `CLEAR_C04_SOURCE_STATIC_REVIEW_APPROVED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_STATIC_REVIEW_STATE` | Current workflow state is exactly C04_SOURCE_CANDIDATE_SUBMITTED for stage SOURCE_STATIC_REVIEW. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SSR01` | The submitted source package identity and checksum closure are exact. | `STOP_C04_SOURCE_CANDIDATE_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `SSR02` | The changed-path set is exactly the three mandatory source paths and all nine protected paths are unchanged. | `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `SSR03` | All eight verified Revision 10 defects are statically satisfied in the same candidate. | `STOP_C04_ATOMIC_SOURCE_RESULT_UNAVAILABLE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `SSR04` | No prohibited new file, dependency, configuration, export, fixture, adjacent refactor, or baseline-support edit is present. | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `SSR05` | The activity report establishes no Git write, execution, test, import, data, network, or project artifact activity. | `STOP_C04_SOURCE_CANDIDATE_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `SSR06` | The package makes no checkpoint-acceptance or lineage-closure claim. | `STOP_C04_TRUSTED_MULTI_ROUND_LINEAGE_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 8 | `SSR07` | Sentinel decision is exactly APPROVE. | `STOP_C04_SOURCE_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.6 `SOURCE_LOCAL_COMMIT_CREATION`

From `C04_SOURCE_STATIC_ACCEPTED_NOT_MATERIALIZED` to `C04_SOURCE_LOCAL_COMMIT_CREATED_PENDING_REVIEW` on `CLEAR_C04_SOURCE_LOCAL_COMMIT_CREATED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_LOCAL_COMMIT_CREATION_STATE` | Current workflow state is exactly C04_SOURCE_STATIC_ACCEPTED_NOT_MATERIALIZED for stage SOURCE_LOCAL_COMMIT_CREATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SLC01` | A separate Gustavo authorization and active Sentinel handoff authorize only local source materialization commit creation for the exact Sentinel-approved source candidate. | `STOP_C04_LOCAL_COMMIT_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `SLC02` | The exact source candidate has a prior Sentinel APPROVE decision and its byte identities remain unchanged. | `STOP_C04_SOURCE_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `SLC03` | The local repository, branch, clean worktree, authorized parent commit, and local HEAD match the exact local-commit package. | `STOP_C04_LOCAL_COMMIT_BASE_OR_BRANCH_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `GUSTAVO_MANUAL_INSTALLER` |
| 5 | `SLC04` | All six canonical source targets are absent from the authorized parent tree, local index, and local worktree before materialization. | `STOP_C04_MATERIALIZATION_TARGET_PRESENT` | `SENTINEL` | `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED` | `SENTINEL` |
| 6 | `SLC05` | The materialization set is exactly six source CREATE actions and contains no test or extra path. | `STOP_C04_MATERIALIZATION_PATH_SET_MISMATCH` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 7 | `SLC06` | The three mandatory source files match the Sentinel-approved final bytes and the three support files match the exact accepted capture bytes. | `STOP_C04_MATERIALIZATION_BYTE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `GUSTAVO_MANUAL_INSTALLER` |
| 8 | `SLC07` | All six created source paths are Git regular files with mode 100644. | `STOP_C04_MATERIALIZATION_GIT_MODE_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `GUSTAVO_MANUAL_INSTALLER` |
| 9 | `SLC08` | The five baseline-support paths remain unedited; only exact-byte creation is performed for the three source support paths. | `STOP_C04_READ_ONLY_PATH_MUTATED` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 10 | `SLC09` | Exactly one ordinary non-merge local commit is created with the exact authorized parent and exactly six source CREATE entries. | `STOP_C04_LOCAL_COMMIT_IDENTITY_MISMATCH` | `SENTINEL` | `MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 11 | `SLC10` | The worktree and index are clean after local commit creation. | `STOP_C04_LOCAL_COMMIT_WORKTREE_NOT_CLEAN` | `SENTINEL` | `MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 12 | `SLC11` | No push, pull, merge, rebase, reset, restore, rollback, checkout repair, force action, or automatic repair occurs. | `STOP_C04_LOCAL_COMMIT_PROHIBITED_OPERATION` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 13 | `SLC12` | Git writes are performed only by Gustavo's manual installer under the exact local-commit authorization. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 14 | `SLC13` | No test, import, compilation, project execution, data access, network activity, or project artifact generation occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

### 10.7 `SOURCE_LOCAL_COMMIT_REVIEW`

From `C04_SOURCE_LOCAL_COMMIT_CREATED_PENDING_REVIEW` to `C04_SOURCE_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` on `CLEAR_C04_SOURCE_LOCAL_COMMIT_REVIEW_APPROVED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_LOCAL_COMMIT_REVIEW_STATE` | Current workflow state is exactly C04_SOURCE_LOCAL_COMMIT_CREATED_PENDING_REVIEW for stage SOURCE_LOCAL_COMMIT_REVIEW. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SLR01` | The submitted local source commit SHA is exact and identifies the same bytes produced by the authorized local-commit stage. | `STOP_C04_LOCAL_COMMIT_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `SLR02` | The local commit has exactly one parent equal to the authorized parent and is not a merge commit. | `STOP_C04_LOCAL_COMMIT_PARENT_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `SLR03` | The reviewed local branch is the exact branch named by the local-commit package. | `STOP_C04_LOCAL_COMMIT_BASE_OR_BRANCH_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `SLR04` | The commit changes exactly six source paths, each with status A, and no other path. | `STOP_C04_PUSH_CHANGED_PATHS_OR_STATUSES_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `SLR05` | The committed source bytes and Git modes exactly match the authorized materialization identities. | `STOP_C04_PUSH_BYTE_OR_MODE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `SLR06` | The local worktree and index are clean and local HEAD equals the submitted commit. | `STOP_C04_LOCAL_COMMIT_WORKTREE_NOT_CLEAN` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 8 | `SLR07` | No push has occurred and no remote ref is claimed to contain the local commit. | `STOP_C04_LOCAL_COMMIT_PUSH_OCCURRED` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 9 | `SLR08` | The review evidence contains no pull, merge, rebase, reset, restore, rollback, force, or automatic-repair operation. | `STOP_C04_LOCAL_COMMIT_PROHIBITED_OPERATION` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 10 | `SLR09` | Sentinel decision on the exact local source commit is exactly APPROVE. | `STOP_C04_LOCAL_COMMIT_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.8 `SOURCE_PUSH_AUTHORIZATION`

From `C04_SOURCE_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` to `C04_SOURCE_PUSH_AUTHORIZED_NOT_PUSHED` on `CLEAR_C04_SOURCE_PUSH_SEPARATELY_AUTHORIZED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_PUSH_AUTHORIZATION_STATE` | Current workflow state is exactly C04_SOURCE_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED for stage SOURCE_PUSH_AUTHORIZATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SPA01` | The exact local source commit has a prior Sentinel APPROVE decision. | `STOP_C04_LOCAL_COMMIT_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `SPA02` | Gustavo separately authorizes exactly one push of the exact reviewed local commit; no local-commit or review authorization is reused. | `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 4 | `SPA03` | The push authorization pins the exact local commit SHA, exact parent and remote base, exact branch, exact refspec, six A-status paths, committed byte hashes, and Git modes. | `STOP_C04_PUSH_AUTHORIZATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 5 | `SPA04` | The push authorization permits force=false, one ordinary fast-forward push, and only the read-only fetch needed for the push gate. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 6 | `SPA05` | The push authorization prohibits pull, merge, rebase, reset, restore, rollback, checkout repair, branch rewrite, and automatic repair. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 7 | `SPA06` | Sentinel issues an active push handoff containing the exact authorization identity and all pinned push facts. | `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.9 `SOURCE_FAST_FORWARD_PUSH`

From `C04_SOURCE_PUSH_AUTHORIZED_NOT_PUSHED` to `C04_SOURCE_PUSHED_PENDING_REMOTE_VERIFICATION` on `CLEAR_C04_SOURCE_FAST_FORWARD_PUSH_COMPLETED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_FAST_FORWARD_PUSH_STATE` | Current workflow state is exactly C04_SOURCE_PUSH_AUTHORIZED_NOT_PUSHED for stage SOURCE_FAST_FORWARD_PUSH. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SFP01` | The separate source push authorization and active Sentinel push handoff are exact and currently active. | `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `SFP02` | Local HEAD equals the exact reviewed local source commit SHA. | `STOP_C04_PUSH_COMMIT_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 4 | `SFP03` | The local branch and exact push refspec equal the authorization. | `STOP_C04_PUSH_BRANCH_REFSPEC_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 5 | `SFP04` | The local commit has the exact authorized parent, six A-status source paths, committed bytes, and Git modes. | `STOP_C04_PUSH_CHANGED_PATHS_OR_STATUSES_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 6 | `SFP05` | The local worktree and index are clean. | `STOP_C04_PUSH_WORKTREE_NOT_CLEAN` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 7 | `SFP06` | A fresh fetch shows the exact remote branch still equals the authorized parent/remote base. | `STOP_C04_PUSH_REMOTE_ADVANCED` | `SENTINEL` | `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED` | `SENTINEL` |
| 8 | `SFP07` | After the fresh fetch, local is exactly one commit ahead and zero commits behind the authorized remote branch. | `STOP_C04_PUSH_AHEAD_BEHIND_MISMATCH` | `SENTINEL` | `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED` | `SENTINEL` |
| 9 | `SFP08` | Force is disabled and no pull, merge, rebase, reset, restore, rollback, checkout repair, or automatic repair is attempted. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 10 | `SFP09` | Exactly one ordinary non-force fast-forward push is issued for the exact refspec. | `STOP_C04_PUSH_FAILED` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 11 | `SFP10` | The push reports success without rejection, non-fast-forward handling, ref rewrite, or additional ref update. | `STOP_C04_PUSH_FAILED` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 12 | `SFP11` | No project test, import, compilation, execution, data access, project artifact generation, or network activity beyond the authorized fetch and push occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 13 | `SFP12` | Git writes are limited to the exact authorized push; no other local or remote Git mutation occurs. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

### 10.10 `SOURCE_REMOTE_INSTALLATION_VERIFICATION`

From `C04_SOURCE_PUSHED_PENDING_REMOTE_VERIFICATION` to `C04_SOURCE_REMOTE_MATERIALIZED_VERIFIED` on `CLEAR_C04_SOURCE_REMOTE_INSTALLATION_VERIFIED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `SOURCE_REMOTE_INSTALLATION_VERIFICATION_STATE` | Current workflow state is exactly C04_SOURCE_PUSHED_PENDING_REMOTE_VERIFICATION for stage SOURCE_REMOTE_INSTALLATION_VERIFICATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `SRV01` | The canonical remote branch head equals the exact reviewed and authorized local source commit SHA. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `SRV02` | The remote commit has the exact authorized parent and forms one ordinary fast-forward commit from the authorized remote base. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `SRV03` | The remote commit changes exactly six source paths with status A and no test or extra path. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `SRV04` | All six remote source bytes and Git modes exactly match the Sentinel-reviewed local commit. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `SRV05` | No force update, merge, rebase, rewritten parent, extra commit, extra ref, or automatic repair is present. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `SRV06` | Sentinel independently verifies the exact canonical remote installation. | `STOP_C04_REMOTE_INSTALLATION_NOT_VERIFIED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.11 `TEST_SCOPE_REVIEW`

From `C04_SOURCE_REMOTE_MATERIALIZED_VERIFIED` to `C04_TEST_SCOPE_ACCEPTED_NOT_AUTHORIZED` on `CLEAR_C04_TEST_SCOPE_REVIEW_APPROVED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_SCOPE_REVIEW_STATE` | Current workflow state is exactly C04_SOURCE_REMOTE_MATERIALIZED_VERIFIED for stage TEST_SCOPE_REVIEW. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TSR01` | The proposed test scope names exactly four writable test paths, two test support paths, and all six source paths as read-only. | `STOP_C04_TEST_SCOPE_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `TSR02` | Test obligations cover every accepted Revision 10 and remediation requirement, including negative, precedence, and false-unblock cases. | `STOP_C04_TEST_SCOPE_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `TSR03` | Allowed new repository files remains NONE during test workspace preparation and authoring. | `STOP_C04_SPEC_SUPERSESSION_INCOMPLETE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `TSR04` | No test execution, source edit, dependency, configuration, fixture relocation, or extra path is included. | `STOP_C04_TEST_SCOPE_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `TSR05` | All test-scope Markdown and JSON representations agree. | `STOP_C04_SPEC_REPRESENTATION_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `TSR06` | Sentinel decision is exactly APPROVE. | `STOP_C04_TEST_SCOPE_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.12 `TEST_WORKSPACE_PREPARATION`

From `C04_TEST_SCOPE_ACCEPTED_NOT_AUTHORIZED` to `C04_TEST_WORKSPACE_READY` on `CLEAR_C04_TEST_WORKSPACE_PREPARED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_WORKSPACE_PREPARATION_STATE` | Current workflow state is exactly C04_TEST_SCOPE_ACCEPTED_NOT_AUTHORIZED for stage TEST_WORKSPACE_PREPARATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TWP01` | A distinct Gustavo test-workspace authorization and active Sentinel handoff exist. | `STOP_C04_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `TWP02` | Canonical HEAD and six installed source identities equal the Sentinel-verified source installation. | `STOP_C04_TEST_WORKSPACE_SOURCE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 4 | `TWP03` | The accepted test scope and Candidate 04 identities are exact and readable. | `STOP_C04_CONTROLLING_CONTRACT_UNAVAILABLE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `TWP04` | The accepted capture supplies exactly six declared test starting paths with exact sizes and hashes. | `STOP_C04_CAPTURE_BYTE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 6 | `TWP05` | The Windows staging root is outside every Git checkout/worktree and contains no Git metadata. | `STOP_C04_WORKSPACE_ROOT_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 7 | `TWP06` | The staging root has zero members before instantiation. | `STOP_C04_WORKSPACE_NOT_EMPTY` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 8 | `TWP07` | Six exact installed source files and six exact captured test files are instantiated as regular files with exact paths, sizes, and hashes. | `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 9 | `TWP08` | No symlink, junction, reparse-point alias, alternate path alias, or hard-link substitution exists. | `STOP_C04_WORKSPACE_ALIAS_OR_LINK_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 10 | `TWP09` | The test workspace has exactly twelve members and no extra or missing path. | `STOP_C04_WORKSPACE_EXTRA_OR_MISSING_PATH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 11 | `TWP10` | Exactly four test paths are designated writable and the other eight paths are designated read-only. | `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 12 | `TWP11` | No thirteenth member or repository file is required. | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 13 | `TWP12` | No failed-gate repair or trusted multi-round lineage is required. | `STOP_C04_FAILED_GATE_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 14 | `TWP13` | No Git write occurs. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 15 | `TWP14` | No test collection/execution, import, compilation, project execution, data, network, or project artifact activity occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

### 10.13 `TEST_AUTHORING`

From `C04_TEST_WORKSPACE_READY` to `C04_TEST_CANDIDATE_SUBMITTED` on `CLEAR_C04_TEST_CANDIDATE_SUBMITTED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_AUTHORING_STATE` | Current workflow state is exactly C04_TEST_WORKSPACE_READY for stage TEST_AUTHORING. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TA01` | A distinct test-authoring authorization and active Sentinel handoff name the exact gated test workspace. | `STOP_C04_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `TA02` | All twelve members still match the gated starts before write opening. | `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `SENTINEL` |
| 4 | `TA03` | Exactly the four mandatory test paths are writable. | `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 5 | `TA04` | All six source paths and two support-test paths remain byte-identical. | `STOP_C04_READ_ONLY_PATH_MUTATED` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 6 | `TA05` | No new member, repository file, fixture path, dependency, configuration, or adjacent path is required. | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `TA06` | No Git write occurs. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 8 | `TA07` | No test collection/execution, project import, compilation, project execution, data, network, or project artifact activity occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 9 | `TA08` | All four writable test files are returned with changed ending hashes and the complete accepted test obligations. | `STOP_C04_TEST_AUTHORING_RESULT_UNAVAILABLE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 10 | `TA09` | The test review package contains exact starts, ends, eight unchanged identities, four payloads, obligation mapping, activity declarations, checksums, and detached archive identity. | `STOP_C04_TEST_CANDIDATE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `CLAUDE` |

### 10.14 `TEST_STATIC_REVIEW`

From `C04_TEST_CANDIDATE_SUBMITTED` to `C04_TEST_STATIC_ACCEPTED_NOT_MATERIALIZED` on `CLEAR_C04_TEST_STATIC_REVIEW_APPROVED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_STATIC_REVIEW_STATE` | Current workflow state is exactly C04_TEST_CANDIDATE_SUBMITTED for stage TEST_STATIC_REVIEW. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TST01` | The test candidate identity and checksum closure are exact. | `STOP_C04_TEST_CANDIDATE_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `TST02` | The changed-path set is exactly four mandatory test paths and all eight protected paths are unchanged. | `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `TST03` | The tests statically cover all accepted obligations, negative cases, precedence, ownership, and false-unblock boundaries. | `STOP_C04_TEST_AUTHORING_RESULT_UNAVAILABLE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `TST04` | No test was collected or executed and no project module was imported or executed. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `TST05` | No prohibited new file, fixture location, dependency, configuration, source edit, or baseline-support edit is present. | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `TST06` | Sentinel decision is exactly APPROVE. | `STOP_C04_TEST_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.15 `TEST_LOCAL_COMMIT_CREATION`

From `C04_TEST_STATIC_ACCEPTED_NOT_MATERIALIZED` to `C04_TEST_LOCAL_COMMIT_CREATED_PENDING_REVIEW` on `CLEAR_C04_TEST_LOCAL_COMMIT_CREATED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_LOCAL_COMMIT_CREATION_STATE` | Current workflow state is exactly C04_TEST_STATIC_ACCEPTED_NOT_MATERIALIZED for stage TEST_LOCAL_COMMIT_CREATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TLC01` | A separate Gustavo authorization and active Sentinel handoff authorize only local test materialization commit creation for the exact Sentinel-approved test candidate. | `STOP_C04_LOCAL_COMMIT_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `TLC02` | The exact test candidate has a prior Sentinel APPROVE decision and the six installed source identities remain unchanged. | `STOP_C04_TEST_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `TLC03` | The local repository, branch, clean worktree, authorized parent commit, and local HEAD match the exact local test-commit package. | `STOP_C04_LOCAL_COMMIT_BASE_OR_BRANCH_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `GUSTAVO_MANUAL_INSTALLER` |
| 5 | `TLC04` | All six canonical test targets are absent from the authorized parent tree, local index, and local worktree before materialization. | `STOP_C04_MATERIALIZATION_TARGET_PRESENT` | `SENTINEL` | `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED` | `SENTINEL` |
| 6 | `TLC05` | The materialization set is exactly six test CREATE actions and contains no source or extra path. | `STOP_C04_MATERIALIZATION_PATH_SET_MISMATCH` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 7 | `TLC06` | The four mandatory test files match the Sentinel-approved final bytes and the two support files match the exact accepted capture bytes. | `STOP_C04_MATERIALIZATION_BYTE_IDENTITY_MISMATCH` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `GUSTAVO_MANUAL_INSTALLER` |
| 8 | `TLC07` | All six created test paths are Git regular files with mode 100644. | `STOP_C04_MATERIALIZATION_GIT_MODE_INVALID` | `SENTINEL` | `SAME_AUTHORIZATION_FRESH_GATE` | `GUSTAVO_MANUAL_INSTALLER` |
| 9 | `TLC08` | The five baseline-support paths remain unedited; only exact-byte creation is performed for the two test support paths. | `STOP_C04_READ_ONLY_PATH_MUTATED` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 10 | `TLC09` | Exactly one ordinary non-merge local commit is created with the exact authorized parent and exactly six test CREATE entries. | `STOP_C04_LOCAL_COMMIT_IDENTITY_MISMATCH` | `SENTINEL` | `MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 11 | `TLC10` | The worktree and index are clean after local commit creation. | `STOP_C04_LOCAL_COMMIT_WORKTREE_NOT_CLEAN` | `SENTINEL` | `MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION` | `GUSTAVO_MANUAL_INSTALLER` |
| 12 | `TLC11` | No push, pull, merge, rebase, reset, restore, rollback, checkout repair, force action, or automatic repair occurs. | `STOP_C04_LOCAL_COMMIT_PROHIBITED_OPERATION` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 13 | `TLC12` | Git writes are performed only by Gustavo's manual installer under the exact local-commit authorization. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 14 | `TLC13` | No test collection/execution, import, compilation, project execution, data access, network activity, or project artifact generation occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

### 10.16 `TEST_LOCAL_COMMIT_REVIEW`

From `C04_TEST_LOCAL_COMMIT_CREATED_PENDING_REVIEW` to `C04_TEST_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` on `CLEAR_C04_TEST_LOCAL_COMMIT_REVIEW_APPROVED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_LOCAL_COMMIT_REVIEW_STATE` | Current workflow state is exactly C04_TEST_LOCAL_COMMIT_CREATED_PENDING_REVIEW for stage TEST_LOCAL_COMMIT_REVIEW. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TLR01` | The submitted local test commit SHA is exact and identifies the same bytes produced by the authorized local-commit stage. | `STOP_C04_LOCAL_COMMIT_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `TLR02` | The local commit has exactly one parent equal to the authorized parent and is not a merge commit. | `STOP_C04_LOCAL_COMMIT_PARENT_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `TLR03` | The reviewed local branch is the exact branch named by the local-commit package. | `STOP_C04_LOCAL_COMMIT_BASE_OR_BRANCH_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `TLR04` | The commit changes exactly six test paths, each with status A, and no source or extra path. | `STOP_C04_PUSH_CHANGED_PATHS_OR_STATUSES_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `TLR05` | The committed test bytes and Git modes exactly match the authorized materialization identities; all six source paths remain unchanged. | `STOP_C04_PUSH_BYTE_OR_MODE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `TLR06` | The local worktree and index are clean and local HEAD equals the submitted commit. | `STOP_C04_LOCAL_COMMIT_WORKTREE_NOT_CLEAN` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 8 | `TLR07` | No push has occurred and no remote ref is claimed to contain the local commit. | `STOP_C04_LOCAL_COMMIT_PUSH_OCCURRED` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 9 | `TLR08` | The review evidence contains no pull, merge, rebase, reset, restore, rollback, force, or automatic-repair operation. | `STOP_C04_LOCAL_COMMIT_PROHIBITED_OPERATION` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 10 | `TLR09` | Sentinel decision on the exact local test commit is exactly APPROVE. | `STOP_C04_LOCAL_COMMIT_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.17 `TEST_PUSH_AUTHORIZATION`

From `C04_TEST_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED` to `C04_TEST_PUSH_AUTHORIZED_NOT_PUSHED` on `CLEAR_C04_TEST_PUSH_SEPARATELY_AUTHORIZED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_PUSH_AUTHORIZATION_STATE` | Current workflow state is exactly C04_TEST_LOCAL_COMMIT_REVIEWED_NOT_PUSH_AUTHORIZED for stage TEST_PUSH_AUTHORIZATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TPA01` | The exact local test commit has a prior Sentinel APPROVE decision. | `STOP_C04_LOCAL_COMMIT_REVIEW_NOT_APPROVED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `TPA02` | Gustavo separately authorizes exactly one push of the exact reviewed local test commit; no local-commit or review authorization is reused. | `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 4 | `TPA03` | The push authorization pins the exact local commit SHA, exact parent and remote base, exact branch, exact refspec, six A-status paths, committed byte hashes, and Git modes. | `STOP_C04_PUSH_AUTHORIZATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 5 | `TPA04` | The push authorization permits force=false, one ordinary fast-forward push, and only the read-only fetch needed for the push gate. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 6 | `TPA05` | The push authorization prohibits pull, merge, rebase, reset, restore, rollback, checkout repair, branch rewrite, and automatic repair. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 7 | `TPA06` | Sentinel issues an active push handoff containing the exact authorization identity and all pinned push facts. | `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.18 `TEST_FAST_FORWARD_PUSH`

From `C04_TEST_PUSH_AUTHORIZED_NOT_PUSHED` to `C04_TEST_PUSHED_PENDING_REMOTE_VERIFICATION` on `CLEAR_C04_TEST_FAST_FORWARD_PUSH_COMPLETED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_FAST_FORWARD_PUSH_STATE` | Current workflow state is exactly C04_TEST_PUSH_AUTHORIZED_NOT_PUSHED for stage TEST_FAST_FORWARD_PUSH. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TFP01` | The separate test push authorization and active Sentinel push handoff are exact and currently active. | `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `GUSTAVO` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 3 | `TFP02` | Local HEAD equals the exact reviewed local test commit SHA. | `STOP_C04_PUSH_COMMIT_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 4 | `TFP03` | The local branch and exact push refspec equal the authorization. | `STOP_C04_PUSH_BRANCH_REFSPEC_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 5 | `TFP04` | The local commit has the exact authorized parent, six A-status test paths, committed bytes, and Git modes; source paths remain unchanged. | `STOP_C04_PUSH_CHANGED_PATHS_OR_STATUSES_MISMATCH` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 6 | `TFP05` | The local worktree and index are clean. | `STOP_C04_PUSH_WORKTREE_NOT_CLEAN` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 7 | `TFP06` | A fresh fetch shows the exact remote branch still equals the authorized parent/remote base. | `STOP_C04_PUSH_REMOTE_ADVANCED` | `SENTINEL` | `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED` | `SENTINEL` |
| 8 | `TFP07` | After the fresh fetch, local is exactly one commit ahead and zero commits behind the authorized remote branch. | `STOP_C04_PUSH_AHEAD_BEHIND_MISMATCH` | `SENTINEL` | `FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED` | `SENTINEL` |
| 9 | `TFP08` | Force is disabled and no pull, merge, rebase, reset, restore, rollback, checkout repair, or automatic repair is attempted. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 10 | `TFP09` | Exactly one ordinary non-force fast-forward push is issued for the exact refspec. | `STOP_C04_PUSH_FAILED` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 11 | `TFP10` | The push reports success without rejection, non-fast-forward handling, ref rewrite, or additional ref update. | `STOP_C04_PUSH_FAILED` | `SENTINEL` | `NEW_PUSH_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 12 | `TFP11` | No test collection/execution, import, compilation, project execution, data access, project artifact generation, or network activity beyond the authorized fetch and push occurs. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 13 | `TFP12` | Git writes are limited to the exact authorized push; no other local or remote Git mutation occurs. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

### 10.19 `TEST_REMOTE_INSTALLATION_VERIFICATION`

From `C04_TEST_PUSHED_PENDING_REMOTE_VERIFICATION` to `C04_TEST_REMOTE_MATERIALIZED_VERIFIED` on `CLEAR_C04_TEST_REMOTE_INSTALLATION_VERIFIED`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `TEST_REMOTE_INSTALLATION_VERIFICATION_STATE` | Current workflow state is exactly C04_TEST_PUSHED_PENDING_REMOTE_VERIFICATION for stage TEST_REMOTE_INSTALLATION_VERIFICATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `TRV01` | The canonical remote branch head equals the exact reviewed and authorized local test commit SHA. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `TRV02` | The remote commit has the exact authorized parent and forms one ordinary fast-forward commit from the authorized remote base. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `TRV03` | The remote commit changes exactly six test paths with status A and no source or extra path. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 5 | `TRV04` | All six remote test bytes and Git modes exactly match the Sentinel-reviewed local commit; all source identities remain unchanged. | `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `TRV05` | No force update, merge, rebase, rewritten parent, extra commit, extra ref, or automatic repair is present. | `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `TRV06` | Sentinel independently verifies the exact canonical remote installation. | `STOP_C04_REMOTE_INSTALLATION_NOT_VERIFIED` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |

### 10.20 `EXECUTION_AUTHORIZATION`

From `C04_TEST_REMOTE_MATERIALIZED_VERIFIED` to `C04_EXECUTION_AUTHORIZED_OUTSIDE_C04` on `CLEAR_C04_EXECUTION_AUTHORIZATION_RECORDED_OUTSIDE_C04`.

| Ordinal | Predicate ID | Condition required for clear | Stop code on failure | Decision owner | Retry eligibility | Retry owner |
|---:|---|---|---|---|---|---|
| 1 | `EXECUTION_AUTHORIZATION_STATE` | Current workflow state is exactly C04_TEST_REMOTE_MATERIALIZED_VERIFIED for stage EXECUTION_AUTHORIZATION. | `STOP_C04_STAGE_STATE_MISMATCH` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 2 | `EA01` | Source and test installations are both Sentinel-verified and exact. | `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 3 | `EA02` | A separate execution specification names exact commands, environment, limits, inputs, outputs, and prohibited activities. | `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 4 | `EA03` | Gustavo separately authorizes that exact execution specification. | `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE` | `GUSTAVO` | `NEW_GUSTAVO_AUTHORIZATION_REQUIRED` | `GUSTAVO` |
| 5 | `EA04` | Sentinel issues an active execution handoff distinct from Candidate 04. | `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 6 | `EA05` | No data, network, credential, artifact, downstream, or Git-write authority is inferred unless the separate execution specification explicitly and validly names it. | `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE` | `SENTINEL` | `NEW_SENTINEL_DECISION_REQUIRED` | `SENTINEL` |
| 7 | `EA06` | No test or project execution occurred before the separate execution authorization became active. | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |
| 8 | `EA07` | No unauthorized Git write occurred. | `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `SENTINEL` | `NO_RETRY_UNDER_SAME_AUTHORIZATION` | `GUSTAVO` |

## 11. Complete stop-code applicability table

| Stop code | Exact applications: stage / predicate / ordinal / decision owner / retry eligibility / retry owner |
|---|---|
| `STOP_C04_ATOMIC_SOURCE_RESULT_UNAVAILABLE` | `SOURCE_AUTHORING/SA10/11/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_STATIC_REVIEW/SSR03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_AUTHORIZATION_NOT_ACTIVE` | `WORKSPACE_PREPARATION/WP01/2/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO`; `SOURCE_AUTHORING/SA01/2/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_WORKSPACE_PREPARATION/TWP01/2/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_AUTHORING/TA01/2/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_CANONICAL_HEAD_MISMATCH` | `WORKSPACE_PREPARATION/WP02/3/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_CAPTURE_BYTE_IDENTITY_MISMATCH` | `WORKSPACE_PREPARATION/WP06/7/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP04/5/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_CAPTURE_PACKAGE_IDENTITY_MISMATCH` | `WORKSPACE_PREPARATION/WP04/5/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_CAPTURE_PATH_SET_MISMATCH` | `WORKSPACE_PREPARATION/WP05/6/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_CONTROLLING_CONTRACT_UNAVAILABLE` | `WORKSPACE_PREPARATION/WP03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_EXECUTION_AUTHORIZATION_INCOMPLETE` | `EXECUTION_AUTHORIZATION/EA01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `EXECUTION_AUTHORIZATION/EA02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `EXECUTION_AUTHORIZATION/EA03/4/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO`; `EXECUTION_AUTHORIZATION/EA04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `EXECUTION_AUTHORIZATION/EA05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_FAILED_GATE_REPAIR_ATTEMPT` | `WORKSPACE_PREPARATION/WP14/15/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP12/13/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_LOCAL_COMMIT_AUTHORIZATION_NOT_ACTIVE` | `SOURCE_LOCAL_COMMIT_CREATION/SLC01/2/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_LOCAL_COMMIT_CREATION/TLC01/2/GUSTAVO/NEW_GUSTAVO_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_LOCAL_COMMIT_BASE_OR_BRANCH_MISMATCH` | `SOURCE_LOCAL_COMMIT_CREATION/SLC03/4/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/GUSTAVO_MANUAL_INSTALLER`; `SOURCE_LOCAL_COMMIT_REVIEW/SLR03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC03/4/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/GUSTAVO_MANUAL_INSTALLER`; `TEST_LOCAL_COMMIT_REVIEW/TLR03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_LOCAL_COMMIT_IDENTITY_MISMATCH` | `SOURCE_LOCAL_COMMIT_CREATION/SLC09/10/SENTINEL/MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER`; `SOURCE_LOCAL_COMMIT_REVIEW/SLR01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC09/10/SENTINEL/MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER`; `TEST_LOCAL_COMMIT_REVIEW/TLR01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_LOCAL_COMMIT_PARENT_MISMATCH` | `SOURCE_LOCAL_COMMIT_REVIEW/SLR02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_REVIEW/TLR02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_LOCAL_COMMIT_PROHIBITED_OPERATION` | `SOURCE_LOCAL_COMMIT_CREATION/SLC11/12/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_LOCAL_COMMIT_REVIEW/SLR08/9/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC11/12/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_LOCAL_COMMIT_REVIEW/TLR08/9/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_LOCAL_COMMIT_PUSH_OCCURRED` | `SOURCE_LOCAL_COMMIT_REVIEW/SLR07/8/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_LOCAL_COMMIT_REVIEW/TLR07/8/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO` |
| `STOP_C04_LOCAL_COMMIT_REVIEW_NOT_APPROVED` | `SOURCE_LOCAL_COMMIT_REVIEW/SLR09/10/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_PUSH_AUTHORIZATION/SPA01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_REVIEW/TLR09/10/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_PUSH_AUTHORIZATION/TPA01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_LOCAL_COMMIT_WORKTREE_NOT_CLEAN` | `SOURCE_LOCAL_COMMIT_CREATION/SLC10/11/SENTINEL/MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER`; `SOURCE_LOCAL_COMMIT_REVIEW/SLR06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC10/11/SENTINEL/MANUAL_CANONICAL_REPAIR_AND_NEW_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER`; `TEST_LOCAL_COMMIT_REVIEW/TLR06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_MANDATORY_FILE_UNAVAILABLE` | `WORKSPACE_PREPARATION/WP12/13/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_MATERIALIZATION_BYTE_IDENTITY_MISMATCH` | `SOURCE_LOCAL_COMMIT_CREATION/SLC06/7/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/GUSTAVO_MANUAL_INSTALLER`; `TEST_LOCAL_COMMIT_CREATION/TLC06/7/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/GUSTAVO_MANUAL_INSTALLER` |
| `STOP_C04_MATERIALIZATION_GIT_MODE_INVALID` | `SOURCE_LOCAL_COMMIT_CREATION/SLC07/8/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/GUSTAVO_MANUAL_INSTALLER`; `TEST_LOCAL_COMMIT_CREATION/TLC07/8/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/GUSTAVO_MANUAL_INSTALLER` |
| `STOP_C04_MATERIALIZATION_PATH_SET_MISMATCH` | `SOURCE_LOCAL_COMMIT_CREATION/SLC05/6/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER`; `TEST_LOCAL_COMMIT_CREATION/TLC05/6/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER` |
| `STOP_C04_MATERIALIZATION_TARGET_PRESENT` | `SOURCE_LOCAL_COMMIT_CREATION/SLC04/5/SENTINEL/FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC04/5/SENTINEL/FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED/SENTINEL` |
| `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` | `WORKSPACE_PREPARATION/WP13/14/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_AUTHORING/SA05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_STATIC_REVIEW/SSR04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP11/12/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_AUTHORING/TA05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_STATIC_REVIEW/TST05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_PUSH_AHEAD_BEHIND_MISMATCH` | `SOURCE_FAST_FORWARD_PUSH/SFP07/8/SENTINEL/FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED/SENTINEL`; `TEST_FAST_FORWARD_PUSH/TFP07/8/SENTINEL/FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED/SENTINEL` |
| `STOP_C04_PUSH_AUTHORIZATION_IDENTITY_MISMATCH` | `SOURCE_PUSH_AUTHORIZATION/SPA03/4/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_PUSH_AUTHORIZATION/TPA03/4/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_PUSH_AUTHORIZATION_NOT_ACTIVE` | `SOURCE_PUSH_AUTHORIZATION/SPA02/3/GUSTAVO/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `SOURCE_PUSH_AUTHORIZATION/SPA06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_FAST_FORWARD_PUSH/SFP01/2/GUSTAVO/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_PUSH_AUTHORIZATION/TPA02/3/GUSTAVO/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_PUSH_AUTHORIZATION/TPA06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_FAST_FORWARD_PUSH/TFP01/2/GUSTAVO/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_PUSH_BRANCH_REFSPEC_MISMATCH` | `SOURCE_FAST_FORWARD_PUSH/SFP03/4/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP03/4/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_PUSH_BYTE_OR_MODE_MISMATCH` | `SOURCE_LOCAL_COMMIT_REVIEW/SLR05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_REVIEW/TLR05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_PUSH_CHANGED_PATHS_OR_STATUSES_MISMATCH` | `SOURCE_LOCAL_COMMIT_REVIEW/SLR04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_FAST_FORWARD_PUSH/SFP04/5/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_LOCAL_COMMIT_REVIEW/TLR04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_FAST_FORWARD_PUSH/TFP04/5/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_PUSH_COMMIT_MISMATCH` | `SOURCE_FAST_FORWARD_PUSH/SFP02/3/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP02/3/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_PUSH_FAILED` | `SOURCE_FAST_FORWARD_PUSH/SFP09/10/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `SOURCE_FAST_FORWARD_PUSH/SFP10/11/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP09/10/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP10/11/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_PUSH_FORCE_OR_REPAIR_ATTEMPT` | `SOURCE_PUSH_AUTHORIZATION/SPA04/5/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `SOURCE_PUSH_AUTHORIZATION/SPA05/6/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `SOURCE_FAST_FORWARD_PUSH/SFP08/9/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SRV05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_PUSH_AUTHORIZATION/TPA04/5/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_PUSH_AUTHORIZATION/TPA05/6/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP08/9/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TRV05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_PUSH_REMOTE_ADVANCED` | `SOURCE_FAST_FORWARD_PUSH/SFP06/7/SENTINEL/FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED/SENTINEL`; `TEST_FAST_FORWARD_PUSH/TFP06/7/SENTINEL/FRESH_MATERIALIZATION_FROM_NEW_REMOTE_BASE_REQUIRED/SENTINEL` |
| `STOP_C04_PUSH_WORKTREE_NOT_CLEAN` | `SOURCE_FAST_FORWARD_PUSH/SFP05/6/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP05/6/SENTINEL/NEW_PUSH_AUTHORIZATION_REQUIRED/GUSTAVO` |
| `STOP_C04_READ_ONLY_PATH_MUTATED` | `SOURCE_AUTHORING/SA04/5/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_LOCAL_COMMIT_CREATION/SLC08/9/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER`; `TEST_AUTHORING/TA04/5/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_LOCAL_COMMIT_CREATION/TLC08/9/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO_MANUAL_INSTALLER` |
| `STOP_C04_RECORD_CROSS_FIELD_MISMATCH` | `SPEC_REVIEW/SR06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_RECORD_SCHEMA_INVALID` | `SPEC_REVIEW/SR05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_REMOTE_INSTALLATION_IDENTITY_MISMATCH` | `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SRV01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SRV02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SRV03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SRV04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TRV01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TRV02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TRV03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TRV04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_REMOTE_INSTALLATION_NOT_VERIFIED` | `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SRV06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TRV06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SOURCE_CANDIDATE_IDENTITY_MISMATCH` | `SOURCE_AUTHORING/SA11/12/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/CLAUDE`; `SOURCE_STATIC_REVIEW/SSR01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_STATIC_REVIEW/SSR05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SOURCE_REVIEW_NOT_APPROVED` | `SOURCE_STATIC_REVIEW/SSR07/8/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_LOCAL_COMMIT_CREATION/SLC02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SOURCE_TEST_BOUNDARY_VIOLATION` | `SOURCE_AUTHORING/SA03/4/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_AUTHORING/SA06/7/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_STATIC_REVIEW/SSR02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP10/11/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_AUTHORING/TA03/4/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_STATIC_REVIEW/TST02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_CANONICAL_BASE_MISMATCH` | `SPEC_REVIEW/SR02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_CANONICAL_INSTALLATION_LIVE_PATH_CHANGE` | `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SCI05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_CANONICAL_INSTALLATION_NOT_APPROVED` | `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SCI01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_CANONICAL_INSTALLATION_NOT_VERIFIED` | `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SCI06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_CANONICAL_INSTALLATION_RECORD_MISSING` | `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SCI03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_DELIVERY_MECHANICS_NOT_EXTERNAL` | `SPEC_REVIEW/SR08/9/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SCI02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_PACKAGE_IDENTITY_MISMATCH` | `SPEC_REVIEW/SR01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_PRESERVED_CONTRACT_MISMATCH` | `SPEC_REVIEW/SR04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_REPRESENTATION_MISMATCH` | `SPEC_REVIEW/SR09/10/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_SCOPE_REVIEW/TSR05/6/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_REVIEW_NOT_APPROVED` | `SPEC_REVIEW/SR10/11/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_SCOPE_DRIFT` | `SPEC_REVIEW/SR03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_SELF_AUTHORIZED_DELIVERY_ATTEMPT` | `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SCI04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_SUPERSESSION_INCOMPLETE` | `TEST_SCOPE_REVIEW/TSR03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_SPEC_WORKFLOW_DOMAIN_NOT_TOTAL` | `SPEC_REVIEW/SR07/8/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_STAGE_STATE_MISMATCH` | `SPEC_REVIEW/SPEC_REVIEW_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SPEC_CANONICAL_INSTALLATION_CONFIRMATION/SPEC_CANONICAL_INSTALLATION_CONFIRMATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `WORKSPACE_PREPARATION/WORKSPACE_PREPARATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_AUTHORING/SOURCE_AUTHORING_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_STATIC_REVIEW/SOURCE_STATIC_REVIEW_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_LOCAL_COMMIT_CREATION/SOURCE_LOCAL_COMMIT_CREATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_LOCAL_COMMIT_REVIEW/SOURCE_LOCAL_COMMIT_REVIEW_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_PUSH_AUTHORIZATION/SOURCE_PUSH_AUTHORIZATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_FAST_FORWARD_PUSH/SOURCE_FAST_FORWARD_PUSH_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_REMOTE_INSTALLATION_VERIFICATION/SOURCE_REMOTE_INSTALLATION_VERIFICATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_SCOPE_REVIEW/TEST_SCOPE_REVIEW_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TEST_WORKSPACE_PREPARATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_AUTHORING/TEST_AUTHORING_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_STATIC_REVIEW/TEST_STATIC_REVIEW_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TEST_LOCAL_COMMIT_CREATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_REVIEW/TEST_LOCAL_COMMIT_REVIEW_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_PUSH_AUTHORIZATION/TEST_PUSH_AUTHORIZATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_FAST_FORWARD_PUSH/TEST_FAST_FORWARD_PUSH_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_REMOTE_INSTALLATION_VERIFICATION/TEST_REMOTE_INSTALLATION_VERIFICATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `EXECUTION_AUTHORIZATION/EXECUTION_AUTHORIZATION_STATE/1/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_TEST_AUTHORING_RESULT_UNAVAILABLE` | `TEST_AUTHORING/TA08/9/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_STATIC_REVIEW/TST03/4/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_TEST_CANDIDATE_IDENTITY_MISMATCH` | `TEST_AUTHORING/TA09/10/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/CLAUDE`; `TEST_STATIC_REVIEW/TST01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_TEST_REVIEW_NOT_APPROVED` | `TEST_STATIC_REVIEW/TST06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_TEST_SCOPE_NOT_APPROVED` | `TEST_SCOPE_REVIEW/TSR01/2/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_SCOPE_REVIEW/TSR02/3/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_SCOPE_REVIEW/TSR04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_SCOPE_REVIEW/TSR06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_TEST_WORKSPACE_SOURCE_IDENTITY_MISMATCH` | `TEST_WORKSPACE_PREPARATION/TWP02/3/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_TRUSTED_MULTI_ROUND_LINEAGE_REQUIRED` | `WORKSPACE_PREPARATION/WP15/16/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_AUTHORING/SA09/10/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `SOURCE_STATIC_REVIEW/SSR06/7/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL` |
| `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` | `WORKSPACE_PREPARATION/WP17/18/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_AUTHORING/SA08/9/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_LOCAL_COMMIT_CREATION/SLC13/14/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_FAST_FORWARD_PUSH/SFP11/12/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_WORKSPACE_PREPARATION/TWP14/15/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_AUTHORING/TA07/8/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_STATIC_REVIEW/TST04/5/SENTINEL/NEW_SENTINEL_DECISION_REQUIRED/SENTINEL`; `TEST_LOCAL_COMMIT_CREATION/TLC13/14/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP11/12/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `EXECUTION_AUTHORIZATION/EA06/7/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO` |
| `STOP_C04_UNAUTHORIZED_GIT_WRITE` | `WORKSPACE_PREPARATION/WP16/17/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_AUTHORING/SA07/8/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_LOCAL_COMMIT_CREATION/SLC12/13/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `SOURCE_FAST_FORWARD_PUSH/SFP12/13/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_WORKSPACE_PREPARATION/TWP13/14/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_AUTHORING/TA06/7/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_LOCAL_COMMIT_CREATION/TLC12/13/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `TEST_FAST_FORWARD_PUSH/TFP12/13/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO`; `EXECUTION_AUTHORIZATION/EA07/8/SENTINEL/NO_RETRY_UNDER_SAME_AUTHORIZATION/GUSTAVO` |
| `STOP_C04_WORKSPACE_ALIAS_OR_LINK_INVALID` | `WORKSPACE_PREPARATION/WP10/11/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP08/9/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_WORKSPACE_EXTRA_OR_MISSING_PATH` | `WORKSPACE_PREPARATION/WP11/12/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP09/10/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID` | `WORKSPACE_PREPARATION/WP09/10/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `SOURCE_AUTHORING/SA02/3/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP07/8/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_AUTHORING/TA02/3/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_WORKSPACE_NOT_EMPTY` | `WORKSPACE_PREPARATION/WP08/9/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP06/7/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |
| `STOP_C04_WORKSPACE_ROOT_INVALID` | `WORKSPACE_PREPARATION/WP07/8/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL`; `TEST_WORKSPACE_PREPARATION/TWP05/6/SENTINEL/SAME_AUTHORIZATION_FRESH_GATE/SENTINEL` |

## 12. Record-schema linkage

### Halt records

- stage MUST identify one exact stage_specs row.
- predicate_id and predicate_ordinal MUST identify one exact predicate in that stage.
- stop_code, decision_owner, retry_eligibility, and retry_owner MUST exactly equal that predicate applicability row.
- authorization_effect MUST equal NONE and record_kind MUST equal HALT.
- If predicate_ordinal is 1 and stop_code is STOP_C04_STAGE_STATE_MISMATCH, state MUST be a closed WorkflowState different from the stage from_state.
- For every other halt, state MUST exactly equal the stage from_state.
- expected.condition and observed.condition MUST exactly equal the predicate condition_for_success.
- expected.status MUST equal EXPECTED; observed.status MUST be one of FALSE, MISSING, MALFORMED, AMBIGUOUS, STALE, or CONFLICTING.
- expected.facts MUST contain exact stage, predicate_id, predicate_ordinal, and condition_for_success facts.
- observed.facts MUST contain exact predicate_satisfied=false, authoring_started, git_write_observed, and execution_activity_observed facts matching the top-level booleans.
- affected_paths MUST equal the sorted unique union of every PATH and PATH_ARRAY value in observed.facts.
- Fact keys MUST be unique and lexicographically ascending; every array Fact MUST satisfy its declared ordering.
- evidence_sha256 MUST equal SHA-256 of RFC 8785 canonical JSON for the evidence projection defined below.

### Success records

- stage MUST identify one exact stage_specs row.
- from_state, to_state, success_code, and decision_owner MUST exactly equal that stage row.
- predicate_count MUST equal the number of predicates in that stage.
- completed_predicate_ids MUST exactly equal the stage predicate_id list in ascending predicate_ordinal with no omission, duplication, or reordering.
- authorization_effect MUST equal NONE and record_kind MUST equal SUCCESS.
- expected.condition and observed.condition MUST equal ALL_STAGE_PREDICATES_TRUE:<stage>.
- expected.status MUST equal EXPECTED; observed.status MUST equal SATISFIED.
- expected.facts MUST contain exact stage, from_state, to_state, success_code, and predicate_count facts.
- observed.facts MUST contain exact all_predicates_satisfied=true, authoring_started, git_write_observed, and execution_activity_observed facts matching the stage row and top-level booleans.
- affected_paths MUST exactly equal the stage success_affected_paths array.
- authoring_started, git_write_observed, and execution_activity_observed MUST exactly equal the stage success booleans.
- Fact keys MUST be unique and lexicographically ascending; every array Fact MUST satisfy its declared ordering.
- evidence_sha256 MUST equal SHA-256 of RFC 8785 canonical JSON for the evidence projection defined below.

## 13. Invalid-record effect

- A structurally invalid or cross-field-invalid record is not a workflow halt or success.
- An invalid record MUST NOT change state, authorize retry, authorize push, authorize repair, or serve as review evidence.
- Sentinel MAY issue a separate review finding citing STOP_C04_RECORD_SCHEMA_INVALID or STOP_C04_RECORD_CROSS_FIELD_MISMATCH, but the invalid record itself is never normalized or repaired in place.

## 14. Terminal boundary

`C04_EXECUTION_AUTHORIZED_OUTSIDE_C04` means only: Candidate 04 ends at recording that a distinct execution authorization exists; Candidate 04 does not define or authorize execution.

Professor self-check is not Sentinel acceptance.
