# Scope Revision Change Ledger — Revision 09

## Status and base

- mode: `AMEND` plus complete materialization;
- status: Professor amendment candidate for Sentinel review;
- accepted base scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`;
- accepted-scope commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`;
- source-gated implementation HEAD: `1e963bb6e8387aff071d697a416fa558956e571e`;
- accepted Revision 08 archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`;
- canonical review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`.

## Accepted finding corrected

Revision 08 required `_validate_descriptor_set_invariants` to emit two private failures that were not decidable from its closed input or summary. Revision 09 preserves those types exactly and removes the impossible private outcomes instead of widening the interface.

## Exact changed contract members

### `I0A_PUBLIC_API_CONTRACT.json`

1. package schema identity advanced from `rev08`/`8` to `rev09`/`9`;
2. `global_rules.private_outcome_boundary._validate_descriptor_set_invariants` narrowed to four decidable failures plus valid;
3. `global_rules.private_result_payload_contracts._PrivateDescriptorSetInvariantResult.every_private_error` bound to the exact four private failure codes;
4. `_PrivateDescriptorSetInvariantCode.values` narrowed to the exact five-value domain;
5. `_PrivateDescriptorSetInvariantResult.result_payload_contract.every_private_error` mechanically reconciled;
6. `_validate_descriptor_set_invariants.rule` and `.ordered_outcomes` narrowed without changing signature or output type;
7. `validate_prepared_object_descriptor.rule` explicitly owns logical-hash nullability;
8. `validate_prepared_descriptor_set.rule` explicitly owns same-ordinal partition path/identity/logical-hash binding.

The fields of `_DescriptorSetInvariantInput` and `_DescriptorSetInvariantSummary` are byte-for-byte unchanged from Revision 08.

### `I0A_STATIC_TEST_CASE_MATRIX.json`

1. package schema identity advanced from `rev08`/`8` to `rev09`/`9`;
2. `fixture_catalog.exact_enum_domains` removes the two impossible private codes;
3. `fixture_catalog.exact_result_payload_contracts` binds `every_private_error` to the exact four retained failures;
4. `construction_algorithm` adds the private decidability closure rule;
5. directly affected existing case traceability is reconciled for: `T041`, `T042`, `T043`, `T044`, `T045`, `T107`, `T108`, `T109`, `T146`, `T149`, `T152`, `T153`;
6. transitively traversing cases revalidated unchanged: `T009`, `T068`, `T070`.

No existing case ID, order, constructed input, expected result/error, expected assurance tuple, or expected return payload changes. The case set remains exactly T001–T165.

### Prose and package identity members

`README_FIRST.md`, `REV23_FINDING4_I0A_SCOPE_REVISION_09.md`, `I0A_VALIDATION_ASSURANCE_LEVELS.md`, `I0A_STOP_AND_RESULT_DOMAIN.md`, `PROPOSED_AUTHORIZED_FILE_MATRIX.md`, `PROPOSED_ACTIVITY_STATUS.md`, `IMPLEMENTATION_ZIP_LAYOUT_CONTRACT.md`, `PROPOSED_CLAUDE_HANDOFF_INACTIVE.md`, and this ledger are reconciled to Revision 09 and the narrow correction.

`I0A_ROLE_CONTENT_SCHEMA_DISPOSITION_MATRIX.json` and `I0A_HASH_PROJECTION_CONTRACT.json` change package schema identity only; their behavioral content is unchanged.

## Explicitly preserved

- every public result code and assurance tuple;
- every public function name, signature, output dataclass, result domain, and ordered error precedence;
- all 30 role rows, path grammars, placeholder domains, frozen bindings, registry counts and ordered IDs;
- all exact JSON/byte fixtures, physical lengths, physical SHA-256 values, logical hashes, plan-derived IDs, and return-payload expectations except the exact private enum-domain contract fixture;
- the twelve-path maximum matrix;
- all authorization and non-authorization boundaries.

## Revalidation boundary

The complete package was statically revalidated, not only the delta: JSON closure, private/public symbols, enum domains, case construction, result coverage, assurance mappings, fixture references, unchanged fixture-byte identities, role/binding counts, imports/exports, package membership, internal checksums, deterministic ZIP metadata, and detached SHA-256.

No implementation, executable test, project execution, research-data access, empirical artifact, source synchronization, or Git write was performed or authorized.
