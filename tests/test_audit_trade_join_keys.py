"""Tests for the TRADES join-key audit (scripts/audit_trade_join_keys.py).

The audit's core is the pure function audit(trades_df) -> report dict, so these
test it directly with crafted frames: all-present, all-missing, mixed, missing
columns entirely, blank-strings-as-missing, duplicate diagnostics, and the two
cardinality rules (tx->multi-token benign/counted; token->multi-condition
flagged).
"""
from __future__ import annotations

import importlib.util
import pathlib

import pandas as pd
import pytest

# load the script module by path (scripts/ is not a package everywhere)
_SPEC = importlib.util.spec_from_file_location(
    "audit_trade_join_keys",
    str(pathlib.Path(__file__).resolve().parents[1]
        / "scripts" / "audit_trade_join_keys.py"))
audit_mod = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(audit_mod)
audit = audit_mod.audit


def _trades(rows):
    """rows: list of dicts with any of the TRADES columns."""
    return pd.DataFrame(rows)


BASE = dict(wallet="0xw", condition_id="c1", outcome="YES", side="BUY",
            price=0.5, size_usdc=10.0,
            traded_at=pd.Timestamp("2025-01-01", tz="UTC"))


def _row(i, **over):
    r = dict(BASE)
    r["trade_id"] = f"t{i}"
    r.update(over)
    return r


# --------------------------------------------------------------------------
# population counts
# --------------------------------------------------------------------------
def test_all_keys_present():
    df = _trades([_row(i, tx_hash=f"0xtx{i}", token_id=f"tok{i}") for i in range(5)])
    rep = audit(df)
    assert rep["total_trades"] == 5
    assert rep["tx_hash_present"] == 5 and rep["tx_hash_present_pct"] == 100.0
    assert rep["token_id_present"] == 5
    assert rep["both_present"] == 5 and rep["both_present_pct"] == 100.0


def test_all_keys_missing_via_na():
    df = _trades([_row(i, tx_hash=pd.NA, token_id=pd.NA) for i in range(4)])
    rep = audit(df)
    assert rep["tx_hash_present"] == 0
    assert rep["token_id_present"] == 0
    assert rep["both_present"] == 0 and rep["both_present_pct"] == 0.0


def test_blank_strings_treated_as_missing():
    df = _trades([_row(i, tx_hash="", token_id="   ") for i in range(3)])
    rep = audit(df)
    assert rep["tx_hash_present"] == 0     # "" is missing
    assert rep["token_id_present"] == 0    # whitespace is missing


def test_mixed_missingness():
    rows = [
        _row(0, tx_hash="0xa", token_id="tok0"),   # both
        _row(1, tx_hash="0xb", token_id=""),        # tx only
        _row(2, tx_hash=pd.NA, token_id="tok2"),    # token only
        _row(3, tx_hash="", token_id=pd.NA),        # neither
    ]
    rep = audit(_trades(rows))
    assert rep["tx_hash_present"] == 2
    assert rep["token_id_present"] == 2
    assert rep["both_present"] == 1
    assert rep["both_present_pct"] == pytest.approx(25.0)


def test_missing_columns_entirely_does_not_crash():
    # frame predating the schema change: no tx_hash / token_id columns at all
    rows = [{k: v for k, v in _row(i).items()} for i in range(3)]
    df = _trades(rows)
    assert "tx_hash" not in df.columns and "token_id" not in df.columns
    rep = audit(df)
    assert rep["total_trades"] == 3
    assert rep["has_tx_hash_column"] is False
    assert rep["both_present"] == 0       # treated as missing, no crash


def test_empty_frame():
    rep = audit(_trades([]))
    assert rep["empty"] is True
    assert rep["total_trades"] == 0


