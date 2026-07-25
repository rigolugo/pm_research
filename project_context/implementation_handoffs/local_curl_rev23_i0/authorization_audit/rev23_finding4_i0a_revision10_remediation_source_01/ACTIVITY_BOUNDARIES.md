# Activity Boundaries — Revision 10 Remediation Source Stage

| Activity | Status after activation | Boundary |
|---|---|---|
| source authoring | authorized | exactly three writable source paths, one atomic candidate |
| test-source authoring | unauthorized | separate later package required |
| test collection/execution | unauthorized | separate execution authorization required |
| project imports/execution | unauthorized | no import or execution of repository modules |
| static parsing | authorized | text/JSON/standard-library parsing only; no project import |
| local Git inspection | authorized | status/diff/path inventory only; no history writes |
| SHA-256/file/archive utilities | authorized | implementation evidence outside repo only |
| local research-data reads | unauthorized | none |
| network/API/RPC/vendor/Dune/curl | unauthorized | none |
| dependencies/CLI/config/runtime | unauthorized | none |
| project artifact production | unauthorized | no research/runtime artifacts |
| implementation-review package | authorized | exact declarative review evidence only |
| Git commit/branch/push/PR | unauthorized for Claude | Gustavo/manual workflow only |
| R2/P1/P2/P3/scoring/probe/gate | unauthorized | separate decisions required |

## Minimal-diff rule

Only accepted Revision 10 obligations may be implemented. Unrelated formatting, comments, docstrings, renaming, sorting, helper extraction, cleanup, dependency changes, and adjacent edits are prohibited. Contract-required private helpers are permitted only where required by the accepted scope.

## Mandatory halt conditions

Halt before editing or immediately upon discovery when HEAD, branch, worktree state, any of the twelve starting hashes, path existence, accepted package identity, or activity boundary differs. Also halt if implementation requires a new file, extra path, dependency/config change, second path parser, old private result reachability, tests, project execution, network/data access, or checkpoint restoration.

A halt must report observed identities and must not repair the starting state, restore historical bytes, or broaden scope.
