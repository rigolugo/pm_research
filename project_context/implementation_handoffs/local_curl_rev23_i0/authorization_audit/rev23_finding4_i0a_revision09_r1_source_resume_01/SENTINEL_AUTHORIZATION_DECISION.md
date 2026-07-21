# Sentinel Authorization Decision

Decision: **APPROVE — CONDITIONAL R1 SOURCE RESUME**

Authorization ID:
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

Sentinel independently verified:

- implementation-review archive SHA-256:
  `e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`;
- all internal archive checksum entries;
- later `prepared_evidence.py` checkpoint SHA-256:
  `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`;
- exact twelve-path composite baseline SHA-256:
  `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`.

Sentinel accepts only the one-file R1 source stage. Activation requires Gustavo's
manual canonical commit of this accepted documentation package and Sentinel's
verification of that exact commit.

After activation, the sole writable path is
`pm_research/local_curl_per_side/prepared_evidence.py`. All other baseline paths
are read-only. Test-source editing, test execution, another source edit, R2, and
every downstream or empirical stage remain unauthorized.
