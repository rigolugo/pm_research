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
6. `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md` — ChatGPT/manual-update workflow for canonical files: ChatGPT reads canonical repo files, prepares complete replacement files for user upload, does not write to GitHub, and does not ask Claude to edit canonical docs.
7. `DATA_CONTRACTS_named_binary_probe.md` — exact inspected schemas/API surfaces for the named-binary probe.
8. `PRICE_INPUT_CONTRACT_named_binary_probe.md` — accepted S0 finding on why P1 is blocked on price input.
9. `SPEC_named_binary_probe.md` — governing spec-only document for the future offline probe.
10. `SPEC_price_source_s1_coverage.md` — accepted S1 coverage-only spec. Historical/accepted spec context only; S1 Pass 1 completed with a negative sampled result.
11. `SPEC_price_source_alt_trade_prints.md` — accepted S1-ALT (Option A local trade-print) coverage-only spec, precision-loss correction applied. Historical/accepted spec context only; S1-ALT Pass 1 completed with a negative sampled result.
12. `SPEC_price_source_option_b_data_api_review.md` — accepted Option B Data API `/trades` spec context. Historical/accepted spec context only: original B0 halted and remained inconclusive because required artifacts were missing; the corrected B0 diagnostic later completed and did **not** establish Data API `/trades` mechanical trust. B1 remains unauthorized.
13. `SPEC_option_b_b0_failure_diagnostic.md` — accepted corrected B0 diagnostic spec. Historical/accepted spec context only; the corrected diagnostic harness has since been implemented and user-run under separate authorization with a negative B0 mechanical-trust result.
14. `SPEC_price_source_option_c_onchain.md` — accepted Option C (on-chain / decoded OrderFilled event tables) price-source candidate review, Revision 3. Option C Revision 3 is accepted / spec-only; C0 (candidate/source-interface selection) is accepted / spec-only. At Revision 3, C1 (bounded coverage/trust pilot) was guardrail-blocked — no safe bounded sample design then resolved the local-`tx_hash`-scoping trap. That pre-C1R block is superseded by the separately accepted C1R addendum below.
15. `SPEC_price_source_option_c_onchain_C1R_addendum.md` — accepted C1R (C1 Revised) design addendum, SPEC ONLY. Resolves the Revision-3 scoping trap via a fixed selector manifest (outcome-independent), subquery-wrapped SQL with per-condition cap+1 over-fetch, hard row-cap enforcement, empty-export detection, row-level evidence artifacts, and source-table validation.
16. `README_price_source_option_c_c1a.md` — C1A manifest + bounded canary implementation package (code/test-only, 50 pure-logic tests passing, no network). C1A bounded user-run executed and is accepted as a valid `C1_ROW_EXPLOSION` halt; historical runbook context only, not authorization for another run.
17. `SPEC_price_source_option_c_c1a_followup.md` — ACCEPTED / SPEC ONLY. C1A-F1 selector-policy shape accepted in principle after the accepted C1A `C1_ROW_EXPLOSION` halt. It records that a deterministic, outcome-independent, bounded selector-policy shape can be safe in principle, with the default selector pool limited to the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool unless separately authorized. It authorizes no implementation, no code/test task, no SQL/query generation, no Dune/API/RPC/network run, no cap increase, no row truncation, no C1B/C2/P1/P2/P3/probe, no scoring/backfill/wallet/`log_index`/PnL, and no price artifact.
18. `SPEC_price_source_option_c_c1a_f2_followup.md` — ACCEPTED / SPEC ONLY. C1A-F2 is no-run / artifact-review-only after accepted C1A-F1 mixed evidence. It rejects selector-only F2, another Dune canary, SQL generation/modification, Dune/API/RPC/network calls, local data runs, cap changes, truncation, local-`tx_hash` Dune filtering, Dune count scouting, C1B/C2/P1/P2/P3/probe, scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, price artifacts, gate changes, and side synthesis.
19. `SPEC_price_source_option_c_artifact_enrichment.md` — ACCEPTED / SPEC ONLY. Defines minimum evidence-capture requirements for any possible future Option C / decoded `OrderFilled` diagnostic so local-only, Dune-only, and overlap rows can be reviewed without rerunning or guessing. It authorizes no implementation, tests, local data reads, Dune/API/RPC/network, SQL generation/modification/execution, additional canary, one-condition diagnostic, C1B/C2, P1/P2/P3/probe, scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, price artifact, gate change, cap change, row truncation, or side synthesis.
20. `SPEC_price_source_option_d_l2_archive.md` — ACCEPTED / SPEC ONLY. Defines Option D: L2 order-book vendor archive coverage feasibility for PMXT v2 and Telonex L2 order-book/quote archives. It is coverage/spec methodology only. PMXT scope is v2 only, effective start `2026-04-13T19:00:00Z`; PMXT v1 is out of scope unless separately reviewed. Telonex L2 order-book/quote scope starts `2025-10-11T00:00:00Z`; Telonex on-chain fills from inception are not L2 book coverage. It authorizes no implementation, tests, local temporal precheck, vendor/network fetch, account/API/paid action, Pass 1, Pass 2, price artifact, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis.
21. `SPEC_price_source_option_d_temporal_inrange_precheck.md` — ACCEPTED / SPEC ONLY. Defines the Option D local-only/read-only temporal in-range precheck design. The precheck has now executed under explicit authorization and is ACCEPTED as `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`: PMXT v2 temporal in-range coverage is 18,137 / 39,693 = 0.456932; Telonex L2 temporal in-range coverage is 37,749 / 39,693 = 0.951024. This result is timing-feasibility only. It does not establish vendor availability, token coverage, side coverage, book depth, price quality, mechanical trust, price-source viability, or P1 viability.
22. Latest active handoffs/review memos:
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
    - `HANDOFF_orchestrator_option_c_c1a_RESULT.md`
    - `HANDOFF_orchestrator_option_c_c1a_followup_SPEC.md`
    - `HANDOFF_orchestrator_option_c_c1a_f1_canary_REVIEW.md`
    - `HANDOFF_orchestrator_option_c_c1a_f2_followup_SPEC.md`
    - `HANDOFF_orchestrator_option_c_c1a_f2_ARTIFACT_REVIEW.md`
    - `HANDOFF_orchestrator_option_c_artifact_enrichment_SPEC.md`
    - `HANDOFF_orchestrator_option_d_temporal_inrange_precheck_IMPLEMENTATION_PATCH.md`
    - `HANDOFF_orchestrator_option_d_temporal_inrange_precheck_RESULT.md`
