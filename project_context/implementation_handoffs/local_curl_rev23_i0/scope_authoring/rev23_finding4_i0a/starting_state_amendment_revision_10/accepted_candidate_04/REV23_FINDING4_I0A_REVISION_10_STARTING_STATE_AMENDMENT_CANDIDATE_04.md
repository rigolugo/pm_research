# REV23 Finding 4 I0A Revision 10 Starting-State Amendment — Candidate 04

## 1. Status

- mode: `AMEND`;
- status: `AMENDMENT CANDIDATE`;
- acceptance: `NOT_ACCEPTED`;
- authorization effect: `NONE`;
- supersedes: Candidate 03 candidate only, if Sentinel accepts Candidate 04;
- Candidate 03 status: `BLOCKED_NOT_ACCEPTED_NON_CONTROLLING`;
- draft owner: Professor;
- specification reviewer and decision owner: Sentinel;
- implementation and execution authorization owner: Gustavo;
- active Claude implementation prompt: `false`.

Professor does not approve its own work.

**Checkable completion sentence:** Candidate 04 is complete when Sentinel can verify that the Candidate 03 architecture is unchanged except for closed workflow record schemas and explicit five-stage source/test delivery separation, with every record and transition mechanically closed and no authorization inferred.

---

## 2. Purpose

Candidate 04 is a narrow correction to Candidate 03.

It corrects exactly:

1. the absence of actual closed halt and success record schemas with complete normative cross-field validation;
2. the failure to separate local commit creation, local commit review, separate push authorization, one ordinary non-force fast-forward push, and canonical remote verification.

It does not redesign the accepted-scope supersession, starting bytes, workspace, source/test boundaries, support-path treatment, provenance model, or failed-gate treatment.

---

## 3. Canonical base

- repository: `rigolugo/pm_research`;
- exact canonical base: `bc957fe05096b790052d0515773b9e0a2dc88a60`;
- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- accepted remediation scope: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- accepted capture decision: `ACCEPT FINDING — CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`;
- accepted capture installation: `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`;
- accepted capture archive SHA-256: `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`;
- checkpoint: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`;
- checkpoint SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`;
- failed authorization: `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`;
- failed authorization installation: `71061065d91fc391e934d7e79a29eefc898cfe82`;
- failed result: `STOP_REV10_REMEDIATION_SOURCE_GATE_FAILED`.

Authority order remains:

1. `GUARDRAILS.md`;
2. current canonical state and decisions;
3. effective Revision 23 contract;
4. accepted Revision 10 scope;
5. accepted remediation scope;
6. accepted twelve-path capture;
7. Candidate 04 only after Sentinel acceptance and canonical documentation installation through the controlling update workflow;
8. later exact Gustavo authorization and active Sentinel handoff.

Candidate 03 is not in the authority chain.

---

## 4. In scope

Candidate 04 defines:

- two closed Draft 2020-12 workflow record schemas;
- exact halt and success field contracts;
- exact path, SHA, timestamp, predicate-ID, boolean, integer, nullability, and evidence-object types;
- normative array ordering and uniqueness;
- exact stage/predicate/transition cross-field validation;
- separate local commit, local review, push authorization, push, and remote verification boundaries;
- exact push preflight and remote-advance halt behavior;
- recomputed workflow enums, transitions, stops, successes, predicates, and applicability;
- external documentation-delivery boundary for Candidate 04 itself.

---

## 5. Preserved without redesign

Candidate 04 preserves:

