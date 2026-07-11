# Polymarket Price Canary Actor — Dry-Run by Default, Gated Live-Canary Capability (Review Only, Not Authorized to Run)

**Status:** Dry-run behavior implemented and accepted per earlier Orchestrator authorization (unchanged in this revision — see "What this Actor does" below). Live-canary capability implemented in this revision per `SPEC_apify_live_price_source_canary.md` (accepted, branch `apify-price-canary-dry-run`) under an **"implementation package review only"** authorization: **no Apify run, no build/deploy, no network call, no live dataset** has occurred as part of this delivery. See the self-attestation near the end of this file.

By default (`dry_run` absent or `true`), this build makes **zero network calls**, exactly as before. A gated live-canary mode exists behind three explicit flags (`dry_run=false` + `live_canary_enabled=true` + `acknowledge_not_p1_evidence=true`) — if any is missing, the run hard-stops before any request. See `SPEC_apify_polymarket_price_canary.md` and `SPEC_apify_live_price_source_canary.md` (project_context in `rigolugo/pm_research`) for the full design rationale.

## Correction applied from spec review

The original spec draft mentioned `POST /batch-prices-history` as a possible batch form. **This build does not implement it.** Current Polymarket docs clearly confirm `GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...`; they do not clearly document `/batch-prices-history`. Only the single-market `GET /prices-history` form is planned (`src/validation.py::_prices_history_url`). A test (`test_prices_history_url_uses_single_market_form_only`, and the forbidden-substring check `test_no_forbidden_endpoint_substrings_in_any_planned_url`) asserts the string `batch-prices-history` never appears in any planned URL.

## What this Actor does

For each valid condition in the input manifest, it plans (builds URLs for, never calls):

1. **Gamma metadata** — `GET {gamma_base_url}/{markets|events}?slug=...`, only if `fetch_gamma_metadata=true` and the condition supplies a `slug`.
2. **CLOB price history** — `GET {clob_base_url}/prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...`, once per side token (2 per condition). `startTs`/`endTs` are derived from the externally-supplied `decision_ts` ± `price_history_window_seconds`; the Actor never derives `decision_ts` itself.
3. **CLOB current-shape checks** — `GET {clob_base_url}/{book|price|midpoint|spread}?token_id=...`, once per side token per endpoint (8 per condition), only if `fetch_clob_book_shape=true`. These are schema/shape validation only — never treated as historical or decision-time data.

Each planned request becomes one output dataset row (see schema below). Invalid conditions (missing required field, malformed token id, bad timestamp, bad subclass) do **not** stop the whole run — they produce a `classification: APIFY_INPUT_SCHEMA_INVALID` row and are simply excluded from the plan for that condition. Manifest-level problems (empty/missing `conditions`, more than 5 conditions, or a plan that would exceed `global_request_cap`) **do** halt the whole run before anything is built.

## What this Actor does NOT do (by construction, not just by flag)

