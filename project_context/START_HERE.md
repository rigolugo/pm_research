# START HERE

*First file to read in any new chat for this project. It orients you to the pinned source-of-truth files, the current branch state, and the rule that keeps this project consistent.*

---

## Rule 0 — source of truth

**Old chats are NOT source of truth.** Do not rely on prior-chat memory, summaries, or recollection of "what we decided."

For ChatGPT/orchestrator work, the canonical source is the private GitHub repo:

`rigolugo/pm_research`

This public repo:

`rigolugo/pm_research_context`

is a Claude-readable mirror of selected accepted context files only. If this public mirror conflicts with the private canonical repo, the private repo wins.

If something needed is not written in the source-of-truth files, treat it as unknown and inspect/verify from source or data. Do not reconstruct it from memory.

---

## Required read order

Read these, in this order, before doing anything:

1. `GUARDRAILS.md` — hard constraints: research only; no live/paper trading; no wallet-copying; no PnL-by-role or `log_index` without explicit authorization; no full indexer.
2. `PROJECT_STATE.md` — current objective, environment, and what is active/blocked right now.
3. `DECISION_LOG.md` — corrected history; settled decisions not to re-litigate.
4. `CLOSED_FINDINGS.md` — settled negative/complete results.
5. `ARTIFACT_INDEX.md` — what exists and where.
6. `DATA_CONTRACTS_named_binary_probe.md` — exact inspected schemas/API surfaces for the named-binary probe.
7. `PRICE_INPUT_CONTRACT_named_binary_probe.md` — accepted S0 finding on why P1 is blocked on price input.
8. `SPEC_named_binary_probe.md` — governing spec-only document for the future offline probe.
9. `SPEC_price_source_s1_coverage.md` — accepted S1 coverage-only spec. Historical/accepted spec context only; S1 Pass 1 completed with a negative sampled result.
10. `SPEC_price_source_alt_trade_prints.md` — accepted S1-ALT (Option A local trade-print) coverage-only spec, precision-loss correction applied. Historical/accepted spec context only; S1-ALT Pass 1 completed with a negative sampled result.
11. `SPEC_price_source_option_b_data_api_review.md` — accepted Option B Data API `/trades` spec context. Historical/accepted spec context only: original B0 halted and remained inconclusive because required artifacts were missing; the corrected B0 diagnostic later completed and did **not** establish Data API `/trades` mechanical trust. B1 remains unauthorized.
12. `SPEC_option_b_b0_failure_diagnostic.md` — accepted corrected B0 diagnostic spec. Historical/accepted spec context only; the corrected diagnostic harness has since been implemented and user-run under separate authorization with a negative B0 mechanical-trust result.
13. `SPEC_price_source_option_c_onchain.md` — accepted Option C (on-chain / decoded OrderFilled event tables) price-source candidate review, Revision 3. Option C Revision 3 is accepted / spec-only; C0 (candidate/source-interface selection) is accepted / spec-only. At Revision 3, C1 (bounded coverage/trust pilot) was guardrail-blocked — no safe bounded sample design then resolved the local-`tx_hash`-scoping trap. That pre-C1R block is superseded by the separately accepted C1R addendum below.
14. `SPEC_price_source_option_c_onchain_C1R_addendum.md` — accepted C1R (C1 Revised) design addendum, SPEC ONLY. Resolves the Revision-3 scoping trap via a fixed selector manifest (outcome-independent), subquery-wrapped SQL with per-condition cap+1 over-fetch, hard row-cap enforcement, empty-export detection, row-level evidence artifacts, and source-table validation.
15. `README_price_source_option_c_c1a.md` — C1A manifest + bounded canary implementation package (code/test-only, 50 pure-logic tests passing, no network). C1A bounded user-run is now authorized only under this accepted README/code path. No C1A result exists yet.
16. Latest active handoffs/review memos:
    - `HANDOFF_orchestrator_s1_pass1_RESULT.md`
    - `HANDOFF_orchestrator_s1_alt_pass1_RESULT.md`
    - `HANDOFF_orchestrator_named_binary_probe_p1_REVIEW.md`
    - `HANDOFF_orchestrator_named_binary_probe_p0.md`
    - `HANDOFF_orchestrator_option_b_spec_s1_1_patch.md`
    - `HANDOFF_orchestrator_option_b_b0_RESULT.md`
    - `HANDOFF_orchestrator_option_b_b0_failure_diagnostic.md`
    - `HANDOFF_orchestrator_option_b_b0_corrected_diagnostic_RESULT.md`
    - `HANDOFF_orchestrator_option_c_onchain_spec.md`
    - `HANDOFF_orchestrator_option_c_c1r_design_addendum.md`
    - `HANDOFF_orchestrator_option_c_c1a_IMPLEMENTATION.md`

