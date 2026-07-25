# PROVENANCE NOTES — REV23 Finding 4 I0A (read-only capture)

## Scope
Read-only provenance capture. No source/test file edited, no repository file
created, no project module imported or executed, no tests/compile/lint/type/
coverage, no network, no Git write (commit/branch/push/reset/restore/checkout).
This package is NOT an acceptance and does not authorize implementation.

## Git state
- repository_root: /home/claude/pm_research_repo
- local_HEAD: 1e1afb29791f42c286b45d3b576f74926add8dce (DETACHED)
- canonical_commit_requested: 71061065d91fc391e934d7e79a29eefc898cfe82
  -> NOT present in the local object store; local HEAD was not moved.
- All twelve inspected paths are UNTRACKED at HEAD (the `local_curl_per_side/`
  directory is not committed on this ref).

## Baseline authority
Eleven read-only paths compared against the committed manifest
`.../rev23_finding4_i0a_revision09_r1_source_resume_01/REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt`
(manifest self-hash 061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7).

## Labels
- BASELINE_MATCHING (11): __init__.py, canonical.py, claim_hashes.py,
  finding4_registry.py, governing_package.py, and all six test files — each
  byte-identical to its baseline manifest entry.
- CHECKPOINT_MODIFIED (1): prepared_evidence.py, sha256
  fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da, 112338 bytes.
  This is the sole writable file at its current in-session checkpoint (reported
  as "v8"). It is NOT the original R1 baseline and is NOT Sentinel-accepted.
- UNRESOLVED_PROVENANCE: none.
- MISSING: none (all twelve exist).

## Original R1 baseline for prepared_evidence.py
Expected historical baseline sha256
8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07.
A full-tree search of /home/claude/pm_research_repo (excluding .git) found NO
file with that hash. The current prepared_evidence.py has diverged from that
baseline through in-session edits; the original baseline bytes are not
recoverable from the local repository tree. (The prior-identified implementation
-review archive REV23_FINDING4_I0A_IMPLEMENTATION_REVIEW.zip carries a Rev08
prepared_evidence.py at 835a60c9..., which is also NOT 8b8e9320..., so it does
not supply the R1 baseline either.)

## Authoring-round evidence available locally
mtimes cluster 2026-07-19/07-20 for the eleven baseline files; prepared_evidence.py
mtime 2026-07-23 reflects the latest in-session checkpoint write. No per-round
authoring log is embedded in these files themselves; round lineage lives in the
session record, not in on-disk metadata.
