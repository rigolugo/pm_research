# Sentinel Implementation Authorization Record — REV23 Amendment 03 I0 Contract Core

Decision: **APPROVE — NARROW IMPLEMENTATION AUTHORING ONLY**

Authorizing authority: Gustavo, explicit current-chat authorization dated `2026-07-15`.
Review authority: Sentinel.
Implementation agent: Claude.
Accepted-contract commit: `fad41de515572ca30b4440b060a69dd6bfc57e2b`.
First authorization-anchor commit: `d737aa9e12cbfa584b275e128c8624e01af72f61`.
Actual implementation baseline: the verified synchronized local `HEAD` after a separately authorized source synchronization.

## Canonical source gate

The accepted-contract commit is `fad41de515572ca30b4440b060a69dd6bfc57e2b`. The first commit containing this active implementation authorization is `d737aa9e12cbfa584b275e128c8624e01af72f61`. These are different roles.

Implementation authoring is blocked until Gustavo separately authorizes canonical source synchronization and the local repository passes the corrected source gate in `authorization_audit/rev23_amendment_03_i0/SENTINEL_CANONICAL_SOURCE_GATE_CORRECTION.md`. This implementation authorization does not itself authorize fetch, pull, reset, checkout/switch, re-clone, or any other source synchronization.

## Accepted governing contract

The governing contract is the effective Revision 23 contract under `accepted_contract/`, consisting of the frozen Revision 23 package plus `REV23_AMENDMENT_01`, `REV23_AMENDMENT_02`, and accepted `REV23_AMENDMENT_03`.

Critical accepted hashes:

- effective specification: `d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9`
- effective schema registry: `e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19`
- effective request/authorization contract: `8095bb923742e8f7eafac61a1de52d9ff4e5537f8a03bb52af62eb795c9f0f7f`
- governing-package semantic hash: `6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b`
- governing-package manifest complete-file hash: `b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa`

## Authorized stage

Claude may author one static implementation package for the **I0 pure deterministic contract core only**.

The implementation must conform directly to the current canonical accepted contract. The previous blocked Claude packages are non-authoritative working material only. They may be consulted if available, but no prior field, schema, default, test expectation, stub, or implementation choice may be carried forward without revalidation against the Amendment 03 contract.

## Authorized repository files

Only the following new source files may be authored:

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/canonical.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `pm_research/local_curl_per_side/identities.py`
- `pm_research/local_curl_per_side/url_serializer.py`
- `pm_research/local_curl_per_side/tables.py`
- `pm_research/local_curl_per_side/request_set.py`
- `pm_research/local_curl_per_side/response_header.py`
- `pm_research/local_curl_per_side/state_machine.py`

Only the following new test-source files may be authored:

- `tests/local_curl_per_side/__init__.py`
- `tests/local_curl_per_side/test_canonical.py`
- `tests/local_curl_per_side/test_governing_package.py`
- `tests/local_curl_per_side/test_identities.py`
- `tests/local_curl_per_side/test_url_serializer.py`
- `tests/local_curl_per_side/test_tables.py`
- `tests/local_curl_per_side/test_request_set.py`
- `tests/local_curl_per_side/test_response_header.py`
- `tests/local_curl_per_side/test_state_machine.py`

All listed repository files must be absent at the verified synchronized local implementation baseline and must be delivered as complete new files. Their absence must be checked before authoring. No other repository path is authorized.

## Required implementation coverage

The source package must implement, within the exact files above, the accepted I0 deterministic contracts for:

1. canonical compact sorted-key JSON, NFC/string discipline, SHA-256 helpers, typed-cell encoding, `NULL` encoding, typed rows, row hashes, logical hashes, and closed-field enforcement;
2. exact governing-package manifest and sidecar validation against the accepted 20-entry package and hashes;
3. exact identity constructors and validators for:
   - five-field `pre_run_attempt_id` with integer `created_at_ns`;
   - request IDs using `token_id_lexeme` without coercion or alias;
   - exact eight-field reservation identity;
   - exact seven-field partition identity, partition-specific three-family domain, evidence bindings, and accepted empty-partition behavior;
   - unchanged exact twelve-field `run_id`;
   - initial 496-request-set hash, authorization-specific request-set semantic hash, and noncircular two-phase authorization identity;
4. closed deterministic validators and hash/order rules for the 600-row token manifest, 496-row request manifest, and 496-row request plan, including exact token-manifest provenance, typed equality, row-hash recomputation, ordinal/order rules, and `.0` lexeme preservation;
5. exact URL serialization and request-plan byte validation under the retained URL policy;
6. authorization-use state streams, STARTED/terminal capture bindings, and positive reservation-cancellation proof validation;
7. the retained response-header status-selection subset required to derive Amendment 03 header state and integer fields; downstream content-type/body analysis is outside I0;
8. total raw-stdout write-out evidence classification from canonical Base64 bytes, mechanical binding of bytes/hash/lexeme/state/integer, selected-header parser binding, all 12 HTTP reconciliation combinations, the 3×3 completed-capture-category/write-out-state lifecycle, mismatch precedence, and `STOP_HTTP_WRITEOUT_INVALID`;
9. unexecuted positive and counterexample test sources covering every accepted branch and the prior Sentinel defects.

