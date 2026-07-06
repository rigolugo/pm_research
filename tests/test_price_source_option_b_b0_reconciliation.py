from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "price_source_option_b_b0_reconciliation.py"
spec = importlib.util.spec_from_file_location("option_b_b0", MODULE_PATH)
b0 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = b0
spec.loader.exec_module(b0)

CID_PREFIX = "0x"
CID_A = CID_PREFIX + "a" * 64
CID_B = CID_PREFIX + "b" * 64
CID_C = CID_PREFIX + "c" * 64
CID_D = CID_PREFIX + "d" * 64
CID_E = CID_PREFIX + "e" * 64
TOKEN0 = "123456789012345678901234567890123456789012345678901234567890123456789012345678"
TOKEN1 = "223456789012345678901234567890123456789012345678901234567890123456789012345678"
TX0 = "0x" + "1" * 64
TX1 = "0x" + "2" * 64
TX2 = "0x" + "3" * 64


def trade(condition_id=CID_A, token_id=TOKEN0, outcome_index="0", side="BUY", price="0.42", size="10.5", timestamp="2025-03-06 00:00:00.000 UTC", tx_hash=TX0):
    return {
        "condition_id": condition_id,
        "asset": token_id,
        "token_id": token_id,
        "outcome_index": outcome_index,
        "side": side,
        "price": price,
        "size": size,
        "size_usdc": size,
        "timestamp": timestamp,
        "traded_at": timestamp,
        "tx_hash": tx_hash,
        "transactionHash": tx_hash,
    }


class FakeClient:
    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def fetch_trades(self, *, condition_id, limit, offset, taker_only):
        self.calls.append((condition_id, limit, offset, taker_only))
        value = self.pages.get((condition_id, taker_only, offset), [])
        if isinstance(value, Exception):
            raise value
        return value


def write_manifest(tmp_path, conditions=None, **overrides):
    if conditions is None:
        conditions = [CID_A[:-1] + f"{i:x}" for i in range(10)]
    data = {
        "source_artifact": "artifacts/named_binary_probe/price_source_s1_alt/price_source_s1_alt_coverage_by_condition.csv",
        "source_verdict": "S1ALT_SOURCE_NOT_VIABLE",
        "selection_basis": "accepted Option A BOTH_SIDES rows from S1-ALT by-condition ledger",
        "provenance_attestation": "Fixed Phase B0 sample drawn from accepted BOTH_SIDES rows; provenance attested.",
        "conditions": [
            {"condition_id": cid, "subclass": "UP_DOWN", "level_b_class": "BOTH_SIDES"}
            for cid in conditions
        ],
    }
    data.update(overrides)
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_unauthorized_run_halts_before_client_call(tmp_path):
    manifest = write_manifest(tmp_path)
    client = FakeClient({})
    result = b0.run_b0(
        root=tmp_path,
        manifest_path=manifest,
        artifacts_dir=tmp_path / "artifacts",
        allow_network_option_b_b0=True,
        confirm_external_polymarket_data_api=False,
        client=client,
        local_trades=[],
        write_artifacts=False,
    )
    assert result["status"] == b0.STOP_NOT_AUTHORIZED
    assert client.calls == []
    assert result["no_price_series_persisted"] is True


@pytest.mark.parametrize(
    "bad_row,expected_status",
    [
        ({"price": "abc"}, b0.STOP_SCHEMA_DEVIATION),
        ({"price": "NaN"}, b0.STOP_SCHEMA_DEVIATION),
        ({"price": "inf"}, b0.STOP_SCHEMA_DEVIATION),
        ({"asset": "1.23e+76"}, b0.STOP_PRECISION_LOSS),
        ({"asset": float(123)}, b0.STOP_PRECISION_LOSS),
        ({"outcome_index": "0.5"}, b0.STOP_SCHEMA_DEVIATION),
        ({"condition_id": "not-a-condition"}, b0.STOP_SCHEMA_DEVIATION),
        ({"timestamp": "abc"}, b0.STOP_SCHEMA_DEVIATION),
        ({"yes_price": "0.5"}, b0.STOP_FORBIDDEN_INFERENCE),
    ],
)
def test_schema_precision_and_forbidden_inference_halts(bad_row, expected_status):
    row = trade()
    row.update(bad_row)
    with pytest.raises(b0.B0Halt) as exc:
        b0.normalize_trade_row(row, expected_condition_id=CID_A, source="api", raw_index=0, aliases=b0.API_ALIASES)
    assert exc.value.status == expected_status


