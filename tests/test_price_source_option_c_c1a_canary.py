"""Pure-logic tests for Option C C1A bounded canary reconciliation.

No network. No local Store / pandas dependency exercised here (LocalTxHashLoader's
real methods are lazy-imported and not invoked by these tests).
"""

import importlib.util
import csv
import json
import os
import sys
from datetime import datetime, timezone

import pytest

_HERE = os.path.dirname(__file__)
_SCRIPT = os.path.abspath(
    os.path.join(_HERE, "..", "scripts", "price_source_option_c_c1a_canary.py")
)
_spec = importlib.util.spec_from_file_location("price_source_option_c_c1a_canary", _SCRIPT)
canary = importlib.util.module_from_spec(_spec)
sys.modules["price_source_option_c_c1a_canary"] = canary
_spec.loader.exec_module(canary)

CID = "0x" + "a" * 64
T0 = "1" + "0" * 74 + "99"
T1 = "2" + "0" * 74 + "99"


def _manifest(**overrides):
    base = dict(
        condition_id=CID,
        side_0_token_id=T0,
        side_1_token_id=T1,
        window_start_utc="2025-01-01 00:00:00",
        window_end_utc="2025-01-02 00:00:00",
        per_condition_row_cap=5,
        global_row_cap=5,
        source_table_version="polymarket_polygon.ctfexchange_evt_orderfilled",
    )
    base.update(overrides)
    return {CID: canary.ManifestEntry(**base)}


def _row(**overrides):
    base = dict(
        condition_id=CID,
        tx_hash="0xNEW1",
        block_time="2025-01-01 01:00:00",
        makerAssetId=T0,
        takerAssetId=T1,
        makerAmountFilled="100",
        takerAmountFilled="200",
        source_provenance="polymarket_polygon.ctfexchange_evt_orderfilled",
    )
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# canonical_int precision discipline (event-row level)
# ---------------------------------------------------------------------------
def test_canonical_int_rejects_scientific_notation():
    with pytest.raises(canary.DataExportPrecisionLoss):
        canary.canonical_int("5.2e76")


def test_parse_ts_utc_accepts_dune_fractional_utc_string():
    got = canary.parse_ts_utc("2025-05-21 23:59:22.000 UTC")
    expected = datetime(2025, 5, 21, 23, 59, 22, tzinfo=timezone.utc).timestamp()
    assert got == expected


def test_parse_ts_utc_accepts_dune_second_precision_utc_string():
    got = canary.parse_ts_utc("2025-05-21 23:59:22 UTC")
    expected = datetime(2025, 5, 21, 23, 59, 22, tzinfo=timezone.utc).timestamp()
    assert got == expected


def test_parse_ts_utc_accepts_datetime_like_values_as_utc():
    aware = datetime(2025, 5, 21, 23, 59, 22, tzinfo=timezone.utc)
    naive = datetime(2025, 5, 21, 23, 59, 22)
    assert canary.parse_ts_utc(aware) == aware.timestamp()
    assert canary.parse_ts_utc(naive) == aware.timestamp()


# ---------------------------------------------------------------------------
# validate_and_tag_row
# ---------------------------------------------------------------------------
def test_validate_and_tag_row_tags_side_0():
    manifest = _manifest()[CID]
    row = canary.validate_and_tag_row(_row(makerAssetId=T0, takerAssetId="9" * 5), manifest)
    assert row.matched_side == "side_0"


def test_validate_and_tag_row_tags_side_1():
    manifest = _manifest()[CID]
    row = canary.validate_and_tag_row(_row(makerAssetId="9" * 5, takerAssetId=T1), manifest)
    assert row.matched_side == "side_1"


def test_validate_and_tag_row_unresolved_if_neither_token_matches():
    manifest = _manifest()[CID]
    row = canary.validate_and_tag_row(_row(makerAssetId="9" * 5, takerAssetId="8" * 5), manifest)
    assert row.matched_side == "UNRESOLVED"


def test_validate_and_tag_row_halts_on_missing_field():
    manifest = _manifest()[CID]
    bad = _row()
    del bad["tx_hash"]
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.validate_and_tag_row(bad, manifest)
    assert exc.value.code == canary.C1_SOURCE_SCHEMA_UNVERIFIED


