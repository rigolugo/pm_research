# ARTIFACT INDEX

*What exists and where. Paths are in the local repo `C:\b1\pm_research` unless noted.*

---

## Artifacts (`artifacts/`)

Recommended subfolder organization (currently flat — reorganize when convenient):

### `artifacts/rank1a/`
- `forecast_vs_price_rank1a.json` + `.md` report + `_splits.csv` + `_conditions.csv` — Rank 1A probe (NEGATIVE).
- `rank1a_price_bucket_diagnostic.json` + `.md` + `.csv` — NO_ACTIONABLE_BUCKET.

### `artifacts/audits/`
- `probe_fast_gate.*` — data gate result CLEAR_WITH_WARNINGS_FOR_RANK1A.
- (audit_market_structure outputs, if retained.)

### `artifacts/rank2_ordersmatched/`
- `ordersmatched_economic_role_expanded.json` + `.md` + `.csv` — Rank 2 final distribution (117 trades, 96 wallets, 71T/46M).
- `ordersmatched_maker_pairing_validation.json` + `.md` + `.csv` — MAKER_PAIRING_VALIDATED.
- `ordersmatched_economic_role.{json,md,csv}` — the pre-expansion probe.
- `ordersmatched_expanded_dune_query.sql` (varchar-cast, 150-tx) and `ordersmatched_expanded_dune_tx_list.txt`.
- `orderfilled_operator_filtered_semantic.*` — event-role recovery + operator filter.
- `orderfilled_fee_role_diagnostic.*` — fee diagnostic (SUPERSEDED, preserved).

### `artifacts/named_binary/`
- `named_binary_audit_gate.json` + `.md` — default/local-only named-binary semantics audit gate: legacy pooled-all gate BLOCKED_BY_RESOLUTION_MAPPING; schema_chosen=label; YES/NO resolves 8,521/8,521 where local resolution rows exist; non-YES/NO unresolved locally. When run with `--resolution-source`, the same gate artifact also includes `stage4_nonyesno_branch` fields described below.
- `named_binary_resolution_mapping_coverage.csv` — per-subclass coverage table. In the local-only audit it reports eligible / with-resolution / winner-maps / rate; after Stage 3/4 it extends this with source_rows, resolved_single_winner, conflicts-by-type, exact_winner_rate, and coverage_rate.
- `named_binary_classification_contract.json` + `.md` — per-condition subclass + eligibility; carries `nb_contract_version` (`nb-contract-2026-06-28.1`). **Chat2 consumes this and asserts version equality.**
- `named_binary_semantics_report.md` — narrative summary.
- `named_binary_label_pair_census.csv` — frequency-ranked label-pair census (11,598 pairs; head covered by seed lexicon).
- `named_binary_resolution_source_rows.parquet` — Stage 3 normalized winners (condition_id, subclass, resolved_winning_token_id/outcome_index/label, resolved_at, source_table, status, nb_contract_version); string-safe token fields; RESOLVED_SINGLE_WINNER rows only.
- `named_binary_resolution_conflicts.csv` — Stage 3 excluded conflicts with status + payout vector.
- `named_binary_resolutions_source_audit.json` + `.md` — Stage 3 build audit (per-subclass resolved/conflict counts).

### `artifacts/named_binary_probe/`
- `p0_preflight.json` — Stage P0 preflight result (machine-readable): `p0_state` (P0_CLEAR), `authorized_scope` (P0_PREFLIGHT_ONLY), `probe_execution_authorized` (false), `named_binary_probe_blocked_observed` (true), contract/resolution-source versions, `gate_snapshot`, `counts_pooled`, `counts_by_subclass`, `excluded_counts`, `reconciliation`, notes. Accepted real-data figures: contract_eligible 39,957 / resolved_single_winner 39,693 / ambiguous_multiple_winners 253 / source_rows 39,946 / missing_source_rows 11 / final_p0_eligible 39,693.
- `p0_preflight.md` — Stage P0 narrative report (same figures + gate snapshot + reconciliation).
- `p0_excluded_counts.csv` — per-subclass tally (source_rows / resolved / ambiguous / missing / non_scoreable / final_p0_eligible).
- `price_input_s0_inspection.txt` — read-only S0 price-input inspection evidence (produced by `scripts/inspect_price_input_s0.py`). Records price provenance, the YES/NO-only / named-binary-unsafe meaning of `yes_price`, the absence of any local per-side/per-token price artifact, and a non-YES/NO price sample.

