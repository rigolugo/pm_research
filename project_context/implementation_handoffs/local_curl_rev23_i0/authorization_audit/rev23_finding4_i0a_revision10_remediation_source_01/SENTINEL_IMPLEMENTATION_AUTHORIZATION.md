APPROVE — REV10_REMEDIATION_SOURCE_AUTHORIZATION_PACKAGE_ACCEPTED

# Sentinel Implementation-Source Authorization — Revision 10 Remediation

## Authorized stage after activation

One atomic implementation-source authoring stage under authorization ID:

`REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`

Controlling inputs:

- canonical repository: `rigolugo/pm_research`;
- package-preparation base: `a4fb0e64056b58a229da481664e4234e3215cd91`;
- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- accepted remediation package: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- remediation package ZIP SHA-256: `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`;
- remediation installation commit: `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`.

## Activation conditions

This decision is conditional. Source authoring becomes active only after all of the following are true:

1. this exact authorization package is manually installed in one documentation-only canonical commit;
2. Sentinel verifies that commit, its parent, exact changed paths, checksums, and absence of live source/test changes;
3. local `HEAD` equals the Sentinel-verified authorization-install commit on branch `main`;
4. the worktree is clean;
5. all twelve paths in `TWELVE_PATH_STARTING_SHA256SUMS.txt` exist and match exactly;
6. Sentinel reviews and accepts the complete local source-gate output;
7. Sentinel issues the active Claude handoff with the verified source-gated commit.

Until all seven conditions are met, return:

`STOP_REV10_REMEDIATION_SOURCE_AUTHORIZATION_NOT_ACTIVATED`

## Writable repository paths after activation

Exactly:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

Allowed new repository files: `NONE`.

## Permitted implementation activity after activation

- read canonical specifications, accepted remediation records, and the twelve gated source/test files;
- edit only the exact three writable source paths;
- use static text/JSON inspection and standard-library parsing that does not import or execute project modules;
- run read-only `git status`, `git diff`, path inventory, and SHA-256 commands;
- use local file/archive utilities only to prepare the implementation-review package outside the repository;
- report exact starting and ending hashes, changed paths, and activity boundaries.

## Unauthorized activity

- any test-source edit or test execution/collection;
- importing or executing `pm_research` or any authored project module;
- compilation, lint, typing, coverage, CI, bytecode, or generated files;
- local research data, credentials, wallets, artifacts, or empirical outputs;
- curl, API, RPC, Dune, vendor, package-manager, or general network access;
- subprocesses other than the narrow read-only Git/hash/file/archive utility boundary above;
- dependency, CLI, config, runtime, export/re-export, packaging, or adjacent cleanup changes;
- repository files outside the three writable paths;
- Git commit, branch/ref, push, merge, pull request, or other history/remote write;
- rollback, restoration, overwrite, or checkpoint promotion;
- R2, P1/P2/P3, scoring, probe execution, or gate change.

## Completion boundary

Claude returns an implementation-review package to Sentinel. Source authoring does not authorize tests or execution. Passing tests later cannot cure a wrong starting state, unauthorized path, or wrong-contract implementation.