def test_validate_and_tag_row_halts_on_precision_loss():
    manifest = _manifest()[CID]
    bad = _row(makerAmountFilled="5.2e76")
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.validate_and_tag_row(bad, manifest)
    assert exc.value.code == canary.C1_SOURCE_SCHEMA_UNVERIFIED


# ---------------------------------------------------------------------------
# run_canary - clean pass, caps, reproduction-only, indexer-shaped
# ---------------------------------------------------------------------------
def test_run_canary_clean_pass_surfaces_new_and_overlap():
    manifest = _manifest()
    rows = [_row(tx_hash="0xNEW1"), _row(tx_hash="0xLOCAL1")]
    local = {CID: {"0xLOCAL1"}}
    coverage, tagged = canary.run_canary(manifest, rows, local)
    cov = coverage[CID]
    assert cov.dune_rows_in_window == 2
    assert cov.dune_only_tx_hashes == {"0xNEW1"}
    assert cov.overlap_tx_hashes == {"0xLOCAL1"}
    assert len(tagged) == 2


def test_run_canary_halts_local_reproduction_only():
    manifest = _manifest()
    rows = [_row(tx_hash="0xLOCAL1")]  # Dune only returns what local already has
    local = {CID: {"0xLOCAL1"}}
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, local)
    assert exc.value.code == canary.C1_LOCAL_TX_HASH_REPRODUCTION_ONLY


def test_run_canary_empty_rows_halts_source_empty_not_design_clear():
    """Patch requirement 2 (prior BLOCK): an empty Dune export must halt with
    C1_SOURCE_EMPTY and must never be mistaken for / equal to
    C1_CANARY_DESIGN_CLEAR."""
    manifest = _manifest()
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, [], {CID: set()})
    assert exc.value.code == canary.C1_SOURCE_EMPTY
    assert exc.value.code != canary.C1_CANARY_DESIGN_CLEAR


def test_run_canary_halts_on_per_condition_row_explosion():
    manifest = _manifest(per_condition_row_cap=1, global_row_cap=5)
    rows = [_row(tx_hash="0xNEW1"), _row(tx_hash="0xNEW2")]
    local = {CID: set()}
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, local)
    assert exc.value.code == canary.C1_ROW_EXPLOSION


def test_run_canary_halts_on_global_row_explosion():
    manifest = _manifest(per_condition_row_cap=5, global_row_cap=1)
    rows = [_row(tx_hash="0xNEW1"), _row(tx_hash="0xNEW2")]
    local = {CID: set()}
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, local)
    assert exc.value.code == canary.C1_ROW_EXPLOSION


def test_run_canary_halts_on_out_of_window_row():
    manifest = _manifest()
    rows = [_row(tx_hash="0xNEW1", block_time="2025-06-01 00:00:00")]
    local = {CID: set()}
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, local)
    assert exc.value.code == canary.C1_INDEXER_SHAPED


def test_run_canary_halts_on_unrequested_condition():
    manifest = _manifest()
    other_cid = "0x" + "b" * 64
    rows = [_row(condition_id=other_cid, tx_hash="0xNEW1")]
    local = {CID: set()}
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, local)
    assert exc.value.code == canary.C1_INDEXER_SHAPED


def test_run_canary_halts_on_missing_ordering_key_when_required():
    manifest = _manifest()
    rows = [_row(tx_hash="0xNEW1")]  # no ordering_key field at all
    local = {CID: set()}
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, local, require_ordering_key=True)
    assert exc.value.code == canary.C1_ORDERING_KEY_MISSING


def test_run_canary_per_condition_cap_plus_one_triggers_explosion():
    """Patch requirement 1, worded exactly: per_condition_row_cap + 1 rows for
    one condition must trigger C1_ROW_EXPLOSION."""
    cap = 3
    manifest = _manifest(per_condition_row_cap=cap, global_row_cap=100)
    rows = [_row(tx_hash=f"0xNEW{i}") for i in range(cap + 1)]  # cap+1 rows
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, {CID: set()})
    assert exc.value.code == canary.C1_ROW_EXPLOSION


def test_run_canary_per_condition_at_exactly_cap_does_not_explode():
    """Exactly at the cap (not cap+1) must NOT trigger explosion - only
    exceeding the cap does."""
    cap = 3
    manifest = _manifest(per_condition_row_cap=cap, global_row_cap=100)
    rows = [_row(tx_hash=f"0xNEW{i}") for i in range(cap)]  # exactly cap rows
    coverage, tagged = canary.run_canary(manifest, rows, {CID: set()})
    assert coverage[CID].dune_rows_in_window == cap
    assert len(tagged) == cap


