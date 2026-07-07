# SPEC ADDENDUM — Option C, C1R (bounded condition/time-window event-query design) — SPEC ONLY

**Type:** SPEC ONLY. Doc-only design addendum. Falsification-minded review, same posture as
Revision 3.
**Status:** PROPOSED FOR REVIEW — **Patch 1 applied** (selector-manifest gap closed per Orchestrator
BLOCK feedback). Not yet accepted by the Orchestrator. This document itself authorizes nothing — it
is a design writeup for review, not an execution authorization.
**Revision note (Patch 1):** The prior draft of this addendum treated `token_id`/`asset_id` mapping
as fully derived and out of scope for C1A. The Orchestrator correctly identified this as a blocking
gap: decoded `OrderFilled` rows are asset/token-keyed, not `condition_id`-keyed, so a future C1A
query defined only by `condition_id` + time window would be underspecified — it would not state
what field the query actually filters on. **Patch 1 adds a required C1A selector manifest (§4)**
that resolves this by requiring the two side `token_id`s per condition as a **static identity**
input, validated before any future query, never computed from outcome-conditioned sources. This
patch does not change §1 (C1R is design-only), does not change the source preference (§2), and does
not authorize anything beyond what the pre-patch draft authorized (i.e., nothing — see §9).
**Relationship to prior spec:** This is an addendum to `SPEC_price_source_option_c_onchain.md`
(Revision 3). It does not replace, restate in full, or silently reverse Revision 3. Revision 3's C0
acceptance and its record of the C1 guardrail block (§2, Branches 1 and 2) stand unchanged as
history. This addendum introduces a new, distinct design — C1R — proposed as a candidate resolution
to that guardrail block. It is not itself C1 execution.
**Authorization basis for this addendum's existence:** explicit in-chat instruction, this chat and
the prior turn in this thread: "OPTION_C_C1_BOUNDED_EVENT_QUERY_DESIGN — SPEC ONLY" /
"APPROVE — Option C continuation authorized as SPEC ONLY," which explicitly authorizes *analysis
and design writing only* and explicitly reverses the prior "C1 closed by default" posture **only
for the purpose of producing this SPEC-ONLY document**. The Orchestrator's follow-up "BLOCK — revise
C1R addendum, DOC PATCH ONLY" instruction authorizes this patch, again as **doc-only**. Neither
authorizes C1A execution, C1B sampling, C2 code/tests, or any data run — see §9.
**Canonical precedence:** `rigolugo/pm_research` wins over this document. This document is not
canonical until an Orchestrator handoff records it as accepted, and even then it remains SPEC ONLY.

---

## 1. C1R is design-only

C1R ("C1 Revised") is a **design-only** re-examination of whether a bounded condition/time-window
OrderFilled event query can be constructed that:

(a) is actually capable of testing the open question Revision 3 identified — whether a broader
on-chain source can recover coverage that local `Store.load_trades()` is missing — which requires
**not** depending on a local `tx_hash` list to build the sample (this is what made Branch 1 in
Revision 3 §2.1 a non-result by construction), and

(b) does not become indexer-shaped work under the "No full indexer" absolute constraint
(`GUARDRAILS.md`), which is what made Branch 2 in Revision 3 §2.2 a guardrail risk.

C1R is **not** an execution plan. Nothing in this document queries Dune, calls an API, touches
local data, or produces a data artifact. C1R defines a *design* that, if separately authorized
step by step (C1A, then C1B), would need to be executed to actually test coverage. This document
stops at the design.

---

## 2. Safest source candidate

Consistent with Revision 3 §0 and §1 (C0), the preferred candidate source for any future C1A/C1B
work remains:

- **Preferred:** bounded, already-decoded Dune/vendor OrderFilled event tables — the same class of
  decoded-event infrastructure already validated elsewhere in this project (the accepted
  OrdersMatched economic-role work, `MAKER_PAIRING_VALIDATED`; the accepted CTF resolution source,
  `ctf_evt_conditionresolution`). This reuses existing decoded tables; it does not add a new
  decoder and does not touch raw logs directly.
- **Not preferred, requires separate justification and separate authorization:** direct RPC or
  archive-node log scanning. Nothing in this document proposes RPC/archive scanning. If a future
  design ever needed it, that would require its own SPEC-ONLY review and its own explicit
  authorization — out of scope here and not assumed.

This preference exists because bounded decoded-table querying is a *read against an existing,
already-decoded dataset with a WHERE clause*, not log-level event reconstruction — the same
distinction Revision 3 §0 drew between Option C and "a new on-chain decoder."

