# SPEC — Option B B0 Failure Diagnostic (corrected artifact-capture / overlap reconciliation)

**Type:** SPEC ONLY. Diagnostic design for a *possible* corrected B0 diagnostic.
**Status:** ACCEPTED / SPEC ONLY. **Authorizes nothing further.** No code, no implementation,
no API/network call, no rerun, no fresh Polymarket download, no B1, no full Pass 1, no S2, no
P1/P2/P3, no probe, no scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, no price-series
artifact, no gate change. `named_binary_probe_blocked` stays `true`. No `yes_price` /
`1 - price` / `1 - yes_price` / side synthesis anywhere.
**Authorization basis:** explicit in-chat approval of "Option B B0 Failure Diagnostic — SPEC
ONLY," followed by explicit in-chat Orchestrator acceptance with four final spec locks (status
line, locked constants, `OVERLAP_MATCHED` clean bar, ledger-cap clarification), applied in this
revision. The corrected diagnostic *run* described here is **not** authorized by this spec or
by its acceptance; it would require a separate, explicit second authorization (§7).
**Locked constants (fixed at acceptance; not tunable after seeing data):**

- tolerance `τ = 120 seconds`
- separation margin `σ = 24 hours`
- primary API row-ledger cap = **25,000 rows total** (see D2 for scope; no uncapped secondary
  capture path exists)
  **Canonical precedence:** `rigolugo/pm_research` wins over this document. This spec was written
  against canonical files fetched directly from that repo this session (`START_HERE.md`,
  `project_context/START_HERE.md`, `GUARDRAILS.md`, `PROJECT_STATE.md`, `DECISION_LOG.md`,
  `ARTIFACT_INDEX.md`, `SPEC_price_source_option_b_data_api_review.md`,
  `HANDOFF_orchestrator_option_b_b0_RESULT.md`).

---

## 0. Provenance and verification caveats (read first)

- **Verified from canonical repo this session:** the B0 halt facts (`STOP_API_LOCAL_MISMATCH`,
  `api_count=1747`, `local_count=8`, `matched_count=0`, `mismatch_count=1755`, first mismatches
  `API_ONLY`); the local-only diagnostic halt (`STOP_API_ARTIFACT_MISSING`); the artifact state
  (only `option_b_b0_manifest.json` persisted under
  `artifacts/named_binary_probe/price_source_option_b_b0/`); the standing consequences (B1 not
  authorized; Option B not closed as a clean API semantic failure; probe blocked).
- **[UNVERIFIED — console-evidence only, not artifact-persisted]:** the specific temporal
  boundary facts supplied in the current authorization — local rows for the failed condition
  ending at `2026-05-26 21:34:02 UTC`, with API example rows later on `2026-05-27`. No persisted
  B0 artifact records these values (that absence is precisely the `STOP_API_ARTIFACT_MISSING`
  finding). This spec treats them as a *plausible, unverified* motivating observation, never as
  an established finding. The corrected diagnostic exists to turn exactly this class of
  observation into persisted, verifiable evidence.
- **[UNVERIFIED — re-read before any authorized run]:** the exact `/trades` response shape,
  parameter surface, and rate limits must be re-read from `docs.polymarket.com` immediately
  before any authorized run, per accepted Option B spec §0/§5 R7. Nothing here re-asserts API
  field values from memory.

---

## 1. What exactly failed in the first B0 run

Facts, all from the accepted B0 result state (`HANDOFF_orchestrator_option_b_b0_RESULT.md`,
`PROJECT_STATE.md`, `DECISION_LOG.md`):

1. **Execution halt.** The separately authorized B0 run halted at the typed halt
   `STOP_API_LOCAL_MISMATCH` with:
   - `api_count = 1747`
   - `local_count = 8`
   - `matched_count = 0`
   - `mismatch_count = 1755` (= 1747 + 8: every row on both sides unmatched)
   - first inspected mismatches were `API_ONLY` rows (rows present in the API retrieval with no
     composite-identity local counterpart).
2. **What the halt means mechanically.** On ground pre-registered as *known two-sided* from the
   accepted Option A `BOTH_SIDES` set, the composite-identity reconciliation (accepted Option B
   spec §2, R1–R3) paired **zero** rows. `matched_count = 0` with an ~218:1 api:local row ratio
   is not a partial-agreement result; it is a total pairing failure.
