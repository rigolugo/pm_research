"""Tests for OrdersMatched asset-id canonical-int normalization (the maker-
pairing precision-loss fix)."""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

_spec = importlib.util.spec_from_file_location(
    "ordersmatched_economic_role",
    str(pathlib.Path(__file__).resolve().parents[1] / "scripts" /
        "ordersmatched_economic_role.py"))
om = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(om)


def test_canonical_int_plain():
    assert om.canonical_int("0") == 0
    assert om.canonical_int(0) == 0
    assert om.canonical_int("123") == 123
    assert om.canonical_int("  456  ") == 456


def test_canonical_int_float_string_zero():
    # "0.0" from a floated CSV must normalize to 0 (the USDC-side anchor)
    assert om.canonical_int("0.0") == 0
    assert om.canonical_int("123.0") == 123


def test_canonical_int_full_precision_big_int():
    big = "79792255824743933242473584104148817428360729889676194064736978155093841181512"
    assert om.canonical_int(big) == int(big)        # 78 digits preserved exactly


def test_canonical_int_blank_none():
    assert om.canonical_int("") is None
    assert om.canonical_int("nan") is None
    assert om.canonical_int(None) is None


def test_canonical_int_scientific_notation_raises():
    # scientific notation = precision already lost -> must fail loudly, not coerce
    with pytest.raises(om.DataExportPrecisionLoss):
        om.canonical_int("5.20896e+76")
    with pytest.raises(om.DataExportPrecisionLoss):
        om.canonical_int("2.58693E+76")


def test_classify_maker_confirmed_after_fix():
    # the real bug case, fixed: wallet is OF maker; USDC side (0) matches
    W = "0x" + "e3" * 20
    OTHER = "0x" + "08" * 20
    token = 332055829101
    om_row = {"takerordermaker": OTHER, "contract_address": "0xc5d5",
              "makerassetid": str(token), "takerassetid": "0",
              "evt_index": 1, "evt_tx_hash": "0xtx"}
    legs = [{"maker": W, "taker": OTHER, "maker_asset_id": token,
             "taker_asset_id": 0, "log_index": 5}]
    res = om.classify_trade(om_row, {W}, legs)
    assert res["economic_role"] == "ECONOMIC_MAKER_CONFIRMED"


def test_classify_taker_unaffected_by_fix():
    # taker side matches on address, never touched by asset-id normalization
    W = "0x" + "e3" * 20
    om_row = {"takerordermaker": W, "contract_address": "0xc5d5",
              "makerassetid": "111", "takerassetid": "0"}
    res = om.classify_trade(om_row, {W}, None)
    assert res["economic_role"] == "ECONOMIC_TAKER_CONFIRMED"


def test_classify_propagates_precision_loss():
    # if the CSV STILL has scientific notation, classify must raise (caller
    # surfaces DATA_EXPORT_PRECISION_LOSS) rather than silently miss the maker
    W = "0x" + "e3" * 20
    OTHER = "0x" + "08" * 20
    om_row = {"takerordermaker": OTHER, "contract_address": "0xc5d5",
              "makerassetid": "5.20896e+76", "takerassetid": "9.9e+75"}
    legs = [{"maker": W, "taker": OTHER, "maker_asset_id": 123,
             "taker_asset_id": 456, "log_index": 5}]
    with pytest.raises(om.DataExportPrecisionLoss):
        om.classify_trade(om_row, {W}, legs)
