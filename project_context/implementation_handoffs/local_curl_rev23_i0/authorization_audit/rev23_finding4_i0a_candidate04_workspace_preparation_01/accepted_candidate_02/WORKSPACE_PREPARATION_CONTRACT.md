# Candidate 04 Workspace-Preparation Contract

## Status and authority

`MATERIALIZED REVIEW CANDIDATE — NO EXECUTION AUTHORITY`

This file narrows only to the accepted Candidate 04 `WORKSPACE_PREPARATION`
stage. The accepted Candidate 04 files listed in `README_FIRST.md` control every
identity, predicate, stop, retry rule, and transition.

## Exact stage identity

- from state: `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED`
- required future authorization effect: `WORKSPACE_PREPARATION_ONLY`
- stage: `WORKSPACE_PREPARATION`
- success code: `CLEAR_C04_SOURCE_WORKSPACE_PREPARED`
- to state: `C04_SOURCE_WORKSPACE_READY`
- success decision owner: `SENTINEL`
- authoring started on success: `false`
- Git write observed on success: `false`
- execution activity observed on success: `false`
- predicate count: `18`

## Proposed exact Windows staging root

`C:\b1\rev23_candidate04_source_workspace_01`

The future gate MUST prove this exact root is outside every Git checkout or
linked worktree, outside the accepted capture evidence directory, outside every
project data or artifact directory, empty before instantiation, and free of all
Git metadata. Failure MUST NOT cause selection of another root.

## Exact twelve-path workspace identity

The tuple `(relative path, REGULAR_FILE, size_bytes, lowercase SHA-256)` is the
workspace identity. Git mode is inapplicable in this isolated workspace.

| Relative path | Size | SHA-256 | Future source stage |
|---|---:|---|---|
| `pm_research/local_curl_per_side/__init__.py` | 4187 | `200019940bbd2c2b8dbac7d322722c7eae43926264c1438ec4a60cfc26e12c93` | protected |
| `pm_research/local_curl_per_side/canonical.py` | 13752 | `60f3141184753d294b8e708a77f381bdd40d04e39c6d1101f2cc14de9a9704b3` | writable |
| `pm_research/local_curl_per_side/claim_hashes.py` | 7772 | `e9153abcbdb073a37d516056ff6fd657742c4d87620f557363855b3c6d728a3d` | protected |
| `pm_research/local_curl_per_side/finding4_registry.py` | 72248 | `06fd23245017fb538d06841d2b2b61f309f533959d16449ace588ccb6080e529` | writable |
| `pm_research/local_curl_per_side/governing_package.py` | 2984 | `75c9b5a19023d737d016bfd0e3e5b9b62ea7730355da7d555aa073192df79fec` | protected |
| `pm_research/local_curl_per_side/prepared_evidence.py` | 112338 | `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da` | writable |
| `tests/local_curl_per_side/test_canonical_i0a.py` | 8898 | `9122ee3a0a4aa93f485a7dc35dbd7420e59b07eeed646007baff4ef5ac652bcd` | protected |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | 15098 | `4e2c8d6d663238c8bd7d3a4f40047bf0888b2ccf64cd5fcf37ce85cd2f158878` | protected; baseline-support edit prohibited |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | 185401 | `fe7a602684b4861db1cb825c0b70f712c9242ef61386d1a76f80ea8f4fed42f8` | protected |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | 209566 | `c1b6a221a997e9c7d5aae0bf5c5bf98f38d0d1e8183bcabbebc8c7f1ac0550e4` | protected; baseline-support edit prohibited |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | 14302 | `c8e69789fc63eebff3d87f14ca6c94748872483e8fcffd541243ffa32e114679` | protected |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | 277359 | `c9c5f9e09136f70902dc70e809d82177303319f431f532126b5aee8d04c2ae37` | protected |

The five baseline-support edit prohibitions are:

- `pm_research/local_curl_per_side/__init__.py`
- `pm_research/local_curl_per_side/claim_hashes.py`
- `pm_research/local_curl_per_side/governing_package.py`
- `tests/local_curl_per_side/test_claim_hashes_i0a.py`
- `tests/local_curl_per_side/test_governing_package_i0a.py`

These values are copied from accepted `EXACT_PATH_AND_BYTE_MATRIX.json`; that
matrix controls any discrepancy.

## Exact accepted capture identity

- source artifact filename:
  `REV23_FINDING4_I0A_PROVENANCE_CAPTURE.zip`
- archive SHA-256:
  `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`