23. `implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`, then `implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md` — active REV23 I0 Claude implementation handoff. Revision 23 with Amendments 01 and 02 is accepted. Gustavo authorized only the pure deterministic contract-core implementation package. Source and test-source authoring are authorized; test execution, local research-data reads, curl/subprocess/network execution, replay, empirical artifacts, P1/P2/P3, and probe execution remain unauthorized.

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

- **Option C (on-chain / decoded OrderFilled event tables) price-source diagnostics: C1A valid halt accepted; C1A-F1 executed and reviewable mixed evidence; C1A-F2 artifact review accepted insufficient.** `SPEC_price_source_option_c_onchain.md` remains the accepted Revision-3 candidate review; C0 remains accepted / spec-only. The Revision-3 C1 guardrail block is superseded by the accepted C1R addendum (`SPEC_price_source_option_c_onchain_C1R_addendum.md`, SPEC ONLY), which defined the fixed selector manifest + cap+1 bounded query design. The original C1A bounded user-run executed and is accepted as a valid halt: manifest `resolved_count = 5`, `excluded_count = 0`; canary outcome `C1_ROW_EXPLOSION`; condition `0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e` returned 2001 rows against `per_condition_row_cap = 2000`, proving cap exceedance rather than truncation. `SPEC_price_source_option_c_c1a_followup.md` accepted the C1A-F1 selector-policy shape in principle; subsequent bounded local-only selector/prep tasks produced a 3-condition C1A-F1 canary package. C1A-F1 then executed and produced reviewable mixed coverage/trust evidence: outcome `C1_CANARY_EXECUTED_NEEDS_REVIEW`; 133 total Dune rows in fixed windows; no row explosion; no unresolved side rows; 34 total Dune-only tx hashes; `NAMED_OTHER` = 104 Dune rows / 27 Dune-only / 2 overlap / 0 local-only / 0 unresolved; `UP_DOWN` = 29 Dune rows / 7 Dune-only / 4 overlap / 0 local-only / 0 unresolved; `OVER_UNDER` = 0 Dune rows / 0 Dune-only / 0 overlap / 2 local-only / 0 unresolved. C1A-F1 is coverage diagnostic only, not a price-source viability verdict; no price was computed or persisted. C1A-F2 artifact review is accepted with result `C1F2_ARTIFACTS_INSUFFICIENT`: the C1A-F1 artifacts are available and confirm the mixed summary plus safe selector/query/cap discipline, but the `OVER_UNDER` local-only evidence lacks local-side timestamp/token/outcome_index/side-match/row-identity/window-membership fields needed for causal classification. No likely-cause label is accepted; no one-condition diagnostic is recommended. It is **not** `C1_CANARY_DESIGN_CLEAR`; Option C is not marked viable; P1 remains BLOCKED; `named_binary_probe_blocked` stays `true`; C1B/C2/P1/P2/P3/probe remain unauthorized.