3. **Failure of the failure diagnosis.** The follow-up local-only artifact inspection halted at
   `STOP_API_ARTIFACT_MISSING`: the expected directory
   `artifacts/named_binary_probe/price_source_option_b_b0/` contained only
   `option_b_b0_manifest.json`. Missing: `option_b_b0_reconciliation.json`,
   `option_b_b0_by_condition.csv`, `option_b_b0_mismatches.csv`, saved API rows, saved mismatch
   rows.
4. **Root defect this spec addresses.** The B0 runner evaluated the mismatch halt *before*
   persisting its evidentiary artifacts, so the halt destroyed the very rows needed to diagnose
   it. The corrected diagnostic must invert that ordering (§3, D1).

---

## 2. Why the failure is inconclusive (H-API vs H-LOCAL confound)

The `matched_count = 0` result admits at least two mutually exclusive explanations, and the
persisted evidence cannot distinguish them:

- **H-API (API semantic mismatch).** The Data API `/trades` rows genuinely fail composite
  identity against correct, complete local rows in the *same* time window — a schema, identity,
  unit, or precision disagreement. This would support closing the Option B candidate.
- **H-LOCAL (stale/incomplete local parquet).** The local store's rows for the manifest
  conditions end earlier than the API's rows; the two sets barely (or never) overlap in time, so
  zero matches is exactly what a *correct* API against a *stale* local store would produce. This
  would say nothing bad about the API and would instead indict local backfill freshness.

Why the current evidence cannot separate them:

1. **Temporal boundary hint, unpersisted.** Console evidence indicated local rows for the failed
   condition ended at `2026-05-26 21:34:02 UTC` while API example rows were later, on
   `2026-05-27` **[UNVERIFIED — console-only, §0]**. If true for the bulk of API rows, the
   mismatch is dominated by non-overlapping time ranges (H-LOCAL-consistent). But "first
   mismatches were `API_ONLY`" is a glance at a sorted head, not a distribution — concluding
   from it would violate the never-conclude-from-one-row / all-one-direction rule.
2. **`local_count = 8` is itself anomalous.** Eight local rows across a manifest of 10
   conditions pre-registered as Option A `BOTH_SIDES` is far sparser than "known two-sided
   ground" should be. That is H-LOCAL-consistent (staleness/incompleteness) but could also be a
   local *load/filter* defect in the B0 runner (wrong root, wrong column filter, wrong id
   normalization). Unverifiable without the persisted local comparison rows.
3. **No persisted rows ⇒ no offline analysis.** With no saved API rows, no saved local
   comparison rows, and no mismatch ledger, none of the temporal-overlap classifications
   (`NO_TEMPORAL_OVERLAP`, `OVERLAP_MATCHED`, `OVERLAP_API_LOCAL_MISMATCH`) can be determined.
   This is the accepted `STOP_API_ARTIFACT_MISSING` finding.
4. **Pagination completeness unrecorded.** Whether `api_count = 1747` was a complete
   per-condition retrieval or a truncated one (accepted spec §3, R4) was not persisted, so even
   the API-side row set's completeness status is unknown.
5. **`takerOnly` cardinality unrecorded.** Whether the API rows are one-per-trade or
   one-per-taker-fill was a required B0 measurement; no persisted record exists, so `api_count`
   cannot be interpreted as a trade count.

Standing consequence (already accepted, restated): B0 blocks B1 but must **not** be closed as a
clean API semantic failure. Local staleness/incompleteness remains plausible but unverified.

---

## 3. What a corrected diagnostic must persist (requirements D1–D9)

**D1 — Persist-before-halt ordering (the core correction).** All evidentiary artifacts below
MUST be written to disk (flushed, durable) *before* any mismatch-based halt is evaluated. Typed
halts remain halts, but a halt may only fire after the evidence that explains it is on disk.
Per-condition artifacts MUST be written incrementally (after each condition, and API raw pages
after each page), so that even a mid-run halt (rate limit, schema deviation) leaves a coherent
partial ledger plus a persisted statement of how far it got.

