# SPEC — Option D Temporal In-Range Precheck — SPEC ONLY

**Proposed filename:** `SPEC_price_source_option_d_temporal_inrange_precheck.md`

**Decision posture:** APPROVE — SPEC ONLY.

**Status:** ACCEPTED / SPEC ONLY. Not implemented. Not run. This document authorizes no work beyond review of this text.

**Authorization basis:** the user authorized **SPEC ONLY design** for the Option D local-only temporal in-range precheck. This authorization does **not** authorize implementation, tests, local data reads, a precheck run, artifact generation, vendor/network fetch, PMXT raw archive download, Telonex fetch, account/API key/paid action, Pass 1, Pass 2, price artifact, canonical-side price computation, P1/P2/P3/probe, scoring, wallet/OrdersMatched/`log_index`/PnL, or gate change.

**Scope:** Define, on paper only, a local-only/read-only precheck that estimates whether Option D's two L2 archive windows are even temporally relevant to the accepted P0 named-binary universe before any vendor fetch, account action, or price-source build is considered.

**Consumes, does not redefine:** accepted named-binary classification contract (`nb-contract-2026-06-28.1`), accepted P0 eligible universe (`final_p0_eligible = 39,693`), accepted resolution-source parquet, pinned `warmup_seconds = 3600` decision-timestamp policy, and accepted Option D vendor-scope dates and inclusive in-range test.

**Canonical-doc workflow constraint:** This document is canonical-ready accepted SPEC ONLY text. Claude must not update canonical project-context files. ChatGPT prepares complete replacement/new files for user manual upload under `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`.

**Hard boundary — this document does not:** implement code; write or modify tests; read any local data file; run the precheck; generate project artifacts; fetch data from any vendor archive/API; download any PMXT raw archive file; fetch from Telonex; create or use a vendor account/API key; take paid action; run Pass 1; run Pass 2; build any price artifact; compute any price, bid, ask, mid, spread, depth, or canonical-side price; continue P1/P2/P3; execute the named-binary probe; compute any score; touch wallets, OrdersMatched, `log_index`, or PnL; change any gate; flip `named_binary_probe_blocked`; use `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or synthesize a missing side price by any other means.

---

## 0. Standing project state preserved

This draft changes nothing about accepted project state.

- **P0 remains accepted:** `P0_CLEAR`.
- Accepted P0 figures remain:
  - `contract_eligible = 39,957`
  - `source_rows = 39,946`
  - `resolved_single_winner = 39,693`
  - `ambiguous_multiple_winners = 253`
  - `missing_source_rows = 11`
  - `final_p0_eligible = 39,693`
- Accepted P0 subclass denominator expected for this precheck:
  - `UP_DOWN = 22,012`
  - `OVER_UNDER = 1,003`
  - `NAMED_OTHER = 16,678`
- **P1 remains BLOCKED** on the absence of accepted per-side/token-identity decision-time price input.
- `Store.load_prices()` exposes only `[condition_id, ts, yes_price]`.
- `yes_price` is YES/NO-only and unsafe for `UP_DOWN`, `OVER_UNDER`, and `NAMED_OTHER`.
- **S1 remains accepted negative:** `S1_SOURCE_NOT_VIABLE`.
- **S1-ALT remains accepted negative:** `S1ALT_SOURCE_NOT_VIABLE`.
- **Option B corrected B0 remains accepted negative:** `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.
- **Option C remains not viable / not design-clear.**
- **Option D remains `ACCEPTED / SPEC ONLY`** as L2 order-book vendor archive coverage feasibility.
- No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or other side synthesis is allowed.
- `named_binary_probe_blocked` remains `true`.

---

## 1. Objective

Define a future local-only/read-only precheck that answers exactly two temporal feasibility questions over the verified P0 named-binary universe:

1. **PMXT v2 temporal in-range fraction.** What fraction of P0-eligible conditions have both:
   - `decision_ts = first_trade_ts + 3600s`
   - `resolved_at`

   at or after `2026-04-13T19:00:00Z`?

