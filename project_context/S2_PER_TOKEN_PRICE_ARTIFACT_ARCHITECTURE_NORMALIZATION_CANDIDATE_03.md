# S2 Per-Token Price-Artifact Architecture Normalization — Candidate 03

## 0. Status, purpose, canonical base, and requested decision

| Field | Value |
|---|---|
| Document ID | `S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03` |
| Status | `ARCHITECTURE_REVIEW_CANDIDATE` |
| Authoring mode | `EXPLORE_AND_NORMALIZE`; not an executable specification |
| Correction relation | Narrow correction to blocked Architecture Normalization Candidate 02 |
| Canonical repository | `rigolugo/pm_research` |
| Expected and observed `main` | `794fb60d8604e7f40d02bb0371aca55fef4ec7ec` |
| Canonical comparison | `IDENTICAL`; ahead `0`, behind `0` |
| Reviewer / decision owner | Sentinel |
| Requested Sentinel decision | `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` |
| Authorization effect | `NONE` |

**Purpose.** Preserve Candidate 02’s accepted architecture direction while correcting the missing Sentinel stage-authorization layer, separating deterministic scientific identity from activity provenance, making global and condition reducers total, representing alignment-policy absence without a phantom candidate, and closing all nineteen audit-evidence dependency sets.

**Checkable completion sentence.** This candidate is complete when Sentinel can verify that no activity can start without both an exact prerequisite Sentinel acceptance plus narrow-stage authorization and an exact Gustavo authorization, original and rebuilt scientific bytes share one activity-free `deterministic_build_id`, every legal global and per-condition vector has one result, every audit check has a closed evidence set, and the complete declared graph is acyclic and equal to its identity/evidence-implied edges.

### 0.1 Source precedence and fixed constraints

Canonical repository state at the exact commit controls. Architecture Candidates 01–02 and their block findings are `SUBMITTED`, noncanonical correction inputs. This document preserves: research-only purpose; no trading; `U0=39,693` with `UP_DOWN=22,012`, `OVER_UNDER=1,003`, `NAMED_OTHER=16,678`; independent token-specific acquisition; no complement synthesis, `1-price`, `1-yes_price`, or winner-conditioned enumeration; historical `interval=max`/fidelity-omitted `S1_SOURCE_NOT_VIABLE`; revised `fidelity=1`/interval-omitted `S1_SOURCE_VIABLE` only for the reviewed 248-condition Pass-1 sample and EC2 route; no full-universe validation; no accepted price artifact; P1 blocked; and `named_binary_probe_blocked=true`.

### 0.2 In scope and out of scope

In scope is architecture normalization only. Out of scope are Candidate 08 drafting, executable schemas, code, tests, fixtures, implementation handoffs, package files, checksums, canonical replacements, research-data access, preflight, network activity, acquisition, construction, alignment, rebuild, audit, transition execution, P1/P2/P3, scoring, probe execution, canonical changes, and Git actions.

---

## 1. Decision-bearing question and load-bearing unknowns

**Question:** What exact evidence, state transitions, dual-control authorizations, deterministic identities, and review decisions are required to produce a reproducible per-token decision-time price artifact without falsely unblocking P1?

| Class | Item | Architectural treatment |
|---|---|---|
| `CANONICAL` | P0 universe, subclass counts, two-side identity requirement, P1/probe blocks | fixed and never silently reduced |
| `SETTLED` | independent token requests; no synthesis; no outcome-conditioned pair enumeration | mandatory invariant |
| `OPEN` | full-universe endpoint behavior and safe span | separately authorized S5/S6 evidence |
| `OPEN` | alignment selector and numeric bounds | real policy candidate plus Sentinel review; absence is separately evidenced |
| `OPEN` | artifact coverage and deterministic equality | separately authorized S7/S8B evidence |
| `OPEN` | exact consumer-eligible subset | only after exact clear, S9 approval, and dual-controlled S10 |

The load-bearing architecture unknown is whether one dual-controlled, immutable, independently rebuilt and audited process can preserve every condition disposition while producing a scientifically identical original/rebuild chain. No open empirical value is selected here.

---

## 2. Total state model: global `G`, processing `P(c)`, transition `T(c)`

The layers are independent. A condition may be final for processing while the global run continues through audit, review, and transition reconciliation. `HALTED` and `COMPLETE` are global only; no per-condition state can advance or halt `G` by itself.

### 2.1 Global vector and total reducer

`G=(phase, phase_status, review_disposition, halt_code)`

- `phase_status∈{NOT_STARTED,IN_PROGRESS,COMPLETE,INCOMPLETE,BLOCKED}` exactly.
- `review_disposition∈{NOT_APPLICABLE,PENDING,APPROVE,ACCEPT_FINDING,BLOCK,DEFER,NEEDS_VERIFICATION}`.
- `halt_code` is null unless `phase=HALTED`; a halted state has exactly one typed code.
- A positive review never starts the next activity. It leaves the completed review phase waiting until the next activity root proves both control records.

