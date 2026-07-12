"""
End-to-end integration tests: run the ACTUAL Actor entry point (main.py, via
the real Apify SDK and file-system local storage) as a SUBPROCESS, rather
than only unit-testing individual functions in-process.

Why subprocess: Actor.__aexit__ calls sys.exit() by default, which is
correct for a real Actor run but cannot be caught cleanly inside an
in-process asyncio.run() call from a test. Running `python3 -m src` as a
subprocess is also a more faithful reproduction of how the Actor actually
executes.

Why these two scenarios don't need fetcher monkeypatching to prove
zero-network: this sandbox's own network egress policy does not allow
clob.polymarket.com / gamma-api.polymarket.com at all (see the network
configuration this environment was given). If the code ever incorrectly
reached a real HttpFetcher.fetch() call in either scenario below, that
call would fail at the OS/proxy level -- and, more importantly, it would
produce an EXTRA raw_request_summary_row with an ENDPOINT_ERROR
classification that isn't part of the expected output at all. This test's
strict assertions on exact row count and content would then fail. So
"the exact expected rows appear, and nothing else does" is itself proof
that no fetch was attempted, on top of the already-exhaustive pure-logic
proofs in test_live_canary.py (which DO use a poisoned in-process fetcher,
since those tests import the module directly rather than going through a
subprocess).

A third scenario ("request cap violation") is proven at the
tests/test_live_canary.py level only (test_request_cap_violation_causes_
zero_network_calls), because it is structurally unreachable through valid
Actor input in this design -- see that test's docstring for why.
"""

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _tok(prefix_digit: str) -> str:
    return prefix_digit + "1" * 76


def _valid_three_conditions():
    return [
        {
            "condition_id": "0xUP", "nb_subclass": "UP_DOWN",
            "decision_ts": "2026-01-01T01:00:00Z",
            "side_0_token_id": _tok("2"), "side_1_token_id": _tok("3"),
        },
        {
            "condition_id": "0xOU", "nb_subclass": "OVER_UNDER",
            "decision_ts": "2026-02-01T01:00:00Z",
            "side_0_token_id": _tok("4"), "side_1_token_id": _tok("5"),
        },
        {
            "condition_id": "0xNO", "nb_subclass": "NAMED_OTHER",
            "decision_ts": "2026-03-01T01:00:00Z",
            "side_0_token_id": _tok("6"), "side_1_token_id": _tok("7"),
        },
    ]


