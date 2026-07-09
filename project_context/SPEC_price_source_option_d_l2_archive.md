# SPEC — Option D (L2 order-book vendor archive) coverage feasibility — SPEC ONLY

**Type:** SPEC ONLY. Coverage-only feasibility candidate-source review, same falsification posture
as Options A(S1/S1-ALT) / B / C.
**Status:** ACCEPTED / SPEC ONLY. **Patch 1 applied and accepted by Orchestrator** (precision-loss wording split into identifier vs. price-field rules, §2's unproven `/prices-history` provenance claim removed, and §5's temporal range test restated with inclusive lower bound). This document authorizes no execution.
**Scope:** Coverage-only feasibility specification for Option D — PMXT v2 and Telonex L2
order-book/quote vendor archives — as a fourth per-side/token-identity price-source candidate for
the named-binary P1 blocker. No implementation, no tests, no local temporal precheck, no vendor
fetch, no PMXT raw archive download, no Telonex fetch, no vendor account, no API key, no paid
action, no Pass 1, no Pass 2, no price artifact build, no canonical-side price computation, no
P1/P2/P3, no probe execution, no scoring, no wallet work, no OrdersMatched/`log_index`/PnL, no gate
change. `named_binary_probe_blocked` stays `true`.
**Orchestrator decision:** `APPROVE — SPEC ONLY`. This acceptance authorizes only the methodology/specification text. It does **not** authorize implementation, tests, local temporal precheck, vendor/network fetch, account/API/key/paid action, Pass 1, Pass 2, price artifact build, P1/P2/P3 continuation, probe execution, scoring, wallet/OrdersMatched/`log_index`/PnL, gate change, or side synthesis.
**Canonical source:** `rigolugo/pm_research`. Read order followed for this task: `START_HERE.md`,
`project_context/START_HERE.md`, `GUARDRAILS.md`, `PROJECT_STATE.md`, `ARTIFACT_INDEX.md`,
`PRICE_INPUT_CONTRACT_named_binary_probe.md`, `DATA_CONTRACTS_named_binary_probe.md`,
`SPEC_named_binary_probe.md`, `SPEC_price_source_s1_coverage.md`,
`SPEC_price_source_alt_trade_prints.md`, `SPEC_price_source_option_b_data_api_review.md`,
`SPEC_price_source_option_c_onchain.md`, `SPEC_price_source_option_c_onchain_C1R_addendum.md`,
`SPEC_price_source_option_c_artifact_enrichment.md`, `DECISION_LOG.md`, `CLOSED_FINDINGS.md`.
**Canonical precedence:** `rigolugo/pm_research` wins over the public context mirror `rigolugo/pm_research_context`. This document is canonical once committed in the private repo and remains SPEC ONLY.
**Vendor-documentation note:** the PMXT / Telonex facts in §3 were verified read-only against the
vendors' own published documentation pages during drafting
(`archive.pmxt.dev/docs/v2-data-overview`, `telonex.io/datasets`, `telonex.io/docs/schemas/overview`).
This is **documentation review, not vendor fetch**: no archive Parquet file, no dataset row, no API
response, and no authenticated endpoint was retrieved; no account and no API key were used. This
distinction matters under the "No vendor fetch" / "No PMXT raw archive download" / "No Telonex
fetch" constraints below, which this drafting step did not cross.
**Hard boundary — this document does not:** implement code; write or modify tests; run a local
temporal precheck; fetch data from any vendor archive/API; download any PMXT raw archive file;
fetch from Telonex; create or use a vendor account; use an API key; take any paid action; run Pass
1; run Pass 2; build any price artifact; compute any canonical-side price; continue P1/P2/P3;
execute the named-binary probe; compute any score (Brier/log-loss/calibration/reliability/splits);
touch wallets, OrdersMatched, `log_index`, or PnL; change any gate; flip
`named_binary_probe_blocked`; use `yes_price`, `1 - price`, or `1 - yes_price` to unblock
named-binary pricing; or synthesize a missing side price by any other means.

---

## 0. Standing state preserved

This document changes nothing about accepted results; it only proposes where the price-source
search goes next.

- **P0 is accepted (`P0_CLEAR`).** 39,693 P0-eligible non-YES/NO conditions
  (`contract_eligible = 39,957`; `resolved_single_winner = 39,693`;
  `ambiguous_multiple_winners = 253` excluded; `missing_source_rows = 11`).
