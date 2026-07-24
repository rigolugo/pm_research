# README FIRST — Revision 09 R1 Source Resume Authorization

Status: **ACTIVE — SENTINEL VERIFIED**.

Authorization ID
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01` is active at the exact verified source-gated commit
`1e1afb29791f42c286b45d3b576f74926add8dce`.

## Read order

1. `GUSTAVO_AUTHORIZATION_RECORD.md`
2. `SENTINEL_AUTHORIZATION_DECISION.md`
3. `SENTINEL_ACTIVATION_VERIFICATION.md`
4. `AUTHORIZED_FILE_MATRIX.md`
5. `REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt`
6. `ACTIVITY_BOUNDARIES.md`
7. `SOURCE_GATE.md`
8. `AUTHORIZATION_MANIFEST.json`
9. `SHA256SUMS.txt`

## Active boundary

Only `pm_research/local_curl_per_side/prepared_evidence.py` may be edited. Its
required starting SHA-256 is
`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`.

The other eleven baseline paths are read-only. Test-source authoring, test
execution, another source-file edit, project imports or execution, R2, and every
downstream or empirical stage remain unauthorized.
