"""
Tests for scripts/price_source_s1_alt_pass1_coverage.py (Option A S1-ALT Pass 1).

Pure-logic / mocked -- NO network, NO pandas, NO real Store, NO real filesystem
except a handful of tmp_path-based writer/CSV-reconstruction tests. Every
FakeLoader/FakeWriter double lives in this file; nothing here imports pandas or
pm_research.
"""

from __future__ import annotations

import ast
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import price_source_s1_alt_pass1_coverage as mod  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def _write_csv(path: Path, header: List[str], rows: List[List[Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for row in rows:
            w.writerow(row)


def _make_valid_s1_sample_csvs(
    tmp_path: Path, variant: str = "real", excluded_reason_style: str = "bare"
) -> Tuple[Path, Path]:
    """
    Builds a pair of CSVs matching the accepted S1 Pass-1 shape.

    Pinned target: 300-condition sample = 248 measured (50 UP_DOWN / 98
    OVER_UNDER / 100 NAMED_OTHER, each carrying a real Level-B class) + 52
    invalid-window (NO_VALID_DECISION_WINDOW_AFTER_WARMUP).

    variant="real" (the accepted run's actual shape): the by-condition ledger
    carries ALL 300 rows (248 measured + the 52 invalid-window rows, the latter
    with level_b_class=NO_VALID_DECISION_WINDOW_AFTER_WARMUP), and the excluded
    ledger carries the SAME 52 ids. The 52-id overlap is expected.

    variant="disjoint": the by-condition ledger carries only the 248 measured
    rows and the excluded ledger carries the 52 invalid ids (no overlap). Both
    variants must reconstruct to the identical 300/248/52 split.

    excluded_reason_style="bare": excluded-ledger `reason` is exactly
    "NO_VALID_DECISION_WINDOW_AFTER_WARMUP".
    excluded_reason_style="diagnostic_suffix": excluded-ledger `reason` bundles
    the class with a parenthesized diagnostic suffix, per the REAL accepted
    shape and the user's reported failure_detail, e.g.
    "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts=1776408162,
    decision_lower_ts=1776411762, resolved_at_ts=1776408318, window_seconds=-3444)".
    """
    by_cond = tmp_path / "by_condition.csv"
    excluded = tmp_path / "excluded.csv"

    measured = []
    counter = 0
    for subclass, n in (("UP_DOWN", 50), ("OVER_UNDER", 98), ("NAMED_OTHER", 100)):
        for _ in range(n):
            # by-condition measured rows: condition_id, subclass, level_b_class
            measured.append([f"0xmeasured{counter:05d}", subclass, "DECISION_PRICE_NEITHER"])
            counter += 1

    invalid_ids = [f"0xexcluded{i:05d}" for i in range(52)]

    by_rows = list(measured)
    if variant == "real":
        for cid in invalid_ids:
            by_rows.append([cid, "UP_DOWN", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"])
    _write_csv(by_cond, ["condition_id", "subclass", "level_b_class"], by_rows)

    if excluded_reason_style == "diagnostic_suffix":
        excl_rows = [
            [
                cid,
                "UP_DOWN",
                (
                    f"NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts={1776408162 + i}, "
                    f"decision_lower_ts={1776411762 + i}, resolved_at_ts={1776408318 + i}, "
                    f"window_seconds=-3444)"
                ),
                "",
            ]
            for i, cid in enumerate(invalid_ids)
        ]
    else:
        excl_rows = [[cid, "UP_DOWN", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", ""] for cid in invalid_ids]
    _write_csv(excluded, ["condition_id", "subclass", "reason", "detail"], excl_rows)

    return by_cond, excluded


class FakeLoader:
    def __init__(
        self,
        sample_result: mod.SampleReconstructionResult,
        p0_state: Optional[str] = "P0_CLEAR",
        contract_version: Optional[str] = mod.NB_CONTRACT_VERSION_EXPECTED,
        contract_result: Optional[mod.ContractVersionResult] = None,
        resolution_version: Optional[str] = mod.NB_CONTRACT_VERSION_EXPECTED,
        resolution_result: Optional[mod.ResolutionSourceResult] = None,
        resolved_at_by_cid: Optional[Dict[str, Any]] = None,
        trades_by_cid: Optional[Dict[str, List[mod.TradeRow]]] = None,
        observed_columns: Optional[List[str]] = None,
    ) -> None:
        self._sample_result = sample_result
        self._p0_state = p0_state
        # Structured overrides win; otherwise build ok-results from the simple
        # version knobs (keeps the many existing tests unchanged in spirit).
        self._contract_result = contract_result or mod.ContractVersionResult(
            ok=True, version=contract_version
        )
        self._resolution_result = resolution_result
        self._resolution_version = resolution_version
        self._resolved_at_by_cid = resolved_at_by_cid or {}
        self._trades_by_cid = trades_by_cid or {}
        self._observed_columns = observed_columns or [
            "trade_id", "wallet", "condition_id", "outcome", "side", "price",
            "size_usdc", "traded_at", "tx_hash", "token_id", "outcome_index",
        ]
        self.load_trades_called = False

    def load_sample_manifest(self) -> mod.SampleReconstructionResult:
        return self._sample_result

    def load_p0_state(self) -> Optional[str]:
        return self._p0_state

    def load_contract_version(self) -> mod.ContractVersionResult:
        return self._contract_result

    def load_resolution_source(self, condition_ids: FrozenSet[str]) -> mod.ResolutionSourceResult:
        if self._resolution_result is not None:
            return self._resolution_result
        return mod.ResolutionSourceResult(
            ok=True,
            version=self._resolution_version,
            resolved_at_by_cid={
                cid: v for cid, v in self._resolved_at_by_cid.items() if cid in condition_ids
            },
        )

    def load_trades_for_conditions(self, condition_ids: FrozenSet[str]) -> Dict[str, List[mod.TradeRow]]:
        self.load_trades_called = True
        return {cid: self._trades_by_cid.get(cid, []) for cid in condition_ids}

    def observed_trades_columns(self) -> List[str]:
        return self._observed_columns


class ExplodingLoader:
    """A loader that raises if ANY method is called -- used to assert the
    unauthorized branch never touches loading at all."""

    def _boom(self, *a, **k):
        raise AssertionError("loader must not be called when unauthorized")

    load_sample_manifest = _boom
    load_p0_state = _boom
    load_contract_version = _boom
    load_resolution_source = _boom
    load_trades_for_conditions = _boom
    observed_trades_columns = _boom


class FakeWriter:
    def __init__(self) -> None:
        self.called = False
        self.result = None
        self.by_condition_rows = None
        self.excluded_rows = None
        self.source_shape_text = None

    def write_all(self, result, by_condition_rows, excluded_rows, source_shape_text) -> None:
        self.called = True
        self.result = result
        self.by_condition_rows = by_condition_rows
        self.excluded_rows = excluded_rows
        self.source_shape_text = source_shape_text


def _cfg(execute=True, write_artifacts=False, warmup_seconds=3600.0, quiet=True) -> mod.RunConfig:
    return mod.RunConfig(execute=execute, write_artifacts=write_artifacts, warmup_seconds=warmup_seconds, quiet=quiet)


def _ok_sample(
    n_up=1, n_over=0, n_named=0, n_excluded=0, raw_reasons: Optional[Dict[str, str]] = None
) -> mod.SampleReconstructionResult:
    """Build a syntactically-OK (ok=True) sample result for orchestration tests
    that don't care about the exact 50/98/100/52 pinned reconciliation (that
    reconciliation is tested separately against reconstruct_s1_pass1_sample
    directly). The n_excluded conditions are treated as S1-authoritative
    invalid-window ids; `raw_reasons` optionally supplies their preserved raw
    (un-normalized) excluded-ledger reason strings."""
    sample: Dict[str, str] = {}
    for i in range(n_up):
        sample[f"up_{i}"] = "UP_DOWN"
    for i in range(n_over):
        sample[f"over_{i}"] = "OVER_UNDER"
    for i in range(n_named):
        sample[f"named_{i}"] = "NAMED_OTHER"
    invalid_ids = []
    for i in range(n_excluded):
        sample[f"excl_{i}"] = "UP_DOWN"
        invalid_ids.append(f"excl_{i}")
    return mod.SampleReconstructionResult(
        ok=True,
        sample=sample,
        measured_count=n_up + n_over + n_named,
        excluded_count=n_excluded,
        measured_by_subclass={"UP_DOWN": n_up, "OVER_UNDER": n_over, "NAMED_OTHER": n_named},
        invalid_window_ids=frozenset(invalid_ids),
        invalid_window_raw_reasons=raw_reasons or {},
    )


# ---------------------------------------------------------------------------
# _is_missing_field / canonical_identifier / valid_price
# ---------------------------------------------------------------------------


def test_is_missing_field_true_cases():
    assert mod._is_missing_field(None)
    assert mod._is_missing_field(float("nan"))
    assert mod._is_missing_field("")
    assert mod._is_missing_field("   ")
    assert mod._is_missing_field("nan")
    assert mod._is_missing_field("NaN")
    assert mod._is_missing_field("none")
    assert mod._is_missing_field("None")


def test_is_missing_field_false_cases():
    assert not mod._is_missing_field("0x123")
    assert not mod._is_missing_field(0)
    assert not mod._is_missing_field("0")
    assert not mod._is_missing_field(5.2e76)  # a real, present, mangled float -- NOT missing


def test_canonical_identifier_normal_string():
    assert mod.canonical_identifier("123456789012345678901234567890") == "123456789012345678901234567890"


def test_canonical_identifier_int():
    assert mod.canonical_identifier(1) == "1"


def test_canonical_identifier_scientific_string_raises():
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.canonical_identifier("5.20896e+76")


def test_canonical_identifier_bare_float_raises():
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.canonical_identifier(5.20896e76)


def test_canonical_identifier_zero_point_zero_float_raises():
    # "0.0" as a float is still a float identifier -> precision loss (never
    # reconstruct as "0"). This is `canonical_identifier`, which is now scoped
    # to `token_id` specifically -- regression item 4: "token_id 0.0 still
    # triggers STOP_PRECISION_LOSS" (v5 patch).
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.canonical_identifier(0.0)


def test_canonical_identifier_token_id_scientific_notation_still_raises():
    # Regression item 4: "token_id scientific notation still triggers
    # STOP_PRECISION_LOSS" (v5 patch) -- unchanged by the outcome_index fix.
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.canonical_identifier("5.20896e+76", field_name="token_id")
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.canonical_identifier(5.20896e76, field_name="token_id")


def test_canonical_identifier_message_includes_field_name_condition_id_raw_value():
    # Task item 3: STOP_PRECISION_LOSS diagnostics must include field name,
    # condition_id (if available), and raw value.
    with pytest.raises(mod.IdentifierPrecisionLoss) as excinfo:
        mod.canonical_identifier(0.0, field_name="token_id", condition_id="cond_0042")
    msg = str(excinfo.value)
    assert "field=token_id" in msg
    assert "condition_id=cond_0042" in msg
    assert "raw_value=0.0" in msg


def test_canonical_identifier_message_omits_condition_id_when_not_supplied():
    with pytest.raises(mod.IdentifierPrecisionLoss) as excinfo:
        mod.canonical_identifier(0.0, field_name="token_id")
    msg = str(excinfo.value)
    assert "field=token_id" in msg
    assert "condition_id=" not in msg
    assert "raw_value=0.0" in msg


# ---------------------------------------------------------------------------
# canonical_outcome_index (v5 patch: bounded {0,1} slot field, separate from
# the strict token_id identifier rules)
# ---------------------------------------------------------------------------


def test_canonical_outcome_index_accepts_int_0_and_1():
    assert mod.canonical_outcome_index(0) == "0"
    assert mod.canonical_outcome_index(1) == "1"


def test_canonical_outcome_index_accepts_string_0_and_1():
    assert mod.canonical_outcome_index("0") == "0"
    assert mod.canonical_outcome_index("1") == "1"


def test_canonical_outcome_index_accepts_float_0_0_and_1_0():
    # THE regression: this is exactly the user's reported failure value.
    assert mod.canonical_outcome_index(0.0) == "0"
    assert mod.canonical_outcome_index(1.0) == "1"


def test_canonical_outcome_index_accepts_string_0_0_and_1_0():
    assert mod.canonical_outcome_index("0.0") == "0"
    assert mod.canonical_outcome_index("1.0") == "1"


def test_canonical_outcome_index_strips_whitespace():
    assert mod.canonical_outcome_index(" 0 ") == "0"
    assert mod.canonical_outcome_index(" 1.0 ") == "1"


def test_canonical_outcome_index_rejects_non_integral_0_5():
    result = mod.canonical_outcome_index(0.5)
    assert result not in ("0", "1")


def test_canonical_outcome_index_rejects_out_of_range_int_2():
    result = mod.canonical_outcome_index(2)
    assert result not in ("0", "1")


def test_canonical_outcome_index_rejects_out_of_range_float_2_0():
    result = mod.canonical_outcome_index(2.0)
    assert result not in ("0", "1")


def test_canonical_outcome_index_rejects_out_of_range_string_2():
    result = mod.canonical_outcome_index("2")
    assert result not in ("0", "1")


def test_canonical_outcome_index_rejects_nan():
    result = mod.canonical_outcome_index(float("nan"))
    assert result not in ("0", "1")


def test_canonical_outcome_index_rejects_infinity():
    result = mod.canonical_outcome_index(float("inf"))
    assert result not in ("0", "1")


def test_canonical_outcome_index_rejects_unsupported_type():
    result = mod.canonical_outcome_index(["0"])
    assert result not in ("0", "1")


def test_canonical_outcome_index_never_raises_identifier_precision_loss():
    # This is the core of the fix: outcome_index domain violations are never
    # precision loss, for any of these inputs.
    for bad in (0.5, 2, 2.0, "2", "0.5", float("nan"), float("inf"), ["x"], object()):
        result = mod.canonical_outcome_index(bad)  # must not raise
        assert result not in ("0", "1")


def test_canonical_outcome_index_does_not_accept_scientific_notation():
    # Deliberately narrow: "1e0" is NOT one of the explicitly reviewed accepted
    # forms, so it is rejected (falls through to the malformed-row path)
    # rather than silently widening the accepted-forms set.
    result = mod.canonical_outcome_index("1e0")
    assert result not in ("0", "1")


def test_valid_price_accepts_finite_in_range():
    assert mod.valid_price(0.0) == 0.0
    assert mod.valid_price(1.0) == 1.0
    assert mod.valid_price(0.42) == 0.42
    assert mod.valid_price("0.42") == 0.42


def test_valid_price_accepts_scientific_notation_price_string():
    # THE required correction: scientific-notation formatting of a numeric
    # price is NOT an error / NOT precision loss.
    assert mod.valid_price("4.2e-1") == pytest.approx(0.42)
    assert mod.valid_price(4.2e-1) == pytest.approx(0.42)


def test_valid_price_rejects_out_of_range_and_nonfinite():
    assert mod.valid_price(-0.1) is None
    assert mod.valid_price(1.1) is None
    assert mod.valid_price(float("nan")) is None
    assert mod.valid_price(float("inf")) is None
    assert mod.valid_price(None) is None
    assert mod.valid_price("not a number") is None


def test_valid_price_never_raises_identifier_precision_loss():
    # Even a huge scientific-notation numeric price must not be flagged --
    # precision loss applies to identifiers only. (It IS out of [0,1] though,
    # so it is correctly rejected as PRINT_PRICE_INVALID, just not via the
    # IdentifierPrecisionLoss path.)
    assert mod.valid_price("5.2e76") is None  # rejected for being out of [0,1], not for notation
    assert mod.valid_price(5.2e-76) is not None  # tiny but valid, in range


# ---------------------------------------------------------------------------
# parse_ts
# ---------------------------------------------------------------------------


def test_parse_ts_millisecond_utc_form():
    ts = mod.parse_ts("2025-03-06 07:25:37.000 UTC")
    assert ts == pytest.approx(1741245937.0, abs=0.001)


def test_parse_ts_whole_second_utc_form():
    ts1 = mod.parse_ts("2025-03-06 07:25:37 UTC")
    ts2 = mod.parse_ts("2025-03-06 07:25:37.000 UTC")
    assert ts1 == pytest.approx(ts2, abs=0.001)


def test_parse_ts_fractional_seconds_honored():
    base = mod.parse_ts("2025-03-06 07:25:37.000 UTC")
    half = mod.parse_ts("2025-03-06 07:25:37.500 UTC")
    assert half - base == pytest.approx(0.5, abs=0.001)


def test_parse_ts_iso_forms():
    assert mod.parse_ts("2025-03-06T07:25:37") is not None
    assert mod.parse_ts("2025-03-06T07:25:37.123456") is not None
    assert mod.parse_ts("2025-03-06") is not None


def test_parse_ts_epoch_numeric_and_string():
    assert mod.parse_ts(1741245937.0) == 1741245937.0
    assert mod.parse_ts("1741245937") == 1741245937.0


def test_parse_ts_python_datetime_naive_treated_as_utc():
    import datetime as dt

    d = dt.datetime(2025, 3, 6, 7, 25, 37)
    assert mod.parse_ts(d) == pytest.approx(1741245937.0, abs=0.001)


def test_parse_ts_pandas_timestamp_like_duck_type():
    class FakeTimestamp:
        def to_pydatetime(self):
            import datetime as dt

            return dt.datetime(2025, 3, 6, 7, 25, 37)

    assert mod.parse_ts(FakeTimestamp()) == pytest.approx(1741245937.0, abs=0.001)


def test_parse_ts_rejects_non_utc_timezone():
    with pytest.raises(ValueError):
        mod.parse_ts("2025-03-06 07:25:37 PST")


def test_parse_ts_rejects_garbage():
    with pytest.raises(ValueError):
        mod.parse_ts("not a timestamp")


def test_parse_ts_rejects_none_and_nan():
    with pytest.raises(ValueError):
        mod.parse_ts(None)
    with pytest.raises(ValueError):
        mod.parse_ts(float("nan"))


# ---------------------------------------------------------------------------
# enumerate_token_pair
# ---------------------------------------------------------------------------


def _row(token_id=None, outcome_index=None, price=0.5, traded_at="2025-01-01 00:00:00 UTC"):
    return mod.TradeRow(token_id=token_id, outcome_index=outcome_index, price=price, traded_at=traded_at)


def test_enumerate_token_pair_resolves_clean_pair():
    rows = [_row("TOKA", "0"), _row("TOKA", "0"), _row("TOKB", "1")]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.side_0_token == "TOKA"
    assert result.side_1_token == "TOKB"
    assert result.malformed_row_count == 0


def test_enumerate_token_pair_skips_missing_and_counts():
    rows = [_row("TOKA", "0"), _row(None, "0"), _row("TOKB", "1"), _row("TOKB", None)]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.malformed_row_count == 2


def test_enumerate_token_pair_nan_token_and_index_ignored():
    rows = [_row("TOKA", "0"), _row(float("nan"), "0"), _row("TOKB", "1"), _row("TOKB", float("nan"))]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.malformed_row_count == 2


def test_enumerate_token_pair_only_malformed_unresolved_no_exception():
    rows = [_row(None, None), _row("", ""), _row(float("nan"), float("nan"))]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "TOKEN_PAIR_UNRESOLVED"
    assert result.reason_detail == "ALL_ROWS_MISSING_KEY"


def test_enumerate_token_pair_unstable_index_unresolved():
    rows = [_row("TOKA", "0"), _row("TOKC", "0"), _row("TOKB", "1")]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "TOKEN_PAIR_UNRESOLVED"
    assert "side_0_candidates=2" in result.reason_detail


def test_enumerate_token_pair_missing_one_side_unresolved():
    rows = [_row("TOKA", "0"), _row("TOKA", "0")]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "TOKEN_PAIR_UNRESOLVED"


def test_enumerate_token_pair_bad_outcome_index_value_counted_as_malformed():
    rows = [_row("TOKA", "0"), _row("TOKB", "1"), _row("TOKC", "2")]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.malformed_row_count == 1


def test_enumerate_token_pair_float_outcome_index_0_0_and_1_0_resolve_cleanly():
    """
    THE regression: outcome_index=0.0 (a Python float) must resolve cleanly,
    not raise STOP_PRECISION_LOSS. This is the exact failure the user hit
    ("float identifier not string-safe: 0.0") during real trade loading.
    """
    rows = [_row("TOKA", 0.0), _row("TOKB", 1.0)]
    result = mod.enumerate_token_pair(rows)  # must NOT raise
    assert result.status == "RESOLVED"
    assert result.side_0_token == "TOKA"
    assert result.side_1_token == "TOKB"
    assert result.malformed_row_count == 0


def test_enumerate_token_pair_string_outcome_index_0_0_and_1_0_resolve_cleanly():
    rows = [_row("TOKA", "0.0"), _row("TOKB", "1.0")]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.malformed_row_count == 0


def test_enumerate_token_pair_mixed_int_and_float_outcome_index_forms_resolve():
    # A realistic messy trades table might mix "0"/1.0/0.0/"1" across rows for
    # the same condition -- all must still resolve to the same two tokens.
    rows = [_row("TOKA", "0"), _row("TOKA", 0.0), _row("TOKB", 1.0), _row("TOKB", "1")]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.side_0_token == "TOKA"
    assert result.side_1_token == "TOKB"


def test_enumerate_token_pair_non_integral_outcome_index_0_5_counted_as_malformed():
    rows = [_row("TOKA", "0"), _row("TOKB", "1"), _row("TOKC", 0.5)]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.malformed_row_count == 1  # the 0.5 row, excluded not stopped


def test_enumerate_token_pair_out_of_range_float_outcome_index_2_0_counted_as_malformed():
    rows = [_row("TOKA", "0"), _row("TOKB", "1"), _row("TOKC", 2.0)]
    result = mod.enumerate_token_pair(rows)
    assert result.status == "RESOLVED"
    assert result.malformed_row_count == 1


def test_enumerate_token_pair_token_id_still_precision_loss_even_with_valid_outcome_index():
    # Confirms the fix is scoped correctly: a float token_id still hard-stops
    # even though its outcome_index (0.0) is now perfectly valid.
    rows = [_row("TOKA", "0"), _row(5.20896e76, 1.0)]
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.enumerate_token_pair(rows)


def test_enumerate_token_pair_precision_loss_message_includes_condition_id():
    rows = [_row("TOKA", "0"), _row(5.20896e76, "1")]
    with pytest.raises(mod.IdentifierPrecisionLoss) as excinfo:
        mod.enumerate_token_pair(rows, condition_id="cond_0042")
    msg = str(excinfo.value)
    assert "field=token_id" in msg
    assert "condition_id=cond_0042" in msg
    assert "raw_value=5.20896e+76" in msg or "5.20896e+76" in msg


def test_enumerate_token_pair_precision_loss_propagates():
    rows = [_row("TOKA", "0"), _row(5.20896e76, "1")]
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.enumerate_token_pair(rows)


def test_enumerate_token_pair_scientific_string_token_precision_loss():
    rows = [_row("TOKA", "0"), _row("5.20896e+76", "1")]
    with pytest.raises(mod.IdentifierPrecisionLoss):
        mod.enumerate_token_pair(rows)


def test_enumerate_token_pair_never_uses_resolved_winning_token_id():
    # Structural guarantee: the function signature does not even accept a
    # winner/resolution argument, so it cannot consult one. `condition_id` is
    # diagnostics-only (STOP_PRECISION_LOSS message enrichment), added in v5.
    import inspect

    sig = inspect.signature(mod.enumerate_token_pair)
    assert "resolved_winning_token_id" not in sig.parameters
    assert list(sig.parameters.keys()) == ["rows", "condition_id"]


# ---------------------------------------------------------------------------
# valid_decision_window / first_print_in_window / classify_level_b
# ---------------------------------------------------------------------------


def test_valid_decision_window_true_case():
    assert mod.valid_decision_window(1000.0, 1000.0 + 3600.0 + 1.0, 3600.0) is True


def test_valid_decision_window_strict_boundary_false():
    # exactly first_trade_ts + warmup is NOT > -- must be False (strict)
    assert mod.valid_decision_window(1000.0, 1000.0 + 3600.0, 3600.0) is False


def test_valid_decision_window_missing_anchors_false():
    assert mod.valid_decision_window(None, 5000.0, 3600.0) is False
    assert mod.valid_decision_window(1000.0, None, 3600.0) is False
    assert mod.valid_decision_window(None, None, 3600.0) is False


def test_first_print_in_window_picks_earliest_in_window():
    rows = [
        _row("TOKA", "0", price=0.3, traded_at=2000.0),  # before window
        _row("TOKA", "0", price=0.5, traded_at=5000.0),  # in window, later
        _row("TOKA", "0", price=0.4, traded_at=4600.0),  # in window, earlier -> winner
    ]
    obs = mod.first_print_in_window(rows, decision_lower_ts=4600.0, resolved_at_ts=10000.0)
    assert obs.ts == 4600.0
    assert obs.gap_seconds == 0.0


def test_first_print_in_window_excludes_at_or_after_resolved_at_strict():
    rows = [
        _row("TOKA", "0", price=0.5, traded_at=9999.999),
        _row("TOKA", "0", price=0.5, traded_at=10000.0),  # exactly at resolved_at -- must NOT count
        _row("TOKA", "0", price=0.5, traded_at=10000.5),  # after resolved_at -- must NOT count
    ]
    obs = mod.first_print_in_window(rows, decision_lower_ts=0.0, resolved_at_ts=10000.0)
    assert obs.ts == 9999.999


def test_first_print_in_window_invalid_price_rows_skipped_and_counted():
    rows = [
        _row("TOKA", "0", price=None, traded_at=5000.0),  # invalid price -> skip
        _row("TOKA", "0", price=1.5, traded_at=5001.0),  # out of range -> skip
        _row("TOKA", "0", price=0.5, traded_at=5002.0),  # valid -> winner
    ]
    obs = mod.first_print_in_window(rows, decision_lower_ts=0.0, resolved_at_ts=10000.0)
    assert obs.ts == 5002.0
    assert obs.invalid_price_row_count == 2


def test_first_print_in_window_no_rows_in_window_gives_none():
    rows = [_row("TOKA", "0", price=0.5, traded_at=1.0)]
    obs = mod.first_print_in_window(rows, decision_lower_ts=100.0, resolved_at_ts=200.0)
    assert obs.ts is None
    assert obs.gap_seconds is None


def test_first_print_in_window_scientific_notation_price_string_counts_as_valid():
    rows = [_row("TOKA", "0", price="4.2e-1", traded_at=5000.0)]
    obs = mod.first_print_in_window(rows, decision_lower_ts=0.0, resolved_at_ts=10000.0)
    assert obs.ts == 5000.0
    assert obs.invalid_price_row_count == 0


def test_classify_level_b_both_sides():
    obs0 = mod.SideObservation(ts=1.0, gap_seconds=0.0, print_count_total_valid=1, invalid_price_row_count=0, malformed_row_count=0)
    obs1 = mod.SideObservation(ts=2.0, gap_seconds=1.0, print_count_total_valid=1, invalid_price_row_count=0, malformed_row_count=0)
    assert mod.classify_level_b(obs0, obs1) == "DECISION_PRICE_BOTH_SIDES"


def test_classify_level_b_one_side():
    obs0 = mod.SideObservation(ts=1.0, gap_seconds=0.0, print_count_total_valid=1, invalid_price_row_count=0, malformed_row_count=0)
    obs1 = mod.SideObservation(ts=None, gap_seconds=None, print_count_total_valid=0, invalid_price_row_count=0, malformed_row_count=0)
    assert mod.classify_level_b(obs0, obs1) == "DECISION_PRICE_ONE_SIDE"


def test_classify_level_b_neither():
    obs0 = mod.SideObservation(ts=None, gap_seconds=None, print_count_total_valid=0, invalid_price_row_count=0, malformed_row_count=0)
    obs1 = mod.SideObservation(ts=None, gap_seconds=None, print_count_total_valid=0, invalid_price_row_count=0, malformed_row_count=0)
    assert mod.classify_level_b(obs0, obs1) == "DECISION_PRICE_NEITHER"


def test_rows_for_side_filters_by_token_identity_only():
    rows = [_row("TOKA", "0"), _row("TOKB", "1"), _row("TOKA", "0")]
    side0 = mod.rows_for_side(rows, "TOKA")
    assert len(side0) == 2
    assert all(r.token_id == "TOKA" for r in side0)


def test_rows_for_side_never_uses_side_or_label():
    # `condition_id` is diagnostics-only (STOP_PRECISION_LOSS message
    # enrichment), added in v5; the guarantee is still "never `side`/label".
    import inspect

    sig = inspect.signature(mod.rows_for_side)
    assert list(sig.parameters.keys()) == ["rows", "side_token", "condition_id"]
    assert "side" not in [p for p in sig.parameters if p != "side_token"]


# ---------------------------------------------------------------------------
# No-synthesis structural guarantees (grep-level, executable-code only)
# ---------------------------------------------------------------------------


def test_no_yes_price_or_complement_synthesis_in_source():
    """
    AST-based (not substring-based): walks real executable expressions only,
    so a documentation/markdown string that mentions "1 - price" as prose (to
    explain what is forbidden) can never trip this check -- only an actual
    `1 - <price-like-name>` expression or a real `yes_price(...)` call would.
    """
    src = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    price_like_substrings = ("price", "yes_price")

    def _is_one_constant(node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and node.value in (1, 1.0)

    def _is_price_like(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return any(s in node.id.lower() for s in price_like_substrings)
        if isinstance(node, ast.Attribute):
            return any(s in node.attr.lower() for s in price_like_substrings)
        return False

    complement_violations = []
    yes_price_call_violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            if _is_one_constant(node.left) and _is_price_like(node.right):
                complement_violations.append(node.lineno)
        if isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else (func.attr if isinstance(func, ast.Attribute) else None)
            if name == "yes_price":
                yes_price_call_violations.append(node.lineno)

    assert not complement_violations, f"forbidden '1 - <price>' synthesis at lines {complement_violations}"
    assert not yes_price_call_violations, f"forbidden yes_price(...) call at lines {yes_price_call_violations}"


def test_named_binary_probe_blocked_never_assigned():
    src = Path(mod.__file__).read_text(encoding="utf-8")
    assert "named_binary_probe_blocked =" not in src
    assert "named_binary_probe_blocked=" not in src
    assert "named_binary_probe_blocked_observed" in src  # only ever observed/echoed


def test_no_network_imports_in_source():
    src = Path(mod.__file__).read_text(encoding="utf-8")
    for bad in ("import requests", "import urllib", "import socket", "clob.polymarket.com", "polymarket.com/trades"):
        assert bad not in src


# ---------------------------------------------------------------------------
# _normalize_excluded_reason (unit level)
# ---------------------------------------------------------------------------


def test_normalize_excluded_reason_bare_class_unchanged():
    assert mod._normalize_excluded_reason("NO_VALID_DECISION_WINDOW_AFTER_WARMUP") == "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"


def test_normalize_excluded_reason_strips_parenthesized_diagnostic_suffix():
    raw = (
        "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts=1776408162, "
        "decision_lower_ts=1776411762, resolved_at_ts=1776408318, window_seconds=-3444)"
    )
    assert mod._normalize_excluded_reason(raw) == "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"


def test_normalize_excluded_reason_strips_whitespace_only_suffix():
    assert mod._normalize_excluded_reason("TOKEN_PAIR_UNRESOLVED with extra words") == "TOKEN_PAIR_UNRESOLVED"


def test_normalize_excluded_reason_handles_leading_trailing_whitespace():
    assert mod._normalize_excluded_reason("  NO_VALID_DECISION_WINDOW_AFTER_WARMUP  ") == "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"


def test_normalize_excluded_reason_no_suffix_no_change():
    assert mod._normalize_excluded_reason("SOME_UNKNOWN_REASON") == "SOME_UNKNOWN_REASON"


def test_normalize_excluded_reason_none_is_empty_string():
    assert mod._normalize_excluded_reason(None) == ""


# ---------------------------------------------------------------------------
# Sample reconstruction (STOP_SAMPLE_IRREPRODUCIBLE discipline)
# ---------------------------------------------------------------------------


def test_reconstruct_sample_excluded_reason_exact_class_succeeds(tmp_path):
    """Regression 1 (task item 5): excluded reason exactly
    NO_VALID_DECISION_WINDOW_AFTER_WARMUP (no suffix) still succeeds."""
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real", excluded_reason_style="bare")
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is True
    assert result.measured_count == 248
    assert result.excluded_count == 52


def test_reconstruct_sample_excluded_reason_with_diagnostic_suffix_succeeds(tmp_path):
    """
    THE regression this patch targets: reproduces the user's exact reported
    failure_detail shape --
    "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts=1776408162,
    decision_lower_ts=1776411762, resolved_at_ts=1776408318, window_seconds=-3444)"
    -- and asserts reconstruction now succeeds instead of halting
    STOP_SAMPLE_IRREPRODUCIBLE(unexpected_excluded_reason).
    """
    by_cond, excluded = _make_valid_s1_sample_csvs(
        tmp_path, variant="real", excluded_reason_style="diagnostic_suffix"
    )
    # Sanity: the fixture really does bundle diagnostics into the reason field,
    # exactly like the user's report.
    raw_reasons = [r["reason"] for r in csv.DictReader(excluded.open())]
    assert any("window_seconds=-3444" in r for r in raw_reasons)
    assert all(r.startswith("NO_VALID_DECISION_WINDOW_AFTER_WARMUP (") for r in raw_reasons)

    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is True
    assert result.failure_reason is None
    assert result.measured_count == 248
    assert result.excluded_count == 52
    assert result.measured_by_subclass == {"UP_DOWN": 50, "OVER_UNDER": 98, "NAMED_OTHER": 100}
    # Raw diagnostic strings are preserved for audit, keyed by condition_id.
    some_excluded_id = next(iter(result.invalid_window_ids))
    assert some_excluded_id in result.invalid_window_raw_reasons
    assert "window_seconds=-3444" in result.invalid_window_raw_reasons[some_excluded_id]
    assert result.invalid_window_raw_reasons[some_excluded_id].startswith(
        "NO_VALID_DECISION_WINDOW_AFTER_WARMUP ("
    )


def test_reconstruct_sample_unknown_reason_with_diagnostics_still_halts(tmp_path):
    """Regression 3 (task item 5): an UNKNOWN reason class bundled with
    diagnostics must still halt -- normalization must not accidentally widen
    acceptance to any bundled string, only to the expected class."""
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real")
    rows = list(csv.DictReader(excluded.open()))
    with excluded.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["condition_id", "subclass", "reason", "detail"])
        for i, r in enumerate(rows):
            reason = r["reason"]
            if i == 0:
                reason = "SOME_UNKNOWN_REASON (first_trade_ts=123, window_seconds=-9)"
            w.writerow([r["condition_id"], r["subclass"], reason, r["detail"]])
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "unexpected_excluded_reason"
    assert "SOME_UNKNOWN_REASON" in result.failure_detail
    assert "normalized=" in result.failure_detail


def test_reconstruct_sample_mixed_bare_and_diagnostic_suffix_reasons_succeeds(tmp_path):
    """A ledger where some rows are bare and others carry diagnostics (a
    plausible real-world mix) must still reconstruct cleanly -- normalization
    is applied per-row, not globally."""
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real")
    rows = list(csv.DictReader(excluded.open()))
    with excluded.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["condition_id", "subclass", "reason", "detail"])
        for i, r in enumerate(rows):
            reason = r["reason"]
            if i % 2 == 0:
                reason = f"{reason} (first_trade_ts={i}, window_seconds=-1)"
            w.writerow([r["condition_id"], r["subclass"], reason, r["detail"]])
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is True
    assert result.excluded_count == 52


def test_reconstruct_sample_succeeds_on_real_shape_with_expected_52_overlap(tmp_path):
    """
    THE regression: the accepted S1 by-condition ledger carries all 300 rows
    (248 measured + 52 invalid-window) and the excluded ledger carries the same
    52 invalid-window ids. The 52-id overlap is EXPECTED and must reconstruct
    cleanly to 300 unique / 248 measured / 52 invalid-window -- not a false
    STOP_SAMPLE_IRREPRODUCIBLE(overlap).
    """
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real")

    # sanity on the fixture itself: 300 by-condition rows, 52 excluded, 52-id overlap
    by_rows = list(csv.DictReader(by_cond.open()))
    ex_rows = list(csv.DictReader(excluded.open()))
    by_ids = {r["condition_id"] for r in by_rows}
    ex_ids = {r["condition_id"] for r in ex_rows}
    assert len(by_rows) == 300
    assert len(ex_rows) == 52
    assert len(by_ids & ex_ids) == 52  # exactly the invalid-window overlap

    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is True
    assert result.failure_reason is None
    assert len(result.sample) == 300  # union of unique ids
    assert result.measured_count == 248
    assert result.excluded_count == 52
    assert len(result.invalid_window_ids) == 52
    assert result.invalid_window_ids == frozenset(ex_ids)
    assert result.measured_by_subclass == {"UP_DOWN": 50, "OVER_UNDER": 98, "NAMED_OTHER": 100}


def test_reconstruct_sample_succeeds_on_disjoint_variant(tmp_path):
    """Robustness: if an accepted-artifact variant lists the 52 invalid ids only
    in the excluded file (not also in by-condition), reconstruction must still
    yield the identical 300/248/52 split via the union."""
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="disjoint")
    by_rows = list(csv.DictReader(by_cond.open()))
    assert len(by_rows) == 248  # disjoint: by-condition holds only measured
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is True
    assert len(result.sample) == 300
    assert result.measured_count == 248
    assert result.excluded_count == 52
    assert len(result.invalid_window_ids) == 52
    assert result.measured_by_subclass == {"UP_DOWN": 50, "OVER_UNDER": 98, "NAMED_OTHER": 100}


def test_reconstruct_sample_missing_file_halts(tmp_path):
    result = mod.reconstruct_s1_pass1_sample(tmp_path / "nope1.csv", tmp_path / "nope2.csv")
    assert result.ok is False
    assert result.failure_reason == "missing_file"


def test_reconstruct_sample_missing_status_column_halts(tmp_path):
    # by-condition file without a level_b_class/status column cannot support the
    # valid/invalid split -> irreproducible.
    by_cond = tmp_path / "by_condition.csv"
    excluded = tmp_path / "excluded.csv"
    _write_csv(by_cond, ["condition_id", "subclass"], [["a", "UP_DOWN"]])
    _write_csv(excluded, ["condition_id", "subclass", "reason", "detail"], [["b", "UP_DOWN", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", ""]])
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "missing_columns"


def test_reconstruct_sample_total_mismatch_halts(tmp_path):
    by_cond = tmp_path / "by_condition.csv"
    excluded = tmp_path / "excluded.csv"
    _write_csv(by_cond, ["condition_id", "subclass", "level_b_class"], [["a", "UP_DOWN", "DECISION_PRICE_NEITHER"]])
    _write_csv(excluded, ["condition_id", "subclass", "reason", "detail"], [["b", "UP_DOWN", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", ""]])
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "total_mismatch"


def test_reconstruct_sample_unrecognized_status_halts(tmp_path):
    # A by-condition row whose status is neither a measured Level-B class nor the
    # invalid-window token is unrecognized -> irreproducible (never silently
    # assumed measured).
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real")
    rows = list(csv.DictReader(by_cond.open()))
    rows[0]["level_b_class"] = "SOMETHING_WEIRD"
    with by_cond.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["condition_id", "subclass", "level_b_class"])
        w.writeheader()
        w.writerows(rows)
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "unrecognized_by_condition_status"


def test_reconstruct_sample_status_conflict_halts(tmp_path):
    """True bad overlap/conflict: an id the excluded file calls invalid-window
    but the by-condition file marks as MEASURED is an unreconcilable status
    conflict -> STOP_SAMPLE_IRREPRODUCIBLE(status_conflict)."""
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real")
    by_rows = list(csv.DictReader(by_cond.open()))
    ex_rows = list(csv.DictReader(excluded.open()))
    conflict_id = ex_rows[0]["condition_id"]  # an invalid-window id per excluded
    # Flip that id's by-condition row to a MEASURED class (the conflict).
    for r in by_rows:
        if r["condition_id"] == conflict_id:
            r["level_b_class"] = "DECISION_PRICE_BOTH_SIDES"
    with by_cond.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["condition_id", "subclass", "level_b_class"])
        w.writeheader()
        w.writerows(by_rows)
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "status_conflict"


def test_reconstruct_sample_subclass_breakdown_mismatch_halts(tmp_path):
    by_cond = tmp_path / "by_condition.csv"
    excluded = tmp_path / "excluded.csv"
    rows = [[f"m{i}", "UP_DOWN", "DECISION_PRICE_NEITHER"] for i in range(248)]  # wrong breakdown: all UP_DOWN
    _write_csv(by_cond, ["condition_id", "subclass", "level_b_class"], rows)
    excl_rows = [[f"e{i}", "UP_DOWN", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", ""] for i in range(52)]
    _write_csv(excluded, ["condition_id", "subclass", "reason", "detail"], excl_rows)
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "measured_subclass_breakdown_mismatch"


def test_reconstruct_sample_unexpected_excluded_reason_halts(tmp_path):
    by_cond, excluded = _make_valid_s1_sample_csvs(tmp_path, variant="real")
    rows = list(csv.DictReader(excluded.open()))
    # Rewrite excluded with one non-invalid-window reason
    with excluded.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["condition_id", "subclass", "reason", "detail"])
        for i, r in enumerate(rows):
            reason = "TOKEN_PAIR_UNRESOLVED" if i == 0 else r["reason"]
            w.writerow([r["condition_id"], r["subclass"], reason, r["detail"]])
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "unexpected_excluded_reason"


def test_reconstruct_sample_duplicate_condition_id_halts(tmp_path):
    by_cond = tmp_path / "by_condition.csv"
    excluded = tmp_path / "excluded.csv"
    rows = [["dup", "UP_DOWN", "DECISION_PRICE_NEITHER"], ["dup", "UP_DOWN", "DECISION_PRICE_NEITHER"]] + [
        [f"m{i}", "UP_DOWN", "DECISION_PRICE_NEITHER"] for i in range(246)
    ]
    _write_csv(by_cond, ["condition_id", "subclass", "level_b_class"], rows)
    excl_rows = [[f"e{i}", "UP_DOWN", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", ""] for i in range(52)]
    _write_csv(excluded, ["condition_id", "subclass", "reason", "detail"], excl_rows)
    result = mod.reconstruct_s1_pass1_sample(by_cond, excluded)
    assert result.ok is False
    assert result.failure_reason == "duplicate_condition_id"


# ---------------------------------------------------------------------------
# Orchestration: authorization gating
# ---------------------------------------------------------------------------


def test_unauthorized_run_touches_no_loader_method_and_writes_nothing():
    cfg = _cfg(execute=False)
    result = mod.run_pass1_alt_coverage(cfg, ExplodingLoader(), None)
    assert result["status"] == mod.STOP_NOT_AUTHORIZED
    assert result["authorized"] is False
    assert result["wrote_artifacts"] is False


def test_authorized_run_without_write_artifacts_computes_but_does_not_write():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={}, trades_by_cid={})
    cfg = _cfg(execute=True, write_artifacts=False)
    writer = FakeWriter()
    result = mod.run_pass1_alt_coverage(cfg, loader, writer)
    assert result["authorized"] is True
    assert result["wrote_artifacts"] is False
    assert writer.called is False
    assert loader.load_trades_called is True  # execution still reads real data


def test_authorized_run_with_write_artifacts_calls_writer():
    now = 10_000.0
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.4, traded_at=now + 3600.0),
            _row("TOKB", "1", price=0.6, traded_at=now + 3700.0),
        ]
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        resolved_at_by_cid={"up_0": now + 100000.0},
        trades_by_cid=trades,
    )
    # first_trade_ts will be min(traded_at) = now + 3600 from the rows themselves
    cfg = _cfg(execute=True, write_artifacts=True)
    writer = FakeWriter()
    result = mod.run_pass1_alt_coverage(cfg, loader, writer)
    assert writer.called is True
    assert result["wrote_artifacts"] is True


# ---------------------------------------------------------------------------
# Orchestration: P0 / contract stops
# ---------------------------------------------------------------------------


def test_p0_not_clear_halts():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, p0_state="SOMETHING_ELSE")
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_P0_NOT_CLEAR


def test_p0_missing_halts():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, p0_state=None)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_P0_NOT_CLEAR


def test_stale_contract_halts():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, contract_version="nb-contract-OLD")
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_STALE_CONTRACT


def test_missing_contract_halts_with_contract_schema_stop():
    # BLOCK patch: the classification contract is a REQUIRED pinned input; a
    # missing file is a setup failure, not tolerable, and must be
    # distinguishable from a stale version.
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        contract_result=mod.ContractVersionResult(ok=False, failure_reason="missing_file", failure_detail="x"),
        trades_by_cid={},
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_CONTRACT_SCHEMA
    assert result["contract_schema_failure"]["failure_reason"] == "missing_file"
    assert loader.load_trades_called is False  # halts before any classification


def test_missing_contract_version_field_halts_with_contract_schema_stop():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        contract_result=mod.ContractVersionResult(
            ok=False, failure_reason="missing_version_field", failure_detail="nb_contract_version absent"
        ),
        trades_by_cid={},
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_CONTRACT_SCHEMA
    assert result["contract_schema_failure"]["failure_reason"] == "missing_version_field"


def test_malformed_contract_halts_with_contract_schema_stop():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        contract_result=mod.ContractVersionResult(
            ok=False, failure_reason="unreadable_or_malformed", failure_detail="Expecting value"
        ),
        trades_by_cid={},
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_CONTRACT_SCHEMA


def test_wrong_contract_version_halts_with_stale_contract_distinguishable():
    # A PRESENT but WRONG version must remain STOP_STALE_CONTRACT -- not the
    # schema stop -- so setup failures and staleness stay distinguishable.
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, contract_version="nb-contract-WRONG")
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_STALE_CONTRACT
    assert result["status"] != mod.STOP_CONTRACT_SCHEMA
    assert result["nb_contract_version_observed"] == "nb-contract-WRONG"


def test_stale_resolution_source_version_halts():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolution_version="nb-contract-OLD")
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_STALE_CONTRACT


# ---------------------------------------------------------------------------
# Orchestration: resolution-source setup/schema stops (BLOCK patch)
# ---------------------------------------------------------------------------


def test_missing_resolution_source_file_halts_with_schema_stop():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        resolution_result=mod.ResolutionSourceResult(
            ok=False, failure_reason="missing_file", failure_detail="x.parquet"
        ),
        trades_by_cid={},
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_RESOLUTION_SOURCE_SCHEMA
    assert result["resolution_source_schema_failure"]["failure_reason"] == "missing_file"
    assert loader.load_trades_called is False  # halts before any classification


def test_missing_resolution_source_columns_halts_with_schema_stop():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        resolution_result=mod.ResolutionSourceResult(
            ok=False, failure_reason="missing_columns", failure_detail="missing=['resolved_at']"
        ),
        trades_by_cid={},
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_RESOLUTION_SOURCE_SCHEMA
    assert "resolved_at" in result["resolution_source_schema_failure"]["failure_detail"]


def test_setup_failure_never_masquerades_as_inconclusive_data_finding():
    """
    THE regression the BLOCK targets: a missing required resolution source must
    NOT flow through as blank resolved_at for every condition -> all invalid
    windows -> S1ALT_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE. It must halt
    with the typed setup stop instead.
    """
    trades = {
        "up_0": [_row("TOKA", "0", price=0.4, traded_at=0.0), _row("TOKB", "1", price=0.6, traded_at=0.0)],
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(
        sample_result=sample,
        resolution_result=mod.ResolutionSourceResult(
            ok=False, failure_reason="missing_file", failure_detail="x.parquet"
        ),
        trades_by_cid=trades,
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_RESOLUTION_SOURCE_SCHEMA
    assert result["status"] != mod.VERDICT_INCONCLUSIVE_NO_VALID_WINDOW
    assert "verdict" not in result  # no data verdict of any kind on a setup stop


def test_valid_resolution_table_with_row_level_missing_resolved_at_excludes_not_stops():
    """
    Required row-level behavior preserved: a VALID resolution-source table in
    which ONE sampled condition lacks a usable resolved_at classifies THAT
    condition as NO_VALID_DECISION_WINDOW_AFTER_WARMUP (excluded + reported,
    not a coverage negative), while the rest of the run proceeds normally --
    never a global stop, never counted against coverage.
    """
    trades = {
        "up_0": [  # will be the row-level invalid-window condition
            _row("TOKA", "0", price=0.4, traded_at=0.0),
            _row("TOKB", "1", price=0.6, traded_at=10.0),
        ],
        "up_1": [  # healthy, measurable, both sides in-window
            _row("TOKC", "0", price=0.4, traded_at=0.0),
            _row("TOKC", "0", price=0.41, traded_at=4000.0),
            _row("TOKD", "1", price=0.59, traded_at=4000.0),
        ],
    }
    sample = _ok_sample(n_up=2)
    loader = FakeLoader(
        sample_result=sample,
        resolved_at_by_cid={
            # up_0's resolved_at is missing entirely (row-level gap in a table
            # that is otherwise valid); up_1 has a proper one.
            "up_1": "2025-06-01 00:00:00.000 UTC",
        },
        trades_by_cid=trades,
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    # No setup stop; run completed with a data verdict.
    assert result["status"] not in (mod.STOP_RESOLUTION_SOURCE_SCHEMA, mod.STOP_CONTRACT_SCHEMA)
    recon = result["universe_reconciliation"]
    assert recon["no_valid_decision_window"] == 1  # up_0 excluded per-condition
    assert recon["measured"] == 1  # up_1 still measured
    assert recon["reconciled"] is True
    # The exclusion is not a coverage negative: the only measured condition is
    # BOTH_SIDES, so the invalid-window one contributed nothing to Level-B counts.
    assert result["level_b_class_counts"]["DECISION_PRICE_BOTH_SIDES"] == 1
    assert result["level_b_class_counts"]["DECISION_PRICE_NEITHER"] == 0


def test_row_level_unparseable_resolved_at_excludes_not_stops():
    trades = {
        "up_0": [_row("TOKA", "0", price=0.4, traded_at=0.0), _row("TOKB", "1", price=0.6, traded_at=10.0)],
        "up_1": [
            _row("TOKC", "0", price=0.4, traded_at=0.0),
            _row("TOKC", "0", price=0.41, traded_at=4000.0),
            _row("TOKD", "1", price=0.59, traded_at=4000.0),
        ],
    }
    sample = _ok_sample(n_up=2)
    loader = FakeLoader(
        sample_result=sample,
        resolved_at_by_cid={
            "up_0": "garbage not a timestamp",  # unparseable row-level value
            "up_1": "2025-06-01 00:00:00.000 UTC",
        },
        trades_by_cid=trades,
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    recon = result["universe_reconciliation"]
    assert recon["no_valid_decision_window"] == 1
    assert recon["measured"] == 1
    assert recon["reconciled"] is True


# ---------------------------------------------------------------------------
# Orchestration: sample reproducibility stop propagation
# ---------------------------------------------------------------------------


def test_sample_irreproducible_propagates_from_loader():
    bad_sample = mod.SampleReconstructionResult(ok=False, failure_reason="missing_file", failure_detail="x")
    loader = FakeLoader(sample_result=bad_sample)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_SAMPLE_IRREPRODUCIBLE
    assert result["sample_reconstruction"]["reconstructed"] is False


# ---------------------------------------------------------------------------
# Orchestration: end-to-end classification scenarios
# ---------------------------------------------------------------------------


def test_end_to_end_both_sides_measured_and_reconciles():
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.4, traded_at=0.0),  # anchor -> first_trade_ts = 0.0
            _row("TOKA", "0", price=0.4, traded_at=3650.0),  # in window (>= 3600)
            _row("TOKB", "1", price=0.6, traded_at=3700.0),  # in window
        ]
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={"up_0": 100000.0}, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["verdict"] in (mod.VERDICT_VIABLE, mod.VERDICT_PARTIAL, mod.VERDICT_NOT_VIABLE)
    assert result["universe_reconciliation"]["reconciled"] is True
    assert result["universe_reconciliation"]["measured"] == 1
    assert result["level_b_class_counts"]["DECISION_PRICE_BOTH_SIDES"] == 1


def test_end_to_end_no_trade_anchor_excluded_not_counted_negative():
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={}, trades_by_cid={})  # no rows at all
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["universe_reconciliation"]["no_trade_anchor"] == 1
    assert result["universe_reconciliation"]["measured"] == 0


def test_end_to_end_token_pair_unresolved_excluded_not_counted_negative():
    trades = {
        "up_0": [_row(None, None, traded_at=1.0), _row("", "", traded_at=2.0)],
        # companion healthy conditions so the single unresolved condition does
        # not itself trip the systemic STOP_TOKEN_ENUMERATION_UNRELIABLE guard
        "up_1": [_row("TOKC", "0", price=0.4, traded_at=0.0), _row("TOKC", "0", price=0.4, traded_at=4000.0), _row("TOKD", "1", price=0.5, traded_at=4000.0)],
        "up_2": [_row("TOKE", "0", price=0.4, traded_at=0.0), _row("TOKE", "0", price=0.4, traded_at=4000.0), _row("TOKF", "1", price=0.5, traded_at=4000.0)],
        "up_3": [_row("TOKG", "0", price=0.4, traded_at=0.0), _row("TOKG", "0", price=0.4, traded_at=4000.0), _row("TOKH", "1", price=0.5, traded_at=4000.0)],
    }
    sample = _ok_sample(n_up=4)
    resolved = {"up_0": 100000.0, "up_1": 100000.0, "up_2": 100000.0, "up_3": 100000.0}
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid=resolved, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["universe_reconciliation"]["token_pair_unresolved"] == 1
    assert result["universe_reconciliation"]["measured"] == 3


def test_end_to_end_invalid_window_excluded_not_counted_negative():
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.4, traded_at=1000.0),
            _row("TOKB", "1", price=0.6, traded_at=1000.0),
        ]
    }
    sample = _ok_sample(n_up=1)
    # resolved_at missing entirely -> invalid window
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={}, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["universe_reconciliation"]["no_valid_decision_window"] == 1
    assert result["universe_reconciliation"]["measured"] == 0


def test_end_to_end_neither_side_in_window_is_a_coverage_negative_not_excluded():
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.4, traded_at=1.0),  # long before window
            _row("TOKB", "1", price=0.6, traded_at=1.0),
        ]
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={"up_0": 100000.0}, trades_by_cid=trades)
    cfg = _cfg(warmup_seconds=3600.0)
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["universe_reconciliation"]["measured"] == 1
    assert result["level_b_class_counts"]["DECISION_PRICE_NEITHER"] == 1


