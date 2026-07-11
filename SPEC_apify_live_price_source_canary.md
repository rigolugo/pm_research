# SPEC — Apify Live Price-Source Canary (CLOB `/prices-history`, 3 Real P0 Conditions)

**Status:** PROPOSED / SPEC ONLY — **NOT YET REVIEWED OR ACCEPTED.** This document authorizes no implementation, no code, no Apify project/build/run, no network call, no full dataset build, no P1/P2/P3/probe, no scoring, no wallet/`OrdersMatched`/`log_index`/PnL, and no gate change. `named_binary_probe_blocked` remains `true` and is not referenced as anything other than a disclaimer term throughout this document.

**Produced by:** Claude (implementation agent), for Orchestrator (ChatGPT) / user review.

**Revision note (this patch):** Orchestrator BLOCKed the prior version pending a schema/identity/status precision patch. This revision, in place, no other scope change:

1. **Token identity confirmation redefined.** The prior version required `token_id_confirmed_in_response`, treating a missing response-body echo as ambiguous. That's wrong for this endpoint shape: single-token `/prices-history` requests are identity-scoped by the request URL itself (`market=TOKEN_ID`, one request per token). §2 now defines `request_token_id`, `request_url_market_param`, `response_body_token_id` (nullable), and a `token_identity_basis` enum (`REQUEST_URL | RESPONSE_BODY | UNCONFIRMED`), with `REQUEST_URL` alone acceptable and a missing response-body echo explicitly **not** a hard-stop by itself.
2. **Output schema split into three row types**, replacing the prior single side-row that mixed both sides' prices into one row: `raw_request_summary_row` (§3.1, one per HTTP request), `parsed_side_candidate_row` (§3.2, one per usable side/token candidate), `condition_pair_summary_row` (§3.3, one per condition — the only row type carrying both sides).
3. **Status taxonomy separated** into `request_classification`, `side_status`, `condition_pair_status`, and the mandatory `disclaimer_label`, each with its own enum (§7), instead of one overloaded set of labels doing all four jobs.
4. **Candidate point selection formalized** (§4): records `window_start_ts`/`window_end_ts`/`fidelity` from the actual request, defines nearest-to-`decision_ts` selection with `signed_gap_seconds`, and a stated earlier-preferred tie-break — still explicitly diagnostic-only, not a P1 price policy.
5. **Hard-stop scoping clarified** (§8): preflight/plan violations abort the whole run before any request; request/parse failures produce a `raw_request_summary_row` and the run continues; one-sided condition outcomes are a `condition_pair_summary_row` fact, never an abort trigger.
6. **Provenance wording cleaned** (§0): kept the factual finding/branch note, removed the informal "hard to fake by accident" phrasing.

No implementation, no Actor file edits, no Apify run, no network call occurred in producing this patch.

---

## 0. Provenance note

**Correction to an earlier claim in this chat:** file 6, `artifacts/named_binary_probe/FINDING_apify_price_canary_dry_run.md`, was initially reported as 404 on the canonical repo; that check only covered `main` and a few common branch-name guesses. The file exists, on branch `apify-price-canary-dry-run`, and has been read in full from that branch. `ARTIFACT_INDEX.md`, `DECISION_LOG.md`, and `PROJECT_STATE.md` on `main` still have no Apify content as of this writing — the branch appears to be pending merge to `main` rather than reflected there yet. The finding's content is consistent with this chat's build: the real-condition dry-run breakdown it reports (`6 clob_prices_history + 24 current-shape = 30 rows`, `dry_run=true` and `disclaimer=APIFY_CANARY_NOT_COVERAGE_EVIDENCE` on every row, no gamma rows because `fetch_gamma_metadata=false`) matches exactly what was built and tested earlier in this chat. Read before writing:

1. `START_HERE.md`
2. `project_context/START_HERE.md`
3. `project_context/PROJECT_STATE.md`
4. `project_context/DECISION_LOG.md`
5. `project_context/ARTIFACT_INDEX.md`
6. `artifacts/named_binary_probe/FINDING_apify_price_canary_dry_run.md` (branch `apify-price-canary-dry-run`)

