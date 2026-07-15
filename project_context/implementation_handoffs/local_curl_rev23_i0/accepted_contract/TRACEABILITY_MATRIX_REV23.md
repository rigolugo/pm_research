# REQUIREMENTS TRACEABILITY MATRIX — Local-Curl Revision 23

| Requirement | Spec section | Schema / invariant | Stop or decision rule | Proposed test |
|---|---|---|---|---|
| Self-contained archive | §1.1 | package manifest + retained contract schemas | STOP_GOVERNING_PACKAGE_MANIFEST_INVALID | delete earlier packages; validate all embedded bytes |
| Complete closed registry | §22 | artifact_catalog + table/json schemas | STOP_SCHEMA_RECONCILIATION_FAILED | one schema/producer/consumer per path; no unresolved refs |
| Detached pre-run attachment | §8.3 | json:detached_pre_run_attachment_semantic | STOP_DETACHED_PRE_RUN_ATTACHMENT_INVALID | mutation/path/hash/logical-hash counterexamples |
| Noncircular run identity | §8.5 | json:run_identity_semantic_v23 | STOP_RUN_ESTABLISHMENT_FAILED | field mutation and run-id recomputation |
| Package-manifest binding | §8.4 | json:governing_package_manifest | STOP_GOVERNING_PACKAGE_MANIFEST_INVALID | extra/missing/changed package file |
| Namespaced authorization | §12 | authorization record/request-set schemas | STOP_AUTHORIZATION_INVALID | coexisting modes without overwrite |
| Request-set equality | §12.2 | json:authorized_request_set_v23 | STOP_AUTHORIZED_REQUEST_SET_INVALID | wrong order/member/hash/file sidecar |
| Reservation cancellation | §13 | authorization_use conditional union | STOP_RESERVATION_NO_START_PROOF_INVALID | missing/partial/contradictory no-start evidence |
| Source B authority | §§3,5 | Source B raw/normalized tables and provenance | STOP_SOURCE_B_INVALID | schema/count/subset/lexical tests |
| Source D isolation | §4 | Source D tables/provenance/contract | STOP_SOURCE_D_ISOLATION_FAILED | forbidden input interface test |
| 600-row reconciliation | §6 | table:source_b_source_d_reconciliation | STOP_RECONCILIATION_FAILED | each mismatch dimension |
| Sole pre-run token manifest | §§8,10 | table:token_manifest; artifact catalog/binding | STOP_MANIFEST_COUNT_OR_HASH_INVALID / STOP_DETACHED_PRE_RUN_ATTACHMENT_INVALID | reject old path, dual copy, 599/601 rows, bad provenance, false eligibility |
| Exact request-manifest binding | §10.2 | table:request_manifest + request_manifest_row_sha256 | STOP_MANIFEST_COUNT_OR_HASH_INVALID / STOP_REQUEST_EXECUTION_ORDER_INVALID | unrelated eligible token hash, `.0` loss, ordinal/order mismatch |
| Exact request-plan closure | §10.4 | table:request_plan + request_plan_row_sha256 | STOP_REQUEST_PLAN_INVALID | field/membership/parameter/fidelity/URL/hash counterexamples |
| Integer pre-run identity | §§7.2,8.2 | json:pre_run_attempt_identity_v23 | STOP_PRE_RUN_ID_COLLISION / STOP_SCHEMA_RECONCILIATION_FAILED | reject string/float/exponent/Boolean/null created_at_ns |
| Sole partition identity | §7.2 | semantic_hashes.partition_id | STOP_ROW_HASH_PROJECTION_INVALID / STOP_SEMANTIC_ID_COLLISION | empty/nonempty families and alternate projection rejection |
| Typed-cell tag closure | §§7.1,10,15 | row_hash_projections.*.typed_cells + typed_row_contract | STOP_ROW_HASH_PROJECTION_INVALID / governing schema stop | reject width-specific tags; verify every storage field resolves once |
| Exact null encoding | §7.1 | typed_row_contract.null_representation + nullable typed cells | STOP_ROW_HASH_PROJECTION_INVALID / governing schema stop | every nullable field null uses `NULL`; non-null-tagged null fails |
| Partition-family closure | §7.2 | enum:partition_audit_family + semantic_hashes.partition_id.field_domains | STOP_ROW_HASH_PROJECTION_INVALID / STOP_SEMANTIC_ID_COLLISION | accept exactly three values; reject broad-enum-only values |
| Twelve HTTP outer cells | §15 | table:http_status_reconciliation.conditional_requirements | STOP_HTTP_WRITEOUT_INVALID / STOP_HTTP_STATUS_EVIDENCE_MISMATCH | exact 3×4 Cartesian nullability and range test |
| Sole HTTP reconciliation schema version | §15.1 | table:http_status_reconciliation.schema_version + schema-version field domain + row-hash schema_id | STOP_SCHEMA_RECONCILIATION_FAILED | assert exactly `local_curl_http_status_reconciliation.v23` and reject aliases |
| Total raw stdout evidence derivation | §15.2 | write_out_evidence_derivation + capture COMPLETED raw Base64 binding | STOP_HTTP_WRITEOUT_INVALID / STOP_SCHEMA_RECONCILIATION_FAILED | arbitrary byte corpus; hash/lexeme/state/integer disagreement counterexamples |
| Selected-header parser binding | §15.3 | selected_header_evidence_derivation + retained parser SHA-256 | STOP_HTTP_STATUS_EVIDENCE_MISMATCH / STOP_SCHEMA_RECONCILIATION_FAILED | exact parser-output equality and caller-override rejection |
| Twelve cells after evidence derivation | §15.4 | unchanged conditional_requirements | STOP_HTTP_WRITEOUT_INVALID / STOP_HTTP_STATUS_EVIDENCE_MISMATCH | derive first, then assert exact 3×4 outputs and reachability |
| Completed-capture lifecycle totality | §§14.1,15 | capture_event_lifecycle_contract + capture_events.COMPLETED + http_status_reconciliation.completed_capture_lifecycle_binding | STOP_HTTP_WRITEOUT_INVALID / registered HTTP-table outcome | assert all 3 categories × all 3 derived states; all 9 persist reconciliation; invalid always stops; no direct C02/C03/C07-C23 |
| Reproducible target transformation | package materialization | RFC 6902 + transformation manifest + replacements | Sentinel verification failure; no acceptance | reconstruct every target byte from baseline |
| Total HTTP status mapping | §15 | table:http_status_reconciliation | STOP_HTTP_WRITEOUT_INVALID / STOP_HTTP_STATUS_EVIDENCE_MISMATCH | all state cells plus equal/generic-unequal status pairs |
| Exact URL/request ordering | §§10-11 | request manifest/plan + Rev22 policies | STOP_REQUEST_PLAN_INVALID | serializer/ordinal/lexeme/hash vectors |
| Capture/auth binding | §§13-15 | capture and authorization-use schemas | STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED | cross-file tuple mismatch |
| Compatibility/strict separation | §§16-17 | compatibility and strict tables | structural or inconclusive rule | retained vector corpora exact execution |
| Valid interruption | §14 | selected disposition schema | no structural stop for valid interruption | fixed-vector unresolved propagation |
| Fixed denominators | §20 | threshold schema and invariants | result decision | 50/98/100 immutable under unresolved |
| Reachable result labels | §21 | result algorithm + table | ordered first match | exact reproduction/clear/difference reachability |
| Finalization immutability | §§8.6,23 | inventories and marker schemas | UNFINALIZED_OPERATIONAL_RESIDUE | atomicity/post-finalization tests |
| Authorization boundary | §§0,28 | non-authorization closing | no progression | acceptance never authorizes implementation/run |
