# S2 Per-Token Price-Artifact Architecture Normalization — Candidate 03 Amendment 01

## 0. Status, purpose, canonical base, and requested decision

| Field | Value |
|---|---|
| Document ID | `S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03_AMENDMENT_01` |
| Status | `ARCHITECTURE_AMENDMENT_CANDIDATE` |
| Authoring mode | `AMEND`; architecture review only |
| Amends | `S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md` |
| Amended base byte length | `68637` |
| Amended base SHA-256 | `6f67619df07e5017c469b6cd8ac9a190c6f66a3e263b2930f8f3997fb7e5b1c2` |
| Canonical repository | `rigolugo/pm_research` |
| Expected and observed `main` | `794fb60d8604e7f40d02bb0371aca55fef4ec7ec` |
| Canonical comparison | `IDENTICAL`; ahead `0`, behind `0` |
| Reviewer / decision owner | Sentinel |
| Requested Sentinel decision | `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` |
| Authorization effect | `NONE` |

**Purpose.** Correct only Candidate 03's activity-control order, controlling-document identity, scientific-projection materialization, authorization-chain evidence, and graph-attestation method without preparing Candidate 08 or converting the normalization into an executable specification.

**Checkable completion sentence.** This amendment is complete when Sentinel can verify that the accepted architecture is exactly Candidate 03 plus this amendment, every activity follows prerequisite acceptance → Gustavo authorization → later Sentinel narrow-stage authorization → activity root, one explicit scientific projection exists for each deterministic source, all prerequisite acceptance bytes and activity chains are independently audited, and the amended authoritative direct-edge registry contains `166` nodes/node families and `678` acyclic edges.

### 0.1 Controlling architecture if accepted

If Sentinel approves this amendment, the controlling architecture IS exactly:

1. `S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md`, byte length `68637`, SHA-256 `6f67619df07e5017c469b6cd8ac9a190c6f66a3e263b2930f8f3997fb7e5b1c2`; plus
2. this amendment's exact submitted bytes, as identified after submission by the Sentinel review record using exact path, byte length, and SHA-256.

This amendment controls on conflict. Architecture Candidates 01 and 02 remain blocked, submitted, noncanonical historical inputs and are not controlling dependencies. Candidate 08 MUST depend only on the accepted controlling architecture-set record `A002`, never directly on Candidate 01 or Candidate 02.

The amendment's own byte length and SHA-256 MUST NOT be written inside its bytes. Sentinel MUST compute and bind them in `A001`; `A002` MUST bind the exact identities of both Candidate 03 and Amendment 01.

### 0.2 Preserved constraints

This amendment preserves Candidate 03's accepted direction and canonical constraints: research only; no trading; `U0=39,693` with `UP_DOWN=22,012`, `OVER_UNDER=1,003`, `NAMED_OTHER=16,678`; independent token-specific acquisition; no complement synthesis, `1-price`, `1-yes_price`, or winner-conditioned enumeration; historical method-qualified `S1_SOURCE_NOT_VIABLE`; revised sample-qualified `S1_SOURCE_VIABLE` only for the reviewed 248-condition Pass-1 sample and EC2 route; no full-universe validation; no accepted price artifact; P1 blocked; `named_binary_probe_blocked=true`; nineteen audit checks; exact clear distinct from clear with limitations; non-authorizing acceptance of valid blocked or limited findings; eleven-conjunct consumer eligibility; and `U0=E⊎I`.

### 0.3 In scope and out of scope

In scope are only the five corrections stated by Gustavo. Out of scope are Candidate 08 drafting, executable schemas, code, tests, fixtures, implementation handoffs, package files, checksums, canonical replacements, data access, preflight, network activity, acquisition, construction, alignment, rebuild, audit execution, transition drafting, P1/P2/P3, scoring, probe execution, canonical mutation, and Git action.

---

## 1. Corrected dual-control authorization order

### 1.1 Normative order

Every controlled activity MUST follow this exact order:

`accepted prerequisite → Gustavo activity authorization → Sentinel narrow-stage authorization → activity root`

Gustavo's record is the substantive permission for implementation authorization, local execution, network execution, empirical runs, and later phases. Sentinel's later narrow-stage authorization is an integrity and scope-activation record. Sentinel MUST NOT broaden Gustavo's scope.

| Record | Mandatory fields and behavior |
|---|---|
| Prerequisite acceptance | exact record ID, path, byte length, SHA-256, decision, decision code, canonical commit, and accepted deliverable identities |
| Gustavo activity authorization | exact ID/path/length/SHA-256; prerequisite acceptance identity; canonical commit; stage code; permitted actor; exact activity; permitted input and output roots; scope; status `AUTHORIZED` |
| Sentinel narrow-stage authorization | exact ID/path/length/SHA-256; exact Gustavo authorization ID/path/length/SHA-256/scope/canonical commit; prerequisite acceptance identity; stage code; activated scope equal to or narrower than Gustavo's scope; decision `AUTHORIZE_STAGE` |
| Activity root | exact prerequisite acceptance identity; exact Gustavo record identity; exact later Sentinel stage-authorization identity; canonical commit; stage code; run ID; declared input/output roots |
| Handoff | exact deliverable identities; prerequisite acceptance; Gustavo authorization; later Sentinel stage authorization; activity root; performed and explicitly unperformed activities |

Sentinel MUST issue the stage authorization only after reading and verifying the exact Gustavo authorization bytes. A Gustavo record without the later Sentinel stage authorization cannot create an activity root. A Sentinel acceptance or stage authorization without the corresponding Gustavo record cannot create an activity root. A Sentinel stage authorization issued before the Gustavo record exists is invalid with `STOP_AUTHORIZATION_ORDER_INVALID`.

### 1.2 Corrected ladder

