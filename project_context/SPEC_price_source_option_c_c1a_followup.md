# SPEC — Option C C1A follow-up after `C1_ROW_EXPLOSION` — SPEC ONLY

**Decision posture:** NEEDS VERIFICATION — SPEC ONLY follow-up recommendation for Orchestrator review.

**Status:** Proposed for review. This document is not acceptance, not implementation authorization, and not data-run authorization.

**Scope:** Decide whether a safe C1A follow-up design exists after the accepted C1A `C1_ROW_EXPLOSION` halt, and define the only narrow form in which such a follow-up could remain a bounded canary rather than become C1B/C2/full-indexer work.

**Canonical source:** `rigolugo/pm_research`. Read order followed from `START_HERE.md` and `project_context/START_HERE.md`, including the current guardrails, project state, decision log, artifact index, S0 price-input contract, S1/S1-ALT/Option B history, Option C Revision 3, C1R addendum, C1A README, C1A result handoff, parser-fix handoffs, Dune notes, and accepted C1A artifacts.

**Hard boundary:** This is a document-only specification. No implementation, code, tests, Dune/API/RPC/network call, query generation, artifact mutation, cap increase, row truncation, ad hoc window narrowing, C1B/C2/P1/P2/P3/probe, scoring/backfill/wallet discovery/OrdersMatched expansion/`log_index`/PnL, price artifact, `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis is authorized or proposed here.

---

## 1. Standing accepted state

C1A is accepted as a valid bounded-canary halt:

- selector manifest completed with `resolved_count = 5`, `excluded_count = 0`;
- canary outcome was `C1_ROW_EXPLOSION`;
- condition `0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e` returned `2001` rows against `per_condition_row_cap = 2000`;
- the SQL was intentionally generated with `LIMIT per_condition_row_cap + 1`, so the halt proves cap exceedance rather than silent truncation;
- the result is coverage/trust diagnostic only, not a price-source viability verdict;
- no price was computed or persisted;
- P1 remains blocked;
- C1B, C2, P1/P2/P3, and probe execution remain unauthorized;
- `named_binary_probe_blocked` remains `true`.

The accepted C1A report also recorded useful diagnostic shape, but it does not authorize using those rows to hand-pick a new manifest. The reported counts are evidence explaining the halt, not a selector source for the next candidate set.

---

## 2. Why the accepted C1A design halted

C1A halted because the bounded query pattern, when applied to the fixed manifest, produced more than the allowed per-condition row budget for one condition/window/token-pair branch.

This is the intended fail-fast behavior of C1R/C1A:

- each condition branch over-fetches by one row (`cap + 1`);
- each branch is subquery-wrapped so the limit is per-condition, not accidentally applied to the full `UNION ALL`;
- the canary reads the returned rows and halts if any per-condition count exceeds the hard cap;
- it does not truncate the overflow and continue.

The halt therefore means:

> At least one fixed condition/window/token-pair selector can exceed the C1A per-condition row budget under the accepted query shape.

It does **not** mean:

- Option C is viable;
- Option C is not viable;
- C1B may begin;
- C2 may be built;
- P1 is unblocked;
- a price artifact exists;
- one can synthesize missing side prices.

---

## 3. Implementation bugs already fixed vs. the real row-explosion finding

The accepted C1A path included implementation/parser defects that were fixed before the final result was accepted. Those defects must not be confused with the row-explosion finding.

### 3.1 Fixed implementation/query-shape defects

Already fixed before accepted C1A interpretation:

1. **SQL truncation masking risk:** earlier generated SQL used the exact cap as `LIMIT`, which could hide overflow. Fixed by using `per_condition_row_cap + 1`.
2. **Per-branch limit scoping risk:** branch-level `LIMIT` needed subquery wrapping so it could not bind to the full union. Fixed by wrapping each condition branch.
3. **Empty export risk:** zero returned Dune rows must not self-clear; fixed as `C1_SOURCE_EMPTY`.
4. **Automatic self-certification risk:** a non-halt run must not automatically emit `C1_CANARY_DESIGN_CLEAR`; fixed to require review.
5. **Manifest timestamp parser defect:** local `Store.load_trades().traded_at` can be datetime-like / pandas `Timestamp`; parser was fixed.
6. **Canary CSV/timestamp parser defect:** Dune CSV timestamps such as `YYYY-MM-DD HH:MM:SS.fff UTC` and UTF-8 BOM headers needed tolerant parsing; parser was fixed.

These are tool correctness fixes. They are not evidence for or against source viability.

### 3.2 Real accepted finding

After the fixes, the accepted result is a real bounded-canary halt: one condition exceeded the hard row cap. The next question is therefore not “fix a parser” or “increase the cap”; it is whether an objective, pre-declared selector policy can keep a follow-up canary within the same caps while still testing the mechanism in a non-tautological way.

---

## 4. Follow-up design question

The only safe follow-up question is:

> Can a pre-declared, outcome-independent, local-identity/static-metadata selector choose 3–5 conditions that are likely enough to stay within C1A caps to test the canary mechanism, without hand-picking after seeing C1A rows and without reducing the test to local-`tx_hash` reproduction?

This is a selector-design question only. It is not a new query, not a run, and not a price-source decision.

---

## 5. Candidate-selection alternatives evaluated

### 5.1 Reject — re-run the same manifest after dropping only the exploding condition

Rejected.

Dropping only `0x00e0...fc8e` after seeing that it exploded is hand-picking after the result. It would convert the accepted halt into a post-hoc pruning rule. Even though it would not use winner fields, it would use C1A result knowledge directly.

### 5.2 Reject — increase per-condition or global caps

Rejected.

The C1R ceiling is `per_condition_row_cap <= 2000` and `global_row_cap <= 6000`. The accepted halt proves the current design can hit the per-condition ceiling. Increasing caps would be a fresh cap-policy revision, not a safe C1A follow-up.

### 5.3 Reject — truncate rows at the cap and continue

Rejected.

Truncation would erase the exact evidence C1A was designed to detect. A truncated branch cannot support a coverage/trust diagnostic because it masks whether more rows existed.

### 5.4 Reject — narrow the exploding condition’s window after seeing the halt

Rejected.

Ad hoc narrowing after seeing overflow is equivalent to tuning the observation window against the result. It also risks making the window no longer comparable to the local decision/time anchor discipline.

### 5.5 Reject — use a local `tx_hash` list as the Dune filter

Rejected.

This is the original Revision-3 Branch 1 trap. A source query filtered to local `tx_hash` values can never discover rows the local store is missing by construction. It may be bounded, but it is not a coverage test for the open question.

### 5.6 Reject — scout Dune counts first, then select low-count conditions

Rejected.

A Dune count preflight would itself be a new data run and would use source-result knowledge to shape the manifest. It is also close to an indexer-shaped “query first, decide sample later” workflow. It is not an acceptable selector source for a C1A follow-up.

### 5.7 Reject — select using winner, resolution, outcome, profit, or score fields

Rejected.

The selector must not read or use `resolved_winning_token_id`, `resolved_winning_outcome_index`, `resolved_winning_label`, payout-vector winner fields, price-convergence outcomes, realized winner fields, profit/PnL fields, score fields, or any field that conditions the selected candidates on which side won.

The selector may use the already accepted static universe status needed to reproduce the P0 eligible universe, but it must read only non-winner fields needed for eligibility and identity, such as `condition_id`, subclass, version/status sanity fields, and local trade-side token identities. It must not read the winner columns.

### 5.8 Conditionally viable — deterministic local-density selector, fixed before any new run

Conditionally viable as SPEC ONLY.

A C1A follow-up can remain safe if it uses a deterministic, pre-declared selector based only on local, outcome-independent data already in the project scope, with an explicit selector-universe boundary:

- default selector pool: the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool, not the full project universe;
- P0-eligible non-YES/NO condition identity only as an eligibility constraint within that bounded selector pool unless broader local-only computation is separately authorized by the Orchestrator;
- subclass (`UP_DOWN`, `OVER_UNDER`, `NAMED_OTHER`);
- exact two stable side-token identities from local distinct `(condition_id, token_id, outcome_index)` tuples;
- local trade-count or local distinct-tx-count inside the same deterministic fixed window rule used for all candidates;
- window duration under the same deterministic fixed window rule;
- optional prior coverage-status labels from accepted coverage-only artifacts only if they are used as coarse static feasibility filters and not as price, winner, profit, or scoring inputs;
- deterministic hash tie-breaker over `condition_id` and a versioned selector-policy string.

This approach does not filter the Dune query by local `tx_hash`. It uses local density only as a weak, outcome-independent proxy for choosing a small number of candidate condition/window/token-pair branches that may be less prone to row explosion under the unchanged caps. Local trade/local tx density is not a reliable estimator of on-chain OrderFilled row volume. A low-density local condition can still explode on Dune. If it does, that is informative and does not authorize cap increases, retries, truncation, or ad hoc window narrowing.

The accepted C1A diagnostics provide only a tiny empirical caution point: two non-empty Dune-returning examples, one of which was cap-truncated by the intentional `cap + 1` halt signal. Those examples must not be turned into constants, ratios, caps, filters, or guarantees. They explain why caution is required; they do not provide a calibrated selector model.

This remains a canary only if it is capped at 3–5 conditions, uses the same or lower row caps, produces coverage/trust diagnostics only, and cannot auto-advance to C1B/C2.

---

## 6. Proposed safe follow-up design: `C1A-F1` selector-policy addendum

A safe next step exists only as a new SPEC-only selector-policy addendum, tentatively named:

`C1A-F1` — deterministic low-density / balanced-subclass selector canary.

This document does not implement `C1A-F1`. It defines what such a later spec must contain before another C1A-style run can be considered.

### 6.1 C1A-F1 purpose

C1A-F1 would test whether the accepted C1A mechanism can produce a readable bounded diagnostic under an objective, pre-declared selector less prone to row explosion.

It would not test full Option C coverage and would not make a price-source viability decision.

### 6.2 Required selector inputs

A C1A-F1 selector policy must be fully specified before any new run and must state its selector-universe boundary. By default, the selector pool must be limited to the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool. It must not imply scanning or profiling the full approximately 288K-condition project universe, and it must not build a reusable volume-profiling artifact. Any broader local-only computation requires separate Orchestrator authorization before it is included in a selector policy.

Within that bounded default pool, a C1A-F1 selector may use only:

1. P0/non-YES/NO eligible condition identity and subclass as eligibility filters.
2. Local trade rows only to derive static token pairs, local trade-count, local distinct-tx-count, and deterministic fixed-window bounds.
3. Token IDs and outcome indexes as static identity fields.
4. Version/status sanity fields required to prove the candidate belongs to the accepted universe.
5. A deterministic tie-breaker: `sha256(condition_id || selector_policy_version)` or equivalent exact, predeclared hash input.

It must not use:

- prior C1A Dune row counts to choose individual conditions;
- any winner/outcome/resolution winner column;
- any realized PnL/score/forecast metric;
- any Dune count scout;
- local `tx_hash` lists as query filters;
- manual candidate edits after selector execution.

### 6.3 Required selector shape

A C1A-F1 selector must be stratified and deterministic:

1. **Candidate universe:** start from the default bounded selector pool: the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool. Within that pool, require non-YES/NO P0 eligibility and exactly two stable, string-safe side tokens from local `(condition_id, token_id, outcome_index)` enumeration. Do not scan or profile the full approximately 288K-condition universe unless the Orchestrator separately authorizes broader local-only computation.
2. **Window rule:** apply one deterministic fixed-window construction rule to every candidate. The rule must be declared in the C1A-F1 spec before implementation. It must not narrow individual windows after seeing Dune results.
3. **Density metric:** compute local density under that same window rule. Acceptable metrics: `local_trade_rows_in_window`, `local_distinct_tx_hash_count_in_window`, and `window_seconds`. These are selector diagnostics only, not query filters, not constants, and not guarantees of on-chain OrderFilled row volume.
4. **Strata:** prefer one candidate per subclass if available (`UP_DOWN`, `OVER_UNDER`, `NAMED_OTHER`). If one subclass has no eligible low-density candidate, record the empty stratum and do not silently backfill it with another subclass unless the spec predeclares an exact replacement rule.
5. **Local-density preference:** choose from the lowest non-empty local-density band that still has nonzero local evidence. A zero-local-evidence-only manifest is not acceptable because it risks an empty or non-comparable diagnostic.
6. **Sentinel condition:** include at most one medium-density sentinel if predeclared, to avoid a manifest that only tests near-empty markets. The sentinel must be selected by the same deterministic hash tie-breaker within its stratum, not by manual inspection.
7. **Tie-breaker:** all ties must resolve deterministically by the versioned hash rule, never manually.
8. **Prior C1A exposure:** if prior C1A conditions are excluded for holdout hygiene, the rule must exclude the entire prior C1A manifest uniformly, not only the exploding condition. This is optional; if used, it must be declared before selection and reported as a selector-policy field. It must not be used as a disguised manual drop of `0x00e0...fc8e` only.

### 6.4 Density-proxy caution

C1A-F1 may use local trade/local distinct-tx density only as a weak, pre-Dune proxy to avoid obvious high-local-density candidates inside the bounded selector pool. It must not claim that local density predicts Dune OrderFilled volume. The accepted C1A diagnostics provide only two non-empty Dune-returning examples, with one deliberately cap-truncated at `2001` rows to prove row explosion. Those observations are too small and too censored to calibrate a ratio, threshold, cap, filter, or guarantee.

A low-density local candidate can still produce `C1_ROW_EXPLOSION`. If it does, the halt is valid and informative. It does not authorize dropping only that condition, increasing caps, retrying until a clean set is found, truncating rows, or narrowing windows after the fact.

### 6.5 Required canary boundaries

A C1A-F1 run, if ever separately authorized after spec review and implementation review, must preserve C1A boundaries:

- condition count: 3–5 maximum;
- per-condition row cap: ≤ 2000;
- global row cap: ≤ 6000;
- decoded OrderFilled tables only;
- fixed token-pair/time-window query shape only;
- `cap + 1` over-fetch preserved;
- subquery-wrapped branch limits preserved;
- no row truncation;
- no Dune count scout;
- no local-`tx_hash` query filter;
- no OrdersMatched expansion;
- no price computation;
- no price artifact;
- no C1B/C2/P1/P2/P3/probe continuation.

### 6.6 Required C1A-F1 outcomes

A C1A-F1 canary, if later authorized and executed, may only produce one of these interpretation states:

- `C1F_SELECTOR_REJECTED` — selector policy could not produce a valid manifest under the stated rules.
- `C1_ROW_EXPLOSION` — unchanged C1A cap halt. If this recurs under low-density selector conditions, the C1A query mechanism should remain blocked for larger work until a fresh spec explains why continuing would not be cap-evasion.
- `C1_SOURCE_EMPTY` — empty source export. This is not clear.
- `C1_CANARY_EXECUTED_NEEDS_REVIEW` — readable diagnostic artifacts exist, but no automatic design-clear or viability verdict follows.
- `C1F_DESIGN_READABLE_ACCEPTED_BY_REVIEW` — label that only the Orchestrator may apply after reviewing artifacts. Even this would not authorize C1B/C2/P1.

---

## 7. Bounded-canary vs C1B/C2/full-indexer boundary

A follow-up remains C1A-style only if it answers a mechanism-safety question at the smallest useful scale:

> Can the accepted C1A query/reconciliation pattern produce bounded, reviewable diagnostics under an objective selector without exploding rows?

It becomes C1B/C2/full-indexer-shaped if it does any of the following:

- expands beyond the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool without separate Orchestrator authorization;
- scans or profiles the full approximately 288K-condition universe;
- builds a reusable local or Dune volume-profiling artifact;
- expands beyond 5 conditions;
- runs repeated batches under one authorization until a non-exploding set is found;
- uses Dune count scouts to choose conditions;
- changes caps upward;
- narrows windows after seeing Dune results;
- queries broad time ranges or all conditions;
- accumulates reusable row ledgers beyond the canary evidence set;
- computes prices or canonical-side prices;
- tries to infer viability from a clean canary run;
- builds reusable production code or data artifacts.

A clean C1A-F1 canary could at most say: “the selector/query mechanism produced reviewable evidence under caps.” It would not say: “Option C covers the universe,” “Option C is viable,” or “P1 is unblocked.”

---

## 8. Explicit reject conditions

Any future C1A follow-up proposal must be rejected if any of the following appears:

1. It drops only the known exploding condition or otherwise edits candidates using C1A result knowledge.
2. It increases `per_condition_row_cap` above 2000 or `global_row_cap` above 6000.
3. It truncates rows or treats a capped result as complete.
4. It narrows windows after seeing C1A/Dune results.
5. It performs a Dune/API/RPC/network count preflight to choose conditions.
6. It filters the Dune query by local `tx_hash` values.
7. It reads or uses `resolved_winning_token_id`, `resolved_winning_outcome_index`, `resolved_winning_label`, payout-vector winner fields, outcome labels, realized-winner data, price convergence, PnL, score, or any outcome-conditioned field for candidate selection.
8. It uses `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis.
9. It uses OrdersMatched, wallet cohorts, address-level selection, `log_index`, or PnL logic.
10. It expands beyond 3–5 conditions or allows automatic repeated batches.
11. It writes price-series artifacts or probe inputs.
12. It self-certifies `C1_CANARY_DESIGN_CLEAR` without Orchestrator review.
13. It treats any C1A-F1 non-halt as a price-source viability verdict.
14. It scans or profiles the full approximately 288K-condition universe without separate Orchestrator authorization.
15. It builds a reusable volume-profiling artifact.
16. It treats local trade/local tx density as a guaranteed predictor of Dune OrderFilled volume.
17. It converts accepted C1A Dune/local ratios into constants, caps, filters, or guarantees.
18. It treats a low-density row explosion as permission to increase caps, retry, truncate, or narrow windows.
19. It does not preserve row-level evidence on halt.
20. It cannot be reproduced from the predeclared selector policy and deterministic tie-breaker.

