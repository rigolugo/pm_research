# SPEC — P0 Representativeness and Quality Audit — SPEC ONLY

**Proposed filename:** `SPEC_p0_representativeness_quality_audit.md`

**Decision posture:** APPROVE — SPEC ONLY, following final revision per Orchestrator review comments (vendor subset-bias section marked explicitly conditional on condition-level Option D data availability; canonical-artifact caveat added; mandatory halt behavior specified; `size_usdc`/`liquidity_usdc` set off by default; histogram granularity left as an implementation-time choice).

**Status:** `P0_REPRESENTATIVENESS_QUALITY_AUDIT_SPEC_ACCEPTED_SPEC_ONLY`. Not implemented. Not run. This document authorizes no work beyond acceptance of this text as methodology/specification.

**Authorization basis:** the user requested a **SPEC ONLY** draft for a local-only/read-only P0 representativeness and quality audit, and Orchestrator has approved this revision as SPEC ONLY. This acceptance does **not** authorize implementation, tests, a real local data run, any vendor/network/API/RPC/Dune fetch, any PMXT/Telonex account or API key use, any price/bid/ask/mid/spread/depth computation, any canonical-side price, any P1/P2/P3/probe, any scoring, any wallet discovery, any OrdersMatched/`log_index`/PnL work, any gate change, or any side synthesis.

**Scope:** Define, on paper only, a local-only/read-only audit of whether the accepted P0 universe is suitable and representative for the named-binary research question, and — conditionally, only if condition-level Option D temporal in-range data is confirmed available at execution time — whether vendor-temporal subsets (PMXT v2 in-range, Telonex L2 in-range) introduce material compositional selection bias beyond the size reduction already established by the completed, accepted Option D temporal in-range precheck result.

**Consumes, does not redefine:** the accepted named-binary classification contract (`nb-contract-2026-06-28.1`), the accepted P0-eligible universe (`final_p0_eligible = 39,693`; subclass denominators `UP_DOWN = 22,012`, `OVER_UNDER = 1,003`, `NAMED_OTHER = 16,678`), the accepted non-YES/NO resolution source (`named_binary_resolution_source_rows.parquet`), the accepted Stage 4 audit gate (`non_yesno_gate_state = CLEAR_WITH_WARNINGS`), and the **accepted, completed** Option D temporal in-range precheck pooled/subclass summary result (`OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`; artifacts `option_d_temporal_inrange_precheck.json` and `.md` at `artifacts/named_binary_probe/price_source_option_d_temporal_inrange/`, per the accepted `ARTIFACT_INDEX.md` entry), consumed as a fixed read-only input, never rerun or re-derived by this document. **This document does not assume a condition-level Option D artifact exists** (see §6.1).

**Canonical-doc workflow constraint:** This document is accepted SPEC ONLY text. Claude must not update canonical project-context files. ChatGPT prepares complete replacement/new files for user manual upload under `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`.