**What the finding establishes, and what it doesn't:**

- `Decision: ACCEPT FINDING — APIFY_REAL_CONDITION_DRY_RUN_ACCEPTED`. Scope: "documentation-only finding... infrastructure/plumbing evidence only." It authorizes no code change, no Actor change, no Apify run, no network call, no price artifact, no P1/P2/P3/probe, no scoring, no wallet work, no gate change.
- It confirms the placeholder dry-run (33 planned rows, gamma included) and the real-condition dry-run (30 planned rows, gamma off) both executed as designed and produced planned URLs only — no fetched response bodies, no HTTP status, no price values, no historical points.
- Its own §5 "Explicit non-meanings" matches this spec's §9 nearly verbatim: does not validate live endpoint availability or response shape, does not validate coverage, does not produce a price artifact, does not overturn `S1_SOURCE_NOT_VIABLE`, does not unblock P1, does not authorize P2/P3/probe/scoring, does not change any gate.
- Its own §8 "Recommended next step" names exactly this document (`SPEC_apify_live_price_source_canary.md`) as the appropriate next task, spec-only, not authorized to run without separate review.

**The three real P0 conditions**, per the finding's §3 (reference only — see the caveat immediately below):

| Subclass | `condition_id` | `decision_ts` |
|---|---|---|
| UP_DOWN | `0x00001032adc2a18f836a38d7da2ffc1d81cbcf44f9a8b33c9c941fd0a07e2914` | `2026-05-08T05:27:06Z` |
| OVER_UNDER | `0x0087652a603d3384be139ddd86863ec929444c228b5b4d60f65975e521f63928` | `2025-10-31T08:00:16Z` |
| NAMED_OTHER | `0x00037e466770d6f50dea9c86bd61bf51b6e8f1691f01f31c79c5d68478a749b7` | `2025-10-26T04:13:19Z` |

**Caveat — this table is traceability reference only, not an operational input.** §5.1 below still requires the canary to read `condition_id`/`nb_subclass`/`decision_ts`/`side_0_token_id`/`side_1_token_id` from `artifacts/named_binary_probe/apify_price_canary_real_condition_input.json` at runtime, verbatim, every time — never from this table, and never from any other hardcoded copy. Two sources of truth for the same identifiers is a drift risk; the manifest file is the only one that matters operationally. (The table above also omits `side_0_token_id`/`side_1_token_id`, which the finding does not print — another reason the manifest file, not this note, has to be the actual input.)

---

## 1. Relationship to accepted state — read this before the design

CLOB `/prices-history` is not a new candidate endpoint. `SPEC_price_source_s1_coverage.md`'s Pass 1 already coverage-tested this exact endpoint against a 300-condition sample (248 measured) drawn from the full accepted P0 universe, and reached an accepted negative — `S1_SOURCE_NOT_VIABLE` — with Level-B both-sides coverage below 0.95 in every subclass (UP_DOWN 0.38, OVER_UNDER ≈0.5204, NAMED_OTHER 0.65). This result is on `DECISION_LOG.md`'s "DO NOT REOPEN unless explicitly asked" list.

**A 3-condition live canary cannot speak to coverage at all**, in either direction, per this project's own standing discipline (never conclude from one row or a small/uniform sample). This spec therefore scopes the live canary strictly as:

> **An infra/shape/reachability check**: can a live Apify-hosted fetch retrieve a response from CLOB `/prices-history` that is structurally usable (timestamped, numeric, in-range, identity-traceable) for 3 specific, already-selected real conditions — nothing about what fraction of the P0 universe this would work for.

Every output row and every run-level summary this canary could ever produce carries the mandatory `APIFY_LIVE_CANARY_NOT_P1_EVIDENCE` disclaimer label (§7.4), and this spec forbids the canary from ever emitting any label resembling "coverage clear," "source viable," "S1 overturned," or similar — those verdicts are Orchestrator/user judgment calls after manual review, not something code emits.

