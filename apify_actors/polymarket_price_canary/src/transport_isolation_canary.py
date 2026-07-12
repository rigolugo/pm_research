"""
Transport-isolation canary logic for the Polymarket Price Canary Actor.

Implements SPEC_apify_transport_isolation_canary.md (ACCEPTED, branch
apify-price-canary-dry-run, orchestrator decision date 2026-07-11). THIS
MODULE IS NOT EXECUTED AGAINST LIVE NETWORK IN THIS DELIVERY. Per the
current authorization ("IMPLEMENTATION PACKAGE ONLY"):
  - no Actor build, no deployment, no run
  - no curl invocation against any URL
  - no CLOB/Polymarket/Gamma/Apify data request
  - offline unit tests only, run in-sandbox

Structural safety, not just a flag:
  - `SubprocessCurlRunner` (the only class that can invoke a real `curl`
    subprocess) is instantiated in exactly one place in this whole module:
    `run_transport_isolation_from_actor_input()`.
  - That function checks, in order, BEFORE constructing any runner:
    acknowledgements (§gate check), mode-ambiguity, the
    optional-current-endpoint prohibition, runtime-override conflicts, and
    full manifest reconciliation. Any failure raises
    `TransportIsolationValidationError` before a `SubprocessCurlRunner`
    exists at all.
  - `main.py` only calls this module's entry point when
    `raw_input.get("dry_run", True) is False` AND
    `raw_input.get("transport_isolation_canary_enabled") is True` --
    checked at the dispatch level before this module is even imported-used
    for that request.
  - Every function that builds a request plan, parses a response, or
    validates the manifest is pure computation -- no I/O -- and is
    independently unit-tested with injected fake/poisoned runners. No test
    in this codebase ever constructs a real `SubprocessCurlRunner`.

Guardrails encoded here (see the accepted spec for full rationale):
  - Exactly 3 conditions, one per subclass (UP_DOWN, OVER_UNDER,
    NAMED_OTHER), reconciled EXACTLY against the fixed identity manifest at
    `artifacts/named_binary_probe/apify_price_canary_real_condition_input.json`
    -- no normalization of side assignment or token identity, no second
    hardcoded manifest.
  - Exactly six requests: GET /prices-history, single-market form, one
    attempt per URL, sequential in fixed manifest order, side 0 then side 1
    per condition.
  - System `curl` executable only, backed by ordinary libcurl. No PycURL,
    no `curl_cffi`, no impersonation, no browser emulation, no proxy, no
    cookies, no retries, no fallback transport.
  - No yes_price / 1-price / 1-yes_price / side synthesis, no
    canonical_side_price, no scoring. None of these concepts appear
    anywhere in this module's data model.
  - Every output row carries disclaimer_label =
    "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE" -- never the old
    live-canary disclaimer. P1/P2/P3/probe/gate terms (including
    named_binary_probe_blocked) appear only in this docstring/comments as
    guardrail language -- never read, modified, computed, or used as
    operational state anywhere in this module.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from .validation import is_iso8601_utc, is_string_safe_decimal

# ---------------------------------------------------------------------------
# Constants (pinned by the accepted spec)
# ---------------------------------------------------------------------------

HARD_REQUEST_COUNT = 6
REQUIRED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
DISCLAIMER_LABEL = "APIFY_TRANSPORT_ISOLATION_NOT_P1_EVIDENCE"
POINT_SELECTION_METHOD = "nearest_ts_prefer_earlier_on_tie"

CLOB_BASE_URL = "https://clob.polymarket.com"
PRICE_HISTORY_WINDOW_SECONDS = 3600
FIDELITY = "1"

# Fixed identity/reconciliation manifest path (spec §3). This
# implementation package includes the accepted identity-only manifest at
# this path (SHA-256: b6a39d08e4d88e660bff69b7b9315ef0450fbc16f639598ea412ad6809b7567c).
# Whether it is correctly packaged into the Actor's actual build/container
# context at runtime remains unresolved -- see the README's "Known
# packaging limitation" and the implementation handoff. If it is absent at
# runtime for any reason, the accepted behavior is the zero-process
# STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID hard-stop below; this
# module never creates, fabricates, duplicates, or hash-enforces it.
MANIFEST_RELATIVE_PATH = "artifacts/named_binary_probe/apify_price_canary_real_condition_input.json"
_REQUIRED_MANIFEST_CONDITION_FIELDS = (
    "condition_id", "nb_subclass", "decision_ts", "side_0_token_id", "side_1_token_id",
)
_ALLOWED_MANIFEST_TOP_LEVEL_KEYS = {"conditions"}

# Bounds (spec §7.2, decoded-character based -- decode first, then slice).
RAW_RESPONSE_EXCERPT_MAX_CHARS = 500
CURL_STDERR_EXCERPT_MAX_CHARS = 500
RESPONSE_HEADERS_EXCERPT_MAX_CHARS = 1000
CURL_VERSION_OUTPUT_MAX_CHARS = 2000

# Curl process constants (spec §6).
CURL_MAX_TIME_SECONDS = 15
CURL_SUBPROCESS_TIMEOUT_SECONDS = CURL_MAX_TIME_SECONDS + 5  # generous margin over curl's own --max-time

# Resource-bounding only (spec §6: "must not become a retry or truncation
# path" -- if exceeded, this is an execution/parse failure, never retried,
# never silently truncated-and-continued).
MAX_RESPONSE_BODY_BYTES = 2_000_000
MAX_HEADER_FILE_BYTES = 100_000

_PROXY_ENV_VAR_LOWER_NAMES = {"http_proxy", "https_proxy", "ftp_proxy", "all_proxy", "no_proxy"}

_LIBCURL_VERSION_RE = re.compile(r"libcurl/(\S+)")
_TLS_BACKEND_RE = re.compile(
    r"\b(OpenSSL|BoringSSL|LibreSSL|Schannel|SecureTransport|GnuTLS|NSS|wolfSSL|mbedTLS)(?:/\S+)?\b"
)


class TransportIsolationValidationError(Exception):
    """Raised for any preflight hard-stop. Every raise site in this module
    that can be reached before SubprocessCurlRunner is constructed
    guarantees zero curl processes were invoked for this run. Messages are
    prefixed with the relevant STOP_* label from the accepted spec where
    one is defined (mode ambiguity, manifest, curl unavailability);
    acknowledgement/override/count failures are hard-stops too but have no
    single dedicated label in the spec, so they carry a plain descriptive
    message instead."""


# ---------------------------------------------------------------------------
# Gate 1/2: acknowledgements (checked first, before anything else)
# ---------------------------------------------------------------------------

def check_transport_isolation_acknowledgements(raw_input: dict) -> None:
    """Hard-stop unless BOTH gates are the literal JSON boolean `true`.
    Nothing about mode ambiguity, the manifest, or curl is touched before
    this check runs and passes."""
    if raw_input.get("transport_isolation_canary_enabled") is not True:
        raise TransportIsolationValidationError(
            "transport_isolation_canary_enabled must be explicitly true (a literal JSON "
            "boolean) to run the transport-isolation canary; missing, false, string, or "
            "integer values are all rejected -- hard-stop before any curl process"
        )
    if raw_input.get("acknowledge_transport_isolation_not_p1_evidence") is not True:
        raise TransportIsolationValidationError(
            "acknowledge_transport_isolation_not_p1_evidence must be explicitly true (a "
            "literal JSON boolean) to run the transport-isolation canary; missing, false, "
            "string, or integer values are all rejected -- hard-stop before any curl process"
        )


def check_no_mode_ambiguity(raw_input: dict) -> None:
    """Hard-stop if both the transport-isolation and the (old) urllib
    live-canary modes are simultaneously requested. Defense-in-depth: also
    checked earlier at the main.py dispatch level, but re-checked here so
    this module's own entry point is safe even if called directly."""
    if raw_input.get("transport_isolation_canary_enabled") is True and raw_input.get("live_canary_enabled") is True:
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MODE_AMBIGUOUS: transport_isolation_canary_enabled and "
            "live_canary_enabled cannot both be true in the same run"
        )


