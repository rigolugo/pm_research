# Sentinel Implementation Authorization — REV23 Finding 4 I0A

Decision: **APPROVE**

## Authorized stage

Bounded implementation-source and unexecuted test-source authoring for accepted
scope `REV23_FINDING4_I0A_SCOPE_REVISION_08`.

- authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`
- verified canonical base: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- scope-review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- accepted scope archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- authorized repository paths: exactly twelve, listed in `AUTHORIZED_FILE_MATRIX.md`

## Activation condition

This authorization becomes active only after Sentinel verifies the canonical
commit containing this exact authorization package. Claude must use that
Sentinel-verified authorization-install commit as the source-gated local HEAD.

## Authorized activities

- read-only synchronization of `rigolugo/pm_research` to the exact source-gated HEAD;
- reading canonical repository source and accepted contract/scope files;
- creating or editing only the exact twelve authorized paths;
- authoring the six declared test-source files without executing them;
- static text/JSON inspection and standalone standard-library validation that
  does not import or execute repository modules;
- local `git status` and `git diff`, file listing/comparison, SHA-256 calculation,
  and ZIP assembly for the implementation review package;
- producing only the implementation review ZIP, static report, and checksum inventory.

## Unauthorized activities

- tests, pytest, unittest discovery, lint, type checking, coverage, CI, or compilation;
- importing or executing `pm_research` or any authored repository module;
- research-data, local run-artifact, empirical-output, credential, or wallet reads;
- Polymarket, API, RPC, vendor, Dune, curl, or general internet access;
- replay, regeneration of project artifacts, scoring, P1/P2/P3, or probe execution;
- dependency, CLI, config, generated-code, runtime-registration, filesystem-adapter,
  cache, bytecode, or Git-metadata additions;
- editing any repository path outside the exact twelve-path matrix;
- commit, branch/ref, push, pull request, merge, or other Git history/remote write.

Implementation-authoring authorization does not authorize test execution. An
implementation package must return to Sentinel for static conformance review.
