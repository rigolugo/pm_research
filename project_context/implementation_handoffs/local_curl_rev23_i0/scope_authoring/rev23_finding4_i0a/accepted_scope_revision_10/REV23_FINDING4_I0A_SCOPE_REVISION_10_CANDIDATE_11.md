# REV23 Finding 4 I0A Scope Revision 10 — Candidate 11


## Canonical checkpoint and implementation-start state

- checkpoint ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`;
- preserved payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`;
- preservation state: `CANONICALLY_PRESERVED`;
- conformance state: `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`;
- acceptance state: `NOT_ACCEPTED`;
- authorization effect: `NONE`;
- historical Revision 09 R1 authorized starting SHA-256: `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`;
- Revision 10 implementation starting point: `NOT_AUTHORIZED_AND_NOT_YET_SELECTED`.

The historical authorized start is not the current implementation starting point. The preserved checkpoint is evidence only and is not accepted, controlling, executable, promoted, or authorized. Candidate 11 creates no rollback, restore, overwrite, promotion, or continuation instruction.


## 1. Status

**Mode:** `AMEND`  
**Status:** `REVIEW CANDIDATE — SPEC ONLY — NOT ACCEPTED`  
**Draft and revision owner:** Professor  
**Specification review and decision owner:** Sentinel  
**Implementation and execution authorization owner:** Gustavo  
**Implementation owner after acceptance and authorization:** Claude

Professor does not approve this package.

**Checkable completion sentence:** Candidate 11 is complete when Sentinel can verify that primary specification Section 10 is identical to the dedicated twelve-path matrix, T228 binds all eight matrix representations and current package identities, and every unrelated Candidate 10 contract remains unchanged.

## 2. Canonical base

