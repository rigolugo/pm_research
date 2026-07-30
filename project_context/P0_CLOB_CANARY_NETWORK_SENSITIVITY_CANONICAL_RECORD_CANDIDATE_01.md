# P0 CLOB Canary Network Sensitivity — Canonical Record — Candidate 01

## 1. Status

| Field | Value |
|---|---|
| Candidate ID | `P0_CLOB_CANARY_NETWORK_SENSITIVITY_CANONICAL_UPDATE_CANDIDATE_01` |
| Record ID | `P0_CLOB_CANARY_NETWORK_SENSITIVITY_CANONICAL_RECORD_CANDIDATE_01` |
| Authoring mode | `MATERIALIZE` |
| Status | `DOCUMENTATION_ONLY_CANONICAL_UPDATE_REVIEW_CANDIDATE` |
| Prepared by | Professor |
| Independent reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Canonical branch | `main` |
| Expected and observed canonical commit | `e675a47ec2c8f6cd769c2673afc16d96e5622ccd` |
| Canonical comparison | `IDENTICAL`; ahead `0`; behind `0` |
| Authorization effect | `NONE` |

This record materializes accepted P0 CLOB `/prices-history` dry-run and canary evidence, the accepted network/environment sensitivity finding, and the accepted Candidate 02 failure-characterization design. It does not rerun, reprocess, or expand the empirical work.

**Checkable completion sentence:** Sentinel can verify that the exact dry-run and two 100-request canary counts, the bounded network-sensitivity conclusion, the `100 / 37,248` limitation, and every preserved non-authorization are recorded consistently in the five proposed canonical files.

## 2. Purpose

The purpose is to make the accepted P0 CLOB canary state available to future canonical chats without:

- accepting P0-scale source viability;
- building or accepting an S2 price artifact;
- unblocking P1;
- authorizing implementation source, tests, local-data access, network activity, a full diagnostic, or Git writes;
- changing any probe or gate state.

## 3. Canonical base and source classification

### 3.1 Canonical controls

The following are `CANONICAL` at `e675a47ec2c8f6cd769c2673afc16d96e5622ccd`:

- `project_context/GUARDRAILS.md`;
- `project_context/PROJECT_STATE.md`;
- `project_context/DECISION_LOG.md`;
- `project_context/CLOSED_FINDINGS.md`;
- `project_context/ARTIFACT_INDEX.md`;
- `project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`;
- `project_context/DATA_CONTRACTS_named_binary_probe.md`;
- `project_context/PRICE_INPUT_CONTRACT_named_binary_probe.md`;
- `project_context/SPEC_named_binary_probe.md`;
- the accepted S1 and S2 documentation layers identified by `project_context/START_HERE.md`.

These controls establish, among other things:

- final P0 eligible universe `39,693`;
- P1 blocked on an accepted per-side/token-identity decision-time price artifact;
- P2/P3, scoring, and probe execution unauthorized;
- `named_binary_probe_blocked = true`;
- `yes_price`, `1 - price`, `1 - yes_price`, and complement synthesis prohibited as named-binary unblock paths;
- specification acceptance does not authorize implementation or execution.

### 3.2 Evidence being memorialized

The exact dry-run and canary results below are `SUBMITTED_ACCEPTED_EVIDENCE` for canonical memorialization. This candidate does not recreate empirical evidence and does not represent the canary script or raw outputs as canonically installed.

The network/environment sensitivity conclusion and Candidate 02 specification-only acceptance are `SUBMITTED_SETTLED_DECISIONS` for Sentinel verification in this canonical update review.

## 4. In scope

This candidate records:

1. exact dry-run reconciliation;
2. exact first 100-request canary results;
3. exact repeat 100-request canary results on a new network;
4. the bounded network/environment sensitivity finding;
5. the explicit limitation that P0-scale source viability remains not established;
6. Candidate 02 failure-characterization design acceptance as SPEC-only;
7. authorization effect `NONE`;
8. complete replacement text for the four canonical control files;
9. one new canonical record.

## 5. Out of scope

This candidate MUST NOT:

- add or install the canary script;
- add or install a Store shim;
- add raw requests, responses, logs, archives, or output directories;
- add local data or parquet artifacts;
- edit `.gitignore`;
- author implementation source or test source;
- execute tests, imports, compilation, lint, typing, coverage, or project code;
- read local research data;
- use network/API/RPC/vendor/Dune/curl/endpoint access;
- save raw responses;
- perform a full diagnostic;
- construct or accept an S2 artifact;
- continue P1, P2, or P3;
- score or execute a probe;
- change a gate or `named_binary_probe_blocked`;
- perform any Git write or canonical installation.