**Hard boundary — this document does not:** implement code; write or modify tests; read any local data file; run any audit; generate project artifacts; fetch data from any vendor archive/API; download any PMXT raw archive file; fetch from Telonex; create or use a vendor account/API key; take paid action; compute any price, bid, ask, mid, spread, or depth; compute any canonical-side price; continue P1/P2/P3; execute the named-binary probe; compute any score; touch wallets, OrdersMatched, `log_index`, or PnL; change any gate; flip `named_binary_probe_blocked`; use `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or synthesize a missing side price by any other means.

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
- Accepted P0 subclass denominators:
  - `UP_DOWN = 22,012`
  - `OVER_UNDER = 1,003`
  - `NAMED_OTHER = 16,678`
- **P1 remains BLOCKED** on the absence of an accepted per-side/token-identity decision-time price input. `Store.load_prices()` exposes only `[condition_id, ts, yes_price]`; `yes_price` is proven YES/NO-only and unsafe for `UP_DOWN`, `OVER_UNDER`, and `NAMED_OTHER`.
- **P2/P3/probe remain UNAUTHORIZED.** `named_binary_probe_blocked` remains `true` in all gate states.
- **S1, S1-ALT, and Option B corrected B0 remain accepted negatives.** Option C remains not viable / not design-clear. **Option D L2 archive coverage remains `ACCEPTED / SPEC ONLY`** (no vendor fetch has occurred). **The Option D temporal in-range precheck is `COMPLETED / ACCEPTED`** (result `OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`), with exact P0 universe reconciliation (39,693/39,693 pooled; no missing anchors) and the following accepted fractions, treated in this document strictly as a fixed read-only input, never recomputed:
  - **PMXT v2 pooled:** `18,137 / 39,693 = 0.456932`; by subclass — `UP_DOWN 0.529211`, `OVER_UNDER 0.661017`, `NAMED_OTHER 0.349263`.
  - **Telonex L2 pooled:** `37,749 / 39,693 = 0.951024`; by subclass — `UP_DOWN 0.974696`, `OVER_UNDER 0.979063`, `NAMED_OTHER 0.918096`.
  - **Accepted interpretation (unchanged by this document):** PMXT v2 is closed/deprioritized for broad full-P0 Option D coverage on timing grounds. Telonex L2 is plausible only for a later, separately authorized SPEC ONLY vendor-coverage review, and is **not** an automatic pass because `NAMED_OTHER` (`0.918096`) sits below the `0.95` subclass floor used elsewhere in this project's gating (e.g., Stage 4). Temporal in-range coverage does not establish vendor availability, token coverage, side coverage, book depth, price quality, mechanical trust, price-source viability, or P1 viability.
- No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or other side synthesis is proposed anywhere in this document.

---

## 1. Objective

Define a future local-only/read-only audit that answers two classes of question about the accepted P0 universe, without touching price, wallet, or scoring surfaces:

1. **Representativeness of P0 itself.** Given what P0 is defined to include and exclude, is the resulting universe a reasonable basis for the named-binary research question, or does it show structural skew (subclass imbalance, timing concentration, resolution-horizon concentration, exclusion-reason concentration) that should qualify any future finding?

2. **Vendor-temporal subset bias**, using the **already-completed and accepted** Option D temporal in-range precheck result as a fixed read-only input. Restricting to PMXT v2 in-range or Telonex L2 in-range conditions changes the size of the usable universe substantially (PMXT v2 to `45.7%` pooled; Telonex L2 to `95.1%` pooled, with `NAMED_OTHER` at `91.8%`). This audit's job is to determine whether that restriction would also change the research universe's *composition* — subclass mix, timing, and other descriptive dimensions — beyond the size reduction already known from the Option D result.

This spec defines the audit design only. It does not rerun the Option D precheck, does not contact any vendor, and treats the Option D result artifacts as a fixed, already-accepted input to be read, not recomputed.

---

## 2. What P0 represents (scope statement, not new analysis)

The audit must state plainly, and treat as fixed, what the accepted P0 universe is and is not:

- P0 **is**: the accepted historical, resolved, single-winner, non-YES/NO named-binary universe — i.e., conditions that are `nb_eligible = True`, subclass in `{UP_DOWN, OVER_UNDER, NAMED_OTHER}`, and `RESOLVED_SINGLE_WINNER` per the accepted resolution source.
- P0 is **not** all Polymarket markets. `YES_NO` (65,603) and `UNUSABLE` (183,124) conditions from the classification contract are excluded by design, not by audit finding.
- P0 is **not** unresolved markets. Only conditions with a resolved, single-winner outcome in `named_binary_resolution_source_rows.parquet` are included.
- P0 is **not** ambiguous or tied outcomes. The 253 `AMBIGUOUS_MULTIPLE_WINNERS` conditions are excluded by design and counted, not silently dropped.
- P0 is **not necessarily** representative of future or currently-live markets. It is a historical accepted-resolution snapshot; nothing in this audit design implies otherwise, and the audit must not conclude forward-looking representativeness from historical composition alone.
- P0 is **not automatically vendor-covered.** As the accepted Option D temporal in-range precheck result shows, only `45.7%` of P0 falls inside the PMXT v2 archive window and `95.1%` inside the Telonex L2 window (pooled). Being in P0 says nothing by itself about whether a condition is reachable by any given vendor archive.

The audit's job is to describe the shape of this defined universe accurately — not to change its definition, and not to argue it should be broadened.

---

## 3. Quality checks already established (inventory only, no new work)

The audit must inventory, not repeat, the following already-accepted checks:

- **P0 exact reconciliation** — pooled and subclass counts already verified: `contract_eligible = 39,957`; `source_rows = 39,946`; `resolved_single_winner = 39,693`; `ambiguous_multiple_winners = 253`; `missing_source_rows = 11`; `final_p0_eligible = 39,693`.
- **Subclass counts** — already fixed at `UP_DOWN = 22,012`, `OVER_UNDER = 1,003`, `NAMED_OTHER = 16,678` (P0-eligible) against classification-contract subclass totals `UP_DOWN 22,013`, `OVER_UNDER 1,039`, `NAMED_OTHER 16,905` (pre-resolution-filter).
- **Outcome-source availability** — Stage 4 pooled map rate `0.99339` (≥ 0.99 floor); per-subclass map rates `UP_DOWN 0.99995`, `NAMED_OTHER 0.98657`, `OVER_UNDER 0.96535` (all ≥ 0.95 floor); gate `non_yesno_gate_state = CLEAR_WITH_WARNINGS`.
- **First-trade timestamp availability** — measured by the completed, accepted Option D temporal in-range precheck: `first_trade_ts = min(traded_at)` per condition (via `Store.load_trades()`) was available for **all** 39,693 P0-eligible conditions pooled and by subclass — zero `NO_FIRST_TRADE_TS`. This audit reuses that already-established availability figure rather than re-measuring it.
- **`resolved_at` availability** — likewise measured by the same completed Option D precheck: zero missing `resolved_at` values across the full P0 universe. Sourced from `named_binary_resolution_source_rows.parquet`; consistent with the Stage 4 map-rate figures above. This audit reuses this figure rather than re-measuring it.
- **`named_binary_probe_blocked = true`** — confirmed unchanged in every accepted artifact and handoff to date; this audit does not touch it.

This section exists so the audit report does not re-derive or re-claim anything already settled — it cites the settled figures and clearly marks what is genuinely new measurement.

---

## 4. Additional representativeness checks proposed (local-only, no price/wallet/score fields)

All of the following are **descriptive, local-only, non-price, non-wallet, non-scoring** checks. Each check below states its proposed source and its exact non-goal.

### 4.1 Subclass mix
- **What:** Pooled and per-subclass share of P0 (`UP_DOWN` / `OVER_UNDER` / `NAMED_OTHER`), plus the pre-resolution-filter classification-contract subclass totals for comparison, to show how much resolution-source filtering shifted the mix (if at all).
- **Source:** `named_binary_classification_contract.json` (`nb_subclass`, `nb_eligible`) joined to `named_binary_resolution_source_rows.parquet`.
- **Non-goal:** does not use price, wallet, or trade-size fields.

### 4.2 Market/category distribution, if locally available
- **What:** Distribution of P0-eligible conditions by `category` from `MARKETS_COLS = [condition_id, category, liquidity_usdc, created_at, resolution_at]` (per `DATA_CONTRACTS_named_binary_probe.md`), reported as counts and shares, pooled and by subclass.
- **Source:** `Store(root).load_markets()`, filtered in-memory to P0-eligible `condition_id`s.
- **`category` is part of the base audit.** It is not price-adjacent and carries no size/value signal.
- **`liquidity_usdc` is OFF BY DEFAULT.** It is **optional and excluded from the base audit** unless separately accepted by Orchestrator (see §10). If separately accepted, its use remains limited to descriptive coverage/completeness reporting (e.g., "is `liquidity_usdc` populated for X% of P0"), never as a price, volume, or sizing input into any score. **The base audit (§4 as a whole, including this check's `category` component) must remain fully valid and executable without `liquidity_usdc`.**
- **Halt condition:** if `category` is absent, empty, or unparseable for a material share of P0, record as a limitation, not a blocking halt (this is a descriptive audit, not a gate).

### 4.3 `first_trade_ts` distribution
- **What:** Pooled and per-subclass distribution (e.g., min/max/quartiles, and a coarse histogram by month or quarter) of `first_trade_ts = min(traded_at)` per condition, computed exactly as defined in the accepted Option D temporal in-range precheck spec §5.1 (same formula). The completed Option D precheck already established that this value is available for all 39,693 conditions (zero `NO_FIRST_TRADE_TS`); this check proposes computing the full **distribution shape** (not just availability) for the first time, for a representativeness purpose distinct from Option D's vendor-timing purpose.
- **Source:** `Store(root).load_trades()`, grouped by `condition_id`, using `traded_at` only. No `price`, `side`, `token_id`, `outcome_index`, `wallet`, or `tx_hash` field is read for this check.
- **Non-goal:** does not compute `decision_ts`, does not touch price fields, does not re-derive vendor in-range classification (that is read from the existing Option D artifact per §6, never recomputed here).
- **Missing-anchor handling:** not applicable in practice (zero missing per the accepted Option D result), but any future implementation must still report the count explicitly rather than assume it, in case local data has changed since the Option D precheck ran.

### 4.4 `resolved_at` distribution
- **What:** Pooled and per-subclass distribution of `resolved_at` (same coarse histogram treatment as §4.3).
- **Source:** `named_binary_resolution_source_rows.parquet`, `resolved_at` field only.
- **Non-goal:** no price, wallet, or scoring use; date-only descriptive statistics.

### 4.5 `decision_ts` distribution
- **What:** Distribution of `decision_ts = first_trade_ts + 3600s` (reusing the accepted `warmup_seconds = 3600` policy), derived purely from §4.3's output — no new data source, no new formula.
- **Source:** derived, not independently fetched.
- **Non-goal:** this is a timestamp arithmetic step only; it does not constitute or approximate any price computation.

### 4.6 Resolution horizon
- **What:** Distribution of `resolved_at − first_trade_ts` (i.e., how long each condition was open, in local trade-anchor terms), pooled and per subclass. This directly informs representativeness: a universe dominated by very-short-horizon or very-long-horizon conditions would not be representative of "typical" named-binary markets.
- **Source:** derived from §4.3 and §4.4 outputs.
- **Non-goal:** no price or wallet use; pure timestamp-difference descriptive statistics.

### 4.7 Trade count per condition
- **What:** Distribution of the count of local trade rows per P0-eligible `condition_id` (pooled and per subclass) — a proxy for how much local trading activity exists per condition, without ever reading a price or size field.
- **Source:** `Store(root).load_trades()`, `condition_id` and `trade_id` (or row count) only.
- **Non-goal:** explicitly excludes `price` and `size_usdc` from this count-only check; those are covered, separately and cautiously, in §4.8.

### 4.8 Volume/size proxies — OFF BY DEFAULT, optional
- **Status:** `size_usdc` is **excluded from the base audit by default.** It may be added only if separately accepted by Orchestrator (see §10). **The base audit (§4 as a whole) must remain fully valid and executable without this check.**
- **What, if separately accepted:** Distribution of `size_usdc` (a trade-table field already present per `TRADES_COLS`) per condition, pooled and per subclass, purely as a descriptive activity-scale proxy — **not** as a price, not as a basis for any canonical-side price, and not combined with any price field.
- **Source, if separately accepted:** `Store(root).load_trades()`, `size_usdc` field only, aggregated (e.g., sum or count of rows) per condition.
- **Explicit boundary:** `size_usdc` is a trade-size field, not a price field, and its use is restricted to descriptive scale/coverage reporting. It must never be multiplied against, divided by, or otherwise combined with `price`, `yes_price`, or any derived price quantity in this audit.

### 4.9 Local data completeness by condition
- **What:** For each P0-eligible condition: does it have (a) at least one local trade row, (b) a `resolved_at` value, (c) a `category` value, pooled and per subclass, reported as completeness rates.
- **Source:** joins of the above.
- **Non-goal:** descriptive completeness only; no inference or imputation of missing values.

### 4.10 Excluded/missing/ambiguous-condition comparison
- **What:** Compare the already-accepted excluded populations — `AMBIGUOUS_MULTIPLE_WINNERS` (253) and `missing_source_rows` (11) — against the included P0-eligible population on the same non-price dimensions as above (subclass mix, `first_trade_ts`/`resolved_at` distribution shape, category mix if available), to check whether exclusions concentrate in a way that could itself introduce bias (e.g., if ambiguous outcomes cluster heavily in one subclass or one time window).
- **Source:** same sources as above, filtered to the excluded sets instead of the eligible set.
- **Non-goal:** this is a comparison of already-settled exclusion decisions, not a request to reconsider or reverse any exclusion. It does not reopen `P0_CLEAR`.

---

## 5. Explicit non-goals for §4 (repeated for clarity)

None of the checks in §4 may, at any point:

- read, compute, or report `price`, `yes_price`, bid, ask, mid, spread, or depth;
- compute or report `canonical_side_price`;
- read or report `token_id`, `outcome_index`, or side labels beyond what is already present in trade rows purely as row identifiers (i.e., they may be counted but never interpreted as a side-price basis);
- read or report wallet identifiers, maker/taker role, `tx_hash`-based identity beyond simple row counting, `OrdersMatched`, or `log_index`;
- compute PnL;
- compute any score, Brier, log-loss, calibration, or reliability metric;
- continue P1/P2/P3 or execute the probe;
- change any gate or flip `named_binary_probe_blocked`.

If any future implementation of this audit finds itself needing a forbidden field to answer a §4 question, it must halt with `STOP_FORBIDDEN_FIELD_REQUIRED` rather than expand scope.

---

## 6. Vendor subset-bias checks — CONDITIONAL on condition-level Option D data being available

**This section is explicitly conditional.** It is included in this SPEC, but it may only be executed by a future implementation if condition-level Option D temporal in-range flags are actually available in the repo. It is not a standing authorization to obtain, generate, or approximate such flags if they are absent — see §6.3 and §6.4 below.

The accepted, completed Option D temporal in-range precheck result establishes the **size** of each vendor-temporal subset (§0 above): pooled and per-subclass fractions only. This section proposes measuring whether restricting to those subsets would also change the **composition** of the research universe — a distinct question the Option D precheck was not designed to answer (it measured only a date-range ceiling, per its own §1/§2 non-goals) — but composition can only be measured if a future implementation can identify *which* individual conditions fall in each vendor's range, not merely the aggregate fraction.

### 6.1 Canonical-artifact caveat

The accepted `ARTIFACT_INDEX.md` entry for the Option D temporal in-range precheck lists exactly:

- `option_d_temporal_inrange_precheck.json`
- `option_d_temporal_inrange_precheck.md`

It does **not** list, confirm, or imply the existence of a per-condition ledger (e.g., `option_d_temporal_inrange_by_condition.csv`). The two listed artifacts carry pooled and per-subclass summary fractions only, per the accepted result. **This SPEC therefore must not assume a by-condition ledger exists.** Any future implementation of §6 must independently verify, by checking the actual repo/artifact contents at execution time, whether a condition-level classification artifact exists before attempting any comparison in §6.2.

### 6.2 What this audit would compare, if and only if condition-level data is available
- Compare PMXT v2 temporally in-range vs. out-of-range P0 conditions on every §4 dimension (subclass mix, `first_trade_ts`/`resolved_at`/`decision_ts` distributions, resolution horizon, trade count, `size_usdc`/`liquidity_usdc` proxy if separately accepted per §10, category mix, completeness).
- Compare Telonex L2 temporally in-range vs. out-of-range P0 conditions on the same dimensions.
- Compare pooled and per-subclass distributions for each vendor split.
- Report whether either vendor's in-range subset differs materially from the full P0 pool on any dimension. This is a live, non-trivial question here: the accepted pooled/subclass result already shows the PMXT v2 subclass fractions are uneven (`OVER_UNDER 0.661` vs. `NAMED_OTHER 0.349` in-range — nearly double the rate), which is suggestive of compositional skew at the subclass level even without condition-level data. But confirming this, or checking other dimensions (timing, category, etc.), requires the condition-level flags this section depends on.

### 6.3 What this section does not do
- It does not fetch PMXT or Telonex data, contact either vendor, or use any account/API key.
- It does not rerun, recompute, or re-emit the Option D temporal in-range precheck or any part of it, under any circumstance, including to fill the gap described in §6.1.
- It does not compute price, wallet, or scoring fields, per §5.
- It does not revisit or contest the accepted Option D interpretation (PMXT v2 closed/deprioritized on timing grounds; Telonex L2 plausible only for a future separately authorized vendor-coverage review, not an automatic pass). Any §6 finding, if it runs, would sit *alongside* that interpretation as an additional, composition-focused data point — not replace or reopen it.
- **It does not request, propose, or perform a local run of any kind to produce a missing by-condition ledger.** If the artifact required by §6.4 is absent, the correct behavior is the typed halt below, not a workaround, not a smaller substitute computation, and not a suggestion embedded in this SPEC for how such a ledger might later be produced.

### 6.4 Required input and mandatory halt if absent

- Accepted P0 universe reconstruction (same as §4).
- A condition-level Option D classification artifact carrying, at minimum, `condition_id` and both `pmxt_v2_temporally_in_range` / `telonex_l2_temporally_in_range` flags per condition.

**If this artifact does not exist** — which, per §6.1, is the presumption unless a future implementation confirms otherwise by checking actual repo contents — **the future audit must halt immediately with `STOP_OPTION_D_CONDITION_LEDGER_ABSENT`.** On this halt, the implementation must not, in any combination:

- rerun or trigger any part of the Option D temporal in-range precheck;
- re-emit, reconstruct, or approximate a by-condition ledger from the pooled/subclass summary figures;
- recompute vendor-in-range flags independently (e.g., by re-deriving `first_trade_ts`/`decision_ts`/`resolved_at` classification logic itself, which would functionally duplicate Option D outside its own governing spec);
- prompt for, request, or schedule a local run to produce the missing ledger.

The correct and only response to this halt is to report `STOP_OPTION_D_CONDITION_LEDGER_ABSENT` and stop; §4 (the base P0 representativeness audit) remains fully executable and unaffected by this halt, since §4 does not depend on vendor-condition-level data.

---

## 7. Representativeness and Sufficiency Criteria

This section defines how a future audit run decides whether local P0 data and vendor-temporal subsets are **valid enough to support later research claims** — not valid enough to unblock P1, which is a separate, unrelated question addressed in §7.5 and §9 (Interpretation guidance). Three layers are required, in order; a layer's checks are meaningful only if the prior layer passed.

### 7.1 Layer 1 — Integrity validation (hard pass/fail)

These are hard gates. Any single failure halts the audit with a typed stop; none of these downgrade to a warning.

| Check | Pass condition | Halt on failure |
|---|---|---|
| Exact P0 reconstruction | P0 universe rebuilt from `named_binary_classification_contract.json` (`nb_subclass`, `nb_eligible`) joined to `named_binary_resolution_source_rows.parquet`, exactly reproducing the accepted construction path (no shortcut through `p0_preflight.json` alone) | `STOP_P0_RECONSTRUCTION_FAILED` |
| Exact P0 count match | Pooled `39,693`; `UP_DOWN = 22,012`; `OVER_UNDER = 1,003`; `NAMED_OTHER = 16,678` | `STOP_P0_UNIVERSE_NOT_VERIFIED` |
| Contract version pin | `nb_contract_version = "nb-contract-2026-06-28.1"` on every source consulted | `STOP_STALE_CONTRACT` |
| Subclass field consistency | Contract `nb_subclass` agrees with resolution-source `subclass` for every joined row (no silent relabeling) | `STOP_SUBCLASS_FIELD_MISMATCH` |
| No silent exclusion-dropping | The 253 `AMBIGUOUS_MULTIPLE_WINNERS` and 11 `missing_source_rows` conditions are counted and retrievable, never merely absent from a denominator without an accompanying reconciling count | `STOP_EXCLUSION_RECONCILIATION_FAILED` |
| Timestamp parseability | Every `traded_at`, `resolved_at`, `first_trade_ts`, and `decision_ts` value used is parsed and normalized to timezone-aware UTC; no naive-timestamp coercion | `STOP_TIMESTAMP_TIMEZONE_AMBIGUOUS` |
| No forbidden fields | No price, wallet, scoring, `log_index`, `OrdersMatched`, PnL, or gate-modification field is read or emitted anywhere in the run (§5, §8.3) | `STOP_FORBIDDEN_FIELD_REQUIRED` / `STOP_OUTPUT_SCHEMA_FORBIDDEN_FIELD` |

If **any** Layer 1 check fails, the audit halts immediately with `STOP_LOCAL_DATA_NOT_VALIDATED` as the overall run-level label (in addition to the specific typed stop above), and Layers 2 and 3 are not attempted or reported. A failed Layer 1 says nothing about representativeness; it says the input itself could not be trusted enough to ask the question.

### 7.2 Layer 2 — Completeness validation (report and judge availability)

Only reached if Layer 1 passes fully. For each of the following, report an exact count/rate, pooled and by subclass, and judge availability against the field's role in the audit (a field the audit depends on structurally needs near-complete coverage to be usable; a purely descriptive optional field does not):

- `first_trade_ts` — per the accepted Option D result, expected 100% (0 missing); the audit must re-confirm this rather than assume it has not drifted since that run.
- `resolved_at` — per the accepted Option D result, expected 100% (0 missing); re-confirm rather than assume.
- `category`, if available from `Store(root).load_markets()` — no prior accepted availability figure exists; report as newly measured.
- Market-row presence — whether a `MARKETS_COLS` row exists at all per P0-eligible `condition_id`.
- Trade-row presence — whether at least one local trade row exists per P0-eligible `condition_id` (distinct from `first_trade_ts` availability, which additionally requires a parseable `traded_at`).
- Excluded/missing/ambiguous comparison rows — confirm the 253 ambiguous and 11 missing-source conditions remain individually identifiable for the §4.10 comparison.

Missingness in any of these must be **counted and interpreted in the report**, never silently dropped from a denominator or omitted from the narrative. A field with material missingness does not by itself halt the audit (Layer 2 failures are reported, not hard stops, unless a Layer-2 gap is severe enough to make Layer 3 comparisons meaningless — see §7.4).

### 7.3 Layer 3 — Representativeness validation (comparisons)

Only reached if Layers 1 and 2 both pass (or Layer 2 gaps are judged non-blocking per §7.4). Required comparisons:

- Included P0 vs. ambiguous/missing/excluded conditions, where the Layer 2 completeness check confirms this comparison is safe to make. **This comparison does not depend on Option D and is always in scope once Layers 1–2 pass.**
- Full P0 vs. PMXT v2 temporally in-range; full P0 vs. PMXT v2 out-of-range; full P0 vs. Telonex L2 temporally in-range; full P0 vs. Telonex L2 out-of-range. **These four vendor-temporal comparisons are required only if §6.4's condition-level Option D artifact exists and is confirmed at execution time.** If that artifact is absent, §6 must halt with `STOP_OPTION_D_CONDITION_LEDGER_ABSENT`, per §6.4, and these four comparisons are skipped rather than attempted, approximated, or substituted. **The base P0 representativeness audit — the exclusion comparison above, plus all of §4 — may still proceed and reach a full verdict without them**; the absence of vendor-temporal comparisons does not by itself trigger `STOP_LOCAL_DATA_NOT_VALIDATED` or block Layer 3 for the base universe.

Each comparison that does run is made across: subclass mix, category mix (if available), `first_trade_ts` distribution, `decision_ts` distribution, `resolved_at` distribution, resolution horizon, trade count per condition, and any approved non-price activity proxy (§4.8, §9). No price, wallet, or scoring dimension is ever a comparison axis.

### 7.4 Interpretation labels

The audit's overall verdict, reported once Layers 1–3 (or the relevant subset) have run, must be exactly one of:

| Label | Meaning |
|---|---|
| `P0_REPRESENTATIVENESS_CLEAR` | Layers 1–2 pass cleanly; Layer 3 comparisons show no material compositional difference between full P0 and either vendor-temporal subset, and no material skew between included and excluded conditions. |
| `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS` | Layers 1–2 pass; Layer 3 shows minor or narrow differences (e.g., a single dimension with modest skew) that qualify but do not undermine using P0, or a subset of it, for future framing. |
| `P0_REPRESENTATIVENESS_BIASED` | Layer 3 shows material compositional skew in at least one comparison — e.g., the PMXT v2 in-range subset materially over/under-represents a subclass or timing band relative to full P0. This does not fail Layer 1 or 2; it is a substantive finding about the data, not a data-quality defect. |
| `P0_REPRESENTATIVENESS_NOT_ESTABLISHED` | Layer 2 gaps are severe enough that Layer 3 comparisons cannot be trusted (e.g., `category` missing for most of P0, making category-mix comparisons meaningless), even though Layer 1 passed. Distinct from `BIASED`: this means "we don't know," not "we know it's skewed." |
| `VENDOR_TEMPORAL_SUBSET_BIASED` | A vendor-subset-specific finding (§6) showing that vendor's in-range subset diverges materially from full P0, reported per vendor (a run could find PMXT v2 subset biased while Telonex L2 subset is not, or vice versa). This label may co-occur with `P0_REPRESENTATIVENESS_CLEAR` for the base P0 audit if the base-universe checks (§4) pass while a specific vendor subset (§6) does not. |
| `STOP_LOCAL_DATA_NOT_VALIDATED` | Layer 1 failed; no representativeness verdict is reached at all. |

### 7.5 What "valid enough" means here

**"Valid enough" in this document means valid enough to frame later research claims responsibly — e.g., to state accurately what population a future finding would and would not generalize to. It does not mean, and cannot be read to mean, valid enough to unblock P1.**

A `P0_REPRESENTATIVENESS_CLEAR` verdict — even a clean one, on both the base P0 audit and both vendor subsets — cannot by itself:

- establish price-source viability for any vendor or method;
- authorize any vendor account, API key, fetch, or paid action;
- authorize P1/P2/P3 or the probe;
- change `named_binary_probe_blocked` or any gate;
- substitute for the separately-gated vendor-coverage review that would still be required before any Telonex L2 (or other) price-source work could proceed, per the accepted Option D interpretation.

Representativeness and price-input availability are independent properties. This audit addresses only the former.

---

## 8. Output design

### 8.1 Primary output
- `JSON` and `Markdown` summary only, mirroring the Option D precheck's own output-design discipline (a machine-readable summary plus a narrative report).

### 8.2 Optional CSV ledgers
A future implementation may optionally produce per-condition CSV ledgers containing only:

- `condition_id`
- `subclass`
- timing-bucket fields (e.g., `first_trade_ts_bucket`, `resolved_at_bucket`, `resolution_horizon_bucket`)
- vendor-temporal flags (`pmxt_v2_temporally_in_range`, `telonex_l2_temporally_in_range`), populated only if §6.4's condition-level artifact exists and is confirmed at execution time; otherwise omitted entirely, per the §6.4 halt
- non-price local descriptive metrics explicitly allowed by §4 (e.g., `local_trade_row_count`, `category`, completeness flags)

### 8.3 Explicitly forbidden output fields
Every output must exclude, and any future implementation must halt with `STOP_OUTPUT_SCHEMA_FORBIDDEN_FIELD` if any of the following appear:

- price fields (`price`, `yes_price`, bid/ask/mid/spread/depth, `canonical_side_price`);
- token-side fields used as a price/side basis (`token_id`, `outcome_index`, side labels), beyond simple non-interpretive row counting already scoped in §4.7;
- wallet fields (wallet identifiers, maker/taker role);
- scoring fields (Brier, log-loss, calibration, reliability, skill score, any forecast-vs-price metric);
- PnL fields;
- `log_index` or `OrdersMatched` fields;
- gate-modification fields, or any field that would flip `named_binary_probe_blocked`.

---

## 9. Interpretation guidance

- A **clean representativeness audit** — i.e., §4 shows no material skew in subclass mix, timing distribution, or exclusion concentration, and §6 shows no material vendor-subset bias (per the §7.4 labels) — may justify treating a later vendor-coverage SPEC as resting on a representative universe, but does **not** itself constitute a vendor-coverage justification and does not authorize any new vendor work by itself.
- A **biased subset finding** (`VENDOR_TEMPORAL_SUBSET_BIASED`, §7.4) — e.g., if §6 shows the PMXT-v2-in-range or Telonex-L2-in-range subset is concentrated in one subclass, one narrow horizon band, or otherwise diverges materially from the full P0 pool — should close or deprioritize reliance on that vendor path for representativeness purposes, or at minimum require any future vendor-coverage spec to explicitly frame its scope as "this subset only," not "P0 broadly." Given the already-known fraction-level skew between PMXT v2's `OVER_UNDER` (0.661) and `NAMED_OTHER` (0.349) in-range rates (§0, §6.1), a `VENDOR_TEMPORAL_SUBSET_BIASED` finding for PMXT v2 specifically would not be a surprising outcome of running this audit.
- **This audit cannot unblock P1 by itself, and cannot authorize vendor action or price-source construction**, regardless of verdict — see §7.5 for the full statement of this limit. Representativeness is a necessary-but-not-sufficient property; it says nothing about price-input availability, which remains the actual P1 blocker per `PRICE_INPUT_CONTRACT_named_binary_probe.md`. A favorable representativeness finding does not change `named_binary_probe_blocked`, does not authorize P1/P2/P3, and does not authorize the probe.
- Because P0 is historical/resolved by construction (§2), any representativeness finding here describes historical composition only and must not be read as a claim about future or live-market representativeness.

---

## 10. Open decision points for Orchestrator review

These are flagged, not resolved, by this draft:

1. **`liquidity_usdc` and `size_usdc` inclusion (§4.2, §4.8) — now OFF BY DEFAULT per this revision.** Both are non-price markets/trades-table fields already present in the accepted data contracts, proposed only as optional descriptive scale/coverage proxies. The base audit is valid and fully executable without either. Orchestrator may separately accept one, both, or neither for a future implementation; absent such acceptance, neither is used.
2. **Coarse histogram bucket granularity** (e.g., monthly vs. quarterly) for §4.3–§4.6 is left unspecified pending Orchestrator preference; this does not change the audit's non-price scope.
3. **Whether §6 (vendor subset-bias) should be included in the base audit SPEC or separated as an addendum.** §6 is explicitly conditional on a condition-level Option D artifact existing, which is not confirmed by the accepted `ARTIFACT_INDEX.md` entry (§6.1). The open question is purely organizational: keep §6 folded into this single spec as a clearly-marked conditional section (as drafted), or split it into its own narrower follow-up spec so the base P0 representativeness audit (§4) can be authorized and run on its own, unaffected by whether §6's precondition is ever met.
4. **Halt-label vocabulary** proposed in §5, §6.3, and §7 (`STOP_FORBIDDEN_FIELD_REQUIRED`, `STOP_OPTION_D_CONDITION_LEDGER_ABSENT`, `STOP_OUTPUT_SCHEMA_FORBIDDEN_FIELD`, `STOP_P0_RECONSTRUCTION_FAILED`, `STOP_SUBCLASS_FIELD_MISMATCH`, `STOP_EXCLUSION_RECONCILIATION_FAILED`, `STOP_LOCAL_DATA_NOT_VALIDATED`) is proposed fresh for this spec and should be reviewed for consistency with existing project halt-label conventions (e.g., overlap with `STOP_P0_UNIVERSE_NOT_VERIFIED` and `STOP_STALE_CONTRACT`, already defined in the Option D precheck spec and reused here) before acceptance.
5. **Confirmed: the accepted `ARTIFACT_INDEX.md` does not list a condition-level Option D artifact** (only `option_d_temporal_inrange_precheck.json` and `.md`, both pooled/subclass summaries). Per §6.1 and §6.4, this SPEC now treats the by-condition ledger as unconfirmed by default; §6 is executable only if a future implementation independently confirms such an artifact exists at execution time, and must halt with `STOP_OPTION_D_CONDITION_LEDGER_ABSENT` otherwise — with no rerun, no re-emission, no independent recomputation of vendor flags, and no request for a local run to fill the gap. This item is resolved as a SPEC-level rule (§6.4), not left open.

---

## 11. Guardrails preserved by this spec

Research only. Spec only. This document authorizes no implementation, no tests, no real local data run, no vendor/network/API/RPC/Dune fetch, no PMXT/Telonex account or API key use, no prices, no bid/ask/mid/spread/depth, no canonical-side price, no P1/P2/P3/probe, no scoring, no wallet discovery, no OrdersMatched/`log_index`/PnL, no gate change, and no side synthesis. `yes_price`, `1 - price`, `1 - yes_price`, and `1 - p` appear only in prohibition, non-goal, and guardrail language. They are never proposed as diagnostic logic, computation, fallback, inference path, price input, side synthesis, or allowed output. `named_binary_probe_blocked` remains `true`, not flipped. P0 remains accepted / `P0_CLEAR`. P1 remains BLOCKED. S1, S1-ALT, and Option B corrected B0 remain accepted negatives. Option C remains not viable / not design-clear. Option D L2 archive coverage remains `ACCEPTED / SPEC ONLY` (no vendor fetch has occurred). The Option D temporal in-range precheck is `COMPLETED / ACCEPTED` (`OPTION_D_TEMPORAL_INRANGE_PRECHECK_COMPLETED_ACCEPTED`), and this document treats that result strictly as a fixed, already-accepted, read-only input — it is never rerun, recomputed, or reinterpreted by this document, and its accepted interpretation (PMXT v2 closed/deprioritized on timing grounds; Telonex L2 plausible only for a future separately authorized vendor-coverage review, not an automatic pass) stands unchanged. Acceptance of this document, if it occurs, is not authorization to run any future step described here; each future step (a local representativeness run per §4, or a vendor-subset comparison per §6 that reads the existing Option D artifacts) requires its own explicit in-chat authorization.

**`P0_REPRESENTATIVENESS_QUALITY_AUDIT_SPEC_ACCEPTED_SPEC_ONLY`**
