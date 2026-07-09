# HANDOFF — Orchestrator — Option D temporal in-range precheck RESULT

**Decision:** ACCEPT FINDING

**Result label:** `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`

**Run status:** `COMPLETED`

**Scope:** local-only, read-only, timing-feasibility-only. No vendor data was fetched, no archive was downloaded, no account/API key/paid action was used, no price/bid/ask/mid/spread/depth/canonical-side value was read or computed, no P1/P2/P3/probe/scoring/wallet/OrdersMatched/log_index/PnL/gate action occurred, and `named_binary_probe_blocked` remained true.

---

## Accepted universe reconciliation

- Pooled expected: `39,693`
- Pooled observed: `39,693`
- Matches expected: `True`

By subclass:

| Subclass | Expected | Observed |
|---|---:|---:|
| UP_DOWN | 22,012 | 22,012 |
| OVER_UNDER | 1,003 | 1,003 |
| NAMED_OTHER | 16,678 | 16,678 |

No first-trade anchors were missing. No `resolved_at` values were missing.

---

## Accepted temporal in-range results

### Pooled

| Vendor window | In range | Denominator | Fraction |
|---|---:|---:|---:|
| PMXT v2 | 18,137 | 39,693 | 0.456932 |
| Telonex L2 | 37,749 | 39,693 | 0.951024 |

### By subclass

| Subclass | PMXT v2 in range | PMXT v2 fraction | Telonex L2 in range | Telonex L2 fraction |
|---|---:|---:|---:|---:|
| UP_DOWN | 11,649 | 0.529211 | 21,455 | 0.974696 |
| OVER_UNDER | 663 | 0.661017 | 982 | 0.979063 |
| NAMED_OTHER | 5,825 | 0.349263 | 15,312 | 0.918096 |

---

## Interpretation

- **PMXT v2:** closed/deprioritized for broad full-P0 Option D coverage on timing grounds: only `0.456932` pooled temporal coverage. A PMXT API key does not change the PMXT v2 start-date limitation. Any future PMXT work would require a separate narrow-subset SPEC ONLY authorization and must not be treated as broad P0 coverage.
- **Telonex L2:** plausible next candidate only for a separate **SPEC ONLY** vendor-coverage review. Pooled temporal coverage is `0.951024`, but `NAMED_OTHER` is below 0.95 at `0.918096`, so this is not an automatic pass.
- **P1 remains blocked.** Timing feasibility is not vendor availability, token coverage, side coverage, both-side book state, book depth, price quality, mechanical trust, price-source viability, or P1 viability.

---

## Standing non-authorization

No vendor fetch, PMXT online/API-key test, Telonex fetch, account/API key/paid action, Pass 1, Pass 2, price artifact, bid/ask/mid/spread/depth/canonical-side price computation, P1/P2/P3/probe, scoring, wallet discovery, OrdersMatched/log_index/PnL, gate change, or side synthesis is authorized by this result.

`named_binary_probe_blocked` remains true.
