# Sentinel Implementation Authorization — REV23 I0 Contract Core

Decision: **APPROVE — NARROW IMPLEMENTATION ONLY**

Authorizing authority: Gustavo, in the current project chat.
Review authority: Sentinel.
Implementation agent: Claude.

## Accepted governing contract

The accepted specification is the effective Revision 23 contract contained in `accepted_contract/`, consisting of the frozen Revision 23 package with `REV23_AMENDMENT_01` and `REV23_AMENDMENT_02` applied.

Critical accepted hashes:

- effective specification: `92e2c4acff45463e8ef566cbc56a5248cb23bd810b310fbea2bdeca197c0d916`
- effective schema registry: `ce1ede1a27b438f6a8f6c04bf7c1642d74a2419719050e2f6bd85cb6ef949aca`
- effective request/authorization contract: `4f0834b48d08fcfdaf32970d2542e61ab7c1263bb7ec727de1f02f2c1a7fbd37`
- governing-package semantic hash: `d62a48d3157937edff343c1249837be4a147356cb960c481804ca4800f889cef`
- governing-package manifest file hash: `cbced7b6072cb33339c624474b746cc7cf347eb33ad946b8364118b83ce1a8eb`

## Authorized implementation tranche: I0 only

Claude may implement a **pure, deterministic, zero-network contract core** for the accepted Revision 23 design.

Authorized code scope:

1. Canonical compact sorted-key JSON serialization and SHA-256 helpers.
2. Typed LF-joined semantic projections and complete-file hash verification.
3. Pure identity constructors and validators for:
   - `pre_run_attempt_id`;
   - `request_id` using `token_id_lexeme`;
   - the exact eight-field `reservation_id`;
   - `partition_id`;
   - the exact twelve-field `run_id`;
   - `initial_496_request_set_sha256`;
   - authorization-specific request-set semantic hash;
   - noncircular two-phase `authorization_id` construction.
4. Governing-package manifest and sidecar validation against exact supplied bytes.
5. Exact URL serializer and request-plan validation under `URL_SERIALIZATION_POLICY_REV22.json`, including preservation of canonical `.0` token lexemes.
6. Pure schemas/enums/validators for the I0 subset only:
   - governing package manifest and sidecar;
   - request manifest and request plan;
   - pre-run and run identity semantic objects;
   - authorized request set and external authorization record validation;
   - authorization-use event states and exact STARTED/terminal capture-row bindings;
   - capture-event authorization/request-set reference fields;
   - reservation cancellation positive-proof contract;
   - HTTP write-out/header status reconciliation.
7. Pure implementation of the registered HTTP-status reconciliation vectors.
8. Test **source files** encoding positive and counterexample cases for the authorized I0 functions. Test execution is not authorized.
9. A static conformance report, changed-file manifest, and patch/diff for Sentinel review.

Preferred new repository paths:

- `pm_research/local_curl_per_side/`
- `tests/local_curl_per_side/`

Minimal edits outside those paths are prohibited unless required only to expose imports. Do not add a CLI command in I0.

## Explicitly unauthorized

Claude must not implement or execute:

- V1 Source D reconstruction;
- V2 Source B artifact capture/normalization;
- Source B/Source D reconciliation;
- policy evidence collection from repository or local data;
- local research-data or empirical-artifact reads;
- artifact recovery or deterministic regeneration;
- curl discovery, subprocess launch, shell execution for the replay, or network access;
- request reservation or execution against a real authorization;
- empirical capture, replay, compatibility analysis, strict analysis, thresholds, results, or finalization;
- full V0–V10 orchestration;
- CLI integration;
- test execution, coverage execution, lint execution, or CI execution;
- package installation or dependency changes;
- edits to canonical `project_context` decision/specification files;
- git commit, push, pull request, or branch publication;
- P1/P2/P3, probe execution, scoring, price construction, side synthesis, wallet work, PnL, paper/live trading, or gate changes.

Repository source reads and `git status`/`git diff` are authorized only as needed to implement and package code. Network fetches and local research-data reads are not.

## Mandatory stop conditions

Claude must stop and return to Sentinel without choosing silently if:

- the local repository HEAD differs from the recorded handoff baseline and the difference affects implementation interfaces;
- an accepted schema or projection is ambiguous;
- a required change would leave the authorized paths or I0 scope;
- implementation requires a new dependency;
- a test must be executed to resolve design ambiguity;
- any contract byte or hash does not match `accepted_contract/`.

## Required delivery

Claude must return one implementation ZIP containing:

- all changed/new source files;
- all authored but unexecuted test files;
- `IMPLEMENTATION_FILE_MANIFEST.json` with path, status, SHA-256, and purpose;
- `IMPLEMENTATION_CONFORMANCE_REV23_I0.md` mapping every implemented function to exact governing sections/schema IDs;
- `IMPLEMENTATION_DIFF.patch` against the recorded repository baseline;
- `IMPLEMENTATION_AUTHORIZATION_OBSERVED.md` confirming every unauthorized activity remained unperformed;
- `TEST_EXECUTION_STATUS.md` stating `NOT_RUN_NOT_AUTHORIZED` and listing the proposed future commands without running them.

Claude must not claim tests passed, runtime correctness, network behavior, or empirical viability.