- source archive size: `487764` bytes
- total archive member count: `17`
- payload member count: `12`
- payload checksum entries: `12`
- payload checksum matches: `12`
- accepted and verified installation commit:
  `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`
- baseline-matching: `11`
- checkpoint-modified: `1`

WP04 binds the exact source archive identity and its total/payload composition.
WP05 separately binds closure of the exact twelve captured payload paths. The
archive's `17` total members MUST NOT be restated as twelve archive members, and
the twelve-path payload closure MUST NOT be used as a substitute for exact
archive identity.

## Ordered predicates and typed stops

The future gate MUST evaluate these in ordinal order and stop at the first
failure. Conditions, decision owners, retry eligibility, and retry owners are
the exact accepted values in `WORKFLOW_DOMAIN.json`; they are incorporated
without amendment.

| Ordinal | Predicate | Required condition summary | Exact stop |
|---:|---|---|---|
| 1 | `WORKSPACE_PREPARATION_STATE` | exact current state | `STOP_C04_STAGE_STATE_MISMATCH` |
| 2 | `WP01` | distinct Gustavo authorization plus active Sentinel handoff | `STOP_C04_AUTHORIZATION_NOT_ACTIVE` |
| 3 | `WP02` | canonical HEAD equals handoff-selected HEAD | `STOP_C04_CANONICAL_HEAD_MISMATCH` |
| 4 | `WP03` | all controlling records exact and readable | `STOP_C04_CONTROLLING_CONTRACT_UNAVAILABLE` |
| 5 | `WP04` | source archive filename, SHA-256, size, total/payload counts, checksum counts, acceptance, and installation identities exact | `STOP_C04_CAPTURE_PACKAGE_IDENTITY_MISMATCH` |
| 6 | `WP05` | exactly twelve declared captured payload paths, once each | `STOP_C04_CAPTURE_PATH_SET_MISMATCH` |
| 7 | `WP06` | all twelve sizes and hashes exact | `STOP_C04_CAPTURE_BYTE_IDENTITY_MISMATCH` |
| 8 | `WP07` | external non-Git Windows root | `STOP_C04_WORKSPACE_ROOT_INVALID` |
| 9 | `WP08` | zero workspace members before instantiation | `STOP_C04_WORKSPACE_NOT_EMPTY` |
| 10 | `WP09` | exact regular-file path, size, and hash identities | `STOP_C04_WORKSPACE_MEMBER_IDENTITY_INVALID` |
| 11 | `WP10` | no symlink, junction, reparse, alternate-path, or hard-link alias | `STOP_C04_WORKSPACE_ALIAS_OR_LINK_INVALID` |
| 12 | `WP11` | exactly twelve final workspace members and no extras | `STOP_C04_WORKSPACE_EXTRA_OR_MISSING_PATH` |
| 13 | `WP12` | three mandatory source and nine protected paths available exactly | `STOP_C04_MANDATORY_FILE_UNAVAILABLE` |
| 14 | `WP13` | no thirteenth workspace member or repository file required | `STOP_C04_NEW_FILE_OR_ADDITIONAL_PATH_REQUIRED` |
| 15 | `WP14` | no failed-gate repair, reuse, or false clear | `STOP_C04_FAILED_GATE_REPAIR_ATTEMPT` |
| 16 | `WP15` | no reliance on incomplete multi-round lineage | `STOP_C04_TRUSTED_MULTI_ROUND_LINEAGE_REQUIRED` |
| 17 | `WP16` | no Git write | `STOP_C04_UNAUTHORIZED_GIT_WRITE` |
| 18 | `WP17` | no test/import/compile/execute/data/network/artifact activity | `STOP_C04_UNAUTHORIZED_EXECUTION_ACTIVITY` |

The future handoff MUST select canonical HEAD
`689e546e588d557c96f28bc722c3f159d635f2c1` unless a later accepted contract
explicitly changes it. A mismatch halts at `WP02`; it does not authorize a
different base.

## Alias and member closure

Every workspace member and ancestor beneath the root MUST satisfy accepted
`WINDOWS_WORKSPACE_IDENTITY.md`, including rejection of case-folded duplicates,
short-name or alternate-stream substitution, path escape, shared hard links,
backup, cache, bytecode, generated, temporary, and any extra workspace member.

## Success effect

Success records only that the exact isolated workspace is prepared. It does not
authorize source authoring. Sentinel must accept the result and Gustavo must
separately authorize `SOURCE_AUTHORING`; a new active Sentinel handoff is also
required by the accepted next-stage row.