def check_no_optional_endpoint(raw_input: dict) -> None:
    """The transport-isolation route never includes the optional
    current-endpoint schema check, Gamma, or any endpoint beyond the six
    mandatory /prices-history requests. Must be absent, or the literal
    JSON boolean false -- checked by identity (`is`), not equality, so
    0/1/"false"/"true" and any other falsy-by-coincidence value is
    rejected rather than silently accepted."""
    value = raw_input.get("live_include_current_endpoint_check")
    if value is not None and value is not False:
        raise TransportIsolationValidationError(
            f"live_include_current_endpoint_check must be the literal boolean false or "
            f"absent for the transport-isolation route (got {value!r}); no /book request, "
            "no optional endpoint, and no Gamma request is permitted on this route"
        )


def check_runtime_overrides(raw_input: dict) -> None:
    """clob_base_url / price_history_window_seconds / fidelity, if supplied
    at all, must equal the fixed accepted values exactly, with exact
    types -- not merely values that happen to compare equal. Any
    conflict, or any type mismatch (e.g. a float or string where an int
    is required, or a bool where an int is required), hard-stops before
    curl execution. Nothing here is silently overridden or coerced."""
    clob_base_url = raw_input.get("clob_base_url")
    if clob_base_url is not None:
        if not isinstance(clob_base_url, str) or clob_base_url != CLOB_BASE_URL:
            raise TransportIsolationValidationError(
                f"clob_base_url, if supplied, must be the exact string {CLOB_BASE_URL!r}; "
                f"got {clob_base_url!r} ({type(clob_base_url).__name__})"
            )

    window = raw_input.get("price_history_window_seconds")
    if window is not None:
        # bool is a subclass of int in Python -- explicitly excluded, since
        # a boolean is never an acceptable representation of a window.
        if isinstance(window, bool) or not isinstance(window, int) or window != PRICE_HISTORY_WINDOW_SECONDS:
            raise TransportIsolationValidationError(
                "price_history_window_seconds, if supplied, must be the exact integer "
                f"{PRICE_HISTORY_WINDOW_SECONDS} (not bool, not float, not string); got "
                f"{window!r} ({type(window).__name__})"
            )

    fidelity = raw_input.get("fidelity")
    if fidelity is not None:
        if not isinstance(fidelity, str) or fidelity != FIDELITY:
            raise TransportIsolationValidationError(
                f"fidelity, if supplied, must be the exact string {FIDELITY!r}; got "
                f"{fidelity!r} ({type(fidelity).__name__})"
            )


# ---------------------------------------------------------------------------
# Manifest loading and reconciliation (spec §3 -- pinned, not open)
# ---------------------------------------------------------------------------

