# Implementation Authorization Scope

## Current stop

`STOP_REV10_STARTING_STATE_AMENDMENT_INSTALLATION_NOT_VERIFIED`

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

## Accepted starting-state amendment

Sentinel accepted `REV23_FINDING4_I0A_REVISION_10_STARTING_STATE_AMENDMENT_CANDIDATE_04` at exact canonical review base `bc957fe05096b790052d0515773b9e0a2dc88a60`.

The accepted amendment supersedes the old starting-state and allowed-new-file assumptions only for future packages that explicitly invoke Candidate 04 after canonical installation verification. It defines an isolated non-Git workspace, exact twelve starting identities, three writable source paths, four separately writable test paths, and later exact CREATE-only materialization boundaries.

Candidate 04 does not activate the failed authorization package. This installation remains `PENDING_SENTINEL_VERIFICATION`; no implementation starting commit, workspace, writable path, local implementation commit, push authorization, or active Claude handoff exists.

## Writable only after a future valid activation

Exactly:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

The three files form one atomic candidate. Partial implementation does not establish conformance.

The historical installed package's allowed-new-files value remains `NONE` and that package remains inactive. Accepted Candidate 04 defines later exact CREATE-only source and test materialization exceptions, but those exceptions are not active until Candidate 04 installation is verified and Gustavo separately authorizes the exact stage. No current repository file creation is authorized.

## Required future sequence

Worktree-capture acceptance is installed and Sentinel-verified at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`. Candidate 04 is accepted and installed by this package with verification pending.

1. Gustavo installs the documentation-only Candidate 04 package at exact base `bc957fe05096b790052d0515773b9e0a2dc88a60` using the controlling canonical-update workflow.
2. Sentinel verifies the exact installation commit and accepted-candidate bytes.
3. Gustavo separately decides whether to authorize workspace preparation or a later bounded source-authoring stage.
4. Sentinel issues a new active Claude handoff only for that exact authorized stage.
5. Any local implementation commit, Sentinel review, push authorization, push, and remote verification remain separate boundaries under Candidate 04.

No step follows automatically from Candidate 04 acceptance or documentation installation.

## Unauthorized now

- workspace preparation, capture extraction for implementation, source/test authoring, or materialization;
- test collection/execution;
- imports, project execution, compilation, lint, typing, coverage, or CI;
- research-data, credentials, wallet, or empirical artifact reads;
- curl/API/RPC/Dune/vendor/package-manager/general network access;
- dependencies, CLI, config, runtime, exports, packaging, or generated files;
- repository paths outside a later exact authorized boundary;
- local implementation commits, Git history, branch/ref, push, merge, or remote writes by Claude;
- rollback, restoration, overwrite, or checkpoint promotion;
- R2, P1/P2/P3, scoring, probe execution, or gate changes.

The preserved `fcf406c4...` checkpoint remains `NOT_ACCEPTED` and cannot be selected as starting bytes without a separately accepted amendment and explicit authorization.
