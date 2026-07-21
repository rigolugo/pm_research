# REV23 Finding 4 I0A Scope Revision 09

## 1. Status and authority

This is a Professor-authored specification revision for Sentinel review. It is not accepted, active, implementation-authorizing, or execution-authorizing.

Canonical scope-review anchor:

`88362521fe9ef247708e4d7b5f90753784b8b88e`

Accepted base identity:

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_08`;
- accepted-scope commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`;
- source-gated implementation HEAD: `1e963bb6e8387aff071d697a416fa558956e571e`;
- accepted Revision 08 archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`.

This is a narrow **SPEC-ONLY amendment candidate**. It neither implements the correction nor authorizes any downstream stage.

Governing accepted hashes remain unchanged:

| Governing member | SHA-256 |
|---|---|
| specification | `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76` |
| schema registry | `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689` |
| request/authorization contract | `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0` |
| governing manifest | `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38` |
| governing semantic hash | `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f` |
| accepted checksum inventory | `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9` |

The private canonical repository is authoritative. Prior scope revisions, chat text, mirrors, and local copies are non-governing.

## 2. Objective and non-objectives

I0A is a narrowly proposed pure deterministic contract-validation surface for caller-supplied typed values and exact caller-supplied bytes. It defines no filesystem adapter, runtime publication, empirical collection, replay, request execution, source synchronization, or project-code execution.

I0A does not authorize implementation, source or test-source authoring, tests, Python/project imports, local reads, artifact recovery, deterministic regeneration, network/curl/subprocess activity, empirical artifacts, Git writes, P1/P2/P3, scoring, probe execution, trading, or gate changes.

A5, A7, and A8 remain unreachable.

## 3. Controlling machine-readable contracts

The controlling package members are:

1. `I0A_PUBLIC_API_CONTRACT.json` — exact modules, public/private symbols, signatures, import graph, result domains, ordered precedence, and assurance tuples.
2. `I0A_ROLE_CONTENT_SCHEMA_DISPOSITION_MATRIX.json` — all 30 prepared-object roles, exact target grammars, nine prepared-unit grammars, placeholder domains, cardinality, schema disposition, and sidecar relationships.
3. `I0A_HASH_PROJECTION_CONTRACT.json` — exact typed-cell, typed-row, relation, digest, JSON persistence, nullability, and ordering contracts.
4. `I0A_STATIC_TEST_CASE_MATRIX.json` — complete immutable fixture catalog and 165 static cases.
5. `I0A_VALIDATION_ASSURANCE_LEVELS.md` — closed assurance semantics.
6. `I0A_STOP_AND_RESULT_DOMAIN.md` — total authoring-stop mapping and closed pure result domain.

No caller-supplied role table, schema-membership table, path grammar, placeholder domain, partition count, success label, or assurance assertion is authoritative.

## 4. Accepted canonical JSON rule

Every persisted JSON object uses the accepted Revision 23 canonical JSON contract:

- strict UTF-8 and no BOM;
- every closed-schema member present, including nullable members;
- object keys recursively serialized in lexicographic Unicode code-point order;
- compact separators `,` and `:`;
- `ensure_ascii=false`;
- integers represented as JSON integers, never floats or numeric strings;
- NFC strings where the scalar type is `STRING`;
- no leading or trailing whitespace and no final LF.

Schema field order governs only closed membership and an explicitly declared typed projection. It never governs persisted JSON key order. Arrays retain their registered ordering.

Revision 09 retains, byte-for-byte, all exact JSON fixtures regenerated under the accepted Revision 08 rule, including claim scope, snapshot claim semantic, preparation plan, prepared unit, every structural sidecar, and all deterministic JSON mutations. Their exact UTF-8, hex bytes, byte lengths, and complete-file SHA-256 values are materialized in `fixture_catalog`.

## 5. Strict accepted-registry parsing

Accepted-registry index materialization first verifies the pinned registry SHA-256 `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`. It then:

1. imports Python standard-library `json`;
2. decodes strict UTF-8;
3. calls `json.loads` with `object_pairs_hook=_reject_duplicate_json_object_pairs`;
4. rejects duplicate object keys through private `_DuplicateJsonKeyError`;
5. rejects floats through `_reject_json_non_integer_number`;
6. rejects non-standard constants through `_reject_json_constant`;
7. requires a top-level JSON object;
8. canonical-reserializes recursively with lexicographic Unicode code-point key order, compact separators, `ensure_ascii=false`, and no final LF;
9. requires byte equality with the supplied pinned bytes; and
10. indexes the complete direct `json_schemas` and `table_schemas` definition domains.

An internal `i0a:` structural relation is never an accepted-registry member.

## 6. Closed assurance and result model

Every result carries exactly:

`established_assurances: tuple[AssuranceLevel, ...]`

Every declared result code has one exact tuple. Every non-success result uses `()`. A failed function retains no unstated partial assurance.

Revision 09 retains the accepted narrow assurance:

`A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED`

It means one fixed structural sidecar's exact bytes were reconciled, its paired target's independently supplied exact bytes were reconciled, and the sidecar values equal the independently derived paired structural path and observed paired-target complete-file SHA-256. It does not establish decoded logical rows, A4, A6, descriptor-set completeness, selected-schema completeness, filesystem facts, A7, or A8.

Its sole success code is:

`I0A_VALID_A3_STRUCTURAL_SIDECAR`

with exact tuple:

`(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)`

No undeclared result label is permitted.

Revision 09 retains the accepted split of the former overloaded A4 success into two exact results:

- `I0A_VALID_A4_INTERNAL_RELATION` establishes only `(A4_DECODED_LOGICAL_ROWS_VALIDATED,)`;
- `I0A_VALID_A3_A4_STRUCTURAL_OBJECT` establishes `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A4_DECODED_LOGICAL_ROWS_VALIDATED)`.

The global success-code map in `I0A_PUBLIC_API_CONTRACT.json` is the sole authority. A public success code cannot carry a function-local alternate tuple. Private descriptor-set and binding-set helpers return private outcome types and establish no public assurance.

Every result dataclass has a closed payload contract. Success requires all declared value fields non-null and exact. Errors/stops require the declared value fields null, except physical size/hash mismatches retain both actual observed size and actual observed SHA-256. Invalid physical expectations terminate before observation and return both observed fields null. No stale or partial value may survive a non-success result.

## 6A. Pinned value-producing outputs

The complete exact payloads are machine-readable in `I0A_STATIC_TEST_CASE_MATRIX.json`. The controlling pinned values include:

| Surface | Exact successful value |
|---|---|
| `canonical_typed_cell_bytes` | UTF-8 `{"n":"run_id","t":"STRING","v":"run_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}`; length 102; SHA-256 `e9fadff218898df01f6dea531208be81d77bf32690e533c80559588505897170` |
| `canonical_typed_row_bytes` claim-scope fixture | length 556; SHA-256 `0348081d83a0330b39a368bb6c8e199251600318c9d8394e48e7ce6186f2cb58`; exact UTF-8 and hex are pinned in the fixture catalog |
| empty relation digest | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| claim-scope digest | `0348081d83a0330b39a368bb6c8e199251600318c9d8394e48e7ce6186f2cb58` |
| acquisition-race-scope digest | `14a998bd9680a50b5c3919ab3476f85117613ec58d82358c1c0b68417cb7e0c8` |
| snapshot-claim-semantic digest | `851f6d56df534e6da9b98e2006bf1b77fbd570079ac90be772b8051b7cd3f23e` |
| successful registry index | 118 `json:` IDs, 29 `table:` IDs, 147 total; registry SHA-256 `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`; ordered-ID logical SHA-256 `5b1cebf772c53a187c6c48a5e6942d2d70bd7515773e8432286ab26043ac06eb`; the exact ordered 147-ID tuple is pinned in T005 |
| successful public binding | `BINDING_PUBLICATION_MARKER_SNAPSHOT_PUBLICATION_ATOMIC_BUNDLE_MEMBER_00`, role `PUBLICATION_MARKER`, unit `SNAPSHOT_PUBLICATION`, mode `ATOMIC_BUNDLE_MEMBER`, grammar `TARGET_PUBLICATION_MARKER_00`, schema `json:snapshot_publication_commit_v23`, non-null logical hash, exactly one marker sidecar |
| physical `abc` reconciliation | observed size 3 and observed SHA-256 `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |

Every value-producing static case compares the complete returned dataclass payload, not only code and assurance.

## 6B. Narrow private descriptor-set invariant correction

### 6B.1 Accepted contradiction

The accepted Revision 08 private reducer advertised two outcomes that its closed interface could not decide. `_DescriptorSetInvariantInput` contains only `summaries` and `expected_role_counts`; `_DescriptorSetInvariantSummary` contains only ordinal, role, canonical target path, sidecar flag, and paired ordinal. Neither type contains descriptor logical-hash values nor snapshot partition-entry/binding values.

Revision 09 preserves both closed dataclass field sets exactly and narrows the reducer rather than widening its input.

### 6B.2 Exact private code domain and precedence

`_PrivateDescriptorSetInvariantCode` is exactly:

```text
PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID
PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID
PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID
PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE
PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID
```

`_validate_descriptor_set_invariants.ordered_outcomes` is exactly:

1. `PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID`;
2. `PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID`;
3. `PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE`;
4. `PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID`;
5. `PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID`.

The helper MUST NOT inspect, infer, synthesize, or report logical-hash-nullability or partition-entry-binding outcomes. Its success payload remains the complete ordinal-order summary tuple. Every private failure returns `summaries=null`; no partial summaries survive.

### 6B.3 Explicit validation ownership

`validate_prepared_object_descriptor` owns role-specific `logical_sha256` nullability because it receives the complete descriptor. Its existing public result remains `ERR_LOGICAL_HASH_NULLABILITY_INVALID`, with unchanged precedence and `established_assurances=()`.

`validate_prepared_descriptor_set` owns same-ordinal `PARTITION_PAYLOAD` binding because it receives exact validated snapshot-claim semantic bytes plus the full descriptor set. It compares canonical target path, partition identity, and logical hash before invoking the private reducer. Its existing public mismatch result remains `ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH`, with unchanged precedence and `established_assurances=()`.

### 6B.4 Preserved public contract

Revision 09 changes no public function name, signature, result code, assurance tuple, return-payload shape, ordered public error precedence, fixture byte, fixture physical SHA-256, logical hash, role row, grammar, binding, or candidate repository path. The public behavior was already expressible; only the impossible private advertisement is removed and ownership is made explicit.

### 6B.5 Existing static cases affected

The existing case set remains T001–T165. Directly affected traceability or enum/payload fixtures are: `T041`, `T042`, `T043`, `T044`, `T045`, `T107`, `T108`, `T109`, `T146`, `T149`, `T152`, `T153`. `T009`, `T068`, `T070` traverse the retained private success/cardinality path and were revalidated without changing their case contents or expectations. Every other existing case is unaffected.

## 7. Snapshot claim and partition-entry cardinality

There is no independent `snapshot_partition_count` authority.

For `SNAPSHOT_PUBLICATION`, `PARTITION_PAYLOAD` cardinality is derived only from exact validated `snapshot_claim.partition_entries`. Revision 09 retains the exact seven-cell typed partition-entry row from accepted Revision 08:

1. `partition_ordinal: UINT`
2. `partition_id: STRING`
3. `partition_path: STRING`
4. `partition_logical_sha256: SHA256`
5. `row_count: UINT`
6. `first_key_canonical_json: STRING`
7. `last_key_canonical_json: STRING`

For the canonical one-partition fixture:

- partition-entry relation SHA-256: `bef068f484d8b9c230dae13031b96c4e4b7ae58a16fd08ff348f6f0d0299b58c`;
- snapshot-claim complete-file SHA-256: `954e5780c67ac9dd5cb099d6174659f68a9e2cd2a2c1649676b85d1618e1df0e`;
- snapshot-claim semantic SHA-256: `851f6d56df534e6da9b98e2006bf1b77fbd570079ac90be772b8051b7cd3f23e`.

For each validated claim entry at ordinal `k`, the same-ordinal `PARTITION_PAYLOAD` descriptor must equal the claim entry's exact canonical target path, partition identity, and logical hash. Path, identity, and logical-hash mismatch counterexamples are independent.

## 8. Frozen path grammar ownership and imports

`finding4_registry.py` solely owns:

- `FrozenPathGrammarId`;
- all frozen prepared-unit and target grammar tables;
- every placeholder-domain table;
- `validate_normalized_relative_path`;
- accepted-registry schema-definition indexing; and
- accepted-registry binding resolution.

`canonical.py` owns foundational enums, dataclasses, and typed-cell/typed-row constructors only. It does not own or import grammar tables.

The import graph is acyclic:

```text
canonical.py
  ↑ governing_package.py
  ↑ finding4_registry.py
  ↑ claim_hashes.py
canonical.py + finding4_registry.py + claim_hashes.py
  ↑ prepared_evidence.py
all five modules
  ↑ __init__.py re-exports
```

There is no reverse import, duplicated grammar table, runtime registration, or caller-defined grammar.

## 9. Exact prepared-unit grammars

All nine prepared-unit grammars are immutable and non-caller-constructible:

| Grammar ID | Exact template |
|---|---|
| `PREPARED_CLAIM_SCOPE_JSON` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SCOPE.json` |
| `PREPARED_CLAIM_SCOPE_SHA256` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SCOPE.sha256` |
| `PREPARED_CLAIM_SEMANTIC_JSON` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SEMANTIC.json` |
| `PREPARED_CLAIM_SEMANTIC_SHA256` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/CLAIM_SEMANTIC.sha256` |
| `PREPARED_PREPARATION_PLAN_JSON` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARATION_PLAN.json` |
| `PREPARED_PREPARATION_PLAN_SHA256` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARATION_PLAN.sha256` |
| `PREPARED_PREPARED_UNIT_JSON` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARED_UNIT.json` |
| `PREPARED_PREPARED_UNIT_SHA256` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/PREPARED_UNIT.sha256` |
| `PREPARED_OBJECT_BIN` | `artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/objects/<object_ordinal_10d>.bin` |

Placeholder domains are exact:

- `run_id`: `^run_[0-9a-f]{64}$`;
- `prepared_unit_id`: `^prep_[0-9a-f]{64}$`;
- `unit_kind`: exact 11-value `PreparedUnitKind`;
- `object_ordinal_10d`: exactly ten ASCII decimal digits, parsed as UINT32 and rendered identically;
- target-specific placeholders: the exact closed domains materialized in the role matrix.

Canonical snapshot publication-marker paths contain only `PUBLICATION_COMMITTED.json` and `PUBLICATION_COMMITTED.sha256`.

## 10. Structural-member validation

`StructuralJsonMemberInput` carries independently supplied and validated:

- `UnitContext`;
- exact `run_id`;
- exact `prepared_unit_id`;
- exact `StructuralMemberName`;
- exact member bytes, expected length, and expected complete-file SHA-256;
- for sidecars, paired target bytes, expected paired-target length, and expected paired-target complete-file SHA-256.

The structural path is derived from independent identity and the frozen grammar. A sidecar's stored `target_path` is checked but never trusted as path authority.

Exact success mapping:

| Structural member | Success result | Exact established assurances |
|---|---|---|
| `CLAIM_SCOPE.json` | `I0A_VALID_A6_STRUCTURAL` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A6_STRUCTURAL_SCHEMA_COMPLETE)` |
| `CLAIM_SCOPE.sha256` | `I0A_VALID_A3_STRUCTURAL_SIDECAR` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)` |
| `CLAIM_SEMANTIC.json` | `I0A_VALID_A6_STRUCTURAL` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A6_STRUCTURAL_SCHEMA_COMPLETE)` for the fully recomputable snapshot branch |
| `CLAIM_SEMANTIC.sha256` | `I0A_VALID_A3_STRUCTURAL_SIDECAR` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)` |
| `PREPARATION_PLAN.json` | `I0A_VALID_A3_A4_STRUCTURAL_OBJECT` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A4_DECODED_LOGICAL_ROWS_VALIDATED)` |
| `PREPARATION_PLAN.sha256` | `I0A_VALID_A3_STRUCTURAL_SIDECAR` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)` |
| `PREPARED_UNIT.json` | `I0A_VALID_A3_A4_STRUCTURAL_OBJECT` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A4_DECODED_LOGICAL_ROWS_VALIDATED)` |
| `PREPARED_UNIT.sha256` | `I0A_VALID_A3_STRUCTURAL_SIDECAR` | `(A3_EXACT_LENGTH_AND_SHA256_RECONCILED, A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED)` |