1. the exact clause-level accepted-scope supersession and retained `C03_*` semantic provision IDs;
2. the exact twelve-path and byte matrix;
3. eleven baseline matches and one checkpoint-modified start;
4. `ISOLATED_CAPTURED_PAYLOAD_WORKSPACE_MODEL_V2`;
5. source authoring across exactly three writable source paths and nine protected paths;
6. test authoring across exactly four writable test paths and eight protected paths;
7. the five baseline-support edit prohibitions;
8. separate source and test authoring;
9. separate source and test materialization;
10. failed-gate non-repair;
11. open `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
12. authorization effect `NONE`.

The retained `C03_*` provision IDs are semantic identifiers incorporated by Candidate 04. They do not make Candidate 03 controlling.

---

## 6. Exact authoring path boundaries

### 6.1 Source writable paths

- `pm_research/local_curl_per_side/canonical.py`
- `pm_research/local_curl_per_side/finding4_registry.py`
- `pm_research/local_curl_per_side/prepared_evidence.py`

### 6.2 Source protected paths

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/claim_hashes.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `tests/local_curl_per_side/test_canonical_i0a.py`
- `tests/local_curl_per_side/test_claim_hashes_i0a.py`
- `tests/local_curl_per_side/test_finding4_registry_i0a.py`
- `tests/local_curl_per_side/test_governing_package_i0a.py`
- `tests/local_curl_per_side/test_i0a_public_contract.py`
- `tests/local_curl_per_side/test_prepared_evidence_i0a.py`

### 6.3 Test writable paths

- `tests/local_curl_per_side/test_canonical_i0a.py`
- `tests/local_curl_per_side/test_finding4_registry_i0a.py`
- `tests/local_curl_per_side/test_i0a_public_contract.py`
- `tests/local_curl_per_side/test_prepared_evidence_i0a.py`

### 6.4 Test protected paths

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/canonical.py`
- `pm_research/local_curl_per_side/claim_hashes.py`
- `pm_research/local_curl_per_side/finding4_registry.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `pm_research/local_curl_per_side/prepared_evidence.py`
- `tests/local_curl_per_side/test_claim_hashes_i0a.py`
- `tests/local_curl_per_side/test_governing_package_i0a.py`

### 6.5 Baseline-support paths prohibited from editing

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/claim_hashes.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `tests/local_curl_per_side/test_claim_hashes_i0a.py`
- `tests/local_curl_per_side/test_governing_package_i0a.py`

The exact path, size, SHA-256, role, and stage treatment remain controlled by `EXACT_PATH_AND_BYTE_MATRIX.json`.

---

## 7. Closed workflow halt record

Normative members:

- `WORKFLOW_HALT_RECORD.schema.json`;
- `WORKFLOW_RECORD_CROSS_FIELD_RULES.md`;
- `WORKFLOW_DOMAIN.json`.

The schema dialect is Draft 2020-12. The schema:

- has `type: object`;
- has `additionalProperties: false`;
- requires all 19 top-level fields;
- binds state, stage, stop, decision owner, retry eligibility, retry owner, and authorization effect to closed domains;
- requires `record_kind = HALT`;
- requires `authorization_effect = NONE`;
- requires positive integer `predicate_ordinal`;
- defines closed expected and observed evidence objects;
- defines closed Fact variants;
- permits null only through an explicit `NULL` Fact;
- validates lowercase SHA-256;
- validates exact-Z UTC timestamps;
- validates repository-relative paths;
- requires exact boolean types;
- declares path and Fact ordering.

Cross-field validation MUST bind the record to one exact stage predicate and applicability row. A mismatch is invalid and changes no state.

---

## 8. Closed workflow success record

Normative members:

- `WORKFLOW_SUCCESS_RECORD.schema.json`;
- `WORKFLOW_RECORD_CROSS_FIELD_RULES.md`;
- `WORKFLOW_DOMAIN.json`.

The schema:

- has `type: object`;
- has `additionalProperties: false`;
- requires all 18 top-level fields;
- requires `record_kind = SUCCESS`;
- requires `authorization_effect = NONE`;
- binds stage, from-state, to-state, success code, and decision owner to closed enums;
- requires a positive predicate count;
- requires unique completed predicate IDs in exact stage order;
- defines exact expected and observed evidence objects;
- validates paths, hashes, timestamps, integers, booleans, and nullability.

Cross-field validation MUST require exact equality to one stage transition row, including all predicate IDs, success paths, and success booleans.

---

## 9. Record invalidity

A record failing structural schema validation or normative cross-field validation:

- is neither a workflow halt nor a success;
- changes no state;
- authorizes no retry, commit, review, push, repair, materialization, or execution;
- MUST NOT be normalized, reordered, coerced, defaulted, or repaired in place.

Sentinel may issue a separate review finding citing:

- `STOP_C04_RECORD_SCHEMA_INVALID`;
- `STOP_C04_RECORD_CROSS_FIELD_MISMATCH`.

The invalid record itself is never promoted into a valid workflow result.

---

## 10. Recomputed total workflow

Candidate 04 defines:

- WorkflowState: `21`;
- WorkflowStage: `20`;
- WorkflowStopCode: `70`;
- WorkflowSuccessCode: `20`;
- ordered predicate applications: `205`.

Every stage has:

1. one exact from-state;
2. one ordered predicate sequence;
3. one first-applicable stop per failed predicate;
4. one exact success code;
5. one exact to-state;
6. one exact success-record projection.

The complete contract is `WORKFLOW_DOMAIN.json` and `WORKFLOW_DOMAIN.md`.

---

## 11. Source materialization delivery separation

Source delivery is exactly:

1. `SOURCE_LOCAL_COMMIT_CREATION`;
2. `SOURCE_LOCAL_COMMIT_REVIEW`;
3. `SOURCE_PUSH_AUTHORIZATION`;
4. `SOURCE_FAST_FORWARD_PUSH`;
5. `SOURCE_REMOTE_INSTALLATION_VERIFICATION`.

### 11.1 Local commit

A separate local-commit authorization permits one local non-merge commit only. It includes no push authority.

### 11.2 Sentinel local review

Sentinel reviews the exact commit SHA, parent, branch, six `A` statuses, committed bytes, modes, and clean worktree. Approval includes no push authority.

### 11.3 Separate push authorization

Gustavo must separately authorize the exact reviewed commit, parent/remote base, branch, refspec, paths, statuses, bytes, modes, and `force = false`.

### 11.4 Push gate

Immediately before push:

- local HEAD equals the reviewed commit;
- worktree and index are clean;
- fresh fetched remote equals the authorized parent;
- local is exactly one commit ahead and zero behind;
- force is disabled;
- no repair operation occurred.

If remote advanced, `STOP_C04_PUSH_REMOTE_ADVANCED` controls. The operator MUST NOT push or repair.

### 11.5 Push and remote verification

Only one ordinary non-force fast-forward push is permitted. Push success does not establish canonical installation. Sentinel must independently verify the canonical remote commit.

---

## 12. Test materialization delivery separation

Test delivery uses the corresponding five distinct stages:

1. `TEST_LOCAL_COMMIT_CREATION`;
2. `TEST_LOCAL_COMMIT_REVIEW`;
3. `TEST_PUSH_AUTHORIZATION`;
4. `TEST_FAST_FORWARD_PUSH`;
5. `TEST_REMOTE_INSTALLATION_VERIFICATION`.

The same parent, branch, refspec, path/status, bytes, modes, clean-worktree, fresh-fetch, one-ahead/zero-behind, non-force, no-repair, and independent remote-verification rules apply.

Source and test delivery MUST NOT be combined.

---

## 13. Candidate 04 documentation installation

Candidate 04 MUST NOT authorize or define its own:

- local commit;
- merge;
- push;
- branch or ref update;
- remote mutation;
- delivery command sequence.

Delivery mechanics are controlled exclusively by:

`project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`

`SPEC_CANONICAL_INSTALLATION_CONFIRMATION` only verifies that an external documentation-only installation was completed and independently verified. It creates no delivery authority.

---

## 14. Windows workspace identity

The isolated workspace remains non-Git. Its exact member identity is:

```text
(exact repository-relative path, REGULAR_FILE, exact size_bytes, exact lowercase SHA-256)
```

Git mode is not part of workspace identity. Symlinks, junctions, reparse-point aliases, alternate path aliases, hard links, case-folded duplicates, short-name substitutions, alternate streams, and path escapes remain prohibited.

Git mode `100644` applies only to later canonical materialization commit and remote verification.

---

## 15. Checkpoint and lineage

`prepared_evidence.py` may be proposed later only from exact opaque starting SHA:

`fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`

This does not accept, promote, or make the checkpoint conformant.

`MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE` remains open. Candidate 04 makes no historical activity claim and requires a halt if a decision depends on undocumented lineage.

---

## 16. Failed-gate non-repair

The prior authorization remains:

- `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`;
- installed at `71061065d91fc391e934d7e79a29eefc898cfe82`;
- result `STOP_REV10_REMEDIATION_SOURCE_GATE_FAILED`;
- state `FAILED_INACTIVE`;
- active source-gated commit `NOT_SELECTED`.

Candidate 04 does not amend, repair, reactivate, or rerun that authorization. All future operational stages require new identities.

---

## 17. Acceptance evidence

Sentinel may statically inspect:

- both schemas under Draft 2020-12;
- every schema enum against `WORKFLOW_DOMAIN.json`;
- all 205 predicate applicability rows;
- all 20 success transitions;
- generated structurally valid records for every predicate and transition;
- negative schema and cross-field cases;
- source/test delivery-stage separation;
- remote-advance no-push behavior;
- preserved supersession and path-matrix hashes;
- deterministic package checksums.

These are review methods only and authorize no operational activity.

---

## 18. Assumptions and open decisions

No current remote branch, local commit, parent, refspec, or materialization byte set is selected by Candidate 04.

Every later operational package must supply exact values. Missing, stale, ambiguous, or conflicting values select the first applicable typed stop.

Sentinel must decide whether the schemas and delivery separation fully correct Candidate 03 without altering preserved architecture.

---

## 19. Self-attack

### 19.1 Strongest alternative

Keep Candidate 03's two materialization stages and place commit/push details only in later authorization packages.

Rejected because it permits the specification state machine to treat local commit completion and canonical installation as too closely coupled, creating an implicit-push false-unblock path.

### 19.2 Premortem

Literal conformance could still fail the intended goal if:

1. a push authorization omits a material identity and relies on the reviewed commit by reference; or
2. a remote advance triggers an unauthorized repair rather than a clean halt.

Candidate 04 requires every push fact to be pinned and makes remote advancement a no-push/no-repair halt.

### 19.3 Record-schema attack

A structurally valid record could still lie about its stage row. Candidate 04 therefore requires separate normative cross-field validation and invalidates any row mismatch.

Professor self-review is not acceptance.

---

## 20. Authorization statement

Candidate 04 is SPEC ONLY. Authorization effect is `NONE`.

No workspace was created. No capture was extracted for implementation. No source/test file was edited. No local materialization commit was created. No push was authorized or performed. No project code, tests, data, network resource, project artifact, or GitHub write was accessed or executed for project operations.

Candidate 04 provides no active Claude implementation prompt.

---

## 21. Requested Sentinel decision

Requested decision:

`APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.

Proposed approval label:

`APPROVE — REV10_STARTING_STATE_AMENDMENT_CANDIDATE_04_ACCEPTED`