- **P1 remains BLOCKED** on the proven absence of a per-side/token-identity price input
  (`PRICE_INPUT_CONTRACT_named_binary_probe.md`, S0, accepted).
- **`Store.load_prices()`** exposes only `[condition_id, ts, yes_price]` — one scalar, no
  token/side discriminator.
- **`yes_price` is YES/NO-only** (`price where outcome=="YES" else 1-price`), source-flagged
  **unsafe** for UP_DOWN / OVER_UNDER / NAMED_OTHER.
- **S1 (CLOB `/prices-history`) Pass 1 is an accepted negative** — `S1_SOURCE_NOT_VIABLE`; Level-B
  both-sides coverage cleared 0.95 in no subclass (UP_DOWN 0.38, OVER_UNDER ≈ 0.5204,
  NAMED_OTHER 0.65).
- **S1-ALT (local trade-print reconstruction) Pass 1 is an accepted negative** —
  `S1ALT_SOURCE_NOT_VIABLE`; UP_DOWN 0.26, OVER_UNDER ≈ 0.4082, NAMED_OTHER 0.71.
- **Option B (Data API `/trades`) corrected B0 is an accepted negative** —
  `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`; B1 remains not authorized.
- **Option C (decoded on-chain OrderFilled event tables)** — C0 accepted / spec-only; C1A accepted
  valid halt `C1_ROW_EXPLOSION`; C1A-F1 accepted mixed evidence `C1_CANARY_EXECUTED_NEEDS_REVIEW`;
  C1A-F2 accepted `C1F2_ARTIFACTS_INSUFFICIENT`. Option C is not marked viable; C1 is not
  design-clear; C1B/C2 remain unauthorized.
- **No `yes_price`, `1 - price`, or `1 - yes_price` fallback is permitted** anywhere in this or any
  future stage; no side synthesis by any other means either.
- `named_binary_probe_blocked` stays `true` throughout; P2/P3/probe execution remain unauthorized.

---

## 1. Status / scope / non-authorization

This document is an **ACCEPTED / SPEC ONLY coverage-feasibility spec**. It
identifies PMXT v2 and Telonex L2 order-book/quote archives as a fourth candidate class for the
named-binary P1 per-side price blocker, states what data such an archive would need to provide
(§4), defines what "coverage" would mean for this candidate (§5), and sketches — as design only,
not authorization — a future local-only temporal precheck (§6) and a future bounded vendor coverage
test (§7). It does not select a final vendor, does not run anything, does not touch any local data
beyond what was already read to write this document, and does not touch any vendor data at all
beyond the read-only documentation pages named above.

Nothing in this document authorizes: implementation; tests; a local temporal precheck; a vendor
fetch; a PMXT raw archive download; a Telonex fetch; a vendor account; an API key; a paid action;
Pass 1; Pass 2; a price artifact build; canonical-side price computation; P1/P2/P3 continuation;
probe execution; scoring; wallet work; OrdersMatched/`log_index`/PnL; or a gate change.
`named_binary_probe_blocked` is not flipped by this document.

---

## 2. Why Option D exists after S1 and S1-ALT negatives

`OrientationContract.canonical_side_price(side_0_price, side_1_price)` needs **two per-side
prices**, selected by token identity, never by `1 - price` synthesis
(`PRICE_INPUT_CONTRACT_named_binary_probe.md`). **S1 (`/prices-history`) and S1-ALT (local trade
prints) both failed as sparse point-observation candidates for both-side decision-window density,**
in every subclass, at broadly similar magnitudes (S1: 0.38 / 0.5204 / 0.65; S1-ALT: 0.26 / 0.4082 /
0.71) — consistent with both exhibiting the same sparse-point-observation failure mode for the
decision window. **This document does not claim, and no canonical-repo or official-source proof was
found during this review establishing, that CLOB `/prices-history`'s internal implementation is
itself trade-derived** — that internal-provenance detail is not asserted here either way; only the
*empirically observed, accepted* S1 coverage result is used. Option B (Data API `/trades`) is
separately closed negative on mechanical trust, not merely coverage. Option C's candidate — decoded
on-chain `OrderFilled` event tables — **is** source-documented as a fills-shaped channel (an
`OrderFilled` event exists only when a trade executes, per the accepted OrdersMatched
economic-role work and `DECISION_LOG.md`); even a hypothetical future C1B would inherit the same
"coverage bounded by whether a trade happened to occur near the decision timestamp" ceiling that
sank S1 and S1-ALT, sourced from on-chain fills rather than off-chain trade records or CLOB history.