2. **Telonex L2 temporal in-range fraction.** What fraction of P0-eligible conditions have both:
   - `decision_ts = first_trade_ts + 3600s`
   - `resolved_at`

   at or after `2025-10-11T00:00:00Z`?

This precheck measures only a date-range ceiling. It does not inspect whether either vendor has rows, token coverage, both-side book state, usable bid/ask depth, quote quality, mechanical trust, price semantics, or P1 viability.

---

## 2. Non-goals

The temporal precheck is not a vendor test and not a price-source build.

It must not:

- fetch, query, browse, or contact PMXT or Telonex in any way;
- download any PMXT raw archive file;
- create or use vendor accounts/API keys;
- inspect L2 rows;
- compute, parse, request, or persist price values;
- compute bid, ask, mid, spread, depth, or book quality;
- compute `canonical_side_price`;
- use token-side price acceptance criteria;
- enumerate token pairs, sides, or `outcome_index` values;
- use `yes_price`, `1 - price`, `1 - yes_price`, or any side synthesis;
- use wallet identifiers;
- use OrdersMatched;
- use `log_index`;
- compute PnL;
- score Brier/log-loss/calibration/reliability/splits;
- run P1/P2/P3/probe;
- change gates or `named_binary_probe_blocked`;
- decide, accept, or recommend a final vendor, price basis, or accepted price source.

---

## 3. Vendor temporal constants

The future precheck must use fixed, UTC, inclusive lower-bound constants from the accepted Option D spec:

| Vendor scope | Constant | Meaning |
|---|---:|---|
| PMXT v2 L2 archive | `2026-04-13T19:00:00Z` | PMXT v2 L2 book archive start. PMXT v1 is out of scope unless separately reviewed. |
| Telonex L2 order-book/quote archive | `2025-10-11T00:00:00Z` | Telonex L2 order-book/quote operative start. Telonex on-chain fills from inception are not L2 book coverage. |

A condition is temporally in range for a vendor only if both `decision_ts` and `resolved_at` are greater than or equal to the vendor's fixed UTC start.

The lower bound is inclusive. There is no vendor-history upper-bound test in this precheck.

---

## 4. Required preliminary schema-discovery phase

Any future implementation must begin with schema discovery and universe verification. It must fail loud before computing fractions if any required source, method, field, or timestamp rule is unavailable or ambiguous.

Nothing below should be treated as guaranteed implementation shape. Every path/field is a design expectation from canonical documentation. The future implementation must re-verify all fields against the live local repo/box before computing anything.

### 4.1 P0-eligible universe source and verification

No known ready-made condition-level `P0-eligible` list is established by this spec.

`artifacts/named_binary_probe/p0_preflight.json` is used to confirm P0 state and counts only. It must not be assumed to contain a per-condition `condition_id` list unless a future read-only inspection proves such a field has been added.

Expected reconstruction path:

1. Load `artifacts/named_binary/named_binary_classification_contract.json`.
2. Keep records where `nb_eligible` is true and `nb_subclass ∈ {UP_DOWN, OVER_UNDER, NAMED_OTHER}`.
3. Load `artifacts/named_binary/named_binary_resolution_source_rows.parquet`.
4. Keep rows where `status == "RESOLVED_SINGLE_WINNER"`.
5. Inner join on `condition_id`.
6. Cross-check `nb_subclass` from the contract equals `subclass` from the resolution-source row for every joined condition.
7. Confirm `nb_contract_version == "nb-contract-2026-06-28.1"` on the contract and resolution source where available. If a version is present but does not match, halt with `STOP_STALE_CONTRACT`.
8. Confirm `p0_preflight.json` is present and `p0_state == "P0_CLEAR"`.

Mandatory reconciliation gate before computing anything:

- pooled `final_p0_eligible = 39,693`
- `UP_DOWN = 22,012`
- `OVER_UNDER = 1,003`
- `NAMED_OTHER = 16,678`

Any deviation halts with `STOP_P0_UNIVERSE_NOT_VERIFIED`.