Supporting references, not overriding the above:

- `DUNE_DATA_NOTES.md`
- `CLAUDE_PROJECT_SETTINGS.md`
- `ORCHESTRATOR_LOW_CONTEXT_MODE.md`
- `WORKFLOW.md`

These supporting files do not authorize implementation, data fetching, P1/P2/P3 continuation, probe execution, wallet discovery, PnL, paper/live trading, `log_index`, or full indexer work.

---

## Current branch state

- **P0 preflight: ACCEPTED (`P0_CLEAR`).** Read-only universe verification; emitted eligible/excluded counts only. It authorizes nothing further.

- **P1 feature assembly: BLOCKED on missing per-side price input.** The accepted semantics layer's `OrientationContract.canonical_side_price(side_0_price, side_1_price)` requires two per-side prices. Local `Store.load_prices()` exposes only `[condition_id, ts, yes_price]`. The accepted S0 finding proves `yes_price` is YES/NO-only and unsafe for UP_DOWN / OVER_UNDER / NAMED_OTHER. No local per-side/per-token price series exists.

- **P2 / P3 / probe execution: UNAUTHORIZED.** `named_binary_probe_blocked = true` in all gate states. A usable realized-outcome source does not authorize a probe.

- **S1 price-source coverage Pass 1: COMPLETED / ACCEPTED — RESULT: `S1_SOURCE_NOT_VIABLE`.** The accepted S1 coverage-only test sampled the P0 universe to check whether Polymarket CLOB `/prices-history` per token can provide usable decision-time per-side prices for both sides. On the accepted sampled run, Level-B both-sides coverage cleared 0.95 in no subclass: UP_DOWN 19/50 = 0.38, OVER_UNDER 51/98 ≈ 0.5204, NAMED_OTHER 65/100 = 0.65. This is Pass 1 sampled coverage only, not Pass 2 full-universe coverage. Consequence: CLOB `/prices-history` is not viable on this evidence; P1 remains BLOCKED with no `yes_price` fallback. No Pass 2, S2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, or gate change is authorized; `named_binary_probe_blocked` stays `true`.

- **S1-ALT Pass 1 (Option A local trade-print) coverage: COMPLETED / ACCEPTED — RESULT: `S1ALT_SOURCE_NOT_VIABLE`.** After the S1 negative, the first candidate alternative per-side price source — local trade-print reconstruction via `Store.load_trades()` (no network) — was tested per `SPEC_price_source_alt_trade_prints.md`, reusing the **exact accepted S1 Pass-1 300-condition sample** (248 measured + 52 S1-invalid-window, pre-excluded and never re-measured). On the accepted sampled run, Level-B both-sides coverage again cleared 0.95 in no subclass: UP_DOWN 13/50 = 0.26, OVER_UNDER 40/98 ≈ 0.4082, NAMED_OTHER 71/100 = 0.71. This is Pass 1 sampled coverage only. Consequence: local trade prints are not viable either on this evidence; P1 remains BLOCKED with no `yes_price` fallback and no `1 - price` synthesis. No Pass 2, Option C, S2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, or gate change is authorized; `named_binary_probe_blocked` stays `true`.

- **Option B Data API `/trades` corrected B0 diagnostic: COMPLETED / ACCEPTED — RESULT: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.** Corrected B0 completed with `artifact_status = API_ARTIFACT_COMPLETE` and `halt_code = null`, but did not establish Data API `/trades` mechanical trust. Fixed 10-condition manifest result: `api_rows_primary = 13,009`, `api_rows_total_all_query_modes = 17,853`, `local_rows = 1,346`, `mismatches = 14,355`; classifications `OVERLAP_API_LOCAL_MISMATCH = 7`, `OVERLAP_PAGINATION_PARTIAL = 3`, `OVERLAP_MATCHED = 0`, `NO_TEMPORAL_OVERLAP = 0`; mismatches `API_ONLY = 11,829`, `LOCAL_ONLY = 145`, `TX_HASH_AMBIGUOUS = 2,381`; pagination `COMPLETE_SHORT_FINAL_PAGE = 7`, `PARTIAL_RETRIEVAL = 3`. Metadata caveat: `takeronly_probe_conditions` differs between reconciliation and offline recompute summaries (3 vs 10), while core status/counts match; this does not change the B0 negative finding. **B1 remains not authorized.** Option B must not proceed to B1/full Pass 1/S2/P1/P2/P3/probe. P1 remains BLOCKED on the absence of an accepted per-side/token-identity price source. No scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, price-series artifact, or gate change is authorized. `named_binary_probe_blocked` stays `true`.