| Accepted prerequisite | Gustavo authorization | Later Sentinel stage authorization | Activity root | Deliverable and activity handoff |
|---|---|---|---|---|
| accepted controlling architecture `A002` | `K006` | `K005` | `K007` | Candidate 08 `K008`; handoff `K009` |
| accepted Candidate 08 `K011` | `K013` | `K012` | `K014` | implementation source `K015`; H1 `K016` |
| accepted implementation source `K018` | `K020` | `K019` | `K021` | test source `K022`; H2 `K023` |
| accepted source `K018` and accepted test source `K025` | `K027` | `K026` | `K028` | test result `K029`; H3 `K030` |
| accepted test result `K032` | `K034` | `K033` | `K035` | S4 deliverables; H4 `K039` |
| accepted S4 result `K041` | `K043` | `K042` | `K044` | S5 deliverables; H5 `K048` |
| accepted S4 `K041`, span policy `K051`, and accepted policy handoff `K052P` | `K054` | `K053` | `K055` | S6 deliverables; H6 `K065` |
| accepted S6 result `K067` and construction contract `K068` | `K070` | `K069` | `K071` | S7 deliverables; H7 `K077` |
| accepted S7 result `K079`, alignment policy `K082`, and accepted policy handoff `K083P` | `K085` | `K084` | `K086` | S8A deliverables; H8A `K089` |
| accepted S8A result `K091` | `K093` | `K092` | `K094` | S8B deliverables; H8B `K102` |
| accepted S8B result `K104` | `K106` | `K105` | `K107` | S8C evidence; activity-completion handoff `A009`; final review handoff `K132` |
| S9 approved-clear record `K137` | `K139` | `K138` | `K140` | S10 reconciliation and one branch handoff |
| accepted eligible-transition record `K146E` | `K148` | `K147` | `K149` | future P1 activity only under a later accepted contract |

Candidate-08 drafting retains dual control. This amendment does not create `K006`, `K005`, or `K007`.

### 1.3 Corrected authorization ranks

For every retained Candidate-03 node not explicitly overridden below:

`amended_rank(Kxxx) = 1000 + 10 × Candidate03_rank(Kxxx)`

`K003` and `K004` are removed. The Gustavo/Sentinel pairs use these exact amended ranks:

| Activity | Gustavo node | Gustavo rank | Sentinel node | Sentinel rank |
|---|---:|---:|---:|---:|
| Candidate-08 drafting | `K006` | `1050` | `K005` | `1060` |
| implementation-source authoring | `K013` | `1120` | `K012` | `1130` |
| test-source authoring | `K020` | `1190` | `K019` | `1200` |
| test execution | `K027` | `1260` | `K026` | `1270` |
| S4 local-data preparation | `K034` | `1330` | `K033` | `1340` |
| S5 preflight/network | `K043` | `1420` | `K042` | `1430` |
| S6 full acquisition | `K054` | `1540` | `K053` | `1550` |
| S7 construction | `K070` | `1700` | `K069` | `1710` |
| S8A alignment | `K085` | `1890` | `K084` | `1900` |
| S8B rebuild | `K093` | `1970` | `K092` | `1980` |
| S8C audit | `K106` | `2100` | `K105` | `2110` |
| S10 transition drafting | `K139` | `2430` | `K138` | `2440` |
| future P1 | `K148` | `2550` | `K147` | `2560` |

The activity root in every row retains the formula rank and is therefore strictly later than both control records.

---

## 2. Self-contained retained architecture rules

This section makes the accepted Candidate-03-plus-Amendment architecture independent of blocked Candidate 02. It does not select empirical values or authorize activity.

### 2.1 Safe-span policy boundary

| Field | Exact architecture type |
|---|---|
| `candidate_spans_seconds` | nonempty, strictly increasing, duplicate-free array of positive `UInt32` seconds |
| `safety_margin_seconds` | `UInt32` seconds |
| `canary_set` | nonempty immutable identity set selected without outcome, winner, coverage, profitability, or later result information |
| candidate/canary observation | `SAFE`, `UNSAFE`, `INCOMPLETE`, or `INTEGRITY_FAILURE` |

Let `C` be the candidate set. Let `C_safe` contain exactly those `c∈C` for which every required canary has one complete recognized observation equal to `SAFE`, with no contradictory identity or evidence.

Reducer precedence:

1. malformed, contradictory, duplicated, wrong-candidate, wrong-canary, or identity-conflicting evidence → `PREFLIGHT_INTEGRITY_FAILURE`;
2. otherwise any missing required observation → `PREFLIGHT_INCOMPLETE`;
3. otherwise `C_safe=∅` → `NO_SAFE_SPAN`;
4. otherwise `safe_ceiling=max(C_safe)`;
5. `C_margin={c∈C_safe | c+safety_margin_seconds≤safe_ceiling}`;
6. `C_margin=∅` → `NO_SAFE_SPAN_AFTER_MARGIN`;
7. otherwise `approved_chunk_span_seconds=max(C_margin)`.

Zero margin therefore selects the largest safe candidate. Positive margin selects the largest safe candidate that leaves the exact margin below the safe ceiling. One candidate, multiple candidates, no safe candidate, only a smaller safe candidate, and largest-candidate-safe cases all reduce through the same equations.

Only the exact approved Sentinel span-policy tuple may create `K051` and `K052P`. No-safe, incomplete, integrity-failed, rejected, deferred, or verification-required results create no accepted policy and prohibit S6.

### 2.2 Accepted alignment-policy interface

No empirical selector or numeric value is chosen here.

| Field | Closed interface |
|---|---|
| `selector` | `EXACT_COINCIDENT_PAIR` or `FIRST_AT_OR_AFTER_ANCHOR` |
| `max_side_staleness_ms` | `UInt64` milliseconds |
| `max_inter_side_skew_ms` | `UInt64` milliseconds |
| `tie_break_rule` | `EARLIEST_PRICE_TS_THEN_ROW_KEY_SHA256` |
| input row fields | `deterministic_build_id`, `condition_id`, `token_id`, `outcome_index`, `price_ts_utc_s`, canonical decimal price string, `row_key_sha256` |
| interpolation/carry/averaging/midpoint/complement | forbidden |