def load_fixed_manifest(manifest_path: str | Path | None = None) -> list[dict]:
    """Load and shape-validate the fixed identity manifest. Raises
    TransportIsolationValidationError, prefixed with
    STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID, on any problem:
    absent, unreadable, invalid JSON, wrong top-level shape, extra
    top-level or per-condition fields, wrong condition count, or any
    per-condition field not a non-empty string. Does NOT compare against
    raw_input -- see reconcile_manifest_and_raw_input for that.

    manifest_path defaults to MANIFEST_RELATIVE_PATH, looked up at call
    time (not bound as a function-definition-time default), so tests can
    monkeypatch the module constant and have it take effect."""
    if manifest_path is None:
        manifest_path = MANIFEST_RELATIVE_PATH
    path = Path(manifest_path)
    if not path.exists():
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest not "
            f"found at {manifest_path}"
        )
    try:
        raw_text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        raise TransportIsolationValidationError(
            f"STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest "
            f"unreadable: {exc}"
        )
    try:
        data = json.loads(raw_text)
    except Exception as exc:  # noqa: BLE001
        raise TransportIsolationValidationError(
            f"STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest is "
            f"not valid JSON: {exc}"
        )
    if not isinstance(data, dict):
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest "
            "top-level must be a JSON object"
        )

    extra_top_level = set(data.keys()) - _ALLOWED_MANIFEST_TOP_LEVEL_KEYS
    if extra_top_level:
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest "
            f"contains unexpected top-level field(s): {sorted(extra_top_level)}"
        )
    if "conditions" not in data:
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest "
            "missing required 'conditions' key"
        )

    conditions = data["conditions"]
    if not isinstance(conditions, list):
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest "
            "'conditions' must be a list"
        )
    if len(conditions) != 3:
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest must "
            f"contain exactly 3 conditions, found {len(conditions)}"
        )

    allowed_condition_keys = set(_REQUIRED_MANIFEST_CONDITION_FIELDS)
    for i, cond in enumerate(conditions):
        if not isinstance(cond, dict):
            raise TransportIsolationValidationError(
                "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: manifest condition at "
                f"index {i} is not a JSON object"
            )
        cond_keys = set(cond.keys())
        if cond_keys != allowed_condition_keys:
            raise TransportIsolationValidationError(
                "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: manifest condition at "
                f"index {i} has field set {sorted(cond_keys)}, expected exactly "
                f"{sorted(allowed_condition_keys)}"
            )
        for key in _REQUIRED_MANIFEST_CONDITION_FIELDS:
            if not isinstance(cond[key], str) or not cond[key]:
                raise TransportIsolationValidationError(
                    "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: manifest condition at "
                    f"index {i}, field {key!r} must be a non-empty string (got {cond[key]!r})"
                )

    subclasses = [c["nb_subclass"] for c in conditions]
    if sorted(subclasses) != sorted(REQUIRED_SUBCLASSES):
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest does "
            f"not contain exactly one each of {REQUIRED_SUBCLASSES}, found {subclasses}"
        )

    all_tokens: list[str] = []
    for c in conditions:
        all_tokens.append(c["side_0_token_id"])
        all_tokens.append(c["side_1_token_id"])
    if len(set(all_tokens)) != 6:
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: fixed identity manifest does "
            f"not contain exactly six unique tokens, found {len(set(all_tokens))}"
        )
    for token in all_tokens:
        if not is_string_safe_decimal(token):
            raise TransportIsolationValidationError(
                "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: token "
                f"{token!r} is not a string-safe decimal id"
            )
    for c in conditions:
        if not is_iso8601_utc(c["decision_ts"]):
            raise TransportIsolationValidationError(
                "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: decision_ts "
                f"{c['decision_ts']!r} is not a timezone-aware ISO8601 string"
            )

    return conditions


def reconcile_manifest_and_raw_input(
    raw_input: dict, manifest_path: str | Path | None = None,
) -> list[dict]:
    """Load the fixed manifest (raising on any shape problem), then require
    EXACT equality -- in order, field-by-field, condition-by-condition --
    against raw_input['conditions']. No normalization, no sorting, no
    coercion. Any mismatch raises TransportIsolationValidationError before
    any curl process. Returns the fixed manifest's conditions (fixed
    order) for use as the plan source -- never the raw_input copy,
    even though they must be identical to pass.

    manifest_path defaults to MANIFEST_RELATIVE_PATH, looked up at call
    time via load_fixed_manifest -- see that function's docstring."""
    fixed_conditions = load_fixed_manifest(manifest_path)

    runtime_conditions = raw_input.get("conditions")
    if not isinstance(runtime_conditions, list):
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: raw_input['conditions'] must "
            "be a list"
        )
    if len(runtime_conditions) != len(fixed_conditions):
        raise TransportIsolationValidationError(
            "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: raw_input has "
            f"{len(runtime_conditions)} conditions, fixed manifest has {len(fixed_conditions)}"
        )

    for i, (fixed_cond, runtime_cond) in enumerate(zip(fixed_conditions, runtime_conditions)):
        if not isinstance(runtime_cond, dict):
            raise TransportIsolationValidationError(
                "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: raw_input condition at "
                f"index {i} is not a JSON object"
            )
        runtime_keys = set(runtime_cond.keys())
        allowed_keys = set(_REQUIRED_MANIFEST_CONDITION_FIELDS)
        if runtime_keys != allowed_keys:
            raise TransportIsolationValidationError(
                "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: raw_input condition at "
                f"index {i} has field set {sorted(runtime_keys)}, expected exactly "
                f"{sorted(allowed_keys)} -- runtime-only fields (e.g. slug or any other "
                "extra key) are not ignored, they hard-stop the run"
            )
        for field_name in _REQUIRED_MANIFEST_CONDITION_FIELDS:
            fixed_val = fixed_cond.get(field_name)
            runtime_val = runtime_cond.get(field_name)
            # Exact string equality only -- no normalization, no numeric
            # reinterpretation, no case-folding, no whitespace trimming.
            if not isinstance(runtime_val, str) or runtime_val != fixed_val:
                raise TransportIsolationValidationError(
                    "STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID: condition at index "
                    f"{i}, field {field_name!r} does not exactly match the fixed manifest "
                    f"(fixed={fixed_val!r}, runtime={runtime_val!r})"
                )

    return fixed_conditions