**Option D's structural motivation is that L2 order-book/quote archives may preserve book state
between trades.** Book state — best bid/ask, and in some feeds full depth — can, in principle, be
recorded (or updated) at a cadence that is not conditioned on a trade having just executed, per
token (`asset_id`), continuously through the archive's operative window. If usable, such a source
could in principle report a per-side price at the decision timestamp (`first_trade_ts + 3600s`)
even when no trade printed near that timestamp — the same sparse-point-observation gap that
produced S1 and S1-ALT's low Level-B density, especially for OVER_UNDER and UP_DOWN. This is why
Option D is proposed as a genuinely different **channel**, not a fourth attempt at the same
trade-print channel under a new
name.

This does **not** presuppose Option D will succeed. Falsification posture unchanged: three prior
candidates failed or remain blocked; Option D is reviewed pessimistically, and it carries its own
likely-fatal weakness up front — both candidate vendors' **operative L2-book history windows start
recently** (PMXT v2: 2026-04-13T19:00:00Z; Telonex L2: 2025-10-11T00:00:00Z) relative to the
project's trade dataset (16,505,185 trades / 288,684 conditions, per `PROJECT_STATE.md`
Environment), so a large share of the 39,693 P0-eligible conditions likely **resolved before either
vendor's window opened** and are structurally out of reach regardless of book-source quality. That
in-range ceiling is exactly what the temporal precheck (§6) exists to measure honestly, cheaply,
and first — before proposing any vendor-side test (mirrors S1's "falsify cheaply, Pass 1 before
Pass 2" discipline).

---

## 3. Vendor scope and source references

### PMXT

- **Candidate is PMXT v2 only.** PMXT's own v2 documentation states v2 was built to fix two
  structural problems in v1: a bloated, poorly-typed schema, and **v1 missing roughly 50% of live
  markets due to incomplete subscription handling**. Using v1 to extend coverage would knowingly
  import a source with a documented, large coverage gap. **PMXT v1 is out of scope and must not be
  silently used to extend coverage; any future PMXT v1 consideration requires separate Orchestrator
  review.**
- **Effective v2 start: 2026-04-13T19:00:00Z** — **[VERIFIED]** against
  `archive.pmxt.dev/docs/v2-data-overview`: "Coverage: starts 2026-04-13T19 UTC."
- **Source shape (documented, verified):** hourly Parquet dumps of the Polymarket CLOB WebSocket
  market-channel event stream, four event types — `book`, `price_change`, `last_trade_price`,
  `tick_size_change` — keyed on `market` (condition id, `fixed_size_binary[66]`) and `asset_id`
  (outcome token id, decimal string), with `timestamp` / `timestamp_received` (ms, UTC). `book`
  events carry `bids`/`asks` JSON depth arrays (~0.031% of rows); `price_change` events carry
  `best_bid`/`best_ask` (`decimal(9,4)`, nullable). Public HTTPS, no credentials required, data
  licensed CC BY 4.0.
- **Reference:** `https://archive.pmxt.dev/docs/v2-data-overview` (schema/coverage — read),
  `https://archive.pmxt.dev/Polymarket` (archive index — named as a source note only; not fetched
  in this drafting pass).

### Telonex

- **Operative L2 order-book/quote start: 2025-10-11T00:00:00Z** — **[VERIFIED]** against
  `telonex.io/datasets`: "Polymarket trades, quotes, order books — from Oct 11, 2025."
- **Telonex separately offers an `onchain_fills` channel "from market inception"** — **[VERIFIED]**
  against the same page. Per `telonex.io/docs/schemas/overview`'s channel table, Polymarket's
  supported channels are `trades, quotes, book_snapshot_5, book_snapshot_25, book_snapshot_full,
  onchain_fills, crypto_prices` — `onchain_fills` is a **distinct channel** from
  `quotes`/`book_snapshot_5`/`book_snapshot_25`/`book_snapshot_full`. **Telonex on-chain fills from
  inception are not L2 book coverage and must not be used to infer decision-time side prices**
  (§8 channel-mismatch guard).
- Telonex requires account/API key for authenticated/paid access; a free-datasets browse path
  exists without one. **No account, API key, cost check beyond public pricing-page text, or paid
  action is authorized here** — any future data pull requires its own separate account/API/cost/ToS
  review, not performed by this document.
- **Schema confirmation status:** the channel catalog (`trades`, `quotes`, `book_snapshot_5/25/full`,
  `onchain_fills`, `crypto_prices`) is confirmed from `telonex.io/docs/schemas/overview`. The
  column-level schema of the `quotes` and `book_snapshot_*` pages specifically
  (`telonex.io/docs/schemas/quotes`, `telonex.io/docs/schemas/book-snapshot`) was **not**
  independently confirmed during this drafting pass — fetch attempts against those exact paths
  returned the docs-overview page content rather than page-specific column tables. This is recorded
  as **[UNVERIFIED — future step]**, not assumed favorable; see §4.
- **Reference:** `https://telonex.io/datasets` (coverage/channel summary — read),
  `https://telonex.io/docs/schemas/overview` (channel catalog — read).

### External references (source notes only, not execution authorization)

- PMXT v2 docs: `https://archive.pmxt.dev/docs/v2-data-overview`
- PMXT archive index: `https://archive.pmxt.dev/Polymarket`
- Telonex datasets page: `https://telonex.io/datasets`
- Telonex schema catalog: `https://telonex.io/docs/schemas/overview`

None of the above constitutes, or is treated as, authorization to download, query, or pull data
from either vendor.

---

## 4. Data required from an L2 archive

For `canonical_side_price` to ever be fed from a vendor L2 archive, the archive must expose all of
the following per queried token at the queried time. Confirmation status reflects only what was
read in this drafting pass — nothing here is measured coverage.

| Required field | Why P1 needs it | PMXT v2 | Telonex L2 |
|---|---|---|---|
| `condition_id` / market | join to the P0-eligible universe | `market` column, `fixed_size_binary[66]`, ASCII `0x`+64 hex — **[DOCUMENTED, verified]** | Polymarket rows presumably carry a market/condition identifier; exact column name **[UNVERIFIED — future step]** |
| `token_id` / `asset_id` | the per-side discriminator `canonical_side_price` needs | `asset_id` column, decimal-string outcome token id — **[DOCUMENTED, verified]** | per-token (`asset_id`) keying not yet confirmed at column level — **[UNVERIFIED — future step]** |
| timestamp | anchor `decision_ts` / `resolved_at` window | `timestamp`, `timestamp_received` (ms, UTC, delta-encoded) — **[DOCUMENTED, verified]** | daily Parquet delivery implied by docs; intra-file timestamp column **[UNVERIFIED — future step]** |
| side / book depth | reconstruct top-of-book or full depth | `bids`/`asks` JSON arrays on `book` events; `side` (`BUY`/`SELL`) on `price_change`/`last_trade_price` — **[DOCUMENTED, verified]** | `book_snapshot_5`/`_25`/`_full` (multi-level depth) + `quotes` (top-of-book) — channel **names** confirmed; column layout **[UNVERIFIED — future step]** |
| best bid / best ask or reconstructable top-of-book | the diagnostic price read needed at `decision_ts` | `best_bid`, `best_ask` (`decimal(9,4)`, nullable, populated on `price_change` events) — **[DOCUMENTED, verified]** | `quotes` channel name implies top-of-book; column-level confirmation pending — **[UNVERIFIED — future step]** |

**PMXT v2's schema is confirmed at the column level** from its own published docs (16-column table,
nullability keyed by event type). **Telonex's schema is confirmed only at the channel-catalog
level** in this pass. A future precheck or test design (§§6–7) must not assume Telonex's
`quotes`/`book_snapshot_*` column layout without first reading
`telonex.io/docs/schemas/quotes` and `telonex.io/docs/schemas/book-snapshot` directly and recording
the verbatim observed schema — the same "documented shape must be confirmed, not assumed" discipline
S1 applied to the CLOB endpoint (`SPEC_price_source_s1_coverage.md` §5).

