"""Pure-logic tests for Option C C1A selector manifest builder.

No network. No local Store / pandas dependency exercised here (StoreLoader's
real methods are lazy-imported and not invoked by these tests, same discipline
as tests/test_price_source_s1_coverage.py).
"""

import importlib.util
import os
import re
import sys

import pytest

_HERE = os.path.dirname(__file__)
_SCRIPT = os.path.abspath(
    os.path.join(_HERE, "..", "scripts", "price_source_option_c_c1a_manifest.py")
)
_spec = importlib.util.spec_from_file_location("price_source_option_c_c1a_manifest", _SCRIPT)
c1a = importlib.util.module_from_spec(_spec)
sys.modules["price_source_option_c_c1a_manifest"] = c1a
_spec.loader.exec_module(c1a)


def _tok(prefix: str) -> str:
    return prefix + "0" * 74 + "99"


T0 = _tok("1")
T1 = _tok("2")
T2 = _tok("3")

CID_A = "0x" + "a" * 64
CID_B = "0x" + "b" * 64
CID_C = "0x" + "c" * 64
CID_D = "0x" + "d" * 64


def _candidate(cid, **overrides):
    base = {
        "condition_id": cid,
        "window_start_utc": "2025-01-01 00:00:00",
        "window_end_utc": "2025-01-02 00:00:00",
        "source_table_version": "polymarket_polygon.ctfexchange_evt_orderfilled",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# canonical_int / precision discipline
# ---------------------------------------------------------------------------
def test_canonical_int_accepts_plain_integer_string():
    assert c1a.canonical_int("12345") == 12345


def test_canonical_int_rejects_scientific_notation():
    with pytest.raises(c1a.DataExportPrecisionLoss):
        c1a.canonical_int("5.2e76")


def test_canonical_int_rejects_float():
    with pytest.raises(c1a.DataExportPrecisionLoss):
        c1a.canonical_int(5.2)


# ---------------------------------------------------------------------------
# enumerate_token_pair
# ---------------------------------------------------------------------------
def test_enumerate_token_pair_ok():
    tuples = [(CID_A, T0, "0"), (CID_A, T1, "1"), (CID_A, T0, "0")]
    s0, s1, status = c1a.enumerate_token_pair(tuples)
    assert (s0, s1, status) == (T0, T1, c1a.MANIFEST_OK)


def test_enumerate_token_pair_empty_is_unresolved():
    s0, s1, status = c1a.enumerate_token_pair([])
    assert status == c1a.C1_SELECTOR_TOKEN_PAIR_UNRESOLVED
    assert s0 is None and s1 is None


def test_enumerate_token_pair_collapsed_sides_not_exactly_two():
    # Same token appears at both outcome_index 0 and 1 -> collapse.
    tuples = [(CID_A, T0, "0"), (CID_A, T0, "1")]
    _s0, _s1, status = c1a.enumerate_token_pair(tuples)
    assert status == c1a.C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO


def test_enumerate_token_pair_unstable_side_not_exactly_two():
    # Two different tokens both claim outcome_index 0 -> unstable pair.
    tuples = [(CID_A, T0, "0"), (CID_A, T2, "0"), (CID_A, T1, "1")]
    _s0, _s1, status = c1a.enumerate_token_pair(tuples)
    assert status == c1a.C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO


def test_enumerate_token_pair_precision_loss_raises_not_soft_status():
    tuples = [(CID_A, "5.2e76", "0"), (CID_A, T1, "1")]
    with pytest.raises(c1a.DataExportPrecisionLoss):
        c1a.enumerate_token_pair(tuples)


# ---------------------------------------------------------------------------
# Candidate list validation (count, forbidden fields, cap ceilings, windows)
# ---------------------------------------------------------------------------
def test_validate_candidate_list_accepts_valid_3():
    candidates = [_candidate(CID_A), _candidate(CID_B), _candidate(CID_C)]
    c1a.validate_candidate_list(candidates)  # should not raise


def test_validate_candidate_list_rejects_too_few():
    candidates = [_candidate(CID_A), _candidate(CID_B)]
    with pytest.raises(ValueError, match=c1a.STOP_CANDIDATE_COUNT_OUT_OF_RANGE):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_too_many():
    candidates = [_candidate(cid) for cid in [CID_A, CID_B, CID_C, CID_D, "0x" + "e" * 64, "0x" + "f" * 64]]
    with pytest.raises(ValueError, match=c1a.STOP_CANDIDATE_COUNT_OUT_OF_RANGE):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_duplicate_condition_id():
    candidates = [_candidate(CID_A), _candidate(CID_A), _candidate(CID_B)]
    with pytest.raises(ValueError):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_bad_window_order():
    candidates = [
        _candidate(CID_A, window_start_utc="2025-01-02 00:00:00", window_end_utc="2025-01-01 00:00:00"),
        _candidate(CID_B),
        _candidate(CID_C),
    ]
    with pytest.raises(ValueError):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_forbidden_winner_field():
    candidates = [
        _candidate(CID_A, resolved_winning_token_id="999"),
        _candidate(CID_B),
        _candidate(CID_C),
    ]
    with pytest.raises(c1a.OutcomeConditionedInputError):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_per_condition_cap_over_ceiling():
    candidates = [
        _candidate(CID_A, per_condition_row_cap=c1a.PER_CONDITION_ROW_CAP_CEILING + 1),
        _candidate(CID_B),
        _candidate(CID_C),
    ]
    with pytest.raises(ValueError, match=c1a.STOP_ROW_CAP_CEILING_EXCEEDED):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_global_cap_over_ceiling():
    candidates = [
        _candidate(CID_A, global_row_cap=c1a.GLOBAL_ROW_CAP_CEILING + 1),
        _candidate(CID_B),
        _candidate(CID_C),
    ]
    with pytest.raises(ValueError, match=c1a.STOP_ROW_CAP_CEILING_EXCEEDED):
        c1a.validate_candidate_list(candidates)


def test_validate_candidate_list_rejects_bad_condition_id_format():
    candidates = [_candidate("not-a-condition-id"), _candidate(CID_B), _candidate(CID_C)]
    with pytest.raises(ValueError):
        c1a.validate_candidate_list(candidates)


# ---------------------------------------------------------------------------
# build_manifest end to end (pure logic; no I/O)
# ---------------------------------------------------------------------------
def test_build_manifest_all_valid():
    candidates = [_candidate(CID_A), _candidate(CID_B), _candidate(CID_C)]
    contract_map = {CID_A: "UP_DOWN", CID_B: "OVER_UNDER", CID_C: "NAMED_OTHER"}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in (CID_A, CID_B, CID_C)}
    trades_by_condition = {
        c: [(c, T0, "0"), (c, T1, "1")] for c in (CID_A, CID_B, CID_C)
    }
    resolved, excluded = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    assert len(resolved) == 3
    assert len(excluded) == 0
    assert all(r.token_pair_validation_status == c1a.MANIFEST_OK for r in resolved)


