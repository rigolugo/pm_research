# PROJECT STATE

*Current objective, environment, and active tasks. Source of truth for "what are we doing now."*

---

## Current Objective

Stay **Polymarket-native**. The wallet-edge thesis has been weakened across three angles (see CLOSED_FINDINGS), so effort moves to a larger, untested universe.

- **Named-binary semantics layer: DONE / audit-gated.** The yes_price → canonical_side_price rewrite is implemented, tested, and validated on the full dataset (orientation 1.0, coverage 0.99601, YES/NO resolution 8,521/8,521). Classification contract pinned (`nb-contract-2026-06-28.1`).

- **Non-YES/NO realized-outcome source: DONE / audit-gated (CLEAR_WITH_WARNINGS).** Dune `ctf_evt_conditionresolution` payout vectors source the non-YES/NO outcomes (Stages 0–4, accepted). Stage 3 built 39,693 RESOLVED_SINGLE_WINNER rows (253 ambiguous excluded + counted). Stage 4 added the additive `--resolution-source` audit flag. The **legacy pooled-all `gate_state` stays BLOCKED_BY_RESOLUTION_MAPPING** (local resolutions are YES/NO-only; YES_NO maps ~0.13, below the pooled floor). A **separate non-YES/NO branch gate is CLEAR_WITH_WARNINGS** (pooled 0.99339 ≥ 0.99; each subclass ≥ 0.95: UP_DOWN 0.99995 / NAMED_OTHER 0.98657 / OVER_UNDER 0.96535). Per-subclass counts separate missing_source_rows from AMBIGUOUS_MULTIPLE_WINNERS. Stage 4 local verification: 87 passed in 1.25s.

- **Named-binary probe: NOT AUTHORIZED.** `named_binary_probe_blocked = true` in all gate states. CLEAR_WITH_WARNINGS means the outcome source/audit is usable — it does NOT authorize a probe. Do not conflate outcome-source scoreability with probe authorization.

- **Named-binary offline probe spec: ACCEPTED / SPEC ONLY.** `SPEC_named_binary_probe.md` is the governing spec-only document for a future offline historical non-YES/NO named-binary forecast-vs-price probe. It authorizes no implementation, no data run, and no probe execution.

- **Named-binary probe Stage P0 preflight: ACCEPTED / P0_CLEAR.** `scripts/named_binary_probe_p0_preflight.py` (read-only except for its P0 artifacts) was implemented, tested (22 passed), and accepted. On real data it emitted eligible/excluded universe counts ONLY: contract_eligible 39,957; resolved_single_winner 39,693; ambiguous_multiple_winners 253; source_rows 39,946; missing_source_rows 11; final_p0_eligible 39,693; `p0_state = P0_CLEAR`. `probe_execution_authorized = False`; `named_binary_probe_blocked` observed True, **not flipped**; gate not modified; no trades/prices, no decision timestamps, no canonical_side_price, no Brier/log-loss/calibration/reliability, no wallet discovery, no PnL. **P0 does NOT authorize P1/P2/P3 or probe execution** — it only verified the universe before any metric exists. Artifacts: `artifacts/named_binary_probe/p0_preflight.{json,md}` + `p0_excluded_counts.csv`.

- **Named-binary probe Stage P1 (feature assembly): BLOCKED on price input.** P1 was attempted, paused for data-contract review, and is now blocked on a proven data-availability gap. The accepted semantics layer's `OrientationContract.canonical_side_price(side_0_price, side_1_price)` requires **two per-side prices** in `outcome_index` order, but `Store.load_prices()` exposes only `[condition_id, ts, yes_price]` — a single scalar. **S0 price-input inspection: ACCEPTED.** `PRICE_INPUT_CONTRACT_named_binary_probe.md` proves from source (`pm_research/data/backfill.py`, `schemas.py`, `audit_market_structure.py`) that the local `yes_price` is a **YES/NO-only** construction (`price where outcome=="YES" else 1-price`), explicitly flagged **unsafe** for UP_DOWN / OVER_UNDER / NAMED_OTHER, and that **no local per-side/per-token price artifact exists**. The price *formula* is resolved (DATA_CONTRACTS §6); the price *input* is not derivable locally. `named_binary_probe_blocked` stays `true`. S0 produced no code changes and no probe artifacts (only the inspection report).

- **S1 price-source coverage spec: ACCEPTED / SPEC ONLY.** `SPEC_price_source_s1_coverage.md` is the accepted, **coverage-only** plan for testing whether Polymarket CLOB `/prices-history` per token can cover the P0 universe with a usable decision-time per-side price for both sides. It does NOT unblock P1 by itself and authorizes no downstream work.

- **S1 Pass 1 sampled coverage: COMPLETED / ACCEPTED — RESULT: `S1_SOURCE_NOT_VIABLE`.** On the accepted run: sample 300/300; 248 valid-window conditions measured; 52 invalid-window excluded; 496 side-token fetches; endpoint shape parsed cleanly. Level-B both-sides coverage cleared 0.95 in no subclass: UP_DOWN 19/50 = 0.38, OVER_UNDER 51/98 ≈ 0.5204, NAMED_OTHER 65/100 = 0.65. Verdict `S1_SOURCE_NOT_VIABLE`. This is Pass 1 sampled coverage only, not Pass 2 full-universe coverage. P1 remains BLOCKED with no `yes_price` fallback. No Pass 2, S2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/log_index/PnL, or gate change is authorized; `named_binary_probe_blocked` stays `true`.