def test_run_canary_global_cap_plus_one_triggers_explosion():
    """Patch requirement 1: global_row_cap + 1 rows total (across conditions)
    must trigger C1_ROW_EXPLOSION even if no single condition exceeds its own
    per-condition cap."""
    cid2 = "0x" + "b" * 64
    manifest = {
        CID: canary.ManifestEntry(
            condition_id=CID,
            side_0_token_id=T0,
            side_1_token_id=T1,
            window_start_utc="2025-01-01 00:00:00",
            window_end_utc="2025-01-02 00:00:00",
            per_condition_row_cap=10,
            global_row_cap=3,
            source_table_version="polymarket_polygon.ctfexchange_evt_orderfilled",
        ),
        cid2: canary.ManifestEntry(
            condition_id=cid2,
            side_0_token_id=T0,
            side_1_token_id=T1,
            window_start_utc="2025-01-01 00:00:00",
            window_end_utc="2025-01-02 00:00:00",
            per_condition_row_cap=10,
            global_row_cap=3,
            source_table_version="polymarket_polygon.ctfexchange_evt_orderfilled",
        ),
    }
    rows = [
        _row(tx_hash="0xA1"),
        _row(tx_hash="0xA2"),
        _row(condition_id=cid2, tx_hash="0xB1"),
        _row(condition_id=cid2, tx_hash="0xB2"),  # 4 total > global_row_cap=3
    ]
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, {CID: set(), cid2: set()})
    assert exc.value.code == canary.C1_ROW_EXPLOSION


def test_canary_halt_carries_partial_evidence_for_persist_before_halt():
    cap = 1
    manifest = _manifest(per_condition_row_cap=cap, global_row_cap=100)
    rows = [_row(tx_hash="0xA"), _row(tx_hash="0xB")]
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, {CID: set()})
    halt = exc.value
    assert len(halt.partial_raw_rows) == 2
    assert len(halt.partial_tagged_rows) == 2
    assert CID in halt.partial_coverage


# ---------------------------------------------------------------------------
# Row-level artifact writer (patch requirement 4)
# ---------------------------------------------------------------------------
def test_write_row_level_artifacts_includes_matched_side_and_relation(tmp_path):
    manifest = _manifest()
    rows = [_row(tx_hash="0xNEW1", makerAssetId=T0, takerAssetId="9" * 5)]
    local = {CID: {"0xLOCAL1"}}
    coverage, tagged = canary.run_canary(manifest, rows, local)
    canary.write_row_level_artifacts(str(tmp_path), rows, tagged, coverage)

    tagged_path = tmp_path / "option_c_c1a_tagged_rows.csv"
    assert tagged_path.exists()
    with open(tagged_path, newline="", encoding="utf-8") as fh:
        out_rows = list(csv.DictReader(fh))

    by_tx = {r["tx_hash"]: r for r in out_rows}
    assert by_tx["0xNEW1"]["matched_side"] == "side_0"
    assert by_tx["0xNEW1"]["tx_hash_relation"] == canary.REL_DUNE_ONLY
    assert by_tx["0xLOCAL1"]["tx_hash_relation"] == canary.REL_LOCAL_ONLY
    assert by_tx["0xLOCAL1"]["matched_side"] == "N/A"

    raw_path = tmp_path / "option_c_c1a_raw_rows_sample.csv"
    assert raw_path.exists()
    with open(raw_path, newline="", encoding="utf-8") as fh:
        raw_out = list(csv.DictReader(fh))
    assert len(raw_out) == 1
    assert raw_out[0]["tx_hash"] == "0xNEW1"


def test_write_row_level_artifacts_called_on_halt_with_partial_evidence(tmp_path):
    cap = 1
    manifest = _manifest(per_condition_row_cap=cap, global_row_cap=100)
    rows = [_row(tx_hash="0xA"), _row(tx_hash="0xB")]
    with pytest.raises(canary.CanaryHalt) as exc:
        canary.run_canary(manifest, rows, {CID: set()})
    halt = exc.value
    canary.write_row_level_artifacts(
        str(tmp_path), halt.partial_raw_rows, halt.partial_tagged_rows, halt.partial_coverage
    )
    tagged_path = tmp_path / "option_c_c1a_tagged_rows.csv"
    with open(tagged_path, newline="", encoding="utf-8") as fh:
        out_rows = list(csv.DictReader(fh))
    assert len(out_rows) == 2  # both rows persisted even though the run halted


