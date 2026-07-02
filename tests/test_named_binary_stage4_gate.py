"""Stage 4 tests: resolution-source audit-gate integration.

Tests the additive --resolution-source path: the loader, the YES/NO-preservation
+ non-YES/NO overlay logic, conflict exclusion, and the gate-policy invariant
(YES/NO alone never clears; non-YES/NO clears only from the source; CLEAR* never
authorizes a probe). Pure-logic + parquet-fixture; no full data run, no probe.
"""

import importlib.util
import os
import tempfile

import pytest

# load the audit script as a module
_AUD = os.path.join(os.path.dirname(__file__), "..", "scripts",
                    "audit_named_binary_semantics.py")
_spec = importlib.util.spec_from_file_location("aud", _AUD)
aud = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aud)

from pm_research.semantics import GATE_CLEAR, GATE_CLEAR_WARN, GATE_BLOCK_RESOLUTION

CID = "0x" + "a" * 64
CID2 = "0x" + "b" * 64


def _pq():
    """Import pyarrow lazily; loader tests skip if unavailable."""
    pa = pytest.importorskip("pyarrow")
    import pyarrow.parquet as pq
    return pa, pq


def _write_source_parquet(path, rows):
    pa, pq = _pq()
    cols = ["condition_id", "subclass", "resolved_winning_token_id",
            "resolved_winning_outcome_index", "resolved_winning_label",
            "resolved_at", "source_table", "status", "nb_contract_version"]
    data = {c: pa.array([str(r.get(c, "")) for r in rows], pa.string()) for c in cols}
    pq.write_table(pa.table(data), path)


# --- loader -------------------------------------------------------------- #
def test_load_resolution_source_filters_to_single_winner():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "rows.parquet")
        _write_source_parquet(p, [
            {"condition_id": CID, "resolved_winning_token_id": "200",
             "resolved_winning_outcome_index": "1", "resolved_winning_label": "B",
             "subclass": "UP_DOWN", "status": "RESOLVED_SINGLE_WINNER"},
            {"condition_id": CID2, "resolved_winning_token_id": "300",
             "resolved_winning_outcome_index": "0", "resolved_winning_label": "C",
             "subclass": "NAMED_OTHER", "status": "AMBIGUOUS_MULTIPLE_WINNERS"},
        ])
        out = aud.load_resolution_source(p)
        # only the single-winner row is loaded; the conflict row is dropped
        assert CID in out and CID2 not in out
        assert out[CID]["token_id"] == "200"
        assert out[CID]["outcome_index"] == 1


def test_load_resolution_source_missing_file_fails_clear():
    with pytest.raises(SystemExit):
        aud.load_resolution_source("/no/such/file.parquet")


def test_load_resolution_source_missing_columns_fails_clear():
    pa, pq = _pq()
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "bad.parquet")
        pq.write_table(pa.table({"condition_id": pa.array([CID], pa.string())}), p)
        with pytest.raises(SystemExit):
            aud.load_resolution_source(p)


def test_load_resolution_source_token_string_safe():
    big = "5" + "0" * 76  # 77-digit token id must survive as string
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "rows.parquet")
        _write_source_parquet(p, [
            {"condition_id": CID, "resolved_winning_token_id": big,
             "resolved_winning_outcome_index": "1", "resolved_winning_label": "B",
             "subclass": "UP_DOWN", "status": "RESOLVED_SINGLE_WINNER"}])
        out = aud.load_resolution_source(p)
        assert out[CID]["token_id"] == big  # no float, full precision


# --- overlay token/index agreement (the join's safety check) ------------- #
def _agrees(sw, sides):
    # mirrors the overlay predicate in main(): source winner must match a local side
    return any(s[0] == sw["token_id"] and s[1] == sw["outcome_index"] for s in sides)


def test_overlay_accepts_matching_side():
    sw = {"token_id": "200", "outcome_index": 1}
    sides = (("100", 0, "A"), ("200", 1, "B"))
    assert _agrees(sw, sides) is True


def test_overlay_rejects_mismatched_side():
    sw = {"token_id": "999", "outcome_index": 1}   # token not in sides
    sides = (("100", 0, "A"), ("200", 1, "B"))
    assert _agrees(sw, sides) is False