# ---------------------------------------------------------------------------
# Request plan construction (pure computation, no I/O)
# ---------------------------------------------------------------------------

@dataclass
class PlannedCurlRequest:
    condition_id: str
    nb_subclass: str
    decision_ts: str
    side: int
    request_token_id: str
    request_url_market_param: str
    request_url_actual: str
    window_start_ts: int
    window_end_ts: int
    fidelity: str


def _prices_history_url(base_url: str, token_id: str, start_ts: int, end_ts: int, fidelity: str) -> str:
    # GET /prices-history?market=TOKEN_ID&startTs=...&endTs=...&fidelity=...
    # Single-market form only. Matches the accepted request builder exactly.
    params = {"market": token_id, "startTs": start_ts, "endTs": end_ts, "fidelity": fidelity}
    return f"{base_url}/prices-history?{urlencode(params)}"


def build_transport_isolation_plan(conditions: list[dict]) -> list[PlannedCurlRequest]:
    """Build the fixed six-request plan, in fixed manifest order, side 0
    then side 1 per condition. Pure computation -- no I/O, no curl."""
    plan: list[PlannedCurlRequest] = []
    for cond in conditions:
        decision_ts = cond["decision_ts"]
        parsed_ts = _dt.datetime.fromisoformat(decision_ts.replace("Z", "+00:00"))
        start_ts = int(parsed_ts.timestamp()) - PRICE_HISTORY_WINDOW_SECONDS
        end_ts = int(parsed_ts.timestamp()) + PRICE_HISTORY_WINDOW_SECONDS
        for side, token_field in ((0, "side_0_token_id"), (1, "side_1_token_id")):
            token_id = cond[token_field]
            plan.append(
                PlannedCurlRequest(
                    condition_id=cond["condition_id"],
                    nb_subclass=cond["nb_subclass"],
                    decision_ts=decision_ts,
                    side=side,
                    request_token_id=token_id,
                    request_url_market_param=token_id,
                    request_url_actual=_prices_history_url(
                        CLOB_BASE_URL, token_id, start_ts, end_ts, FIDELITY
                    ),
                    window_start_ts=start_ts,
                    window_end_ts=end_ts,
                    fidelity=FIDELITY,
                )
            )
    return plan


def check_exact_request_count(plan: list[PlannedCurlRequest]) -> None:
    """Defense-in-depth: the plan must contain exactly six requests before
    the first one runs. Given exactly-3-condition reconciliation upstream,
    this should always hold by construction -- checked explicitly anyway."""
    if len(plan) != HARD_REQUEST_COUNT:
        raise TransportIsolationValidationError(
            f"request plan has {len(plan)} requests, expected exactly {HARD_REQUEST_COUNT}; "
            "refusing to start (zero curl processes)"
        )


# ---------------------------------------------------------------------------
# Subprocess environment sanitization
# ---------------------------------------------------------------------------

def sanitized_subprocess_env() -> dict:
    """Copy of the current environment with all proxy-related variables
    removed, case-insensitively (http_proxy/HTTP_PROXY/Http_Proxy/etc, and
    the https/ftp/all/no_proxy variants). This does not add a proxy
    option to curl -- it only prevents an inherited proxy env var from
    being silently honored by libcurl."""
    env = dict(os.environ)
    for key in list(env.keys()):
        if key.lower() in _PROXY_ENV_VAR_LOWER_NAMES:
            del env[key]
    return env


# ---------------------------------------------------------------------------
# Curl subprocess abstraction
# ---------------------------------------------------------------------------

@dataclass
class CurlVersionResult:
    exit_code: int | None
    stdout: str | None  # decoded
    stderr: str | None  # decoded
    error: str | None  # non-None only for a failure to even launch the process


@dataclass
class CurlRequestResult:
    exit_code: int | None
    http_status: int | None
    body_bytes: bytes | None
    headers_text: str | None  # decoded
    stderr_text: str | None  # decoded
    error: str | None  # non-None for launch failure, timeout, or a resource-bound violation