### `artifacts/named_binary_probe/price_source_s1/`
S1 Pass 1 **coverage-only** artifacts (user-run, ACCEPTED; verdict `S1_SOURCE_NOT_VIABLE`). Coverage diagnostics only — **no price series is persisted**.
- `price_source_s1_coverage.json` — machine-readable Pass-1 result: `s1_verdict = S1_SOURCE_NOT_VIABLE`, sample 300, valid_window 248 / invalid_window 52, 496 fetched side tokens, clean endpoint shape, and per-subclass coverage below 0.95 in every subclass.
- `price_source_s1_coverage.md` — narrative summary.
- `price_source_s1_coverage_by_condition.csv` — per-condition coverage ledger. **No price values.**
- `price_source_s1_excluded.csv` — excluded conditions with reasons.
- `price_source_s1_endpoint_shape.md` — documented-vs-observed endpoint shape.

### `artifacts/named_binary_probe/price_source_s1_alt/`
S1-ALT Pass 1 (Option A local trade-print) **coverage-only** artifacts (user-run, ACCEPTED; verdict `S1ALT_SOURCE_NOT_VIABLE`). Local-only (no network); reuses the exact accepted S1 Pass-1 300-condition sample. Coverage diagnostics only — **no price series is persisted**.
- `price_source_s1_alt_coverage.json` — machine-readable Pass-1 result: `status`/`verdict = S1ALT_SOURCE_NOT_VIABLE`, reconstructed sample 300/300, measured 248, S1-invalid-window 52, Level-B class counts BOTH_SIDES 124 / ONE_SIDE 65 / NEITHER 59, and per-subclass coverage below 0.95 in every subclass.
- `price_source_s1_alt_coverage.md` — narrative summary.
- `price_source_s1_alt_coverage_by_condition.csv` — per-condition coverage ledger. **No price values.**
- `price_source_s1_alt_excluded.csv` — excluded conditions with reasons.
- `price_source_s1_alt_source_shape.md` — observed local `Store.load_trades()` column shape.

---

## Scripts (`scripts/`)

### Rank 1A
- `forecast_vs_price.py` — pooled YES/NO forecast-vs-price probe (Rung 0 + Rung 1).
- `rank1a_price_bucket_diagnostic.py` — price-bucket segmentation diagnostic.

### Audit / gate
- `audit_market_structure.py` — streaming market-structure audit.
- `probe_fast_gate.py` — overlap/concentration data gate.

### Rank 2 (OrdersMatched / OrderFilled)
- `orderfilled_sample_join.py` — **validated decoder** (topic2=maker, topic3=taker; canonical-int helpers live here / in the OrdersMatched module).
- `ordersmatched_economic_role.py` — economic-role probe (taker via takerordermaker; maker via pairing). Contains `canonical_int`, `DataExportPrecisionLoss`, varchar Dune query template.
- `ordersmatched_economic_role_expanded.py` — stratified 150-tx expansion + per-wallet/contract/time/fill breakdowns.
- `ordersmatched_maker_pairing_validation.py` — known-maker-case validation harness.