---

## 3. Canary C1A (design parameters, not an execution)

If C1A is separately authorized in the future, it would be bounded as follows. These are design
parameters, recorded now so any future authorization request is evaluated against a concrete,
already-reviewed shape rather than an open-ended one.

- **Condition count:** 3–5 fixed conditions, maximum. Not a "starter batch" that could grow inside
  the same authorization — a hard, named ceiling.
- **Condition selection:** fixed `condition_id` values, listed in the C1A authorization request
  itself (not selected dynamically at run time).
- **Time window:** fixed decision-time windows per condition, explicit start/end timestamps chosen
  in advance. No open-ended or wildcard time range.
- **Row caps:** a hard per-condition row cap and a hard global row cap, both fixed numbers set in
  the C1A authorization request, bounded above by the ceilings in §7.
- **Fail-fast on row explosion:** if any per-condition or global cap would be exceeded, the pilot
  halts immediately with `C1_ROW_EXPLOSION` rather than truncating silently.
- **Output:** coverage diagnostics only. No price series, no `canonical_side_price`, no scoring
  input.

The 3–5 condition ceiling and fixed-window design are deliberately tighter than Option B's B0
diagnostic (10-condition manifest), because C1A tests a **new query pattern** and the discipline
calls for proving the pattern safe at the smallest useful scale first — no request to go larger is
implied or pre-approved by this document.

---

## 4. C1A selector manifest requirement (Patch 1 — closes the token/condition scoping gap)

Decoded `OrderFilled` rows are keyed by asset/token (`makerAssetId`, `takerAssetId`), not by
`condition_id`. A C1A design that only names `condition_id` + time window is underspecified: it
does not say what field the query filters on. **Any future C1A authorization request must include
a per-condition selector manifest**, listing, for each of the 3–5 fixed conditions:

| Field | Description |
|---|---|
| `condition_id` | The fixed condition under test. |
| `side_0_token_id` | Full-precision, string-safe `token_id` for `outcome_index = 0`. |
| `side_1_token_id` | Full-precision, string-safe `token_id` for `outcome_index = 1`. |
| `outcome_index_0` | `"0"` — recorded explicitly for auditability, not inferred at query time. |
| `outcome_index_1` | `"1"` — recorded explicitly for auditability, not inferred at query time. |
| `window_start_utc` | Fixed decision-time window start. |
| `window_end_utc` | Fixed decision-time window end. |
| `per_condition_row_cap` | Hard cap for this condition, ≤ the §7 ceiling. |
| `global_row_cap` | Hard cap across all conditions in the manifest, ≤ the §7 ceiling. |
| `source table/version` | The specific decoded Dune/vendor OrderFilled table + version to be queried. |

No C1A authorization is complete without this manifest, fully populated, for every condition in
scope. A manifest row missing any field is not a partial authorization — it is not an
authorization at all for that condition.

### 4.1 Selector mapping is static identity only

The two `token_id`s per condition are a **static identity lookup**, not a computation performed at
query time and not a step that produces any price, target, or scoring artifact:

- **Basis.** The selector manifest **may reuse/adapt the accepted S1 token-pair enumeration
  discipline** (`SPEC_price_source_s1_coverage.md` §3.1): the primary enumeration basis is
  **distinct local `(condition_id, token_id, outcome_index)`** tuples from `trades` (`DATA_CONTRACTS`
  §5, `TRADES_COLS`). This is the same accepted basis S1 used, not a new one invented for C1R.
- **Validation, not assumption.** Before any future query, the manifest-population step must
  validate that each of the 3–5 selected conditions yields **exactly two distinct, stable,
  string-safe** side `token_id`s — one per `outcome_index ∈ {0, 1}` — stable across the condition's
  local trades, string-safe per the project's `canonical_int` discipline (78-digit range, fail loud
  on scientific notation — `DUNE_DATA_NOTES` §5). This mirrors S1's "candidate, not assumed valid"
  posture (`SPEC_price_source_s1_coverage.md` §3.1) exactly; it is not a new discipline, it is the
  existing one applied to a new (still-unexecuted) design.
- **Scope limit.** This static lookup produces exactly two `token_id` strings per condition and
  nothing else. It must **not** compute side price, canonical price, target, score, or any probe
  feature. It is an identity manifest, not a pricing or labeling step.
