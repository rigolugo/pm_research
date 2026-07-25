# Implementation Authorization Scope

## Current stop

`STOP_REV10_REMEDIATION_SOURCE_AUTHORIZATION_NOT_ACTIVATED`

## Conditional authorization package

- authorization ID: `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`;
- package-preparation base: `a4fb0e64056b58a229da481664e4234e3215cd91`;
- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- accepted remediation scope: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- Gustavo authorization: recorded on `2026-07-24`;
- Sentinel package decision: `APPROVE — REV10_REMEDIATION_SOURCE_AUTHORIZATION_PACKAGE_ACCEPTED`;
- canonical installation verification: pending;
- local twelve-path source gate: pending;
- active source-gated commit: not selected.

## Writable after activation

Exactly:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

Allowed new repository files: `NONE`.

The three files form one atomic candidate. Partial implementation does not establish conformance.

## Activation requirements

1. Install this exact authorization package in one documentation-only canonical commit.
2. Sentinel verifies the commit, parent, path scope, and checksums.
3. Local `HEAD` equals that verified commit on `main` with a clean worktree.
4. All twelve paths match `TWELVE_PATH_STARTING_SHA256SUMS.txt` exactly.
5. Sentinel accepts the complete local source-gate report.
6. Sentinel issues the active Claude handoff naming the verified source-gated commit.

## Unauthorized now and throughout source authoring

- test-source authoring and test collection/execution;
- imports, project execution, compilation, lint, typing, coverage, or CI;
- research-data, credentials, wallet, or empirical artifact reads;
- curl/API/RPC/Dune/vendor/package-manager/general network access;
- dependencies, CLI, config, runtime, exports, packaging, or generated files;
- repository paths outside the exact three writable paths;
- Git history or remote writes by Claude;
- rollback, restoration, overwrite, or checkpoint promotion;
- R2, P1/P2/P3, scoring, probe execution, or gate changes.

The preserved `fcf406c4...` checkpoint remains `NOT_ACCEPTED` and cannot be used as starting bytes.
