# HANDOFF — Orchestrator Option C C1A-F2 artifact review

**Primary decision label:** `C1F2_ARTIFACTS_INSUFFICIENT`

**Revision note:** This memo supersedes the prior F2 artifact-review memo. The prior memo used `C1F2_ARTIFACTS_INSUFFICIENT` because the C1A-F1 artifacts were not available from canonical GitHub paths during that review. That reason is no longer the governing reason for this revision. The user supplied the C1A-F1 artifact ZIP as explicit review input for this session, and the expected C1A-F1 files are present. The primary label remains `C1F2_ARTIFACTS_INSUFFICIENT`, but now because the `OVER_UNDER` local-only evidence is too thin for safe F2 causal classification.

**Scope:** Review-only / documentation-only F2 artifact memo for C1A-F2. No code, tests, SQL generation, SQL edits, Dune/API/RPC/network calls, local data processing, rerun, new canary, price artifact, probe/scoring/backfill/wallet/OrdersMatched/`log_index`/PnL work, cap change, row truncation, side synthesis, or gate change was performed.

---

## 1. Reviewed artifact list

The supplied C1A-F1 artifact ZIP contains the expected C1A-F1 files:

1. `c1a_f1_windows.json`
2. `c1a_f1_windows.json.provenance.json`
3. `c1a_f1_selector_provenance.json`
4. `c1a_f1_selected_conditions.csv`
5. `c1a_f1_selector_excluded.csv`
6. `c1a_f1_canary_manifest.json`
7. `c1a_f1_dune_query.sql` — historical evidence only, not for edit or rerun
8. `c1a_canary_result.json`
9. `c1a_canary_result.md`
10. `c1a_canary_by_condition.csv`
11. `option_c_c1a_raw_rows_sample.csv`
12. `option_c_c1a_tagged_rows.csv`

The ZIP also includes:

13. `c1a_f1_dune_export.csv`

Artifact availability is therefore not the F2 blocker in this revision.

---

## 2. Artifact completeness finding

The artifact set is present and is sufficient to review:

- accepted C1A-F1 by-subclass counts;
- selected `OVER_UNDER` condition identity;
- selected-condition / manifest / windows / SQL consistency for the fixed window and side-token pair;
- selector provenance guardrails;
- cap discipline;
- SQL query shape as fixed token-pair/time-window filtering against decoded `OrderFilled` tables;
- positive Dune-returning subclasses for returned-row consistency with fixed windows and token pairs.

The artifact set is still insufficient for F2 causal classification because the `OVER_UNDER` evidence consists of only two local-only tx hashes, and the tagged evidence does not carry the local-side row fields needed to decide why Dune returned zero rows for that condition.

Decision consequence: keep `C1F2_ARTIFACTS_INSUFFICIENT`, not a likely-cause label.

---

## 3. Accepted C1A-F1 counts

The accepted C1A-F1 counts are internally consistent:

| Subclass | Dune rows | Dune-only tx hashes | Overlap tx hashes | Local-only tx hashes | Unresolved side rows |
|---|---:|---:|---:|---:|---:|
| `OVER_UNDER` | 0 | 0 | 0 | 2 | 0 |
| `NAMED_OTHER` | 104 | 27 | 2 | 0 | 0 |
| `UP_DOWN` | 29 | 7 | 4 | 0 | 0 |

The result remains mixed review evidence. `NAMED_OTHER` and `UP_DOWN` returned decoded `OrderFilled` rows and Dune-only tx hashes. `OVER_UNDER` returned zero Dune rows and has two local-only tx hashes.

This is not price-source viability evidence. No price was computed or persisted.

---

## 4. `OVER_UNDER` evidence summary

The selected `OVER_UNDER` condition is:

`0xf7361f4c577945b89d4a537eda2acd3cceb1e22cb722c8a48a3114eff058b8d7`

Key fields are consistent across selected conditions, manifest, windows, and SQL:

- fixed window: `2026-05-17 20:12:58 UTC` to `2026-05-17 22:57:23 UTC`;
- side-token IDs match across selected conditions, manifest, and SQL:
  - `side_0_token_id = 99739207105257790128075344211534912968459868715904103406100301477967219589411`;
  - `side_1_token_id = 106729855668864395518421132772923669991080130848538476329326157512462635983691`;
- `local_trade_rows_in_window = 2`;
- `local_distinct_tx_hash_count_in_window = 2`;
- `per_condition_row_cap = 2000`;
- Dune per-condition query limit = `2001` (`cap + 1` over-fetch);
- `global_row_cap = 6000`.

The zero-Dune `OVER_UNDER` result is real at the artifact-summary level: the by-condition/result artifacts show `0` Dune rows, `0` overlap, and `2` local-only tx hashes. However, the artifacts do not provide enough local-side row detail to classify the cause.

---

## 5. Selector / window / token / source-table / local-only evidence review

### Selector provenance

Selector provenance remains safe on the inspected artifacts:

- no Dune count scout;
- no local-tx-hash Dune filter;
- no winner/outcome field use;
- no price/score field use;
- no OrdersMatched/wallet/PnL use;
- no full-universe scan;
- bounded accepted pool source retained;
- deterministic local-density / subclass-balanced selector shape retained;
- caps not raised;
- no reusable volume-profile artifact.

The `OVER_UNDER` condition was selected under the accepted deterministic policy. The inspected selector provenance does not show result-aware edits, Dune counts, local-tx-hash filtering, winner/outcome fields, price fields, score fields, OrdersMatched, wallet, PnL, or full-universe profiling as selector inputs.

### Manifest integrity