class SubprocessCurlRunner:
    """The ONLY class in this codebase that can invoke a real `curl`
    subprocess. Instantiated in exactly one place:
    run_transport_isolation_from_actor_input(). Never instantiated in any
    test -- tests always inject a fake/poisoned runner instead. Never
    exercised against a real network in this delivery."""

    def __init__(
        self,
        curl_path: str,
        max_time_seconds: int = CURL_MAX_TIME_SECONDS,
        subprocess_timeout_seconds: int = CURL_SUBPROCESS_TIMEOUT_SECONDS,
        max_body_bytes: int = MAX_RESPONSE_BODY_BYTES,
        max_header_bytes: int = MAX_HEADER_FILE_BYTES,
    ):
        self.curl_path = curl_path
        self.max_time_seconds = max_time_seconds
        self.subprocess_timeout_seconds = subprocess_timeout_seconds
        self.max_body_bytes = max_body_bytes
        self.max_header_bytes = max_header_bytes

    def run_version(self) -> CurlVersionResult:  # pragma: no cover (never exercised in this delivery)
        try:
            proc = subprocess.run(
                [self.curl_path, "-q", "--version"],
                capture_output=True,
                timeout=self.subprocess_timeout_seconds,
                env=sanitized_subprocess_env(),
                shell=False,
            )
        except Exception as exc:  # noqa: BLE001
            return CurlVersionResult(exit_code=None, stdout=None, stderr=None, error=str(exc))
        return CurlVersionResult(
            exit_code=proc.returncode,
            stdout=proc.stdout.decode("utf-8", errors="replace"),
            stderr=proc.stderr.decode("utf-8", errors="replace"),
            error=None,
        )

    def run_request(self, url: str) -> CurlRequestResult:  # pragma: no cover (never exercised in this delivery)
        with tempfile.TemporaryDirectory() as tmp_dir:
            header_path = os.path.join(tmp_dir, "headers.txt")
            body_path = os.path.join(tmp_dir, "body.bin")
            argv = [
                self.curl_path,
                "-q",  # disable .curlrc; must be first per curl's own docs
                "--silent",
                "--show-error",
                "--max-time", str(self.max_time_seconds),
                "--dump-header", header_path,
                "--output", body_path,
                "--write-out", "%{http_code}",
                url,
            ]
            try:
                proc = subprocess.run(
                    argv,
                    capture_output=True,
                    timeout=self.subprocess_timeout_seconds,
                    env=sanitized_subprocess_env(),
                    shell=False,
                )
            except Exception as exc:  # noqa: BLE001
                return CurlRequestResult(
                    exit_code=None, http_status=None, body_bytes=None,
                    headers_text=None, stderr_text=None, error=str(exc),
                )

            stdout_text = proc.stdout.decode("utf-8", errors="replace").strip()
            http_status = int(stdout_text) if stdout_text.isdigit() else None
            stderr_text = proc.stderr.decode("utf-8", errors="replace")

            body_bytes: bytes | None = None
            if os.path.exists(body_path):
                size = os.path.getsize(body_path)
                if size > self.max_body_bytes:
                    return CurlRequestResult(
                        exit_code=proc.returncode, http_status=http_status, body_bytes=None,
                        headers_text=None, stderr_text=stderr_text,
                        error=f"response body size {size} exceeded max bound {self.max_body_bytes} bytes",
                    )
                with open(body_path, "rb") as fh:
                    body_bytes = fh.read()

            headers_text: str | None = None
            if os.path.exists(header_path):
                size = os.path.getsize(header_path)
                if size > self.max_header_bytes:
                    return CurlRequestResult(
                        exit_code=proc.returncode, http_status=http_status, body_bytes=body_bytes,
                        headers_text=None, stderr_text=stderr_text,
                        error=f"header file size {size} exceeded max bound {self.max_header_bytes} bytes",
                    )
                with open(header_path, "rb") as fh:
                    headers_text = fh.read().decode("utf-8", errors="replace")

            return CurlRequestResult(
                exit_code=proc.returncode, http_status=http_status, body_bytes=body_bytes,
                headers_text=headers_text, stderr_text=stderr_text, error=None,
            )


# ---------------------------------------------------------------------------
# Curl --version output parsing (deterministic, no guessing)
# ---------------------------------------------------------------------------

def parse_curl_version_output(stdout_text: str) -> dict:
    """Deterministically parse `curl --version` stdout. Returns a dict
    with curl_version, libcurl_version, tls_backend (may be None if not
    recognized -- never guessed), and curl_supported_protocols (list, may
    be empty if no Protocols: line found)."""
    result: dict = {
        "curl_version": None,
        "libcurl_version": None,
        "tls_backend": None,
        "curl_supported_protocols": [],
    }
    if not stdout_text:
        return result

    lines = stdout_text.splitlines()
    if lines:
        first_line = lines[0]
        m = re.match(r"curl\s+(\S+)", first_line)
        if m:
            result["curl_version"] = m.group(1)
        m2 = _LIBCURL_VERSION_RE.search(first_line)
        if m2:
            result["libcurl_version"] = m2.group(1)
        m3 = _TLS_BACKEND_RE.search(first_line)
        if m3:
            result["tls_backend"] = m3.group(0)

    for line in lines:
        if line.startswith("Protocols:"):
            result["curl_supported_protocols"] = line[len("Protocols:"):].strip().split()
            break

    return result


def run_curl_version_preflight(runner: Any) -> dict:
    """Runs `curl --version` via the injected runner -- NOT a network
    request. Raises TransportIsolationValidationError
    (STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE) if curl is absent, execution
    fails, exit code is non-zero, or ANY of the following required
    provenance cannot be captured: curl_version, libcurl_version,
    tls_backend, a non-empty curl_supported_protocols list, or "https"
    being present in that protocol list. Nothing here is guessed or
    fabricated -- tls_backend parsing only recognizes ordinary backend
    names actually reported by system curl builds (OpenSSL, BoringSSL,
    LibreSSL, Schannel, SecureTransport, GnuTLS, NSS, wolfSSL, mbedTLS);
    if curl reports something this module doesn't recognize, that is
    itself treated as missing provenance and hard-stops, rather than
    silently guessing."""
    curl_path = shutil.which("curl")
    if curl_path is None:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: curl executable not found on PATH"
        )

    runner.curl_path = curl_path  # in case the injected runner needs it; harmless if unused
    version_result = runner.run_version()
    if version_result.error is not None:
        raise TransportIsolationValidationError(
            f"STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: curl --version execution failed: "
            f"{version_result.error}"
        )
    if version_result.exit_code != 0:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: curl --version returned non-zero exit "
            f"code {version_result.exit_code}"
        )

    parsed = parse_curl_version_output(version_result.stdout or "")
    if parsed["curl_version"] is None or parsed["libcurl_version"] is None:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: required curl/libcurl provenance could "
            f"not be parsed from curl --version output: {version_result.stdout!r}"
        )
    if parsed["tls_backend"] is None:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: required TLS backend could not be "
            f"recognized in curl --version output: {version_result.stdout!r}"
        )
    if not parsed["curl_supported_protocols"]:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: no (or empty) Protocols: line found in "
            f"curl --version output: {version_result.stdout!r}"
        )
    if "https" not in parsed["curl_supported_protocols"]:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: curl does not report https in its "
            f"supported protocols: {parsed['curl_supported_protocols']!r}"
        )

    return {
        "curl_executable_path": curl_path,
        "curl_version": parsed["curl_version"],
        "libcurl_version": parsed["libcurl_version"],
        "tls_backend": parsed["tls_backend"],
        "curl_supported_protocols": parsed["curl_supported_protocols"],
        "curl_version_output": _bounded_text(version_result.stdout, CURL_VERSION_OUTPUT_MAX_CHARS),
        "curl_version_exit_code": version_result.exit_code,
    }


