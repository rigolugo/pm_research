"""Tests for scripts/audit_market_structure.py and pm_research/splits.py."""
from __future__ import annotations

import importlib.util
import pathlib
from datetime import date

import pandas as pd
import pytest

from pm_research.splits import rolling_train_test_splits

_spec = importlib.util.spec_from_file_location(
    "audit_market_structure",
    str(pathlib.Path(__file__).resolve().parents[1]
        / "scripts" / "audit_market_structure.py"))
ams = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ams)


# ---------------- splits ----------------
def test_splits_train_precedes_test_and_tiles_span():
    sp = rolling_train_test_splits(date(2025, 1, 1), date(2026, 1, 1), 5)
    assert len(sp) == 5
    for (trs, tre, tes, tee) in sp:
        assert trs < tre <= tes < tee          # train before test, no overlap
    assert sp[-1][3] == date(2026, 1, 1)        # last test ends at span_end


def test_splits_validation():
    with pytest.raises(ValueError):
        rolling_train_test_splits(date(2025, 1, 1), date(2025, 1, 1), 5)  # zero span
    with pytest.raises(ValueError):
        rolling_train_test_splits(date(2025, 1, 1), date(2026, 1, 1), 0)  # n<1


# ---------------- classification ----------------
def _trades(rows):
    return pd.DataFrame(rows)


def _row(cid, tok, oi, outcome, tid, traded_at="2025-06-01"):
    return {"trade_id": tid, "wallet": "0xw", "condition_id": cid,
            "outcome": outcome, "side": "BUY", "price": 0.5, "size_usdc": 10.0,
            "traded_at": pd.Timestamp(traded_at, tz="UTC"),
            "tx_hash": "0xtx", "token_id": tok, "outcome_index": oi}


def test_binary_yesno_two_tokens_is_usable():
    trades = _trades([
        _row("c1", "tokA", 0, "YES", "t1"),
        _row("c1", "tokB", 1, "NO", "t2"),
    ])
    markets = pd.DataFrame({"condition_id": ["c1"], "category": ["Sports"],
                            "liquidity_usdc": [100.0]})
    res = pd.DataFrame({"condition_id": ["c1"], "winning_outcome": ["YES"],
                        "resolved_at": [pd.Timestamp("2025-07-01", tz="UTC")]})
    cc = ams.classify_conditions(trades, markets, res, {"c1"})
    row = cc.iloc[0]
    assert row["class"] == "binary" and row["usable"]
    assert row["has_category"]


def test_named_binary_two_tokens_named_labels_not_usable():
    trades = _trades([
        _row("c2", "tokA", 0, "LAKERS", "t1"),
        _row("c2", "tokB", 1, "CELTICS", "t2"),
    ])
    res = pd.DataFrame({"condition_id": ["c2"], "winning_outcome": ["LAKERS"],
                        "resolved_at": [pd.Timestamp("2025-07-01", tz="UTC")]})
    cc = ams.classify_conditions(trades, pd.DataFrame(
        columns=["condition_id", "category", "liquidity_usdc"]), res, {"c2"})
    row = cc.iloc[0]
    assert row["class"] == "named_binary" and not row["usable"]


def test_multi_outcome_three_tokens():
    trades = _trades([
        _row("c3", "tokA", 0, "A", "t1"), _row("c3", "tokB", 1, "B", "t2"),
        _row("c3", "tokC", 2, "C", "t3"),
    ])
    cc = ams.classify_conditions(trades, pd.DataFrame(
        columns=["condition_id", "category", "liquidity_usdc"]),
        pd.DataFrame(columns=["condition_id", "winning_outcome", "resolved_at"]),
        set())
    assert cc.iloc[0]["class"] == "multi" and not cc.iloc[0]["usable"]


