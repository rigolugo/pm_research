# HANDOFF — Orchestrator: Option C C1R Design Addendum, Patch 1 — FOR REVIEW

**Decision requested:** REVIEW / ACCEPT-OR-REJECT-AS-SPEC-ONLY. This is a resubmission responding
to the Orchestrator's "BLOCK — revise C1R addendum, DOC PATCH ONLY" instruction. Claude has not
accepted this on the project's behalf — only the user/Orchestrator can do that.

**Scope:** Doc-only patch to `SPEC_price_source_option_c_onchain_C1R_addendum.md`. Closes the
blocking gap identified by the Orchestrator: C1A was scoped by `condition_id` + time window while
decoded `OrderFilled` rows are asset/token-keyed, leaving the future query underspecified.

No code changes. No implementation. No tests. No commands. No API/RPC/network call. No data run.
No full indexer. No broad backfill. No `log_index` work. No OrdersMatched expansion. No wallet
discovery. No PnL/scoring. No price-series artifacts. No `yes_price` / `1 - price` / `1 - yes_price`
/ `1 - p` / side synthesis. `named_binary_probe_blocked` remains `true`, untouched.

---

## 1. What changed (Patch 1)

Re-read canonical source directly (`rigolugo/pm_research`) for this patch, specifically
`SPEC_price_source_s1_coverage.md` §3.1 (the accepted S1 token-pair enumeration discipline) and
`DATA_CONTRACTS_named_binary_probe.md` (§2, §5 — `resolved_winning_token_id`, `TRADES_COLS`), to
ground the patch in existing accepted discipline rather than inventing a new one.

Changes to `SPEC_price_source_option_c_onchain_C1R_addendum.md`:

1. **New §4 — C1A selector manifest requirement.** Any future C1A authorization must supply a
   per-condition manifest: `condition_id`, `side_0_token_id`, `side_1_token_id`, `outcome_index_0`,
   `outcome_index_1`, `window_start_utc`, `window_end_utc`, `per_condition_row_cap`,
   `global_row_cap`, `source table/version`.
2. **New §4.1 — selector mapping is static identity only.** Reuses/adapts the accepted S1
   token-pair enumeration basis (`trades` distinct `(condition_id, token_id, outcome_index)`);
   requires validating exactly two stable, string-safe tokens per condition before any query;
   explicitly forbids computing price/target/score/probe features at this step; explicitly forbids
   `resolved_winning_token_id` as a pair source (outcome-conditioned, would leak the outcome —
   same reasoning `SPEC_price_source_s1_coverage.md` §3.1 already uses).
3. **New selector stop codes (§9):** `C1_SELECTOR_TOKEN_PAIR_UNRESOLVED`,
   `C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO`, `C1_SELECTOR_TOKEN_PRECISION_LOSS`,
   `C1_SELECTOR_USES_WINNER_TOKEN_ONLY`, `C1_SELECTOR_OUTCOME_CONDITIONED`. Prior stop codes are
   carried over unchanged.
4. **New §7 — explicit future C1A query shape.** Decoded OrderFilled table only; fixed `block_time`
   window; filter on `makerAssetId`/`takerAssetId` in the manifest's two-token pair; no assumption
   that the event table exposes a native `condition_id` column.
5. **New §7.1 — absolute C1R-level cap ceilings.** Per-condition ceiling 2,000 rows; global ceiling
   6,000 rows (deliberately below the naive 5×2,000 product). A future C1A authorization may set
   equal-or-lower caps but not exceed these without a fresh addendum revision. Row caps are no
   longer left entirely to a later prompt.
6. §6 (derived fields) and §8 (blocked-shape avoidance) updated to reference the selector manifest
   and confirm the token-pair filter does not reintroduce outcome leakage or wallet/PnL scope.
7. All pre-patch guardrail preservation language (§11) retained and extended to explicitly cover
   the selector manifest.

No other structural change. §1 (C1R is design-only), §2 (source preference), and §3 (canary
parameters) are substantively unchanged from the pre-patch draft; §3 gained a forward reference to
the new §7.1 ceilings.

## 2. What this patch does NOT do

- Does not execute C1A, including the manifest-population/validation step itself (§4.1), which
  would require a local `trades`-table read — that is a data operation and remains unauthorized
  here.
- Does not authorize C1A, C1B, C2, or any data run.
- Does not flip `named_binary_probe_blocked`. Does not touch P1/P2/P3 gate state.
- Does not reopen or alter Options A or B. Does not reverse Revision 3's acceptance or C1
  guardrail-block record.
- Does not assert the selector-manifest patch fully resolves Revision 3's Branch 2 concern by
  itself — that remains an Orchestrator judgment call (addendum §8, closing paragraph).

## 3. Suggested canonical files to patch, IF this addendum is accepted (not done by this package)

Unchanged from the prior handoff, still pending actual acceptance:

- `project_context/PROJECT_STATE.md`, `DECISION_LOG.md`, `ARTIFACT_INDEX.md`, `START_HERE.md` —
  would need new entries recording whatever the actual review outcome is (accept, reject, or
  accept-with-further-changes). None of this has been done.

## 4. Files delivered this turn

- `SPEC_price_source_option_c_onchain_C1R_addendum.md` (revised, Patch 1 applied)
- `HANDOFF_orchestrator_option_c_c1r_design_addendum.md` (revised, this file)

Delivery is not acceptance. The user commits these to `C:\b1\pm_research` (or the canonical repo,
once reviewed) at their discretion, and only after Orchestrator review.

## 5. Guardrails compliance attestation

Research only. Docs only. No code. No implementation. No tests. No commands. No API/RPC/network
call. No data run. No full indexer. No broad backfill. No `log_index` work. No OrdersMatched
expansion. No wallet discovery. No PnL/scoring. No price-series artifacts. No `yes_price` /
`1 - price` / `1 - yes_price` / `1 - p` / side synthesis. No gate change. P1 remains BLOCKED. B1
remains unauthorized. P2/P3/probe remain unauthorized. `named_binary_probe_blocked` remains `true`.
Revision 3 is not silently reversed. This patch responds only to the specific selector-manifest gap
the Orchestrator flagged; it does not expand scope beyond that fix.
