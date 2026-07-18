# START HERE

*First file to read in every new project chat.*

---

## Rule 0 — canonical source

The private GitHub repository is authoritative:

`rigolugo/pm_research`

Old chats, memory, uploaded duplicates, archived files, and the public context
mirror are non-authoritative. If they conflict with the private repository, the
private repository wins.

The public mirror `rigolugo/pm_research_context` is context-only.

---

## Required read order

Read these before doing anything:

1. `GUARDRAILS.md`
2. `PROJECT_STATE.md`
3. `DECISION_LOG.md`
4. `CLOSED_FINDINGS.md`
5. `ARTIFACT_INDEX.md`
6. `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`
7. `DATA_CONTRACTS_named_binary_probe.md`
8. `PRICE_INPUT_CONTRACT_named_binary_probe.md`
9. `SPEC_named_binary_probe.md`
10. The accepted price-source specifications and result handoffs relevant to the task.
11. `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`
12. `implementation_handoffs/local_curl_rev23_i0/SENTINEL_ACCEPTANCE_DECISION.md`
13. `implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
14. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/README_FIRST.md`
15. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/SENTINEL_IMPLEMENTATION_AUTHORIZATION.md`
16. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/AUTHORIZATION_MANIFEST.json`
17. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/AUTHORIZED_FILE_MATRIX.md`
18. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/ACTIVITY_BOUNDARIES.md`
19. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/SOURCE_GATE.md`
20. `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/README_FIRST.md`
21. `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/accepted_scope_revision_08/README_FIRST.md`
22. `implementation_handoffs/local_curl_rev23_i0/accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
23. The remaining files required by the handoff, authorization, and accepted-scope read orders.

---

## Current canonical contract

Revision 23 with Amendments 01–03 and accepted Finding 4 is the governing
SPEC-ONLY contract.

Finding 4 canonical installation was completed through the linear commit sequence:

- `3f8cc54dc12a5335472f00f5ffcf5c0d56d8d1ba`
- `c394b9ab5eb5dc07f8d716818e02507994ce41d7`
- `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Authorized installation base:

`f6cb60df66c2bbcdfb6d797119ed25ad79e06a11`

Finding 4 installation commit:

`e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Effective hashes:

- governing specification: `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`
- schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`
- request-plan and authorization contract: `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`
- governing-package manifest: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- governing-package semantic SHA-256: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`
- accepted-contract checksum inventory: `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`

The installed contract and Finding 4 audit trail live under:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

---

## Accepted Finding 4 I0A scope

Revision 08 is accepted as the bounded implementation-authoring scope.

- review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- accepted archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- canonical scope path:
  `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/`
- accepted-scope canonical commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff` — Sentinel verified
- implementation-source authoring: **AUTHORIZED AFTER AUTHORIZATION-PACKAGE INSTALL VERIFICATION**
- unexecuted test-source authoring: **AUTHORIZED AFTER AUTHORIZATION-PACKAGE INSTALL VERIFICATION**
- test execution: **UNAUTHORIZED**

Gustavo authorized the bounded authoring stage on `2026-07-18`. The active package is
`implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/`.
No Revision 09 is required.

---

## Current project state

- P0 preflight: **ACCEPTED — `P0_CLEAR`**.
- P0 representativeness audit: **ACCEPTED — `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`**.
- P1 feature assembly: **BLOCKED** on an accepted per-side/token-identity decision-time price source.
- P2, P3, scoring, and probe execution: **UNAUTHORIZED**.
- `named_binary_probe_blocked = true`.
- `yes_price`, `1 - price`, and `1 - yes_price` must not be used to synthesize named-binary sides.
- S1 CLOB `/prices-history`: `S1_SOURCE_NOT_VIABLE`.
- S1-ALT local trade prints: `S1ALT_SOURCE_NOT_VIABLE`.
- Option B corrected B0: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`; B1 unauthorized.
- Option C: mixed/incomplete evidence; `C1F2_ARTIFACTS_INSUFFICIENT`; C1B/C2 unauthorized.
- Option D temporal precheck: accepted; PMXT v2 deprioritized for broad P0 coverage; Telonex L2 may only proceed through a separately authorized SPEC-ONLY vendor-coverage review.

---

## Implementation authorization state

A bounded Claude implementation-authoring prompt is installed but becomes active
only after Sentinel verifies the canonical commit containing the authorization
package.

The earlier Amendment 03 I0 authorization remains superseded. Current Gustavo
and Sentinel authorization permits read-only source synchronization and authoring
of exactly six source plus six unexecuted test-source paths. Tests, project
imports/execution, research-data reads, general network/API/curl, empirical work,
Git history/remote writes, P1/P2/P3, scoring, probe execution, and gate changes
remain unauthorized.

The next boundary is manual installation and Sentinel verification of the active
authorization package. After that verification Claude may author under the exact
source gate; no test execution follows automatically.

---

## Working discipline

- Verify exact paths, bytes, hashes, schemas, and authorization boundaries.
- Passing tests do not prove correctness when tests encode the wrong contract.
- Specification acceptance does not authorize implementation.
- Implementation acceptance does not authorize tests or execution.
- Canonical project-document changes are prepared by ChatGPT as complete files
  and uploaded manually by Gustavo.
- Claude must not edit canonical project-context files.
- Never silently reverse a settled decision or reactivate superseded material.
- Do not open Revision 09 for optional polish; reopen only for a concrete material contradiction.
