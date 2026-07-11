# Polymarket Price Canary Actor — DRY-RUN ONLY

**Status:** Implemented per Orchestrator authorization (SPEC ACCEPTED, dry-run implementation only). This build makes **zero network calls** to Polymarket, Gamma, or any other external host. It validates a small, fixed condition manifest and emits the *planned* request URLs a future, separately authorized live-run mode could call — it never calls them.

See `SPEC_apify_polymarket_price_canary.md` (project_context in `rigolugo/pm_research`) for the full design rationale, and the Orchestrator's acceptance message for the correction applied below.

## Correction applied from spec review

The original spec draft mentioned `POST /batch-prices-history` as a possible batch form. **This build does not implement it.** Current Polymarket docs clearly confirm `GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...`; they do not clearly document `/batch-prices-history`. Only the single-market `GET /prices-history` form is planned (`src/validation.py::_prices_history_url`). A test (`test_prices_history_url_uses_single_market_form_only`, and the forbidden-substring check `test_no_forbidden_endpoint_substrings_in_any_planned_url`) asserts the string `batch-prices-history` never appears in any planned URL.

## What this Actor does

For each valid condition in the input manifest, it plans (builds URLs for, never calls):

1. **Gamma metadata** — `GET {gamma_base_url}/{markets|events}?slug=...`, only if `fetch_gamma_metadata=true` and the condition supplies a `slug`.
2. **CLOB price history** — `GET {clob_base_url}/prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...`, once per side token (2 per condition). `startTs`/`endTs` are derived from the externally-supplied `decision_ts` ± `price_history_window_seconds`; the Actor never derives `decision_ts` itself.
3. **CLOB current-shape checks** — `GET {clob_base_url}/{book|price|midpoint|spread}?token_id=...`, once per side token per endpoint (8 per condition), only if `fetch_clob_book_shape=true`. These are schema/shape validation only — never treated as historical or decision-time data.

Each planned request becomes one output dataset row (see schema below). Invalid conditions (missing required field, malformed token id, bad timestamp, bad subclass) do **not** stop the whole run — they produce a `classification: APIFY_INPUT_SCHEMA_INVALID` row and are simply excluded from the plan for that condition. Manifest-level problems (empty/missing `conditions`, more than 5 conditions, or a plan that would exceed `global_request_cap`) **do** halt the whole run before anything is built.

## What this Actor does NOT do (by construction, not just by flag)

- **No HTTP client is imported anywhere in `src/`.** Not `requests`, not `httpx`, not `aiohttp`, not `urllib.request`. There is no code path capable of making an external network call in this build — this isn't just a `dry_run` flag being respected, it's structural. Setting `dry_run: false` in the input only produces a logged warning; it does not enable anything.
- No wallet/profile/leaderboard/comments/positions/activity endpoint is ever addressed — only three fixed, known-safe endpoint families exist in the code (`_prices_history_url`, `_gamma_url`, `_book_shape_url`), and no user-supplied path/endpoint string is ever used verbatim.
- No `yes_price`, `1 - price`, `1 - yes_price`, or side synthesis. No price is ever computed. No `canonical_side_price`. No scoring (Brier/log-loss/calibration/reliability/splits/EV).
- These terms appear only in guardrail/disclaimer language and are never read, modified, computed, or used as operational state: P1/P2/P3, the probe, `named_binary_probe_blocked`, and gate state. This Actor cannot flip or read that flag; the only place these words appear in the codebase is inside disclaimer/log strings (e.g. `"does not by itself authorize S2/P1/probe/any gate change"` in `src/main.py`).
- No claim that `S1_SOURCE_NOT_VIABLE` (the accepted S1 Pass-1 result) has changed. Every output row carries `disclaimer: "APIFY_CANARY_NOT_COVERAGE_EVIDENCE"`.

## Folder layout

```
apify_actors/polymarket_price_canary/
├── .actor/
│   ├── actor.json          # Apify actor metadata
│   ├── input_schema.json   # Actor input UI schema (see below)
│   └── Dockerfile
├── src/
│   ├── __init__.py
│   ├── __main__.py         # `python3 -m src` entry point
│   ├── main.py             # Apify SDK wiring: Actor.get_input / push_data / log / fail
│   └── validation.py       # pure logic: validation + request-plan builder, NO network, NO apify import
├── tests/
│   └── test_validation.py  # 32 pure-logic tests, no network, no Apify runtime needed
├── examples/
│   └── input_dry_run_example.json   # 3 placeholder conditions, one per subclass
├── requirements.txt
└── README.md                # this file
```

`src/validation.py` has no dependency on the `apify` package at all, so its logic can be tested (and read/audited) completely independently of any Apify runtime or account.

## Running the tests (no network, no Apify account needed)

```bash
cd apify_actors/polymarket_price_canary
pip install pytest --break-system-packages   # or just `pip install pytest` in a venv
python3 -m pytest tests/test_validation.py -v
```

All 32 tests are pure-logic (token-id/timestamp validation, condition-cap enforcement, global-request-cap enforcement, per-condition error isolation, and structural guardrail assertions like "no forbidden URL substring ever appears" and "no price field exists on the row model at all"). This was run and verified passing (32/32) before delivery.

## Running the dry-run locally (no Apify account needed)

The Apify Python SDK supports a local file-system storage mode, so the whole Actor can be exercised end-to-end on a laptop with zero account/credentials and zero network access to Polymarket:

