# I0A Stop and Result Domain — Revision 10 Candidate 11

## Status and authority

`SPEC-ONLY REVIEW CANDIDATE — NOT ACCEPTED`

Accepted Revision 09 remains controlling. Its accepted base SHA-256 is
`6a16695f7ffbc01fdd8a119844df5ffb6f83268eda4a70838f86c05b3c9a573a`. Candidate 10, ZIP SHA-256 `d5aa07180aae9685b21499d50e944ba5962379c77aa9cd5661ba7bde3dfb8979`, is the direct non-authoritative drafting predecessor. Candidate 09 and earlier candidates are non-controlling historical evidence.

## Public domain amendment

Candidate 11 preserves the four Revision 10 amendment error codes:

```text
ERR_UNIT_CONTEXT_INVALID
ERR_SEMANTIC_FAMILY_BINDING_MISMATCH
ERR_RUN_ID_BINDING_MISMATCH
ERR_REUSE_SOURCE_TARGET_MISMATCH
```

Every error and stop returns `established_assurances=()`.

The complete function-specific domains and order are materialized in `I0A_PUBLIC_API_CONTRACT_REVISION_10_CANDIDATE_11.json`.
No result may be inferred from another caller's narrower reachable subset.

## Resolver and wrapper

`resolve_selected_schema_binding` retains `ERR_BINDING_QUERY_INVALID` in its direct
closed domain. Through `validate_selected_json_payload`, that result is statically
unreachable only because `_project_selected_binding_query` constructs the complete
accepted `BindingQuery` after all listed typed preconditions.

`STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A` remains a selected-wrapper result after
successful binding. It is not a resolver result.

## Delegated failures

The unit validator and dispatcher propagate reachable delegated failures unchanged,
including:

```text
ERR_LOGICAL_SHA256_MISMATCH
ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED
ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH
ERR_LOGICAL_ROWS_INVALID
```

No delegated non-success becomes success or retains partial assurance.

## Selected sidecar

The exact precedence remains:

```text
selected physical expectation
selected physical size
selected physical SHA-256
paired physical expectation
paired physical size
paired physical SHA-256
final sidecar target-path/hash semantic relation
```

The final semantic mismatch returns
`ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH`.

## Persisted domain

Candidate 11 adds no persisted `REV23_STOP_CODE`, research result, gate state, or
negative finding.


## Candidate 11 canonical-state boundary

Canonical HEAD is `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`. `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` is the historical Revision 09 R1 authorized start only. Checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` at `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da` is canonically preserved but `NOT_ACCEPTED`, has conformance `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`, and authorization effect `NONE`. Candidate 11 selects no implementation starting SHA and creates no rollback or promotion instruction.