---

## 5. Coverage definition

- **P0 eligible universe only** — the same 39,693-condition set as S1/S1-ALT; no redefinition of
  eligibility, subclass, or orientation.
- **`decision_ts = first_trade_ts + 3600s`** — identical warm-up policy to S1/S1-ALT
  (`warmup_seconds = 3600`, DATA_CONTRACTS §7); no new decision-timestamp definition is introduced.
- **A condition is in-range for a given vendor iff both `decision_ts` and `resolved_at` are on or
  after that vendor's operative L2-book history start** (inclusive lower bound, open upper bound —
  "present"):
  - **PMXT v2 in-range iff** `decision_ts >= 2026-04-13T19:00:00Z` **and**
    `resolved_at >= 2026-04-13T19:00:00Z`.
  - **Telonex L2 in-range iff** `decision_ts >= 2025-10-11T00:00:00Z` **and**
    `resolved_at >= 2025-10-11T00:00:00Z`.
  A condition whose `decision_ts` or `resolved_at` is before a vendor's start is **not** in scope
  for that vendor's coverage, regardless of any other property. This in-range test is a **separate
  concern from the leakage rule below** — in-range says a timestamp is late enough for the vendor's
  history to plausibly exist at all; leakage says a *specific observation* used for coverage must
  still come from strictly before `resolved_at`.