**D2 — Full API raw-row ledger (bounded).** For the fixed B0 manifest only: every API row
retrieved, verbatim-faithful (original string forms for identifiers preserved; no numeric
round-trip of token ids), plus retrieval metadata (condition queried, page number, per-call
`limit`, retrieval UTC timestamp). Bound: the **locked** primary API row-ledger cap of
**25,000 rows total** (well above the observed 1,747) — exceeding it is a typed halt
(`STOP_ROW_LEDGER_CAP_EXCEEDED`), never silent truncation. A ledger that is knowingly
incomplete for any reason must be labeled `API_ARTIFACT_INCOMPLETE` (§5).
**Cap scope (locked clarification):** the 25,000-row cap applies to the *primary
condition-scoped API row ledger*. Any `takerOnly` cardinality-probe rows (D6) MUST either
(a) be included under the same 25,000-row cap, with a `query_mode` field on every ledger row
distinguishing primary retrieval from probe retrieval, or (b) be written to a *separate,
explicitly capped* probe ledger whose cap is declared in the run manifest before the run.
There is **no uncapped secondary capture path** of any kind.

**D3 — Full local comparison rows.** Every local row loaded for the manifest conditions, exactly
as consumed by the reconciler (post-normalization values *and* pre-normalization originals),
including the local load parameters (data root, file set, filters). This makes a local
load/filter defect (§2 item 2) independently checkable offline.

**D4 — Full mismatch ledger.** Every unmatched row, both directions (`API_ONLY`, `LOCAL_ONLY`),
plus every counted ambiguity (`TX_HASH_AMBIGUOUS`, per accepted spec R3), with the composite-key
fields that failed to pair. Never only the "first N" mismatches.

**D5 — Pagination completeness status per condition.** For each manifest condition: pages
fetched, per-page row counts, and a typed completeness flag — `COMPLETE_SHORT_FINAL_PAGE` or
`PARTIAL_RETRIEVAL` (full final page / cap hit), per accepted spec R4. A `PARTIAL_RETRIEVAL`
condition's API set MUST NOT be reconciled as if complete.

**D6 — `takerOnly` cardinality status.** For the pre-registered probe subset of manifest
conditions: row counts with `takerOnly` true vs false and the delta, persisted per condition.
Recorded as a measurement; never assumed. Probe rows are captured only under the locked D2 cap
scope: same 25,000-row ledger with a `query_mode` field, or a separate explicitly capped probe
ledger — never an uncapped path.

**D7 — Local temporal bounds per condition.** `min(traded_at)` / `max(traded_at)` (UTC,
unit-attested) over the local comparison rows of each manifest condition, plus local row count.
Conditions with zero local rows are recorded as `LOCAL_EMPTY` with null bounds — not dropped.

**D8 — API temporal bounds per condition.** `min(timestamp)` / `max(timestamp)` (UTC, with the
empirically detected timestamp unit persisted per accepted spec R5) over retrieved API rows per
condition, plus API row count and the pagination flag from D5.

**D9 — Overlap window classification per condition.** The typed classification of §5, computed
offline-reproducibly from D2/D3/D7/D8 alone, persisted per condition and summarized. The
classification code path must be re-runnable against the persisted ledgers without any network
access (that is the definition of "enough artifacts": the offline diagnostic that previously
halted at `STOP_API_ARTIFACT_MISSING` must be fully computable from these files).

Persistence format (accepted layout; changeable only by a future doc-only patch): under
`artifacts/named_binary_probe/price_source_option_b_b0_diag/` — a manifest-attested copy of the
run inputs, `api_rows.csv` (D2), `local_rows.csv` (D3), `mismatches.csv` (D4),
`by_condition.csv` (D5–D9 per condition), `reconciliation.json` (summary + typed statuses +
artifact-completeness self-attestation), `summary.md`. **No file under any `prices/` path; no
price series of any kind.**

---

## 4. Time-bounded overlap reconciliation — safety conditions

A time-bounded reconciliation is **safe only under all of the following**, and is otherwise
forbidden:

1. **Window restriction.** Row-level API↔local matching for agreement purposes is evaluated only
   for API rows whose timestamps fall within `[local_min_traded_at − τ, local_max_traded_at + τ]`
   per condition, where `τ` is the single predeclared tolerance **locked at acceptance:
   `τ = 120 seconds`**. It must not be tuned after seeing data.
2. **Later API rows prove nothing about local incompleteness by themselves.** API rows later
   than `local_max_traded_at + τ` are classified as `API_AFTER_LOCAL_WINDOW` and counted, but
   MUST NOT be used to *claim* local incompleteness unless they are **clearly separated**: a
   predeclared separation margin **locked at acceptance: `σ = 24 hours`** such that the
   rows lie beyond `local_max_traded_at + σ`. Even then the persisted claim is limited to
   "temporal non-overlap consistent with H-LOCAL," never "local store proven incomplete" — that
   stronger claim would require a separately authorized local-completeness diagnostic.