def test_cardinality_contradiction_unusable():
    # 2 tokens but 3 distinct labels -> contradiction
    trades = _trades([
        _row("c4", "tokA", 0, "YES", "t1"),
        _row("c4", "tokB", 1, "NO", "t2"),
        _row("c4", "tokA", 0, "MAYBE", "t3"),
    ])
    cc = ams.classify_conditions(trades, pd.DataFrame(
        columns=["condition_id", "category", "liquidity_usdc"]),
        pd.DataFrame(columns=["condition_id", "winning_outcome", "resolved_at"]),
        set())
    assert cc.iloc[0]["class"] == "unusable"
    assert cc.iloc[0]["reason"].startswith("cardinality_contradiction")


def test_binary_unresolved_or_unpriced_not_usable():
    trades = _trades([_row("c5", "tokA", 0, "YES", "t1"),
                      _row("c5", "tokB", 1, "NO", "t2")])
    mk = pd.DataFrame(columns=["condition_id", "category", "liquidity_usdc"])
    # resolved but no price
    cc = ams.classify_conditions(trades, mk, pd.DataFrame(
        {"condition_id": ["c5"], "winning_outcome": ["YES"],
         "resolved_at": [pd.Timestamp("2025-07-01", tz="UTC")]}), set())
    assert cc.iloc[0]["class"] == "binary" and not cc.iloc[0]["usable"]
    assert cc.iloc[0]["reason"] == "no_price_series"


# ---------------- gate logic ----------------
def _base_metrics(**over):
    m = {"outcome_index_present_pct": 100.0, "token_multi_condition_count": 0,
         "cardinality_contradiction_count": 0, "categories_meeting_bar": 0,
         "aggregate_binary_meets_bar": False}
    m.update(over); return m


_PARAMS = {"max_residual_na_pct": 20.0, "max_suspicious": 0,
           "max_contradictions": 0, "min_categories": 3}


def test_gate_blocked_semantics_low_outcome_index():
    m = _base_metrics(outcome_index_present_pct=50.0)
    assert ams.decide_gate(m, _PARAMS) == "BLOCKED_SEMANTICS"


def test_gate_blocked_semantics_suspicious_tokens():
    m = _base_metrics(token_multi_condition_count=5)
    assert ams.decide_gate(m, _PARAMS) == "BLOCKED_SEMANTICS"


def test_gate_blocked_semantics_contradictions():
    m = _base_metrics(cardinality_contradiction_count=3)
    assert ams.decide_gate(m, _PARAMS) == "BLOCKED_SEMANTICS"


def test_gate_category_specialist():
    m = _base_metrics(categories_meeting_bar=3, aggregate_binary_meets_bar=True)
    assert ams.decide_gate(m, _PARAMS) == "PASS_CATEGORY_SPECIALIST"


def test_gate_binary_only_when_categories_thin():
    m = _base_metrics(categories_meeting_bar=1, aggregate_binary_meets_bar=True)
    assert ams.decide_gate(m, _PARAMS) == "PASS_BINARY_ONLY"


def test_gate_insufficient_sample():
    m = _base_metrics(categories_meeting_bar=0, aggregate_binary_meets_bar=False)
    assert ams.decide_gate(m, _PARAMS) == "BLOCKED_INSUFFICIENT_SAMPLE"


def test_gate_precedence_semantics_beats_everything():
    # even with categories meeting the bar, bad semantics blocks
    m = _base_metrics(outcome_index_present_pct=10.0, categories_meeting_bar=5,
                      aggregate_binary_meets_bar=True)
    assert ams.decide_gate(m, _PARAMS) == "BLOCKED_SEMANTICS"


# ---------------- per-split counting ----------------
def test_meets_bar_robustness():
    # 4 of 5 splits clear (100 train / 50 test); one fails -> meets at 4/5
    per_split = [(120, 60), (110, 55), (130, 70), (90, 40), (105, 51)]
    assert ams._meets_bar(per_split, 100, 50, 4) is True
    # only 3 clear -> fails at robust=4
    per_split2 = [(120, 60), (110, 55), (130, 70), (90, 40), (80, 30)]
    assert ams._meets_bar(per_split2, 100, 50, 4) is False


