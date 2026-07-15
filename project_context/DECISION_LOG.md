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

The corrected harness was later implemented and user-run under separate authorization. The completed result is recorded next.

### Option B corrected B0 diagnostic result: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED` (ACCEPTED) — SETTLED

The corrected Option B B0 diagnostic harness was implemented and then user-run under separate authorization to repair the original persist-before-halt defect. The corrected run completed and persisted enough artifacts for offline diagnosis.

**Accepted run result.** `artifact_status = API_ARTIFACT_COMPLETE`; `halt_code = null`; `manifest_conditions = 10`; `api_rows_primary = 13,009`; `api_rows_total_all_query_modes = 17,853`; `local_rows = 1,346`; `mismatches = 14,355`.

**Classification counts.** `OVERLAP_API_LOCAL_MISMATCH = 7`; `OVERLAP_PAGINATION_PARTIAL = 3`; `OVERLAP_MATCHED = 0`; `NO_TEMPORAL_OVERLAP = 0`.

**Mismatch counts.** `API_ONLY = 11,829`; `LOCAL_ONLY = 145`; `TX_HASH_AMBIGUOUS = 2,381`.

**Pagination counts.** `COMPLETE_SHORT_FINAL_PAGE = 7`; `PARTIAL_RETRIEVAL = 3`.

**Interpretation.** Corrected B0 did **not** establish Data API `/trades` mechanical trust. The earlier `STOP_API_ARTIFACT_MISSING` defect is closed for this corrected run, but the completed evidence is negative for B0 mechanical trust on the fixed manifest. This is B0 only; it is not a coverage verdict, not a price-source build authorization, and not a downstream gate input.

**Metadata caveat.** `reconciliation.json` reports `takeronly_probe_conditions = 3`, while `offline_recompute_summary.json` reports `takeronly_probe_conditions = 10`. Core fields match; treat this as a metadata/recompute inconsistency only.

**Standing consequence.** B1 remains not authorized. Option B must not proceed to B1/full Pass 1/S2/P1/P2/P3/probe. P1 remains BLOCKED on the absence of an accepted per-side/token-identity price source. `named_binary_probe_blocked` stays `true`.

### Option C Revision 3: SPEC ACCEPTED — C0 candidate selected, C1 GUARDRAIL BLOCKED AT REVISION 3 (SETTLED — HISTORICAL; SUPERSEDED FOR C1 BY LATER C1R/C1A DECISIONS)

After Option A/S1-ALT and Option B both closed negative, `SPEC_price_source_option_c_onchain.md` (Revision 3) was accepted as the third per-side/token-identity price-source candidate review: on-chain reconstruction via bounded, already-decoded Dune/vendor OrderFilled event tables.

C0 (candidate/source-interface selection) remains accepted, spec-only. The Revision-3 C1 guardrail block is historical and superseded by C1R/C1A. The unsafe old C1 designs remain closed: local-`tx_hash`-only scoping cannot test missing coverage by construction, and broad independent condition/time-window event querying risks indexer-shaped work.

### Option C C1R (C1 Revised) design addendum: SPEC ACCEPTED (SETTLED — CURRENT STATE FOR C1 DESIGN)

`SPEC_price_source_option_c_onchain_C1R_addendum.md` (Patch 1) is the accepted design that resolves the Revision-3 C1 guardrail block via fixed selector manifest, subquery-wrapped SQL with per-condition cap+1 over-fetch, hard row-cap enforcement, empty-export detection, row-level evidence artifacts, and source-table validation. C1R remains SPEC ONLY by itself: no execution, no Claude run, no Dune/API/RPC call. Pure-logic tests: 50 passing. P1 remains BLOCKED. `named_binary_probe_blocked` stays `true`.

### Option C C1A manifest + bounded canary: ACCEPTED VALID HALT — `C1_ROW_EXPLOSION` (SETTLED)

The C1A implementation package implemented the C1R design. It was code/test-only, pure Python, no-network, with 50 pure-logic tests passing before user execution. The user then executed the bounded C1A flow locally and returned artifacts for review.

**Accepted result.** Selector manifest construction succeeded with `resolved_count = 5` and `excluded_count = 0`. The bounded canary halted with `C1_ROW_EXPLOSION`: condition `0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e` returned `2001` rows, exceeding `per_condition_row_cap = 2000`. This halt is valid and expected because the generated SQL intentionally uses `LIMIT per_condition_row_cap + 1`.

**Interpretation.** This is a valid bounded-canary halt, not a price-source viability verdict. It does not compute or persist price. No C1B/C2/P1 conclusion follows.