def test_outcome_index_integral_float_is_slot_safe_not_precision_loss():
    row = trade(outcome_index=0.0)
    normalized = b0.normalize_trade_row(row, expected_condition_id=CID_A, source="api", raw_index=0, aliases=b0.API_ALIASES)
    assert normalized.outcome_index == 0


def test_manifest_rejects_placeholder_and_bad_scope(tmp_path):
    path = write_manifest(tmp_path, provenance_attestation="TODO placeholder sample")
    with pytest.raises(b0.B0Halt) as exc:
        b0.load_condition_manifest(path)
    assert exc.value.status == b0.STOP_SAMPLE_SCOPE_EXCEEDED

    path = write_manifest(tmp_path, conditions=[CID_A])
    with pytest.raises(b0.B0Halt) as exc:
        b0.load_condition_manifest(path)
    assert exc.value.status == b0.STOP_SAMPLE_SCOPE_EXCEEDED


def test_manifest_can_verify_against_source_csv(tmp_path):
    manifest = write_manifest(tmp_path)
    cids = [c["condition_id"] for c in json.loads(manifest.read_text())["conditions"]]
    source_csv = tmp_path / "source.csv"
    source_csv.write_text(
        "condition_id,level_b_class\n" + "\n".join(f"{cid},BOTH_SIDES" for cid in cids) + "\n",
        encoding="utf-8",
    )
    loaded = b0.load_condition_manifest(manifest, provenance_source_csv=source_csv)
    assert len(loaded.conditions) == 10

    source_csv.write_text(f"condition_id,level_b_class\n{cids[0]},ONE_SIDE\n", encoding="utf-8")
    with pytest.raises(b0.B0Halt) as exc:
        b0.load_condition_manifest(manifest, provenance_source_csv=source_csv)
    assert exc.value.status == b0.STOP_SAMPLE_SCOPE_EXCEEDED


def test_pagination_short_final_page_is_complete():
    client = FakeClient({(CID_A, False, 0): [trade()]})
    rows, stats = b0.fetch_complete_condition_trades(
        client,
        condition_id=CID_A,
        limit=2,
        max_pages=5,
        taker_only=False,
        budget=b0.CallBudget(max_calls=10),
    )
    assert len(rows) == 1
    assert stats.complete is True
    assert stats.pages_fetched == 1


def test_pagination_full_final_page_halts_as_partial_retrieval():
    client = FakeClient({(CID_A, False, 0): [trade()], (CID_A, False, 1): [trade(tx_hash=TX1)]})
    with pytest.raises(b0.B0Halt) as exc:
        b0.fetch_complete_condition_trades(
            client,
            condition_id=CID_A,
            limit=1,
            max_pages=2,
            taker_only=False,
            budget=b0.CallBudget(max_calls=10),
        )
    assert exc.value.status == b0.STOP_PAGINATION_PARTIAL_RETRIEVAL


def test_call_budget_preflight_halts():
    with pytest.raises(b0.B0Halt) as exc:
        b0.validate_caps(sample_size=20, page_limit=500, max_pages_per_condition=5, total_call_budget=100, taker_only_probe_count=3)
    assert exc.value.status == b0.STOP_CALL_BUDGET_EXCEEDED


def test_one_to_one_composite_reconciliation_does_not_double_match_same_tx_hash():
    local = [
        b0.normalize_trade_row(trade(tx_hash=TX0, token_id=TOKEN0, outcome_index="0", price="0.42"), expected_condition_id=CID_A, source="local", raw_index=0, aliases=b0.LOCAL_ALIASES)
    ]
    api = [
        b0.normalize_trade_row(trade(tx_hash=TX0, token_id=TOKEN0, outcome_index="0", price="0.42"), expected_condition_id=CID_A, source="api", raw_index=0, aliases=b0.API_ALIASES),
        b0.normalize_trade_row(trade(tx_hash=TX0, token_id=TOKEN1, outcome_index="1", price="0.58"), expected_condition_id=CID_A, source="api", raw_index=1, aliases=b0.API_ALIASES),
    ]
    rec = b0.reconcile_trades(condition_id=CID_A, api_trades=api, local_trades=local)
    assert rec.matched_count == 1
    assert rec.mismatch_count == 1
    assert rec.mismatches[0]["mismatch_type"] == "TX_HASH_AMBIGUOUS"