# ---------------------------------------------------------------------------
# Response parsing (pure computation given a CurlRequestResult -- no I/O)
# ---------------------------------------------------------------------------

def _bounded_text(text: str | None, max_chars: int) -> str | None:
    """Matches the accepted excerpt behavior exactly: text is decoded
    first (see _decode_bytes), then sliced to the first max_chars
    characters -- plain truncation, deterministic, no attempt to preserve
    complete lines/fields past the bound."""
    if text is None:
        return None
    return text[:max_chars]


def _decode_bytes(data: bytes | None) -> str | None:
    if data is None:
        return None
    return data.decode("utf-8", errors="replace")


def _try_parse_json(body_bytes: bytes | None) -> tuple[Any, bool]:
    if body_bytes is None:
        return None, False
    try:
        return json.loads(body_bytes.decode("utf-8")), True
    except Exception:  # noqa: BLE001
        return None, False


_RESPONSE_BODY_ID_KEYS = ("market", "token_id", "asset_id")


def _extract_response_body_token_id(parsed_json: Any) -> str | None:
    if not isinstance(parsed_json, dict):
        return None
    for key in _RESPONSE_BODY_ID_KEYS:
        val = parsed_json.get(key)
        if isinstance(val, str) and val:
            return val
    return None


def _extract_valid_points(history_list: list) -> list[tuple[int, float]]:
    """Return [(ts:int, price:float), ...] for items whose t/p both parse
    and whose price is in [0, 1]. Malformed items are skipped -- a
    request is only PARSE_BLOCKED if NO valid points remain."""
    points: list[tuple[int, float]] = []
    for item in history_list:
        if not isinstance(item, dict):
            continue
        try:
            t_val = int(item.get("t"))
        except (TypeError, ValueError):
            continue
        try:
            p_val = float(item.get("p"))
        except (TypeError, ValueError):
            continue
        if not (0.0 <= p_val <= 1.0):
            continue
        points.append((t_val, p_val))
    return points


def select_nearest_point(points: list[tuple[int, float]], decision_ts_unix: int) -> tuple[int, float] | None:
    """Select the point nearest decision_ts_unix. Ties broken by
    preferring the EARLIER timestamp, regardless of input order."""
    if not points:
        return None
    best: tuple[int, float] | None = None
    best_gap: int | None = None
    for ts, price in points:
        gap = abs(ts - decision_ts_unix)
        if best is None or gap < best_gap or (gap == best_gap and ts < best[0]):
            best = (ts, price)
            best_gap = gap
    return best


