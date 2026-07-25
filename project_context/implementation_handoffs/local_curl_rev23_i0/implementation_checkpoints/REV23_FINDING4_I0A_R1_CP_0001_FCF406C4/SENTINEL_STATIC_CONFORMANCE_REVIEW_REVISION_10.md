# Sentinel Static-Conformance Review — Revision 10

Immutable review record for checkpoint
`REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`.

## Decision

`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`

The preserved checkpoint is recoverable and contains useful historical Revision 09
implementation progress, but it does not conform to the installed
`REV23_FINDING4_I0A_SCOPE_REVISION_10` contract.

## Review identity

- review date: `2026-07-24`
- Sentinel review base: `3cf0871ae97d112324031190822756379d1236e8`
- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- controlling scope installation commit:
  `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- checkpoint ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- preserved payload SHA-256:
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- preserved payload size: `112338` bytes
- checkpoint acceptance state: `NOT_ACCEPTED`
- checkpoint authorization effect: `NONE`
- controlling implementation: `false`
- implementation starting SHA selected: `false`

## Review boundary

This was a static documentation-and-source inspection only.

Not performed:

- tests, test collection, project imports, project execution, compilation, lint,
  typing, coverage, or CI;
- local research-data reads;
- vendor, API, RPC, Dune, curl, or project-network access;
- source or test edits;
- rollback, restoration, overwrite, promotion, or checkpoint synchronization;
- implementation authorization or selection of implementation starting bytes.

## Evidence classification

- `CANONICAL`: installed Revision 10 accepted package, installation-verification
  record, current canonical state documents, checkpoint index and manifest.
- `OBSERVED`: exact preserved `prepared_evidence.py` payload and its static content.
- `SUBMITTED`: multi-round activity narrative and current twelve-path worktree
  claims not independently captured in the checkpoint.
- `INFERRED`: downstream consequences that follow from the canonical mandatory
  path matrix and observed one-file checkpoint boundary.

## Resolved contract areas

The following are not blockers to this review:

1. The exact checkpoint payload is canonically preserved and recoverable at the
   recorded SHA-256 and size.
2. The payload contains material Revision 09 progress, including substantial
   descriptor, descriptor-set, selected-payload, structural-member, unit, and
   dispatch logic.
3. Revision 10 resolves the former T107 and T153 specification reachability
   contradictions.
4. Candidate 09 is not controlling; Revision 10 is the installed controlling
   specification.

These resolved areas do not establish Revision 10 implementation conformance.

## Failed Revision 10 contract areas

### 1. Mandatory source-path coverage is incomplete

Revision 10 marks all three of the following source paths as mandatory future
changes:

- `pm_research/local_curl_per_side/canonical.py`;
- `pm_research/local_curl_per_side/finding4_registry.py`;
- `pm_research/local_curl_per_side/prepared_evidence.py`.

The checkpoint preserves only `prepared_evidence.py`. It contains no candidate
Revision 10 bytes for `canonical.py` or `finding4_registry.py`.

### 2. Four required public result codes are not materialized

The checkpoint does not materialize:

- `ERR_UNIT_CONTEXT_INVALID`;
- `ERR_SEMANTIC_FAMILY_BINDING_MISMATCH`;
- `ERR_RUN_ID_BINDING_MISMATCH`;
- `ERR_REUSE_SOURCE_TARGET_MISMATCH`.

The checkpoint continues to map the affected failures to older result classes,
including `ERR_PATH_GRAMMAR_MISMATCH` and
`ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH`.

### 3. UnitContext validation is missing

The observed public surfaces gate `unit_context.unit_kind`, but do not implement
Revision 10's closed UnitContext validation and do not return
`ERR_UNIT_CONTEXT_INVALID` before later predicates.

### 4. Registry-owned path decomposition and typed bindings are missing

Revision 10 requires the sole registry-owned normalized-path decomposition and
its typed binding outputs. The checkpoint instead performs private string
splitting, suffix checks, direct frozen-table access, and locally reconstructed
source identity in `prepared_evidence.py`.

### 5. Descriptor pre-binding and global reductions are missing

The required typed descriptor pre-binding result, fault-evidence domain, global
path-class reduction, reuse reduction, semantic-family reduction, and run-binding
reduction helpers are not materialized. The checkpoint retains per-descriptor
validation and later ad hoc cross-input comparisons.

### 6. The private descriptor-set reducer remains superseded

The checkpoint retains:

- `PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID` in the private reducer
  domain; and
- `expected_role_counts` in `_DescriptorSetInvariantInput`.

Revision 10 removes private ordinal ownership and narrows the reducer to fixed
role cardinality, canonical-target uniqueness, sidecar relation, then valid.

### 7. Selected-payload predicate order and projection are nonconformant

`validate_selected_json_payload` performs registry/schema-selection work before
its descriptor-set delegate, performs physical and semantic checks in the old
order, and constructs the older `BindingQuery` directly. It does not implement
`_project_selected_binding_query` or Revision 10's ordered predicate sequence.

### 8. Unit validation bypasses the selected wrapper

`validate_prepared_unit_structure` directly reconciles object payloads and emits
schema-reference or implementation stops. It does not delegate selected JSON
members through `validate_selected_json_payload`, so Revision 10 sidecar-first
propagation and wrapper ordering are not established.

## Open provenance gaps

The following remain open and are not converted into implementation defects or
negative facts beyond their exact evidence state:

1. `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE` — the complete multi-round
   implementation activity lineage was not independently captured.
2. `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED` — the current exact
   twelve-path worktree was not independently captured in the checkpoint.

These provenance gaps are separate from the verified static-conformance block.
Resolving either gap cannot make the preserved one-file checkpoint conformant to
Revision 10 without new implementation bytes for the failed mandatory contract
areas.

## Self-attack

Strongest alternative verdict: treat the checkpoint as a useful partial-progress
artifact and issue `ACCEPT FINDING` rather than `BLOCK`.

Rejection of that alternative: the requested boundary is Revision 10 static
implementation conformance, not usefulness or recoverability. The canonical
impact matrix mandates three source changes, while the checkpoint preserves one,
and the observed payload retains superseded interfaces and result mappings.
Those are verified material defects. `BLOCK` is therefore the correct verdict.

## Authorization state

This record authorizes nothing.

Still unauthorized:

- implementation or implementation-source authoring;
- test-source authoring or test execution;
- rollback, restoration, overwrite, promotion, or continuation from checkpoint;
- project execution, data access, network access, subprocesses, or artifact runs;
- Git writes by Claude;
- R2, P1, P2, P3, scoring, probe execution, or gate changes.

No implementation starting SHA, source-gated commit, or writable implementation
path is selected by this review.

## Next action and owner

Gustavo may manually install this documentation-only canonical record package at
base `3cf0871ae97d112324031190822756379d1236e8` and return the resulting commit SHA
to Sentinel for installation verification.

No implementation remediation package or Claude implementation prompt follows
from this review.