# --------------------------------------------------------------------------
# cardinality diagnostics
# --------------------------------------------------------------------------
def test_tx_hash_with_multiple_token_id_counted_not_flagged():
    # one tx, two assets -> benign, counted
    rows = [
        _row(0, tx_hash="0xsame", token_id="tokA"),
        _row(1, tx_hash="0xsame", token_id="tokB"),
    ]
    rep = audit(_trades(rows))
    q = rep["join_key_quality"]
    assert q["tx_hash_with_multiple_token_id"] == 1
    assert "expected" in q["tx_hash_with_multiple_token_id_note"]


def test_token_id_with_multiple_condition_id_flagged():
    # same token mapping to two markets -> suspicious, flagged
    rows = [
        _row(0, tx_hash="0xa", token_id="tokX", condition_id="c1"),
        _row(1, tx_hash="0xb", token_id="tokX", condition_id="c2"),
    ]
    rep = audit(_trades(rows))
    q = rep["join_key_quality"]
    assert q["token_id_with_multiple_condition_id"] == 1
    assert q["token_id_multi_condition_FLAGGED"] is True
    assert "tokX" in q["token_id_multi_condition_examples"]


def test_token_id_single_condition_not_flagged():
    rows = [
        _row(0, tx_hash="0xa", token_id="tokX", condition_id="c1"),
        _row(1, tx_hash="0xb", token_id="tokX", condition_id="c1"),
    ]
    rep = audit(_trades(rows))
    assert rep["join_key_quality"]["token_id_multi_condition_FLAGGED"] is False


def test_duplicate_fingerprint_counted():
    # identical (tx, token, price, size, time) twice -> 1 duplicate
    r = dict(tx_hash="0xa", token_id="tokA", price=0.5, size_usdc=10.0,
             traded_at=pd.Timestamp("2025-01-01", tz="UTC"))
    rows = [_row(0, **r), _row(1, **r)]
    rep = audit(_trades(rows))
    assert rep["join_key_quality"]["duplicate_fingerprint_rows"] == 1


def test_unique_pair_counts():
    rows = [
        _row(0, tx_hash="0xa", token_id="tokA"),
        _row(1, tx_hash="0xa", token_id="tokB"),
        _row(2, tx_hash="0xb", token_id="tokA"),
    ]
    rep = audit(_trades(rows))
    q = rep["join_key_quality"]
    assert q["unique_tx_hash"] == 2
    assert q["unique_token_id"] == 2
    assert q["unique_tx_token_pairs"] == 3


# --------------------------------------------------------------------------
# dimension concentration
# --------------------------------------------------------------------------
def test_missingness_concentrated_by_wallet():
    rows = [
        _row(0, wallet="old", tx_hash=pd.NA, token_id=pd.NA),
        _row(1, wallet="old", tx_hash=pd.NA, token_id=pd.NA),
        _row(2, wallet="new", tx_hash="0xa", token_id="tokA"),
    ]
    rep = audit(_trades(rows))
    dims = rep["missingness_by_dimension"]
    assert dims["wallets_fully_missing"] == 1     # 'old'
    assert dims["wallets_fully_present"] == 1     # 'new'


def test_few_outcomes_show_full_breakdown():
    # <= 6 distinct outcomes -> per-outcome dict emitted
    rows = [_row(0, outcome="YES", tx_hash="0xa", token_id="t0"),
            _row(1, outcome="NO", tx_hash=pd.NA, token_id=pd.NA)]
    rep = audit(_trades(rows))
    dims = rep["missingness_by_dimension"]
    assert "by_outcome_missing" in dims
    assert dims["distinct_outcomes"] == 2


def test_many_named_outcomes_are_summarised_not_dumped():
    # many distinct named outcomes (sports/match markets) -> summary, no flood
    rows = [_row(i, outcome=f"TEAM_{i}", tx_hash=pd.NA, token_id=pd.NA)
            for i in range(20)]
    rep = audit(_trades(rows))
    dims = rep["missingness_by_dimension"]
    assert "by_outcome_missing" not in dims          # not dumped
    assert "by_outcome_missing_summary" in dims
    s = dims["by_outcome_missing_summary"]
    assert s["distinct_outcomes"] == 20
    assert s["outcomes_fully_missing"] == 20


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
