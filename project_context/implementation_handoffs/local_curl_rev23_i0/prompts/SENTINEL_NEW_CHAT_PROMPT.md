# New Sentinel chat — Verify REV23 Finding 4 Canonical Installation

Use only after Gustavo supplies the manual canonical-install commit SHA.

Review boundary: static canonical-install verification only.

Verify:

1. the submitted commit is a descendant of
   `f6cb60df66c2bbcdfb6d797119ed25ad79e06a11`;
2. changed paths equal the authorized Phase A installation set;
3. every accepted-contract file matches `ACCEPTED_CONTRACT_SHA256SUMS.txt`;
4. the governing manifest and sidecar validate;
5. the Finding 4 audit tree matches the accepted package;
6. the handoff checksum inventory reconciles;
7. no implementation, tests, dependency, CLI/runtime, empirical artifact, or
   research-data path changed;
8. implementation and source synchronization remain unauthorized.

Do not authorize implementation, tests, execution, local-data reads, network,
replay, P1/P2/P3, scoring, probe execution, or gate changes.
