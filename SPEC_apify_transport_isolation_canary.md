# SPEC — Apify Transport Isolation Canary (system curl/libcurl vs. Python `urllib`)

**Status:** ACCEPTED — **SPEC ONLY. NO IMPLEMENTATION OR RUN AUTHORIZED.** **Orchestrator decision date:** 2026-07-11. This document authorizes nothing by itself: no code implementation, no dependency or Dockerfile change, no Actor build, no deployment, no dry run, no live run, no CLOB request, no Apify request, no package installation, no broader sample, no retry, no P1 artifact, no manifest creation, and no P1/P2/P3/probe/scoring continuation. Each later stage requires its own separate, explicit authorization.

**Produced by:** Claude (implementation agent), for Orchestrator (ChatGPT) / user review.

**Depends on:** `FINDING_apify_live_canary_endpoint_blocked.md` (accepted as written, unchanged in this patch — records the original Apify block and the transport-sensitivity evidence this spec follows up on), `SPEC_apify_live_price_source_canary.md` (accepted — the design this spec's fixed request plan is inherited from), `src/live_canary.py` (accepted implementation whose request-plan, row-type, and token-identity conventions this spec reuses without duplication). **Note:** `live_canary.py`'s accepted Actor receives conditions via `Actor.get_input()`/`raw_input` at runtime — it does not load any manifest file from disk or from the repo. §3 below pins how a future transport-isolation implementation must relate to a fixed manifest file without creating a second runtime path.

**Revision note (this final patch):** Five corrections applied on top of the prior patch, per Orchestrator review:

1. **PycURL removed as an allowed transport (§2).** The only transport in this spec is now the system `curl` executable backed by ordinary libcurl. PycURL is explicitly out of scope; a later proposal to use it would need its own separate review.
2. **Manifest runtime interface pinned (§3).** Exact JSON shape pinned (a single `conditions` array, identity fields only, no operational flags). Runtime behavior pinned: the Actor keeps using `Actor.get_input()`/`raw_input`; no second direct-file runtime path is created; the fixed file is a reviewed identity/reconciliation artifact checked against `raw_input` before any request, with no normalization of side assignment or token identity. Responsibility pinned: Orchestrator/user supplies and accepts the manifest; Claude must not fabricate or independently select its contents.
3. **Complete exact schemas (§7).** All 22 retained `raw_request_summary_row` fields, all 12 additive transport fields (added `curl_supported_protocols`), all 17 `parsed_side_candidate_row` fields, and all 15 `condition_pair_summary_row` fields are now fully enumerated — not partially listed or referenced by description. `curl_version_output` is now described as the *bounded* raw `curl --version` output, not the "full" output.
4. **Handoff counts corrected.** The handoff (delivered alongside this spec) now states the correct field counts (22/12/17/15), replacing the prior incorrect "21 retained / 5 additive."
5. **Open-design section cleaned (§12).** Removed four now-resolved questions (system curl vs. PycURL; file-loading vs. Actor-input mechanism; who prepares the manifest; whether the 2000-byte curl-version bound is accepted — it is accepted). Three genuinely open implementation-stage questions remain.

No implementation, no code edit, no network request, no build, and no run occurred in producing this patch.

---

## 1. Exact research question

> Keeping the accepted manifest identity, six URLs, request windows, fidelity, request count, parsing rules, and disclaimer discipline fixed, does replacing Python `urllib` with ordinary curl/libcurl change endpoint reachability from Apify?

This is **transport-isolation evidence only**. It is explicitly **not**:

- a coverage test
- a source-viability test
- a P1 artifact build
- a retry of S1
- an S1 reversal
- a Cloudflare-bypass project
- a browser-emulation experiment
- a proxy experiment

---

## 2. Transport definition

The **only** transport in this spec is:

```text
system curl executable backed by ordinary libcurl
```

This is not one of several options — it is the sole allowed transport. Reasons:

- this is the transport actually tested successfully in the controlled local diagnostic (§4.2 of the finding);
- all preflight and command interfaces in this spec are already executable-based (§4, §6);
- a Python binding (e.g. PycURL) would introduce an additional wrapper layer and potentially a new dependency/build change, which this spec does not authorize.

**PycURL, or any other libcurl binding, is outside the scope of this spec.** A later proposal to use PycURL instead of (or alongside) the system `curl` executable would require its own separate review — it is not an option under this document.

**Explicitly prohibited**, without exception, regardless of framing:

- `curl_cffi`
- libcurl-impersonate
- browser impersonation of any kind
- TLS-fingerprint impersonation
- Selenium or Playwright
- custom anti-bot headers
- user-agent spoofing
- copied/browser-derived headers
- proxy rotation (residential or otherwise)
- cookie harvesting
- challenge solving
- session replay
- falling back to `urllib`, `requests`, or any other transport after a curl failure

This is **not** an evasion or bypass task. Any design or implementation that drifts toward the prohibited list, even incrementally, is out of scope for this spec and would require an entirely separate authorization and framing — not an extension of this one.

---

## 3. Operational manifest — currently absent, pinned future fixed path

The required operational manifest path is:

```text
artifacts/named_binary_probe/apify_price_canary_real_condition_input.json
```

**This file is currently absent from the repository.** Verified directly by Claude: `HTTP 404` fetching this path from both `apify-price-canary-dry-run` and `main`. This spec does not claim the file exists, and **acceptance of this spec does not authorize creating or committing it.**

### 3.1 Pinned shape

The file, when supplied, must contain **exactly one** `conditions` array with **exactly the three reviewed conditions**, identity fields only:

```json
{
  "conditions": [
    {
      "condition_id": "...",
      "nb_subclass": "...",
      "decision_ts": "...",
      "side_0_token_id": "...",
      "side_1_token_id": "..."
    }
  ]
}
```

**Operational flags are not part of this identity file** — no `dry_run`, no `live_canary_enabled`, no `acknowledge_not_p1_evidence`, no request caps, no fidelity/window overrides, no other runtime control. This file records condition/token identity only.

### 3.2 Pinned runtime behavior

- The Actor continues receiving runtime data through `Actor.get_input()` / `raw_input`, exactly as the existing accepted live-canary Actor already does. **The future implementation must not create a second, direct-file runtime execution path** — this fixed file is not an alternate way for the Actor to obtain its input at runtime.
- The fixed file is the **reviewed identity/reconciliation artifact**: it pins, in the repo, exactly which three conditions and six tokens were reviewed and accepted, so that whatever `raw_input` the Actor actually receives at runtime can be checked against it before any request.
- **Before any request**, `raw_input["conditions"]` must reconcile **exactly** to the fixed file:
  - exact condition IDs;
  - exact subclasses;
  - exact decision timestamps;
  - exact side-0 and side-1 token assignments;
  - exact decimal-string forms;
  - exactly three conditions;
  - exactly six unique tokens.
- **Normalize neither side assignment nor token identity.** If `raw_input` and the fixed file disagree on which token is side 0 vs. side 1 for a condition, or differ in string form (e.g. leading zeros, whitespace) even where numerically equal, that is a reconciliation **failure** — not something to silently coerce into agreement.
- **If the file is absent, malformed, or does not exactly match runtime input, hard-stop with zero CLOB requests:**

```text
STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID
```

This check is independent of, and must both pass alongside, the curl-transport preflight in §4 — both gates must clear before any request is made.

### 3.3 Pinned responsibility

- **The Orchestrator/user supplies and accepts the exact manifest content.**
- **Claude must not fabricate or independently select its contents** — not for this spec, and not for any future implementation task, unless a separate, explicit authorization says otherwise.
- A later, separately authorized implementation package may include the supplied file at the path above, once the Orchestrator/user has supplied and accepted it.

This section resolves the manifest-loading-mechanism and manifest-authorship questions from the prior patch's open-design list — both are now pinned, not open (see §12).

---

## 4. Required zero-network preflight (curl/libcurl provenance)

Before any future network run, and independent of the manifest check in §3, the design must require a preflight that records, without making any CLOB/Gamma/Polymarket request:

- whether `curl` exists on the execution environment
- the executable path
- the full `curl --version` output (captured, then bounded per §7.2 for storage)
- curl version
- libcurl version
- TLS backend (e.g. OpenSSL/BoringSSL/Schannel, whatever curl reports)
- supported protocols (parsed into `curl_supported_protocols`, §7.2)
- the return code from the version-check command itself (`curl_version_exit_code`, §7.2)

**If curl/libcurl is unavailable, or its provenance cannot be captured, the run hard-stops before any CLOB request** with a label:

```text
STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE
```

No package installation or container/Dockerfile modification is authorized by this spec. If a future implementation finds curl is not present in the Actor's current container image, adding it would itself require a separate implementation authorization after this spec is accepted — this spec does not pre-approve that step.

---

## 5. Fixed request plan

A future canary, if later implemented and separately authorized to run, must use — with **zero** deviation:

- exactly the existing three accepted conditions (one condition per subclass: `UP_DOWN`, `OVER_UNDER`, `NAMED_OTHER`), obtained via `raw_input` and reconciled exactly against the fixed manifest per §3, as the **sole** operational source of condition and token identity. **No second, independently hardcoded operational manifest is created.**
- exactly two token requests per condition (side 0, side 1) — exactly **six** total HTTP requests.
- only `GET /prices-history`, single-market form (`market=TOKEN_ID&startTs=...&endTs=...&fidelity=...`) — no batch endpoint.
- the exact existing token IDs, exact existing decision timestamps, exact existing ±3,600-second windows, exact `fidelity=1` — all unchanged from the reconciled manifest (§3) and from `SPEC_apify_live_price_source_canary.md`.
- one attempt per URL. No retries. No parallel expansion.
- **No Gamma, no `/book`, no `/price`, no `/midpoint`, no `/spread`, no batch endpoint** — the mandatory six `/prices-history` requests only, nothing else, in any circumstance.

---

## 6. Curl command constraints

A future implementation must use **ordinary curl behavior only**. Allowed functional arguments are limited to what is strictly necessary for bounded, single-shot collection:

- silent-but-show-errors output mode
- an exact `--max-time 15` bound per request
- `GET` (curl's default; no method override needed)
- output the response body to a bounded temporary file (not stdout captured unbounded)
- dump response headers separately
- emit the resulting HTTP status
- the exact target URL

**Must NOT set:**

- a custom user-agent
- a custom `Accept` header
- any browser-like header
- a cookie jar, or any manually supplied cookie
- `Referer` or `Origin`
- any proxy
- any retry flag
- any compression/browser-mimicry option
- any HTTP-version forcing flag, unless a future revision explicitly justifies one and that revision is separately reviewed — not assumed by this spec

The six requests must execute **sequentially in the fixed manifest order**. Each request must be a **fresh curl process**, invoked independently, unless a future revision explicitly justifies a different ordinary-libcurl mechanism (e.g. a single libcurl multi-handle) and that revision is separately reviewed. **No cookie persistence or session state of any kind between the six requests.**

---

## 7. Required output

The same three logical row types are retained. All existing fields and field names remain unchanged. Transport-provenance fields are additive and are defined explicitly below.

1. `raw_request_summary_row`
2. `parsed_side_candidate_row`
3. `condition_pair_summary_row`

### 7.1 `raw_request_summary_row` — all 22 retained fields (unchanged, verified against `src/live_canary.py`'s accepted implementation)

```text
row_type
run_id
request_id
condition_id
nb_subclass
side
endpoint
request_token_id
request_url_market_param
request_url_actual
window_start_ts
window_end_ts
fidelity
http_status
response_byte_length
raw_point_count
raw_response_excerpt
response_body_token_id
token_identity_basis
fetched_at
request_classification
disclaimer_label
```

`response_byte_length` is retained exactly as named — not renamed to `response_byte_count`.

### 7.2 `raw_request_summary_row` — all 12 additive transport-provenance fields (new, this spec)

```text
execution_origin
transport
curl_executable_path
curl_version
libcurl_version
tls_backend
curl_supported_protocols
curl_version_output
curl_version_exit_code
curl_exit_code
curl_stderr_excerpt
response_headers_excerpt
```

| Field | Meaning | Bound |
|---|---|---|
| `execution_origin` | Fixed value `APIFY_CURL_LIBCURL` for this canary | — |
| `transport` | Fixed value `CURL` | — |
| `curl_executable_path` | Absolute path to the curl binary, from the preflight (§4) | — |
| `curl_version` | Parsed curl version string, from the preflight | — |
| `libcurl_version` | Parsed libcurl version string, from the preflight | — |
| `tls_backend` | Parsed TLS backend name, from the preflight | — |
| `curl_supported_protocols` | Deterministic list of protocol strings parsed from the protocol line of `curl --version` (e.g. `["http","https","ftp", ...]`), from the preflight | — |
| `curl_version_output` | The **bounded** decoded `curl --version` output — not the "full" output; truncated to the bound below | **2000 characters** |
| `curl_version_exit_code` | Exit code of the `curl --version` command itself (preflight step, §4) — distinct from `curl_exit_code` below | — |
| `curl_exit_code` | Exit code of this specific data-fetching curl invocation (one per request) | — |
| `curl_stderr_excerpt` | Captured stderr from this specific curl invocation, decoded with replacement on errors | **500 characters** |
| `response_headers_excerpt` | Captured response headers for this specific request, decoded with replacement on errors | **1000 characters** |

**Fixed bounds (explicit, deterministic, plain truncation — no attempt to preserve "complete" lines or fields past the bound):**

```text
raw_response_excerpt      = 500 decoded characters   (retained behavior)
curl_stderr_excerpt       = 500 decoded characters
response_headers_excerpt  = 1000 decoded characters
curl_version_output       = 2000 decoded characters
```

The retained `raw_response_excerpt` behavior is preserved exactly: decode the response body as UTF-8 with replacement on decode errors, then retain the first 500 characters. The existing constant name `RAW_EXCERPT_MAX_BYTES` is historical; the accepted implementation slices decoded text rather than raw bytes.

### 7.3 Disclaimer (every row, every type)

Every row, of every type, must carry exactly:

```text
APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE
```

**Do not emit the old live-canary disclaimer (`APIFY_LIVE_CANARY_NOT_P1_EVIDENCE`) for this separate transport-isolation run.** The two canaries are distinct, separately authorized efforts; their disclaimers must not be interchanged or blended.

### 7.4 `parsed_side_candidate_row` — all 17 fields (complete enumeration)

```text
row_type
run_id
condition_id
nb_subclass
side
token_id
decision_ts
candidate_price
candidate_source_ts
signed_gap_seconds
point_selection_method
side_status
schema_matches_documented
price_in_range_0_1
timestamp_parseable
is_synthesized
disclaimer_label
```

**No transport fields, and no `token_identity_basis`, are added to this row.** This matches the accepted live-canary implementation's actual field layout: `src/live_canary.py`'s `_parsed_side_candidate_row` function does not include `token_identity_basis` (verified by reading the implementation directly). A candidate row's token-identity provenance is available by joining back to its corresponding `raw_request_summary_row` via `run_id` + `condition_id` + `side`.

`is_synthesized` is always hardcoded `false`. **No** `canonical_side_price` anywhere on this row.

### 7.5 `condition_pair_summary_row` — all 15 fields (complete enumeration)

```text
row_type
run_id
condition_id
nb_subclass
side_0_token_id
side_1_token_id
side_0_price_candidate
side_1_price_candidate
side_0_source_ts
side_1_source_ts
side_0_status
side_1_status
condition_pair_status
disclaimer_label
generated_at
```

**No transport fields are required on this row.** Transport provenance (`execution_origin`, `transport`, all `curl_*` fields, `response_headers_excerpt`, etc.) is recorded on the two corresponding `raw_request_summary_row` entries (one per side), joinable via `run_id` + `condition_id` + `side` if a reader needs to trace a pair's provenance back to its individual requests.

---

## 8. Required classifications

Transport-specific classifications, chosen so they cannot be mistaken for a source-viability verdict:

- `APIFY_CURL_TRANSPORT_USABLE_SHAPE`
- `APIFY_CURL_TRANSPORT_EMPTY_HISTORY`
- `APIFY_CURL_TRANSPORT_PARSE_BLOCKED`
- `APIFY_CURL_TRANSPORT_ENDPOINT_ERROR`
- `APIFY_CURL_TRANSPORT_EXECUTION_ERROR` (curl itself failed to execute or returned a non-zero exit code before any HTTP response was obtained — distinct from an HTTP-level error)

Condition-pair statuses remain the same three as the accepted live-canary design:

- `BOTH_SIDES_PRESENT`
- `ONE_SIDED_ONLY`
- `BOTH_SIDES_MISSING_OR_BLOCKED`

**Must never emit**, under any circumstance: `SOURCE_VIABLE`, `COVERAGE_CLEAR`, `S1_OVERTURNED`, `P1_UNBLOCKED`, or any comparable downstream verdict. No code path in a future implementation may construct or emit any label resembling these.

---

## 9. Required interpretation matrix

A future implementation's documentation (and any finding written about a future run) must define these four outcomes in advance:

1. **All six curl requests also return Cloudflare 1010 (or equivalent block).**
   Transport substitution did not restore reachability from Apify. No further retry or evasion work follows from this result — it would indicate the block is not resolved by transport substitution alone, and any next step is a new, separately authorized question, not an automatic escalation.

2. **Some curl requests return 200 and some fail.**
   Mixed transport/reachability evidence only. Not coverage evidence. No rerun is automatically authorized by this outcome.

3. **All six curl requests return 200 with usable shape.**
   The Apify curl/libcurl transport path is reachable, on this fixed six-request canary, from Apify's hosting environment. This would confirm transport/client-profile sensitivity (extending the local-diagnostic finding to Apify's own network origin) but:
   - does not identify the exact Cloudflare signal being keyed on;
   - does not establish P0 coverage;
   - does not overturn `S1_SOURCE_NOT_VIABLE`;
   - does not create a P1 artifact;
   - does not authorize broader collection, a larger sample, or any subsequent phase.

4. **Curl unavailable, or execution fails before any request (per §4's preflight), or the manifest is missing/invalid/does not reconcile (per §3).**
   Infrastructure/preflight halt. Zero CLOB requests made. No fallback transport is used or authorized.

---

## 10. Guardrails

The following are preserved without exception:

- Research only.
- `named_binary_probe_blocked = true`, unchanged.
- P1 remains blocked.
- P2/P3/probe remain unauthorized.
- `S1_SOURCE_NOT_VIABLE` remains accepted, unreopened.
- No `yes_price`.
- No `1 - price`.
- No `1 - yes_price`.
- No canonical-side-price computation.
- No scoring.
- No wallet discovery.
- No `OrdersMatched`.
- No `log_index`.
- No PnL.
- No trading of any kind (live or paper).
- No gate change.

---

## 11. Non-authorization statement

**Acceptance of this spec, by itself, authorizes NONE of the following:**

- code implementation
- any dependency or Dockerfile change
- any Actor build
- any deployment
- any dry run
- any live run
- any CLOB request
- any Apify request
- any package installation
- **creating or committing the operational manifest file at the path in §3**
- a broader sample of any kind
- a retry of any kind
- a P1 artifact
- any P1/P2/P3/probe/scoring continuation

**Each of the above, at each later stage, requires its own separate, explicit authorization** — spec acceptance is not implementation authorization; implementation (if separately authorized) is not run authorization.

---

## 12. Open design questions for Orchestrator review

Only genuinely undecided implementation-stage questions remain here; the prior version's transport choice, manifest-loading mechanism, manifest authorship, and curl-version byte bound are now pinned above (§2, §3) and accepted (§7.2), not open.

- Whether a future curl-based fetch is implemented as a new module alongside `HttpFetcher` in `live_canary.py`, or as a fully separate Actor/script entry path.
- Whether the existing Apify Actor's container image already includes the system `curl` executable, or would require a Dockerfile change (itself requiring separate authorization per §11).
- Exact implementation mechanics for the bounded temporary file used to capture the response body (§6) — e.g. naming/cleanup discipline — left as an implementation-stage detail.