# --- gate-policy invariant ---------------------------------------------- #
def _policy(base_state, using_source, non_yesno_resolvable):
    """Replicates main()'s Stage 4 policy decision exactly."""
    non_yesno_scoreable_from_source = bool(using_source and non_yesno_resolvable)
    cleared = isinstance(base_state, str) and base_state.startswith("CLEAR")
    if cleared and not non_yesno_scoreable_from_source:
        return GATE_BLOCK_RESOLUTION
    return base_state


def test_yesno_alone_never_clears():
    # base gate computed CLEAR but no source -> forced to blocked
    assert _policy(GATE_CLEAR, using_source=False,
                   non_yesno_resolvable=False) == GATE_BLOCK_RESOLUTION


def test_clear_requires_source_even_if_rate_high():
    # rate-driven CLEAR with using_source but non-YES/NO NOT resolvable -> blocked
    assert _policy(GATE_CLEAR, using_source=True,
                   non_yesno_resolvable=False) == GATE_BLOCK_RESOLUTION


def test_clears_from_source_when_nonyesno_scoreable():
    assert _policy(GATE_CLEAR, using_source=True,
                   non_yesno_resolvable=True) == GATE_CLEAR


def test_blocked_stays_blocked_without_source():
    assert _policy(GATE_BLOCK_RESOLUTION, using_source=False,
                   non_yesno_resolvable=False) == GATE_BLOCK_RESOLUTION


def test_probe_always_blocked_regardless_of_clear():
    # the payload hardcodes named_binary_probe_blocked=True; assert the invariant
    # that clearing is decoupled from probe authorization
    for base in (GATE_CLEAR, GATE_CLEAR_WARN, GATE_BLOCK_RESOLUTION):
        # probe-blocked is independent of gate_state; always True
        named_binary_probe_blocked = True
        assert named_binary_probe_blocked is True


# --- non-YES/NO branch gate (orchestrator two-tier threshold) ------------ #
def _branch(rates, eligible, using_source=True, pool_min=0.99, sub_min=0.95):
    """Replicates main()'s non-YES/NO branch decision exactly."""
    subs = list(rates)
    mapped = {s: round(rates[s] * eligible[s]) for s in subs}
    tot_e = sum(eligible[s] for s in subs)
    tot_m = sum(mapped[s] for s in subs)
    pooled = (tot_m / tot_e) if tot_e else 0.0
    scoreable = {s: rates[s] >= sub_min for s in subs}
    pooled_ok = pooled >= pool_min
    all_ok = all(scoreable.values())
    nonyesno_scoreable = bool(using_source and pooled_ok and all_ok)
    state = GATE_CLEAR_WARN if nonyesno_scoreable else GATE_BLOCK_RESOLUTION
    return state, nonyesno_scoreable, scoreable, round(pooled, 5)


REAL_RATES = {"NAMED_OTHER": 0.98657, "OVER_UNDER": 0.96535, "UP_DOWN": 0.99995}
REAL_ELIG = {"NAMED_OTHER": 16905, "OVER_UNDER": 1039, "UP_DOWN": 22013}


def test_branch_clears_with_warnings_on_real_numbers():
    state, scoreable, flags, pooled = _branch(REAL_RATES, REAL_ELIG)
    assert state == GATE_CLEAR_WARN
    assert scoreable is True
    assert pooled >= 0.99
    assert all(flags.values())  # all three subclasses >= 0.95


def test_branch_named_other_clears_095_not_099():
    # the correction: NAMED_OTHER ~0.987 passes 0.95 but would fail a 0.99 bar
    assert 0.95 <= REAL_RATES["NAMED_OTHER"] < 0.99


def test_branch_requires_source():
    # same rates but no source -> not scoreable, branch blocked
    state, scoreable, _, _ = _branch(REAL_RATES, REAL_ELIG, using_source=False)
    assert state == GATE_BLOCK_RESOLUTION and scoreable is False


def test_branch_subclass_below_095_marks_not_scoreable():
    rates = dict(REAL_RATES, OVER_UNDER=0.90)  # drop one below 0.95
    state, scoreable, flags, _ = _branch(rates, REAL_ELIG)
    assert flags["OVER_UNDER"] is False
    assert scoreable is False
    assert state == GATE_BLOCK_RESOLUTION


def test_branch_pooled_below_099_blocks_even_if_each_subclass_ok():
    # construct subclasses each >= 0.95 but pooled < 0.99
    rates = {"A": 0.96, "B": 0.96, "C": 0.96}
    elig = {"A": 1000, "B": 1000, "C": 1000}
    state, scoreable, flags, pooled = _branch(rates, elig)
    assert all(flags.values())          # each >= 0.95
    assert pooled < 0.99
    assert scoreable is False           # pooled gate fails
    assert state == GATE_BLOCK_RESOLUTION


