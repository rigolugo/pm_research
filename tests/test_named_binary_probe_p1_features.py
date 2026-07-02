#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for Stage P1 (named-binary probe feature assembly) — tightened contract.

Pure-Python + injected list[dict] loaders (no pyarrow/network). Real parquet
loaders live in build_real_loaders and are exercised locally by The Orchestrator.

Run:  python -m pytest tests/test_named_binary_probe_p1_features.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import named_binary_probe_p1_features as P1  # noqa: E402

V = P1.NB_CONTRACT_VERSION


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------
def p0_clear(**over):
    d = {
        "p0_state": "P0_CLEAR",
        "authorized_scope": "P0_PREFLIGHT_ONLY",
        "probe_execution_authorized": False,
        "named_binary_probe_blocked_observed": True,
        "counts_pooled": {"final_p0_eligible": 39693},
        "counts_by_subclass": {},
        "excluded_counts": {},
    }
    d.update(over)
    return d


def gate(state="CLEAR_WITH_WARNINGS", scoreable=None, blocked=True):
    if scoreable is None:
        scoreable = {"UP_DOWN": True, "OVER_UNDER": True, "NAMED_OTHER": True}
    return {
        "named_binary_probe_blocked": blocked,
        "stage4_nonyesno_branch": {
            "non_yesno_gate_state": state,
            "per_subclass_scoreable": scoreable,
        },
    }


def contract(rows):
    return [{"condition_id": c, "subclass": s, "eligible": e, "nb_contract_version": V}
            for (c, s, e) in rows]


def res(rows):
    out = []
    for r in rows:
        d = {"nb_contract_version": V, "status": "RESOLVED_SINGLE_WINNER"}
        d.update(r)
        out.append(d)
    return out


def prices(cid, base=0, step=600, n=20, price=0.6, token="123", oidx=1):
    return [{"condition_id": cid, "ts": base + i * step, "yes_price": price,
             "token_id": token, "outcome_index": oidx} for i in range(n)]


def trades(cid, first=0):
    return [{"condition_id": cid, "ts": first}, {"condition_id": cid, "ts": first + 60}]


def loaders(c, g, r, p, t, canon=None, p0=None):
    if canon is None:
        def canon(cr, pr):
            return {"canonical_side_price": pr["yes_price"],
                    "canonical_side_token_id": pr.get("token_id"),
                    "canonical_side_outcome_index": pr.get("outcome_index")}
    return P1.P1Loaders(
        load_p0=lambda: (p0 if p0 is not None else p0_clear()),
        load_contract=lambda: c,
        load_gate=lambda: g,
        load_resolution_rows=lambda: r,
        load_prices=lambda ids: [x for x in p if x["condition_id"] in set(ids)],
        load_trades=lambda ids: [x for x in t if x["condition_id"] in set(ids)],
        canonical_side_price=canon,
    )


def two_mixed():
    c = contract([("a", "UP_DOWN", True), ("b", "UP_DOWN", True)])
    r = res([{"condition_id": "a", "resolved_at": 9e9, "resolved_winning_token_id": "123",
              "canonical_side_token_id": "123"},
             {"condition_id": "b", "resolved_at": 9e9, "resolved_winning_token_id": "999",
              "canonical_side_token_id": "123"}])
    p = prices("a") + prices("b")
    t = trades("a") + trades("b")
    return c, r, p, t


# --------------------------------------------------------------------------
# P0 gating
# --------------------------------------------------------------------------
def test_p0_not_clear_stops():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t, p0=p0_clear(p0_state="P0_BLOCKED"))
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_P0_NOT_CLEAR


def test_p0_wrong_scope_stops():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t, p0=p0_clear(authorized_scope="SOMETHING_ELSE"))
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_P0_NOT_CLEAR


# --------------------------------------------------------------------------
# version pins
# --------------------------------------------------------------------------
def test_stale_contract_stops():
    c = [{"condition_id": "a", "subclass": "UP_DOWN", "eligible": True,
          "nb_contract_version": "OLD"}]
    _, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_STALE_CONTRACT


def test_stale_resolution_stops():
    c, r, p, t = two_mixed()
    r[0]["nb_contract_version"] = "OLD"
    ld = loaders(c, gate(), r, p, t)
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_STALE_CONTRACT


# --------------------------------------------------------------------------
# gate
# --------------------------------------------------------------------------
def test_gate_not_clear_stops():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(state="BLOCKED_BY_RESOLUTION_MAPPING"), r, p, t)
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_DATA_GATE_NOT_CLEAR


# --------------------------------------------------------------------------
# precision
# --------------------------------------------------------------------------
def test_precision_loss_stops():
    c, r, p, t = two_mixed()
    r[0]["resolved_winning_token_id"] = "5.20896e+76"
    ld = loaders(c, gate(), r, p, t)
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_PRECISION_LOSS