# ---------------------------------------------------------------------------
# End-to-end main(): non-halt run reports EXECUTED_NEEDS_REVIEW, never
# DESIGN_CLEAR (patch requirement 3)
# ---------------------------------------------------------------------------
def test_main_non_halt_run_reports_executed_needs_review_not_design_clear(tmp_path, monkeypatch):
    manifest_doc = {
        "phase": "OPTION_C_C1A_SELECTOR_MANIFEST",
        "conditions": [
            {
                "condition_id": CID,
                "side_0_token_id": T0,
                "side_1_token_id": T1,
                "window_start_utc": "2025-01-01 00:00:00",
                "window_end_utc": "2025-01-02 00:00:00",
                "per_condition_row_cap": 10,
                "global_row_cap": 10,
                "source_table_version": "polymarket_polygon.ctfexchange_evt_orderfilled",
            }
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest_doc), encoding="utf-8")

    dune_csv_path = tmp_path / "dune_export.csv"
    with open(dune_csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "condition_id",
                "tx_hash",
                "block_time",
                "makerAssetId",
                "takerAssetId",
                "makerAmountFilled",
                "takerAmountFilled",
                "source_provenance",
            ],
        )
        w.writeheader()
        w.writerow(_row(tx_hash="0xNEW1"))

    out_dir = tmp_path / "out"

    # Avoid the lazy pandas/Store import: local trades are empty (Dune's row
    # is genuinely new relative to local, which is required to avoid
    # C1_LOCAL_TX_HASH_REPRODUCTION_ONLY).
    monkeypatch.setattr(canary.LocalTxHashLoader, "load", lambda self, manifest: {CID: set()})

    rc = canary.main(
        [
            "--manifest",
            str(manifest_path),
            "--dune-csv",
            str(dune_csv_path),
            "--out-dir",
            str(out_dir),
        ]
    )
    assert rc == 0

    with open(out_dir / "c1a_canary_result.json", encoding="utf-8") as fh:
        result = json.load(fh)
    assert result["outcome"] == canary.C1_CANARY_EXECUTED_NEEDS_REVIEW
    assert result["outcome"] != canary.C1_CANARY_DESIGN_CLEAR
    assert (out_dir / "option_c_c1a_tagged_rows.csv").exists()
    assert (out_dir / "option_c_c1a_raw_rows_sample.csv").exists()



def test_main_accepts_utf8_bom_prefixed_dune_csv_header(tmp_path, monkeypatch):
    manifest_doc = {
        "phase": "OPTION_C_C1A_SELECTOR_MANIFEST",
        "conditions": [
            {
                "condition_id": CID,
                "side_0_token_id": T0,
                "side_1_token_id": T1,
                "window_start_utc": "2025-05-21 00:00:00 UTC",
                "window_end_utc": "2025-05-22 00:00:00 UTC",
                "per_condition_row_cap": 10,
                "global_row_cap": 10,
                "source_table_version": "polymarket_polygon.ctfexchange_evt_orderfilled",
            }
        ],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest_doc), encoding="utf-8")

    dune_csv_path = tmp_path / "dune_export_bom.csv"
    with open(dune_csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=[
                "condition_id",
                "tx_hash",
                "block_time",
                "makerAssetId",
                "takerAssetId",
                "makerAmountFilled",
                "takerAmountFilled",
                "source_provenance",
            ],
        )
        w.writeheader()
        w.writerow(_row(tx_hash="0xNEW_BOM", block_time="2025-05-21 23:59:22.000 UTC"))

    out_dir = tmp_path / "out_bom"
    monkeypatch.setattr(canary.LocalTxHashLoader, "load", lambda self, manifest: {CID: set()})

    rc = canary.main(
        [
            "--manifest",
            str(manifest_path),
            "--dune-csv",
            str(dune_csv_path),
            "--out-dir",
            str(out_dir),
        ]
    )
    assert rc == 0
    with open(out_dir / "c1a_canary_result.json", encoding="utf-8") as fh:
        result = json.load(fh)
    assert result["outcome"] == canary.C1_CANARY_EXECUTED_NEEDS_REVIEW