Missing paired-target evidence on an otherwise valid structural sidecar returns `ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED`; T094 proves this precedence.

## 11. Complete canonical snapshot fixture

`complete_snapshot_publication_unit` is one complete immutable fixture with:

- `unit_kind = SNAPSHOT_PUBLICATION`;
- eight exact structural members and no extra member;
- all four exact canonical structural JSON objects;
- all four exact canonical structural sidecars;
- exact cross-member complete-file and semantic hashes;
- preparation-plan file SHA-256 `e0c141d97d078cfc958c0a8098e65fafbd79ab317325e0eb525cb5ccf308bec1`;
- plan-derived `prepared_unit_id = prep_e0c141d97d078cfc958c0a8098e65fafbd79ab317325e0eb525cb5ccf308bec1`;
- prepared-unit file SHA-256 `81f8ab435de30a86eccfa118d7b43824218ca7c39957338e339285d26858598f`;
- exact 14-object descriptor set in canonical ordinal order;
- exact object payload bytes by ordinal;
- exact claim-bound one-partition descriptor;
- exact accepted-registry byte identity pinned by anchor, path, and `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`.

The fixture clears structural membership, canonical JSON, cross-member, predecessor, coverage, prepared-unit-ID, descriptor-set, binding, sidecar, and physical checks. `validate_prepared_unit_structure` and `dispatch_i0a_unit_validation` then terminate at the exact first unimplemented selected-schema boundary:

`STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A`

for ordinal 0 schema `table:capture_events`.

T142 and T143 prove those two direct boundaries.

## 12. Descriptor-selected sidecar validation

The only descriptor-selected A6 schema implemented in I0A is `json:sha256_sidecar`. Success requires:

1. accepted `SNAPSHOT_PUBLICATION` unit kind;
2. complete A2 descriptor set;
3. complete accepted-registry membership and exactly one frozen binding;
4. selected sidecar exact length/hash reconciliation;
5. paired target descriptor identity;
6. paired target independently supplied exact bytes, length, and complete-file SHA-256; and
7. canonical sidecar fields equal to the paired descriptor target path and independently observed paired-target digest.

This branch returns `I0A_VALID_A6_SELECTED`. Structural sidecars use the narrower result in §10 and never receive A4 or A6.

## 13. Deterministic error precedence

Every public and private function materializes an ordered error/stop sequence. Multi-fault inputs return the first satisfied predicate. Repeated row, cell, descriptor, or object faults choose the lowest canonical ordinal.

Every surface that accepts `unit_kind` or `UnitContext` evaluates first:

`unit_kind != SNAPSHOT_PUBLICATION → STOP_UNIT_KIND_NOT_ACCEPTED_I0A`

Typed-row precedence is:

1. arity;
2. field name/order at the first differing ordinal;
3. tag;
4. runtime value type;
5. NFC, range, SHA-256, or bytes-format rule.

