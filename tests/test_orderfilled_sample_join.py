"""Offline fixture tests for the Rank 2 OrderFilled sample-join probe.

NO RPC. NO network. All logs are synthetic fixtures. Tests decode, join,
role assignment, ambiguity, wallet-not-in-fill, and gate-state selection.
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

_spec = importlib.util.spec_from_file_location(
    "orderfilled_sample_join",
    str(pathlib.Path(__file__).resolve().parents[1] / "scripts" / "orderfilled_sample_join.py"))
ofj = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ofj)

# inject a known topic0 so decode works offline without a keccak lib
_TOPIC0 = "0x" + "aa" * 32
ofj.KNOWN_TOPICS[_TOPIC0] = ofj.ORDERFILLED_SIGNATURE

_W = "0x" + "cc" * 20         # our wallet
_M = "0x" + "dd" * 20         # counterparty
_TOK = 12345                  # CLOB token id


def _pad_addr(a):
    return "0x" + "00" * 12 + a[2:]


def _word(x):
    return format(x, "064x")


def mk_log(contract, log_index, maker, taker, maker_asset, taker_asset,
           maker_amt, taker_amt, fee=0):
    # V2-source indexed-topic order: [topic0, orderHash, maker, taker]
    data = "0x" + _word(maker_asset) + _word(taker_asset) + _word(maker_amt) \
        + _word(taker_amt) + _word(fee)
    return {"address": contract, "logIndex": hex(log_index),
            "topics": [_TOPIC0, "0x" + "11" * 32, _pad_addr(maker),
                       _pad_addr(taker)], "data": data}


def _fill(maker=_M, taker=_W, maker_asset=_TOK, taker_asset=999,
          maker_amt=100_000000, taker_amt=70_000000, log_index=5,
          contract="0x4bfb41d5b3570defd03c39a9a4d8de6bd8b8982e"):
    return mk_log(contract, log_index, maker, taker, maker_asset, taker_asset,
                  maker_amt, taker_amt)


def _trade(token_id=_TOK, wallet=_W, price=0.70, size=70.0):
    return {"token_id": str(token_id), "wallet": wallet, "price": price,
            "size_usdc": size, "trade_id": "t1", "tx_hash": "0x" + "ab" * 32}


# 1. JSON-RPC receipt parsing fixture ----------------------------------------
def test_receipt_logs_extracted():
    # a receipt dict shape -> logs list is what the script reads
    receipt = {"logs": [_fill(), _fill(log_index=6, maker_asset=999,
                                        taker_asset=_TOK)]}
    logs = receipt.get("logs", [])
    assert len(logs) == 2
    assert all("topics" in lg for lg in logs)


# 2. OrderFilled ABI decode fixture ------------------------------------------
def test_decode_orderfilled_fields():
    d = ofj.decode_orderfilled(_fill())
    assert d is not None
    assert d["maker"] == _M and d["taker"] == _W
    assert d["maker_asset_id"] == _TOK
    assert d["log_index"] == 5
    assert d["signature"] == ofj.ORDERFILLED_SIGNATURE


def test_decode_rejects_unknown_topic():
    bad = _fill()
    bad["topics"][0] = "0x" + "ff" * 32        # unknown topic0
    assert ofj.decode_orderfilled(bad) is None


# 3. tx_hash join + 4. token_id matching -------------------------------------
def test_join_resolved_taker_role():
    d = ofj.decode_orderfilled(_fill())          # wallet W is taker
    res = ofj.join_trade_to_fills(_trade(), [d])
    assert res["match_status"] == "resolved"
    assert res["role"] == "taker"
    assert res["log_index"] == 5


def test_join_resolved_maker_role():
    # flip: our wallet is the MAKER and holds the token on the maker side
    d = ofj.decode_orderfilled(_fill(maker=_W, taker=_M))
    res = ofj.join_trade_to_fills(_trade(), [d])
    assert res["match_status"] == "resolved"
    assert res["role"] == "maker"


def test_token_id_mismatch_no_fill():
    d = ofj.decode_orderfilled(_fill())
    res = ofj.join_trade_to_fills(_trade(token_id=99999), [d])  # token not in fill
    assert res["match_status"] == "NO_FILL"


# 5. maker/taker role assignment edge: wallet not in fill --------------------
def test_wallet_not_in_fill():
    d = ofj.decode_orderfilled(_fill(maker=_M, taker="0x" + "ee" * 20))
    res = ofj.join_trade_to_fills(_trade(), [d])   # our wallet W is neither
    assert res["match_status"] == "WALLET_NOT_IN_FILL"


# 6. ambiguous multi-fill handling -------------------------------------------
def test_ambiguous_two_matching_fills():
    d = ofj.decode_orderfilled(_fill())
    res = ofj.join_trade_to_fills(_trade(), [d, d])
    assert res["match_status"] == "AMBIGUOUS"
    assert res["role"] is None                    # never guessed


def test_no_fill_empty():
    assert ofj.join_trade_to_fills(_trade(), [])["match_status"] == "NO_FILL"


# 7. price/size tolerance gating ---------------------------------------------
def test_price_tolerance_excludes_mismatch():
    # fill implies price 0.70; trade claims 0.40 -> should not match
    d = ofj.decode_orderfilled(_fill())
    res = ofj.join_trade_to_fills(_trade(price=0.40), [d])
    assert res["match_status"] == "NO_FILL"


# 8. gate state selection ----------------------------------------------------
def test_gate_clear():
    assert ofj.decide_gate({"undecoded_log_rate": 0.0, "join_success_rate": 0.9,
                            "maker_taker_resolvable_rate": 0.8,
                            "ambiguity_rate": 0.1, "rpc_limited": False}) \
        == "CLEAR_FOR_ORDERFILLED_INDEXER"


def test_gate_low_join():
    assert ofj.decide_gate({"undecoded_log_rate": 0.0, "join_success_rate": 0.5,
                            "maker_taker_resolvable_rate": 0.8,
                            "ambiguity_rate": 0.1, "rpc_limited": False}) \
        == "BLOCKED_BY_LOW_JOIN_RATE"


def test_gate_ambiguous_role():
    assert ofj.decide_gate({"undecoded_log_rate": 0.0, "join_success_rate": 0.9,
                            "maker_taker_resolvable_rate": 0.5,
                            "ambiguity_rate": 0.3, "rpc_limited": False}) \
        == "BLOCKED_BY_AMBIGUOUS_ROLE"


def test_gate_rpc_limited():
    assert ofj.decide_gate({"undecoded_log_rate": 0.0, "join_success_rate": 0.9,
                            "maker_taker_resolvable_rate": 0.8,
                            "ambiguity_rate": 0.1, "rpc_limited": True}) \
        == "BLOCKED_BY_RPC_LIMITS"


def test_gate_need_abi_discovery():
    assert ofj.decide_gate({"undecoded_log_rate": 0.7, "join_success_rate": 0.2,
                            "maker_taker_resolvable_rate": 0.0,
                            "ambiguity_rate": 0.0, "rpc_limited": False}) \
        == "NEED_ABI_OR_CONTRACT_DISCOVERY"


# 9. discovery: contract address + signature surfaced ------------------------
def test_decode_surfaces_contract_address():
    d = ofj.decode_orderfilled(_fill(contract="0xC5d563a36AE78145C45a50134d48a1215220f80A".lower()))
    assert d["contract_address"] == "0xc5d563a36ae78145c45a50134d48a1215220f80a"
    assert d["contract_address"] in ofj.KNOWN_EXCHANGES
