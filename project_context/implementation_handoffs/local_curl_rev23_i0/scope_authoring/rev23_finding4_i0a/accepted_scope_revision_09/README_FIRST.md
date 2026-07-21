# README FIRST — REV23 Finding 4 I0A Scope Revision 09

Status: **PROFESSOR AMENDMENT CANDIDATE FOR SENTINEL REVIEW — NOT ACCEPTED**

Canonical scope-review anchor:

`88362521fe9ef247708e4d7b5f90753784b8b88e`

Accepted base:

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`
- accepted-scope commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- source-gated implementation HEAD: `1e963bb6e8387aff071d697a416fa558956e571e`
- accepted Revision 08 archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`

Revision 09 retains every verified Revision 08 correction and every exact reconciled fixture byte. It makes one narrow contract correction: `_validate_descriptor_set_invariants` is limited to the four failures decidable from its unchanged closed input plus success. Logical-hash nullability remains the responsibility of `validate_prepared_object_descriptor`; same-ordinal partition-entry binding remains the responsibility of `validate_prepared_descriptor_set`.

Definition of done: **the complete package advertises no private descriptor-set outcome that cannot be decided from `_DescriptorSetInvariantInput`, while preserving every public interface, public result code, assurance tuple, error precedence, exact fixture byte/hash, and twelve-path maximum matrix.**

## Read order

1. `REV23_FINDING4_I0A_SCOPE_REVISION_09.md`
2. `I0A_VALIDATION_ASSURANCE_LEVELS.md`
3. `I0A_ROLE_CONTENT_SCHEMA_DISPOSITION_MATRIX.json`
4. `I0A_PUBLIC_API_CONTRACT.json`
5. `I0A_HASH_PROJECTION_CONTRACT.json`
6. `I0A_STOP_AND_RESULT_DOMAIN.md`
7. `I0A_STATIC_TEST_CASE_MATRIX.json`
8. `PROPOSED_AUTHORIZED_FILE_MATRIX.md`
9. `PROPOSED_ACTIVITY_STATUS.md`
10. `IMPLEMENTATION_ZIP_LAYOUT_CONTRACT.md`
11. `PROPOSED_CLAUDE_HANDOFF_INACTIVE.md`
12. `SCOPE_REVISION_CHANGE_LEDGER.md`
13. `SHA256SUMS.txt`

## Revision 09 controlling correction

- `_DescriptorSetInvariantInput` fields are unchanged: `summaries` and `expected_role_counts` only.
- `_DescriptorSetInvariantSummary` fields are unchanged: ordinal, role, canonical target path, sidecar flag, and paired ordinal only.
- `_PrivateDescriptorSetInvariantCode` is narrowed to exactly four failures plus `PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID`.
- `_validate_descriptor_set_invariants.ordered_outcomes` is exactly role cardinality, ordinal sequence, canonical-target duplicate, sidecar relation, then valid.
- The two impossible private outcomes are removed from every machine-readable enum, helper contract, fixture, and static-domain assertion.
- Public result codes, public assurance tuples, public signatures, public error precedence, all exact data fixtures and hashes, all 30 role rows, all frozen bindings, and the twelve-path maximum matrix are unchanged.
- Existing T001–T165 case IDs, order, constructed inputs, expected result codes, expected assurance tuples, and expected return payloads are preserved. Only the exact enum-domain fixture, private payload wording, and directly affected traceability text change.

This package contains specification text, declarative JSON contracts, and static case descriptions only. It contains no implementation, executable project tests, source synchronization, project-code execution, local-data access, empirical artifacts, or Git writes.

## Sentinel review focus

Verify that the private reducer can decide every remaining outcome from its unchanged input; that the two removed outcomes do not remain in machine-readable domains; that public nullability and partition-binding ownership is explicit; and that the complete Revision 09 package preserves the accepted Revision 08 public and fixture surface.