Authoritative half-open boundary:

`decision_lower_ts_ms <= price_ts_utc_s * 1000 < resolved_at_ts_ms`

No integer-second truncation of either millisecond anchor is permitted.

For each side, `staleness_ms = price_ts_utc_s*1000 - decision_lower_ts_ms`. For a selected pair, `inter_side_skew_ms = abs(side_0_ts_s-side_1_ts_s)*1000`.

| Selector | Candidate population and order | Success | Exact failure disposition |
|---|---|---|---|
| `EXACT_COINCIDENT_PAIR` | all in-window side-0/side-1 pairs with equal `price_ts_utc_s`; order by timestamp, side-0 row key, side-1 row key | first ordered pair with both staleness values within limit; skew is zero; result `BOTH_SIDE_USABLE` | no side-complete pair → `NEITHER_SIDE_USABLE::NO_COINCIDENT_PAIR`; pairs exist but all stale → `NEITHER_SIDE_USABLE::STALE_COINCIDENT_PAIR`; this selector never emits one-side usable |
| `FIRST_AT_OR_AFTER_ANCHOR` | independently select the minimum `(price_ts_utc_s,row_key_sha256)` per side from in-window rows | both selected, both within staleness, and skew within limit → `BOTH_SIDE_USABLE` | exactly one selected/within-staleness side → `ONE_SIDE_USABLE::OTHER_SIDE_MISSING_OR_STALE`; neither valid → `NEITHER_SIDE_USABLE::NO_VALID_SIDE`; both individually valid but skew exceeds limit → `NEITHER_SIDE_USABLE::INTER_SIDE_SKEW_EXCEEDED` |

Only a real candidate submission reviewed and accepted into `K082` plus `K083P` may enter S8A. Absence, rejection, deferral, or verification requirement remains a pre-S8A halt.

### 2.3 Complete populations and denominators

Let `U0` be the exact 39,693-condition universe.

- `39,693 = 22,012 + 1,003 + 16,678`.
- `U0 = V ⊎ Ew ⊎ Im ⊎ Br`, where `V` is valid-window, `Ew` immutable invalid-window valid exclusion, `Im` missing-anchor incomplete, and `Br` malformed/conflicting boundary block.
- Token identity is applicable exactly to `V`: `T=V`.
- `T = Ts ⊎ Tu ⊎ Tunstable ⊎ Tprecision`, where only `Ts` is a stable independent pair.
- Request-planned population `P=Ts`.
- `P = Rc ⊎ Ri ⊎ Rb`, complete, incomplete, and blocked request outcomes.
- `Rc = C2 ⊎ C1 ⊎ C0 ⊎ Ci ⊎ Cb`, two-partition, one-partition, zero-partition, construction-incomplete, construction-blocked.
- Alignment-applicable `L=C2⊎C1⊎C0`.
- `L = B ⊎ O ⊎ N ⊎ Li ⊎ Lb`, both-side, one-side, neither-side, alignment-incomplete, alignment-blocked.
- Consumer transition: `U0=E⊎I` and `|E|+|I|=39,693`.

Every condition appears exactly once in the S4 processing ledger, complete condition-effect ledger, and S10 consumer reconciliation. Narrower applicable populations never delete rows from the complete ledger.

The eleven conjuncts for `c∈E` are: valid window; stable independent pair; complete requests; complete construction; artifact inclusion; accepted alignment policy; `BOTH_SIDE_USABLE`; exact `S2_GATE_CLEAR`; approved Sentinel clear review; matching reconciliation identities; and a valid S10 activity root formed from Gustavo authorization followed by Sentinel narrow-stage authorization. Any failed conjunct places `c` in `I` with ordered failure reasons.

### 2.4 Effects, gate, and review distinctions

Effect precedence remains:

`BLOCKING_DEFECT > INCOMPLETE_EVIDENCE > LIMITATION > VALID_EXCLUSION > CLEAR_COMPONENT`

- `VALID_EXCLUSION` is immutable, counted, not acquisition/alignment applicable, compatible with exact global clear when every applicable check passes, and always consumer-ineligible.
- `LIMITATION` is completed evidence that prevents exact clear but is not incomplete or blocking.
- `INCOMPLETE_EVIDENCE` means a required observation or closure is missing.
- `BLOCKING_DEFECT` means contradictory, malformed, unauthorized, leakage-bearing, identity-invalid, or otherwise nonconforming evidence.

Gate reducer:

- any blocking effect → `S2_GATE_BLOCKED`;
- otherwise any incomplete effect → `S2_GATE_INCOMPLETE`;
- otherwise any limitation → `S2_GATE_CLEAR_WITH_LIMITATIONS`;
- otherwise all nineteen checks PASS, rebuild PASS, complete 39,693 reconciliation, and every alignment-applicable condition both-side usable → `S2_GATE_CLEAR`.

Sentinel may `ACCEPT FINDING` for a conforming blocked or limited result without unblocking S10 or P1. Acceptance of evidence is not gate clearance; gate clearance is not activity authorization; no finding automatically changes canonical state.

### 2.5 Mandatory handoff and denominator invariants

Every activity handoff MUST:

1. be created after the exact deliverable bytes it reports;
2. bind exact prerequisite acceptance bytes;
3. bind the exact Gustavo authorization and the later Sentinel stage authorization;
4. bind the exact activity root and canonical commit;
5. list deliverable path, byte length, SHA-256, and ID;
6. preserve valid exclusions, limitations, incomplete stops, and blocking stops in distinct arrays;
7. retain every emitted evidence identity even for blocked, incomplete, or limited outcomes;
8. list activities performed and explicitly not performed;
9. avoid a completion or sealed-candidate label when the identified deliverable does not exist;
10. prohibit successor activity until a new Gustavo authorization and later Sentinel stage authorization create the successor root.

