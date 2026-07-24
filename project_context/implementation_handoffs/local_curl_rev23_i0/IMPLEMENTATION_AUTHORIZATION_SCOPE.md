# Revision 09 R1 Controlling Authorization Scope

Decision: **APPROVE — ACTIVE ONE-FILE R1 SOURCE RESUME**

Authorization ID:
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

Revision 09 is canonically installed and Sentinel-verified at
`c4e8b1011c51272042decac4bc89e762d767a72a`.

Sentinel verified the exact authorization-installation and source-gated commit:

`1e1afb29791f42c286b45d3b576f74926add8dce`

Gustavo explicitly authorized the R1 handoff to Claude on `2026-07-24`.
Claude may edit only:

`pm_research/local_curl_per_side/prepared_evidence.py`

Required starting SHA-256:

`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

The exact twelve-path starting state is the immutable
`authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt`,
SHA-256
`061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`.
The other eleven paths are read-only.

## Required implementation correction

Within the sole writable file, Claude MUST:

1. narrow `_PrivateDescriptorSetInvariantCode` to the exact five Revision 09
   outcomes;
2. remove the two obsolete logical-hash-nullability and partition-binding private
   outcomes;
3. remove obsolete silent-deferral comment or behavior;
4. enforce the exact private reducer order and closed private result domain;
5. ensure every `validate_prepared_descriptor_set` branch returns only an accepted
   public-domain result, including malformed/missing partition-entry handling;
6. statically revalidate the corrected cross-member comparison, path validation,
   selected binding, seven-cell relation projection, descriptor-set ordering,
   same-ordinal binding, and complete payload traversal;
7. preserve all public interfaces, assurances, fixtures, hashes, role rows,
   frozen bindings, and T001–T165 expectations.

Fixtures and expected results MUST NOT be changed to accommodate implementation
behavior.

## Source gate and checkpoint

The source gate requires local `HEAD` to equal
`1e1afb29791f42c286b45d3b576f74926add8dce` and
`git status --short --untracked-files=all` to contain exactly the twelve baseline
paths, with exact hash equality and no thirteenth or other changed path. Only
`prepared_evidence.py` may change after the gate.

The edited existing `prepared_evidence.py` is the only source file submitted.
The static source report, exact path inventory, diff summary, and checksums are
returned as textual chat content and MUST NOT be created as repository files.
Implementation ZIP reconstruction is prohibited.

## Continuing prohibitions

This package does not authorize R2, another source-file edit, test-source editing,
test collection/discovery/execution, project imports or execution, compilation,
lint, type checking, coverage, CI, dependencies, CLI/config, generated files,
caches, bytecode, research data, empirical artifacts, API/RPC/vendor/Dune/curl or
general network use, Claude Git history/remote writes, P1/P2/P3, scoring, probe
execution, or gate changes.

---

## Historical pre-R1 Revision 09 status and Revision 08 authorization evidence

# Revision 09 Controlling Authorization Status

Decision: **STOP_IMPLEMENTATION_NOT_AUTHORIZED**

`REV23_FINDING4_I0A_SCOPE_REVISION_09` was accepted on `2026-07-20` as a narrow SPEC-ONLY correction. The Revision 08 authorization record retained below does not automatically carry forward and cannot authorize Revision 09 source synchronization, implementation-source authoring, test-source authoring, or an active Claude prompt. Any Revision 09 implementation stage requires a later separate Gustavo authorization and Sentinel handoff pinned to a verified post-install canonical commit.

The only current activity is documentation/checksum installation review, Gustavo's manual commit after Sentinel approval, and Sentinel verification of that commit.

---

## Historical Revision 08 authorization record — preserved verbatim

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