### Named-binary semantics
- `audit_named_binary_semantics.py` — orchestration entry point; streams sharded trades, runs mapping/classification/resolution/orientation/gate, writes named-binary artifacts. Stage 4 optional `--resolution-source <rows.parquet>` overlays the Stage 3 RESOLVED_SINGLE_WINNER winners onto non-YES/NO subclasses. CLEAR_WITH_WARNINGS means the outcome source/audit is usable and never authorizes a probe (`named_binary_probe_blocked` stays True).
- `named_binary_label_census.py` — frequency-ranked label-pair census feeding the lexicon.
- `diag_resolution_mapping.py`, `diag_resolution_coverage.py`, `diag_named_binary_resolvable.py` — read-only diagnostics that isolated the YES/NO-only resolutions finding.
- `inspect_named_binary_resolution_dune_schema.py` — Stage 0 read-only Dune schema inspection.
- `export_contract_for_dune.py` — exports the classification contract to a Dune-upload CSV.
- `build_named_binary_resolution_source.py` — Stage 3 bulk builder.

### Named-binary probe (Stage P0 only)
- `named_binary_probe_p0_preflight.py` — Stage P0 preflight (ACCEPTED, P0_CLEAR). Read-only except for its three `artifacts/named_binary_probe/` outputs. Counts only; no trades/prices, no decision timestamps, no canonical_side_price, no scoring, no Dune/network, no log_index, no wallet logic.

### Named-binary probe (S1 price-source coverage — coverage-only, user-run)
- `price_source_s1_coverage.py` — S1 Pass 1 CLOB `/prices-history` coverage test (ACCEPTED run; verdict `S1_SOURCE_NOT_VIABLE`). **Coverage-only:** no `yes_price`/`1 - yes_price`/`1 - price`/`1 - p` synthesis; no writes to `prices/`; no scoring/backfill; `named_binary_probe_blocked` never flipped.
- `price_source_s1_alt_pass1_coverage.py` — S1-ALT Pass 1 local trade-print coverage test (ACCEPTED run; verdict `S1ALT_SOURCE_NOT_VIABLE`). Local-only; reuses accepted S1 sample; no price series persisted.

### Named-binary probe (read-only inspection scripts — no code/gate/probe changes)
- `inspect_named_binary_probe_data_contracts.py` — read-only inspector for exact schemas/API surfaces.
- `inspect_oriented_price_formula.py` — read-only inspector for price/orientation callables.
- `inspect_price_input_s0.py` — read-only S0 price-input inspector. Refuses to infer `side_1 = 1 - yes_price`.

### Tests (`tests/`)
- `test_forecast_vs_price.py`, `test_orderfilled_sample_join.py`, `test_ordersmatched_economic_role.py`, plus the existing store/audit/backfill suites.
- `test_named_binary_semantics.py` — named-binary suite.
- `test_named_binary_resolution_source.py` — Stage 2 suite.
- `test_build_named_binary_resolution_source.py` — Stage 3 builder suite.
- `test_named_binary_stage4_gate.py` — Stage 4 suite.
- `test_named_binary_probe_p0_preflight.py` — Stage P0 preflight suite.
- `test_price_source_s1_coverage.py` — S1 Pass 1 coverage suite.

---

## Core package (`pm_research/`)

- `data/store.py` — flat parquet store; `load_trades` applies hygiene (drop null condition_id, key-preferring dedup); `load_prices`, `load_resolutions`, `load_markets`.
- `data/schemas.py` — TRADES_COLS (11; no log_index), PRICES_COLS [condition_id, ts, yes_price], RESOLUTIONS_COLS [condition_id, winning_outcome, resolved_at], MARKETS_COLS.
- `semantics/` — named-binary semantics layer: `lexicon.py`, `mapping_audit.py`, `resolution_schema.py`, `resolution_source.py`, `named_binary.py`, `__init__.py`.
- `splits.py` — `rolling_train_test_splits` (shared by audit/gate/probes).
- `calibration.py` — `IsotonicCalibrator` (.fit/.apply, static .brier).

---