### 4.2 First trade timestamp source

The future implementation must compute:

`first_trade_ts = min(traded_at)` per `condition_id`

Expected source:

- `Store(root).load_trades()`
- group by `condition_id`
- use `traded_at`

Important constraints:

- `Store(root).load_trades()` is a method on `Store`, not a module-level function.
- `token_id`, `outcome_index`, side labels, and price fields are not needed for this precheck.
- If the trades source, `condition_id`, or `traded_at` field is unavailable at source/schema level, halt with `STOP_FIRST_TRADE_TS_UNAVAILABLE`.
- If individual conditions have no local trade anchor after the universe is verified, do not silently drop them. Keep the full P0 denominator, mark those conditions as `NO_FIRST_TRADE_TS`, and count them separately. If the count is large enough to suggest a broken source/universe rather than ordinary missing anchors, halt with `STOP_MISSING_TRADE_ANCHOR_SYSTEMIC` rather than emit a clean finding.

### 4.3 Resolution timestamp source

The future implementation must use `resolved_at` from `named_binary_resolution_source_rows.parquet`.

Expected field:

- `resolved_at`

Rules:

- Parse `resolved_at` explicitly as UTC.
- Do not assume it is already datetime-typed.
- Use `resolved_at` only for this temporal range classification.
- Do not use `resolved_at` in feature construction, price construction, scoring, or selection.
- Do not default, interpolate, or infer missing `resolved_at`.

If `resolved_at` is unavailable, duplicated ambiguously, or unparseable for the verified universe, halt with `STOP_RESOLVED_AT_UNAVAILABLE`.

### 4.4 Timestamp timezone handling

Before comparison, the future implementation must normalize all timestamps to timezone-aware UTC or an equivalent unambiguous epoch representation:

- `traded_at`
- `first_trade_ts`
- `decision_ts`
- `resolved_at`
- PMXT v2 start constant
- Telonex L2 start constant

A future implementation must re-locate and re-verify the accepted timestamp parser/helper behavior before parsing. It must not silently coerce naive timestamps to UTC.

If timestamp handling is ambiguous, halt with `STOP_TIMESTAMP_TIMEZONE_AMBIGUOUS`.

### 4.5 Stop on nonlocal or vendor requirements

If a future implementation discovers that computing either required fraction needs any nonlocal input, external service, vendor archive, API call, account, paid action, or old-chat/uploaded duplicate, it must halt rather than broaden scope.

Relevant halt labels:

- `STOP_NONLOCAL_INPUT_REQUIRED`
- `STOP_VENDOR_DATA_REQUIRED`
- `STOP_SCOPE_CREEP`

---

## 5. Computation design

### 5.1 First trade timestamp

For each condition in the verified P0 universe:

1. Select local trade rows with the same `condition_id`.
2. Compute `first_trade_ts = min(traded_at)` after timestamp normalization.
3. Do not inspect or aggregate price fields.
4. Do not inspect token-side fields.

If a condition has no trade anchor, record `NO_FIRST_TRADE_TS`; it remains in the denominator and is not counted as temporally in range for either vendor.

### 5.2 Decision timestamp

For each condition with a valid `first_trade_ts`:

```text
decision_ts = first_trade_ts + 3600 seconds
```

This reuses the accepted `warmup_seconds = 3600` policy. It does not redefine decision timing.

### 5.3 Resolution timestamp

For each condition:

1. Parse `resolved_at` from the verified resolution-source row.
2. Normalize to UTC.
3. Use only as a date boundary for this precheck.

### 5.4 Vendor in-range classification

For each condition with valid `decision_ts` and `resolved_at`:

```text
pmxt_v2_temporally_in_range =
    decision_ts >= 2026-04-13T19:00:00Z
    and resolved_at >= 2026-04-13T19:00:00Z
```

```text
telonex_l2_temporally_in_range =
    decision_ts >= 2025-10-11T00:00:00Z
    and resolved_at >= 2025-10-11T00:00:00Z
```