- **Both side tokens** (`side_0_token`, `side_1_token`, in `outcome_index` order — same enumeration
  basis as S1 §3.1: `trades` distinct `(condition_id, token_id, outcome_index)`, never
  `resolved_winning_token_id`) **must have usable book state before `resolved_at`.** This reuses
  S1's Level A / Level B distinction rather than redefining it: mere existence of a series for a
  token (Level-A analogue) is not sufficient; a usable point in the decision window, strictly
  before `resolved_at` (Level-B analogue), is the binding criterion for a book/quote-shaped source
  exactly as it was for a price-history-shaped one.
- **Leakage discipline unchanged from S1 §4.2, kept separate from the in-range test above:** any
  future book/quote observation counted toward coverage must be strictly before `resolved_at`;
  `resolved_at` bounds the window and is used only to report pre-resolution availability — no point
  at/after resolution ever counts as coverage.

---

## 6. Temporal in-range precheck design (future step — NOT authorized here)

**Design only.** If separately authorized in the future, a local-only, read-only precheck would
compute, for each vendor independently, the fraction of the P0-eligible universe that is **in-range**
per §5's inclusive-lower-bound test — i.e. `decision_ts` and `resolved_at` both on or after that
vendor's operative start — using only already-materialized local artifacts:

- `artifacts/named_binary_probe/p0_preflight.json` (universe, `p0_state == P0_CLEAR` assertion),
- `named_binary_resolution_source_rows.parquet` (`resolved_at`),
- local `trades` via `Store.load_trades()` (`first_trade_ts = min(traded_at)` per condition).

**No vendor fetch, no network call to either vendor, no API key** — this is a local date-range
join over already-accepted local timestamps against two fixed constant date ranges (§5), computed
and reported per subclass and pooled, plus a count of conditions in neither range.

**Purpose:** because both vendor windows open recently (Telonex 2025-10-11, PMXT v2 2026-04-13)
relative to the dataset's apparent full span, most P0-eligible conditions are plausibly resolved
before either vendor's operative start. This precheck exists to measure that **honestly and
cheaply, before** proposing any vendor-side test — mirroring S1's "Pass 1 before Pass 2, falsify
cheaply" gating (`SPEC_price_source_s1_coverage.md` §6). A precheck result showing a negligible
in-range fraction for a vendor is itself a legitimate, reportable negative and would end
consideration of that vendor without ever touching vendor data.

This section defines the design; **it does not authorize running it.** A separate, explicit
in-chat authorization is required before this precheck may be implemented or executed.

---

## 7. Future vendor coverage test design, not authorized

If — and only if — the §6 precheck later shows a non-negligible in-range fraction for a vendor, a
future bounded coverage/trust test (a "D1"-equivalent stage, analogous to S1 Pass 1 or Option C's
C1A) could be proposed as its **own, separately authorized spec**. Recorded now, informationally,
as constraints any such future proposal would need to satisfy — **none of this is authorized or
proposed by this document**:

- **Typed statuses mirroring S1 §4** (Level-A reachability, Level-B decision-window density,
  Level-C integrity spot-check), applied per vendor and per token.
- **Channel-mismatch stops apply throughout** (§8): any future test may query only a vendor's L2
  book/quote channel(s) — PMXT v2's `book`/`price_change` event types; Telonex's
  `quotes`/`book_snapshot_5`/`book_snapshot_25`/`book_snapshot_full` channels — never a
  trades/fills/on-chain-fills channel, to answer a book-coverage question.