No stubbed accepted identity or validator is permitted. No test may encode a known rejected contract.

## Exact activity status

- **Source authoring:** AUTHORIZED, exact listed files only.
- **Test-source authoring:** AUTHORIZED, exact listed files only.
- **Test execution:** NOT AUTHORIZED.
- **Python/project-code execution or import:** NOT AUTHORIZED.
- **Lint, coverage, type checking, CI, generated-code execution:** NOT AUTHORIZED.
- **Local research-data or empirical-artifact reads:** NOT AUTHORIZED.
- **Network, API, RPC, vendor, curl, or request execution:** NOT AUTHORIZED.
- **Subprocess/shell use:** NOT AUTHORIZED except read-only local Git inspection (`git rev-parse HEAD`, `git status --short`, `git merge-base --is-ancestor`, `git diff`, `git diff --check`, `git cat-file -e`) and static byte hashing needed for source-gate/package integrity. Source synchronization commands are not authorized here and require a separate explicit Gustavo decision. No command may execute Python, tests, project modules, generated code, curl, or unrelated network activity.
- **Artifact production:** AUTHORIZED only for the static implementation ZIP, complete source/test-source files, patch, manifests, conformance report, authorization-observed statement, review notes, and checksum inventory. No file under empirical `artifacts/` may be produced.
- **Working-tree writes:** AUTHORIZED only for the exact listed source/test-source files and package-only deliverables in Claude's sandbox.
- **Git history or remote writes:** NOT AUTHORIZED — no commit, branch, tag, push, pull, fetch, reset, checkout/switch to a remote ref, PR, merge, or repository publication. A later explicit source-sync authorization may narrowly permit specified read-only remote acquisition and working-tree synchronization commands; it does not follow from this implementation authorization.
- **Canonical project-context edits:** NOT AUTHORIZED.

## Mandatory stop conditions

Claude must stop and return to Sentinel without choosing silently if:

- source synchronization has not been separately authorized and completed;
- local `HEAD` is not `d737aa9e12cbfa584b275e128c8624e01af72f61` or a descendant, or `d737aa9e12cbfa584b275e128c8624e01af72f61` is absent/not an ancestor;
- `git diff --name-only d737aa9e12cbfa584b275e128c8624e01af72f61..HEAD` includes any accepted-contract, `pm_research/`, `tests/`, dependency, CLI, or runtime-configuration path;
- any authorized new source/test-source path already exists before authoring, or the working tree contains material interface drift;
- any accepted contract byte or hash does not match the values above;
- an accepted schema, projection, lifecycle, or issue-code mapping remains ambiguous;
- implementation requires any file outside the exact authorized matrix;
- implementation requires a dependency, CLI change, project-context edit, Python/test execution, local-data read, network/curl/subprocess action, or empirical artifact;
- static reasoning cannot establish the implementation choice without executing code;
- the prior blocked package conflicts with the current contract.

## Required delivery

Return one ZIP named:

`claude_rev23_amendment03_i0_implementation_package.zip`

It must contain:

1. all exact authorized source files in repository-relative paths;
2. all exact authorized test-source files in repository-relative paths;
3. `IMPLEMENTATION_FILE_MANIFEST.json` with the actual verified synchronized baseline commit, authorization-anchor commit, accepted-contract commit, path, status, SHA-256, size, and purpose for every repository file;
4. `IMPLEMENTATION_CONFORMANCE_REV23_AMENDMENT03_I0.md` mapping every public function/validator to exact governing sections and schema IDs;
5. `IMPLEMENTATION_DIFF.patch` against the actual verified synchronized local implementation baseline recorded in the manifest;
6. `IMPLEMENTATION_AUTHORIZATION_OBSERVED.md` listing every performed and expressly unperformed action;
7. `TEST_EXECUTION_STATUS.md` with status exactly `NOT_RUN_NOT_AUTHORIZED`, plus proposed future commands only;
8. `REVIEW_NOTES_FOR_SENTINEL.md` listing ambiguities, limitations, and any accepted behavior not implemented because it lies outside I0;
9. `SHA256SUMS.txt` covering every ZIP member except itself.

Claude must not claim tests passed, runtime correctness, network behavior, or empirical viability.

## Downstream boundary

This authorization does not authorize test execution, local execution, network execution, replay, empirical capture, full V0–V10 orchestration, CLI integration, dependencies, P1/P2/P3, probe execution, scoring, price construction, side synthesis, wallet/PnL/trading, or gate changes.
