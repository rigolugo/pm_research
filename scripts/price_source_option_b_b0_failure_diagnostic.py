"""Option B corrected B0 failure diagnostic harness.

This module is intentionally diagnostic-only.  It captures evidence for an
already fixed 10-condition manifest, persists ledgers before any mismatch halt,
and can recompute overlap classifications from persisted artifacts without
network access.

The command-line network path is guarded by two explicit flags and is not meant
to be run unless a future authorization specifically permits the corrected B0
run.  Unit tests exercise only pure/local code paths.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
import tempfile
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, MutableMapping, Sequence

try:
    import pandas as pd
except Exception:  # pragma: no cover - import error is surfaced by callers.
    pd = None  # type: ignore[assignment]

TAU_SECONDS = 120
SIGMA_HOURS = 24
SIGMA_SECONDS = SIGMA_HOURS * 60 * 60
PRIMARY_API_ROW_LEDGER_CAP = 25_000
EXPECTED_MANIFEST_CONDITIONS = 10
DEFAULT_PAGE_LIMIT = 500
MAX_PAGES_PER_CONDITION = 5
MAX_TOTAL_CALLS = 100
DEFAULT_TAKERONLY_PROBE_CONDITIONS = 3

ARTIFACT_DIR_REL = Path("artifacts/named_binary_probe/price_source_option_b_b0_diag")
SOURCE_MANIFEST_REL = Path(
    "artifacts/named_binary_probe/price_source_option_b_b0/option_b_b0_manifest.json"
)

QUERY_MODE_PRIMARY = "PRIMARY"
QUERY_MODE_TAKERONLY_TRUE = "TAKERONLY_TRUE_PROBE"
QUERY_MODE_TAKERONLY_FALSE = "TAKERONLY_FALSE_PROBE"

PAGINATION_COMPLETE = "COMPLETE_SHORT_FINAL_PAGE"
PAGINATION_PARTIAL = "PARTIAL_RETRIEVAL"

OVERLAP_SCHEMA_BLOCKED = "OVERLAP_SCHEMA_BLOCKED"
OVERLAP_PAGINATION_PARTIAL = "OVERLAP_PAGINATION_PARTIAL"
NO_TEMPORAL_OVERLAP = "NO_TEMPORAL_OVERLAP"
OVERLAP_MATCHED = "OVERLAP_MATCHED"
OVERLAP_API_LOCAL_MISMATCH = "OVERLAP_API_LOCAL_MISMATCH"

API_ARTIFACT_COMPLETE = "API_ARTIFACT_COMPLETE"
API_ARTIFACT_INCOMPLETE = "API_ARTIFACT_INCOMPLETE"

STOP_NOT_AUTHORIZED = "STOP_NOT_AUTHORIZED"
STOP_CALL_BUDGET_EXCEEDED = "STOP_CALL_BUDGET_EXCEEDED"
STOP_SAMPLE_SCOPE_EXCEEDED = "STOP_SAMPLE_SCOPE_EXCEEDED"
STOP_PAGINATION_UNBOUNDED = "STOP_PAGINATION_UNBOUNDED"
STOP_RATE_LIMIT_HIT = "STOP_RATE_LIMIT_HIT"
STOP_SCHEMA_DEVIATION = "STOP_SCHEMA_DEVIATION"
STOP_PRECISION_LOSS = "STOP_PRECISION_LOSS"
STOP_FORBIDDEN_INFERENCE = "STOP_FORBIDDEN_INFERENCE"
STOP_NO_WRITE_PATH = "STOP_NO_WRITE_PATH"
STOP_ROW_LEDGER_CAP_EXCEEDED = "STOP_ROW_LEDGER_CAP_EXCEEDED"
STOP_API_LOCAL_MISMATCH = "STOP_API_LOCAL_MISMATCH"

VALID_CONDITION_CLASSIFICATIONS = {
    NO_TEMPORAL_OVERLAP,
    OVERLAP_MATCHED,
    OVERLAP_API_LOCAL_MISMATCH,
    OVERLAP_SCHEMA_BLOCKED,
    OVERLAP_PAGINATION_PARTIAL,
}
VALID_RUN_ARTIFACT_STATUSES = {API_ARTIFACT_COMPLETE, API_ARTIFACT_INCOMPLETE}

CONDITION_RE = re.compile(r"^0x[0-9a-f]{64}$")
SCI_NOTATION_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?[eE][+-]?\d+$")
ZERO64 = "0x" + "0" * 64

# API fields are a run-time contract and must be re-verified against official docs
# before any future authorized network run.  The pure harness does not assume a
# response shape beyond this explicit map.
# Accepted Data API document-shaped fields are camelCase for condition,
# transaction hash, and outcome index.  Snake-case aliases are accepted only
# for synthetic/internal normalized rows and backwards-compatible tests.
API_FIELD_ALIASES = {
    "condition_id": ("conditionId", "condition_id"),
    "tx_hash": ("transactionHash", "tx_hash"),
    "token_id": ("asset", "token_id"),
    "outcome_index": ("outcomeIndex", "outcome_index"),
    "side": ("side",),
    "price": ("price",),
    "size": ("size",),
    "timestamp": ("timestamp",),
}
API_FIELD_MAP = {key: aliases[0] for key, aliases in API_FIELD_ALIASES.items()}

LOCAL_REQUIRED_COLUMNS = {
    "condition_id",
    "tx_hash",
    "token_id",
    "outcome_index",
    "side",
    "price",
    "size_usdc",
    "traded_at",
}

API_LEDGER_COLUMNS = [
    "query_mode",
    "query_condition_id",
    "page_number",
    "page_limit",
    "retrieved_at_utc",
    "row_number_in_page",
    "raw_json_sha256",
    "condition_id_original",
    "tx_hash_original",
    "token_id_original",
    "outcome_index_original",
    "side_original",
    "price_original",
    "size_original",
    "timestamp_original",
    "condition_id",
    "tx_hash",
    "token_id",
    "outcome_index",
    "side",
    "price_norm",
    "size_norm",
    "timestamp_utc",
    "timestamp_epoch_ms",
    "timestamp_unit",
    "composite_key",
]

LOCAL_LEDGER_COLUMNS = [
    "condition_id_original",
    "tx_hash_original",
    "token_id_original",
    "outcome_index_original",
    "side_original",
    "price_original",
    "size_original",
    "traded_at_original",
    "trade_id_original",
    "wallet_original",
    "outcome_original",
    "condition_id",
    "tx_hash",
    "token_id",
    "outcome_index",
    "side",
    "price_norm",
    "size_norm",
    "traded_at_utc",
    "traded_at_epoch_ms",
    "composite_key",
]

MISMATCH_COLUMNS = [
    "condition_id",
    "mismatch_type",
    "row_source",
    "query_mode",
    "tx_hash",
    "token_id",
    "outcome_index",
    "side",
    "price_norm",
    "size_norm",
    "timestamp_utc",
    "composite_key",
    "in_overlap_window",
]

SCHEMA_ERROR_COLUMNS = [
    "condition_id",
    "query_condition_id",
    "query_mode",
    "page_number",
    "row_number_in_page",
    "raw_json_sha256",
    "error_code",
    "error_message",
    "error_details_json",
]

BY_CONDITION_COLUMNS = [
    "condition_id",
    "api_row_count",
    "local_row_count",
    "local_min_traded_at_utc",
    "local_max_traded_at_utc",
    "api_min_timestamp_utc",
    "api_max_timestamp_utc",
    "api_timestamp_units",
    "pagination_status",
    "pages_fetched",
    "page_row_counts_json",
    "takeronly_true_count",
    "takeronly_false_count",
    "takeronly_delta",
    "takeronly_status",
    "api_before_window_count",
    "api_in_window_count",
    "api_after_window_count",
    "api_after_sigma_count",
    "matched_in_window_count",
    "api_only_in_window_count",
    "local_only_in_window_count",
    "tx_hash_ambiguous_in_window_count",
    "temporal_subflag",
    "classification",
]


class DiagnosticHalt(RuntimeError):
    """Typed halt used by the diagnostic harness."""

    def __init__(self, code: str, message: str, *, details: Mapping[str, Any] | None = None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.details = dict(details or {})


@dataclass(frozen=True)
class PageResult:
    rows: list[Mapping[str, Any]]
    status_code: int = 200
    rate_limited: bool = False


@dataclass
class ConditionPagination:
    condition_id: str
    status: str = PAGINATION_COMPLETE
    pages_fetched: int = 0
    page_counts: list[int] = field(default_factory=list)


@dataclass
class DiagnosticArtifacts:
    manifest: dict[str, Any]
    manifest_conditions: list[str]
    api_rows: list[dict[str, Any]] = field(default_factory=list)
    local_rows: list[dict[str, Any]] = field(default_factory=list)
    mismatches: list[dict[str, Any]] = field(default_factory=list)
    by_condition: list[dict[str, Any]] = field(default_factory=list)
    pagination: dict[str, ConditionPagination] = field(default_factory=dict)
    takeronly_counts: dict[str, dict[str, int | str | None]] = field(default_factory=dict)
    schema_blocked_conditions: set[str] = field(default_factory=set)
    raw_api_pages: list[dict[str, Any]] = field(default_factory=list)
    raw_api_rows: list[dict[str, Any]] = field(default_factory=list)
    schema_errors: list[dict[str, Any]] = field(default_factory=list)
    local_load_provenance: dict[str, Any] = field(default_factory=dict)
    halt_code: str | None = None
    halt_message: str | None = None
    halt_details: dict[str, Any] | None = None
    row_cap_status: dict[str, Any] | None = None


FetchPageFn = Callable[[str, int, int, bool | None], PageResult]
LocalRowsLoader = Callable[[Path, Sequence[str]], Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _same_dir_tmp_path(target: Path) -> tuple[int, Path]:
    """Create a temp file in target's directory and return (fd, path)."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    return fd, Path(raw)