- **No price-basis decision is made by such a test.** Best bid, best ask, and mid (if computed) are
  **diagnostics only** — exactly as S1's `p` was recorded as a source-defined diagnostic, never an
  asserted canonical probability. No `canonical_side_price` is computed by any such test.
- **Bounded scope required:** a small, pre-registered, stratified sample — fixed condition list,
  fixed time window, hard row/request caps, fail-fast on cap exceedance — mirroring S1 §6 Pass 1 and
  Option C's C1R fixed-manifest discipline (`SPEC_price_source_option_c_onchain_C1R_addendum.md`
  §3), never a full sweep or an open-ended query.
- **Any account/API key/paid action** needed to run such a test would itself require separate,
  explicit authorization; this document does not request or imply that authorization.

---

## 8. Explicit false-unblock prevention

- **No `yes_price`.**
- **No `1 - price`.**
- **No `1 - yes_price`.**
- **No side synthesis of any kind** — deriving one side's price from the other's, from a label
  flip, or from any transformation not sourced from an actual per-token/per-side observation.
- **No on-chain fills/trades used as an L2 substitute** — Telonex's `onchain_fills` channel, or any
  trade/fill channel from any vendor, is a record of realized transactions, not book/quote state. A
  trade print at time *t* is not evidence of the book at time *t*; substituting it would silently
  reintroduce the exact trade-print-shaped ceiling Option D exists to test past (§2). This is
  precisely the failure mode the channel-mismatch guard below exists to block.
- **No price-source acceptance until later build + audit.** Nothing in this document, the §6
  precheck design, or the §7 test design confers **[ACCEPTED PRICE SOURCE]** status on PMXT v2 or
  Telonex — mirroring S1's explicit rule that acceptance is reached only after a later build + audit
  gate (a hypothetical future "D2" stage, analogous to the Stage 0–4 resolution-source build), never
  by a coverage test alone.

### Required channel-mismatch guard

- **`VENDOR_HISTORY_NOT_L2_BOOK_RELEVANT`** — a typed tag applied to any vendor data channel, field,
  or artifact that is **not** L2 order-book/quote state for the queried token at the queried time
  (e.g., a trades channel, an on-chain fills channel, a metadata/markets-dataset channel, or any
  vendor history from a different data class). Any candidate data source or field must be checked
  against this label before being treated as book-state evidence.
- **`STOP_VENDOR_HISTORY_CHANNEL_MISMATCH`** — the halt any future precheck, test, or build must
  raise on detecting that non-L2-book vendor history (trades, fills, on-chain fills, metadata, or
  any other channel) is being used, or is about to be used, in place of L2 order-book depth. This
  halt is **unconditional**: it applies even if the non-L2 channel has better coverage, longer
  history, or is easier to query than the actual L2 book channel. Coverage convenience never
  justifies a channel substitution.

**Purpose (restated):** to prevent Telonex's `onchain_fills` — available "from market inception,"
i.e., a materially longer history than the `quotes`/`book_snapshot_*` channels' 2025-10-11 start —
or any other older, broader, non-book vendor history, from being quietly substituted for genuine L2
book/quote depth merely because it covers more of the P0 universe. A broader but wrong-channel
source is not a coverage win; it is exactly the channel mismatch this guard exists to block.

---

## 9. Halt states and typed findings

**Document-level status label:**
- `OPTION_D_SPEC_ACCEPTED_SPEC_ONLY` — this document's accepted status. It authorizes no execution and does not unblock P1.

