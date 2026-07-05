# SPEC — Option B (Polymarket Data API `/trades`) per-side price source — SPEC-ONLY REVIEW

**Type:** SPEC ONLY. Falsification-minded review + bounded test design.
**Status:** Draft for Orchestrator review. **Authorizes nothing.** No implementation, no network
call, no data run, no backfill, no scoring, no probe, no gate change. `named_binary_probe_blocked`
stays `true`. No `yes_price` / `1 - price` / `1 - yes_price` synthesis anywhere.
**Authorization basis:** spec-only Option B review, explicitly authorized in-chat; this is the one
"next possible task" the canonical mirror README and `project_context/START_HERE.md` permit.

---

## 0. Provenance & verification caveats (read first)

This spec was written against canonical context read this session, but not all of it could be
re-fetched from canonical source on the turn it was written. Stated plainly so the Orchestrator
can decide what to re-verify before acting:

- **Verified by direct fetch this turn:** `rigolugo/pm_research_context` README (the public
  mirror). Confirms P0 accepted, P1 blocked on per-side/token-identity price input, P2/P3/probe
  unauthorized, wallet discovery blocked, "next possible task, only if explicitly authorized, is a
  SPEC-ONLY price-source build plan," and the no-`yes_price`/`1 - price`/`1 - yes_price` rule.
- **Verified earlier this session** from the Drive sync copy the user confirmed is identical to
  the pushed GitHub content: `project_context/START_HERE.md` branch state (S1 and S1-ALT closed
  negative; Option B is a permitted spec-only candidate; no implementation).
- **NOT re-fetched this turn (GitHub robots wall blocks subfolder trees + raw redirects), so
  treated as UNVERIFIED and flagged inline below:** `GUARDRAILS.md`, `PROJECT_STATE.md`, the exact
  prior Option-B spec text, and the `Store` / `load_trades()` data contract
  (`DATA_CONTRACTS_*` / `PRICE_INPUT_CONTRACT_*`). Every place this spec depends on one of those
  is marked **[UNVERIFIED — cross-check canonical]**.
- **Canonical precedence:** the private `rigolugo/pm_research` repo wins over anything here. Where
  this spec and the private repo disagree, the private repo is correct and this spec must be
  amended.

This spec deliberately does not restate any API field values, endpoint parameters, or rate limits
as fact. The prior Option-B feasibility spec already recorded those from the official Polymarket
docs; this review does not re-assert them from memory. Any concrete API shape claim must be
re-read from `docs.polymarket.com` immediately before any future authorized run
**[UNVERIFIED — cross-check canonical]**.

---

## 1. What Option B is, and why it is only a candidate

**Option B** = use the Polymarket **Data API `/trades`** endpoint as a per-side / token-identity
price source, **gap-fill only** — i.e. to fill per-condition price coverage that the local
backfill (Option A and its S1/S1-ALT variants) did not achieve, **not** to become a new primary
indexer.

It is a *candidate* because the price-input line for named-binary P1 is blocked: P1 needs per-side
(token-identity-resolved) prices, and the local sources tried so far closed negative. Option B is
one of a small, shrinking set of remaining candidate sources. It is **not** presumed to work.

### 1.1 The falsification frame — two competing hypotheses

The prior negative results (Option A / S1-ALT: measured per-subclass coverage far below the 0.95
threshold) admit **two mutually exclusive explanations**, and this spec refuses to assume which is
true:

- **H1 — Local backfill is incomplete.** The trades exist upstream; the local store simply didn't
  capture them. If H1 holds, a *different retrieval path* (Option B) could raise coverage.
- **H2 — The trading was genuinely one-sided / sparse.** For the affected conditions, the
  underlying market genuinely had little or no two-sided, token-identity-resolvable trading. If H2
  holds, **no** retrieval path can manufacture coverage that never existed — Option B would fail
  for the same reason Option A did: the Data API `/trades` path would not supply two-sided,
  token-identity-resolvable observations for those conditions. That would close the Option B
  candidate on this evidence, but any different future candidate source would require a fresh,
  separately authorized spec. Option C/on-chain reconstruction remains out of scope by current
  guardrails.

The Option A failure pattern is **at least as consistent with H2 as with H1.** This spec is
explicitly pessimistic: it treats H2 as the live default and designs the test to *try to falsify
H2*, not to confirm H1. A result that merely "looks better" without distinguishing H1 from H2 is a
**non-result**.

### 1.2 What would make Option B viable (the bar, stated up front)

