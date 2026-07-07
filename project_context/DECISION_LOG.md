# DECISION LOG

*Corrected history. The most important file in the project: it records what was tried, what was wrong, and what is now settled — so settled questions are not re-litigated.*

---

## Settled decisions (with corrected history)

### Rank 1A decision policy: `first_price_after_warmup`

Chosen over fixed-lead-before-resolution because resolution time is derived from price convergence — a fixed lead would leak the outcome. Decision timestamp = first YES price >= 1h after first trade. Lookahead-safe.

### OrderFilled topic order: topic2=maker, topic3=taker (RESOLVED)

**History (3 reversals before settling):**

1. Initial decode assumed topic2=maker/topic3=taker.
2. A buggy mid-pass showed "both roles" -> reversed to topic2=taker/topic3=maker.
3. Reversal was based on an invalid comparison (local log_index 1227 vs Dune evt_index 1229 — different logs in a multi-fill tx).
4. Resolved by exact-log-index Dune match across BOTH contracts: all rows showed Dune maker == topic2. Reverted to original (topic2=maker). Matches the CTF Exchange V2 source.

**Settled:** `topic1=orderHash, topic2=maker, topic3=taker`. Verified, both contracts.

### The 217/0 and 10/0 "all-taker" results were ARTIFACTS, not findings

- **217/0** (early OrderFilled sample-join): a join-logic artifact compounded by the topic swap.
- **10/0** (first OrdersMatched run): an asset-id precision-loss bug — Dune web-UI CSV export floated 78-digit token IDs into scientific notation and turned `0` into `0.0`, breaking asset matching so no maker could be confirmed.

Lesson: all-one-role outputs are a red flag; validate against a known case before interpreting.

### Asset-id precision fix (two parts)

- Dune query casts uint256 asset/amount fields to varchar.
- Read those columns as `dtype=str`; compare via `canonical_int`; raise `DataExportPrecisionLoss` loudly on scientific notation.

After fix + Dune-API CSV path: MAKER_PAIRING_VALIDATED (4/4), expanded run 100% recoverable / 0 precision-loss.

### Fee-field diagnostic: SUPERSEDED

Inconclusive (`NEED_MORE_SAMPLE`; fee sparse, ~9% nonzero, weak separator). Superseded by OrdersMatched, which gives economic role directly via `takerordermaker`. Artifact preserved; line closed.

### Data hygiene (store contract)

- Missing `condition_id` rows are persisted in raw parquet but DROPPED at analysis load. `save_wallet_trades` keeps them; `load_trades` drops null/blank `condition_id`.
- Trade-id dedup prefers rows with populated semantic keys (tx_hash x4 + token_id x2 + outcome_index x1, stable mergesort).

### Reference cross-checks (external, corroborated)

- antflow Dune queries: OrdersMatched fires once per trade, OrderFilled twice per trade; volume = `LEAST(maker,taker amountFilled)/1e6`.
- warproxxx/poly_data: confirms `/1e6` scaling, USDC side = `assetId == 0`, and the operator-leg filter.
- ghost-hunter: off-chain matches can revert on-chain — a live-execution risk only; on-chain event data excludes ghosts by construction.

### Named-binary semantics validated; probe BLOCKED on missing non-YES/NO outcomes (SETTLED)

- Semantics/orientation validated. The yes_price → canonical_side_price rewrite is complete and audit-gated. Orientation reads token identity (not display label); orientation correctness rate = 1.0; token_id/outcome_index coverage = 0.99601. Classification contract pinned (`nb_contract_version = nb-contract-2026-06-28.1`).
- Audit-reporting Issue A fixed. Schema selection now operates on the cleanly-mappable subset; unmappable rows stay blocked but no longer veto selection.
- local `resolutions.parquet` is YES/NO-only. No team / UP-DOWN / OVER-UNDER winner value appears.
- non-YES/NO named-binary outcomes are unresolvable locally.
- named-binary probe remains BLOCKED until a validated non-YES/NO realized-outcome source exists.

### Named-binary non-YES/NO outcome source implemented and audit-gated — Stage 4 ACCEPTED (SETTLED)

