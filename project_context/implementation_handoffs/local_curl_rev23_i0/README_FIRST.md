# REV23 Finding 4 Canonical Handoff — Contract Installed; I0A Scope Accepted

## Current canonical state

Finding 4 is accepted and canonically installed. Revision 08 is accepted as the
bounded I0A implementation-authoring scope.

- pre-scope-installation review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- Finding 4 installation commit: `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`
- accepted Finding 4 package SHA-256: `9ec22f611a1f6b8a598725e0b60b7591503fd6271ae79eb366359e7e312099f8`
- accepted I0A scope archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`

The commit containing this scope installation must be returned to Sentinel for
verification before implementation may be separately authorized.

## Required read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
3. `scope_authoring/rev23_finding4_i0a/README_FIRST.md`
4. `scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
5. `scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json`
6. `scope_authoring/rev23_finding4_i0a/accepted_scope_revision_08/README_FIRST.md`
7. the remaining accepted-scope files in their own read order
8. `authorization_audit/rev23_finding4/SENTINEL_ACCEPTANCE_DECISION_REV23_FINDING4.md`
9. `authorization_audit/rev23_finding4/AUTHORIZATION_SUPERSESSION_REV23_FINDING4.md`
10. `authorization_audit/rev23_finding4/CANONICAL_INSTALL_STATUS.md`
11. `authorization_audit/rev23_amendment_03_i0/SENTINEL_SUPERSESSION_REV23_FINDING4.md`
12. root `START_HERE.md`, then `project_context/START_HERE.md`
13. `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
14. `accepted_contract/ACCEPTED_CONTRACT_SHA256SUMS.txt`
15. `accepted_contract/SPEC_local_curl_per_side_price_dataset_verification_REV23.md`
16. `accepted_contract/SCHEMA_REGISTRY_REV23.json`
17. `accepted_contract/REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`
18. `amendment_audit/rev23_finding4/README_FIRST.md`
19. `amendment_audit/rev23_finding4/HANDOFF_SENTINEL_REV23_FINDING4.md`

## Effective contract hashes

- specification: `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`
- schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`
- request/authorization contract: `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`
- governing manifest: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- governing semantic hash: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`

## Scope status

Revision 08 is accepted. The twelve paths in its file matrix are the maximum
candidate implementation-authoring scope, not an active authorization.

No Revision 09 follows for optional polish. Reopening requires a concrete
material contradiction that cannot be resolved from Revision 08.

## Authorization boundary

No implementation prompt is active.

No source synchronization, source/test-source authoring, tests, project-code
execution, local-data read, network/curl, replay, empirical work, P1/P2/P3,
scoring, probe execution, Git publication by an agent, or gate change is
authorized.