# ---------------- end-to-end ----------------
def test_empty_trades_blocked_insufficient():
    rep = ams.audit_market_structure(
        pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), set(),
        {"splits": 5, "robust_pass_splits": 4, "min_test_signals_per_split": 50,
         "min_train_signals_per_split": 100, "min_categories": 3,
         "max_residual_na_pct": 20.0, "max_suspicious": 0,
         "max_contradictions": 0, "span_start": date(2025, 1, 1),
         "span_end": date(2026, 1, 1)})
    assert rep["verdict"] == "BLOCKED_INSUFFICIENT_SAMPLE"
    assert rep["empty"] is True


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))


# ---------------- streaming path ----------------
import pathlib as _pathlib


def _install_fake_parquet(monkeypatch, files: dict):
    """Make ams.pd.read_parquet + Path.glob read from an in-memory {name: df}."""
    def fake_glob(self, pat):
        return [_pathlib.Path("/fake") / n for n in files]
    def fake_read_parquet(fp, columns=None):
        df = files[_pathlib.Path(fp).name].copy()
        if columns:
            return df[[c for c in columns if c in df.columns]]
        return df
    monkeypatch.setattr(ams.pd, "read_parquet", fake_read_parquet)
    monkeypatch.setattr(_pathlib.Path, "glob", fake_glob)


def _trow(cid, tok, oi, outcome, tid, t="2025-06-01", tx="0xtx"):
    return {"trade_id": tid, "wallet": "0xw", "condition_id": cid,
            "outcome": outcome, "side": "BUY", "price": 0.5, "size_usdc": 10.0,
            "traded_at": pd.Timestamp(t, tz="UTC"),
            "tx_hash": tx, "token_id": tok, "outcome_index": oi}


def test_stream_accumulates_tokens_across_files(monkeypatch):
    # bin1 is split across two files: must gather BOTH tokens
    files = {
        "wA.parquet": pd.DataFrame([_trow("bin1", "TA", 0, "YES", "t1")]),
        "wB.parquet": pd.DataFrame([_trow("bin1", "TB", 1, "NO", "t2")]),
    }
    _install_fake_parquet(monkeypatch, files)
    agg, diag = ams.stream_condition_aggregates(_pathlib.Path("/fake"))
    assert diag["files"] == 2 and diag["total_rows"] == 2
    assert agg["bin1"]["tokens"] == {"TA", "TB"}      # cross-file
    assert agg["bin1"]["labels"] == {"YES", "NO"}


def test_stream_flags_zero_key_file(monkeypatch):
    files = {
        "good.parquet": pd.DataFrame([_trow("c1", "TA", 0, "YES", "t1")]),
        "bad.parquet": pd.DataFrame([_trow("c2", "", None, "X", "t2", tx="")]),
    }
    _install_fake_parquet(monkeypatch, files)
    agg, diag = ams.stream_condition_aggregates(_pathlib.Path("/fake"))
    assert "bad.parquet" in [f[0] for f in diag["zero_key_files"]]
    assert diag["rows_missing_any_key"] == 1


def test_stream_counts_partial_key_file(monkeypatch):
    files = {"mix.parquet": pd.DataFrame([
        _trow("c1", "TA", 0, "YES", "t1"),
        _trow("c1", "", None, "NO", "t2", tx=""),   # one missing-key row
    ])}
    _install_fake_parquet(monkeypatch, files)
    agg, diag = ams.stream_condition_aggregates(_pathlib.Path("/fake"))
    assert any(f[0] == "mix.parquet" for f in diag["partial_key_files"])
    assert diag["rows_missing_any_key"] == 1


def test_stream_duplicate_trade_id_detected(monkeypatch):
    files = {
        "a.parquet": pd.DataFrame([_trow("c1", "TA", 0, "YES", "dup")]),
        "b.parquet": pd.DataFrame([_trow("c1", "TA", 0, "YES", "dup")]),  # same tid
    }
    _install_fake_parquet(monkeypatch, files)
    agg, diag = ams.stream_condition_aggregates(_pathlib.Path("/fake"))
    assert diag["duplicate_trade_id_rows"] == 1


