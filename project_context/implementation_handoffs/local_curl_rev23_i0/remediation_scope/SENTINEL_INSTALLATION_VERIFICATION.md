APPROVE — REMEDIATION_SCOPE_CANONICAL_INSTALLATION_VERIFIED

# Sentinel Installation Verification — Revision 10 Local-Curl Remediation Scope

## Verified identity

- canonical repository: `rigolugo/pm_research`;
- accepted remediation candidate: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- candidate ZIP SHA-256: `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`;
- installation package ZIP SHA-256: `5c4594a01b6210b1b8865815d4617447c2470720e540ac03d4144836de48a72c`;
- installation base and parent: `cc2964840d197a40d1c4ef567b42eda762c0be0a`;
- verified installation commit: `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`;
- commit message: `Install accepted Revision 10 local-curl remediation scope`.

## Observed installation evidence

Gustavo's guarded local verification and push output established:

- local `HEAD` before push was the exact installation commit;
- local parent was the exact authorized base;
- branch was `main`;
- worktree status count was `0`;
- fetched `origin/main` equaled the authorized base before push;
- remote commits ahead: `0`;
- local commits ahead: `1`;
- the push was a non-force fast-forward from `cc296484...` to `ee4a639...`;
- post-push local `HEAD` and fetched `origin/main` both equaled the installation commit;
- final worktree status count was `0`.

GitHub independently exposed commit `ee4a639f9a9429e642391f1fb1e0ab356a6f965a` with the expected message and parent chain.

## Exact installation boundary

The installation changed exactly `17` documentation paths:

- one complete replacement:
  `project_context/implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`;
- sixteen new files under:
  `project_context/implementation_handoffs/local_curl_rev23_i0/remediation_scope/`.

The exact path inventory is preserved by the installation package metadata. No
live path under `pm_research/` or `tests/` changed. The accepted Revision 10
scope package and preserved checkpoint payload were not modified.

## Decision effect

The accepted remediation scope is now:

`INSTALLED_AND_SENTINEL_VERIFIED`

Its authorization effect remains:

`NONE`

No implementation starting SHA or source-gated commit is selected. No Claude
implementation prompt is active.

## Remaining unauthorized

Implementation, source synchronization, source/test authoring, test collection
or execution, imports, compilation, lint, typing, coverage, CI, rollback,
restoration, overwrite, checkpoint promotion, project execution, local
research-data reads, curl/API/vendor/network activity, subprocess execution,
artifact production, R2, P1/P2/P3, scoring, probe execution, and gate changes
remain unauthorized.

The two provenance gaps remain open and independent:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.
