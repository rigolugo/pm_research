APPROVE — DOCUMENTATION_ONLY_INSTALLATION_AUTHORIZED

# Sentinel Installation Authorization — Accepted Revision 10 Remediation Scope

## Authorization basis

On `2026-07-24`, Gustavo explicitly authorized documentation-only installation of the accepted Revision 10 local-curl remediation-scope record.

## Exact installation base

`cc2964840d197a40d1c4ef567b42eda762c0be0a`

Stop on any base mismatch, dirty worktree, unexpected changed path, or checksum mismatch. Do not reset, merge, rebase, or force an installation over a mismatch.

## Authorized installation content

- one complete replacement file:
  `project_context/implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`;
- sixteen new files under:
  `project_context/implementation_handoffs/local_curl_rev23_i0/remediation_scope/`.

The complete path inventory is defined by the installation package's `PACKAGE_METADATA/CHANGED_PATHS.txt`.

## Explicit exclusions

No path under any of the following may change:

- `pm_research/`;
- `tests/`;
- accepted Revision 10 scope members;
- preserved checkpoint payload bytes;
- dependencies, packaging, CLI, configuration, runtime, data, empirical artifacts, or generated outputs.

## Installation state

The manual commit installs the accepted documentation as `INSTALLED_PENDING_SENTINEL_VERIFICATION`. It does not select an implementation starting SHA and does not activate a Claude handoff.

## Remaining unauthorized

Implementation, source/test authoring, tests, imports, compilation, lint, typing, coverage, CI, rollback, restoration, checkpoint promotion, project execution, local research-data reads, network/vendor/curl activity, subprocesses, artifact production, R2, P1/P2/P3, scoring, probe execution, and gate changes remain unauthorized.

ChatGPT performs no direct GitHub write. Gustavo applies, commits, and returns the resulting full commit SHA for Sentinel verification.