For a condition without a valid `first_trade_ts`, both vendor flags must be false or null with an explicit `NO_FIRST_TRADE_TS` reason, depending on the chosen output schema. The denominator still remains the full verified P0 universe.

### 5.5 Denominators and fractions

Primary denominator:

- full verified P0-eligible universe
- expected pooled denominator: `39,693`
- expected subclass denominators: `UP_DOWN = 22,012`, `OVER_UNDER = 1,003`, `NAMED_OTHER = 16,678`

Primary numerator for each vendor:

- count of conditions satisfying that vendor's in-range test.

Required reported counts, pooled and by subclass:

- denominator
- valid `first_trade_ts` count
- `NO_FIRST_TRADE_TS` count
- valid `resolved_at` count
- PMXT v2 in-range count/fraction
- Telonex L2 in-range count/fraction
- out-of-range count/fraction
- halt/exclusion reason counts

The spec intentionally sets no automatic pass/fail threshold. It reports exact fractions and counts only.

This version does not compute combined "either vendor" or "both vendors" metrics. Those are out of scope unless separately specified, because adding derived vendor-combination questions would exceed the two-question authorization.

---

## 6. Output artifact design

No artifact is generated by this spec. If a future run is separately authorized, it may produce coverage/time feasibility artifacts only.

Recommended future artifact folder:

`artifacts/named_binary_probe/price_source_option_d_temporal_inrange/`

Recommended future files:

- `option_d_temporal_inrange_precheck.json`
- `option_d_temporal_inrange_precheck.md`
- optional `option_d_temporal_inrange_by_condition.csv`

### 6.1 Summary JSON

The summary JSON should include:

```json
{
  "status": "COMPLETED_OR_TYPED_STOP",
  "authorized_scope": "OPTION_D_TEMPORAL_INRANGE_PRECHECK_ONLY",
  "spec_version": "option-d-temporal-inrange-precheck-YYYY-MM-DD",
  "p0_state_observed": "P0_CLEAR",
  "named_binary_probe_blocked_observed": true,
  "nb_contract_version": "nb-contract-2026-06-28.1",
  "vendor_start_constants": {
    "pmxt_v2": "2026-04-13T19:00:00Z",
    "telonex_l2": "2025-10-11T00:00:00Z"
  },
  "universe_reconciliation": {
    "expected_total": 39693,
    "observed_total": null,
    "matches_expected": null
  },
  "counts_pooled": {
    "denominator": null,
    "valid_first_trade_ts": null,
    "no_first_trade_ts": null,
    "valid_resolved_at": null,
    "pmxt_v2_in_range": null,
    "telonex_l2_in_range": null,
    "pmxt_v2_fraction": null,
    "telonex_l2_fraction": null
  },
  "counts_by_subclass": {},
  "halt_code": null,
  "halt_detail": null,
  "forbidden_actions_observed": {
    "vendor_fetch": false,
    "price_fields_read": false,
    "token_side_fields_read": false,
    "canonical_side_price_computed": false,
    "p1_unblocked": false,
    "probe_execution": false,
    "gate_changed": false
  }
}
```

The exact schema may be adjusted in a later implementation spec, but no price, wallet, `log_index`, PnL, scoring, or side-price fields may be added.

### 6.2 Summary Markdown

The Markdown report should include:

- scope and non-authorization statement;
- exact source files/methods used;
- universe reconciliation;
- timestamp parsing policy;
- pooled and subclass temporal fractions for PMXT v2 and Telonex L2;
- no-price/no-vendor/no-P1-unblock confirmation;
- interpretation limits;
- typed halt if halted.

### 6.3 Optional per-condition ledger

A future per-condition ledger may contain only timing and classification fields.

Allowed columns:

- `condition_id`
- `subclass`
- `first_trade_ts`
- `decision_ts`
- `resolved_at`
- `pmxt_v2_temporally_in_range`
- `telonex_l2_temporally_in_range`
- `exclusion_reason`
- `halt_code`

No other field is allowed without a separate spec revision.

### 6.4 Forbidden output fields