| Phase | `NOT_STARTED` | `IN_PROGRESS` | `COMPLETE` | `INCOMPLETE` | `BLOCKED` |
|---|---|---|---|---|---|
| `ARCHITECTURE_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | APPROVE normalization; wait for K005+K006+K007; successor `SPEC_DRAFTING` only under its stated guard | `HALTED::ARCHITECTURE_REVIEW::INCOMPLETE` | `HALTED::ARCHITECTURE_REVIEW::BLOCKED` |
| `SPEC_DRAFTING` | stay; no activity/root | stay; exact submission or dual-controlled root required | K008+K009 emitted; successor `SPEC_REVIEW` only under its stated guard | `HALTED::SPEC_DRAFTING::INCOMPLETE` | `HALTED::SPEC_DRAFTING::BLOCKED` |
| `SPEC_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | APPROVE Candidate 08; wait for K012+K013+K014; successor `IMPLEMENTATION_SOURCE` only under its stated guard | `HALTED::SPEC_REVIEW::INCOMPLETE` | `HALTED::SPEC_REVIEW::BLOCKED` |
| `IMPLEMENTATION_SOURCE` | stay; no activity/root | stay; exact submission or dual-controlled root required | K015+K016 emitted; successor `SOURCE_REVIEW` only under its stated guard | `HALTED::IMPLEMENTATION_SOURCE::INCOMPLETE` | `HALTED::IMPLEMENTATION_SOURCE::BLOCKED` |
| `SOURCE_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K018; wait for K019+K020+K021; successor `TEST_AUTHORING` only under its stated guard | `HALTED::SOURCE_REVIEW::INCOMPLETE` | `HALTED::SOURCE_REVIEW::BLOCKED` |
| `TEST_AUTHORING` | stay; no activity/root | stay; exact submission or dual-controlled root required | K022+K023 emitted; successor `TEST_REVIEW` only under its stated guard | `HALTED::TEST_AUTHORING::INCOMPLETE` | `HALTED::TEST_AUTHORING::BLOCKED` |
| `TEST_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K025; wait for K026+K027+K028; successor `TEST_EXECUTION` only under its stated guard | `HALTED::TEST_REVIEW::INCOMPLETE` | `HALTED::TEST_REVIEW::BLOCKED` |
| `TEST_EXECUTION` | stay; no activity/root | stay; exact submission or dual-controlled root required | K029+K030 emitted; successor `TEST_RESULT_REVIEW` only under its stated guard | `HALTED::TEST_EXECUTION::INCOMPLETE` | `HALTED::TEST_EXECUTION::BLOCKED` |
| `TEST_RESULT_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K032; wait for K033+K034+K035; successor `S4_PREPARATION` only under its stated guard | `HALTED::TEST_RESULT_REVIEW::INCOMPLETE` | `HALTED::TEST_RESULT_REVIEW::BLOCKED` |
| `S4_PREPARATION` | stay; no activity/root | stay; exact submission or dual-controlled root required | K036–K039 emitted; successor `S4_REVIEW` only under its stated guard | `HALTED::S4_PREPARATION::INCOMPLETE` | `HALTED::S4_PREPARATION::BLOCKED` |
| `S4_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K041; wait for K042+K043+K044; successor `S5_PREFLIGHT` only under its stated guard | `HALTED::S4_REVIEW::INCOMPLETE` | `HALTED::S4_REVIEW::BLOCKED` |
| `S5_PREFLIGHT` | stay; no activity/root | stay; exact submission or dual-controlled root required | K045–K048 emitted; successor `SPAN_REVIEW` only under its stated guard | `HALTED::S5_PREFLIGHT::INCOMPLETE` | `HALTED::S5_PREFLIGHT::BLOCKED` |
| `SPAN_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | K051+K052P accepted; wait for K053+K054+K055; successor `S6_ACQUISITION` only under its stated guard | `HALTED::SPAN_REVIEW::INCOMPLETE` | `HALTED::SPAN_REVIEW::BLOCKED` |
| `S6_ACQUISITION` | stay; no activity/root | stay; exact submission or dual-controlled root required | K056F–K065 emitted; successor `S6_REVIEW` only under its stated guard | `HALTED::S6_ACQUISITION::INCOMPLETE` | `HALTED::S6_ACQUISITION::BLOCKED` |
| `S6_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K067; wait for K069+K070+K071; successor `S7_CONSTRUCTION` only under its stated guard | `HALTED::S6_REVIEW::INCOMPLETE` | `HALTED::S6_REVIEW::BLOCKED` |
| `S7_CONSTRUCTION` | stay; no activity/root | stay; exact submission or dual-controlled root required | K072–K077 emitted; successor `S7_REVIEW` only under its stated guard | `HALTED::S7_CONSTRUCTION::INCOMPLETE` | `HALTED::S7_CONSTRUCTION::BLOCKED` |
| `S7_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K079; successor `ALIGNMENT_POLICY_REVIEW` only under its stated guard | `HALTED::S7_REVIEW::INCOMPLETE` | `HALTED::S7_REVIEW::BLOCKED` |
| `ALIGNMENT_POLICY_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | K082+K083P accepted; wait for K084+K085+K086; successor `S8A_ALIGNMENT` only under its stated guard | `HALTED::ALIGNMENT_POLICY_REVIEW::INCOMPLETE` | `HALTED::ALIGNMENT_POLICY_REVIEW::BLOCKED` |
| `S8A_ALIGNMENT` | stay; no activity/root | stay; exact submission or dual-controlled root required | K087–K089 emitted; successor `S8A_REVIEW` only under its stated guard | `HALTED::S8A_ALIGNMENT::INCOMPLETE` | `HALTED::S8A_ALIGNMENT::BLOCKED` |
| `S8A_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K091; wait for K092+K093+K094; successor `S8B_REBUILD` only under its stated guard | `HALTED::S8A_REVIEW::INCOMPLETE` | `HALTED::S8A_REVIEW::BLOCKED` |
| `S8B_REBUILD` | stay; no activity/root | stay; exact submission or dual-controlled root required | K095–K102 emitted; successor `S8B_REVIEW` only under its stated guard | `HALTED::S8B_REBUILD::INCOMPLETE` | `HALTED::S8B_REBUILD::BLOCKED` |
| `S8B_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | accepted K104; wait for K105+K106+K107; successor `S8C_AUDIT` only under its stated guard | `HALTED::S8B_REVIEW::INCOMPLETE` | `HALTED::S8B_REVIEW::BLOCKED` |
| `S8C_AUDIT` | stay; no activity/root | stay; exact submission or dual-controlled root required | K108–K132 emitted; successor `S9_RESULT_REVIEW` only under its stated guard | `HALTED::S8C_AUDIT::INCOMPLETE` | `HALTED::S8C_AUDIT::BLOCKED` |
| `S9_RESULT_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | APPROVED_CLEAR K137; wait for K138+K139+K140; successor `S10_TRANSITION` only under its stated guard | `HALTED::S9_RESULT_REVIEW::INCOMPLETE` | `HALTED::S9_RESULT_REVIEW::BLOCKED` |
| `S10_TRANSITION` | stay; no activity/root | stay; exact submission or dual-controlled root required | exact K142I+K143I or K142E+K143E+K144E; successor `S10_REVIEW` only under its stated guard | `HALTED::S10_TRANSITION::INCOMPLETE` | `HALTED::S10_TRANSITION::BLOCKED` |
| `S10_REVIEW` | stay; no activity/root | stay; exact submission or dual-controlled root required | K144I accepted or K146E accepted; eligible branch waits for future K147+K148+K149; successor `COMPLETE` only under its stated guard | `HALTED::S10_REVIEW::INCOMPLETE` | `HALTED::S10_REVIEW::BLOCKED` |
| `COMPLETE` | stay `COMPLETE` | invalid | stay complete; no implicit P1 | invalid | invalid |
| `HALTED` | invalid | invalid | invalid | invalid | stay halted; only separately authorized correction may create a new run |

**Exact review-disposition reducer.** A review phase with `phase_status=COMPLETE` applies the following closed mapping; `PENDING` with `COMPLETE`, `NOT_APPLICABLE` on a review phase, or any unlisted branch/disposition tuple is `GLOBAL_STATE_INVALID`.

| Review phase class | `APPROVE` | `ACCEPT_FINDING` | `BLOCK` | `DEFER` | `NEEDS_VERIFICATION` |
|---|---|---|---|---|---|
| Architecture/spec/source/test/S4/S6/S7/S8A/S8B reviews | remain complete until the exact next dual-controlled root exists, then enter the named successor | `HALTED::<phase>::ACCEPTED_FINDING_NO_PROGRESSION` | `HALTED::<phase>::BLOCKED_BY_SENTINEL` | `HALTED::<phase>::DEFERRED` | `HALTED::<phase>::NEEDS_VERIFICATION` |
| Span review, accepted-policy branch | create K051/K052P; remain complete until K053+K054+K055, then S6 | invalid | `HALTED::SPAN_REVIEW::REJECTED_OR_NO_SAFE_SPAN` | `HALTED::SPAN_REVIEW::DEFERRED_OR_PREFLIGHT_INCOMPLETE` | `HALTED::SPAN_REVIEW::NEEDS_VERIFICATION` |
| Alignment-policy review, real-candidate branch | create K082/K083P; remain complete until K084+K085+K086, then S8A | invalid | `HALTED::ALIGNMENT_POLICY_REVIEW::REJECTED` | `HALTED::ALIGNMENT_POLICY_REVIEW::DEFERRED` | `HALTED::ALIGNMENT_POLICY_REVIEW::NEEDS_VERIFICATION` |
| Alignment-policy absence branch | invalid; absence cannot be approved as a policy | `HALTED::ALIGNMENT_POLICY_REVIEW::ABSENCE_ACCEPTED_FINDING` via K080A/K081A/K083A | `HALTED::ALIGNMENT_POLICY_REVIEW::ABSENCE_BLOCKED` | `HALTED::ALIGNMENT_POLICY_REVIEW::ABSENCE_DEFERRED` | `HALTED::ALIGNMENT_POLICY_REVIEW::ABSENCE_NEEDS_VERIFICATION` |
| S9 exact-clear branch | create K137; remain complete until K138+K139+K140, then S10 | invalid | `HALTED::S9::PACKAGE_OR_SPEC_DEFECT` | `HALTED::S9::INCOMPLETE_EVIDENCE` | `HALTED::S9::UNRESOLVED_VERIFICATION` |
| S9 conforming limited/blocked branch | invalid | `HALTED::S9::ACCEPTED_NEGATIVE_FINDING` | `HALTED::S9::PACKAGE_OR_SPEC_DEFECT` | `HALTED::S9::INCOMPLETE_EVIDENCE` | `HALTED::S9::UNRESOLVED_VERIFICATION` |
| S10 eligible branch | create K146E; `COMPLETE::ELIGIBLE_WAITING_P1_DUAL_AUTH` | invalid | `HALTED::S10::TRANSITION_DEFECT` | `HALTED::S10::INCOMPLETE` | `HALTED::S10::NEEDS_VERIFICATION` |
| S10 ineligible branch | invalid | `COMPLETE::INELIGIBLE_FINDING` | `HALTED::S10::TRANSITION_DEFECT` | `HALTED::S10::INCOMPLETE` | `HALTED::S10::NEEDS_VERIFICATION` |

**Global totality.** For every phase, the five statuses and every legal review disposition above have one action. An unlisted phase/status/disposition tuple, a successor root without both authorization records, or a positive acceptance that auto-starts a successor is `GLOBAL_STATE_INVALID`.

### 2.2 Per-condition vector and exact initial state

For every `c∈U0`, `P(c)=(position,window,token_pair,request,construction,alignment,effect)`.

| Dimension | Closed enum |
|---|---|
| `position` | `INITIAL`, `TOKEN_PAIR`, `REQUEST`, `CONSTRUCTION`, `READY_ALIGNMENT`, `FINAL` |
| `window` | `NOT_EVALUATED`, `QUERY_ELIGIBLE`, `VALID_EXCLUSION_INVALID_WINDOW`, `INCOMPLETE_MISSING_TRADE_ANCHOR`, `BLOCKED_RESOLUTION_BOUNDARY` |
| `token_pair` | `NOT_EVALUATED`, `NOT_APPLICABLE_WINDOW`, `STABLE_INDEPENDENT_PAIR`, `UNRESOLVED`, `UNSTABLE`, `PRECISION_INVALID` |
| `request` | `NOT_EVALUATED`, `NOT_APPLICABLE`, `PLANNED`, `IN_PROGRESS`, `COMPLETE_BOTH_TERMINALS`, `INCOMPLETE`, `BLOCKED` |
| `construction` | `NOT_EVALUATED`, `NOT_APPLICABLE`, `BOTH_PARTITIONS_INCLUDED`, `ONE_PARTITION_INCLUDED`, `NO_PARTITION_INCLUDED`, `INCOMPLETE`, `BLOCKED` |
| `alignment` | `NOT_EVALUATED`, `NOT_APPLICABLE`, `BOTH_SIDE_USABLE`, `ONE_SIDE_USABLE`, `NEITHER_SIDE_USABLE`, `INCOMPLETE`, `BLOCKED` |
| `effect` | `ACTIVE`, `VALID_EXCLUSION`, `CLEAR_COMPONENT`, `LIMITATION`, `INCOMPLETE_EVIDENCE`, `BLOCKING_DEFECT` |

| Class | Exact vector predicate | Successor / final effect |
|---|---|---|
| `P00` | `INITIAL`; every processing field `NOT_EVALUATED`; `effect=ACTIVE` | window evaluation only |
| `P01` | query-eligible window; token pair `NOT_EVALUATED`; later fields `NOT_EVALUATED` | `TOKEN_PAIR` |
| `P02` | `VALID_EXCLUSION_INVALID_WINDOW`; token `NOT_APPLICABLE_WINDOW`; request/construction/alignment `NOT_APPLICABLE` | `FINAL/VALID_EXCLUSION` |
| `P03` | missing trade anchor; all later fields `NOT_APPLICABLE` | `FINAL/INCOMPLETE_EVIDENCE` |
| `P04` | malformed/missing resolution boundary; all later fields `NOT_APPLICABLE` | `FINAL/BLOCKING_DEFECT` |
| `P05` | query eligible + `STABLE_INDEPENDENT_PAIR`; request `NOT_EVALUATED` | `REQUEST` |
| `P06` | query eligible + token `UNRESOLVED|UNSTABLE|PRECISION_INVALID`; later fields `NOT_APPLICABLE` | `FINAL/BLOCKING_DEFECT` |
| `P07` | stable pair + request `PLANNED|IN_PROGRESS`; later fields `NOT_EVALUATED` | stay `REQUEST` |
| `P08` | request `COMPLETE_BOTH_TERMINALS`; construction `NOT_EVALUATED` | `CONSTRUCTION` |
| `P09` | request `INCOMPLETE`; later fields `NOT_APPLICABLE` | `FINAL/INCOMPLETE_EVIDENCE` |
| `P10` | request `BLOCKED`; later fields `NOT_APPLICABLE` | `FINAL/BLOCKING_DEFECT` |
| `P11` | construction in `BOTH|ONE|NO_PARTITION_INCLUDED`; alignment `NOT_EVALUATED` | `READY_ALIGNMENT`; waits for accepted policy and dual S8A authorization |
| `P12` | construction `INCOMPLETE`; alignment `NOT_APPLICABLE` | `FINAL/INCOMPLETE_EVIDENCE` |
| `P13` | construction `BLOCKED`; alignment `NOT_APPLICABLE` | `FINAL/BLOCKING_DEFECT` |
| `P14` | legal construction/alignment pair ending `BOTH_SIDE_USABLE` | `FINAL/CLEAR_COMPONENT` |
| `P15` | legal pair ending `ONE_SIDE_USABLE` | `FINAL/LIMITATION` |
| `P16` | legal pair ending `NEITHER_SIDE_USABLE` | `FINAL/LIMITATION` |
| `P17` | alignment `INCOMPLETE` | `FINAL/INCOMPLETE_EVIDENCE` |
| `P18` | alignment `BLOCKED` | `FINAL/BLOCKING_DEFECT` |

Legal construction/alignment pairs are total: `BOTH_PARTITIONS_INCLUDED` permits both/one/neither/incomplete/blocked; `ONE_PARTITION_INCLUDED` permits one/neither/incomplete/blocked; `NO_PARTITION_INCLUDED` permits neither/incomplete/blocked; incomplete or blocked construction permits alignment `NOT_APPLICABLE` only. Any vector matching zero or multiple rows is `CONDITION_STATE_INVALID`.

A `P02` invalid-window condition is immutable, appears in every later 39,693-condition reconciliation, never becomes token/request/construction/alignment applicable, may coexist with exact global clear when all applicable evidence passes, and must later receive `T(c)=TRANSITION_INELIGIBLE` because `W=false`.

### 2.3 Consumer-transition vector

`T(c)=(evaluation,W,T,R,C,A,P,L,G,S,I,U,outcome,failing_conjuncts)` uses the inherited eleven-conjunct predicate: valid window; stable independent pair; complete requests; complete construction; artifact inclusion; accepted alignment policy; `BOTH_SIDE_USABLE`; exact clear gate; approved Sentinel clear review; matching identities; and valid Gustavo S10 authorization under the exact Sentinel S10 stage authorization. All true gives `ELIGIBLE_CANDIDATE_INCLUDED`; otherwise `TRANSITION_INELIGIBLE`. Therefore `U0=E⊎I` and `|E|+|I|=39,693`.

---

## 3. Dual-control stage authorization

### 3.1 Record contracts

A prerequisite review acceptance, a Sentinel narrow-stage authorization, and a Gustavo activity authorization are three distinct immutable records.

| Record | Required identity fields | Forbidden implication |
|---|---|---|
| Sentinel acceptance/review | reviewed deliverable ID/path/length/SHA-256; decision; decision code; canonical commit | does not authorize activity |
| Sentinel stage authorization | `stage_authorization_id`; prerequisite acceptance ID; canonical commit; stage code; exact permitted activity; output roots; status `AUTHORIZED` | does not substitute for Gustavo |
| Gustavo activity authorization | `activity_authorization_id`; exact Sentinel stage-authorization ID; prerequisite acceptance ID; canonical commit; stage code; allowed activity/actor/output roots | cannot exist as a lifecycle advance without matching Sentinel authorization |
| Activity root | root ID; both exact authorization IDs; prerequisite acceptance ID; canonical commit; stage code; run ID | absent/mismatched record is `STOP_AUTHORIZATION_PROVENANCE_INVALID` |
| Handoff | exact deliverable identities; root ID; both authorization IDs; performed/not-performed activities | cannot omit either control record |

The Sentinel stage authorization never references the later Gustavo record. The Gustavo record references the prior Sentinel stage authorization. The root references both. This one-way order prevents an authorization cycle.

### 3.2 Mandatory dual-control ladder

| Prerequisite acceptance | Sentinel stage authorization | Gustavo authorization | Activity root | Deliverable/handoff |
|---|---|---|---|---|
| accepted normalization K004 | `K005` | `K006` | `K007` | Candidate 08 K008 / H K009 |
| accepted Candidate 08 K011 | `K012` | `K013` | `K014` | implementation source K015 / H1 K016 |
| accepted source K018 | `K019` | `K020` | `K021` | test source K022 / H2 K023 |
| accepted test source K025 + source K018 | `K026` | `K027` | `K028` | test result K029 / H3 K030 |
| accepted test result K032 | `K033` | `K034` | `K035` | S4 K036–K038 / H4 K039 |
| accepted S4 K041 | `K042` | `K043` | `K044` | S5 K045–K047 / H5 K048 |
| accepted span policy K051 + H K052P | `K053` | `K054` | `K055` | S6 K056F–K064 / H6 K065 |
| accepted S6 K067 | `K069` | `K070` | `K071` | S7 K072–K076 / H7 K077 |
| accepted alignment policy K082 + H K083P | `K084` | `K085` | `K086` | S8A K087–K088 / H K089 |
| accepted S8A K091 | `K092` | `K093` | `K094` | S8B K095–K101 / H K102 |
| accepted S8B K104 | `K105` | `K106` | `K107` | S8C K108–K131 / H K132 |
| S9 approved clear K137 | `K138` | `K139` | `K140` | S10 K141 plus one branch handoff |
| accepted eligible transition K146E | `K147` | `K148` | `K149` | future P1 only; no artifact authorized here |

**No single-party progression.** A Gustavo authorization without its exact Sentinel stage authorization cannot create a root. A Sentinel acceptance or stage authorization without Gustavo authorization cannot create a root. No completed review automatically creates either record.

---

## 4. Deterministic scientific identity and row identity

### 4.1 Shared `deterministic_build_id`

`deterministic_build_id = SHA256(JCS(preimage))`, with this exact ordered preimage:

1. `schema_id = pm_research.s2.deterministic_build_identity.v1`;
2. accepted construction-contract ID and SHA-256 (`K068`);
3. canonical Git commit (`K000`);
4. accepted S4 scientific processing-ledger identity (`K037`), using its time-free scientific projection only;
5. full scientific request-plan manifest path/length/SHA-256 (`K057`), excluding activity IDs, actors, and execution timestamps;
6. detached raw-archive identity fields, including archive path/length/SHA-256 (`K063`);
7. deterministic serialization-profile ID;
8. deterministic construction-algorithm ID.

`K037`, `K057`, and `K063` are scientific identities only; their activity provenance remains in the corresponding roots, provenance wrappers, and handoffs. It MUST NOT contain any authorization ID, activity-root ID, execution/rebuild run ID, timestamp, actor, environment, output path hash, partition hash, manifest hash, reconciliation hash, inventory hash, handoff ID, or review ID.

### 4.2 Compared versus provenance artifacts

| Byte-compared original/rebuild pair | Same required scientific identity |
|---|---|
| `K073F` ↔ `K096F` | same logical paths, rows, order, bytes, and `deterministic_build_id` |
| `K074` ↔ `K097` | same scientific manifest bytes and `deterministic_build_id` |
| `K075` ↔ `K098` | same scientific reconciliation bytes and `deterministic_build_id` |

`K076`, `K095`, `K099`, `K100`, `K101`, activity roots, authorizations, run IDs, timestamps, actors, environments, and handoffs are intentionally not byte-compared. They preserve activity provenance and compare exact scientific output identities without entering those output bytes.

### 4.3 Acyclic row-key preimage

Every original and rebuilt row uses the identical key:

`row_key_sha256 = SHA256(JCS([row_schema_id, deterministic_build_id, condition_id, token_id, outcome_index, price_ts_utc_ms, deterministic_source_row_id]))`

- IDs are canonical strings; `outcome_index∈{0,1}` is an integer; timestamp is an integer millisecond UTC value.
- `deterministic_source_row_id` is fixed from predecessor raw evidence only: request ID, raw-member SHA-256, raw point ordinal, normalized source timestamp, and canonical decimal price.
- The preimage excludes original/rebuild activity IDs, run IDs, authorizations, actor/time/environment fields, and all descendant partition/manifest/reconciliation/inventory/archive/handoff hashes.
- Original and rebuild compute it independently from the same sealed predecessors; neither may read original output bytes as a rebuild source.

---

## 5. Immutable artifact registry and complete DAG

Each row is one artifact or explicitly indexed family. Conditional branch nodes are absent outside their branch. Rank is the list order below; every predecessor has a lower rank.

| Rank | Node | Artifact / record | Producer | Class | Branch | Byte-compared |
|---:|---|---|---|---|---|---|
| 0 | `K000` | Canonical Git commit identity | canonical repository | canonical input | `all` | `no` |
| 1 | `K001` | Canonical S1/P0/guardrail contract set | canonical repository | canonical input | `all` | `no` |
| 2 | `K002` | Architecture Normalization Candidate 03 bytes | Professor | architecture candidate | `all` | `no` |
| 3 | `K003` | Sentinel normalization review record | Sentinel | review decision | `all` | `no` |
| 4 | `K004` | Accepted normalization record | Sentinel | accepted record | `approve-only` | `no` |
| 5 | `K005` | Sentinel Candidate-08 drafting-stage authorization | Sentinel | stage authorization | `all` | `no` |
| 6 | `K006` | Gustavo Candidate-08 drafting authorization | Gustavo | activity authorization | `all` | `no` |
| 7 | `K007` | Candidate-08 drafting activity root | future Professor | activity root | `all` | `no` |
| 8 | `K008` | Future Candidate-08 specification candidate bytes | future Professor | specification candidate | `all` | `no` |
| 9 | `K009` | Candidate-08 review handoff | future Professor | handoff | `all` | `no` |
| 10 | `K010` | Sentinel Candidate-08 review record | Sentinel | review decision | `all` | `no` |
| 11 | `K011` | Accepted Candidate-08 specification record | Sentinel | accepted record | `approve-only` | `no` |
| 12 | `K012` | Sentinel implementation-source stage authorization | Sentinel | stage authorization | `all` | `no` |
| 13 | `K013` | Gustavo implementation-source authoring authorization | Gustavo | activity authorization | `all` | `no` |
| 14 | `K014` | Implementation-source authoring activity root | Claude/future implementer | activity root | `all` | `no` |
| 15 | `K015` | Implementation-source candidate | Claude/future implementer | source candidate | `all` | `no` |
| 16 | `K016` | H1 implementation-source handoff | Claude/future implementer | handoff | `all` | `no` |
| 17 | `K017` | Sentinel source review record | Sentinel | review decision | `all` | `no` |
| 18 | `K018` | Accepted implementation-source record | Sentinel | accepted record | `approve-only` | `no` |
| 19 | `K019` | Sentinel test-source-authoring stage authorization | Sentinel | stage authorization | `all` | `no` |
| 20 | `K020` | Gustavo test-source-authoring authorization | Gustavo | activity authorization | `all` | `no` |
| 21 | `K021` | Test-source-authoring activity root | Claude/future test author | activity root | `all` | `no` |
| 22 | `K022` | Test-source candidate | Claude/future test author | test-source candidate | `all` | `no` |
| 23 | `K023` | H2 test-source handoff | Claude/future test author | handoff | `all` | `no` |
| 24 | `K024` | Sentinel test-source review record | Sentinel | review decision | `all` | `no` |
| 25 | `K025` | Accepted test-source record | Sentinel | accepted record | `approve-only` | `no` |
| 26 | `K026` | Sentinel test-execution stage authorization | Sentinel | stage authorization | `all` | `no` |
| 27 | `K027` | Gustavo test-execution authorization | Gustavo | activity authorization | `all` | `no` |
| 28 | `K028` | Test-execution activity root | authorized executor | activity root | `all` | `no` |
| 29 | `K029` | Test-execution result | authorized executor | result evidence | `all` | `no` |
| 30 | `K030` | H3 test-result handoff | authorized executor | handoff | `all` | `no` |
| 31 | `K031` | Sentinel test-result review record | Sentinel | review decision | `all` | `no` |
| 32 | `K032` | Accepted test-result record | Sentinel | accepted record | `accept-only` | `no` |
| 33 | `K033` | Sentinel S4 stage authorization | Sentinel | stage authorization | `all` | `no` |
| 34 | `K034` | Gustavo S4 local-data authorization | Gustavo | activity authorization | `all` | `no` |
| 35 | `K035` | S4 activity root | authorized S4 actor | activity root | `all` | `no` |
| 36 | `K036` | S4 local-input identity manifest | authorized S4 actor | input identity | `all` | `no` |
| 37 | `K037` | S4 per-condition processing ledger | authorized S4 actor | condition ledger | `all` | `no` |
| 38 | `K038` | S4 reconciliation | authorized S4 actor | reconciliation | `all` | `no` |
| 39 | `K039` | H4 S4 handoff | authorized S4 actor | handoff | `all` | `no` |
| 40 | `K040` | Sentinel S4 review record | Sentinel | review decision | `all` | `no` |
| 41 | `K041` | Accepted S4 result record | Sentinel | accepted record | `accept-only` | `no` |
| 42 | `K042` | Sentinel S5 stage authorization | Sentinel | stage authorization | `all` | `no` |
| 43 | `K043` | Gustavo S5 preflight/network authorization | Gustavo | activity authorization | `all` | `no` |
| 44 | `K044` | S5 activity root | authorized S5 actor | activity root | `all` | `no` |
| 45 | `K045` | S5 deterministic preflight plan | authorized S5 actor | plan | `all` | `no` |
| 46 | `K046` | S5 preflight evidence set | authorized S5 actor | preflight evidence | `all` | `no` |
| 47 | `K047` | S5 preflight closure | authorized S5 actor | closure record | `all` | `no` |
| 48 | `K048` | H5 preflight handoff | authorized S5 actor | handoff | `all` | `no` |
| 49 | `K049` | Span-policy candidate | policy proposer | policy candidate | `all` | `no` |
| 50 | `K050` | Sentinel span-policy review record | Sentinel | review decision | `all` | `no` |
| 51 | `K051` | Accepted span-policy record | Sentinel | accepted policy | `approve-only` | `no` |
| 52 | `K052P` | Pre-S6 accepted span-policy handoff | Sentinel | handoff | `approve-only` | `no` |
| 53 | `K052N` | Pre-S6 negative span-review handoff | Sentinel | handoff | `negative-only` | `no` |
| 54 | `K053` | Sentinel S6 stage authorization | Sentinel | stage authorization | `all` | `no` |
| 55 | `K054` | Gustavo S6 full-acquisition authorization | Gustavo | activity authorization | `all` | `no` |
| 56 | `K055` | S6 activity root | authorized S6 actor | activity root | `all` | `no` |
| 57 | `K056F` | Full request-plan row family | authorized S6 planner | plan rows | `all` | `no` |
| 58 | `K057` | Full request-plan manifest | authorized S6 planner | plan manifest | `all` | `no` |
| 59 | `K058F` | Raw request-attempt family | authorized S6 actor | raw evidence | `all` | `no` |
| 60 | `K059F` | Request-terminal family | authorized S6 actor | terminal evidence | `all` | `no` |
| 61 | `K060` | Raw-evidence inventory | authorized S6 actor | inventory | `all` | `no` |
| 62 | `K061` | Raw completion record | authorized S6 actor | closure record | `all` | `no` |
| 63 | `K062` | Raw archive bytes | authorized S6 actor | archive bytes | `all` | `no` |
| 64 | `K063` | Detached raw-archive identity file | authorized S6 actor | detached identity | `all` | `no` |
| 65 | `K064` | S6 acquisition reconciliation | authorized S6 actor | reconciliation | `all` | `no` |
| 66 | `K065` | H6 acquisition handoff | authorized S6 actor | handoff | `all` | `no` |
| 67 | `K066` | Sentinel S6 result review record | Sentinel | review decision | `all` | `no` |
| 68 | `K067` | Accepted S6 result record | Sentinel | accepted record | `accept-only` | `no` |
| 69 | `K068` | Accepted construction-contract identity | Sentinel/spec workflow | accepted contract identity | `all` | `no` |
| 70 | `K069` | Sentinel S7 stage authorization | Sentinel | stage authorization | `all` | `no` |
| 71 | `K070` | Gustavo S7 construction authorization | Gustavo | activity authorization | `all` | `no` |
| 72 | `K071` | S7 original-construction activity root | authorized S7 actor | activity root | `all` | `no` |
| 73 | `K072` | Shared deterministic_build_id | deterministic identity function | scientific identity | `all` | `no` |
| 74 | `K073F` | Original scientific price-partition family | authorized S7 actor | byte-compared scientific output | `all` | `yes` |
| 75 | `K074` | Original scientific artifact manifest | authorized S7 actor | byte-compared scientific output | `all` | `yes` |
| 76 | `K075` | Original scientific construction reconciliation | authorized S7 actor | byte-compared scientific output | `all` | `yes` |
| 77 | `K076` | Original activity provenance wrapper/inventory | authorized S7 actor | non-compared provenance | `all` | `no` |
| 78 | `K077` | H7 construction handoff | authorized S7 actor | handoff | `all` | `no` |
| 79 | `K078` | Sentinel S7 result review record | Sentinel | review decision | `all` | `no` |
| 80 | `K079` | Accepted S7 result record | Sentinel | accepted record | `accept-only` | `no` |
| 81 | `K080P` | Alignment-policy candidate submission | policy proposer | policy candidate | `candidate-present` | `no` |
| 82 | `K080A` | Alignment-policy absence submission | policy proposer/reviewer | absence evidence | `candidate-absent` | `no` |
| 83 | `K081P` | Sentinel alignment-policy candidate review record | Sentinel | review decision | `candidate-present` | `no` |
| 84 | `K081A` | Sentinel alignment-policy absence review record | Sentinel | review decision | `candidate-absent` | `no` |
| 85 | `K082` | Accepted alignment-policy record | Sentinel | accepted policy | `approve-real-candidate-only` | `no` |
| 86 | `K083P` | Pre-S8A accepted alignment-policy handoff | Sentinel | handoff | `approve-real-candidate-only` | `no` |
| 87 | `K083R` | Pre-S8A rejected/deferred/verification handoff | Sentinel | handoff | `candidate-negative` | `no` |
| 88 | `K083A` | Pre-S8A policy-absence handoff | Sentinel | handoff | `absence-reviewed` | `no` |
| 89 | `K084` | Sentinel S8A stage authorization | Sentinel | stage authorization | `all` | `no` |
| 90 | `K085` | Gustavo S8A alignment authorization | Gustavo | activity authorization | `all` | `no` |
| 91 | `K086` | S8A activity root | authorized S8A actor | activity root | `all` | `no` |
| 92 | `K087` | Decision-time coverage ledger | authorized S8A actor | alignment evidence | `all` | `no` |
| 93 | `K088` | Alignment reconciliation | authorized S8A actor | reconciliation | `all` | `no` |
| 94 | `K089` | H8A alignment handoff | authorized S8A actor | handoff | `all` | `no` |
| 95 | `K090` | Sentinel S8A result review record | Sentinel | review decision | `all` | `no` |
| 96 | `K091` | Accepted S8A result record | Sentinel | accepted record | `accept-only` | `no` |
| 97 | `K092` | Sentinel S8B stage authorization | Sentinel | stage authorization | `all` | `no` |
| 98 | `K093` | Gustavo S8B rebuild authorization | Gustavo | activity authorization | `all` | `no` |
| 99 | `K094` | S8B activity root | authorized S8B controller | activity root | `all` | `no` |
| 100 | `K095` | Rebuild activity provenance wrapper | authorized S8B controller | non-compared provenance | `all` | `no` |
| 101 | `K096F` | Rebuilt scientific price-partition family | isolated rebuild actor | byte-compared scientific output | `all` | `yes` |
| 102 | `K097` | Rebuilt scientific artifact manifest | isolated rebuild actor | byte-compared scientific output | `all` | `yes` |
| 103 | `K098` | Rebuilt scientific construction reconciliation | isolated rebuild actor | byte-compared scientific output | `all` | `yes` |
| 104 | `K099` | Rebuilt activity provenance inventory | authorized S8B controller | non-compared provenance | `all` | `no` |
| 105 | `K100` | Original scientific-output comparison inventory | authorized S8B controller | comparison inventory | `all` | `no` |
| 106 | `K101` | Deterministic-rebuild comparison evidence | authorized S8B controller | comparison evidence | `all` | `no` |
| 107 | `K102` | H8B rebuild handoff | authorized S8B controller | handoff | `all` | `no` |
| 108 | `K103` | Sentinel S8B result review record | Sentinel | review decision | `all` | `no` |
| 109 | `K104` | Accepted S8B result record | Sentinel | accepted record | `accept-only` | `no` |
| 110 | `K105` | Sentinel S8C stage authorization | Sentinel | stage authorization | `all` | `no` |
| 111 | `K106` | Gustavo S8C audit authorization | Gustavo | activity authorization | `all` | `no` |
| 112 | `K107` | S8C activity root | authorized S8C auditor | activity root | `all` | `no` |
| 113 | `K108` | Complete condition-effect ledger | authorized S8C auditor | audit evidence | `all` | `no` |
| 114 | `K109` | Audit evidence closure: canonical_base_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 115 | `K110` | Audit evidence closure: complete_universe_reconciliation | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 116 | `K111` | Audit evidence closure: decision_window_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 117 | `K112` | Audit evidence closure: token_pair_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 118 | `K113` | Audit evidence closure: span_policy_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 119 | `K114` | Audit evidence closure: request_plan_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 120 | `K115` | Audit evidence closure: request_terminal_completeness | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 121 | `K116` | Audit evidence closure: raw_archive_closure | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 122 | `K117` | Audit evidence closure: independent_token_acquisition | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 123 | `K118` | Audit evidence closure: no_synthesis_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 124 | `K119` | Audit evidence closure: original_construction_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 125 | `K120` | Audit evidence closure: duplicate_conflict_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 126 | `K121` | Audit evidence closure: alignment_policy_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 127 | `K122` | Audit evidence closure: alignment_execution_integrity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 128 | `K123` | Audit evidence closure: decision_time_coverage | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 129 | `K124` | Audit evidence closure: deterministic_build_identity | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 130 | `K125` | Audit evidence closure: deterministic_rebuild_byte_equality | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 131 | `K126` | Audit evidence closure: condition_effect_reconciliation | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 132 | `K127` | Audit evidence closure: authorization_and_handoff_provenance | authorized S8C auditor | audit evidence closure | `all` | `no` |
| 133 | `K128` | Nineteen-check audit record | authorized S8C auditor | audit record | `all` | `no` |
| 134 | `K129` | Audit gate record | authorized S8C auditor | gate record | `all` | `no` |
| 135 | `K130` | Audit report | authorized S8C auditor | human rendering | `all` | `no` |
| 136 | `K131` | Gate reconciliation | authorized S8C auditor | reconciliation | `all` | `no` |
| 137 | `K132` | H8C exact audit handoff | authorized S8C auditor | handoff | `all` | `no` |
| 138 | `K133` | S9 review_id | Sentinel | review identity | `all` | `no` |
| 139 | `K134` | Sentinel S9 result-review record | Sentinel | review decision | `all` | `no` |
| 140 | `K135` | S9 review reconciliation | Sentinel | reconciliation | `all` | `no` |
| 141 | `K136` | H9 result-review handoff | Sentinel | handoff | `all` | `no` |
| 142 | `K137` | Approved-clear progression record | Sentinel | accepted record | `approved-clear-only` | `no` |
| 143 | `K138` | Sentinel S10 stage authorization | Sentinel | stage authorization | `all` | `no` |
| 144 | `K139` | Gustavo S10 transition-drafting authorization | Gustavo | activity authorization | `all` | `no` |
| 145 | `K140` | S10 activity root | authorized S10 actor | activity root | `all` | `no` |
| 146 | `K141` | Consumer-eligibility reconciliation | authorized S10 evaluator | reconciliation | `all` | `no` |
| 147 | `K142I` | Ineligible transition record | authorized S10 evaluator | transition record | `ineligible` | `no` |
| 148 | `K143I` | H10-I ineligible-branch handoff | authorized S10 evaluator | handoff | `ineligible` | `no` |
| 149 | `K144I` | Sentinel ineligible-transition review record | Sentinel | review decision | `ineligible` | `no` |
| 150 | `K142E` | Bounded P1-consumer specification candidate bytes | Professor | specification candidate | `eligible` | `no` |
| 151 | `K143E` | Candidate-sealing transition record | authorized S10 evaluator | transition record | `eligible` | `no` |
| 152 | `K144E` | H10-E eligible-branch handoff | authorized S10 evaluator/Professor | handoff | `eligible` | `no` |
| 153 | `K145E` | Sentinel eligible-transition review record | Sentinel | review decision | `eligible` | `no` |
| 154 | `K146E` | Accepted eligible-transition record | Sentinel | accepted record | `eligible-accepted` | `no` |
| 155 | `K147` | Sentinel future-P1 stage authorization | Sentinel | stage authorization | `future-P1` | `no` |
| 156 | `K148` | Gustavo future-P1 activity authorization | Gustavo | activity authorization | `future-P1` | `no` |
| 157 | `K149` | Future-P1 activity root | future authorized actor | activity root | `future-P1` | `no` |

### 5.1 Complete direct-edge table

An edge `X→Y` means `Y` stores or derives from an identity, path, byte length, SHA-256, ID, count, or identified content of `X`. Nodes with no predecessors are roots.

| Target | Exact direct predecessors |
|---|---|
| `K000` | none |
| `K001` | `K000` |
| `K002` | `K000`, `K001` |
| `K003` | `K002` |
| `K004` | `K002`, `K003` |
| `K005` | `K004` |
| `K006` | `K004`, `K005` |
| `K007` | `K004`, `K005`, `K006` |
| `K008` | `K007` |
| `K009` | `K005`, `K006`, `K007`, `K008` |
| `K010` | `K008`, `K009` |
| `K011` | `K008`, `K010` |
| `K012` | `K011` |
| `K013` | `K011`, `K012` |
| `K014` | `K011`, `K012`, `K013` |
| `K015` | `K014` |
| `K016` | `K012`, `K013`, `K014`, `K015` |
| `K017` | `K015`, `K016` |
| `K018` | `K015`, `K017` |
| `K019` | `K018` |
| `K020` | `K018`, `K019` |
| `K021` | `K018`, `K019`, `K020` |
| `K022` | `K021` |
| `K023` | `K019`, `K020`, `K021`, `K022` |
| `K024` | `K022`, `K023` |
| `K025` | `K022`, `K024` |
| `K026` | `K018`, `K025` |
| `K027` | `K018`, `K025`, `K026` |
| `K028` | `K018`, `K025`, `K026`, `K027` |
| `K029` | `K028` |
| `K030` | `K026`, `K027`, `K028`, `K029` |
| `K031` | `K029`, `K030` |
| `K032` | `K029`, `K031` |
| `K033` | `K032` |
| `K034` | `K032`, `K033` |
| `K035` | `K032`, `K033`, `K034` |
| `K036` | `K035` |
| `K037` | `K035`, `K036` |
| `K038` | `K035`, `K037` |
| `K039` | `K033`, `K034`, `K035`, `K036`, `K037`, `K038` |
| `K040` | `K038`, `K039` |
| `K041` | `K038`, `K040` |
| `K042` | `K041` |
| `K043` | `K041`, `K042` |
| `K044` | `K041`, `K042`, `K043` |
| `K045` | `K044` |
| `K046` | `K044`, `K045` |
| `K047` | `K044`, `K045`, `K046` |
| `K048` | `K042`, `K043`, `K044`, `K045`, `K046`, `K047` |
| `K049` | `K045`, `K047`, `K048` |
| `K050` | `K048`, `K049` |
| `K051` | `K049`, `K050` |
| `K052P` | `K050`, `K051` |
| `K052N` | `K048`, `K050` |
| `K053` | `K041`, `K051`, `K052P` |
| `K054` | `K041`, `K051`, `K052P`, `K053` |
| `K055` | `K041`, `K051`, `K052P`, `K053`, `K054` |
| `K056F` | `K037`, `K051`, `K055` |
| `K057` | `K055`, `K056F` |
| `K058F` | `K055`, `K057` |
| `K059F` | `K055`, `K056F`, `K058F` |
| `K060` | `K055`, `K058F`, `K059F` |
| `K061` | `K055`, `K057`, `K059F`, `K060` |
| `K062` | `K055`, `K060`, `K061` |
| `K063` | `K062` |
| `K064` | `K037`, `K057`, `K059F`, `K061`, `K063` |
| `K065` | `K053`, `K054`, `K055`, `K057`, `K060`, `K061`, `K062`, `K063`, `K064` |
| `K066` | `K064`, `K065` |
| `K067` | `K064`, `K066` |
| `K068` | `K011`, `K018` |
| `K069` | `K067`, `K068` |
| `K070` | `K067`, `K068`, `K069` |
| `K071` | `K067`, `K068`, `K069`, `K070` |
| `K072` | `K000`, `K037`, `K057`, `K063`, `K068` |
| `K073F` | `K059F`, `K063`, `K072` |
| `K074` | `K072`, `K073F` |
| `K075` | `K037`, `K059F`, `K072`, `K074` |
| `K076` | `K069`, `K070`, `K071`, `K072`, `K073F`, `K074`, `K075` |
| `K077` | `K069`, `K070`, `K071`, `K074`, `K075`, `K076` |
| `K078` | `K075`, `K077` |
| `K079` | `K075`, `K078` |
| `K080P` | `K074`, `K075`, `K077`, `K079` |
| `K080A` | `K077`, `K079` |
| `K081P` | `K080P` |
| `K081A` | `K080A` |
| `K082` | `K080P`, `K081P` |
| `K083P` | `K081P`, `K082` |
| `K083R` | `K080P`, `K081P` |
| `K083A` | `K080A`, `K081A` |
| `K084` | `K079`, `K082`, `K083P` |
| `K085` | `K079`, `K082`, `K083P`, `K084` |
| `K086` | `K079`, `K082`, `K083P`, `K084`, `K085` |
| `K087` | `K037`, `K074`, `K075`, `K082`, `K086` |
| `K088` | `K037`, `K075`, `K086`, `K087` |
| `K089` | `K084`, `K085`, `K086`, `K087`, `K088` |
| `K090` | `K088`, `K089` |
| `K091` | `K088`, `K090` |
| `K092` | `K091` |
| `K093` | `K091`, `K092` |
| `K094` | `K091`, `K092`, `K093` |
| `K095` | `K092`, `K093`, `K094`, `K072` |
| `K096F` | `K059F`, `K063`, `K072` |
| `K097` | `K072`, `K096F` |
| `K098` | `K037`, `K059F`, `K072`, `K097` |
| `K099` | `K092`, `K093`, `K094`, `K095`, `K096F`, `K097`, `K098` |
| `K100` | `K073F`, `K074`, `K075`, `K094` |
| `K101` | `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K099`, `K100` |
| `K102` | `K092`, `K093`, `K094`, `K095`, `K099`, `K100`, `K101` |
| `K103` | `K101`, `K102` |
| `K104` | `K101`, `K103` |
| `K105` | `K104` |
| `K106` | `K104`, `K105` |
| `K107` | `K104`, `K105`, `K106` |
| `K108` | `K037`, `K038`, `K059F`, `K064`, `K075`, `K088`, `K101`, `K107` |
| `K109` | `K000`, `K001`, `K011`, `K068` |
| `K110` | `K036`, `K037`, `K038`, `K041` |
| `K111` | `K037`, `K038` |
| `K112` | `K037`, `K038` |
| `K113` | `K045`, `K046`, `K047`, `K049`, `K050`, `K051`, `K052P` |
| `K114` | `K051`, `K052P`, `K056F`, `K057` |
| `K115` | `K057`, `K058F`, `K059F`, `K061`, `K064` |
| `K116` | `K060`, `K061`, `K062`, `K063` |
| `K117` | `K056F`, `K058F`, `K059F`, `K064` |
| `K118` | `K057`, `K059F`, `K073F`, `K074`, `K096F`, `K097` |
| `K119` | `K072`, `K073F`, `K074`, `K075`, `K076` |
| `K120` | `K073F`, `K074`, `K075` |
| `K121` | `K080P`, `K081P`, `K082`, `K083P`, `K084`, `K085`, `K086` |
| `K122` | `K074`, `K075`, `K082`, `K087`, `K088` |
| `K123` | `K037`, `K087`, `K088`, `K108` |
| `K124` | `K000`, `K037`, `K057`, `K063`, `K068`, `K072`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098` |
| `K125` | `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K100`, `K101` |
| `K126` | `K037`, `K038`, `K059F`, `K064`, `K075`, `K088`, `K101`, `K108` |
| `K127` | `K005`, `K006`, `K007`, `K009`, `K012`, `K013`, `K014`, `K016`, `K019`, `K020`, `K021`, `K023`, `K026`, `K027`, `K028`, `K030`, `K033`, `K034`, `K035`, `K039`, `K042`, `K043`, `K044`, `K048`, `K053`, `K054`, `K055`, `K065`, `K069`, `K070`, `K071`, `K077`, `K083P`, `K084`, `K085`, `K086`, `K089`, `K092`, `K093`, `K094`, `K102`, `K105`, `K106`, `K107` |
| `K128` | `K107`, `K109`, `K110`, `K111`, `K112`, `K113`, `K114`, `K115`, `K116`, `K117`, `K118`, `K119`, `K120`, `K121`, `K122`, `K123`, `K124`, `K125`, `K126`, `K127` |
| `K129` | `K107`, `K108`, `K128` |
| `K130` | `K129` |
| `K131` | `K108`, `K128`, `K129`, `K130` |
| `K132` | `K105`, `K106`, `K107`, `K108`, `K128`, `K129`, `K130`, `K131` |
| `K133` | `K132` |
| `K134` | `K132`, `K133` |
| `K135` | `K129`, `K131`, `K132`, `K134` |
| `K136` | `K134`, `K135` |
| `K137` | `K134`, `K135`, `K136` |
| `K138` | `K137` |
| `K139` | `K137`, `K138` |
| `K140` | `K137`, `K138`, `K139` |
| `K141` | `K037`, `K108`, `K129`, `K134`, `K135`, `K140` |
| `K142I` | `K138`, `K139`, `K140`, `K141` |
| `K143I` | `K138`, `K139`, `K140`, `K141`, `K142I` |
| `K144I` | `K143I` |
| `K142E` | `K004`, `K011`, `K138`, `K139`, `K140`, `K141` |
| `K143E` | `K138`, `K139`, `K140`, `K141`, `K142E` |
| `K144E` | `K138`, `K139`, `K140`, `K141`, `K142E`, `K143E` |
| `K145E` | `K144E` |
| `K146E` | `K142E`, `K143E`, `K144E`, `K145E` |
| `K147` | `K146E` |
| `K148` | `K146E`, `K147` |
| `K149` | `K146E`, `K147`, `K148` |