### Option C C1A-F1 and C1A-F2: mixed evidence accepted; artifacts insufficient for causal closure (SETTLED)

C1A-F1 executed and produced reviewable mixed coverage/trust evidence: outcome `C1_CANARY_EXECUTED_NEEDS_REVIEW`; 133 total Dune rows in fixed windows; no row explosion; no unresolved side rows; 34 total Dune-only tx hashes; `NAMED_OTHER` = 104 Dune rows / 27 Dune-only / 2 overlap / 0 local-only / 0 unresolved; `UP_DOWN` = 29 Dune rows / 7 Dune-only / 4 overlap / 0 local-only / 0 unresolved; `OVER_UNDER` = 0 Dune rows / 0 Dune-only / 0 overlap / 2 local-only / 0 unresolved.

C1A-F2 artifact review is accepted with result `C1F2_ARTIFACTS_INSUFFICIENT`: the C1A-F1 artifacts confirm the mixed summary plus safe selector/query/cap discipline, but the `OVER_UNDER` local-only evidence is too thin for safe causal classification because the two local-only rows lack local-side timestamp/token/outcome_index/side-match/row-identity/window-membership fields. No likely-cause label is accepted and no one-condition diagnostic is recommended.

Option C is not viable, C1 is not design-clear, P1 remains BLOCKED, and `named_binary_probe_blocked` stays `true`.

### Option C artifact-enrichment evidence-capture SPEC: ACCEPTED / SPEC ONLY — SETTLED

`SPEC_price_source_option_c_artifact_enrichment.md` is accepted as SPEC ONLY. It defines minimum evidence-capture requirements for any possible future Option C / decoded `OrderFilled` diagnostic. It authorizes no implementation, tests, local data reads, Dune/API/RPC/network, SQL generation/modification/execution, additional canary, one-condition diagnostic, C1B/C2/P1/P2/P3/probe, scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, price artifact, gate change, cap change, row truncation, or side synthesis.

### Option D L2 order-book vendor archive coverage spec: ACCEPTED / SPEC ONLY — SETTLED

`SPEC_price_source_option_d_l2_archive.md` is accepted as a methodology/specification document only. It defines Option D as a coverage-only feasibility review for third-party L2 order-book/quote vendor archives as a fourth per-side/token-identity price-source candidate family after S1/S1-ALT/Option B negatives and unresolved Option C evidence.

**Vendor scope.** PMXT scope is **PMXT v2 only**, with effective v2 L2 order-book archive start `2026-04-13T19:00:00Z`; PMXT v1 is out of scope and must not be silently used to extend coverage unless separately reviewed. Telonex L2 order-book/quote scope starts `2025-10-11T00:00:00Z`; Telonex on-chain fills from market inception are not L2 book coverage and must not be used to infer decision-time side prices.

**Channel-mismatch guard.** The accepted guard labels are `VENDOR_HISTORY_NOT_L2_BOOK_RELEVANT` and `STOP_VENDOR_HISTORY_CHANNEL_MISMATCH`. Older or broader non-L2 channels — trades, fills, on-chain fills, metadata, or any other non-book history — must never be substituted for L2 book/quote depth. Better coverage from the wrong channel is not Option D coverage and does not unblock P1.

**Price-basis discipline.** Best bid, best ask, and mid are diagnostics only in the coverage spec. No final canonical price basis is accepted. Any future price-basis decision would require a separately accepted build spec and audit.

**Standing consequence.** Option D acceptance authorizes no implementation, tests, local temporal precheck, vendor/network fetch, PMXT raw archive download, Telonex fetch, vendor account/API key/paid action, Pass 1, Pass 2, price artifact build, canonical-side price computation, P1/P2/P3 continuation, probe execution, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis. P1 remains BLOCKED; `named_binary_probe_blocked` remains `true`.

### Option D temporal in-range precheck SPEC: ACCEPTED / SPEC ONLY — SETTLED

`SPEC_price_source_option_d_temporal_inrange_precheck.md` is accepted as SPEC ONLY. It defines a local-only/read-only timing-feasibility precheck design for Option D.

**Purpose.** The spec asks only what fraction of accepted P0-eligible conditions have both `decision_ts = first_trade_ts + 3600s` and `resolved_at` inside the PMXT v2 and Telonex L2 archive windows.

**Required universe discipline.** The spec must not assume `p0_preflight.json` contains condition-level rows. A future implementation, if separately authorized, must reconstruct and verify the exact P0 universe from the named-binary classification contract joined to `named_binary_resolution_source_rows.parquet`, then reconcile to `final_p0_eligible = 39,693`, with subclass denominators `UP_DOWN = 22,012`, `OVER_UNDER = 1,003`, and `NAMED_OTHER = 16,678`.