- **S1-ALT Pass 1 (Option A local trade-print) sampled coverage: COMPLETED / ACCEPTED — RESULT: `S1ALT_SOURCE_NOT_VIABLE`.** The first candidate alternative after the S1 negative — local trade-print reconstruction via `Store.load_trades()` — was implemented per `SPEC_price_source_alt_trade_prints.md`, patched through review, user-run, and accepted as sampled coverage. It reused the exact accepted S1 Pass-1 300-condition sample. Level-B both-sides coverage again cleared 0.95 in no subclass: UP_DOWN 13/50 = 0.26, OVER_UNDER 40/98 ≈ 0.4082, NAMED_OTHER 71/100 = 0.71. Verdict `S1ALT_SOURCE_NOT_VIABLE`. P1 remains BLOCKED with no `yes_price` fallback and no `1 - price` synthesis. No Pass 2, Option C, S2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/log_index/PnL, or gate change is authorized; `named_binary_probe_blocked` stays `true`.

- **Option B Data API `/trades` corrected B0 diagnostic: COMPLETED / ACCEPTED — RESULT: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.** The accepted Option B Data API `/trades` spec remains historical context. The original B0 execution halted at `STOP_API_LOCAL_MISMATCH`, and local-only failure diagnosis halted at `STOP_API_ARTIFACT_MISSING` because only the manifest was persisted. That original artifact-missing defect is superseded by the corrected B0 diagnostic result. The corrected B0 diagnostic harness was implemented and then user-run under separate authorization. It completed with `artifact_status = API_ARTIFACT_COMPLETE` and `halt_code = null`, so the prior missing-artifact defect is closed for this corrected run. On the fixed 10-condition manifest: `api_rows_primary = 13,009`, `api_rows_total_all_query_modes = 17,853`, `local_rows = 1,346`, `mismatches = 14,355`. Classifications: `OVERLAP_API_LOCAL_MISMATCH = 7`, `OVERLAP_PAGINATION_PARTIAL = 3`, `OVERLAP_MATCHED = 0`, `NO_TEMPORAL_OVERLAP = 0`. Mismatches: `API_ONLY = 11,829`, `LOCAL_ONLY = 145`, `TX_HASH_AMBIGUOUS = 2,381`. Pagination: `COMPLETE_SHORT_FINAL_PAGE = 7`, `PARTIAL_RETRIEVAL = 3`. Therefore corrected B0 did **not** establish Data API `/trades` mechanical trust. **B1 remains not authorized.** Option B must not proceed to B1/full Pass 1/S2/P1/P2/P3/probe. P1 remains BLOCKED on the absence of an accepted per-side/token-identity price source. No scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, price-series artifact, or gate change is authorized. `named_binary_probe_blocked` stays `true`, not flipped. Minor metadata caveat: `reconciliation.json` reports `takeronly_probe_conditions = 3`, while `offline_recompute_summary.json` reports `takeronly_probe_conditions = 10`; core `artifact_status`, `halt_code`, row counts, `mismatch_counts`, `pagination_counts`, and `classification_counts` match, so this is a metadata/recompute inconsistency only and does not change the B0 negative finding. Handoff: `HANDOFF_orchestrator_option_b_b0_corrected_diagnostic_RESULT.md`.

- **Option B B0 Failure Diagnostic spec: ACCEPTED / SPEC ONLY; corrected harness later executed under separate authorization.** `SPEC_option_b_b0_failure_diagnostic.md` is the accepted design that fixed the original B0 root defect: the first B0 runner evaluated `STOP_API_LOCAL_MISMATCH` before persisting evidence. The spec required persist-before-halt ordering (D1), full API/local/mismatch ledgers, per-condition temporal bounds and pagination status, takerOnly cardinality status, offline-recomputable overlap classifications, locked constants `τ = 120 seconds`, `σ = 24 hours`, and primary API row-ledger cap 25,000 rows total. The corrected diagnostic run is now accepted negative for B0 mechanical trust as recorded above; the spec itself remains historical/accepted context and authorizes nothing further.

