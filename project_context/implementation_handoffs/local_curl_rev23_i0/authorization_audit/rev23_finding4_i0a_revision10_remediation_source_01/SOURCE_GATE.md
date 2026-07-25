# Source Gate — Revision 10 Remediation Source Authoring

The gate is evaluated after the authorization package is canonically installed and Sentinel-verified, but before Claude edits any file.

## Ordered predicates

1. Gustavo authorization record is present.
2. Sentinel authorization decision is present.
3. Authorization package checksums match `SHA256SUMS.txt`.
4. Canonical `HEAD` equals the Sentinel-verified authorization-install commit.
5. Current branch is exactly `main`.
6. Worktree has no tracked, untracked, staged, or unstaged changes.
7. Every path in `TWELVE_PATH_STARTING_SHA256SUMS.txt` exists.
8. Every path's SHA-256 equals the declared value.
9. The controlling Revision 10 and accepted remediation package identities match.
10. Allowed-new-files is exactly `NONE`.
11. No additional source/test path or unauthorized activity is required.
12. No material ambiguity remains.

The first failed predicate returns:

`STOP_REV10_REMEDIATION_SOURCE_GATE_FAILED`

with the exact predicate number, expected identity, and observed identity. No edit, restore, overwrite, or checkpoint promotion is permitted after a failed predicate.

Only Sentinel acceptance of the complete gate output may establish:

`REV10_REMEDIATION_SOURCE_GATE_CLEAR`

That result permits only the exact source-authoring stage. It does not authorize test-source authoring, tests, imports, execution, data/network access, Git history writes, or downstream work.