**Timestamp discipline.** `first_trade_ts = min(traded_at)` per condition; `decision_ts = first_trade_ts + 3600s`; `resolved_at` comes from `named_binary_resolution_source_rows.parquet`; all timestamps must be normalized to timezone-aware UTC before comparison.

**Vendor constants.** PMXT v2 start is `2026-04-13T19:00:00Z`; Telonex L2 start is `2025-10-11T00:00:00Z`; lower bounds are inclusive.

**Interpretation.** Temporal in-range coverage does not establish vendor availability, token coverage, side coverage, both-side book state, book depth, price quality, mechanical trust, price-source viability, or P1 viability. A positive temporal result may only justify proposing a later separately authorized vendor-coverage SPEC. A negative temporal result may close or deprioritize Option D without touching P1.

**Standing consequence.** This spec authorizes no implementation, tests, local data reads, precheck run, artifact generation, vendor/network fetch, PMXT raw archive download, Telonex fetch, vendor account/API key/paid action, Pass 1, Pass 2, price artifact build, price computation, canonical-side price computation, P1/P2/P3 continuation, probe execution, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis. P1 remains BLOCKED and `named_binary_probe_blocked` remains `true`.

### Option D temporal in-range precheck result: COMPLETED / ACCEPTED — SETTLED

The Option D local-only/read-only temporal in-range precheck was implemented after separate authorization, fixture-tested, user-run locally, and accepted.

**Result label.** `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`.

**Run status.** `COMPLETED`; `halt_code = null`; `uniform_result_detected = false`.

**Universe reconciliation.** Exact accepted P0 match: expected 39,693 / observed 39,693; subclass observed counts UP_DOWN 22,012, OVER_UNDER 1,003, NAMED_OTHER 16,678. No first-trade anchors were missing and no `resolved_at` values were missing.

**Pooled temporal coverage.**
- PMXT v2: 18,137 / 39,693 = 0.456932.
- Telonex L2: 37,749 / 39,693 = 0.951024.

**Subclass temporal coverage.**
- UP_DOWN: PMXT v2 0.529211; Telonex L2 0.974696.
- OVER_UNDER: PMXT v2 0.661017; Telonex L2 0.979063.
- NAMED_OTHER: PMXT v2 0.349263; Telonex L2 0.918096.

**Interpretation.** PMXT v2 is closed/deprioritized for broad full-P0 Option D coverage on timing grounds. A PMXT API key does not change the PMXT v2 archive start-date limitation. Any future PMXT work would require a separate narrow-subset SPEC ONLY authorization and must not be treated as broad P0 coverage. Telonex L2 remains plausible only for a later separately authorized SPEC ONLY vendor-coverage review: pooled temporal coverage narrowly clears 0.95, but NAMED_OTHER is below 0.95, so it is not a clean automatic pass.

**Standing consequence.** Timing feasibility does not establish vendor availability, token coverage, side coverage, both-side book state, book depth, price quality, mechanical trust, price-source viability, or P1 viability. No vendor fetch, PMXT online/API-key test, Telonex fetch, account/API key/paid action, Pass 1, Pass 2, price artifact, bid/ask/mid/spread/depth/canonical-side price computation, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis follows. P1 remains BLOCKED and `named_binary_probe_blocked` remains `true`.

### P0 Representativeness and Quality Audit: ACCEPTED — `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`

Spec `SPEC_p0_representativeness_quality_audit.md`, implementation `scripts/p0_representativeness_quality_audit.py`, tests `tests/test_p0_representativeness_quality_audit.py`. Local-only/read-only run authorized and completed; result accepted.

**Accepted result.** Base P0 (39,693) is valid enough for later historical named-binary research framing, with limitations. The excluded/missing/ambiguous tail (264 conditions) is compositionally skewed relative to included P0, but the impact-weighted comparison `pre_resolution_candidate_vs_final_p0` is CLEAR, so that tail is too small to materially change final P0 composition.

**Vendor subset-bias section.** §6 did not run; it correctly halted with `STOP_OPTION_D_CONDITION_LEDGER_ABSENT` because no condition-level Option D artifact exists. No Option D rerun, re-emission, or recomputation occurred.

**Standing consequence.** This finding does not unblock P1, does not authorize vendor action, does not authorize price-source construction, does not authorize P1/P2/P3/probe, and does not change `named_binary_probe_blocked`. **DO NOT REOPEN** absent a new condition-level Option D artifact or a new representativeness question.

