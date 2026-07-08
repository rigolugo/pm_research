"""Pure-logic tests for the Option C C1A-F1 deterministic selector policy.

CODE / TEST ONLY. No network, no Dune, no run. Bare Python 3 (no pandas/Store).

Proves, against project_context/SPEC_price_source_option_c_c1a_followup.md and the
Orchestrator BLOCK patch:
  - density is computed from APPROVED local-trade fields only, never S1 CLOB point
    counts (BLOCK patch objective + reject conditions 16, 17, 18);
  - S1 observed_point_count_* / nearest-gap columns are ignored for identity and
    REFUSED as density inputs;
  - full-universe profiling is rejected/impossible under the interface (reject 14, 15);
  - winner/outcome/PnL/score fields are hard-rejected (reject 7, 8, 9);
  - deterministic, reproducible selection (reject 20);
  - caps + cap+1 preserved, never raised (spec 6.5 / reject 2);
  - 3-5 bound enforced (spec 6.5 / reject 10);
  - uniform prior-C1A holdout (spec 6.3 item 8 / reject 1);
  - no Dune/network/run path exists.
"""

import hashlib
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import price_source_option_c_c1a_f1_selector as sel  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _cid(n: int) -> str:
    return "0x" + f"{n:064x}"


def _identity(n, subclass="UP_DOWN", t0=None, t1=None, reach="both", **extra):
    r = {
        "condition_id": _cid(n),
        "subclass": subclass,
        "side_0_token": t0 if t0 is not None else str(1000 + n),
        "side_1_token": t1 if t1 is not None else str(2000 + n),
        "condition_reachability": reach,
        "level_b_class": "DECISION_PRICE_BOTH_SIDES",
    }
    r.update(extra)
    return r


def _density(rows, tx, wsec=3600):
    return {
        "local_trade_rows_in_window": str(rows),
        "local_distinct_tx_hash_count_in_window": str(tx),
        "window_seconds": str(wsec),
    }


def _balanced():
    """3 oriented subclasses, 2 candidates each, varied local-trade density."""
    ids = [1, 2, 3, 4, 5, 6]
    subs = ["UP_DOWN", "UP_DOWN", "OVER_UNDER", "OVER_UNDER", "NAMED_OTHER", "NAMED_OTHER"]
    rows = [2, 40, 3, 55, 4, 70]
    txs = [1, 20, 2, 25, 2, 30]
    identity = [_identity(i, s) for i, s in zip(ids, subs)]
    density = {_cid(i): _density(r, t) for i, r, t in zip(ids, rows, txs)}
    return identity, density


# ---------------------------------------------------------------------------
# Density must be approved local-trade fields only (BLOCK core)
# ---------------------------------------------------------------------------
def test_selected_carry_local_trade_density_not_clob_points():
    identity, density = _balanced()
    selected, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    for s in selected:
        # These fields exist and come from local-trade density.
        assert hasattr(s, "local_trade_rows_in_window")
        assert hasattr(s, "local_distinct_tx_hash_count_in_window")
        assert hasattr(s, "window_seconds")
        # The old CLOB-derived field must NOT exist on the record anymore.
        assert not hasattr(s, "local_density_points")


def test_precomputed_density_file_with_s1_clob_columns_is_refused(tmp_path):
    p = tmp_path / "c1a_f1_local_density.csv"
    p.write_text(
        "condition_id,local_trade_rows_in_window,local_distinct_tx_hash_count_in_window,"
        "window_seconds,observed_point_count_side_0\n"
        f"{_cid(1)},10,5,3600,99\n",
        encoding="utf-8",
    )
    with pytest.raises(sel.RejectedDensitySourceError):
        sel.read_precomputed_local_density(str(p))


def test_density_dict_carrying_clob_field_is_refused_in_evaluate():
    ident = _identity(1)
    bad_density = {
        "local_trade_rows_in_window": "10",
        "local_distinct_tx_hash_count_in_window": "5",
        "window_seconds": "3600",
        "observed_point_count_side_0": "99",  # rejected proxy sneaking in
    }
    with pytest.raises(sel.RejectedDensitySourceError):
        sel.evaluate_candidate(ident, bad_density)


def test_ranking_uses_local_trade_rows_order():
    # Lower local_trade_rows must be preferred within a subclass, regardless of any
    # (now absent) CLOB counts. cid1 has fewer rows than cid2 -> cid1 wins UP_DOWN.
    identity, density = _balanced()
    selected, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    ud = [s for s in selected if s.subclass == "UP_DOWN" and s.stratum_role == "SUBCLASS_PRIMARY"]
    assert ud and ud[0].condition_id == _cid(1)


