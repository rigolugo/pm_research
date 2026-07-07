"""Pure-logic tests for S1 price-source coverage - Pass 1 only.

No network. All endpoint responses are mocked (injected transport / injected bodies).
Mirrors the project discipline: tests pass on injected shapes first; fixtures must later
mirror the *verified* real shape (HANDOFF P1_REVIEW) before any run is believed.
"""

import importlib.util
import os
import sys

import pytest

# Import the script module directly (scripts/ is not a package).
_HERE = os.path.dirname(__file__)
_SCRIPT = os.path.abspath(os.path.join(_HERE, "..", "scripts", "price_source_s1_coverage.py"))
_spec = importlib.util.spec_from_file_location("price_source_s1_coverage", _SCRIPT)
s1 = importlib.util.module_from_spec(_spec)
# Register before exec so @dataclass can resolve annotations via sys.modules.
sys.modules["price_source_s1_coverage"] = s1
_spec.loader.exec_module(s1)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------
V = s1.NB_CONTRACT_VERSION
TOK_A = "111" + "0" * 74 + "01"   # 78-ish digit string-safe token
TOK_B = "222" + "0" * 74 + "02"
TOK_C = "333" + "0" * 74 + "03"
TOK_D = "444" + "0" * 74 + "04"


def _p0_clear(final=39693):
    return {
        "p0_state": "P0_CLEAR",
        "nb_contract_version_expected": V,
        "nb_contract_version_contract": V,
        "nb_contract_version_resolution_source": V,
        "counts_pooled": {"final_p0_eligible": final},
    }


def _contract_rec(cid, sub, eligible="True"):
    return {
        "condition_id": cid,
        "nb_subclass": sub,
        "nb_eligible": eligible,
        "nb_contract_version": V,
        "exclusion_reason": "None",
    }


def _res_row(cid, sub, resolved_at="2025-03-06 00:00:00 UTC", winner_token=TOK_A):
    return {
        "condition_id": cid,
        "subclass": sub,
        "resolved_winning_token_id": winner_token,
        "resolved_winning_outcome_index": "0",
        "resolved_winning_label": "WINNER",
        "resolved_at": resolved_at,
        "source_table": "polymarket_polygon.ctf_evt_conditionresolution",
        "status": "RESOLVED_SINGLE_WINNER",
        "nb_contract_version": V,
    }


def _series(token, pts, status=s1.SERIES_PRESENT):
    return s1.SeriesResult(
        token_id=token,
        status=status,
        points=[s1.PricePoint(ts=t, p=p, token_id=token) for (t, p) in pts],
    )


# ---------------------------------------------------------------------------
# P0 not clear / stale contract
# ---------------------------------------------------------------------------
def test_p0_not_clear_raises():
    bad = _p0_clear()
    bad["p0_state"] = "STOP_SOMETHING"
    with pytest.raises(ValueError) as e:
        s1.validate_p0(bad)
    assert s1.STOP_P0_NOT_CLEAR in str(e.value)


def test_p0_missing_dict_raises():
    with pytest.raises(ValueError) as e:
        s1.validate_p0(None)
    assert s1.STOP_P0_NOT_CLEAR in str(e.value)


def test_stale_contract_version_raises():
    bad = _p0_clear()
    bad["nb_contract_version_resolution_source"] = "nb-contract-OLD.0"
    with pytest.raises(ValueError) as e:
        s1.validate_p0(bad)
    assert s1.STOP_STALE_CONTRACT in str(e.value)


def test_p0_clear_returns_authoritative_count():
    # Artifact is authoritative even if it diverges from the pinned expected count.
    assert s1.validate_p0(_p0_clear(39693)) == 39693
    assert s1.validate_p0(_p0_clear(40000)) == 40000  # reported clearly, not overridden


# ---------------------------------------------------------------------------
# Universe build + subclass cross-check (join)
# ---------------------------------------------------------------------------
def test_build_universe_inner_join_excludes_yesno_and_unusable():
    contract = [
        _contract_rec("0xa", "UP_DOWN"),
        _contract_rec("0xb", "YES_NO"),          # excluded (not oriented)
        _contract_rec("0xc", "UNUSABLE"),        # excluded
        _contract_rec("0xd", "NAMED_OTHER", eligible="False"),  # excluded (ineligible)
        _contract_rec("0xe", "OVER_UNDER"),
    ]
    rows = [
        _res_row("0xa", "UP_DOWN"),
        _res_row("0xb", "YES_NO"),
        _res_row("0xe", "OVER_UNDER"),
        _res_row("0xz", "UP_DOWN"),  # not in contract -> not joined
    ]
    uni = s1.build_universe(contract, rows)
    cids = sorted(c.condition_id for c in uni)
    assert cids == ["0xa", "0xe"]


def test_build_universe_subclass_mismatch_hard_stops():
    contract = [_contract_rec("0xa", "UP_DOWN")]
    rows = [_res_row("0xa", "NAMED_OTHER")]  # subclass disagreement
    with pytest.raises(ValueError) as e:
        s1.build_universe(contract, rows)
    assert s1.STOP_STALE_CONTRACT in str(e.value)


def test_build_universe_only_resolved_single_winner_rows():
    contract = [_contract_rec("0xa", "UP_DOWN")]
    row = _res_row("0xa", "UP_DOWN")
    row["status"] = "AMBIGUOUS_MULTIPLE_WINNERS"
    assert s1.build_universe(contract, [row]) == []


# ---------------------------------------------------------------------------
# Token-pair enumeration: exactly two stable string-safe tokens
# ---------------------------------------------------------------------------
def test_token_pair_exactly_two_stable_tokens():
    tuples = [("0xa", TOK_A, "0"), ("0xa", TOK_B, "1"), ("0xa", TOK_A, "0")]
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == "OK"
    assert (s0, s1_tok) == (TOK_A, TOK_B)
    assert malformed == 0


def test_token_pair_missing_side_unresolved():
    tuples = [("0xa", TOK_A, "0")]  # only side 0
    _, _, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == s1.TOKEN_PAIR_UNRESOLVED
    assert malformed == 0


def test_token_pair_unstable_index_maps_two_tokens_unresolved():
    tuples = [("0xa", TOK_A, "0"), ("0xa", TOK_C, "0"), ("0xa", TOK_B, "1")]
    _, _, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == s1.TOKEN_PAIR_UNRESOLVED
    assert malformed == 0


def test_token_pair_three_indices_unresolved():
    tuples = [("0xa", TOK_A, "0"), ("0xa", TOK_B, "1"), ("0xa", TOK_C, "2")]
    _, _, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == s1.TOKEN_PAIR_UNRESOLVED
    assert malformed == 0


def test_token_pair_duplicate_token_both_sides_unresolved():
    tuples = [("0xa", TOK_A, "0"), ("0xa", TOK_A, "1")]
    _, _, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == s1.TOKEN_PAIR_UNRESOLVED
    assert malformed == 0


def test_token_pair_rejects_winning_token_as_source():
    # Guard-by-construction: enumeration consumes only (cid, token_id, outcome_index)
    # tuples from TRADES. There is no code path that accepts resolved_winning_token_id.
    import inspect
    code = _executable_code_only(inspect.getsource(s1.enumerate_token_pair))
    assert "resolved_winning_token_id" not in code
    assert "winning" not in code.lower()
    # resolve_token_pairs is fed trades_by_condition only.
    sig = inspect.signature(s1.resolve_token_pairs)
    assert list(sig.parameters) == ["universe", "trades_by_condition"]


# ---------------------------------------------------------------------------
# Precision-loss rejection (fail loud, never soft-unresolved)
# ---------------------------------------------------------------------------
def test_precision_loss_scientific_notation_token_raises():
    tuples = [("0xa", "5.20896e+76", "0"), ("0xa", TOK_B, "1")]
    with pytest.raises(s1.DataExportPrecisionLoss):
        s1.enumerate_token_pair(tuples)


def test_precision_loss_float_token_raises():
    tuples = [("0xa", 5.20896e76, "0"), ("0xa", TOK_B, "1")]
    with pytest.raises(s1.DataExportPrecisionLoss):
        s1.enumerate_token_pair(tuples)


def test_canonical_int_accepts_string_safe_and_zero_float_tail():
    assert s1.canonical_int("0") == 0
    assert s1.canonical_int("0.0") == 0
    assert s1.canonical_int("  12 ") == 12
    big = "9" * 78
    assert s1.canonical_int(big) == int(big)


def test_client_get_rejects_precision_loss_token():
    client = s1.PricesHistoryClient(transport=lambda *a, **k: (200, {"history": []}))
    with pytest.raises(s1.DataExportPrecisionLoss):
        client.get_prices_history("5.20896e+76", 0, 100)


# ---------------------------------------------------------------------------
# resolve_token_pairs: large unreliable fraction -> STOP
# ---------------------------------------------------------------------------
def test_resolve_token_pairs_large_unreliable_fraction_stops():
    uni = [s1.ConditionRecord(f"0x{i}", "UP_DOWN", "2025-01-01 00:00:00 UTC") for i in range(10)]
    trades = {}
    # Only 5 conditions resolvable; 5 missing -> 50% unresolved > 20% guard.
    for i in range(5):
        trades[f"0x{i}"] = [(f"0x{i}", TOK_A, "0"), (f"0x{i}", TOK_B, "1")]
    with pytest.raises(ValueError) as e:
        s1.resolve_token_pairs(uni, trades)
    assert s1.STOP_TOKEN_ENUMERATION_UNRELIABLE in str(e.value)


def test_resolve_token_pairs_small_unreliable_fraction_ok():
    uni = [s1.ConditionRecord(f"0x{i}", "UP_DOWN", "2025-01-01 00:00:00 UTC") for i in range(20)]
    trades = {}
    for i in range(19):  # 1 missing -> 5% < 20%
        trades[f"0x{i}"] = [(f"0x{i}", TOK_A, "0"), (f"0x{i}", TOK_B, "1")]
    resolved, unresolved = s1.resolve_token_pairs(uni, trades)
    assert len(resolved) == 19 and len(unresolved) == 1


# ---------------------------------------------------------------------------
# Level A status mapping (mocked responses)
# ---------------------------------------------------------------------------
def test_level_a_present():
    r = s1.map_response_to_status(200, {"history": [{"t": 100, "p": 0.5}]}, TOK_A)
    assert r.status == s1.SERIES_PRESENT and len(r.points) == 1


def test_level_a_empty():
    r = s1.map_response_to_status(200, {"history": []}, TOK_A)
    assert r.status == s1.SERIES_EMPTY


def test_level_a_notfound_404():
    r = s1.map_response_to_status(404, None, TOK_A)
    assert r.status == s1.SERIES_ERROR_NOTFOUND


def test_level_a_transient_5xx_and_429():
    assert s1.map_response_to_status(503, None, TOK_A).status == s1.SERIES_ERROR_TRANSIENT
    assert s1.map_response_to_status(429, None, TOK_A).status == s1.SERIES_ERROR_TRANSIENT


def test_level_a_malformed_missing_tp():
    r = s1.map_response_to_status(200, {"history": [{"t": 100}]}, TOK_A)
    assert r.status == s1.SERIES_MALFORMED


def test_level_a_malformed_sci_notation_token_echo():
    r = s1.map_response_to_status(
        200, {"history": [{"t": 100, "p": 0.5, "token_id": "5.2e+76"}]}, TOK_A
    )
    assert r.status == s1.SERIES_MALFORMED


def test_endpoint_shape_unrecognized_raises():
    with pytest.raises(s1.EndpointShapeError):
        s1.map_response_to_status(200, {"unexpected": 1}, TOK_A)
    with pytest.raises(s1.EndpointShapeError):
        s1.map_response_to_status(200, ["not", "a", "dict"], TOK_A)


