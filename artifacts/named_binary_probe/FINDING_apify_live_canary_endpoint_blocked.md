# FINDING — Apify Live Canary: Endpoint Blocked (REVISED)

**Original result label (retained, historical, unchanged):** `APIFY_LIVE_CANARY_COMPLETED_ENDPOINT_BLOCKED`
**Refined causal label (this revision, additive — does not replace the original):** `APIFY_PYTHON_URLLIB_TRANSPORT_BLOCKED`
**Status:** Documentation-only finding — REVISED (complete replacement of the prior version)
**Scope:** Infra/reachability + transport-profile evidence only — not P1 evidence, not coverage evidence, not a Cloudflare bypass
**Date recorded (original):** 2026-07-11
**Date revised:** 2026-07-11

---

## 0. Revision note — read this before the rest of the document

This is a **complete replacement** of the prior `FINDING_apify_live_canary_endpoint_blocked.md`. What changes, and what doesn't:

- **Unchanged:** the original Apify live-run result (§2–§3 below). Nothing about what was actually observed on Apify is rewritten as a success, and the original result label (`APIFY_LIVE_CANARY_COMPLETED_ENDPOINT_BLOCKED`) is retained for historical traceability, not erased.
- **New:** two controlled local diagnostics (§4) that were not available when the original finding was written — a local Python-`urllib` recreation and a local curl/libcurl recreation of the identical six requests.
- **Changed:** the causal interpretation (§5). The original finding's wording ("the block operates ... against this Actor's outbound requests specifically") is corrected below, because the new evidence shows the block is **not** specific to Apify's network origin — the same block reproduced locally via `urllib`. That phrasing is removed and replaced with the more precise, narrower claim the evidence actually supports: transport/client-profile sensitivity, not confirmed Apify-origin isolation.

### Evidence provenance

The two local diagnostics in §4 are drawn from four supporting artifacts:

- `local_clob_live_canary_20260711T214800Z.json`
- `local_clob_live_canary_20260711T214800Z.md`
- `local_clob_curl_canary_20260711T215418Z.json`
- `local_clob_curl_canary_20260711T215418Z.md`

**Claude did not independently inspect these four files during this drafting task** — they were not supplied to Claude as uploads or otherwise made accessible. The Orchestrator independently inspected these artifacts before issuing the patch request that produced this revision. This finding summarizes the results as **reported by the Orchestrator and verified by the Orchestrator against those artifacts** — not as independently re-derived by Claude from the raw files. If the user uploads the accepted package, these four files should be retained as supporting branch artifacts alongside this finding, so a future reader can trace the reported results back to their source.

This is consistent with, and extends, the provenance statement already made for the original Apify run (unchanged from the prior version): no raw dataset file has been independently inspected by Claude for the original Apify run either. The original Apify facts were cross-checked for internal consistency against this project's `live_canary.py` implementation (§0 of the original finding) and found consistent; that cross-check is a corroboration of internal consistency, not a substitute for direct inspection of any of the six files (the original run's data plus these four) referenced across this finding.

---

## 1. Scope

Unchanged from the original. This document is documentation only. It authorizes no code changes, no Actor changes, no further Apify run, no network call, no price artifact, no P1/P2/P3/probe continuation, no scoring, no wallet work, no gate change, and no change to the standing P1 blocker or to `S1_SOURCE_NOT_VIABLE`.

This revision additionally makes explicit (see §7) that it authorizes no general retry work, no proxy rotation, no browser impersonation, and no anti-bot/fingerprint-spoofing work of any kind — the new evidence does not open the door to any of that; see §6 for why.

---

## 2. Original Apify live-run configuration (historical — unchanged)

- **Authorization:** one explicit live run of the 3-condition live canary (one condition per subclass — `UP_DOWN`, `OVER_UNDER`, `NAMED_OTHER` — from the accepted real-condition manifest).
- **Input flags:** `dry_run = false`, `live_canary_enabled = true`, `acknowledge_not_p1_evidence = true`, `live_include_current_endpoint_check = false`.
- **Request plan:** mandatory only — 3 conditions × 2 side tokens = 6 CLOB `GET /prices-history` requests (single-market form). No optional current-endpoint requests. No Gamma requests.
- **Execution origin:** the Apify Actor's own Python `urllib.request`-based `HttpFetcher` (see `src/live_canary.py`), running inside Apify's hosting environment.

---

## 3. Original Apify observed result (historical — unchanged)

Output rows: 9 total.

| Row type | Count |
|---|---|
| `raw_request_summary_row` | 6 |
| `parsed_side_candidate_row` | 0 |
| `condition_pair_summary_row` | 3 |
| **Total** | **9** |