def test_provenance_declares_local_trade_density_and_no_clob():
    identity, density = _balanced()
    _, _, prov = sel.run_selector(identity, density, density_source="COMPUTED_FROM_LOCAL_TRADES")
    assert prov["density_fields_used"] == list(sel.APPROVED_DENSITY_FIELDS)
    assert prov["used_s1_clob_point_counts_as_density"] is False
    assert set(prov["density_fields_rejected_and_never_used"]) >= {
        "observed_point_count_side_0", "observed_point_count_side_1",
        "nearest_gap_side_0_seconds", "nearest_gap_side_1_seconds",
    }
    assert prov["density_source"] == "COMPUTED_FROM_LOCAL_TRADES"


def test_identity_reader_drops_s1_clob_columns(tmp_path):
    # An S1 coverage CSV may define the bounded SET, but its CLOB columns must be
    # dropped so they can never reach density logic from the identity path.
    p = tmp_path / "price_source_s1_coverage_by_condition.csv"
    p.write_text(
        "condition_id,subclass,side_0_token,side_1_token,condition_reachability,"
        "observed_point_count_side_0,observed_point_count_side_1,nearest_gap_side_0_seconds\n"
        f"{_cid(1)},UP_DOWN,1001,2001,both,42,43,7\n",
        encoding="utf-8",
    )
    rows = sel.read_bounded_pool_identity(str(p))
    assert "observed_point_count_side_0" not in rows[0]
    assert "observed_point_count_side_1" not in rows[0]
    assert "nearest_gap_side_0_seconds" not in rows[0]
    assert rows[0]["condition_id"] == _cid(1)


def test_run_selector_rejects_non_approved_density_source():
    identity, density = _balanced()
    with pytest.raises(sel.SelectorPolicyError):
        sel.run_selector(identity, density, density_source="S1_CLOB_POINTS")


# ---------------------------------------------------------------------------
# Full-universe profiling rejected / impossible (reject 14, 15)
# ---------------------------------------------------------------------------
def test_universe_named_pool_source_is_rejected(tmp_path):
    for name in ("full_universe_pool.csv", "all_conditions.csv", "volume_profile_all.csv"):
        p = tmp_path / name
        p.write_text("condition_id,subclass,side_0_token,side_1_token,condition_reachability\n", encoding="utf-8")
        with pytest.raises(sel.SelectorPolicyError):
            sel.read_bounded_pool_identity(str(p))


def test_universe_named_density_source_is_rejected(tmp_path):
    p = tmp_path / "full_universe_volume_profile.csv"
    p.write_text(
        "condition_id,local_trade_rows_in_window,local_distinct_tx_hash_count_in_window,window_seconds\n"
        f"{_cid(1)},1,1,10\n",
        encoding="utf-8",
    )
    with pytest.raises(sel.SelectorPolicyError):
        sel.read_precomputed_local_density(str(p))


def test_provenance_flags_no_universe_scan_or_profile():
    identity, density = _balanced()
    _, _, prov = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert prov["scanned_full_universe"] is False
    assert prov["built_reusable_volume_profile"] is False
    assert prov["pool_source_is_bounded_accepted_pool"] is True


