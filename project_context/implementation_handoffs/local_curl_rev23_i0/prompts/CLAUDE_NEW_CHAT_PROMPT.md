# New Claude chat: Implement REV23 Amendment 03 I0 Contract Core

You are Claude, the implementation agent for `rigolugo/pm_research`.

Use the pm-research-implementing Skill. Skill invocation does not expand the authorization below.

Gustavo authorized one bounded implementation stage: **Revision 23 Amendment 03 I0 pure deterministic contract core only**. The stage is currently blocked until canonical source synchronization is separately authorized and the corrected source gate passes.

## Mandatory source gate

Before editing anything:

1. Read `README_FIRST.md`, `SENTINEL_ACCEPTANCE_DECISION.md`, and `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`.
2. Read all records under `authorization_audit/rev23_amendment_03_i0/`, especially `SENTINEL_CANONICAL_SOURCE_GATE_CORRECTION.md` and `SOURCE_SYNC_AUTHORIZATION_STATUS.md`.
3. If source synchronization has not been separately and explicitly authorized, stop with `STOP_CANONICAL_SOURCE_UNAVAILABLE` and make no changes.
4. Do not fetch, pull, reset, checkout/switch, re-clone, or contact a remote unless a later explicit synchronization instruction lists the exact permitted commands.
5. After an authorized synchronization, record with read-only local Git inspection:
   - `git rev-parse HEAD`;
   - `git status --short`;
   - ancestor result for `d737aa9e12cbfa584b275e128c8624e01af72f61`;
   - `git diff --name-only d737aa9e12cbfa584b275e128c8624e01af72f61..HEAD`.
6. Require local `HEAD` to be `d737aa9e12cbfa584b275e128c8624e01af72f61` or a descendant, a clean pre-authoring tree, no prohibited path drift, all exact accepted-contract hashes, and absence of every authorized new source/test-source path.
7. The accepted-contract commit is `fad41de515572ca30b4440b060a69dd6bfc57e2b`. Do not check out that commit as the implementation working `HEAD`; it does not contain the active authorization records.

Any failure requires a stop to Sentinel.

## Authorized stage after the source gate passes

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

- Source authoring: authorized after source gate, exact listed files only.
- Test-source authoring: authorized after source gate, exact listed files only.
- Source synchronization: prohibited unless separately authorized with exact commands.
- Test execution: prohibited.
- Python/project-code execution or import: prohibited.
- Local-data reads: prohibited.
- Network/API/RPC/vendor/curl: prohibited except any later exact source-sync command, if explicitly authorized.
- Subprocess: prohibited except read-only local Git inspection, static hashing, and any later exact source-sync commands.
- Artifact production: static implementation ZIP and required reports only; no empirical `artifacts/` output.
- Git writes: working-tree authoring in exact listed files only; no Git history or remote publication.
- Canonical project-context edits: prohibited.

## Required output

Return `claude_rev23_amendment03_i0_implementation_package.zip` with every source/test-source and report required by `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`. The manifest and patch must use the actual synchronized local `HEAD` as baseline. `TEST_EXECUTION_STATUS.md` must state exactly `NOT_RUN_NOT_AUTHORIZED`. Do not claim tests passed or runtime correctness.

Do not update canonical project-context files. If a canonical update is needed, return a finding only.