Swapping equal-tag cells is a field-order failure, not a tag failure.

## 14. Static fixture and test closure

The matrix contains 165 ordered static cases.

- Every public function has direct coverage.
- Every declared result/error code has direct coverage.
- Every `StructuralMemberName` branch has direct success coverage.
- All four structural JSON members have exact physical mutation cases.
- All four structural sidecars have missing-paired-proof cases.
- T094 expects `ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED`.
- T142 and T143 prove the complete-unit unimplemented-schema boundary.
- Every fixture reference resolves to one immutable fixture.
- Every mutation identifies a complete base fixture and an exact deterministic operation.
- No prose-only positive or negative fixture remains.
- Unused or nominally accepted incomplete fixtures are absent.

The matrix is specification-only. It contains no executable project test source.

## 15. Artifact producer-consumer matrix

| Artifact | Producer | Intended consumer | Status |
|---|---|---|---|
| Revision 09 scope-review ZIP | Professor | Sentinel | draft for review only |
| detached ZIP SHA-256 | Professor | Sentinel | integrity verification only |
| API, role, hash, and static-test contracts | Professor | Sentinel; later authorized implementer only after acceptance and separate authorization | draft |
| assurance and stop/result documents | Professor | Sentinel | draft |
| inactive Claude handoff | Professor | Sentinel | explicit non-authorization |
| implementation ZIP | none | none | not authorized and not produced |
| runtime or empirical artifacts | none | none | prohibited |

