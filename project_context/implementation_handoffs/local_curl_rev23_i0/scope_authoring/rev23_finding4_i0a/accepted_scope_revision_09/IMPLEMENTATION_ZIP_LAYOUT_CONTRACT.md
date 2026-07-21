# Implementation ZIP Layout Contract — Revision 09

This retained layout is descriptive only. Revision 09 does not authorize creation, modification, or submission of an implementation package.

A later separately accepted and authorized implementation ZIP may contain only:

1. the exact candidate source paths in `PROPOSED_AUTHORIZED_FILE_MATRIX.md`;
2. the exact unexecuted test-source paths in that matrix;
3. package-only static reports explicitly required by the active authorization; and
4. one `SHA256SUMS.txt` covering every other member exactly once and excluding itself.

The package must not contain dependencies, CLI/config changes, generated code, runtime registration, duplicated grammar tables, reverse imports, runtime artifacts, empirical artifacts, caches, bytecode, local data, or Git metadata.

A future package must record separately:

- governing accepted-contract hashes;
- scope-review anchor `88362521fe9ef247708e4d7b5f90753784b8b88e`;
- then-current active authorization-package identity and hash;
- then-current source-gated local HEAD.

None may substitute for another. Scope-review acceptance does not create an implementation authorization or source gate.

Revision 09 changes no candidate source/test path and no package-layout rule. Any later implementation review must identify the Sentinel-accepted scope revision and its separately authorized source gate; `1e963bb6e8387aff071d697a416fa558956e571e` is recorded here only as the canonical source-gated HEAD supplied for this SPEC-ONLY review.
