from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "price_source_option_b_b0_failure_diagnostic.py"
spec = importlib.util.spec_from_file_location("b0_diag", MODULE_PATH)
b0_diag = importlib.util.module_from_spec(spec)
sys.modules["b0_diag"] = b0_diag
assert spec.loader is not None
spec.loader.exec_module(b0_diag)


def cond(n: int) -> str:
    return "0x" + f"{n:064x}"


def tx(n: int) -> str:
    return "0x" + f"{n:064x}"


CONDS = [cond(i + 1) for i in range(10)]


def write_manifest(tmp_path: Path) -> Path:
    source = tmp_path / "artifacts" / "named_binary_probe" / "price_source_option_b_b0" / "option_b_b0_manifest.json"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(json.dumps({"conditions": [{"condition_id": c} for c in CONDS]}), encoding="utf-8")
    return source


def local_row(condition_id: str = CONDS[0], *, price: str = "0.42", size: str = "17.5", ts: str = "2026-05-26T21:34:02Z", token: str = "12345678901234567890", tx_hash: str = tx(1)) -> dict:
    return {
        "trade_id": "local-1",
        "wallet": "0xwallet",
        "condition_id": condition_id,
        "outcome": "A",
        "side": "BUY",
        "price": price,
        "size_usdc": size,
        "traded_at": ts,
        "tx_hash": tx_hash,
        "token_id": token,
        "outcome_index": "0",
    }


def api_row(condition_id: str = CONDS[0], *, price: str = "0.42", size: str = "17.5", ts_value=1779831242, token: str = "12345678901234567890", tx_hash: str = tx(1)) -> dict:
    return {
        "conditionId": condition_id,
        "transactionHash": tx_hash,
        "asset": token,
        "outcomeIndex": "0.0",
        "side": "buy",
        "price": price,
        "size": size,
        "timestamp": ts_value,
    }


def make_fetch(pages_by_condition: dict[str, list[list[dict]]]):
    def fetch_page(condition_id: str, page_number: int, page_limit: int, taker_only):
        pages = pages_by_condition.get(condition_id, [[]])
        rows = pages[page_number] if page_number < len(pages) else []
        return b0_diag.PageResult(rows=rows)

    return fetch_page


def run_with(tmp_path: Path, *, pages_by_condition: dict[str, list[list[dict]]], local_rows: list[dict], page_limit: int = 2, max_pages: int = 1, probe_condition_count: int = 1):
    manifest = write_manifest(tmp_path)
    out_dir = tmp_path / "artifacts" / "named_binary_probe" / "price_source_option_b_b0_diag"

    def load_local(_data_root: Path, _conditions):
        return local_rows

    summary = b0_diag.run_diagnostic(
        project_root=tmp_path,
        data_root=tmp_path / "data",
        manifest_path=manifest,
        out_dir=out_dir,
        fetch_page=make_fetch(pages_by_condition),
        load_local_rows=load_local,
        page_limit=page_limit,
        max_pages=max_pages,
        probe_condition_count=probe_condition_count,
    )
    by_condition = list(__import__("csv").DictReader((out_dir / "by_condition.csv").open(newline="", encoding="utf-8")))
    mismatches = list(__import__("csv").DictReader((out_dir / "mismatches.csv").open(newline="", encoding="utf-8")))
    return summary, by_condition, mismatches, out_dir


def test_constants_and_locked_classification_vocab():
    assert b0_diag.TAU_SECONDS == 120
    assert b0_diag.SIGMA_HOURS == 24
    assert b0_diag.PRIMARY_API_ROW_LEDGER_CAP == 25_000
    assert b0_diag.EXPECTED_MANIFEST_CONDITIONS == 10
    assert {
        b0_diag.NO_TEMPORAL_OVERLAP,
        b0_diag.OVERLAP_MATCHED,
        b0_diag.OVERLAP_API_LOCAL_MISMATCH,
        b0_diag.OVERLAP_SCHEMA_BLOCKED,
        b0_diag.OVERLAP_PAGINATION_PARTIAL,
    } == b0_diag.VALID_CONDITION_CLASSIFICATIONS
    assert {b0_diag.API_ARTIFACT_COMPLETE, b0_diag.API_ARTIFACT_INCOMPLETE} == b0_diag.VALID_RUN_ARTIFACT_STATUSES


def test_manifest_must_be_fixed_ten_conditions(tmp_path: Path):
    bad = tmp_path / "manifest.json"
    bad.write_text(json.dumps({"conditions": CONDS[:9]}), encoding="utf-8")
    with pytest.raises(b0_diag.DiagnosticHalt) as exc:
        b0_diag.load_manifest(bad)
    assert exc.value.code == b0_diag.STOP_SAMPLE_SCOPE_EXCEEDED


