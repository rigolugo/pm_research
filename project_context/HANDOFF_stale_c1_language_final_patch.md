# HANDOFF — Orchestrator: Final Patch — Stale Option C C1 Language Removed

**Important note on canonical state:** A direct sparse-checkout read of `rigolugo/pm_research` (files only, no full clone/scan) confirmed the canonical repo's most recent commit is still `9ac7490 "Add files via upload"` — i.e., **none of the C1R/C1A documentation patches from prior turns were ever actually committed**. This is consistent with "delivery is not acceptance": nothing in this project's canonical repo has changed until the user commits. This patch is therefore built fresh from the true canonical baseline, folding in both the original C1R/C1A recording and every stale-language correction requested in this and the prior BLOCK, in one internally-consistent pass.

**Status:** COMPLETE. Documentation-only. No code run. No Dune/API/RPC call. No result artifacts.

---

## Problems fixed (mapped to BLOCK items)

### 1. `project_context/START_HERE.md` — required-read list (item 13)
**Before:** "C1 is GUARDRAIL BLOCKED pending future design... No implementation follows."
**After:** Split into three numbered entries with historical/current wording:
- Item 13: Option C Rev 3 / C0 accepted; **at Revision 3**, C1 was guardrail-blocked; that pre-C1R block is superseded by the C1R addendum.
- Item 14 (new): `SPEC_price_source_option_c_onchain_C1R_addendum.md` — accepted, SPEC ONLY, resolves the scoping trap.
- Item 15 (new): `README_price_source_option_c_c1a.md` — C1A bounded user-run authorized only under this path; no result yet.
- Handoff list extended with `HANDOFF_orchestrator_option_c_c1r_design_addendum.md` and `HANDOFF_orchestrator_option_c_c1a_IMPLEMENTATION.md`.

### 1b. `project_context/START_HERE.md` — Current branch state Option C bullet
Same historical/current-state rewrite applied to the "Current branch state" section's Option C bullet, so both the required-read list and the branch-state summary agree.

### 2. `project_context/START_HERE.md` — "Next possible step" (item 2)
**Before:** "C1 is GUARDRAIL BLOCKED and not proposed... A future move would require a C1 design."
**After:** "The next possible step is the bounded C1A user-run, exactly per README... Results must return to orchestrator for review before any C1B/C2/P1 discussion... C1B not authorized. C2 not authorized. P1/P2/P3/probe remain unauthorized. `named_binary_probe_blocked` remains true."

### 2b. `project_context/START_HERE.md` — "What is NOT authorized"
**Before:** "No C1 pilot of any kind follows... C1 is GUARDRAIL BLOCKED, not merely unauthorized-pending-request."
**After:** "No C1B full sampled coverage, C2 reusable/production implementation, P1/P2/P3 continuation, or probe execution follows from C1A. The only authorized C1A action is the bounded user-run exactly per README, with results returned to orchestrator for review."

### 3. `project_context/DECISION_LOG.md` — main Option C Rev 3 section
- Section header now explicitly marked: **"SETTLED — HISTORICAL; SUPERSEDED FOR C1 BY LATER C1R/C1A DECISIONS"**.
- Added an explicit marker sentence at the top of the section: *"Historical Rev 3 state, superseded for C1 by later C1R/C1A decisions."*
- All current-tense "C1 is GUARDRAIL BLOCKED" language changed to past tense ("was guardrail-blocked... at that time"), with an explicit forward-pointer to the C1R entry that supersedes it.
- **Preserved in full:** the explanation of why local-`tx_hash`-only scoping and broad independent indexing are unsafe (both bullet points kept verbatim in substance).
- **Added two new decision sections** immediately after (before "DO NOT REOPEN"):
  - "Option C C1R (C1 Revised) design addendum: SPEC ACCEPTED (SETTLED — CURRENT STATE FOR C1 DESIGN)"
  - "Option C C1A manifest + bounded canary: AUTHORIZED FOR USER-RUN ONLY (SETTLED — CURRENT STATE FOR C1 EXECUTION)"
- **DO-NOT-REOPEN bullet fixed:** no longer says "C1 is GUARDRAIL BLOCKED" as current state; now reads "At Revision 3, C1 was guardrail-blocked. That pre-C1R block is superseded by the separately accepted C1R addendum... Current allowed path is only the accepted C1A bounded user-run." Two new DO-NOT-REOPEN bullets added for the C1R and C1A decisions themselves.

### 4. `project_context/ARTIFACT_INDEX.md` — new C1R/C1A entries
Added all eight required entries:
- `SPEC_price_source_option_c_onchain_C1R_addendum.md`
- `HANDOFF_orchestrator_option_c_c1r_design_addendum.md`
- `README_price_source_option_c_c1a.md`
- `HANDOFF_orchestrator_option_c_c1a_IMPLEMENTATION.md`
- `scripts/price_source_option_c_c1a_manifest.py`
- `scripts/price_source_option_c_c1a_canary.py`
- `tests/test_price_source_option_c_c1a_manifest.py`
- `tests/test_price_source_option_c_c1a_canary.py`

Also updated the existing `SPEC_price_source_option_c_onchain.md` / `HANDOFF_orchestrator_option_c_onchain_spec.md` entries to historical wording, and extended the "Active specs/handoffs" pinned-context list at the bottom of the file to include the new C1R/C1A spec and README.

### 5. `project_context/PROJECT_STATE.md` — touched for consistency
The BLOCK said "only if touched" — this file's Option C bullet still had the same stale current-tense language, so it was touched to stay consistent with the other three files: same historical ("at Revision 3, C1 was guardrail-blocked") + current-state (C1R resolves it, SPEC ONLY; C1A authorized for user-run only, no result yet; C1B/C2 not authorized) wording, with handoff references added.

---

## Preserved current state (confirmed unchanged)

- Option C Rev 3: accepted / spec-only.
- C0: accepted / spec-only.
- C1R: accepted / spec-only (SPEC ONLY, no execution).
- C1A: code/test package approved for bounded user-run only (not Claude execution); 50 pure-logic tests passing (29 manifest + 21 canary).
- No C1A result exists yet.
- C1B: not authorized.
- C2: not authorized.
- P1: blocked.
- B1: unauthorized.
- P2/P3/probe: unauthorized.
- `named_binary_probe_blocked`: true (never flipped).

## Guardrails preserved

No run. No Dune/API/RPC call. No result artifacts. No price-series artifact. No scoring. No wallet discovery. No OrdersMatched expansion. No `log_index` work. No full indexer. No broad backfill. No `yes_price` / `1 - price` / `1 - yes_price` / `1 - p` / side synthesis.

---

## Files delivered

- `project_context/START_HERE.md`
- `project_context/DECISION_LOG.md`
- `project_context/ARTIFACT_INDEX.md`
- `project_context/PROJECT_STATE.md` (touched, per above)

All four are ready to commit to `rigolugo/pm_research` upon Orchestrator approval. Delivery here is not acceptance — the user commits at their discretion after review.