---

## 9. Safe next SPEC-only recommendation

A safe next recommendation exists, but it is narrower than “run C1A again.” The recommended next step is:

> Draft and review a C1A-F1 selector-policy addendum that pins a deterministic, outcome-independent, local-density / subclass-balanced selector, an explicit bounded selector-pool rule, the weak-proxy caution for local density, and its reject conditions. The default selector pool must be the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool unless the Orchestrator separately authorizes broader local-only computation. Only after that addendum is accepted may a separate code/test-only task be considered. Only after code/test review may a separately authorized bounded user-run be considered.

This document itself can serve as the first version of that selector-policy addendum if the Orchestrator accepts the C1A-F1 framing. If accepted, it should still not authorize implementation or execution. It should only close the design question: “a safe selector-policy shape exists in principle.”

---

## 10. Recommendation on another C1A-style user-run

Another C1A-style bounded user-run should remain **blocked** until all of the following occur in order:

1. This follow-up SPEC is reviewed and accepted or patched.
2. A separate code/test-only authorization is issued for the selector-policy implementation, if needed.
3. The implementation is reviewed and accepted as scope-compliant.
4. A separate bounded user-run authorization is issued, naming the exact accepted selector policy and caps.

Without those steps, another run risks becoming post-hoc condition pruning, cap evasion, or a disguised C1B/C2/full-indexer continuation.

---

## 11. Guardrails preserved

Research only. This SPEC authorizes no implementation, no code, no tests, no Dune/API/RPC/network call, no new query, no artifact mutation, no cap increase, no row truncation, no ad hoc window narrowing, no C1B/C2/P1/P2/P3/probe, no scoring/backfill/wallet discovery/OrdersMatched expansion/`log_index`/PnL, no price artifact, and no side synthesis. It does not authorize scanning/profiling the full approximately 288K-condition universe or building a reusable volume-profiling artifact.

`named_binary_probe_blocked` remains `true`. P1 remains blocked on the absence of an accepted per-side/token-identity price source.