Option B clears the bar **only** if a bounded pilot shows, on ground already known to be
two-sided, that the API is *mechanically trustworthy* (§4 Phase B0), **and then** that it supplies
genuine, correctly-identified extra coverage on the gap set (§4 Phase B1) — and even then, a full
build is gated on a favorable **full Pass-1 coverage** result, not a favorable pilot (§6). Anything
short of that leaves Option B rejected and the per-side price line where it is now.

---

## 2. Reconciliation identity — the core correctness requirement

**Requirement R1 (composite trade identity).** A trade returned by the API MUST NOT be matched to
a local trade on `tx_hash` alone. A single on-chain transaction can contain multiple distinct
fills (e.g. one taker order filling against several maker orders), so `tx_hash` is **not** a unique
trade key. Matching MUST use a composite identity:

> `tx_hash` **+** token identity (`asset` / `token_id`) **+** `outcome_index` **+** `side`
> **+** `price` **+** `size` **+** `timestamp`, to the extent each is available and precision-safe.

**Requirement R2 (one-to-one pairing).** Reconciliation MUST pair each API row to at most one
local row and vice versa. Once a local row is consumed by a match, it MUST NOT be reused to
"absorb" a second API row. (The failure this guards against: two API rows sharing a `tx_hash`
both matching one local row and being counted as two clean matches — a false 100% reconciliation.)

**Requirement R3 (ambiguity is a counted mismatch, never a clean match).** If rows share a
`tx_hash` but cannot be uniquely paired on the full composite identity, each unpaired row MUST be
recorded as a **counted ambiguity/mismatch** (e.g. `TX_HASH_AMBIGUOUS`), surfaced in the
reconciliation report. It MUST NOT be silently promoted to a match, and MUST NOT be dropped.

**Acceptance evidence for R1–R3 (test-design level, not implementation):**
- A reconciliation over a *known two-sided* condition where two API rows share a `tx_hash` and
  only one local row shares it MUST NOT yield `matched_count = 2` with zero mismatch. The correct
  outcome is one match + one counted ambiguity (or two ambiguities), never two clean matches.
- A case with two genuinely-distinct local rows sharing a `tx_hash` MUST be able to match both,
  proving R2 does not over-reject legitimate multi-fill transactions.

**Explicit non-goal / guardrail:** reconciliation compares values for agreement only. It MUST NOT
transform a price, MUST NOT derive one side from the other, and MUST NOT compute `yes_price`,
`1 - price`, `1 - p`, or `1 - yes_price` anywhere. A disagreement is reported, not "fixed."

---

## 3. Retrieval completeness — pagination must be proven, not assumed

**Requirement R4 (bounded pagination with proven completeness).** `/trades` has no server-side
time-range parameter **[UNVERIFIED — cross-check canonical / re-read docs]**, so per-condition
history is retrieved by pagination under a hard page cap. The cap MUST be enforced pre-flight
(a page that would exceed the cap is never fetched), AND completeness MUST be *proven*, not
inferred from "the loop ended."

- Completeness is proven **only** by observing a short/empty final page (fewer rows than the page
  limit), which demonstrates no further page exists.
- If the **last allowed page is full**, the retrieval is **not** complete. It MUST be marked
  `PARTIAL_RETRIEVAL` (typed status/halt), and that condition's API set MUST NOT be reconciled as
  if complete. A possibly-truncated set silently treated as complete would fabricate a false
  coverage/agreement number — exactly the H1/H2 confound this project must avoid.

**Acceptance evidence for R4 (test-design level):**
- Exactly-full final page ⇒ result flagged `PARTIAL_RETRIEVAL`; not counted as complete.
- Short final page ⇒ result flagged complete.
- Over-cap pagination ⇒ stops at the cap and flags `PARTIAL_RETRIEVAL`, never runs unbounded.

---

## 4. Bounded two-phase test design (each phase separately authorized)

Neither phase below is authorized by accepting this spec. Each requires its own explicit
authorization. No autonomous escalation: B0 passing does not authorize B1; B1 passing does not
authorize a full Pass 1.

### 4.1 Phase B0 — mechanical-trust reconciliation pilot (on KNOWN-good ground)

**Purpose:** before touching any gap, test whether `/trades` is *mechanically trustworthy* on
conditions the local store already measured as two-sided (`DECISION_PRICE_BOTH_SIDES`)
**[UNVERIFIED — confirm the exact decision label in canonical Option A output]**.

**Design constraints (spec-level):**
- **Pre-registered, provenance-attested sample:** a fixed list of ~10–20 conditions drawn from
  Option A's accepted `BOTH_SIDES` rows. The list MUST carry an explicit provenance attestation
  proving it came from that accepted set; a template/placeholder list MUST be rejected at runtime,
  not silently accepted.