def test_end_to_end_all_invalid_window_gives_inconclusive_verdict():
    trades = {
        "up_0": [_row("TOKA", "0", price=0.4, traded_at=1.0), _row("TOKB", "1", price=0.6, traded_at=1.0)],
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={}, trades_by_cid=trades)  # all invalid window
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["verdict"] == mod.VERDICT_INCONCLUSIVE_NO_VALID_WINDOW
    assert result["status"] == mod.VERDICT_INCONCLUSIVE_NO_VALID_WINDOW


def test_precision_loss_halts_whole_run():
    trades = {
        "up_0": [_row("TOKA", "0", traded_at=1.0), _row(5.20896e76, "1", traded_at=1.0)],
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={"up_0": 100000.0}, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_PRECISION_LOSS


def test_precision_loss_detail_includes_field_condition_id_raw_value():
    trades = {
        "up_0": [_row("TOKA", "0", traded_at=1.0), _row(5.20896e76, "1", traded_at=1.0)],
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={"up_0": 100000.0}, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_PRECISION_LOSS
    detail = result["precision_loss_detail"]
    assert "field=token_id" in detail
    assert "condition_id=up_0" in detail
    assert "5.20896e+76" in detail


def test_end_to_end_float_outcome_index_does_not_halt_reproduces_user_bug():
    """
    THE regression, at full pipeline level: real accepted-S1-shape trades where
    outcome_index is stored as a Python float (0.0 / 1.0) -- exactly the
    user-reported scenario (sample reconstruction succeeded: 300/248/52, then
    the run halted STOP_PRECISION_LOSS with "float identifier not string-safe:
    0.0" while loading trades). After the fix, this must reach a real coverage
    classification, not a precision-loss stop.
    """
    trades = {
        "up_0": [
            _row("TOKA", 0.0, price=0.4, traded_at=0.0),
            _row("TOKA", 0.0, price=0.41, traded_at=4000.0),
            _row("TOKB", 1.0, price=0.59, traded_at=4000.0),
        ],
    }
    sample = _ok_sample(n_up=1)
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={"up_0": 100000.0}, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] != mod.STOP_PRECISION_LOSS
    assert result["universe_reconciliation"]["measured"] == 1
    assert result["level_b_class_counts"]["DECISION_PRICE_BOTH_SIDES"] == 1


def test_token_enumeration_unreliable_halts_when_majority_unresolved():
    trades = {}
    for i in range(10):
        cid = f"up_{i}"
        if i < 7:
            trades[cid] = [_row(None, None, traded_at=1.0)]  # unresolved
        else:
            trades[cid] = [_row("TOKA", "0", price=0.4, traded_at=1.0), _row("TOKB", "1", price=0.6, traded_at=1.0)]
    sample = _ok_sample(n_up=10)
    resolved = {f"up_{i}": 100000.0 for i in range(10)}
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid=resolved, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["status"] == mod.STOP_TOKEN_ENUMERATION_UNRELIABLE


def test_never_uses_yes_price_or_complement_at_runtime():
    # A price observation for side_1 that would equal 1 - side_0's price must
    # NOT be derived; side_1 must come only from its own token's own prints.
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.3, traded_at=0.0),
            # No TOKB rows at all -- side_1 must be classified as unreachable,
            # never filled in as 1 - 0.3.
        ],
        "up_1": [_row("TOKC", "0", price=0.4, traded_at=0.0), _row("TOKC", "0", price=0.4, traded_at=4000.0), _row("TOKD", "1", price=0.5, traded_at=4000.0)],
        "up_2": [_row("TOKE", "0", price=0.4, traded_at=0.0), _row("TOKE", "0", price=0.4, traded_at=4000.0), _row("TOKF", "1", price=0.5, traded_at=4000.0)],
        "up_3": [_row("TOKG", "0", price=0.4, traded_at=0.0), _row("TOKG", "0", price=0.4, traded_at=4000.0), _row("TOKH", "1", price=0.5, traded_at=4000.0)],
    }
    sample = _ok_sample(n_up=4)
    resolved = {"up_0": 100000.0, "up_1": 100000.0, "up_2": 100000.0, "up_3": 100000.0}
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid=resolved, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    # side_1 token can't even be resolved (only one distinct token present) ->
    # TOKEN_PAIR_UNRESOLVED, not a fabricated coverage row.
    assert result["universe_reconciliation"]["token_pair_unresolved"] == 1