## 16. Requirements traceability matrix

| Requirement | Section | Schema/invariant | Stop or decision rule | Static cases |
|---|---|---|---|---|
| private descriptor-set decidability | §6B | unchanged private input/summary; five-code private domain | four private failures then valid | T041–T045, T107–T109, T146, T149, T152–T153 |
| canonical JSON key order | §4 | canonical persistence rule; exact byte fixtures | `ERR_CANONICAL_JSON_INVALID` | T126–T141 plus exact fixture audit |
| duplicate-key rejection | §5 | strict registry parser and private duplicate-key hook | `ERR_CANONICAL_JSON_INVALID` | registry parser cases |
| exact partition-entry digest | §7 | seven-cell row and `bef068f484d8b9c230dae13031b96c4e4b7ae58a16fd08ff348f6f0d0299b58c` | logical/hash mismatch | one-partition fixture; T107–T109 |
| sole grammar ownership | §8 | module ownership/import graph | package static-validation failure | T001, T115–T123 |
| all nine prepared paths | §9 | `prepared_unit_path_grammars` | lexical/grammar errors | T115–T123 |
| structural member result split | §10 | exact success-by-member table | exact result and assurance tuple | T126–T133 |
| missing sidecar target proof | §10 | independent paired-target fields | `ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED` | T094, T138–T141 |
| complete snapshot unit | §11 | eight members, hashes, ID, 14 descriptors/payloads | first unimplemented schema stop | T142–T143 |
| selected sidecar dual A3 | §12 | complete descriptor and paired-byte proof | proof/mismatch/physical errors | T012, T052–T053, T072 |
| unit-kind first | §13 | per-function ordered precedence | `STOP_UNIT_KIND_NOT_ACCEPTED_I0A` | all unit-kind direct cases |
| total result/fixture coverage | §14 | coverage maps and closed enums | static package failure | all 165 cases |