- **Condition-scoped calls only:** query by condition/market identity only. No `eventId`, no
  `user`, no unscoped/wildcard/broad market queries.
- **Hard caps:** ≤ ~100 total calls for the phase; ≤5 pages/condition; a bounded per-call `limit`.
  Caps enforced pre-flight and never raisable above the spec ceiling by configuration.
- **`takerOnly` cardinality probe:** on a handful of the pre-registered conditions, retrieve with
  `takerOnly` true and false and record the row-count delta, to resolve whether the endpoint
  returns one row per trade or one row per taker fill (the direct analogue of the
  OrdersMatched-vs-OrderFilled row-cardinality lesson). This is a *measurement*, recorded, not an
  assumption.
- **Reconciliation checks (per §2, §3, §5):** condition/token identity, `outcome_index`
  normalization, timestamp-unit detection, price numeric validity/range, `tx_hash`
  presence/matching, composite-identity pairing, pagination completeness.
- **Outputs:** reconciliation-only artifacts (JSON + Markdown summaries, per-condition CSV,
  API↔local mismatch ledger). **No price series. No writes to any `prices/` path.**

**B0 pass condition:** the API reconciles cleanly against known-good local data (identities line
up, no unexplained schema/precision drift, pagination proven complete or honestly flagged partial,
`takerOnly` cardinality understood). B0 is a trust test, not a coverage test — it produces **no**
coverage verdict.

### 4.2 Phase B1 — gap-coverage pilot (gated on B0)

**Gate:** B1 may be proposed **only if** B0 passed **and** B0 produced genuine `API_HAS_EXTRA`
evidence (the API demonstrably carries correctly-identified rows the local store lacks, on known
ground). Absent that, H2 is not yet falsified and B1 is not justified.

**Design constraints (spec-level):**
- Sample: ~30–50 conditions drawn from Option A's `ONE_SIDE` / `NEITHER` gap set.
- Same reused, already-trusted (Level-B) reconciliation logic from B0. Same caps discipline
  (bounded calls, ≤5 pages/condition, condition-scoped only).
- **Purpose:** measure whether the API supplies genuine, correctly-token-identified *extra*
  two-sided coverage on the gap set — i.e. whether H1 (fixable gap) or H2 (genuinely one-sided)
  is the better-supported explanation for each gap condition.
- Still far short of a full 300-condition Pass 1; explicitly a pilot.

**B1 pass condition:** the API supplies genuine, correctly-identified extra coverage that
materially moves gap conditions toward the per-side threshold **without** any forbidden inference
or side synthesis. A result where "extra" rows are duplicates, mis-identified, or only appear via
disallowed transforms is a **fail**, and supports H2.

---

## 5. Schema, precision, and typing requirements (falsification hygiene)

**Requirement R5 (typed numeric parsing inside validation).** `price`, `size`, and `timestamp`
MUST be converted/validated inside the schema-validation path, returning typed values. A
non-numeric string, `NaN`, `inf`, or an unsupported timestamp unit MUST produce a typed
schema-deviation halt (`STOP_SCHEMA_DEVIATION`), never a raw uncaught `ValueError` surfacing
downstream. Test-design evidence: `price='abc'`, `size='abc'`, `timestamp='abc'`, `price='NaN'`,
`price='inf'` each yield `STOP_SCHEMA_DEVIATION`.

**Requirement R6 (identifier precision guards).**
- **Token identity (`asset` / `token_id`)** MUST be string-safe / canonical-int-safe. A
  scientific-notation representation (e.g. `1.23e+76`) or a float-typed token id MUST be treated
  as `STOP_PRECISION_LOSS` — a 76–78-digit id cannot survive a float round-trip. This mirrors the
  project's existing `outcome_index` / `token_id` precision-split lesson.
- **`outcome_index`** MUST normalize only safe `0` / `1` representations (int `0/1`, or the exact
  strings `'0'`,`'1'`,`'0.0'`,`'1.0'`); anything else (`'0.5'`, out-of-range, non-numeric, bool)
  is a schema deviation.
- **`condition_id`** MUST retain canonical `0x`+64-hex form; a malformed id is a schema deviation.
- Test-design evidence: local `token_id='1.23e+76'` ⇒ `STOP_PRECISION_LOSS`; float `token_id`
  ⇒ `STOP_PRECISION_LOSS`; `outcome_index='0.0'` ⇒ normalizes to `0`; invalid `outcome_index`
  ⇒ schema deviation; malformed `condition_id` ⇒ schema deviation.

**Requirement R7 (schema drift halts, never adapts).** Missing required fields, unexpected field
types, or a response for the wrong condition MUST halt with a typed schema-deviation, not be
worked around. The pinned response shape MUST be re-read from `docs.polymarket.com` immediately
before any authorized run **[UNVERIFIED — cross-check canonical]**; documented placeholder fields
(historically: `asset` format, `price` units/range, `timestamp` units) MUST be empirically
resolved on the tiny known sample in B0 before any count is trusted.

---

## 6. Typed halt conditions (minimum set) and no-autonomous-escalation

Any authorized run MUST implement at least these typed halts. A halt stops the phase; it is never
downgraded to a warning:

- `STOP_NOT_AUTHORIZED` — missing explicit run authorization or external-host confirmation.
- `STOP_CALL_BUDGET_EXCEEDED` — would exceed the phase call ceiling.
- `STOP_SAMPLE_SCOPE_EXCEEDED` — off-list condition, bad sample size, or template/placeholder or
  provenance-failed condition list.
- `STOP_PAGINATION_UNBOUNDED` — page cap would be exceeded / full final page (`PARTIAL_RETRIEVAL`).
- `STOP_RATE_LIMIT_HIT` — HTTP 429 / rate-limit signal; halt, no retry loop.
- `STOP_SCHEMA_DEVIATION` — missing/mistyped field, wrong-condition response, bad numeric parse.
- `STOP_PRECISION_LOSS` — identifier precision unsafe (float/scientific-notation token id, etc.).
- `STOP_FORBIDDEN_INFERENCE` — any attempt to synthesize a side or use a forbidden transform.
- `STOP_NO_WRITE_PATH` — any attempt to write a price series or touch a `prices/` path.

**No autonomous escalation (explicit):** B0 passing does not authorize B1; B1 passing does not
authorize a full Pass 1; nothing here reaches Pass 2, S2, P1/P2/P3, the probe, scoring, backfill,
wallet/OrdersMatched/`log_index`/PnL, or a gate change. Each step is a separate authorization.

---

## 7. Environment / `Store(root)` note (for any future authorized run)

The canonical environment is **project path `C:\b1\pm_research`, data path `C:\b1\data`**. For any
future authorized run, `Store(root)` is expected to take the **data** root (`C:\b1\data`), because
`load_trades()` reads the local trades dataset, not the project tree
**[UNVERIFIED — confirm against `Store` source and the accepted data contract before any run]**.
This is a spec note only; nothing here runs `Store`.

---

## 8. What a favorable result would (and would not) justify — the build gate

- A favorable **B0** justifies *only* proposing B1. It does not justify any build.
- A favorable **B1** justifies *only* proposing a full Option-B Pass-1 coverage evaluation under
  separate authorization. It does not justify a build.
- A build spec for Option B is justified **only** by a favorable **full Pass-1 coverage** result
  — the same build-gate the project already applies to S1 / S1-ALT (favorable *full* coverage, not
  a favorable *pilot*).
- A **negative or ambiguous** result at any phase supports H2 for Option B and closes the Data API
  `/trades` candidate on this evidence. Any further candidate source would require a fresh,
  separately authorized spec. Option C / on-chain reconstruction remains out of scope by current
  guardrails.

---

## 9. Guardrails preserved by this spec

Research only. This document authorizes nothing. No implementation, no network/API call, no data
run, no broad backfill, no full indexer, no Pass 2, no S2, no P1/P2/P3, no probe, no scoring, no
wallet/OrdersMatched/`log_index`/PnL, no gate change, no `yes_price`/`1 - price`/`1 - yes_price`
synthesis. `named_binary_probe_blocked` stays `true`. Delivery is not acceptance; the user commits
this to `C:\b1\pm_research` at their discretion after Orchestrator review.

---

## 10. Decisions requested from the Orchestrator

1. Accept / reject / amend this spec-only review.
2. Confirm the H1/H2 pessimistic framing (§1.1) is the right way to set expectations.
3. Cross-check the four **[UNVERIFIED]** items (§0) against canonical `GUARDRAILS.md`,
   `PROJECT_STATE.md`, the prior Option-B spec, and the `Store` / price-input data contract —
   especially the `Store(root)` = data-root assumption (§7) and the `/trades` schema/rate-limit
   details (§3, §5, §7).
4. If (and only if) accepted, whether to separately authorize **Phase B0** (still requires its own
   explicit authorization even after spec acceptance).