```bash
cd apify_actors/polymarket_price_canary
pip install -r requirements.txt --break-system-packages

export APIFY_LOCAL_STORAGE_DIR=/tmp/apify_storage
mkdir -p "$APIFY_LOCAL_STORAGE_DIR/key_value_stores/default"
cp examples/input_dry_run_example.json "$APIFY_LOCAL_STORAGE_DIR/key_value_stores/default/INPUT.json"

python3 -m src
```

This was run during implementation with the exact example input in `examples/input_dry_run_example.json` (3 conditions, one per subclass, both `fetch_gamma_metadata` and `fetch_clob_book_shape` true) and produced **32 planned request rows, 0 validation errors, exit code 0, zero network calls** — output dataset rows land under `$APIFY_LOCAL_STORAGE_DIR/datasets/default/*.json`.

## Output row schema

```json
{
  "schema_version": "apify-canary-plan-1.0",
  "run_id": "uuid4 string, one per run",
  "condition_id": "string | null",
  "nb_subclass": "UP_DOWN | OVER_UNDER | NAMED_OTHER | null",
  "side": "0 | 1 | null",
  "token_id": "string | null",
  "source": "gamma_metadata | clob_prices_history | clob_book | clob_price | clob_midpoint | clob_spread | validation | manifest_validation",
  "planned_url": "string | null (null for validation-error rows)",
  "dry_run": true,
  "disclaimer": "APIFY_CANARY_NOT_COVERAGE_EVIDENCE",
  "classification": "APIFY_INPUT_SCHEMA_INVALID | APIFY_GUARDRAIL_CONDITION_CAP_EXCEEDED | APIFY_GLOBAL_REQUEST_CAP_EXCEEDED | null",
  "errors": "array of strings | null",
  "generated_at": "ISO8601 UTC"
}
```

This build never emits the six live-run classification labels from the accepted spec (`APIFY_CLOB_PRICE_HISTORY_BOTH_SIDES_PRESENT`, etc.) — those require an actual response to classify, and this build makes no requests. They remain reserved for a future, separately authorized live-run implementation.

## Apify Git source setup steps (manual, for reviewer/operator use — does not itself authorize a run)

1. In the Apify Console, create a new Actor and choose **"Link Git Repository"** as the source type.
2. Point it at `rigolugo/pm_research`, a **dedicated review branch** (not `main`), subdirectory `apify_actors/polymarket_price_canary`.
3. Since `rigolugo/pm_research` is private, attach a deploy key or install Apify's GitHub App per Apify's private-repo instructions; store the credential only in Apify's secret store, never in the repo.
4. Confirm the build detects the Python Actor template (`.actor/Dockerfile`, `requirements.txt`, `src/main.py`, `src/__main__.py`).
5. In the Actor's Input UI (auto-generated from `.actor/input_schema.json`), paste the contents of `examples/input_dry_run_example.json`, or your own 3–5 condition manifest. Leave `dry_run: true` (it has no live-call effect either way in this build).
6. Set Actor build settings: minimal memory (256–512MB), timeout ~120s. **No scheduler, no webhooks, no auto-run-on-push.**
7. Build the Actor. This only compiles/deploys the container image — it executes nothing.
8. Run it. Because this build has no network-call code path at all, running it on Apify is equivalent to the local run above: it will validate input and emit planned-request dataset rows only. No Polymarket/Gamma/CLOB traffic will occur regardless of how many times or how it is run.
9. A **separate, explicitly authorized implementation** is required before any live-run mode (one that actually issues the planned HTTP requests) is added to this Actor. This README and this codebase do not authorize that step.

## Guardrail-to-code mapping (for reviewer convenience)

| Guardrail | Enforced in | Test(s) |
|---|---|---|
| Hard condition cap ≤ 5 | `validation.build_request_plan` (`effective_cap = min(max_conditions, HARD_MAX_CONDITIONS)`) | `test_condition_cap_exceeded_raises`, `test_max_conditions_cannot_exceed_hard_cap`, `test_at_cap_five_conditions_does_not_raise_cap_error` |
| Required fields present | `validation.validate_condition` | `test_missing_condition_id`, `test_bad_nb_subclass`, `test_bad_decision_ts` |
| String-safe decimal token ids, no scientific notation | `validation.is_string_safe_decimal` | `test_rejects_scientific_notation`, `test_rejects_decimal_point_and_signs`, `test_accepts_typical_78_digit_token_id` |
| Only 3 known-safe endpoint families, no forbidden endpoints | `validation._prices_history_url` / `_gamma_url` / `_book_shape_url` (fixed paths only) | `test_no_forbidden_endpoint_substrings_in_any_planned_url` |
| No `/batch-prices-history` | `validation._prices_history_url` (single-market form only) | `test_prices_history_url_uses_single_market_form_only` |
| Zero network calls | No HTTP client import anywhere in `src/` | manual grep (documented above); end-to-end local run produced output with no network access |
| No price computation / no price fields | `RequestPlanRow` dataclass has no price-shaped field | `test_no_price_fields_anywhere_on_row` |
| Every row disclaims coverage-evidence status | `main._row_to_dict` / `validation.DISCLAIMER` | `test_all_rows_carry_dry_run_true_and_disclaimer` |
| Global request cap | `validation.build_request_plan` (`global_request_cap`) | `test_global_request_cap_exceeded_raises` |