- **Option D L2 order-book vendor archive coverage spec: ACCEPTED / SPEC ONLY.** Option D is a coverage-only feasibility spec for PMXT v2 and Telonex L2 order-book/quote archives as a fourth candidate per-side/token-identity price-source family. PMXT candidate scope is v2 only from `2026-04-13T19:00:00Z`; PMXT v1 is out of scope unless separately reviewed. Telonex L2 order-book/quote scope starts `2025-10-11T00:00:00Z`; Telonex on-chain fills from inception are not L2 book coverage. Channel-mismatch guards are accepted: `VENDOR_HISTORY_NOT_L2_BOOK_RELEVANT` and `STOP_VENDOR_HISTORY_CHANNEL_MISMATCH`. Best bid, best ask, and mid are diagnostics only; no price-basis decision is accepted. Option D does not unblock P1 and authorizes no temporal precheck, vendor fetch, implementation, tests, Pass 1, Pass 2, price artifact, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis. `named_binary_probe_blocked` remains `true`.

- **Option D temporal in-range precheck: COMPLETED / ACCEPTED — RESULT `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`.** Local-only/read-only run completed with exact P0 reconciliation: 39,693 / 39,693 pooled; UP_DOWN 22,012; OVER_UNDER 1,003; NAMED_OTHER 16,678; no missing first-trade anchors; no missing `resolved_at`; no halt. PMXT v2 temporal in-range coverage: 18,137 / 39,693 = 0.456932 pooled (UP_DOWN 0.529211 / OVER_UNDER 0.661017 / NAMED_OTHER 0.349263). Telonex L2 temporal in-range coverage: 37,749 / 39,693 = 0.951024 pooled (UP_DOWN 0.974696 / OVER_UNDER 0.979063 / NAMED_OTHER 0.918096). PMXT v2 is closed/deprioritized for broad full-P0 Option D coverage on timing grounds. Telonex L2 is plausible only for a later separately authorized SPEC ONLY vendor-coverage review; `NAMED_OTHER` below 0.95 prevents treating it as a clean automatic pass. No vendor data, prices, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis follows. `named_binary_probe_blocked` remains `true`.

- **Local-curl per-side dataset verification Revision 23: ACCEPTED / SPEC ONLY.** The frozen Revision 23 package plus `REV23_AMENDMENT_01` and `REV23_AMENDMENT_02` form the accepted governing contract. No empirical replay has been authorized or performed under this acceptance.

- **REV23 I0 contract-core implementation package: AUTHORIZED / ACTIVE.** Gustavo explicitly authorized Claude to author one narrowly scoped, pure deterministic implementation package under `implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md`. Authorized: source code and unexecuted test-source files for canonical serialization/hashing, identities, manifests, URL/request-plan validation, I0 schemas/state bindings, cancellation proof validation, and HTTP-status reconciliation. Unauthorized: test execution, local research-data reads, curl/subprocess/network execution, reservation or request execution, replay, empirical artifacts, V1/V2/full V0–V10 orchestration, CLI integration, dependency changes, P1/P2/P3, probe, scoring, price construction, side synthesis, wallet/PnL/trading, and gate changes.

- **Chat2 Dune wallet-cohort discovery: BLOCKED.** It is a separate phase. Outcome-source scoreability does not unblock wallet discovery.

---

## Next possible step — only if explicitly authorized by the user

The current authorized step is Claude preparation of the REV23 I0 pure deterministic contract-core implementation package. Claude must return source files, authored-but-unexecuted tests, a conformance report, a changed-file manifest, a patch, an authorization-observed statement, and `TEST_EXECUTION_STATUS.md = NOT_RUN_NOT_AUTHORIZED`.

No test execution follows from I0 implementation authorization. A later test-execution stage requires a separate explicit Gustavo authorization after Sentinel reviews the implementation package.

No further Option B B0 execution is authorized. B1 remains not authorized. Option B should not proceed to B1/full Pass 1/S2/P1/P2/P3/probe.

