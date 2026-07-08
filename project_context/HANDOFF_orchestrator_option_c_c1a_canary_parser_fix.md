# HANDOFF — Option C C1A Canary Parser Fix

**Decision:** BLOCK fix implemented — local parser / CSV-header normalization only.

## User-run bug

The C1A selector manifest was successfully built:

- `C1A selector manifest: 5 resolved, 0 excluded`

The user then ran Dune and downloaded a structurally valid C1A CSV with the required event columns. The first local canary failure was caused by a UTF-8 BOM on the first header (`\ufeff"block_time"`). After creating a no-BOM copy, the canary progressed and failed on a Dune timestamp string:

```text
ValueError: unparseable timestamp: '2025-05-21 23:59:22.000 UTC'
```

## Root cause

`scripts/price_source_option_c_c1a_canary.py::parse_ts_utc()` accepted only whole-second string formats and did not accept Dune CSV timestamps with fractional seconds plus an explicit `UTC` suffix.

## Patch

Patched `scripts/price_source_option_c_c1a_canary.py`:

- `parse_ts_utc()` now accepts Dune CSV strings such as:
  - `2025-05-21 23:59:22.000 UTC`
  - `2025-05-21 23:59:22 UTC`
- Existing accepted timestamp forms are preserved.
- Explicit `UTC` / `Z` suffixes are treated as UTC, never local time.
- Datetime-like inputs are also accepted defensively:
  - tz-aware values are converted to UTC.
  - tz-naive values are treated as UTC.
- Main CSV loading now opens Dune CSV input with `encoding="utf-8-sig"`, so a UTF-8 BOM on the first header is tolerated.

Patched `tests/test_price_source_option_c_c1a_canary.py`:

- Added tests for fractional-second Dune UTC strings.
- Added tests for whole-second Dune UTC strings.
- Added tests for datetime-like UTC handling.
- Added an end-to-end `main()` test that writes a BOM-prefixed CSV and verifies the canary reads it and reaches `C1_CANARY_EXECUTED_NEEDS_REVIEW` rather than failing schema validation.

## Verification

Command run locally in this sandbox:

```powershell
python -m py_compile scripts/price_source_option_c_c1a_canary.py tests/test_price_source_option_c_c1a_canary.py
python -m pytest tests/test_price_source_option_c_c1a_canary.py tests/test_price_source_option_c_c1a_manifest.py -q
```

Result:

```text
54 passed in 0.16s
```

## Scope attestation

No Dune run was performed. No API/RPC/network call was made. The generated SQL was not changed. The candidate set, caps, manifest scope, and canary reconciliation semantics were not changed. This is not a source viability decision. It is only a local parser and CSV-header tolerance fix.

No C1B/C2/P1/P2/P3/probe behavior was added. No scoring, backfill, wallet work, OrdersMatched expansion, `log_index`, PnL, price-series artifact, or gate change was added. No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis was introduced.