# ---------------------------------------------------------------------------
# Level B decision-window classification
# ---------------------------------------------------------------------------
def test_point_at_warmup_counts():
    ft = 1000.0
    resolved_at = 1_000_000.0
    s0 = _series(TOK_A, [(ft + s1.WARMUP_SECONDS, 0.4)])       # exactly at warmup -> counts
    s1r = _series(TOK_B, [(ft + s1.WARMUP_SECONDS + 5, 0.6)])
    cls = s1.classify_decision_window(s0, s1r, ft, resolved_at)
    assert cls == s1.DECISION_PRICE_BOTH_SIDES


def test_point_before_warmup_does_not_count():
    ft = 1000.0
    resolved_at = 1_000_000.0
    s0 = _series(TOK_A, [(ft + s1.WARMUP_SECONDS - 1, 0.4)])   # 1s before warmup
    s1r = _series(TOK_B, [(ft + s1.WARMUP_SECONDS + 5, 0.6)])
    cls = s1.classify_decision_window(s0, s1r, ft, resolved_at)
    assert cls == s1.DECISION_PRICE_ONE_SIDE  # only side 1 usable


def test_point_at_or_after_resolved_at_does_not_count_leakage():
    ft = 1000.0
    resolved_at = ft + s1.WARMUP_SECONDS + 100
    # both sides only have a point AT resolved_at (leakage) -> neither counts
    s0 = _series(TOK_A, [(resolved_at, 0.4)])
    s1r = _series(TOK_B, [(resolved_at + 50, 0.6)])
    cls = s1.classify_decision_window(s0, s1r, ft, resolved_at)
    assert cls == s1.DECISION_PRICE_NEITHER


def test_one_side_not_usable():
    ft = 1000.0
    resolved_at = 1_000_000.0
    s0 = _series(TOK_A, [(ft + s1.WARMUP_SECONDS + 10, 0.4)])
    s1r = _series(TOK_B, [], status=s1.SERIES_EMPTY)  # side 1 absent
    cls = s1.classify_decision_window(s0, s1r, ft, resolved_at)
    assert cls == s1.DECISION_PRICE_ONE_SIDE


def test_no_trade_anchor():
    s0 = _series(TOK_A, [(5000, 0.4)])
    s1r = _series(TOK_B, [(5000, 0.6)])
    cls = s1.classify_decision_window(s0, s1r, None, 1_000_000.0)
    assert cls == s1.NO_TRADE_ANCHOR


def test_side_not_present_status_never_counts():
    ft = 1000.0
    resolved_at = 1_000_000.0
    # points exist in window but status is TRANSIENT error -> not counted
    s0 = s1.SeriesResult(TOK_A, s1.SERIES_ERROR_TRANSIENT,
                         points=[s1.PricePoint(ft + 5000, 0.4, TOK_A)])
    s1r = _series(TOK_B, [(ft + 5000, 0.6)])
    cls = s1.classify_decision_window(s0, s1r, ft, resolved_at)
    assert cls == s1.DECISION_PRICE_ONE_SIDE


# ---------------------------------------------------------------------------
# All-one-status guard
# ---------------------------------------------------------------------------
def test_all_one_status_guard_fires():
    assert s1.all_one_status_guard([s1.SERIES_PRESENT] * 50) is True
    assert s1.all_one_status_guard([s1.SERIES_EMPTY] * 50) is True


def test_all_one_status_guard_mixed_ok():
    assert s1.all_one_status_guard([s1.SERIES_PRESENT, s1.SERIES_EMPTY]) is False


def test_all_one_status_guard_trivial_n():
    assert s1.all_one_status_guard([s1.SERIES_PRESENT]) is False


# ---------------------------------------------------------------------------
# Forbidden inference: no yes_price / 1 - yes_price / 1 - p side synthesis
# ---------------------------------------------------------------------------
def _executable_code_only(src):
    """Return source with all comments and string/docstring literals removed, so
    pattern scans target EXECUTABLE code, not prose that names the forbidden pattern
    in order to forbid it."""
    import io
    import tokenize

    out = []
    toks = tokenize.generate_tokens(io.StringIO(src).readline)
    for tok in toks:
        if tok.type in (tokenize.COMMENT, tokenize.STRING):
            continue
        out.append(tok.string)
    return " ".join(out)


def test_no_forbidden_side_synthesis_in_source():
    code = _executable_code_only(open(_SCRIPT).read()).replace(" ", "")
    # Executable side-synthesis patterns that must never appear.
    banned_exec = [
        "1-yes_price",
        "1-p",              # covers 1 - p, 1 - pt.p (after space-strip: 1-pt.p contains 1-p)
        "1-price",
        "1-side_0_price",
        "1-side_1_price",
    ]
    for pat in banned_exec:
        assert pat not in code, f"forbidden side-synthesis in executable code: {pat!r}"


def test_map_response_does_not_convert_p():
    import inspect
    code = _executable_code_only(inspect.getsource(s1.map_response_to_status)).replace(" ", "")
    assert "1-p" not in code
    # p is carried verbatim as the source-defined price.
    r = s1.map_response_to_status(200, {"history": [{"t": 1, "p": 0.73}]}, TOK_A)
    assert r.points[0].p == 0.73


# ---------------------------------------------------------------------------
# Batch-vs-single equivalence (mocked)
# ---------------------------------------------------------------------------
def test_batch_single_equivalent_true():
    single = _series(TOK_A, [(100, 0.5), (200, 0.6)])
    batched = _series(TOK_A, [(100, 0.5), (200, 0.6)])
    assert s1.batch_single_equivalent(single, batched) is True


def test_batch_single_divergence_flags_false():
    single = _series(TOK_A, [(100, 0.5), (200, 0.6)])
    batched = _series(TOK_A, [(100, 0.5), (200, 0.61)])  # price diverges
    assert s1.batch_single_equivalent(single, batched) is False


def test_batch_client_maps_histories(monkeypatch):
    body = {"histories": {TOK_A: [{"t": 1, "p": 0.5}], TOK_B: []}}
    client = s1.PricesHistoryClient(transport=lambda *a, **k: (200, body))
    out = client.post_batch_prices_history([TOK_A, TOK_B], 0, 100)
    assert out[TOK_A].status == s1.SERIES_PRESENT
    assert out[TOK_B].status == s1.SERIES_EMPTY


# ---------------------------------------------------------------------------
# Network hard-gate: STOP_NOT_AUTHORIZED without explicit auth
# ---------------------------------------------------------------------------
def test_client_without_auth_or_transport_refuses_network():
    client = s1.PricesHistoryClient(network_authorized=False, transport=None)
    with pytest.raises(s1.NotAuthorizedError) as e:
        client.get_prices_history(TOK_A, 0, 100)
    assert s1.STOP_NOT_AUTHORIZED in str(e.value)


def test_cli_default_is_not_authorized(capsys):
    rc = s1.main([])  # no auth flags
    out = capsys.readouterr().out
    assert rc == 2
    assert s1.STOP_NOT_AUTHORIZED in out


def test_cli_requires_both_auth_flags():
    class NS: pass
    ns = NS()
    ns.i_authorize_s1_pass1_network_run = True
    ns.confirm_external_host = "wrong-host"
    assert s1.network_authorized_from_args(ns) is False
    ns.confirm_external_host = "clob.polymarket.com"
    assert s1.network_authorized_from_args(ns) is True


def test_transport_injection_never_hits_network():
    calls = []

    def fake_transport(method, url, payload):
        calls.append((method, url, payload))
        return 200, {"history": [{"t": 100, "p": 0.5}]}

    client = s1.PricesHistoryClient(transport=fake_transport)
    r = client.get_prices_history(TOK_A, 0, 100, interval="max", fidelity=60)
    assert r.status == s1.SERIES_PRESENT
    method, url, payload = calls[0]
    assert method == "GET"
    assert url.endswith("/prices-history")
    assert payload["market"] == TOK_A       # market == token id
    assert payload["startTs"] == 0 and payload["endTs"] == 100  # camelCase for single GET
    assert payload["fidelity"] == 60


# ---------------------------------------------------------------------------
# Pass 2 not available
# ---------------------------------------------------------------------------
def test_pass2_hard_stops():
    with pytest.raises(s1.Pass2NotAvailable):
        s1.run_pass2()


# ---------------------------------------------------------------------------
# No writes to prices/ ; gate/blocked flag never touched (guard-by-construction)
# ---------------------------------------------------------------------------
def test_no_writes_to_prices_or_gate_in_source():
    code = _executable_code_only(open(_SCRIPT).read())
    # No persistence into prices/, no store save calls, no backfill invocation.
    assert "save_prices" not in code
    assert "backfill_prices_from_clob" not in code
    assert "save_resolutions" not in code
    assert "save_markets" not in code


def test_named_binary_probe_blocked_not_flipped():
    code = _executable_code_only(open(_SCRIPT).read())
    # The script must not assign the gate flag at all.
    assert "named_binary_probe_blocked" not in code


# ---------------------------------------------------------------------------
# Reconciliation: buckets sum to the P0 universe
# ---------------------------------------------------------------------------
def test_reconcile_exact():
    rec = s1.reconcile(39693, {"a": 39000, "b": 693})
    assert rec["exact"] is True and rec["bucket_total"] == 39693


def test_reconcile_off_by_one_fails():
    rec = s1.reconcile(39693, {"a": 39000, "b": 692})
    assert rec["exact"] is False


# ---------------------------------------------------------------------------
# Subclass coverage rate excludes NO_TRADE_ANCHOR
# ---------------------------------------------------------------------------
def test_subclass_coverage_rate():
    classifications = [
        ("UP_DOWN", s1.DECISION_PRICE_BOTH_SIDES),
        ("UP_DOWN", s1.DECISION_PRICE_BOTH_SIDES),
        ("UP_DOWN", s1.DECISION_PRICE_ONE_SIDE),
        ("UP_DOWN", s1.NO_TRADE_ANCHOR),  # excluded from denominator
        ("OVER_UNDER", s1.DECISION_PRICE_BOTH_SIDES),
    ]
    both, measured, rate = s1.subclass_coverage_rate(classifications, "UP_DOWN")
    assert (both, measured) == (2, 3)
    assert abs(rate - (2 / 3)) < 1e-9


# ---------------------------------------------------------------------------
# Stratified sample: bounded, deterministic, covers subclasses
# ---------------------------------------------------------------------------
def _sample_universe():
    conds = []
    for i in range(500):
        conds.append(s1.ConditionRecord(f"0xup{i:04d}", "UP_DOWN",
                                        f"2024-0{(i%6)+1}-01 00:00:00 UTC"))
    for i in range(60):
        conds.append(s1.ConditionRecord(f"0xou{i:04d}", "OVER_UNDER",
                                        f"2024-0{(i%6)+1}-01 00:00:00 UTC"))
    for i in range(300):
        conds.append(s1.ConditionRecord(f"0xno{i:04d}", "NAMED_OTHER",
                                        f"2024-0{(i%6)+1}-01 00:00:00 UTC"))
    return conds


def test_sample_is_bounded_and_not_full_universe():
    conds = _sample_universe()
    sample = s1.build_pass1_sample(conds, sample_size=300, seed=1)
    assert len(sample) <= 300
    assert len(sample) < len(conds)  # never the full universe


def test_sample_is_deterministic():
    conds = _sample_universe()
    a = [c.condition_id for c in s1.build_pass1_sample(conds, 300, seed=7)]
    b = [c.condition_id for c in s1.build_pass1_sample(conds, 300, seed=7)]
    assert a == b


def test_sample_covers_all_present_subclasses():
    conds = _sample_universe()
    sample = s1.build_pass1_sample(conds, 300, seed=3)
    subs = {c.subclass for c in sample}
    assert subs == {"UP_DOWN", "OVER_UNDER", "NAMED_OTHER"}


def test_sample_respects_small_subclass_pool():
    # OVER_UNDER pool is only 60; its allocation must not exceed the pool.
    conds = _sample_universe()
    sample = s1.build_pass1_sample(conds, 300, seed=5)
    ou = [c for c in sample if c.subclass == "OVER_UNDER"]
    assert len(ou) <= 60