def test_build_manifest_excludes_non_oriented_subclass():
    # 4 candidates so 3 can still resolve after CID_A is excluded (YES_NO).
    cids = (CID_A, CID_B, CID_C, CID_D)
    candidates = [_candidate(c) for c in cids]
    contract_map = {CID_A: "YES_NO", CID_B: "OVER_UNDER", CID_C: "NAMED_OTHER", CID_D: "UP_DOWN"}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in cids}
    trades_by_condition = {c: [(c, T0, "0"), (c, T1, "1")] for c in cids}
    resolved, excluded = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    assert CID_A not in {r.condition_id for r in resolved}
    assert any(e.condition_id == CID_A for e in excluded)
    assert len(resolved) == 3


def test_build_manifest_excludes_ambiguous_status():
    # 4 candidates so 3 can still resolve after CID_A is excluded (ambiguous).
    cids = (CID_A, CID_B, CID_C, CID_D)
    candidates = [_candidate(c) for c in cids]
    contract_map = {c: "UP_DOWN" for c in cids}
    resolution_status = {
        CID_A: "AMBIGUOUS_MULTIPLE_WINNERS",
        CID_B: "RESOLVED_SINGLE_WINNER",
        CID_C: "RESOLVED_SINGLE_WINNER",
        CID_D: "RESOLVED_SINGLE_WINNER",
    }
    trades_by_condition = {c: [(c, T0, "0"), (c, T1, "1")] for c in cids}
    resolved, excluded = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    assert CID_A not in {r.condition_id for r in resolved}
    assert len(resolved) == 3


def test_build_manifest_raises_if_too_few_resolve():
    # Only one condition has a usable token pair; the other two have none.
    candidates = [_candidate(CID_A), _candidate(CID_B), _candidate(CID_C)]
    contract_map = {c: "UP_DOWN" for c in (CID_A, CID_B, CID_C)}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in (CID_A, CID_B, CID_C)}
    trades_by_condition = {CID_A: [(CID_A, T0, "0"), (CID_A, T1, "1")], CID_B: [], CID_C: []}
    with pytest.raises(ValueError, match=c1a.STOP_CANDIDATE_COUNT_OUT_OF_RANGE):
        c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)


def test_build_manifest_never_reads_winner_token_field():
    """Structural guard: even if resolution_status dict were (mis-)populated with
    a resolved_winning_token_id-shaped value under an unexpected key, build_manifest
    only ever reads condition_id->status; it has no code path that extracts a
    token id from resolution_status at all."""
    candidates = [_candidate(CID_A), _candidate(CID_B), _candidate(CID_C)]
    contract_map = {c: "UP_DOWN" for c in (CID_A, CID_B, CID_C)}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in (CID_A, CID_B, CID_C)}
    trades_by_condition = {c: [(c, T0, "0"), (c, T1, "1")] for c in (CID_A, CID_B, CID_C)}
    resolved, _excluded = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    for r in resolved:
        assert r.side_0_token_id in (T0, T1)
        assert r.side_1_token_id in (T0, T1)
        assert r.side_0_token_id != r.side_1_token_id


