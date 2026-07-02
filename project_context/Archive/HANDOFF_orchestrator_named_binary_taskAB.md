# Claude-to-Orchestrator Handoff — Named-Binary Tasks A & B (COMPLETE, real-data verified)

Both tasks done. Task A verified on the full dataset. Task B delivered (spec only).
Named-binary probe remains BLOCKED. No probe was run; none is authorized.

---

## Task A — narrow audit-reporting fix (COMPLETE)

### Exact bug fixed
`determine_schema` (pm_research/semantics/resolution_schema.py) required one
interpretation to map >=99% of the ENTIRE mixed eligible universe, then applied
it globally. The non-YES/NO majority (which structurally cannot map against a
YES/NO-only resolutions feed) dragged the `label` interpretation below 99%, so
`chosen_schema` returned `None` and the gate reported
`resolution_mapping_success_rate=0.0` for EVERYTHING — masking a perfect
8,521/8,521 YES/NO result.

Fix: schema is now selected as the dominant interpretation on the CLEANLY-
MAPPABLE subset. Rows that map under no interpretation are unresolvable
conditions, not votes against the schema. `min_success` now guards agreement
among rows that map at all. If nothing maps, schema is still `None` (true block).
Reporting now includes true per-subclass mapping rates and explicit resolvability
flags.

### Files changed
- `pm_research/semantics/resolution_schema.py` — selection logic fix.
- `scripts/audit_named_binary_semantics.py` — per-subclass reporting, resolvability
  flags, coverage CSV.
- `tests/test_named_binary_semantics.py` — 3 new Issue-A regression tests.

Not touched: Rank 1A/Rank 2 scripts, store.py, schemas.py, Chat2/wallet/probe
code, lexicon.py, named_binary.py, mapping_audit.py.

### Tests run (real environment)
`python -m pytest tests\test_named_binary_semantics.py -q`
=> **37 passed in 0.07s** (34 prior + 3 new Issue-A tests).
(Note: an earlier run showed 2 failures caused by a STALE resolution_schema.py on
disk — the fixed file had not been copied over. After copying the corrected file
and clearing __pycache__, all 37 pass. Root cause was deployment, not logic.)

### Audit run (real data, full 16,505,185 trades / 288,684 conditions, ~92s)
`python scripts\audit_named_binary_semantics.py --root C:\b1\data --out-dir artifacts`

Gate JSON summary:
```
gate_state                       : BLOCKED_BY_RESOLUTION_MAPPING
total_conditions                 : 288684
named_binary_eligible            : 105560
usable_named_binary_conditions   : 8521
token_id_coverage                : 0.99601
outcome_index_coverage           : 0.99601
resolution_mapping_success_rate  : 0.08072
orientation_correctness_rate     : 1.0
resolution_schema_chosen         : label
per_subclass_map_rate            : YES_NO 0.12989 | UP_DOWN 0.0 | OVER_UNDER 0.0 | NAMED_OTHER 0.0
non_yesno_named_binary_resolvable: false
named_binary_probe_blocked       : true
blocked_reason_counts            : RESOLUTION_MAPPING 97039 | FAIL_NOT_EXACTLY_TWO_TOKENS 183123 | LABEL_PAIR_UNMATCHED 1
nb_contract_version              : nb-contract-2026-06-28.1
```

### Before / after (real data)
| field | before | after |
|---|---|---|
| gate_state | BLOCKED_BY_RESOLUTION_MAPPING | BLOCKED_BY_RESOLUTION_MAPPING |
| resolution_schema_chosen | None (bug) | label |
| resolution_mapping_success_rate | 0.0 (misleading) | 0.08072 (true) |
| usable_named_binary_conditions | 0 | 8521 |
| YES_NO mapping | masked 0 | 1.0 of resolved (0.12989 of eligible) |
| UP_DOWN mapping | masked 0 | 0.0 (true) |
| OVER_UNDER mapping | masked 0 | 0.0 (true) |
| NAMED_OTHER mapping | masked 0 | 0.0 (true) |
| orientation_correctness_rate | 1.0 | 1.0 |
| nb_contract_version | nb-contract-2026-06-28.1 | unchanged |

