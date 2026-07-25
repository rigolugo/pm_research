# Revision 10 Local-Curl Implementation Remediation Scope — Candidate 01

## 1. Status

- mode: `SPECIFY`;
- status: `REVIEW CANDIDATE`;
- draft owner: Professor;
- specification reviewer and decision owner: Sentinel;
- implementation/execution authorization owner: Gustavo;
- implementation owner after acceptance and authorization: Claude.

Professor does not approve this package.

## 2. Purpose and canonical base

Canonical repository: `rigolugo/pm_research`  
Canonical base inspected: `cc2964840d197a40d1c4ef567b42eda762c0be0a`  
Controlling accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`  
Preserved checkpoint evidence: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`  
Checkpoint state: `NOT_ACCEPTED`; authorization effect: `NONE`; static result: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`.


The package defines a future correction contract only. It does not select or activate implementation bytes.

## 3. In scope

The future remediation MUST correct all eight verified static defects as one coordinated Revision 10 source change:

1. complete the three mandatory source-path responsibilities;
2. materialize the four public result codes and total assurance mappings;
3. enforce closed `UnitContext` validation at every applicable public surface;
4. make `finding4_registry.py` the sole normalized-path decomposition owner;
5. materialize typed descriptor pre-binding and deterministic global reductions;
6. replace the superseded private descriptor-set reducer shape;
7. implement the exact selected-payload predicate sequence and typed query projection;
8. route selected JSON object validation in the unit validator through the selected wrapper and propagate non-success unchanged.

## 4. Out of scope

The remediation MUST NOT alter accepted behavior not named above. In particular it MUST NOT change hash projection algorithms, governing-package pins, CLI/runtime behavior, dependencies, packaging, configuration, exported symbols, filesystem boundaries, network behavior, research-data behavior, assurance levels, accepted success payloads, or downstream project gates.

It MUST NOT resolve, close, or reinterpret the two provenance gaps.

## 5. Mandatory source ownership

### 5.1 `canonical.py`

This file MUST:

- add exactly these `I0AResultCode` values: `ERR_UNIT_CONTEXT_INVALID`, `ERR_SEMANTIC_FAMILY_BINDING_MISMATCH`, `ERR_RUN_ID_BINDING_MISMATCH`, and `ERR_REUSE_SOURCE_TARGET_MISMATCH`;
- include each code exactly once in the effective result inventory;
- map every new error to `ValidationResult(code=<code>, established_assurances=())` with no additional payload fields;
- preserve all existing codes, assurance enums, success payloads, and public constructors;
- avoid unrelated enum reorder or formatting changes except the minimum ordering required by the accepted Revision 10 inventory.

`canonical.py` MUST NOT implement UnitContext checks, path parsing, descriptor reductions, or selected-wrapper behavior.

### 5.2 `finding4_registry.py`

This file MUST own:

- the semantic-family domain and bidirectional path expansion mapping;
- the exact frozen `SchemaBinding` type and four-field selection key;
- `_FrozenPathBindings`, `_PrivatePathMatchCode`, `_PathMatchResult`, and `_match_and_decompose_normalized_relative_path`;
- the sole frozen-grammar matcher and placeholder decomposition;
- the unchanged public `validate_normalized_relative_path` result mapping;
- the unchanged public resolver domain, including direct `ERR_BINDING_QUERY_INVALID` reachability.

It MUST NOT import `prepared_evidence.py`. Private matcher/decomposition symbols MUST remain unexported. No caller-supplied grammar, runtime registration, alias regex, local split, prefix slice, or second parser is permitted.

### 5.3 `prepared_evidence.py`

This file MUST own:

- UnitContext validation at applicable public wrappers;
- typed descriptor pre-binding results and reduction;
- reuse, semantic-family, and run-binding decisions;
- public descriptor and descriptor-set stage order;
- the narrowed private set reducer;
- `_project_selected_binding_query` and selected-wrapper stage order;
- unit-level delegation and exact result propagation.

It MUST consume registry-produced typed bindings. It MUST NOT directly import frozen grammar tables, reconstruct path identity with string operations, or duplicate registry grammar logic.

## 6. Closed UnitContext contract

The accepted input is the existing canonical `UnitContext` type. The remediation MUST preserve its existing field inventory and constructor. No new field, coercion, alias, mapping input, or structural-lookalike input is introduced by this scope.

For `PreparedUnitKind.SNAPSHOT_PUBLICATION`, validation MUST require:

- `unit_kind` is the accepted enum value; unsupported unit kind returns `STOP_UNIT_KIND_NOT_ACCEPTED_I0A` before context validation;
- `subject_family` is non-null and exactly one of `capture`, `analysis_compatibility`, or `analysis_strict`;
- path-form aliases including `analysis/compatibility` and `strict` as a semantic alias are invalid (`strict` remains only the path lexeme for semantic value `analysis_strict`);
- `subject_sequence` is non-null; `type(value) is int`; `bool` is invalid; inclusive range is `0..18446744073709551615`.

Any invalid context returns `ERR_UNIT_CONTEXT_INVALID` with empty assurances. Context validation occurs immediately after the unit-kind gate and before claim parsing, structural JSON parsing, registry-byte validation, descriptor validation, physical reconciliation, or nested delegation. No later predicate may mask an invalid context.

## 7. Sole normalized-path decomposition

The sole matcher MUST have the accepted signature:

`_match_and_decompose_normalized_relative_path(path: str, grammar_id: FrozenPathGrammarId) -> _PathMatchResult`.

Inputs are the exact caller-supplied Python `str` and exact frozen enum member. No normalization or coercion occurs before validation.

`_PathMatchResult` is closed over `code` and `bindings`. Outcomes are ordered:

1. `PRIVATE_PATH_LEXICAL_INVALID`, bindings null;
2. `PRIVATE_PATH_GRAMMAR_MISMATCH`, bindings null;
3. `PRIVATE_PATH_MATCH_VALID`, bindings non-null.

`_FrozenPathBindings` has exactly: `grammar_id`, non-null `run_id`, and nullable-by-grammar `semantic_family`, `snapshot_sequence`, `partition_id`, `fence_sequence`, `unit_kind`, `prepared_unit_id`, and `object_ordinal`.

`validate_normalized_relative_path` MUST call the matcher exactly once, map lexical to `ERR_PATH_LEXICAL_INVALID`, grammar to `ERR_PATH_GRAMMAR_MISMATCH`, valid to `I0A_VALID_A1_PATH`, and discard private bindings.

Prohibited duplicate ownership includes `str.split`, `rsplit`, suffix stripping, prefix slicing, first-`run_` scanning, direct frozen-table imports, caller grammar tables, local source-identity reconstruction, or any parallel grammar implementation in `prepared_evidence.py`.

## 8. SchemaBinding and descriptor pre-binding

The frozen `SchemaBinding` fields remain exactly:

`binding_id`, `role`, `unit_kind`, `publication_mode`, `target_grammar_id`, `content_schema_id`, `logical_sha256_nullability`, `sidecar_rule`.

Selection MUST use only:

`(descriptor.object_role, unit_context.unit_kind, descriptor.publication_mode, descriptor.content_schema_id)`.

Exactly one typed match is required; zero or multiple matches return `ERR_ROLE_DISPOSITION_INVALID`. Actual `descriptor.logical_sha256` nullability MUST NOT affect selection.

`_DescriptorPreBindingResult` MUST be a frozen closed result containing: `code`, exact non-coerced `object_ordinal`, selected `SchemaBinding`, canonical-target `_PathMatchResult`, and durable-source `_PathMatchResult`.

The closed code domain is:

- `PRIVATE_DESCRIPTOR_PRE_BINDING_VALID`;
- `PRIVATE_DESCRIPTOR_PATH_LEXICAL_INVALID`;
- `PRIVATE_DESCRIPTOR_PATH_GRAMMAR_MISMATCH`;
- `PRIVATE_DESCRIPTOR_REUSE_SOURCE_TARGET_MISMATCH`;
- `PRIVATE_DESCRIPTOR_SEMANTIC_FAMILY_BINDING_MISMATCH`.

The pre-binding validator MUST inspect both path fields without short-circuiting the other field. It evaluates local lexical before grammar, then reuse equality, then family binding.

Fault evidence MUST contain exact `object_ordinal`, nullable `path_field` (`canonical_target_path` or `durable_source_path` for lexical/grammar; null for reuse/family), and `source_code`.

The global reducer MUST collect all descriptors before selecting a class. Its total order is lexical, grammar, reuse, family, valid. Failure returns every fault in the selected highest-precedence class, ordered by numeric `object_ordinal`, then canonical target before durable source. Duplicate ordinals are retained; the reducer does not choose an authoritative descriptor. Success returns the exact ordered result tuple and null evidence.

## 9. Global semantic and run reductions

### 9.1 Reuse reduction

For a selected binding with `publication_mode == REUSE_IMMUTABLE_SOURCE`, both paths MUST first be lexical-valid and match the selected target grammar. Then `durable_source_path` MUST equal `canonical_target_path` as exact Unicode strings and UTF-8 bytes. Inequality returns `ERR_REUSE_SOURCE_TARGET_MISMATCH`.

This result replaces any older post-path use of `ERR_ROLE_DISPOSITION_INVALID`; it occurs after all global path faults and before family, run, or nullability checks.

### 9.2 Semantic-family reduction

The semantic domain is closed to `capture`, `analysis_compatibility`, and `analysis_strict`. Forward path expansions are respectively `capture`, `analysis/compatibility`, and `strict`; reverse mapping is unique.

Partition-specific schemas bind as follows:

- `table:capture_events` -> `capture`;
- `table:canonical_compatibility_analysis` -> `analysis_compatibility`;
- `table:strict_audit_analysis` -> `analysis_strict`.

Family-neutral schemas never choose or override family. Grammar-valid wrong-family input returns `ERR_SEMANTIC_FAMILY_BINDING_MISMATCH`, not a path result. Single-descriptor validation compares UnitContext, selected schema family when applicable, and parsed target family. Descriptor-set validation additionally requires parsed claim `audit_family` and every target family to equal UnitContext. The result occurs after path and reuse reductions and before run binding and nullability.

### 9.3 Run-ID reduction

Descriptor-set validation MUST require equality among parsed claim `run_id`, canonical-target decomposed `run_id`, and durable-source decomposed `run_id` for every descriptor, every role, and every publication mode. A grammar-valid cross-input mismatch returns `ERR_RUN_ID_BINDING_MISMATCH`, not `ERR_PATH_GRAMMAR_MISMATCH` or `ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH`.

Run binding occurs after family binding and before logical-hash nullability. For reuse mode, path equality is already established before run comparison. Repeated or contradictory descriptors are evaluated deterministically in ascending `object_ordinal`; any mismatch returns the public error with empty assurances.

## 10. Narrowed descriptor-set reducer

`_DescriptorSetInvariantInput` MUST have exactly `summaries` and `expected_fixed_role_counts`. The fixed-role map MUST exclude `PARTITION_PAYLOAD`.

The private code domain MUST contain only:

1. `PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID`;
2. `PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE`;
3. `PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID`;
4. `PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID`.

Every failure returns `summaries=None`; success returns complete ordinal-order summaries.

The following MUST be removed and made unreachable:

- `PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID` enum member;
- its branch and translation;
- `expected_role_counts` input field;
- private variable `PARTITION_PAYLOAD` count ownership;
- any test expecting private ordinal rejection;
- locally reconstructed sidecar role/path grammar authority.

Public wrapper order after descriptor global reductions is: logical-hash nullability delegates in ascending ordinal, public exact ordinal sequence `0..M-1`, variable `PARTITION_PAYLOAD == len(validated claim.partition_entries)`, private fixed-role cardinality, canonical-target uniqueness, sidecar relation, then same-ordinal partition binding. Old private results MUST NOT remain reachable by reflection, enum iteration, direct helper calls, or public translation.

## 11. Selected-payload predicate order

`validate_selected_json_payload` MUST evaluate the following exact predicate order:

1. unit-kind gate;
2. UnitContext validation;
3. accepted registry bytes validation;
4. selected sidecar canonical JSON parse;
5. selected descriptor exact-ordinal lookup;
6. selected sidecar closed-schema membership and types;
7. complete descriptor-set delegate with its exact internal order;
8. `_project_selected_binding_query`, then resolver delegate;
9. selected-schema implementation gate;
10. paired-target physical-proof presence;
11. paired-target descriptor selection and pairing;
12. selected expected size/SHA syntax;
13. selected observed size;
14. selected observed SHA-256;
15. paired expected size/SHA syntax;
16. paired observed size;
17. paired observed SHA-256;
18. final sidecar target-path/hash semantic relation;
19. success.

`_project_selected_binding_query` MUST copy exactly: unit kind; selected role, publication mode, content schema, canonical target; booleans computed from actual null identity; and the complete paired-target tuple only for a sidecar. Direct construction of the older `BindingQuery` inside the wrapper is prohibited.

The projection has one private success code and no failure result after its typed preconditions. `ERR_BINDING_QUERY_INVALID` remains in the direct resolver domain but is statically unreachable through the wrapper. The wrapper propagates reachable resolver lexical/grammar/reference/binding results unchanged. `STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A` remains wrapper-owned after successful resolution.

Selected physical predicates MUST precede paired physical predicates, and all physical predicates MUST precede the final semantic relation. The final semantic mismatch is `ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH`. Repeated code spelling does not collapse stage identity.

## 12. Unit-level wrapper delegation

`validate_prepared_unit_structure` MUST retain this high-level order:

1. unit-kind gate;
2. UnitContext validation;
3. structural-member set validation;
4. accepted registry bytes validation;
5. structural members through `validate_structural_json_member`, preserving its order;
6. complete descriptor-set delegate;
7. selected JSON object iteration through `validate_selected_json_payload`;
8. success.

Every descriptor-selected JSON member represented by an object descriptor with a `json:` content-schema ID and supplied payload bytes MUST use the selected wrapper. Table/parquet payloads are not converted into selected JSON inputs by this requirement.

Sidecar selected JSON members MUST be evaluated before non-sidecar selected JSON members so paired proof and wrapper-owned stops propagate before any direct member shortcut. Within each class, this candidate proposes ascending `object_ordinal` for deterministic order; Sentinel MUST confirm this tie-break against the accepted fixture ordering before implementation authorization.

For sidecars, wrapper input MUST carry the exact paired target descriptor and `paired_target_payload_bytes` from its pointed-to ordinal. Missing paired proof returns the wrapper result. Unit validation MUST return every wrapper non-success unchanged, with no remap, success substitution, or retained assurance.

The unit validator MUST NOT directly reconcile, schema-resolve, or emit implementation/reference stops for wrapper-eligible selected JSON members. Direct reconciliation is a forbidden bypass. `STOP_SCHEMA_REFERENCE_UNRESOLVED`, `STOP_CONTENT_SCHEMA_TARGET_BINDING_INVALID`, and `STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A` remain outcomes of the selected wrapper and propagate unchanged through unit and dispatch.

## 13. Recommended implementation sequence

### Alternative A — one atomic source-authoring stage (recommended)

A single bounded source stage changes all three mandatory source paths. It materializes canonical codes, registry typed parsing, and prepared-evidence consumers together. The deliverable is one exact three-file candidate plus a changed-path inventory. No partial stage is executable or test-authorized.

This is safest because each file supplies types or behavior required by the others. A one-file or two-file checkpoint could falsely appear improved while retaining incompatible result enums, duplicate parser ownership, or direct wrapper bypass.

### Alternative B — multiple source substages (not recommended)

A possible split would be canonical result inventory, registry parser/types, then prepared-evidence consumers. It is rejected because intermediate states expose imports or contracts that are missing on the other side, and no accepted typed stop exists that prevents all downstream use of the partially migrated surfaces. It also creates temporary dual parser ownership.

### Staged review after source authoring

1. Sentinel static source review of the exact three-file candidate; no execution.
2. Separately proposed and Gustavo-authorized test-source authoring for the four mandatory test paths.
3. Sentinel static test-contract review.
4. Separately proposed test execution, with exact commands and environment, only after its own authorization.

Acceptance of this package does not activate any stage.

## 14. Deliverables for any later authorized source stage

A later authorization package MUST require:

- exact selected starting commit and per-path starting SHA-256 values;
- clean/dirty/untracked state capture;
- exact three changed source files and no others;
- full-file outputs or patch plus post-authoring SHA-256 inventory;
- statement of no tests/imports/project execution/data/network/subprocess/Git writes unless separately authorized;
- static mapping from each requirement in this candidate to the exact changed symbol.

## 15. Acceptance criteria

Specification acceptance requires Sentinel to verify canonical alignment, completeness, determinism, closed paths, and non-authorization.

Later implementation conformance requires static inspection that every requirement is materialized and no prohibited shortcut remains. Passing tests alone are insufficient, because tests may encode Revision 09 or a partial contract.

Later test-source conformance requires exact contract coverage, negative and precedence cases, and no test that makes old private results reachable.

Test execution, project execution, data access, and network use remain separately authorized activities.

## 16. Stops and open decisions

Implementation MUST halt before edits if the authorized base, exact starting bytes, dirty state, mandatory files, or scope differs. It MUST halt on any conflict between this candidate and installed Revision 10 and return the conflict to Sentinel.

Open Sentinel decision:

- confirm the deterministic order among multiple wrapper-eligible sidecars and multiple non-sidecars; this candidate proposes sidecars first and ascending ordinal within each class;
- confirm the no-coercion interpretation of `UnitContext` where the accepted contract names field domains but does not separately restate subclass handling;
- approve or replace the internal checksum self-reference convention.

## 17. Authorization statement

This review candidate authorizes nothing. No implementation starting SHA is selected. The preserved checkpoint remains immutable evidence and MUST NOT be restored, promoted, copied over, or used as an active continuation start.

## 18. Requested Sentinel decision

Requested decision: `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.