def test_reconciliation_always_sums_to_sample_size():
    trades = {
        "up_0": [_row("TOKA", "0", price=0.4, traded_at=3600.0), _row("TOKB", "1", price=0.6, traded_at=3650.0)],
        "up_1": [],  # no trade anchor
        "up_2": [_row(None, None, traded_at=1.0)],  # token pair unresolved
        "up_3": [_row("TOKC", "0", price=0.4, traded_at=1.0), _row("TOKD", "1", price=0.4, traded_at=1.0)],  # invalid window (no resolved_at)
    }
    sample = _ok_sample(n_up=4)
    loader = FakeLoader(
        sample_result=sample,
        resolved_at_by_cid={"up_0": 100000.0},  # only up_0 has a resolved_at
        trades_by_cid=trades,
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    recon = result["universe_reconciliation"]
    assert recon["sample_size"] == 4
    total = (
        recon["measured"]
        + recon["token_pair_unresolved"]
        + recon["no_trade_anchor"]
        + recon["no_valid_decision_window"]
        + recon["s1_invalid_window"]
    )
    assert total == recon["sample_size"]
    assert recon["reconciled"] is True


def test_s1_authoritative_invalid_window_ids_are_pre_excluded_never_measured():
    """
    Task point 4/5: conditions the accepted S1 run classified invalid-window
    MUST stay excluded/reported as NO_VALID_DECISION_WINDOW_AFTER_WARMUP and
    NEVER become coverage negatives -- even if this pass's local trades WOULD
    admit a measurable window. Here excl_0's trades would otherwise measure as
    BOTH_SIDES, but because it is in invalid_window_ids it is pre-excluded.
    """
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.4, traded_at=0.0),
            _row("TOKA", "0", price=0.4, traded_at=4000.0),
            _row("TOKB", "1", price=0.6, traded_at=4000.0),
        ],
        # excl_0's trades look perfectly measurable (both sides in-window)...
        "excl_0": [
            _row("TOKC", "0", price=0.4, traded_at=0.0),
            _row("TOKC", "0", price=0.4, traded_at=4000.0),
            _row("TOKD", "1", price=0.6, traded_at=4000.0),
        ],
    }
    sample = _ok_sample(n_up=1, n_excluded=1)  # excl_0 is S1-authoritative invalid-window
    loader = FakeLoader(
        sample_result=sample,
        resolved_at_by_cid={"up_0": 100000.0, "excl_0": 100000.0},  # excl_0 WOULD have a valid window
        trades_by_cid=trades,
    )
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    recon = result["universe_reconciliation"]
    assert recon["sample_size"] == 2
    # ...yet excl_0 is pre-excluded as S1 invalid-window, not measured.
    assert recon["s1_invalid_window"] == 1
    assert recon["measured"] == 1  # only up_0
    assert recon["reconciled"] is True
    # And it did NOT become a coverage negative:
    assert result["level_b_class_counts"]["DECISION_PRICE_NEITHER"] == 0
    assert result["level_b_class_counts"]["DECISION_PRICE_BOTH_SIDES"] == 1  # up_0 only


