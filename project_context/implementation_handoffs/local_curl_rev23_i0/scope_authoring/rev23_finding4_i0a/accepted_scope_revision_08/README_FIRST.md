# README FIRST — REV23 Finding 4 I0A Scope Revision 08

Status: **PROFESSOR DRAFT FOR SENTINEL REVIEW — NOT APPROVED**

Canonical scope-review anchor:

`88362521fe9ef247708e4d7b5f90753784b8b88e`

Revision 08 retains the verified Revision 06 corrections and exact reconciled fixture bytes. It closes the overloaded-A4, private-helper assurance, result-payload, exact-return-value, registry-index, binding-result, physical-observation, export/import, and global assurance-map defects.

## Read order

1. `REV23_FINDING4_I0A_SCOPE_REVISION_08.md`
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

## Controlling corrections

- Persisted JSON object keys use recursive lexicographic Unicode code-point order. Schema field order governs membership and typed projections only.
- Every exact JSON fixture and dependent physical length/SHA-256 was regenerated.
- The one-partition snapshot fixture uses the exact seven-cell relation hash `bef068f484d8b9c230dae13031b96c4e4b7ae58a16fd08ff348f6f0d0299b58c`.
- `finding4_registry.py` is the sole path-grammar and placeholder owner; the import graph is acyclic.
- Accepted-registry parsing uses strict UTF-8, `json.loads`, duplicate-key rejection, float/constant rejection, and canonical byte-equality.
- Structural sidecars use `I0A_VALID_A3_STRUCTURAL_SIDECAR`; they never receive A4 or A6.
- Internal logical A4 and physically reconciled structural-object A3+A4 use distinct success codes.
- Every public success code has one exact global assurance tuple; every error/stop has `()`.
- Every value-producing case pins the complete returned payload, including exact bytes, digests, registry index, binding, observed size/SHA-256, and required nulls.
- Private binding-set and descriptor-set helpers return private outcomes only and cannot establish public I0A assurances.
- One complete eight-member `SNAPSHOT_PUBLICATION` fixture has exact cross-member hashes, plan-derived ID `prep_e0c141d97d078cfc958c0a8098e65fafbd79ab317325e0eb525cb5ccf308bec1`, 14 descriptors, 14 payload mappings, and pinned accepted-registry byte identity.
- T142 and T143 clear every prior check and stop at the first `STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A` boundary.
- All eight `StructuralMemberName` branches have direct result/assurance coverage.
- Unused and incomplete nominally accepted fixtures were removed.

This package contains specifications and static case descriptions only. It contains no implementation, executable project tests, source synchronization, project-code execution, local-data access, network/curl/subprocess activity, empirical artifacts, or Git writes.

## Revision 08 review focus

Verify the canonical compatibility/strict table identifiers, the two exact normal-final marker bindings to `json:finalization_marker_v23`, the schema-domain subset and identity-agreement invariants, and the two complete analysis-family SNAPSHOT_PUBLICATION fixtures.
