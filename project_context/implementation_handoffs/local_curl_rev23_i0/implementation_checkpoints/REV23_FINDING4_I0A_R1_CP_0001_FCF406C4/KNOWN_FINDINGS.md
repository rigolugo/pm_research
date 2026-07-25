# Known Findings

## Accepted identity findings

- The checkpoint payload is exactly preserved at SHA-256
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`.
- Payload size is `112338` bytes.
- The checkpoint is recoverable and contains useful historical Revision 09
  implementation progress.
- The checkpoint remains `NOT_ACCEPTED`, non-controlling, and authorization
  effect `NONE`.

## Resolved specification matters

- `T107_FIXTURE_REACHABILITY_CONTRADICTION` — resolved by installed Revision 10.
- `T153_FIXTURE_REACHABILITY_CONTRADICTION` — resolved by installed Revision 10.
- `CANDIDATE_09_NOT_ACCEPTED` — no longer an open specification blocker because
  Revision 10 is controlling.

## Verified Revision 10 conformance failures

1. `REVISION10_MANDATORY_SOURCE_PATHS_INCOMPLETE`
2. `REVISION10_PUBLIC_RESULT_CODES_NOT_MATERIALIZED`
3. `REVISION10_UNIT_CONTEXT_VALIDATION_MISSING`
4. `REVISION10_REGISTRY_PATH_DECOMPOSITION_AND_TYPED_BINDINGS_MISSING`
5. `REVISION10_DESCRIPTOR_PRE_BINDING_AND_GLOBAL_REDUCTIONS_MISSING`
6. `REVISION10_PRIVATE_REDUCER_SUPERSEDED_SHAPE_RETAINED`
7. `REVISION10_SELECTED_PAYLOAD_ORDER_AND_PROJECTION_NONCONFORMANT`
8. `REVISION10_UNIT_SELECTED_WRAPPER_PROPAGATION_MISSING`

Controlling result:

`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`

## Open provenance gaps

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`

The provenance gaps are not evidence that the checkpoint conforms or does not
conform beyond the observed static defects. They remain separately open.

## Authorization effect

None. No implementation start, rollback, restoration, overwrite, promotion,
source/test edit, tests, execution, data/network access, Git writes by Claude,
R2, P1/P2/P3, scoring, probe execution, or gate change is authorized.
