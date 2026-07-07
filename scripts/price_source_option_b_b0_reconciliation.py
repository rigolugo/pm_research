"""Option B Phase B0 mechanical-trust reconciliation pilot.

CODE / TEST ONLY until a later, explicit run authorization is given.

This module implements the Phase B0 mechanics described in
project_context/SPEC_price_source_option_b_data_api_review.md:

- no execution unless two explicit network authorization flags are supplied;
- condition-scoped Data API /trades retrieval only;
- provenance-attested known-good condition manifest validation;
- bounded pagination with typed halts for partial retrieval;
- schema, numeric, timestamp, and identifier precision validation;
- one-to-one API<->local reconciliation using composite trade identity;
- takerOnly cardinality/subset probe;
- reconciliation artifacts only, never a price-series artifact.

It does not use yes_price, 1 - price, 1 - p, or 1 - yes_price. It does not
compute canonical_side_price, score anything, touch wallets/OrdersMatched,
backfill, log_index, P1/P2/P3, or the named-binary gate.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence

import pandas as pd


# ---------------------------------------------------------------------------
# Typed statuses / constants
# ---------------------------------------------------------------------------

PHASE = "OPTION_B_PHASE_B0_MECHANICAL_TRUST"
AUTHORIZED_SCOPE = "OPTION_B_B0_CODE_ONLY_UNLESS_EXPLICITLY_AUTHORIZED"

STATUS_OK = "B0_MECHANICAL_TRUST_PASSED"
STOP_NOT_AUTHORIZED = "STOP_NOT_AUTHORIZED"
STOP_CALL_BUDGET_EXCEEDED = "STOP_CALL_BUDGET_EXCEEDED"
STOP_SAMPLE_SCOPE_EXCEEDED = "STOP_SAMPLE_SCOPE_EXCEEDED"
STOP_PAGINATION_UNBOUNDED = "STOP_PAGINATION_UNBOUNDED"
STOP_PAGINATION_PARTIAL_RETRIEVAL = "STOP_PAGINATION_PARTIAL_RETRIEVAL"
STOP_RATE_LIMIT_HIT = "STOP_RATE_LIMIT_HIT"
STOP_SCHEMA_DEVIATION = "STOP_SCHEMA_DEVIATION"
STOP_PRECISION_LOSS = "STOP_PRECISION_LOSS"
STOP_FORBIDDEN_INFERENCE = "STOP_FORBIDDEN_INFERENCE"
STOP_NO_WRITE_PATH = "STOP_NO_WRITE_PATH"
STOP_API_LOCAL_MISMATCH = "STOP_API_LOCAL_MISMATCH"
STOP_TAKER_ONLY_CARDINALITY_UNRESOLVED = "STOP_TAKER_ONLY_CARDINALITY_UNRESOLVED"

ALLOWED_SUBCLASSES = {"UP_DOWN", "OVER_UNDER", "NAMED_OTHER"}
KNOWN_GOOD_STATUS_ALIASES = {"BOTH_SIDES", "DECISION_PRICE_BOTH_SIDES"}

DEFAULT_API_BASE_URL = "https://data-api.polymarket.com"
DEFAULT_PAGE_LIMIT = 500
DEFAULT_MAX_PAGES_PER_CONDITION = 5
DEFAULT_TOTAL_CALL_BUDGET = 100
DEFAULT_TAKER_ONLY_PROBE_COUNT = 3
MIN_B0_CONDITIONS = 10
MAX_B0_CONDITIONS = 20
MAX_PAGE_LIMIT = 500
MAX_PAGES_PER_CONDITION = 5

CONDITION_ID_RE = re.compile(r"^0x[0-9a-f]{64}$")
SCI_NOTATION_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)[eE][+-]?\d+$")
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|PLACEHOLDER|TEMPLATE|EXAMPLE|DUMMY|REPLACE_ME)\b", re.I)

FORBIDDEN_FIELD_NAMES = {
    "yes_price",
    "one_minus_price",
    "one_minus_yes_price",
    "side_1_from_side_0",
    "synthetic_side_price",
}


class B0Halt(RuntimeError):
    """Typed halt for Phase B0. The status is the result; do not continue."""

    def __init__(self, status: str, message: str, details: Mapping[str, Any] | None = None):
        super().__init__(f"{status}: {message}")
        self.status = status
        self.message = message
        self.details = dict(details or {})

    def to_result(self) -> dict[str, Any]:
        return {
            "phase": PHASE,
            "status": self.status,
            "message": self.message,
            "details": self.details,
            "network_call_attempted": False,
            "no_price_series_persisted": True,
            "named_binary_probe_blocked_untouched": True,
        }


class RateLimitSignal(RuntimeError):
    """Raised by a client when the API returns 429/rate-limit behavior."""


# ---------------------------------------------------------------------------
# Protocols / data models
# ---------------------------------------------------------------------------


class TradesClient(Protocol):
    def fetch_trades(
        self,
        *,
        condition_id: str,
        limit: int,
        offset: int,
        taker_only: bool,
    ) -> Sequence[Mapping[str, Any]]:
        """Return one page of condition-scoped API /trades rows."""


@dataclass(frozen=True)
class ManifestCondition:
    condition_id: str
    subclass: str | None = None
    provenance_status: str = "BOTH_SIDES"


@dataclass(frozen=True)
class ConditionManifest:
    manifest_path: str
    source_artifact: str
    source_verdict: str
    selection_basis: str
    provenance_attestation: str
    conditions: tuple[ManifestCondition, ...]


@dataclass(frozen=True)
class NormalizedTrade:
    source: str
    raw_index: int
    condition_id: str
    token_id: str
    outcome_index: int
    side: str
    price: Decimal
    size: Decimal
    timestamp_ms: int
    tx_hash: str

    def composite_key(self) -> tuple[str, str, int, str, str, str, int]:
        return (
            self.tx_hash,
            self.token_id,
            self.outcome_index,
            self.side,
            decimal_key(self.price),
            decimal_key(self.size),
            self.timestamp_ms,
        )


@dataclass
class PaginationStats:
    condition_id: str
    taker_only: bool
    pages_fetched: int
    rows_fetched: int
    complete: bool
    final_page_size: int


@dataclass
class ConditionReconciliation:
    condition_id: str
    api_count: int
    local_count: int
    matched_count: int
    mismatch_count: int
    mismatches: list[dict[str, Any]] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return self.mismatch_count == 0 and self.matched_count == self.api_count == self.local_count


@dataclass
class TakerOnlyProbeResult:
    condition_id: str
    taker_only_false_count: int
    taker_only_true_count: int
    row_count_delta: int
    true_subset_of_false: bool


@dataclass
class CallBudget:
    max_calls: int
    calls_used: int = 0

    def reserve_one(self, *, condition_id: str, taker_only: bool, page_index: int) -> None:
        if self.calls_used + 1 > self.max_calls:
            raise B0Halt(
                STOP_CALL_BUDGET_EXCEEDED,
                "Phase B0 would exceed its total call budget.",
                {
                    "max_calls": self.max_calls,
                    "calls_used": self.calls_used,
                    "condition_id": condition_id,
                    "taker_only": taker_only,
                    "page_index": page_index,
                },
            )
        self.calls_used += 1


# ---------------------------------------------------------------------------
# Authorization and scope guards
# ---------------------------------------------------------------------------


def require_b0_network_authorization(*, allow_network_option_b_b0: bool, confirm_external_polymarket_data_api: bool) -> None:
    """Require two deliberate flags before any client call is attempted."""

    if not allow_network_option_b_b0 or not confirm_external_polymarket_data_api:
        raise B0Halt(
            STOP_NOT_AUTHORIZED,
            "Phase B0 network execution requires both explicit authorization flags.",
            {
                "allow_network_option_b_b0": allow_network_option_b_b0,
                "confirm_external_polymarket_data_api": confirm_external_polymarket_data_api,
                "required_flags": [
                    "--allow-network-option-b-b0",
                    "--confirm-external-polymarket-data-api",
                ],
            },
        )


def assert_no_forbidden_inference_fields(row: Mapping[str, Any], *, source: str) -> None:
    names = {str(k).strip().lower() for k in row.keys()}
    found = sorted(names & FORBIDDEN_FIELD_NAMES)
    if found:
        raise B0Halt(
            STOP_FORBIDDEN_INFERENCE,
            "Forbidden price-synthesis field encountered.",
            {"source": source, "fields": found},
        )


def assert_output_path_allowed(path: Path) -> None:
    parts = {p.lower() for p in path.parts}
    name = path.name.lower()
    if "prices" in parts or "price_series" in name or "side_price" in name:
        raise B0Halt(
            STOP_NO_WRITE_PATH,
            "Phase B0 may write reconciliation artifacts only; price-series paths are forbidden.",
            {"path": str(path)},
        )


# ---------------------------------------------------------------------------
# Parsing / normalization helpers
# ---------------------------------------------------------------------------


def _is_nullish(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    try:
        return bool(pd.isna(value))
    except Exception:
        return False


def _field(row: Mapping[str, Any], aliases: Sequence[str], *, required: bool, source: str) -> Any:
    for alias in aliases:
        if alias in row and not _is_nullish(row[alias]):
            return row[alias]
    if required:
        raise B0Halt(
            STOP_SCHEMA_DEVIATION,
            "Missing required trade field.",
            {"source": source, "aliases": list(aliases), "available_fields": sorted(map(str, row.keys()))},
        )
    return None


def canonical_condition_id(value: Any, *, source: str) -> str:
    if not isinstance(value, str):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "condition_id must be a string.", {"source": source, "value": repr(value)})
    cid = value.strip().lower()
    if not CONDITION_ID_RE.match(cid):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Malformed condition_id.", {"source": source, "value": value})
    return cid


def canonical_token_id(value: Any, *, source: str) -> str:
    if isinstance(value, bool):
        raise B0Halt(STOP_PRECISION_LOSS, "Boolean token_id is invalid.", {"source": source, "value": repr(value)})
    if isinstance(value, float):
        raise B0Halt(STOP_PRECISION_LOSS, "Float token_id is precision-unsafe.", {"source": source, "value": repr(value)})
    if isinstance(value, int):
        if value < 0:
            raise B0Halt(STOP_SCHEMA_DEVIATION, "Negative token_id is invalid.", {"source": source, "value": value})
        return str(value)
    if not isinstance(value, str):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "token_id must be a string or exact int.", {"source": source, "value": repr(value)})

    token = value.strip()
    if SCI_NOTATION_RE.match(token) or "e" in token.lower():
        raise B0Halt(STOP_PRECISION_LOSS, "Scientific-notation token_id is precision-unsafe.", {"source": source, "value": value})
    if "." in token:
        raise B0Halt(STOP_PRECISION_LOSS, "Decimal token_id is precision-unsafe.", {"source": source, "value": value})
    if not token.isdigit():
        raise B0Halt(STOP_SCHEMA_DEVIATION, "token_id must contain only digits.", {"source": source, "value": value})
    return token.lstrip("0") or "0"


def canonical_outcome_index(value: Any, *, source: str) -> int:
    if isinstance(value, bool):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Boolean outcome_index is invalid.", {"source": source, "value": repr(value)})
    if isinstance(value, int):
        idx = value
    elif isinstance(value, float):
        if not math.isfinite(value) or value not in (0.0, 1.0):
            raise B0Halt(STOP_SCHEMA_DEVIATION, "Invalid float outcome_index.", {"source": source, "value": repr(value)})
        idx = int(value)
    elif isinstance(value, str):
        raw = value.strip()
        if raw not in {"0", "1", "0.0", "1.0"}:
            raise B0Halt(STOP_SCHEMA_DEVIATION, "Invalid string outcome_index.", {"source": source, "value": value})
        idx = int(float(raw))
    else:
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Unsupported outcome_index type.", {"source": source, "value": repr(value)})
    if idx not in (0, 1):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "outcome_index must be 0 or 1.", {"source": source, "value": repr(value)})
    return idx


def parse_decimal(value: Any, *, source: str, field_name: str, min_value: Decimal | None = None, max_value: Decimal | None = None) -> Decimal:
    if isinstance(value, bool):
        raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} must be numeric, not bool.", {"source": source, "value": repr(value)})
    try:
        dec = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError):
        raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} is not numeric.", {"source": source, "value": repr(value)}) from None
    if not dec.is_finite():
        raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} must be finite.", {"source": source, "value": repr(value)})
    if min_value is not None and dec < min_value:
        raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} below allowed range.", {"source": source, "value": repr(value), "min": str(min_value)})
    if max_value is not None and dec > max_value:
        raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} above allowed range.", {"source": source, "value": repr(value), "max": str(max_value)})
    return dec


def decimal_key(value: Decimal) -> str:
    normalized = value.normalize()
    if normalized == 0:
        return "0"
    return format(normalized, "f")


def parse_timestamp_ms(value: Any, *, source: str, field_name: str = "timestamp") -> int:
    if isinstance(value, bool):
        raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} must not be bool.", {"source": source, "value": repr(value)})

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if isinstance(value, float) and not math.isfinite(value):
            raise B0Halt(STOP_SCHEMA_DEVIATION, f"{field_name} must be finite.", {"source": source, "value": repr(value)})
        numeric = float(value)
        if numeric >= 1_000_000_000_000:  # milliseconds since epoch
            return int(numeric)
        if numeric >= 1_000_000_000:  # seconds since epoch
            return int(numeric * 1000)
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Unsupported numeric timestamp unit.", {"source": source, "value": repr(value)})

    if isinstance(value, str):
        raw = value.strip()
        if raw.isdigit():
            return parse_timestamp_ms(int(raw), source=source, field_name=field_name)
        try:
            ts = pd.to_datetime(raw, utc=True)
        except Exception:
            raise B0Halt(STOP_SCHEMA_DEVIATION, "Unparseable timestamp string.", {"source": source, "value": value}) from None
        if pd.isna(ts):
            raise B0Halt(STOP_SCHEMA_DEVIATION, "Unparseable timestamp string.", {"source": source, "value": value})
        return int(ts.value // 1_000_000)

    # pandas Timestamp and datetime-like values
    try:
        ts = pd.to_datetime(value, utc=True)
    except Exception:
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Unsupported timestamp type.", {"source": source, "value": repr(value)}) from None
    if pd.isna(ts):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Unsupported timestamp value.", {"source": source, "value": repr(value)})
    return int(ts.value // 1_000_000)


def normalize_side(value: Any, *, source: str) -> str:
    if not isinstance(value, str):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "side must be a string.", {"source": source, "value": repr(value)})
    side = value.strip().upper()
    if side not in {"BUY", "SELL"}:
        raise B0Halt(STOP_SCHEMA_DEVIATION, "side must be BUY or SELL.", {"source": source, "value": value})
    return side


def normalize_tx_hash(value: Any, *, source: str) -> str:
    if not isinstance(value, str):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "tx_hash must be a string.", {"source": source, "value": repr(value)})
    tx = value.strip().lower()
    if not tx.startswith("0x") or len(tx) < 10:
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Malformed tx_hash.", {"source": source, "value": value})
    return tx


API_ALIASES = {
    "condition_id": ("condition_id", "conditionId", "market", "marketId"),
    "token_id": ("asset", "token_id", "tokenId", "asset_id", "assetId"),
    "outcome_index": ("outcome_index", "outcomeIndex"),
    "side": ("side",),
    "price": ("price",),
    "size": ("size", "amount", "size_usdc", "sizeUsd"),
    "timestamp": ("timestamp", "time", "createdAt", "created_at", "traded_at", "tradedAt"),
    "tx_hash": ("tx_hash", "transactionHash", "transaction_hash", "hash"),
}

LOCAL_ALIASES = {
    "condition_id": ("condition_id",),
    "token_id": ("token_id", "asset", "asset_id"),
    "outcome_index": ("outcome_index",),
    "side": ("side",),
    "price": ("price",),
    "size": ("size_usdc", "size", "amount"),
    "timestamp": ("traded_at", "timestamp", "time"),
    "tx_hash": ("tx_hash", "transactionHash", "transaction_hash"),
}


def normalize_trade_row(
    row: Mapping[str, Any],
    *,
    expected_condition_id: str,
    source: str,
    raw_index: int,
    aliases: Mapping[str, Sequence[str]],
) -> NormalizedTrade:
    assert_no_forbidden_inference_fields(row, source=source)

    cid = canonical_condition_id(_field(row, aliases["condition_id"], required=True, source=source), source=source)
    expected = canonical_condition_id(expected_condition_id, source="expected_condition_id")
    if cid != expected:
        raise B0Halt(
            STOP_SCHEMA_DEVIATION,
            "Trade row belongs to the wrong condition.",
            {"source": source, "expected_condition_id": expected, "observed_condition_id": cid},
        )

    return NormalizedTrade(
        source=source,
        raw_index=raw_index,
        condition_id=cid,
        token_id=canonical_token_id(_field(row, aliases["token_id"], required=True, source=source), source=source),
        outcome_index=canonical_outcome_index(_field(row, aliases["outcome_index"], required=True, source=source), source=source),
        side=normalize_side(_field(row, aliases["side"], required=True, source=source), source=source),
        price=parse_decimal(_field(row, aliases["price"], required=True, source=source), source=source, field_name="price", min_value=Decimal("0"), max_value=Decimal("1")),
        size=parse_decimal(_field(row, aliases["size"], required=True, source=source), source=source, field_name="size", min_value=Decimal("0")),
        timestamp_ms=parse_timestamp_ms(_field(row, aliases["timestamp"], required=True, source=source), source=source),
        tx_hash=normalize_tx_hash(_field(row, aliases["tx_hash"], required=True, source=source), source=source),
    )


def normalize_api_trades(rows: Sequence[Mapping[str, Any]], *, condition_id: str) -> list[NormalizedTrade]:
    return [
        normalize_trade_row(row, expected_condition_id=condition_id, source="api", raw_index=i, aliases=API_ALIASES)
        for i, row in enumerate(rows)
    ]


def _records_from_frame_or_rows(frame_or_rows: Any) -> list[dict[str, Any]]:
    if isinstance(frame_or_rows, pd.DataFrame):
        return frame_or_rows.to_dict("records")
    if isinstance(frame_or_rows, list):
        return [dict(r) for r in frame_or_rows]
    return [dict(r) for r in list(frame_or_rows)]


def normalize_local_trades(frame_or_rows: Any, *, condition_id: str) -> list[NormalizedTrade]:
    expected = canonical_condition_id(condition_id, source="expected_condition_id")
    records = []
    for row in _records_from_frame_or_rows(frame_or_rows):
        if "condition_id" in row and not _is_nullish(row["condition_id"]):
            try:
                if canonical_condition_id(row["condition_id"], source="local_prefilter") != expected:
                    continue
            except B0Halt:
                # Let full validation below raise the correct schema halt if this row is selected.
                pass
        records.append(row)
    return [
        normalize_trade_row(row, expected_condition_id=expected, source="local", raw_index=i, aliases=LOCAL_ALIASES)
        for i, row in enumerate(records)
        if canonical_condition_id(row.get("condition_id", expected), source="local_prefilter") == expected
    ]


# ---------------------------------------------------------------------------
# Manifest and Store handling
# ---------------------------------------------------------------------------


def _normalize_known_good_status(value: Any) -> str:
    if value is None:
        return ""
    raw = str(value).strip().upper()
    if not raw:
        return ""
    # Preserve common S1/S1-ALT diagnostic suffixes as only the leading class token.
    raw = raw.split()[0]
    if raw in KNOWN_GOOD_STATUS_ALIASES:
        return "BOTH_SIDES"
    return raw


def _load_source_csv_status_map(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Provenance source CSV is empty.", {"path": str(path)})

    cid_cols = [c for c in reader.fieldnames or [] if c.lower() == "condition_id"]
    if not cid_cols:
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Provenance source CSV lacks condition_id.", {"path": str(path)})
    cid_col = cid_cols[0]
    status_candidates = ["level_b_class", "decision_price_class", "status", "coverage_class", "provenance_status"]
    status_col = next((c for c in status_candidates if c in (reader.fieldnames or [])), None)
    if status_col is None:
        raise B0Halt(
            STOP_SAMPLE_SCOPE_EXCEEDED,
            "Provenance source CSV lacks a recognized known-good status column.",
            {"path": str(path), "available_fields": reader.fieldnames},
        )

    out: dict[str, str] = {}
    for row in rows:
        cid = canonical_condition_id(row[cid_col], source="manifest_source_csv")
        out[cid] = _normalize_known_good_status(row.get(status_col))
    return out


def load_condition_manifest(
    path: str | Path,
    *,
    provenance_source_csv: str | Path | None = None,
    min_conditions: int = MIN_B0_CONDITIONS,
    max_conditions: int = MAX_B0_CONDITIONS,
) -> ConditionManifest:
    manifest_path = Path(path)
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Manifest must be a JSON object.", {"path": str(manifest_path)})

    source_artifact = str(data.get("source_artifact", "")).strip()
    source_verdict = str(data.get("source_verdict", "")).strip()
    selection_basis = str(data.get("selection_basis", "")).strip()
    attestation = str(data.get("provenance_attestation", data.get("provenance", ""))).strip()

    provenance_text = "\n".join([source_artifact, source_verdict, selection_basis, attestation])
    if not source_artifact or not source_verdict or not selection_basis or not attestation:
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Manifest lacks required provenance fields.", {"path": str(manifest_path)})
    if PLACEHOLDER_RE.search(provenance_text):
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Manifest provenance contains placeholder/template text.", {"path": str(manifest_path)})
    if "BOTH" not in selection_basis.upper() and "DECISION_PRICE_BOTH_SIDES" not in selection_basis.upper():
        raise B0Halt(
            STOP_SAMPLE_SCOPE_EXCEEDED,
            "Manifest selection_basis must attest to accepted BOTH_SIDES known-good rows.",
            {"selection_basis": selection_basis},
        )

    raw_conditions = data.get("conditions")
    if not isinstance(raw_conditions, list):
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Manifest conditions must be a list.", {"path": str(manifest_path)})
    if len(raw_conditions) < min_conditions or len(raw_conditions) > max_conditions:
        raise B0Halt(
            STOP_SAMPLE_SCOPE_EXCEEDED,
            "Manifest condition count is outside Phase B0 bounds.",
            {"count": len(raw_conditions), "min": min_conditions, "max": max_conditions},
        )

    source_status_map: dict[str, str] | None = None
    if provenance_source_csv is not None:
        source_status_map = _load_source_csv_status_map(Path(provenance_source_csv))

    seen: set[str] = set()
    conditions: list[ManifestCondition] = []
    for i, item in enumerate(raw_conditions):
        if isinstance(item, str):
            raw = {"condition_id": item, "provenance_status": "BOTH_SIDES"}
        elif isinstance(item, dict):
            raw = item
        else:
            raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Manifest condition entry must be string or object.", {"index": i})

        cid = canonical_condition_id(raw.get("condition_id"), source="manifest")
        if cid in seen:
            raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Duplicate manifest condition_id.", {"condition_id": cid})
        seen.add(cid)

        subclass = raw.get("subclass") or raw.get("nb_subclass")
        if subclass is not None:
            subclass = str(subclass).strip().upper()
            if subclass not in ALLOWED_SUBCLASSES:
                raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Manifest condition has invalid subclass.", {"condition_id": cid, "subclass": subclass})

        status = _normalize_known_good_status(
            raw.get("provenance_status")
            or raw.get("level_b_class")
            or raw.get("status")
            or raw.get("decision_price_class")
        )
        if status != "BOTH_SIDES":
            raise B0Halt(
                STOP_SAMPLE_SCOPE_EXCEEDED,
                "Manifest condition is not attested as BOTH_SIDES known-good ground.",
                {"condition_id": cid, "status": status},
            )
        if source_status_map is not None:
            observed = source_status_map.get(cid)
            if observed != "BOTH_SIDES":
                raise B0Halt(
                    STOP_SAMPLE_SCOPE_EXCEEDED,
                    "Manifest condition is not present as BOTH_SIDES in the provenance source CSV.",
                    {"condition_id": cid, "source_status": observed},
                )

        conditions.append(ManifestCondition(condition_id=cid, subclass=subclass, provenance_status="BOTH_SIDES"))

    return ConditionManifest(
        manifest_path=str(manifest_path),
        source_artifact=source_artifact,
        source_verdict=source_verdict,
        selection_basis=selection_basis,
        provenance_attestation=attestation,
        conditions=tuple(conditions),
    )


def load_local_trades_from_store(root: str | Path, condition_ids: Iterable[str]) -> pd.DataFrame:
    """Load local trades through the canonical Store(root) data-root contract."""

    from pm_research.data.store import Store  # imported only when a real run is authorized

    wanted = {canonical_condition_id(cid, source="load_local_trades_from_store") for cid in condition_ids}
    store = Store(Path(root))
    trades = store.load_trades()
    if not isinstance(trades, pd.DataFrame):
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Store(root).load_trades() did not return a DataFrame.", {"root": str(root)})
    if "condition_id" not in trades.columns:
        raise B0Halt(STOP_SCHEMA_DEVIATION, "Store(root).load_trades() lacks condition_id.", {"columns": list(trades.columns)})
    return trades[trades["condition_id"].astype(str).str.lower().isin(wanted)].copy()


# ---------------------------------------------------------------------------
# API client and pagination
# ---------------------------------------------------------------------------


class DataApiTradesClient:
    """Thin condition-scoped client for Polymarket Data API /trades.

    The exact response shape must be re-verified against official docs before any
    future authorized run. This class is not constructed or used unless both B0
    network authorization flags are supplied.
    """

    def __init__(self, *, base_url: str = DEFAULT_API_BASE_URL, timeout_seconds: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def fetch_trades(self, *, condition_id: str, limit: int, offset: int, taker_only: bool) -> Sequence[Mapping[str, Any]]:
        import requests  # imported only in the concrete network client path

        cid = canonical_condition_id(condition_id, source="api_client")
        response = requests.get(
            f"{self.base_url}/trades",
            params={"market": cid, "limit": limit, "offset": offset, "takerOnly": str(taker_only).lower()},
            timeout=self.timeout_seconds,
        )
        if response.status_code == 429:
            raise RateLimitSignal("HTTP 429 from Data API")
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ("trades", "data", "results"):
                value = payload.get(key)
                if isinstance(value, list):
                    return value
        raise B0Halt(
            STOP_SCHEMA_DEVIATION,
            "Data API /trades response does not contain a trade-row list.",
            {"condition_id": cid, "payload_type": type(payload).__name__},
        )


def validate_caps(*, sample_size: int, page_limit: int, max_pages_per_condition: int, total_call_budget: int, taker_only_probe_count: int) -> None:
    if page_limit <= 0 or page_limit > MAX_PAGE_LIMIT:
        raise B0Halt(STOP_CALL_BUDGET_EXCEEDED, "Page limit is outside Phase B0 bounds.", {"page_limit": page_limit, "max": MAX_PAGE_LIMIT})
    if max_pages_per_condition <= 0 or max_pages_per_condition > MAX_PAGES_PER_CONDITION:
        raise B0Halt(
            STOP_PAGINATION_UNBOUNDED,
            "max_pages_per_condition exceeds Phase B0 cap.",
            {"max_pages_per_condition": max_pages_per_condition, "cap": MAX_PAGES_PER_CONDITION},
        )
    if taker_only_probe_count < 0 or taker_only_probe_count > sample_size:
        raise B0Halt(STOP_SAMPLE_SCOPE_EXCEEDED, "Invalid takerOnly probe count.", {"taker_only_probe_count": taker_only_probe_count, "sample_size": sample_size})

    worst_case_calls = (sample_size + taker_only_probe_count) * max_pages_per_condition
    if worst_case_calls > total_call_budget:
        raise B0Halt(
            STOP_CALL_BUDGET_EXCEEDED,
            "Worst-case Phase B0 call plan exceeds total call budget.",
            {
                "sample_size": sample_size,
                "taker_only_probe_count": taker_only_probe_count,
                "max_pages_per_condition": max_pages_per_condition,
                "worst_case_calls": worst_case_calls,
                "total_call_budget": total_call_budget,
            },
        )


def fetch_complete_condition_trades(
    client: TradesClient,
    *,
    condition_id: str,
    limit: int,
    max_pages: int,
    taker_only: bool,
    budget: CallBudget,
) -> tuple[list[Mapping[str, Any]], PaginationStats]:
    cid = canonical_condition_id(condition_id, source="pagination")
    all_rows: list[Mapping[str, Any]] = []
    final_page_size = 0

    for page_index in range(max_pages):
        budget.reserve_one(condition_id=cid, taker_only=taker_only, page_index=page_index)
        offset = page_index * limit
        try:
            page = list(client.fetch_trades(condition_id=cid, limit=limit, offset=offset, taker_only=taker_only))
        except RateLimitSignal as exc:
            raise B0Halt(STOP_RATE_LIMIT_HIT, "Data API rate limit encountered; halt instead of retrying.", {"condition_id": cid}) from exc
        if len(page) > limit:
            raise B0Halt(STOP_SCHEMA_DEVIATION, "Client returned more rows than requested limit.", {"condition_id": cid, "limit": limit, "rows": len(page)})
        final_page_size = len(page)
        all_rows.extend(page)
        if len(page) < limit:
            return all_rows, PaginationStats(cid, taker_only, page_index + 1, len(all_rows), True, final_page_size)

    # The last allowed page was full; completeness is not proven.
    raise B0Halt(
        STOP_PAGINATION_PARTIAL_RETRIEVAL,
        "Last allowed page was full; retrieval is partial and cannot be reconciled as complete.",
        {
            "condition_id": cid,
            "taker_only": taker_only,
            "limit": limit,
            "max_pages": max_pages,
            "rows_fetched": len(all_rows),
        },
    )


# ---------------------------------------------------------------------------
# Reconciliation and takerOnly probe
# ---------------------------------------------------------------------------


def reconcile_trades(*, condition_id: str, api_trades: Sequence[NormalizedTrade], local_trades: Sequence[NormalizedTrade]) -> ConditionReconciliation:
    cid = canonical_condition_id(condition_id, source="reconcile")

    local_by_key: dict[tuple[str, str, int, str, str, str, int], list[NormalizedTrade]] = defaultdict(list)
    local_by_tx: dict[str, list[NormalizedTrade]] = defaultdict(list)
    for local in local_trades:
        local_by_key[local.composite_key()].append(local)
        local_by_tx[local.tx_hash].append(local)

    matched_count = 0
    mismatches: list[dict[str, Any]] = []

    for api in api_trades:
        key = api.composite_key()
        candidates = local_by_key.get(key, [])
        if candidates:
            candidates.pop()
            matched_count += 1
            continue

        if local_by_tx.get(api.tx_hash):
            mismatch_type = "TX_HASH_AMBIGUOUS"
        else:
            mismatch_type = "API_ONLY"
        mismatches.append(
            {
                "condition_id": cid,
                "mismatch_type": mismatch_type,
                "source": "api",
                "api_raw_index": api.raw_index,
                "tx_hash": api.tx_hash,
                "token_id": api.token_id,
                "outcome_index": api.outcome_index,
                "side": api.side,
                "price": decimal_key(api.price),
                "size": decimal_key(api.size),
                "timestamp_ms": api.timestamp_ms,
            }
        )

    for leftovers in local_by_key.values():
        for local in leftovers:
            mismatches.append(
                {
                    "condition_id": cid,
                    "mismatch_type": "LOCAL_ONLY",
                    "source": "local",
                    "local_raw_index": local.raw_index,
                    "tx_hash": local.tx_hash,
                    "token_id": local.token_id,
                    "outcome_index": local.outcome_index,
                    "side": local.side,
                    "price": decimal_key(local.price),
                    "size": decimal_key(local.size),
                    "timestamp_ms": local.timestamp_ms,
                }
            )

    return ConditionReconciliation(
        condition_id=cid,
        api_count=len(api_trades),
        local_count=len(local_trades),
        matched_count=matched_count,
        mismatch_count=len(mismatches),
        mismatches=mismatches,
    )


def verify_taker_only_probe(*, condition_id: str, full_api_trades: Sequence[NormalizedTrade], taker_only_trades: Sequence[NormalizedTrade]) -> TakerOnlyProbeResult:
    full_counts = Counter(t.composite_key() for t in full_api_trades)
    taker_counts = Counter(t.composite_key() for t in taker_only_trades)

    if len(taker_only_trades) > len(full_api_trades):
        raise B0Halt(
            STOP_TAKER_ONLY_CARDINALITY_UNRESOLVED,
            "takerOnly=true returned more rows than takerOnly=false.",
            {"condition_id": condition_id, "false_count": len(full_api_trades), "true_count": len(taker_only_trades)},
        )

    extra = {key: count for key, count in taker_counts.items() if count > full_counts.get(key, 0)}
    if extra:
        raise B0Halt(
            STOP_TAKER_ONLY_CARDINALITY_UNRESOLVED,
            "takerOnly=true rows are not a subset of takerOnly=false rows by composite identity.",
            {"condition_id": condition_id, "extra_key_count": len(extra)},
        )

    return TakerOnlyProbeResult(
        condition_id=canonical_condition_id(condition_id, source="taker_only_probe"),
        taker_only_false_count=len(full_api_trades),
        taker_only_true_count=len(taker_only_trades),
        row_count_delta=len(full_api_trades) - len(taker_only_trades),
        true_subset_of_false=True,
    )


# ---------------------------------------------------------------------------
# Phase runner / artifact writing
# ---------------------------------------------------------------------------


def _condition_rows_from_local_frame(local_trades: Any, condition_id: str) -> Any:
    if isinstance(local_trades, dict):
        return local_trades.get(condition_id, [])
    if isinstance(local_trades, pd.DataFrame):
        return local_trades[local_trades["condition_id"].astype(str).str.lower() == condition_id]
    rows = _records_from_frame_or_rows(local_trades)
    return [r for r in rows if str(r.get("condition_id", "")).strip().lower() == condition_id]


def run_b0(
    *,
    root: str | Path,
    manifest_path: str | Path,
    artifacts_dir: str | Path,
    allow_network_option_b_b0: bool,
    confirm_external_polymarket_data_api: bool,
    client: TradesClient | None = None,
    local_trades: Any | None = None,
    provenance_source_csv: str | Path | None = None,
    page_limit: int = DEFAULT_PAGE_LIMIT,
    max_pages_per_condition: int = DEFAULT_MAX_PAGES_PER_CONDITION,
    total_call_budget: int = DEFAULT_TOTAL_CALL_BUDGET,
    taker_only_probe_count: int = DEFAULT_TAKER_ONLY_PROBE_COUNT,
    write_artifacts: bool = True,
) -> dict[str, Any]:
    """Run a future-authorized B0 pilot, or return a typed halt.

    Unit tests may inject a fake client and in-memory local_trades. A real run
    still requires the two authorization flags before any client call.
    """

    try:
        require_b0_network_authorization(
            allow_network_option_b_b0=allow_network_option_b_b0,
            confirm_external_polymarket_data_api=confirm_external_polymarket_data_api,
        )

        manifest = load_condition_manifest(manifest_path, provenance_source_csv=provenance_source_csv)
        validate_caps(
            sample_size=len(manifest.conditions),
            page_limit=page_limit,
            max_pages_per_condition=max_pages_per_condition,
            total_call_budget=total_call_budget,
            taker_only_probe_count=taker_only_probe_count,
        )

        cids = [c.condition_id for c in manifest.conditions]
        if local_trades is None:
            local_trades = load_local_trades_from_store(root, cids)
        if client is None:
            client = DataApiTradesClient()

        budget = CallBudget(max_calls=total_call_budget)
        condition_reports: list[dict[str, Any]] = []
        mismatch_rows: list[dict[str, Any]] = []
        taker_probe_reports: list[dict[str, Any]] = []
        pagination_reports: list[dict[str, Any]] = []

        for index, item in enumerate(manifest.conditions):
            api_rows, pagination = fetch_complete_condition_trades(
                client,
                condition_id=item.condition_id,
                limit=page_limit,
                max_pages=max_pages_per_condition,
                taker_only=False,
                budget=budget,
            )
            pagination_reports.append(asdict(pagination))
            api_norm = normalize_api_trades(api_rows, condition_id=item.condition_id)

            local_rows = _condition_rows_from_local_frame(local_trades, item.condition_id)
            local_norm = normalize_local_trades(local_rows, condition_id=item.condition_id)

            reconciliation = reconcile_trades(condition_id=item.condition_id, api_trades=api_norm, local_trades=local_norm)
            condition_reports.append(asdict(reconciliation))
            mismatch_rows.extend(reconciliation.mismatches)
            if not reconciliation.clean:
                raise B0Halt(
                    STOP_API_LOCAL_MISMATCH,
                    "API rows did not reconcile cleanly to local known-good rows.",
                    {
                        "condition_id": item.condition_id,
                        "api_count": reconciliation.api_count,
                        "local_count": reconciliation.local_count,
                        "matched_count": reconciliation.matched_count,
                        "mismatch_count": reconciliation.mismatch_count,
                        "first_mismatches": reconciliation.mismatches[:5],
                    },
                )

            if index < taker_only_probe_count:
                taker_rows, taker_pagination = fetch_complete_condition_trades(
                    client,
                    condition_id=item.condition_id,
                    limit=page_limit,
                    max_pages=max_pages_per_condition,
                    taker_only=True,
                    budget=budget,
                )
                pagination_reports.append(asdict(taker_pagination))
                taker_norm = normalize_api_trades(taker_rows, condition_id=item.condition_id)
                taker_probe_reports.append(asdict(verify_taker_only_probe(condition_id=item.condition_id, full_api_trades=api_norm, taker_only_trades=taker_norm)))

        result = {
            "phase": PHASE,
            "status": STATUS_OK,
            "authorized_scope": AUTHORIZED_SCOPE,
            "manifest": asdict(manifest),
            "sample_size": len(manifest.conditions),
            "condition_reports": condition_reports,
            "pagination_reports": pagination_reports,
            "taker_only_probe_reports": taker_probe_reports,
            "mismatch_rows": mismatch_rows,
            "calls_used": budget.calls_used,
            "no_price_series_persisted": True,
            "named_binary_probe_blocked_untouched": True,
            "forbidden_transforms_absent": True,
            "writes_limited_to_reconciliation_artifacts": bool(write_artifacts),
        }
        if write_artifacts:
            write_b0_artifacts(result, artifacts_dir=artifacts_dir)
        return result
    except B0Halt as halt:
        return halt.to_result()


def write_b0_artifacts(result: Mapping[str, Any], *, artifacts_dir: str | Path) -> None:
    out_dir = Path(artifacts_dir) / "named_binary_probe" / "price_source_option_b_b0"
    assert_output_path_allowed(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "option_b_b0_reconciliation.json"
    md_path = out_dir / "option_b_b0_reconciliation.md"
    by_condition_path = out_dir / "option_b_b0_by_condition.csv"
    mismatch_path = out_dir / "option_b_b0_mismatches.csv"

    for path in (json_path, md_path, by_condition_path, mismatch_path):
        assert_output_path_allowed(path)

    json_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Option B Phase B0 reconciliation",
        "",
        f"Status: `{result.get('status')}`",
        "",
        "Scope: mechanical-trust reconciliation only. No price series, no scoring, no P1/P2/P3/probe, no gate change.",
        f"Calls used: `{result.get('calls_used', 0)}`",
        f"Sample size: `{result.get('sample_size', 0)}`",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    condition_rows = list(result.get("condition_reports", []))
    if condition_rows:
        with by_condition_path.open("w", encoding="utf-8", newline="") as f:
            fieldnames = ["condition_id", "api_count", "local_count", "matched_count", "mismatch_count"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in condition_rows:
                writer.writerow({k: row.get(k) for k in fieldnames})

    mismatch_rows = list(result.get("mismatch_rows", []))
    if mismatch_rows:
        with mismatch_path.open("w", encoding="utf-8", newline="") as f:
            fieldnames = sorted({key for row in mismatch_rows for key in row.keys()})
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in mismatch_rows:
                writer.writerow(row)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Option B Phase B0 mechanical-trust reconciliation pilot. No run is authorized unless both flags are supplied.")
    parser.add_argument("--root", required=True, help="Data root, e.g. C:\\b1\\data. This is passed to Store(root), not the project root.")
    parser.add_argument("--manifest", required=True, help="Provenance-attested B0 known-good condition manifest JSON.")
    parser.add_argument("--provenance-source-csv", default=None, help="Optional accepted S1-ALT by-condition CSV used to verify manifest provenance.")
    parser.add_argument("--artifacts-dir", default="artifacts", help="Project artifacts directory. Writes only reconciliation artifacts under named_binary_probe/price_source_option_b_b0/.")
    parser.add_argument("--page-limit", type=int, default=DEFAULT_PAGE_LIMIT)
    parser.add_argument("--max-pages-per-condition", type=int, default=DEFAULT_MAX_PAGES_PER_CONDITION)
    parser.add_argument("--total-call-budget", type=int, default=DEFAULT_TOTAL_CALL_BUDGET)
    parser.add_argument("--taker-only-probe-count", type=int, default=DEFAULT_TAKER_ONLY_PROBE_COUNT)
    parser.add_argument("--no-write-artifacts", action="store_true", help="Do not write reconciliation artifacts even if the authorized run succeeds.")
    parser.add_argument("--allow-network-option-b-b0", action="store_true", help="First required explicit authorization flag for Phase B0 network calls.")
    parser.add_argument("--confirm-external-polymarket-data-api", action="store_true", help="Second required explicit authorization flag acknowledging external Polymarket Data API calls.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = run_b0(
        root=args.root,
        manifest_path=args.manifest,
        artifacts_dir=args.artifacts_dir,
        allow_network_option_b_b0=args.allow_network_option_b_b0,
        confirm_external_polymarket_data_api=args.confirm_external_polymarket_data_api,
        provenance_source_csv=args.provenance_source_csv,
        page_limit=args.page_limit,
        max_pages_per_condition=args.max_pages_per_condition,
        total_call_budget=args.total_call_budget,
        taker_only_probe_count=args.taker_only_probe_count,
        write_artifacts=not args.no_write_artifacts,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == STATUS_OK else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