- All 6 `raw_request_summary_row` entries recorded **HTTP 403**.
- All 6 `request_classification` values: `APIFY_LIVE_CANARY_ENDPOINT_ERROR`.
- Raw response excerpts identify **Cloudflare Error 1010 / "Access denied" / `browser_signature_banned`**.
- **0** `parsed_side_candidate_row` rows.
- All 3 `condition_pair_summary_row` records: `side_0_status = ERROR`, `side_1_status = ERROR`, `condition_pair_status = BOTH_SIDES_MISSING_OR_BLOCKED`.
- No candidate prices were produced for any condition, either side.
- Every row (all 9) carries `disclaimer_label = APIFY_LIVE_CANARY_NOT_P1_EVIDENCE`.

**Correction to the original wording (this revision):** the original finding stated the block operated "against this Actor's outbound requests **specifically**" — implying the Apify network origin itself had been isolated as the cause. That implication is withdrawn in this revision; see §5. The block is still fully real and still fully blocked the original run — only the *specifically-Apify-origin* framing is corrected.

---

## 4. New evidence — controlled local diagnostics (this revision)

Both diagnostics reused the identical three conditions, the identical six token IDs, the identical six `/prices-history` URLs, the identical ±3,600-second windows, and the identical `fidelity=1` as the original Apify run — only the execution origin and HTTP transport/client differ.

### 4.1 Local Python `urllib` run

- **Execution origin:** `LOCAL_WINDOWS_PYTHON_URLLIB`
- **Transport:** Python `urllib.request`, `Accept: application/json`, 15-second timeout, no retries — the same transport library the Apify Actor itself uses.
- **Result:** all six requests returned **HTTP 403**, all six returned **Cloudflare Error 1010 / `browser_signature_banned`**, **zero** candidate rows.

### 4.2 Local curl/libcurl run

- **Execution origin:** `LOCAL_WINDOWS_CURL_EXE_LIBCURL`
- **Executable:** `C:\Windows\System32\curl.exe`
- **Transport:** one attempt per request, no retries, no custom headers, no user-agent override, no proxy configuration, no cookie jar, no browser emulation.
- **Result:** all six curl exit codes were `0`; all six responses were **HTTP 200**; all six matched the documented `{"history": [...]}` structure; **six** parsed candidate rows were produced; all three conditions showed `condition_pair_status = BOTH_SIDES_PRESENT`.

**Observed diagnostic candidates** (diagnostic only — not accepted P1 prices, not `canonical_side_price`, not derived via `yes_price`/`1 - price`):

| Condition | Side | Candidate price | Signed gap (s) |
|---|---|---|---|
| `UP_DOWN` | 0 | 0.995 | −3360 |
| `UP_DOWN` | 1 | 0.005 | −3359 |
| `OVER_UNDER` | 0 | 0.49 | +3 |
| `OVER_UNDER` | 1 | 0.51 | 0 |
| `NAMED_OTHER` | 0 | 0.54 | −14 |
| `NAMED_OTHER` | 1 | 0.46 | −13 |

---

## 5. Revised causal interpretation (this revision)

Putting §2–§4 together:

1. The Apify Actor's Python-`urllib` request path **was blocked by Cloudflare Error 1010**.
2. A later local Python-`urllib` recreation of the identical six requests **produced the same uniform 403/1010 result**.
3. A later local curl/libcurl recreation of the identical six URLs **produced six HTTP 200 responses**.

**Therefore:**

- **Apify network origin alone is not established as the cause.** The block reproduced from a local Windows machine using the same transport library — if Apify's IP range or hosting origin were the sole cause, the local `urllib` run would not be expected to show the identical block.
- **CLOB endpoint unreachability is not established.** The same six URLs, same tokens, same windows, same fidelity, returned clean HTTP 200 with the documented shape via curl — the endpoint itself is reachable and responsive to *some* client profile.
- **The evidence implicates the HTTP transport/client profile** — something about how `urllib` presents itself (at the TLS layer, HTTP layer, header layer, or some combination) differs from how curl presents itself, and Polymarket's Cloudflare-fronted edge treats the two differently.
- **The evidence does not isolate the exact decisive feature.** Two client libraries differ in many dimensions simultaneously (TLS library and negotiated cipher/extension set, HTTP/1.1 vs HTTP/2 behavior, default header set and ordering, connection-handling behavior, and more). This finding does not attempt to and cannot disentangle which of these, or which combination, Cloudflare's edge is actually keying on.

**Explicit non-claims (this revision does NOT assert any of the following):**