# ---------------------------------------------------------------------------
# resolved_at used only as a window bound (guard-by-construction)
# ---------------------------------------------------------------------------
def test_resolved_at_only_bounds_window():
    import inspect
    raw = inspect.getsource(s1.has_decision_window_point)
    code = _executable_code_only(raw).replace(" ", "")
    # resolved_at appears only in the strict upper-bound comparison (ts < resolved_at_ts).
    assert "ts<resolved_at_ts" in code
    # It is never added to features/targets in executable code.
    exec_all = _executable_code_only(open(_SCRIPT).read())
    assert "feature" not in exec_all and "target" not in exec_all


# ===========================================================================
# Orchestration tests (run_pass1_coverage) - mocked loader / client / writer.
# No network, no filesystem, no parquet. Pure logic over injected doubles.
# ===========================================================================
class FakeLoader:
    """Injected store loader. Returns in-memory contract/resolution/trades."""

    def __init__(self, p0=None, contract=None, rows=None, trades=None, first_ts=None):
        self._p0 = p0 if p0 is not None else _p0_clear()
        self._contract = contract if contract is not None else []
        self._rows = rows if rows is not None else []
        self._trades = trades if trades is not None else {}
        self._first_ts = first_ts if first_ts is not None else {}
        self.trades_requested_for = None

    def load_p0_preflight(self):
        return self._p0

    def load_contract_conditions(self):
        return self._contract

    def load_resolution_rows(self):
        return self._rows

    def load_trades_index(self, condition_ids):
        self.trades_requested_for = list(condition_ids)
        t = {c: self._trades[c] for c in condition_ids if c in self._trades}
        f = {c: self._first_ts[c] for c in condition_ids if c in self._first_ts}
        return t, f


class FakeClient:
    """Injected endpoint client. Mirrors the real client's shape-capture contract.

    NEVER touches the network - it does not subclass PricesHistoryClient and has no
    transport. It builds SYNTHETIC raw bodies (documented shape) and feeds shape_sink
    exactly like the real client, so the orchestration's observed-shape capture path is
    genuinely exercised by mocks.

    body_by_token: optional {token_id: raw_body} to inject arbitrary/deviant shapes.
    """

    def __init__(self, series_by_token=None, default_status=None, body_by_token=None,
                 batch_body=None):
        self.series_by_token = series_by_token or {}
        self.default_status = default_status or s1.SERIES_PRESENT
        self.body_by_token = body_by_token or {}
        self.batch_body = batch_body
        self.get_calls = []
        self.batch_calls = []
        self.shape_sink = None  # set by the orchestration

    def _synth_body(self, token_id, start_ts):
        # Documented shape: {"history": [{"t":..,"p":..,"token_id":..}, ...]}
        if token_id in self.body_by_token:
            return self.body_by_token[token_id]
        status = self.default_status
        if token_id in self.series_by_token:
            sr = self.series_by_token[token_id]
            return {"history": [{"t": pt.ts, "p": pt.p, "token_id": pt.token_id}
                                for pt in sr.points]} if sr.status == s1.SERIES_PRESENT else (
                {"history": []} if sr.status == s1.SERIES_EMPTY else {"history": []}
            )
        if status == s1.SERIES_EMPTY:
            return {"history": []}
        return {"history": [{"t": start_ts + s1.WARMUP_SECONDS + 10, "p": 0.5,
                             "token_id": token_id}]}

    def _capture(self, context, path, payload, http_status, body):
        if self.shape_sink is None:
            return
        self.shape_sink.append({
            "context": context,
            "path": path,
            "payload_keys": sorted(str(k) for k in payload.keys()),
            "payload": {k: (v if not isinstance(v, list) else f"<list:{len(v)}>")
                        for k, v in payload.items()},
            "http_status": http_status,
            "body": body,
        })

    def get_prices_history(self, token_id, start_ts, end_ts, interval="max", fidelity=None):
        self.get_calls.append((token_id, start_ts, end_ts, interval, fidelity))
        params = {"market": str(token_id), "startTs": int(start_ts), "endTs": int(end_ts),
                  "interval": interval}
        if fidelity is not None:
            params["fidelity"] = int(fidelity)
        body = self._synth_body(token_id, start_ts)
        self._capture("get", "/prices-history", params, 200, body)
        # Injected canned SeriesResult takes precedence when provided (status-focused tests).
        if token_id in self.series_by_token:
            return self.series_by_token[token_id]
        return s1.map_response_to_status(200, body, str(token_id))

    def post_batch_prices_history(self, token_ids, start_ts, end_ts, interval="max", fidelity=None):
        self.batch_calls.append((tuple(token_ids), start_ts, end_ts))
        payload = {"markets": [str(t) for t in token_ids], "start_ts": int(start_ts),
                   "end_ts": int(end_ts), "interval": interval}
        if fidelity is not None:
            payload["fidelity"] = int(fidelity)
        if self.batch_body is not None:
            body = self.batch_body
        else:
            body = {"histories": {str(t): self._synth_body(t, start_ts).get("history", [])
                                  for t in token_ids}}
        # Capture BEFORE any shape validation, exactly like the real client, so a deviating
        # batch body is still recorded in shape_sink for the endpoint-shape ledger.
        self._capture("batch", "/batch-prices-history", payload, 200, body)
        # Fidelity to the real client's contract: a body without a histories key is a
        # documented-shape deviation and must raise (never coerce).
        if not isinstance(body, dict) or "histories" not in body:
            raise s1.EndpointShapeError(
                f"{s1.STOP_ENDPOINT_SHAPE_UNRECOGNIZED}: batch has no histories"
            )
        out = {}
        for t in token_ids:
            per = body["histories"].get(str(t))
            if per is None:
                out[t] = s1.map_response_to_status(200, self._synth_body(t, start_ts), str(t))
            else:
                out[t] = s1.map_response_to_status(None, {"history": per}, str(t))
        return out


class FakeWriter:
    """Injected artifact writer. Captures writes in memory; touches no disk."""

    def __init__(self):
        self.written = {}  # filename -> content

    def s1_dir(self):
        return "artifacts/named_binary_probe/price_source_s1"

    def write_text(self, filename, text):
        self.written[filename] = text
        return f"{self.s1_dir()}/{filename}"

    def write_json(self, filename, obj):
        import json
        self.written[filename] = json.dumps(obj, sort_keys=True)
        return f"{self.s1_dir()}/{filename}"

    def write_csv(self, filename, header, rows):
        import csv, io
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(list(header))
        for r in rows:
            w.writerow(list(r))
        self.written[filename] = buf.getvalue()
        return f"{self.s1_dir()}/{filename}"


def _universe_fixture(n_up=40, n_ou=8, n_no=24):
    """Build matching contract + resolution rows + trades for a small universe."""
    contract, rows, trades, first_ts = [], [], {}, {}
    counter = 0

    def add(cid, sub):
        nonlocal counter
        contract.append(_contract_rec(cid, sub))
        rows.append(_res_row(cid, sub, resolved_at="2025-03-06 00:00:00 UTC"))
        t0 = "111" + f"{counter:074d}" + "10"   # side 0 token (string-safe)
        t1 = "222" + f"{counter:074d}" + "20"   # side 1 token
        trades[cid] = [(cid, t0, "0"), (cid, t1, "1")]
        # first trade well before resolution so the decision window is open
        first_ts[cid] = s1.parse_ts("2025-03-01 00:00:00 UTC")
        counter += 1

    for i in range(n_up):
        add(f"0xup{i:04d}", "UP_DOWN")
    for i in range(n_ou):
        add(f"0xou{i:04d}", "OVER_UNDER")
    for i in range(n_no):
        add(f"0xno{i:04d}", "NAMED_OTHER")
    return contract, rows, trades, first_ts


def _cfg(**kw):
    base = dict(root="R", artifacts_dir="A", sample_size=12, seed=1,
                interval="max", fidelity=None, allow_batch=False, network_authorized=True,
                quiet=True, progress_every=25)  # quiet by default: dedicated progress tests opt in
    base.update(kw)
    return s1.RunConfig(**base)


# ---------------------------------------------------------------------------
# No artifacts written without explicit network authorization
# ---------------------------------------------------------------------------
def test_run_without_network_auth_writes_nothing():
    contract, rows, trades, first_ts = _universe_fixture()
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(network_authorized=False), loader, client, writer)
    assert result["s1_verdict"] == s1.STOP_NOT_AUTHORIZED
    assert result["wrote_artifacts"] is False
    assert writer.written == {}                 # nothing written
    assert client.get_calls == []               # nothing fetched


# ---------------------------------------------------------------------------
# Authorized mocked run writes ALL FIVE expected artifacts
# ---------------------------------------------------------------------------
def test_authorized_run_writes_all_five_artifacts():
    contract, rows, trades, first_ts = _universe_fixture()
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()  # default: both sides present with an in-window point
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=12), loader, client, writer)
    assert result["wrote_artifacts"] is True
    assert set(writer.written.keys()) == set(s1.S1_ARTIFACT_FILENAMES)
    assert result["artifact_dir"] == writer.s1_dir()


def test_authorized_run_calls_injected_abstractions_only():
    contract, rows, trades, first_ts = _universe_fixture()
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=9), loader, client, writer)
    # loader was asked for trades of exactly the universe cids
    assert loader.trades_requested_for is not None
    # client.get was called (2 tokens per sampled condition); batch not called (disabled)
    assert len(client.get_calls) > 0
    assert client.batch_calls == []


# ---------------------------------------------------------------------------
# Run only samples Pass 1, never the full universe
# ---------------------------------------------------------------------------
def test_run_samples_pass1_never_full_universe():
    contract, rows, trades, first_ts = _universe_fixture(n_up=200, n_ou=40, n_no=120)  # 360 total
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    cfg = _cfg(sample_size=30)
    result = s1.run_pass1_coverage(cfg, loader, client, writer)
    assert result["sample_size_actual"] <= 30
    assert result["sample_size_actual"] < result["universe_resolved_pairs"]  # strict subset
    assert result["sampled_only"] is True
    # Exactly 2 fetches per sampled condition, and never more than 2*sample_size.
    assert result["fetched_token_count"] == 2 * result["sample_size_actual"]
    assert len(client.get_calls) == 2 * result["sample_size_actual"]
    assert len(client.get_calls) <= 2 * cfg.sample_size


def test_run_fetches_both_side_tokens_per_condition():
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=6), loader, client, writer)
    fetched = {c[0] for c in client.get_calls}
    # every sampled condition contributes its two distinct side tokens
    assert len(fetched) == 2 * result["sample_size_actual"]


# ---------------------------------------------------------------------------
# Pass 2 remains unavailable (even from the orchestration path)
# ---------------------------------------------------------------------------
def test_pass2_unavailable_from_orchestration_result():
    contract, rows, trades, first_ts = _universe_fixture()
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(_cfg(), loader, FakeClient(), FakeWriter())
    assert result["pass2_available"] is False
    with pytest.raises(s1.Pass2NotAvailable):
        s1.run_pass2()


# ---------------------------------------------------------------------------
# Stop propagation: P0 not clear / stale contract halt the run, write nothing
# ---------------------------------------------------------------------------
def test_run_p0_not_clear_halts_and_writes_nothing():
    bad = _p0_clear()
    bad["p0_state"] = "STOP_DATA_GATE_NOT_CLEAR"
    loader = FakeLoader(p0=bad)
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(), loader, FakeClient(), writer)
    assert result["s1_verdict"] == s1.STOP_P0_NOT_CLEAR
    assert result["wrote_artifacts"] is False
    assert writer.written == {}


def test_run_stale_contract_halts():
    bad = _p0_clear()
    bad["nb_contract_version_resolution_source"] = "nb-contract-OLD.0"
    loader = FakeLoader(p0=bad)
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(), loader, FakeClient(), writer)
    assert result["s1_verdict"] == s1.STOP_STALE_CONTRACT
    assert writer.written == {}


