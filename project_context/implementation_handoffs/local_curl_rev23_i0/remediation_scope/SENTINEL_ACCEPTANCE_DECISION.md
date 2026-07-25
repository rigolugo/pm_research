APPROVE — REV10_LOCAL_CURL_REMEDIATION_SCOPE_ACCEPTED

# Sentinel Acceptance Decision — Revision 10 Local-Curl Remediation Scope

## Decision identity

- decision date: `2026-07-24`;
- canonical review base: `cc2964840d197a40d1c4ef567b42eda762c0be0a`;
- controlling implementation specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`;
- accepted remediation source: `REV10_LOCAL_CURL_IMPLEMENTATION_REMEDIATION_SCOPE_CANDIDATE_01`;
- submitted ZIP SHA-256: `e6bc7139c39bd75630ad480821c203dbd5c2a914dae3b23fd26b9bfe2f513c1a`;
- accepted materialized member count: `11`;
- package authorization effect: `NONE`;
- implementation authorization: `false`;
- implementation starting SHA selected: `false`.

## Decision

Sentinel accepts the submitted remediation-scope package as the smallest complete planning contract that could correct the eight verified Revision 10 implementation-conformance defects.

Acceptance applies only to the immutable materialized files under `accepted_remediation_scope_candidate_01/` together with the binding determinations in this decision. It does not accept or promote any implementation bytes.

## Accepted boundary

### Atomic future source-authoring candidate

Any later implementation-authoring authorization must treat these three source paths as one atomic conformance candidate:

1. `pm_research/local_curl_per_side/canonical.py`;
2. `pm_research/local_curl_per_side/finding4_registry.py`;
3. `pm_research/local_curl_per_side/prepared_evidence.py`.

A partial one-file correction is not sufficient and must not be represented as Revision 10 conformance.

### Separately gated future test-source candidate

Test-source authoring, if later accepted and explicitly authorized, is limited to:

1. `tests/local_curl_per_side/test_canonical_i0a.py`;
2. `tests/local_curl_per_side/test_finding4_registry_i0a.py`;
3. `tests/local_curl_per_side/test_i0a_public_contract.py`;
4. `tests/local_curl_per_side/test_prepared_evidence_i0a.py`.

Source authoring, test-source authoring, and test execution remain separate authorization boundaries.

## Verified defect coverage

The accepted scope covers:

1. coordinated mandatory source-path coverage;
2. four missing public result codes and empty-assurance mappings;
3. closed `UnitContext` validation;
4. sole registry-owned normalized-path decomposition and typed bindings;
5. descriptor pre-binding and global path/reuse/family/run reductions;
6. removal of superseded private descriptor-set ordinal ownership;
7. Revision 10 selected-payload predicate order and typed projection;
8. unit-level delegation through `validate_selected_json_payload`.

## Binding determinations

### Selected-member ordering

The accepted deterministic order is:

1. wrapper-eligible sidecars;
2. wrapper-eligible non-sidecars;
3. ascending numeric `object_ordinal` within each class.

### Closed `UnitContext` interpretation

- preserve the accepted `UnitContext` type and field inventory;
- reject mappings and structural lookalikes;
- accept only exact semantic-family values;
- treat path representations as distinct from semantic-family values;
- require `type(subject_sequence) is int`;
- reject `bool`;
- require `0 <= subject_sequence <= 2^64 - 1`;
- perform no aliasing, coercion, or inferred defaulting.

### Checksum convention

The candidate `SHA256SUMS.txt` correctly inventories every other candidate member. The detached ZIP SHA-256 identifies the complete submitted archive and resolves the unavoidable checksum-file self-reference boundary.

## Checkpoint and provenance

The preserved checkpoint remains `NOT_ACCEPTED`, non-controlling, evidence-only, and authorization effect `NONE`. The two open provenance gaps remain open and separate from implementation conformance.

## Strongest alternative verdict

The strongest alternative was `BLOCK` because the candidate left three interpretation questions to Sentinel and did not select implementation starting bytes. That alternative is rejected because this decision resolves the interpretation questions from the controlling contract, while starting-byte selection properly belongs to a later, separately authorized implementation package.

## Authorization

This decision authorizes only documentation-only canonical installation of this accepted record after Gustavo's explicit authorization. It does not authorize implementation, source/test authoring, test execution, project execution, data/network activity, artifact generation, Git writes by Claude, or any downstream phase.

## Next action

Gustavo manually installs and commits the documentation package at exact base `cc2964840d197a40d1c4ef567b42eda762c0be0a`, then returns the resulting full commit SHA to Sentinel. Sentinel verifies the installed paths and bytes before any implementation-authorization decision is considered.
