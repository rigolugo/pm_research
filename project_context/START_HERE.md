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
   - `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/CHECKPOINT_INDEX.json`
   - `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/LATEST_PRESERVED_CHECKPOINT.json`
   - `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/LATEST_ACCEPTED_CHECKPOINT.json`
   - `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/README_FIRST.md`
   - `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/CHECKPOINT_MANIFEST.json`
   - `implementation_handoffs/local_curl_rev23_i0/implementation_checkpoints/REV23_FINDING4_I0A_R1_CP_0001_FCF406C4/SENTINEL_INSTALLATION_VERIFICATION.md`
24. The remaining files required by the handoff, authorization, accepted-scope, and selected checkpoint read orders.

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

### Controlling Revision 10 scope

Revision 10 is accepted, canonically installed, and Sentinel-verified at
`3d6fbe5eda504c32d94fed72be99adb9485fe1b1`.

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- accepted base: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- accepted archive SHA-256: `8a0065ecd75a3283afd3599a1d33639a7cf962d2fec1230e49c73bff07f2f202`
- accepted member count: `15`
- canonical installation base: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`
- verified installation commit: `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- immutable installed directory: `accepted_scope_revision_10/`
- implementation authorized: **NO**
- Revision 10 implementation start selected: **NO**

Revision 10 supersedes Revision 09 for the complete Finding 4 I0A specification package. Revision 09 and Revision 08 remain immutable historical accepted evidence.

The preserved `fcf406c4...` checkpoint remains unaccepted and non-authorizing. Revision 10 resolves its former T107/T153/Candidate 09 specification blockers, but provenance and implementation-conformance review remain open. Historical Revision 09 and Revision 08 implementation authorizations do not carry forward.

### Historical Revision 09 scope record

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`
- accepted archive SHA-256: `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`
- verified canonical installation commit: `c4e8b1011c51272042decac4bc89e762d767a72a`
- immutable installed directory: `accepted_scope_revision_09/`
- historical R1 checkpoint source-gated commit: `1e1afb29791f42c286b45d3b576f74926add8dce`
- historical R1 authorization carries forward: **NO**

### Historical Revision 08 scope record at installation base

Revision 08 remains immutable historical accepted evidence.

- review anchor: `88362521fe9ef247708e4d7b5f90753784b8b88e`
- accepted archive SHA-256: `004c08c02743608af71cfb84084390822893b9ee505a6f0a86a0719c219cf876`
- accepted-scope canonical commit: `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`
- historical implementation authorization carries forward: **NO**
- current source/test authoring authorization: **NONE**
- current test-execution authorization: **NONE**

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
- Recovered unreviewed R1 implementation evidence: checkpoint `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`, payload SHA-256 `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`, size `112338` bytes; canonically preserved and Sentinel-verified at commit `58acbac493840c45d84c6b7e33c583d722f4d559`, evidence-only, not accepted, and authorizes nothing.

---

## Implementation authorization state

### Controlling Revision 10 state

`STOP_IMPLEMENTATION_NOT_AUTHORIZED`

Revision 10 specification acceptance does not authorize source synchronization, source/test authoring, tests, project execution, rollback, restoration, overwrite, checkpoint promotion, data/network access, Git writes by Claude, R2, P1/P2/P3, scoring, probe execution, or gate changes.

No Revision 10 implementation starting SHA or source-gated commit is selected. The Revision 09 R1 and Revision 08 authorizations remain historical and do not carry forward.

### Historical Revision 08 authorization record at installation base

The historical Revision 08 implementation-authoring package and the later
Revision 09 R1 one-file authorization remain preserved as audit evidence. Both
are superseded and inactive under Revision 10. Neither may authorize source
synchronization, source/test authoring, rollback, restoration, overwrite,
promotion, tests, execution, data/network access, Git writes, or a downstream
stage.

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
- Preserve material unaccepted implementation progress as an evidence-only canonical checkpoint before chat/model/session transitions; never place it at the executable source path until separately accepted and authorized.
- Revision 10 is specification-only; no implementation follows without separate Gustavo authorization and Sentinel handoff.
- Do not treat the historical `8b8e9320...` start or preserved `fcf406c4...` checkpoint as a current implementation start.
