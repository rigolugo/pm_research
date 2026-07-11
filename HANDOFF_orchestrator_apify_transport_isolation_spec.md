# HANDOFF — Apify Live Canary Finding + Transport Isolation Spec (FINAL PATCH)

**Orchestrator disposition (2026-07-11):** `APPROVE — SPEC ONLY`. No implementation, build, deployment, network run, P1 continuation, or gate change is authorized. The accepted upload copy changes only acceptance metadata, pins the request timeout/order, and normalizes excerpt bounds to the existing decoded-character behavior.

**From:** Claude (implementation/spec-drafting agent)
**To:** Orchestrator (ChatGPT) / user
**Task:** Final patch of the three-file Apify transport-isolation documentation package. Documentation/spec only — no implementation, no code edits, no Actor build, no Apify deployment, no network request, no live run, no retry, no downstream continuation.

---

## Revision note (this final patch)

The finding is **accepted as written** and returned **unchanged** — see "Files produced" below; it is not re-derived or re-edited in this response, only re-included so the three-file package remains self-contained.

Five corrections applied to the spec, per Orchestrator review:

1. **PycURL removed as an allowed transport.** The spec's §2 now names exactly one transport — the system `curl` executable backed by ordinary libcurl — and states PycURL is out of scope, requiring its own separate review if ever proposed.
2. **Manifest runtime interface pinned.** New spec §3 pins the exact JSON shape (single `conditions` array, identity fields only, no operational flags), pins runtime behavior (Actor keeps using `Actor.get_input()`/`raw_input`; no second direct-file runtime path; exact reconciliation required before any request, with no normalization of side assignment or token identity), and pins responsibility (Orchestrator/user supplies and accepts the manifest; Claude must not fabricate or independently select its contents).
3. **Complete exact schemas.** Spec §7 now fully enumerates all four field lists (see counts below), rather than partially listing or describing them. `curl_version_output` is now described as the *bounded* raw output, not the "full" output.
4. **Corrected counts (this handoff).** See "Exact field counts" below — replaces the prior handoff's incorrect "21 retained / 5 additive."
5. **Open-design section cleaned.** Spec §12 now lists only 3 genuinely open implementation-stage questions; four previously-listed questions are resolved and removed (system curl vs. PycURL; file-loading vs. Actor-input mechanism; who prepares the manifest; the 2000-byte curl-version bound, which is accepted).

No code was changed, no network request was made beyond read-only GitHub verification, and no Actor build or run occurred in producing this patch.

---

## Files produced

1. `FINDING_apify_live_canary_endpoint_blocked.md` — **unchanged**, returned as-is per this task's instruction that it is accepted as written. Target path: `artifacts/named_binary_probe/FINDING_apify_live_canary_endpoint_blocked.md`.
2. `SPEC_apify_transport_isolation_canary.md` — **complete replacement**, still `PROPOSED / SPEC ONLY — NOT YET REVIEWED OR ACCEPTED`.
3. This handoff memo.

Per `CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`, these are complete replacement/new files for the user to upload manually — no GitHub write occurred, and none was attempted.

---

## Exact field counts (corrected this patch)

```text
22 retained raw-request fields
12 additive transport-provenance fields
17 retained candidate-row fields
15 retained condition-pair fields
```

Verified programmatically against the spec document itself (parsed each fenced field list, counted entries, checked for duplicates, and confirmed no `token_identity_basis` or transport field leaked into the candidate or condition-pair rows) before delivery — not hand-counted.

The prior handoff's "21 retained raw-request fields" and "5 additive transport fields" were incorrect and are superseded by the counts above.

---

## Sources inspected

Re-confirmed this turn: the operational manifest path (`artifacts/named_binary_probe/apify_price_canary_real_condition_input.json`) remains absent — `HTTP 404` on both `apify-price-canary-dry-run` and `main`, consistent with the prior patch's finding. `src/live_canary.py`'s `_parsed_side_candidate_row` and `_raw_request_summary_row` functions were re-read to confirm the exact retained field lists in spec §7.1/§7.4 match the actual accepted implementation, field-for-field.

---

## Open design questions (spec §12 — reduced to 3, from the prior patch's list)

- Whether a future curl-based fetch is implemented as a new module alongside `HttpFetcher` in `live_canary.py`, or as a fully separate Actor/script entry path.
- Whether the existing Apify Actor's container image already includes the system `curl` executable, or would require a Dockerfile change (itself requiring separate authorization).
- Exact implementation mechanics for the bounded temporary file used to capture the response body — naming/cleanup discipline — left as an implementation-stage detail.

Removed from this list, as now resolved in the spec: system curl vs. PycURL (§2 — curl only); file-loading vs. Actor-input mechanism (§3.2 — Actor-input, no second path); who prepares the manifest (§3.3 — Orchestrator/user); whether the 2000-byte curl-version bound is accepted (§7.2 — yes, accepted).

---

## Explicit statements

- **No code was changed.** No file under `apify_actors/polymarket_price_canary/` was touched in producing this patch. `live_canary.py` was read again (to verify exact field lists) and not modified.
- **No network request was made** to Polymarket, Gamma, CLOB, or Apify. The only network activity in producing this patch was reading the canonical GitHub repository (read-only) to re-confirm the manifest's continued absence.
- **No Actor build or run occurred.** No Apify project was touched, built, or deployed. No `dry_run: false` run, no curl invocation, no `urllib` invocation against any live endpoint.
- **No manifest was created or committed.** `artifacts/named_binary_probe/apify_price_canary_real_condition_input.json` remains absent; nothing in this patch creates, fabricates, or independently selects its contents.

---

## Recommended Orchestrator decision

```text
APPROVED SPEC ONLY — NO IMPLEMENTATION OR RUN AUTHORIZED
```

## Tests

```text
NOT APPLICABLE — documentation/spec-only patch
```

---

**File delivery only** — not a commit, not a build, not a run, not an implementation authorization. Awaiting Orchestrator review of the finalized spec; the finding requires no further review, having been accepted as written.