## 17. Unresolved questions

None within this proposed scope. A need for another repository path, dependency, parser, schema implementation, filesystem adapter, grammar authority, or changed canonical interface is a typed scope-expansion halt and cannot be inferred into I0A.

## 18. Sentinel handoff and authorization boundary

**Status:** amendment candidate / materialized review candidate.

**Purpose:** correct the accepted Revision 08 private descriptor-set invariant interface without widening it.

**Canonical base:** `rigolugo/pm_research`; accepted-scope commit `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`; source-gated implementation HEAD `1e963bb6e8387aff071d697a416fa558956e571e`; accepted Revision 08 archive `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`.

**In scope:** the exact private enum/outcome narrowing, explicit public ownership, affected static-contract traceability, complete package materialization, and integrity validation.

**Out of scope:** implementation, implementation/test repository edits, test execution, project imports, research data, empirical artifacts, network/vendor activity, Git writes, and downstream authorization.

**Assumptions and open decisions:** none in the correction text. Sentinel owns acceptance and the downstream effect on any implementation conformance claim based on Revision 08.

**Acceptance evidence:** static inspection must prove the unchanged private dataclass fields, exact five-code private domain, exact five ordered outcomes, absence of the two impossible outcomes from machine-readable contracts, unchanged public signatures/results/assurances/precedence, unchanged exact data fixtures/hashes, unchanged 30-role and twelve-path matrices, complete T001–T165 construction, and valid internal/detached checksums.

**Authorization statement:** this package is SPEC ONLY. It does not implement the amendment, activate or modify an implementation handoff, authorize tests or execution, or change any research gate.

**Requested Sentinel decision:** `APPROVE` the narrow Revision 09 amendment candidate, or `BLOCK` with a specific remaining contract contradiction.

## Revision 09 schema-identity closure

The selected-content schema domain is now closed by exact string identity against the complete accepted registry index. The only partition payload table IDs are `table:capture_events`, `table:canonical_compatibility_analysis`, and `table:strict_audit_analysis`. No legacy shorthand table identifier is permitted.

Both normal-final marker targets—`REPLAY_FINALIZED.json` and `STOP_FINALIZED.json`—bind exactly `json:finalization_marker_v23`, as read from the accepted `PATH_GRAMMAR_REGISTRY.json`; neither branch is inferred from a similar filename. `NORMAL_FINALIZATION` remains outside the narrowed I0A execution domain and therefore still yields `STOP_UNIT_KIND_NOT_ACCEPTED_I0A` on public execution surfaces.

The role matrix materializes a complete immutable frozen-production binding table. Static acceptance requires (1) the role-matrix selected-schema union to be a subset of the exact accepted registry schema-ID tuple and (2) exact equality between the role-matrix schema union and frozen-binding schema union.