def test_s1_invalid_window_reported_in_excluded_ledger_rows():
    """The pre-excluded S1 invalid-window conditions must appear in the excluded
    ledger rows with reason NO_VALID_DECISION_WINDOW_AFTER_WARMUP (reported, not
    silently dropped)."""
    trades = {
        "up_0": [
            _row("TOKA", "0", price=0.4, traded_at=0.0),
            _row("TOKA", "0", price=0.4, traded_at=4000.0),
            _row("TOKB", "1", price=0.6, traded_at=4000.0),
        ],
        "excl_0": [_row("TOKC", "0", price=0.4, traded_at=0.0)],
    }
    sample = _ok_sample(n_up=1, n_excluded=1)
    loader = FakeLoader(
        sample_result=sample,
        resolved_at_by_cid={"up_0": 100000.0},
        trades_by_cid=trades,
    )
    writer = FakeWriter()
    cfg = _cfg(write_artifacts=True)
    result = mod.run_pass1_alt_coverage(cfg, loader, writer)
    assert writer.called is True
    excl_reasons = {(row[0], row[2]) for row in writer.excluded_rows}
    assert ("excl_0", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP") in excl_reasons


def test_s1_invalid_window_raw_diagnostic_reason_flows_through_to_own_ledger():
    """Task item 3: the raw (un-normalized) S1 excluded-reason string is
    preserved end-to-end, from reconstruction through orchestration, into this
    tool's own excluded-ledger detail column -- while the DECISION (that this
    condition is pre-excluded, never measured) is made on the normalized class
    only."""
    raw = (
        "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts=1776408162, "
        "decision_lower_ts=1776411762, resolved_at_ts=1776408318, window_seconds=-3444)"
    )
    trades = {"up_0": [_row("TOKA", "0", price=0.4, traded_at=0.0), _row("TOKB", "1", price=0.6, traded_at=4000.0)]}
    sample = _ok_sample(n_up=1, n_excluded=1, raw_reasons={"excl_0": raw})
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid={"up_0": 100000.0}, trades_by_cid=trades)
    writer = FakeWriter()
    cfg = _cfg(write_artifacts=True)
    result = mod.run_pass1_alt_coverage(cfg, loader, writer)
    detail_by_cid = {row[0]: row[3] for row in writer.excluded_rows}
    assert detail_by_cid["excl_0"] == raw
    assert "window_seconds=-3444" in detail_by_cid["excl_0"]
    # And the decision itself is still correct: pre-excluded, never measured.
    assert result["universe_reconciliation"]["s1_invalid_window"] == 1