Repository: `rigolugo/pm_research`  
Canonical HEAD inspected: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`  
Accepted Revision 09 archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`  
Accepted public API SHA-256: `935289dbf48a004f334773895da80537b71f4e50b09a4ce7a2e77a01e0ef16cc`  
Accepted role matrix SHA-256: `d8c524dc95efba13b6ea81ac32396690cc665a3d3e3e57e1adcbda5206b3cd8a`  
Accepted static matrix SHA-256: `162661e09f7d19fcc7ba4b635f5f452b469c3ecfd1d6fc9d8d85a999885f5021`  
Twelve-path baseline SHA-256: `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`  
Historical Revision 09 R1 authorized starting SHA-256: `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

The Revision 09 R1 authorization is canonically installed and Sentinel-verified at
the current HEAD. It is separate from this specification task and does not authorize
Professor to edit any repository path.

## 3. Authority chain

- Revision 09 (`REV23_FINDING4_I0A_SCOPE_REVISION_09`) is the controlling accepted specification.
- Candidate 10, ZIP SHA-256 `d5aa07180aae9685b21499d50e944ba5962379c77aa9cd5661ba7bde3dfb8979`, is the direct non-authoritative drafting predecessor and review evidence only. Candidate 09 and earlier candidates are non-controlling historical evidence.
- Candidate 07 is earlier rejected drafting and review evidence.
- Candidates 01–06 are earlier rejected or non-authoritative review evidence.
- Candidate 11 is not controlling unless Sentinel accepts it and an accepted package is later canonically installed.
- Professor owns drafting and revision. Sentinel owns specification review and decision. Gustavo owns implementation and execution authorization. Claude may implement only accepted and separately authorized scope.

Every retained requirement is restated in Candidate 11 and justified against accepted Revision 09 plus Sentinel correction decisions. No unnamed rejected-candidate rule carries forward.

## 4. In scope

Candidate 11 changes only two Candidate 08 defects and their mechanical consequences:

1. replace the stale `caller_callee_closure_inventory_static_assertion` bytes under the same fixture ID so T228 proves Candidate 11's current case, fixture, call-edge, authority, future-path, and materialized-member identities; and
2. identify Candidate 10 as the direct non-authoritative drafting predecessor, with Candidate 09 and earlier candidates classified as non-controlling historical evidence.

No production interface, result domain, precedence, assurance mapping, call edge, stage order, case ID, fixture ID, path status, or authorization boundary is redesigned.

## 5. Preserved substantive contract

Candidate 11 preserves:

- the accepted physical helper signature
  `reconcile_physical_payload(expected_file_size_bytes: int, expected_file_sha256: str, payload_bytes: bytes) -> PhysicalPayloadResult`;
- selected-sidecar predicate order;
- selected physical → paired physical → final semantic relation precedence;
- `ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH` for final sidecar target-path/hash mismatch;
- T215 and T218;
- the exact four-field `SchemaBinding` key;
- exclusion of actual descriptor `logical_sha256` nullability from binding selection;
- resolver success at `I0A_BINDING_RESOLVED_A1`;
- wrapper ownership of `STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A`;
- typed impossibility of `ERR_BINDING_QUERY_INVALID` at the selected-wrapper boundary;
- propagation of `ERR_LOGICAL_SHA256_MISMATCH`,
  `ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED`, and
  `ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH`.

## 6. Current fixture namespace

The sole fixture lookup domain is:

```text
accepted Revision 09 fixture_catalog IDs
UNION
Candidate 11 current fixture_catalog_delta IDs
```

Prior-candidate fixture deltas are not lookup sources; Candidate 11 contains its own complete current delta.

Machine-readable reconciliation:

- accepted Revision 09 fixture count: `106`;
- Candidate 11 fixture-delta count: `63`;
- resolved union count: `169`;
- collision count: `0`;
- unresolved reference count: `0`;
- resolved-set SHA-256:
  `712766a925dd39e61f776bad76a6fb3c7862459cf6de65f74b63f88bfb2afe64`.

Every case and fixture-to-fixture reference resolves by exact top-level ID. Dotted,
indexed, pointer, path, or prior-candidate lookup is forbidden.

## 7. One case account

| Range | Status | Count |
|---|---|---:|
| T001–T165 | accepted Revision 09 | 165 |
| T166–T218 | preserved Candidate 05 material, restated in Candidate 11 | 53 |
| T219–T228 | preserved Candidate 06/07 material; T228 fixture bytes corrected in Candidate 11 | 10 |
| T229 | preserved Candidate 07 direct descriptor-set behavioral case | 1 |
| T230 | preserved Candidate 08 direct unit-validator behavioral case | 1 |
| **Total** |  | **230** |

No case is appended, removed, renumbered, or redefined. T228 retains its package-wide static-closure purpose and expected outcome but resolves to corrected current-package fixture bytes. T222 still references T230. T229 and T230 retain their accepted drafting-evidence partition.

## 8. Complete call-edge closure

`I0A_PUBLIC_API_CONTRACT_REVISION_10_CANDIDATE_11.json` contains `23` named edges. Every edge satisfies:

```text
callee reachable non-success domain
=
caller propagated results
+ caller translated results
+ statically proven unreachable results
```

The sets are pairwise disjoint. Every claimed unreachable result has an exact typed
invariant. An empty non-success domain remains inventoried for the success-only
`_project_selected_binding_query` edge.

The descriptor-set validator invokes `validate_prepared_object_descriptor` only
after global lexical, grammar, reuse, family, and run reductions pass. Therefore
the only reachable non-success from that delegated public call is
`ERR_LOGICAL_HASH_NULLABILITY_INVALID`; the callee cannot reverse global path-fault
precedence.

## 9. Typed seam and behavioral reachability

The private inspection-only seam remains `_inspect_delegated_non_success` and is owned by the existing retained path `tests/local_curl_per_side/test_prepared_evidence_i0a.py` (`tests.local_curl_per_side.test_prepared_evidence_i0a`). No thirteenth path is introduced.

Its exact precondition is: `full_behavioral_reachability_case_id resolves to a direct public behavioral case for the seam’s exact named callee and the same non-success result code. The behavioral case need not produce the result at the same internal delegated stage; originating-stage reachability is proven separately by the applicable lower-level behavioral case and call-edge seam case.`

- T229 directly proves descriptor-set-origin reachability.
- T221 separately proves descriptor-set-to-unit typed propagation.
- T230 directly proves exact-callee behavioral reachability at `validate_prepared_unit_structure`; its first failure is the earlier structural-member semantic-digest comparison, not descriptor-set delegation.
- T222 proves dispatch pass-through and sets `full_behavioral_reachability_case_id = T230`.
- T223–T227 and T215/T218 remain unchanged.

## 10. Twelve-path future-impact declaration

### Status and authority

Accepted Revision 09 controls. Candidate 10, ZIP SHA-256 `d5aa07180aae9685b21499d50e944ba5962379c77aa9cd5661ba7bde3dfb8979`, is the direct non-authoritative drafting predecessor. Candidate 09 and earlier candidates are non-controlling historical drafting or review evidence. Candidate 11 is not accepted and authorizes nothing.

Canonical repository HEAD inspected: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`.