## Specs & handoffs (repo root or specs folder)
- `SPEC_named_binary_resolution_source.md` — spec for sourcing non-YES/NO realized outcomes from Dune; IMPLEMENTED + ACCEPTED across Stages 0–4.
- `PLAN_named_binary_resolution_source_implementation.md` — staged implementation plan (Stages 0–4).
- `HANDOFF_orchestrator_named_binary_taskAB.md` — orchestrator handoff: Issue-A fix + spec, with real-data before/after.
- `FINDINGS_named_binary_resolution_blocker.md` — dated finding: YES/NO-only resolutions block the named-binary probe (superseded by the Dune source).
- **Stage 0** — `SCHEMA_INSPECTION_named_binary_resolution_source.md`.
- **Stage 1** — `DUNE_SQL_named_binary_resolution_stage1.sql` + `STAGE1_named_binary_resolution_query_plan.md` + `FINDINGS_stage1_named_binary_resolution_coverage.md`.
- **Stage 2** — `HANDOFF_orchestrator_stage2_resolution_source.md`.
- **Stage 3** — `HANDOFF_orchestrator_stage3_resolution_builder.md`.
- **Stage 4** — `HANDOFF_orchestrator_stage4_gate_integration.md`.
- `REVIEW_nautilus_scavenge_named_binary_resolution.md` — file-based review of the NautilusTrader bundle (engineering shapes only; LGPL — no code copied; not a canonical source).
- `SPEC_named_binary_probe.md` — ACCEPTED spec-only document for a future offline historical non-YES/NO named-binary forecast-vs-price probe. Authorizes no implementation, no data run, and no probe execution.
- `HANDOFF_orchestrator_named_binary_probe_p0.md` — Stage P0 preflight handoff (ACCEPTED, P0_CLEAR).
- `HANDOFF_orchestrator_named_binary_probe_p1_REVIEW.md` — Stage P1 review memo (PAUSED/BLOCKED). Superseded by DATA_CONTRACTS + PRICE_INPUT_CONTRACT; P1 stays blocked.
- `DATA_CONTRACTS_named_binary_probe.md` — ACCEPTED reference contract.
- `PRICE_INPUT_CONTRACT_named_binary_probe.md` — ACCEPTED S0 finding. **P1 remains BLOCKED on price input.**
- `SPEC_price_source_s1_coverage.md` — **ACCEPTED / SPEC ONLY / coverage-only.** Authorizes no implementation, no S1 run, no network/data fetch, no backfill, no scoring, no S2, no P1/P2/P3, no probe execution. Forbids `yes_price` / `1 - yes_price` / `1 - p` side-synthesis.
- `HANDOFF_orchestrator_s1_pass1_RESULT.md` — **S1 Pass 1 sampled coverage RESULT (ACCEPTED): `S1_SOURCE_NOT_VIABLE`.** Pass 1 sampled coverage only; P1 stays blocked.
- `HANDOFF_orchestrator_s1_alt_pass1_RESULT.md` — **S1-ALT Pass 1 sampled coverage RESULT (ACCEPTED): `S1ALT_SOURCE_NOT_VIABLE`.** Pass 1 sampled coverage only; P1 stays blocked.
- `SPEC_price_source_option_b_data_api_review.md` — **ACCEPTED / SPEC ONLY**, at orchestrator review, with two doc-only wording amendments (§8 build-gate wording, §1.1 H2-hypothesis wording). A pessimistic, falsification-minded review of the Polymarket Data API `/trades` endpoint as a per-side/token-identity price-source candidate. Sets out H1 (local backfill incomplete, fixable) vs. H2 (trading genuinely one-sided, unfixable by any retrieval path), composite-identity reconciliation, pagination-completeness, typed numeric parsing, and identifier precision guards as spec-level requirements R1–R7; sets out a bounded two-phase B0/B1 test design (each phase separately authorized, no autonomous escalation); and restates the minimum typed-halt set. A negative/ambiguous result closes **only** the Data API `/trades` candidate on that evidence; a different future candidate source needs a fresh, separately authorized spec; Option C/on-chain reconstruction stays out of scope by guardrail. **Authorizes no implementation, no Phase B0/B1 run, no network/API call, no full Pass 1, no S2, no P1/P2/P3, no probe, no scoring, no backfill, no wallet/OrdersMatched/`log_index`/PnL, no gate change.** A draft Phase B0 implementation (code + tests) produced in the authoring chat thread is **draft/reference only — not an accepted artifact, not committed, not authorized for use as-is** (see `DECISION_LOG.md`). `named_binary_probe_blocked` stays `true`.
- `HANDOFF_orchestrator_option_b_spec_s1_1_patch.md` — Claude-to-Orchestrator handoff recording the final §1.1 wording patch applied to `SPEC_price_source_option_b_data_api_review.md` (the H2-hypothesis sentence), verified by diff to be the only change made on top of the earlier §8 patch. Documentation-only artifact; authorizes nothing.