# ---------------------------------------------------------------------------
# All-one-status guard / Level-C spot check
# ---------------------------------------------------------------------------


def test_all_one_status_detected_flag_set_and_level_c_runs():
    trades = {
        f"up_{i}": [
            _row("TOKA", "0", price=0.4, traded_at=3600.0),
            _row("TOKB", "1", price=0.6, traded_at=3650.0),
        ]
        for i in range(5)
    }
    sample = _ok_sample(n_up=5)
    resolved = {f"up_{i}": 100000.0 for i in range(5)}
    loader = FakeLoader(sample_result=sample, resolved_at_by_cid=resolved, trades_by_cid=trades)
    cfg = _cfg()
    result = mod.run_pass1_alt_coverage(cfg, loader, None)
    assert result["all_one_status_detected"] is True
    assert result["level_c_validation"]["checked"] == 5
    assert result["level_c_validation"]["passed"] is True


# ---------------------------------------------------------------------------
# Ledger schema: no price columns, ever
# ---------------------------------------------------------------------------


def test_by_condition_header_has_no_forbidden_price_columns():
    mod._assert_no_forbidden_columns(mod.BY_CONDITION_HEADER)  # must not raise
    for col in mod.BY_CONDITION_HEADER:
        assert "price" not in col.lower()


def test_writer_writes_expected_files(tmp_path):
    writer = mod.ArtifactWriter(tmp_path)
    result = {"status": "S1ALT_SOURCE_NOT_VIABLE", "verdict": "S1ALT_SOURCE_NOT_VIABLE", "per_subclass_coverage": {}}
    writer.write_all(result, by_condition_rows=[], excluded_rows=[], source_shape_text="shape\n")
    out_dir = tmp_path / "named_binary_probe" / "price_source_s1_alt"
    assert (out_dir / "price_source_s1_alt_coverage.json").is_file()
    assert (out_dir / "price_source_s1_alt_coverage.md").is_file()
    assert (out_dir / "price_source_s1_alt_coverage_by_condition.csv").is_file()
    assert (out_dir / "price_source_s1_alt_excluded.csv").is_file()
    assert (out_dir / "price_source_s1_alt_source_shape.md").is_file()

    with (out_dir / "price_source_s1_alt_coverage_by_condition.csv").open() as fh:
        header = next(csv.reader(fh))
    assert "price" not in ",".join(header).lower()


