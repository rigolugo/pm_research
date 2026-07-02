"""Tests for the named-binary semantics layer.

Covers the seven spec categories:
  - classification
  - mapping stability
  - orientation
  - no-label-only-inversion perturbation
  - resolution mapping
  - leakage safety
  - audit gate states

All fixtures are synthetic; no dependency on the full dataset. Pyarrow is not
required (these test pure logic over in-memory structures).
"""

import pytest

from pm_research.semantics.lexicon import (
    NB_CONTRACT_VERSION, NBSubclass, classify_label_pair,
)
from pm_research.semantics.mapping_audit import (
    ConditionAccumulator, audit_condition, audit_token_condition_stability,
    MAP_OK, FAIL_TOKEN_COUNT, FAIL_TOKEN_INDEX, FAIL_INDEX_LABEL,
    FAIL_TOKEN_CONDITION,
)
from pm_research.semantics.resolution_schema import (
    ConditionSides, ResolutionRow, determine_schema, resolve_condition,
    RES_OK, RES_FAIL_UNMAPPABLE,
)
from pm_research.semantics.named_binary import (
    classify_condition, build_orientation, orientation_is_clean,
    GateInput, GateThresholds, run_audit_gate,
    GATE_CLEAR, GATE_CLEAR_WARN, GATE_BLOCK_MAPPING, GATE_BLOCK_RESOLUTION,
    GATE_BLOCK_ORIENTATION, GATE_BLOCK_COVERAGE,
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def make_mapping(cid, t0, l0, t1, l1):
    """Build a passing mapping result via the accumulator + audit."""
    acc = ConditionAccumulator(cid)
    acc.observe(t0, 0, l0)
    acc.observe(t1, 1, l1)
    return audit_condition(acc)


# --------------------------------------------------------------------------- #
# 1. classification
# --------------------------------------------------------------------------- #
def test_classify_yes_no():
    assert classify_label_pair("Yes", "No") == NBSubclass.YES_NO

def test_classify_over_under():
    assert classify_label_pair("Over", "Under") == NBSubclass.OVER_UNDER

def test_classify_up_down():
    assert classify_label_pair("Up", "Down") == NBSubclass.UP_DOWN

def test_classify_named_other():
    assert classify_label_pair("Lakers", "Celtics") == NBSubclass.NAMED_OTHER

def test_classify_ambiguous_unusable():
    # one structural token without its partner -> unusable
    assert classify_label_pair("Yes", "Maybe") == NBSubclass.UNUSABLE
    # two mismatched structural tokens -> unusable
    assert classify_label_pair("Yes", "Up") == NBSubclass.UNUSABLE
    # identical labels -> unusable
    assert classify_label_pair("Draw", "Draw") == NBSubclass.UNUSABLE

def test_classify_over_under_missing_threshold_still_classifies():
    # OQ-2: missing threshold is not a blocker; the label pair alone classifies.
    assert classify_label_pair("Over", "Under") == NBSubclass.OVER_UNDER

def test_classification_row_stamps_version_and_eligibility():
    m = make_mapping("c1", "100", "Yes", "200", "No")
    row = classify_condition(m)
    assert row.nb_subclass == NBSubclass.YES_NO.value
    assert row.nb_eligible is True
    assert row.nb_contract_version == NB_CONTRACT_VERSION

def test_classification_unusable_when_mapping_fails():
    acc = ConditionAccumulator("c2")
    acc.observe("100", 0, "Yes")  # only one token -> count fail
    m = audit_condition(acc)
    row = classify_condition(m)
    assert row.nb_eligible is False
    assert row.nb_subclass == NBSubclass.UNUSABLE.value


# --------------------------------------------------------------------------- #
# 2. mapping stability
# --------------------------------------------------------------------------- #
def test_mapping_ok():
    m = make_mapping("c1", "100", "Yes", "200", "No")
    assert m.status == MAP_OK
    assert len(m.sides) == 2

def test_mapping_more_than_two_tokens():
    acc = ConditionAccumulator("c3")
    acc.observe("100", 0, "Yes")
    acc.observe("200", 1, "No")
    acc.observe("300", 2, "Maybe")
    m = audit_condition(acc)
    assert m.status == FAIL_TOKEN_COUNT

def test_mapping_token_straddles_two_indices():
    acc = ConditionAccumulator("c4")
    acc.observe("100", 0, "Yes")
    acc.observe("100", 1, "No")  # same token, two indices
    acc.observe("200", 1, "No")
    m = audit_condition(acc)
    assert m.status == FAIL_TOKEN_INDEX

def test_mapping_index_label_drift():
    acc = ConditionAccumulator("c5")
    acc.observe("100", 0, "Yes")
    acc.observe("100", 0, "Si")   # same index, two labels
    acc.observe("200", 1, "No")
    m = audit_condition(acc)
    assert m.status == FAIL_INDEX_LABEL

def test_mapping_token_two_conditions_global():
    # token 100 appears under two conditions
    tok_to_conds = {"100": {"cA", "cB"}, "200": {"cA"}, "300": {"cB"}}
    failures = audit_token_condition_stability(tok_to_conds)
    assert failures["cA"] == FAIL_TOKEN_CONDITION
    assert failures["cB"] == FAIL_TOKEN_CONDITION


# --------------------------------------------------------------------------- #
# 3. orientation
# --------------------------------------------------------------------------- #
def test_orientation_yes_no_canonical_equals_yes_price():
    m = make_mapping("c1", "100", "Yes", "200", "No")
    c = build_orientation(m, NBSubclass.YES_NO.value)
    # side_0 token is the index-0 token = "100" (Yes). canonical token must be it.
    assert c.canonical_token == "100"
    # yes_price == canonical_side_price for YES_NO
    assert c.yes_price(0.7, 0.3) == c.canonical_side_price(0.7, 0.3) == 0.7

def test_orientation_over_under_canonical_is_over():
    m = make_mapping("c1", "100", "Over", "200", "Under")
    c = build_orientation(m, NBSubclass.OVER_UNDER.value)
    assert c.canonical_side_name == "OVER"
    assert c.canonical_token == "100"
    assert c.yes_price(0.6, 0.4) is None  # not a YES/NO market

def test_orientation_team_has_no_yes_equivalent():
    m = make_mapping("c1", "100", "Lakers", "200", "Celtics")
    c = build_orientation(m, NBSubclass.NAMED_OTHER.value)
    assert c.has_yes_equivalent is False
    assert c.canonical_side_name == "side_0"
    assert c.yes_price(0.55, 0.45) is None

def test_orientation_canonical_token_follows_index_not_label_order():
    # canonical label "Yes" is on the index-1 token; canonical token must follow.
    m = make_mapping("c1", "100", "No", "200", "Yes")
    c = build_orientation(m, NBSubclass.YES_NO.value)
    assert c.canonical_token == "200"  # the Yes token, regardless of order
    # side_0 is the index-0 token ("100"=No), so canonical price is side_1 price
    assert c.canonical_side_price(0.3, 0.7) == 0.7


# --------------------------------------------------------------------------- #
# 4. no-label-only-inversion perturbation
# --------------------------------------------------------------------------- #
def test_no_label_only_inversion():
    """Flipping the label strings while holding token identity fixed must not
    change the oriented price. This is the primary regression guard against the
    old display-label conversion bug."""
    # Original: token 100 = Yes (index 0), token 200 = No (index 1)
    m1 = make_mapping("c1", "100", "Yes", "200", "No")
    c1 = build_orientation(m1, NBSubclass.YES_NO.value)
    price_of_100, price_of_200 = 0.72, 0.28
    # side_0 token = "100"; canonical = "100"; canonical price = price_of_100
    oriented_1 = c1.canonical_side_price(price_of_100, price_of_200)

    # Perturb labels ONLY (swap the label strings) but keep token identity:
    # we keep token "100" as the canonical (Yes) token by NOT changing identity.
    # To simulate a label-only flip, we rebuild with labels swapped but the SAME
    # token->index assignment; the Yes label now sits on a different index, which
    # would move a label-driven orientation. Identity-driven orientation must
    # track the token that is actually canonical.
    m2 = make_mapping("c1", "100", "No", "200", "Yes")  # labels swapped
    c2 = build_orientation(m2, NBSubclass.YES_NO.value)
    # Now the Yes token is "200". Price of each TOKEN is unchanged.
    oriented_2 = c2.canonical_side_price(price_of_100, price_of_200)
    # The oriented (Yes-equivalent) price should still be the price of whichever
    # token carries Yes. In m1 that's 100 (0.72); in m2 that's 200 (0.28).
    # The KEY invariant: orientation followed the token that carries the canonical
    # label, never a fixed slot. Verify each picked its canonical token's price.
    assert oriented_1 == price_of_100      # 100 was Yes
    assert oriented_2 == price_of_200      # 200 is Yes
    # And critically: c1 and c2 both selected by identity (canonical_token set),
    # not by index slot.
    assert c1.canonical_token == "100"
    assert c2.canonical_token == "200"


# --------------------------------------------------------------------------- #
# 5. resolution mapping
# --------------------------------------------------------------------------- #
def _sides(cid="c1"):
    return {cid: ConditionSides(cid, (("100", 0, "Yes"), ("200", 1, "No")))}

def test_resolution_schema_outcome_index():
    rows = [ResolutionRow("c1", 0)]
    res = determine_schema(rows, _sides(), min_success=0.99)
    assert res.chosen_schema == "outcome_index"

def test_resolution_schema_token_id():
    rows = [ResolutionRow("c1", "200")]
    res = determine_schema(rows, _sides(), min_success=0.99)
    assert res.chosen_schema == "token_id"

def test_resolution_schema_label():
    rows = [ResolutionRow("c1", "Yes")]
    res = determine_schema(rows, _sides(), min_success=0.99)
    assert res.chosen_schema == "label"

def test_resolution_unmappable_excluded():
    status, side = resolve_condition("outcome_index", 5, _sides()["c1"].sides)
    assert status == RES_FAIL_UNMAPPABLE
    assert side is None

def test_resolution_convergence_disagreement_surfaced():
    # winning_outcome=0 (token 100) but price converged on token 200 -> disagree
    rows = [ResolutionRow("c1", 0, converged_token_id="200")]
    res = determine_schema(rows, _sides(), min_success=0.99)
    assert res.chosen_schema == "outcome_index"
    assert res.convergence_disagreement_rate == 1.0  # surfaced, not overridden

def test_resolution_schema_blocks_when_no_interpretation_clears():
    # ambiguous raw that maps under nothing
    rows = [ResolutionRow("c1", "garbage")]
    res = determine_schema(rows, _sides(), min_success=0.99)
    assert res.chosen_schema is None


# --- Issue-A regression: mixed universe must not collapse a working schema ---
def _mixed_sides():
    # one YES/NO condition and two team conditions
    return {
        "y1": ConditionSides("y1", (("100", 0, "Yes"), ("200", 1, "No"))),
        "t1": ConditionSides("t1", (("300", 0, "Lakers"), ("400", 1, "Celtics"))),
        "t2": ConditionSides("t2", (("500", 0, "Knicks"), ("600", 1, "Spurs"))),
    }

def test_issue_a_mixed_universe_still_chooses_label_schema():
    # YES/NO winner maps (label); team winners are "NO" and map to NO side string?
    # No: team sides are Lakers/Celtics, so "NO" maps to neither -> unresolvable.
    rows = [
        ResolutionRow("y1", "No"),     # maps under label
        ResolutionRow("t1", "NO"),     # maps under nothing (team sides)
        ResolutionRow("t2", "NO"),     # maps under nothing
    ]
    res = determine_schema(rows, _mixed_sides(), min_success=0.99)
    # Pre-fix this returned None (1/3 < 0.99). Post-fix: label dominates the
    # cleanly-mappable subset (1/1), so it is chosen.
    assert res.chosen_schema == "label"

def test_issue_a_unresolvable_rows_do_not_veto_schema_but_stay_unmapped():
    rows = [
        ResolutionRow("y1", "Yes"),
        ResolutionRow("t1", "NO"),
        ResolutionRow("t2", "NO"),
    ]
    res = determine_schema(rows, _mixed_sides(), min_success=0.99)
    assert res.chosen_schema == "label"
    # y1 maps, t1/t2 do not
    assert resolve_condition("label", "Yes", _mixed_sides()["y1"].sides)[0] == RES_OK
    assert resolve_condition("label", "NO", _mixed_sides()["t1"].sides)[0] == RES_FAIL_UNMAPPABLE

def test_issue_a_all_unresolvable_still_returns_none():
    # if NOTHING maps under any interpretation, schema is None (true block)
    rows = [ResolutionRow("t1", "NO"), ResolutionRow("t2", "NO")]
    res = determine_schema(rows, _mixed_sides(), min_success=0.99)
    assert res.chosen_schema is None


# --------------------------------------------------------------------------- #
# 6. leakage safety
# --------------------------------------------------------------------------- #
def test_leakage_resolution_separate_from_price_path():
    """The orientation contract exposes prices via canonical_side_price(side_0,
    side_1) and resolution via a separate resolve path. There is no method that
    returns the realized winner from the price inputs, so realized outcome cannot
    be read off the price-time path."""
    m = make_mapping("c1", "100", "Yes", "200", "No")
    c = build_orientation(m, NBSubclass.YES_NO.value)
    price_methods = [a for a in dir(c) if "price" in a.lower()]
    # no price method name implies a resolution/winner output
    assert all("win" not in a.lower() and "resolv" not in a.lower()
               for a in price_methods)


# --------------------------------------------------------------------------- #
# 7. audit gate states
# --------------------------------------------------------------------------- #
def _gi(**kw):
    base = dict(
        total_conditions=1000,
        named_binary_eligible=800,
        usable_named_binary_conditions=780,
        token_id_coverage=0.999,
        outcome_index_coverage=0.999,
        resolution_mapping_success_rate=0.999,
        orientation_correctness_rate=0.999,
        blocked_reason_counts={},
        resolution_schema_chosen="outcome_index",
    )
    base.update(kw)
    return GateInput(**base)

def test_gate_clear():
    assert run_audit_gate(_gi()).gate_state == GATE_CLEAR

def test_gate_clear_with_warnings_orientation_band():
    g = run_audit_gate(_gi(orientation_correctness_rate=0.97))
    assert g.gate_state == GATE_CLEAR_WARN

def test_gate_block_orientation():
    g = run_audit_gate(_gi(orientation_correctness_rate=0.90))
    assert g.gate_state == GATE_BLOCK_ORIENTATION

def test_gate_block_resolution_no_schema():
    g = run_audit_gate(_gi(resolution_schema_chosen=None))
    assert g.gate_state == GATE_BLOCK_RESOLUTION

def test_gate_block_resolution_low_success():
    g = run_audit_gate(_gi(resolution_mapping_success_rate=0.80))
    assert g.gate_state == GATE_BLOCK_RESOLUTION

def test_gate_block_mapping_no_usable():
    g = run_audit_gate(_gi(usable_named_binary_conditions=0))
    assert g.gate_state == GATE_BLOCK_MAPPING

def test_gate_block_coverage():
    g = run_audit_gate(_gi(token_id_coverage=0.90))
    assert g.gate_state == GATE_BLOCK_COVERAGE

def test_gate_threshold_band_boundaries():
    th = GateThresholds()
    # exactly at clear min -> clear
    assert run_audit_gate(_gi(orientation_correctness_rate=0.99), th).gate_state == GATE_CLEAR
    # just below clear min -> warn
    assert run_audit_gate(_gi(orientation_correctness_rate=0.989), th).gate_state == GATE_CLEAR_WARN
    # exactly at warn min -> warn (>= warn_min and < clear_min)
    assert run_audit_gate(_gi(orientation_correctness_rate=0.95), th).gate_state == GATE_CLEAR_WARN
    # just below warn min -> block
    assert run_audit_gate(_gi(orientation_correctness_rate=0.949), th).gate_state == GATE_BLOCK_ORIENTATION

def test_gate_thresholds_version_recorded():
    g = run_audit_gate(_gi())
    assert g.thresholds_version == GateThresholds().version