# ---------------------------------------------------------------------------
# by-condition CSV carries no price values (coverage ledger only)
# ---------------------------------------------------------------------------
def test_by_condition_csv_has_no_price_values():
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=6), loader, FakeClient(), writer)
    csv_text = writer.written["price_source_s1_coverage_by_condition.csv"]
    header = csv_text.splitlines()[0].split(",")
    # No price-bearing columns.
    for banned in ("p", "price", "yes_price", "side_0_price", "side_1_price", "series"):
        assert banned not in header
    # Header is exactly the coverage-ledger schema.
    assert tuple(header) == s1.BY_CONDITION_HEADER


# ---------------------------------------------------------------------------
# Level B feeds the verdict; both-sides present -> VIABLE on this clean fixture
# ---------------------------------------------------------------------------
def test_clean_both_sides_fixture_is_viable():
    contract, rows, trades, first_ts = _universe_fixture(n_up=20, n_ou=6, n_no=12)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(_cfg(sample_size=30), loader, FakeClient(), FakeWriter())
    # every side present with an in-window point -> all subclasses clear
    assert result["s1_verdict"] == s1.S1_SOURCE_VIABLE
    for sub, v in result["per_subclass_coverage"].items():
        if v["measured"]:
            assert v["clears_threshold"] is True


# ---------------------------------------------------------------------------
# Empty-both-sides fixture -> NOT_VIABLE (systemic absence), still writes artifacts
# ---------------------------------------------------------------------------
def test_empty_series_fixture_is_not_viable_but_writes():
    contract, rows, trades, first_ts = _universe_fixture(n_up=20, n_ou=6, n_no=12)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    # All tokens return EMPTY series.
    client = FakeClient(default_status=s1.SERIES_EMPTY)
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=30), loader, client, writer)
    assert result["s1_verdict"] == s1.S1_SOURCE_NOT_VIABLE
    # Falsify cheaply, but still emit the coverage artifacts.
    assert set(writer.written.keys()) == set(s1.S1_ARTIFACT_FILENAMES)


# ---------------------------------------------------------------------------
# Batch path only when explicitly enabled; equivalence recorded
# ---------------------------------------------------------------------------
def test_batch_path_only_when_enabled():
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    s1.run_pass1_coverage(_cfg(sample_size=6, allow_batch=True), loader, client, FakeWriter())
    assert len(client.batch_calls) > 0  # batch used because enabled


def test_batch_disabled_by_default():
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    s1.run_pass1_coverage(_cfg(sample_size=6, allow_batch=False), loader, client, FakeWriter())
    assert client.batch_calls == []


# ---------------------------------------------------------------------------
# main() CLI: default is unauthorized (rc=2), no run object composed
# ---------------------------------------------------------------------------
def test_main_default_unauthorized(capsys):
    rc = s1.main(["--root", "R", "--artifacts-dir", "A"])
    out = capsys.readouterr().out
    assert rc == 2 and s1.STOP_NOT_AUTHORIZED in out


def test_build_run_config_reflects_auth_flags():
    parser = s1.build_arg_parser()
    args = parser.parse_args([
        "--i-authorize-s1-pass1-network-run",
        "--confirm-external-host", "clob.polymarket.com",
        "--sample-size", "50", "--allow-batch",
    ])
    cfg = s1.build_run_config(args)
    assert cfg.network_authorized is True
    assert cfg.sample_size == 50 and cfg.allow_batch is True


def test_real_writer_refuses_prices_path(tmp_path):
    # ArtifactWriter must never target a prices/ directory.
    w = s1.ArtifactWriter(str(tmp_path / "prices"))
    with pytest.raises(RuntimeError):
        w.write_text("x.txt", "data")


def test_real_writer_writes_under_s1_subpath(tmp_path):
    w = s1.ArtifactWriter(str(tmp_path))
    p = w.write_text("price_source_s1_coverage.md", "hello")
    assert p.endswith("named_binary_probe/price_source_s1/price_source_s1_coverage.md") \
        or p.endswith("named_binary_probe\\price_source_s1\\price_source_s1_coverage.md")
    assert "prices" not in p.replace("price_source", "").replace("prices_history", "")


# ===========================================================================
# Endpoint-shape capture tests (observed GET / batch facts + deviations).
# All mocked; no network.
# ===========================================================================

# ---- Pure helpers -------------------------------------------------------------
def test_observe_response_shape_get_facts():
    body = {"history": [{"t": 100, "p": 0.5, "token_id": TOK_A}, {"t": 200, "p": 0.6}]}
    facts = s1.observe_response_shape(200, body, TOK_A)
    assert facts["http_status"] == 200
    assert facts["series_key"] == "history"
    assert facts["point_count"] == 2
    assert facts["first_point_keys"] == sorted(["t", "p", "token_id"])
    assert facts["top_level_keys"] == ["history"]
    assert facts["level_a_status"] == s1.SERIES_PRESENT


def test_observe_response_shape_prices_key_variant():
    body = {"prices": [{"t": 1, "p": 0.4}]}
    facts = s1.observe_response_shape(200, body, TOK_A)
    assert facts["series_key"] == "prices"
    assert facts["point_count"] == 1


def test_observe_response_shape_records_deviation():
    facts = s1.observe_response_shape(200, {"unexpected": 1}, TOK_A)
    assert facts["level_a_status"] == s1.STOP_ENDPOINT_SHAPE_UNRECOGNIZED
    assert facts["note"]  # deviation note captured


def test_observe_response_shape_no_price_values_leaked():
    body = {"history": [{"t": 100, "p": 0.777, "token_id": TOK_A}]}
    facts = s1.observe_response_shape(200, body, TOK_A)
    # Only KEYS/counts are recorded; the price value 0.777 must not appear anywhere.
    import json
    blob = json.dumps(facts)
    assert "0.777" not in blob
    assert facts["first_point_keys"] == sorted(["t", "p", "token_id"])


def test_build_shape_observations_get_and_batch():
    sink = [
        {"context": "get", "path": "/prices-history",
         "payload_keys": ["endTs", "interval", "market", "startTs"],
         "payload": {"market": TOK_A, "startTs": 0, "endTs": 100, "interval": "max"},
         "http_status": 200,
         "body": {"history": [{"t": 10, "p": 0.5, "token_id": TOK_A}]}},
        {"context": "batch", "path": "/batch-prices-history",
         "payload_keys": ["end_ts", "interval", "markets", "start_ts"],
         "payload": {"markets": "<list:2>", "start_ts": 0, "end_ts": 100, "interval": "max"},
         "http_status": 200,
         "body": {"histories": {TOK_A: [{"t": 10, "p": 0.5}], TOK_B: []}}},
    ]
    obs = s1._build_shape_observations(sink)
    assert obs["get_observed"]["series_key"] == "history"
    assert obs["get_observed"]["params_used"] == ["endTs", "interval", "market", "startTs"]
    assert obs["get_observed"]["point_count"] == 1
    assert obs["batch_observed"]["histories_key_present"] is True
    assert obs["deviation"] is None


# ---- Full mocked run -> endpoint_shape.md content -----------------------------
def test_authorized_run_writes_get_shape_facts():
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()  # feeds shape_sink with synthetic documented-shape bodies
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=6), loader, client, writer)
    shape_md = writer.written["price_source_s1_endpoint_shape.md"]
    # Observed GET facts present in the shape file.
    assert "Single-token GET" in shape_md
    assert "/prices-history" in shape_md
    assert "detected series key: history" in shape_md
    assert "first point keys:" in shape_md
    assert "Level A status: SERIES_PRESENT" in shape_md
    # params used names the documented single-token params.
    assert "market" in shape_md and "startTs" in shape_md and "endTs" in shape_md
    # And the JSON result carries the structured observations too.
    assert result["endpoint_shape_observations"]["get_observed"]["series_key"] == "history"


def test_authorized_run_shape_md_has_no_price_values():
    contract, rows, trades, first_ts = _universe_fixture(n_up=4, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    # inject a distinctive price value; it must NOT appear in the shape file (keys/counts only).
    body = {TOK: {"history": [{"t": 111, "p": 0.98765, "token_id": TOK}]}
            for TOK in []}  # placeholder; real bodies come from synth
    client = FakeClient()
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=4), loader, client, writer)
    shape_md = writer.written["price_source_s1_endpoint_shape.md"]
    # The synthetic price is 0.5; ensure no bare price series is dumped (only 'p' as a KEY).
    assert "0.5," not in shape_md and "\"p\": 0.5" not in shape_md
    # by-condition ledger likewise carries no price value column.
    header = writer.written["price_source_s1_coverage_by_condition.csv"].splitlines()[0]
    assert "0.5" not in header


# ---- Batch shape + equivalence ------------------------------------------------
def test_allow_batch_writes_batch_shape_and_equivalence():
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()  # synth batch equals synth single -> equivalence True
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=6, allow_batch=True), loader, client, writer)
    shape_md = writer.written["price_source_s1_endpoint_shape.md"]
    assert "Batch POST" in shape_md
    assert "/batch-prices-history" in shape_md
    assert "histories key present: True" in shape_md
    assert result["batch_enabled"] is True
    assert result["batch_equivalence_all_ok"] is True
    assert result["endpoint_shape_observations"]["batch_observed"]["histories_key_present"] is True


def test_batch_shape_absent_when_disabled():
    contract, rows, trades, first_ts = _universe_fixture(n_up=4, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=4, allow_batch=False), loader, client, writer)
    shape_md = writer.written["price_source_s1_endpoint_shape.md"]
    assert "batch not exercised this run" in shape_md
    assert result["endpoint_shape_observations"]["batch_observed"] is None


# ---- Deviation surfaced -------------------------------------------------------
def test_get_deviation_surfaced_in_shape_md_and_stop_result():
    contract, rows, trades, first_ts = _universe_fixture(n_up=4, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    # Every token returns a body that does NOT match the documented shape.
    # body_by_token keyed by every side token we generate: use a catch-all via default.
    class DeviantClient(FakeClient):
        def _synth_body(self, token_id, start_ts):
            return {"unexpected_key": [1, 2, 3]}  # no history/prices -> EndpointShapeError
    client = DeviantClient()
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=4), loader, client, writer)
    # Stop verdict returned...
    assert result["s1_verdict"].startswith(s1.STOP_ENDPOINT_SHAPE_UNRECOGNIZED)
    # ...deviation surfaced in the returned result...
    assert result["endpoint_shape_observations"]["deviation"]
    # ...and best-effort written to the shape file.
    assert result.get("endpoint_shape_written") is True
    shape_md = writer.written.get("price_source_s1_endpoint_shape.md", "")
    assert "Deviation" in shape_md
    assert "unexpected_key" in shape_md or "no history/prices" in shape_md
    # No coverage JSON was written on a hard stop.
    assert "price_source_s1_coverage.json" not in writer.written


def test_batch_deviation_missing_histories_surfaced():
    contract, rows, trades, first_ts = _universe_fixture(n_up=4, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    # GET is fine, but batch returns a body without a histories key -> EndpointShapeError.
    client = FakeClient(batch_body={"wrong": {}})
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=4, allow_batch=True), loader, client, writer)
    assert result["s1_verdict"].startswith(s1.STOP_ENDPOINT_SHAPE_UNRECOGNIZED)
    # The deviation is recorded in the returned stop result...
    assert result["endpoint_shape_observations"]["deviation"]
    # ...and best-effort written into the shape MD so S2 review can see it.
    assert result.get("endpoint_shape_written") is True
    assert "price_source_s1_endpoint_shape.md" in writer.written
    dmd = writer.written["price_source_s1_endpoint_shape.md"]
    assert "### Deviation" in dmd
    assert "histories" in dmd  # the observed deviation mentions the missing key
    # On a stop, the coverage JSON must NOT be written.
    assert "price_source_s1_coverage.json" not in writer.written
    # The captured batch request facts are still present (path + payload keys).
    assert "/batch-prices-history" in dmd