Every output must exclude:

- price values;
- bid/ask/mid/spread/depth values;
- side/canonical price fields;
- token-side price acceptance fields;
- token identifiers and side-enumeration fields (`token_id`, `outcome_index`, side labels), unless separately authorized by a later spec revision;
- `yes_price`;
- wallet identifiers;
- maker/taker role fields;
- OrdersMatched fields;
- `log_index`;
- PnL fields;
- scoring fields;
- forecast-vs-price metrics;
- gate-modification fields.

If any forbidden field appears in an output schema, halt with `STOP_OUTPUT_SCHEMA_FORBIDDEN_FIELD`.

### 6.5 Artifact self-attestation

Any future run report must self-attest:

- no vendor data fetched;
- no external network/API/RPC call made;
- no PMXT archive downloaded;
- no Telonex fetch performed;
- no account/API key/paid action used;
- no price-like field read or computed;
- no canonical-side price computed;
- no P1/P2/P3/probe run;
- no scoring/wallet/OrdersMatched/`log_index`/PnL work;
- no gate changed;
- `named_binary_probe_blocked` observed true.

If self-attestation is absent, halt with `STOP_ARTIFACT_SELF_ATTESTATION_MISSING`.

---

## 7. Required halt / reject labels

The future precheck must use typed halt labels rather than emitting misleading partial numbers.

Required labels:

| Label | Trigger |
|---|---|
| `STOP_NOT_AUTHORIZED` | A future implementation or run is attempted without separate explicit in-chat authorization naming this precheck. |
| `STOP_P0_UNIVERSE_NOT_VERIFIED` | The implementation cannot prove its universe exactly matches accepted P0 `final_p0_eligible`, including pooled and subclass reconciliation. |
| `STOP_STALE_CONTRACT` | `nb_contract_version` is present but does not match the accepted contract version `nb-contract-2026-06-28.1`. |
| `STOP_FIRST_TRADE_TS_UNAVAILABLE` | `Store.load_trades()`, `condition_id`, or `traded_at` is unavailable or unparseable at source/schema level. |
| `STOP_RESOLVED_AT_UNAVAILABLE` | `resolved_at` is unavailable, duplicated ambiguously, or unparseable for the verified universe. |
| `STOP_TIMESTAMP_TIMEZONE_AMBIGUOUS` | `traded_at`, `resolved_at`, or vendor start constants cannot be normalized to unambiguous timezone-aware UTC before comparison. |
| `STOP_NONLOCAL_INPUT_REQUIRED` | The computation would require any nonlocal file, old chat, uploaded duplicate, public mirror, web lookup, or external service not already present in local project/P0 data. |
| `STOP_VENDOR_DATA_REQUIRED` | The computation attempts or requires PMXT/Telonex/vendor data, archive browsing, API access, or a vendor account/key. |
| `STOP_PRICE_FIELD_REQUESTED` | The computation requests, parses, persists, or derives any price-like field, including bid/ask/mid/spread/depth. |
| `STOP_P1_UNBLOCK_ATTEMPT` | The output or workflow treats temporal coverage as accepted price input, P1 viability, or permission to resume P1/P2/P3/probe. |
| `STOP_SCOPE_CREEP` | Any request or code path expands beyond local-only timing feasibility into vendor coverage, source trust, price construction, scoring, wallet work, OrdersMatched, `log_index`, PnL, or gate changes. |
| `STOP_UNIVERSE_RECONCILIATION_FAILED` | Summary and optional per-condition ledger do not reconcile to the verified P0 denominator. |
| `STOP_MISSING_TRADE_ANCHOR_SYSTEMIC` | Conditions without `first_trade_ts` are too numerous or patterned enough to suggest a broken trade source or incorrect universe rather than ordinary missing anchors. |
| `STOP_OUTPUT_SCHEMA_FORBIDDEN_FIELD` | Output contains any forbidden field class listed in §6.4. |
| `STOP_ARTIFACT_SELF_ATTESTATION_MISSING` | Future run artifacts do not explicitly attest no vendor/price/P1/probe/gate/scoring/wallet actions occurred. |
| `STOP_VALIDATION_REQUIRED` | Aggregate output is all-true/all-false or otherwise suspicious before a small validation sample is manually checked. |
| `STOP_VENDOR_HISTORY_CHANNEL_MISMATCH` | Any non-L2 vendor channel is introduced or substituted. This should be unreachable in this local-only precheck because no vendor channel should be touched; if it appears, halt immediately. |

