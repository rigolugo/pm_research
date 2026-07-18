# Implementation ZIP Layout Contract — Revision 08

This is a future proposal only. It does not authorize creation of an implementation package.

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