### Reading note (so 0.12989 is not misread)
`YES_NO 0.12989` is resolution-ROW COVERAGE, not mapping correctness: 8,521
resolved of 65,603 eligible YES/NO conditions (~13% have a resolution row; most
are unresolved/open). Of YES/NO conditions that DO have a row, 100% map
(8,521/8,521). Semantics are perfect where outcome data exists; the data is
sparse. `resolution_mapping_success_rate 0.08072` = 8,521/105,560 across all
eligible (incl. the ~80% non-YES/NO that structurally can't resolve locally).

### Probe status
Named-binary probe remains **BLOCKED**. The fix corrected misleading REPORTING
only; it did not make any non-YES/NO market resolvable and did not let the gate
appear to clear named-binary testing. `gate_state` stays
BLOCKED_BY_RESOLUTION_MAPPING; `named_binary_probe_blocked: true` is explicit in
the artifacts.

### Artifacts written (artifacts\)
- named_binary_audit_gate.json / .md (corrected; per-subclass table + resolvability note)
- named_binary_resolution_mapping_coverage.csv (new; per-subclass coverage)
- named_binary_classification_contract.json / .md (unchanged contract; nb_contract_version intact for Chat2)
- named_binary_semantics_report.md

---

## Task B — SPEC_named_binary_resolution_source.md (COMPLETE, spec only)

Delivered. Covers all required points: candidate payout-vector source (CTF
ConditionResolution / PayoutRedemption keyed by condition_id); required fields
(condition_id, winning token_id OR payout vector, outcome_index/label if present,
resolved_at, source tables); Dune precision rules (varchar casts, API CSV,
dtype=str, fail-loud on scientific notation); join/audit gates (condition<->token,
token<->index, exactly-one-winning-side, subclass coverage, conflict detection,
no convergence-derived winners); expected output artifacts; stop conditions; and
an explicit non-authorization list (no probe, no wallet cohort, no PnL, no
live/paper trading, no wallet-copying, no log_index backfill, no full indexer).

The spec builds nothing and authorizes no probe. It gets the branch to "outcomes
exist and are validated," not to "probe."

---

## Decision returned to orchestrator

The named-binary unlock is blocked on realized outcomes that are not in the local
resolutions feed. The fork (per the accepted finding) is the orchestrator's:
1. Build the Dune resolution source per SPEC_named_binary_resolution_source.md
   (the only path that unblocks the probe), or
3. Pause the branch and record the finding.
(Option 2 — fix-and-rebaseline on YES/NO only — is now effectively done by Task A's
reporting fix; it re-enters the Rank 1A-closed YES/NO universe and adds no new
ground.)

Nothing in this handoff authorizes a probe. A future CLEAR* gate on a new outcome
source would make a probe technically runnable but still requires separate
explicit authorization.

---

## Source-of-truth updates recommended (not yet applied)
- DECISION_LOG.md: record "named-binary realized outcomes absent from local
  resolutions.parquet (YES/NO-only); semantics validated; probe blocked pending
  outcome source." (Draft text in FINDINGS_named_binary_resolution_blocker.md.)
- PROJECT_STATE.md: named-binary semantics DONE+gated; probe BLOCKED pending
  non-YES/NO outcomes; SPEC_named_binary_resolution_source.md is the next unit if
  the orchestrator chooses to unblock.
- ARTIFACT_INDEX.md: add the semantics package, audit/diagnostic scripts, and the
  new artifacts.

## Unresolved assumptions (spec §10; none block Task A)
- A1: CTF ConditionResolution payout-vector tables present/current on Dune for in-scope markets.
- A2: Dune condition_id matches local byte-for-byte or needs normalization.
- A3: any non-YES/NO markets resolving via a mechanism not captured by payout vectors (caps coverage).
- A4: per-subclass coverage threshold for the gate to call non-YES/NO "scoreable" (orchestrator policy).

## Offered, not done (awaiting your go-ahead)
- Dated `__version__` marker on each semantics module + audit echo, so a stale
  file is a one-glance check (this round cost a debugging cycle to a stale file).
- Draft DECISION_LOG / PROJECT_STATE / ARTIFACT_INDEX diff text for the above.
