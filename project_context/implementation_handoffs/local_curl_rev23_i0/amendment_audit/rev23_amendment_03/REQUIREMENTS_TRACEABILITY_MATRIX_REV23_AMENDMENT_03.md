# Requirements Traceability Matrix — REV23 Amendment 03 Rematerialization

| Requirement | Spec | Schema/invariant | Stop/decision | Proposed assertion |
|---|---|---|---|---|
| sole HTTP schema version | §§10.1/15.1 | table schema, field domain, row-hash schema_id | `STOP_SCHEMA_RECONCILIATION_FAILED` | only `local_curl_http_status_reconciliation.v23` occurs in active governing bytes |
| total write-out mapping | §§10.2/15.2 | `write_out_evidence_derivation` | `STOP_HTTP_WRITEOUT_INVALID` | arbitrary bytes map exactly once |
| evidence agreement | §§10.2/15.2 | Base64, SHA-256, lexeme, state, integer equality | schema or write-out stop | all listed counterexamples reject |
| selected-header binding | §§10.3/15.3 | retained parser adapter | HTTP mismatch/schema stop | state and integer equal parser output |
| preserved 12 combinations | §§10.4/15.4 | unchanged `conditional_requirements` | registered HTTP stops/continuations | exact 3×4 table after derivation |
| completed-capture lifecycle totality | §§10.5/14.1/15 | lifecycle contract + COMPLETED union + HTTP lifecycle binding | `STOP_HTTP_WRITEOUT_INVALID` / registered HTTP continuation | exact 3×3 matrix; every pair persists reconciliation; no bypass |
| preserved handoff | package handoff | baseline handoff exact-prefix invariant | Sentinel verification failure | prefix hash/bytes exact; no stale alternative |
| reproducible rematerialization | package manifests | RFC 6902/diff/replacement reconstruction | Sentinel verification failure | every target reconstructs byte-exactly |