def test_validate_source_table_version_accepts_allowlisted():
    assert (
        c1a.validate_source_table_version("polymarket_polygon.ctfexchange_evt_orderfilled")
        == "polymarket_polygon.ctfexchange_evt_orderfilled"
    )


def test_validate_source_table_version_rejects_bad_format():
    with pytest.raises(ValueError, match=c1a.STOP_SOURCE_TABLE_VERSION_INVALID):
        c1a.validate_source_table_version("polymarket_polygon.ctfexchange_evt_orderfilled; drop table x")


def test_validate_source_table_version_rejects_non_allowlisted():
    with pytest.raises(ValueError, match=c1a.STOP_SOURCE_TABLE_VERSION_INVALID):
        c1a.validate_source_table_version("some_other_schema.some_other_table")


def test_validate_candidate_list_rejects_invalid_source_table_version():
    candidates = [
        _candidate(CID_A, source_table_version="'; drop table x; --"),
        _candidate(CID_B),
        _candidate(CID_C),
    ]
    with pytest.raises(ValueError, match=c1a.STOP_SOURCE_TABLE_VERSION_INVALID):
        c1a.validate_candidate_list(candidates)


# ---------------------------------------------------------------------------
# Dune query rendering (text only, never executed)
# ---------------------------------------------------------------------------
def test_render_dune_query_contains_varchar_casts_and_fixed_bounds():
    candidates = [_candidate(CID_A), _candidate(CID_B), _candidate(CID_C)]
    contract_map = {c: "UP_DOWN" for c in (CID_A, CID_B, CID_C)}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in (CID_A, CID_B, CID_C)}
    trades_by_condition = {c: [(c, T0, "0"), (c, T1, "1")] for c in (CID_A, CID_B, CID_C)}
    resolved, _ = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    sql = c1a.render_dune_query(resolved)
    assert "cast(makerassetid as varchar)" in sql
    assert "cast(takerassetid as varchar)" in sql
    assert "limit" in sql
    assert CID_A in sql and CID_B in sql and CID_C in sql
    # No open-ended time range anywhere in the generated text.
    assert "between timestamp" in sql


def test_render_dune_query_limit_is_cap_plus_one_not_exact_cap():
    """Patch requirement 1: the rendered LIMIT must never equal the exact cap -
    an exact-cap LIMIT would silently truncate and hide row explosion."""
    candidates = [
        _candidate(CID_A, per_condition_row_cap=100),
        _candidate(CID_B, per_condition_row_cap=100),
        _candidate(CID_C, per_condition_row_cap=100),
    ]
    contract_map = {c: "UP_DOWN" for c in (CID_A, CID_B, CID_C)}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in (CID_A, CID_B, CID_C)}
    trades_by_condition = {c: [(c, T0, "0"), (c, T1, "1")] for c in (CID_A, CID_B, CID_C)}
    resolved, _ = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    for r in resolved:
        assert r.per_condition_row_cap == 100
        assert r.dune_query_limit == 101
    sql = c1a.render_dune_query(resolved)
    assert "limit 101" in sql
    assert "limit 100" not in sql


def test_render_dune_query_wraps_each_branch_as_subquery_before_union_all():
    """Second BLOCK fix: a bare `limit N` immediately before `union all` is not
    reliably scoped to just that branch in Trino/Presto (Dune's engine) - it
    must be wrapped as `select * from ( ... limit N )` so the LIMIT
    unambiguously applies per-condition, not to the union's overall result."""
    candidates = [_candidate(CID_A), _candidate(CID_B), _candidate(CID_C)]
    contract_map = {c: "UP_DOWN" for c in (CID_A, CID_B, CID_C)}
    resolution_status = {c: "RESOLVED_SINGLE_WINNER" for c in (CID_A, CID_B, CID_C)}
    trades_by_condition = {c: [(c, T0, "0"), (c, T1, "1")] for c in (CID_A, CID_B, CID_C)}
    resolved, _ = c1a.build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    sql = c1a.render_dune_query(resolved)

    assert sql.count("select * from (") == 3
    assert sql.count("union all") == 2

    # Line-based check on the real SQL body only: find every line that is
    # exactly "  limit N" (the actual per-branch LIMIT clause, not a mention
    # of the word "limit" in a comment), and assert the very next non-blank
    # line is exactly ")" - i.e. the LIMIT is immediately closed by its own
    # subquery's parenthesis, never left bare right before "union all".
    limit_line_re = re.compile(r"^\s*limit \d+\s*$")
    lines = sql.split("\n")
    limit_line_indices = [i for i, line in enumerate(lines) if limit_line_re.match(line)]
    assert len(limit_line_indices) == 3  # one real LIMIT clause per condition
    for idx in limit_line_indices:
        next_line = lines[idx + 1].strip()
        assert next_line == ")", f"LIMIT at line {idx!r} not immediately closed by ')': {next_line!r}"
