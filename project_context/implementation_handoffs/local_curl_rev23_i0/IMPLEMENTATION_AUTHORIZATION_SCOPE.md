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
- canonical installation verification: `INSTALLED_AND_SENTINEL_VERIFIED`;
- canonical installation commit: `71061065d91fc391e934d7e79a29eefc898cfe82`;
- local canonical-worktree source gate: `STOP_REV10_REMEDIATION_SOURCE_GATE_FAILED`;
- active source-gated commit: `NOT_SELECTED`.

## Failed-gate finding

The installed gate required all twelve live source/test paths to exist at the canonical worktree and match `TWELVE_PATH_STARTING_SHA256SUMS.txt`. At canonical commit `71061065...`, those live paths were absent. The gate halted before any edit.

The separately captured Claude workspace is accepted only as provenance evidence under:

`CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`

It was captured at detached local HEAD `1e1afb29791f42c286b45d3b576f74926add8dce`, with all twelve paths untracked. It is not the canonical worktree required by the installed gate, and `prepared_evidence.py` has checkpoint SHA-256 `fcf406c4...` rather than the gate's historical baseline `8b8e9320...`.

Therefore the accepted capture does not clear, repair, or reactivate the installed source gate.

## Writable only after a future valid activation

Exactly:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

The three files form one atomic candidate. Partial implementation does not establish conformance.

The installed package's allowed-new-files value remains `NONE`; it cannot be silently changed by the provenance finding. A separately accepted amendment is required before any different starting-state or materialization model may be authorized.

## Required future sequence

Worktree-capture acceptance installation is complete and Sentinel-verified at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`.

1. Professor finalizes the SPEC-ONLY Candidate 02 starting-state amendment using the accepted capture finding.
2. Sentinel reviews and accepts or blocks that amendment.
3. Gustavo separately authorizes the resulting bounded implementation stage.
4. Sentinel issues a new active Claude handoff with exact starting identities and path/activity boundaries.

No step above follows automatically from provenance acceptance.

## Unauthorized now

- source/test authoring or materialization;
- test collection/execution;
- imports, project execution, compilation, lint, typing, coverage, or CI;
- research-data, credentials, wallet, or empirical artifact reads;
- curl/API/RPC/Dune/vendor/package-manager/general network access;
- dependencies, CLI, config, runtime, exports, packaging, or generated files;
- repository paths outside a later exact authorized boundary;
- Git history or remote writes by Claude;
- rollback, restoration, overwrite, or checkpoint promotion;
- R2, P1/P2/P3, scoring, probe execution, or gate changes.

The preserved `fcf406c4...` checkpoint remains `NOT_ACCEPTED` and cannot be selected as starting bytes without a separately accepted amendment and explicit authorization.