def classify_and_parse_curl_request(
    result: CurlRequestResult,
    request_token_id: str,
    request_url_market_param: str,
    decision_ts_iso: str,
) -> dict:
    """Derive request_classification, side_status, token-identity fields
    (for the raw row only -- candidate rows never carry these), and (if
    usable) the candidate point, from a single curl request result. Pure
    function -- no I/O."""
    derived: dict = {
        "request_classification": None,
        "side_status": None,
        "response_body_token_id": None,
        "token_identity_basis": "REQUEST_URL",
        "raw_point_count": 0,
        "candidate_price": None,
        "candidate_source_ts_iso": None,
        "signed_gap_seconds": None,
        "schema_matches_documented": False,
        "price_in_range_0_1": False,
        "timestamp_parseable": False,
    }

    if result.error is not None or result.exit_code is None or result.exit_code != 0:
        derived["request_classification"] = "APIFY_CURL_TRANSPORT_EXECUTION_ERROR"
        derived["side_status"] = "ERROR"
        return derived

    if result.http_status is None or result.http_status >= 400:
        derived["request_classification"] = "APIFY_CURL_TRANSPORT_ENDPOINT_ERROR"
        derived["side_status"] = "ERROR"
        return derived

    parsed_json, is_valid_json = _try_parse_json(result.body_bytes)
    if not is_valid_json:
        # Consistent with the accepted live-canary convention: a response
        # that isn't valid JSON at all is an endpoint-level error, not a
        # parse-blocked shape problem.
        derived["request_classification"] = "APIFY_CURL_TRANSPORT_ENDPOINT_ERROR"
        derived["side_status"] = "ERROR"
        return derived

    response_body_token_id = _extract_response_body_token_id(parsed_json)
    derived["response_body_token_id"] = response_body_token_id
    if response_body_token_id is not None:
        derived["token_identity_basis"] = (
            "RESPONSE_BODY" if response_body_token_id == request_token_id else "UNCONFIRMED"
        )
    if request_url_market_param != request_token_id:
        derived["token_identity_basis"] = "UNCONFIRMED"

    if not isinstance(parsed_json, dict) or not isinstance(parsed_json.get("history"), list):
        derived["request_classification"] = "APIFY_CURL_TRANSPORT_PARSE_BLOCKED"
        derived["side_status"] = "PARSE_BLOCKED"
        return derived

    derived["schema_matches_documented"] = True
    history = parsed_json["history"]
    derived["raw_point_count"] = len(history)

    if len(history) == 0:
        derived["request_classification"] = "APIFY_CURL_TRANSPORT_EMPTY_HISTORY"
        derived["side_status"] = "EMPTY"
        return derived

    valid_points = _extract_valid_points(history)
    if not valid_points:
        derived["request_classification"] = "APIFY_CURL_TRANSPORT_PARSE_BLOCKED"
        derived["side_status"] = "PARSE_BLOCKED"
        return derived

    decision_ts_unix = int(_dt.datetime.fromisoformat(decision_ts_iso.replace("Z", "+00:00")).timestamp())
    nearest = select_nearest_point(valid_points, decision_ts_unix)
    candidate_ts, candidate_price = nearest  # type: ignore[misc]

    derived["timestamp_parseable"] = True
    derived["price_in_range_0_1"] = True
    derived["candidate_price"] = candidate_price
    derived["candidate_source_ts_iso"] = (
        _dt.datetime.fromtimestamp(candidate_ts, tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    derived["signed_gap_seconds"] = candidate_ts - decision_ts_unix
    derived["request_classification"] = "APIFY_CURL_TRANSPORT_USABLE_SHAPE"
    # Per patch: unconfirmed token identity must never produce a usable
    # candidate for this canary. If token_identity_basis is UNCONFIRMED
    # (response body conflicts with the requested token, or the request
    # URL's market= param doesn't match the requested token), side_status
    # becomes UNCONFIRMED_TOKEN_ID instead of PRESENT. The orchestration
    # loop only builds a parsed_side_candidate_row and populates
    # candidate_map when side_status == "PRESENT", so UNCONFIRMED_TOKEN_ID
    # is structurally excluded from both -- and therefore never counts
    # toward BOTH_SIDES_PRESENT in the pair summary. The raw row still
    # retains the conflicting token evidence via response_body_token_id
    # and token_identity_basis.
    derived["side_status"] = (
        "UNCONFIRMED_TOKEN_ID" if derived["token_identity_basis"] == "UNCONFIRMED" else "PRESENT"
    )
    return derived


# ---------------------------------------------------------------------------
# Row builders (pure, no I/O)
# ---------------------------------------------------------------------------

def _raw_request_summary_row(
    run_id: str, generated_at: str, planned: PlannedCurlRequest,
    curl_result: CurlRequestResult, derived: dict, provenance: dict,
) -> dict:
    return {
        # 22 retained fields (spec §7.1)
        "row_type": "raw_request_summary_row",
        "run_id": run_id,
        "request_id": str(uuid.uuid4()),
        "condition_id": planned.condition_id,
        "nb_subclass": planned.nb_subclass,
        "side": planned.side,
        "endpoint": "clob_prices_history",
        "request_token_id": planned.request_token_id,
        "request_url_market_param": planned.request_url_market_param,
        "request_url_actual": planned.request_url_actual,
        "window_start_ts": planned.window_start_ts,
        "window_end_ts": planned.window_end_ts,
        "fidelity": planned.fidelity,
        "http_status": curl_result.http_status,
        "response_byte_length": len(curl_result.body_bytes) if curl_result.body_bytes else 0,
        "raw_point_count": derived.get("raw_point_count", 0),
        "raw_response_excerpt": _bounded_text(_decode_bytes(curl_result.body_bytes), RAW_RESPONSE_EXCERPT_MAX_CHARS),
        "response_body_token_id": derived.get("response_body_token_id"),
        "token_identity_basis": derived.get("token_identity_basis", "REQUEST_URL"),
        "fetched_at": generated_at,
        "request_classification": derived["request_classification"],
        "disclaimer_label": DISCLAIMER_LABEL,
        # 12 additive transport-provenance fields (spec §7.2)
        "execution_origin": "APIFY_CURL_LIBCURL",
        "transport": "CURL",
        "curl_executable_path": provenance["curl_executable_path"],
        "curl_version": provenance["curl_version"],
        "libcurl_version": provenance["libcurl_version"],
        "tls_backend": provenance["tls_backend"],
        "curl_supported_protocols": provenance["curl_supported_protocols"],
        "curl_version_output": provenance["curl_version_output"],
        "curl_version_exit_code": provenance["curl_version_exit_code"],
        "curl_exit_code": curl_result.exit_code,
        "curl_stderr_excerpt": _bounded_text(curl_result.stderr_text, CURL_STDERR_EXCERPT_MAX_CHARS),
        "response_headers_excerpt": _bounded_text(curl_result.headers_text, RESPONSE_HEADERS_EXCERPT_MAX_CHARS),
    }


def _parsed_side_candidate_row(run_id: str, planned: PlannedCurlRequest, derived: dict) -> dict:
    # Exactly 17 fields (spec §7.4). No transport fields, no token_identity_basis.
    return {
        "row_type": "parsed_side_candidate_row",
        "run_id": run_id,
        "condition_id": planned.condition_id,
        "nb_subclass": planned.nb_subclass,
        "side": planned.side,
        "token_id": planned.request_token_id,
        "decision_ts": planned.decision_ts,
        "candidate_price": derived["candidate_price"],
        "candidate_source_ts": derived["candidate_source_ts_iso"],
        "signed_gap_seconds": derived["signed_gap_seconds"],
        "point_selection_method": POINT_SELECTION_METHOD,
        "side_status": derived["side_status"],
        "schema_matches_documented": derived["schema_matches_documented"],
        "price_in_range_0_1": derived["price_in_range_0_1"],
        "timestamp_parseable": derived["timestamp_parseable"],
        "is_synthesized": False,
        "disclaimer_label": DISCLAIMER_LABEL,
    }


def _condition_pair_summary_rows(
    conditions: list[dict],
    side_status_map: dict[tuple[str, int], str],
    candidate_map: dict[tuple[str, int], tuple[float, str]],
    run_id: str,
    generated_at: str,
) -> list[dict]:
    # Exactly 15 fields (spec §7.5). No transport fields.
    rows = []
    for cond in conditions:
        cid = cond["condition_id"]
        s0_status = side_status_map.get((cid, 0), "ERROR")
        s1_status = side_status_map.get((cid, 1), "ERROR")
        s0_price, s0_ts = candidate_map.get((cid, 0), (None, None))
        s1_price, s1_ts = candidate_map.get((cid, 1), (None, None))

        present_count = sum(1 for s in (s0_status, s1_status) if s == "PRESENT")
        if present_count == 2:
            pair_status = "BOTH_SIDES_PRESENT"
        elif present_count == 1:
            pair_status = "ONE_SIDED_ONLY"
        else:
            pair_status = "BOTH_SIDES_MISSING_OR_BLOCKED"

        rows.append({
            "row_type": "condition_pair_summary_row",
            "run_id": run_id,
            "condition_id": cid,
            "nb_subclass": cond["nb_subclass"],
            "side_0_token_id": cond["side_0_token_id"],
            "side_1_token_id": cond["side_1_token_id"],
            "side_0_price_candidate": s0_price,
            "side_1_price_candidate": s1_price,
            "side_0_source_ts": s0_ts,
            "side_1_source_ts": s1_ts,
            "side_0_status": s0_status,
            "side_1_status": s1_status,
            "condition_pair_status": pair_status,
            "disclaimer_label": DISCLAIMER_LABEL,
            "generated_at": generated_at,
        })
    return rows


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_transport_isolation_canary(
    conditions: list[dict], curl_runner: Any, run_id: str | None = None,
) -> list[dict]:
    """Build the plan, enforce the exact request count (zero curl calls if
    it fails), run the curl-version preflight (zero data requests if it
    fails), then run every planned request through `curl_runner`, and
    return the full row list. `conditions` must already have passed
    reconcile_manifest_and_raw_input -- this function does not re-validate
    manifest shape."""
    plan = build_transport_isolation_plan(conditions)
    check_exact_request_count(plan)  # raises before ANY subprocess call

    provenance = run_curl_version_preflight(curl_runner)  # raises before any data request

    if run_id is None:
        run_id = str(uuid.uuid4())
    generated_at = _dt.datetime.now(_dt.timezone.utc).isoformat()

    raw_rows: list[dict] = []
    candidate_rows: list[dict] = []
    side_status_map: dict[tuple[str, int], str] = {}
    candidate_map: dict[tuple[str, int], tuple[float, str]] = {}

    # Sequential, fixed manifest order, side 0 then side 1 per condition --
    # guaranteed by build_transport_isolation_plan's construction order and
    # this plain for-loop (no concurrency, no reordering).
    for planned in plan:
        curl_result = curl_runner.run_request(planned.request_url_actual)
        derived = classify_and_parse_curl_request(
            curl_result, planned.request_token_id, planned.request_url_market_param, planned.decision_ts,
        )
        raw_rows.append(_raw_request_summary_row(run_id, generated_at, planned, curl_result, derived, provenance))
        side_status_map[(planned.condition_id, planned.side)] = derived["side_status"]
        if derived["side_status"] == "PRESENT":
            candidate_rows.append(_parsed_side_candidate_row(run_id, planned, derived))
            candidate_map[(planned.condition_id, planned.side)] = (
                derived["candidate_price"], derived["candidate_source_ts_iso"],
            )

    pair_rows = _condition_pair_summary_rows(conditions, side_status_map, candidate_map, run_id, generated_at)

    return raw_rows + candidate_rows + pair_rows


def run_transport_isolation_from_actor_input(raw_input: dict) -> list[dict]:
    """The ONLY function in this module that constructs a real
    SubprocessCurlRunner. Called from main.py only when
    raw_input.get("dry_run", True) is False AND
    raw_input.get("transport_isolation_canary_enabled") is True. Checks,
    in order, before touching curl at all:
      1. acknowledgements (both literal-true gates)
      2. mode ambiguity (defense-in-depth re-check)
      3. optional-current-endpoint prohibition
      4. runtime-override conflicts
      5. manifest reconciliation (exact equality, zero normalization)
    Any failure raises TransportIsolationValidationError before
    SubprocessCurlRunner exists at all."""
    check_transport_isolation_acknowledgements(raw_input)
    check_no_mode_ambiguity(raw_input)
    check_no_optional_endpoint(raw_input)
    check_runtime_overrides(raw_input)
    conditions = reconcile_manifest_and_raw_input(raw_input)

    curl_path = shutil.which("curl")
    if curl_path is None:
        raise TransportIsolationValidationError(
            "STOP_APIFY_CURL_TRANSPORT_UNAVAILABLE: curl executable not found on PATH"
        )
    runner = SubprocessCurlRunner(curl_path)  # the only construction site in the whole module
    return run_transport_isolation_canary(conditions, runner)