The blocker above is now resolved as a data-availability matter. A Dune-sourced non-YES/NO realized-outcome pipeline (Stages 0–4) was built and accepted.

- **Source.** `polymarket_polygon.ctf_evt_conditionresolution` exposes `payoutnumerators` keyed by `conditionid`; it covers the non-YES/NO named-binary universe. Winners derive ONLY from the payout vector, never from price convergence. Corroboration: `ctf_evt_payoutredemption`.
- **Build.** Stage 3 produced 39,693 RESOLVED_SINGLE_WINNER rows; 253 AMBIGUOUS_MULTIPLE_WINNERS excluded + counted.
- **Gate.** The legacy pooled-all `gate_state` remains BLOCKED_BY_RESOLUTION_MAPPING because local resolutions are YES/NO-only and YES_NO sparsity holds the pooled rate below the 0.99 floor. A separate non-YES/NO branch gate is `CLEAR_WITH_WARNINGS`: non_yesno_pooled_map_rate 0.99339 and each subclass ≥0.95.
- **Probe still blocked.** `named_binary_probe_blocked = true` in all states. CLEAR_WITH_WARNINGS means the outcome source/audit is usable; it does NOT authorize a probe.

### S1 Pass 1 price-source coverage: `S1_SOURCE_NOT_VIABLE` (ACCEPTED, sampled) — SETTLED

The first stage of the per-side price-source build plan was implemented as a coverage-only, network-hard-gated, user-run test and completed with a NEGATIVE Pass-1 sampled result.

- **Result.** Sample 300/300; 248 valid-window conditions measured; 52 invalid-window excluded; 496 side-token fetches; endpoint shape parsed cleanly. Level-B both-sides coverage cleared 0.95 in no subclass: UP_DOWN 19/50 = 0.38, OVER_UNDER 51/98 ≈ 0.5204, NAMED_OTHER 65/100 = 0.65. Verdict `S1_SOURCE_NOT_VIABLE`.
- **Consequence.** CLOB `/prices-history` does not provide a usable decision-window per-side price for both sides across the sampled P0 universe. P1 remains BLOCKED with no `yes_price` fallback. This is Pass 1 sampled coverage only, not Pass 2 full-universe coverage. No Pass 2, S2, P1/P2/P3, probe, scoring, backfill, or gate change is authorized; `named_binary_probe_blocked` stays `true`.
- **Artifact-vs-finding discipline.** The verdict was only trusted after request-window, invalid-window, and timestamp parsing defects were fixed.

### S1-ALT Pass 1 (Option A local trade-print) price-source coverage: `S1ALT_SOURCE_NOT_VIABLE` (ACCEPTED, sampled) — SETTLED

After the S1 negative, the first candidate alternative per-side price source — local trade-print reconstruction via `Store.load_trades()` — was implemented per `SPEC_price_source_alt_trade_prints.md` and completed with a NEGATIVE Pass-1 sampled result.

- **Result.** Reused the exact accepted S1 Pass-1 300-condition sample (248 measured-eligible + 52 S1-invalid-window). Level-B class counts: BOTH_SIDES 124 / ONE_SIDE 65 / NEITHER 59. Level-B both-sides coverage cleared 0.95 in no subclass: UP_DOWN 13/50 = 0.26, OVER_UNDER 40/98 ≈ 0.4081632653, NAMED_OTHER 71/100 = 0.71. Verdict `S1ALT_SOURCE_NOT_VIABLE`.
- **Consequence.** Local trade prints do not provide a usable decision-window per-side price source on the sampled P0 universe. P1 remains BLOCKED with no `yes_price` fallback and no `1 - price` synthesis. No Pass 2, Option C, S2, P1/P2/P3, probe, scoring, backfill, or gate change is authorized; `named_binary_probe_blocked` stays `true`.

### Option B Phase B0 Data API `/trades`: original halt + artifact-missing diagnostic (SUPERSEDED BY CORRECTED B0 RESULT)

`SPEC_price_source_option_b_data_api_review.md` was accepted as a pessimistic, falsification-minded review of the Polymarket Data API `/trades` endpoint as a per-side/token-identity price-source candidate.

