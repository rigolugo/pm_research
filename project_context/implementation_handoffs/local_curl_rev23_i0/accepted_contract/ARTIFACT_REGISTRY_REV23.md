# ARTIFACT REGISTRY — Local-Curl Per-Side Dataset Verification — Revision 23

This registry is specification-only. Runtime paths describe possible future artifacts and authorize no production or execution. `SCHEMA_REGISTRY_REV23.json` is the machine-readable governing registry.

## Governing package bytes

The archive is self-contained. `GOVERNING_PACKAGE_MANIFEST_REV23.json` binds all governing documents, retained contracts/vector corpora, and Revision-22 policy files by exact package path and complete file SHA-256. `SHA256SUMS.txt` includes every archive member except itself.

## Persisted artifact catalog

| Path template | Schema | Producer | Cardinality | Mutability | Lifecycle |
|---|---|---|---|---|---|
| `GOVERNING_PACKAGE_MANIFEST_REV23.json` | `json:governing_package_manifest` | Professor package builder | exactly 1 | immutable | package detached manifest |
| `GOVERNING_PACKAGE_MANIFEST_REV23.sha256` | `json:sha256_sidecar` | Professor package builder | exactly 1 | immutable | package sidecar |
| `artifacts/local_curl_per_side/operational_audit/<run_id>.jsonl` | `table:operational_audit_events` | external operational audit writer | zero or more events | append-only outside finalized run | post-finalization write rejection and atomicity residue only |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/attachments/detached_pre_run_attachment_semantic.json` | `json:detached_pre_run_attachment_semantic` | V5A detached attachment builder | exactly 1 | immutable | pre-run detached semantic object |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/attachments/detached_pre_run_attachment_semantic.sha256` | `json:detached_pre_run_attachment_hash` | V5A detached attachment builder | exactly 1 | immutable | pre-run detached hash sidecar |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/fingerprint_readiness/run_policy_fingerprint_readiness.json` | `json:fingerprint_readiness_v23` | V5 fingerprint builder | exactly 1 | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/identity/pre_run_attempt_identity.json` | `json:pre_run_attempt_identity_v23` | V0 pre-run identity | exactly 1 | immutable | first committed pre-run artifact |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/policy/policy_observations.parquet` | `table:policy_observations` | V4 policy observer | exactly registered observation count | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/policy/policy_resolution.parquet` | `table:policy_resolution` | V4 policy resolver | exactly 32 rows | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/reconciliation/source_b_source_d_reconciliation.parquet` | `table:source_b_source_d_reconciliation` | V3 reconciliation | exactly 600 rows | immutable | all rows reconciled |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/reconciliation/source_b_source_d_reconciliation_summary.json` | `json:source_b_reconciliation_summary` | V3 reconciliation | exactly 1 | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_manifest/request_manifest.parquet` | `table:request_manifest` | V5 request manifest builder | exactly 496 rows | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_plan/request_plan.parquet` | `table:request_plan` | V5 request plan builder | exactly 496 rows | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_plan/request_plan_hashes.json` | `json:request_plan_hashes` | V5 request plan builder | exactly 1 | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/endpoint_shape_observations.parquet` | `table:endpoint_shape_observations` | V2 Source B parser/normalizer | exact registered locator rows | immutable | opens only after Source D commit |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/source_b_by_condition_raw.parquet` | `table:source_b_by_condition_raw` | V2 Source B parser/normalizer | exactly 300 rows | immutable | opens only after Source D commit |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/source_b_condition_rows.parquet` | `table:source_b_condition_normalized` | V2 Source B parser/normalizer | exactly 300 rows | immutable | opens only after Source D commit |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/source_b_excluded_raw.parquet` | `table:source_b_excluded_raw` | V2 Source B parser/normalizer | exactly 52 rows | immutable | opens only after Source D commit |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/source_b_excluded_rows.parquet` | `table:source_b_excluded_normalized` | V2 Source B parser/normalizer | exactly 52 rows | immutable | opens only after Source D commit |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/source_b_normalization_summary.json` | `json:source_b_normalization_summary` | V2 Source B normalizer | exactly 1 | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_b/source_b_provenance.json` | `json:source_b_provenance_v23` | V2 Source B provenance producer | exactly 1 | immutable | pre-run |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_data_input_inventory.json` | `json:source_d_data_input_inventory` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_detached_provenance.json` | `json:source_d_detached_provenance_v23` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_implementation_provenance.json` | `json:implementation_provenance` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_isolation_attestation.json` | `json:source_d_isolation_attestation` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_provenance_attestation.json` | `json:source_d_provenance_attestation` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_regeneration_summary.json` | `json:source_d_regeneration_summary` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_request_rows.parquet` | `table:source_d_request` | V1 Source D pure reconstruction | exactly 496 rows | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_runtime_provenance.json` | `json:runtime_provenance` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_source_b_ordering_attestation.json` | `json:source_d_source_b_ordering_attestation` | V1 Source D provenance producer | exactly 1 | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_token_rows.parquet` | `table:source_d_token` | V1 Source D pure reconstruction | exactly 600 rows | immutable | committed before Source B opens |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/stops/<stop_code>/PRE_RUN_STOP_FINALIZATION_FAILED.json` | `json:finalization_marker_v23` | pre-run finalization failure handler | zero or one | append-only residue outside finalized directory | no finalized marker |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/stops/<stop_code>/PRE_RUN_STOP_FINALIZED.json` | `json:finalization_marker_v23` | pre-run stop finalizer | zero or one | immutable marker | mutually exclusive with failure residue |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/stops/<stop_code>/pre_run_stop_envelope.json` | `json:pre_run_stop_envelope_v23` | V0-V6 pre-run stop handler | zero or one per stop | immutable if committed | pre-run stop |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/stops/<stop_code>/pre_run_stop_inventory.json` | `json:pre_run_stop_inventory_v23` | pre-run stop finalizer | zero or one | immutable | absent if finalization failed |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/compatibility/audit_snapshot_manifest.json` | `json:audit_snapshot_manifest` | compatibility snapshot finalizer | one current manifest plus immutable historical manifests by sequence | immutable per sequence | hash chain uses previous manifest file hash; never self-hashes |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/compatibility/partitions/<partition_id>.parquet` | `table:canonical_compatibility_analysis` | compatibility detached partition writer | zero or more immutable partitions | immutable | partition bytes committed before snapshot manifest |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/compatibility/snapshot_partitions.parquet` | `table:snapshot_partition` | compatibility snapshot indexer | zero or more rows, one per immutable partition | append-only via replacement snapshot object | detached partition index; rows never contain containing snapshot hash |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/compatibility_analysis.parquet` | `table:canonical_compatibility_analysis` | V8 compatibility analyzer | exactly 496 rows at closure including interrupted branches | immutable partitioned | pinned target analysis |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/compatibility_analysis_summary.json` | `json:compatibility_analysis_summary` | V9 summary builder | exactly 1 | immutable | C01-C23 counts sum 496 |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/compatibility_decoded_points.parquet` | `table:canonical_compatibility_decoded_points` | V8 compatibility analyzer | zero or more rows | immutable partitioned | only complete valid point series |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/condition_pair_analysis.parquet` | `table:condition_pair_analysis` | V9 pair reducer | exactly 300 rows | immutable | 248 query-eligible plus 52 invalid-window conditions |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/http_status_reconciliation.parquet` | `table:http_status_reconciliation` | V8 status reconciler | one per selected completed attempt | immutable partitioned | before body analysis |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/request_disposition_summary.json` | `json:request_disposition_summary` | V9 disposition builder | exactly 1 | immutable | counts reconcile 496 |
| `artifacts/local_curl_per_side/runs/<run_id>/analysis/selected_request_dispositions.parquet` | `table:selected_request_disposition` | V9 disposition builder | exactly 496 rows | immutable | highest-attempt precedence |
| `artifacts/local_curl_per_side/runs/<run_id>/attachments/pre_run_attachment_manifest.json` | `json:run_attachment_manifest_v23` | V6 run establishment | exactly 1 | immutable | references detached hash without altering it |
| `artifacts/local_curl_per_side/runs/<run_id>/authorization/authorization_use_events.parquet` | `table:authorization_use_events` | V7 authorization-use ledger | append-only rows | append-only with detached snapshots | authorization namespace retained per row |
| `artifacts/local_curl_per_side/runs/<run_id>/authorization/records/<authorization_id>/authorization_record.json` | `json:network_authorization_record_v23` | Gustavo external authorization | one per authorization ID | immutable external | never overwritten |
| `artifacts/local_curl_per_side/runs/<run_id>/authorization/records/<authorization_id>/authorization_record.sha256` | `json:authorization_record_sidecar_v23` | Gustavo/external sidecar producer | one per authorization ID | immutable external | never overwritten |
| `artifacts/local_curl_per_side/runs/<run_id>/authorization/records/<authorization_id>/authorized_request_set.json` | `json:authorized_request_set_v23` | Gustavo/external request-set producer | one per authorization ID | immutable external | never overwritten |
| `artifacts/local_curl_per_side/runs/<run_id>/authorization/records/<authorization_id>/authorized_request_set.sha256` | `json:authorized_request_set_sidecar_v23` | Gustavo/external sidecar producer | one per authorization ID | immutable external | never overwritten |
| `artifacts/local_curl_per_side/runs/<run_id>/capture/audit_snapshot_manifest.json` | `json:audit_snapshot_manifest` | capture snapshot finalizer | one current manifest plus immutable historical manifests by sequence | immutable per sequence | hash chain uses previous manifest file hash; never self-hashes |
| `artifacts/local_curl_per_side/runs/<run_id>/capture/capture_events.parquet` | `table:capture_events` | V7 capture runner | append-only attempts | append-only with detached snapshots | STARTED before launch; one terminal max |
| `artifacts/local_curl_per_side/runs/<run_id>/capture/partitions/<partition_id>.parquet` | `table:capture_events` | capture detached partition writer | zero or more immutable partitions | immutable | partition bytes committed before snapshot manifest |
| `artifacts/local_curl_per_side/runs/<run_id>/capture/quarantine_index.parquet` | `table:quarantine_index` | V8 quarantine indexer | zero or more, one row per quarantined attempt | append-only with detached snapshots | oversize or structurally isolated response residue only |
| `artifacts/local_curl_per_side/runs/<run_id>/capture/snapshot_partitions.parquet` | `table:snapshot_partition` | capture snapshot indexer | zero or more rows, one per immutable partition | append-only via replacement snapshot object | detached partition index; rows never contain containing snapshot hash |
| `artifacts/local_curl_per_side/runs/<run_id>/comparison/all_one_safeguard.json` | `json:all_one_safeguard` | V9 safeguard engine | exactly 1 | immutable | exactly two vector records |
| `artifacts/local_curl_per_side/runs/<run_id>/comparison/comparison_rows.parquet` | `table:comparison_rows` | V9 comparison builder | exactly 300 rows | immutable | 248 eligible + 52 invalid |
| `artifacts/local_curl_per_side/runs/<run_id>/comparison/comparison_summary.json` | `json:comparison_summary` | V9 comparison builder | exactly 1 | immutable | comparison counts total |
| `artifacts/local_curl_per_side/runs/<run_id>/comparison/current_pair_states.parquet` | `table:current_pair_states` | V9 pair reducer | exactly 248 rows | immutable | fixed denominators |
| `artifacts/local_curl_per_side/runs/<run_id>/comparison/subclass_thresholds.json` | `json:subclass_thresholds_array` | V9 threshold engine | exactly 3 records | immutable | fixed denominators 50/98/100 |
| `artifacts/local_curl_per_side/runs/<run_id>/finalization/REPLAY_FINALIZED.json` | `json:finalization_marker_v23` | V10 replay finalizer | zero or one | immutable marker | mutually exclusive |
| `artifacts/local_curl_per_side/runs/<run_id>/finalization/RUN_STOP_FINALIZATION_FAILED.json` | `json:finalization_marker_v23` | V10 finalization failure handler | zero or one | external residue | no finalized marker |
| `artifacts/local_curl_per_side/runs/<run_id>/finalization/STOP_FINALIZED.json` | `json:finalization_marker_v23` | V10 stop finalizer | zero or one | immutable marker | mutually exclusive |
| `artifacts/local_curl_per_side/runs/<run_id>/finalization/final_artifact_inventory.json` | `json:final_artifact_inventory` | V10 replay finalizer | zero or one | immutable | package hash bound |
| `artifacts/local_curl_per_side/runs/<run_id>/finalization/stop_artifact_inventory.json` | `json:stop_artifact_inventory` | V10 stop finalizer | zero or one | immutable | package hash bound |
| `artifacts/local_curl_per_side/runs/<run_id>/identity/run_identity.json` | `json:run_identity_v23` | V6 run establishment | exactly 1 | immutable | first run identity |
| `artifacts/local_curl_per_side/runs/<run_id>/policy/pre_v7_metadata.json` | `json:pre_v7_metadata` | V6/V7 validator | exactly 1 | immutable | must bind package/contract hashes |
| `artifacts/local_curl_per_side/runs/<run_id>/policy/run_policy_fingerprint.json` | `json:run_policy_fingerprint` | V6 run establishment | exactly 1 | immutable | run-scoped validated fingerprint |
| `artifacts/local_curl_per_side/runs/<run_id>/reports/result_summary.json` | `json:result_summary_v23` | V9 result engine | zero or one | immutable | only structurally valid replay result |
| `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_manifest/token_manifest.parquet` | `table:token_manifest` | V5 token-manifest builder | exactly 600 rows | immutable | V5 pre-run; after V3 reconciliation and before request manifest |
| `artifacts/local_curl_per_side/runs/<run_id>/resume/resume_journal.parquet` | `table:resume_journal` | V7-V9 resume controller | zero or more, strictly increasing journal_ordinal | append-only with detached snapshots | records every resume/skip/retry/cancellation decision |
| `artifacts/local_curl_per_side/runs/<run_id>/stop/stop_state.json` | `json:stop_state` | V7-V10 stop handler | zero or one | immutable | no replay label |
| `artifacts/local_curl_per_side/runs/<run_id>/strict/audit_snapshot_manifest.json` | `json:audit_snapshot_manifest` | strict snapshot finalizer | one current manifest plus immutable historical manifests by sequence | immutable per sequence | hash chain uses previous manifest file hash; never self-hashes |
| `artifacts/local_curl_per_side/runs/<run_id>/strict/partitions/<partition_id>.parquet` | `table:strict_audit_analysis` | strict detached partition writer | zero or more immutable partitions | immutable | partition bytes committed before snapshot manifest |
| `artifacts/local_curl_per_side/runs/<run_id>/strict/snapshot_partitions.parquet` | `table:snapshot_partition` | strict snapshot indexer | zero or more rows, one per immutable partition | append-only via replacement snapshot object | detached partition index; rows never contain containing snapshot hash |
| `artifacts/local_curl_per_side/runs/<run_id>/strict/strict_audit.parquet` | `table:strict_audit_analysis` | V8 strict analyzer | one per selected request or explicit noncompleted state | immutable partitioned | independent raw-byte audit |
| `artifacts/local_curl_per_side/runs/<run_id>/strict/strict_audit_summary.json` | `json:strict_audit_summary` | V9 strict summary builder | exactly 1 | immutable | counts reconcile selected requests |
| `artifacts/local_curl_per_side/runs/<run_id>/strict/strict_decoded_points.parquet` | `table:strict_audit_decoded_points` | V8 strict analyzer | zero or more rows | immutable partitioned | only strict-valid complete series |
| `contracts/CANONICAL_COMPATIBILITY_EDGE_VECTORS_REV21.json` | `json:compatibility_edge_vectors` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `contracts/CURL_SUBPROCESS_CONTRACT_REV20.json` | `json:curl_subprocess_contract` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `contracts/REQUESTS_JSON_EQUIVALENCE_CONTRACT_REV18.json` | `json:requests_json_equivalence_contract` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `contracts/RESPONSE_HEADER_EXTRACTION_CONTRACT_REV21.json` | `json:response_header_extraction_contract` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `contracts/RESPONSE_HEADER_EXTRACTION_VECTORS_REV21.json` | `json:response_header_extraction_vectors` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `contracts/SOURCE_D_ALGORITHM_CONTRACT_REV17.json` | `json:source_d_algorithm_contract` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `policies/HTTP_STATUS_RECONCILIATION_VECTORS_REV22.json` | `json:http_status_reconciliation_vectors_v22` | Professor byte-copy packager | exactly 1 | immutable | package retained vector bytes |
| `policies/TRANSPORT_POLICY_REV22.json` | `json:transport_policy` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |
| `policies/URL_SERIALIZATION_POLICY_REV22.json` | `json:url_serialization_policy` | Professor byte-copy packager | exactly 1 | immutable | package retained governing bytes |

## Global invariants

- Every listed path has exactly one governing schema and one producer.
- Every consumer list is nonempty.
- Pre-run artifacts cannot contain a `run_id` before V6. The sole token manifest is the registered V5 pre-run artifact; a run-scoped token-manifest copy is prohibited.
- Authorization records are namespaced and immutable.
- Finalized directories are immutable; rejected writes are logged only outside them.
- Missing evidence never becomes negative evidence or continuation eligibility.


# REV23 Finding 4 artifact additions


The following path families are closed and governing only as defined by the effective Finding 4 amendment:

```text
artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/<unit_kind>/<prepared_unit_id>/
artifacts/local_curl_per_side/runs/<run_id>/<audit_family>/snapshot_history/<snapshot_sequence_20d>/
artifacts/local_curl_per_side/runs/<run_id>/<audit_family>/snapshot_partitions/<partition_id>.parquet
artifacts/local_curl_per_side/runs/<run_id>/<audit_family>/current_generations/<snapshot_sequence_20d>/
artifacts/local_curl_per_side/runs/<run_id>/capture/commit_fence_history/<fence_sequence_20d>/
artifacts/local_curl_per_side/runs/<run_id>/authorization_use/row_batches/<batch_id>.parquet
artifacts/local_curl_per_side/runs/<run_id>/capture/row_batches/<batch_id>.parquet
artifacts/local_curl_per_side/runs/<run_id>/CONFLICT_STOP_FINALIZED/
```

Each immutable multi-file publication commits by atomic no-replace directory promotion. Every prepared source, row batch, history member, fence member, sidecar, aggregate view, and terminal object has the exact producer, consumer, cardinality, hash, recovery, inventory, and immutability rule in the effective amendment. Current aliases and aggregate Parquet views are derived views and never historical authority.
