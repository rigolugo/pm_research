"""Tests for Stage P0 preflight of the named-binary offline probe.

Aligned to the corrected count model:
  - The resolution-source parquet holds RESOLVED_SINGLE_WINNER rows ONLY.
  - ambiguous_multiple_winners comes from named_binary_resolution_conflicts.csv
    (preferred) or the gate per_subclass_breakdown (fallback).
  - source_rows            = resolved + ambiguous
  - missing_source_rows    = contract_eligible - source_rows
  - final_p0_eligible      = resolved for scoreable subclasses (else 0)

These tests assert each typed STOP state, the exclusion logic, the corrected
count definitions (including the regression case), that probe execution stays
False, that named_binary_probe_blocked is observed but never flipped, and that
no trades/prices loaders are ever called.
"""

import importlib.util
import json
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPT = os.path.join(_HERE, "..", "scripts", "named_binary_probe_p0_preflight.py")
_spec = importlib.util.spec_from_file_location("p0_preflight", _SCRIPT)
p0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p0)

EXPECTED = p0.EXPECTED_CONTRACT_VERSION


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def _nb_dir(root):
    d = os.path.join(root, "named_binary")
    os.makedirs(d, exist_ok=True)
    return d


# Canonical synthetic universe:
#   UP_DOWN     : eligible 4, resolved 2, ambiguous 1  -> source 3, missing 1
#   OVER_UNDER  : eligible 1, resolved 1, ambiguous 0  -> source 1, missing 0
#   NAMED_OTHER : eligible 3, resolved 1, ambiguous 1  -> source 2, missing 1
_UNIVERSE = {
    "UP_DOWN": {"eligible": 4, "resolved": 2, "ambiguous": 1},
    "OVER_UNDER": {"eligible": 1, "resolved": 1, "ambiguous": 0},
    "NAMED_OTHER": {"eligible": 3, "resolved": 1, "ambiguous": 1},
}


def _write_contract(root, version=EXPECTED, universe=_UNIVERSE, include_yes_no=True):
    d = _nb_dir(root)
    conditions = []
    for sc, spec in universe.items():
        for i in range(spec["eligible"]):
            conditions.append(
                {"condition_id": f"0x{sc[:2].lower()}{i}", "subclass": sc,
                 "eligible": True}
            )
    if include_yes_no:
        conditions += [
            {"condition_id": "0xyn0", "subclass": "YES_NO", "eligible": True},
            {"condition_id": "0xyn1", "subclass": "YES_NO", "eligible": True},
        ]
    payload = {"nb_contract_version": version, "conditions": conditions}
    with open(os.path.join(d, "named_binary_classification_contract.json"), "w") as fh:
        json.dump(payload, fh)


def _breakdown(universe=_UNIVERSE):
    bd = {}
    for sc, spec in universe.items():
        source_rows = spec["resolved"] + spec["ambiguous"]
        bd[sc] = {
            "eligible": spec["eligible"],
            "source_rows": source_rows,
            "resolved_single_winner": spec["resolved"],
            "AMBIGUOUS_MULTIPLE_WINNERS": spec["ambiguous"],
            "missing_source_rows": spec["eligible"] - source_rows,
        }
    return bd


def _write_gate(root, state="CLEAR_WITH_WARNINGS", scoreable=None,
                blocked=True, breakdown="default", with_branch=True,
                universe=_UNIVERSE):
    d = _nb_dir(root)
    if scoreable is None:
        scoreable = {"UP_DOWN": True, "OVER_UNDER": True, "NAMED_OTHER": True}
    gate = {
        "gate_state": "BLOCKED_BY_RESOLUTION_MAPPING",
        "named_binary_probe_blocked": blocked,
    }
    if with_branch:
        branch = {
            "non_yesno_gate_state": state,
            "non_yesno_scoreable": all(scoreable.values()),
            "non_yesno_pooled_map_rate": 0.99339,
            "pooled_threshold": 0.99,
            "subclass_threshold": 0.95,
            "per_subclass_map_rate": {
                "UP_DOWN": 0.99995, "OVER_UNDER": 0.96535, "NAMED_OTHER": 0.98657,
            },
            "per_subclass_scoreable": scoreable,
            "named_binary_probe_blocked": blocked,
        }
        if breakdown == "default":
            branch["per_subclass_breakdown"] = _breakdown(universe)
        elif breakdown is not None:
            branch["per_subclass_breakdown"] = breakdown
        gate["stage4_nonyesno_branch"] = branch
    with open(os.path.join(d, "named_binary_audit_gate.json"), "w") as fh:
        json.dump(gate, fh)