**Mechanical graph result.** The registry contains `158` nodes/node families and `557` direct edges. The declared direct-edge set is exactly the union of every registry predecessor field. Every edge points to a strictly later rank; depth-first cycle detection finds zero direct or indirect cycles. The nineteen audit-closure predecessor sets are also exactly equal to the check-evidence table in §6.

### 5.2 Why no back-edge exists

- Review acceptance precedes stage authorization; stage authorization precedes Gustavo authorization; both precede the activity root; deliverables precede handoffs; handoffs precede review.
- `K072` is activity-free and precedes both scientific chains. Original and rebuild provenance wrappers depend on scientific bytes, never the reverse.
- The alignment absence decision depends on `K080A`, not on nonexistent `K080P`. Only `K080P+K081P(APPROVE)` can create `K082`.
- Archive bytes `K062` precede detached identity `K063`.
- S10 ineligible order is `K141→K142I→K143I`; eligible order is `K141→K142E→K143E→K144E`.
- `review_id K133` depends only on exact Stage-8 handoff `K132`; neither H9 nor H10 can enter its preimage.
- Row keys depend only on `K072` and sealed raw predecessors, never on output descendants.

**Strongest attempted cycle.** Put the original activity root into `K074`, require rebuild byte equality, then put the rebuild root into `K097`. This would force unequal bytes or a cross-root dependency. The model rejects both roots from scientific bytes and binds them only in `K076/K095/K099`, so the attempted cycle has no edge into either scientific manifest.

