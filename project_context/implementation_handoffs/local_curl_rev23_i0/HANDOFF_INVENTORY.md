# Handoff Inventory

Revision 10 controlling status: `REV23_FINDING4_I0A_SCOPE_REVISION_10` is accepted, canonically installed, and Sentinel-verified at `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`.

Checkpoint static-conformance status: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED` at review base `3cf0871ae97d112324031190822756379d1236e8`.

Accepted remediation scope: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`, installed and Sentinel-verified at `ee4a639f9a9429e642391f1fb1e0ab356a6f965a`.

Conditional package `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01` is installed and Sentinel-verified at `71061065d91fc391e934d7e79a29eefc898cfe82`, but it is not active. Its canonical-worktree source gate failed before edits.

Accepted provenance finding:

`ACCEPT FINDING — CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_ACCEPTED`

Source archive SHA-256: `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`. Canonical installation is Sentinel-verified at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`.

Accepted starting-state amendment:

`APPROVE — REV10_STARTING_STATE_AMENDMENT_CANDIDATE_04_ACCEPTED`

Candidate `REV23_FINDING4_I0A_REVISION_10_STARTING_STATE_AMENDMENT_CANDIDATE_04`, ZIP SHA-256 `9b6e05ff09e916b02b990556ee1ef6a37e3bc044a83c317ecfcc60fa65a63193`, is canonically installed and Sentinel-verified at `689e546e588d557c96f28bc722c3f159d635f2c1`. Authorization effect remains `NONE`.

Accepted Candidate 04 workspace-preparation package:

`APPROVE — CANDIDATE_04_WORKSPACE_PREPARATION_PACKAGE_CANDIDATE_02_ACCEPTED`

Package `REV23_FINDING4_I0A_CANDIDATE04_WORKSPACE_PREPARATION_PACKAGE_CANDIDATE_02`, ZIP SHA-256 `77c70fec832b97f2d2b78c9fb7886f1fe8f3b1aa03739a73a6213684d8c89601`, is installed by this documentation package with Sentinel installation verification pending. Workspace execution authorization remains `NONE`.

## Controlling files

- `README_FIRST.md` — current handoff and read order.
- `IMPLEMENTATION_AUTHORIZATION_SCOPE.md` — current inactive authorization and failed-gate state.
- `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md` — Revision 10 acceptance decision.
- `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_INSTALLATION_VERIFICATION_REVISION_10.md` — immutable installation-verification record.
- `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json` — installed Revision 10 identity and non-authorization state.
- `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_10/` — exact accepted 15-member scope package.
- `implementation_checkpoints/README_FIRST.md` — checkpoint system state.
- `implementation_checkpoints/CHECKPOINT_INDEX.json` — current checkpoint index.
- `implementation_checkpoints/LATEST_PRESERVED_CHECKPOINT.json` — current evidence-only pointer.
- `implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_STATIC_CONFORMANCE_REVIEW_REVISION_10.md` — immutable static-conformance review record.
- `HANDOFF_REVISION_10_STATIC_CONFORMANCE_SHA256SUMS.txt` — focused static-review inventory.
- `remediation_scope/README_FIRST.md` — accepted remediation-scope read order.
- `remediation_scope/SENTINEL_ACCEPTANCE_DECISION.md` — Sentinel remediation-scope acceptance.
- `remediation_scope/SENTINEL_INSTALLATION_VERIFICATION.md` — verified canonical installation at `ee4a639f...`.
- `remediation_scope/ACCEPTED_REMEDIATION_SCOPE_MANIFEST.json` — installed identity and non-authorization state.
- `remediation_scope/accepted_remediation_scope_candidate_01/` — exact accepted 11-member candidate package.
- `HANDOFF_REVISION_10_REMEDIATION_SCOPE_SHA256SUMS.txt` — focused remediation-scope inventory.
- `authorization_audit/rev23_finding4_i0a_revision10_remediation_source_01/` — installed but inactive three-source authorization package with a failed source gate.
- `HANDOFF_REVISION_10_REMEDIATION_SOURCE_AUTHORIZATION_SHA256SUMS.txt` — focused authorization inventory.
- `provenance_audit/rev23_finding4_i0a_current_twelve_path_worktree_capture_01/` — accepted and Sentinel-verified worktree-capture evidence.
- `provenance_audit/rev23_finding4_i0a_current_twelve_path_worktree_capture_01/SENTINEL_INSTALLATION_VERIFICATION.md` — verified canonical installation at `b2e0506cce3e7be60ed5a5ec6b18b6eec07cf7e1`.
- `HANDOFF_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_SHA256SUMS.txt` — focused historical inventory for the capture-acceptance package.
- `HANDOFF_CURRENT_TWELVE_PATH_WORKTREE_CAPTURE_VERIFICATION_SHA256SUMS.txt` — focused inventory for installation verification and central synchronization.
- `scope_authoring/rev23_finding4_i0a/starting_state_amendment_revision_10/` — accepted Candidate 04 and Sentinel acceptance records.
- `HANDOFF_REVISION_10_STARTING_STATE_AMENDMENT_SHA256SUMS.txt` — focused Candidate 04 installation inventory.
- `authorization_audit/rev23_finding4_i0a_candidate04_workspace_preparation_01/` — accepted Candidate 02 workspace-preparation documentation package.
- `HANDOFF_CANDIDATE04_WORKSPACE_PREPARATION_SHA256SUMS.txt` — focused Candidate 02 installation inventory.

Historical checksum inventories remain immutable evidence of the states they recorded. They are not regenerated or reinterpreted as inventories of this later provenance acceptance.

## Historical accepted evidence

- `accepted_scope_revision_09/` and `accepted_scope_revision_08/` remain immutable.
- Their corresponding manifests, decisions, and authorization records remain audit evidence.
- Revision 09 R1 and Revision 08 implementation authorizations are historical and non-reusable under Revision 10.

## Preserved implementation evidence

- checkpoint: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- exact payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
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

## Provenance state

Closed by accepted capture:

- `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`.

Still open:

- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`.

The capture contains all twelve untracked paths: eleven baseline-matching and one checkpoint-modified. It is evidence only and does not select an implementation start.

## Current authorization state

No source authoring is active. The installed authorization package cannot activate from its failed canonical-worktree source gate. Candidate 04 is installed and verified but does not repair or reactivate the old package. Accepted Candidate 02 defines a possible future workspace-preparation gate; its documentation installation remains pending Sentinel verification. Workspace execution authorization is `NONE`. Workspace preparation, source/test authoring, materialization, local implementation commits, pushes, tests, execution, rollback, promotion, data/network activity, Git history writes by Claude, and downstream stages remain unauthorized.
