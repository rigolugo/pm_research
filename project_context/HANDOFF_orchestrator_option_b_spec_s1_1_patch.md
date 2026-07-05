# HANDOFF — Claude → Orchestrator: Option B SPEC-ONLY REVIEW (§1.1 wording patch)

**Task:** Apply the approved doc-only §1.1 wording patch to
`SPEC_price_source_option_b_data_api_review.md`.
**Status:** Done. **Spec only.** No implementation, no B0 run, no network/API call, no state
change. `named_binary_probe_blocked` stays `true`.

---

## Only change made

Replaced one sentence in the §1.1 H2 bullet. It now reads:

> ...Option B would fail for the same reason Option A did: the Data API `/trades` path would not
> supply two-sided, token-identity-resolvable observations for those conditions. That would close
> the Option B candidate on this evidence, but any different future candidate source would require
> a fresh, separately authorized spec. Option C/on-chain reconstruction remains out of scope by
> current guardrails.

Verified by diff against the prior pinned copy (which already carried the approved §8 patch): the
only delta is this sentence in §1.1. Nothing else changed. Line count 294 → 296 (net +2 lines from
the longer sentence).

## Guardrails preserved

Research only. No implementation, no network/API call, no data run, no backfill, no Pass 2, no S2,
no P1/P2/P3, no probe, no scoring, no wallet/OrdersMatched/`log_index`/PnL, no gate change, no
`yes_price`/`1 - price`/`1 - yes_price` synthesis. Delivery is not acceptance; the user commits to
`C:\b1\pm_research` at their discretion.