### Local-curl per-side dataset verification Revision 23 with Amendment 03: SPEC ACCEPTED; implementation not authorized — SETTLED

Revision 23 is accepted as the frozen Revision 23 package plus `REV23_AMENDMENT_01`, `REV23_AMENDMENT_02`, and `REV23_AMENDMENT_03`.

Accepted effective hashes:

- specification: `d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9`;
- schema registry: `e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19`;
- request-plan and authorization contract: `8095bb923742e8f7eafac61a1de52d9ff4e5537f8a03bb52af62eb795c9f0f7f`;
- governing-package semantic hash: `6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b`;
- governing-package manifest complete-file hash: `b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa`.

Amendment 03 resolves the token-manifest lifecycle cycle, exact partition/request schemas, typed-tag and null rules, integer pre-run identity timestamp, total raw-evidence-bound HTTP reconciliation, and the completed-capture lifecycle path. Populations remain 600 token-manifest rows, 496 request-manifest rows, and 496 request-plan rows. The twelve-field `run_id`, denominators, thresholds, result ordering, guardrails, P1 block, and `named_binary_probe_blocked = true` remain unchanged.

The prior I0 source/test-source authorization was tied to the Amendments-01/02 contract bytes. It does not authorize work against Amendment 03 and is superseded/inactive. The previously submitted Claude implementation package was blocked and is not accepted as conformant.

**Current authorization:** specification accepted and canonicalized only. No implementation correction, source/test-source authoring, tests, Python/project-code execution, local-data read, curl/subprocess/network action, reservation, replay, empirical artifact, P1/P2/P3, probe, scoring, price construction, wallet/PnL/trading, or gate change is authorized. A later implementation stage requires a new explicit Gustavo authorization and a newly pinned handoff.

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
- Option B corrected B0 state (`B0_MECHANICAL_TRUST_NOT_ESTABLISHED`). Do not re-litigate the original artifact-missing defect; the corrected run has enough evidence and is negative for B0 mechanical trust on the fixed manifest. B1 remains not authorized; no full Pass 1/S2/P1/P2/P3/probe/scoring/backfill is authorized.
- Option C Revision 3 SPEC ONLY acceptance, C1R accepted design, C1A accepted valid halt, C1A-F1 mixed evidence, and C1A-F2 insufficient-artifact result. Do not reopen old unsafe C1 designs, do not mark C1 design-clear, and do not authorize C1B/C2/P1/P2/P3/probe from these findings.
- Option D L2 order-book vendor archive coverage SPEC (`OPTION_D_SPEC_ACCEPTED_SPEC_ONLY`). Do not substitute non-L2 channels for L2 book depth; do not treat best bid/ask/mid diagnostics as an accepted price basis; P1 stays blocked.
- Option D temporal in-range precheck SPEC and result (`OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`). Do not re-run or reinterpret the temporal precheck without explicit authorization. Do not treat timing feasibility as vendor availability, side/token coverage, book depth, price quality, mechanical trust, price-source viability, or P1 viability. PMXT v2 is closed/deprioritized for broad full-P0 coverage on timing grounds; Telonex L2 may only proceed to a separately authorized SPEC ONLY vendor-coverage review.
- P0 Representativeness and Quality Audit result (`P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`). Do not reinterpret the excluded-tail skew as broad P0 bias; the impact-weighted pre-resolution-vs-final-P0 comparison is CLEAR. Do not use this result to unblock P1, authorize vendor action, authorize price-source construction, authorize P1/P2/P3/probe, or change gates.
- REV23 Amendment 03 acceptance. Do not restore the old run-scoped token manifest, the six-field partition shorthand, conflicting request schemas, string-valued pre-run timestamp, partial HTTP mapping, or a completed-capture path that bypasses reconciliation.
- Prior REV23 I0 authorization. Do not treat the superseded Amendments-01/02 source/test-source authorization or old Claude prompt as permission to implement Amendment 03. Any new implementation or test-source authoring requires a separate explicit Gustavo authorization pinned to the current canonical hashes.

---

## Self-correction discipline (meta)

This project corrected itself repeatedly (217/0, topic swap, topic-order mismatch, asset-id precision loss, the original B0 persist-before-halt defect, the REV23 manifest size correction, and the Revision-23 I0 conformance/lifecycle contradictions). Each was caught by validating against authoritative source or persisted artifacts before concluding, not by trusting tooling. Maintain this: one row, one all-one-role output, one incomplete artifact set, or one unverified hash/size pair is never sufficient to conclude.