def _resolved_rows(universe=_UNIVERSE, version=EXPECTED, include_yes_no=True):
    """RESOLVED_SINGLE_WINNER rows ONLY (mirrors the real parquet)."""
    rows = []
    tok = 100
    for sc, spec in universe.items():
        for i in range(spec["resolved"]):
            tok += 1
            rows.append({
                "condition_id": f"0x{sc[:2].lower()}r{i}", "subclass": sc,
                "status": "RESOLVED_SINGLE_WINNER",
                "resolved_winning_token_id": str(tok),
                "resolved_outcome_index": str(i % 2),
                "nb_contract_version": version,
            })
    if include_yes_no:
        rows.append({
            "condition_id": "0xynr", "subclass": "YES_NO",
            "status": "RESOLVED_SINGLE_WINNER",
            "resolved_winning_token_id": "5", "resolved_outcome_index": "0",
            "nb_contract_version": version,
        })
    return rows


def _conflict_rows(universe=_UNIVERSE):
    """AMBIGUOUS_MULTIPLE_WINNERS rows for the conflicts CSV."""
    rows = []
    for sc, spec in universe.items():
        for i in range(spec["ambiguous"]):
            rows.append({
                "condition_id": f"0x{sc[:2].lower()}a{i}", "subclass": sc,
                "status": "AMBIGUOUS_MULTIPLE_WINNERS",
                "payout_vector": "[1,1]",
            })
    return rows


def _write_rows(root, rows=None):
    import pandas as pd
    d = _nb_dir(root)
    if rows is None:
        rows = _resolved_rows()
    pd.DataFrame(rows).to_parquet(
        os.path.join(d, "named_binary_resolution_source_rows.parquet"), index=False
    )


def _write_conflicts(root, rows=None):
    import pandas as pd
    d = _nb_dir(root)
    if rows is None:
        rows = _conflict_rows()
    pd.DataFrame(rows).to_csv(
        os.path.join(d, "named_binary_resolution_conflicts.csv"), index=False
    )


def _full_setup(root, with_conflicts=True, **kw):
    _write_contract(root, version=kw.get("contract_version", EXPECTED))
    _write_gate(
        root,
        state=kw.get("gate_state", "CLEAR_WITH_WARNINGS"),
        scoreable=kw.get("scoreable"),
        blocked=kw.get("blocked", True),
        breakdown=kw.get("breakdown", "default"),
        with_branch=kw.get("with_branch", True),
    )
    _write_rows(root, rows=kw.get("rows"))
    if with_conflicts:
        _write_conflicts(root, rows=kw.get("conflicts"))


# ---------------------------------------------------------------------------
# Happy path + corrected count definitions
# ---------------------------------------------------------------------------

def test_p0_clear_happy_path(tmp_path):
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "P0_CLEAR"
    assert res["probe_execution_authorized"] is False
    p = res["counts_pooled"]
    # resolved 2+1+1=4 ; ambiguous 1+0+1=2 ; source 6 ; eligible 8 ; missing 2
    assert p["resolved_single_winner"] == 4
    assert p["ambiguous_multiple_winners"] == 2
    assert p["source_rows"] == 6
    assert p["contract_eligible"] == 8
    assert p["missing_source_rows"] == 2
    assert p["final_p0_eligible"] == 4


def test_source_rows_is_resolved_plus_ambiguous_regression(tmp_path):
    """REGRESSION for the P0 count-definition bug: resolved rows live only in the
    source parquet, ambiguous rows only in conflicts; source_rows must still
    equal resolved + ambiguous, and missing = eligible - source_rows."""
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    ud = res["counts_by_subclass"]["UP_DOWN"]
    assert ud["resolved_single_winner"] == 2   # from parquet
    assert ud["ambiguous_multiple_winners"] == 1  # from conflicts csv
    assert ud["source_rows"] == 3              # NOT 2 (the old bug)
    assert ud["missing_source_rows"] == 1      # eligible 4 - source 3
    no = res["counts_by_subclass"]["NAMED_OTHER"]
    assert no["resolved_single_winner"] == 1
    assert no["ambiguous_multiple_winners"] == 1
    assert no["source_rows"] == 2
    assert no["missing_source_rows"] == 1