The original B0 run halted at `STOP_API_LOCAL_MISMATCH`: `api_count=1747`, `local_count=8`, `matched_count=0`, `mismatch_count=1755`; first mismatches were `API_ONLY` rows. A later local-only artifact inspection halted at `STOP_API_ARTIFACT_MISSING` because only `option_b_b0_manifest.json` had been persisted; no saved API rows, mismatch rows, reconciliation JSON, by-condition CSV, or full evidence ledgers existed.

This original artifact-missing defect is now superseded by the accepted corrected B0 diagnostic result below. Do not reopen the original missing-artifact state as if it were still the final Option B state.

### Option B B0 Failure Diagnostic spec: ACCEPTED / SPEC ONLY (SETTLED)

`SPEC_option_b_b0_failure_diagnostic.md` is the accepted spec-only design for the corrected B0 diagnostic run. The spec targets the original root defect: the first B0 runner evaluated `STOP_API_LOCAL_MISMATCH` before persisting evidentiary artifacts.

**Persistence requirements (D1–D9).** Corrected design requires persist-before-halt ordering with incremental per-condition/per-page writes; full API raw-row ledger (bounded at 25,000 rows); full local comparison rows with load provenance; full bidirectional mismatch ledger including ambiguities; per-condition pagination completeness status; `takerOnly` cardinality measurements; local temporal min/max per condition; API temporal min/max per condition; and offline-recomputable overlap classifications.

**Time-bounded reconciliation safety.** Row-level matching is evaluated only within `[local_min_traded_at − τ, local_max_traded_at + τ]` per condition, where `τ = 120 seconds`. API rows later than `local_max_traded_at + σ` with `σ = 24 hours` are limited to "consistent with H-LOCAL" and never prove local incompleteness.

**Classifications.** Per-condition precedence: `OVERLAP_SCHEMA_BLOCKED` > `OVERLAP_PAGINATION_PARTIAL` > `NO_TEMPORAL_OVERLAP` > `OVERLAP_MATCHED` > `OVERLAP_API_LOCAL_MISMATCH`. Run-level statuses: `API_ARTIFACT_COMPLETE` / `API_ARTIFACT_INCOMPLETE`.

**Locked `OVERLAP_MATCHED` clean bar.** All in-window API rows and all in-window local rows must pair by full composite identity; zero `API_ONLY`; zero `LOCAL_ONLY`; zero `TX_HASH_AMBIGUOUS`; pagination complete; artifacts complete and offline-recomputable. Any shortfall means not matched.

The corrected harness was later implemented and user-run under separate authorization. The completed result is recorded next.

### Option B corrected B0 diagnostic result: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED` (ACCEPTED) — SETTLED

The corrected Option B B0 diagnostic harness was implemented and then user-run under separate authorization to repair the original persist-before-halt defect. The corrected run completed and persisted enough artifacts for offline diagnosis.

**Accepted run result.**

- `artifact_status = API_ARTIFACT_COMPLETE`
- `halt_code = null`
- `manifest_conditions = 10`
- `api_rows_primary = 13,009`
- `api_rows_total_all_query_modes = 17,853`
- `local_rows = 1,346`
- `mismatches = 14,355`

**Classification counts.**

- `OVERLAP_API_LOCAL_MISMATCH = 7`
- `OVERLAP_PAGINATION_PARTIAL = 3`
- `OVERLAP_MATCHED = 0`
- `NO_TEMPORAL_OVERLAP = 0`

**Mismatch counts.**

- `API_ONLY = 11,829`
- `LOCAL_ONLY = 145`
- `TX_HASH_AMBIGUOUS = 2,381`

**Pagination counts.**

- `COMPLETE_SHORT_FINAL_PAGE = 7`
- `PARTIAL_RETRIEVAL = 3`

**Interpretation.** Corrected B0 did **not** establish Data API `/trades` mechanical trust. The earlier `STOP_API_ARTIFACT_MISSING` defect is closed for this corrected run, but the completed evidence is negative for B0 mechanical trust on the fixed manifest: seven conditions show overlap API/local mismatch, three conditions are pagination-partial, and zero conditions are cleanly matched. This is B0 only; it is not a coverage verdict, not a price-source build authorization, and not a downstream gate input.

