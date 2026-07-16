# REV23 Amendment 03 I0 Implementation Handoff — Source-Gated

## Purpose

This directory contains the accepted effective Revision 23 specification with Amendments 01, 02, and 03 and Gustavo's bounded I0 implementation-authoring authorization.

The authorization remains valid in principle, but implementation authoring is currently blocked on canonical source synchronization. Claude correctly returned `STOP_CANONICAL_SOURCE_UNAVAILABLE` from a clean clone at `226085ca9ba7fa41a8b666005499827d6fa6b9c5`.

## Read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
3. `authorization_audit/rev23_amendment_03_i0/README_FIRST.md`
4. `authorization_audit/rev23_amendment_03_i0/SENTINEL_CANONICAL_SOURCE_GATE_CORRECTION.md`
5. `authorization_audit/rev23_amendment_03_i0/SOURCE_SYNC_AUTHORIZATION_STATUS.md`
6. In the canonical repository, root `START_HERE.md`, then `project_context/START_HERE.md`, then its required read order.
7. `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
8. `accepted_contract/SPEC_local_curl_per_side_price_dataset_verification_REV23.md`
9. `accepted_contract/SCHEMA_REGISTRY_REV23.json`
10. `accepted_contract/REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`
11. Relevant retained contracts/policies/vectors under `accepted_contract/contracts/` and `accepted_contract/policies/`.
12. `amendment_audit/rev23_amendment_03/SENTINEL_ACCEPTANCE_DECISION_REV23_AMENDMENT_03.md`

## Commit roles

- Accepted-contract commit: `fad41de515572ca30b4440b060a69dd6bfc57e2b`.
- First canonical authorization-anchor commit: `d737aa9e12cbfa584b275e128c8624e01af72f61`.
- Actual implementation baseline: the verified synchronized local `HEAD` recorded by Claude after a separately authorized source synchronization.

The accepted-contract commit and authorization-anchor commit are intentionally different. Do not require the working tree to be checked out at `fad41de515572ca30b4440b060a69dd6bfc57e2b`, because that commit does not contain the active authorization records.

## Corrected canonical source gate

Before authoring any file, all of the following must hold:

1. source synchronization has been separately and explicitly authorized by Gustavo;
2. local `HEAD` is `d737aa9e12cbfa584b275e128c8624e01af72f61` or a descendant;
3. `d737aa9e12cbfa584b275e128c8624e01af72f61` is present in local history and is an ancestor of local `HEAD`;
4. every accepted-contract byte and hash matches the registered Amendment 03 values;
5. changes from `d737aa9e12cbfa584b275e128c8624e01af72f61` to local `HEAD` do not touch `accepted_contract/`, `pm_research/`, `tests/`, dependency files, CLI files, or runtime configuration;
6. every authorized new source/test-source path is absent before authoring;
7. the working tree is clean before authoring.

Any failure requires a stop to Sentinel.

## Current source-sync status

No fetch, pull, reset, checkout/switch, re-clone, remote update, or equivalent source synchronization is authorized by this handoff. A separate Gustavo authorization is required. Until then, Claude must not author implementation or test-source files.

## Contract integrity

The accepted contract is bound by `accepted_contract/ACCEPTED_CONTRACT_SHA256SUMS.txt`, `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`, and the manifest sidecar. Static hash verification is allowed only after canonical source is available.

## Active implementation boundary

After the source gate passes, one static I0 implementation package is authorized. Source and test-source authoring remain limited to the exact file matrix. Test execution, Python/project execution, local-data reads, network/curl actions, empirical artifacts, and Git publication remain prohibited.