The `OVER_UNDER` manifest evidence is internally consistent with the selected-condition evidence:

- exactly two string-safe side-token IDs are present;
- subclass label is `OVER_UNDER`;
- fixed window bounds are present;
- `per_condition_row_cap = 2000`;
- `global_row_cap = 6000`;
- Dune query branch over-fetch is `2001`.

### Window comparability

The `OVER_UNDER` fixed window is consistent across the selected-condition evidence, windows artifact, manifest, SQL text, canary result, and by-condition ledger:

`2026-05-17 20:12:58 UTC` to `2026-05-17 22:57:23 UTC`.

This supports window consistency as far as the artifacts expose the selected-condition/window surfaces.

It does not prove that the two local-only rows individually carried local timestamps inside the window, because `option_c_c1a_tagged_rows.csv` does not carry local timestamp/traded_at fields for those local-only rows.

### Token-pair comparability

The `OVER_UNDER` side-token IDs match across selected conditions, manifest, and SQL. Because `OVER_UNDER` returned no Dune rows, there are no returned source rows for that subclass from which to evaluate source-side token behavior.

Positive Dune-returning subclasses (`NAMED_OTHER`, `UP_DOWN`) have raw rows consistent with their fixed windows and token pairs. That supports the general SQL/tagging mechanism for returned rows in those subclasses only. It does not resolve the `OVER_UNDER` zero-row cause.

### Source-table provenance

The SQL is fixed token-pair/time-window filtering against decoded `OrderFilled` tables and does not filter by local tx hash. The inspected SQL/result metadata does not imply arbitrary table substitution for the reviewed C1A-F1 result.

This supports source-table/query-shape discipline at the canary level. It does not classify the `OVER_UNDER` zero-Dune cause.

### Local-only evidence shape

This is the F2 blocker.

`option_c_c1a_tagged_rows.csv` contains the two `OVER_UNDER` local-only tx hashes. However, those rows lack the local-side fields needed for F2 classification, including:

- local timestamp / `traded_at`;
- local `token_id`;
- local `outcome_index`;
- local side-token match;
- local amount or local row identity;
- direct proof that the local rows individually fall inside the fixed window;
- enough local-row context to compare local row identity against the Dune token/window query surface.

Therefore the artifact review cannot safely decide whether the `OVER_UNDER` zero-Dune result is due to:

- selector/window artifact;
- source coverage gap;
- local/Dune identity mismatch;
- source-table mismatch;
- timestamp/window-boundary issue;
- or another unresolved artifact-level cause.

No tx-hash lookup, Dune requery, source lookup, count scout, or local data rerun was performed.

---

## 6. No price leakage review

The inspected artifacts support the standing no-price-leakage boundary:

- selector provenance does not use price or score fields;
- selector provenance does not use winner/outcome fields;
- selector provenance does not use OrdersMatched/wallet/PnL fields;
- windows provenance records no price artifact;
- C1A-F1 result remains coverage/trust diagnostics only.

No price, canonical-side price, winner/PnL/score/probe metric, `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis is accepted or used by this memo.

---

## 7. Cap discipline review

Cap discipline is preserved on the inspected artifacts:

- `per_condition_row_cap = 2000`;
- Dune per-condition query limit = `2001` (`cap + 1` over-fetch);
- `global_row_cap = 6000`;
- no row explosion in C1A-F1;
- no truncation claim is used to self-clear the result.

The result is still not `C1_CANARY_DESIGN_CLEAR` and does not authorize any larger run or cap policy change.

---

## 8. Defects / insufficiencies found

Primary insufficiency:

- The `OVER_UNDER` local-only evidence is too thin for causal classification. The tagged artifact records the two local-only tx hashes, but not the local-side row details needed to distinguish a selector/window issue from a true source coverage gap, local/Dune identity mismatch, source-table mismatch, timestamp/window-boundary issue, or another cause.

This is not a finding that the C1A-F1 result is invalid. It is a finding that F2 cannot classify the `OVER_UNDER` zero-Dune cause from the present artifacts.

No likely-cause label is supported.

---

## 9. Interpretation discipline

No F2 outcome unblocks P1.

This memo does not mark Option C viable. It does not mark C1 design-clear. It does not emit or record `C1_CANARY_DESIGN_CLEAR`. It does not authorize C1B, C2, P1, P2, P3, probe execution, scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, cap increases, truncation, SQL modification, another canary, or any price artifact.

Standing state remains:

- Option C is not viable.
- C1 is not design-clear.
- P1 remains `BLOCKED` on missing accepted per-side/token-identity decision-time price source.
- `named_binary_probe_blocked` remains `true`.
- C1B/C2/P1/P2/P3/probe remain unauthorized.
- No `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, or side synthesis may be used to unblock named-binary pricing.

---

## 10. Recommended next action

**Recommended next action:** stop / remain unresolved.

Do not proceed to another canary, C1B, C2, P1/P2/P3, probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, cap change, row truncation, SQL modification, price artifact, gate change, or any implementation task from this memo.

Do not recommend a one-condition diagnostic from this memo.

If the project later wants to pursue this exact unresolved issue, the only safe next step would be a separate doc-only artifact-enrichment review specification, explicitly authorized later, focused on whether future artifacts should include enough local-side row evidence to make a review classification possible. That would still not authorize implementation, a run, SQL changes, a Dune/API/RPC/network call, local data processing, another canary, C1B/C2/P1/P2/P3/probe, scoring, backfill, wallet/OrdersMatched/`log_index`/PnL, price artifacts, gate changes, cap changes, row truncation, or side synthesis.