- **Option C (on-chain / decoded OrderFilled event tables) price-source spec: ACCEPTED / SPEC ONLY (Revision 3).** `SPEC_price_source_option_c_onchain.md` is the accepted third candidate review for the named-binary P1 per-side price-source search, after Option A/S1-ALT and Option B (both closed negative). **C0** — bounded decoded Dune/vendor OrderFilled event tables as the candidate — remains accepted as **source-interface/spec verification only**: no coverage claim, no run, no artifact beyond the spec record. **At Revision 3, C1** (a bounded coverage/trust pilot analogous to Option B's B0) **was guardrail-blocked**: no safe bounded sample design then resolved the local-`tx_hash`-scoping trap — scoping by local `tx_hash` likely reproduces S1-ALT and cannot test missing coverage by construction, while independent condition/time-window event querying risks broad event reconstruction / indexer-shaped work under the "No full indexer" guardrail. **That pre-C1R block is superseded by the separately accepted `SPEC_price_source_option_c_onchain_C1R_addendum.md`** (SPEC ONLY): C1R resolves the design-level scoping trap via a fixed selector manifest (outcome-independent), subquery-wrapped SQL with per-condition `cap+1` over-fetch, hard row-cap enforcement, empty-export detection, row-level evidence, and source-table validation. **C1A (manifest + bounded canary) is authorized for user-run only** (code/test-only, 50 tests passing; not for Claude execution). **No C1A result exists yet. C1B full sampled coverage is not authorized. C2 reusable/production implementation is not authorized.** P1 remains BLOCKED; `named_binary_probe_blocked` stays `true`. Handoffs: `HANDOFF_orchestrator_option_c_onchain_spec.md`, `HANDOFF_orchestrator_option_c_c1r_design_addendum.md`, `HANDOFF_orchestrator_option_c_c1a_IMPLEMENTATION.md`.

- **Chat2 Dune wallet cohort discovery: BLOCKED** unless separately authorized. It consumes the named-binary contract but is a distinct phase; do NOT conflate the now-usable outcome source with wallet discovery. Outcome-source scoreability does not unblock Chat2.

---

## Environment

- **Execution:** Windows / Miniconda, local. conda env `pmresearch` (Python 3.11; pandas, pyarrow, numpy, scipy, sklearn, requests, pycryptodome present). NOT EC2 (OOM-prone).
- **Project path:** `C:\b1\pm_research`
- **Data path:** `C:\b1\data` (trades, prices, markets.parquet, resolutions.parquet)
- **Artifacts path:** `C:\b1\pm_research\artifacts`
- **PYTHONPATH:** set `$env:PYTHONPATH="C:\b1\pm_research"` once per PowerShell session for bare `python scripts\...` calls.
- **Dune API CSV (full precision):** `curl.exe -H "x-dune-api-key: $env:DUNE_API_KEY" "https://api.dune.com/api/v1/query/<id>/results/csv?limit=5000" -o <out>.csv` — only if the saved query casts uint256 fields to varchar AND the query has been executed on Dune. Use `curl.exe` (not PowerShell's `curl` alias) and `$env:DUNE_API_KEY`.
- **Dataset:** 16,505,185 trades / 288,684 conditions (distinct condition_ids present in `trades\*.parquet`, per the named-binary audit's reproducible `total_conditions`); key coverage (tx_hash/token_id/outcome_index) ~99.6%.

---

## Workflow

- Claude works in its sandbox (no network/pytest/keccak guaranteed), verifies logic via direct python + monkeypatched reads when code is authorized, and **delivers files** for the user to copy into the Windows tree.
- User runs locally, pastes outputs back.
- Each task closes with a **Claude-to-Orchestrator handoff memo**.
- Start a fresh chat per task to keep context lean.

---

## Completed — Non-YES/NO realized-outcome source (Stages 0–4, ACCEPTED)

`SPEC_named_binary_resolution_source.md` is now implemented and accepted, Stages 0–4:

- **Stage 0** — Dune schema inspection confirmed `ctf_evt_conditionresolution` (payoutnumerators array(uint256), keyed by conditionid) + `ctf_evt_payoutredemption` corroboration.
- **Stage 1** — Dune SQL package + coverage measurement: non-YES/NO coverage ~1.0, exact-winner 0.965–0.99995 per subclass.
- **Stage 2** — `pm_research/semantics/resolution_source.py`: pure payout-vector winner derivation + slot→token mapping + 8-status conflict model.
- **Stage 3** — `scripts/build_named_binary_resolution_source.py`: 39,693 RESOLVED_SINGLE_WINNER rows; 253 ambiguous excluded + counted.
- **Stage 4** — additive `--resolution-source` audit flag + non-YES/NO branch gate = CLEAR_WITH_WARNINGS; legacy pooled-all gate stays BLOCKED; probe stays blocked.

Winners derive ONLY from payout numerators, never from price convergence. The named-binary probe remains NOT AUTHORIZED — a CLEAR* gate does not grant it. `SPEC_named_binary_probe.md` is ACCEPTED (spec only); its Stage P0 preflight is implemented and ACCEPTED (`P0_CLEAR`). Stage P1 remains BLOCKED on a proven price-input gap. The only further named-binary step, if explicitly authorized, is a separate price-source continuation under current guardrails; no P1/P2/P3 or probe execution is authorized.

---

## Blocked — Dune wallet cohort discovery (Chat2)

Still BLOCKED; requires SEPARATE explicit authorization. The non-YES/NO outcome source is now usable, but outcome-source scoreability does NOT unblock Chat2 — wallet discovery is a distinct phase. When/if authorized: identify named-binary active wallets; classify maker/taker via OrdersMatched (validated machinery); strict discovery vs holdout split; no PnL-based selection without holdout; no copy-trading.