def test_ambiguous_from_gate_when_conflicts_absent(tmp_path):
    root = str(tmp_path)
    _full_setup(root, with_conflicts=False)  # no conflicts CSV
    res = p0.run_preflight(root)
    assert res["p0_state"] == "P0_CLEAR"
    assert res["excluded_counts"]["ambiguous_source"] == "gate_breakdown_only"
    # ambiguous still taken from gate breakdown
    assert res["counts_pooled"]["ambiguous_multiple_winners"] == 2
    assert res["counts_pooled"]["source_rows"] == 6
    assert res["reconciliation"]["ambiguous_source"] == "gate_breakdown_only"


def test_pooled_sums_subclass_after_yes_no_exclusion(tmp_path):
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    by = res["counts_by_subclass"]
    for key in ("resolved_single_winner", "ambiguous_multiple_winners",
                "source_rows", "contract_eligible", "missing_source_rows",
                "final_p0_eligible"):
        assert res["counts_pooled"][key] == sum(
            by[sc][key] for sc in ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
        )


# ---------------------------------------------------------------------------
# Stop states
# ---------------------------------------------------------------------------

def test_missing_source(tmp_path):
    root = str(tmp_path)
    _write_contract(root)
    _write_gate(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_MISSING_OUTCOME_SOURCE"


def test_empty_source(tmp_path):
    root = str(tmp_path)
    _write_contract(root)
    _write_gate(root)
    _write_rows(root, rows=[])
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_MISSING_OUTCOME_SOURCE"


def test_stale_contract_version(tmp_path):
    root = str(tmp_path)
    _full_setup(root, contract_version="nb-contract-OLD.0")
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_STALE_CONTRACT"


def test_contract_source_version_mismatch(tmp_path):
    root = str(tmp_path)
    _write_contract(root, version=EXPECTED)
    _write_gate(root)
    rows = _resolved_rows(version="nb-contract-2026-06-28.2")
    _write_rows(root, rows=rows)
    _write_conflicts(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_STALE_CONTRACT"


def test_gate_not_clear(tmp_path):
    root = str(tmp_path)
    _full_setup(root, gate_state="BLOCKED_BY_RESOLUTION_MAPPING")
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_DATA_GATE_NOT_CLEAR"


def test_gate_missing_branch(tmp_path):
    root = str(tmp_path)
    _full_setup(root, with_branch=False)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_DATA_GATE_NOT_CLEAR"


def test_precision_loss_scientific_notation(tmp_path):
    root = str(tmp_path)
    rows = _resolved_rows()
    rows[0]["resolved_winning_token_id"] = "5.20896e+76"
    _write_contract(root)
    _write_gate(root)
    _write_rows(root, rows=rows)
    _write_conflicts(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_PRECISION_LOSS"


def test_precision_loss_float_zero(tmp_path):
    root = str(tmp_path)
    rows = _resolved_rows()
    rows[1]["resolved_winning_token_id"] = "0.0"
    _write_contract(root)
    _write_gate(root)
    _write_rows(root, rows=rows)
    _write_conflicts(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_PRECISION_LOSS"


# ---------------------------------------------------------------------------
# Exclusion logic
# ---------------------------------------------------------------------------

def test_yes_no_excluded(tmp_path):
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    assert "YES_NO" not in res["counts_by_subclass"]
    # one YES_NO resolved row in the parquet is excluded + counted
    assert res["excluded_counts"]["yes_no_rows_excluded_source"] == 1
    # two YES_NO contract conditions excluded + counted
    assert res["excluded_counts"]["yes_no_excluded_contract"] == 2


def test_ambiguous_excluded_and_counted(tmp_path):
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    ud = res["counts_by_subclass"]["UP_DOWN"]
    assert ud["ambiguous_multiple_winners"] == 1
    assert ud["final_p0_eligible"] == 2  # ambiguous NOT eligible


def test_missing_excluded_and_counted_separately(tmp_path):
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    ud = res["counts_by_subclass"]["UP_DOWN"]
    # missing derived = eligible - source; never relabeled ambiguous
    assert ud["missing_source_rows"] == 1
    assert ud["ambiguous_multiple_winners"] == 1


def test_non_scoreable_subclass_excluded(tmp_path):
    root = str(tmp_path)
    scoreable = {"UP_DOWN": True, "OVER_UNDER": False, "NAMED_OTHER": True}
    _write_contract(root)
    _write_gate(root, scoreable=scoreable)
    _write_rows(root)
    _write_conflicts(root)
    res = p0.run_preflight(root)
    ou = res["counts_by_subclass"]["OVER_UNDER"]
    assert ou["final_p0_eligible"] == 0
    assert ou["non_scoreable"] == ou["source_rows"]


# ---------------------------------------------------------------------------
# Authorization / block-marker invariants
# ---------------------------------------------------------------------------

def test_probe_execution_remains_false_and_block_not_flipped(tmp_path):
    root = str(tmp_path)
    _full_setup(root, blocked=True)
    res = p0.run_preflight(root)
    assert res["probe_execution_authorized"] is False
    assert res["named_binary_probe_blocked_observed"] is True
    with open(os.path.join(root, "named_binary",
                           "named_binary_audit_gate.json")) as fh:
        gate_on_disk = json.load(fh)
    assert gate_on_disk["named_binary_probe_blocked"] is True


# ---------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------

def test_reconciliation_hard_mismatch_fails(tmp_path):
    root = str(tmp_path)
    bad = _breakdown()
    bad["UP_DOWN"]["resolved_single_winner"] = 99  # disagrees with tally (2)
    _write_contract(root)
    _write_gate(root, breakdown=bad)
    _write_rows(root)
    _write_conflicts(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "STOP_COUNT_RECONCILIATION_FAILED"


def test_reconciliation_source_rows_like_for_like(tmp_path):
    """With conflicts CSV present, source_rows is independently computed and
    must match the gate's source_rows field."""
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    assert res["p0_state"] == "P0_CLEAR"
    assert res["reconciliation"]["exact"] is True
    assert res["reconciliation"]["ambiguous_source"] == "conflicts_csv"


# ---------------------------------------------------------------------------
# Read-only guarantees / artifacts
# ---------------------------------------------------------------------------

def test_no_trades_or_prices_loaded(tmp_path, monkeypatch):
    root = str(tmp_path)
    _full_setup(root)
    import types
    boom = types.ModuleType("pm_research")
    boom_data = types.ModuleType("pm_research.data")
    boom_store = types.ModuleType("pm_research.data.store")

    def _explode(*a, **k):
        raise AssertionError("P0 must not load trades/prices")

    for name in ("load_trades", "load_prices", "load_resolutions", "load_markets"):
        setattr(boom_store, name, _explode)
    boom_data.store = boom_store
    boom.data = boom_data
    monkeypatch.setitem(sys.modules, "pm_research", boom)
    monkeypatch.setitem(sys.modules, "pm_research.data", boom_data)
    monkeypatch.setitem(sys.modules, "pm_research.data.store", boom_store)

    res = p0.run_preflight(root)
    assert res["p0_state"] == "P0_CLEAR"


def test_emit_artifacts_writes_three_files(tmp_path):
    root = str(tmp_path)
    _full_setup(root)
    res = p0.run_preflight(root)
    paths = p0.emit_artifacts(root, res)
    assert os.path.exists(paths["json"])
    assert os.path.exists(paths["md"])
    assert os.path.exists(paths["csv"])
    with open(paths["json"]) as fh:
        on_disk = json.load(fh)
    assert on_disk["stage"] == "P0_PREFLIGHT"
    assert on_disk["authorized_scope"] == "P0_PREFLIGHT_ONLY"
    assert on_disk["probe_execution_authorized"] is False


def test_canonical_int_rejects_sci_and_float():
    with pytest.raises(p0.DataExportPrecisionLoss):
        p0.canonical_int("5.20896e+76")
    with pytest.raises(p0.DataExportPrecisionLoss):
        p0.canonical_int("0.0")
    with pytest.raises(p0.DataExportPrecisionLoss):
        p0.canonical_int(1.0)
    assert p0.canonical_int("0") == "0"
    assert p0.canonical_int("520896") == "520896"
    assert p0.canonical_int(777) == "777"