3. **Symmetry.** The same treatment applies to API rows earlier than
   `local_min_traded_at − τ` (`API_BEFORE_LOCAL_WINDOW`) and to `LOCAL_ONLY` rows inside the
   window (which are H-API-relevant and must not be discounted).
4. **No degraded matching.** Inside the window, matching still uses the full composite identity
   (accepted spec R1–R3). Time-bounding narrows *which rows are compared*; it never weakens *how
   they are compared*. No timestamp-only "fuzzy" matches counted as clean.
5. **No side synthesis.** No `yes_price`, no `1 - price`, no `1 - yes_price`, no derivation of
   one side from the other, no price transformation — anywhere, including inside classification
   logic. Any attempt is `STOP_FORBIDDEN_INFERENCE`.
6. **No single-condition conclusions.** No overlap verdict is drawn from one condition or from
   an all-one-direction ledger without the full per-condition breakdown persisted (D9) and all
   10 conditions accounted for.
7. **Unit honesty.** Timestamp-unit detection (seconds vs milliseconds, per R5) must be resolved
   and persisted *before* any window arithmetic; a unit ambiguity is `STOP_SCHEMA_DEVIATION`,
   never a guess.

---

## 5. Result classifications (typed, per condition + run-level)

Per-condition temporal/agreement classification — precedence top-down; first match wins:

1. `OVERLAP_SCHEMA_BLOCKED` — schema/precision deviation prevented trustworthy comparison for
   this condition (R5–R7 violation observed). No overlap verdict may be issued for it.
2. `OVERLAP_PAGINATION_PARTIAL` — API retrieval for this condition is `PARTIAL_RETRIEVAL`
   (D5). A truncated API set must not yield any overlap verdict (a fabricated
   `NO_TEMPORAL_OVERLAP` from truncation is exactly the confound to avoid).
3. `NO_TEMPORAL_OVERLAP` — API and local windows are disjoint beyond tolerance `τ` (including
   the `LOCAL_EMPTY` degenerate case, which must be sub-flagged as such). Consistent with
   H-LOCAL; not proof of it (§4.2).
4. `OVERLAP_MATCHED` — windows overlap and the **locked clean bar** is met in full. All of:
   - all in-window API rows and all in-window local rows pair by full composite identity
     (R1–R3);
   - zero `API_ONLY` in-window rows;
   - zero `LOCAL_ONLY` in-window rows;
   - zero `TX_HASH_AMBIGUOUS` rows;
   - pagination complete for the condition (`COMPLETE_SHORT_FINAL_PAGE`, D5);
   - artifacts complete and offline-recomputable (i.e. the run-level status is
     `API_ARTIFACT_COMPLETE`, §5.6).
     Any shortfall on any element means the condition is **not** `OVERLAP_MATCHED`; there is no
     weaker or partial "clean" bar.
5. `OVERLAP_API_LOCAL_MISMATCH` — windows overlap but in-window rows fail composite pairing.
   This is the H-API-supporting outcome and the only classification that would let a *future*
   decision treat the API as semantically untrustworthy on this ground.

Run-level artifact-completeness status (self-attested in `reconciliation.json` and verified by
the offline re-run of D9):

6. `API_ARTIFACT_COMPLETE` — every artifact required by D1–D9 exists, is non-empty where rows
   were observed, internally consistent (ledger counts reconcile with summary counts), and
   sufficient to recompute all per-condition classifications offline.
7. `API_ARTIFACT_INCOMPLETE` — anything less. An `API_ARTIFACT_INCOMPLETE` run yields **no**
   H-API/H-LOCAL evidence weight, regardless of what its counts appear to show; it may only
   motivate a further corrected attempt under fresh authorization.

Anti-overreach rules: no classification here is a coverage verdict, a viability verdict, or a
B1 gate input by itself; a run mixing classifications across conditions must be reported
per-condition, never averaged into a single label.

---

## 6. Interpretation table (predeclared, to prevent post-hoc reading)

- Mostly `NO_TEMPORAL_OVERLAP` (esp. with clear `σ`-separation) → H-LOCAL plausible and now
  *evidenced*; Option B stays open-but-blocked; any local-freshness/completeness diagnostic or
  data refresh is a separate, separately authorized decision. Not an API exoneration.
