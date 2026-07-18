# Implementation Authorization Scope — REV23 Finding 4 I0A

Decision: **DEFER — REVISION 08 SCOPE ACCEPTED; IMPLEMENTATION NOT AUTHORIZED**

## Accepted scope identity

- canonical scope-review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- reviewed archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- canonical scope path:
  `scope_authoring/rev23_finding4_i0a/`
- accepted maximum candidate matrix: six source paths and six test-source paths

The prior Amendment 03 I0 authorization is `SUPERSEDED_INACTIVE`.

Revision 08 scope acceptance does not authorize Claude to synchronize sources,
author files, write tests, execute code, or produce an implementation package.
The commit containing this scope installation must first be returned to Sentinel
for verification.

## Current activity status

- Scope preparation/review: COMPLETE — Revision 08 accepted.
- Canonical manual upload by Gustavo: REQUIRED.
- Sentinel verification of the resulting commit: REQUIRED.
- Source synchronization: NOT AUTHORIZED.
- Implementation-source authoring: NOT AUTHORIZED.
- Test-source authoring: NOT AUTHORIZED.
- Test execution: NOT AUTHORIZED.
- Python/project-code execution or import: NOT AUTHORIZED.
- Local research-data reads: NOT AUTHORIZED.
- Network/API/RPC/vendor/curl: NOT AUTHORIZED.
- Replay, regeneration, or empirical work: NOT AUTHORIZED.
- Artifact production: NOT AUTHORIZED.
- Git writes by ChatGPT or Claude: NOT AUTHORIZED.
- P1/P2/P3, scoring, probe execution, and gate changes: NOT AUTHORIZED.

## Future implementation boundary

A later bounded implementation-authoring stage requires all of the following:

1. Sentinel verification of the canonical commit containing this scope package;
2. Gustavo's separate explicit implementation authorization;
3. a new active Sentinel handoff pinned to that verified commit;
4. the exact accepted twelve-path matrix and no additional paths;
5. explicit status for source sync, test-source authoring, test execution,
   project imports, local-data reads, network/subprocess use, artifact production,
   and Git writes.

Specification acceptance is not implementation authorization. Implementation
source acceptance would not authorize tests or execution.

Claude must return `STOP_IMPLEMENTATION_NOT_AUTHORIZED` unless and until the
future active implementation package satisfies every boundary above.