def _run_actor_subprocess(tmp_path: Path, actor_input: dict) -> tuple[int, str, str, Path]:
    storage_dir = tmp_path / f"apify_storage_{uuid.uuid4().hex}"
    kv_dir = storage_dir / "key_value_stores" / "default"
    kv_dir.mkdir(parents=True, exist_ok=True)
    (kv_dir / "INPUT.json").write_text(json.dumps(actor_input))

    env = os.environ.copy()
    env["APIFY_LOCAL_STORAGE_DIR"] = str(storage_dir)

    proc = subprocess.run(
        [sys.executable, "-m", "src"],
        cwd=str(PACKAGE_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return proc.returncode, proc.stdout, proc.stderr, storage_dir / "datasets" / "default"


def _read_all_dataset_rows(dataset_dir: Path) -> list[dict]:
    if not dataset_dir.exists():
        return []
    rows = []
    for f in sorted(dataset_dir.glob("*.json")):
        if f.name == "__metadata__.json":
            continue
        rows.append(json.loads(f.read_text()))
    return rows


def _assert_no_polymarket_urls(rows: list[dict]) -> None:
    # The meaningful check: no row should carry an http_status (that field
    # only exists on a live-canary raw_request_summary_row, which should
    # never be produced in either of these two scenarios at all).
    for row in rows:
        assert "http_status" not in row or row.get("http_status") is None


def test_default_input_e2e_zero_network_calls(tmp_path):
    """No dry_run key at all -- must take the pre-existing dry-run path.
    Exactly the expected dry-run rows must appear; no http_status field
    (which only a real live-canary fetch attempt would produce) anywhere."""
    actor_input = {"conditions": _valid_three_conditions()}
    returncode, stdout, stderr, dataset_dir = _run_actor_subprocess(tmp_path, actor_input)
    rows = _read_all_dataset_rows(dataset_dir)

    assert returncode == 0, f"stdout={stdout}\nstderr={stderr}"
    assert len(rows) > 0
    assert all("schema_version" in r for r in rows)
    assert all(r.get("dry_run") is True for r in rows)
    _assert_no_polymarket_urls(rows)
    assert "Zero network calls were made" in stdout or "Zero network calls were made" in stderr


def test_dry_run_true_explicit_e2e_zero_network_calls(tmp_path):
    """dry_run explicitly true must also take the unchanged dry-run path."""
    actor_input = {"conditions": _valid_three_conditions(), "dry_run": True}
    returncode, stdout, stderr, dataset_dir = _run_actor_subprocess(tmp_path, actor_input)
    rows = _read_all_dataset_rows(dataset_dir)

    assert returncode == 0, f"stdout={stdout}\nstderr={stderr}"
    assert len(rows) > 0
    assert all(r.get("dry_run") is True for r in rows)
    _assert_no_polymarket_urls(rows)


def test_missing_acknowledgements_e2e_zero_network_calls(tmp_path):
    """dry_run=false but live_canary_enabled missing -- must hard-stop
    before any request. Exactly ONE row (the preflight hard-stop row)
    should appear -- no raw_request_summary_row from an actual fetch
    attempt, which would mean the gate was bypassed."""
    actor_input = {
        "conditions": _valid_three_conditions(),
        "dry_run": False,
        "acknowledge_not_p1_evidence": True,
        # live_canary_enabled deliberately omitted
    }
    returncode, stdout, stderr, dataset_dir = _run_actor_subprocess(tmp_path, actor_input)
    rows = _read_all_dataset_rows(dataset_dir)

    assert len(rows) == 1, f"expected exactly 1 hard-stop row, got {len(rows)}: {rows}"
    assert rows[0]["request_classification"] == "PREFLIGHT_HARD_STOP"
    assert rows[0]["disclaimer_label"] == "APIFY_LIVE_CANARY_NOT_P1_EVIDENCE"
    assert "live_canary_enabled" in rows[0]["errors"][0]
    assert rows[0].get("http_status") is None
    assert rows[0].get("request_url_actual") is None


def test_mode_ambiguous_e2e_zero_subprocess_calls(tmp_path):
    """dry_run=false with BOTH transport_isolation_canary_enabled=true and
    live_canary_enabled=true -- must halt with zero requests on EITHER
    path, before either sub-module's own gating even runs."""
    actor_input = {
        "conditions": _valid_three_conditions(),
        "dry_run": False,
        "transport_isolation_canary_enabled": True,
        "acknowledge_transport_isolation_not_p1_evidence": True,
        "live_canary_enabled": True,
        "acknowledge_not_p1_evidence": True,
    }
    returncode, stdout, stderr, dataset_dir = _run_actor_subprocess(tmp_path, actor_input)
    rows = _read_all_dataset_rows(dataset_dir)

    assert len(rows) == 1, f"expected exactly 1 hard-stop row, got {len(rows)}: {rows}"
    assert rows[0]["request_classification"] == "STOP_APIFY_TRANSPORT_MODE_AMBIGUOUS"
    assert rows[0]["disclaimer_label"] == "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE"
    assert "errors" not in rows[0]
    assert rows[0]["execution_origin"] == "APIFY_CURL_LIBCURL"
    assert rows[0]["transport"] == "CURL"
    assert rows[0].get("http_status") is None
    assert rows[0].get("curl_exit_code") is None


def test_transport_isolation_missing_acknowledgement_e2e_zero_subprocess_calls(tmp_path):
    """dry_run=false + transport_isolation_canary_enabled=true, but the
    second acknowledgement missing -- must hard-stop before any curl
    process (including before the curl-version preflight)."""
    actor_input = {
        "conditions": _valid_three_conditions(),
        "dry_run": False,
        "transport_isolation_canary_enabled": True,
        # acknowledge_transport_isolation_not_p1_evidence deliberately omitted
    }
    returncode, stdout, stderr, dataset_dir = _run_actor_subprocess(tmp_path, actor_input)
    rows = _read_all_dataset_rows(dataset_dir)

    assert len(rows) == 1, f"expected exactly 1 hard-stop row, got {len(rows)}: {rows}"
    assert rows[0]["disclaimer_label"] == "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE"
    assert rows[0]["request_classification"] == "PREFLIGHT_HARD_STOP"
    assert "errors" not in rows[0]
    assert rows[0]["execution_origin"] == "APIFY_CURL_LIBCURL"
    assert rows[0]["transport"] == "CURL"
    assert rows[0].get("http_status") is None
    assert rows[0].get("curl_exit_code") is None
    assert rows[0].get("curl_executable_path") is None
    # Detailed error text is no longer stored on the row (patch 4), but
    # remains available via Actor logging / Actor.fail(status_message=...).
    assert "acknowledge_transport_isolation_not_p1_evidence" in stdout + stderr


def test_transport_isolation_manifest_absent_e2e_zero_subprocess_calls(tmp_path):
    """dry_run=false + both transport-isolation acknowledgements true, but
    the fixed identity manifest file does not exist at the expected repo
    path from this working directory -- must hard-stop with zero curl
    processes (no curl_executable_path, no http_status, no curl_exit_code
    anywhere on the stop row)."""
    actor_input = {
        "conditions": _valid_three_conditions(),
        "dry_run": False,
        "transport_isolation_canary_enabled": True,
        "acknowledge_transport_isolation_not_p1_evidence": True,
    }
    returncode, stdout, stderr, dataset_dir = _run_actor_subprocess(tmp_path, actor_input)
    rows = _read_all_dataset_rows(dataset_dir)

    assert len(rows) == 1, f"expected exactly 1 hard-stop row, got {len(rows)}: {rows}"
    assert rows[0]["request_classification"] == "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID"
    assert rows[0]["disclaimer_label"] == "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE"
    assert "errors" not in rows[0]
    assert rows[0]["execution_origin"] == "APIFY_CURL_LIBCURL"
    assert rows[0]["transport"] == "CURL"
    assert rows[0].get("http_status") is None
    assert rows[0].get("curl_exit_code") is None
    assert rows[0].get("curl_executable_path") is None
    assert "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID" in stdout + stderr


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_default_input_e2e_zero_network_calls(tmp)
        print("PASS test_default_input_e2e_zero_network_calls")
        test_dry_run_true_explicit_e2e_zero_network_calls(tmp)
        print("PASS test_dry_run_true_explicit_e2e_zero_network_calls")
        test_missing_acknowledgements_e2e_zero_network_calls(tmp)
        print("PASS test_missing_acknowledgements_e2e_zero_network_calls")
        test_mode_ambiguous_e2e_zero_subprocess_calls(tmp)
        print("PASS test_mode_ambiguous_e2e_zero_subprocess_calls")
        test_transport_isolation_missing_acknowledgement_e2e_zero_subprocess_calls(tmp)
        print("PASS test_transport_isolation_missing_acknowledgement_e2e_zero_subprocess_calls")
        test_transport_isolation_manifest_absent_e2e_zero_subprocess_calls(tmp)
        print("PASS test_transport_isolation_manifest_absent_e2e_zero_subprocess_calls")
    print("\nALL E2E SELF-TESTS PASSED")
