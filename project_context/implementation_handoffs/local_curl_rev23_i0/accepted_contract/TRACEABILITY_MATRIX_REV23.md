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
| Exact URL/request ordering | §§10-11 | request manifest/plan + Rev22 policies | STOP_REQUEST_PLAN_INVALID | serializer/ordinal/lexeme/hash vectors |
| Capture/auth binding | §§13-15 | capture and authorization-use schemas | STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED | cross-file tuple mismatch |
| Compatibility/strict separation | §§16-17 | compatibility and strict tables | structural or inconclusive rule | retained vector corpora exact execution |
| Valid interruption | §14 | selected disposition schema | no structural stop for valid interruption | fixed-vector unresolved propagation |
| Fixed denominators | §20 | threshold schema and invariants | result decision | 50/98/100 immutable under unresolved |
| Reachable result labels | §21 | result algorithm + table | ordered first match | exact reproduction/clear/difference reachability |
| Finalization immutability | §§8.6,23 | inventories and marker schemas | UNFINALIZED_OPERATIONAL_RESIDUE | atomicity/post-finalization tests |
| Authorization boundary | §§0,28 | non-authorization closing | no progression | acceptance never authorizes implementation/run |
