# HANDOFF — Orchestrator: Option C On-Chain Price-Source Spec (Revision 3) — ACCEPT FINDING

**Decision:** ACCEPT FINDING — DOCS ONLY.

**Scope:** Record the accepted Option C (on-chain / decoded OrderFilled event tables) price-source
candidate review, Revision 3, as SPEC ONLY. Documentation only.

No code changes. No implementation. No tests. No commands. No API/RPC/network call. No data run.
No full indexer. No broad backfill. No `log_index` work. No OrdersMatched expansion. No wallet
discovery. No PnL/scoring. No price-series artifacts. No `yes_price` / `1 - price` / `1 - yes_price`
/ `1 - p` / side synthesis. `named_binary_probe_blocked` remains `true`, untouched.

---

## 1. Accepted finding

- **Option C** selects **bounded decoded Dune/vendor OrderFilled event tables** as the **C0**
  candidate for a per-side/token-identity price source (the third candidate reviewed, after
  Option A/S1-ALT and Option B, both closed negative).
- **C0** is **source-interface / spec verification only** — candidate identification and bounding
  discipline, no coverage claim, no run, no artifact beyond the spec record.
- **C1** (a bounded coverage/trust pilot analogous to Option B's B0) is currently **GUARDRAIL
  BLOCKED**. No safe bounded sample design currently resolves the local-`tx_hash`-scoping trap:
  - Scoping a sample by local `tx_hash` values likely **reproduces S1-ALT** (Option A, already
    closed negative) and **cannot test for missing coverage by construction** — a sample built
    from what local already knows can never surface trades local is missing.
  - Scoping a sample **independently** by `condition_id`/time window, in order to actually test
    for missing coverage, risks **broad event reconstruction / indexer-shaped work**, which the
    project's "No full indexer" guardrail forbids regardless of pilot scale.
- **No implementation follows.** This is a design-level (guardrail) block, not an empirical
  negative, and it does **not** close Option C. C0 stands accepted; C1 remains an open design
  problem pending a future, separately authorized SPEC-ONLY document, if any.

This is Revision 3 of the Option C review. This handoff records only the final accepted Revision
3 content; it does not restate or re-derive Revisions 1–2.

---

## 2. Files pinned/added (documentation-only artifacts)

- `SPEC_price_source_option_c_onchain.md` (new) — the accepted Revision 3 spec, recording C0
  candidate selection and the C1 guardrail block in full (§§0–5 of that document).
- `HANDOFF_orchestrator_option_c_onchain_spec.md` (new, this file).

## 3. Canonical documentation files patched to record this finding

- `project_context/PROJECT_STATE.md` — new bullet recording Option C Revision 3 SPEC ONLY
  acceptance, C0 scope, and the C1 guardrail block.
- `project_context/DECISION_LOG.md` — new settled-decision section
  ("Option C Revision 3: SPEC ACCEPTED — C0 candidate selected, C1 GUARDRAIL BLOCKED") plus a new
  DO NOT REOPEN entry.
- `project_context/ARTIFACT_INDEX.md` — new entries for both files in "Specs & handoffs" and in
  the "Pinned context" active-specs list.
- `project_context/START_HERE.md` — new item in the required read order, new entry in the active
  handoffs sub-list, updated "Current branch state" bullet, and updated "Next possible step"
  section to reflect that Option C C0 is accepted-spec / C1 is guardrail-blocked rather than an
  unexplored future candidate.

No other files were changed. No artifacts directory was created or implied (nothing was run).

---

## 4. Standing state — confirmed unchanged by this docs-only package

- **P1 remains BLOCKED** on the absence of an accepted per-side/token-identity price source.
  Option C does not unblock it; C0 is spec-only and C1 is guardrail-blocked.
- **B1 (Option B) remains unauthorized.** Unaffected by this finding.
- **P2/P3/probe remain unauthorized.** `named_binary_probe_blocked = true` in all gate states,
  **not flipped** by this package.
- **No implementation, tests, commands, API/RPC/network calls, data runs, full indexer, broad
  backfill, `log_index` work, OrdersMatched expansion, wallet discovery, PnL/scoring, or
  price-series artifacts were authorized, proposed, or performed by this package.**
- **No `yes_price` / `1 - price` / `1 - yes_price` / `1 - p` / side synthesis** appears anywhere in
  the new spec or in any patched file.
- **No gate was modified.** No prior decision was silently reversed; Options A and B remain
  closed negative exactly as previously recorded.

---

## 5. Guardrails compliance attestation

Research only. Docs only. No code. No implementation. No tests. No commands. No API/RPC/network
call. No data run. No full indexer. No broad backfill. No `log_index` work. No OrdersMatched
expansion. No wallet discovery. No PnL/scoring. No price-series artifacts. No `yes_price` /
`1 - price` / `1 - yes_price` / `1 - p` / side synthesis. No gate change. `named_binary_probe_blocked`
remains `true`. Delivery is not acceptance beyond what was explicitly approved in-chat; the user
commits these files to `C:\b1\pm_research` (or the canonical repo, once reviewed) at their
discretion.