# ---- JSON final-state fix -----------------------------------------------------
def test_coverage_json_reflects_final_wrote_artifacts_state():
    import json
    contract, rows, trades, first_ts = _universe_fixture(n_up=8, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=8), loader, client, writer)
    # The JSON artifact as written must already reflect wrote_artifacts + artifact_dir.
    written_json = json.loads(writer.written["price_source_s1_coverage.json"])
    assert written_json["wrote_artifacts"] is True
    assert written_json["artifact_dir"] == writer.s1_dir()
    assert written_json["endpoint_shape_observations"]["get_observed"]["series_key"] == "history"
    # Returned result agrees.
    assert result["wrote_artifacts"] is True


# ---- real client shape_sink capture (no network; direct map) ------------------
def test_real_client_populates_shape_sink_via_transport():
    sink = []
    client = s1.PricesHistoryClient(
        transport=lambda *a, **k: (200, {"history": [{"t": 1, "p": 0.5, "token_id": TOK_A}]}),
        shape_sink=sink,
    )
    client.get_prices_history(TOK_A, 0, 100, interval="max", fidelity=60)
    assert len(sink) == 1
    entry = sink[0]
    assert entry["context"] == "get"
    assert entry["path"] == "/prices-history"
    assert entry["payload_keys"] == sorted(["market", "startTs", "endTs", "interval", "fidelity"])
    assert entry["http_status"] == 200
    obs = s1._build_shape_observations(sink)
    assert obs["get_observed"]["series_key"] == "history"


# ===========================================================================
# parse_ts datetime-like patch (bug: pandas Timestamp from Store.load_trades()
# was rejected as "unparseable timestamp"). Timestamp-only fix; token-id / integer
# identity handling is unaffected (token ids never pass through parse_ts).
# ===========================================================================
def test_parse_ts_accepts_pandas_timestamp_utc():
    import pandas as pd
    ts = pd.Timestamp("2026-05-08 04:27:06+0000", tz="UTC")
    # 2026-05-08 04:27:06 UTC == epoch 1778214426
    assert s1.parse_ts(ts) == 1778214426.0


def test_parse_ts_accepts_python_datetime_with_tzinfo():
    from datetime import datetime, timezone
    dt = datetime(2026, 5, 8, 4, 27, 6, tzinfo=timezone.utc)
    assert s1.parse_ts(dt) == 1778214426.0


def test_parse_ts_naive_datetime_treated_as_utc():
    # tz-naive datetime must be treated as UTC (not the runner's local tz) so the
    # result is deterministic regardless of where the user runs it.
    from datetime import datetime, timezone
    naive = datetime(2026, 5, 8, 4, 27, 6)
    aware = datetime(2026, 5, 8, 4, 27, 6, tzinfo=timezone.utc)
    assert s1.parse_ts(naive) == s1.parse_ts(aware) == 1778214426.0


def test_parse_ts_naive_pandas_timestamp_treated_as_utc():
    import pandas as pd
    naive = pd.Timestamp("2026-05-08 04:27:06")  # no tz
    assert s1.parse_ts(naive) == 1778214426.0


def test_parse_ts_string_and_epoch_forms_preserved():
    # Existing behavior must be untouched by the datetime patch.
    assert s1.parse_ts("2025-03-06 00:00:00 UTC") == 1741219200.0
    assert s1.parse_ts("2025-03-06T00:00:00") == 1741219200.0
    assert s1.parse_ts("2025-03-06") == 1741219200.0
    assert s1.parse_ts(1778214426) == 1778214426.0
    assert s1.parse_ts("1778214426") == 1778214426.0
    assert s1.parse_ts(1778214426.5) == 1778214426.5


def test_parse_ts_still_fails_loud_on_garbage():
    with pytest.raises(ValueError):
        s1.parse_ts("not-a-timestamp")
    with pytest.raises(ValueError):
        s1.parse_ts(None)
    with pytest.raises(ValueError):
        s1.parse_ts(True)


def test_store_loader_load_trades_index_handles_pandas_timestamps(monkeypatch):
    """StoreLoader.load_trades_index must consume a trades dataframe whose traded_at
    values are pandas Timestamp objects (the real Store.load_trades() shape).

    Pure/mocked: we inject a fake pm_research.data.store.Store returning an in-memory
    dataframe. No network, no disk, no real Store. Exercises the real load_trades_index
    code path (groupby + astype(str) + parse_ts on Timestamps)."""
    import sys
    import types
    import pandas as pd

    # Two conditions, tz-aware pandas Timestamps (incl. the previously-failing value),
    # plus 78-digit string-safe token ids to confirm identity handling is untouched.
    tok0 = "111" + "0" * 74 + "10"
    tok1 = "222" + "0" * 74 + "20"
    df = pd.DataFrame({
        "condition_id": ["0xaaa", "0xaaa", "0xbbb"],
        "token_id": [tok0, tok1, tok0],
        "outcome_index": ["0", "1", "0"],
        "traded_at": [
            pd.Timestamp("2026-05-08 04:27:06+0000", tz="UTC"),   # the failing case
            pd.Timestamp("2026-05-08 05:00:00+0000", tz="UTC"),
            pd.Timestamp("2025-03-06 00:00:00+0000", tz="UTC"),
        ],
    })

    class _FakeStore:
        def __init__(self, root):
            self.root = root

        def load_trades(self):
            return df

    fake_mod = types.ModuleType("pm_research.data.store")
    fake_mod.Store = _FakeStore
    # Ensure the parent packages exist so `from pm_research.data.store import Store` resolves.
    for name in ("pm_research", "pm_research.data"):
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = []  # mark as package
            monkeypatch.setitem(sys.modules, name, pkg)
    monkeypatch.setitem(sys.modules, "pm_research.data.store", fake_mod)

    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    tuples, first_ts = loader.load_trades_index(["0xaaa", "0xbbb"])

    # Timestamps parsed to epoch; min() picked per condition.
    assert first_ts["0xaaa"] == 1778214426.0          # the min of the two 0xaaa rows
    assert first_ts["0xbbb"] == 1741219200.0
    # Token pairs preserved string-safe (identity untouched by the timestamp patch).
    assert ("0xaaa", tok0, "0") in tuples["0xaaa"]
    assert ("0xaaa", tok1, "1") in tuples["0xaaa"]
    # Enumeration still yields exactly two stable side tokens.
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples["0xaaa"])
    assert status == "OK" and {s0, s1_tok} == {tok0, tok1}
    assert malformed == 0


# ===========================================================================
# Token-pair enumeration: NaN / missing / malformed trade rows (bug: a real
# STOP_PRECISION_LOSS on "float token/index not string-safe: nan" fired during
# enumeration because a raw NaN reached canonical_int directly). Root cause:
# pandas 3.x's `.astype(str)` does NOT stringify NaN under the native string
# dtype - it leaves a raw Python float NaN in place - so the missing-value guard
# must live in enumerate_token_pair itself, not rely on upstream stringification.
# Missing/malformed rows are SKIPPED + COUNTED; real non-null float-mangled values
# must still STOP_PRECISION_LOSS.
# ===========================================================================
def test_enumerate_token_pair_ignores_nan_token_id_reports_malformed():
    tuples = [
        ("0xa", float("nan"), "0"),   # malformed: NaN token_id -> skipped, counted
        ("0xa", TOK_A, "0"),          # valid
        ("0xa", TOK_B, "1"),          # valid
    ]
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == "OK"
    assert (s0, s1_tok) == (TOK_A, TOK_B)
    assert malformed == 1


def test_enumerate_token_pair_ignores_nan_outcome_index_reports_malformed():
    tuples = [
        ("0xa", TOK_A, float("nan")),  # malformed: NaN outcome_index -> skipped, counted
        ("0xa", TOK_A, "0"),           # valid
        ("0xa", TOK_B, "1"),           # valid
    ]
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == "OK"
    assert (s0, s1_tok) == (TOK_A, TOK_B)
    assert malformed == 1


def test_enumerate_token_pair_resolves_despite_unrelated_malformed_rows():
    # A mix of every malformed form (NaN float, None, empty string, "nan"/"none" text)
    # interleaved with enough valid rows to still resolve exactly two side tokens.
    tuples = [
        ("0xa", float("nan"), "0"),
        ("0xa", None, "1"),
        ("0xa", TOK_A, None),
        ("0xa", TOK_B, ""),
        ("0xa", "  ", "1"),
        ("0xa", TOK_A, "0"),
        ("0xa", TOK_B, "1"),
    ]
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == "OK"
    assert (s0, s1_tok) == (TOK_A, TOK_B)
    assert malformed == 5


def test_enumerate_token_pair_only_malformed_rows_is_unresolved_not_stop():
    tuples = [
        ("0xa", float("nan"), "0"),
        ("0xa", None, "1"),
        ("0xa", TOK_A, float("nan")),
        ("0xa", "", "0"),
        ("0xa", "nan", "1"),
        ("0xa", "None", "0"),
    ]
    # Must NOT raise - a condition with only malformed/missing rows is TOKEN_PAIR_UNRESOLVED.
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples)
    assert status == s1.TOKEN_PAIR_UNRESOLVED
    assert s0 is None and s1_tok is None
    assert malformed == 6


def test_enumerate_token_pair_real_float_mangled_id_still_stops_amid_valid_rows():
    # A REAL non-null float-mangled token id (not NaN) must still STOP_PRECISION_LOSS,
    # even surrounded by otherwise-valid rows - precision loss is never downgraded to
    # a missing/malformed skip.
    tuples = [
        ("0xa", TOK_A, "0"),
        ("0xa", TOK_B, "1"),
        ("0xa", 5.20896e76, "0"),  # real float-mangled id, NOT NaN
    ]
    with pytest.raises(s1.DataExportPrecisionLoss):
        s1.enumerate_token_pair(tuples)


def test_enumerate_token_pair_scientific_notation_string_still_stops_amid_malformed():
    # Scientific-notation STRING token id amid missing rows: still a hard stop, not skipped.
    tuples = [
        ("0xa", None, "1"),
        ("0xa", "5.20896e+76", "0"),
        ("0xa", TOK_B, "1"),
    ]
    with pytest.raises(s1.DataExportPrecisionLoss):
        s1.enumerate_token_pair(tuples)


def test_enumerate_token_pair_never_reads_resolved_winning_token_id():
    # Guard-by-construction (unchanged by this patch): enumeration only ever consumes
    # (condition_id, token_id, outcome_index) trade tuples.
    import inspect
    src = inspect.getsource(s1.enumerate_token_pair)
    assert "resolved_winning_token_id" not in src
    assert "winning" not in src.lower()


def test_resolve_token_pairs_aggregates_malformed_rows_onto_condition_record():
    uni = [s1.ConditionRecord("0xa", "UP_DOWN", "2025-01-01 00:00:00 UTC")]
    trades = {
        "0xa": [
            ("0xa", float("nan"), "0"),
            ("0xa", TOK_A, "0"),
            ("0xa", TOK_B, "1"),
        ]
    }
    resolved, unresolved = s1.resolve_token_pairs(uni, trades)
    assert len(resolved) == 1 and len(unresolved) == 0
    assert resolved[0].malformed_trade_rows == 1
    assert resolved[0].pair_status == "OK"