- **Forbidden source.** The selector manifest must **not** use `resolved_winning_token_id`
  (`DATA_CONTRACTS` §2) as the pair source. That field is a single, outcome-conditioned winner
  label — using it to build or validate the two-sided pair would leak the outcome into the
  selector itself, exactly the failure mode `SPEC_price_source_s1_coverage.md` §3.1 already forbids
  for the identical reason. `resolved_winning_token_id` may only ever be used downstream, in a
  separately authorized later stage, as a winner label — never to construct or check the side pair.

This subsection intentionally does not introduce a new enumeration method. It binds C1R to the
same static, outcome-independent, already-accepted identity discipline the project already uses,
so the selector manifest is bounded by precedent rather than by a fresh judgment call.

---

## 5. Required fields (source-level, retrieved as-is)

If a future C1A pilot is authorized and executed, the following fields would be retrieved directly
from the decoded event source, unmodified:

- **Event table / source** — the specific decoded Dune/vendor table name and version queried
  (must match the manifest's `source table/version`, §4).
- **Contract** — which CTF Exchange contract instance the event was decoded from (per the settled
  `topic1=orderHash, topic2=maker, topic3=taker` decode, `DECISION_LOG.md`).
- **`tx_hash`** — retrieved as a field, but per §8 below, never used alone as a matching key.
- **`block_time`**.
- **Ordering key, if already source-provided** — e.g. a vendor-provided `evt_index` or equivalent,
  used only if the decoded table already exposes it; this design does not construct or infer an
  ordering key the source does not already provide.
- **`makerAssetId`**.
- **`takerAssetId`**.
- **`makerAmountFilled`**.
- **`takerAmountFilled`**.
- **Source provenance** — which table/query/vendor version produced the row, so results remain
  attributable and reproducible.

These are retrieved as the source expresses them. No transformation, unit conversion, or
side-assignment happens at this stage. The **only** identity input consumed from outside the raw
event row itself is the selector manifest's two side `token_id`s (§4), used purely as a filter
value — not merged, joined, or blended into the row's own fields.

---

## 6. Separate: derived fields (not part of C1A retrieval)

The following remain explicitly **derived**, out of scope for C1A itself, listed here for design
clarity — to show where raw retrieval stops and interpretation would begin in any later phase:

- `outcome_index` **as applied to a retrieved row** (the manifest records `outcome_index_0`/`_1`
  as static labels for the two selector tokens, §4 — but C1A does not derive or attach an
  outcome_index to individual retrieved event rows beyond echoing which of the two manifest tokens
  matched).
- Side identity beyond "matched `side_0_token_id`" or "matched `side_1_token_id`" as a raw filter
  match (i.e., no interpretation of what that means for price or outcome).
- Canonical side price (`OrientationContract.canonical_side_price`).
- Any price, target, or scoring computation whatsoever.

C1A, as designed in §3–§5, retrieves the §5 fields for rows where `makerAssetId` or `takerAssetId`
equals one of the manifest's two side tokens, and compares row presence/absence against local
`Store.load_trades()` for the same fixed conditions/windows. Any future phase that computes the
above would be a distinct, separately authorized step (§9), not an automatic continuation of C1A.

---

## 7. Future C1A query shape (explicit, bounded)

If C1A is separately authorized, its query shape is fixed as follows — this section constrains
what a future C1A authorization is allowed to ask for, not what is being run now:

- **Source:** decoded OrderFilled table only (§2). No other event table.
- **Time bound:** fixed `block_time` window per condition, taken from the selector manifest
  (`window_start_utc`/`window_end_utc`, §4). No open-ended range.
- **Filter:** rows where `makerAssetId` **or** `takerAssetId` is in the fixed two-token selector
  pair for that condition (`side_0_token_id`, `side_1_token_id`, §4). This is an asset/token-keyed
  filter, matching how the source is actually keyed.
- **No native `condition_id` assumption.** The query does not assume or require the decoded event
  table to expose a `condition_id` column. `condition_id` is a local/manifest-side label used only
  to organize the 3–5-condition manifest and to compare results back against local data — it is
  never asserted to exist as a queryable field on the event table itself.

### 7.1 Absolute C1R-level cap ceilings

To avoid leaving row caps entirely to a later prompt, this addendum fixes **ceiling** values that
any future C1A authorization must stay at or under:

- **Per-condition row cap ceiling: 2,000 rows.** A future C1A authorization may set an equal or
  lower per-condition cap; it may not set a higher one without a fresh addendum revision.
- **Global row cap ceiling: 6,000 rows** (i.e., not simply 5 × 2,000 — the global ceiling is set
  below the naive product to keep the pilot small even if multiple conditions approach their
  per-condition cap simultaneously). A future C1A authorization may set an equal or lower global
  cap; it may not set a higher one without a fresh addendum revision.
- These ceilings are deliberately small relative to Option B's accepted 25,000-row B0 ledger cap,
  because C1A is a new, unproven query pattern being tested at the smallest useful scale — not a
  pattern with existing empirical trust.

---

## 8. How this design avoids the blocked shapes

Revision 3 identified two blocking branches (§2.1, §2.2) plus other standing prohibitions. C1R,
with the selector manifest (§4) and fixed query shape (§7), is designed to avoid all of them:

- **Local-`tx_hash`-only reproduction of S1-ALT (Revision 3 Branch 1).** C1A's sample is defined by
  fixed `condition_id` + fixed time window + fixed token-pair selector (§4) — **not** derived from,
  or filtered through, any `tx_hash` list already present in local `Store.load_trades()`. C1A can,
  in principle, surface event rows the local store does not have for the same condition/window/
  token pair — the entire point of testing coverage, and the exact capability Branch 1 could never
  have by construction.
- **Full event indexing / broad block scans.** No time range is open-ended; no condition or token
  pair is chosen dynamically at query time; there is no "all conditions" or "all time" mode. The
  3–5 condition ceiling, fixed windows, fixed token-pair filters, and hard row caps with fail-fast
  (§3, §7.1) keep this a small, enumerable, one-shot query against a bounded set.
- **Broad block scans specifically.** This design queries a decoded event **table** (§2, §7), not
  raw block ranges or logs. No block-height iteration appears anywhere in this design.
- **OrdersMatched expansion.** OrdersMatched is not part of this design. C1A queries OrderFilled
  only, per the existing settled decode (`DECISION_LOG.md`).
- **Wallet discovery.** No wallet, maker/taker address cohort, or address-level aggregation is
  computed or retrieved beyond the raw asset-id/amount fields already present in the event row
  (§5). No wallet list is produced or consumed.
- **PnL / scoring / probe.** C1A produces coverage diagnostics only (§3, §6). No
  `canonical_side_price`, no Brier/log-loss/calibration metric, no probe input, no forecast-vs-price
  comparison.
- **Outcome leakage into the selector itself.** §4.1 forbids `resolved_winning_token_id` as a pair
  source, so the selector manifest cannot smuggle outcome information into which rows get queried.

This design still involves condition/time-window querying, independent of local `tx_hash` — the
general shape Revision 3's Branch 2 flagged as a risk. The distinction proposed here, for
Orchestrator review, is that Branch 2's concern was about **open-ended** condition/time-scoped
querying (no bound on how many conditions, how wide a window, how large a result set — a pattern
that generalizes into an indexer by removing any one constraint). C1R's §3/§4/§7 parameters (hard
3–5 condition ceiling, fixed pre-named condition_ids and token pairs, fixed pre-named windows, hard
per-condition and global row caps at fixed ceilings, fail-fast) are proposed as that missing bound.
Whether this is bound *enough* to not read as indexer-shaped work remains an Orchestrator judgment
call — not self-certified here.