Every population reconciliation MUST be keyed by unique `condition_id`; MUST preserve all 39,693 rows in the complete effect ledger; MUST NOT treat missing evidence as negative evidence; and MUST NOT reduce a denominator by omitting missing anchors, failed requests, or invalid identities.

---

## 3. Explicit scientific projections and deterministic identity

### 3.1 Canonical serialization rule

All three scientific projections use UTF-8 RFC 8785 JCS. Token IDs and request IDs are canonical strings; timestamps are integer UTC milliseconds or integer source seconds as named; prices are canonical decimal strings, never binary floating-point values. Arrays use the exact ordering stated below.

For projection `X`:

`projection_sha256 = SHA256(UTF8(JCS(X)))`

`projection_id = "<projection-kind>:sha256:" + projection_sha256`

For one complete source artifact and one projection-profile ID, exactly one projection SHA-256 is legal. Two different projection hashes for the same source identity and profile are `SCIENTIFIC_PROJECTION_CONFLICT`.

### 3.2 Projection nodes

| Node | Exact source artifact | Included scientific fields | Excluded activity/provenance fields | Ordering and identity | Provenance wrapper and audit proof |
|---|---|---|---|---|---|
| `A003` S4 scientific processing-ledger projection | complete `K037` S4 processing ledger | schema/profile ID; canonical commit; row count; per row: `condition_id`, subclass, window status, nullable decision-lower ms, nullable resolution ms, token-pair status, nullable side token IDs, nullable outcome indexes, immutable processing disposition and reason | Gustavo/Sentinel authorization IDs; activity root/run ID; actor; host; environment; created/modified time; handoff/review IDs; source path metadata not scientifically consumed | rows sorted by UTF-8 `condition_id`; identity by JCS SHA-256 | `A004` binds `K035`, `K036`, exact `K037` path/length/SHA, exact `A003` path/length/SHA/profile; `K110`, `K119`, and `K124` verify the link |
| `A005` scientific request-plan projection | `K056F` plan-row family plus complete `K057` plan manifest | schema/profile ID; accepted span-policy ID; canonical commit; row count; per row: condition, token, outcome index, request ID, chunk ordinal, start/end seconds, fidelity, interval-null marker, HTTP method/route and deterministic request parameters | authorization/root/run IDs; actor; environment; planning or execution timestamps; progress/retry logs; handoff IDs | sort by condition ID, outcome index, chunk ordinal, request ID; identity by JCS SHA-256 | `A006` binds `K055`, exact `K056F` family identity, exact `K057` path/length/SHA, and `A005`; `K114`, `K115`, `K119`, and `K124` verify the link |
| `A007` scientific raw-payload root | raw archive `K062`, closed by inventory `K060`, completion `K061`, and detached identity `K063` | schema/profile ID; canonical commit; request-plan projection ID; ordered entries containing request ID, token ID, outcome index, chunk ordinal, terminal scientific code, nullable payload logical path, nullable payload byte length/SHA; payload entries identify exact raw response bytes consumed by construction | activity authorizations, root/run ID, actor, host, environment, receipt wall-clock time, progress/log members, handoffs, review records | entries sorted by request ID then payload path; root SHA-256 over JCS inventory; construction independently verifies each payload member byte hash before parsing | `A008` binds `K055`, `K060`–`K063`, exact archive and detached identities, exact member coverage, and `A007`; `K116`, `K119`, `K124`, and `K125` verify the link |

`A003`, `A005`, and `A007` are scientific identities. `A004`, `A006`, and `A008` are non-byte-compared provenance wrappers.

### 3.3 Shared deterministic build identity

Candidate 03 §4.1 is replaced by:

`deterministic_build_id = SHA256(UTF8(JCS(preimage)))`

with exact preimage:

1. `schema_id = "pm_research.s2.deterministic_build_identity.v2"`;
2. canonical commit identity `K000`;
3. accepted construction-contract ID/path/length/SHA-256 `K068`;
4. S4 scientific projection ID and SHA-256 `A003`;
5. scientific request-plan projection ID and SHA-256 `A005`;
6. scientific raw-payload-root ID and SHA-256 `A007`;
7. deterministic serialization-profile ID;
8. deterministic construction-algorithm ID.

No prose-described projection of `K037`, `K057`, or `K063` is permitted. Original and rebuild MUST use these same three explicit identities.

### 3.4 Compared and non-compared artifacts

Byte-compared pairs:

- original partitions `K073F` ↔ rebuilt partitions `K096F`;
- original scientific manifest `K074` ↔ rebuilt scientific manifest `K097`;
- original scientific construction reconciliation `K075` ↔ rebuilt scientific construction reconciliation `K098`.

Each compared byte stream MUST contain the same `deterministic_build_id` and MUST exclude authorization IDs, stage-authorization IDs, activity roots, execution/rebuild run IDs, actors, environments, and execution timestamps.

Intentionally non-byte-compared provenance includes `A004`, `A006`, `A008`, `K076`, `K095`, `K099`, `K100`, `K101`, all control records, roots, run IDs, actors, environments, timestamps, reviews, and handoffs.

### 3.5 Corrected row key

`row_key_sha256 = SHA256(UTF8(JCS({`
`"schema_id":"pm_research.s2.price_row_key.v2",`
`"deterministic_build_id":K072,`
`"condition_id":condition_id,`
`"token_id":token_id,`
`"outcome_index":outcome_index,`
`"price_ts_utc_ms":price_ts_utc_ms,`
`"deterministic_source_row_id":deterministic_source_row_id`
`})))`