def test_store_loader_load_trades_index_real_pandas_nan_end_to_end(monkeypatch):
    """End-to-end reproduction of the exact originally-reported failure mode: a pandas
    dataframe with a real np.nan in token_id (pandas 3.x: .astype(str) leaves it as a raw
    float, not the text "nan"). Must flow through StoreLoader -> enumerate_token_pair
    without raising, and the malformed row must be counted. No network, no real Store."""
    import sys
    import types
    import pandas as pd
    import numpy as np

    tok0 = "111" + "0" * 74 + "10"
    tok1 = "222" + "0" * 74 + "20"
    df = pd.DataFrame({
        "condition_id": ["0xaaa", "0xaaa", "0xaaa"],
        "token_id": [np.nan, tok0, tok1],           # real NaN, matches the original bug
        "outcome_index": ["0", "0", "1"],
        "traded_at": [
            pd.Timestamp("2026-05-08 04:00:00+0000", tz="UTC"),
            pd.Timestamp("2026-05-08 04:27:06+0000", tz="UTC"),
            pd.Timestamp("2026-05-08 05:00:00+0000", tz="UTC"),
        ],
    })

    class _FakeStore:
        def __init__(self, root):
            self.root = root

        def load_trades(self):
            return df

    fake_mod = types.ModuleType("pm_research.data.store")
    fake_mod.Store = _FakeStore
    for name in ("pm_research", "pm_research.data"):
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = []
            monkeypatch.setitem(sys.modules, name, pkg)
    monkeypatch.setitem(sys.modules, "pm_research.data.store", fake_mod)

    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    # Must not raise (this is the exact regression the bug report described).
    tuples, first_ts = loader.load_trades_index(["0xaaa"])
    s0, s1_tok, status, malformed = s1.enumerate_token_pair(tuples["0xaaa"])
    assert status == "OK"
    assert {s0, s1_tok} == {tok0, tok1}
    assert malformed == 1


def test_orchestration_reports_malformed_trade_rows_total_diagnostically():
    """Missing/malformed rows must be counted and reported diagnostically at the
    artifact level (JSON result), not just inside enumerate_token_pair."""
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    # Inject one malformed (NaN token_id) row into the first condition's trades, alongside
    # its existing valid pair, so it still resolves but contributes to the diagnostic count.
    first_cid = next(iter(trades))
    trades[first_cid] = list(trades[first_cid]) + [(first_cid, float("nan"), "0")]
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(_cfg(sample_size=6), loader, FakeClient(), FakeWriter())
    assert result["malformed_trade_rows_total"] >= 1


# ===========================================================================
# Progress / heartbeat (stderr only, flush=True, quiet toggle, --progress-every).
# ===========================================================================
def test_progress_appears_in_mocked_authorized_run_when_not_quiet(capsys):
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(
        _cfg(sample_size=6, quiet=False), loader, FakeClient(), FakeWriter()
    )
    captured = capsys.readouterr()
    err = captured.err
    # Progress goes to stderr, never stdout.
    assert captured.out == ""
    for marker in (
        "[S1] loading P0/contract/resolution/trades...",
        "[S1] universe built:",
        "[S1] token pairs resolved:",
        "[S1] sample selected:",
        "[S1] fetching coverage:",
        "[S1] writing artifacts...",
        f"[S1] done: verdict={result['s1_verdict']}",
    ):
        assert marker in err, f"missing progress marker: {marker!r}"
    # No price series / excessive token dumps in the heartbeat.
    assert "0.5" not in err  # no stray price-like float literal leaking into progress text


def test_progress_suppressed_when_quiet(capsys):
    contract, rows, trades, first_ts = _universe_fixture(n_up=6, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), FakeWriter())
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == ""


def test_progress_heartbeat_before_first_fetch_and_every_n(capsys):
    contract, rows, trades, first_ts = _universe_fixture(n_up=200, n_ou=0, n_no=0)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    s1.run_pass1_coverage(
        _cfg(sample_size=100, quiet=False, progress_every=25),
        loader, FakeClient(), FakeWriter(),
    )
    err = capsys.readouterr().err
    # "before the first fetch" -> a 0/N line must appear.
    assert "[S1] fetching coverage: 0/100 conditions" in err
    # periodic every 25 -> 25/100, 50/100, 75/100 should all appear.
    for n in (25, 50, 75):
        assert f"[S1] fetching coverage: {n}/100 conditions" in err
    # final tally line (new wording: valid-window fetched / skipped-invalid).
    assert "[S1] fetching coverage: 100/100 valid-window conditions fetched" in err


def test_progress_stop_path_still_prints_done_marker(capsys):
    # An early stop (P0 not clear) should still emit a done marker when not quiet.
    bad = _p0_clear()
    bad["p0_state"] = "STOP_DATA_GATE_NOT_CLEAR"
    loader = FakeLoader(p0=bad)
    result = s1.run_pass1_coverage(_cfg(quiet=False), loader, FakeClient(), FakeWriter())
    err = capsys.readouterr().err
    assert "[S1] loading P0/contract/resolution/trades..." in err
    assert f"[S1] done: verdict={result['s1_verdict']}" in err


def test_progress_default_is_on_for_real_cli_runs():
    parser = s1.build_arg_parser()
    args = parser.parse_args([])
    cfg = s1.build_run_config(args)
    assert cfg.quiet is False  # progress ON by default
    assert cfg.progress_every == 25


def test_cli_quiet_flag_and_progress_every_flag():
    parser = s1.build_arg_parser()
    args = parser.parse_args(["--quiet", "--progress-every", "10"])
    cfg = s1.build_run_config(args)
    assert cfg.quiet is True
    assert cfg.progress_every == 10


def test_fmt_elapsed_formats_hh_mm_ss():
    assert s1._fmt_elapsed(0) == "00:00:00"
    assert s1._fmt_elapsed(72) == "00:01:12"
    assert s1._fmt_elapsed(3661) == "01:01:01"


# ===========================================================================
# Request-window fix (bug: endpoint GET used a ~1-second window
# [first_trade_ts, first_trade_ts+1], returning SERIES_EMPTY for everything and a
# false S1_SOURCE_NOT_VIABLE). The request must span the FULL decision window:
#   startTs = floor(first_trade_ts + warmup_seconds)
#   endTs   = ceil(resolved_at)
# with the leakage-safe strict `< resolved_at` cut kept in Level B classification.
# ===========================================================================
_FT = "2025-03-01 00:00:00 UTC"     # first_trade_ts
_RA = "2025-03-06 00:00:00 UTC"     # resolved_at (5 days later)


def _window_fixture(n=6):
    """A universe of `n` UP_DOWN conditions with known ft/resolved_at, and a client we
    control per-test. Returns (contract, rows, trades, first_ts)."""
    return _universe_fixture(n_up=n, n_ou=0, n_no=0)


def test_decision_request_window_helper_floor_ceil():
    ft = s1.parse_ts(_FT)
    ra = s1.parse_ts(_RA) + 0.7  # fractional -> ceil must round up
    start, end = s1._decision_request_window(ft, ra)
    assert start == int(ft) + s1.WARMUP_SECONDS          # floor(ft + warmup)
    assert end == int(s1.parse_ts(_RA)) + 1              # ceil(resolved_at + 0.7)
    assert (end - start) > 1                             # NOT the 1-second bug window


def test_decision_request_window_no_resolved_at_is_degenerate_not_wide():
    ft = s1.parse_ts(_FT)
    start, end = s1._decision_request_window(ft, None)
    assert start == int(ft) + s1.WARMUP_SECONDS
    assert end == start + 1  # cannot bound; stays a non-usable diagnostic (Level B won't hit)


def test_decision_request_window_backwards_is_clamped_wellformed():
    start, end = s1._decision_request_window(2_000_000.0, 1000.0)  # lower >= upper
    assert end > start  # well-formed, never a backwards range


def test_get_receives_decision_window_not_one_second():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    s1.run_pass1_coverage(_cfg(sample_size=6), loader, client, FakeWriter())
    expected_start = int(s1.parse_ts(_FT)) + s1.WARMUP_SECONDS   # 1740790800
    expected_end = int(s1.parse_ts(_RA))                          # 1741219200 (ceil of exact sec)
    assert client.get_calls, "no GET calls recorded"
    for (_tok, start_ts, end_ts, _interval, _fid) in client.get_calls:
        assert start_ts == expected_start, f"startTs {start_ts} != decision lower {expected_start}"
        assert end_ts == expected_end, f"endTs {end_ts} != resolved_at bound {expected_end}"
        assert (end_ts - start_ts) > 1                            # wide, not the 1-second bug


def test_point_after_decision_ts_before_resolved_at_counts():
    contract, rows, trades, first_ts = _window_fixture(n=4)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    ft = s1.parse_ts(_FT)
    ra = s1.parse_ts(_RA)
    # Put a single in-window point per token: strictly after ft+warmup and before resolved_at.
    in_window_ts = ft + s1.WARMUP_SECONDS + 3600  # 1h into the decision window
    series = {}
    for cid, rowlist in trades.items():
        for (_c, tok, _oi) in rowlist:
            series[tok] = _series(tok, [(in_window_ts, 0.42)])
    client = FakeClient(series_by_token=series)
    result = s1.run_pass1_coverage(_cfg(sample_size=4), loader, client, FakeWriter())
    # Every condition has both sides with an in-window point -> BOTH_SIDES for UP_DOWN.
    assert result["level_b_class_counts"].get(s1.DECISION_PRICE_BOTH_SIDES, 0) >= 1
    # UP_DOWN-only fixture: UP_DOWN clears but OVER_UNDER/NAMED_OTHER are unmeasured, so the
    # pooled verdict is PARTIAL (VIABLE requires all three subclasses to clear, spec 7.2).
    assert result["s1_verdict"] == s1.S1_SOURCE_PARTIAL
    assert result["per_subclass_coverage"]["UP_DOWN"]["clears_threshold"] is True
    # sanity: the point is truly inside the leakage-safe window
    assert in_window_ts >= ft + s1.WARMUP_SECONDS and in_window_ts < ra


def test_point_at_or_after_resolved_at_does_not_count():
    contract, rows, trades, first_ts = _window_fixture(n=4)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    ra = s1.parse_ts(_RA)
    # Only points AT/AFTER resolved_at exist (leakage) -> must NOT count.
    series = {}
    for cid, rowlist in trades.items():
        for (_c, tok, _oi) in rowlist:
            series[tok] = _series(tok, [(ra, 0.5), (ra + 100, 0.6)])
    client = FakeClient(series_by_token=series)
    result = s1.run_pass1_coverage(_cfg(sample_size=4), loader, client, FakeWriter())
    # No in-window point anywhere -> NEITHER for every condition, NOT_VIABLE.
    assert result["level_b_class_counts"].get(s1.DECISION_PRICE_BOTH_SIDES, 0) == 0
    assert result["s1_verdict"] == s1.S1_SOURCE_NOT_VIABLE


def test_endpoint_shape_records_wide_request_params():
    contract, rows, trades, first_ts = _window_fixture(n=4)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=4, quiet=True), loader, FakeClient(), writer)
    shape_md = writer.written["price_source_s1_endpoint_shape.md"]
    expected_start = int(s1.parse_ts(_FT)) + s1.WARMUP_SECONDS
    expected_end = int(s1.parse_ts(_RA))
    # The observed GET params in the shape ledger must show the wide decision window.
    assert f"'startTs': {expected_start}" in shape_md
    assert f"'endTs': {expected_end}" in shape_md
    # And the Level A scope note must be present (labeling clarification).
    assert "queried decision window" in shape_md.lower() or "queried" in shape_md.lower()


def test_endpoint_shape_notes_level_a_scope():
    # Level A is labeled as the queried-decision-window response, not "series exists at all".
    contract, rows, trades, first_ts = _window_fixture(n=3)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=3, quiet=True), loader, FakeClient(), writer)
    shape_md = writer.written["price_source_s1_endpoint_shape.md"]
    assert "Level A scope note" in shape_md
    assert "decision window" in shape_md


# ===========================================================================
# Request-window DIAGNOSTICS (this patch): prove the by-condition CSV and the
# JSON/MD summary expose the queried window so a single 1-second observed GET can
# never be mistaken for the whole sample, and the ledger matches the actual calls.
# ===========================================================================
def _csv_rows(writer, filename="price_source_s1_coverage_by_condition.csv"):
    import csv
    import io
    return list(csv.reader(io.StringIO(writer.written[filename])))