## 6. Preserved project state

The following MUST remain unchanged:

| State | Required value |
|---|---|
| Final P0 eligible | `39,693` |
| P1 | `BLOCKED` |
| P2 | `UNAUTHORIZED` |
| P3 | `UNAUTHORIZED` |
| scoring | `UNAUTHORIZED` |
| probe execution | `UNAUTHORIZED` |
| `named_binary_probe_blocked` | `true` |
| accepted per-token price artifact | `NONE` |
| S2 artifact construction | `NOT AUTHORIZED` |
| gate changes | `NOT AUTHORIZED` |

The following synthesis paths remain prohibited:

- `yes_price`;
- `1 - price`;
- `1 - yes_price`;
- `1 - p`;
- any complement-derived reconstruction of one token side from the other.

## 7. Accepted dry-run evidence

| Field | Accepted value |
|---|---:|
| `final_p0_rows_loaded` | `39,693` |
| `token_pair_clear_conditions` | `39,693` |
| `request_eligible_conditions` | `18,624` |
| `request_eligible_token_sides` | `37,248` |
| `INVALID_DECISION_WINDOW` | `21,069` |
| `REQUEST_ELIGIBLE` | `18,624` |
| `executed_requests` | `0` |

Required reconciliations:

- `INVALID_DECISION_WINDOW + REQUEST_ELIGIBLE = final_p0_rows_loaded`;
- `21,069 + 18,624 = 39,693`;
- `request_eligible_token_sides = request_eligible_conditions × 2`;
- `37,248 = 18,624 × 2`.

The dry-run executed no network requests and created no source-viability finding.

## 8. Accepted first 100-request canary

### 8.1 Identity

| Field | Value |
|---|---|
| Script SHA-256 | `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00` |
| Script installed by this package | `NO` |
| Raw outputs installed by this package | `NO` |

### 8.2 Results

| Field | Count |
|---|---:|
| `executed_requests` | `100` |
| HTTP 200 | `17` |
| HTTP 500 | `73` |
| HTTP NONE | `10` |
| `TRANSPORT_OK` | `17` |
| `TRANSPORT_HTTP_ERROR` | `73` |
| `TRANSPORT_CONNECTION_ERROR` | `9` |
| `TRANSPORT_TIMEOUT` | `1` |
| `SERIES_PRESENT` | `17` |
| `in_window_present_sides` | `17` |
| `condition_both_sides_present` | `0` |

Required reconciliations:

- `17 + 73 + 10 = 100`;
- `17 + 73 + 9 + 1 = 100`.

Disposition:

`SOURCE_VIABILITY_NOT_ESTABLISHED`

The first canary MUST NOT be interpreted as proof that the route is dead because the repeat canary materially changed the transport outcome under a new network.

## 9. Accepted repeat 100-request canary on a new network

### 9.1 Identity and base verification

| Field | Value |
|---|---|
| `canonical_base_verified` | `true` |
| Canonical commit | `e675a47ec2c8f6cd769c2673afc16d96e5622ccd` |
| Script SHA-256 | `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00` |

### 9.2 Results

| Field | Count |
|---|---:|
| `executed_requests` | `100` |
| HTTP 200 | `100` |
| `TRANSPORT_OK` | `100` |
| `SERIES_PRESENT` | `100` |
| `IN_WINDOW_PRESENT` | `100` |
| `condition_both_sides_present` | `50` |
| `error_response_count` | `0` |
| `malformed_response_count` | `0` |

The repeat canary used the same script identity and exact canonical base recorded above.

## 10. Accepted finding

The accepted finding is bounded to the following statements:

1. The repeat canary supports network/environment sensitivity of the first failure pattern.
2. The CLOB `/prices-history` route is not dead.
3. P0-scale source viability remains `NOT ESTABLISHED`.
4. Only `100 / 37,248` request-eligible token sides were tested.
5. The repeat canary does not establish full-universe coverage, transport stability across environments, long-run rate behavior, raw-evidence closure, deterministic resumability, or S2 artifact acceptability.
6. No full diagnostic is authorized.

No stronger conclusion is permitted from this record.

## 11. Candidate 02 failure-characterization design

The Candidate 02 failure-characterization design is accepted as SPEC-only.

