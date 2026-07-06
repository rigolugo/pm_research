# README — Option B Phase B0 implementation package

Status: **CODE / TEST ONLY**.

This package implements only the Phase B0 mechanical-trust reconciliation pilot described in `project_context/SPEC_price_source_option_b_data_api_review.md`. It does **not** authorize a run.

## Files

- `scripts/price_source_option_b_b0_reconciliation.py`
- `tests/test_price_source_option_b_b0_reconciliation.py`

## Scope preserved

- No real API/network call is authorized by this package.
- No B0 execution is authorized by this package.
- No B1, full Pass 1, S2, P1/P2/P3, probe, scoring, backfill, wallet work, OrdersMatched, `log_index`, or PnL.
- No price-series artifact is written.
- No `yes_price`, `1 - price`, `1 - p`, or `1 - yes_price` synthesis.
- `named_binary_probe_blocked` remains true and untouched.

## Local test command only

```powershell
$env:PYTHONPATH="C:\b1\pm_research"
cd C:\b1\pm_research
python -m pytest tests\test_price_source_option_b_b0_reconciliation.py -q
```

## Do not run Phase B0 now

The script is network-hard-gated. A future run, if separately authorized, requires both deliberate flags:

```powershell
python scripts\price_source_option_b_b0_reconciliation.py `
  --root C:\b1\data `
  --manifest artifacts\named_binary_probe\price_source_option_b_b0\option_b_b0_manifest.json `
  --provenance-source-csv artifacts\named_binary_probe\price_source_s1_alt\price_source_s1_alt_coverage_by_condition.csv `
  --artifacts-dir artifacts `
  --allow-network-option-b-b0 `
  --confirm-external-polymarket-data-api
```

That command is shown only to document the future command shape. It is **not authorized now**.

## Manifest requirement

The B0 manifest must be a fixed, provenance-attested list of known-good conditions drawn from accepted S1-ALT `BOTH_SIDES` rows. Template, placeholder, duplicate, bad-scope, and non-`BOTH_SIDES` entries halt with `STOP_SAMPLE_SCOPE_EXCEEDED`.

Expected JSON shape:

```json
{
  "source_artifact": "artifacts/named_binary_probe/price_source_s1_alt/price_source_s1_alt_coverage_by_condition.csv",
  "source_verdict": "S1ALT_SOURCE_NOT_VIABLE",
  "selection_basis": "accepted Option A BOTH_SIDES rows from S1-ALT by-condition ledger",
  "provenance_attestation": "Fixed Phase B0 sample drawn from accepted BOTH_SIDES rows; provenance attested.",
  "conditions": [
    {
      "condition_id": "0x...64 hex...",
      "subclass": "UP_DOWN",
      "level_b_class": "BOTH_SIDES"
    }
  ]
}
```

## Implemented typed halts

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
