# REV23 Amendment 03 I0 Implementation Handoff — Active

## Purpose

This directory contains the accepted effective Revision 23 specification with Amendments 01, 02, and 03 and the active bounded I0 implementation-authoring handoff.

Gustavo explicitly authorized one Amendment 03 I0 implementation stage on `2026-07-15`. Sentinel authorizes Claude to author the exact source and unexecuted test-source files listed in `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`. No test or runtime execution is authorized.

## Read order

1. `SENTINEL_ACCEPTANCE_DECISION.md`
2. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
3. `authorization_audit/rev23_amendment_03_i0/README_FIRST.md`
4. In the canonical repository, root `START_HERE.md`, then `project_context/START_HERE.md`, then its required read order.
5. `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
6. `accepted_contract/SPEC_local_curl_per_side_price_dataset_verification_REV23.md`
7. `accepted_contract/SCHEMA_REGISTRY_REV23.json`
8. `accepted_contract/REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`
9. Relevant retained contracts/policies/vectors under `accepted_contract/contracts/` and `accepted_contract/policies/`.
10. `amendment_audit/rev23_amendment_03/SENTINEL_ACCEPTANCE_DECISION_REV23_AMENDMENT_03.md`

## Canonical implementation baseline

Claude must observe exact repository `HEAD`:

`fad41de515572ca30b4440b060a69dd6bfc57e2b`

Claude must not fetch, pull, reset, commit, push, create a branch, or open a PR. Material drift requires a stop to Sentinel.

## Contract integrity

The accepted contract is bound by `accepted_contract/ACCEPTED_CONTRACT_SHA256SUMS.txt`, `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`, and the manifest sidecar. Static hash verification is allowed.

## Active authorization

One static I0 implementation package is authorized. Source and test-source authoring are limited to the exact file matrix. Test execution, Python/project execution, local-data reads, network/curl actions, empirical artifacts, and Git publication remain prohibited.
