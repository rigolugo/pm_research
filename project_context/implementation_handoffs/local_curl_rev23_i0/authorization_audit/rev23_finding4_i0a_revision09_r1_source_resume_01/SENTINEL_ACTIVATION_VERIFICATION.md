# Sentinel Activation Verification — Revision 09 R1

Decision: **APPROVE — R1 ACTIVE**

Authorization ID:
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`

## Verified activation identity

- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`;
- accepted scope archive SHA-256:
  `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`;
- verified Revision 09 installation commit:
  `c4e8b1011c51272042decac4bc89e762d767a72a`;
- verified authorization-installation and source-gated commit:
  `1e1afb29791f42c286b45d3b576f74926add8dce`;
- activation verification date: `2026-07-24`;
- Gustavo explicit Claude-handoff authorization date: `2026-07-24`.

Sentinel verified that the authorization-installation commit is exactly one
linear documentation-only commit after the accepted Revision 09 installation,
that the accepted Revision 09 scope remained unchanged, and that no
`pm_research/`, `tests/`, dependency, research-data, empirical, or runtime path
changed in the authorization installation.

## Active boundary

The sole writable path is:

`pm_research/local_curl_per_side/prepared_evidence.py`

Required starting SHA-256:

`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

The immutable exact twelve-path baseline has SHA-256:

`061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`

The other eleven baseline paths remain read-only. Claude must use local `HEAD`
`1e1afb29791f42c286b45d3b576f74926add8dce` and satisfy `SOURCE_GATE.md` before editing.

## Continuing prohibitions

This activation does not authorize test-source editing, test collection or
execution, project imports or execution, compilation, lint, type checking,
coverage, CI, another source-file edit, dependencies, CLI/config/generated
files, implementation ZIP reconstruction, research data, empirical artifacts,
API/RPC/vendor/Dune/curl/general network activity, Claude Git history or remote
writes, R2, P1/P2/P3, scoring, probe execution, or gate changes.

This record activates only the accepted one-file R1 source checkpoint. It does
not expand or amend the accepted Revision 09 contract.
