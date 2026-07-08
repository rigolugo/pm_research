# HANDOFF — Orchestrator: Option C C1A bounded canary RESULT — ACCEPT FINDING

**Decision:** ACCEPT FINDING — C1A bounded canary executed and halted validly on `C1_ROW_EXPLOSION`.

**Scope:** Documentation-only result recording. This handoff records the user-run C1A result and the project-file state update. It authorizes no further Dune/API/RPC/network run, no cap increase, no row truncation, no ad hoc window narrowing, no C1B/C2/P1/P2/P3/probe continuation, no scoring/backfill/wallet discovery/OrdersMatched/`log_index`/PnL, no price artifact, and no side synthesis.

---

## 1. Accepted C1A result

C1A selector-manifest construction completed successfully:

- `resolved_count = 5`
- `excluded_count = 0`

The bounded canary then halted with:

- `canary_outcome = C1_ROW_EXPLOSION`

The halt is accepted as valid. The condition `0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e` returned `2001` rows, exceeding `per_condition_row_cap = 2000`. This is the intended behavior: the generated SQL uses `LIMIT per_condition_row_cap + 1` so the canary can detect cap exceedance rather than silently truncating evidence.

This is a coverage/trust diagnostic only. It is not a price-source viability verdict and it does not compute or persist a price series.

---

## 2. Diagnostic counts reported

Per-condition highlights from the accepted user-run report:

- `0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e`: 2001 Dune rows, 794 Dune-only tx hashes, 136 local-only, 24 overlap, 0 unresolved side rows.
- `0x0cb2...61c2`: 705 Dune rows, 248 Dune-only tx hashes, 0 local-only, 44 overlap, 0 unresolved side rows.
- Three other candidates returned 0 Dune rows and local-only tx hashes.

These diagnostics show that the canary mechanism was able to surface non-local event rows for at least part of the fixed token/window manifest, but the valid cap halt prevents any C1B/C2/P1 conclusion. No viability decision follows from this C1A halt.

---

## 3. Artifacts to record

Artifacts under `artifacts/named_binary_probe/price_source_option_c_c1a/`:

- `c1a_selector_manifest.json`
- `c1a_selector_manifest.csv`
- `c1a_dune_query.sql`
- `c1a_canary_result.json`
- `c1a_canary_result.md`
- `c1a_canary_by_condition.csv`
- `option_c_c1a_raw_rows_sample.csv`
- `option_c_c1a_tagged_rows.csv`

The row-level files are evidence artifacts. They are not reusable price artifacts.

---

## 4. Parser fixes discovered during C1A

Two implementation bugs were discovered and patched during the user-run path:

1. Manifest parser: `parse_ts_utc()` needed datetime-like / pandas `Timestamp` support for `Store.load_trades().traded_at` values.
2. Canary parser: `parse_ts_utc()` needed Dune timestamp string support for forms such as `YYYY-MM-DD HH:MM:SS.fff UTC`, and CSV reading needed UTF-8 BOM tolerance.

These were local parser fixes only. They are not evidence for or against source viability.

---

## 5. Standing state

- P1 remains BLOCKED on the absence of an accepted per-side/token-identity price source.
- C1B full sampled coverage is NOT authorized.
- C2 reusable/production implementation is NOT authorized.
- P1/P2/P3/probe remain unauthorized.
- `named_binary_probe_blocked = true` remains unchanged.
- No scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, price-series artifact, or side synthesis is authorized.

---

## 6. Only possible next step

The only possible next step, if separately authorized later, is SPEC ONLY: a C1A follow-up design to decide whether a bounded candidate-selection rule can avoid row explosion without hand-picking, leakage, or full-indexer behavior.

No implementation or Dune run follows from this result.
