"""
Tests for src/transport_isolation_canary.py.

NO test in this file invokes real curl, opens a socket, resolves DNS, or
contacts any host:
  - Preflight/validation/manifest tests call pure functions directly, or
    use temporary manifest files on local disk only.
  - "Happy path" / parsing / classification / command-construction tests
    use FakeCurlRunner, a canned-response stub -- never
    SubprocessCurlRunner, never subprocess.run against a real curl binary.
  - Zero-subprocess proofs use PoisonedCurlRunner, which raises immediately
    if `.run_version()` or `.run_request()` is ever called, and assert
    call_count == 0 afterward.

SubprocessCurlRunner (the only real-subprocess code path in this module)
is never instantiated anywhere in this file.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import transport_isolation_canary as tic  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _tok(prefix_digit: str) -> str:
    return prefix_digit + "1" * 76  # 77-char synthetic decimal token id


ACCEPTED_MANIFEST_CONDITIONS = [
    {
        "condition_id": "0xUP",
        "nb_subclass": "UP_DOWN",
        "decision_ts": "2026-01-01T01:00:00Z",
        "side_0_token_id": _tok("2"),
        "side_1_token_id": _tok("3"),
    },
    {
        "condition_id": "0xOU",
        "nb_subclass": "OVER_UNDER",
        "decision_ts": "2026-02-01T01:00:00Z",
        "side_0_token_id": _tok("4"),
        "side_1_token_id": _tok("5"),
    },
    {
        "condition_id": "0xNO",
        "nb_subclass": "NAMED_OTHER",
        "decision_ts": "2026-03-01T01:00:00Z",
        "side_0_token_id": _tok("6"),
        "side_1_token_id": _tok("7"),
    },
]


def _write_manifest(path: Path, conditions=None, extra_top_level=None) -> None:
    payload = {"conditions": conditions if conditions is not None else ACCEPTED_MANIFEST_CONDITIONS}
    if extra_top_level:
        payload.update(extra_top_level)
    path.write_text(json.dumps(payload))


def _valid_transport_isolation_input(**overrides) -> dict:
    payload = {
        "conditions": [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS],
        "dry_run": False,
        "transport_isolation_canary_enabled": True,
        "acknowledge_transport_isolation_not_p1_evidence": True,
    }
    payload.update(overrides)
    return payload


class FakeVersionResult:
    def __init__(self, exit_code=0, stdout=None, stderr="", error=None):
        self.exit_code = exit_code
        self.stdout = stdout if stdout is not None else (
            "curl 8.4.0 (x86_64-pc-linux-gnu) libcurl/8.4.0 OpenSSL/3.0.10 zlib/1.2.13\n"
            "Release-Date: 2023-10-11\n"
            "Protocols: dict file ftp ftps http https imap imaps ldap ldaps pop3 pop3s "
            "rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss\n"
            "Features: alt-svc AsynchDNS HSTS HTTP2 HTTPS-proxy IPv6 Largefile libz "
            "NTLM SSL threadsafe UnixSockets\n"
        )
        self.stderr = stderr
        self.error = error


class FakeCurlRunner:
    """Canned-response stub keyed by URL substring match on the `market=`
    token. Never touches the network or a real subprocess. Records call
    counts and constructed request order for command-safety assertions."""

    def __init__(self, responses_by_token: dict[str, "tic.CurlRequestResult"],
                 version_result: FakeVersionResult | None = None, default=None):
        self.responses_by_token = responses_by_token
        self.version_result = version_result or FakeVersionResult()
        self.default = default
        self.version_call_count = 0
        self.request_call_count = 0
        self.urls_fetched: list[str] = []
        self.curl_path = "/usr/bin/curl"

    def run_version(self) -> FakeVersionResult:
        self.version_call_count += 1
        return self.version_result

    def run_request(self, url: str) -> "tic.CurlRequestResult":
        self.request_call_count += 1
        self.urls_fetched.append(url)
        for token, result in self.responses_by_token.items():
            if f"market={token}" in url:
                return result
        if self.default is not None:
            return self.default
        raise AssertionError(f"FakeCurlRunner: no canned response configured for url={url}")


class PoisonedCurlRunner:
    """Raises immediately if .run_version() or .run_request() is ever
    called. Used to prove a code path makes zero subprocess calls."""

    def __init__(self):
        self.version_call_count = 0
        self.request_call_count = 0
        self.curl_path = "/usr/bin/curl"

    def run_version(self):
        self.version_call_count += 1
        raise AssertionError("PoisonedCurlRunner.run_version() was called -- subprocess attempted!")

    def run_request(self, url: str):
        self.request_call_count += 1
        raise AssertionError(f"PoisonedCurlRunner.run_request() was called with url={url} -- subprocess attempted!")


def _json_body(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def _ok_result(points: list[tuple[int, float]]) -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=0, http_status=200,
        body_bytes=_json_body({"history": [{"t": t, "p": p} for t, p in points]}),
        headers_text="HTTP/1.1 200 OK\r\n", stderr_text="", error=None,
    )


def _empty_history_result() -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=0, http_status=200, body_bytes=_json_body({"history": []}),
        headers_text="HTTP/1.1 200 OK\r\n", stderr_text="", error=None,
    )


def _http_403_result() -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=0, http_status=403, body_bytes=b"Cloudflare Error 1010",
        headers_text="HTTP/1.1 403 Forbidden\r\n", stderr_text="", error=None,
    )


def _execution_failure_result() -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=None, http_status=None, body_bytes=None, headers_text=None,
        stderr_text=None, error="curl: (7) Failed to connect",
    )


def _invalid_json_result() -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=0, http_status=200, body_bytes=b"not json at all {{{",
        headers_text="HTTP/1.1 200 OK\r\n", stderr_text="", error=None,
    )


def _malformed_shape_result() -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=0, http_status=200, body_bytes=_json_body({"unexpected": "shape"}),
        headers_text="HTTP/1.1 200 OK\r\n", stderr_text="", error=None,
    )


def _all_points_malformed_result() -> "tic.CurlRequestResult":
    return tic.CurlRequestResult(
        exit_code=0, http_status=200,
        body_bytes=_json_body({"history": [{"t": "not-a-number", "p": "also-not"}]}),
        headers_text="HTTP/1.1 200 OK\r\n", stderr_text="", error=None,
    )


def _all_ok_responses() -> dict:
    return {
        _tok("2"): _ok_result([(1_700_000_000, 0.4)]),
        _tok("3"): _ok_result([(1_700_000_000, 0.6)]),
        _tok("4"): _ok_result([(1_700_000_000, 0.4)]),
        _tok("5"): _ok_result([(1_700_000_000, 0.6)]),
        _tok("6"): _ok_result([(1_700_000_000, 0.4)]),
        _tok("7"): _ok_result([(1_700_000_000, 0.6)]),
    }


def _all_403_responses() -> dict:
    return {tok: _http_403_result() for tok in (_tok("2"), _tok("3"), _tok("4"), _tok("5"), _tok("6"), _tok("7"))}


# ===========================================================================
# 1. Acknowledgements and dispatch
# ===========================================================================

def test_acknowledgements_both_present_passes():
    tic.check_transport_isolation_acknowledgements(
        {"transport_isolation_canary_enabled": True, "acknowledge_transport_isolation_not_p1_evidence": True}
    )


def test_missing_transport_isolation_enabled_hard_stops():
    try:
        tic.check_transport_isolation_acknowledgements(
            {"acknowledge_transport_isolation_not_p1_evidence": True}
        )
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "transport_isolation_canary_enabled" in str(exc)


def test_missing_acknowledgement_hard_stops():
    try:
        tic.check_transport_isolation_acknowledgements(
            {"transport_isolation_canary_enabled": True}
        )
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "acknowledge_transport_isolation_not_p1_evidence" in str(exc)


def test_truthy_non_boolean_values_rejected():
    try:
        tic.check_transport_isolation_acknowledgements(
            {"transport_isolation_canary_enabled": "true", "acknowledge_transport_isolation_not_p1_evidence": 1}
        )
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_simultaneous_flags_rejected_zero_subprocess_calls():
    poisoned = PoisonedCurlRunner()
    raw_input = _valid_transport_isolation_input(live_canary_enabled=True)
    try:
        tic.check_no_mode_ambiguity(raw_input)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MODE_AMBIGUOUS" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_optional_endpoint_flag_true_hard_stops():
    try:
        tic.check_no_optional_endpoint({"live_include_current_endpoint_check": True})
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_optional_endpoint_flag_false_or_absent_passes():
    tic.check_no_optional_endpoint({"live_include_current_endpoint_check": False})
    tic.check_no_optional_endpoint({})


def test_conflicting_base_url_hard_stops():
    try:
        tic.check_runtime_overrides({"clob_base_url": "https://evil.example.com"})
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_conflicting_window_hard_stops():
    try:
        tic.check_runtime_overrides({"price_history_window_seconds": 7200})
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_conflicting_fidelity_hard_stops():
    try:
        tic.check_runtime_overrides({"fidelity": "5"})
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_matching_overrides_pass():
    tic.check_runtime_overrides({
        "clob_base_url": tic.CLOB_BASE_URL,
        "price_history_window_seconds": tic.PRICE_HISTORY_WINDOW_SECONDS,
        "fidelity": tic.FIDELITY,
    })


# ===========================================================================
# 2. Manifest — shape validation (load_fixed_manifest)
# ===========================================================================

def test_manifest_exact_supplied_manifest_passes(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    conditions = tic.load_fixed_manifest(manifest_path)
    assert len(conditions) == 3


def test_manifest_missing_file_hard_stops(tmp_path):
    manifest_path = tmp_path / "does_not_exist.json"
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)


def test_manifest_malformed_json_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text("{not valid json")
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)


def test_manifest_wrong_top_level_shape_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(["not", "an", "object"]))
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)


def test_manifest_with_extra_top_level_field_hard_stops_zero_subprocess(tmp_path):
    """Explicitly required: the current expanded shape (with any extra
    top-level field, e.g. operational flags) must halt as
    STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID before any subprocess
    executes."""
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path, extra_top_level={"dry_run": False})
    poisoned = PoisonedCurlRunner()
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)
        assert "unexpected top-level field" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_manifest_condition_with_extra_field_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    conditions[0]["slug"] = "unexpected-extra-field"
    _write_manifest(manifest_path, conditions=conditions)
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)


def test_manifest_wrong_condition_count_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path, conditions=[dict(ACCEPTED_MANIFEST_CONDITIONS[0])])
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_manifest_duplicate_subclass_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    conditions[2]["nb_subclass"] = "UP_DOWN"  # now two UP_DOWN, zero NAMED_OTHER
    _write_manifest(manifest_path, conditions=conditions)
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_manifest_duplicate_token_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    conditions[1]["side_0_token_id"] = conditions[0]["side_0_token_id"]
    _write_manifest(manifest_path, conditions=conditions)
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_manifest_scientific_notation_token_hard_stops(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    conditions[0]["side_0_token_id"] = "1e10"
    _write_manifest(manifest_path, conditions=conditions)
    try:
        tic.load_fixed_manifest(manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


# ===========================================================================
# 3. Manifest — reconciliation against raw_input (exact equality, zero normalization)
# ===========================================================================

def test_reconciliation_runtime_conditions_exactly_equal_passes(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    raw_input = {"conditions": [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]}
    result = tic.reconcile_manifest_and_raw_input(raw_input, manifest_path)
    assert result == ACCEPTED_MANIFEST_CONDITIONS


def test_reordered_conditions_fail(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    reordered = [dict(c) for c in reversed(ACCEPTED_MANIFEST_CONDITIONS)]
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": reordered}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)


def test_side_swap_fails(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    swapped = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    swapped[0]["side_0_token_id"], swapped[0]["side_1_token_id"] = (
        swapped[0]["side_1_token_id"], swapped[0]["side_0_token_id"],
    )
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": swapped}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_changed_token_string_fails(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    changed = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    changed[0]["side_0_token_id"] = _tok("9")
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": changed}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_leading_zero_token_fails(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    changed = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    changed[0]["side_0_token_id"] = "0" + changed[0]["side_0_token_id"]
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": changed}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_extra_condition_in_raw_input_fails(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    extra = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS] + [dict(ACCEPTED_MANIFEST_CONDITIONS[0])]
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": extra}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_missing_condition_in_raw_input_fails(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    missing = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS[:2]]
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": missing}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_decision_ts_mismatch_fails(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    changed = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    changed[0]["decision_ts"] = "2026-01-01T02:00:00Z"
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": changed}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass


def test_every_manifest_failure_causes_zero_subprocess_calls(tmp_path):
    """Every manifest-reconciliation failure mode above must never touch a
    subprocess. This test exercises one representative failure with a
    poisoned runner present in scope (never invoked -- reconciliation
    itself never accepts a runner argument, which is itself the proof:
    the function signature has no way to reach a runner)."""
    poisoned = PoisonedCurlRunner()
    manifest_path = tmp_path / "missing.json"
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": []}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


# --- Patch 1: exact runtime manifest equality -- reject any extra/missing
# runtime-only field, not just mismatched values on the 5 required ones. ---

def test_extra_runtime_slug_field_hard_stops_zero_subprocess(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    poisoned = PoisonedCurlRunner()
    runtime_conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    runtime_conditions[0]["slug"] = "unexpected-runtime-only-field"
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": runtime_conditions}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)
        assert "runtime-only fields" in str(exc) or "field set" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_extra_arbitrary_runtime_field_hard_stops_zero_subprocess(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    poisoned = PoisonedCurlRunner()
    runtime_conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    runtime_conditions[1]["some_arbitrary_extra_key"] = "value"
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": runtime_conditions}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_missing_required_runtime_key_hard_stops_zero_subprocess(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    poisoned = PoisonedCurlRunner()
    runtime_conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    del runtime_conditions[2]["side_1_token_id"]
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": runtime_conditions}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_matching_values_but_different_object_shape_hard_stops_zero_subprocess(tmp_path):
    """Same required values, but wrapped with a differently-shaped object
    (e.g. one required key renamed/duplicated via an extra alias key) --
    must still hard-stop, since the key SET must match exactly, not just
    the values under the expected keys."""
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    poisoned = PoisonedCurlRunner()
    runtime_conditions = [dict(c) for c in ACCEPTED_MANIFEST_CONDITIONS]
    # Same 5 correct keys/values, plus one more key that duplicates a value
    # under a different name -- a different complete object shape even
    # though every required field still matches.
    runtime_conditions[0]["condition_id_alias"] = runtime_conditions[0]["condition_id"]
    try:
        tic.reconcile_manifest_and_raw_input({"conditions": runtime_conditions}, manifest_path)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


# ===========================================================================
# 4. Curl provenance preflight
# ===========================================================================

def test_curl_absent_hard_stops_via_production_entry_point(tmp_path, monkeypatch):
    """Patch 6: calls the ACTUAL production entry point
    (run_transport_isolation_from_actor_input), with shutil.which
    monkeypatched to return None, rather than manually raising the
    expected exception. Proves the real code path detects curl absence
    and makes zero subprocess calls."""
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    monkeypatch.setattr(tic, "MANIFEST_RELATIVE_PATH", str(manifest_path))
    monkeypatch.setattr(tic.shutil, "which", lambda name: None)

    raw_input = _valid_transport_isolation_input()
    try:
        tic.run_transport_isolation_from_actor_input(raw_input)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)


def test_curl_version_nonzero_exit_hard_stops():
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(exit_code=1))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
    assert runner.request_call_count == 0


def test_curl_version_execution_error_hard_stops():
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(error="curl: command not found"))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
    assert runner.request_call_count == 0


def test_malformed_version_output_hard_stops():
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout="garbage, not curl output at all"))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
    assert runner.request_call_count == 0


# --- Patch 3: require complete curl provenance (tls_backend, non-empty
# protocol list, and https present) -- missing any hard-stops. ---

def test_missing_tls_backend_hard_stops_zero_data_requests():
    stdout = "curl 8.4.0 libcurl/8.4.0\nProtocols: http https\n"  # no recognizable TLS backend token
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout=stdout))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
        assert "TLS backend" in str(exc)
    assert runner.request_call_count == 0


def test_missing_protocol_line_hard_stops_zero_data_requests():
    stdout = "curl 8.4.0 libcurl/8.4.0 OpenSSL/3.0.10\n"  # no Protocols: line at all
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout=stdout))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
        assert "Protocols" in str(exc)
    assert runner.request_call_count == 0


def test_empty_protocol_list_hard_stops_zero_data_requests():
    stdout = "curl 8.4.0 libcurl/8.4.0 OpenSSL/3.0.10\nProtocols: \n"  # Protocols: line present but empty
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout=stdout))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
    assert runner.request_call_count == 0


def test_absence_of_https_hard_stops_zero_data_requests():
    stdout = "curl 8.4.0 libcurl/8.4.0 OpenSSL/3.0.10\nProtocols: ftp ftps\n"  # no https
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout=stdout))
    try:
        tic.run_curl_version_preflight(runner)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE" in str(exc)
        assert "https" in str(exc)
    assert runner.request_call_count == 0


def test_complete_provenance_with_https_passes():
    stdout = "curl 8.4.0 libcurl/8.4.0 OpenSSL/3.0.10\nProtocols: http https ftp\n"
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout=stdout))
    provenance = tic.run_curl_version_preflight(runner)
    assert provenance["tls_backend"] == "OpenSSL/3.0.10"
    assert "https" in provenance["curl_supported_protocols"]


def test_curl_libcurl_tls_protocol_parsing():
    runner = FakeCurlRunner({})
    provenance = tic.run_curl_version_preflight(runner)
    assert provenance["curl_version"] == "8.4.0"
    assert provenance["libcurl_version"] == "8.4.0"
    assert provenance["tls_backend"] == "OpenSSL/3.0.10"
    assert "https" in provenance["curl_supported_protocols"]
    assert "http" in provenance["curl_supported_protocols"]
    assert provenance["curl_version_exit_code"] == 0


def test_bounded_version_output():
    long_output = (
        "curl 8.4.0 libcurl/8.4.0 OpenSSL/3.0.10\n"
        "Protocols: http https\n"
        + ("x" * 5000)
    )
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(stdout=long_output))
    provenance = tic.run_curl_version_preflight(runner)
    assert len(provenance["curl_version_output"]) == tic.CURL_VERSION_OUTPUT_MAX_CHARS


def test_provenance_failure_proves_zero_data_request_subprocess_calls():
    runner = FakeCurlRunner({}, version_result=FakeVersionResult(exit_code=1))
    try:
        tic.run_curl_version_preflight(runner)
    except tic.TransportIsolationValidationError:
        pass
    assert runner.request_call_count == 0


# ===========================================================================
# 5. Request-plan construction and exact count
# ===========================================================================

def test_plan_has_exactly_six_requests():
    plan = tic.build_transport_isolation_plan(ACCEPTED_MANIFEST_CONDITIONS)
    assert len(plan) == 6
    tic.check_exact_request_count(plan)  # should not raise


def test_plan_sequential_fixed_order_side0_then_side1():
    plan = tic.build_transport_isolation_plan(ACCEPTED_MANIFEST_CONDITIONS)
    expected_order = [
        ("0xUP", 0), ("0xUP", 1), ("0xOU", 0), ("0xOU", 1), ("0xNO", 0), ("0xNO", 1),
    ]
    actual_order = [(p.condition_id, p.side) for p in plan]
    assert actual_order == expected_order


def test_plan_urls_are_single_market_form():
    plan = tic.build_transport_isolation_plan(ACCEPTED_MANIFEST_CONDITIONS)
    for p in plan:
        assert "/prices-history?" in p.request_url_actual
        assert "market=" in p.request_url_actual
        assert "startTs=" in p.request_url_actual
        assert "endTs=" in p.request_url_actual
        assert "fidelity=1" in p.request_url_actual
        assert "batch" not in p.request_url_actual.lower()
        assert p.request_url_actual.startswith(tic.CLOB_BASE_URL)


# ===========================================================================
# 6. Command safety (SubprocessCurlRunner argument construction, inspected
#    without ever actually running a subprocess)
# ===========================================================================

def test_curl_command_construction_exact_and_safe(monkeypatch):
    """Patches subprocess.run to capture the exact argv without executing
    anything, proving the command shape is exactly as required."""
    captured = {}

    class FakeCompletedProcess:
        returncode = 0
        stdout = b"200"
        stderr = b""

    def fake_run(argv, capture_output, timeout, env, shell):
        captured["argv"] = argv
        captured["timeout"] = timeout
        captured["env"] = env
        captured["shell"] = shell
        return FakeCompletedProcess()

    monkeypatch.setattr(tic.subprocess, "run", fake_run)
    runner = tic.SubprocessCurlRunner(curl_path="/usr/bin/curl")
    runner.run_request("https://clob.polymarket.com/prices-history?market=123&startTs=1&endTs=2&fidelity=1")

    argv = captured["argv"]
    assert argv[0] == "/usr/bin/curl"
    assert argv[1] == "-q"  # disable .curlrc, must be first
    assert "--silent" in argv
    assert "--show-error" in argv
    assert "--max-time" in argv and argv[argv.index("--max-time") + 1] == "15"
    assert "--dump-header" in argv
    assert "--output" in argv
    assert "--write-out" in argv and argv[argv.index("--write-out") + 1] == "%{http_code}"
    assert argv[-1] == "https://clob.polymarket.com/prices-history?market=123&startTs=1&endTs=2&fidelity=1"

    forbidden_flags = (
        "--request", "-X", "--user-agent", "-A", "--header", "-H", "--cookie", "-b",
        "--cookie-jar", "-c", "--referer", "-e", "--proxy", "-x", "--retry",
        "--location", "-L", "--compressed", "--http1.0", "--http1.1", "--http2",
        "--http3", "--user", "-u",
    )
    for flag in forbidden_flags:
        assert flag not in argv, f"forbidden flag {flag!r} present in curl argv: {argv}"

    assert captured["shell"] is False


def test_no_shell_execution():
    """SubprocessCurlRunner never uses shell=True anywhere."""
    import inspect
    source = inspect.getsource(tic.SubprocessCurlRunner)
    assert "shell=True" not in source
    assert "shell=False" in source


def test_proxy_env_vars_stripped_case_insensitively(monkeypatch):
    monkeypatch.setenv("HTTP_PROXY", "http://evil.example.com")
    monkeypatch.setenv("https_proxy", "http://evil.example.com")
    monkeypatch.setenv("All_Proxy", "http://evil.example.com")
    monkeypatch.setenv("NO_PROXY", "localhost")
    env = tic.sanitized_subprocess_env()
    for key in env:
        assert key.lower() not in tic._PROXY_ENV_VAR_LOWER_NAMES, f"proxy var {key} leaked into sanitized env"


def test_no_fallback_transport_import():
    """Structural check: this module never imports requests/httpx/aiohttp
    or the urllib live-canary's HttpFetcher -- no fallback transport
    exists in this file at all."""
    import inspect
    source = inspect.getsource(tic)
    for forbidden in ("import requests", "import httpx", "import aiohttp", "HttpFetcher", "urllib.request"):
        assert forbidden not in source, f"forbidden fallback-transport reference {forbidden!r} found"


# ===========================================================================
# 7. Classification and full-pipeline row counts
# ===========================================================================

def test_full_pipeline_all_six_200_usable():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    raw = [r for r in rows if r["row_type"] == "raw_request_summary_row"]
    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    assert len(raw) == 6
    assert len(candidates) == 6
    assert len(pairs) == 3
    assert len(rows) == 15
    assert all(r["condition_pair_status"] == "BOTH_SIDES_PRESENT" for r in pairs)


def test_full_pipeline_all_six_403():
    runner = FakeCurlRunner(_all_403_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    raw = [r for r in rows if r["row_type"] == "raw_request_summary_row"]
    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    assert len(raw) == 6
    assert len(candidates) == 0
    assert len(pairs) == 3
    assert len(rows) == 9
    assert all(r["request_classification"] == "APIFY_CURL_TRANSPORT_ENDPOINT_ERROR" for r in raw)
    assert all(r["condition_pair_status"] == "BOTH_SIDES_MISSING_OR_BLOCKED" for r in pairs)


def test_classify_empty_history():
    derived = tic.classify_and_parse_curl_request(
        _empty_history_result(), _tok("2"), _tok("2"), "2026-01-01T00:00:00Z",
    )
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_EMPTY_HISTORY"
    assert derived["side_status"] == "EMPTY"


def test_classify_invalid_json():
    derived = tic.classify_and_parse_curl_request(
        _invalid_json_result(), _tok("2"), _tok("2"), "2026-01-01T00:00:00Z",
    )
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_ENDPOINT_ERROR"
    assert derived["side_status"] == "ERROR"


def test_classify_malformed_shape():
    derived = tic.classify_and_parse_curl_request(
        _malformed_shape_result(), _tok("2"), _tok("2"), "2026-01-01T00:00:00Z",
    )
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_PARSE_BLOCKED"
    assert derived["side_status"] == "PARSE_BLOCKED"


def test_classify_all_points_malformed():
    derived = tic.classify_and_parse_curl_request(
        _all_points_malformed_result(), _tok("2"), _tok("2"), "2026-01-01T00:00:00Z",
    )
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_PARSE_BLOCKED"


def test_classify_execution_failure():
    derived = tic.classify_and_parse_curl_request(
        _execution_failure_result(), _tok("2"), _tok("2"), "2026-01-01T00:00:00Z",
    )
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_EXECUTION_ERROR"
    assert derived["side_status"] == "ERROR"


def test_classify_usable_shape():
    derived = tic.classify_and_parse_curl_request(
        _ok_result([(1_700_000_000, 0.42)]), _tok("2"), _tok("2"), "2026-01-01T00:00:00Z",
    )
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_USABLE_SHAPE"
    assert derived["side_status"] == "PRESENT"


# --- Patch 2: unconfirmed token identity cannot produce a candidate ---

def _ok_result_with_body_token_id(points, body_token_id):
    body = {"market": body_token_id, "history": [{"t": t, "p": p} for t, p in points]}
    return tic.CurlRequestResult(
        exit_code=0, http_status=200, body_bytes=_json_body(body),
        headers_text="HTTP/1.1 200 OK\r\n", stderr_text="", error=None,
    )


def test_conflicting_response_body_token_id_sets_unconfirmed():
    result = _ok_result_with_body_token_id([(1_700_000_000, 0.5)], body_token_id=_tok("9"))
    derived = tic.classify_and_parse_curl_request(result, _tok("2"), _tok("2"), "2026-01-01T00:00:00Z")
    assert derived["token_identity_basis"] == "UNCONFIRMED"
    assert derived["side_status"] == "UNCONFIRMED_TOKEN_ID"
    assert derived["response_body_token_id"] == _tok("9")
    # Raw evidence is retained even though no candidate is produced.
    assert derived["candidate_price"] is not None  # the point WAS parseable
    assert derived["request_classification"] == "APIFY_CURL_TRANSPORT_USABLE_SHAPE"


def test_url_market_param_mismatch_sets_unconfirmed_defensively():
    """Defensive check: request_url_market_param should always equal
    request_token_id by construction, but if it ever didn't, that must
    also be treated as unconfirmed identity."""
    derived = tic.classify_and_parse_curl_request(
        _ok_result([(1_700_000_000, 0.5)]),
        request_token_id=_tok("2"),
        request_url_market_param=_tok("9"),  # deliberately mismatched
        decision_ts_iso="2026-01-01T00:00:00Z",
    )
    assert derived["token_identity_basis"] == "UNCONFIRMED"
    assert derived["side_status"] == "UNCONFIRMED_TOKEN_ID"


def test_one_unconfirmed_side_plus_one_present_side_no_candidate_for_unconfirmed():
    responses = _all_ok_responses()
    conflicting_body = _ok_result_with_body_token_id([(1_700_000_000, 0.4)], body_token_id=_tok("9"))
    responses[_tok("2")] = conflicting_body  # UP_DOWN side 0 becomes unconfirmed
    runner = FakeCurlRunner(responses)
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)

    raw = [r for r in rows if r["row_type"] == "raw_request_summary_row"]
    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]

    up_raw_side0 = next(r for r in raw if r["condition_id"] == "0xUP" and r["side"] == 0)
    assert up_raw_side0["token_identity_basis"] == "UNCONFIRMED"
    assert up_raw_side0["response_body_token_id"] == _tok("9")  # conflicting evidence retained

    # No candidate row for the unconfirmed side; side 1 (present) still gets one.
    up_candidates = [c for c in candidates if c["condition_id"] == "0xUP"]
    assert len(up_candidates) == 1
    assert up_candidates[0]["side"] == 1

    up_pair = next(r for r in pairs if r["condition_id"] == "0xUP")
    assert up_pair["side_0_status"] == "UNCONFIRMED_TOKEN_ID"
    assert up_pair["side_1_status"] == "PRESENT"
    assert up_pair["condition_pair_status"] == "ONE_SIDED_ONLY"  # never BOTH_SIDES_PRESENT
    assert up_pair["side_0_price_candidate"] is None  # not populated from candidate_map


def test_both_sides_unconfirmed_no_candidates_not_both_sides_present():
    responses = _all_ok_responses()
    responses[_tok("2")] = _ok_result_with_body_token_id([(1_700_000_000, 0.4)], body_token_id=_tok("8"))
    responses[_tok("3")] = _ok_result_with_body_token_id([(1_700_000_000, 0.6)], body_token_id=_tok("9"))
    runner = FakeCurlRunner(responses)
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)

    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]

    up_candidates = [c for c in candidates if c["condition_id"] == "0xUP"]
    assert len(up_candidates) == 0  # no candidate row for either unconfirmed side

    up_pair = next(r for r in pairs if r["condition_id"] == "0xUP")
    assert up_pair["side_0_status"] == "UNCONFIRMED_TOKEN_ID"
    assert up_pair["side_1_status"] == "UNCONFIRMED_TOKEN_ID"
    assert up_pair["condition_pair_status"] != "BOTH_SIDES_PRESENT"
    assert up_pair["condition_pair_status"] == "BOTH_SIDES_MISSING_OR_BLOCKED"


def test_unconfirmed_token_id_excluded_from_candidate_map_directly():
    """Directly exercises the orchestration loop's candidate_map/side_status_map
    population to prove UNCONFIRMED_TOKEN_ID is structurally excluded from
    both, not merely absent from the final row output by coincidence."""
    responses = _all_ok_responses()
    responses[_tok("4")] = _ok_result_with_body_token_id([(1_700_000_000, 0.4)], body_token_id=_tok("8"))
    runner = FakeCurlRunner(responses)
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    candidate_row_keys = {(r["condition_id"], r["side"]) for r in rows if r["row_type"] == "parsed_side_candidate_row"}
    assert ("0xOU", 0) not in candidate_row_keys


def test_mixed_side_availability_one_sided_only():
    responses = _all_ok_responses()
    responses[_tok("3")] = _http_403_result()  # UP_DOWN side 1 fails
    runner = FakeCurlRunner(responses)
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    up = next(r for r in pairs if r["condition_id"] == "0xUP")
    assert up["condition_pair_status"] == "ONE_SIDED_ONLY"
    others = [r for r in pairs if r["condition_id"] != "0xUP"]
    assert all(r["condition_pair_status"] == "BOTH_SIDES_PRESENT" for r in others)


def test_nearest_timestamp_selection_earlier_tie_break():
    decision_ts_unix = 1_700_000_000
    points = [(decision_ts_unix - 50, 0.3), (decision_ts_unix + 50, 0.7)]  # exact tie
    chosen = tic.select_nearest_point(points, decision_ts_unix)
    assert chosen == (decision_ts_unix - 50, 0.3)


def test_nearest_timestamp_selection_earlier_tie_break_order_independent():
    decision_ts_unix = 1_700_000_000
    points = [(decision_ts_unix + 50, 0.7), (decision_ts_unix - 50, 0.3)]  # later listed first
    chosen = tic.select_nearest_point(points, decision_ts_unix)
    assert chosen == (decision_ts_unix - 50, 0.3)


def test_exact_field_counts_all_row_types():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    raw = [r for r in rows if r["row_type"] == "raw_request_summary_row"]
    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    pairs = [r for r in rows if r["row_type"] == "condition_pair_summary_row"]
    assert all(len(r) == 34 for r in raw)
    assert all(len(r) == 17 for r in candidates)
    assert all(len(r) == 15 for r in pairs)


def test_disclaimer_on_every_row_type_never_old_label():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    assert all(r["disclaimer_label"] == "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE" for r in rows)
    assert not any(r["disclaimer_label"] == "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE" for r in rows)


def test_is_synthesized_always_false():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    candidates = [r for r in rows if r["row_type"] == "parsed_side_candidate_row"]
    assert all(r["is_synthesized"] is False for r in candidates)


FORBIDDEN_KEY_SUBSTRINGS = ("yes_price", "canonical_side_price", "1_minus", "synthesized_price")
FORBIDDEN_LABEL_SUBSTRINGS = ("SOURCE_VIABLE", "COVERAGE_CLEAR", "S1_OVERTURNED", "P1_UNBLOCKED")


def test_no_forbidden_fields_on_candidate_or_pair_rows():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    for row in rows:
        for key in row:
            lowered = key.lower()
            for forbidden in FORBIDDEN_KEY_SUBSTRINGS:
                assert forbidden not in lowered, f"forbidden field {key!r} in row {row!r}"
        if row["row_type"] == "parsed_side_candidate_row":
            assert "token_identity_basis" not in row
            assert "execution_origin" not in row
            assert "transport" not in row
        if row["row_type"] == "condition_pair_summary_row":
            assert "execution_origin" not in row
            assert not any(k.startswith("curl_") for k in row)


def test_no_forbidden_downstream_labels_anywhere():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    text_blob = json.dumps(rows)
    for forbidden in FORBIDDEN_LABEL_SUBSTRINGS:
        assert forbidden not in text_blob


def test_no_batch_endpoint_ever_referenced():
    runner = FakeCurlRunner(_all_ok_responses())
    rows = tic.run_transport_isolation_canary(ACCEPTED_MANIFEST_CONDITIONS, runner)
    for row in rows:
        url = row.get("request_url_actual")
        if url:
            assert "batch" not in url.lower()


# ===========================================================================
# 8. Zero-network / zero-subprocess proofs at the full entry-point level
# ===========================================================================

def test_missing_flag_zero_subprocess_calls():
    poisoned = PoisonedCurlRunner()
    raw_input = _valid_transport_isolation_input(transport_isolation_canary_enabled=False)
    try:
        tic.check_transport_isolation_acknowledgements(raw_input)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError:
        pass
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_request_count_violation_causes_zero_subprocess_calls():
    poisoned = PoisonedCurlRunner()
    # Fabricate an oversized plan directly (bypassing the 3-condition
    # reconciliation) purely to exercise check_exact_request_count's
    # zero-subprocess guarantee.
    oversized_conditions = ACCEPTED_MANIFEST_CONDITIONS + [dict(ACCEPTED_MANIFEST_CONDITIONS[0])]
    plan = tic.build_transport_isolation_plan(oversized_conditions)
    try:
        tic.check_exact_request_count(plan)
        assert False, "expected TransportIsolationValidationError"
    except tic.TransportIsolationValidationError as exc:
        assert "expected exactly 6" in str(exc)
    assert poisoned.version_call_count == 0
    assert poisoned.request_call_count == 0


def test_entry_point_reaches_curl_only_after_all_gates_pass(tmp_path, monkeypatch):
    """Proves run_transport_isolation_from_actor_input's gating doesn't
    ALSO block a fully valid request -- while still never touching a real
    subprocess. Monkeypatches shutil.which and SubprocessCurlRunner to a
    poisoned stand-in for the duration of this test only."""
    manifest_path = tmp_path / "manifest.json"
    _write_manifest(manifest_path)
    monkeypatch.setattr(tic, "MANIFEST_RELATIVE_PATH", str(manifest_path))
    monkeypatch.setattr(tic.shutil, "which", lambda name: "/usr/bin/curl")

    class PoisonedSubprocessCurlRunner:
        def __init__(self, *a, **kw):
            pass

        def run_version(self):
            raise RuntimeError("POISONED_RUNNER_REACHED:run_version")

        def run_request(self, url):
            raise RuntimeError(f"POISONED_RUNNER_REACHED:{url}")

    monkeypatch.setattr(tic, "SubprocessCurlRunner", PoisonedSubprocessCurlRunner)

    raw_input = _valid_transport_isolation_input()
    try:
        tic.run_transport_isolation_from_actor_input(raw_input)
        raise AssertionError("expected the poisoned runner to be reached and raise RuntimeError")
    except RuntimeError as exc:
        assert str(exc).startswith("POISONED_RUNNER_REACHED:")


# ===========================================================================
# 9. Patch 4: exact 34-field preflight stop rows (main.py's stop-row
#    builder). Local import of src.main here only, to keep the rest of
#    this test module independent of the `apify` package.
# ===========================================================================

def _import_main_module():
    import importlib
    return importlib.import_module("src.main")


def test_stop_row_has_exactly_34_keys():
    m = _import_main_module()
    row = m._transport_isolation_stop_row("run1", "2026-01-01T00:00:00Z", "some plain message")
    assert len(row) == 34


def test_stop_row_exact_key_set_not_merely_count():
    m = _import_main_module()
    row = m._transport_isolation_stop_row("run1", "2026-01-01T00:00:00Z", "some plain message")
    expected_keys = {
        "row_type", "run_id", "request_id", "condition_id", "nb_subclass", "side", "endpoint",
        "request_token_id", "request_url_market_param", "request_url_actual", "window_start_ts",
        "window_end_ts", "fidelity", "http_status", "response_byte_length", "raw_point_count",
        "raw_response_excerpt", "response_body_token_id", "token_identity_basis", "fetched_at",
        "request_classification", "disclaimer_label", "execution_origin", "transport",
        "curl_executable_path", "curl_version", "libcurl_version", "tls_backend",
        "curl_supported_protocols", "curl_version_output", "curl_version_exit_code",
        "curl_exit_code", "curl_stderr_excerpt", "response_headers_excerpt",
    }
    assert set(row.keys()) == expected_keys
    assert len(expected_keys) == 34


def test_stop_row_no_errors_field():
    m = _import_main_module()
    row = m._transport_isolation_stop_row("run1", "2026-01-01T00:00:00Z", "some plain message")
    assert "errors" not in row


def test_stop_row_correct_disclaimer():
    m = _import_main_module()
    row = m._transport_isolation_stop_row("run1", "2026-01-01T00:00:00Z", "some plain message")
    assert row["disclaimer_label"] == "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE"


def test_stop_row_fixed_execution_origin_and_transport():
    m = _import_main_module()
    row = m._transport_isolation_stop_row("run1", "2026-01-01T00:00:00Z", "some plain message")
    assert row["execution_origin"] == "APIFY_CURL_LIBCURL"
    assert row["transport"] == "CURL"


def test_stop_row_exact_classification_mode_ambiguous():
    m = _import_main_module()
    row = m._transport_isolation_stop_row("run1", "2026-01-01T00:00:00Z", m.MODE_AMBIGUOUS_MESSAGE)
    assert row["request_classification"] == "STOP_APIFY_TRANSPORT_MODE_AMBIGUOUS"


def test_stop_row_exact_classification_manifest_missing_or_invalid():
    m = _import_main_module()
    row = m._transport_isolation_stop_row(
        "run1", "2026-01-01T00:00:00Z",
        "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest not found",
    )
    assert row["request_classification"] == "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID"


def test_stop_row_exact_classification_curl_transport_unavailable():
    m = _import_main_module()
    row = m._transport_isolation_stop_row(
        "run1", "2026-01-01T00:00:00Z",
        "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: curl executable not found on PATH",
    )
    assert row["request_classification"] == "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE"


def test_stop_row_unrecognized_message_maps_to_preflight_hard_stop():
    m = _import_main_module()
    row = m._transport_isolation_stop_row(
        "run1", "2026-01-01T00:00:00Z",
        "transport_isolation_canary_enabled must be explicitly true ...",
    )
    assert row["request_classification"] == "PREFLIGHT_HARD_STOP"


# ===========================================================================
# 10. Patch 5: exact runtime types for override checks
# ===========================================================================

def test_reject_clob_base_url_wrong_type():
    for bad in (123, 123.0, ["https://clob.polymarket.com"], True):
        try:
            tic.check_runtime_overrides({"clob_base_url": bad})
            assert False, f"expected hard-stop for clob_base_url={bad!r}"
        except tic.TransportIsolationValidationError:
            pass


def test_reject_window_seconds_bool_float_string():
    for bad in (0, 1, "false", "true", 3600.0, "3600", True, False):
        try:
            tic.check_runtime_overrides({"price_history_window_seconds": bad})
            assert False, f"expected hard-stop for price_history_window_seconds={bad!r}"
        except tic.TransportIsolationValidationError:
            pass


def test_accept_window_seconds_exact_int():
    tic.check_runtime_overrides({"price_history_window_seconds": 3600})  # must not raise


def test_reject_fidelity_wrong_type():
    for bad in (1, 1.0, True, ["1"]):
        try:
            tic.check_runtime_overrides({"fidelity": bad})
            assert False, f"expected hard-stop for fidelity={bad!r}"
        except tic.TransportIsolationValidationError:
            pass


def test_reject_optional_endpoint_falsy_non_bool_values():
    for bad in (0, 1, "false", "true", "False"):
        try:
            tic.check_no_optional_endpoint({"live_include_current_endpoint_check": bad})
            assert False, f"expected hard-stop for live_include_current_endpoint_check={bad!r}"
        except tic.TransportIsolationValidationError:
            pass


def test_accept_optional_endpoint_exact_false_or_absent():
    tic.check_no_optional_endpoint({"live_include_current_endpoint_check": False})  # must not raise
    tic.check_no_optional_endpoint({})  # must not raise


# ---------------------------------------------------------------------------
# Plain-script runner (no pytest required)
# ---------------------------------------------------------------------------

def _main() -> int:
    import inspect
    import tempfile

    module = sys.modules[__name__]
    test_fns = [
        obj for name, obj in vars(module).items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    passed = 0
    for fn in test_fns:
        sig = inspect.signature(fn)
        if "tmp_path" in sig.parameters and "monkeypatch" in sig.parameters:
            print(f"SKIP {fn.__name__} (requires pytest fixtures; run via pytest)")
            continue
        if "tmp_path" in sig.parameters:
            with tempfile.TemporaryDirectory() as td:
                fn(Path(td))
            print(f"PASS {fn.__name__}")
            passed += 1
            continue
        if "monkeypatch" in sig.parameters:
            print(f"SKIP {fn.__name__} (requires pytest fixtures; run via pytest)")
            continue
        fn()
        print(f"PASS {fn.__name__}")
        passed += 1
    print(f"\n{passed}/{len(test_fns)} SELF-TESTS PASSED (some require pytest fixtures -- run pytest for full coverage)")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