def _is_windows_replace_permission_error(exc: OSError) -> bool:
    return isinstance(exc, PermissionError) or getattr(exc, "winerror", None) == 5


def _cleanup_tmp(tmp_path: Path) -> None:
    try:
        tmp_path.unlink(missing_ok=True)
    except OSError:
        pass


def _replace_with_retries(tmp_path: Path, target: Path, *, attempts: int = 5, delay_seconds: float = 0.025) -> bool:
    """Best-effort atomic replace.

    Some Windows/Miniconda environments intermittently raise WinError 5 on
    same-directory replacement even after handles are closed.  Persist-before-
    halt is the stronger requirement for this diagnostic, so callers fall back
    to direct final-path writes if these retries fail.
    """
    last_exc: OSError | None = None
    for attempt in range(max(1, attempts)):
        try:
            os.replace(str(tmp_path), str(target))
            return True
        except OSError as exc:
            if not _is_windows_replace_permission_error(exc):
                raise
            last_exc = exc
            if attempt + 1 < attempts:
                time.sleep(delay_seconds)
    if last_exc is not None:
        return False
    return False


def _safe_write_file(path: Path, write_fn: Callable[[Any], None]) -> None:
    """Write an artifact with Windows-safe replacement plus direct-write fallback.

    The temp file is created in the same directory as the target and all handles
    are closed before replacement.  If os.replace repeatedly raises
    PermissionError/WinError 5, the payload is written directly to the final
    path so the diagnostic does not lose persist-before-halt evidence.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = _same_dir_tmp_path(path)
    tmp_closed = False
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as tmp:
            write_fn(tmp)
            tmp.flush()
            os.fsync(tmp.fileno())
        tmp_closed = True
        replaced = _replace_with_retries(tmp_path, path)
        if replaced:
            return
        # Direct-write fallback: reliable artifact presence is more important
        # here than crash-proof atomicity.  Re-run the same writer against the
        # final path, then remove the abandoned temp artifact.
        with path.open("w", encoding="utf-8", newline="") as final:
            write_fn(final)
            final.flush()
            os.fsync(final.fileno())
        _cleanup_tmp(tmp_path)
    except Exception:
        if not tmp_closed:
            try:
                os.close(fd)
            except OSError:
                pass
        _cleanup_tmp(tmp_path)
        raise


def atomic_write_text(path: Path, text: str) -> None:
    def write_fn(handle: Any) -> None:
        handle.write(text)

    _safe_write_file(path, write_fn)


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    atomic_write_text(path, rendered)


def atomic_write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    def write_fn(handle: Any) -> None:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: _csv_value(row.get(col)) for col in columns})

    _safe_write_file(path, write_fn)


def atomic_write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    def write_fn(handle: Any) -> None:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, default=str, separators=(",", ":")) + "\n")

    _safe_write_file(path, write_fn)

def _csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(value, sort_keys=True)
    return value


def normalize_condition_id(value: Any) -> str:
    if not isinstance(value, str):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "condition_id must be a string")
    out = value.strip().lower()
    if not CONDITION_RE.match(out):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "malformed condition_id", details={"value": value})
    return out


def normalize_tx_hash(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "tx_hash must be a non-empty string")
    out = value.strip().lower()
    if out.startswith("0x") and len(out) != 66:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "malformed tx_hash", details={"value": value})
    return out


def canonical_int_string(value: Any, *, field_name: str, allow_binary_float_strings: bool = False) -> str:
    if isinstance(value, bool):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must not be bool")
    if isinstance(value, float):
        raise DiagnosticHalt(STOP_PRECISION_LOSS, f"{field_name} was float-typed")
    if isinstance(value, int):
        if value < 0:
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must be non-negative")
        return str(value)
    if not isinstance(value, str):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must be int-like string")
    s = value.strip()
    if not s:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} is blank")
    if SCI_NOTATION_RE.match(s):
        raise DiagnosticHalt(STOP_PRECISION_LOSS, f"{field_name} uses scientific notation")
    if allow_binary_float_strings and s in {"0.0", "1.0"}:
        return s[0]
    if not re.fullmatch(r"\d+", s):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} is not a safe integer string")
    return str(int(s))


def normalize_outcome_index(value: Any) -> str:
    if isinstance(value, float):
        if value in (0.0, 1.0):
            return str(int(value))
        if value.is_integer():
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "outcome_index must normalize to 0 or 1")
        raise DiagnosticHalt(STOP_PRECISION_LOSS, "outcome_index float must be exact 0.0 or 1.0")
    out = canonical_int_string(value, field_name="outcome_index", allow_binary_float_strings=True)
    if out not in {"0", "1"}:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "outcome_index must normalize to 0 or 1")
    return out


def normalize_side(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "side must be a non-empty string")
    return value.strip().upper()


def normalize_decimal(value: Any, *, field_name: str) -> str:
    if isinstance(value, bool):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must not be bool")
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must be finite")
        dec = Decimal(str(value))
    else:
        try:
            dec = Decimal(str(value).strip())
        except (InvalidOperation, AttributeError):
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} is not numeric") from None
    if not dec.is_finite():
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must be finite")
    if dec < 0:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must be non-negative")
    normalized = dec.normalize()
    if normalized == Decimal("-0"):
        normalized = Decimal("0")
    return format(normalized, "f")


def parse_timestamp(value: Any, *, field_name: str) -> tuple[str, int, str]:
    """Return (UTC ISO string, epoch_ms, unit)."""
    if isinstance(value, bool):
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} must not be bool")
    if isinstance(value, datetime):
        dt = _ensure_utc(value)
        return _format_utc(dt), _epoch_ms(dt), "datetime"
    if pd is not None and hasattr(pd, "Timestamp") and isinstance(value, pd.Timestamp):
        dt = _ensure_utc(value.to_pydatetime())
        return _format_utc(dt), _epoch_ms(dt), "datetime"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not value.is_integer():
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} numeric timestamp must be integer")
        return _parse_numeric_timestamp(str(int(value)), field_name=field_name)
    if isinstance(value, str):
        s = value.strip()
        if not s:
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} is blank")
        if re.fullmatch(r"\d+", s):
            return _parse_numeric_timestamp(s, field_name=field_name)
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        if s.endswith(" UTC"):
            s = s[:-4] + "+00:00"
        try:
            dt = datetime.fromisoformat(s)
        except ValueError:
            if pd is None:
                raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} timestamp parse failed") from None
            try:
                ts = pd.to_datetime(value, utc=True, errors="raise")
                dt = ts.to_pydatetime()
            except Exception:
                raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} timestamp parse failed") from None
        dt = _ensure_utc(dt)
        return _format_utc(dt), _epoch_ms(dt), "iso"
    raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} unsupported timestamp type")


def _parse_numeric_timestamp(value: str, *, field_name: str) -> tuple[str, int, str]:
    ivalue = int(value)
    # Seconds in a modern Unix timestamp are 10 digits; milliseconds are 13.
    if 1_000_000_000 <= ivalue <= 4_102_444_800:
        dt = datetime.fromtimestamp(ivalue, tz=timezone.utc)
        return _format_utc(dt), _epoch_ms(dt), "seconds"
    if 1_000_000_000_000 <= ivalue <= 4_102_444_800_000:
        dt = datetime.fromtimestamp(ivalue / 1000, tz=timezone.utc)
        return _format_utc(dt), _epoch_ms(dt), "milliseconds"
    raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, f"{field_name} timestamp unit unsupported")


def _ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _format_utc(dt: datetime) -> str:
    dt = dt.astimezone(timezone.utc)
    if dt.microsecond:
        return dt.isoformat().replace("+00:00", "Z")
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _epoch_ms(dt: datetime) -> int:
    return int(round(dt.astimezone(timezone.utc).timestamp() * 1000))


def row_sha256(row: Mapping[str, Any]) -> str:
    raw = json.dumps(row, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def composite_key(
    condition_id: str,
    tx_hash: str,
    token_id: str,
    outcome_index: str,
    side: str,
    price_norm: str,
    size_norm: str,
    epoch_ms: int,
) -> str:
    parts = [condition_id, tx_hash, token_id, outcome_index, side, price_norm, size_norm, str(epoch_ms)]
    return "|".join(parts)


def _api_get(raw: Mapping[str, Any], logical_name: str) -> Any:
    for field in API_FIELD_ALIASES[logical_name]:
        if field in raw:
            return raw[field]
    raise DiagnosticHalt(
        STOP_SCHEMA_DEVIATION,
        "API row missing mapped field",
        details={"field": logical_name, "accepted_fields": list(API_FIELD_ALIASES[logical_name])},
    )


def normalize_api_row(
    raw: Mapping[str, Any],
    *,
    query_condition_id: str,
    query_mode: str,
    page_number: int,
    page_limit: int,
    row_number_in_page: int,
    retrieved_at_utc: str,
) -> dict[str, Any]:
    condition_original = _api_get(raw, "condition_id")
    tx_hash_original = _api_get(raw, "tx_hash")
    token_original = _api_get(raw, "token_id")
    outcome_index_original = _api_get(raw, "outcome_index")
    side_original = _api_get(raw, "side")
    price_original = _api_get(raw, "price")
    size_original = _api_get(raw, "size")
    timestamp_original = _api_get(raw, "timestamp")

    condition_id = normalize_condition_id(condition_original)
    expected_condition = normalize_condition_id(query_condition_id)
    if condition_id != expected_condition:
        raise DiagnosticHalt(
            STOP_SCHEMA_DEVIATION,
            "API row condition does not match query condition",
            details={"row_condition": condition_id, "query_condition": expected_condition},
        )
    tx_hash = normalize_tx_hash(tx_hash_original)
    token_id = canonical_int_string(token_original, field_name="token_id")
    outcome_index = normalize_outcome_index(outcome_index_original)
    side = normalize_side(side_original)
    price_norm = normalize_decimal(price_original, field_name="price")
    size_norm = normalize_decimal(size_original, field_name="size")
    ts_utc, ts_epoch_ms, ts_unit = parse_timestamp(timestamp_original, field_name="timestamp")
    ckey = composite_key(condition_id, tx_hash, token_id, outcome_index, side, price_norm, size_norm, ts_epoch_ms)
    return {
        "query_mode": query_mode,
        "query_condition_id": expected_condition,
        "page_number": page_number,
        "page_limit": page_limit,
        "retrieved_at_utc": retrieved_at_utc,
        "row_number_in_page": row_number_in_page,
        "raw_json_sha256": row_sha256(raw),
        "condition_id_original": condition_original,
        "tx_hash_original": tx_hash_original,
        "token_id_original": token_original,
        "outcome_index_original": outcome_index_original,
        "side_original": side_original,
        "price_original": price_original,
        "size_original": size_original,
        "timestamp_original": timestamp_original,
        "condition_id": condition_id,
        "tx_hash": tx_hash,
        "token_id": token_id,
        "outcome_index": outcome_index,
        "side": side,
        "price_norm": price_norm,
        "size_norm": size_norm,
        "timestamp_utc": ts_utc,
        "timestamp_epoch_ms": ts_epoch_ms,
        "timestamp_unit": ts_unit,
        "composite_key": ckey,
    }


def normalize_local_row(row: Mapping[str, Any]) -> dict[str, Any]:
    missing = sorted(col for col in LOCAL_REQUIRED_COLUMNS if col not in row)
    if missing:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "local row missing required fields", details={"missing": missing})
    condition_original = row["condition_id"]
    tx_hash_original = row["tx_hash"]
    token_original = row["token_id"]
    outcome_index_original = row["outcome_index"]
    side_original = row["side"]
    price_original = row["price"]
    size_original = row["size_usdc"]
    traded_at_original = row["traded_at"]

    condition_id = normalize_condition_id(condition_original)
    tx_hash = normalize_tx_hash(tx_hash_original)
    token_id = canonical_int_string(token_original, field_name="token_id")
    outcome_index = normalize_outcome_index(outcome_index_original)
    side = normalize_side(side_original)
    price_norm = normalize_decimal(price_original, field_name="price")
    size_norm = normalize_decimal(size_original, field_name="size")
    ts_utc, ts_epoch_ms, _unit = parse_timestamp(traded_at_original, field_name="traded_at")
    ckey = composite_key(condition_id, tx_hash, token_id, outcome_index, side, price_norm, size_norm, ts_epoch_ms)
    return {
        "condition_id_original": condition_original,
        "tx_hash_original": tx_hash_original,
        "token_id_original": token_original,
        "outcome_index_original": outcome_index_original,
        "side_original": side_original,
        "price_original": price_original,
        "size_original": size_original,
        "traded_at_original": traded_at_original,
        "trade_id_original": row.get("trade_id"),
        "wallet_original": row.get("wallet"),
        "outcome_original": row.get("outcome"),
        "condition_id": condition_id,
        "tx_hash": tx_hash,
        "token_id": token_id,
        "outcome_index": outcome_index,
        "side": side,
        "price_norm": price_norm,
        "size_norm": size_norm,
        "traded_at_utc": ts_utc,
        "traded_at_epoch_ms": ts_epoch_ms,
        "composite_key": ckey,
    }


def extract_manifest_conditions(manifest: Any) -> list[str]:
    candidates: Any = None
    if isinstance(manifest, list):
        candidates = manifest
    elif isinstance(manifest, dict):
        for key in ("conditions", "condition_ids", "manifest_conditions", "b0_conditions"):
            if key in manifest:
                candidates = manifest[key]
                break
    if not isinstance(candidates, list):
        raise DiagnosticHalt(STOP_SAMPLE_SCOPE_EXCEEDED, "manifest must contain a condition list")

    out: list[str] = []
    for item in candidates:
        if isinstance(item, str):
            value = item
        elif isinstance(item, Mapping) and "condition_id" in item:
            value = item["condition_id"]
        else:
            raise DiagnosticHalt(STOP_SAMPLE_SCOPE_EXCEEDED, "manifest condition entry is unsupported")
        condition_id = normalize_condition_id(value)
        if condition_id == ZERO64:
            raise DiagnosticHalt(STOP_SAMPLE_SCOPE_EXCEEDED, "placeholder condition_id is not allowed")
        out.append(condition_id)

    if len(out) != EXPECTED_MANIFEST_CONDITIONS:
        raise DiagnosticHalt(
            STOP_SAMPLE_SCOPE_EXCEEDED,
            "manifest must contain exactly the fixed B0 10-condition list",
            details={"count": len(out)},
        )
    if len(set(out)) != len(out):
        raise DiagnosticHalt(STOP_SAMPLE_SCOPE_EXCEEDED, "manifest condition list contains duplicates")
    return out


def load_manifest(path: Path) -> tuple[dict[str, Any], list[str]]:
    if not path.exists():
        raise DiagnosticHalt(STOP_SAMPLE_SCOPE_EXCEEDED, "source B0 manifest is missing", details={"path": str(path)})
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    conditions = extract_manifest_conditions(payload)
    if isinstance(payload, dict):
        manifest = dict(payload)
    else:
        manifest = {"conditions": payload}
    manifest["diagnostic_manifest_attestation"] = {
        "source_path": str(path),
        "condition_count": len(conditions),
        "condition_sha256": hashlib.sha256("\n".join(conditions).encode("utf-8")).hexdigest(),
        "fixed_same_10_condition_design": True,
    }
    return manifest, conditions


def ensure_output_path_safe(out_dir: Path) -> None:
    parts_lower = {part.lower() for part in out_dir.parts}
    if "prices" in parts_lower:
        raise DiagnosticHalt(STOP_NO_WRITE_PATH, "diagnostic output path must not be under a prices directory")


def load_local_rows_default(data_root: Path, conditions: Sequence[str]) -> Any:
    from pm_research.data.store import Store

    if pd is None:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "pandas is required to load local rows")
    trades = Store(data_root).load_trades()
    if "condition_id" not in trades.columns:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "local trades missing condition_id")
    normalized_conditions = set(conditions)
    frame = trades[trades["condition_id"].astype(str).str.lower().isin(normalized_conditions)].copy()
    return frame


def normalize_local_frame(local_obj: Any, conditions: Sequence[str]) -> list[dict[str, Any]]:
    if pd is not None and isinstance(local_obj, pd.DataFrame):
        records = local_obj.to_dict(orient="records")
    elif isinstance(local_obj, list):
        records = local_obj
    else:
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "local loader returned unsupported type")
    allowed = set(conditions)
    out: list[dict[str, Any]] = []
    for rec in records:
        normalized = normalize_local_row(rec)
        if normalized["condition_id"] in allowed:
            out.append(normalized)
    return out


def enforce_row_cap(row_count: int) -> None:
    if row_count > PRIMARY_API_ROW_LEDGER_CAP:
        raise DiagnosticHalt(
            STOP_ROW_LEDGER_CAP_EXCEEDED,
            "API row ledger cap exceeded",
            details={"row_count": row_count, "cap": PRIMARY_API_ROW_LEDGER_CAP},
        )


def _raw_row_record(
    raw: Mapping[str, Any],
    *,
    condition_id: str,
    query_mode: str,
    page_number: int,
    row_number_in_page: int,
) -> dict[str, Any]:
    sha = row_sha256(raw)
    return {
        "query_condition_id": condition_id,
        "query_mode": query_mode,
        "page_number": page_number,
        "row_number_in_page": row_number_in_page,
        "raw_json_sha256": sha,
        "raw_json": json.dumps(raw, sort_keys=True, default=str, separators=(",", ":")),
    }


def _schema_error_record(
    *,
    condition_id: str,
    query_mode: str,
    page_number: int,
    row_number_in_page: int,
    raw_json_sha256: str | None,
    error: DiagnosticHalt,
) -> dict[str, Any]:
    return {
        "condition_id": condition_id,
        "query_condition_id": condition_id,
        "query_mode": query_mode,
        "page_number": page_number,
        "row_number_in_page": row_number_in_page,
        "raw_json_sha256": raw_json_sha256 or "",
        "error_code": error.code,
        "error_message": error.message,
        "error_details_json": json.dumps(error.details, sort_keys=True, default=str),
    }


def _set_cap_halt(
    artifacts: DiagnosticArtifacts,
    *,
    condition_id: str,
    query_mode: str,
    page_number: int,
    row_number_in_page: int,
) -> None:
    details = {
        "condition_id": condition_id,
        "query_mode": query_mode,
        "page_number": page_number,
        "row_number_in_page": row_number_in_page,
        "cap": PRIMARY_API_ROW_LEDGER_CAP,
        "current_count": len(artifacts.raw_api_rows),
    }
    artifacts.halt_code = STOP_ROW_LEDGER_CAP_EXCEEDED
    artifacts.halt_message = "API row ledger cap exceeded before accepting row"
    artifacts.halt_details = details
    artifacts.row_cap_status = details


def fetch_and_capture_condition(
    condition_id: str,
    *,
    fetch_page: FetchPageFn,
    page_limit: int,
    max_pages: int,
    artifacts: DiagnosticArtifacts,
    query_mode: str,
    taker_only: bool | None,
) -> ConditionPagination:
    pagination = ConditionPagination(condition_id=condition_id)
    for page_number in range(max_pages):
        result = fetch_page(condition_id, page_number, page_limit, taker_only)
        if result.rate_limited or result.status_code == 429:
            raise DiagnosticHalt(STOP_RATE_LIMIT_HIT, "rate limit returned by page fetch")
        if result.status_code >= 400:
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "API page fetch failed", details={"status": result.status_code})
        rows = list(result.rows)
        pagination.pages_fetched += 1
        pagination.page_counts.append(len(rows))
        retrieved = utc_now_iso()
        page_record = {
            "query_condition_id": condition_id,
            "query_mode": query_mode,
            "page_number": page_number,
            "page_limit": page_limit,
            "retrieved_at_utc": retrieved,
            "row_count_reported": len(rows),
            "raw_row_sha256": [],
            "cap_truncated": False,
            "cap_status": None,
        }
        for idx, raw in enumerate(rows):
            if len(artifacts.raw_api_rows) >= PRIMARY_API_ROW_LEDGER_CAP:
                _set_cap_halt(
                    artifacts,
                    condition_id=condition_id,
                    query_mode=query_mode,
                    page_number=page_number,
                    row_number_in_page=idx,
                )
                page_record["cap_truncated"] = True
                page_record["cap_status"] = dict(artifacts.row_cap_status or {})
                artifacts.raw_api_pages.append(page_record)
                raise DiagnosticHalt(
                    STOP_ROW_LEDGER_CAP_EXCEEDED,
                    "API row ledger cap exceeded before accepting row",
                    details=dict(artifacts.row_cap_status or {}),
                )
            raw_record = _raw_row_record(
                raw,
                condition_id=condition_id,
                query_mode=query_mode,
                page_number=page_number,
                row_number_in_page=idx,
            )
            artifacts.raw_api_rows.append(raw_record)
            page_record["raw_row_sha256"].append(raw_record["raw_json_sha256"])
            try:
                artifacts.api_rows.append(
                    normalize_api_row(
                        raw,
                        query_condition_id=condition_id,
                        query_mode=query_mode,
                        page_number=page_number,
                        page_limit=page_limit,
                        row_number_in_page=idx,
                        retrieved_at_utc=retrieved,
                    )
                )
            except DiagnosticHalt as exc:
                if exc.code not in {STOP_SCHEMA_DEVIATION, STOP_PRECISION_LOSS}:
                    raise
                artifacts.schema_blocked_conditions.add(condition_id)
                artifacts.schema_errors.append(
                    _schema_error_record(
                        condition_id=condition_id,
                        query_mode=query_mode,
                        page_number=page_number,
                        row_number_in_page=idx,
                        raw_json_sha256=raw_record["raw_json_sha256"],
                        error=exc,
                    )
                )
                pagination.status = "SCHEMA_BLOCKED"
        artifacts.raw_api_pages.append(page_record)
        if pagination.status == "SCHEMA_BLOCKED":
            return pagination
        if len(rows) < page_limit:
            pagination.status = PAGINATION_COMPLETE
            return pagination
    pagination.status = PAGINATION_PARTIAL
    return pagination


def compute_takeronly_probe_status(
    conditions: Sequence[str],
    *,
    fetch_page: FetchPageFn,
    page_limit: int,
    max_pages: int,
    artifacts: DiagnosticArtifacts,
    probe_condition_count: int = DEFAULT_TAKERONLY_PROBE_CONDITIONS,
) -> dict[str, dict[str, int | str | None]]:
    results: dict[str, dict[str, int | str | None]] = {}
    for condition_id in list(conditions)[:probe_condition_count]:
        before = len(artifacts.raw_api_rows)
        true_pag = fetch_and_capture_condition(
            condition_id,
            fetch_page=fetch_page,
            page_limit=page_limit,
            max_pages=max_pages,
            artifacts=artifacts,
            query_mode=QUERY_MODE_TAKERONLY_TRUE,
            taker_only=True,
        )
        mid = len(artifacts.raw_api_rows)
        false_pag = fetch_and_capture_condition(
            condition_id,
            fetch_page=fetch_page,
            page_limit=page_limit,
            max_pages=max_pages,
            artifacts=artifacts,
            query_mode=QUERY_MODE_TAKERONLY_FALSE,
            taker_only=False,
        )
        after = len(artifacts.raw_api_rows)
        true_count = mid - before
        false_count = after - mid
        status = "MEASURED"
        if true_pag.status == PAGINATION_PARTIAL or false_pag.status == PAGINATION_PARTIAL:
            status = "PARTIAL_RETRIEVAL"
        if true_pag.status == "SCHEMA_BLOCKED" or false_pag.status == "SCHEMA_BLOCKED":
            status = "SCHEMA_BLOCKED"
        results[condition_id] = {
            "takeronly_true_count": true_count,
            "takeronly_false_count": false_count,
            "takeronly_delta": false_count - true_count,
            "takeronly_status": status,
        }
    return results

def pair_rows(
    api_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    conditions: Sequence[str],
    *,
    local_bounds: Mapping[str, tuple[int | None, int | None]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    api_by_key: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    local_by_key: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in api_rows:
        if row.get("query_mode") == QUERY_MODE_PRIMARY:
            api_by_key[str(row["composite_key"])].append(row)
    for row in local_rows:
        local_by_key[str(row["composite_key"])].append(row)

    matched_api_ids: set[int] = set()
    matched_local_ids: set[int] = set()
    matched_in_window_by_condition: Counter[str] = Counter()
    for key, api_bucket in api_by_key.items():
        local_bucket = local_by_key.get(key, [])
        pair_count = min(len(api_bucket), len(local_bucket))
        for idx in range(pair_count):
            api_row = api_bucket[idx]
            local_row = local_bucket[idx]
            matched_api_ids.add(id(api_row))
            matched_local_ids.add(id(local_row))
            condition_id = str(api_row["condition_id"])
            if is_api_row_in_local_window(api_row, local_bounds.get(condition_id)):
                matched_in_window_by_condition[condition_id] += 1

    unmatched_api = [row for bucket in api_by_key.values() for row in bucket if id(row) not in matched_api_ids]
    unmatched_local = [row for bucket in local_by_key.values() for row in bucket if id(row) not in matched_local_ids]
    local_unmatched_tx = {(str(row["condition_id"]), str(row["tx_hash"])) for row in unmatched_local}
    api_unmatched_tx = {(str(row["condition_id"]), str(row["tx_hash"])) for row in unmatched_api}
    ambiguous_tx = local_unmatched_tx & api_unmatched_tx

    mismatches: list[dict[str, Any]] = []
    for row in unmatched_api:
        condition_id = str(row["condition_id"])
        mismatch_type = "TX_HASH_AMBIGUOUS" if (condition_id, str(row["tx_hash"])) in ambiguous_tx else "API_ONLY"
        in_window = is_api_row_in_local_window(row, local_bounds.get(condition_id))
        mismatches.append(mismatch_from_api(row, mismatch_type=mismatch_type, in_window=in_window))
    for row in unmatched_local:
        condition_id = str(row["condition_id"])
        mismatch_type = "TX_HASH_AMBIGUOUS" if (condition_id, str(row["tx_hash"])) in ambiguous_tx else "LOCAL_ONLY"
        in_window = is_local_row_in_local_window(row, local_bounds.get(condition_id))
        mismatches.append(mismatch_from_local(row, mismatch_type=mismatch_type, in_window=in_window))
    return mismatches, dict(matched_in_window_by_condition)


def is_api_row_in_local_window(row: Mapping[str, Any], bounds: tuple[int | None, int | None] | None) -> bool:
    if bounds is None or bounds[0] is None or bounds[1] is None:
        return False
    ts = int(row["timestamp_epoch_ms"])
    start = bounds[0] - TAU_SECONDS * 1000
    end = bounds[1] + TAU_SECONDS * 1000
    return start <= ts <= end


def is_local_row_in_local_window(row: Mapping[str, Any], bounds: tuple[int | None, int | None] | None) -> bool:
    if bounds is None or bounds[0] is None or bounds[1] is None:
        return False
    ts = int(row["traded_at_epoch_ms"])
    return bounds[0] <= ts <= bounds[1]


def mismatch_from_api(row: Mapping[str, Any], *, mismatch_type: str, in_window: bool) -> dict[str, Any]:
    return {
        "condition_id": row["condition_id"],
        "mismatch_type": mismatch_type,
        "row_source": "API",
        "query_mode": row.get("query_mode", ""),
        "tx_hash": row["tx_hash"],
        "token_id": row["token_id"],
        "outcome_index": row["outcome_index"],
        "side": row["side"],
        "price_norm": row["price_norm"],
        "size_norm": row["size_norm"],
        "timestamp_utc": row["timestamp_utc"],
        "composite_key": row["composite_key"],
        "in_overlap_window": bool(in_window),
    }


def mismatch_from_local(row: Mapping[str, Any], *, mismatch_type: str, in_window: bool) -> dict[str, Any]:
    return {
        "condition_id": row["condition_id"],
        "mismatch_type": mismatch_type,
        "row_source": "LOCAL",
        "query_mode": "",
        "tx_hash": row["tx_hash"],
        "token_id": row["token_id"],
        "outcome_index": row["outcome_index"],
        "side": row["side"],
        "price_norm": row["price_norm"],
        "size_norm": row["size_norm"],
        "timestamp_utc": row["traded_at_utc"],
        "composite_key": row["composite_key"],
        "in_overlap_window": bool(in_window),
    }


def compute_bounds(
    conditions: Sequence[str],
    api_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, tuple[int | None, int | None]], dict[str, tuple[int | None, int | None]]]:
    local_bounds: dict[str, tuple[int | None, int | None]] = {}
    api_bounds: dict[str, tuple[int | None, int | None]] = {}
    for condition_id in conditions:
        l_times = [int(row["traded_at_epoch_ms"]) for row in local_rows if row["condition_id"] == condition_id]
        a_times = [
            int(row["timestamp_epoch_ms"])
            for row in api_rows
            if row["condition_id"] == condition_id and row.get("query_mode") == QUERY_MODE_PRIMARY
        ]
        local_bounds[condition_id] = (min(l_times), max(l_times)) if l_times else (None, None)
        api_bounds[condition_id] = (min(a_times), max(a_times)) if a_times else (None, None)
    return local_bounds, api_bounds


def epoch_ms_to_iso(value: int | None) -> str | None:
    if value is None:
        return None
    return _format_utc(datetime.fromtimestamp(value / 1000, tz=timezone.utc))


def classify_condition(
    *,
    condition_id: str,
    api_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    mismatches: Sequence[Mapping[str, Any]],
    matched_in_window_count: int,
    pagination_status: str,
    local_bounds: tuple[int | None, int | None],
    api_bounds: tuple[int | None, int | None],
    schema_blocked: bool,
    artifact_status: str,
) -> dict[str, Any]:
    condition_api = [row for row in api_rows if row["condition_id"] == condition_id and row.get("query_mode") == QUERY_MODE_PRIMARY]
    condition_local = [row for row in local_rows if row["condition_id"] == condition_id]
    timestamp_units = sorted({str(row["timestamp_unit"]) for row in condition_api})

    if local_bounds[0] is None or local_bounds[1] is None:
        window_start = window_end = None
    else:
        window_start = local_bounds[0] - TAU_SECONDS * 1000
        window_end = local_bounds[1] + TAU_SECONDS * 1000

    api_before = api_in = api_after = api_after_sigma = 0
    for row in condition_api:
        ts = int(row["timestamp_epoch_ms"])
        if window_start is None or window_end is None:
            api_after += 0
        elif ts < window_start:
            api_before += 1
        elif ts > window_end:
            api_after += 1
            if local_bounds[1] is not None and ts > local_bounds[1] + SIGMA_SECONDS * 1000:
                api_after_sigma += 1
        else:
            api_in += 1

    condition_mismatches = [row for row in mismatches if row["condition_id"] == condition_id]
    api_only_in = sum(1 for row in condition_mismatches if row["mismatch_type"] == "API_ONLY" and row["in_overlap_window"])
    local_only_in = sum(1 for row in condition_mismatches if row["mismatch_type"] == "LOCAL_ONLY" and row["in_overlap_window"])
    ambiguous_in = sum(
        1 for row in condition_mismatches if row["mismatch_type"] == "TX_HASH_AMBIGUOUS" and row["in_overlap_window"]
    )

    temporal_subflag = ""
    if schema_blocked:
        classification = OVERLAP_SCHEMA_BLOCKED
    elif pagination_status == PAGINATION_PARTIAL:
        classification = OVERLAP_PAGINATION_PARTIAL
    elif local_bounds[0] is None or local_bounds[1] is None:
        classification = NO_TEMPORAL_OVERLAP
        temporal_subflag = "LOCAL_EMPTY"
    elif api_bounds[0] is None or api_bounds[1] is None:
        classification = NO_TEMPORAL_OVERLAP
        temporal_subflag = "API_EMPTY"
    elif api_bounds[1] < local_bounds[0] - TAU_SECONDS * 1000:
        classification = NO_TEMPORAL_OVERLAP
        temporal_subflag = "API_BEFORE_LOCAL_WINDOW"
    elif api_bounds[0] > local_bounds[1] + TAU_SECONDS * 1000:
        classification = NO_TEMPORAL_OVERLAP
        temporal_subflag = "API_AFTER_LOCAL_WINDOW"
    elif (
        artifact_status == API_ARTIFACT_COMPLETE
        and pagination_status == PAGINATION_COMPLETE
        and api_in == matched_in_window_count
        and len(condition_local) == matched_in_window_count
        and api_only_in == 0
        and local_only_in == 0
        and ambiguous_in == 0
    ):
        classification = OVERLAP_MATCHED
    else:
        classification = OVERLAP_API_LOCAL_MISMATCH

    return {
        "condition_id": condition_id,
        "api_row_count": len(condition_api),
        "local_row_count": len(condition_local),
        "local_min_traded_at_utc": epoch_ms_to_iso(local_bounds[0]),
        "local_max_traded_at_utc": epoch_ms_to_iso(local_bounds[1]),
        "api_min_timestamp_utc": epoch_ms_to_iso(api_bounds[0]),
        "api_max_timestamp_utc": epoch_ms_to_iso(api_bounds[1]),
        "api_timestamp_units": ";".join(timestamp_units),
        "pagination_status": pagination_status,
        "api_before_window_count": api_before,
        "api_in_window_count": api_in,
        "api_after_window_count": api_after,
        "api_after_sigma_count": api_after_sigma,
        "matched_in_window_count": matched_in_window_count,
        "api_only_in_window_count": api_only_in,
        "local_only_in_window_count": local_only_in,
        "tx_hash_ambiguous_in_window_count": ambiguous_in,
        "temporal_subflag": temporal_subflag,
        "classification": classification,
    }


def compute_by_condition(
    artifacts: DiagnosticArtifacts,
    *,
    artifact_status: str,
) -> list[dict[str, Any]]:
    local_bounds, api_bounds = compute_bounds(artifacts.manifest_conditions, artifacts.api_rows, artifacts.local_rows)
    mismatches, matched_by_condition = pair_rows(
        artifacts.api_rows,
        artifacts.local_rows,
        artifacts.manifest_conditions,
        local_bounds=local_bounds,
    )
    artifacts.mismatches = mismatches
    rows: list[dict[str, Any]] = []
    for condition_id in artifacts.manifest_conditions:
        pagination = artifacts.pagination.get(condition_id) or ConditionPagination(condition_id=condition_id, status=PAGINATION_PARTIAL)
        base = classify_condition(
            condition_id=condition_id,
            api_rows=artifacts.api_rows,
            local_rows=artifacts.local_rows,
            mismatches=mismatches,
            matched_in_window_count=matched_by_condition.get(condition_id, 0),
            pagination_status=pagination.status,
            local_bounds=local_bounds[condition_id],
            api_bounds=api_bounds[condition_id],
            schema_blocked=condition_id in artifacts.schema_blocked_conditions,
            artifact_status=artifact_status,
        )
        taker_status = artifacts.takeronly_counts.get(condition_id, {})
        base.update(
            {
                "pages_fetched": pagination.pages_fetched,
                "page_row_counts_json": json.dumps(pagination.page_counts),
                "takeronly_true_count": taker_status.get("takeronly_true_count"),
                "takeronly_false_count": taker_status.get("takeronly_false_count"),
                "takeronly_delta": taker_status.get("takeronly_delta"),
                "takeronly_status": taker_status.get("takeronly_status", "NOT_PROBED"),
            }
        )
        rows.append(base)
    artifacts.by_condition = rows
    return rows


def artifact_status_for(out_dir: Path, artifacts: DiagnosticArtifacts) -> str:
    required = [
        out_dir / "manifest_attested.json",
        out_dir / "api_rows.csv",
        out_dir / "api_raw_rows.jsonl",
        out_dir / "api_raw_pages.jsonl",
        out_dir / "schema_errors.csv",
        out_dir / "local_load_provenance.json",
        out_dir / "local_rows.csv",
        out_dir / "mismatches.csv",
        out_dir / "by_condition.csv",
        out_dir / "reconciliation.json",
        out_dir / "summary.md",
    ]
    if artifacts.halt_code is not None:
        return API_ARTIFACT_INCOMPLETE
    if len(artifacts.manifest_conditions) != EXPECTED_MANIFEST_CONDITIONS:
        return API_ARTIFACT_INCOMPLETE
    if len(artifacts.raw_api_rows) > PRIMARY_API_ROW_LEDGER_CAP or len(artifacts.api_rows) > PRIMARY_API_ROW_LEDGER_CAP:
        return API_ARTIFACT_INCOMPLETE
    if any(row.get("cap_truncated") for row in artifacts.raw_api_pages):
        return API_ARTIFACT_INCOMPLETE
    if any((v.get("takeronly_status") in {"PARTIAL_RETRIEVAL", "SCHEMA_BLOCKED"}) for v in artifacts.takeronly_counts.values()):
        return API_ARTIFACT_INCOMPLETE
    if any(not path.exists() for path in required):
        return API_ARTIFACT_INCOMPLETE
    if len(artifacts.by_condition) != len(artifacts.manifest_conditions):
        return API_ARTIFACT_INCOMPLETE
    return API_ARTIFACT_COMPLETE


def reconciliation_summary(artifacts: DiagnosticArtifacts, *, artifact_status: str) -> dict[str, Any]:
    classification_counts = Counter(row["classification"] for row in artifacts.by_condition)
    mismatch_counts = Counter(row["mismatch_type"] for row in artifacts.mismatches)
    return {
        "stage": "OPTION_B_B0_FAILURE_DIAGNOSTIC",
        "artifact_status": artifact_status,
        "halt_code": artifacts.halt_code,
        "halt_message": artifacts.halt_message,
        "halt_details": artifacts.halt_details,
        "row_cap_status": artifacts.row_cap_status,
        "constants": {
            "tau_seconds": TAU_SECONDS,
            "sigma_hours": SIGMA_HOURS,
            "primary_api_row_ledger_cap": PRIMARY_API_ROW_LEDGER_CAP,
            "manifest_condition_count": EXPECTED_MANIFEST_CONDITIONS,
        },
        "counts": {
            "manifest_conditions": len(artifacts.manifest_conditions),
            "api_rows_total_all_query_modes": len(artifacts.api_rows),
            "api_raw_rows_total_all_query_modes": len(artifacts.raw_api_rows),
            "api_rows_primary": sum(1 for row in artifacts.api_rows if row.get("query_mode") == QUERY_MODE_PRIMARY),
            "local_rows": len(artifacts.local_rows),
            "mismatches": len(artifacts.mismatches),
        },
        "classification_counts": dict(sorted(classification_counts.items())),
        "mismatch_counts": dict(sorted(mismatch_counts.items())),
        "pagination_counts": dict(sorted(Counter(p.status for p in artifacts.pagination.values()).items())),
        "takeronly_probe_conditions": len(artifacts.takeronly_counts),
        "guardrails": {
            "condition_scoped_fixed_manifest_only": True,
            "no_downstream_authorization": True,
            "no_gate_change": True,
            "no_store_repair": True,
            "no_scoring": True,
        },
    }


def write_summary_md(path: Path, summary: Mapping[str, Any]) -> None:
    lines = [
        "# Option B B0 Failure Diagnostic summary",
        "",
        f"Artifact status: `{summary['artifact_status']}`",
        f"Halt code: `{summary.get('halt_code')}`",
        "",
        "This is a diagnostic artifact set only. It is not a B1 gate, coverage verdict, build verdict, probe authorization, or gate change.",
        "",
        "## Counts",
        "",
    ]
    for key, value in summary["counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Classifications", ""])
    for key, value in summary["classification_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Guardrails", "", "- Fixed 10-condition manifest only.", "- Diagnostic ledgers only; no downstream work authorized."])
    atomic_write_text(path, "\n".join(lines) + "\n")


def persist_artifacts(out_dir: Path, artifacts: DiagnosticArtifacts, *, final: bool = False) -> dict[str, Any]:
    ensure_output_path_safe(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(out_dir / "manifest_attested.json", artifacts.manifest)
    atomic_write_csv(out_dir / "api_rows.csv", artifacts.api_rows, API_LEDGER_COLUMNS)
    atomic_write_jsonl(out_dir / "api_raw_rows.jsonl", artifacts.raw_api_rows)
    atomic_write_jsonl(out_dir / "api_raw_pages.jsonl", artifacts.raw_api_pages)
    atomic_write_csv(out_dir / "schema_errors.csv", artifacts.schema_errors, SCHEMA_ERROR_COLUMNS)
    atomic_write_json(out_dir / "local_load_provenance.json", artifacts.local_load_provenance)
    atomic_write_csv(out_dir / "local_rows.csv", artifacts.local_rows, LOCAL_LEDGER_COLUMNS)

    # First pass: incomplete status prevents a premature clean label while files are being built.
    compute_by_condition(artifacts, artifact_status=API_ARTIFACT_INCOMPLETE)
    atomic_write_csv(out_dir / "mismatches.csv", artifacts.mismatches, MISMATCH_COLUMNS)
    atomic_write_csv(out_dir / "by_condition.csv", artifacts.by_condition, BY_CONDITION_COLUMNS)
    preliminary = reconciliation_summary(artifacts, artifact_status=API_ARTIFACT_INCOMPLETE)
    atomic_write_json(out_dir / "reconciliation.json", preliminary)
    write_summary_md(out_dir / "summary.md", preliminary)

    if final:
        status = artifact_status_for(out_dir, artifacts)
        compute_by_condition(artifacts, artifact_status=status)
        atomic_write_csv(out_dir / "mismatches.csv", artifacts.mismatches, MISMATCH_COLUMNS)
        atomic_write_csv(out_dir / "by_condition.csv", artifacts.by_condition, BY_CONDITION_COLUMNS)
        final_summary = reconciliation_summary(artifacts, artifact_status=status)
        atomic_write_json(out_dir / "reconciliation.json", final_summary)
        write_summary_md(out_dir / "summary.md", final_summary)
        return final_summary
    return preliminary



def _local_trade_inventory(data_root: Path) -> dict[str, Any]:
    trades_dir = data_root / "trades"
    if not trades_dir.exists():
        return {"trades_dir": str(trades_dir), "exists": False, "file_count": None}
    try:
        files = sorted(trades_dir.glob("*.parquet"))
        return {"trades_dir": str(trades_dir), "exists": True, "file_count": len(files)}
    except OSError as exc:
        return {"trades_dir": str(trades_dir), "exists": True, "file_count": None, "inventory_error": str(exc)}

def run_diagnostic(
    *,
    project_root: Path,
    data_root: Path,
    manifest_path: Path | None = None,
    out_dir: Path | None = None,
    fetch_page: FetchPageFn,
    load_local_rows: LocalRowsLoader = load_local_rows_default,
    page_limit: int = DEFAULT_PAGE_LIMIT,
    max_pages: int = MAX_PAGES_PER_CONDITION,
    max_total_calls: int = MAX_TOTAL_CALLS,
    probe_condition_count: int = DEFAULT_TAKERONLY_PROBE_CONDITIONS,
    primary_taker_only: bool | None = True,
) -> dict[str, Any]:
    if page_limit <= 0 or max_pages <= 0:
        raise DiagnosticHalt(STOP_PAGINATION_UNBOUNDED, "page_limit and max_pages must be positive")
    if max_pages > MAX_PAGES_PER_CONDITION or max_total_calls > MAX_TOTAL_CALLS:
        raise DiagnosticHalt(STOP_CALL_BUDGET_EXCEEDED, "configured caps exceed accepted B0 ceilings")
    manifest_path = manifest_path or project_root / SOURCE_MANIFEST_REL
    out_dir = out_dir or project_root / ARTIFACT_DIR_REL
    ensure_output_path_safe(out_dir)
    manifest, conditions = load_manifest(manifest_path)
    max_calls_needed = len(conditions) * max_pages + min(probe_condition_count, len(conditions)) * max_pages * 2
    if max_calls_needed > max_total_calls:
        raise DiagnosticHalt(
            STOP_CALL_BUDGET_EXCEEDED,
            "preflight call budget would be exceeded",
            details={"calls_needed": max_calls_needed, "max_total_calls": max_total_calls},
        )

    artifacts = DiagnosticArtifacts(manifest=manifest, manifest_conditions=conditions)
    try:
        local_obj = load_local_rows(data_root, conditions)
        pre_filter_count = len(local_obj) if hasattr(local_obj, "__len__") else None
        artifacts.local_rows = normalize_local_frame(local_obj, conditions)
        artifacts.local_load_provenance = {
            "data_root": str(data_root),
            "loader_name": getattr(load_local_rows, "__name__", type(load_local_rows).__name__),
            "loader_module": getattr(load_local_rows, "__module__", ""),
            "condition_filter_count": len(conditions),
            "condition_filter_sha256": hashlib.sha256("\n".join(conditions).encode("utf-8")).hexdigest(),
            "condition_filter_list": list(conditions),
            "pre_filter_row_count_if_available": pre_filter_count,
            "post_filter_local_row_count": len(artifacts.local_rows),
            "loaded_at_utc": utc_now_iso(),
            "trade_file_inventory": _local_trade_inventory(data_root),
        }
        persist_artifacts(out_dir, artifacts)

        for condition_id in conditions:
            pagination = fetch_and_capture_condition(
                condition_id,
                fetch_page=fetch_page,
                page_limit=page_limit,
                max_pages=max_pages,
                artifacts=artifacts,
                query_mode=QUERY_MODE_PRIMARY,
                taker_only=primary_taker_only,
            )
            artifacts.pagination[condition_id] = pagination
            persist_artifacts(out_dir, artifacts)

        artifacts.takeronly_counts = compute_takeronly_probe_status(
            conditions,
            fetch_page=fetch_page,
            page_limit=page_limit,
            max_pages=max_pages,
            artifacts=artifacts,
            probe_condition_count=probe_condition_count,
        )
        persist_artifacts(out_dir, artifacts)
        return persist_artifacts(out_dir, artifacts, final=True)
    except DiagnosticHalt as exc:
        artifacts.halt_code = artifacts.halt_code or exc.code
        artifacts.halt_message = artifacts.halt_message or exc.message
        artifacts.halt_details = artifacts.halt_details or dict(exc.details)
        if exc.code == STOP_ROW_LEDGER_CAP_EXCEEDED and artifacts.row_cap_status is None:
            artifacts.row_cap_status = dict(exc.details)
        persist_artifacts(out_dir, artifacts, final=True)
        raise


def _read_csv_dicts(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "required artifact missing", details={"path": str(path)})
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def recompute_from_artifacts(out_dir: Path) -> dict[str, Any]:
    manifest = json.loads((out_dir / "manifest_attested.json").read_text(encoding="utf-8"))
    conditions = extract_manifest_conditions(manifest)
    artifacts = DiagnosticArtifacts(manifest=manifest, manifest_conditions=conditions)
    artifacts.api_rows = _read_csv_dicts(out_dir / "api_rows.csv")
    artifacts.local_rows = _read_csv_dicts(out_dir / "local_rows.csv")
    artifacts.raw_api_rows = _read_jsonl(out_dir / "api_raw_rows.jsonl")
    artifacts.raw_api_pages = _read_jsonl(out_dir / "api_raw_pages.jsonl")
    artifacts.schema_errors = _read_csv_dicts(out_dir / "schema_errors.csv") if (out_dir / "schema_errors.csv").exists() else []
    if (out_dir / "local_load_provenance.json").exists():
        artifacts.local_load_provenance = json.loads((out_dir / "local_load_provenance.json").read_text(encoding="utf-8"))

    previous: dict[str, Any] = {}
    if (out_dir / "reconciliation.json").exists():
        previous = json.loads((out_dir / "reconciliation.json").read_text(encoding="utf-8"))
        artifacts.halt_code = previous.get("halt_code")
        artifacts.halt_message = previous.get("halt_message")
        artifacts.halt_details = previous.get("halt_details")
        artifacts.row_cap_status = previous.get("row_cap_status")

    for err in artifacts.schema_errors:
        cid = err.get("condition_id") or err.get("query_condition_id")
        if cid:
            artifacts.schema_blocked_conditions.add(normalize_condition_id(cid))

    by_rows = _read_csv_dicts(out_dir / "by_condition.csv")
    artifacts.by_condition = list(by_rows)
    for row in by_rows:
        condition_id = normalize_condition_id(row["condition_id"])
        status = row.get("pagination_status") or PAGINATION_PARTIAL
        page_counts_raw = row.get("page_row_counts_json") or "[]"
        try:
            page_counts = json.loads(page_counts_raw)
        except json.JSONDecodeError:
            page_counts = []
        artifacts.pagination[condition_id] = ConditionPagination(
            condition_id=condition_id,
            status=status,
            pages_fetched=int(row.get("pages_fetched") or 0),
            page_counts=list(page_counts),
        )
        artifacts.takeronly_counts[condition_id] = {
            "takeronly_true_count": _maybe_int(row.get("takeronly_true_count")),
            "takeronly_false_count": _maybe_int(row.get("takeronly_false_count")),
            "takeronly_delta": _maybe_int(row.get("takeronly_delta")),
            "takeronly_status": row.get("takeronly_status") or "NOT_PROBED",
        }

    required = [
        "manifest_attested.json",
        "api_rows.csv",
        "api_raw_rows.jsonl",
        "api_raw_pages.jsonl",
        "schema_errors.csv",
        "local_load_provenance.json",
        "local_rows.csv",
        "mismatches.csv",
        "by_condition.csv",
        "reconciliation.json",
        "summary.md",
    ]
    required_missing = [name for name in required if not (out_dir / name).exists()]
    cap_truncated = any(bool(row.get("cap_truncated")) for row in artifacts.raw_api_pages)
    taker_incomplete = any(
        v.get("takeronly_status") in {"PARTIAL_RETRIEVAL", "SCHEMA_BLOCKED"}
        for v in artifacts.takeronly_counts.values()
    )
    if artifacts.halt_code or required_missing or cap_truncated or taker_incomplete:
        status = API_ARTIFACT_INCOMPLETE
    else:
        status = artifact_status_for(out_dir, artifacts)
    compute_by_condition(artifacts, artifact_status=status)
    summary = reconciliation_summary(artifacts, artifact_status=status)
    if required_missing:
        summary["required_missing"] = required_missing
    return summary

def _maybe_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def make_requests_fetcher(endpoint: str, timeout_seconds: int = 30) -> FetchPageFn:
    def fetch_page(condition_id: str, page_number: int, page_limit: int, taker_only: bool | None) -> PageResult:
        import requests

        params: dict[str, Any] = {
            "market": condition_id,
            "limit": page_limit,
            "offset": page_number * page_limit,
        }
        if taker_only is not None:
            params["takerOnly"] = str(taker_only).lower()
        response = requests.get(endpoint, params=params, timeout=timeout_seconds)
        if response.status_code == 429:
            return PageResult(rows=[], status_code=429, rate_limited=True)
        payload = response.json()
        if isinstance(payload, list):
            rows = payload
        elif isinstance(payload, Mapping) and isinstance(payload.get("trades"), list):
            rows = payload["trades"]
        else:
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "unexpected API response envelope")
        return PageResult(rows=list(rows), status_code=response.status_code)

    return fetch_page


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Option B corrected B0 failure diagnostic harness")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--data-root", type=Path, required=False)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--endpoint", default="https://data-api.polymarket.com/trades")
    parser.add_argument("--page-limit", type=int, default=DEFAULT_PAGE_LIMIT)
    parser.add_argument("--max-pages", type=int, default=MAX_PAGES_PER_CONDITION)
    parser.add_argument("--offline-recompute-only", action="store_true")
    parser.add_argument("--authorize-corrected-b0-diagnostic-run", action="store_true")
    parser.add_argument("--allow-polymarket-network", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    out_dir = args.out_dir or args.project_root / ARTIFACT_DIR_REL
    try:
        if args.offline_recompute_only:
            summary = recompute_from_artifacts(out_dir)
            atomic_write_json(out_dir / "offline_recompute_summary.json", summary)
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        if not args.authorize_corrected_b0_diagnostic_run or not args.allow_polymarket_network:
            raise DiagnosticHalt(
                STOP_NOT_AUTHORIZED,
                "network diagnostic run requires fresh explicit authorization and both command-line guard flags",
            )
        if args.data_root is None:
            raise DiagnosticHalt(STOP_SCHEMA_DEVIATION, "--data-root is required for a run")
        fetcher = make_requests_fetcher(args.endpoint)
        summary = run_diagnostic(
            project_root=args.project_root,
            data_root=args.data_root,
            manifest_path=args.manifest,
            out_dir=out_dir,
            fetch_page=fetcher,
            page_limit=args.page_limit,
            max_pages=args.max_pages,
        )
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except DiagnosticHalt as exc:
        payload = {"status": exc.code, "message": exc.message, "details": exc.details}
        print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