| Question | State |
|---|---|
| Design acceptance | `ACCEPTED SPEC-ONLY` |
| Authorization effect | `NONE` |
| Implementation-source authoring | `UNAUTHORIZED` |
| Test-source authoring | `UNAUTHORIZED` |
| Tests | `UNAUTHORIZED` |
| Imports/project execution | `UNAUTHORIZED` |
| Local-data reads | `UNAUTHORIZED` |
| Network execution | `UNAUTHORIZED` |
| Raw-save activity | `UNAUTHORIZED` |
| Full diagnostic | `UNAUTHORIZED` |
| Git writes | `UNAUTHORIZED` |

This record does not install the Candidate 02 design text or convert it into an implementation contract.

### 11.1 Exact-identity limitation

The exact Candidate 02 document path, byte length, SHA-256, and review-record identity were not supplied as canonical inputs to this authoring task. They MUST NOT be invented.

This candidate therefore records only:

- the submitted settled status `ACCEPTED SPEC-ONLY`;
- authorization effect `NONE`;
- the unchanged prohibition on implementation-source authoring and execution.

A later identity-bearing canonical record requires the exact accepted Candidate 02 bytes and Sentinel review identity. Absence of those identities MUST NOT be used as a false authorization path.

## 12. False-unblock prohibitions

The following conclusions MUST NOT be drawn:

- `100 / 100` success on the repeat canary means P0-scale source viability is established;
- network sensitivity means the first canary can be discarded;
- a live route means an accepted S2 artifact can be built;
- `condition_both_sides_present = 50` authorizes wider acquisition;
- the repeat canary authorizes raw-output preservation or a full diagnostic;
- specification-only acceptance authorizes source or test authoring;
- documentation installation unblocks P1;
- either canary changes `named_binary_probe_blocked`;
- either canary permits side synthesis or winner-based token enumeration.

## 13. Proposed canonical file set

Complete replacements:

1. `project_context/START_HERE.md`;
2. `project_context/PROJECT_STATE.md`;
3. `project_context/DECISION_LOG.md`;
4. `project_context/ARTIFACT_INDEX.md`.

New canonical record:

5. `project_context/P0_CLOB_CANARY_NETWORK_SENSITIVITY_CANONICAL_RECORD_CANDIDATE_01.md`.

No other repository path is proposed.

## 14. Acceptance evidence

Sentinel SHOULD verify:

1. canonical `main` is exactly `e675a47ec2c8f6cd769c2673afc16d96e5622ccd`;
2. the package changes only the five canonical paths in §13;
3. dry-run counts and arithmetic reconcile;
4. first-canary HTTP and transport counts each reconcile to `100`;
5. repeat-canary counts match the accepted evidence;
6. the script SHA-256 is identical in both canary sections;
7. `100 / 37,248` is preserved as the tested-scope limitation;
8. source viability remains `NOT ESTABLISHED`;
9. P0 remains `39,693`;
10. P1 remains blocked;
11. P2/P3, scoring, and probe execution remain unauthorized;
12. no synthesis path is reopened;
13. Candidate 02 authorization effect remains `NONE`;
14. no script, shim, raw output, local data, parquet, or `.gitignore` change is included;
15. the read-order path to the installed S1 Candidate 02 record is corrected from the nonexistent Candidate 05 path without changing S1 substance.

## 15. Alternative design considered

The strongest narrower alternative was to add only this record and one `START_HERE.md` pointer, leaving `PROJECT_STATE.md`, `DECISION_LOG.md`, and `ARTIFACT_INDEX.md` unchanged.

That alternative was not selected because it would leave the accepted current state absent from the three canonical control surfaces future chats are required to read for active state, settled decisions, and artifact identity. The selected five-file canonical set is the smallest set that records the same bounded finding consistently across those authority domains.

## 16. Authorization statement

This record and package authorize no implementation-source authoring, test-source authoring, test execution, imports, project execution, compilation, linting, type checking, coverage, local research-data reads, network/API/RPC/vendor/Dune/curl/endpoint activity, raw-response saving, Store-shim authoring, full diagnostic, dependency or packaging change, acquisition, construction, alignment, rebuild, audit, transition, empirical work, S2 artifact construction, P1/P2/P3, scoring, probe execution, gate changes, branch, commit, push, merge, tag, release, ref update, or canonical installation itself.

Implementation-source installation remains a separate later decision requiring exact Gustavo authorization and Sentinel review/authorization.

## 17. Requested Sentinel decision

`APPROVE`

Approval would accept this bounded documentation-only canonical update candidate for later manual installation review. It would not authorize implementation, execution, networking, tests, empirical work, or Git activity.