def test_by_condition_csv_has_request_window_columns():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), writer)
    header = _csv_rows(writer)[0]
    for col in (
        "first_trade_ts", "decision_lower_ts", "resolved_at_ts",
        "request_start_ts", "request_end_ts", "request_window_seconds",
        "observed_point_count_side_0", "observed_point_count_side_1",
    ):
        assert col in header, f"missing request-window column: {col}"
    # No price value column was introduced.
    for banned in ("p", "price", "yes_price", "side_0_price", "side_1_price", "series"):
        assert banned not in header


def test_by_condition_csv_window_values_are_consistent():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), writer)
    rows_out = _csv_rows(writer)
    h = rows_out[0]
    i_ft = h.index("first_trade_ts")
    i_lo = h.index("decision_lower_ts")
    i_ra = h.index("resolved_at_ts")
    i_s = h.index("request_start_ts")
    i_e = h.index("request_end_ts")
    i_w = h.index("request_window_seconds")
    ft = int(s1.parse_ts(_FT))
    ra = int(s1.parse_ts(_RA))
    for row in rows_out[1:]:
        assert int(row[i_ft]) == ft
        assert int(row[i_lo]) == ft + s1.WARMUP_SECONDS           # decision_lower = ft + warmup
        assert int(row[i_ra]) == ra
        assert int(row[i_s]) == ft + s1.WARMUP_SECONDS            # request_start = floor(lower)
        assert int(row[i_e]) == ra                               # request_end = ceil(resolved_at)
        assert int(row[i_w]) == int(row[i_e]) - int(row[i_s])    # window == end - start
        assert int(row[i_w]) > 1                                 # NOT the 1-second bug


def test_by_condition_csv_window_matches_actual_client_calls():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, client, writer)
    rows_out = _csv_rows(writer)
    h = rows_out[0]
    i_s = h.index("request_start_ts")
    i_e = h.index("request_end_ts")
    csv_windows = {(int(r[i_s]), int(r[i_e])) for r in rows_out[1:]}
    call_windows = {(s, e) for (_tok, s, e, _i, _f) in client.get_calls}
    # Every window recorded in the ledger corresponds to a window actually sent to the client.
    assert csv_windows == call_windows


def test_json_has_request_window_summary():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), FakeWriter())
    rw = result["request_window_summary"]
    for k in (
        "min_request_window_seconds", "median_request_window_seconds",
        "max_request_window_seconds", "count_request_window_seconds_le_1",
        "count_request_window_seconds_le_60", "count_request_window_seconds_gt_3600",
        "sample_count_by_subclass",
    ):
        assert k in rw, f"missing summary key: {k}"
    # Wide windows on this fixture: none <= 1s, all > 3600s.
    assert rw["count_request_window_seconds_le_1"] == 0
    assert rw["count_request_window_seconds_gt_3600"] == rw["n"]
    assert rw["min_request_window_seconds"] > 3600
    assert rw["sample_count_by_subclass"].get("UP_DOWN") == 6


def test_md_contains_request_window_summary():
    contract, rows, trades, first_ts = _window_fixture(n=4)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=4, quiet=True), loader, FakeClient(), writer)
    md = writer.written["price_source_s1_coverage.md"]
    assert "Request-window summary" in md
    assert "min_request_window_seconds" in md


def test_endpoint_shape_marks_get_as_one_sample_and_includes_summary():
    contract, rows, trades, first_ts = _window_fixture(n=4)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    s1.run_pass1_coverage(_cfg(sample_size=4, quiet=True), loader, FakeClient(), writer)
    smd = writer.written["price_source_s1_endpoint_shape.md"]
    assert "ONE SAMPLE ONLY" in smd
    assert "Request-window summary (whole sample)" in smd
    # The whole-sample distribution appears so a 1-second example can't be over-read.
    assert "count_request_window_seconds_le_1" in smd


def test_one_second_first_get_does_not_imply_all_windows_one_second():
    """Regression guard for the exact failure mode in the uploaded artifacts: even if ONE
    condition has a missing/invalid decision window, it must be EXCLUDED (not fetched, not
    counted as a 1-second window in the coverage summary), while the remaining valid conditions
    are fetched with wide windows. A single observed GET must not be read as the whole sample."""
    contract, rows, trades, first_ts = _window_fixture(n=6)
    # Make exactly ONE condition degenerate: blank its resolved_at -> invalid decision window.
    first_cid = rows[0]["condition_id"]
    for row in rows:
        if row["condition_id"] == first_cid:
            row["resolved_at"] = ""  # unparseable -> _safe_resolved_at None -> INVALID window
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), writer)
    # The invalid-window condition is excluded, NOT fetched, NOT a 1-second coverage window.
    dwv = result["decision_window_validity"]
    assert dwv["invalid_window"] == 1
    assert dwv["valid_window"] == 5
    # The request-window summary is over FETCHED (valid) conditions only -> all wide, none <=1s.
    rw = result["request_window_summary"]
    assert rw["count_request_window_seconds_le_1"] == 0
    assert rw["min_request_window_seconds"] > 3600
    assert rw["n"] == 5
    # by-condition ledger: the excluded condition is present with NO_VALID_DECISION_WINDOW and a
    # blank request window; the fetched ones carry wide windows (a MIX of row types, not all-one).
    rows_out = _csv_rows(writer)
    h = rows_out[0]
    i_w = h.index("request_window_seconds")
    i_lb = h.index("level_b_class")
    fetched_widths = {int(r[i_w]) for r in rows_out[1:] if r[i_w] != ""}
    invalid_rows = [r for r in rows_out[1:] if r[i_lb] == s1.NO_VALID_DECISION_WINDOW]
    assert len(invalid_rows) == 1
    assert all(w > 3600 for w in fetched_widths)
    assert fetched_widths, "expected fetched valid-window rows with wide windows"


def test_request_window_summary_empty_is_safe():
    # Degenerate: empty sample -> summary is well-formed with None/zero fields, no crash.
    rw = s1.request_window_summary([], [])
    assert rw["n"] == 0
    assert rw["min_request_window_seconds"] is None
    assert rw["count_request_window_seconds_le_1"] == 0


# ===========================================================================
# Invalid / missing decision window handling (this patch). Root cause of the
# uploaded all-1-second / all-NEITHER / false-NOT_VIABLE run: sampled conditions
# had resolved_at missing (or <= first_trade_ts+warmup), so there was NO valid
# ex-ante decision window. Such conditions must be EXCLUDED + reported, never
# fetched, never classified DECISION_PRICE_NEITHER, and an all-invalid sample must
# return a typed inconclusive verdict - not S1_SOURCE_NOT_VIABLE.
# ===========================================================================
def _blank_all_resolved_at(rows):
    for row in rows:
        row["resolved_at"] = ""   # -> _safe_resolved_at None -> invalid decision window
    return rows


def test_valid_decision_window_helper():
    ft = 1_000_000.0
    # valid: resolved_at strictly after ft + warmup
    assert s1.valid_decision_window(ft, ft + s1.WARMUP_SECONDS + 1) is True
    # invalid: resolved_at exactly at the lower bound (not strictly after)
    assert s1.valid_decision_window(ft, ft + s1.WARMUP_SECONDS) is False
    # invalid: resolved_at before the lower bound
    assert s1.valid_decision_window(ft, ft + 100) is False
    # invalid: missing resolved_at
    assert s1.valid_decision_window(ft, None) is False
    # invalid: missing first_trade_ts
    assert s1.valid_decision_window(None, ft + 10_000) is False


def test_invalid_window_condition_is_not_fetched():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    _blank_all_resolved_at(rows)  # every sampled condition -> invalid window
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, client, FakeWriter())
    # No GET calls at all - invalid-window conditions are skipped before any fetch.
    assert client.get_calls == []


def test_invalid_window_is_excluded_not_neither():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    _blank_all_resolved_at(rows)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), writer)
    # Never classified DECISION_PRICE_NEITHER.
    assert result["level_b_class_counts"].get(s1.DECISION_PRICE_NEITHER, 0) == 0
    # Reported as invalid-window in the by-condition ledger and the excluded ledger.
    by_cond = _csv_rows(writer)
    h = by_cond[0]
    i_lb = h.index("level_b_class")
    assert all(r[i_lb] == s1.NO_VALID_DECISION_WINDOW for r in by_cond[1:])
    excluded = _csv_rows(writer, "price_source_s1_excluded.csv")
    reasons = " ".join(r[2] for r in excluded[1:])
    assert s1.NO_VALID_DECISION_WINDOW in reasons
    # Excluded ledger carries the window diagnostics.
    assert "first_trade_ts=" in reasons and "decision_lower_ts=" in reasons


def test_all_invalid_sample_returns_inconclusive_not_not_viable():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    _blank_all_resolved_at(rows)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), FakeWriter())
    assert result["s1_verdict"] == s1.S1_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE
    assert result["s1_verdict"] != s1.S1_SOURCE_NOT_VIABLE
    dwv = result["decision_window_validity"]
    assert dwv["valid_window"] == 0
    assert dwv["invalid_window"] == 6


def test_mixed_valid_invalid_sample_fetches_only_valid_and_reconciles():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    # Blank resolved_at on exactly THREE of the six conditions -> invalid; leave three valid.
    invalid_cids = {rows[0]["condition_id"], rows[1]["condition_id"], rows[2]["condition_id"]}
    for row in rows:
        if row["condition_id"] in invalid_cids:
            row["resolved_at"] = ""
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    client = FakeClient()
    writer = FakeWriter()
    result = s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, client, writer)
    dwv = result["decision_window_validity"]
    assert dwv["valid_window"] == 3 and dwv["invalid_window"] == 3
    # Only the 3 valid conditions were fetched: 2 tokens each = 6 GET calls.
    assert len(client.get_calls) == 6
    assert result["fetched_token_count"] == 6
    # Reconciliation: by-condition rows == full sample (valid measured + invalid reported).
    by_cond = _csv_rows(writer)
    assert len(by_cond) - 1 == 6  # header + 6 rows
    # request-window summary covers only the 3 fetched (valid) conditions.
    assert result["request_window_summary"]["n"] == 3
    # Excluded ledger has the 3 invalid-window conditions.
    excluded = _csv_rows(writer, "price_source_s1_excluded.csv")
    n_invalid_excluded = sum(1 for r in excluded[1:] if s1.NO_VALID_DECISION_WINDOW in r[2])
    assert n_invalid_excluded == 3


def test_mixed_sample_measures_coverage_on_valid_only():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    invalid_cids = {rows[0]["condition_id"], rows[1]["condition_id"], rows[2]["condition_id"]}
    for row in rows:
        if row["condition_id"] in invalid_cids:
            row["resolved_at"] = ""
    ft = s1.parse_ts(_FT)
    # Give the valid conditions an in-window point on both sides.
    in_window_ts = ft + s1.WARMUP_SECONDS + 3600
    series = {}
    for cid, rowlist in trades.items():
        if cid in invalid_cids:
            continue
        for (_c, tok, _oi) in rowlist:
            series[tok] = _series(tok, [(in_window_ts, 0.4)])
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(
        _cfg(sample_size=6, quiet=True), loader, FakeClient(series_by_token=series), FakeWriter()
    )
    # UP_DOWN measured over the 3 valid conditions only (all BOTH_SIDES) -> clears.
    up = result["per_subclass_coverage"]["UP_DOWN"]
    assert up["measured"] == 3
    assert up["both_sides"] == 3
    assert up["clears_threshold"] is True
    # Per-subclass valid-window counts are reported.
    assert result["decision_window_validity"]["valid_window_by_subclass"].get("UP_DOWN") == 3


def test_invalid_window_json_reports_validity_counts():
    contract, rows, trades, first_ts = _window_fixture(n=6)
    _blank_all_resolved_at(rows)
    loader = FakeLoader(contract=contract, rows=rows, trades=trades, first_ts=first_ts)
    result = s1.run_pass1_coverage(_cfg(sample_size=6, quiet=True), loader, FakeClient(), FakeWriter())
    dwv = result["decision_window_validity"]
    for k in ("sampled", "valid_window", "invalid_window",
              "valid_window_by_subclass", "invalid_window_by_subclass"):
        assert k in dwv
    assert dwv["sampled"] == 6