`deterministic_source_row_id` is derived only from `A007` predecessor evidence: request ID, payload-member SHA-256, raw-point ordinal, normalized source timestamp, and canonical decimal price.

The row key MUST NOT use original or rebuild activity IDs, roots, run IDs, actors, timestamps, or any descendant partition, manifest, reconciliation, inventory, archive, comparison, review, or handoff identity. Rebuild MUST compute the key from `A003`, `A005`, and `A007`; it MUST NOT read original output bytes as a key source.

---

## 4. Complete authorization-chain audit evidence

### 4.1 Referenced acceptance bytes are mandatory

`authorization_and_handoff_provenance` MUST independently load and verify each prerequisite acceptance record's exact path, byte length, SHA-256, canonical commit, decision, decision code, and accepted deliverable identities. A copied acceptance ID without the referenced acceptance bytes is `AUTHORIZATION_PREREQUISITE_BYTES_MISSING`.

The exact accepted prerequisite records are:

- controlling normalization `A002`;
- Candidate 08 specification `K011`;
- implementation source `K018`;
- test source `K025`;
- test result `K032`;
- S4 result `K041`;
- span policy `K051` and accepted review handoff `K052P`;
- S6 result `K067`;
- accepted construction contract `K068`;
- S7 result `K079`;
- alignment policy `K082` and accepted review handoff `K083P`;
- S8A result `K091`;
- S8B result `K104`.

For each completed activity through S8B, the closure MUST bind in order: prerequisite acceptance bytes, Gustavo authorization, later Sentinel narrow-stage authorization, activity root, and activity handoff.

For the currently executing S8C audit, `A009` is a distinct activity-completion handoff created after the condition-effect ledger and the first eighteen closure records `K109`–`K126`, but before `K127`. It binds `K106`, `K105`, `K107`, and those deliverables. `K127` then audits `A009`. The later `K132` is the final result-review handoff after gate production and is reviewed independently by S9; it cannot be an input to its own gate without a cycle.

### 4.2 Exact amended evidence sets

The following closure predecessor sets replace Candidate 03's corresponding sets; all other check evidence sets remain unchanged.

| Check | Closure | Exact ordered evidence-node set |
|---|---|---|
| `canonical_base_integrity` | `K109` | `K000`, `K001`, `A002`, `K011`, `K068` |
| `complete_universe_reconciliation` | `K110` | `K036`, `K037`, `A003`, `A004`, `K038`, `K041` |
| `request_plan_integrity` | `K114` | `K051`, `K052P`, `K056F`, `K057`, `A005`, `A006` |
| `request_terminal_completeness` | `K115` | `K057`, `A005`, `A006`, `K058F`, `K059F`, `K061`, `K064` |
| `raw_archive_closure` | `K116` | `K060`, `K061`, `K062`, `K063`, `A007`, `A008` |
| `independent_token_acquisition` | `K117` | `K056F`, `K057`, `A005`, `K058F`, `K059F`, `K064` |
| `no_synthesis_integrity` | `K118` | `K057`, `A005`, `K059F`, `K073F`, `K074`, `K096F`, `K097` |
| `original_construction_integrity` | `K119` | `A003`, `A004`, `A005`, `A006`, `A007`, `A008`, `K072`, `K073F`, `K074`, `K075`, `K076` |
| `deterministic_build_identity` | `K124` | `K000`, `K068`, `A003`, `A004`, `A005`, `A006`, `A007`, `A008`, `K072`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098` |
| `deterministic_rebuild_byte_equality` | `K125` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K100`, `K101` |
| `authorization_and_handoff_provenance` | `K127` | `A002`, `K011`, `K018`, `K025`, `K032`, `K041`, `K051`, `K052P`, `K067`, `K068`, `K079`, `K082`, `K083P`, `K091`, `K104`, `K006`, `K005`, `K007`, `K009`, `K013`, `K012`, `K014`, `K016`, `K020`, `K019`, `K021`, `K023`, `K027`, `K026`, `K028`, `K030`, `K034`, `K033`, `K035`, `K039`, `K043`, `K042`, `K044`, `K048`, `K054`, `K053`, `K055`, `K065`, `K070`, `K069`, `K071`, `K077`, `K085`, `K084`, `K086`, `K089`, `K093`, `K092`, `K094`, `K102`, `K106`, `K105`, `K107`, `A009` |

Missing any listed node is `INCOMPLETE`. Identity mismatch, wrong ordering, authorization scope expansion, missing referenced bytes, or a Sentinel authorization timestamp/identity preceding its Gustavo authorization is `FAIL` with blocking effect.

---

## 5. Authoritative graph registry and attestation

### 5.1 Chosen attestation method

This amendment chooses option 2: the direct-edge table is the authoritative architecture edge registry.

Candidate 03's claim that edges were derived from registry predecessor fields is removed. Candidate 03's artifact registry remains descriptive for artifact class and producer, but it is not an edge source.

The accepted edge registry IS:

`Candidate03 §5.1 direct-edge table`
`minus every target row replaced or removed in §5.4 below`
`plus every replacement row in §5.4 below`.

Candidate 08 MUST derive every schema-implied edge mechanically from every field carrying an ID, path, byte length, SHA-256, count, or identified content dependency. The derived set MUST equal this accepted edge registry exactly. Any omitted or extra edge is `PROVENANCE_EDGE_SET_MISMATCH`.

### 5.2 New and removed nodes

`K003` and `K004` are removed from the controlling graph and replaced by `A000`–`A002`.