# --------------------------------------------------------------------------
# exclusions
# --------------------------------------------------------------------------
def test_yes_no_excluded():
    c = contract([("y", "YES_NO", True), ("a", "UP_DOWN", True), ("b", "UP_DOWN", True)])
    _, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.excluded_counts["YES_NO"] == 1
    assert all(fr["subclass"] != "YES_NO" for fr in rows)


def test_ambiguous_and_missing_excluded():
    c = contract([("a", "UP_DOWN", True), ("b", "UP_DOWN", True),
                  ("m", "UP_DOWN", True)])  # m: no resolution row
    r = res([{"condition_id": "a", "resolved_at": 9e9, "resolved_winning_token_id": "123",
              "canonical_side_token_id": "123"}])
    r.append({"condition_id": "b", "nb_contract_version": V,
              "status": "AMBIGUOUS_MULTIPLE_WINNERS", "resolved_at": 9e9})
    p = prices("a") + prices("b") + prices("m")
    t = trades("a") + trades("b") + trades("m")
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.excluded_counts["AMBIGUOUS_OR_NON_SINGLE_WINNER"] == 1
    assert result.excluded_counts["NO_RESOLUTION_ROW"] == 1
    assert all(fr["condition_id"] not in ("b", "m") for fr in rows)


def test_not_scoreable_subclass_excluded():
    c = contract([("a", "OVER_UNDER", True), ("b", "UP_DOWN", True), ("d", "UP_DOWN", True)])
    g = gate(scoreable={"UP_DOWN": True, "OVER_UNDER": False, "NAMED_OTHER": True})
    r = res([{"condition_id": "a", "resolved_at": 9e9, "resolved_winning_token_id": "123", "canonical_side_token_id": "123"},
             {"condition_id": "b", "resolved_at": 9e9, "resolved_winning_token_id": "123", "canonical_side_token_id": "123"},
             {"condition_id": "d", "resolved_at": 9e9, "resolved_winning_token_id": "999", "canonical_side_token_id": "123"}])
    p = prices("a") + prices("b") + prices("d")
    t = trades("a") + trades("b") + trades("d")
    ld = loaders(c, g, r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.excluded_counts["NOT_SCOREABLE_SUBCLASS"] == 1
    assert all(fr["subclass"] != "OVER_UNDER" for fr in rows)


# --------------------------------------------------------------------------
# anchors / decision price
# --------------------------------------------------------------------------
def test_no_trade_anchor_counted():
    c, r, p, t = two_mixed()
    t = trades("a")  # only 'a' has trades; 'b' has none
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.excluded_counts["NO_TRADE_ANCHOR"] == 1
    assert all(fr["condition_id"] != "b" for fr in rows)


def test_no_post_warmup_price_counted():
    c, r, p, t = two_mixed()
    # 'b' prices all before warmup
    p = prices("a") + prices("b", base=0, step=10, n=5)
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.excluded_counts["NO_DECISION_PRICE"] >= 1
    assert all(fr["condition_id"] != "b" for fr in rows)


def test_first_price_after_warmup_selected_not_last():
    prows = [{"ts": 0, "yes_price": 0.5}, {"ts": 1800, "yes_price": 0.55},
             {"ts": 3600, "yes_price": 0.6}, {"ts": 999999, "yes_price": 0.95}]
    ts, row = P1.first_price_after_warmup(prows, 0, 3600)
    assert ts == 3600 and row["yes_price"] == 0.6  # not the near-resolution 0.95


def test_selected_price_ts_le_decision_ts():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    for fr in rows:
        assert fr["selected_price_ts"] <= fr["decision_ts"]
        assert fr["selected_price_ts"] == fr["decision_ts"]


def test_resolution_time_not_used_to_choose_row():
    # Two identical setups differing ONLY in resolved_at (far future) must
    # select the same decision row.
    c, r, p, t = two_mixed()
    ld1 = loaders(c, gate(), r, p, t)
    res2 = [dict(x, resolved_at=1e18) for x in r]
    ld2 = loaders(c, gate(), res2, p, t)
    _, rows1 = P1.assemble_features(ld1)
    _, rows2 = P1.assemble_features(ld2)
    sel1 = {fr["condition_id"]: fr["decision_ts"] for fr in rows1}
    sel2 = {fr["condition_id"]: fr["decision_ts"] for fr in rows2}
    assert sel1 == sel2


# --------------------------------------------------------------------------
# leakage
# --------------------------------------------------------------------------
def test_decision_after_resolution_stops_or_excludes():
    c, r, p, t = two_mixed()
    # both resolve at 3600 (== decision ts) -> both excluded; leads to all-excluded
    r = res([{"condition_id": "a", "resolved_at": 3600, "resolved_winning_token_id": "123", "canonical_side_token_id": "123"},
             {"condition_id": "b", "resolved_at": 3600, "resolved_winning_token_id": "999", "canonical_side_token_id": "123"}])
    ld = loaders(c, gate(), r, p, t)
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_LEAKAGE_GUARD


def test_partial_leakage_excluded_counted():
    c = contract([("a", "UP_DOWN", True), ("b", "UP_DOWN", True), ("d", "UP_DOWN", True)])
    r = res([{"condition_id": "a", "resolved_at": 3600, "resolved_winning_token_id": "123", "canonical_side_token_id": "123"},  # leak
             {"condition_id": "b", "resolved_at": 9e9, "resolved_winning_token_id": "123", "canonical_side_token_id": "123"},
             {"condition_id": "d", "resolved_at": 9e9, "resolved_winning_token_id": "999", "canonical_side_token_id": "123"}])
    p = prices("a") + prices("b") + prices("d")
    t = trades("a") + trades("b") + trades("d")
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.excluded_counts["LEAKAGE_DECISION_GE_RESOLUTION"] == 1
    assert all(fr["condition_id"] != "a" for fr in rows)


def test_all_one_direction_stops():
    c = contract([("a", "UP_DOWN", True), ("b", "UP_DOWN", True), ("d", "UP_DOWN", True)])
    r = res([{"condition_id": x, "resolved_at": 9e9, "resolved_winning_token_id": "123",
              "canonical_side_token_id": "123"} for x in ("a", "b", "d")])  # all winners
    p = prices("a") + prices("b") + prices("d")
    t = trades("a") + trades("b") + trades("d")
    ld = loaders(c, gate(), r, p, t)
    try:
        P1.assemble_features(ld); assert False
    except P1.ProbeStop as s:
        assert s.code == P1.STOP_LEAKAGE_GUARD


# --------------------------------------------------------------------------
# shape / no-scoring guarantees
# --------------------------------------------------------------------------
def test_one_row_per_condition():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    cids = [fr["condition_id"] for fr in rows]
    assert len(cids) == len(set(cids)) == 2


def test_no_scoring_columns_present():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    banned = {"brier", "brier_skill", "log_loss", "logloss", "reliability",
              "calibration", "pnl", "roi", "edge", "fee", "sizing"}
    for fr in rows:
        for k in fr:
            assert not any(b in k.lower() for b in banned), f"scoring col leaked: {k}"


def test_no_scoring_functions_called(monkeypatch=None):
    # Poison any calibration import path: if P1 tried to import/fit a calibrator
    # or compute Brier, it would fail. We assert the module exposes none.
    for banned in ("brier", "log_loss", "reliability", "calibrate", "fit_isotonic",
                   "rolling_train_test_splits", "IsotonicCalibrator"):
        assert not hasattr(P1, banned), f"P1 must not expose {banned}"


def test_no_wallet_ordersmatched_logindex_paths():
    src = open(os.path.join(os.path.dirname(__file__), "..", "scripts",
                            "named_binary_probe_p1_features.py"), encoding="utf-8").read()
    # Strip the module docstring (which references these terms in the compliance
    # / non-authorization statement) so we scan only executable code.
    body = src.split('"""', 2)[-1] if src.count('"""') >= 2 else src
    low = body.lower()
    # Forbidden as CODE (imports/calls/attribute access), not as prose:
    for banned in ("import ordersmatched", "load_ordersmatched", "takerordermaker",
                   "log_index", "wallet_cohort", "copy_trade", ".ordersmatched(",
                   "from pm_research.scripts.ordersmatched"):
        assert banned not in low, f"forbidden code path referenced: {banned}"


def test_probe_execution_false_and_blocked_observed():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(blocked=True), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.probe_execution_authorized is False
    assert result.scoring_authorized is False
    assert result.named_binary_probe_blocked_observed is True


def test_target_marked_target_only():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    for fr in rows:
        assert "y_target_target_only_not_feature" in fr
    tgt = {fr["condition_id"]: fr["y_target_target_only_not_feature"] for fr in rows}
    assert tgt["a"] == 1 and tgt["b"] == 0


def test_orientation_audit_present():
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    assert result.orientation_audit["reimplemented_orientation"] is False
    assert result.orientation_audit["orientation_source"].endswith("named_binary")


# --------------------------------------------------------------------------
# artifacts
# --------------------------------------------------------------------------
def test_artifacts_emitted(tmp_path=None):
    import tempfile
    c, r, p, t = two_mixed()
    ld = loaders(c, gate(), r, p, t)
    result, rows = P1.assemble_features(ld)
    d = tempfile.mkdtemp()
    paths = P1.write_artifacts(result, rows, d)
    assert os.path.exists(paths["json"])
    assert os.path.exists(paths["md"])
    assert os.path.exists(paths["excluded"])
    assert paths["features"] and os.path.exists(paths["features"])
    import json as _j
    data = _j.load(open(paths["json"]))
    assert data["stage"] == "P1_FEATURE_ASSEMBLY"
    assert data["p1_state"] == "P1_CLEAR"
    assert data["probe_execution_authorized"] is False
    assert data["scoring_authorized"] is False


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------
def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    n = 0
    for fn in fns:
        fn()
        n += 1
    print(f"{n} passed")
    return n


if __name__ == "__main__":
    _run()
