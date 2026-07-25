# Handoff Inventory

Revision 10 controlling status: `REV23_FINDING4_I0A_SCOPE_REVISION_10` is
accepted, canonically installed, and Sentinel-verified at
`3d6fbe5eda504c32d94fed72be99adb9485fe1b1`.

Checkpoint static-conformance status:
`BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED` at review base
`3cf0871ae97d112324031190822756379d1236e8`.

Implementation is not authorized.

## Controlling files

- `README_FIRST.md` — current handoff and read order.
- `IMPLEMENTATION_AUTHORIZATION_SCOPE.md` —
  `STOP_IMPLEMENTATION_NOT_AUTHORIZED`.
- `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md` —
  Revision 10 acceptance decision.
- `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_INSTALLATION_VERIFICATION_REVISION_10.md` —
  immutable installation-verification record.
- `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json` —
  installed Revision 10 identity and non-authorization state.
- `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_10/` — exact
  accepted 15-member scope package; unchanged by the static review record.
- `implementation_checkpoints/README_FIRST.md` — checkpoint system state.
- `implementation_checkpoints/CHECKPOINT_INDEX.json` — current checkpoint index.
- `implementation_checkpoints/LATEST_PRESERVED_CHECKPOINT.json` — current
  evidence-only pointer.
- `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md` —
  immutable static-conformance review record.
- `HANDOFF_REVISION_10_STATIC_CONFORMANCE_SHA256SUMS.txt` — focused checksum
  inventory for this review-record installation.

Historical checksum inventories remain immutable evidence of the states they
recorded. They are not regenerated or reinterpreted as inventories of this later
static-review installation.

## Historical accepted evidence

- `accepted_scope_revision_09/` and `accepted_scope_revision_08/` remain immutable.
- Their corresponding manifests, decisions, and authorization records remain
  audit evidence.
- Revision 09 R1 and Revision 08 implementation authorizations are historical
  and non-reusable under Revision 10.

## Preserved implementation evidence

- checkpoint: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- exact payload SHA-256:
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- payload size: `112338` bytes
- preservation state: `CANONICALLY_PRESERVED`
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`
- conformance state: `REVISION10_STATIC_CONFORMANCE_BLOCKED`

Resolved specification areas:

- T107 reachability;
- T153 reachability;
- Candidate 09 non-controlling status.

Verified failed contract areas:

- mandatory source-path coverage;
- four new public result codes;
- UnitContext validation;
- registry-owned path decomposition and typed bindings;
- descriptor pre-binding and global reductions;
- private reducer Revision 10 shape;
- selected-payload ordering and typed projection;
- unit-to-selected-wrapper propagation.

Open provenance gaps:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`;
- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

No checkpoint, accepted specification, or static review record authorizes
implementation, tests, execution, rollback, promotion, data/network activity,
Git writes by Claude, or a downstream stage.