| Node | Amended rank | Artifact | Class | Exact predecessors |
|---|---:|---|---|---|
| `A000` | `1021` | Amendment 01 exact bytes | architecture amendment candidate | `K000`, `K001`, `K002` |
| `A001` | `1022` | Sentinel combined architecture review record | review decision | `K002`, `A000` |
| `A002` | `1023` | Accepted controlling architecture-set record | accepted record | `K002`, `A000`, `A001` |
| `A003` | `1371` | S4 scientific processing-ledger projection | scientific projection | `K037` |
| `A004` | `1372` | S4 projection provenance wrapper | provenance wrapper | `K035`, `K036`, `K037`, `A003` |
| `A005` | `1581` | Scientific full-request-plan projection | scientific projection | `K056F`, `K057` |
| `A006` | `1582` | Request-plan projection provenance wrapper | provenance wrapper | `K055`, `K056F`, `K057`, `A005` |
| `A007` | `1641` | Scientific raw-payload root | scientific projection/root | `K060`, `K061`, `K062`, `K063` |
| `A008` | `1642` | Raw-payload projection provenance wrapper | provenance wrapper | `K055`, `K060`, `K061`, `K062`, `K063`, `A007` |
| `A009` | `2315` | S8C activity-completion handoff used by authorization audit | handoff | `K106`, `K105`, `K107`, `K108`, `K109`–`K126` |

For `A009`, `K109`–`K126` means every individual closure node in that inclusive range; the authoritative edge registry below lists them individually.

### 5.3 Rank rule and graph totals

- Every retained non-overridden Candidate-03 node uses `1000 + 10×old_rank`.
- The thirteen Gustavo/Sentinel pairs use §1.3's swapped ranks.
- New nodes use §5.2's explicit ranks.
- Removed nodes have no rank.
- Every authoritative edge has `rank(source) < rank(target)`.

Graph totals after applying this amendment:

| Metric | Exact result |
|---|---:|
| Candidate-03 nodes | 158 |
| removed nodes | 2 |
| added nodes | 10 |
| amended nodes/node families | 166 |
| Candidate-03 direct edges | 557 |
| old edges in replaced/removed target rows | 345 |
| new edges in replacement target rows | 466 |
| amended direct edges | 678 |
| direct cycles | 0 |
| indirect cycles | 0 |

### 5.4 Exact replacement target rows

For every target below, this row fully replaces Candidate 03 §5.1's row. `REMOVED` deletes the node and all incident edges. Every unlisted target retains Candidate 03's exact predecessor set.

