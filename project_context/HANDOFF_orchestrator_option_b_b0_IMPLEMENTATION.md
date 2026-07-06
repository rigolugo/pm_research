# HANDOFF — Option B Phase B0 implementation package

Decision requested: **NEEDS VERIFICATION** until the user runs the local unit tests.

## Scope delivered

Implemented Phase B0 only as code/tests:

1. `scripts/price_source_option_b_b0_reconciliation.py`
2. `tests/test_price_source_option_b_b0_reconciliation.py`
3. `project_context/README_price_source_option_b_b0.md`
4. This handoff memo

No Phase B0 run was executed. No real API/network call was made. No B1, full Pass 1, S2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, gate edit, or price-series artifact was produced.

## What the code implements

- Two-flag network hard gate: `--allow-network-option-b-b0` and `--confirm-external-polymarket-data-api`.
- Correct data-root contract: future real runs call `Store(root).load_trades()` with `--root C:\b1\data`, not the project root.
- Provenance-attested B0 manifest handling: fixed 10–20 condition list, source artifact/verdict/selection-basis/attestation required, placeholder/template rejection, duplicate rejection, subclass validation, optional verification against accepted S1-ALT by-condition CSV.
- Condition-scoped API retrieval only.
- Hard pagination caps with partial-retrieval halt when the last allowed page is full.
- Typed numeric parsing inside validation for `price`, `size`, and `timestamp`.
- Identifier precision guards for token ids; bounded safe normalization for `outcome_index`.
- Composite one-to-one reconciliation: `tx_hash + token_id + outcome_index + side + price + size + timestamp`.
- Counted mismatch handling for `TX_HASH_AMBIGUOUS`, `API_ONLY`, and `LOCAL_ONLY`; no `tx_hash`-only matching.
- `takerOnly` cardinality/subset probe with typed halt if unresolved.
- Output guard preventing writes to `prices/` or price-series-like paths.
- No `yes_price`, `1 - price`, `1 - p`, or `1 - yes_price` synthesis.

## Typed halts covered

- `STOP_NOT_AUTHORIZED`
- `STOP_CALL_BUDGET_EXCEEDED`
- `STOP_SAMPLE_SCOPE_EXCEEDED`
- `STOP_PAGINATION_UNBOUNDED`
- `STOP_PAGINATION_PARTIAL_RETRIEVAL`
- `STOP_RATE_LIMIT_HIT`
- `STOP_SCHEMA_DEVIATION`
- `STOP_PRECISION_LOSS`
- `STOP_FORBIDDEN_INFERENCE`
- `STOP_NO_WRITE_PATH`
- `STOP_API_LOCAL_MISMATCH`
- `STOP_TAKER_ONLY_CARDINALITY_UNRESOLVED`

## Test command for user

```powershell
$env:PYTHONPATH="C:\b1\pm_research"
cd C:\b1\pm_research
python -m pytest tests\test_price_source_option_b_b0_reconciliation.py -q
```

## Non-authorization reminder

Do **not** run the script against the Polymarket Data API from this handoff. This package is code/test only. A real B0 run requires separate explicit authorization after review.