- **No HTTP client is imported by the dry-run path, and the live-canary path's only HTTP client (`live_canary.HttpFetcher`) is constructed in exactly one place in the whole codebase** (`live_canary.run_live_canary_from_actor_input`), reached only when `dry_run` is the literal JSON boolean `false` AND both acknowledgement flags are the literal JSON boolean `true`. Setting `dry_run: false` alone (without both acknowledgements) now enters the live-canary code path's gating logic — but that logic hard-stops before `HttpFetcher` is ever constructed. This is a change from the prior revision, where `dry_run: false` only produced a logged warning and had no other effect; see "Live-canary mode" below for the full gating story.
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
│   ├── main.py             # Apify SDK wiring: dispatches dry-run vs. gated live-canary path
│   ├── validation.py       # pure logic: dry-run validation + request-plan builder, NO network, NO apify import
│   └── live_canary.py      # pure logic + HttpFetcher: live-canary gating, plan, parsing, row types (§ below)
├── tests/
│   ├── test_validation.py               # 32 pure-logic tests for the dry-run path, no network, no Apify runtime needed
│   ├── test_live_canary.py              # 52 pure-logic + fake-fetcher tests for the live-canary path, no network
│   └── test_zero_network_integration.py # 3 real end-to-end Actor runs (subprocess + local storage), no network
├── examples/
│   └── input_dry_run_example.json   # 3 placeholder conditions, one per subclass
├── requirements.txt
└── README.md                # this file
```

`src/validation.py` and `src/live_canary.py` both have no dependency on the `apify` package at all (`live_canary.py` does import `.validation`, a sibling pure module — not `apify`), so their logic can be tested (and read/audited) completely independently of any Apify runtime or account.

## Running the tests (no network, no Apify account needed)

```bash
cd apify_actors/polymarket_price_canary
pip install pytest --break-system-packages   # or just `pip install pytest` in a venv
python3 -m pytest tests/ -v
```

**87 tests total, all passing, verified before delivery:**
- `test_validation.py` — 32 pure-logic tests for the dry-run path (unchanged from the prior revision).
- `test_live_canary.py` — 52 pure-logic + fake-fetcher tests for the live-canary path: acknowledgement gating, strict whole-manifest condition validation, request-plan construction (mandatory 6 / optional 9, single-market form only, no batch, no Gamma), request-cap enforcement (including a zero-network proof via a poisoned fetcher), token-identity basis (`REQUEST_URL` default-acceptable / `RESPONSE_BODY` bonus / `UNCONFIRMED` narrow-trigger), response parsing (usable shape, empty history, endpoint error incl. invalid JSON, parse-blocked incl. out-of-range price), nearest-timestamp selection with an explicit tie-break test (and an order-independence test), condition-pair rollup (all three `condition_pair_status` values, including proof that `UNCONFIRMED_TOKEN_ID` never counts toward `BOTH_SIDES_PRESENT`), mandatory disclaimer on every row type, and a forbidden-field sweep across every output row.
- `test_zero_network_integration.py` — 3 real end-to-end Actor runs, each as a subprocess against Apify's file-system local storage (not just unit tests): default input, explicit `dry_run: true`, and `dry_run: false` with a missing acknowledgement. Each asserts the correct output rows appear and that no row carries an `http_status` field (which only a real live-canary fetch attempt would produce) — proof at the full Actor-entry-point level, not only inside isolated functions.

`HttpFetcher` (the only code path in the whole package capable of a real network call) is never instantiated in any test — `test_live_canary.py` uses `FakeFetcher`/`PoisonedFetcher` stand-ins, and `test_zero_network_integration.py` relies on the sandbox's own network egress policy (which does not allow the Polymarket/Gamma/CLOB hosts at all) as a second line of defense on top of the code's own gating.

A request-cap violation is proven to cause zero network calls only at the `test_live_canary.py` level (`test_request_cap_violation_causes_zero_network_calls`), via direct parameter injection of an artificially-lowered cap — this is the only way to exercise that branch at all, since a valid 3-condition manifest always produces 6 or 9 requests, both under the real 12 cap, making a genuine cap violation structurally unreachable through valid Actor input by design.

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

## Dry-run output row schema

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

This is the dry-run path's schema, unchanged from the prior revision. The live-canary path (below) uses a different, three-row-type schema per `SPEC_apify_live_price_source_canary.md`.

---

## Live-canary mode (implemented this revision — NOT executed as part of this delivery)

**This mode has never been run, built, or deployed as part of producing this package.** No network call occurred. See the self-attestation at the end of this section.

### Gating — three explicit flags, checked before anything else

The live-canary code path is only reached when `dry_run` is the **literal JSON boolean `false`**. Once there, `live_canary.check_live_acknowledgements()` runs **first**, before `conditions` is even read from input, before any request plan is built, before `HttpFetcher` is ever constructed:

| Flag | Required value | If missing/false |
|---|---|---|
| `dry_run` | `false` | Takes the unchanged dry-run path instead — not an error, just the default/safe behavior |
| `live_canary_enabled` | `true` | Hard-stop, zero requests |
| `acknowledge_not_p1_evidence` | `true` | Hard-stop, zero requests |

All three must be the literal JSON boolean value — a string `"true"` or the integer `1` does **not** satisfy the gate (tested: `test_acknowledgements_truthy_but_not_literal_true_rejected`).

After the acknowledgement gate passes, the conditions manifest is validated with **zero per-condition tolerance** (unlike the dry-run planner): exactly 3 conditions, exactly one each of `UP_DOWN`/`OVER_UNDER`/`NAMED_OTHER`, all string-safe token ids, no duplicate tokens anywhere in the manifest, no missing fields. **Any** problem hard-stops the **whole** run before any request. Only after that does the request plan get built and cap-checked (`<=12`, hard-stop if exceeded) — and only after *that* does `HttpFetcher` (the sole real-network code path in this package) ever get constructed.

### What gets fetched, if it ever runs

- **Mandatory (6 requests):** `GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...` for each side of each of the 3 conditions. Single-market form only — `/batch-prices-history` is never built.
- **Optional (+3 requests, `live_include_current_endpoint_check: true`):** `GET /book?token_id=...` for `side_0` of each condition, for current-state schema comparison only. Never contributes a `parsed_side_candidate_row`; always classified `APIFY_LIVE_CANARY_CURRENT_ONLY_NOT_HISTORICAL`.
- No Gamma, ever, in this mode.

### Output: three row types (per spec §3)

1. **`raw_request_summary_row`** — one per actual HTTP request, with `request_classification` (`APIFY_LIVE_CANARY_USABLE_SHAPE` / `EMPTY_HISTORY` / `ENDPOINT_ERROR` / `PARSE_BLOCKED` / `CURRENT_ONLY_NOT_HISTORICAL`), token-identity fields (`request_token_id`, `request_url_market_param`, `response_body_token_id` nullable, `token_identity_basis`), and raw audit fields (URL, HTTP status, byte length, bounded excerpt, etc.).
2. **`parsed_side_candidate_row`** — one per side where a candidate point was extracted (including `UNCONFIRMED_TOKEN_ID` cases — recorded and flagged, not silently dropped), with `candidate_price`, `candidate_source_ts`, `signed_gap_seconds`, and `point_selection_method` (always `"nearest_ts_prefer_earlier_on_tie"`).
3. **`condition_pair_summary_row`** — exactly one per condition, the **only** row type with both sides together, with `condition_pair_status` (`BOTH_SIDES_PRESENT` / `ONE_SIDED_ONLY` / `BOTH_SIDES_MISSING_OR_BLOCKED`).

Every row of every type carries `disclaimer_label: "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE"`.

### Token identity — `REQUEST_URL` confirmation is sufficient

Per spec correction: this canary does **not** require the response body to echo the token id. `request_token_id` + `request_url_market_param` (the URL's own `market=` parameter) are sufficient identity confirmation by default (`token_identity_basis: "REQUEST_URL"`). A missing `response_body_token_id` is normal, not an error. `UNCONFIRMED` is reserved for the narrow cases: the URL's `market=` param doesn't match the manifest token, or the response body echoes a **conflicting** token id.

### Point selection — diagnostic only, never a P1 price policy

Among returned points, the one nearest `decision_ts` is selected (`signed_gap_seconds = candidate_source_ts - decision_ts`); exact ties are broken by preferring the **earlier** timestamp, regardless of input order (`test_select_nearest_point_tie_prefers_earlier_regardless_of_input_order`). This exists purely for shape/diagnostic inspection — `candidate_price` cannot be used by P1 or any downstream step without a later, separately accepted price-selection build spec.

### Forbidden, and verified absent from every output row

No `yes_price`, `1 - price`, `1 - yes_price`, side synthesis, or `canonical_side_price` — none of these concepts exist anywhere in `live_canary.py`'s data model (`test_no_forbidden_fields_in_any_output_row` sweeps every row's keys against a forbidden-substring list, and confirms `is_synthesized` is hardcoded `False` wherever present).

### Runbook — review only, not authorized to run

1. Do **not** build or deploy this Actor to Apify as part of this review.
2. Do **not** set `dry_run: false` against a real Apify run under any circumstances until a separate, explicit user authorization for an actual live run is given — Orchestrator review of this code is not that authorization (see `SPEC_apify_live_price_source_canary.md` §10, "Implementation Not Authorized").
3. If/when a live run is separately authorized: populate the Actor input with the accepted real-condition manifest's 3 conditions (from `artifacts/named_binary_probe/apify_price_canary_real_condition_input.json`, never hand-typed), set `dry_run: false`, `live_canary_enabled: true`, `acknowledge_not_p1_evidence: true`, and (optionally) `live_include_current_endpoint_check`. Review the resulting rows per the spec's interpretation rules (§9) before drawing any conclusion — the run's own output never self-labels a coverage or viability verdict.
4. Export and review results with the Orchestrator before any further step. A clean `BOTH_SIDES_PRESENT` result on all 3 conditions still only proves shape/reachability for those 3 conditions at that moment — never coverage, never an S1 reversal, never a P1 unblock.

### Self-attestation (this delivery)

- **No Apify run performed.** No Actor build, no deploy, no Apify Console action of any kind.
- **No network call performed.** `HttpFetcher` (the only real-network code path in the package) was never instantiated against a real host anywhere in this implementation or its verification — all tests use `FakeFetcher`/`PoisonedFetcher` stand-ins, and the end-to-end tests that do run the real Actor entry point only exercise scenarios (default input, explicit `dry_run: true`, missing acknowledgement) that structurally never reach `HttpFetcher` at all.
- **No live dataset produced.** No file under `artifacts/named_binary_probe/apify_live_canary/` (the spec's designated live-canary output path) was created; that path doesn't exist anywhere in this delivery.
- **P1 remains blocked.** `named_binary_probe_blocked` stays `true`; this codebase does not reference it as operational state anywhere, only in disclaimer/log strings.
- **`S1_SOURCE_NOT_VIABLE` unchanged.** Nothing in this delivery touches, re-derives, or claims to affect that accepted finding.

---

1. In the Apify Console, create a new Actor and choose **"Link Git Repository"** as the source type.
2. Point it at `rigolugo/pm_research`, a **dedicated review branch** (not `main`), subdirectory `apify_actors/polymarket_price_canary`.
3. Since `rigolugo/pm_research` is private, attach a deploy key or install Apify's GitHub App per Apify's private-repo instructions; store the credential only in Apify's secret store, never in the repo.
4. Confirm the build detects the Python Actor template (`.actor/Dockerfile`, `requirements.txt`, `src/main.py`, `src/__main__.py`).
5. In the Actor's Input UI (auto-generated from `.actor/input_schema.json`), paste the contents of `examples/input_dry_run_example.json`, or your own 3–5 condition manifest. **Leave `dry_run: true`** — this is now important, not merely cosmetic: setting it to `false` (even accidentally) enters the live-canary gating path, which is safe (it hard-stops without both acknowledgement flags) but is no longer a no-op the way it was in the prior revision.
6. Set Actor build settings: minimal memory (256–512MB), timeout ~120s. **No scheduler, no webhooks, no auto-run-on-push.**
7. Build the Actor. This only compiles/deploys the container image — it executes nothing.
8. Run it with `dry_run: true` (the default). This build's dry-run path still has no network-call code path at all — running it on Apify is equivalent to the local run above: it will validate input and emit planned-request dataset rows only. **Do not** set `dry_run: false` on a real Apify run as part of this review — see the live-canary Runbook above; that requires a separate, explicit user authorization not granted by this delivery.
9. This package **does** now contain live-fetch code (`live_canary.HttpFetcher`), unlike the prior dry-run-only revision — but it is reachable only via the explicit three-flag gate described above, and no run against real Apify infrastructure has occurred or is authorized as part of this delivery.

## Guardrail-to-code mapping (for reviewer convenience)

### Dry-run path (unchanged from prior revision)

| Guardrail | Enforced in | Test(s) |
|---|---|---|
| Hard condition cap ≤ 5 | `validation.build_request_plan` (`effective_cap = min(max_conditions, HARD_MAX_CONDITIONS)`) | `test_condition_cap_exceeded_raises`, `test_max_conditions_cannot_exceed_hard_cap`, `test_at_cap_five_conditions_does_not_raise_cap_error` |
| Required fields present | `validation.validate_condition` | `test_missing_condition_id`, `test_bad_nb_subclass`, `test_bad_decision_ts` |
| String-safe decimal token ids, no scientific notation | `validation.is_string_safe_decimal` | `test_rejects_scientific_notation`, `test_rejects_decimal_point_and_signs`, `test_accepts_typical_78_digit_token_id` |
| Only 3 known-safe endpoint families, no forbidden endpoints | `validation._prices_history_url` / `_gamma_url` / `_book_shape_url` (fixed paths only) | `test_no_forbidden_endpoint_substrings_in_any_planned_url` |
| No `/batch-prices-history` | `validation._prices_history_url` (single-market form only) | `test_prices_history_url_uses_single_market_form_only` |
| Zero network calls | No HTTP client import anywhere in `validation.py`/dry-run `main.py` path | manual grep; end-to-end local run produced output with no network access |
| No price computation / no price fields | `RequestPlanRow` dataclass has no price-shaped field | `test_no_price_fields_anywhere_on_row` |
| Every row disclaims coverage-evidence status | `main._row_to_dict` / `validation.DISCLAIMER` | `test_all_rows_carry_dry_run_true_and_disclaimer` |
| Global request cap | `validation.build_request_plan` (`global_request_cap`) | `test_global_request_cap_exceeded_raises` |

### Live-canary path (this revision)

| Guardrail | Enforced in | Test(s) |
|---|---|---|
| Zero network calls by default | `main.py` only enters the live path when `dry_run` is the literal `False`; `HttpFetcher` constructed in exactly one place | `test_default_input_e2e_zero_network_calls`, `test_dry_run_true_explicit_e2e_zero_network_calls` |
| Both acknowledgements required, checked first | `live_canary.check_live_acknowledgements` | `test_acknowledgements_missing_live_canary_enabled`, `test_acknowledgements_missing_acknowledge_not_p1_evidence`, `test_acknowledgements_truthy_but_not_literal_true_rejected`, `test_missing_acknowledgements_cause_zero_network_calls`, `test_missing_acknowledgements_e2e_zero_network_calls` |
| Exactly 3 conditions, one per subclass, whole-manifest hard-stop | `live_canary.validate_live_canary_conditions` | `test_validate_conditions_wrong_count`, `test_validate_conditions_missing_subclass` |
| String-safe tokens, no duplicates, no malformed pairs | `live_canary.validate_live_canary_conditions` | `test_validate_conditions_non_string_safe_token_id`, `test_validate_conditions_duplicate_side_tokens_within_condition`, `test_validate_conditions_duplicate_token_across_conditions` |
| Single-market `/prices-history` only, no batch, no Gamma | `live_canary.build_live_request_plan` | `test_plan_urls_are_single_market_form_only`, `test_plan_no_gamma_ever` |
| Hard request cap ≤ 12, zero network on violation | `live_canary.check_request_cap` | `test_request_cap_violation_raises`, `test_request_cap_violation_causes_zero_network_calls` |
| Token identity: `REQUEST_URL` acceptable, missing echo not a hard-stop | `live_canary.classify_and_parse_prices_history` | `test_token_identity_defaults_to_request_url`, `test_token_identity_response_body_conflict_is_unconfirmed`, `test_token_identity_url_param_mismatch_is_unconfirmed` |
| Nearest-timestamp selection, earlier-wins tie-break | `live_canary.select_nearest_point` | `test_select_nearest_point_tie_prefers_earlier`, `test_select_nearest_point_tie_prefers_earlier_regardless_of_input_order` |
| `UNCONFIRMED_TOKEN_ID` never counts as a usable pair | `live_canary._condition_pair_summary_rows` | `test_condition_pair_unconfirmed_token_id_never_counts_as_present` |
| No forbidden fields, `is_synthesized` always `False` | `live_canary` row builders | `test_no_forbidden_fields_in_any_output_row` |
| Mandatory disclaimer on every row type | `live_canary.DISCLAIMER_LABEL` | `test_disclaimer_on_every_row_type` |
