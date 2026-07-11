# FINDING — Apify Price Canary Dry-Run

**Decision:** ACCEPT FINDING — `APIFY_REAL_CONDITION_DRY_RUN_ACCEPTED`  
**Status:** Documentation-only finding  
**Scope:** Infrastructure/plumbing evidence only  
**Date recorded:** 2026-07-11

---

## 1. Scope

This finding records the completed Apify price-canary dry-run sequence.

This document is documentation only.

It authorizes no code changes, no Actor changes, no Apify run, no network call, no price artifact, no P1/P2/P3/probe continuation, no scoring, no wallet work, no gate change, and no change to the standing P1 blocker.

---

## 2. Placeholder dry-run result

The placeholder Apify dry-run succeeded.

Observed result:

- `33` planned rows
- `gamma_metadata` included
- `dry_run = true`
- `disclaimer = APIFY_CANARY_NOT_COVERAGE_EVIDENCE`
- planned URLs only
- no fetched response body
- no HTTP status
- no bid/ask/book data
- no price values
- no historical price points

Expected row reconciliation:

```text
3 gamma metadata rows
6 clob_prices_history rows
24 current-shape rows:
  clob_book, clob_price, clob_midpoint, clob_spread
  × 2 sides
  × 3 conditions
= 33 rows
```

Interpretation:

The placeholder run validated that the GitHub-backed Apify Actor could execute in dry-run mode and emit planned request rows. It did not validate Polymarket/Gamma/CLOB endpoint availability, response schema, price coverage, or price usability.

---

## 3. Real-condition manifest generation result

The real-condition Apify dry-run manifest was generated locally.

Observed result:

- one accepted P0 condition selected per named-binary subclass:
  - `UP_DOWN`
  - `OVER_UNDER`
  - `NAMED_OTHER`
- real `side_0_token_id` and `side_1_token_id` included for each selected condition
- `fetch_gamma_metadata = false`
- `fetch_clob_book_shape = true`
- `dry_run = true`
- `global_request_cap = 50`
- no slug fields
- no price fields
- no wallet fields
- no PnL fields
- no `log_index`
- no scoring fields

Selected real P0 conditions:

```text
UP_DOWN
condition_id = 0x00001032adc2a18f836a38d7da2ffc1d81cbcf44f9a8b33c9c941fd0a07e2914
decision_ts  = 2026-05-08T05:27:06Z

OVER_UNDER
condition_id = 0x0087652a603d3384be139ddd86863ec929444c228b5b4d60f65975e521f63928
decision_ts  = 2025-10-31T08:00:16Z

NAMED_OTHER
condition_id = 0x00037e466770d6f50dea9c86bd61bf51b6e8f1691f01f31c79c5d68478a749b7
decision_ts  = 2025-10-26T04:13:19Z
```

Interpretation:

The manifest generator successfully carried real accepted P0 identifiers into the existing Apify Actor input format. This validates manifest plumbing only. It does not validate endpoint availability or price coverage.

---

## 4. Real-condition Apify dry-run result

The real-condition Apify dry-run succeeded.

Observed result:

- `30` planned rows
- `dry_run = true` on every row
- `disclaimer = APIFY_CANARY_NOT_COVERAGE_EVIDENCE` on every row
- `errors = null` on every row
- `classification = null` on every row
- no `gamma_metadata` rows, as expected because `fetch_gamma_metadata = false`

Source count reconciliation:

```text
clob_prices_history = 6
clob_book           = 6
clob_price          = 6
clob_midpoint       = 6
clob_spread         = 6
total               = 30
```

Expected row reconciliation:

```text
3 conditions
× 2 sides
× 1 clob_prices_history endpoint
= 6 historical planned rows

3 conditions
× 2 sides
× 4 current-shape endpoints
= 24 current-shape planned rows

6 + 24 = 30 rows
```

The planned endpoint families were:

- `clob_prices_history`
- `clob_book`
- `clob_price`
- `clob_midpoint`
- `clob_spread`

The output contained planned URLs only. It did not contain fetched response bodies, HTTP status codes, bid/ask book data, midpoint values, spread values, price values, wallet fields, PnL fields, `log_index`, scoring fields, or gate fields.

---

## 5. Accepted interpretation

Decision:

```text
APIFY_REAL_CONDITION_DRY_RUN_ACCEPTED
```

Accepted meaning:

- validates the GitHub-backed Apify Actor build/run path
- validates Apify dry-run execution
- validates real-condition manifest plumbing
- validates planned URL construction for real P0 condition/token identifiers

Explicit non-meanings:

- does not validate live endpoint availability
- does not validate `/prices-history` response shape
- does not validate historical price coverage
- does not produce a price artifact
- does not create `side_0_price` / `side_1_price`
- does not compute canonical-side price
- does not overturn `S1_SOURCE_NOT_VIABLE`
- does not unblock P1
- does not authorize P2/P3/probe/scoring
- does not change any gate state

---

## 6. Standing guardrails

The following remain in force:

- `dry_run = false` remains unauthorized.
- Live Polymarket/Gamma/CLOB fetch remains unauthorized.
- Full P0 price-source build remains unauthorized.
- P1 continuation remains unauthorized.
- P2/P3/probe execution remains unauthorized.
- Scoring remains unauthorized.
- Wallet discovery / wallet-copying remains unauthorized.
- `OrdersMatched`, `log_index`, and PnL analysis remain unauthorized.
- No project gate changes are implied.

---

## 7. Standing blocker

P1 remains blocked on missing per-side/token-identity decision-time price input.

The accepted price-input blocker remains:

```text
OrientationContract.canonical_side_price(side_0_price, side_1_price)
requires two per-side prices in outcome_index order.

Local Store.load_prices() exposes only:
[condition_id, ts, yes_price]

yes_price is YES/NO-only and unsafe for:
UP_DOWN
OVER_UNDER
NAMED_OTHER
```

Therefore, the Apify dry-run finding does not make P1 runnable. A valid P1-unblocking source would still need an audited artifact containing both per-side/token-identity prices at or near the decision timestamp.

---

## 8. Recommended next step

If continuing in the Apify direction, the next disciplined task is a specification-only live canary plan:

```text
SPEC_apify_live_price_source_canary.md
```

That future spec, if authorized separately, should define a tightly bounded live Apify canary for exactly the three real P0 conditions already selected. It must not claim coverage, must not create a P1 artifact, and must not run without separate review and authorization.

---

## 9. File placement

Recommended project path:

```text
artifacts/named_binary_probe/FINDING_apify_price_canary_dry_run.md
```