The C1A-F1 bounded canary has executed and is accepted as reviewable mixed coverage/trust evidence only. The C1A-F2 artifact review has also completed and is accepted as `C1F2_ARTIFACTS_INSUFFICIENT`. No further C1A-F1 run, additional canary, C1B full sampled coverage, C2 reusable/production implementation, P1/P2/P3/probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, cap change, row truncation, SQL modification, or price artifact is authorized by either C1A-F1 or C1A-F2.

**C1B full sampled coverage is not authorized. C2 reusable/production implementation is not authorized. P1/P2/P3/probe remain unauthorized. `named_binary_probe_blocked` remains `true`.**

Any further move remains bounded by the project guardrails. Outside the explicit REV23 I0 source-authoring tranche, no data run, network/API/RPC call, implementation, backfill, scoring, probe, P1/P2/P3 continuation, wallet/OrdersMatched/`log_index`/PnL, or gate change is authorized unless explicitly approved in-chat and allowed by the current repo guardrails. The artifact-enrichment evidence-capture SPEC remains ACCEPTED / SPEC ONLY for the unresolved `OVER_UNDER` evidence gap and authorizes no implementation or run.

For Option D, the temporal in-range precheck has completed and is ACCEPTED. The only possible next Option D step — and only if separately authorized — is a **SPEC ONLY** vendor-coverage review, with Telonex L2 the only broad candidate still plausible from timing coverage. PMXT v2 should not be pursued as broad full-P0 coverage after the 0.456932 pooled temporal result; any PMXT work would require a separate narrow-subset SPEC ONLY framing and must not use an API key or vendor fetch without explicit authorization. No vendor fetch, account/API key use, price build, canonical-side price computation, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, or gate change follows from the temporal result.

---

## What is NOT authorized

No REV23 I0 test execution, lint, coverage, CI execution, local research-data read, curl discovery, subprocess launch, network access, reservation/request execution, replay, empirical capture, compatibility/strict analysis, results/finalization, CLI integration, dependency change, git publication, P1/P2/P3, probe, scoring, price construction, side synthesis, wallet/PnL/trading, or gate change.

No B1, full Pass 1, S2, P1/P2/P3, or probe execution follows from the corrected B0 diagnostic result.

No C1B full sampled coverage, C2 reusable/production implementation, P1/P2/P3 continuation, or probe execution follows from the accepted C1A `C1_ROW_EXPLOSION` halt. No further C1A run is authorized by the historical README/code path unless separately approved.

No C1A-F1 rerun/additional canary, C1B full sampled coverage, C2 reusable/production implementation, P1/P2/P3 continuation, probe execution, cap increase, row truncation, SQL modification, price artifact, or side synthesis follows from the accepted C1A-F1 result or accepted C1A-F2 artifact review. Do not mark `C1_CANARY_DESIGN_CLEAR`; the observed C1A-F1 outcome is `C1_CANARY_EXECUTED_NEEDS_REVIEW`, the accepted C1A-F2 result is `C1F2_ARTIFACTS_INSUFFICIENT`, and the evidence remains mixed/unresolved.

No scoring: no Brier, log-loss, calibration, reliability, splits, or forecast-vs-price metrics.

No wallet work, OrdersMatched expansion, `log_index`, PnL-by-role, gate modification, live trading, paper trading, wallet-copying, or full indexer.

Do not flip `named_binary_probe_blocked`.

Do not use `yes_price`, `1 - price`, or `1 - yes_price` to unblock named-binary pricing.

No additional Option D run, rerun, ledger expansion, vendor/network fetch, PMXT online/API-key test, PMXT raw archive download, Telonex fetch, vendor account/API key/paid action, Pass 1, Pass 2, price artifact, canonical-side price computation, P1/P2/P3/probe execution, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis follows from the accepted Option D temporal in-range result.

---

## Working discipline

* Verify before concluding.
* Never conclude from one row or from an all-one-role/all-one-direction output.
* Spec before implementation.
* Never silently reverse a prior decision.
* Close each task with a Claude-to-Orchestrator handoff memo.
* Canonical project file updates are manual: ChatGPT reads the canonical repo, prepares complete replacement files for the user, and does not write to GitHub. Claude should not be asked to update canonical project files in the repo.
* Claude should treat this public mirror as context only. It authorizes no implementation.
* For REV23 I0, future chats must read the canonical handoff directory. The authorization lives in `implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md`, not in chat memory.
