# CHANGE LEDGER — Revision 22 to Revision 23

| Finding | Revision 23 correction |
|---|---|
| Archive depended on retained bytes outside Revision 22 | Embedded byte-identical Source D R17, Requests R18, curl R20, header R21, compatibility R21, and all R22 policy/vector files; all members enter SHA256SUMS. |
| Partial schema registry | Replaced with a complete closed registry covering all pre-run, run, authorization, capture, analysis, comparison, stop, inventory, and finalization artifacts. |
| Run establishment attachment could be circular | Added detached pre-run attachment semantic object computed before run ID, then a closed run-identity semantic object and nonmutating run-scoped attachment manifest. |
| Revision number was insufficient package binding | Added detached governing-package manifest and bound its semantic hash across fingerprint readiness, run identity, authorization, pre-V7 validation, and final inventories. |
| Authorization files could overwrite one another | Added immutable per-authorization directories, semantic IDs, complete-file sidecars, request-set semantic/file hashes, and cross-file equality rules. |
| Reservation-before-start recovery was open | Added terminal `REQUEST_RESERVATION_CANCELLED_NO_START` requiring positive zero-start snapshots and irreversible old-authorization closure. |
| Result table contained impossible all-clear exact-reproduction branch and causal wording | Replaced with reachable mutually exclusive exact-negative, below-threshold-difference, gain-only-clear, nonmonotone-clear, threshold-inconclusive, stop, and residue outcomes. |
| Consistency | Updated governing documents, registries, matrices, stops, results, tests, lifecycle, and package hashes; retained internal contract bytes unchanged. |
