# HANDOFF — Orchestrator: Option C C1A manifest timestamp parsing fix

**Decision requested:** REVIEW / APPROVE-OR-BLOCK.

**Scope:** Narrow bug-fix patch after the user-run C1A manifest diagnostic exposed that
`Store.load_trades().traded_at` can be `datetime64[us, UTC]` / pandas `Timestamp` values and the
C1A manifest parser rejected every row as `unparseable window bound`.

No Dune/API/RPC/network call was performed. No real C1A canary was run. This patch changes only the
manifest timestamp parser and its tests.

---

## 1. User-run bug

Reported local diagnostic:

- candidate_count: 5
- local_trade_rows_for_candidates: 469
- `traded_at dtype: datetime64[us, UTC]`
- for every candidate: `parse_ok: 0`, `parse_fail == raw_rows`, `in_window_rows: 0`, token pair unresolved
- examples were pandas datetime-like values such as `Timestamp('2025-11-01 09:06:02+0000', tz='UTC')`
- C1A parser error: `unparseable window bound`

Root cause confirmed in code: `scripts/price_source_option_c_c1a_manifest.py::parse_ts_utc()` handled
epoch numbers and a few string formats, but did not handle `datetime` / pandas `Timestamp` objects.
The real loader path passes `grp["traded_at"]` values directly to `parse_ts_utc()`, so datetime-like
values were skipped in `load_trades_for_conditions()`, leaving every candidate with zero in-window
trade rows.

---

## 2. Exact fix

Patched `parse_ts_utc()` to accept datetime-like values:

- if `isinstance(value, datetime)` and tz-aware, return `value.timestamp()`;
- if tz-naive, treat it as UTC via `value.replace(tzinfo=timezone.utc).timestamp()`;
- pandas `Timestamp` is covered because it is datetime-like in the test/runtime environment;
- retained numeric epoch handling;
- added low-risk ISO support through `datetime.fromisoformat()` for fractional seconds and timezone
  suffixes such as `Z` / `+00:00`, while preserving the existing fallback formats.

No selector logic changed. Token pairs still come only from local `(condition_id, token_id,
outcome_index)` tuples. `resolved_winning_token_id` remains unread by the manifest builder.

---

## 3. Tests added

Added tests in `tests/test_price_source_option_c_c1a_manifest.py`:

1. `parse_ts_utc(datetime(..., tzinfo=timezone.utc))` works.
2. `parse_ts_utc(datetime(...))` treats naive datetime as UTC.
3. `parse_ts_utc(pd.Timestamp(..., tz="UTC"))` works when pandas is available; otherwise the case
   skips cleanly.
4. A low-risk string case confirms fractional ISO/Z support.
5. A loader-level pure test monkeypatches a fake `pm_research.data.store.Store` and proves
   datetime-like `traded_at` rows are included inside the fixed window and then resolve a valid
   side-token pair; an out-of-window row is excluded.

---

## 4. Test result

Sandbox command:

```powershell
python -m pytest tests/test_price_source_option_c_c1a_manifest.py tests/test_price_source_option_c_c1a_canary.py -q
```

Result:

```text
55 passed in 0.34s
```

This preserves the existing 50 tests and adds 5 focused tests for the timestamp/parser regression.

---

## 5. Files patched

- `scripts/price_source_option_c_c1a_manifest.py`
- `tests/test_price_source_option_c_c1a_manifest.py`

No canary implementation change was required.

---

## 6. Guardrails compliance attestation

Research only. No Dune/API/RPC/network call. No real C1A canary run. No candidate-scope change. No
cap change. No C1B/C2/P1/P2/P3/probe behavior. No scoring/backfill/wallet/OrdersMatched/`log_index`/
PnL. No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis. No use of
`resolved_winning_token_id` in manifest selection. No gate change. `named_binary_probe_blocked`
remains untouched.
