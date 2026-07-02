# PROJECT STATE

*Current objective, environment, and active tasks. Source of truth for "what are we doing now."*

---

## Current Objective

Stay **Polymarket-native**. The wallet-edge thesis has been weakened across three angles (see CLOSED_FINDINGS), so effort moves to a larger, untested universe.

- **Named-binary semantics layer: DONE / audit-gated.** The yes_price → canonical_side_price rewrite is implemented, tested, and validated on the full dataset (orientation 1.0, coverage 0.99601, YES/NO resolution 8,521/8,521). Classification contract pinned (`nb-contract-2026-06-28.1`).
- **Non-YES/NO realized-outcome source: DONE / audit-gated (CLEAR_WITH_WARNINGS).** Dune `ctf_evt_conditionresolution` payout vectors source the non-YES/NO outcomes (Stages 0–4, accepted). Stage 3 built 39,693 RESOLVED_SINGLE_WINNER rows (253 ambiguous excluded + counted). Stage 4 added the additive `--resolution-source` audit flag. The **legacy pooled-all `gate_state` stays BLOCKED_BY_RESOLUTION_MAPPING** (local resolutions are YES/NO-only; YES_NO maps ~0.13, below the pooled floor). A **separate non-YES/NO branch gate is CLEAR_WITH_WARNINGS** (pooled 0.99339 ≥ 0.99; each subclass ≥ 0.95: UP_DOWN 0.99995 / NAMED_OTHER 0.98657 / OVER_UNDER 0.96535). Per-subclass counts separate missing_source_rows from AMBIGUOUS_MULTIPLE_WINNERS. Stage 4 local verification: 87 passed in 1.25s.
- **Named-binary probe: NOT AUTHORIZED.** `named_binary_probe_blocked = true` in all gate states. CLEAR_WITH_WARNINGS means the outcome source/audit is usable — it does NOT authorize a probe. Do not conflate outcome-source scoreability with probe authorization.
- **Named-binary offline probe spec: ACCEPTED / SPEC ONLY.** `SPEC_named_binary_probe.md` is the governing spec-only document for a future offline historical non-YES/NO named-binary forecast-vs-price probe. It authorizes no implementation, no data run, and no probe execution.
- **Named-binary probe Stage P0 preflight: ACCEPTED / P0_CLEAR.** `scripts/named_binary_probe_p0_preflight.py` (read-only except for its P0 artifacts) was implemented, tested (22 passed), and accepted. On real data it emitted eligible/excluded universe counts ONLY: contract_eligible 39,957; resolved_single_winner 39,693; ambiguous_multiple_winners 253; source_rows 39,946 (= resolved + ambiguous); missing_source_rows 11; final_p0_eligible 39,693; `p0_state = P0_CLEAR`. `probe_execution_authorized = False`; `named_binary_probe_blocked` observed True, **not flipped**; gate not modified; no trades/prices, no decision timestamps, no canonical_side_price, no Brier/log-loss/calibration/reliability, no wallet discovery, no PnL. **P0 does NOT authorize P1/P2/P3 or probe execution** — it only verified the universe before any metric exists. Artifacts: `artifacts/named_binary_probe/p0_preflight.{json,md}` + `p0_excluded_counts.csv`.
- **Named-binary probe Stage P1 (feature assembly): BLOCKED on price input.** P1 was attempted, paused for data-contract review, and is now blocked on a proven data-availability gap. The accepted semantics layer's `OrientationContract.canonical_side_price(side_0_price, side_1_price)` requires **two per-side prices** in `outcome_index` order, but `Store.load_prices()` exposes only `[condition_id, ts, yes_price]` — a single scalar. **S0 price-input inspection: ACCEPTED.** `PRICE_INPUT_CONTRACT_named_binary_probe.md` proves from source (`pm_research/data/backfill.py`, `schemas.py`, `audit_market_structure.py`) that the local `yes_price` is a **YES/NO-only** construction (`price where outcome=="YES" else 1-price`), explicitly flagged **unsafe** for UP_DOWN / OVER_UNDER / NAMED_OTHER, and that **no local per-side/per-token price artifact exists**. The price *formula* is resolved (DATA_CONTRACTS §6); the price *input* is not derivable locally. `named_binary_probe_blocked` stays `true`. S0 produced no code changes and no probe artifacts (only the inspection report).
- **Next possible step, only if explicitly authorized by the user:** a **spec-only price-source build plan** for a per-side / token-identity-keyed decision-time price series (e.g. a new artifact `[condition_id, ts, outcome_index/token_id, side_price]` sourced from CLOB/print history per token), analogous to the Stage 0–4 non-YES/NO resolution-source build. **Spec only** — no implementation, no data run, no backfill, no scoring, no probe. P1 cannot resume until such a price source exists and is audit-checked. **No P1/P2/P3 or probe execution is authorized.**
- **Chat2 Dune wallet cohort discovery: BLOCKED** unless separately authorized. It consumes the named-binary contract but is a distinct phase; do NOT conflate the now-usable outcome source with wallet discovery. Outcome-source scoreability does not unblock Chat2.