---

## 8. Interpretation rules

### 8.1 Positive temporal result

A positive temporal result establishes only that a fraction of P0-eligible conditions falls inside a vendor's operative L2 archive window.

It does not establish:

- vendor availability for those conditions;
- token coverage;
- side coverage;
- both-side book state;
- book depth;
- price quality;
- mechanical trust;
- price-source viability;
- P1 viability.

A positive result may only justify proposing a later separately authorized vendor-coverage SPEC. It must not authorize vendor fetches, implementation, price artifact construction, or P1 continuation.

### 8.2 Negative temporal result

A negative result may close or deprioritize Option D for a vendor without touching P1.

A negative result does not worsen or resolve P1. P1 was already blocked on missing per-side/token-identity price input and remains blocked.

### 8.3 No automatic threshold

This precheck spec does not set an automatic pass/fail threshold. It reports exact fractions, counts, and exclusions. Orchestrator decides whether the temporal ceiling is high enough to justify a later vendor-coverage SPEC.

---

## 9. Proposed future tests — not authorized here

If implementation is separately authorized later, tests should be designed before real-data reads. This spec does not authorize writing or running them.

Suggested future tests:

- universe reconciliation reproduces exactly `39,693` pooled and `22,012 / 1,003 / 16,678` by subclass on fixtures shaped like the real inputs;
- timestamp parser handles documented UTC strings and pandas `Timestamp` values without naive coercion;
- inclusive boundary: a `decision_ts`/`resolved_at` pair exactly equal to a vendor-start constant counts as in-range;
- one second before a vendor-start constant counts as out-of-range;
- no-price output schema: forbidden price/bid/ask/mid/depth/side/wallet/scoring fields fail schema validation;
- all-one-status guard triggers `STOP_VALIDATION_REQUIRED` rather than silently reporting a suspicious aggregate;
- denominator policy keeps full P0 denominator and counts no-anchor conditions separately;
- stale `nb_contract_version` fixtures halt with `STOP_STALE_CONTRACT`;
- systemic missing trade-anchor fixtures halt with `STOP_MISSING_TRADE_ANCHOR_SYSTEMIC`.

---

## 10. Review acceptance criteria for this spec

This spec should be accepted only if the Orchestrator confirms it:

1. is local-only and read-only;
2. does not authorize implementation/tests/run/artifacts;
3. does not fetch vendor data;
4. does not require or touch price fields;
5. reconstructs and verifies the exact P0 universe before computation;
6. uses the full P0 denominator;
7. handles missing trade anchors explicitly;
8. uses UTC-aware timestamp comparisons;
9. preserves the inclusive lower-bound vendor dates from accepted Option D;
10. prevents false P1 unblock paths;
11. preserves all standing project guardrails;
12. keeps `named_binary_probe_blocked = true`.

---

## 11. Guardrails preserved

This document writes no code, reads no local data, runs nothing, and generates no artifact. It does not fetch from any vendor, create any account, use any API key, or take any paid action. It does not compute any price, bid, ask, mid, spread, depth, or canonical-side price. It does not continue P1/P2/P3, does not score, does not touch wallets/OrdersMatched/`log_index`/PnL, does not modify the audit gate, and does not flip `named_binary_probe_blocked`.

Executing this precheck requires separate, explicit, in-chat user authorization naming the precheck itself. Accepting this spec is not execution authorization.

**Final accepted-spec label:** `OPTION_D_TEMPORAL_INRANGE_PRECHECK_SPEC_ACCEPTED_SPEC_ONLY`