def test_compute_from_trades_restricts_to_bounded_ids(monkeypatch):
    # Prove the local-trades path filters to the bounded pool set (not a universe
    # scan) without importing pandas: stub a tiny DataFrame-like object.
    calls = {}

    class _Grp(list):
        pass

    class _FakeDF:
        def __init__(self, data):
            self._data = data  # list of dict rows

        def __getitem__(self, mask):
            return self  # isin() path returns a filtered frame; we simulate below

        def isin(self, wanted):  # noqa: D401 - test shim
            calls["isin_wanted"] = set(wanted)
            # emulate boolean mask; store filtered rows for groupby
            self._filtered = [r for r in self._data if r["condition_id"] in wanted]
            return self

        # allow df[df['condition_id'].isin(wanted)] shape
        def groupby(self, key):
            from collections import defaultdict
            g = defaultdict(list)
            for r in getattr(self, "_filtered", self._data):
                g[r["condition_id"]].append(r)
            for cid, rows in g.items():
                class _G:
                    def __init__(self, rows):
                        self._rows = rows
                    def __getitem__(self, col):
                        vals = [r[col] for r in self._rows]
                        class _Col(list):
                            def astype(self, _):
                                return _Col([str(v) for v in self])
                        return _Col(vals)
                yield cid, _G(rows)

        # df['condition_id'] used inside isin chain
        class _CidCol:
            def __init__(self, outer):
                self.outer = outer
            def isin(self, wanted):
                return self.outer.isin(wanted)

        # emulate df["condition_id"].isin(...)
        def _col(self, name):
            return _FakeDF._CidCol(self)

    fake_rows = [
        {"condition_id": _cid(1), "tx_hash": "0xa", "traded_at": 100},
        {"condition_id": _cid(1), "tx_hash": "0xa", "traded_at": 150},   # same tx
        {"condition_id": _cid(1), "tx_hash": "0xb", "traded_at": 900},
        {"condition_id": _cid(999), "tx_hash": "0xz", "traded_at": 100}, # out of pool
    ]

    class _DF2(_FakeDF):
        def __getitem__(self, item):
            # support df["condition_id"] -> col with isin, and df[mask] -> filtered
            if item == "condition_id":
                return _FakeDF._CidCol(self)
            return self

    class _FakeStore:
        def __init__(self, root):
            calls["root"] = root
        def load_trades(self):
            return _DF2(fake_rows)

    fake_mod = type(sys)("pm_research.data.store")
    fake_mod.Store = _FakeStore
    monkeypatch.setitem(sys.modules, "pm_research", type(sys)("pm_research"))
    monkeypatch.setitem(sys.modules, "pm_research.data", type(sys)("pm_research.data"))
    monkeypatch.setitem(sys.modules, "pm_research.data.store", fake_mod)

    windows = {_cid(1): (0.0, 1000.0)}
    out = sel.compute_local_density_from_trades("root", [_cid(1)], windows)
    assert calls["isin_wanted"] == {_cid(1)}          # bounded set only
    assert _cid(999) not in out                        # universe row excluded
    assert out[_cid(1)]["local_trade_rows_in_window"] == 3
    assert out[_cid(1)]["local_distinct_tx_hash_count_in_window"] == 2  # 0xa,0xb
    assert out[_cid(1)]["window_seconds"] == 1000


# ---------------------------------------------------------------------------
# Winner/outcome/PnL/score rejection (reject 7, 8, 9)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "bad_field",
    ["resolved_winning_token_id", "resolved_winning_outcome_index", "resolved_winning_label",
     "winner_token_id", "payout_numerators", "pnl", "score", "price", "yes_price",
     "side_0_price", "canonical_side_price"],
)
def test_identity_record_with_forbidden_field_hard_rejected(bad_field):
    ident = _identity(1)
    ident[bad_field] = "x"
    with pytest.raises(sel.OutcomeConditionedInputError):
        sel.evaluate_candidate(ident, _density(5, 3))


def test_identity_csv_header_with_forbidden_column_raises(tmp_path):
    p = tmp_path / "price_source_s1_coverage_by_condition.csv"
    p.write_text(
        "condition_id,subclass,side_0_token,side_1_token,resolved_winning_token_id\n"
        f"{_cid(1)},UP_DOWN,1001,2001,9\n",
        encoding="utf-8",
    )
    with pytest.raises(sel.OutcomeConditionedInputError):
        sel.read_bounded_pool_identity(str(p))


def test_provenance_asserts_no_outcome_or_price_use():
    identity, density = _balanced()
    _, _, prov = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert prov["used_winner_or_outcome_field"] is False
    assert prov["used_price_or_score_field"] is False
    assert prov["used_ordersmatched_or_wallet_or_pnl"] is False
    assert prov["used_dune_count_scout"] is False
    assert prov["used_local_tx_hash_filter"] is False


