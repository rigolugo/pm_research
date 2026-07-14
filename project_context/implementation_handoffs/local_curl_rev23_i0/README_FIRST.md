# REV23 I0 Claude Implementation Handoff

## Purpose

This handoff authorizes Claude to produce one narrowly scoped, pure implementation package for the accepted local-curl per-side verification contract. It does not authorize execution.

## Read order

1. `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
2. `prompts/CLAUDE_NEW_CHAT_PROMPT.md`
3. In the canonical repository, read root `START_HERE.md`, then `project_context/START_HERE.md`, then its required read order.
4. `accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
5. `accepted_contract/SPEC_local_curl_per_side_price_dataset_verification_REV23.md`
6. `accepted_contract/SCHEMA_REGISTRY_REV23.json`
7. `accepted_contract/REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`
8. Relevant retained contracts/policies/vectors under `accepted_contract/contracts/` and `accepted_contract/policies/`.

## Repository baseline

At handoff creation, canonical `rigolugo/pm_research` main HEAD was:

`67af34d1e44504b8cde848b71117bd88de827e29`

Claude must record its actual local `git rev-parse HEAD`. It must not fetch, pull, reset, or rewrite history. Material interface drift must be returned to Sentinel.

## Contract integrity

Run no tests or scripts. Static file hashing of the supplied handoff and source files is allowed. `accepted_contract/ACCEPTED_CONTRACT_SHA256SUMS.txt` and root `HANDOFF_SHA256SUMS.txt` provide integrity checks.

## Chat names

- Claude: **Implement REV23 I0 Contract Core**
- Sentinel: **Review REV23 I0 Implementation**