def test_streaming_classification_matches_inmemory(monkeypatch):
    # same data via streaming vs in-memory must classify identically
    rows = [_trow("bin1", "TA", 0, "YES", "t1"), _trow("bin1", "TB", 1, "NO", "t2"),
            _trow("multi1", "MA", 0, "X", "t3"), _trow("multi1", "MB", 1, "Y", "t4"),
            _trow("multi1", "MC", 2, "Z", "t5")]
    mk = pd.DataFrame({"condition_id": ["bin1"], "category": ["Sports"],
                       "liquidity_usdc": [1.0]})
    res = pd.DataFrame({"condition_id": ["bin1"], "winning_outcome": ["YES"],
                        "resolved_at": [pd.Timestamp("2025-07-01", tz="UTC")]})
    # in-memory
    cc_mem = ams.classify_conditions(pd.DataFrame(rows), mk, res, {"bin1"})
    cls_mem = dict(zip(cc_mem["condition_id"], cc_mem["class"]))
    # streaming
    _install_fake_parquet(monkeypatch, {"w.parquet": pd.DataFrame(rows)})
    agg, diag = ams.stream_condition_aggregates(_pathlib.Path("/fake"))
    cc_str = ams.classify_from_aggregates(agg, mk, res, {"bin1"})
    cls_str = dict(zip(cc_str["condition_id"], cc_str["class"]))
    assert cls_mem == cls_str
    assert cls_str["bin1"] == "binary" and cls_str["multi1"] == "multi"


def test_streaming_audit_emits_streaming_diagnostics(monkeypatch):
    files = {"w.parquet": pd.DataFrame([
        _trow("bin1", "TA", 0, "YES", "t1"), _trow("bin1", "TB", 1, "NO", "t2")])}
    _install_fake_parquet(monkeypatch, files)
    mk = pd.DataFrame(columns=["condition_id", "category", "liquidity_usdc"])
    res = pd.DataFrame({"condition_id": ["bin1"], "winning_outcome": ["YES"],
                        "resolved_at": [pd.Timestamp("2025-07-01", tz="UTC")]})
    P = {"splits": 5, "robust_pass_splits": 4, "min_test_signals_per_split": 50,
         "min_train_signals_per_split": 100, "min_categories": 3,
         "max_residual_na_pct": 20.0, "max_suspicious": 0,
         "max_contradictions": 0, "span_start": date(2025, 1, 1),
         "span_end": date(2026, 1, 1)}
    rep = ams.audit_streaming(_pathlib.Path("/fake"), mk, res, {"bin1"}, P)
    for k in ["files_scanned", "zero_key_file_count", "partial_key_file_count",
              "rows_missing_any_key", "rows_missing_any_key_pct",
              "usable_via_token_rule", "usable_via_label_fallback"]:
        assert k in rep
    assert rep["verdict"] in ("PASS_CATEGORY_SPECIALIST", "PASS_BINARY_ONLY",
                              "BLOCKED_SEMANTICS", "BLOCKED_INSUFFICIENT_SAMPLE")


def test_streaming_empty_dir(monkeypatch):
    _install_fake_parquet(monkeypatch, {})
    rep = ams.audit_streaming(_pathlib.Path("/fake"), pd.DataFrame(),
                              pd.DataFrame(), set(),
                              {"splits": 5, "robust_pass_splits": 4,
                               "min_test_signals_per_split": 50,
                               "min_train_signals_per_split": 100,
                               "min_categories": 3, "max_residual_na_pct": 20.0,
                               "max_suspicious": 0, "max_contradictions": 0,
                               "span_start": date(2025, 1, 1),
                               "span_end": date(2026, 1, 1)})
    assert rep["verdict"] == "BLOCKED_INSUFFICIENT_SAMPLE"