---

## 6. Nineteen audit evidence closures and exact gate model

Every check has one immutable closure node. A closure records its ordered evidence-node identities, expected/applicable/pass/fail/incomplete/zero-population counts, status, stop, and gate effect. Missing mandatory evidence is `INCOMPLETE`, never `NOT_APPLICABLE`.

| # | Check | Closure | Exact ordered evidence nodes | Zero-population rule |
|---:|---|---|---|---|
| 1 | `canonical_base_integrity` | `K109` | `K000`, `K001`, `K011`, `K068` | not permitted; mandatory singleton closure |
| 2 | `complete_universe_reconciliation` | `K110` | `K036`, `K037`, `K038`, `K041` | not permitted; denominator is 39,693 |
| 3 | `decision_window_integrity` | `K111` | `K037`, `K038` | zero invalid windows is PASS after complete scan |
| 4 | `token_pair_integrity` | `K112` | `K037`, `K038` | zero applicable pairs is PASS only if all 39,693 are evidenced valid exclusions; otherwise incomplete |
| 5 | `span_policy_integrity` | `K113` | `K045`, `K046`, `K047`, `K049`, `K050`, `K051`, `K052P` | not permitted once S6 is attempted |
| 6 | `request_plan_integrity` | `K114` | `K051`, `K052P`, `K056F`, `K057` | zero planned requests is PASS only when query-eligible population is proven zero; otherwise incomplete |
| 7 | `request_terminal_completeness` | `K115` | `K057`, `K058F`, `K059F`, `K061`, `K064` | zero terminals is PASS only when planned population is proven zero |
| 8 | `raw_archive_closure` | `K116` | `K060`, `K061`, `K062`, `K063` | not applicable only when planned population is proven zero and no archive is required |
| 9 | `independent_token_acquisition` | `K117` | `K056F`, `K058F`, `K059F`, `K064` | zero applicable requests follows request-plan closure; unsupported N/A forbidden |
| 10 | `no_synthesis_integrity` | `K118` | `K057`, `K059F`, `K073F`, `K074`, `K096F`, `K097` | zero constructed rows is PASS only after complete request/construction closure |
| 11 | `original_construction_integrity` | `K119` | `K072`, `K073F`, `K074`, `K075`, `K076` | zero outputs is PASS only when artifact-included population is proven zero |
| 12 | `duplicate_conflict_integrity` | `K120` | `K073F`, `K074`, `K075` | completed zero-conflict scan is PASS |
| 13 | `alignment_policy_integrity` | `K121` | `K080P`, `K081P`, `K082`, `K083P`, `K084`, `K085`, `K086` | not permitted; mandatory before S8A |
| 14 | `alignment_execution_integrity` | `K122` | `K074`, `K075`, `K082`, `K087`, `K088` | zero applicable rows is PASS only when construction reconciliation proves zero applicable rows |
| 15 | `decision_time_coverage` | `K123` | `K037`, `K087`, `K088`, `K108` | zero BOTH_SIDE_USABLE may be a limitation or block per accepted contract, never unsupported N/A |
| 16 | `deterministic_build_identity` | `K124` | `K000`, `K037`, `K057`, `K063`, `K068`, `K072`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098` | not permitted when outputs exist; mandatory closure |
| 17 | `deterministic_rebuild_byte_equality` | `K125` | `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K100`, `K101` | zero expected paths is PASS only if original output inventory proves zero paths |
| 18 | `condition_effect_reconciliation` | `K126` | `K037`, `K038`, `K059F`, `K064`, `K075`, `K088`, `K101`, `K108` | not permitted; denominator is 39,693 |
| 19 | `authorization_and_handoff_provenance` | `K127` | `K005`, `K006`, `K007`, `K009`, `K012`, `K013`, `K014`, `K016`, `K019`, `K020`, `K021`, `K023`, `K026`, `K027`, `K028`, `K030`, `K033`, `K034`, `K035`, `K039`, `K042`, `K043`, `K044`, `K048`, `K053`, `K054`, `K055`, `K065`, `K069`, `K070`, `K071`, `K077`, `K083P`, `K084`, `K085`, `K086`, `K089`, `K092`, `K093`, `K094`, `K102`, `K105`, `K106`, `K107` | not permitted; every executed stage is mandatory evidence |

The check status domain is `PASS|FAIL|INCOMPLETE`. `NOT_APPLICABLE` is not a gate-clearing status; closed zero populations are represented as positive `PASS` with explicit zero counts and independent population-closure evidence.

| Gate result | Exact reducer | Downstream effect |
|---|---|---|
| `S2_GATE_BLOCKED` | any closure `FAIL` with blocking effect | no S10; Sentinel may `ACCEPT FINDING` only |
| `S2_GATE_INCOMPLETE` | no blocking fail and at least one `INCOMPLETE` | no S10; `DEFER` or `NEEDS_VERIFICATION` |
| `S2_GATE_CLEAR_WITH_LIMITATIONS` | all closures `PASS`, no incomplete/block, and at least one accepted limitation effect | non-authorizing finding; no S10 progression under this architecture |
| `S2_GATE_CLEAR` | all nineteen closures `PASS`, zero limitation/incomplete/blocking effects, complete `39,693` effect reconciliation | eligible for S9 review only; not S10 or P1 authorization |

Valid exclusions are not limitations or failures. They remain in `K108` and may coexist with exact clear because the applicable checks pass and the exclusion count is reconciled. Raw archive closure cannot pass unless `K060`, `K061`, `K062`, and `K063` are all present and mutually consistent.

---

## 7. Review and consumer-transition semantics

| Submitted S8C result | Permitted Sentinel outcome | Progression |
|---|---|---|
| conforming exact clear | `APPROVE` and create `K137` | may await dual S10 authorization |
| conforming clear with limitations | `ACCEPT_FINDING` | halted; no S10 or P1 |
| conforming blocked finding | `ACCEPT_FINDING` | halted; no S10 or P1 |
| incomplete evidence | `DEFER` or `NEEDS_VERIFICATION` | halted pending separately authorized correction |
| package/specification defect | `BLOCK` | halted |

Acceptance of evidence is not gate clearance. Gate clearance is not S10 authorization. S10 acceptance is not P1 authorization. No finding automatically changes canonical state.

S10 has two acyclic branches:

- **Ineligible:** `K141 consumer reconciliation → K142I ineligible transition record → K143I handoff → K144I review`; no consumer-spec candidate exists.
- **Eligible:** `K141 → K142E candidate bytes → K143E sealing record → K144E handoff → K145E review → K146E accepted transition`. `K143E` and `K144E` identify the exact candidate ID, path, byte length, and SHA-256. No `CANDIDATE_SEALED` claim exists before `K142E`.

Any future P1 root requires both `K147` and `K148`; neither is created or authorized by this document.

---

## 8. Counterexample suite

| Counterexample | Required classification / stop | Gate/review/transition consequence |
|---|---|---|
| Valid invalid-window condition survives an exact-clear run | `P02/VALID_EXCLUSION`; remains in K108 and K141 | gate may be exact clear; T(c) explicitly ineligible; no acquisition/alignment applicability |
| Gustavo authorizes S7 but Sentinel has not issued K069 | no K071 root; `STOP_AUTHORIZATION_PROVENANCE_INVALID` | no construction artifact or H7 is conforming |
| Sentinel accepts S6 but Gustavo has not authorized S7 | global S6 review remains complete waiting | no automatic progression; no K071 root |
| Sentinel stage authorization exists without Gustavo authorization | root cannot be created | single-party bypass rejected |
| Original and rebuilt scientific manifests include different activity IDs | nonconforming scientific bytes | deterministic equality FAIL; activity IDs belong only in wrappers |
| Rebuilt row key uses rebuild-run ID | `CONDITION_STATE_INVALID`/identity defect | byte equality FAIL and audit blocked |
| Initial condition before window evaluation | exact `P00`: every processing field NOT_EVALUATED | one representable initial state; window evaluation only |
| Alignment-policy absence reviewed without a candidate | K080A→K081A→K083A | valid halted absence finding; no K082 or S8A |
| Absent review incorrectly depends on K080P | optional-artifact contradiction | graph invalid; no review record accepted |
| Raw archive audit omits detached identity K063 | raw_archive_closure INCOMPLETE | gate incomplete; never clear |
| Original artifact produced with valid bytes but no K069/K070 provenance | K076 cannot close | authorization check FAIL; artifact not accepted |
| Candidate seal attempted before K142E bytes exist | K143E predecessor missing | no seal or eligible handoff |
| Row key includes K074 or partition hash | descendant self-reference | identity invalid; construction blocked |
| One failed side request | P09 or P10 according to terminal evidence | condition remains in effect ledger; no both-side eligibility |
| Both requests complete but no rows | construction/alignment reaches no-partition/neither usable | limitation; consumer ineligible |
| Duplicate timestamp conflict | duplicate check FAIL | S2_GATE_BLOCKED |
| Price exactly at resolution boundary | excluded by half-open window | cannot be selected; coverage disposition follows remaining rows |
| Conforming blocked gate accepted as finding | S9 ACCEPT_FINDING | canonical/P1 state unchanged |
| Exact clear without dual S10 authorization | S9 complete waiting | no K140 root and no T(c) evaluation |

---

## 9. Self-attack

| Attack | Strongest failure attempt | Model response | Remaining acceptance condition |
|---|---|---|---|
| single-party authorization bypass | use Gustavo permission as the only start signal | Gustavo record must reference prior Sentinel stage authorization; root requires both | Sentinel must verify every ladder row and K127 closure |
| automatic stage progression | treat accepted result as implicit next-stage authority | review phase stays complete until dual-controlled root exists | no successor phase may be inferred from approval alone |
| activity values in scientific bytes | embed actor/run/timestamp/root in manifest | scientific schema excludes them; wrappers preserve them separately | Candidate 08 must enumerate forbidden fields |
| row-key divergence | use original/rebuild run IDs | both use K072 and raw predecessor source-row ID | row-key preimage must be schema-locked |
| unrepresentable initial state | use NOT_APPLICABLE before window decision | P00 fixes all fields to NOT_EVALUATED | implementation must reject any other initial vector |
| optional policy contradiction | review absence through missing candidate | K080A is a real absence submission and has its own decision/handoff branch | only K080P approval can create K082 |
| omitted audit edge | check raw archive without detached identity | K116 closure requires K060–K063 and graph equality check catches omission | Sentinel must compare §6 sets to §5 edges |
| hidden composite self-reference | combine deliverable and handoff bytes | every handoff is a later node with deliverable predecessor | no node may represent both roles |
| forward seal attestation | declare candidate sealed from reconciliation alone | K143E requires K142E bytes | candidate identity must be observed, not predicted |

**Strongest alternative architecture.** Use one append-only event log and derive every state and artifact relation by replay. It reduces explicit record types but shifts correctness into replay ordering, event-schema compatibility, and snapshot identity. The normalized explicit-DAG model is preferred because Sentinel can statically inspect every prerequisite, branch, and identity without trusting a replay engine.

**Strongest complexity objection.** The dual-control ladder and 158-node graph are substantial. The complexity is not accidental: each node corresponds to a distinct authorization, deliverable, handoff, review, policy, scientific output, provenance wrapper, or branch whose prior combination caused a false-unblock or cycle risk. Candidate 08 may materialize repeated schemas through one reusable envelope, but it must not collapse identities or lifecycle positions.

### 9.1 Open decisions

| Question | Why it matters | Permitted options | Recommended treatment | Consequence |
|---|---|---|---|---|
| Actual safe chunk span | controls full acquisition | accepted value from S5 evidence or no-safe result | do not choose here | blocks S6 until reviewed |
| Alignment selector and numeric bounds | controls selected rows | only interfaces accepted by future Candidate 08 | do not choose empirically here | blocks S8A until real candidate approval |
| Full-universe coverage outcome | determines effects and gate | clear, limited, incomplete, blocked | preserve all counts | determines S9 review only |
| Exact consumer-eligible subset | determines optional bounded candidate | any subset satisfying all eleven conjuncts | compute only under dual S10 authorization | no P1 authorization follows automatically |

No unresolved architecture issue is concealed. Sentinel should block Candidate 03 if the dual-control record contracts, deterministic identity separation, total reducers, absence branch, or audit-evidence equality are not accepted as the controlling normalization.

---

## 10. Candidate-08 mandatory architecture constraints

1. Candidate 08 MUST depend on an accepted normalization record K004 and its own dual-controlled drafting root; this document does not create those records.
2. Every executable activity MUST use the exact prerequisite acceptance → Sentinel stage authorization → Gustavo authorization → activity-root order.
3. Every handoff MUST directly identify both authorization records and follow the deliverable bytes it reports.
4. Every scientific original/rebuild output MUST use the same K072 deterministic_build_id and exclude all activity provenance.
5. Row keys MUST use the §4.3 preimage and MUST NOT contain activity IDs or descendant content hashes.
6. P00 and every global phase/status/review tuple MUST be represented exactly; unlisted vectors MUST halt with GLOBAL_STATE_INVALID or CONDITION_STATE_INVALID.
7. Alignment-policy absence MUST use K080A/K081A/K083A; only a real approved K080P may create K082 or enter S8A.
8. Candidate 08 MUST materialize all nineteen §6 evidence closures and every listed evidence edge; omitted or extra schema-implied edges are nonconforming.
9. Raw archive closure MUST bind inventory, completion, archive bytes, and detached identity.
10. Original and rebuilt scientific partitions, manifests, and construction reconciliations are the only byte-compared construction outputs.
11. Valid exclusions MUST remain immutable rows through effect, gate, review, and consumer reconciliation and may coexist with exact clear.
12. S10 MUST implement the two branch orders exactly; no sealed-candidate claim may precede candidate bytes.
13. Accepted blocked or limited findings MUST remain non-authorizing.
14. Future P1 MUST require accepted eligible transition plus separate K147/K148 dual control; named_binary_probe_blocked remains true unless canonically changed by a separately authorized process.

---

## 11. Candidate-07 disposition map

| Candidate-07 structure | Disposition | Candidate-03 normalization |
|---|---|---|
| method-qualified S1 findings and fixed universe | retain unchanged | canonical facts remain controlling |
| global/per-condition lifecycle idea | retain with correction | separate total G, P(c), and T(c); exact P00 and phase reducer |
| stage authorization model | replace | dual Sentinel stage authorization plus Gustavo authorization for every activity |
| construction/rebuild run identities in scientific bytes | remove | shared activity-free deterministic_build_id only |
| row key using construction/rebuild run identity | replace | §4.3 deterministic_build_id preimage |
| alignment policy absent branch | replace | real K080A absence submission and separate review/handoff |
| original/rebuilt partition→manifest→reconciliation order | retain with correction | same scientific ID and explicit provenance wrappers |
| audit check list and gate reducer | retain with correction | nineteen exact closure nodes and evidence-implied edges |
| raw archive closure | retain with correction | inventory+completion+archive bytes+detached identity mandatory |
| stage-specific handoffs | retain with correction | each follows deliverable and binds both authorizations |
| S9 negative finding acceptance | retain unchanged | non-authorizing and nonprogressing |
| S10 eligible/ineligible branches | retain with correction | candidate bytes precede seal; dual S10 control |
| future P1 progression | replace | accepted eligible transition plus separate Sentinel/Gustavo P1 controls |

---

## 12. Acceptance evidence and authorization statement

Architecture-review evidence available to Sentinel:

- canonical `main` equals `794fb60d8604e7f40d02bb0371aca55fef4ec7ec`;
- `158` distinct nodes/node families and `557` direct edges;
- every predecessor exists at a lower rank;
- zero direct or indirect cycles;
- registry-derived direct edges equal the declared direct-edge table;
- nineteen evidence-implied audit edge sets equal the nineteen closure-node predecessor sets;
- one exact P00 initial vector and one total five-status reducer for every global phase;
- separate alignment candidate-present and candidate-absent branches;
- one shared scientific identity and activity-free row-key preimage;
- exact `U0=E⊎I` transition reconciliation preserved.

**Authorization statement.** This document is submitted to Sentinel for architecture review only. It does not authorize Candidate 08 drafting or any implementation, test authoring, test execution, local-data access, S4 preparation, S5 preflight, networking, S6 acquisition, S7 construction, S8A alignment, S8B rebuild, S8C audit, S10 transition, P1/P2/P3, scoring, probe execution, canonical change, or Git action. Professor does not approve this candidate.

**Requested Sentinel decision:** `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.