**Metadata caveat.** `reconciliation.json` reports `takeronly_probe_conditions = 3`, while `offline_recompute_summary.json` reports `takeronly_probe_conditions = 10`. Core fields match: `artifact_status`, `halt_code`, row counts, `mismatch_counts`, `pagination_counts`, and `classification_counts`. Treat this as a metadata/recompute inconsistency only; it does not change the B0 negative finding.

**Standing consequence.** B1 remains not authorized. Option B must not proceed to B1/full Pass 1/S2/P1/P2/P3/probe. P1 remains BLOCKED on the absence of an accepted per-side/token-identity price source. `named_binary_probe_blocked` stays `true`. No scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, price-series artifact, or gate change is authorized.

---

## DO NOT REOPEN unless explicitly asked

- Rung 1 price recalibration (closed negative).
- Fee-field diagnostic (inconclusive, superseded).
- OrderFilled topic-order debate (resolved: topic2=maker, Dune-verified).
- The 217/0 and 10/0 taker artifacts (explained: join artifact + precision-loss bug, both fixed).
- PnL-by-role / H1' (not authorized — separate phase).
- Live / paper trading (permanently out of scope).
- Named-binary semantics/orientation (validated) and Issue-A reporting fix (settled). Do not re-derive.
- Named-binary non-YES/NO outcome source + Stage 4 gate integration (ACCEPTED). Do not re-derive the source, the build, or the gate-policy split. The legacy pooled-all gate stays BLOCKED_BY_RESOLUTION_MAPPING; the non-YES/NO branch is CLEAR_WITH_WARNINGS. The probe itself remains unauthorized.
- S1 Pass 1 sampled coverage result (`S1_SOURCE_NOT_VIABLE`, ACCEPTED). Do not re-derive or re-litigate the sampled negative or per-subclass rates. It is Pass 1 sampled coverage only; a Pass 2 full-universe run or any alternative price source is a separate, explicitly-authorized step. P1 stays blocked with no `yes_price` fallback; the probe stays unauthorized.
- S1-ALT Pass 1 sampled coverage result (`S1ALT_SOURCE_NOT_VIABLE`, ACCEPTED). Do not re-derive or re-litigate the sampled negative or per-subclass rates. It reused the exact accepted S1 Pass-1 sample and is Pass 1 sampled coverage only. P1 stays blocked with no `yes_price` fallback or `1 - price` synthesis; the probe stays unauthorized.
- Option B (Data API `/trades`) corrected B0 state: corrected B0 diagnostic completed with `artifact_status = API_ARTIFACT_COMPLETE`, `halt_code = null`, but did **not** establish mechanical trust (`OVERLAP_API_LOCAL_MISMATCH = 7`, `OVERLAP_PAGINATION_PARTIAL = 3`, `OVERLAP_MATCHED = 0`, `NO_TEMPORAL_OVERLAP = 0`; mismatches `API_ONLY = 11,829`, `LOCAL_ONLY = 145`, `TX_HASH_AMBIGUOUS = 2,381`; pagination `COMPLETE_SHORT_FINAL_PAGE = 7`, `PARTIAL_RETRIEVAL = 3`). Do not re-litigate the original artifact-missing defect; the corrected run has enough evidence and is negative for B0 mechanical trust on the fixed manifest. Metadata caveat: `takeronly_probe_conditions` differs between reconciliation and offline recompute summaries (3 vs 10), but core counts/statuses match and the caveat does not change the negative finding. B1 remains not authorized; no full Pass 1/S2/P1/P2/P3/probe/scoring/backfill is authorized.

---

## Self-correction discipline (meta)

This project corrected itself repeatedly (217/0, topic swap, topic-order mismatch, asset-id precision loss, and the original B0 persist-before-halt defect). Each was caught by validating against authoritative source or persisted artifacts before concluding, not by trusting tooling. Maintain this: one row, one all-one-role output, or one incomplete artifact set is never sufficient to conclude.