### Current checkpoint state

- historical Revision 09 R1 authorized starting SHA-256: `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`;
- latest canonically preserved implementation evidence: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`;
- checkpoint ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`;
- preservation state: `CANONICALLY_PRESERVED`;
- conformance: `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`;
- acceptance: `NOT_ACCEPTED`;
- authorization effect: `NONE`;
- Revision 10 implementation starting point: `NOT_AUTHORIZED_AND_NOT_YET_SELECTED`.

Candidate 11 creates no rollback, restore, overwrite, promotion, or implementation-start instruction.

### Exact twelve-path future-impact matrix

| Path | Historical R1 baseline SHA-256 | Latest preserved checkpoint SHA-256 | Current status | Candidate 11 implementation starting SHA | Future change | Reason | Class | Requirement | Later authorization |
|---|---|---|---|---|---|---|---|---|---|
| `pm_research/local_curl_per_side/__init__.py` | `200019940bbd2c2b8dbac7d322722c7eae43926264c1438ec4a60cfc26e12c93` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No public symbol or re-export change is required; private helpers remain unexported. | `SOURCE` | `NOT_IMPLICATED` | no |
| `pm_research/local_curl_per_side/canonical.py` | `60f3141184753d294b8e708a77f381bdd40d04e39c6d1101f2cc14de9a9704b3` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Materialize four Revision 10 public result codes and their total empty-assurance mappings. | `SOURCE` | `MANDATORY` | yes |
| `pm_research/local_curl_per_side/claim_hashes.py` | `e9153abcbdb073a37d516056ff6fd657742c4d87620f557363855b3c6d728a3d` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No accepted hash projection or constructor algorithm changes. | `SOURCE` | `NOT_IMPLICATED` | no |
| `pm_research/local_curl_per_side/finding4_registry.py` | `06fd23245017fb538d06841d2b2b61f309f533959d16449ace588ccb6080e529` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Materialize semantic-family path mapping, sole path decomposition, exact four-field SchemaBinding key, and unchanged resolver domain. | `SOURCE` | `MANDATORY` | yes |
| `pm_research/local_curl_per_side/governing_package.py` | `75c9b5a19023d737d016bfd0e3e5b9b62ea7730355da7d555aa073192df79fec` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | Pinned governing-package bytes and validation behavior remain unchanged. | `SOURCE` | `NOT_IMPLICATED` | no |
| `pm_research/local_curl_per_side/prepared_evidence.py` | `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` | `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da` | `R1_CHECKPOINT_CANONICALLY_PRESERVED_NOT_ACCEPTED` | `UNSELECTED_PENDING_SENTINEL_DECISION_AND_GUSTAVO_AUTHORIZATION` | yes | Potential later materialization of UnitContext, global path reduction, reuse/family/run binding, descriptor-set propagation, selected-sidecar ordering, typed projection, and caller pass-through. This is planning evidence only. The preserved fcf406c4 checkpoint is not accepted or authorized, the historical 8b8e9320 start is not the current implementation starting point, and no restore or overwrite is directed. | `SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_canonical_i0a.py` | `9122ee3a0a4aa93f485a7dc35dbd7420e59b07eeed646007baff4ef5ac652bcd` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Conformance coverage for new public result-code and assurance inventories. | `TEST_SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | `4e2c8d6d663238c8bd7d3a4f40047bf0888b2ccf64cd5fcf37ce85cd2f158878` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No hash helper behavior changes. | `TEST_SOURCE` | `NOT_IMPLICATED` | no |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | `fe7a602684b4861db1cb825c0b70f712c9242ef61386d1a76f80ea8f4fed42f8` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Conformance coverage for family mapping, path decomposition, binding key, direct resolver domain, and typed impossibility boundary. | `TEST_SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | `c1b6a221a997e9c7d5aae0bf5c5bf98f38d0d1e8183bcabbebc8c7f1ac0550e4` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No governing-package behavior changes. | `TEST_SOURCE` | `NOT_IMPLICATED` | no |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | `c8e69789fc63eebff3d87f14ca6c94748872483e8fcffd541243ffa32e114679` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Contract closure, private types, precedence, authority chain, fixture namespace, case counts, and twelve-path consistency. | `TEST_SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `c9c5f9e09136f70902dc70e809d82177303319f431f532126b5aee8d04c2ae37` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Behavioral and seam coverage for T166–T230, including sidecar-first unit reachability and delegated failures. | `TEST_SOURCE` | `MANDATORY` | yes |

Canonical row-array SHA-256: `0f0dbcde71d358380280e519e4f6c95987a2b8493d31cb640a9ec27ac9df211b`.

The identical canonical row array and SHA-256 are required across all eight comparison members, including this primary specification Section 10 and T228's closure fixture. This matrix is planning evidence only. It does not authorize any edit, test, execution, rollback, restoration, overwrite, promotion, or implementation start.
## 11. Preservation and supersession

Candidate 11 preserves 62 of 63 Candidate 10 fixture records byte-for-byte. It replaces only `caller_callee_closure_inventory_static_assertion` under the same fixture ID and adds no fixture ID.

T001–T230 are preserved. T228 changes only mechanically dependent constructed-input and governing-requirement fields required to bind the corrected fixture. T222 still references T230. T107, T153, T177, T215, T218, T229, and T230 retain their intended identities, results, and precedence except for package-name references mechanically updated to Candidate 11.

Candidate 11 supersedes no accepted Revision 09 requirement unless Sentinel later accepts the named amendment and it is canonically installed.

## 12. Acceptance evidence

Sentinel MAY inspect:

- repository and accepted-base identities;
- JSON closed-field equality;
- fixture-set union and reference resolution;
- exact fixture lengths and SHA-256 values;
- case IDs, order, and totals;
- edge closure equations;
- typed unreachability invariants;
- full unit-fixture cross-member hashes;
- future-impact matrix hash equality;
- member paths and internal checksums.

Naming an acceptance method does not authorize implementation or execution.

## 13. Self-attack

Professor attempted to reject Candidate 11 using these hypotheses:

1. T228 still proves a Candidate 07 or Candidate 08 current identity;
2. the closure fixture still declares final case T229, total 229, fixture delta 62, or namespace size 168;
3. T228 can pass without resolving Candidate 11's current static-matrix and hash-contract member SHA-256 values;
4. Candidate 06 or Candidate 07 is still described as the direct predecessor;
5. an unrelated Candidate 08 interface, result domain, call edge, assurance map, case, fixture ID, or path status changed;
6. T222 no longer references T230;
7. a thirteenth path appears;
8. a stale predecessor hash is presented as current evidence;
9. Candidate 11 is represented as accepted or implementation-authorizing.

Result:

`NO_UNRESOLVED_CONTRADICTION_FOUND_BY_PROFESSOR_SELF_ATTACK`

This is not acceptance. Sentinel decides.

## 14. Authorization statement

This package authorizes no source or test edit, test execution, project import or
execution, compilation, lint, type checking, coverage, CI, research-data access,
network/vendor use, implementation artifact, baseline mutation, Git write, R1
source work, R2, downstream phase, scoring, probe, or gate change.

Current constraints remain: P1 blocked; P2/P3/scoring/probe unauthorized;
`named_binary_probe_blocked = true`.

## 15. Requested Sentinel decision

Requested decision: `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.

READY_FOR_SENTINEL_SPEC_REVIEW

## Candidate 11 required self-attack result

Professor statically checked:

1. T107 is not intercepted by path grammar or semantic-family validation.
2. T153 is not intercepted by role or path grammar before duplicate detection.
3. No public function both includes and excludes the same result.
4. `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` is historical authorization provenance only, not a current Revision 10 implementation start.
5. `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da` is preserved unaccepted evidence and Candidate 11 creates no rollback path to the historical start.
6. The future-impact inventory remains exactly twelve paths.
7. Revision 09 alone remains controlling.

No unresolved contradiction was found in this bounded self-attack. This is Professor self-review, not Sentinel acceptance.

READY_FOR_SENTINEL_SPEC_REVIEW
