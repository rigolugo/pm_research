# HANDOFF — Orchestrator: Option C C1A-F1 selector-policy implementation (PATCHED) — CODE/TEST ONLY

**Decision requested:** Review the patched CODE/TEST-ONLY selector machinery for scope-compliance and
accept/patch. No run authorization is requested and none is implied.

**Prior BLOCK addressed:** The previous implementation ranked candidates by
`observed_point_count_side_0 + observed_point_count_side_1` from
`price_source_s1_coverage_by_condition.csv`. Those are S1 CLOB `/prices-history` coverage diagnostics
of a different, already-rejected source (Option A / S1) — not local trade-store density. This patch
removes that entirely and ranks only by approved local-trade density.

**Governing spec:** `project_context/SPEC_price_source_option_c_c1a_followup.md` (canonical repo
version), §6.2–§6.6 and §8. C1A-F1 selector-policy shape accepted in principle, SPEC ONLY. Current
task remains CODE/TEST ONLY. No run is authorized.

---

## 1. Density-source answer (explicit, as required)

**The selector supports BOTH approved density-input shapes and never uses S1 CLOB point counts:**

- **Shape 1 — precomputed bounded local-only density file** (`density_source =
  PRECOMPUTED_LOCAL_POOL_FILE`): `read_precomputed_local_density()` reads a bounded CSV keyed by
  `condition_id` carrying exactly the approved fields `local_trade_rows_in_window`,
  `local_distinct_tx_hash_count_in_window`, `window_seconds`. It **refuses** any file that carries a
  rejected S1 CLOB field (`observed_point_count_*`, `nearest_gap_*`, etc.), so a mislabeled S1
  coverage CSV cannot smuggle CLOB density in. No pandas/network needed.
- **Shape 2 — computed from local trades** (`density_source = COMPUTED_FROM_LOCAL_TRADES`):
  `compute_local_density_from_trades()` lazily imports `Store`, loads trades, **immediately restricts
  to the bounded pool condition IDs** (never a full-universe scan), and inside the deterministic fixed
  window counts local trade **rows**, counts **distinct local `tx_hash`**, and computes
  `window_seconds`. It returns an in-memory dict and **persists no reusable profiling artifact**.
  Claude does not execute this path.

The bounded candidate **set + static identity** is still read from the accepted small S1/S1-ALT pool
CSV via `read_bounded_pool_identity()`, but that reader keeps only identity/eligibility columns
(`ALLOWED_IDENTITY_COLUMNS`) and **drops the S1 CLOB columns**, so identity use of an S1 CSV is fine
while its CLOB point counts can never reach density logic. Ranking is by `density_rank_value =
(local_trade_rows_in_window, local_distinct_tx_hash_count_in_window)`, tie-broken by
`sha256(condition_id | selector_policy_version)`.

---

## 2. Required patch details — status

1. **Replaced `local_density_points` (S1 CLOB sum) with approved fields.** Done. The old field no
   longer exists on any record; ranking uses local-trade-row density only.
2. **Compute-from-local-trades path.** Done: loads only bounded-pool condition IDs; counts local
   trade rows and distinct `tx_hash` in the fixed window; computes `window_seconds`; persists no
   reusable profile.
3. **Deterministic subclass-balanced selection.** Preserved.
4. **Deterministic hash tie-breaker.** Preserved (policy version bumped to
   `c1a-f1-selector-2026-07-08.2-localtrade-density` so the density-metric change is auditable in
   every tie-break).
5. **Uniform prior-C1A holdout.** Preserved (whole prior manifest excluded uniformly, never a
   single-condition drop).
6. **3–5 condition canary scale.** Preserved.
7. **No-run / no-network boundaries.** Preserved.
8. **Tests fail if S1 CLOB point counts are used.** Added: a precomputed density file carrying
   `observed_point_count_side_0` is refused; a density dict carrying a CLOB field is refused in
   `evaluate_candidate`; the identity reader drops S1 CLOB columns; selected records no longer expose
   `local_density_points`.
9. **Added tests proving:** density comes from approved local-trade fields only; full-universe
   profiling is rejected by filename guard and the compute path restricts to bounded IDs; S1 observed
   point-count columns are ignored (identity) / refused (density); winner/outcome/PnL/score fields are
   rejected; deterministic selection is stable; no Dune/network/run path exists (source-scan test).

---

## 3. Files changed

Two files, no existing file or artifact mutated:

- `scripts/price_source_option_c_c1a_f1_selector.py` (patched)
- `tests/test_price_source_option_c_c1a_f1_selector.py` (patched)

No `artifacts/` write or mutation. Selector output files are produced only on a future local user-run
of the CLI, not by this handoff and not by Claude.

---

## 4. Test command and result

```powershell
$env:PYTHONPATH="C:\b1\pm_research"
cd C:\b1\pm_research
python -m pytest tests\test_price_source_option_c_c1a_f1_selector.py -q
```

**Result (sandbox):** `48 passed in 0.05s`. Bare Python 3, no pandas/Store/network exercised. The
`COMPUTED_FROM_LOCAL_TRADES` path is covered via a lazy-import stub proving it restricts to the
bounded condition set (out-of-pool rows excluded) and computes rows=3 / distinct_tx=2 / window=1000
on the fixture — independently re-verified outside pytest as well.

---

## 5. Density fields — approved vs. rejected (enforced in code)

- **Approved (ranking basis):** `local_trade_rows_in_window`,
  `local_distinct_tx_hash_count_in_window`, `window_seconds` — all from local trade rows.
- **Rejected and never used as density:** `observed_point_count_side_0`,
  `observed_point_count_side_1`, `nearest_gap_side_0_seconds`, `nearest_gap_side_1_seconds`,
  `price_history_point_count`, `clob_point_count`, `clob_density` — refused loudly if supplied as a
  density input. Provenance records `used_s1_clob_point_counts_as_density = false` and lists both
  sets.

Density remains a **weak within-pool proxy only** (spec §6.4): no ratio/threshold/cap/filter is
derived from it, and a low-density condition may still explode on a future (separately authorized)
canary.

---

## 6. Standing state unchanged

- P1 remains BLOCKED on the absence of an accepted per-side/token-identity price source.
- C1B, C2, P1/P2/P3, and probe remain unauthorized. `named_binary_probe_blocked` stays `true`.
- No scoring, backfill, wallet discovery, OrdersMatched expansion, `log_index`, PnL, or price-series
  artifact is produced or authorized.
- The accepted C1A `C1_ROW_EXPLOSION` result is untouched; the selector cannot target the exploding
  condition as a disguised single-condition drop (holdout is uniform-only).

---

## 7. Explicit no-authorization statement

**No implementation run, no Dune/API/RPC/network call, no SQL generation or execution, no C1B/C2/
P1/P2/P3/probe, no price artifact, and no scoring/backfill/wallet/`log_index`/PnL work is authorized
by this delivery.** The selector is code/test only and generates no query. A future bounded user-run
would require, in order: (1) this patched implementation reviewed and accepted as scope-compliant,
and (2) a separate, explicit bounded user-run authorization naming the exact accepted selector policy
and caps — per §10 of the governing spec. Delivery is not acceptance; the user may copy these files
into `C:\b1\pm_research` at their discretion.

---

## 8. Files delivered

- `scripts/price_source_option_c_c1a_f1_selector.py`
- `tests/test_price_source_option_c_c1a_f1_selector.py`
- `HANDOFF_orchestrator_option_c_c1a_f1_selector_IMPLEMENTATION.md` (this memo)