- **Option C (on-chain / decoded OrderFilled event tables) price-source spec: ACCEPTED / SPEC ONLY (Revision 3).** `SPEC_price_source_option_c_onchain.md` is the accepted third per-side/token-identity price-source candidate review, after Option A/S1-ALT and Option B (both closed negative). **C0** (bounded decoded Dune/vendor OrderFilled event tables as the candidate) remains accepted / spec-only — no coverage claim, no run. **At Revision 3, C1** (a bounded coverage/trust pilot) **was guardrail-blocked**: no safe bounded sample design then resolved the local-`tx_hash`-scoping trap — local-`tx_hash` scoping likely reproduces S1-ALT and cannot test missing coverage by construction, while independent condition/time-window event querying risks broad event reconstruction / indexer-shaped work under the "No full indexer" constraint. **That pre-C1R block is superseded by the separately accepted C1R addendum** (`SPEC_price_source_option_c_onchain_C1R_addendum.md`, SPEC ONLY), which resolves the design-level scoping trap via a fixed selector manifest, subquery-wrapped SQL with cap+1 over-fetch, hard row-cap enforcement, empty-export detection, row-level evidence artifacts, and source-table validation. **C1A bounded user-run is now authorized only under the accepted README/code path** (`README_price_source_option_c_c1a.md`; code/test-only, 50 pure-logic tests passing, no network). **No C1A result exists yet.** P1 remains BLOCKED; `named_binary_probe_blocked` stays `true`.

- **Chat2 Dune wallet-cohort discovery: BLOCKED.** It is a separate phase. Outcome-source scoreability does not unblock wallet discovery.

---

## Next possible step — only if explicitly authorized by the user

No further Option B B0 execution is authorized. B1 remains not authorized. Option B should not proceed to B1/full Pass 1/S2/P1/P2/P3/probe.

**The next possible step is the bounded C1A user-run, exactly per `README_price_source_option_c_c1a.md`.** C1A (manifest design + bounded canary reconciliation) is code/test-only (50 pure-logic tests passing, no network) and is authorized for user-run, not for Claude execution. **Results must return to the orchestrator for review before any C1B/C2/P1 discussion.**

**C1B full sampled coverage is not authorized. C2 reusable/production implementation is not authorized. P1/P2/P3/probe remain unauthorized. `named_binary_probe_blocked` remains `true`.**

Any further move remains bounded by the project guardrails. No data run, network/API/RPC call, implementation, backfill, scoring, probe, P1/P2/P3 continuation, wallet/OrdersMatched/`log_index`/PnL, or gate change is authorized unless explicitly approved in-chat and allowed by the current repo guardrails.

---

## What is NOT authorized

No B1, full Pass 1, S2, P1/P2/P3, or probe execution follows from the corrected B0 diagnostic result.

No C1B full sampled coverage, C2 reusable/production implementation, P1/P2/P3 continuation, or probe execution follows from C1A. The only authorized C1A action is the bounded user-run exactly per `README_price_source_option_c_c1a.md`, with results returned to orchestrator for review.

No scoring: no Brier, log-loss, calibration, reliability, splits, or forecast-vs-price metrics.

No wallet work, OrdersMatched expansion, `log_index`, PnL-by-role, gate modification, live trading, paper trading, wallet-copying, or full indexer.

Do not flip `named_binary_probe_blocked`.

Do not use `yes_price`, `1 - price`, or `1 - yes_price` to unblock named-binary pricing.

---

## Working discipline

- Verify before concluding.
- Never conclude from one row or from an all-one-role/all-one-direction output.
- Spec before implementation.
- Never silently reverse a prior decision.
- Close each task with a Claude-to-Orchestrator handoff memo.
- Claude should treat this public mirror as context only. It authorizes no implementation.