---

## Environment

- **Execution:** Windows / Miniconda, local. conda env `pmresearch` (Python 3.11; pandas, pyarrow, numpy, scipy, sklearn, requests, pycryptodome present). NOT EC2 (OOM-prone).
- **Project path:** `C:\b1\pm_research`
- **Data path:** `C:\b1\data` (trades, prices, markets.parquet, resolutions.parquet)
- **Artifacts path:** `C:\b1\pm_research\artifacts`
- **PYTHONPATH:** set `$env:PYTHONPATH="C:\b1\pm_research"` once per PowerShell session for bare `python scripts\...` calls.
- **Dune API CSV (full precision):** `curl.exe -H "x-dune-api-key: $env:DUNE_API_KEY" "https://api.dune.com/api/v1/query/<id>/results/csv?limit=5000" -o <out>.csv` — only if the saved query **casts uint256 fields to varchar** AND the query has been **executed** on Dune (API serves the last execution, not the saved SQL). Use `curl.exe` (not PowerShell's `curl` alias) and `$env:DUNE_API_KEY`.
- **Dataset:** 16,505,185 trades / 288,684 conditions (distinct condition_ids present in `trades\*.parquet`, per the named-binary audit's reproducible `total_conditions`; supersedes the earlier 288,685 carried-forward figure, which had no documented derivation — difference is one condition, likely a null/blank or trade-absent condition); key coverage (tx_hash/token_id/outcome_index) ~99.6%.

---

## Workflow

- Claude works in its sandbox (no network/pytest/keccak guaranteed), verifies logic via direct python + monkeypatched reads, and **delivers files** for the user to copy into the Windows tree.
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

Winners derive ONLY from payout numerators, never from price convergence. The named-binary probe remains NOT AUTHORIZED — a CLEAR* gate does not grant it. `SPEC_named_binary_probe.md` is ACCEPTED (spec only); its **Stage P0 preflight is implemented and ACCEPTED (P0_CLEAR)**. **Stage P1 (feature assembly) is BLOCKED on a proven price-input gap** — the local `yes_price` is YES/NO-only and unsafe for named-binary canonical-side pricing, and no local per-side price series exists (`PRICE_INPUT_CONTRACT_named_binary_probe.md`, accepted). The only further named-binary step, if explicitly authorized, is a spec-only price-source build plan for a per-side/token-identity price series; no P1/P2/P3 or probe execution is authorized.

---

## Blocked — Dune wallet cohort discovery (Chat2)

Still BLOCKED; requires SEPARATE explicit authorization. The non-YES/NO outcome source is now usable, but **outcome-source scoreability does NOT unblock Chat2** — wallet discovery is a distinct phase. When/if authorized: identify named-binary active wallets; classify maker/taker via OrdersMatched (validated machinery — see CLOSED_FINDINGS / ARTIFACT_INDEX); strict discovery vs holdout split; no PnL-based selection without holdout; no copy-trading.
