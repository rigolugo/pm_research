# Implementation Review Deliverables

Claude must return one deterministic review package outside the repository containing:

1. `README_FIRST.md` — package identity, source-gated commit, authorization ID, and read order;
2. `IMPLEMENTATION_ACTIVITY_REPORT.json` — activities performed and explicit false values for tests, imports, project execution, data, network, and Git writes;
3. `CHANGED_PATHS.txt` — exactly the three writable source paths;
4. `STARTING_SHA256SUMS.txt` — exact authorized starting hashes for the three writable paths;
5. `ENDING_SHA256SUMS.txt` — exact ending hashes for the three writable paths;
6. `READ_ONLY_PATH_SHA256SUMS.txt` — exact ending hashes for the nine protected paths, unchanged from the gate;
7. `DIFF_SUMMARY.md` — per-file contract obligations implemented, with no claim of test success;
8. `payload_exact/` — exact final bytes for the three writable paths only;
9. `SHA256SUMS.txt` — checksums for every package member except itself;
10. detached ZIP SHA-256.

The package must state that no tests were authored or executed, no project module was imported or executed, no research data or network was accessed, no Git history was written, and no downstream stage was performed.

The implementation-review package is evidence for Sentinel static review only. It does not promote its payload into the canonical executable tree and authorizes no subsequent stage.
