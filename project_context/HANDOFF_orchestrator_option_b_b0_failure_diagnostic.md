# HANDOFF — Claude → Orchestrator: Option B B0 Failure Diagnostic spec — FINAL LOCKS APPLIED

**Task:** Apply the four approved final spec locks to `SPEC_option_b_b0_failure_diagnostic.md`
following its in-chat acceptance as SPEC ONLY.
**Status:** Done. **Docs only. Spec only.** No code, no implementation, no B0 rerun, no
API/network call to Polymarket, no fresh Polymarket download, no data run, no state change.
Nothing here authorizes B1, full Pass 1, S2, P1/P2/P3, probe, scoring, backfill,
wallet/OrdersMatched/`log_index`/PnL, or any gate change. `named_binary_probe_blocked` remains
`true`, not flipped.

---

## Basis

Canonical context was read directly from `rigolugo/pm_research` earlier this session (full
required read order per `project_context/START_HERE.md`). Before editing,
`project_context/START_HERE.md` was re-fetched and verified byte-identical (matching SHA-256)
to the session's earlier read — no canonical drift during the task.

---

## Changes applied (the only changes)

1. **Status line (Lock 1).** Header status changed from draft-for-review to:
   **ACCEPTED / SPEC ONLY. Authorizes nothing further.** Authorization-basis paragraph updated
   to record the acceptance and the four locks; an explicit locked-constants block was added to
   the header.
2. **Constants locked (Lock 2).** All "proposed / Orchestrator to confirm or amend" language
   removed. Now fixed and marked locked-at-acceptance in the header, §3 D2, §4.1, §4.2, and §9:
   - `τ = 120 seconds`
   - `σ = 24 hours`
   - primary API row-ledger cap = 25,000 rows total
     All three remain declared as not tunable after seeing data.
3. **`OVERLAP_MATCHED` clean bar locked (Lock 3).** §5.4 replaced with the locked definition —
   all in-window API rows and all in-window local rows pair by full composite identity (R1–R3);
   zero `API_ONLY` in-window rows; zero `LOCAL_ONLY` in-window rows; zero `TX_HASH_AMBIGUOUS`
   rows; pagination complete (`COMPLETE_SHORT_FINAL_PAGE`); artifacts complete and
   offline-recomputable (`API_ARTIFACT_COMPLETE`). Any shortfall on any element ⇒ not
   `OVERLAP_MATCHED`; no weaker or partial bar exists.
4. **Ledger-cap scope clarified (Lock 4).** §3 D2 now states the 25,000-row cap governs the
   *primary condition-scoped API row ledger*, and that `takerOnly` cardinality-probe rows must
   either be included under that same cap with a `query_mode` field on every row, or be written
   to a separate *explicitly capped* probe ledger declared in the run manifest. **No uncapped
   secondary capture path.** §3 D6 cross-references this rule.
5. **Consequential doc tidy-ups only:** §9 rewritten from "decisions requested" to
   "decisions RESOLVED at acceptance" (recording locks 1–4 and noting the two deliberately open
   items: console-evidence temporal facts stay motivation-only, and the second authorization
   for a corrected run is **not** granted); §3 persistence-format line changed from
   "proposal, Orchestrator may amend" to "accepted layout; changeable only by a future doc-only
   patch."

Verification: a post-edit scan confirms no remaining "proposed" / "draft" / "confirm or amend"
language anywhere in the spec; the three locked constants appear consistently in the header,
D2/D6, §4, and §9.

## What did NOT change

The six substantive answers (§1 failure facts, §2 inconclusiveness, §3 D1–D9 persistence
requirements, §4 time-bounded reconciliation safety rules, §5 classification taxonomy and
precedence, §7 rerun preconditions), the interpretation table (§6), the typed-halt additions,
the provenance/UNVERIFIED flags (§0), and the guardrails section (§8) are unchanged in
substance.

---

## Standing state after this task

- Spec is ACCEPTED / SPEC ONLY. It authorizes nothing further.
- The corrected B0 diagnostic **run remains not authorized** (§7.2 second authorization not
  granted).
- B1 remains not authorized. Option B remains not-closed-as-clean-API-failure.
- P1 remains blocked on the absence of an accepted per-side/token-identity price source.
- `named_binary_probe_blocked` remains `true`.

## Suggested doc follow-ups (Orchestrator discretion; not performed here)

If/when the user commits the revised spec to `C:\b1\pm_research`, the usual pinned-context
patches would be: add the spec to `ARTIFACT_INDEX.md` and the `project_context/START_HERE.md`
read order, and note the accepted-spec state in `PROJECT_STATE.md` / `DECISION_LOG.md`. Not
done in this task; docs-only patching of canonical context files needs its own approval.

---

## Guardrails compliance attestation

Research only. Spec only. No code written. No API/network call to Polymarket (only read-only
fetch of one canonical GitHub context file for drift verification, as directed by the project
bootstrap). No rerun, no fresh Polymarket download, no B1/full Pass 1/S2/P1/P2/P3/probe/
scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, no price-series artifact, no
`yes_price` / `1 - price` / `1 - yes_price` / side synthesis. Delivery is not acceptance of
anything beyond what the Orchestrator already approved in-chat; the user commits to
`C:\b1\pm_research` at their discretion.
