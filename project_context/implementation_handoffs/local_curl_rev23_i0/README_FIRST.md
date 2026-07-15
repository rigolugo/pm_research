# REV23 I0 Handoff — Amendment 03 Accepted / Implementation Not Authorized

## Purpose

This directory contains the accepted effective Revision 23 specification with Amendments 01, 02, and 03, plus its audit trail.

It does **not** currently authorize Claude implementation, correction, test-source authoring, tests, or execution.

## Read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
3. In the canonical repository, root `START_HERE.md`, then `project_context/START_HERE.md`, then its required read order.
4. `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
5. `accepted_contract/SPEC_local_curl_per_side_price_dataset_verification_REV23.md`
6. `accepted_contract/SCHEMA_REGISTRY_REV23.json`
7. `accepted_contract/REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`
8. Relevant retained contracts/policies/vectors under `accepted_contract/contracts/` and `accepted_contract/policies/`.
9. `amendment_audit/rev23_amendment_03/SENTINEL_ACCEPTANCE_DECISION_REV23_AMENDMENT_03.md`

## Canonical-install baseline

This canonical update package was prepared against private-repository commit:

`226085ca9ba7fa41a8b666005499827d6fa6b9c5`

After manual upload, the user must record the new commit. Any future implementation handoff must be regenerated and pinned to that new commit.

## Contract integrity

The accepted contract is bound by `accepted_contract/ACCEPTED_CONTRACT_SHA256SUMS.txt`, `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`, and the manifest sidecar.

## Current authorization

No active REV23 I0 implementation authorization exists. The prior Amendments-01/02 authorization and Claude prompt are superseded and must not be reused.
