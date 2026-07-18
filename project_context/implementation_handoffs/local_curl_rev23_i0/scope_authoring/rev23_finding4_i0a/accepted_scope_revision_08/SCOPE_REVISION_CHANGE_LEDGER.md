# Scope Revision Change Ledger — Revision 08

Preceding package: the immediately prior accepted review draft. Canonical review anchor remains `88362521fe9ef247708e4d7b5f90753784b8b88e`.

1. Corrected the compatibility partition payload schema identity to `table:canonical_compatibility_analysis` everywhere.
2. Corrected the strict partition payload schema identity to `table:strict_audit_analysis` everywhere.
3. Resolved both `NORMAL_FINAL_MARKER` target branches directly from accepted `PATH_GRAMMAR_REGISTRY.json`; both bind `json:finalization_marker_v23`.
4. Materialized exact per-grammar schema IDs and a complete immutable frozen-production binding table.
5. Added the selected-schema-union subset invariant against the exact accepted RegistryDefinitionIndex.
6. Added exact identity agreement among role rows, frozen bindings, and accepted registry membership.
7. Added complete deterministic `analysis_compatibility` and `analysis_strict` SNAPSHOT_PUBLICATION fixtures and direct boundary cases.
8. Added direct normal-final-marker matrix closure and excluded-unit public stop cases.
9. Revalidated all 30 roles, schema IDs, bindings, registry counts/ordered IDs, results/assurances, fixtures/hashes, exports/imports, ZIP members, and checksums.

No implementation, executable test, project execution, empirical run, source synchronization, repository write, or active Claude handoff is authorized.
