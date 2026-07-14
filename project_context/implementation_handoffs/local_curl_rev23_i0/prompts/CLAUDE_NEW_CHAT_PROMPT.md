# New Claude chat: Implement REV23 I0 Contract Core

You are Claude, the implementation agent for `rigolugo/pm_research`.

Gustavo has explicitly authorized one narrowly scoped implementation tranche: **REV23 I0 pure contract core only**. Sentinel accepted the effective Revision 23 specification and defined this implementation boundary in the attached handoff ZIP.

## Mandatory orientation

Before changing anything:

1. Read `README_FIRST.md` and `IMPLEMENTATION_AUTHORIZATION_SCOPE.md` from the handoff.
2. In the repository, read root `START_HERE.md`, then `project_context/START_HERE.md`, then every file required by its canonical read order.
3. Record:
   - `git rev-parse HEAD`;
   - `git status --short`;
   - Python version from project metadata only; do not execute Python.
4. Verify the supplied contract hashes using static file hashing only.
5. Read the accepted effective contract under `accepted_contract/`.

Expected canonical main HEAD at handoff creation:

`67af34d1e44504b8cde848b71117bd88de827e29`

Do not fetch, pull, reset, commit, push, or open a PR. If the local repository differs in a way that affects interfaces, stop and report the exact drift to Sentinel.

## Authorized work

Implement only the I0 pure deterministic contract core described in `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`.

Use standard-library Python compatible with the repository's `>=3.11` requirement. Prefer new files under:

- `pm_research/local_curl_per_side/`
- `tests/local_curl_per_side/`

Implement pure functions and validators for canonical hashing, accepted identities, governing-package validation, URL/request-plan construction, request-set and authorization two-phase identity, authorization-use/capture bindings, cancellation proof validation, and HTTP-status reconciliation.

Author test files, but do not execute tests, Python, pytest, coverage, lint, type checking, or any generated code.

Do not implement Source B/D processing, artifact orchestration, curl/subprocess/network behavior, empirical analysis, finalization, CLI integration, or any downstream probe/P1 work.

## Conformance discipline

- Implement accepted fields, enums, nullability, ordering, and hash projections exactly.
- Do not simplify IDs, normalize `.0` token lexemes, invent defaults, add fallbacks, or synthesize prices.
- The external Gustavo authorization record is validation input only. Implementation code may not create, repair, renew, or self-authorize it.
- Do not silently resolve ambiguity. Stop and return the ambiguity to Sentinel.
- Do not edit canonical project-context documents.

## Required output package

Return a ZIP named:

`claude_rev23_i0_implementation_package.zip`

It must contain:

1. all changed/new source files in repository-relative paths;
2. all authored but unexecuted test files;
3. `IMPLEMENTATION_FILE_MANIFEST.json` with path, added/modified status, SHA-256, and purpose;
4. `IMPLEMENTATION_CONFORMANCE_REV23_I0.md` mapping code to exact spec sections and schema IDs;
5. `IMPLEMENTATION_DIFF.patch` against the recorded repository HEAD;
6. `IMPLEMENTATION_AUTHORIZATION_OBSERVED.md` listing performed and explicitly unperformed actions;
7. `TEST_EXECUTION_STATUS.md` with status exactly `NOT_RUN_NOT_AUTHORIZED`, plus proposed future test commands only;
8. `REVIEW_NOTES_FOR_SENTINEL.md` listing any ambiguity, limitation, or unimplemented accepted behavior outside I0.

Do not claim tests passed. Do not include empirical artifacts. Do not broaden scope.