def test_writer_refuses_prices_path(tmp_path):
    writer = mod.ArtifactWriter(tmp_path)
    writer.out_dir = tmp_path / "prices" / "price_source_s1_alt"
    with pytest.raises(RuntimeError):
        writer.write_all({"status": "x"}, [], [], "shape\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_default_is_unauthorized(capsys):
    rc = mod.main([])
    assert rc == 2
    out = capsys.readouterr().out
    assert mod.STOP_NOT_AUTHORIZED in out


def test_cli_requires_root_when_authorized(capsys):
    rc = mod.main(["--i-authorize-s1-alt-pass1-local-run"])
    assert rc == 2
    out = capsys.readouterr().out
    assert "STOP_MISSING_ROOT" in out


def test_build_run_config_reflects_flags():
    parser = mod.build_arg_parser()
    args = parser.parse_args(
        ["--i-authorize-s1-alt-pass1-local-run", "--write-artifacts", "--root", "C:/b1/data"]
    )
    cfg = mod.build_run_config(args)
    assert cfg.execute is True
    assert cfg.write_artifacts is True


def test_build_run_config_default_is_safe():
    parser = mod.build_arg_parser()
    args = parser.parse_args([])
    cfg = mod.build_run_config(args)
    assert cfg.execute is False
    assert cfg.write_artifacts is False


# ---------------------------------------------------------------------------
# Real StoreLoader setup/schema paths (tmp_path; parquet tests use pandas via
# importorskip so the suite still runs where pandas is unavailable)
# ---------------------------------------------------------------------------


def _make_store_loader(tmp_path: Path) -> mod.StoreLoader:
    return mod.StoreLoader(
        root="unused",
        p0_preflight_json=tmp_path / "p0.json",
        classification_contract_json=tmp_path / "contract.json",
        resolution_source_parquet=tmp_path / "resolution.parquet",
        s1_by_condition_csv=tmp_path / "by_cond.csv",
        s1_excluded_csv=tmp_path / "excl.csv",
    )


def test_store_loader_contract_missing_file(tmp_path):
    loader = _make_store_loader(tmp_path)
    result = loader.load_contract_version()
    assert result.ok is False
    assert result.failure_reason == "missing_file"


def test_store_loader_contract_malformed_json(tmp_path):
    loader = _make_store_loader(tmp_path)
    (tmp_path / "contract.json").write_text("{not valid json", encoding="utf-8")
    result = loader.load_contract_version()
    assert result.ok is False
    assert result.failure_reason == "unreadable_or_malformed"


def test_store_loader_contract_non_dict_top_level(tmp_path):
    loader = _make_store_loader(tmp_path)
    (tmp_path / "contract.json").write_text("[1, 2, 3]", encoding="utf-8")
    result = loader.load_contract_version()
    assert result.ok is False
    assert result.failure_reason == "malformed_top_level"


def test_store_loader_contract_missing_version_field(tmp_path):
    loader = _make_store_loader(tmp_path)
    (tmp_path / "contract.json").write_text(json.dumps({"conditions": []}), encoding="utf-8")
    result = loader.load_contract_version()
    assert result.ok is False
    assert result.failure_reason == "missing_version_field"


def test_store_loader_contract_wrong_version_is_ok_result_not_schema_failure(tmp_path):
    # A wrong version must come back ok=True with the observed value -- the
    # STALE stop happens at the orchestration layer, distinguishably.
    loader = _make_store_loader(tmp_path)
    (tmp_path / "contract.json").write_text(
        json.dumps({"nb_contract_version": "nb-contract-WRONG"}), encoding="utf-8"
    )
    result = loader.load_contract_version()
    assert result.ok is True
    assert result.version == "nb-contract-WRONG"


def test_store_loader_contract_correct_version_ok(tmp_path):
    loader = _make_store_loader(tmp_path)
    (tmp_path / "contract.json").write_text(
        json.dumps({"nb_contract_version": mod.NB_CONTRACT_VERSION_EXPECTED}), encoding="utf-8"
    )
    result = loader.load_contract_version()
    assert result.ok is True
    assert result.version == mod.NB_CONTRACT_VERSION_EXPECTED


def test_store_loader_resolution_missing_file_no_pandas_needed(tmp_path):
    # The file-existence check precedes the lazy pandas import, so this path is
    # exercised even where pandas is absent.
    loader = _make_store_loader(tmp_path)
    result = loader.load_resolution_source(frozenset(["c1"]))
    assert result.ok is False
    assert result.failure_reason == "missing_file"


def test_store_loader_resolution_missing_resolved_at_column(tmp_path):
    pd = pytest.importorskip("pandas")
    pytest.importorskip("pyarrow")
    loader = _make_store_loader(tmp_path)
    df = pd.DataFrame(
        [{"condition_id": "c1", "status": "RESOLVED_SINGLE_WINNER", "nb_contract_version": mod.NB_CONTRACT_VERSION_EXPECTED}]
    )
    df.to_parquet(tmp_path / "resolution.parquet")
    result = loader.load_resolution_source(frozenset(["c1"]))
    assert result.ok is False
    assert result.failure_reason == "missing_columns"
    assert "resolved_at" in result.failure_detail


def test_store_loader_resolution_empty_table_halts(tmp_path):
    pd = pytest.importorskip("pandas")
    pytest.importorskip("pyarrow")
    loader = _make_store_loader(tmp_path)
    df = pd.DataFrame(columns=list(mod.REQUIRED_RESOLUTION_SOURCE_COLUMNS))
    df.to_parquet(tmp_path / "resolution.parquet")
    result = loader.load_resolution_source(frozenset(["c1"]))
    assert result.ok is False
    assert result.failure_reason == "empty_table"


def test_store_loader_resolution_unreadable_file(tmp_path):
    pytest.importorskip("pandas")
    loader = _make_store_loader(tmp_path)
    (tmp_path / "resolution.parquet").write_bytes(b"this is not a parquet file")
    result = loader.load_resolution_source(frozenset(["c1"]))
    assert result.ok is False
    assert result.failure_reason == "unreadable_or_malformed"


def test_store_loader_resolution_valid_table_row_level_gap_stays_row_level(tmp_path):
    pd = pytest.importorskip("pandas")
    pytest.importorskip("pyarrow")
    loader = _make_store_loader(tmp_path)
    df = pd.DataFrame(
        [
            {"condition_id": "c1", "resolved_at": "2025-06-01 00:00:00.000 UTC",
             "status": "RESOLVED_SINGLE_WINNER", "nb_contract_version": mod.NB_CONTRACT_VERSION_EXPECTED},
            # c2 is simply absent from the table -- a row-level gap, not schema
        ]
    )
    df.to_parquet(tmp_path / "resolution.parquet")
    result = loader.load_resolution_source(frozenset(["c1", "c2"]))
    assert result.ok is True
    assert result.version == mod.NB_CONTRACT_VERSION_EXPECTED
    assert "c1" in result.resolved_at_by_cid
    assert "c2" not in result.resolved_at_by_cid  # downstream per-condition exclusion


# ---------------------------------------------------------------------------
# Guardrail re-audit: executable source contains no forbidden operations
# ---------------------------------------------------------------------------


def test_no_scoring_terms_in_executable_code():
    src = Path(mod.__file__).read_text(encoding="utf-8")
    for bad in ("brier", "log_loss", "calibrat", "backtest", " roi ", "sharpe", "isotonic"):
        assert bad not in src.lower()


def test_no_pass2_or_probe_entrypoints():
    src = Path(mod.__file__).read_text(encoding="utf-8")
    for bad in ("run_pass2", "def probe", "run_probe", "backfill_prices_from_clob", "save_prices"):
        assert bad not in src
