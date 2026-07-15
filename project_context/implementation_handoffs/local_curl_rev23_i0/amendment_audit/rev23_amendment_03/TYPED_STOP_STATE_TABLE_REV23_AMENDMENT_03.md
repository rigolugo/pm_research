# Typed Stop-State Table — REV23 Amendment 03 Correction

| Stop code | Exact corrected trigger | Stage | Zero requests guaranteed | Artifact behavior | Downstream effect |
|---|---|---|---:|---|---|
| `STOP_ROW_HASH_PROJECTION_INVALID` | amended projection uses width-specific tag, wrong registered non-null tag, null with non-`NULL` tag, non-null with `NULL`, wrong field/order, coercion, or destination inclusion | stage-dependent | stage-dependent | preserve committed evidence and typed stop | no result |
| `STOP_MANIFEST_COUNT_OR_HASH_INVALID` | token/request manifest fails exact storage/tag/null/provenance/count/order/hash contract | V5 | true | pre-run stop evidence only | no V6/authorization/capture |
| `STOP_REQUEST_PLAN_INVALID` | request plan fails exact storage/tag/membership/URL/hash contract | V5 | true | pre-run stop evidence only | no V6 |
| `STOP_REQUEST_EXECUTION_ORDER_INVALID` | ordinal/order/order-hash defect | V5 | true | pre-run stop evidence only | no V6 |
| `STOP_SEMANTIC_ID_COLLISION` | same partition ID maps to different exact seven-cell bytes | snapshot stage | false | preserve partition evidence | structural stop |
| `STOP_CAPTURE_SNAPSHOT_INVALID` | capture partition family/value/actual/snapshot binding invalid | V7/V8 | false | preserve immutable evidence | no result |
| `STOP_ANALYSIS_SNAPSHOT_INVALID` | compatibility/strict partition family/value/actual/snapshot binding invalid | V8 | false | preserve immutable evidence | no result |
| `STOP_HTTP_WRITEOUT_INVALID` | any of the three completed curl categories derives `HTTP_CODE_INVALID`; persist the exact reconciliation row first | V8 | false | preserve completed capture and exact `NOT_RECONCILABLE_STOP` / `HTTP_WRITEOUT_INVALID` row | stop before compatibility or strict body analysis; C01–C23 unreachable |
| `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | any registered mismatch branch or unequal valid-status subcase | V8 | false | persist exact reconciliation row | C14–C23 unreachable |
