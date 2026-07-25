# Commit, Review, Push, and Remote-Verification Boundaries — Candidate 04

## 1. Status

`SPEC ONLY — NOT ACCEPTED — AUTHORIZATION EFFECT NONE`

This document defines future delivery separation. It authorizes no commit, review action, fetch, push, remote mutation, or installation.

## 2. Governing separation

Source and test materialization each use five distinct boundaries:

1. local materialization commit creation;
2. Sentinel review of that exact local commit;
3. separate Gustavo authorization of the exact push;
4. one ordinary non-force fast-forward push;
5. Sentinel verification of canonical remote installation.

No boundary may inherit authority from an earlier boundary.

## 3. Local commit creation

A local materialization authorization MAY authorize exactly one local non-merge commit and MUST explicitly state:

- the exact authorized parent commit;
- the exact local branch;
- the exact six-path CREATE set;
- exact status `A` for all six paths;
- exact committed byte identities;
- exact Git mode `100644` for all six paths;
- exact actor;
- exact clean-worktree precondition;
- exact prohibition on push.

The local-commit authorization MUST NOT authorize:

- fetch for push gating;
- push;
- pull;
- merge;
- rebase;
- reset;
- restore;
- rollback;
- force;
- branch rewrite;
- remote-ref update;
- automatic repair.

A successful local commit moves only to a pending Sentinel-review state.

## 4. Sentinel local-commit review

Sentinel MUST review the exact local commit SHA and verify:

- exactly one parent;
- parent equals the authorized parent;
- commit is not a merge;
- branch equals the authorized branch;
- changed paths equal the exact six-path set;
- all statuses equal `A`;
- committed bytes and Git modes are exact;
- local HEAD equals the submitted commit;
- worktree and index are clean;
- no push has occurred;
- no prohibited repair operation occurred.

Sentinel approval of the local commit does not authorize push.

## 5. Separate Gustavo push authorization

After Sentinel local-commit approval, Gustavo MAY separately authorize one exact push.

The push authorization MUST pin:

- exact reviewed local commit SHA;
- exact parent commit;
- exact remote base;
- exact branch;
- exact source ref;
- exact destination ref;
- exact refspec;
- exact six paths and status `A`;
- exact committed bytes;
- exact Git modes;
- `force = false`;
- exactly one push attempt;
- only the read-only fetch required for the push gate.

The authorization MUST prohibit:

- pull;
- merge;
- rebase;
- reset;
- restore;
- rollback;
- checkout repair;
- branch rewrite;
- forced push;
- lease-based force;
- automatic repair;
- any additional ref update.

No local-commit authorization or Sentinel local-review decision may substitute for this push authorization.

## 6. Push gate

Immediately before push, the authorized operator MUST verify:

1. local HEAD equals the reviewed commit;
2. local branch and refspec equal the authorization;
3. local worktree and index are clean;
4. local commit parent, paths, statuses, bytes, and modes remain exact;
5. a fresh fetch completed;
6. fetched remote branch equals the exact authorized parent/remote base;
7. local branch is exactly one commit ahead and zero commits behind;
8. force is disabled;
9. no prohibited repair action occurred.

If the fetched remote differs from the authorized parent, the controlling result is:

`STOP_C04_PUSH_REMOTE_ADVANCED`

The operator MUST NOT push and MUST NOT pull, merge, rebase, reset, restore, rollback, force, or repair. A fresh materialization package based on the new remote state requires new Sentinel review and new Gustavo authorization.

## 7. Push operation

Only after every push-gate predicate is true MAY the operator issue exactly one ordinary non-force fast-forward push for the exact refspec.

A rejected, non-fast-forward, ambiguous, partial, additional-ref, or rewritten-ref result is:

`STOP_C04_PUSH_FAILED`

No automatic retry or repair is permitted under the same authorization.

## 8. Sentinel remote verification

Push completion is not canonical installation acceptance.

Sentinel MUST independently verify:

- canonical remote branch head equals the reviewed commit;
- exact parent and one-commit fast-forward relation;
- exact six paths and status `A`;
- exact bytes and Git modes;
- no source/test boundary violation;
- no extra commit or ref;
- no force update, merge, rebase, rewritten parent, or repair.

Only then may the workflow enter the corresponding remote-materialized-verified state.

## 9. Source delivery stages

1. `SOURCE_LOCAL_COMMIT_CREATION`
2. `SOURCE_LOCAL_COMMIT_REVIEW`
3. `SOURCE_PUSH_AUTHORIZATION`
4. `SOURCE_FAST_FORWARD_PUSH`
5. `SOURCE_REMOTE_INSTALLATION_VERIFICATION`

## 10. Test delivery stages

1. `TEST_LOCAL_COMMIT_CREATION`
2. `TEST_LOCAL_COMMIT_REVIEW`
3. `TEST_PUSH_AUTHORIZATION`
4. `TEST_FAST_FORWARD_PUSH`
5. `TEST_REMOTE_INSTALLATION_VERIFICATION`

The source and test stage sequences are independent and may not be combined.

## 11. Candidate 04 documentation installation

Candidate 04 does not define or authorize its own commit, merge, push, ref update, or remote mutation.

Delivery mechanics for Candidate 04 documentation are controlled exclusively by:

`project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`

Candidate 04 may be used operationally only after Sentinel confirms a documentation-only canonical installation produced through that controlling workflow. The confirmation stage records the external result; it does not authorize or prescribe the delivery mechanics.
