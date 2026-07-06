# HANDOFF — Orchestrator → Claude: Option C SPEC-ONLY authorization

**Decision:** APPROVE — Option C may proceed as a **SPEC-ONLY** candidate-source review.

**Authorization basis:** The user explicitly authorized Option C in-chat after the orchestrator accepted Claude's prior BLOCK that Option C was previously out of scope under current guardrails. This handoff records a deliberate, narrow reversal of that prior standing exclusion.

---

## What is authorized

Claude may draft these files only:

1. `SPEC_price_source_option_c_onchain.md`
2. `HANDOFF_orchestrator_option_c_onchain_spec.md`

The deliverable is a source-interface / feasibility spec for Option C as a possible on-chain/event-level candidate price source for named-binary P1 price input.

The spec must remain **SPEC ONLY**. It may discuss candidate sources, required fields, hard stops, evidence requirements, and staged gates. It must not implement or execute anything.

---

## Required framing

Option C was previously recorded as out of scope by current guardrails. This authorization is an explicit, narrow reversal for **spec drafting only**.

Claude must state that reversal plainly in the Option C spec and handoff, and must not treat older Option C exclusion language as still blocking this spec-only task. Older exclusion language remains historically correct for implementation/execution and for any unapproved on-chain reconstruction work.

---

## Current project state to preserve

- Named-binary P0 remains accepted / `P0_CLEAR`.
- P1 remains **BLOCKED** on missing accepted per-side/token-identity price input.
- S1 CLOB `/prices-history` Pass 1 remains accepted negative: `S1_SOURCE_NOT_VIABLE`.
- S1-ALT / Option A local trade-print Pass 1 remains accepted negative: `S1ALT_SOURCE_NOT_VIABLE`.
- Option B B0 remains inconclusive for API trust; B1 remains unauthorized.
- P2/P3/probe execution remain unauthorized.
- `named_binary_probe_blocked` remains `true`.

A favorable Option C spec does **not** unblock P1 by itself. It can only justify a later, separately reviewed and separately authorized code/tests-only task, if the spec is accepted.

---

## Hard non-authorization list

This authorization does **not** permit:

- implementation;
- tests;
- commands;
- API/RPC/network calls;
- data runs;
- archive-node access;
- broad chain backfill;
- full indexer;
- `log_index` work;
- OrdersMatched expansion except as a discussed blocked dependency;
- wallet discovery;
- PnL-by-role;
- scoring;
- B1;
- full Pass 1;
- S2;
- P1/P2/P3;
- probe execution;
- paper/live trading;
- any price-series artifact;
- `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis.

---

## Required Option C spec questions

The Option C spec must answer at least:

1. What exactly is Option C: on-chain event reconstruction, event-log sourced trade extraction, archive/RPC access, vendor event archive, or another bounded source-interface candidate?
2. What exact source candidate is being evaluated?
3. What fields are required to prove per-side/token-identity price input: `condition_id`, `token_id`/`asset_id`, `outcome_index` if available, side/source role if relevant, price, size, timestamp, `tx_hash`, and any ordering key if needed?
4. Is maker/taker or OrdersMatched role needed? If yes, why, and what guardrail risk does that create?
5. Can the source provide token-level/per-side identity without `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis?
6. Can the source support decision-window coverage for the P0 universe?
7. Can it be sampled safely without becoming a full indexer?
8. What would constitute a negative result?
9. How do C0 source-interface/spec verification and C1 bounded sample coverage design stop before implementation or execution?
10. What remains blocked even after a favorable spec?

---

## Safe staged gates

- **C0:** Source-interface/spec verification only. No calls, no code, no data. Identify the candidate source and required schema/evidence.
- **C1:** Bounded sample coverage design only. No execution. Define how a future sample would avoid full-indexer, log-index, wallet, and OrdersMatched creep.
- **C2 or later:** Not authorized. Any implementation, source fetch, RPC/API call, event extraction, data run, or coverage measurement requires separate explicit authorization after spec acceptance.

---

## Prompt to Claude

Review the canonical repo in the required order. Then draft `SPEC_price_source_option_c_onchain.md` and `HANDOFF_orchestrator_option_c_onchain_spec.md` only.

This is an explicit narrow reversal of the prior "Option C out of scope" stance, limited to SPEC-ONLY drafting. Preserve all guardrails and state that no implementation, no network/RPC/API call, no data run, no full indexer, no `log_index`, no OrdersMatched expansion, no wallet discovery, no PnL/scoring, no P1/P2/P3/probe, and no side synthesis is authorized. A favorable Option C spec does not unblock P1 by itself.
