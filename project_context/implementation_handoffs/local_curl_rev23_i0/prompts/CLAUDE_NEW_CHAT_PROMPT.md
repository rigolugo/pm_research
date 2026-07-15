# New Claude chat: Implement REV23 Amendment 03 I0 Contract Core

You are Claude, the implementation agent for `rigolugo/pm_research`.

Use the pm-research-implementing Skill. Skill invocation does not expand the authorization below.

Gustavo explicitly authorized one bounded implementation stage: **Revision 23 Amendment 03 I0 pure deterministic contract core only**. Sentinel accepted the governing specification and defined the exact implementation boundary in `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`.

## Mandatory orientation

Before editing anything:

1. Read `README_FIRST.md` and `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`.
2. Read `authorization_audit/rev23_amendment_03_i0/README_FIRST.md` and its three controlled records.
3. In the repository, read root `START_HERE.md`, then `project_context/START_HERE.md`, then every file required by its canonical read order.
4. Record, using read-only Git commands only:
   - `git rev-parse HEAD`;
   - `git status --short`.
5. Require exact `HEAD`:

   `fad41de515572ca30b4440b060a69dd6bfc57e2b`

6. Verify the accepted contract with static byte hashing only. Do not execute Python, project modules, tests, generated code, lint, type checking, coverage, or CI.
7. Read the complete effective contract under `accepted_contract/`, including the Amendment 03 audit and retained contracts/policies/vectors.

Do not fetch, pull, reset, create a branch, commit, push, or open a PR. Stop on material working-tree drift.

## Authorized stage

Author one static implementation package for the exact I0 functions and exact repository files listed in `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`.

The previous blocked Claude packages are non-authoritative working material only. Revalidate every field, type, enum, projection, hash, lifecycle, stop, and test expectation against the current accepted contract. Do not preserve stubs or rejected contracts.

Implement the accepted Amendment 03 behavior, including:

- exact canonical serialization, typed tags, and `NULL` cells;
- five-field pre-run identity and seven-field partition identity;
- unchanged twelve-field run identity;
- exact 600-row token-manifest, 496-row request-manifest, and 496-row request-plan validators and provenance bindings;
- `token_id_lexeme` and `.0` preservation;
- governing manifest/sidecar validation;
- URL/request-plan validation;
- request-set and two-phase authorization identity;
- authorization-use/capture bindings and cancellation proof;
- retained status-header parsing needed for reconciliation;
- raw Base64 stdout evidence derivation;
- all 12 HTTP reconciliation combinations and the complete 3×3 completed-capture lifecycle.

Author the exact test-source files, but do not execute them.

## Explicit status

- Test-source authoring: authorized, exact listed files only.
- Test execution: prohibited.
- Python/project-code execution or import: prohibited.
- Local-data reads: prohibited.
- Network/API/RPC/vendor/curl: prohibited.
- Subprocess: prohibited except the exact read-only Git inspection commands, `git diff`, `git diff --check`, and static hashing.
- Artifact production: static implementation ZIP and required reports only; no empirical `artifacts/` output.
- Git writes: working-tree authoring in exact listed files only; no Git history or remote writes.
- Canonical project-context edits: prohibited.

If any needed behavior cannot be implemented within this boundary without execution or another file, stop and return the exact ambiguity or scope defect to Sentinel.

## Required output

Return one ZIP named:

`claude_rev23_amendment03_i0_implementation_package.zip`

It must contain every source/test-source and report required by `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`. `TEST_EXECUTION_STATUS.md` must state exactly `NOT_RUN_NOT_AUTHORIZED`. Do not claim tests passed or runtime correctness.

Do not update canonical project-context files in the repo. If a canonical doc update is needed, return a handoff/finding only. ChatGPT will prepare complete replacement files for the user to upload manually.
