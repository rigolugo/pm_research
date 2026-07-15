# Artifact Producer–Consumer Matrix — REV23_AMENDMENT_03 Delta

| Artifact | Producer | Consumers | Schema | Lifecycle |
|---|---|---|---|---|
| `pre_run_attempts/<pre_run_attempt_id>/source_d/source_d_token_rows.parquet` | V1 Source D | V3 reconciliation; V5 token-manifest builder; V5A | existing `table:source_d_token` | committed before Source B opens |
| `pre_run_attempts/<pre_run_attempt_id>/reconciliation/source_b_source_d_reconciliation.parquet` | V3 | V5 token-manifest builder; V5A; Sentinel | existing reconciliation table | immutable pre-run |
| `pre_run_attempts/<pre_run_attempt_id>/request_manifest/token_manifest.parquet` | V5 token-manifest builder | V5 request-manifest builder; V5A; V6 validator; authorization validator; Sentinel | `table:token_manifest` | immutable pre-run |
| `pre_run_attempts/<pre_run_attempt_id>/request_manifest/request_manifest.parquet` | V5 request-manifest builder | V5 plan builder; V5A; V6; authorization validator | `table:request_manifest` | immutable pre-run |
| `pre_run_attempts/<pre_run_attempt_id>/request_plan/request_plan.parquet` | V5 plan builder | V5A; V6; authorization validator; capture | `table:request_plan` | immutable pre-run |
| `pre_run_attempts/<pre_run_attempt_id>/attachments/detached_pre_run_attachment_semantic.json` | V5A | V6; authorization validator | existing detached attachment schema | immutable pre-run |
| `runs/<run_id>/capture/partitions/<partition_id>.parquet` | capture partition writer | snapshot validator; Sentinel | capture rows | immutable after commit |
| `runs/<run_id>/analysis/compatibility/partitions/<partition_id>.parquet` | compatibility partition writer | snapshot validator; Sentinel | compatibility rows | immutable after commit |
| `runs/<run_id>/strict/partitions/<partition_id>.parquet` | strict partition writer | snapshot validator; Sentinel | strict rows | immutable after commit |
| `runs/<run_id>/analysis/http_status_reconciliation.parquet` | V8 status reconciler | compatibility; strict; stop handler | totalized reconciliation schema | immutable partitioned |

**Prohibited artifact:** `runs/<run_id>/request_manifest/token_manifest.parquet`.

**Typed-cell metadata:** hash projections are schema-registry metadata; they do not create new artifacts, producers, or consumers.

The existing capture producer persists exact raw stdout Base64; the existing HTTP reconciliation producer copies and derives its hash/lexeme/state/integer. No new artifact or consumer is introduced.