- Does **not** claim that changing only the user-agent header would be sufficient to restore reachability.
- Does **not** claim that TLS fingerprint alone is the proven cause.
- Does **not** claim that curl will necessarily succeed if run **from Apify's own hosting environment** — the successful curl run was local (Windows), not from Apify; whether curl's transport profile also succeeds from Apify's network origin is precisely the open question a future, separately authorized canary would need to test (see `SPEC_apify_transport_isolation_canary.md`).
- Does **not** describe any of this as a "Cloudflare bypass," an evasion, or a countermeasure success. Nothing here defeated, circumvented, or was designed to defeat Polymarket's bot/edge protection — it is an observation of differential behavior between two ordinary, unmodified HTTP client libraries.
- Does **not** overturn the original historical result label. `APIFY_LIVE_CANARY_COMPLETED_ENDPOINT_BLOCKED` remains the accepted label for what was actually observed on Apify. `APIFY_PYTHON_URLLIB_TRANSPORT_BLOCKED` is an **additive, refining** causal label — it says *why* the original block likely occurred (transport-profile sensitivity, not simply "Apify is blocked"), not that the original observation was wrong.

---

## 6. Explicit non-meanings (carried forward and reaffirmed from the original, unchanged in substance)

- **Does not establish the endpoint's response shape as a new fact.** The curl run's clean `{"history": [...]}` responses are consistent with what `SPEC_price_source_s1_coverage.md` §5 already documented — this finding does not add new shape evidence beyond confirming consistency for these 3 conditions via one particular transport.
- **Does not establish P0 coverage of any kind.** 3 conditions was never a coverage test (`SPEC_apify_live_price_source_canary.md` §7), and nothing about running a different local diagnostic changes that.
- **Does not overturn or modify `S1_SOURCE_NOT_VIABLE`.** That result remains accepted and on the `DECISION_LOG.md` "DO NOT REOPEN" list, untouched by this revision.
- **Does not unblock P1.** `named_binary_probe_blocked` remains `true`; the standing per-side/token-identity price-input blocker (`PRICE_INPUT_CONTRACT_named_binary_probe.md`) is unaffected. The diagnostic candidate prices in §4.2 are exactly that — diagnostic — and are not `canonical_side_price`, not derived via `yes_price`/`1 - price`, and not usable by P1 without a later, separately accepted price-selection build spec.
- **Does not authorize** any of the items in §7.

---

## 7. Standing guardrails (updated this revision)

The following remain in force, with new items added given the transport-sensitivity evidence:

- `dry_run = false` for any further live run remains unauthorized without separate explicit authorization.
- **No general retry authorization** — neither of a `urllib`-based run nor any other.
- **No proxy rotation** (residential or otherwise).
- **No browser impersonation** (Selenium, Playwright, or similar) of any kind.
- **No anti-bot or fingerprint-spoofing work** — no `curl_cffi`, no libcurl-impersonate, no TLS-fingerprint impersonation, no copied/spoofed browser headers, no user-agent spoofing, no challenge-solving, no session replay, no cookie harvesting.
- Alternate-endpoint or alternate-data-source substitution remains unauthorized.
- Full P0 price-source build remains unauthorized.
- P1 continuation remains unauthorized.
- P2/P3/probe execution remains unauthorized.
- Scoring remains unauthorized.
- Wallet discovery / wallet-copying remains unauthorized.
- `OrdersMatched`, `log_index`, and PnL analysis remain unauthorized.
- No project gate changes are implied.
- No claim of a "Cloudflare bypass" may be made based on this finding or on any future transport-isolation canary result.

---

## 8. Standing blocker (unchanged in substance)

P1 remains blocked on missing per-side/token-identity decision-time price input. This finding — including its revision — does not change that. The diagnostic candidate prices observed via the local curl run (§4.2) are not accepted P1 prices; the accepted price-input blocker is entirely unaffected:

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

---

## 9. Recommended next step

A specification-only document, `SPEC_apify_transport_isolation_canary.md`, has been drafted alongside this revision (delivered separately, `PROPOSED / SPEC ONLY — NOT YET REVIEWED OR ACCEPTED`). It proposes testing — if and when separately authorized at every later stage — whether an ordinary curl/libcurl transport, run *from Apify's own hosting environment* (not locally), changes reachability for the identical fixed six-request canary. This finding does not itself authorize that spec, its implementation, or any run; it only records that such a narrowly-scoped follow-up question now has a clear basis, given the transport-sensitivity evidence in §4–§5.

---

## 10. File placement

Recommended project path:

```text
artifacts/named_binary_probe/FINDING_apify_live_canary_endpoint_blocked.md
```

(Complete replacement of the prior version at this same path.)