| Target | Exact direct predecessors |
|---|---|
| `K003` | `REMOVED` |
| `K004` | `REMOVED` |
| `A000` | `K000`, `K001`, `K002` |
| `A001` | `K002`, `A000` |
| `A002` | `K002`, `A000`, `A001` |
| `K006` | `A002` |
| `K005` | `A002`, `K006` |
| `K007` | `A002`, `K006`, `K005` |
| `K009` | `K006`, `K005`, `K007`, `K008` |
| `K013` | `K011` |
| `K012` | `K011`, `K013` |
| `K014` | `K011`, `K013`, `K012` |
| `K016` | `K013`, `K012`, `K014`, `K015` |
| `K020` | `K018` |
| `K019` | `K018`, `K020` |
| `K021` | `K018`, `K020`, `K019` |
| `K023` | `K020`, `K019`, `K021`, `K022` |
| `K027` | `K018`, `K025` |
| `K026` | `K018`, `K025`, `K027` |
| `K028` | `K018`, `K025`, `K027`, `K026` |
| `K030` | `K027`, `K026`, `K028`, `K029` |
| `K034` | `K032` |
| `K033` | `K032`, `K034` |
| `K035` | `K032`, `K034`, `K033` |
| `A003` | `K037` |
| `A004` | `K035`, `K036`, `K037`, `A003` |
| `K038` | `K035`, `K037`, `A003`, `A004` |
| `K039` | `K034`, `K033`, `K035`, `K036`, `K037`, `A003`, `A004`, `K038` |
| `K043` | `K041` |
| `K042` | `K041`, `K043` |
| `K044` | `K041`, `K043`, `K042` |
| `K048` | `K043`, `K042`, `K044`, `K045`, `K046`, `K047` |
| `K054` | `K041`, `K051`, `K052P` |
| `K053` | `K041`, `K051`, `K052P`, `K054` |
| `K055` | `K041`, `K051`, `K052P`, `K054`, `K053` |
| `A005` | `K056F`, `K057` |
| `A006` | `K055`, `K056F`, `K057`, `A005` |
| `A007` | `K060`, `K061`, `K062`, `K063` |
| `A008` | `K055`, `K060`, `K061`, `K062`, `K063`, `A007` |
| `K064` | `K037`, `A003`, `A004`, `K057`, `A005`, `A006`, `K059F`, `K061`, `K063`, `A007`, `A008` |
| `K065` | `K054`, `K053`, `K055`, `K057`, `A005`, `A006`, `K060`, `K061`, `K062`, `K063`, `A007`, `A008`, `K064` |
| `K070` | `K067`, `K068` |
| `K069` | `K067`, `K068`, `K070` |
| `K071` | `K067`, `K068`, `K070`, `K069` |
| `K072` | `K000`, `K068`, `A003`, `A005`, `A007` |
| `K073F` | `A007`, `K072` |
| `K075` | `A003`, `A005`, `A007`, `K072`, `K074` |
| `K076` | `K070`, `K069`, `K071`, `A004`, `A006`, `A008`, `K072`, `K073F`, `K074`, `K075` |
| `K077` | `K070`, `K069`, `K071`, `K074`, `K075`, `K076` |
| `K085` | `K079`, `K082`, `K083P` |
| `K084` | `K079`, `K082`, `K083P`, `K085` |
| `K086` | `K079`, `K082`, `K083P`, `K085`, `K084` |
| `K093` | `K091` |
| `K092` | `K091`, `K093` |
| `K094` | `K091`, `K093`, `K092` |
| `K095` | `K093`, `K092`, `K094`, `K072`, `A003`, `A005`, `A007` |
| `K096F` | `A007`, `K072` |
| `K098` | `A003`, `A005`, `A007`, `K072`, `K097` |
| `K099` | `K093`, `K092`, `K094`, `K095`, `A004`, `A006`, `A008`, `K096F`, `K097`, `K098` |
| `K100` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K094` |
| `K101` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K099`, `K100` |
| `K102` | `K093`, `K092`, `K094`, `K095`, `K099`, `K100`, `K101` |
| `K106` | `K104` |
| `K105` | `K104`, `K106` |
| `K107` | `K104`, `K106`, `K105` |
| `K109` | `K000`, `K001`, `A002`, `K011`, `K068` |
| `K110` | `K036`, `K037`, `A003`, `A004`, `K038`, `K041` |
| `K114` | `K051`, `K052P`, `K056F`, `K057`, `A005`, `A006` |
| `K115` | `K057`, `A005`, `A006`, `K058F`, `K059F`, `K061`, `K064` |
| `K116` | `K060`, `K061`, `K062`, `K063`, `A007`, `A008` |
| `K117` | `K056F`, `K057`, `A005`, `K058F`, `K059F`, `K064` |
| `K118` | `K057`, `A005`, `K059F`, `K073F`, `K074`, `K096F`, `K097` |
| `K119` | `A003`, `A004`, `A005`, `A006`, `A007`, `A008`, `K072`, `K073F`, `K074`, `K075`, `K076` |
| `K124` | `K000`, `K068`, `A003`, `A004`, `A005`, `A006`, `A007`, `A008`, `K072`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098` |
| `K125` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K100`, `K101` |
| `A009` | `K106`, `K105`, `K107`, `K108`, `K109`, `K110`, `K111`, `K112`, `K113`, `K114`, `K115`, `K116`, `K117`, `K118`, `K119`, `K120`, `K121`, `K122`, `K123`, `K124`, `K125`, `K126` |
| `K127` | `A002`, `K011`, `K018`, `K025`, `K032`, `K041`, `K051`, `K052P`, `K067`, `K068`, `K079`, `K082`, `K083P`, `K091`, `K104`, `K006`, `K005`, `K007`, `K009`, `K013`, `K012`, `K014`, `K016`, `K020`, `K019`, `K021`, `K023`, `K027`, `K026`, `K028`, `K030`, `K034`, `K033`, `K035`, `K039`, `K043`, `K042`, `K044`, `K048`, `K054`, `K053`, `K055`, `K065`, `K070`, `K069`, `K071`, `K077`, `K085`, `K084`, `K086`, `K089`, `K093`, `K092`, `K094`, `K102`, `K106`, `K105`, `K107`, `A009` |
| `K132` | `K106`, `K105`, `K107`, `K108`, `K128`, `K129`, `K130`, `K131` |
| `K139` | `K137` |
| `K138` | `K137`, `K139` |
| `K140` | `K137`, `K139`, `K138` |
| `K141` | `K037`, `K108`, `K129`, `K134`, `K135`, `K139`, `K138`, `K140` |
| `K142I` | `K139`, `K138`, `K140`, `K141` |
| `K143I` | `K139`, `K138`, `K140`, `K141`, `K142I` |
| `K142E` | `A002`, `K011`, `K139`, `K138`, `K140`, `K141` |
| `K143E` | `K139`, `K138`, `K140`, `K141`, `K142E` |
| `K144E` | `K139`, `K138`, `K140`, `K141`, `K142E`, `K143E` |
| `K148` | `K146E` |
| `K147` | `K146E`, `K148` |
| `K149` | `K146E`, `K148`, `K147` |

### 5.5 Cycle and closure proof

A mechanical topological check over the amended registry proves:

1. all `166` target nodes exist exactly once;
2. all `678` predecessors exist;
3. every edge points to a strictly later amended rank;
4. depth-first search finds zero direct or indirect cycles;
5. the exact evidence-node arrays in §4.2 equal the corresponding authoritative predecessor sets for `K109`, `K110`, `K114`–`K119`, `K124`, `K125`, and `K127`;
6. archive bytes `K062` precede detached identity `K063`;
7. projection identities precede `K072` and both scientific chains;
8. every Gustavo authorization precedes the Sentinel stage authorization that binds it;
9. every activity root and handoff follow both control records;
10. `A009` precedes `K127`, while final H8C `K132` remains after gate production;
11. no candidate, policy, projection, row key, review, handoff, detached identity, or transition record contains a descendant identity.

The strongest attempted cycle is to place an activity-root ID in a scientific projection, derive `K072`, serialize it into original outputs, then require rebuilt bytes produced under another root to match. The projection schemas forbid activity fields; only provenance wrappers contain them. The attempted edge therefore does not exist.

---

## 6. Focused counterexamples

| Counterexample | Required result |
|---|---|
| Sentinel issues `K053` before Gustavo `K054` exists | `STOP_AUTHORIZATION_ORDER_INVALID`; no `K055`; no S6 work |
| Gustavo issues `K070`, but Sentinel never issues `K069` | no `K071`; no construction despite Gustavo permission |
| Sentinel accepts S6 result `K067`, but Gustavo does not authorize S7 | lifecycle remains at accepted S6; no automatic progression |
| Accepted architecture references blocked Candidate 02 | `ARCHITECTURE_CONTROL_SET_INVALID`; only Candidate 03 exact bytes plus Amendment 01 exact bytes may form `A002` |
| Two different `A003` hashes are produced from the same `K037` identity and projection profile | `SCIENTIFIC_PROJECTION_CONFLICT`; deterministic build blocked |
| Original manifest embeds `K071` while rebuild manifest embeds `K094` | deterministic bytes differ; `K125=FAIL`; gate blocked |
| Rebuilt row key uses rebuild run ID | `ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN`; rebuild invalid |
| Authorization audit contains `K032` as a copied ID but cannot load its recorded bytes | `AUTHORIZATION_PREREQUISITE_BYTES_MISSING`; `K127=INCOMPLETE` |
| Raw-payload projection contains an archive log member or omits a scientific payload member | `SCIENTIFIC_RAW_PROJECTION_MISMATCH`; raw closure/build identity fail |
| A hand-authored edge table omits `A007→K072` but a future schema contains `raw_payload_root_id` | Candidate-08 derived edges differ; `PROVENANCE_EDGE_SET_MISMATCH` |
| `K132` is inserted into `K127` to audit its own handoff | direct cycle; rejected; `A009` is the causally prior activity handoff |
| Candidate 08 depends directly on Candidate 02 | nonconforming dependency; no Candidate-08 drafting root |