**Candidate-scope findings (this document's own content, §§3–5):**
- `D0_VENDOR_SCOPE_DEFINED` — PMXT v2 and Telonex L2 identified as candidates, with documented
  (PMXT v2) or partially-documented (Telonex) schemas and stated operative-history start dates.
- `D0_SCHEMA_PARTIALLY_UNVERIFIED` — applies to Telonex: channel catalog confirmed; `quotes` /
  `book_snapshot_*` column-level schema not independently confirmed in this pass. Recorded as an
  open item for §§6–7, not as an S1-style measured finding.

**Future-stage halt states** (none triggered by this document; recorded for the design in §§6–7):
- `STOP_P0_NOT_CLEAR` — precheck/test aborts if `p0_preflight.json` is absent or
  `p0_state != P0_CLEAR` (reused from S1 §8.1).
- `STOP_STALE_CONTRACT` — contract/resolution-source version mismatch (reused from S1 §8.2).
- `STOP_TOKEN_ENUMERATION_UNRELIABLE` — token-pair enumeration basis (§5) fails at scale (reused
  from S1 §8.3).
- `STOP_OUT_OF_RANGE_UNIVERSE` — the §6 precheck finds a negligible (pre-registered threshold, to be
  fixed in the precheck's own future spec) in-range fraction for a vendor; that vendor is reported
  `D_VENDOR_NOT_IN_RANGE` and no §7 test is proposed for it.
- `VENDOR_HISTORY_NOT_L2_BOOK_RELEVANT` / `STOP_VENDOR_HISTORY_CHANNEL_MISMATCH` — per §8.
- `STOP_PRECISION_LOSS` — applies to **identifier fields requiring exact identity**: `token_id`,
  `asset_id`, `condition_id`, other large-integer IDs, and any comparable identifier field, if
  mangled, truncated, or rendered in scientific notation anywhere in the pipeline (reused from S1
  §8.4 / `DUNE_DATA_NOTES` §5). This identifier-precision discipline is not weakened by the
  price-field rule below.
- **Price-field validation (separate from `STOP_PRECISION_LOSS`, not an identity stop):**
  price-like fields (`best_bid`, `best_ask`, `p`, mid, or any other observed price value) must be
  parseable, finite numeric values in `[0,1]` where a valid range applies; decimal precision/scale
  should be preserved per the source schema where relevant. **Scientific-notation formatting of an
  ordinary small numeric price value is not, by itself, identifier precision loss** — it is a
  formatting detail of a small finite number, not a mangled or ambiguous identifier. A price field
  that fails to parse as a finite numeric value, or that falls outside a defined valid range where
  one is specified, is `PRICE_FIELD_MALFORMED` (a diagnostic/parse-quality finding on the price
  value itself); it does not by itself trigger `STOP_PRECISION_LOSS`, which remains reserved for
  identifier fields.
- `STOP_LEAKAGE_OR_FORBIDDEN_INFERENCE` — any attempt to read a price at/after `resolved_at`, or any
  `yes_price` / `1 - price` / `1 - yes_price` / side-synthesis attempt (reused from S1 §8.7,
  extended per §8 above).
- `STOP_NOT_AUTHORIZED` — any future precheck or test launched without its own separate, explicit
  in-chat authorization (reused from S1 §8.8). **This applies now:** nothing in this document is
  that authorization.

**Typed vendor-coverage verdicts for a possible future §7 test** (design-only, not emitted by this
document):
- `D1_SOURCE_VIABLE` / `D1_SOURCE_PARTIAL` / `D1_SOURCE_NOT_VIABLE` — mirroring S1 §7.1's
  `S1_SOURCE_VIABLE` / `_PARTIAL` / `_NOT_VIABLE`, applied per vendor, using the same Level-B
  both-sides ≥ 0.95-per-subclass threshold discipline as S1 §7.2 unless a future D1 spec proposes
  and gets a separately pre-registered threshold.

---

## 10. Handoff requirements

- This document has been accepted by Orchestrator as **ACCEPTED / SPEC ONLY**. Acceptance authorizes only this methodology/specification text. It does **not** authorize the §6 precheck or the §7 test design — each remains a separately gated future step requiring its own explicit authorization, per the project's staged-gating discipline (S1 Pass 1 → Pass 2 gating; Option C's C0 → C1 → C1R → C1A → C1A-F1 → C1A-F2 staged pattern).

---

## Guardrails preserved

Research only. This document authorizes no implementation, no tests, no local temporal precheck, no
vendor fetch, no PMXT raw archive download, no Telonex fetch, no vendor account, no API key, no paid
action, no Pass 1, no Pass 2, no price artifact build, no canonical-side price computation, no
P1/P2/P3, no probe execution, no scoring, no wallet work, no OrdersMatched/`log_index`/PnL, no gate
change, and no `yes_price` / `1 - price` / `1 - yes_price` / side synthesis of any kind.
`named_binary_probe_blocked` remains `true`, not flipped. P1 remains BLOCKED. P0 remains accepted /
`P0_CLEAR`. S1 and S1-ALT remain accepted negatives. Option B remains closed negative. Option C
remains not viable / not design-clear. Acceptance of this document is not authorization to run any future step.

**`OPTION_D_SPEC_ACCEPTED_SPEC_ONLY`**
