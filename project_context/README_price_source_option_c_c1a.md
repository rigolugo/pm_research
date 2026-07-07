# README — Option C, C1A implementation package

Status: **CODE / TEST ONLY. No execution performed by Claude. Patch 1 applied (Orchestrator BLOCK); SQL-shape follow-up applied; tiny test-only patch applied (missing empty-result test restored).**

This package implements the fixed C1A selector-manifest build and bounded canary
reconciliation described in `SPEC_price_source_option_c_onchain_C1R_addendum.md`
(Patch 1, sections 3-9). It does **not** itself run a Dune query, does **not**
call the Polymarket API, and does **not** touch the local `trades` store. Claude
does not execute this path — same discipline as every prior price-source script
in this project (S1, S1-ALT, Option B B0). Real execution is a two-step,
user-run task on the local Windows/Miniconda box, and is **not authorized by
this package** — the Orchestrator's BLOCK said "do not run the real C1A canary
yet," so this revision corrects the implementation only.

## Files

- `scripts/price_source_option_c_c1a_manifest.py` — builds and validates the
  fixed C1A selector manifest from local data only (no network); validates
  `source_table_version` against a strict identifier regex plus a two-table
  allowlist before rendering anything; renders the Dune SQL query TEXT with a
  `per_condition_row_cap + 1` LIMIT (never the exact cap — see "What Patch 1
  fixed" below).
- `scripts/price_source_option_c_c1a_canary.py` — consumes a Dune CSV export
  (fetched manually) plus the manifest, enforces hard caps with fail-fast on a
  true over-fetch signal, treats an empty export as a distinct non-clear
  outcome, reports a non-halt run as `C1_CANARY_EXECUTED_NEEDS_REVIEW` (never
  self-certifies `C1_CANARY_DESIGN_CLEAR`), and writes row-level diagnostic
  artifacts in addition to the per-condition summary.
- `tests/test_price_source_option_c_c1a_manifest.py` — 29 pure-logic tests.
- `tests/test_price_source_option_c_c1a_canary.py` — 21 pure-logic tests.
- All 50 tests pass locally in a bare Python 3 environment (no pandas/Store
  dependency exercised; those paths are lazy-imported and untested here, same
  convention as `StoreLoader` in `scripts/price_source_s1_coverage.py`).

## What Patch 1 fixed (Orchestrator BLOCK, this revision)

1. **Row explosion could be masked by SQL LIMIT.** The Dune query previously
   rendered `limit {per_condition_row_cap}`, so Dune itself would silently
   truncate at the cap — the canary's client-side "exceeded cap" check could
   never fire because the query never returned more rows than the cap in the
   first place. Fixed: the rendered LIMIT is now `per_condition_row_cap + 1`
   (`ManifestRow.dune_query_limit`), so if more rows exist than the true cap,
   the canary actually sees the (cap+1)-th row and can prove the cap was
   exceeded instead of hiding it. The global cap is enforced by a running
   client-side count across all conditions, which already is a genuine count
   mechanism (not a truncating LIMIT), and is unaffected by this fix.
1b. **(Second BLOCK, this revision) The per-condition LIMIT wasn't reliably
   scoped to its own branch.** A bare `limit N` attached directly to a `SELECT`
   immediately before `UNION ALL` is not reliably scoped to that branch alone
   in Trino/Presto (Dune's query engine) — it can bind to the union's overall
   result instead of the individual branch, which would silently defeat the
   per-condition over-fetch bound the whole design depends on. Fixed: each
   condition's block is now wrapped as its own subquery,
   `select * from ( select ... limit N )`, before being combined with
   `UNION ALL`, so the LIMIT unambiguously applies to that condition only.
2. **Empty result no longer clears.** Zero Dune rows now halts with
   `C1_SOURCE_EMPTY` — it can never reach a clean outcome.
3. **Non-halt runs no longer self-certify.** A clean run now reports
   `C1_CANARY_EXECUTED_NEEDS_REVIEW`. `C1_CANARY_DESIGN_CLEAR` is retained only
   as a label the Orchestrator may apply by hand after reviewing the artifacts;
   the code never emits it automatically.
4. **Row-level evidence is now persisted**, bounded to the C1A canary only:
   - `option_c_c1a_raw_rows_sample.csv` — the raw ingested Dune CSV rows.
   - `option_c_c1a_tagged_rows.csv` — one row per Dune-returned event
     (`matched_side`, `tx_hash_relation` = `DUNE_ONLY`/`OVERLAP`), plus a
     synthetic row per `LOCAL_ONLY` tx_hash (present locally, never returned by
     Dune — event fields blank since Dune never returned that row).
   Both are written even on a halt (whatever partial evidence existed at the
   moment of the halt is attached to the `CanaryHalt` exception itself and
   persisted), not only on a clean run.
5. **`source_table_version` is now validated**, not rendered as an arbitrary
   string: a strict lowercase-dotted-identifier regex plus a two-entry
   allowlist (`polymarket_polygon.ctfexchange_evt_orderfilled`,
   `polymarket_polygon.negriskctfexchange_evt_orderfilled` — the two decoded
   OrderFilled tables named in `DUNE_DATA_NOTES.md` section 3). This also
   structurally keeps C1A from ever referencing an OrdersMatched table.

## Scope preserved

- No real Dune/API/RPC call is performed by this package.
- No C1B full sampled coverage. No C2 reusable/production implementation.
- No P1/P2/P3, no probe, no scoring, no wallet work, no OrdersMatched
  expansion, no `log_index`, no PnL.
- No price-series artifact is written; canary output (including the new
  row-level artifacts) is coverage/identity diagnostics only — row counts,
  tx_hash relations, raw asset ids/amounts — never a price.
- No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis
  anywhere. `resolved_winning_token_id` is never read by the manifest builder,
  not even for cross-checking.
- `named_binary_probe_blocked` remains `true`, untouched.

## Local test command only

```powershell
$env:PYTHONPATH="C:\b1\pm_research"
cd C:\b1\pm_research
python -m pytest tests\test_price_source_option_c_c1a_manifest.py tests\test_price_source_option_c_c1a_canary.py -q
```

## Step 1 — build the selector manifest (local only, no network)

Prepare a fixed candidate-condition file (3-5 conditions, chosen in advance —
preferably drawn from the accepted S1/S1-ALT 300-condition sample already on
your machine, e.g. `artifacts/named_binary_probe/price_source_s1/price_source_s1_coverage_by_condition.csv`,
filtered to `BOTH_SIDES`/measured rows in `UP_DOWN`/`OVER_UNDER`/`NAMED_OTHER`):

```json
[
  {
    "condition_id": "0x...64-hex...",
    "window_start_utc": "2025-03-01 00:00:00",
    "window_end_utc": "2025-03-02 00:00:00",
    "per_condition_row_cap": 2000,
    "global_row_cap": 6000,
    "source_table_version": "polymarket_polygon.ctfexchange_evt_orderfilled"
  }
]
```

Then, on the local box:

```powershell
python scripts\price_source_option_c_c1a_manifest.py `
  --root C:\b1\data `
  --artifacts-dir artifacts `
  --candidates artifacts\named_binary_probe\price_source_option_c_c1a\c1a_candidates.json `
  --out-dir artifacts\named_binary_probe\price_source_option_c_c1a
```

This command is shown only to document the future command shape. It is **not
run by Claude**. It reads only local files (`trades`, the named-binary contract
JSON, the resolution-source parquet) and writes:

- `c1a_selector_manifest.json` / `.csv` — the validated manifest (only
  conditions that resolved exactly two stable, string-safe side tokens).
- `c1a_selector_excluded.csv` — excluded candidates with a typed reason.
- `c1a_dune_query.sql` — the fixed, bounded query TEXT to paste into Dune.

## Step 2 — run the query in Dune, fetch the CSV (user-run, per DUNE_DATA_NOTES §7)

```powershell
# 1. Paste c1a_dune_query.sql into the Dune query editor. Run it.
#    Note: the query's LIMIT is per_condition_row_cap + 1 by design (an
#    over-fetch, not the true cap) so row explosion can actually be detected -
#    see "What Patch 1 fixed" above.
# 2. Fetch the latest result via the documented API flow:
curl.exe -H "x-dune-api-key: $env:DUNE_API_KEY" "https://api.dune.com/api/v1/query/<QUERY_ID>/results/csv?limit=6000" -o C:\b1\csv\c1a_dune_export.csv
# 3. Verify no scientific notation appears in the CSV before proceeding.
```

Not run by Claude. Claude has no network path to Dune in this environment.

## Step 3 — run the canary reconciliation (local only, no network)

```powershell
python scripts\price_source_option_c_c1a_canary.py `
  --root C:\b1\data `
  --manifest artifacts\named_binary_probe\price_source_option_c_c1a\c1a_selector_manifest.json `
  --dune-csv C:\b1\csv\c1a_dune_export.csv `
  --out-dir artifacts\named_binary_probe\price_source_option_c_c1a
```

Not run by Claude. Writes:

- `c1a_canary_result.json` / `.md`, `c1a_canary_by_condition.csv` — per-condition
  coverage summary. Outcome will read `C1_CANARY_EXECUTED_NEEDS_REVIEW` on a
  non-halt run (never `C1_CANARY_DESIGN_CLEAR` — the code does not self-certify
  that label) or a specific halt code (`C1_SOURCE_EMPTY`, `C1_ROW_EXPLOSION`,
  etc.) otherwise.
- `option_c_c1a_raw_rows_sample.csv` / `option_c_c1a_tagged_rows.csv` —
  row-level evidence (matched side, `tx_hash_relation` = DUNE_ONLY / OVERLAP /
  LOCAL_ONLY), written even on a halt via the persisted partial evidence.

## Do not run C1A now

Nothing in this package has been executed, and this revision does not change
that: the Orchestrator's BLOCK explicitly said not to run the real canary yet.
The manifest builder needs the local `trades` store and named-binary artifacts
Claude does not have access to in this chat's sandbox; the canary script needs
a real Dune CSV export Claude has no network path to fetch. Both steps remain
user-run, and results (including the row-level artifacts) should be reported
back for Orchestrator review before any C1B/C2 discussion or before the
`C1_CANARY_EXECUTED_NEEDS_REVIEW` output is ever relabeled `C1_CANARY_DESIGN_CLEAR`.