`yes_price`, `1 - price`, and `1 - yes_price` remain forbidden for `UP_DOWN` / `OVER_UNDER` / `NAMED_OTHER`, per the accepted S0 finding (`PRICE_INPUT_CONTRACT_named_binary_probe.md`) and the standing guardrails. Nothing in this design computes, derives, or stores a synthesized price of any kind.

---

## 2. Token identity confirmation

For single-token `/prices-history`, the request is inherently identity-scoped: one request, one token, via `market=TOKEN_ID`. The response body is not required to echo the token id back for identity to be considered confirmed. Every request-scoped row carries:

| Field | Meaning |
|---|---|
| `request_token_id` | The token id used to build this specific request, taken verbatim from the manifest (`side_0_token_id` or `side_1_token_id`). |
| `request_url_market_param` | The exact value placed in the URL's `market=` query parameter for this request — should equal `request_token_id`; recorded separately so a URL-construction bug would show up as a mismatch rather than being silently assumed correct. |
| `response_body_token_id` | Nullable. Populated only if the response happens to include an identifiable token/market field. Frequently `null` for this endpoint — that is expected, not an error. |
| `token_identity_basis` | `REQUEST_URL` \| `RESPONSE_BODY` \| `UNCONFIRMED`. |

**Rules:**

- `REQUEST_URL` is an **acceptable** basis for this canary on its own — one request per token, via the request's own `market=` parameter, is sufficient identity confirmation. This is the default/expected value for the large majority of rows.
- If `response_body_token_id` is present and matches `request_token_id`, basis may be recorded as `RESPONSE_BODY` (strictly stronger evidence than `REQUEST_URL` alone) — but this is a bonus, never a requirement.
- **A missing `response_body_token_id` is not a hard-stop by itself**, and does not by itself demote `token_identity_basis` away from `REQUEST_URL`.
- `token_identity_basis = UNCONFIRMED` is reserved for the narrow cases where identity is genuinely in doubt: the request URL's `market=` parameter cannot be tied back to the manifest's `request_token_id` for this row (e.g. a construction bug, or `request_url_market_param != request_token_id`), **or** `response_body_token_id` is present but **conflicts** with `request_token_id`, **or** request/response bookkeeping for this row is otherwise ambiguous (e.g. the row can't be matched back to a specific planned request). This is the only condition that produces `side_status = UNCONFIRMED_TOKEN_ID` (§7.2).

---

## 3. Output schema — three row types

The prior single-row schema (one row per side, carrying that side's price) is replaced. No row type below ever contains both `side_0_price` and `side_1_price` except `condition_pair_summary_row` (§3.3), which exists precisely to be the one place that pairing is visible.

### 3.1 Row type A — `raw_request_summary_row`

One row per **actual HTTP request made** (mandatory + any optional schema-comparison requests, per §5), regardless of outcome, including hard-stopped ones. Fields:

| Field | Meaning |
|---|---|
| `row_type` | `"raw_request_summary_row"` |
| `run_id`, `request_id` | Run + per-request identifiers. |
| `condition_id`, `nb_subclass` | Echoed from the manifest. |
| `side` | `0`, `1`, or `null` for a non-side-scoped call (none expected in this design — every planned request is side-scoped). |
| `endpoint` | `clob_prices_history` (mandatory) or `clob_book`/`clob_price`/`clob_midpoint`/`clob_spread` (optional, §5.3). |
| `request_token_id`, `request_url_market_param` | Per §2. |
| `request_url_actual` | The full URL actually fetched. |
| `window_start_ts`, `window_end_ts`, `fidelity` | The actual `startTs`/`endTs`/`fidelity` used in this request (null/NA for current-endpoint requests, which don't take a window). |
| `http_status` | Raw HTTP status code. |
| `response_byte_length` | Byte length of the raw response. |
| `raw_point_count` | Count of points in the raw response before any filtering. |
| `raw_response_excerpt` | First N bytes/points only, bounded — never the full raw blob. |
| `response_body_token_id` | Per §2, nullable. |
| `token_identity_basis` | Per §2. |
| `fetched_at` | ISO8601 UTC. |
| `request_classification` | One of the five values in §7.1. |
| `disclaimer_label` | Always `APIFY_LIVE_CANARY_NOT_P1_EVIDENCE` (§7.4). |

### 3.2 Row type B — `parsed_side_candidate_row`

One row per side/token where a candidate point was actually extracted (numeric, timestamped, in `[0,1]`) from a `clob_prices_history` request — including cases where `token_identity_basis = UNCONFIRMED`, so that doubtful rows are recorded and flagged rather than silently dropped. Never produced for a request that returned no usable point (that request's outcome lives only on its `raw_request_summary_row`), and never produced for a current-endpoint schema-comparison request (§5.3). Fields:

| Field | Meaning |
|---|---|
| `row_type` | `"parsed_side_candidate_row"` |
| `run_id`, `condition_id`, `nb_subclass` | As above. |
| `side` | `0` or `1`. |
| `token_id` | `= request_token_id` for this side, echoed. |
| `decision_ts` | Echoed from the manifest. |
| `candidate_price` | The selected candidate's numeric value (§4). Diagnostic only — never `canonical_side_price`. |
| `candidate_source_ts` | Timestamp of the selected point. |
| `signed_gap_seconds` | `candidate_source_ts - decision_ts`, signed (§4). |
| `point_selection_method` | Fixed constant describing the selection rule used (§4) — self-documenting on the row. |
| `side_status` | One of the five values in §7.2. Expected to be `PRESENT` or `UNCONFIRMED_TOKEN_ID` for any row of this type (a row only exists here because *some* candidate was parsed). |
| `schema_matches_documented`, `price_in_range_0_1`, `timestamp_parseable` | Parse/audit flags (bool). |
| `is_synthesized` | Always `false`, hardcoded — a structural guarantee, not a live check, that nothing here was computed via `1 - price` or similar. |
| `disclaimer_label` | Always `APIFY_LIVE_CANARY_NOT_P1_EVIDENCE`. |

### 3.3 Row type C — `condition_pair_summary_row`

One row per condition (exactly 3 for a complete run). This is the **only** row type that contains both sides together. Fields:

| Field | Meaning |
|---|---|
| `row_type` | `"condition_pair_summary_row"` |
| `run_id`, `condition_id`, `nb_subclass` | As above. |
| `side_0_token_id`, `side_1_token_id` | Echoed from the manifest. |
| `side_0_price_candidate`, `side_1_price_candidate` | Nullable — populated from the corresponding `parsed_side_candidate_row` if one exists for that side, else `null`. Diagnostic only. |
| `side_0_source_ts`, `side_1_source_ts` | Nullable, from the same source. |
| `side_0_status`, `side_1_status` | One of the five `side_status` values (§7.2) each — `EMPTY`/`ERROR`/`PARSE_BLOCKED` sides have no candidate row but still get a status here, derived from that side's `raw_request_summary_row`. |
| `condition_pair_status` | One of the three values in §7.3. |
| `disclaimer_label` | Always `APIFY_LIVE_CANARY_NOT_P1_EVIDENCE`. |

This row is still diagnostic only. It is not a P1 artifact, and it does not compute or imply `canonical_side_price`.

---

## 4. Candidate point selection (diagnostic only)

For any `clob_prices_history` request that returns ≥1 point, before any candidate is selected the canary records:

- `window_start_ts`, `window_end_ts` — the actual `startTs`/`endTs` used in the request.
- `fidelity` — the actual `fidelity` parameter used.

**Selection rule:** among all returned points, select the single point whose timestamp is nearest to `decision_ts` (minimizing absolute time difference). This is diagnostic point selection for shape inspection only.

- `candidate_source_ts` = the timestamp of the selected point.
- `signed_gap_seconds` = `candidate_source_ts - decision_ts` (signed: positive = after `decision_ts`, negative = before).
- **Tie-break:** if two or more points are equidistant from `decision_ts`, prefer the **earlier** (smaller) timestamp. This spec does not otherwise justify a different tie-break; a future revision could, with explicit reasoning, but this canary always uses earlier-preferred by default.
- `point_selection_method` is recorded as a fixed constant (e.g. `"nearest_ts_prefer_earlier_on_tie"`) on every `parsed_side_candidate_row`, so the method is self-documenting on the row itself, not only in this spec text.

**This does not define an accepted decision-price policy.** It exists only so the canary can report *a* candidate value for shape/diagnostic inspection. `candidate_price` cannot be used by P1, or by any downstream step, without a later, separately accepted price-selection build spec with its own audit.

---

## 5. Live canary scope

### 5.1 Input: the existing real-condition manifest, not a fresh selection

The canary's **only** condition-selection input is the file already specified and (if authorized and run) produced by the accepted real-condition manifest generator:

```
artifacts/named_binary_probe/apify_price_canary_real_condition_input.json
```

The canary must:
- **Read this file as-is.** It must not re-run selection logic, re-query the classification contract/resolution parquet/trades, or derive any new condition.
- **Hard-stop the entire run, before any request** if the file is missing, is not valid JSON, does not contain exactly a `conditions` array, or that array does not contain exactly 3 entries covering exactly `{UP_DOWN, OVER_UNDER, NAMED_OTHER}` (one each). No substitution, no padding, no re-selection.
- Use `condition_id`, `nb_subclass`, `decision_ts`, `side_0_token_id`, `side_1_token_id` from that file verbatim. No slug is used (`fetch_gamma_metadata` stays `false` in that file and stays irrelevant here — see §5.4).

### 5.2 Mandatory fetch: CLOB `/prices-history`, single-market form only

For each of the 3 conditions, for each side (`side_0_token_id`, `side_1_token_id`): one `GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...` request, using the same single-market URL construction already validated in the dry-run Actor's `validation.py` (§0). This is **6 mandatory requests**, fixed.

`POST /batch-prices-history` (or any batch form) is **not used** — same correction already applied to the dry-run Actor, for the same reason: current Polymarket docs do not clearly document it.

### 5.3 Optional: current-endpoint schema comparison — bounded, and only for shape, never for decision price

Optionally, the canary may additionally call current-state endpoints (`/book`, `/price`, `/midpoint`, `/spread`) **strictly to compare today's response schema against the documented shape** — never to stand in for a historical/decision-time price, and never contributing to a `parsed_side_candidate_row`. If included:

- Limit to **one side per condition** (e.g., `side_0_token_id` only) and **one endpoint** (`/book`, the richest shape for comparison) = 3 additional requests.
- Any request of this kind produces a `raw_request_summary_row` with `request_classification = APIFY_LIVE_CANARY_CURRENT_ONLY_NOT_HISTORICAL` (§7.1) and **never** produces a `parsed_side_candidate_row`.
- This is optional; the canary is complete and valid with **zero** current-endpoint calls (6 total requests) or with this comparison included (9 total requests). Both fit the request cap below.

### 5.4 No Gamma

`fetch_gamma_metadata` stays unused in this canary. Gamma metadata lookup adds a request family with no bearing on the price-shape question this canary asks, and no slug is available without inventing one (forbidden). If a future need for Gamma arises, it requires a separate, explicit justification in a revised spec — not a default inclusion here.

### 5.5 Hard global request cap

**Hard cap: 12 requests total for the entire canary run.** The mandatory path uses 6; the optional schema comparison (§5.3) uses at most 3 more (9 total) — both comfortably under the cap. If any future revision of this spec wants more, that increase must be explicitly justified in-document and still hard-capped; it is not open-ended. The canary must refuse to start (hard-stop, zero requests made) if its own configured request plan would exceed 12.

---

## 6. Required outputs

1. **`raw_request_summary_row`** (§3.1) — one per actual HTTP request made (6–9, per §5), for every request regardless of outcome, including hard-stopped ones.
2. **`parsed_side_candidate_row`** (§3.2) — one per side/token where a usable candidate point was extracted. Never present for a request with no usable point. Never present for a current-endpoint-only request (§5.3).
3. **`condition_pair_summary_row`** (§3.3) — exactly one per condition (3 for a complete run), the only row type combining both sides.
4. **Explicitly forbidden in any output:**
   - No synthesized price of any kind.
   - No `yes_price`.
   - No `1 - price` / `1 - yes_price`.
   - No `canonical_side_price` computation — this canary produces *candidate* per-side prices only; turning them into a canonical price is a separate, not-yet-authorized build step with its own audit requirements.
   - No P1 artifact. Output must not be written under any path that could be mistaken for a P1 feature-assembly artifact. Recommended output location: `artifacts/named_binary_probe/apify_live_canary/` (a new, clearly-separate subfolder), never inside a path implying P1 acceptance.

Every row of every type, and the run-level summary, carries `disclaimer_label = "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE — infra/shape diagnostic only; does not update S1_SOURCE_NOT_VIABLE, does not establish coverage, does not unblock P1"`.

---

## 7. Status taxonomy

Four separate, purpose-scoped enums — not one overloaded label set.

### 7.1 `request_classification` (on every `raw_request_summary_row`)

| Label | Meaning / trigger |
|---|---|
| `APIFY_LIVE_CANARY_USABLE_SHAPE` | The request succeeded (HTTP 200), returned ≥1 point, the nearest-to-`decision_ts` point is timestamped, numeric, and in `[0,1]`. Request-level only — says nothing about the other requests/sides/conditions. |
| `APIFY_LIVE_CANARY_EMPTY_HISTORY` | The endpoint was reachable (HTTP 200, schema otherwise fine) but returned zero points for the requested window/token. |
| `APIFY_LIVE_CANARY_ENDPOINT_ERROR` | HTTP failure (4xx/5xx), timeout, connection error, or a response that isn't valid JSON at all. |
| `APIFY_LIVE_CANARY_PARSE_BLOCKED` | A response was received but its shape doesn't match the documented contract closely enough to parse into points, or the structure is ambiguous in a way not covered by the other labels. Fail loud here — no guessed field mapping. |
| `APIFY_LIVE_CANARY_CURRENT_ONLY_NOT_HISTORICAL` | This request was one of the optional current-state schema-comparison calls (§5.3) — current-state data, never treated as historical/decision-time. |

### 7.2 `side_status` (on `parsed_side_candidate_row` and rolled up into `condition_pair_summary_row`)

| Label | Meaning |
|---|---|
| `PRESENT` | A usable candidate was extracted and token identity is `REQUEST_URL`- or `RESPONSE_BODY`-confirmed. |
| `EMPTY` | That side's mandatory `clob_prices_history` request returned zero points. |
| `ERROR` | That side's request hard-failed (HTTP/connection/timeout). |
| `PARSE_BLOCKED` | A response was received but could not be parsed into a usable point. |
| `UNCONFIRMED_TOKEN_ID` | A candidate point was extracted, but §2's narrow unconfirmed-identity conditions applied — recorded, not discarded, but not counted as `PRESENT` for pairing purposes (§7.3). |

### 7.3 `condition_pair_status` (on `condition_pair_summary_row` only)

| Label | Meaning |
|---|---|
| `BOTH_SIDES_PRESENT` | `side_0_status == PRESENT` and `side_1_status == PRESENT`. |
| `ONE_SIDED_ONLY` | Exactly one side is `PRESENT`; the other is `EMPTY`/`ERROR`/`PARSE_BLOCKED`/`UNCONFIRMED_TOKEN_ID`. Never treated as a usable pair. |
| `BOTH_SIDES_MISSING_OR_BLOCKED` | Neither side is `PRESENT`. |

### 7.4 `disclaimer_label` (on every row of every type, and the run summary)

| Label | Meaning |
|---|---|
| `APIFY_LIVE_CANARY_NOT_P1_EVIDENCE` | Mandatory, unconditional, on every row and the run summary — not a competing technical classification. States plainly that nothing in this canary's output, including a full `BOTH_SIDES_PRESENT` result on all 3 conditions, is P1 evidence, coverage evidence, or an S1 reversal. |

---

## 8. Hard-stop scoping

Three distinct scopes, not one blanket rule:

- **Preflight/plan violations abort the whole run, before any request is made.** This covers: the manifest file missing/invalid/wrong-shape (§5.1), and a configured request plan that would exceed the 12-request cap (§5.5). Zero requests are made in these cases.
- **Request/parse failures produce a `raw_request_summary_row` and the run continues to the next planned request.** This covers HTTP failures, empty history, parse-blocked responses, and current-only responses to historical requests (§7.1) — each is recorded with its classification and the canary proceeds to the next side/condition/request in the plan rather than aborting. The entire point of the canary is to observe outcomes across exactly these 3 conditions; an early full-abort on the first failure would defeat that. *(This per-request continuation is a deliberate design choice, unchanged from the prior version and flagged again here for Orchestrator confirmation — the alternative, whole-run-abort-on-first-failure, remains defensible and could be substituted before implementation if preferred.)*
- **Condition-level one-sided or missing-pair outcomes are never an abort trigger.** They are summarized honestly in `condition_pair_summary_row`'s `condition_pair_status` (§7.3) and are never treated as a usable pair — but observing a `ONE_SIDED_ONLY` or `BOTH_SIDES_MISSING_OR_BLOCKED` condition does not stop the canary from completing diagnostics for the remaining conditions.

In every case: no output row is silently dropped. A hard-stopped request/side still gets a `raw_request_summary_row` (§3.1) documenting exactly what happened.

The eight required hard-stop triggers, mapped to the new taxonomy:

| Hard-stop condition | → Result |
|---|---|
| HTTP failure (4xx/5xx/timeout/connection error) | `request_classification = APIFY_LIVE_CANARY_ENDPOINT_ERROR`; `side_status = ERROR` |
| Empty history for a given side | `request_classification = APIFY_LIVE_CANARY_EMPTY_HISTORY`; `side_status = EMPTY` |
| One-sided only (one side usable, the other not, after both requests complete) | No abort. `condition_pair_status = ONE_SIDED_ONLY` on that condition's `condition_pair_summary_row`; never treated as a usable pair |
| No timestamped points in an otherwise-200 response | `EMPTY_HISTORY` (if genuinely zero points) or `PARSE_BLOCKED` (if points exist but lack usable timestamps) |
| Ambiguous response shape (doesn't match documented contract) | `request_classification = APIFY_LIVE_CANARY_PARSE_BLOCKED`; `side_status = PARSE_BLOCKED` |
| Price missing / non-numeric / out of `[0,1]` range | `PARSE_BLOCKED` on both `request_classification` and `side_status` |
| Response cannot be tied to the requested `token_id` (per §2's narrow rule — not merely a missing `response_body_token_id`) | `token_identity_basis = UNCONFIRMED`; `side_status = UNCONFIRMED_TOKEN_ID` on the `parsed_side_candidate_row` if a point was otherwise parseable, else `PARSE_BLOCKED` |
| Endpoint returns current-only data for a historical request | `request_classification = APIFY_LIVE_CANARY_CURRENT_ONLY_NOT_HISTORICAL`; no `parsed_side_candidate_row` emitted — this must never silently substitute for a missing historical point |

---

## 9. Interpretation rules

- A successful 3-condition canary (even `BOTH_SIDES_PRESENT` on all 3) only proves that live endpoint shape/availability worked for **those 3 specific conditions, at that specific moment**. It is a mechanical reachability/shape observation, not a statistical claim.
- **It does not establish P0 coverage.** 3 conditions is not a sample; no coverage rate, confidence interval, or generalization follows from it, per this project's own "never conclude from one row or a small/uniform sample" discipline.
- **It does not overturn `S1_SOURCE_NOT_VIABLE`.** That result is accepted, sampled (n=300, 248 measured), and on the DECISION_LOG "DO NOT REOPEN" list. A 3-condition live check cannot re-derive or re-litigate it in either direction.
- **It does not unblock P1.** `named_binary_probe_blocked` stays `true`. P1 remains blocked on the absence of an accepted per-side/token-identity price source; this canary produces candidate diagnostic rows, not an accepted source.
- **It only authorizes consideration of** — not automatically triggers — a later, separately authorized, statistically meaningful sampled coverage spec (comparable in scale to S1/S1-ALT, i.e. on the order of the accepted 300-condition sample, not 3 conditions) if the Orchestrator/user judges the shape results promising enough to warrant that larger, separate effort.

---

## 10. Implementation Not Authorized

This section is required and controlling, regardless of anything else in this document.

- This spec authorizes **no implementation**: no `.actor/` files, no `src/` code, no test files, no request-building code, no parsing code — nothing beyond this markdown document.
- This spec authorizes **no Apify project creation, build, or run** of any kind.
- This spec authorizes **no network call** — not a test call, not a single-request smoke test, not a "just checking the endpoint responds" call. Zero.
- This spec authorizes **no full dataset build**, no P1/P2/P3/probe step, no scoring, no wallet/`OrdersMatched`/`log_index`/PnL work, and no gate change. `named_binary_probe_blocked` stays `true`, untouched.
- **Any future code change implementing this design requires separate Orchestrator review** before it is written — this spec being accepted does not itself authorize drafting `main.py` or any other file.
- **Any future Apify live run requires separate, explicit user authorization**, distinct from and in addition to Orchestrator review of the implementation. Orchestrator-approved code does not imply permission to run it; running it against live Polymarket infrastructure is its own explicit go/no-go decision for the user to make.
- Even after a live run (if ever separately authorized), its results must be reviewed and interpreted per §9 before any further step is proposed — the run's own output never self-labels a coverage or viability verdict.

---

## Standing consequence

This document, by itself, changes nothing about the project's current state:

- `S1_SOURCE_NOT_VIABLE` stands, unreopened.
- P1 remains BLOCKED.
- `named_binary_probe_blocked` remains `true`.
- No Apify Actor code exists as a result of this spec (the dry-run Actor referenced in §0 was separately authorized and delivered earlier; this spec does not modify it).
- No network call, of any kind, to any Polymarket/Gamma/CLOB/Apify endpoint has occurred as part of producing this document.

If accepted as SPEC ONLY, the only next possible step — pending separate explicit authorization for *each* stage — is: (1) Orchestrator review of an implementation matching this design, then, separately, (2) explicit user authorization to actually run it live.

---

## Claude-to-Orchestrator handoff

**Task:** Patch `SPEC_apify_live_price_source_canary.md` per the Orchestrator's schema/identity/status precision block — six numbered items (see Revision note at top), no other scope change.

**Read before writing:** Same five canonical files as the prior version, plus the located `FINDING_apify_price_canary_dry_run.md` on branch `apify-price-canary-dry-run` (§0) — no re-fetch was needed for this patch since no new factual claim about repo state was being made; the patch is a design-precision revision of the prior spec's own content.

**Produced:** revised `SPEC_apify_live_price_source_canary.md` — SPEC ONLY. No code, no Actor file edits, no Apify run, no network call.

**What changed:** all six items from the BLOCK decision, applied as described in the Revision note. Nothing outside those six was touched: §1 (relationship to S1), §9 (interpretation rules), §10 (Implementation Not Authorized), and Standing Consequence are unchanged in substance from the prior version.

**Flag for Orchestrator:** (1) the finding branch still doesn't appear reflected in `main`'s canonical files — unchanged from before, worth confirming when it merges; (2) §8's per-request continuation-on-failure remains a flagged design choice, not a unilateral decision — same flag as the prior version, carried forward since this patch didn't change that judgment call, only clarified its scoping in writing.

**Not authorized by this handoff:** any implementation, any Apify action, any network call, any P1/P2/P3/probe step, any gate change. `named_binary_probe_blocked` remains `true`, untouched, referenced only as a disclaimer term.

**File delivery only** — not a commit, not an acceptance. Awaiting Orchestrator/user review.