---

## 7. Candidate-08 mandatory amendment constraints

Once, and only once, the controlling architecture set is accepted, any future Candidate 08 MUST:

1. bind `A002`, which identifies Candidate 03 exact bytes plus Amendment 01 exact bytes, with Amendment 01 controlling on conflict;
2. implement every activity ladder as prerequisite acceptance → Gustavo authorization → later Sentinel stage authorization → activity root;
3. prohibit Sentinel stage authorization until the exact Gustavo record has been verified;
4. make the Sentinel stage record bind Gustavo ID/path/length/SHA/scope/canonical commit and forbid scope expansion;
5. create and schema-lock exactly one `A003`, `A005`, and `A007` projection per source identity/profile;
6. keep `A004`, `A006`, and `A008` as non-byte-compared provenance wrappers;
7. derive `K072` only from `K000`, `K068`, `A003`, `A005`, `A007`, and fixed algorithm/profile identities;
8. byte-compare only `K073F/K096F`, `K074/K097`, and `K075/K098`;
9. use the amended row-key preimage and forbid every activity or descendant identity;
10. materialize the safe-span reducer, alignment interface, millisecond boundary, population equations, gate distinctions, and handoff/denominator invariants in §2;
11. materialize the complete `K127` prerequisite-byte and activity-chain audit, including `A009`;
12. treat the amended direct-edge table as the accepted architecture edge registry;
13. mechanically derive schema-implied edges and prove exact equality before specification acceptance;
14. preserve exact Stage-10 ineligible and eligible orders and all P1/probe blocks;
15. add no authorization or execution effect to the architecture documents.

This amendment does not authorize Candidate-08 drafting.

---

## 8. Focused self-attack

| Attack | Strongest attempt | Required defense | Acceptance blocker |
|---|---|---|---|
| Sentinel-before-Gustavo | create stage authorization from prerequisite acceptance alone | stage record schema requires exact existing Gustavo bytes; rank and edge order place Gustavo first | any ladder row retaining old order |
| hidden Candidate-02 dependency | cite Candidate 02 for safe span or alignment semantics | §2 restates the complete retained rules; `A002` contains only Candidate 03 and Amendment 01 | any normative dependency on Candidate 01/02 |
| divergent scientific projections | original and rebuild independently choose different field subsets | one profile ID and one projection hash per complete source identity; wrappers prove source linkage | two accepted projection hashes for one source/profile |
| ID-only authorization audit | copy acceptance IDs without loading bytes | K127 verifies exact path/length/SHA and accepted contents | missing referenced bytes can pass |
| manual graph misrepresented as derived | call Candidate-03 registry a predecessor registry | §5 declares the direct-edge table authoritative; Candidate 08 performs actual schema derivation and equality | any claim of mechanical derivation without schemas |
| activity leakage | place run/actor/time in A003/A005/A007 or compared outputs | projection and scientific-output exclusions are normative; provenance wrappers retain activity facts | any activity-specific field in compared bytes |
| self-auditing handoff cycle | require K127 to contain later K132 | A009 is the prior activity-completion handoff; K132 is later review submission | K132 becomes K127 predecessor |
| omitted audit edge | projection wrapper exists but closure ignores it | §4.2 and §5.4 must be identical | evidence array differs from edge registry |

**Strongest remaining false-unblock path.** A future specification could correctly model all records but treat the later Sentinel stage authorization as a formality that silently broadens Gustavo's scope. This amendment blocks that path by requiring exact scope equality or narrowing and by making any expansion a blocking authorization failure.

**Open decisions.** No new architecture decision is left open by this amendment. Actual safe span, alignment selector, numeric staleness/skew limits, empirical coverage, gate result, and consumer-eligible subset remain future evidence or policy decisions and are not selected here.

---

## 9. Acceptance evidence and authorization statement

Sentinel review can inspect:

- canonical `main` equality at `794fb60d8604e7f40d02bb0371aca55fef4ec7ec`;
- Candidate 03 exact identity: `68637` bytes and `6f67619df07e5017c469b6cd8ac9a190c6f66a3e263b2930f8f3997fb7e5b1c2`;
- one explicit controlling-set rule with no Candidate-01/02 dependency;
- thirteen corrected Gustavo-before-Sentinel activity ladders;
- three explicit scientific projections and three provenance wrappers;
- one shared activity-free deterministic build identity;
- one activity-free row-key preimage;
- exact prerequisite-byte evidence and activity-chain evidence for `K127`;
- authoritative edge-registry method;
- `166` nodes/node families, `678` direct edges, strict rank increase, and zero cycles;
- audit-evidence arrays equal to the amended authoritative edge rows.

**Authorization statement.** This amendment returns to Sentinel for architecture review only. It authorizes no Candidate-08 drafting, implementation, test authoring or execution, data access, preflight, network activity, acquisition, construction, alignment, rebuild, audit, transition, P1/P2/P3, scoring, probe execution, canonical change, or Git action. Professor does not approve its own amendment.

**Requested Sentinel decision:** `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.