---

## 9. Stop codes

If C1A is separately authorized and executed, it would halt on any of the following, persisting
whatever evidence exists before the halt (consistent with the accepted Option B B0 persist-before-
halt discipline, `SPEC_option_b_b0_failure_diagnostic.md` D1):

**Query/coverage-level stops (carried over from the pre-patch draft):**
- **`C1_SOURCE_SCHEMA_UNVERIFIED`** — the decoded event table's schema (field names, types,
  precision) does not match what was verified/assumed at design time.
- **`C1_ORDERING_KEY_MISSING`** — no source-provided ordering key exists where one is needed to
  disambiguate same-block or same-tx events, and none is available to use as-is (this design does
  not construct one — §5).
- **`C1_ROW_EXPLOSION`** — a per-condition or global row cap (§3, §7.1) would be exceeded.
- **`C1_LOCAL_TX_HASH_REPRODUCTION_ONLY`** — if execution ends up only surfacing rows already
  present in local `Store.load_trades()` for the fixed conditions/windows/token pairs, the pilot's
  coverage claim is treated as void, not silently accepted.
- **`C1_INDEXER_SHAPED`** — if execution reveals the query pattern behaving like open-ended
  retrieval in practice (e.g. caps only bind after very large intermediate scans), the pilot halts
  rather than continuing on a technicality.
