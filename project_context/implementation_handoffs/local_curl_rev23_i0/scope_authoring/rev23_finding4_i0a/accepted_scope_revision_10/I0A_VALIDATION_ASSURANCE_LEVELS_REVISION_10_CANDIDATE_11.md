# I0A Validation Assurance Levels — Revision 10 Candidate 11

## Status and base

`SPEC-ONLY REVIEW CANDIDATE — NOT ACCEPTED`

Accepted Revision 09 remains controlling. Accepted base SHA-256:
`9bf2907d3af4de2f7e0aec0fb648229d72e9af26366a8c167cf77b8d4a51cd43`.

## Non-success invariant

Every public error or stop returns the empty assurance tuple. This includes every
direct, translated, propagated, and typed-seam-inspected non-success.

No A1, A2, A3, A4, A6, or partial assurance survives:

- `ERR_LOGICAL_SHA256_MISMATCH`;
- `ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED`;
- `ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH`;
- `ERR_BINDING_QUERY_INVALID`;
- any other error or stop in the controlling inventory.

## Success preservation

Candidate 11 does not change accepted success assurance tuples. In particular:

- `I0A_BINDING_RESOLVED_A1` remains resolver success;
- `I0A_VALID_A3_EXACT` remains physical-reconciliation success;
- `I0A_VALID_A6_SELECTED` is reached only after all selected-sidecar predicates pass.

The success-only `_project_selected_binding_query` helper establishes no public
assurance. The inspection seam establishes no assurance and has no success domain.

## Closure rule

For every delegated edge, caller assurances equal the exact callee non-success
mapping after any declared translation. Because every non-success mapping is empty,
propagation cannot accumulate or retain assurance.


## Candidate 11 canonical-state boundary

Canonical HEAD is `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`. `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` is the historical Revision 09 R1 authorized start only. Checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` at `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da` is canonically preserved but `NOT_ACCEPTED`, has conformance `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`, and authorization effect `NONE`. Candidate 11 selects no implementation starting SHA and creates no rollback or promotion instruction.
