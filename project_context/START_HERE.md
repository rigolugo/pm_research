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
    For S1 CLOB `/prices-history`, read in this order without omitting the
    historical method-qualified negative:
    - `SPEC_price_source_s1_coverage.md`
    - `HANDOFF_orchestrator_price_source_s1_pass1_IMPLEMENTATION.md`
    - `HANDOFF_orchestrator_s1_pass1_parse_ts_patch.md`
    - `HANDOFF_orchestrator_s1_pass1_nan_and_progress_patch.md`
    - `HANDOFF_orchestrator_s1_pass1_request_window_fix.md`
    - `HANDOFF_orchestrator_s1_pass1_request_window_diagnostics.md`
    - `HANDOFF_orchestrator_s1_pass1_invalid_decision_window.md`
    - `HANDOFF_orchestrator_s1_parse_ts_millisecond_utc.md`
    - `HANDOFF_orchestrator_s1_pass1_RESULT.md`
    - `S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02.md`
    For the accepted P0 CLOB canary evidence and network-sensitivity finding, read:
    - `P0_CLOB_CANARY_NETWORK_SENSITIVITY_CANONICAL_RECORD_CANDIDATE_01.md`
    For the accepted S2 per-token price-artifact specification layer, read:
    - `S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md`
    - `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md`
    - `HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md`
    - `../nodes/K010/artifact.json`
    - `../nodes/K011/artifact.json`
    - `S2_CANDIDATE_08_CANONICAL_INSTALLATION_PACKAGE_MANIFEST_01.json`
    - `S2_CANDIDATE_08_CANONICAL_INSTALLATION_PACKAGE_SHA256SUMS_01.txt`
    - `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01_CANONICAL_INSTALLATION_RECORD.md`
    - `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`
11. `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`
12. `implementation_handoffs/local_curl_rev23_i0/SENTINEL_ACCEPTANCE_DECISION.md`
13. `implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
14. Historical Revision 08 authorization evidence: `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/README_FIRST.md`
15. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/SENTINEL_IMPLEMENTATION_AUTHORIZATION.md`
16. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/AUTHORIZATION_MANIFEST.json`
17. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/AUTHORIZED_FILE_MATRIX.md`
18. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/ACTIVITY_BOUNDARIES.md`
19. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a/SOURCE_GATE.md`
    Historical Revision 09 R1 authorization evidence — does not carry forward:
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/README_FIRST.md`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/SENTINEL_AUTHORIZATION_DECISION.md`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/SENTINEL_ACTIVATION_VERIFICATION.md`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/AUTHORIZATION_MANIFEST.json`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/AUTHORIZED_FILE_MATRIX.md`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/ACTIVITY_BOUNDARIES.md`
    - `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/SOURCE_GATE.md`
20. `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/README_FIRST.md`
    Revision 10 controlling insert, before historical revisions:
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION.md`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_INSTALLATION_VERIFICATION_REVISION_10.md`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST.json`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/accepted_scope_revision_10/README_FIRST.md`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION_REVISION_09.md`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST_REVISION_09.json`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/accepted_scope_revision_09/README_FIRST.md`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/SENTINEL_SCOPE_ACCEPTANCE_DECISION_REVISION_08.md`
    - `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/ACCEPTED_SCOPE_MANIFEST_REVISION_08.json`