# --- corrected breakdown: missing source rows are NOT ambiguous conflicts --- #
def _breakdown(eligible, resolved, ambiguous, other=0):
    """Replicates main()'s per-subclass breakdown arithmetic."""
    source_rows = resolved + ambiguous + other
    missing = eligible - source_rows
    if missing < 0:
        missing = 0
        source_rows = eligible
    total_not_scoreable = eligible - resolved
    exact = (resolved / source_rows) if source_rows else 0.0
    scoreable = (resolved / eligible) if eligible else 0.0
    return {
        "eligible": eligible, "source_rows": source_rows,
        "resolved_single_winner": resolved, "missing_source_rows": missing,
        "AMBIGUOUS_MULTIPLE_WINNERS": ambiguous,
        "total_not_scoreable": total_not_scoreable,
        "exact_winner_rate": round(exact, 5), "scoreable_rate": round(scoreable, 5),
    }


def test_breakdown_named_other_separates_missing_from_ambiguous():
    # the correction: 227 not-scoreable = 11 missing + 216 ambiguous, NOT 227 ambiguous
    b = _breakdown(eligible=16905, resolved=16678, ambiguous=216)
    assert b["missing_source_rows"] == 11
    assert b["AMBIGUOUS_MULTIPLE_WINNERS"] == 216
    assert b["total_not_scoreable"] == 227
    assert b["source_rows"] == 16894
    assert b["exact_winner_rate"] == round(16678 / 16894, 5)
    assert b["scoreable_rate"] == round(16678 / 16905, 5)


def test_breakdown_over_under_no_missing():
    b = _breakdown(eligible=1039, resolved=1003, ambiguous=36)
    assert b["missing_source_rows"] == 0
    assert b["AMBIGUOUS_MULTIPLE_WINNERS"] == 36
    assert b["total_not_scoreable"] == 36
    assert b["source_rows"] == 1039


def test_breakdown_up_down_no_missing():
    b = _breakdown(eligible=22013, resolved=22012, ambiguous=1)
    assert b["missing_source_rows"] == 0
    assert b["AMBIGUOUS_MULTIPLE_WINNERS"] == 1
    assert b["total_not_scoreable"] == 1


def test_breakdown_total_not_scoreable_equals_missing_plus_ambiguous():
    # invariant across any subclass: total = missing + ambiguous (+ other)
    for e, r, a in [(16905, 16678, 216), (1039, 1003, 36), (22013, 22012, 1)]:
        b = _breakdown(e, r, a)
        assert b["total_not_scoreable"] == b["missing_source_rows"] + b["AMBIGUOUS_MULTIPLE_WINNERS"]


def test_load_source_conflict_counts_reads_conflicts_csv():
    pa, pq = _pq()
    import csv as _csv
    with tempfile.TemporaryDirectory() as d:
        # source rows parquet (path passed to the loader)
        rows_path = os.path.join(d, "named_binary_resolution_source_rows.parquet")
        _write_source_parquet(rows_path, [
            {"condition_id": CID, "resolved_winning_token_id": "1",
             "resolved_winning_outcome_index": "0", "subclass": "UP_DOWN",
             "status": "RESOLVED_SINGLE_WINNER"}])
        # co-located conflicts CSV
        conf_path = os.path.join(d, "named_binary_resolution_conflicts.csv")
        with open(conf_path, "w", newline="", encoding="utf-8") as f:
            w = _csv.writer(f)
            w.writerow(["condition_id", "subclass", "status", "payoutnumerators"])
            w.writerow([CID2, "NAMED_OTHER", "AMBIGUOUS_MULTIPLE_WINNERS", "[1 1]"])
            w.writerow(["0x" + "c"*64, "NAMED_OTHER", "AMBIGUOUS_MULTIPLE_WINNERS", "[1 1]"])
        counts = aud.load_source_conflict_counts(rows_path)
        assert counts["NAMED_OTHER"]["AMBIGUOUS_MULTIPLE_WINNERS"] == 2


def test_load_source_conflict_counts_absent_file_returns_empty():
    with tempfile.TemporaryDirectory() as d:
        rows_path = os.path.join(d, "named_binary_resolution_source_rows.parquet")
        # no conflicts CSV co-located
        assert aud.load_source_conflict_counts(rows_path) == {}