def test_overlapped_exact_composite_match_gets_clean_label_after_artifacts_complete(tmp_path: Path):
    summary, by_condition, mismatches, out_dir = run_with(
        tmp_path,
        pages_by_condition={CONDS[0]: [[api_row()]]},
        local_rows=[local_row()],
        probe_condition_count=0,
    )
    assert summary["artifact_status"] == b0_diag.API_ARTIFACT_COMPLETE
    row0 = {row["condition_id"]: row for row in by_condition}[CONDS[0]]
    assert row0["classification"] == b0_diag.OVERLAP_MATCHED
    assert row0["matched_in_window_count"] == "1"
    assert row0["api_only_in_window_count"] == "0"
    assert row0["local_only_in_window_count"] == "0"
    assert row0["tx_hash_ambiguous_in_window_count"] == "0"
    assert mismatches == []
    offline = b0_diag.recompute_from_artifacts(out_dir)
    assert offline["classification_counts"][b0_diag.OVERLAP_MATCHED] == 1


def test_partial_pagination_takes_precedence_over_matching(tmp_path: Path):
    summary, by_condition, _mismatches, _out_dir = run_with(
        tmp_path,
        pages_by_condition={CONDS[0]: [[api_row(), api_row(tx_hash=tx(2), token="22345678901234567890")]]},
        local_rows=[local_row()],
        page_limit=2,
        max_pages=1,
    )
    row0 = {row["condition_id"]: row for row in by_condition}[CONDS[0]]
    assert summary["artifact_status"] == b0_diag.API_ARTIFACT_INCOMPLETE
    assert row0["pagination_status"] == b0_diag.PAGINATION_PARTIAL
    assert row0["classification"] == b0_diag.OVERLAP_PAGINATION_PARTIAL


def test_no_temporal_overlap_when_api_after_local_window(tmp_path: Path):
    late_api = api_row(ts_value=1779921242)  # More than 24h after the local row.
    _summary, by_condition, _mismatches, _out_dir = run_with(
        tmp_path,
        pages_by_condition={CONDS[0]: [[late_api]]},
        local_rows=[local_row()],
    )
    row0 = {row["condition_id"]: row for row in by_condition}[CONDS[0]]
    assert row0["classification"] == b0_diag.NO_TEMPORAL_OVERLAP
    assert row0["temporal_subflag"] == "API_AFTER_LOCAL_WINDOW"
    assert row0["api_after_sigma_count"] == "1"


def test_local_empty_is_not_dropped_and_is_classified(tmp_path: Path):
    _summary, by_condition, _mismatches, _out_dir = run_with(
        tmp_path,
        pages_by_condition={CONDS[0]: [[api_row()]]},
        local_rows=[],
    )
    row0 = {row["condition_id"]: row for row in by_condition}[CONDS[0]]
    assert row0["local_row_count"] == "0"
    assert row0["classification"] == b0_diag.NO_TEMPORAL_OVERLAP
    assert row0["temporal_subflag"] == "LOCAL_EMPTY"


def test_tx_hash_ambiguity_blocks_clean_match(tmp_path: Path):
    _summary, by_condition, mismatches, _out_dir = run_with(
        tmp_path,
        pages_by_condition={CONDS[0]: [[api_row(price="0.43")]]},
        local_rows=[local_row(price="0.42")],
    )
    row0 = {row["condition_id"]: row for row in by_condition}[CONDS[0]]
    assert row0["classification"] == b0_diag.OVERLAP_API_LOCAL_MISMATCH
    assert row0["tx_hash_ambiguous_in_window_count"] == "2"
    assert {row["mismatch_type"] for row in mismatches} == {"TX_HASH_AMBIGUOUS"}


