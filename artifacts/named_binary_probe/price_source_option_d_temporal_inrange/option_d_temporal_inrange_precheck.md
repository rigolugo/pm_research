# Option D Temporal In-Range Precheck — Result Report

**Spec:** `SPEC_price_source_option_d_temporal_inrange_precheck.md` (`OPTION_D_TEMPORAL_INRANGE_PRECHECK_SPEC_ACCEPTED_SPEC_ONLY`)
**Spec version:** `option-d-temporal-inrange-precheck-2026-07-09`
**Status:** `COMPLETED`

## Scope and non-authorization

This is a **local-only, read-only, timing-feasibility-only** precheck. It computed only whether P0-eligible conditions fall inside two vendor archive windows by date. It fetched no vendor data, downloaded no archive, used no account/API key, read/computed no price/bid/ask/mid/spread/depth/canonical-side value, read no token/side fields, ran no P1/P2/P3/probe, performed no scoring/wallet/OrdersMatched/`log_index`/PnL work, and changed no gate. `named_binary_probe_blocked` remains `true`.

## Universe reconciliation

- Expected pooled `final_p0_eligible`: **39693**
- Observed pooled: **39693**
- Matches expected: **True**

| Subclass | Expected | Observed |
|---|---:|---:|
| UP_DOWN | 22012 | 22012 |
| OVER_UNDER | 1003 | 1003 |
| NAMED_OTHER | 16678 | 16678 |

## Timestamp policy

- `first_trade_ts = min(traded_at)` per `condition_id` (`Store(data_root).load_trades()`, reading only `condition_id` + `traded_at`).
- `decision_ts = first_trade_ts + 3600s`.
- `resolved_at` from `named_binary_resolution_source_rows.parquet`, parsed explicitly to timezone-aware UTC.
- All timestamps normalized to timezone-aware UTC before comparison; naive timestamps halt (`STOP_TIMESTAMP_TIMEZONE_AMBIGUOUS`).
- Vendor lower bounds are **inclusive**; there is no upper-bound test:
  - PMXT v2: `>= 2026-04-13T19:00:00Z`
  - Telonex L2: `>= 2025-10-11T00:00:00Z`

## Temporal in-range fractions

### Pooled

- Denominator: **39693** (valid first_trade_ts 39693, no_first_trade_ts 0)
- PMXT v2 in range: **18137** (fraction **0.456932**)
- Telonex L2 in range: **37749** (fraction **0.951024**)

### By subclass

| Subclass | Denom | PMXT v2 in-range | PMXT v2 frac | Telonex L2 in-range | Telonex L2 frac |
|---|---:|---:|---:|---:|---:|
| UP_DOWN | 22012 | 11649 | 0.529211 | 21455 | 0.974696 |
| OVER_UNDER | 1003 | 663 | 0.661017 | 982 | 0.979063 |
| NAMED_OTHER | 16678 | 5825 | 0.349263 | 15312 | 0.918096 |

## Self-attestation

- `account_api_key_paid_action`: **False**
- `canonical_side_price_computed`: **False**
- `external_network_api_rpc_call`: **False**
- `gate_changed`: **False**
- `named_binary_probe_blocked_observed`: **True**
- `p1_unblocked`: **False**
- `pmxt_archive_downloaded`: **False**
- `price_fields_read`: **False**
- `probe_execution`: **False**
- `scoring_wallet_ordersmatched_logindex_pnl`: **False**
- `telonex_fetch`: **False**
- `token_side_fields_read`: **False**
- `vendor_fetch`: **False**

## Interpretation limits

A positive temporal in-range fraction establishes **only** that those conditions fall inside a vendor's operative window. It does **not** establish vendor availability, token coverage, side coverage, both-side book state, book depth, price quality, mechanical trust, price-source viability, or P1 viability. A positive result may only justify proposing a later, separately authorized vendor-coverage SPEC. A negative result may close or deprioritize Option D for a vendor **without touching P1**, which remains blocked on the missing per-side/token-identity price input. There is no automatic pass/fail threshold; the Orchestrator decides.
