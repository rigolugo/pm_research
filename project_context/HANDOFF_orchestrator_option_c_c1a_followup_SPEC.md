# HANDOFF — Orchestrator: Option C C1A follow-up SPEC — FOR REVIEW

**Decision requested:** REVIEW / ACCEPT-OR-BLOCK-AS-SPEC-ONLY.

**Decision posture in delivered spec:** NEEDS VERIFICATION — a safe C1A follow-up selector shape appears possible, but only as a SPEC-only `C1A-F1` selector-policy addendum. No implementation or run is authorized.

**Scope:** Documentation-only follow-up after the accepted C1A `C1_ROW_EXPLOSION` halt. This handoff records the delivered spec and its guardrail posture.

---

## 1. Source read

Canonical repo source of truth: `rigolugo/pm_research`.

Read/reconciled:

1. `START_HERE.md`
2. `project_context/START_HERE.md`
3. `project_context/GUARDRAILS.md`
4. `project_context/PROJECT_STATE.md`
5. `project_context/DECISION_LOG.md`
6. `project_context/CLOSED_FINDINGS.md`
7. `project_context/ARTIFACT_INDEX.md`
8. `project_context/DATA_CONTRACTS_named_binary_probe.md`
9. `project_context/PRICE_INPUT_CONTRACT_named_binary_probe.md`
10. `project_context/SPEC_named_binary_probe.md` context as standing probe block
11. `project_context/SPEC_price_source_s1_coverage.md`
12. `project_context/SPEC_price_source_alt_trade_prints.md` context via canonical state/decision log
13. `project_context/SPEC_price_source_option_b_data_api_review.md` / B0 state context via canonical state/decision log
14. `project_context/SPEC_option_b_b0_failure_diagnostic.md` context via canonical state/decision log
15. `project_context/SPEC_price_source_option_c_onchain.md`
16. `project_context/SPEC_price_source_option_c_onchain_C1R_addendum.md`
17. `project_context/README_price_source_option_c_c1a.md`
18. `project_context/HANDOFF_orchestrator_option_c_c1a_RESULT.md`
19. `project_context/HANDOFF_orchestrator_option_c_c1a_timestamp_fix.md`
20. `project_context/HANDOFF_orchestrator_option_c_c1a_canary_parser_fix.md`
21. `project_context/DUNE_DATA_NOTES.md`
22. Accepted C1A artifacts listed in `ARTIFACT_INDEX.md`, especially `c1a_selector_manifest.json`, `c1a_dune_query.sql`, and `c1a_canary_result.json`.

Note: some referenced historical handoff filenames were not required to be re-derived because current canonical state, decision log, and artifact index already record the accepted C1A status and standing consequences.

---

## 2. Delivered files

- `SPEC_price_source_option_c_c1a_followup.md`
- `HANDOFF_orchestrator_option_c_c1a_followup_SPEC.md`

No code files. No tests. No artifacts.

---

## 3. Core finding of the SPEC

The accepted C1A halt is not a parser defect and not a query-truncation defect. Parser defects and SQL-shape defects were already fixed before the accepted result. The real accepted finding is that at least one fixed condition/window/token-pair branch exceeded the C1A per-condition row cap: 2001 rows against cap 2000.

The follow-up question is therefore selector design only: whether an objective, pre-declared selector can choose a small 3–5 condition manifest that remains within the same caps without hand-picking conditions after seeing C1A rows and without reducing the test to local-`tx_hash` reproduction.

---

## 4. Recommendation

The spec recommends a narrow SPEC-only path named `C1A-F1`:

- deterministic low-density / subclass-balanced selector;
- explicit default selector pool: the already accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool;
- no implication of scanning/profiling the full approximately 288K-condition universe;
- no reusable volume-profiling artifact;
- broader local-only computation only if separately authorized by the Orchestrator;
- outcome-independent;
- no winner/resolution-winner fields;
- no Dune count scout;
- no local `tx_hash` query filter;
- no cap increase;
- no row truncation;
- no ad hoc window narrowing;
- same 3–5 condition canary scale;
- same or lower C1A caps;
- coverage/trust diagnostics only.

The patched spec adds explicit caution that local trade/local tx density is only a weak proxy for on-chain OrderFilled row volume. The accepted C1A diagnostics provide only two non-empty Dune examples, one cap-truncated, and must not be converted into constants, caps, filters, ratios, or guarantees. A low-density condition can still explode; if it does, that is informative and does not authorize cap increases, truncation, retries, or ad hoc window narrowing.

A clean `C1A-F1` run, if ever separately authorized later, would still not be a price-source viability verdict. It would only mean the C1A mechanism produced readable evidence under caps and requires Orchestrator review.

---

## 5. Explicit rejections included

The spec rejects:

1. dropping only the exploding condition;
2. increasing caps;
3. truncating rows;
4. narrowing windows ad hoc;
5. local-`tx_hash` Dune filtering;
6. Dune count scouting before candidate choice;
7. winner/outcome/profit/score-based selection;
8. `yes_price` / complement / side synthesis;
9. OrdersMatched/wallet/`log_index`/PnL expansion;
10. automatic repeated batches or expansion beyond 5 conditions;
11. price artifacts or probe inputs;
12. self-certification of design-clear status;
13. scanning/profiling the full approximately 288K-condition universe without separate authorization;
14. building a reusable volume-profiling artifact;
15. treating local density or accepted C1A ratios as constants, caps, filters, or guarantees;
16. treating low-density row explosion as permission to increase caps, retry, truncate, or narrow windows.

---

## 6. Run remains blocked

The spec explicitly states that another C1A-style bounded user-run remains blocked until:

1. this follow-up spec is reviewed and accepted or patched;
2. a separate code/test-only authorization is issued, if implementation is needed;
3. that implementation is reviewed and accepted;
4. a separate bounded user-run authorization names the accepted selector policy and caps.

No C1B/C2/P1/P2/P3/probe continuation follows from this document. The patched spec also keeps another C1A-style run blocked unless the bounded selector-pool rule and weak-density-proxy cautions are accepted or further patched by the Orchestrator.

---

## 7. Guardrails attestation

Research only. Docs only. No implementation. No code. No tests. No SQL. No candidate lists. No run instructions. No Dune/API/RPC/network call. No new query. No artifact mutation. No cap increase. No row truncation. No ad hoc window narrowing. No C1B/C2/P1/P2/P3/probe. No scanning/profiling the full approximately 288K-condition universe. No reusable volume-profiling artifact. No scoring/backfill/wallet discovery/OrdersMatched expansion/`log_index`/PnL. No price artifact. No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis. No `resolved_winning_token_id` or winner/outcome field for candidate selection. `named_binary_probe_blocked` remains `true`. P1 remains blocked.