# ---------------------------------------------------------------------------
# Determinism (reject 20)
# ---------------------------------------------------------------------------
def test_selection_deterministic_across_runs_and_ordering():
    identity, density = _balanced()
    a, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    b, _, _ = sel.run_selector(list(reversed(identity)), density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert [s.condition_id for s in a] == [s.condition_id for s in b]
    assert [s.tie_break for s in a] == [s.tie_break for s in b]


def test_tie_break_matches_documented_formula_and_policy_version():
    cid = _cid(42)
    expected = hashlib.sha256(f"{cid}|{sel.SELECTOR_POLICY_VERSION}".encode("utf-8")).hexdigest()
    assert sel.tie_break_key(cid) == expected
    assert sel.tie_break_key(cid, "v-a") != sel.tie_break_key(cid, "v-b")


def test_equal_density_ties_resolve_by_hash_not_input_order():
    identity = [_identity(7, "UP_DOWN"), _identity(8, "UP_DOWN"),
                _identity(3, "OVER_UNDER"), _identity(5, "NAMED_OTHER")]
    density = {_cid(7): _density(5, 5), _cid(8): _density(5, 5),
               _cid(3): _density(2, 2), _cid(5): _density(2, 2)}
    fwd, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    rev, _, _ = sel.run_selector(list(reversed(identity)), density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    ud_fwd = [s.condition_id for s in fwd if s.subclass == "UP_DOWN"]
    ud_rev = [s.condition_id for s in rev if s.subclass == "UP_DOWN"]
    assert ud_fwd == ud_rev


# ---------------------------------------------------------------------------
# Caps + cap+1 preserved (spec 6.5 / reject 2)
# ---------------------------------------------------------------------------
def test_selected_carry_unchanged_caps_and_cap_plus_one():
    identity, density = _balanced()
    selected, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    for s in selected:
        assert s.per_condition_row_cap == 2000
        assert s.global_row_cap == 6000
        assert s.dune_query_limit_over_fetch == 2001


def test_module_constants_match_c1a_ceilings():
    assert sel.PER_CONDITION_ROW_CAP_CEILING == 2000
    assert sel.GLOBAL_ROW_CAP_CEILING == 6000
    assert sel.DUNE_QUERY_LIMIT_OVER_FETCH == 2001


def test_provenance_records_caps_not_raised():
    identity, density = _balanced()
    _, _, prov = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert prov["caps_raised"] is False


# ---------------------------------------------------------------------------
# 3-5 bound (spec 6.5 / reject 10)
# ---------------------------------------------------------------------------
def test_selection_never_exceeds_five():
    subs = ["UP_DOWN", "OVER_UNDER", "NAMED_OTHER"]
    identity = [_identity(i, subs[i % 3]) for i in range(1, 30)]
    density = {_cid(i): _density(i, i) for i in range(1, 30)}
    selected, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert 3 <= len(selected) <= 5


def test_pool_too_small_raises_rejected():
    identity = [_identity(1, "UP_DOWN")]
    density = {_cid(1): _density(1, 1)}
    with pytest.raises(sel.SelectorPolicyError) as ei:
        sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE", allow_sentinel=False)
    assert sel.FAIL_POOL_TOO_SMALL in str(ei.value)


def test_out_of_range_bounds_rejected():
    c = sel.PoolCandidate(_cid(1), "UP_DOWN", "1", "2", "both", "x", 2, 1, 3600, sel.tie_break_key(_cid(1)))
    with pytest.raises(sel.SelectorPolicyError):
        sel.select_conditions([c], max_conditions=6)


# ---------------------------------------------------------------------------
# Subclass stratification + sentinel (spec 6.3)
# ---------------------------------------------------------------------------
def test_prefers_one_candidate_per_subclass():
    identity, density = _balanced()
    selected, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert {s.subclass for s in selected} == {"UP_DOWN", "OVER_UNDER", "NAMED_OTHER"}


def test_empty_subclass_not_silently_relabeled():
    identity = [_identity(1, "UP_DOWN"), _identity(2, "UP_DOWN"), _identity(3, "OVER_UNDER")]
    density = {_cid(1): _density(1, 1), _cid(2): _density(2, 2), _cid(3): _density(3, 3)}
    selected, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert "NAMED_OTHER" not in {s.subclass for s in selected}


def test_sentinel_added_when_below_min_and_deterministic():
    identity = [_identity(1, "UP_DOWN"), _identity(3, "OVER_UNDER"),
                _identity(9, "UP_DOWN"), _identity(11, "UP_DOWN"), _identity(13, "UP_DOWN")]
    density = {_cid(1): _density(1, 1), _cid(3): _density(2, 2), _cid(9): _density(10, 5),
               _cid(11): _density(20, 8), _cid(13): _density(30, 10)}
    fwd, _, _ = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE", allow_sentinel=True)
    rev, _, _ = sel.run_selector(list(reversed(identity)), density, density_source="PRECOMPUTED_LOCAL_POOL_FILE", allow_sentinel=True)
    assert any(s.stratum_role == "SENTINEL" for s in fwd)
    fwd_sent = [s.condition_id for s in fwd if s.stratum_role == "SENTINEL"]
    rev_sent = [s.condition_id for s in rev if s.stratum_role == "SENTINEL"]
    assert fwd_sent == rev_sent


# ---------------------------------------------------------------------------
# Uniform prior-C1A holdout (spec 6.3 item 8 / reject 1)
# ---------------------------------------------------------------------------
def test_holdout_excludes_whole_prior_manifest_uniformly():
    identity, density = _balanced()
    holdout = [_cid(1), _cid(3)]
    selected, rejected, _ = sel.run_selector(
        identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE", prior_c1a_holdout_ids=holdout
    )
    sel_ids = {s.condition_id for s in selected}
    assert _cid(1) not in sel_ids and _cid(3) not in sel_ids
    reasons = {r.condition_id: r.reason for r in rejected}
    assert reasons.get(_cid(1)) == sel.REJECT_PRIOR_C1A_HOLDOUT
    assert reasons.get(_cid(3)) == sel.REJECT_PRIOR_C1A_HOLDOUT


def test_holdout_flag_recorded_in_provenance():
    identity, density = _balanced()
    _, _, prov = sel.run_selector(
        identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE", prior_c1a_holdout_ids=[_cid(1)]
    )
    assert prov["prior_c1a_holdout_applied"] is True
    assert prov["prior_c1a_holdout_uniform_whole_manifest"] is True


# ---------------------------------------------------------------------------
# Token/precision/eligibility discipline
# ---------------------------------------------------------------------------
def test_token_pair_must_be_two_distinct_stable_tokens():
    cand, rej = sel.evaluate_candidate(_identity(1, t0="1001", t1="1001"), _density(5, 3))
    assert cand is None and rej.reason == sel.REJECT_TOKEN_PAIR_NOT_TWO_STABLE


def test_scientific_notation_token_is_precision_loss():
    cand, rej = sel.evaluate_candidate(_identity(1, t0="1e21", t1="2002"), _density(5, 3))
    assert cand is None and rej.reason == sel.REJECT_TOKEN_PRECISION_LOSS


def test_scientific_notation_density_is_reject():
    cand, rej = sel.evaluate_candidate(_identity(1), {"local_trade_rows_in_window": "1e3",
                                                      "local_distinct_tx_hash_count_in_window": "5",
                                                      "window_seconds": "3600"})
    assert cand is None and rej.reason == sel.REJECT_DENSITY_UNPARSEABLE


def test_missing_density_is_reject():
    cand, rej = sel.evaluate_candidate(_identity(1), None)
    assert cand is None and rej.reason == sel.REJECT_DENSITY_MISSING


def test_non_oriented_subclass_rejected():
    cand, rej = sel.evaluate_candidate(_identity(1, subclass="YES_NO"), _density(5, 3))
    assert cand is None and rej.reason == sel.REJECT_SUBCLASS_NOT_ORIENTED


def test_malformed_condition_id_rejected():
    ident = _identity(1)
    ident["condition_id"] = "0xdeadbeef"
    cand, rej = sel.evaluate_candidate(ident, _density(5, 3))
    assert cand is None and rej.reason == sel.REJECT_CONDITION_ID_MALFORMED


def test_not_reachable_both_rejected_when_required():
    cand, rej = sel.evaluate_candidate(_identity(1, reach="one"), _density(5, 3))
    assert cand is None and rej.reason == sel.REJECT_NOT_REACHABLE_BOTH


def test_canonical_count_rejects_float_and_scientific():
    with pytest.raises(sel.DensityPrecisionError):
        sel.canonical_count(3.0)
    with pytest.raises(sel.DensityPrecisionError):
        sel.canonical_count("1e5")


# ---------------------------------------------------------------------------
# No Dune / network / run path exists
# ---------------------------------------------------------------------------
def test_no_run_authorized_flag_and_scope():
    identity, density = _balanced()
    _, _, prov = sel.run_selector(identity, density, density_source="PRECOMPUTED_LOCAL_POOL_FILE")
    assert prov["no_run_authorized"] is True
    assert prov["authorized_scope"].endswith("NO_NETWORK_NO_RUN")


def test_module_has_no_network_or_sql_symbols():
    src_path = os.path.join(os.path.dirname(__file__), "..", "scripts",
                            "price_source_option_c_c1a_f1_selector.py")
    with open(src_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    for banned in ("import requests", "urllib.request", "http.client", "socket.",
                   ".execute(", "read_sql", "api.dune.com", "x-dune-api-key"):
        assert banned not in src, f"unexpected network/sql construct: {banned}"
