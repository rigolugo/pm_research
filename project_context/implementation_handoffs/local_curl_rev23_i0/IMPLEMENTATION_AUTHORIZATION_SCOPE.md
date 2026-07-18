# Implementation Authorization Scope — REV23 Finding 4 I0A

Decision: **APPROVE — BOUNDED IMPLEMENTATION-SOURCE AND UNEXECUTED TEST-SOURCE AUTHORING AUTHORIZED**

## Authorization identity

- authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`
- verified pre-authorization canonical commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- scope-review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- accepted scope archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- active authorization package:
  `authorization_audit/rev23_finding4_i0a/`

Gustavo explicitly authorized the bounded Finding 4 I0A implementation-authoring
stage on `2026-07-18`. Sentinel approves the exact bounded stage recorded here.

## Activation

The authorization becomes active when Sentinel verifies the canonical commit
containing this exact package. That verified commit is the required source-gated
local HEAD. No further specification revision is required.

## Activity status

- Source synchronization: AUTHORIZED — read-only to source-gated HEAD only.
- Implementation-source authoring: AUTHORIZED — exact six source paths only.
- Test-source authoring: AUTHORIZED — exact six unexecuted test paths only.
- Test execution: NOT AUTHORIZED.
- Python/project-code execution or import: NOT AUTHORIZED.
- Static standard-library validation: AUTHORIZED within `ACTIVITY_BOUNDARIES.md`.
- Local repository source reads: AUTHORIZED.
- Research/local data reads: NOT AUTHORIZED.
- Network: LIMITED to read-only Git/GitHub synchronization.
- Subprocess/shell: LIMITED to static file/git-status/diff/hash/ZIP operations.
- Artifact production: LIMITED to implementation review package/report/checksums.
- Working-tree writes: AUTHORIZED only for the exact twelve paths.
- Git history or remote writes: NOT AUTHORIZED.
- P1/P2/P3, scoring, probe execution, and gate changes: NOT AUTHORIZED.

## Exact files

The exact create-only matrix is `authorization_audit/rev23_finding4_i0a/AUTHORIZED_FILE_MATRIX.md`.
No additional path is permitted.

## Required procedure

Claude must use the `pm-research-implementing` Skill. Skill invocation does not
expand this authorization. Claude must evaluate the accepted ordered source gate
before authoring and must stop on the first applicable halt. The completed
implementation package returns to Sentinel for static conformance review. Tests
and project execution require a later separate decision.
