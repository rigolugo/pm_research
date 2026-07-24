# Sentinel Scope Acceptance Decision — REV23 Finding 4 I0A

Decision: **APPROVE**

## Accepted scope identity

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- accepted base: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- Sentinel acceptance date: `2026-07-20`
- review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- canonical installation base: `1e963bb6e8387aff071d697a416fa558956e571e`
- reviewed archive: `REV23_FINDING4_I0A_SCOPE_REVISION_09.zip`
- reviewed archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
- accepted member count: `14`
- proposed immutable canonical copy: `accepted_scope_revision_09/`
- historical immutable copy: `accepted_scope_revision_08/`

The proposed 14-member Revision 09 directory MUST remain byte-identical to the accepted archive. `ACCEPTED_SCOPE_MANIFEST.json` and `SCOPE_SHA256SUMS.txt` bind the exact member sizes and SHA-256 values.

## Decision basis

Revision 08 contained a concrete material contradiction in the private descriptor-set invariant contract. `_validate_descriptor_set_invariants` was required to emit `PRIVATE_DESCRIPTOR_SET_LOGICAL_HASH_NULLABILITY_INVALID` and `PRIVATE_DESCRIPTOR_SET_PARTITION_BINDING_INVALID`, but its closed `_DescriptorSetInvariantInput` and `_DescriptorSetInvariantSummary` contained neither logical-hash values nor partition-entry/binding information. Those private outcomes were therefore impossible to determine through the accepted interface.

Revision 09 accepts the minimal SPEC-ONLY correction:

- preserve the existing closed private input and summary fields;
- narrow the private ordered outcomes to role cardinality, ordinal sequence, canonical-target uniqueness, sidecar relation, then valid;
- remove the two impossible private outcomes from the private enum and result contract;
- assign logical-hash-nullability validation to `validate_prepared_object_descriptor`; and
- assign same-ordinal partition-entry binding to `validate_prepared_descriptor_set`.

The complete package revalidates T001–T165, private traceability, and the full Revision 09 scope.

## Accepted file matrix status

The existing six-source and six-test maximum candidate matrix remains unchanged. Revision 09 acceptance does not activate it. No additional source, test, dependency, CLI, configuration, generated-code, filesystem-adapter, runtime-registration, artifact, data, cache, bytecode, or Git-metadata path is accepted.

## Supersession boundary

Revision 09 supersedes Revision 08 only for the private descriptor-set invariant contract described above. Revision 08 remains immutable historical accepted evidence. Public result codes, public assurances, public interfaces, error precedence, fixtures, hashes, all 30 role rows, frozen bindings, T001–T165 identities, and the twelve-path maximum matrix remain preserved except for directly required mechanical private-contract reconciliation.

## Authorization state

This decision authorizes no Revision 09 implementation activity. The Revision 08 implementation authorization `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01` does not automatically carry forward. No active Revision 09 Claude implementation prompt exists.

The following remain unauthorized:

- Revision 09 source synchronization;
- implementation-source or test-source authoring;
- tests, imports, lint, type checking, coverage, CI, compilation, or project execution;
- local research-data or empirical-artifact access;
- network, API, RPC, vendor, Dune, or curl activity;
- replay, capture, regeneration, scoring, P1/P2/P3, or probe execution;
- agent Git writes;
- gate changes.

## Canonical installation boundary

This acceptance decision is included in a documentation-only installation candidate. The candidate is not canonical until Sentinel statically approves it, Gustavo manually commits the exact files, and Sentinel verifies the resulting commit. The installation MUST preserve `accepted_scope_revision_08/` byte-identically and MUST contain no source/test or downstream paths.

## Next boundary

1. Sentinel statically reviews the Revision 09 canonical installation Revision 02 package.
2. On `APPROVE`, Gustavo manually uploads and commits only the exact documented files.
3. Gustavo returns the full commit SHA to Sentinel.
4. Sentinel verifies paths, bytes, checksums, preservation attestations, Revision 08 immutability, and absence of source/test changes.
5. Any Revision 09 implementation stage requires a later separate Gustavo authorization and Sentinel handoff.
