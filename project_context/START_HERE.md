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
9. `SPEC_price_source_s1_coverage.md` — accepted S1 coverage-only spec. Historical/accepted spec context only; S1 Pass 1 has now completed with a negative sampled result.
10. `SPEC_price_source_alt_trade_prints.md` — accepted S1-ALT (Option A local trade-print) coverage-only spec, precision-loss correction applied. Historical/accepted spec context only; S1-ALT Pass 1 has now completed with a negative sampled result.
11. `SPEC_price_source_option_b_data_api_review.md` — **accepted Option B Data API `/trades` spec-only review.** Historical/accepted spec context only; it authorizes nothing further.
12. Latest active handoffs/review memos:
    - `HANDOFF_orchestrator_s1_pass1_RESULT.md`
    - `HANDOFF_orchestrator_s1_alt_pass1_RESULT.md`
    - `HANDOFF_orchestrator_named_binary_probe_p1_REVIEW.md`
    - `HANDOFF_orchestrator_named_binary_probe_p0.md`
    - `HANDOFF_orchestrator_option_b_spec_s1_1_patch.md`

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

- **Option B Data API `/trades` spec-only review: ACCEPTED / SPEC ONLY.** `SPEC_price_source_option_b_data_api_review.md` was accepted at orchestrator review with two doc-only wording amendments (§8 and §1.1). Acceptance authorizes **nothing further**: no Phase B0 run, no Phase B1, no full Pass 1, no S2, no implementation, no network/API call, no data run, no backfill, no scoring, no P1/P2/P3, no probe, no wallet/OrdersMatched/`log_index`/PnL, and no gate change. Earlier Phase B0 code is draft/reference only unless separately authorized after the spec is pinned. A negative or ambiguous Option B result would close only the Data API `/trades` candidate on that evidence; any different future candidate source would require a fresh, separately authorized spec. Option C/on-chain reconstruction remains out of scope by current guardrails.

- **Chat2 Dune wallet-cohort discovery: BLOCKED.** It is a separate phase. Outcome-source scoreability does not unblock wallet discovery.

---

## Next possible step — only if explicitly authorized by the user

No next execution or implementation task is authorized by the Option B spec acceptance.

A future move would require separate explicit authorization and a fresh scoped decision. Examples include a Phase B0 implementation review/code-only task, a Phase B0 network execution task, a B1 gap pilot, a full Pass 1 coverage task, a Pass 2 generalization check, or a different candidate-source spec. None follows automatically.

Any further move remains bounded by the project guardrails. No data run, network/API call, implementation, backfill, scoring, probe, P1/P2/P3 continuation, wallet/OrdersMatched/`log_index`/PnL, or gate change is authorized unless explicitly approved in-chat and allowed by the current repo guardrails.

---

## What is NOT authorized

No Phase B0 run, Phase B1, full Pass 1, S2, P1/P2/P3, or probe execution.

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
