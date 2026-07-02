"""Stage 3 builder tests. Exercises the builder's CSV reading, winner derivation
wiring, conflict isolation, precision failure, and coverage math against tiny
fixtures. Pure-logic paths run without pyarrow; the parquet-write path is checked
only if pyarrow is importable.
"""

import csv
import importlib.util
import json
import os
import sys
import tempfile

import pytest

# load the builder module by path (it's a script, not a package module)
_BUILDER = os.path.join(os.path.dirname(__file__), "..", "scripts",
                        "build_named_binary_resolution_source.py")
_spec = importlib.util.spec_from_file_location("nb_builder", _BUILDER)
b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b)

from pm_research.semantics import (
    DataExportPrecisionLoss, RESOLVED_SINGLE_WINNER, AMBIGUOUS_MULTIPLE_WINNERS,
    MALFORMED_PAYOUT_VECTOR,
)


def _write_csv(path, rows, header):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header)
        for r in rows:
            w.writerow(r)


CID1 = "0x" + "a" * 64
CID2 = "0x" + "b" * 64
HEADER = ["condition_id", "outcomeslotcount", "payoutnumerators", "resolved_at"]


def test_load_resolution_csv_dtype_str_and_normalizes():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.csv")
        _write_csv(p, [[CID1.upper(), "2", "[0 1]", "2025-01-01"]], HEADER)
        out = b.load_resolution_csv(p)
        # uppercase condition_id normalized to lowercase 0x key
        assert CID1 in out
        assert out[CID1]["payoutnumerators"] == "[0 1]"


def test_load_resolution_csv_fails_loud_on_scientific_notation():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.csv")
        _write_csv(p, [[CID1, "2", "[5.2e+76 0]", "2025-01-01"]], HEADER)
        with pytest.raises(DataExportPrecisionLoss):
            b.load_resolution_csv(p)


def test_load_resolution_csv_flags_duplicate_different_payout():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.csv")
        _write_csv(p, [[CID1, "2", "[0 1]", "t"],
                       [CID1, "2", "[1 0]", "t"]], HEADER)
        out = b.load_resolution_csv(p)
        assert out[CID1].get("__dup_conflict__") == "1"


def test_resolve_one_wiring_single_winner():
    # exercise resolve_one through the builder's import surface
    sides = (("100", 0, "A"), ("200", 1, "B"))
    rr = b.resolve_one(CID1, "[0 1]", sides)
    assert rr.status == RESOLVED_SINGLE_WINNER
    assert rr.resolved_winning_token_id == "200"
    assert rr.resolved_winning_outcome_index == 1


def test_resolve_one_wiring_multiple_winner_conflict():
    sides = (("100", 0, "A"), ("200", 1, "B"))
    assert b.resolve_one(CID1, "[1 1]", sides).status == AMBIGUOUS_MULTIPLE_WINNERS


def test_resolve_one_wiring_three_slot_malformed():
    sides = (("100", 0, "A"), ("200", 1, "B"))
    assert b.resolve_one(CID1, "[0 1 0]", sides).status == MALFORMED_PAYOUT_VECTOR


def test_coverage_writer_schema_stable():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "cov.csv")
        elig = {"UP_DOWN": 10, "NAMED_OTHER": 5}
        source = {"UP_DOWN": 9, "NAMED_OTHER": 5}
        from collections import defaultdict
        per_sub = defaultdict(lambda: defaultdict(int))
        per_sub["UP_DOWN"][RESOLVED_SINGLE_WINNER] = 8
        per_sub["UP_DOWN"][AMBIGUOUS_MULTIPLE_WINNERS] = 1
        per_sub["NAMED_OTHER"][RESOLVED_SINGLE_WINNER] = 5
        cov = b._write_coverage(p, elig, source, per_sub)
        # stable header present
        with open(p) as f:
            header = f.readline().strip().split(",")
        assert header[:4] == ["subclass", "eligible", "source_rows", "resolved_single_winner"]
        assert "exact_winner_rate" in header and "coverage_rate" in header
        # math
        assert cov["UP_DOWN"]["resolved_single_winner"] == 8
        assert abs(cov["UP_DOWN"]["exact_winner_rate"] - 8/9) < 1e-6
        assert abs(cov["UP_DOWN"]["coverage_rate"] - 9/10) < 1e-6


def test_conflicts_writer_includes_status():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "conf.csv")
        b._write_conflicts(p, [(CID1, "UP_DOWN", "AMBIGUOUS_MULTIPLE_WINNERS", "[1 1]")])
        with open(p) as f:
            rows = list(csv.reader(f))
        assert rows[0] == ["condition_id", "subclass", "status", "payoutnumerators"]
        assert rows[1][2] == "AMBIGUOUS_MULTIPLE_WINNERS"


@pytest.mark.skipif(importlib.util.find_spec("pyarrow") is None,
                    reason="pyarrow not available")
def test_rows_parquet_write_roundtrip():
    import pyarrow.parquet as pq
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "rows.parquet")
        rows = [{"condition_id": CID1, "subclass": "UP_DOWN",
                 "resolved_winning_token_id": "200",
                 "resolved_winning_outcome_index": 1,
                 "resolved_winning_label": "B", "resolved_at": "t",
                 "source_table": b.SOURCE_TABLE, "status": RESOLVED_SINGLE_WINNER,
                 "nb_contract_version": "nb-contract-2026-06-28.1"}]
        b._write_rows_parquet(p, rows)
        tbl = pq.read_table(p)
        assert tbl.num_rows == 1
        # token id preserved as string (no float)
        assert tbl.column("resolved_winning_token_id")[0].as_py() == "200"


def test_rows_parquet_empty_schema_stable():
    # empty input still writes a stable-schema table (or csv fallback)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "rows.parquet")
        b._write_rows_parquet(p, [])
        # either the parquet or the csv fallback exists
        assert os.path.exists(p) or os.path.exists(p.replace(".parquet", ".csv"))
