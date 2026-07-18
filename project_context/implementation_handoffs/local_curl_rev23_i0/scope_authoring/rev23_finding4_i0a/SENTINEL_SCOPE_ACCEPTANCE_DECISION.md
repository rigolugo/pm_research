# Sentinel Scope Acceptance Decision — REV23 Finding 4 I0A

Decision: **APPROVE**

## Accepted scope identity

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- reviewed archive: `REV23_FINDING4_I0A_SCOPE_REVISION_08.zip`
- reviewed archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- accepted member count: `14`
- accepted canonical copy: `accepted_scope_revision_08/`

The accepted canonical copy must remain byte-identical to the reviewed archive
members. `ACCEPTED_SCOPE_MANIFEST.json` and `SCOPE_SHA256SUMS.txt` bind those
bytes in the canonical tree.

## Decision basis

Revision 08 closes the previously identified canonical-path, schema-domain,
assurance, result-payload, fixture, import-graph, and static-contract defects.
The accepted scope includes:

- the complete 30-role descriptor-selected schema and disposition matrix;
- exact canonical and structural hash projections;
- closed result, assurance, and stop domains;
- exact public API contracts and return-payload rules;
- 165 static contract cases;
- the accepted six-source and six-test candidate path matrix;
- an inactive Claude handoff and implementation ZIP-layout contract.

No blocking scope finding remains.

## Accepted file matrix status

The twelve paths in
`accepted_scope_revision_08/PROPOSED_AUTHORIZED_FILE_MATRIX.md` are accepted as
the maximum candidate I0A implementation-authoring matrix. They are not active
authorizations until Gustavo separately authorizes implementation and Sentinel
installs an active implementation handoff pinned to a verified canonical commit.

No additional source, test, dependency, CLI, configuration, generated-code,
filesystem-adapter, runtime-registration, artifact, data, cache, bytecode, or
Git-metadata path is accepted.

## Authorization state

This decision authorizes no implementation activity.

The following remain unauthorized:

- source synchronization;
- source or test-source authoring;
- tests, imports, lint, type checking, coverage, CI, or project execution;
- filesystem publication, recovery, rename, reopen, or fsync activity;
- local research-data or empirical-artifact access;
- network, API, RPC, vendor, Dune, or curl activity;
- replay, capture, regeneration, scoring, P1/P2/P3, or probe execution;
- Git writes by ChatGPT or Claude;
- gate changes.

Claude must return `STOP_IMPLEMENTATION_NOT_AUTHORIZED` until a later active
implementation package satisfies every authorization boundary.

## Next boundary

1. Gustavo manually uploads and commits this canonical update package.
2. Gustavo returns the resulting commit SHA to Sentinel.
3. Sentinel verifies exact paths, bytes, checksums, and repository state.
4. Gustavo may then separately decide whether to authorize bounded I0A
   implementation-source and test-source authoring.
5. Any implementation authorization requires a new Sentinel handoff. It does not
   authorize test execution, local-data access, network access, artifacts, or Git
   writes unless each is separately stated.

No Revision 09 follows automatically. Ordinary implementation questions must be
resolved from Revision 08; only a concrete material contradiction may reopen the
scope.
