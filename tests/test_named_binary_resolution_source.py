"""Stage 2 tests for pm_research.semantics.resolution_source.

Covers every case the orchestrator enumerated: payout parsing + winner
derivation, scientific-notation rejection, condition_id normalization, slot->token
mapping (success + conflict), and resolution-independence of classification.
Pure logic; no CSV, no network, no gate, no probe.
"""

import pytest

from pm_research.semantics.resolution_source import (
    normalize_condition_id, parse_payout_vector, winner_from_payout,
    map_slot_to_token, resolve_one, reject_scientific_notation, safe_int_str,
    DataExportPrecisionLoss,
    RESOLVED_SINGLE_WINNER, AMBIGUOUS_ZERO_WINNER, AMBIGUOUS_MULTIPLE_WINNERS,
    MALFORMED_PAYOUT_VECTOR, CONDITION_ID_INVALID, SLOT_TOKEN_MAPPING_MISSING,
    TOKEN_INDEX_CONFLICT, PRECISION_LOSS, CONFLICT_STATUSES,
)


CID = "0x" + "a" * 64
SIDES = (("100", 0, "Lakers"), ("200", 1, "Celtics"))


# --- winner derivation from payout vectors ---------------------------------- #
def test_payout_0_1_resolves_slot_1():
    v = parse_payout_vector("[0 1]")
    r = winner_from_payout(v)
    assert r.status == RESOLVED_SINGLE_WINNER and r.winning_slot == 1

def test_payout_1_0_resolves_slot_0():
    v = parse_payout_vector("[1 0]")
    r = winner_from_payout(v)
    assert r.status == RESOLVED_SINGLE_WINNER and r.winning_slot == 0

def test_payout_0_0_conflicts_zero():
    r = winner_from_payout(parse_payout_vector("[0 0]"))
    assert r.status == AMBIGUOUS_ZERO_WINNER

def test_payout_1_1_conflicts_multiple():
    r = winner_from_payout(parse_payout_vector("[1 1]"))
    assert r.status == AMBIGUOUS_MULTIPLE_WINNERS

def test_three_slot_vector_conflicts_for_binary():
    r = winner_from_payout(parse_payout_vector("[0 1 0]"), expect_binary=True)
    assert r.status == MALFORMED_PAYOUT_VECTOR

def test_comma_variant_parses():
    assert parse_payout_vector("[1, 0]") == ["1", "0"]
    assert parse_payout_vector("0,1") == ["0", "1"]

def test_large_payout_value_not_via_float():
    # a big numerator must round-trip as a string, never float
    big = "1000000000000000000000000000000"
    v = parse_payout_vector(f"[{big} 0]")
    assert v == [big, "0"]
    assert winner_from_payout(v).winning_slot == 0


# --- scientific notation rejection ------------------------------------------ #
def test_scientific_notation_rejected_in_vector():
    with pytest.raises(DataExportPrecisionLoss):
        parse_payout_vector("[5.2e+76 0]")

def test_reject_scientific_notation_helper():
    with pytest.raises(DataExportPrecisionLoss):
        reject_scientific_notation("5.20896e+76", "payout")
    # plain integers and 0 pass
    reject_scientific_notation("0", "payout")
    reject_scientific_notation("123456789", "payout")

def test_resolve_one_maps_precision_loss_status():
    r = resolve_one(CID, "[5.2e+76 0]", SIDES)
    assert r.status == PRECISION_LOSS
    assert r.status in CONFLICT_STATUSES

def test_safe_int_str_normalizes_without_float():
    assert safe_int_str("007") == "7"
    assert safe_int_str("0") == "0"
    assert safe_int_str("00") == "0"


# --- condition_id normalization --------------------------------------------- #
def test_normalize_already_0x_lower():
    assert normalize_condition_id(CID) == CID

def test_normalize_uppercase_and_no_prefix():
    upper = "0x" + "A" * 64
    assert normalize_condition_id(upper) == CID
    noprefix = "a" * 64
    assert normalize_condition_id(noprefix) == CID

def test_normalize_whitespace():
    assert normalize_condition_id("  " + CID + "  ") == CID

def test_normalize_malformed_returns_none():
    assert normalize_condition_id("0x123") is None          # too short
    assert normalize_condition_id("0x" + "z" * 64) is None  # non-hex
    assert normalize_condition_id("") is None
    assert normalize_condition_id(None) is None

def test_resolve_one_condition_id_invalid_status():
    r = resolve_one("0xbad", "[0 1]", SIDES)
    assert r.status == CONDITION_ID_INVALID


# --- slot -> token mapping -------------------------------------------------- #
def test_slot_to_token_correct_mapping():
    r = map_slot_to_token(1, SIDES)
    assert r.status == RESOLVED_SINGLE_WINNER
    assert r.resolved_winning_token_id == "200"
    assert r.resolved_winning_outcome_index == 1
    assert r.resolved_winning_label == "Celtics"

def test_slot_to_token_slot0():
    r = map_slot_to_token(0, SIDES)
    assert (r.resolved_winning_token_id, r.resolved_winning_outcome_index,
            r.resolved_winning_label) == ("100", 0, "Lakers")

def test_slot_to_token_missing_index():
    # winning slot 1 but sides only define index 0
    r = map_slot_to_token(1, (("100", 0, "Solo"),))
    assert r.status == SLOT_TOKEN_MAPPING_MISSING

def test_slot_to_token_duplicate_index_conflict():
    bad_sides = (("100", 0, "A"), ("200", 0, "B"))  # both index 0
    r = map_slot_to_token(0, bad_sides)
    assert r.status == TOKEN_INDEX_CONFLICT

def test_slot_to_token_empty_token_conflict():
    r = map_slot_to_token(0, (("", 0, "A"), ("200", 1, "B")))
    assert r.status == TOKEN_INDEX_CONFLICT


# --- end to end ------------------------------------------------------------- #
def test_resolve_one_happy_path():
    r = resolve_one(CID, "[0 1]", SIDES)
    assert r.status == RESOLVED_SINGLE_WINNER
    assert r.resolved_winning_token_id == "200"
    assert r.resolved_winning_outcome_index == 1
    assert r.resolved_winning_label == "Celtics"

def test_resolve_one_ambiguous_excluded_not_silent():
    r = resolve_one(CID, "[1 1]", SIDES)
    assert r.status == AMBIGUOUS_MULTIPLE_WINNERS
    assert r.status in CONFLICT_STATUSES
    assert r.resolved_winning_token_id is None  # excluded, no winner emitted


# --- resolution-independence of classification ------------------------------ #
def test_classification_independent_of_resolution():
    """The classifier must not depend on resolution data. Verify the
    resolution_source module imports nothing from the classifier and the
    classifier imports nothing from resolution_source (no leakage path)."""
    import pm_research.semantics.resolution_source as rs
    import pm_research.semantics.named_binary as nb
    import inspect
    rs_src = inspect.getsource(rs)
    nb_src = inspect.getsource(nb)
    # classifier does not import resolution_source
    assert "resolution_source" not in nb_src
    # resolution_source does not import the classifier/lexicon classify path
    assert "from .named_binary" not in rs_src
    assert "classify_label_pair" not in rs_src