def test_row_cap_halt_persists_incomplete_artifacts(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(b0_diag, "PRIMARY_API_ROW_LEDGER_CAP", 1)
    manifest = write_manifest(tmp_path)
    out_dir = tmp_path / "artifacts" / "named_binary_probe" / "price_source_option_b_b0_diag"

    def load_local(_data_root: Path, _conditions):
        return []

    rows = [api_row(tx_hash=tx(3)), api_row(tx_hash=tx(4), token="777")]
    with pytest.raises(b0_diag.DiagnosticHalt) as exc:
        b0_diag.run_diagnostic(
            project_root=tmp_path,
            data_root=tmp_path / "data",
            manifest_path=manifest,
            out_dir=out_dir,
            fetch_page=make_fetch({CONDS[0]: [rows]}),
            load_local_rows=load_local,
            page_limit=3,
            max_pages=1,
            probe_condition_count=0,
        )
    assert exc.value.code == b0_diag.STOP_ROW_LEDGER_CAP_EXCEEDED
    reconciliation = json.loads((out_dir / "reconciliation.json").read_text(encoding="utf-8"))
    assert reconciliation["artifact_status"] == b0_diag.API_ARTIFACT_INCOMPLETE
    assert reconciliation["halt_code"] == b0_diag.STOP_ROW_LEDGER_CAP_EXCEEDED
    assert (out_dir / "api_rows.csv").exists()
    assert (out_dir / "local_rows.csv").exists()
    assert (out_dir / "mismatches.csv").exists()


def test_main_refuses_network_path_without_dual_flags(capsys):
    rc = b0_diag.main([])
    captured = capsys.readouterr()
    assert rc == 2
    assert b0_diag.STOP_NOT_AUTHORIZED in captured.err


def test_atomic_writers_are_repeat_replace_safe(tmp_path: Path):
    target_text = tmp_path / "nested" / "local_load_provenance.json"
    target_csv = tmp_path / "nested" / "schema_errors.csv"
    target_jsonl = tmp_path / "nested" / "api_raw_rows.jsonl"
    for idx in range(25):
        b0_diag.atomic_write_json(target_text, {"idx": idx})
        b0_diag.atomic_write_csv(target_csv, [{"condition_id": cond(1), "error_code": "X"}], b0_diag.SCHEMA_ERROR_COLUMNS)
        b0_diag.atomic_write_jsonl(target_jsonl, [{"idx": idx, "raw_json": "{}"}])
    assert json.loads(target_text.read_text(encoding="utf-8"))["idx"] == 24
    assert len(list(csv.DictReader(target_csv.open(newline="", encoding="utf-8")))) == 1
    assert len([line for line in target_jsonl.read_text(encoding="utf-8").splitlines() if line]) == 1




def test_atomic_writers_retry_replace_after_permission_error(tmp_path: Path, monkeypatch):
    original_replace = b0_diag.os.replace
    calls = {"count": 0}

    def flaky_replace(src, dst):
        calls["count"] += 1
        if calls["count"] == 1:
            raise PermissionError("simulated WinError 5")
        return original_replace(src, dst)

    monkeypatch.setattr(b0_diag.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(b0_diag.os, "replace", flaky_replace)

    target = tmp_path / "nested" / "retry.json"
    b0_diag.atomic_write_json(target, {"ok": True})

    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}
    assert calls["count"] == 2
    assert list(target.parent.glob(f".{target.name}.*.tmp")) == []


def test_atomic_writers_fallback_to_direct_write_when_replace_keeps_failing(tmp_path: Path, monkeypatch):
    def always_fail_replace(_src, _dst):
        raise PermissionError("simulated persistent WinError 5")

    monkeypatch.setattr(b0_diag.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(b0_diag.os, "replace", always_fail_replace)

    target_text = tmp_path / "nested" / "fallback.txt"
    target_json = tmp_path / "nested" / "fallback.json"
    target_csv = tmp_path / "nested" / "fallback.csv"
    target_jsonl = tmp_path / "nested" / "fallback.jsonl"

    b0_diag.atomic_write_text(target_text, "hello\n")
    b0_diag.atomic_write_json(target_json, {"idx": 1})
    b0_diag.atomic_write_csv(target_csv, [{"condition_id": cond(1), "error_code": "X"}], b0_diag.SCHEMA_ERROR_COLUMNS)
    b0_diag.atomic_write_jsonl(target_jsonl, [{"idx": 1}, {"idx": 2}])

    assert target_text.read_text(encoding="utf-8") == "hello\n"
    assert json.loads(target_json.read_text(encoding="utf-8"))["idx"] == 1
    assert len(list(csv.DictReader(target_csv.open(newline="", encoding="utf-8")))) == 1
    assert [json.loads(line)["idx"] for line in target_jsonl.read_text(encoding="utf-8").splitlines()] == [1, 2]
    assert list(target_text.parent.glob(".*.tmp")) == []


def test_requests_fetcher_uses_market_param(monkeypatch):
    captured = {}

    class Response:
        status_code = 200
        def json(self):
            return []

    def fake_get(endpoint, params, timeout):
        captured["endpoint"] = endpoint
        captured["params"] = params
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setitem(sys.modules, "requests", type("Requests", (), {"get": staticmethod(fake_get)}))
    fetch = b0_diag.make_requests_fetcher("https://example.invalid/trades", timeout_seconds=7)
    fetch(CONDS[0], 0, 500, True)
    assert captured["params"]["market"] == CONDS[0]
    assert "condition_id" not in captured["params"]
    assert captured["params"]["takerOnly"] == "true"


def test_doc_shaped_api_row_and_outcome_index_float_forms():
    normalized = b0_diag.normalize_api_row(
        api_row(),
        query_condition_id=CONDS[0],
        query_mode=b0_diag.QUERY_MODE_PRIMARY,
        page_number=0,
        page_limit=10,
        row_number_in_page=0,
        retrieved_at_utc="2026-01-01T00:00:00Z",
    )
    assert normalized["condition_id"] == CONDS[0]
    assert normalized["tx_hash"] == tx(1)
    for value in (0.0, 1.0, "0.0", "1.0", 0, 1):
        assert b0_diag.normalize_outcome_index(value) in {"0", "1"}
    with pytest.raises(b0_diag.DiagnosticHalt):
        b0_diag.normalize_outcome_index(2.0)
    with pytest.raises(b0_diag.DiagnosticHalt) as exc:
        b0_diag.canonical_int_string(1.23e76, field_name="token_id")
    assert exc.value.code == b0_diag.STOP_PRECISION_LOSS
