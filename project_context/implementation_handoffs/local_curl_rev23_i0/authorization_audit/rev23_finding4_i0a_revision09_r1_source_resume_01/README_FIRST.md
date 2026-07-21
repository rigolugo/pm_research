# README FIRST — Revision 09 R1 Source Resume Authorization

Status: installation review candidate.

Authorization ID
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01` is accepted but inactive
until Gustavo manually commits this exact documentation package and Sentinel
verifies the resulting commit.

## Read order

1. `GUSTAVO_AUTHORIZATION_RECORD.md`
2. `SENTINEL_AUTHORIZATION_DECISION.md`
3. `AUTHORIZED_FILE_MATRIX.md`
4. `REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt`
5. `ACTIVITY_BOUNDARIES.md`
6. `SOURCE_GATE.md`
7. `AUTHORIZATION_MANIFEST.json`
8. `SHA256SUMS.txt`

## Active-after-verification boundary

Only `pm_research/local_curl_per_side/prepared_evidence.py` may be edited after
activation. Its required starting SHA-256 is
`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`.

The other eleven baseline paths are read-only. Test-source authoring, test
execution, another source-file edit, project imports or execution, R2, and every
downstream or empirical stage remain unauthorized.