# ===========================================================================
# resolved_at loader diagnosis (S1 blocker). Root-cause candidate proven in the
# sandbox: a blanket df.astype(str) in load_resolution_rows turns a tz-aware
# datetime64 `resolved_at` into "2025-03-06 00:00:00+00:00", which parse_ts rejects
# -> None -> blank -> the false all-invalid-window sample. The fix keeps identity
# columns string-safe but carries resolved_at as the raw pandas value (parse_ts's
# datetime branch handles it), fails loud if the column is absent, and maps NaT->None.
# ===========================================================================
def _mock_resolution_df(resolved_at_values, monkeypatch, m=s1):
    """Build a mocked resolution-source dataframe and monkeypatch pd.read_parquet so
    StoreLoader.load_resolution_rows reads it. Pure; no disk, no parquet file."""
    import pandas as pd
    n = len(resolved_at_values)
    df = pd.DataFrame({
        "condition_id": [f"0x{i:040x}" for i in range(n)],
        "subclass": ["UP_DOWN"] * n,
        "resolved_winning_token_id": ["111" + "0" * 74 + "10"] * n,
        "resolved_winning_outcome_index": ["0"] * n,
        "resolved_winning_label": ["W"] * n,
        "resolved_at": resolved_at_values,
        "source_table": ["polymarket_polygon.ctf_evt_conditionresolution"] * n,
        "status": ["RESOLVED_SINGLE_WINNER"] * n,
        "nb_contract_version": [m.NB_CONTRACT_VERSION] * n,
    })
    monkeypatch.setattr(pd, "read_parquet", lambda *a, **k: df.copy())
    return df


def test_load_resolution_rows_tz_aware_timestamp_parses(monkeypatch):
    import pandas as pd
    _mock_resolution_df([pd.Timestamp("2025-03-06 00:00:00+00:00")], monkeypatch)
    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    rows = loader.load_resolution_rows()
    ra = rows[0]["resolved_at"]
    # resolved_at is NOT the unparseable "...+00:00" string; parse_ts resolves it.
    assert s1.parse_ts(ra) == 1741219200.0
    # identity columns are still string-safe (not mangled by the timestamp handling).
    assert isinstance(rows[0]["resolved_winning_token_id"], str)
    assert rows[0]["resolved_winning_outcome_index"] == "0"


def test_load_resolution_rows_string_form_still_parses(monkeypatch):
    _mock_resolution_df(["2025-03-06 00:00:00 UTC"], monkeypatch)
    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    rows = loader.load_resolution_rows()
    assert s1.parse_ts(rows[0]["resolved_at"]) == 1741219200.0


def test_load_resolution_rows_nat_becomes_none(monkeypatch):
    import pandas as pd
    _mock_resolution_df([pd.NaT], monkeypatch)
    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    rows = loader.load_resolution_rows()
    # NaT -> None so _safe_resolved_at cleanly yields None (invalid window), never "NaT" text.
    assert rows[0]["resolved_at"] is None
    assert s1._safe_resolved_at(rows[0]["resolved_at"]) is None


def test_load_resolution_rows_missing_column_fails_loud(monkeypatch):
    import pandas as pd
    df = pd.DataFrame({
        "condition_id": ["0xaaa"],
        "subclass": ["UP_DOWN"],
        # resolved_at intentionally ABSENT; a block-time column present instead.
        "evt_block_time": [pd.Timestamp("2025-03-06 00:00:00+00:00")],
        "status": ["RESOLVED_SINGLE_WINNER"],
        "nb_contract_version": [s1.NB_CONTRACT_VERSION],
    })
    monkeypatch.setattr(pd, "read_parquet", lambda *a, **k: df.copy())
    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    with pytest.raises(ValueError) as e:
        loader.load_resolution_rows()
    msg = str(e.value)
    assert "STOP_RESOLUTION_SCHEMA" in msg
    assert "resolved_at" in msg
    # The error surfaces the actual columns so the user can spot a renamed field.
    assert "evt_block_time" in msg


def test_end_to_end_tz_aware_resolved_at_yields_valid_windows(monkeypatch):
    """The exact fix path end-to-end: tz-aware resolved_at that previously blanked now
    produces valid decision windows (given a first_trade_ts well before resolution)."""
    import pandas as pd
    import sys
    import types

    # resolution rows: 3 UP_DOWN conditions, tz-aware resolved_at 5 days after first trade.
    ra = pd.Timestamp("2025-03-06 00:00:00+00:00")
    _mock_resolution_df([ra, ra, ra], monkeypatch)

    # matching contract conditions + trades via a fake Store; first_trade_ts 5 days earlier.
    ft = pd.Timestamp("2025-03-01 00:00:00+00:00")
    cids = [f"0x{i:040x}" for i in range(3)]
    contract = [
        {"condition_id": c, "nb_subclass": "UP_DOWN", "nb_eligible": "True",
         "nb_contract_version": s1.NB_CONTRACT_VERSION, "exclusion_reason": "None"}
        for c in cids
    ]
    tok0 = "111" + "0" * 74 + "10"
    tok1 = "222" + "0" * 74 + "20"
    trade_rows = []
    for c in cids:
        trade_rows += [
            {"condition_id": c, "token_id": tok0, "outcome_index": "0", "traded_at": ft},
            {"condition_id": c, "token_id": tok1, "outcome_index": "1", "traded_at": ft},
        ]
    trades_df = pd.DataFrame(trade_rows)

    class _FakeStore:
        def __init__(self, root): pass
        def load_trades(self): return trades_df

    fake_mod = types.ModuleType("pm_research.data.store")
    fake_mod.Store = _FakeStore
    for name in ("pm_research", "pm_research.data"):
        if name not in sys.modules:
            pkg = types.ModuleType(name); pkg.__path__ = []
            monkeypatch.setitem(sys.modules, name, pkg)
    monkeypatch.setitem(sys.modules, "pm_research.data.store", fake_mod)

    # Contract loader also reads JSON; monkeypatch StoreLoader.load_contract_conditions.
    monkeypatch.setattr(s1.StoreLoader, "load_contract_conditions", lambda self: contract)
    # P0 preflight: patch to a clear state.
    monkeypatch.setattr(s1.StoreLoader, "load_p0_preflight", lambda self: _p0_clear())

    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    cfg = s1.RunConfig(root="R", artifacts_dir="A", sample_size=3, seed=1,
                       network_authorized=True, quiet=True)
    result = s1.run_pass1_coverage(cfg, loader, FakeClient(), FakeWriter())
    # With resolved_at now parsing, all 3 conditions have VALID windows (were invalid before).
    assert result["decision_window_validity"]["valid_window"] == 3
    assert result["decision_window_validity"]["invalid_window"] == 0
    assert result["s1_verdict"] != s1.S1_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE


# ===========================================================================
# parse_ts: real resolution-source format (user inspection: resolved_at is a
# populated str like "2025-03-06 07:25:37.000 UTC" - millisecond precision +
# " UTC" suffix). This fractional-seconds form was the actual S1 blocker.
# ===========================================================================
def test_parse_ts_accepts_millisecond_utc_string():
    # 2025-03-06 07:25:37 UTC == epoch 1741245937; ".000" adds nothing.
    assert s1.parse_ts("2025-03-06 07:25:37.000 UTC") == 1741245937.0


def test_parse_ts_accepts_whole_second_utc_string():
    assert s1.parse_ts("2025-03-06 07:25:37 UTC") == 1741245937.0


def test_parse_ts_millisecond_fraction_is_honored():
    # ".500" must add half a second (fraction parsed, not dropped).
    base = s1.parse_ts("2025-03-06 07:25:37 UTC")
    assert s1.parse_ts("2025-03-06 07:25:37.500 UTC") == base + 0.5


def test_parse_ts_preserves_prior_formats():
    # ISO, ISO-fractional, date-only, epoch numeric, and pandas/py datetime still work.
    from datetime import datetime, timezone
    assert s1.parse_ts("2025-03-06T00:00:00") == 1741219200.0
    assert s1.parse_ts("2025-03-06T00:00:00.250") == 1741219200.25
    assert s1.parse_ts("2025-03-06") == 1741219200.0
    assert s1.parse_ts(1741245937) == 1741245937.0
    assert s1.parse_ts("1741245937") == 1741245937.0
    assert s1.parse_ts(datetime(2025, 3, 6, 0, 0, 0, tzinfo=timezone.utc)) == 1741219200.0


def test_parse_ts_still_fails_loud_on_garbage_after_fix():
    with pytest.raises(ValueError):
        s1.parse_ts("2025-03-06 07:25:37.000 PST")   # non-UTC tz text not silently accepted
    with pytest.raises(ValueError):
        s1.parse_ts("not-a-timestamp")


def test_millisecond_utc_resolved_at_yields_valid_window(monkeypatch):
    """End-to-end: a condition whose resolved_at is in the real millisecond-UTC string
    form, with first_trade_ts earlier, must have a VALID decision window (was invalid
    before this fix). Pure/mocked - no parquet, no network."""
    import pandas as pd
    import sys
    import types

    cid = "0x" + "a" * 40
    # resolved_at in the exact real format, ~5 days after first trade.
    _mock_resolution_df(["2025-03-06 07:25:37.000 UTC"], monkeypatch)
    # But _mock_resolution_df generates its own cid; align contract/trades to it.
    # Rebuild deterministically so cids match across contract/resolution/trades.
    import importlib
    ra_val = "2025-03-06 07:25:37.000 UTC"
    df = pd.DataFrame({
        "condition_id": [cid],
        "subclass": ["UP_DOWN"],
        "resolved_winning_token_id": ["111" + "0" * 74 + "10"],
        "resolved_winning_outcome_index": ["0"],
        "resolved_winning_label": ["W"],
        "resolved_at": [ra_val],
        "source_table": ["polymarket_polygon.ctf_evt_conditionresolution"],
        "status": ["RESOLVED_SINGLE_WINNER"],
        "nb_contract_version": [s1.NB_CONTRACT_VERSION],
    })
    monkeypatch.setattr(pd, "read_parquet", lambda *a, **k: df.copy())

    tok0 = "111" + "0" * 74 + "10"
    tok1 = "222" + "0" * 74 + "20"
    ft = "2025-03-01 00:00:00.000 UTC"  # earlier than resolved_at, same real format
    trades_df = pd.DataFrame([
        {"condition_id": cid, "token_id": tok0, "outcome_index": "0", "traded_at": ft},
        {"condition_id": cid, "token_id": tok1, "outcome_index": "1", "traded_at": ft},
    ])

    class _FakeStore:
        def __init__(self, root): pass
        def load_trades(self): return trades_df

    fake_mod = types.ModuleType("pm_research.data.store")
    fake_mod.Store = _FakeStore
    for name in ("pm_research", "pm_research.data"):
        if name not in sys.modules:
            pkg = types.ModuleType(name); pkg.__path__ = []
            monkeypatch.setitem(sys.modules, name, pkg)
    monkeypatch.setitem(sys.modules, "pm_research.data.store", fake_mod)

    contract = [{"condition_id": cid, "nb_subclass": "UP_DOWN", "nb_eligible": "True",
                 "nb_contract_version": s1.NB_CONTRACT_VERSION, "exclusion_reason": "None"}]
    monkeypatch.setattr(s1.StoreLoader, "load_contract_conditions", lambda self: contract)
    monkeypatch.setattr(s1.StoreLoader, "load_p0_preflight", lambda self: _p0_clear())

    loader = s1.StoreLoader(root="R", artifacts_dir="A")
    cfg = s1.RunConfig(root="R", artifacts_dir="A", sample_size=1, seed=1,
                       network_authorized=True, quiet=True)
    result = s1.run_pass1_coverage(cfg, loader, FakeClient(), FakeWriter())
    assert result["decision_window_validity"]["valid_window"] == 1
    assert result["decision_window_validity"]["invalid_window"] == 0
    assert result["s1_verdict"] != s1.S1_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE
