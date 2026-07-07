# SPEC — Option C (on-chain / decoded OrderFilled event tables) per-side price source — Revision 3

**Type:** SPEC ONLY. Falsification-minded candidate-source review.
**Status:** ACCEPTED / SPEC ONLY (Revision 3). **Authorizes nothing further.** No implementation,
no network/RPC/API call, no data run, no backfill, no scoring, no probe, no gate change.
`named_binary_probe_blocked` stays `true`. No `yes_price` / `1 - price` / `1 - yes_price` / `1 - p`
/ side synthesis anywhere.
**Authorization basis:** explicit in-chat "ACCEPT FINDING — Option C Revision 3 is accepted as
SPEC ONLY." This document records that acceptance. It is Revision 3 of the Option C review; this
document does not restate or re-derive the content of Revisions 1–2, which were reviewed and
superseded outside this record — only the final accepted Revision 3 content is recorded here.
**Canonical precedence:** `rigolugo/pm_research` wins over this document.

---

## 0. Where Option C sits in the price-source search

Three per-side/token-identity price-source candidates have now been reviewed for the named-binary
P1 blocker (`OrientationContract.canonical_side_price` needs two per-side prices; local
`Store.load_prices()` exposes only a single YES/NO-only `yes_price` scalar — accepted S0 finding,
`PRICE_INPUT_CONTRACT_named_binary_probe.md`):

- **Option A / S1-ALT** — local trade-print reconstruction via `Store.load_trades()`. **CLOSED
  NEGATIVE** (`S1ALT_SOURCE_NOT_VIABLE`, accepted sampled Pass 1: UP_DOWN 0.26, OVER_UNDER 0.4082,
  NAMED_OTHER 0.71 — none clears the 0.95 both-sides bar).
- **Option B** — Polymarket Data API `/trades`. **CLOSED NEGATIVE** (corrected B0 diagnostic,
  accepted: `OVERLAP_API_LOCAL_MISMATCH = 7`, `OVERLAP_PAGINATION_PARTIAL = 3`,
  `OVERLAP_MATCHED = 0` of 10 manifest conditions — Data API `/trades` mechanical trust was not
  established).
- **Option C** — **this document.** On-chain reconstruction via **bounded, already-decoded
  Dune/vendor OrderFilled event tables** (the same general class of decoded-event Dune
  infrastructure already validated elsewhere in this project — e.g. the accepted OrdersMatched
  economic-role work, `MAKER_PAIRING_VALIDATED`, and the accepted CTF resolution source,
  `ctf_evt_conditionresolution`). Option C is **not** raw RPC log-fetching or a new on-chain
  decoder; it proposes reusing existing decoded event tables as a data source, the same way the
  project already reuses `ctf_evt_conditionresolution` for outcomes.

Same falsification posture as Options A and B: this spec does not assume Option C will work. Two
prior local/local-adjacent price-source candidates already failed; Option C is one of a shrinking
set of remaining candidates, reviewed pessimistically.

---

## 1. C0 — candidate/source-interface verification (accepted scope)

**C0 selects bounded decoded Dune/vendor OrderFilled event tables as the Option C candidate.**

C0 is **source-interface / spec verification only** — it is the same kind of preliminary step as
Option B's spec-only review before any B0 pilot: confirming what the candidate source *is* and
what its *shape* would need to be, without running anything.

C0, as accepted, establishes only:

1. **Candidate identity.** The decoded OrderFilled event (CTF Exchange, `topic1=orderHash,
   topic2=maker, topic3=taker` — settled per `DECISION_LOG.md`) as exposed through existing
   decoded Dune/vendor tables, is the specific candidate under review for Option C. This is a
   *source selection*, not a coverage claim.
2. **Bounded framing.** Any future use of this candidate must remain **bounded** — condition-
   scoped, sample-scoped, call/row-capped — following the same discipline already required of
   Option A and Option B (accepted specs' R-series requirements: composite identity, no
   `tx_hash`-alone matching, proven-not-assumed pagination completeness, typed schema/precision
   halts, no side synthesis).
3. **No coverage claim, no run.** C0 does not measure coverage, does not query Dune, does not
   touch local data, and does not produce any artifact beyond this spec record. It is explicitly
   **not** a B0-equivalent pilot.

C0 authorizes nothing beyond having identified the candidate and the bounding discipline it would
need to satisfy. It does not authorize C1.

---

## 2. C1 — GUARDRAIL BLOCKED (the local-tx_hash scoping trap)

**C1 (a bounded coverage/trust pilot analogous to Option B's B0) is currently GUARDRAIL BLOCKED.**
No safe bounded sample design has been found that resolves the following dilemma. Both branches
of it are blocking, not merely difficult:

### 2.1 Branch 1 — local `tx_hash` scoping

If a C1 pilot samples the decoded OrderFilled event tables **by first collecting `tx_hash` values
already present in the local trades store**, then queries the decoded event tables for exactly
those transactions:

- This is **structurally the same shape as S1-ALT (Option A)**, which is already closed negative.
  Reconstructing per-side prices from decoded events for transactions the local store *already
  has* does not test anything S1-ALT did not already test — it is very likely to reproduce the
  same negative result via the same underlying data, not a genuinely different observation.
- More fundamentally: **this design cannot test for missing coverage by construction.** If the
  local store is missing trades entirely (the H1 hypothesis that motivated looking beyond Option
  A/B in the first place), a sample built from the local store's own `tx_hash` list can never
  surface those missing trades — it only ever looks at what local already knows about. A
  seemingly-clean result from this branch would be a **non-result** for the actual question
  (does a broader source recover coverage local is missing?), exactly the kind of confound this
  project's falsification discipline exists to catch (cf. Option B spec's H1/H2 framing).

### 2.2 Branch 2 — independent condition/time-window event querying

If instead a C1 pilot queries the decoded OrderFilled event tables **independently of any
local `tx_hash` list** — by `condition_id` and/or time window, to actually surface trades local
may be missing:

- This requires querying the on-chain event stream by market/time criteria rather than by a
  pre-known, bounded transaction list. That is structurally **event reconstruction over a
  market/time axis** — the same shape of work as building a broad event indexer, differing only
  in scale, not in kind.
- This risks the **"No full indexer"** absolute constraint (`GUARDRAILS.md`) even at a
  seemingly-small pilot scale, because the risk is in the *querying pattern* (open-ended
  condition/time-scoped event retrieval), not merely in the row count. A "just 10 conditions"
  pilot built this way is still indexer-shaped work, not a bounded reconciliation test in the
  sense Option A/B's accepted specs used the term.

### 2.3 Why this is a spec-level block, not an empirical one

Options A and B were tested and closed on **empirical** grounds (measured coverage/mechanical
trust came back negative). Option C's C1 is blocked at the **design** level: no sample
construction has been identified that (a) is capable of testing the actual open question (does a
broader on-chain source recover missing coverage?) and (b) stays within the bounded,
non-indexer-shaped discipline every prior candidate test in this project was held to. Until a
third design resolves this — neither reproducing Option A's already-negative shape nor tripping
into indexer-shaped querying — C1 does not have a safe bounded form to authorize, and no C1 pilot
is proposed.

This is recorded as a **guardrail block**, not a negative coverage result. Option C is **not**
closed by this spec; C0 (candidate selection) stands accepted, and C1 remains an open design
problem, not a closed candidate.

---

## 3. What would need to be true for C1 to become proposable (informational only)

Recorded for future reference; **none of this is authorized or proposed by this document**:

- A sampling design that can surface local-missing trades **without** first depending on a local
  `tx_hash` list (resolving Branch 1), **and**
- A query pattern bounded tightly enough (condition-scoped, capped calls/rows, no open-ended
  time-range or wildcard event retrieval) that it does not read as indexer-shaped work under the
  project's existing "No full indexer" constraint (resolving Branch 2), **and**
- The same composite-identity, pagination-completeness, and no-side-synthesis discipline the
  accepted Option A/B specs already require, carried over unchanged.

Any such design would be a **fresh, separately authorized SPEC-ONLY document** (a hypothetical
"C1 spec"), reviewed with the same falsification posture as this one. Nothing here proposes,
sketches, or pre-authorizes that design.

---

## 4. Guardrails preserved by this spec

Research only. This document authorizes nothing: no implementation, no network/RPC/API call, no
data run, no broad backfill, no full indexer, no Pass 2, no S2, no P1/P2/P3, no probe, no scoring,
no wallet/OrdersMatched-expansion/`log_index`/PnL, no gate change, no `yes_price`/`1 - price`/
`1 - yes_price`/`1 - p`/side synthesis. `named_binary_probe_blocked` stays `true`. P1 remains
BLOCKED on the absence of an accepted per-side/token-identity price source. Delivery is not
acceptance beyond what was explicitly approved in-chat; the user commits this to
`C:\b1\pm_research` at their discretion.

---

## 5. Decisions recorded as resolved at acceptance

1. **Accepted.** Status is ACCEPTED / SPEC ONLY (Revision 3); authorizes nothing further.
2. **C0 (candidate/source-interface selection) is accepted scope.** Decoded Dune/vendor
   OrderFilled event tables, bounded, are the identified Option C candidate. No coverage claim,
   no run, no artifact beyond this record.
3. **C1 (bounded coverage/trust pilot) is GUARDRAIL BLOCKED**, for the reasons in §2: local
   `tx_hash` scoping cannot test missing coverage and likely reproduces S1-ALT; independent
   condition/time-window querying risks indexer-shaped work. This is a design-level block, not an
   empirical negative, and does not close Option C.
4. **No implementation follows** from this acceptance. A future C1 design, if any, requires a
   separate, freshly authorized SPEC-ONLY document.
5. **Standing consequences unchanged:** P1 remains BLOCKED; B1 (Option B) remains unauthorized;
   P2/P3/probe remain unauthorized; `named_binary_probe_blocked` remains `true`.