- **`C1_SIDE_IDENTITY_UNRESOLVED`** — reserved for a later phase if raw retrieval succeeds and a
  follow-on design attempts side-identity *interpretation* (beyond the raw manifest-token match in
  §6) without a resolved mapping.
- **`C1_CANARY_DESIGN_CLEAR`** — not a halt; a diagnostic-only outcome meaning the fixed 3–5
  condition canary retrieved rows within caps, with a verified schema, ordering key (or none
  needed), and valid selector manifest, and produced a coverage comparison against local
  `Store.load_trades()` without triggering any halt. This does **not** mean coverage is good or
  bad — only that the pilot mechanism ran cleanly enough to produce a readable diagnostic. Not a
  price-source viability verdict.

**Selector-manifest stops (Patch 1 — new):**
- **`C1_SELECTOR_TOKEN_PAIR_UNRESOLVED`** — a condition's static token-pair lookup (§4.1) fails to
  produce a usable pair from the local enumeration basis (missing, or the local basis has no
  qualifying rows for that condition). That condition is excluded from the manifest; it does not
  block the other manifest conditions unless it drops the manifest below a usable count.
- **`C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO`** — the enumeration basis yields fewer or more than
  two distinct, stable side tokens for a condition. Counted and excluded, not guessed or forced to
  two.
- **`C1_SELECTOR_TOKEN_PRECISION_LOSS`** — a candidate token_id fails the string-safe/`canonical_int`
  check (e.g. scientific-notation coercion, truncation) at manifest-population time.
- **`C1_SELECTOR_USES_WINNER_TOKEN_ONLY`** — the manifest-population step is found to have derived
  or checked a token pair using `resolved_winning_token_id` (forbidden, §4.1). This halts manifest
  construction for the affected condition(s); it is a discipline violation, not a data property.
- **`C1_SELECTOR_OUTCOME_CONDITIONED`** — more generally, if any part of the manifest-population
  logic is found to depend on which side ultimately won (beyond the two static, pre-resolution
  token identities themselves), the manifest is void for that condition. This guards against subtler
  leakage than the single-field case `C1_SELECTOR_USES_WINNER_TOKEN_ONLY` already covers.

---

## 10. Separate authorization required for every step beyond this document

This addendum, including Patch 1, is a design writeup only. Each of the following is a distinct,
future, separately authorized step — none is implied, pre-approved, or unlocked by this document,
by the user's "SPEC ONLY" authorization for the original design task, or by the Orchestrator's
"DOC PATCH ONLY" authorization for this patch:

- **C1A execution** — actually running the fixed 3–5 condition canary query (including
  manifest-population/validation, §4) against the decoded event source.
- **C1B sample coverage** — any broadening of C1A into a larger, still-bounded coverage sample.
- **C2 code/tests** — any implementation, test harness, or code artifact building on a C1A/C1B
  result.
- **Any data run** — any network, API, RPC, or Dune call of any kind, including the local
  `trades`-table read that manifest-population (§4.1) would itself require.

No such step is authorized by this document. Each requires its own explicit in-chat authorization
and must remain within the repo's current guardrails at the time it is requested.

---

## 11. Guardrails preserved by this addendum

- **P1 remains BLOCKED** on the absence of an accepted per-side/token-identity price source. This
  addendum does not unblock it — it is a design document, not a coverage result.
- **B1 (Option B) remains unauthorized.** Unaffected by this addendum.
- **P2/P3/probe remain unauthorized.** `named_binary_probe_blocked` stays `true`, not flipped by
  this addendum or its patch.
- **No `yes_price` / `1 - price` / `1 - yes_price` / `1 - p` / side synthesis** appears anywhere in
  this design, including the selector manifest (§4), which is explicitly restricted to static
  identity only and forbidden from computing price, target, score, or probe features.
- **No implementation, no code, no tests, no commands, no API/RPC/network call, no data run, no
  full indexer, no broad backfill, no `log_index` work, no OrdersMatched expansion, no wallet
  discovery, no PnL/scoring, no price-series artifact** is authorized, proposed, or performed by
  this document or its patch.
- **Revision 3 is not silently reversed.** Revision 3's C0 acceptance and its record of the C1
  guardrail block stand as history. This addendum (now patched) proposes a candidate resolution for
  Orchestrator review; it does not itself declare the guardrail block resolved or C1 unblocked.