21. `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/accepted_scope_revision_08/README_FIRST.md`
22. `implementation_handoffs/local_curl_rev23_i0/accepted_contract/GOVERNING_PACKAGE_MANIFEST_REV23.json`
23. `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/README_FIRST.md`
24. `implementation_handoffs/local_curl_rev23_i0/remediation_scope/README_FIRST.md`
25. `implementation_handoffs/local_curl_rev23_i0/provenance_audit/rev23_finding4_i0a_current_twelve_path_worktree_capture_01/README_FIRST.md`
26. `implementation_handoffs/local_curl_rev23_i0/scope_authoring/rev23_finding4_i0a/starting_state_amendment_revision_10/README_FIRST.md`
27. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_candidate04_workspace_preparation_01/README_FIRST.md`
28. `implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision10_remediation_source_01/README_FIRST.md`
29. The remaining files required by the handoff, authorization, accepted-scope, selected-checkpoint, remediation-scope, provenance-capture, accepted starting-state amendment, and accepted Candidate 05 workspace-preparation package read orders.

---

## Current S2 Candidate 08 amendment state

S2 Candidate 08 Implementation-Source Amendment 01 is accepted as a SPEC-only amendment after this documentation-only installation. Exact installed amendment identity:

- path: `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md`;
- byte length: `24599`;
- SHA-256: `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63`;
- Sentinel decision: `APPROVE — S2 Candidate 08 Implementation-Source Amendment 01 accepted as a SPEC-only amendment`;
- authorization effect: `NONE`.

It resolves only the package-layout/path-boundary defect, registry-provenance ambiguity, K015 ordering ambiguity, K016 self-identity ambiguity, and incorrect Appendix-A matrix citation.

Future implementation-source authoring remains unauthorized and requires:

`K011 + accepted installed amendment → fresh K013 → fresh K012 → fresh K014 → K015/K016`

Selected future package: `pm_research.named_binary_probe_s2`.
Selected future repository directory: `pm_research/named_binary_probe_s2/`.
Future matrix: exactly fourteen files under that directory.
Forbidden for this stage: `src/` layout, namespace package behavior, `pyproject.toml` changes.
K016 `/payload/self_identity = null`.

---

## Current canonical contract

Revision 23 with Amendments 01–03 and accepted Finding 4 is the governing SPEC-ONLY contract. The installed contract and Finding 4 audit trail live under:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

---

## Current project state

- P0 preflight: **ACCEPTED — `P0_CLEAR`**.
- P0 representativeness audit: **ACCEPTED — `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`**.
- P1 feature assembly: **BLOCKED** on an accepted per-side/token-identity decision-time price source.
- P2, P3, scoring, and probe execution: **UNAUTHORIZED**.
- `named_binary_probe_blocked = true`.
- `yes_price`, `1 - price`, and `1 - yes_price` must not be used to synthesize named-binary sides.
- S1 CLOB `/prices-history`: historical `interval=max`, fidelity-omitted method: `S1_SOURCE_NOT_VIABLE`; revised `fidelity=1`, interval-omitted method: `S1_SOURCE_VIABLE` only for the existing stratified Pass-1 sample and reviewed EC2 route. This is not full-universe validation; no price artifact is accepted.
- P0 CLOB `/prices-history` dry-run and two bounded 100-request canaries: **ACCEPTED EVIDENCE**. The repeat canary supports network/environment sensitivity of the first failure pattern and shows the route is not dead. P0-scale source viability remains **NOT ESTABLISHED** because only `100 / 37,248` request-eligible token sides were tested.
- P0 CLOB Candidate 02 failure-characterization design: **ACCEPTED SPEC-ONLY**; authorization effect `NONE`. Implementation-source authoring, tests, imports, local-data reads, networking, raw-save activity, a full diagnostic, and Git writes remain unauthorized.
- S2 per-token price-artifact Candidate 08: **ACCEPTED SPECIFICATION** through K010/K011; no implementation source exists or is accepted; implementation authorization is `NONE`.
- S2 Candidate 08 Implementation-Source Amendment 01: **ACCEPTED SPEC-ONLY AMENDMENT** after installation of this package; authorization effect `NONE`.
- Recovered R1 checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` remains exact, evidence-only, `NOT_ACCEPTED`, and non-authorizing.
- Static checkpoint conformance: **BLOCKED — `REVISION10_STATIC_CONFORMANCE_BLOCKED`**.

---

## Working discipline

- Verify exact paths, bytes, hashes, schemas, and authorization boundaries.
- Passing tests do not prove correctness when tests encode the wrong contract.
- Specification acceptance does not authorize implementation.
- Implementation acceptance does not authorize tests or execution.
- Canonical project-document changes are prepared as complete files and uploaded manually by Gustavo.
- Claude must not edit canonical project-context files.
- Never silently reverse a settled decision or reactivate superseded material.
- Revision 10 and S2 Candidate 08 remain specification-only until separate Gustavo authorization and Sentinel handoff.
