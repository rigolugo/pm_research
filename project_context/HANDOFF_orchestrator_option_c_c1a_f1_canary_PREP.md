# HANDOFF — Orchestrator: Option C C1A-F1 bounded canary PREP package

**Decision:** APPROVE PREP ONLY — bounded C1A-F1 canary SQL and manifest package prepared from accepted selector artifacts.

**Scope:** PREP ONLY. No Dune execution, no API/RPC/network call, no SQL execution, no C1B/C2/P1/P2/P3/probe, no price artifact, no scoring/backfill/wallet/OrdersMatched/`log_index`/PnL, no cap increase, no truncation, no local-`tx_hash` filtering, no Dune count scouting, and no winner/outcome/PnL/score fields.

---

## 1. Inputs used

Accepted C1A-F1 selector artifacts:

- `c1a_f1_windows.json`
- `c1a_f1_windows.json.provenance.json`
- `c1a_f1_selector_provenance.json`
- `c1a_f1_selected_conditions.csv`
- `c1a_f1_selector_excluded.csv`

Accepted selected conditions:

1. `OVER_UNDER` — `0xf7361f4c577945b89d4a537eda2acd3cceb1e22cb722c8a48a3114eff058b8d7`
2. `NAMED_OTHER` — `0x2bd2a48746fbdecf0555bfe8f5138340341ac3909c7fb5bdf281293039e97148`
3. `UP_DOWN` — `0x8f08f282ea61a9a8ec2b22413e2a8764487eea351337fd14f4409ca34151dec7`

The prepared SQL and manifest use token pairs from `c1a_f1_selected_conditions.csv` and windows from `c1a_f1_windows.json`.

---

## 2. Manifest gap closed

The accepted local C1A canary consumer requires `--manifest`. This prep package now writes:

```text
artifacts/named_binary_probe/price_source_option_c_c1a_f1/c1a_f1_canary_manifest.json
```

The manifest includes only:

- `conditions[]`
- `condition_id`
- `side_0_token_id`
- `side_1_token_id`
- `window_start_utc`
- `window_end_utc`
- `per_condition_row_cap`
- `global_row_cap`

No winner, resolution-winner, outcome, PnL, score, or local `tx_hash` fields/lists are included.

---

## 3. Source-table handling

The prepared SQL uses only the two accepted decoded `OrderFilled` tables:

- `polymarket_polygon.ctfexchange_evt_orderfilled`
- `polymarket_polygon.negriskctfexchange_evt_orderfilled`

No OrdersMatched table, wallet table, price table, PnL table, score table, winner table, or outcome table appears.

---

## 4. Prepared files

- `price_source_option_c_c1a_f1_prepare_canary.py` — local-only prep helper; writes inert SQL and manifest.
- `c1a_f1_dune_query.sql` — generated SQL text, PREP ONLY.
- `c1a_f1_canary_manifest.json` — generated manifest consumed by `scripts/price_source_option_c_c1a_canary.py --manifest` after separate authorization.
- `README_price_source_option_c_c1a_f1_canary_prep.md` — runbook; explicitly says not to execute SQL or downstream canary until separate Orchestrator authorization.
- `test_price_source_option_c_c1a_f1_canary_prep.py` — local tests for SQL, manifest, and guardrails.
- `HANDOFF_orchestrator_option_c_c1a_f1_canary_PREP.md` — this handoff.

---

## 5. Guardrails verified by tests

Tests verify:

- manifest exists;
- manifest has exactly 3 conditions;
- IDs match accepted selected conditions;
- token IDs and windows match selector artifacts;
- caps are 2000/6000;
- no forbidden winner/outcome/PnL/score/local_tx fields are present;
- generated SQL and manifest refer to the same condition IDs;
- no prior C1A exploding-condition logic is present;
- no local `tx_hash` filter exists;
- cap+1 over-fetch is preserved (`LIMIT 2001` for `per_condition_row_cap = 2000`);
- branch limits are subquery-wrapped;
- decoded `OrderFilled` tables only;
- no SQL execution or network path exists in the prep helper.

Sandbox verification:

```text
14 passed
```

---

## 6. Local generation command

```cmd
python scripts\price_source_option_c_c1a_f1_prepare_canary.py --selected-csv artifacts\named_binary_probe\price_source_option_c_c1a_f1\c1a_f1_selected_conditions.csv --windows-json artifacts\named_binary_probe\price_source_option_c_c1a_f1\c1a_f1_windows.json --out-sql artifacts\named_binary_probe\price_source_option_c_c1a_f1\c1a_f1_dune_query.sql --out-manifest artifacts\named_binary_probe\price_source_option_c_c1a_f1\c1a_f1_canary_manifest.json
```

## 7. Local test command

```cmd
python -m pytest tests\test_price_source_option_c_c1a_f1_canary_prep.py -q
```

---

## 8. Standing state

This package prepares inert SQL, a manifest, and review files only. It does not authorize the user to paste or run the SQL and does not authorize running the canary consumer against a Dune export. A bounded C1A-F1 Dune run requires separate explicit Orchestrator authorization.

No Dune execution or downstream work is authorized.
