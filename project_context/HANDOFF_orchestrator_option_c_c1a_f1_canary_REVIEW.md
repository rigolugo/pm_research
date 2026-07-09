# HANDOFF — Orchestrator Option C C1A-F1 bounded canary REVIEW

**Decision posture:** ACCEPT FINDING — C1A-F1 bounded canary executed and produced reviewable mixed coverage/trust evidence.

**Scope of this document:** DOCS ONLY. This handoff records the observed C1A-F1 canary result and proposes project-state documentation updates. It does not implement code, modify SQL, rerun Dune, fetch data, create price artifacts, authorize downstream work, or alter project gates.

---

## 1. Accepted observed result

The C1A-F1 bounded canary executed and emitted:

- `outcome = C1_CANARY_EXECUTED_NEEDS_REVIEW`
- total Dune rows in window = `133`
- row explosion = `false`
- unresolved side rows = `0`
- total Dune-only tx hashes = `34`
- no price was computed or persisted
- this is **not** `C1_CANARY_DESIGN_CLEAR`
- this does **not** unblock P1

Per-condition / subclass evidence:

| Subclass | Dune rows in window | Dune-only tx hashes | Overlap tx hashes | Local-only tx hashes | Unresolved side rows |
|---|---:|---:|---:|---:|---:|
| `NAMED_OTHER` | 104 | 27 | 2 | 0 | 0 |
| `UP_DOWN` | 29 | 7 | 4 | 0 | 0 |
| `OVER_UNDER` | 0 | 0 | 0 | 2 | 0 |

Interpretation of the mixed evidence:

- `NAMED_OTHER` and `UP_DOWN` show that bounded decoded `OrderFilled` retrieval can surface event tx hashes absent from local trades for these selected conditions.
- `OVER_UNDER` returned zero Dune rows in the fixed window while local-only tx hashes existed, so the evidence is mixed, not clean.
- The absence of row explosion in this C1A-F1 canary is useful but narrow; it does not prove full sampled coverage, production viability, or reusable source fitness.
- Zero unresolved side rows supports token-side identity tagging for the returned rows only. It does not establish canonical decision-time price input coverage.

---

## 2. Required decision boundaries

Accepted:

- C1A-F1 executed.
- The result is reviewable.
- The result is coverage/trust diagnostic evidence only.
- The C1A-F1 bounded canary did not hit the previous row-explosion halt.
- The result contains mixed evidence: two subclasses with Dune-only tx hashes and one selected subclass with zero Dune rows.

Not accepted / not authorized:

- Do **not** mark Option C viable.
- Do **not** mark C1 design-clear.
- Do **not** emit or record `C1_CANARY_DESIGN_CLEAR`.
- Do **not** unblock P1.
- Do **not** authorize C1B, C2, P1, P2, P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, cap changes, row truncation, new Dune runs, or additional canaries.
- Do **not** treat Dune-only tx hashes as a price artifact.
- Do **not** use `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis.

---

## 3. Project-state impact

Current standing state after accepting this finding:

- Named-binary P1 remains blocked on the absence of an accepted per-side/token-identity decision-time price source.
- `named_binary_probe_blocked` remains `true`.
- Option C remains a candidate under diagnostic review, not a viable source.
- C1A-F1 is now historical executed evidence, no longer merely a proposed selector-policy or prep-only package.
- Any next step must be separately authorized. A safe next step, if any, should be review/spec-only before any implementation or run discussion.

---

## 4. Suggested documentation changes

Apply the companion proposed-update files:

1. `PROPOSED_ARTIFACT_INDEX_option_c_c1a_f1_canary_REVIEW.md`
2. `PROPOSED_PROJECT_STATE_option_c_c1a_f1_canary_REVIEW.md`
3. `PROPOSED_START_HERE_option_c_c1a_f1_canary_REVIEW.md`

These are proposed text patches only. They do not mutate the repo by themselves.

---

## 5. Guardrail attestation

This handoff is documentation-only. It includes no code, no tests, no SQL edits, no Dune/API/RPC/network calls, no SQL execution, no additional canary, no C1B/C2 implementation, no price artifact, no probe/scoring/wallet/OrdersMatched/`log_index`/PnL, and no authorization for any downstream work.