- Mostly `OVERLAP_API_LOCAL_MISMATCH` → H-API supported on this ground; would justify proposing
  (not enacting) closure of the Option B candidate per accepted spec §8.
- Mostly `OVERLAP_MATCHED` → mechanical trust evidence on overlapped ground only; still not a
  B0 "pass" by itself (the original B0 pass bar includes pagination + cardinality + full-sample
  behavior) and still authorizes nothing.
- Mixed / `OVERLAP_SCHEMA_BLOCKED` / `OVERLAP_PAGINATION_PARTIAL`-dominated /
  `API_ARTIFACT_INCOMPLETE` → inconclusive; nothing changes; no escalation.

---

## 7. Conditions that would justify a corrected B0 diagnostic rerun (all required)

1. **Fixed manifest, unchanged.** The exact persisted `option_b_b0_manifest.json` 10-condition
   list, provenance-attested against the accepted Option A `BOTH_SIDES` set; any drift, edit, or
   placeholder ⇒ `STOP_SAMPLE_SCOPE_EXCEEDED`. No new sampling.
2. **Explicit second authorization.** A fresh, explicit in-chat authorization naming the
   corrected diagnostic run. This spec's acceptance does not grant it; the prior B0
   authorization does not carry over.
3. **Full artifact persistence before halt.** D1–D9 implemented and verified (persist-then-halt
   ordering demonstrably enforced) before any mismatch evaluation runs.
4. **No B1 and no coverage verdict.** The rerun is a trust/diagnostic measurement only; its
   output feeds Orchestrator review, not any coverage number and not any B1 proposal by itself.
5. **No broad Polymarket download.** Condition-scoped `/trades` calls for the 10 manifest
   conditions only; hard caps at or below the accepted spec ceilings (≤100 calls total,
   ≤5 pages/condition, bounded per-call `limit`), pre-flight enforced; no `eventId`/`user`/
   wildcard queries.
6. **No backfill / no indexer.** The rerun writes only its own diagnostic artifacts; it never
   writes to the local trades/prices stores, never "repairs" local data, and never grows into
   any indexer-like loop.
7. **Standing halts.** All accepted-spec typed halts (§6 of the Option B spec) plus
   `STOP_ROW_LEDGER_CAP_EXCEEDED` (D2) remain in force; `named_binary_probe_blocked` stays
   `true`; failure to persist ⇒ the run self-classifies `API_ARTIFACT_INCOMPLETE`.

---

## 8. Guardrails preserved by this spec

Research only. Spec only. This document authorizes nothing: no code, no API/network call, no
rerun, no fresh Polymarket download, no B1, no full Pass 1, no S2, no P1/P2/P3, no probe, no
scoring, no backfill, no wallet/OrdersMatched/`log_index`/PnL, no price-series artifact, no
writes to any `prices/` path, no gate change. No `yes_price` / `1 - price` / `1 - yes_price` /
side synthesis anywhere, including inside diagnostic classification logic.
`named_binary_probe_blocked` remains `true`. Delivery is not acceptance; the user commits to
`C:\b1\pm_research` at their discretion after Orchestrator review.

---

## 9. Orchestrator decisions — RESOLVED at acceptance

Recorded outcomes of the review (do not re-litigate without an explicit new decision):

1. **Accepted.** Status is ACCEPTED / SPEC ONLY; authorizes nothing further.
2. **Constants locked:** `τ = 120 seconds`; `σ = 24 hours`; primary API row-ledger cap =
   25,000 rows total. Not tunable after seeing data.
3. **`OVERLAP_MATCHED` clean bar locked** as in §5.4 (full composite pairing of all in-window
   rows on both sides; zero `API_ONLY` in-window; zero `LOCAL_ONLY` in-window; zero
   `TX_HASH_AMBIGUOUS`; pagination complete; artifacts complete and offline-recomputable).
   Classification precedence order of §5 stands.
4. **Ledger-cap scope clarified and locked** (D2): the 25,000-row cap governs the primary
   condition-scoped API row ledger; `takerOnly` probe rows go under the same cap with a
   `query_mode` field or into a separate explicitly capped probe ledger; no uncapped secondary
   capture path.
5. **Still open, deliberately:** the console-evidence temporal facts (§0) remain
   motivation-only pending persisted evidence, and the explicit second authorization for a
   corrected diagnostic run (§7.2) has **not** been granted. Acceptance of this spec runs
   nothing.