def test_two_distinct_rows_sharing_tx_hash_can_both_match():
    local_rows = [
        trade(tx_hash=TX0, token_id=TOKEN0, outcome_index="0", price="0.42"),
        trade(tx_hash=TX0, token_id=TOKEN1, outcome_index="1", price="0.58"),
    ]
    api_rows = list(local_rows)
    local = [b0.normalize_trade_row(r, expected_condition_id=CID_A, source="local", raw_index=i, aliases=b0.LOCAL_ALIASES) for i, r in enumerate(local_rows)]
    api = [b0.normalize_trade_row(r, expected_condition_id=CID_A, source="api", raw_index=i, aliases=b0.API_ALIASES) for i, r in enumerate(api_rows)]
    rec = b0.reconcile_trades(condition_id=CID_A, api_trades=api, local_trades=local)
    assert rec.clean is True
    assert rec.matched_count == 2


def test_api_local_mismatch_halts_in_run(tmp_path):
    manifest = write_manifest(tmp_path)
    cids = [c["condition_id"] for c in json.loads(manifest.read_text())["conditions"]]
    pages = {(cid, False, 0): [trade(condition_id=cid, tx_hash=TX0)] for cid in cids}
    client = FakeClient(pages)
    local = {cid: [trade(condition_id=cid, tx_hash=TX1)] for cid in cids}
    result = b0.run_b0(
        root=tmp_path,
        manifest_path=manifest,
        artifacts_dir=tmp_path / "artifacts",
        allow_network_option_b_b0=True,
        confirm_external_polymarket_data_api=True,
        client=client,
        local_trades=local,
        page_limit=2,
        max_pages_per_condition=1,
        total_call_budget=20,
        taker_only_probe_count=0,
        write_artifacts=False,
    )
    assert result["status"] == b0.STOP_API_LOCAL_MISMATCH


def test_taker_only_true_must_be_subset_of_false():
    full = [
        b0.normalize_trade_row(trade(tx_hash=TX0), expected_condition_id=CID_A, source="api", raw_index=0, aliases=b0.API_ALIASES)
    ]
    taker = [
        b0.normalize_trade_row(trade(tx_hash=TX1), expected_condition_id=CID_A, source="api", raw_index=0, aliases=b0.API_ALIASES)
    ]
    with pytest.raises(b0.B0Halt) as exc:
        b0.verify_taker_only_probe(condition_id=CID_A, full_api_trades=full, taker_only_trades=taker)
    assert exc.value.status == b0.STOP_TAKER_ONLY_CARDINALITY_UNRESOLVED


def test_happy_path_synthetic_b0_writes_reconciliation_only(tmp_path):
    manifest = write_manifest(tmp_path)
    cids = [c["condition_id"] for c in json.loads(manifest.read_text())["conditions"]]
    pages = {}
    local = {}
    for i, cid in enumerate(cids):
        tx = "0x" + f"{i + 1:x}" * 64
        tx = tx[:66]
        row = trade(condition_id=cid, tx_hash=tx)
        pages[(cid, False, 0)] = [row]
        pages[(cid, True, 0)] = [row] if i < 2 else []
        local[cid] = [row]
    client = FakeClient(pages)
    result = b0.run_b0(
        root=tmp_path,
        manifest_path=manifest,
        artifacts_dir=tmp_path / "artifacts",
        allow_network_option_b_b0=True,
        confirm_external_polymarket_data_api=True,
        client=client,
        local_trades=local,
        page_limit=2,
        max_pages_per_condition=1,
        total_call_budget=20,
        taker_only_probe_count=2,
        write_artifacts=True,
    )
    assert result["status"] == b0.STATUS_OK
    out_dir = tmp_path / "artifacts" / "named_binary_probe" / "price_source_option_b_b0"
    assert (out_dir / "option_b_b0_reconciliation.json").exists()
    assert not any("price_series" in p.name for p in out_dir.iterdir())
    assert result["no_price_series_persisted"] is True


def test_output_path_guard_rejects_prices_path(tmp_path):
    with pytest.raises(b0.B0Halt) as exc:
        b0.assert_output_path_allowed(tmp_path / "prices" / "x.json")
    assert exc.value.status == b0.STOP_NO_WRITE_PATH