## Stage 4 audit gate fields (in `named_binary_audit_gate.json` when `--resolution-source` is supplied)
- `gate_state` / `base_gate_state` — legacy pooled-all (stays BLOCKED_BY_RESOLUTION_MAPPING; YES/NO sparsity).
- `gate_policy_note` — describes both the legacy gate and the non-YES/NO branch without contradiction.
- `stage4_nonyesno_branch` — `non_yesno_gate_state` (CLEAR_WITH_WARNINGS), `non_yesno_scoreable`, `non_yesno_pooled_map_rate` (0.99339), `pooled_threshold` 0.99, `subclass_threshold` 0.95, `per_subclass_map_rate`, `per_subclass_scoreable`, and `per_subclass_breakdown`.
- `non_yesno_scoreable_from_source`, `source_winner_count` (39,693), `source_conflict_counts`, `per_subclass_source_coverage`.
- `named_binary_probe_blocked` — always true; CLEAR_WITH_WARNINGS does NOT authorize a probe.

---

## Pinned context (this folder, `project_context/`)

Pin all of the following in the Claude Project Files panel (read `START_HERE.md` first):
- `START_HERE.md` — onboarding + required read order + current branch state + "old chats are not source of truth" rule.
- `PROJECT_STATE.md` — current objective / active / blocked.
- `GUARDRAILS.md` — hard constraints.
- `DECISION_LOG.md` — corrected history / settled decisions.
- `CLOSED_FINDINGS.md` — settled negative/complete results.
- `ARTIFACT_INDEX.md` (this file) — what exists and where.
- `DATA_CONTRACTS_named_binary_probe.md` — exact inspected schemas/API surfaces for the probe.
- `PRICE_INPUT_CONTRACT_named_binary_probe.md` — accepted S0 price-input finding (why P1 is blocked).
- `CLAUDE_PROJECT_SETTINGS.md` — operational Claude capability settings (network allowlist, skills); does not override the above and authorizes nothing.
- Active specs/handoffs as applicable — `SPEC_named_binary_probe.md` (spec only; post-S0 blocker addendum), `SPEC_price_source_s1_coverage.md` (accepted / spec only / coverage-only), `SPEC_price_source_alt_trade_prints.md` (accepted / historical after negative S1-ALT), `SPEC_price_source_option_b_data_api_review.md` (accepted / spec only), `HANDOFF_orchestrator_named_binary_probe_p0.md` (P0 accepted), `HANDOFF_orchestrator_named_binary_probe_p1_REVIEW.md` (P1 paused/blocked), `HANDOFF_orchestrator_option_b_spec_s1_1_patch.md`.
- `ORCHESTRATOR_LOW_CONTEXT_MODE.md` — reusable low-context review/decision protocol. Documentation only; overrides nothing and authorizes nothing.
- Supporting reference (not overriding): `DUNE_DATA_NOTES.md`.

Keep these version-controlled in the repo AND pinned in the Claude Project Files panel; re-upload when changed so the two stay in sync.
