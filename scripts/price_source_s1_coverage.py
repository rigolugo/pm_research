"""S1 price-source coverage test - Pass 1 (stratified probe) ONLY.

Governing spec: project_context/SPEC_price_source_s1_coverage.md (ACCEPTED / coverage-only).
Authorization: S1 Pass 1 implementation + tests only. This file performs NO network
fetch by itself; a real fetch requires explicit CLI authorization flags and is a
user-run task on the Windows/Miniconda box. Claude does not fetch Polymarket data.

What this file IS:
  - Pure-logic Pass-1 coverage machinery: P0/contract validation, token-pair
    enumeration from `trades`, a pre-registered stratified sample, Level-A status
    mapping, Level-B decision-window classification, reconciliation, and an
    endpoint-client *shape* whose real network calls are hard-gated behind an
    explicit authorization flag (default -> STOP_NOT_AUTHORIZED).

What this file is NOT (hard non-goals, enforced):
  - No Pass 2 (full sweep). `run_pass2` exists only as a hard stop.
  - No writes into prices/. No backfill. No scoring. No probe. No gate change.
  - No `yes_price`, `1 - yes_price`, `1 - price`, or `1 - p` side synthesis anywhere.
  - `resolved_winning_token_id` is NEVER a token-pair source.
  - `resolved_at` is used ONLY as a coverage-window upper bound, never as feature/target.

Coverage-window / decision policy (lookahead-safe, per DECISION_LOG + DATA_CONTRACTS 7):
  first_trade_ts = min(traded_at) per condition
  warmup_seconds = 3600   # == Rank 1A forecast_vs_price.py default --warmup-hours 1.0
  decision-window point must satisfy:  ts >= first_trade_ts + 3600  AND  ts < resolved_at
"""

from __future__ import annotations

import argparse
import math
import os
import random
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Pinned constants (consumed, never redefined)
# ---------------------------------------------------------------------------
NB_CONTRACT_VERSION = "nb-contract-2026-06-28.1"
WARMUP_SECONDS = 3600  # == Rank 1A forecast_vs_price.py default --warmup-hours 1.0
ORIENTED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
EXPECTED_FINAL_P0_ELIGIBLE = 39693  # accepted P0 figure; overridden only by the artifact
AUTHORIZED_SCOPE = "S1_PASS1_COVERAGE_ONLY"

# Default Pass-1 sample bound: a few hundred conditions total, NOT the full universe.
DEFAULT_PASS1_SAMPLE_SIZE = 300
DEFAULT_SEED = 20260628

# ---------------------------------------------------------------------------
# Typed statuses (spec 4, 7.1, 8)
# ---------------------------------------------------------------------------
# Level A - token-endpoint reachability
SERIES_PRESENT = "SERIES_PRESENT"
SERIES_EMPTY = "SERIES_EMPTY"
SERIES_ERROR_TRANSIENT = "SERIES_ERROR_TRANSIENT"
SERIES_ERROR_NOTFOUND = "SERIES_ERROR_NOTFOUND"
SERIES_MALFORMED = "SERIES_MALFORMED"
LEVEL_A_STATUSES = frozenset(
    {SERIES_PRESENT, SERIES_EMPTY, SERIES_ERROR_TRANSIENT, SERIES_ERROR_NOTFOUND, SERIES_MALFORMED}
)

# Level B - decision-window density (condition-level)
DECISION_PRICE_BOTH_SIDES = "DECISION_PRICE_BOTH_SIDES"
DECISION_PRICE_ONE_SIDE = "DECISION_PRICE_ONE_SIDE"
DECISION_PRICE_NEITHER = "DECISION_PRICE_NEITHER"
NO_TRADE_ANCHOR = "NO_TRADE_ANCHOR"
# Invalid/missing decision window: resolved_at missing OR resolved_at <= first_trade_ts+warmup.
# Such a condition has NO ex-ante decision window at all, so it is NOT measurable coverage and
# must never be counted as DECISION_PRICE_NEITHER (which is a real "queried, nothing there"
# negative). Excluded and reported separately; never fetched.
NO_VALID_DECISION_WINDOW = "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"

# Stop / exclusion states
STOP_P0_NOT_CLEAR = "STOP_P0_NOT_CLEAR"
STOP_STALE_CONTRACT = "STOP_STALE_CONTRACT"
TOKEN_PAIR_UNRESOLVED = "TOKEN_PAIR_UNRESOLVED"
STOP_TOKEN_ENUMERATION_UNRELIABLE = "STOP_TOKEN_ENUMERATION_UNRELIABLE"
STOP_PRECISION_LOSS = "STOP_PRECISION_LOSS"
STOP_ENDPOINT_SHAPE_UNRECOGNIZED = "STOP_ENDPOINT_SHAPE_UNRECOGNIZED"
STOP_VALIDATION_REQUIRED = "STOP_VALIDATION_REQUIRED"
STOP_LEAKAGE_OR_FORBIDDEN_INFERENCE = "STOP_LEAKAGE_OR_FORBIDDEN_INFERENCE"
STOP_NOT_AUTHORIZED = "STOP_NOT_AUTHORIZED"

# Verdicts (Pass 1 may already reach a verdict, spec 7.1)
S1_SOURCE_VIABLE = "S1_SOURCE_VIABLE"
S1_SOURCE_PARTIAL = "S1_SOURCE_PARTIAL"
S1_SOURCE_NOT_VIABLE = "S1_SOURCE_NOT_VIABLE"
S1_INCONCLUSIVE_SHAPE = "S1_INCONCLUSIVE_SHAPE"
S1_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE = (
    "S1_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE"
)
S1_PASS1_COMPLETE = "S1_PASS1_COMPLETE"

# Coverage threshold (spec 7.2, LOCKED) - Level B is the binding criterion.
SUBCLASS_BOTH_SIDES_THRESHOLD = 0.95

# Large-unreliable-fraction guard for token enumeration (spec 8.3).
TOKEN_ENUMERATION_UNRELIABLE_FRACTION = 0.20

# All-one-status guard fires when a nontrivial aggregate collapses to a single value.
ALL_ONE_STATUS_MIN_N = 2


class DataExportPrecisionLoss(ValueError):
    """Raised (fail-loud) on scientific notation / float mangling of a token id or price.

    Precision is already lost; never reconstruct a 78-digit id from `5.20896e+76`.
    (DUNE_DATA_NOTES 5.)
    """


class ForbiddenInference(ValueError):
    """Raised if any path attempts to synthesize a side price from yes_price / 1 - p."""


class EndpointShapeError(ValueError):
    """Raised when a real response deviates from the DOCUMENTED SHAPE (spec 5)."""


class NotAuthorizedError(RuntimeError):
    """Raised when a network fetch is attempted without explicit CLI authorization."""


class Pass2NotAvailable(RuntimeError):
    """Pass 2 is not implemented under this authorization. Hard stop."""


# ---------------------------------------------------------------------------
# Precision-safe integer canonicalization (self-contained; mirrors Rank 2 helper)
# ---------------------------------------------------------------------------
_SCI_RE = re.compile(r"[eE]")
_INT_RE = re.compile(r"^[0-9]+$")


def canonical_int(value: Any) -> int:
    """Normalize a string-safe integer token id / index to a Python int.

    Accepts full-precision integer strings ("0", "0.0" -> 0, whitespace tolerated,
    78-digit ids). Fails LOUD on scientific notation or any non-integer float text -
    precision is already lost and must never be reconstructed.
    """
    if value is None:
        raise DataExportPrecisionLoss("canonical_int received None")
    if isinstance(value, bool):
        raise DataExportPrecisionLoss(f"bool is not a token/index: {value!r}")
    if isinstance(value, float):
        raise DataExportPrecisionLoss(f"float token/index not string-safe: {value!r}")
    s = str(value).strip()
    if s == "":
        raise DataExportPrecisionLoss("canonical_int received empty string")
    if _SCI_RE.search(s):
        raise DataExportPrecisionLoss(f"scientific notation (precision lost): {s!r}")
    if "." in s:
        head, _, tail = s.partition(".")
        if tail.strip("0") != "" or not _INT_RE.match(head or "0"):
            raise DataExportPrecisionLoss(f"non-integer / float-mangled token/index: {s!r}")
        s = head if head != "" else "0"
    if not _INT_RE.match(s):
        raise DataExportPrecisionLoss(f"non-integer token/index: {s!r}")
    return int(s)


def is_string_safe_token(value: Any) -> bool:
    try:
        canonical_int(value)
        return True
    except DataExportPrecisionLoss:
        return False


# ---------------------------------------------------------------------------
# Time parsing (resolved_at is a STRING like "2025-03-06 00:00:00 UTC")
# ---------------------------------------------------------------------------
def parse_ts(value: Any) -> float:
    """Parse a timestamp to epoch seconds (float). Accepts epoch numbers or the
    resolution-source string form. Fails loud on unparseable input."""
    if value is None:
        raise ValueError("parse_ts received None")
    if isinstance(value, bool):
        raise ValueError("parse_ts received bool")
    if isinstance(value, (int, float)):
        return float(value)
    # Datetime-like objects (pandas Timestamp, datetime) as returned by
    # Store.load_trades()'s traded_at column. pandas Timestamp IS a datetime subclass, so
    # this one branch covers both, tz-aware and tz-naive. Timestamp-only fix: it touches
    # NO token-id / integer-identity handling (token ids never pass through parse_ts; they
    # go through canonical_int). tz-aware -> epoch directly; tz-naive -> treat as UTC
    # (project convention) so the result is independent of the runner's local timezone.
    if isinstance(value, datetime):
        dt = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    s = str(value).strip()
    if s == "":
        raise ValueError("parse_ts received empty string")
    if re.match(r"^[0-9]+(\.[0-9]+)?$", s):
        return float(s)
    s2 = s.replace(" UTC", "").replace("Z", "").strip()
    # Accept the real resolution-source form "2025-03-06 07:25:37.000 UTC" (fractional
    # seconds, " UTC" suffix already stripped above) alongside the whole-second and ISO
    # forms. %f matches 1-6 fractional digits, covering ".000" millisecond precision.
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s2, fmt).replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except ValueError:
            continue
    raise ValueError(f"unparseable timestamp: {value!r}")


# ---------------------------------------------------------------------------
# P0 + contract validation (spec 8.1, 8.2)
# ---------------------------------------------------------------------------
def validate_p0(p0_preflight: Dict[str, Any]) -> int:
    """Assert P0_CLEAR + contract-version equality; return the authoritative
    final_p0_eligible count (from the artifact itself, reported clearly).

    Raises ValueError(<stop_state>) on failure; the caller maps to a stop state.
    """
    if not isinstance(p0_preflight, dict):
        raise ValueError(STOP_P0_NOT_CLEAR)
    if p0_preflight.get("p0_state") != "P0_CLEAR":
        raise ValueError(STOP_P0_NOT_CLEAR)

    contract_v = p0_preflight.get("nb_contract_version_contract")
    ressrc_v = p0_preflight.get("nb_contract_version_resolution_source")
    expected_v = p0_preflight.get("nb_contract_version_expected", NB_CONTRACT_VERSION)
    if expected_v != NB_CONTRACT_VERSION:
        raise ValueError(STOP_STALE_CONTRACT)
    for v in (contract_v, ressrc_v):
        if v != NB_CONTRACT_VERSION:
            raise ValueError(STOP_STALE_CONTRACT)

    counts = p0_preflight.get("counts_pooled", {}) or {}
    final_eligible = int(counts.get("final_p0_eligible", EXPECTED_FINAL_P0_ELIGIBLE))
    return final_eligible


def assert_contract_version(*versions: Optional[str]) -> None:
    for v in versions:
        if v != NB_CONTRACT_VERSION:
            raise ValueError(STOP_STALE_CONTRACT)


# ---------------------------------------------------------------------------
# Universe assembly (spec 3, DATA_CONTRACTS 1/2 join rule)
# ---------------------------------------------------------------------------
@dataclass
class ConditionRecord:
    condition_id: str
    subclass: str  # one of ORIENTED_SUBCLASSES
    resolved_at: Any  # raw resolution timestamp (pandas Timestamp / str / None); parsed via parse_ts
    side_0_token: Optional[str] = None
    side_1_token: Optional[str] = None
    pair_status: str = "PENDING"  # "OK" or TOKEN_PAIR_UNRESOLVED
    malformed_trade_rows: int = 0  # diagnostic: count of skipped missing/malformed trade rows


def _normalize_eligible(value: Any) -> bool:
    """nb_eligible is the STRING "True"/"False" in the contract JSON (DATA_CONTRACTS 1)."""
    if isinstance(value, bool):
        return value
    s = str(value).strip()
    if s == "True":
        return True
    if s == "False":
        return False
    raise ValueError(f"unexpected nb_eligible value (not True/False): {value!r}")


def build_universe(
    contract_conditions: Sequence[Dict[str, Any]],
    resolution_rows: Sequence[Dict[str, Any]],
) -> List[ConditionRecord]:
    """Contract (nb_eligible True + nb_subclass in oriented set) INNER-JOIN resolved
    parquet rows (status == RESOLVED_SINGLE_WINNER) on condition_id, with a subclass
    cross-check (hard stop on mismatch). Returns oriented eligible conditions only.

    Never reads winners as anything but the resolved_at carrier + subclass cross-check.
    """
    contract_map: Dict[str, str] = {}
    for rec in contract_conditions:
        assert_contract_version(rec.get("nb_contract_version"))
        if not _normalize_eligible(rec.get("nb_eligible")):
            continue
        sub = rec.get("nb_subclass")
        if sub not in ORIENTED_SUBCLASSES:  # excludes YES_NO and UNUSABLE
            continue
        contract_map[rec["condition_id"]] = sub

    universe: List[ConditionRecord] = []
    seen = set()
    for row in resolution_rows:
        if row.get("status") != "RESOLVED_SINGLE_WINNER":
            continue
        assert_contract_version(row.get("nb_contract_version"))
        cid = row["condition_id"]
        if cid not in contract_map or cid in seen:
            continue
        seen.add(cid)
        c_sub = contract_map[cid]
        r_sub = row.get("subclass")
        if c_sub != r_sub:
            raise ValueError(
                f"{STOP_STALE_CONTRACT}: subclass mismatch for {cid}: "
                f"contract={c_sub} resolution={r_sub}"
            )
        universe.append(
            ConditionRecord(condition_id=cid, subclass=c_sub, resolved_at=row.get("resolved_at"))
        )
    return universe


# ---------------------------------------------------------------------------
# Token-pair enumeration from TRADES (spec 3.1) - never from winners
# ---------------------------------------------------------------------------
def _is_missing_field(value: Any) -> bool:
    """True iff a trade-row token_id / outcome_index is MISSING/malformed rather than a
    real value: None, empty/whitespace string, or a NaN float (`v != v`).

    A NaN is a missing field, not precision loss. A *real* non-null float (e.g. 5.2e76 or a
    float-mangled large id) is NOT missing — it must still reach canonical_int and STOP_PRECISION_LOSS.
    """
    if value is None:
        return True
    if isinstance(value, float):
        return value != value  # NaN
    s = str(value).strip()
    if s == "":
        return True
    if s.lower() in ("nan", "none"):
        return True
    return False


def enumerate_token_pair(
    trade_tuples: Sequence[Tuple[str, Any, Any]],
) -> Tuple[Optional[str], Optional[str], str, int]:
    """Given distinct (condition_id, token_id, outcome_index) tuples for ONE condition,
    return (side_0_token, side_1_token, status, malformed_rows).

    Requires exactly two stable, string-safe side tokens: one for outcome_index 0 and
    one for outcome_index 1. Anything else -> (None, None, TOKEN_PAIR_UNRESOLVED, malformed).

    Rows with a MISSING/malformed token_id or outcome_index (None / empty / NaN) are
    SKIPPED and counted (`malformed_rows`) — they are not precision loss. A condition that
    cannot yield two stable string-safe side tokens from the *valid* rows is
    TOKEN_PAIR_UNRESOLVED, never a STOP.

    Fails LOUD (DataExportPrecisionLoss) only on a *real* non-null value that is
    scientific-notation / float-mangled / non-integer identity — precision loss is never a
    soft TOKEN_PAIR_UNRESOLVED and never a missing row.
    """
    by_index: Dict[int, set] = {}
    malformed = 0
    for _cid, token_id, outcome_index in trade_tuples:
        # Missing/malformed row -> skip + count (not precision loss).
        if _is_missing_field(token_id) or _is_missing_field(outcome_index):
            malformed += 1
            continue
        _ = canonical_int(token_id)  # precision discipline first (raises on sci-notation)
        idx = canonical_int(outcome_index)
        if idx not in (0, 1):
            return None, None, TOKEN_PAIR_UNRESOLVED, malformed
        by_index.setdefault(idx, set()).add(str(token_id).strip())

    if set(by_index.keys()) != {0, 1}:
        return None, None, TOKEN_PAIR_UNRESOLVED, malformed
    if len(by_index[0]) != 1 or len(by_index[1]) != 1:
        return None, None, TOKEN_PAIR_UNRESOLVED, malformed

    s0 = next(iter(by_index[0]))
    s1 = next(iter(by_index[1]))
    if canonical_int(s0) == canonical_int(s1):
        return None, None, TOKEN_PAIR_UNRESOLVED, malformed
    return s0, s1, "OK", malformed


def resolve_token_pairs(
    universe: Sequence[ConditionRecord],
    trades_by_condition: Dict[str, Sequence[Tuple[str, Any, Any]]],
) -> Tuple[List[ConditionRecord], List[ConditionRecord]]:
    """Resolve the side-token pair for each condition from trades. Returns
    (resolved, unresolved). Raises ValueError(STOP_TOKEN_ENUMERATION_UNRELIABLE) if the
    unresolved fraction is large (spec 8.3)."""
    resolved: List[ConditionRecord] = []
    unresolved: List[ConditionRecord] = []
    for c in universe:
        tuples = trades_by_condition.get(c.condition_id, [])
        s0, s1, status, malformed = enumerate_token_pair(tuples)
        c.side_0_token, c.side_1_token, c.pair_status = s0, s1, status
        c.malformed_trade_rows = malformed
        (resolved if status == "OK" else unresolved).append(c)

    total = len(universe)
    if total and (len(unresolved) / total) > TOKEN_ENUMERATION_UNRELIABLE_FRACTION:
        raise ValueError(STOP_TOKEN_ENUMERATION_UNRELIABLE)
    return resolved, unresolved


# ---------------------------------------------------------------------------
# Pre-registered Pass-1 stratified sample (spec 6)
# ---------------------------------------------------------------------------
def time_bucket(resolved_at: str) -> str:
    """Coarse time bucket by resolution year-quarter, for stratification where feasible.
    Returns 'UNKNOWN' if unparseable (bucket stratification is best-effort)."""
    try:
        ts = parse_ts(resolved_at)
    except ValueError:
        return "UNKNOWN"
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}Q{q}"


def build_pass1_sample(
    resolved_conditions: Sequence[ConditionRecord],
    sample_size: int = DEFAULT_PASS1_SAMPLE_SIZE,
    seed: int = DEFAULT_SEED,
) -> List[ConditionRecord]:
    """Deterministic, subclass- and time-bucket-stratified sample bounded by sample_size.

    Bounded by default to a few hundred conditions total - never the full universe.
    Pass 2 (full sweep) is a SEPARATE, hard-gated decision (see run_pass2)."""
    if sample_size <= 0:
        return []
    rng = random.Random(seed)

    by_sub: Dict[str, List[ConditionRecord]] = {s: [] for s in ORIENTED_SUBCLASSES}
    for c in resolved_conditions:
        by_sub.setdefault(c.subclass, []).append(c)

    present_subs = [s for s in ORIENTED_SUBCLASSES if by_sub.get(s)]
    if not present_subs:
        return []

    base = sample_size // len(present_subs)
    remainder = sample_size % len(present_subs)
    per_sub_budget: Dict[str, int] = {}
    for i, s in enumerate(present_subs):
        per_sub_budget[s] = base + (1 if i < remainder else 0)

    selected: List[ConditionRecord] = []
    for s in present_subs:
        pool = by_sub[s]
        budget = min(per_sub_budget[s], len(pool))
        buckets: Dict[str, List[ConditionRecord]] = {}
        for c in pool:
            buckets.setdefault(time_bucket(c.resolved_at), []).append(c)
        bucket_keys = sorted(buckets.keys())
        for k in bucket_keys:
            buckets[k].sort(key=lambda c: c.condition_id)
            rng.shuffle(buckets[k])

        drawn: List[ConditionRecord] = []
        exhausted = False
        while len(drawn) < budget and not exhausted:
            exhausted = True
            for k in bucket_keys:
                if buckets[k]:
                    drawn.append(buckets[k].pop())
                    exhausted = False
                    if len(drawn) >= budget:
                        break
        selected.extend(drawn)

    selected.sort(key=lambda c: c.condition_id)
    return selected


# ---------------------------------------------------------------------------
# Endpoint client SHAPE (DOCUMENTED SHAPE, spec 5) - network hard-gated
# ---------------------------------------------------------------------------
@dataclass
class PricePoint:
    ts: float          # epoch seconds
    p: float           # SOURCE-DEFINED CLOB history price for the queried token
    token_id: str      # string-safe echo of the requested token


@dataclass
class SeriesResult:
    token_id: str
    status: str                    # Level-A status
    points: List[PricePoint] = field(default_factory=list)
    http_status: Optional[int] = None
    note: str = ""


def map_response_to_status(
    http_status: Optional[int],
    body: Any,
    requested_token: str,
) -> SeriesResult:
    """Map a raw endpoint response (already-decoded JSON body) to a Level-A SeriesResult.

    PURE - takes an already-fetched body (tests inject it); performs no I/O.
    NEVER converts p to a canonical side price and NEVER computes 1 - p.
    """
    if http_status is not None:
        if http_status == 404:
            return SeriesResult(requested_token, SERIES_ERROR_NOTFOUND, http_status=http_status)
        if http_status >= 500 or http_status == 429:
            return SeriesResult(requested_token, SERIES_ERROR_TRANSIENT, http_status=http_status)
        if http_status >= 400:
            return SeriesResult(requested_token, SERIES_ERROR_NOTFOUND, http_status=http_status)

    if not isinstance(body, dict):
        raise EndpointShapeError(f"{STOP_ENDPOINT_SHAPE_UNRECOGNIZED}: body not an object")
    series = body.get("history", body.get("prices"))
    if series is None:
        raise EndpointShapeError(f"{STOP_ENDPOINT_SHAPE_UNRECOGNIZED}: no history/prices key")
    if not isinstance(series, list):
        raise EndpointShapeError(f"{STOP_ENDPOINT_SHAPE_UNRECOGNIZED}: history not a list")
    if len(series) == 0:
        return SeriesResult(requested_token, SERIES_EMPTY, points=[])

    points: List[PricePoint] = []
    for raw in series:
        if not isinstance(raw, dict) or ("t" not in raw) or ("p" not in raw):
            return SeriesResult(requested_token, SERIES_MALFORMED, note="point missing t/p")
        echoed = raw.get("token_id", requested_token)
        if isinstance(echoed, str) and _SCI_RE.search(echoed) and not re.match(r"^\d+$", echoed):
            return SeriesResult(requested_token, SERIES_MALFORMED, note="sci-notation token echo")
        try:
            ts = parse_ts(raw["t"])
            p = float(raw["p"])
        except (ValueError, TypeError):
            return SeriesResult(requested_token, SERIES_MALFORMED, note="unparseable t/p")
        if math.isnan(p) or math.isinf(p):
            return SeriesResult(requested_token, SERIES_MALFORMED, note="nan/inf price")
        points.append(PricePoint(ts=ts, p=p, token_id=str(echoed)))

    return SeriesResult(requested_token, SERIES_PRESENT, points=points)


def observe_response_shape(
    http_status: Optional[int],
    body: Any,
    requested_token: str,
) -> Dict[str, Any]:
    """Extract STRUCTURAL shape facts from a response for the endpoint-shape ledger.

    Returns keys/counts/statuses only - NEVER a reusable price series. This is what
    price_source_s1_endpoint_shape.md records so a later S2 review can trust the shape.
    Pure; performs no I/O and no price synthesis.
    """
    facts: Dict[str, Any] = {
        "requested_token": str(requested_token),
        "http_status": http_status,
        "top_level_keys": None,
        "series_key": None,          # "history" | "prices" | None
        "point_count": None,
        "first_point_keys": None,
        "level_a_status": None,
        "note": "",
    }
    # Level-A status via the shared mapper (may raise EndpointShapeError for deviations;
    # the caller decides whether to catch + record).
    if isinstance(body, dict):
        facts["top_level_keys"] = sorted(str(k) for k in body.keys())
        series = body.get("history", body.get("prices"))
        if body.get("history") is not None:
            facts["series_key"] = "history"
        elif body.get("prices") is not None:
            facts["series_key"] = "prices"
        if isinstance(series, list):
            facts["point_count"] = len(series)
            if series and isinstance(series[0], dict):
                # First-point KEYS only (structure), never the values / price series.
                facts["first_point_keys"] = sorted(str(k) for k in series[0].keys())
    elif body is not None:
        facts["top_level_keys"] = f"<non-dict body: {type(body).__name__}>"

    # Attach the Level-A status if it maps cleanly; leave None if it would deviate.
    try:
        facts["level_a_status"] = map_response_to_status(http_status, body, requested_token).status
    except EndpointShapeError as exc:
        facts["level_a_status"] = STOP_ENDPOINT_SHAPE_UNRECOGNIZED
        facts["note"] = str(exc)
    return facts


class PricesHistoryClient:
    """Endpoint client SHAPE for CLOB /prices-history (DOCUMENTED SHAPE, spec 5).

    Real network calls are HARD-GATED: unless `network_authorized=True` (set only by the
    explicit CLI flag on the user's box), any fetch raises NotAuthorizedError so accidental
    execution stops with STOP_NOT_AUTHORIZED. Claude never sets this flag.

    Tests inject a `transport` callable (mocked) and never touch the network.
    """

    BASE_URL = "https://clob.polymarket.com"
    GET_PATH = "/prices-history"
    BATCH_PATH = "/batch-prices-history"

    def __init__(
        self,
        network_authorized: bool = False,
        transport: Optional[Callable[..., Tuple[Optional[int], Any]]] = None,
        shape_sink: Optional[List[Dict[str, Any]]] = None,
    ):
        self.network_authorized = network_authorized
        self._transport = transport
        # When provided, the client records structural request/response facts here
        # (path, params/payload keys, http_status, raw body) for the endpoint-shape ledger.
        self.shape_sink = shape_sink

    def _capture(self, context: str, path: str, payload: Dict[str, Any],
                 http_status: Optional[int], body: Any) -> None:
        if self.shape_sink is None:
            return
        self.shape_sink.append({
            "context": context,          # "get" | "batch"
            "path": path,
            "payload_keys": sorted(str(k) for k in payload.keys()),
            "payload": {k: (v if not isinstance(v, list) else f"<list:{len(v)}>")
                        for k, v in payload.items()},
            "http_status": http_status,
            "body": body,                # raw; converted to keys/counts only by observe_response_shape
        })

    def _do(self, method: str, path: str, payload: Dict[str, Any]) -> Tuple[Optional[int], Any]:
        if self._transport is not None:
            return self._transport(method, self.BASE_URL + path, payload)
        if not self.network_authorized:
            raise NotAuthorizedError(STOP_NOT_AUTHORIZED)
        import requests  # lazy import: module has no hard requests dependency

        if method == "GET":
            resp = requests.get(self.BASE_URL + path, params=payload, timeout=30)
        else:
            resp = requests.post(self.BASE_URL + path, json=payload, timeout=30)
        try:
            body = resp.json()
        except Exception:  # noqa: BLE001
            body = None
        return resp.status_code, body

    def get_prices_history(
        self,
        token_id: str,
        start_ts: int,
        end_ts: int,
        interval: str = "max",
        fidelity: Optional[int] = None,
    ) -> SeriesResult:
        """Single-token GET /prices-history. camelCase startTs/endTs (spec 5)."""
        if not is_string_safe_token(token_id):
            raise DataExportPrecisionLoss(f"{STOP_PRECISION_LOSS}: token {token_id!r}")
        params: Dict[str, Any] = {
            "market": str(token_id),  # market = the token id
            "startTs": int(start_ts),
            "endTs": int(end_ts),
            "interval": interval,
        }
        if fidelity is not None:
            params["fidelity"] = int(fidelity)
        http_status, body = self._do("GET", self.GET_PATH, params)
        self._capture("get", self.GET_PATH, params, http_status, body)
        return map_response_to_status(http_status, body, str(token_id))

    def post_batch_prices_history(
        self,
        token_ids: Sequence[str],
        start_ts: int,
        end_ts: int,
        interval: str = "max",
        fidelity: Optional[int] = None,
    ) -> Dict[str, SeriesResult]:
        """Optional POST /batch-prices-history (CANDIDATE path only). snake_case start_ts/end_ts.

        Batch is a cost optimization and NEVER a source of truth over single-token until
        proven equivalent (see batch_single_equivalent)."""
        for t in token_ids:
            if not is_string_safe_token(t):
                raise DataExportPrecisionLoss(f"{STOP_PRECISION_LOSS}: token {t!r}")
        payload: Dict[str, Any] = {
            "markets": [str(t) for t in token_ids],
            "start_ts": int(start_ts),
            "end_ts": int(end_ts),
            "interval": interval,
        }
        if fidelity is not None:
            payload["fidelity"] = int(fidelity)
        http_status, body = self._do("POST", self.BATCH_PATH, payload)
        self._capture("batch", self.BATCH_PATH, payload, http_status, body)
        if http_status is not None and http_status >= 400:
            status = SERIES_ERROR_NOTFOUND if http_status == 404 else SERIES_ERROR_TRANSIENT
            return {str(t): SeriesResult(str(t), status, http_status=http_status) for t in token_ids}
        if not isinstance(body, dict) or "histories" not in body:
            raise EndpointShapeError(f"{STOP_ENDPOINT_SHAPE_UNRECOGNIZED}: batch has no histories")
        out: Dict[str, SeriesResult] = {}
        for t in token_ids:
            per = body["histories"].get(str(t))
            if per is None:
                out[str(t)] = SeriesResult(str(t), SERIES_ERROR_NOTFOUND)
            else:
                out[str(t)] = map_response_to_status(None, {"history": per}, str(t))
        return out


def batch_single_equivalent(single: SeriesResult, batched: SeriesResult) -> bool:
    """Point-for-point equivalence between a single-token GET and a batched result for
    the SAME token (spec 5.1 point 7). Any divergence -> False (single is authoritative)."""
    if single.token_id != batched.token_id:
        return False
    if single.status != batched.status:
        return False
    if len(single.points) != len(batched.points):
        return False
    for a, b in zip(single.points, batched.points):
        if a.ts != b.ts or a.p != b.p or str(a.token_id) != str(b.token_id):
            return False
    return True


# ---------------------------------------------------------------------------
# Level-B decision-window classification (spec 4.2) - lookahead-safe
# ---------------------------------------------------------------------------
def has_decision_window_point(
    points: Sequence[PricePoint],
    first_trade_ts: float,
    resolved_at_ts: float,
    warmup_seconds: int = WARMUP_SECONDS,
) -> bool:
    """True iff at least one point satisfies:
        ts >= first_trade_ts + warmup_seconds  AND  ts < resolved_at_ts.
    resolved_at is a strict UPPER bound (never counted); a point at/after resolution
    is leakage and does not count."""
    lower = first_trade_ts + warmup_seconds
    for pt in points:
        if pt.ts >= lower and pt.ts < resolved_at_ts:
            return True
    return False


def classify_decision_window(
    side_0: SeriesResult,
    side_1: SeriesResult,
    first_trade_ts: Optional[float],
    resolved_at_ts: float,
    warmup_seconds: int = WARMUP_SECONDS,
) -> str:
    """Condition-level Level-B classification.

    - No local trade anchor -> NO_TRADE_ANCHOR (never force a timestamp).
    - Both sides have an in-window point -> DECISION_PRICE_BOTH_SIDES.
    - Exactly one -> DECISION_PRICE_ONE_SIDE (NOT usable; canonical_side_price needs both).
    - Neither -> DECISION_PRICE_NEITHER.

    A side counts only if its Level-A status is SERIES_PRESENT.
    """
    if first_trade_ts is None:
        return NO_TRADE_ANCHOR

    def side_ok(s: SeriesResult) -> bool:
        if s.status != SERIES_PRESENT:
            return False
        return has_decision_window_point(s.points, first_trade_ts, resolved_at_ts, warmup_seconds)

    a = side_ok(side_0)
    b = side_ok(side_1)
    if a and b:
        return DECISION_PRICE_BOTH_SIDES
    if a or b:
        return DECISION_PRICE_ONE_SIDE
    return DECISION_PRICE_NEITHER


# ---------------------------------------------------------------------------
# All-one-status guard (spec 8.6, 217/0 & 10/0 lesson)
# ---------------------------------------------------------------------------
def all_one_status_guard(statuses: Sequence[str], min_n: int = ALL_ONE_STATUS_MIN_N) -> bool:
    """True if the aggregate is a red flag (all one value over a nontrivial n), meaning
    the caller must run the Level-C validation sample and STOP_VALIDATION_REQUIRED rather
    than report the aggregate as a finding."""
    if len(statuses) < min_n:
        return False
    return len(set(statuses)) == 1


# ---------------------------------------------------------------------------
# Reconciliation (spec 7) - every condition lands in exactly one bucket
# ---------------------------------------------------------------------------
def reconcile(final_p0_eligible: int, per_bucket_counts: Dict[str, int]) -> Dict[str, Any]:
    """Buckets must sum to final_p0_eligible exactly (fail-loud discipline)."""
    total = sum(per_bucket_counts.values())
    return {
        "final_p0_eligible": final_p0_eligible,
        "bucket_total": total,
        "exact": total == final_p0_eligible,
        "per_bucket": dict(per_bucket_counts),
    }


# ---------------------------------------------------------------------------
# Subclass coverage rate (spec 7.2) - Level B binding
# ---------------------------------------------------------------------------
def subclass_coverage_rate(
    classifications: Sequence[Tuple[str, str]],  # (subclass, level_b_class) over MEASURED conditions
    subclass: str,
) -> Tuple[int, int, float]:
    """(both_sides, measured, rate) for a subclass. `measured` excludes NO_TRADE_ANCHOR
    (reconciled separately in the excluded ledger)."""
    both = 0
    measured = 0
    for sub, cls in classifications:
        if sub != subclass:
            continue
        if cls == NO_TRADE_ANCHOR:
            continue
        measured += 1
        if cls == DECISION_PRICE_BOTH_SIDES:
            both += 1
    rate = (both / measured) if measured else 0.0
    return both, measured, rate


# ---------------------------------------------------------------------------
# Pass 2 - HARD STOP (not authorized under this task)
# ---------------------------------------------------------------------------
def run_pass2(*args: Any, **kwargs: Any):
    """Pass 2 (full-universe sweep) is NOT implemented under this authorization.

    Pass 1 success does not auto-authorize Pass 2 (spec 6, LOCKED). Implementing Pass 2
    requires a separate, explicit go/no-go after the Pass 1 handoff is reviewed."""
    raise Pass2NotAvailable(
        "Pass 2 is not available. It requires separate explicit authorization "
        "(spec 6). Pass 1 success does not auto-authorize Pass 2."
    )


# ---------------------------------------------------------------------------
# Injectable I/O abstractions (real impls used on the user's box; tests inject mocks)
# ---------------------------------------------------------------------------
#
# The orchestrator (run_pass1_coverage) depends ONLY on these three protocols, so
# pure-logic tests can drive the full run with mocks and never touch the network,
# the filesystem, parquet, or the store.
#
#   StoreLoader : reads P0 artifact, contract JSON, resolution-source rows, and
#                 per-condition (token_id, outcome_index) trade tuples + first_trade_ts.
#   Client      : PricesHistoryClient-shaped (get_prices_history / post_batch_prices_history).
#   ArtifactWriter : writes coverage-only artifacts under the S1 directory.
#
# None of these is constructed by Claude with a live network; the real Client is
# armed only by the two explicit CLI flags on the user's Windows box.


class StoreLoader:
    """Real loader. Reads local artifacts + trades via Store(root).

    Imports (pandas / pyarrow / Store) are LAZY so the module has no hard dependency
    and tests can import it in a bare environment. Claude does not execute this path.
    """

    def __init__(self, root: str, artifacts_dir: str):
        self.root = root
        self.artifacts_dir = artifacts_dir

    def _art(self, *parts: str) -> str:
        return os.path.join(self.artifacts_dir, *parts)

    def load_p0_preflight(self) -> Dict[str, Any]:
        import json

        path = self._art("named_binary_probe", "p0_preflight.json")
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def load_contract_conditions(self) -> List[Dict[str, Any]]:
        import json

        path = self._art("named_binary", "named_binary_classification_contract.json")
        with open(path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        # Version pin at the document level (DATA_CONTRACTS 1).
        assert_contract_version(doc.get("nb_contract_version"))
        return list(doc.get("conditions", []))

    def load_resolution_rows(self) -> List[Dict[str, Any]]:
        import pandas as pd  # lazy

        path = self._art("named_binary", "named_binary_resolution_source_rows.parquet")
        df = pd.read_parquet(path)

        # --- resolved_at diagnosis/fix (S1 blocker) --------------------------------
        # DATA_CONTRACTS §2 lists the timestamp column as `resolved_at`. Guard against a
        # schema/name drift AND against a coercion bug: a blanket df.astype(str) turns a
        # tz-aware datetime64 `resolved_at` into "2025-03-06 00:00:00+00:00", which
        # parse_ts rejects -> None -> blank -> the false all-invalid-window sample.
        #
        # Fix: string-cast the string-safe identity columns (token ids, indices) as before,
        # but DO NOT stringify `resolved_at` — carry it as the raw pandas value so
        # parse_ts's datetime branch handles Timestamp/tz-aware/naive correctly. If the
        # column is entirely absent, fail loud rather than silently blanking every window.
        if "resolved_at" not in df.columns:
            raise ValueError(
                "STOP_RESOLUTION_SCHEMA: resolution-source parquet has no 'resolved_at' "
                f"column. Present columns: {list(df.columns)}. Per DATA_CONTRACTS §2 the "
                "column must be named 'resolved_at'; inspect the resolution-source builder/"
                "export before rerunning S1 (do not silently remap block-time columns)."
            )
        string_safe_cols = [c for c in df.columns if c != "resolved_at"]
        for c in string_safe_cols:
            df[c] = df[c].astype(str)
        # resolved_at kept as-is (Timestamp / str / NaT). Convert to plain Python objects;
        # NaT/NaN -> None so downstream parse_ts fails cleanly per-row instead of on "NaT".
        resolved_col = df["resolved_at"].tolist()
        records = df[string_safe_cols].to_dict("records")
        for rec, ra in zip(records, resolved_col):
            rec["resolved_at"] = None if pd.isna(ra) else ra
        return records

    def load_trades_index(
        self, condition_ids: Sequence[str]
    ) -> Tuple[Dict[str, List[Tuple[str, str, str]]], Dict[str, float]]:
        """Return (trades_by_condition, first_trade_ts_by_condition) for the given cids.

        trades_by_condition[cid] = list of (condition_id, token_id, outcome_index) as STRINGS.
        first_trade_ts_by_condition[cid] = min(traded_at) epoch seconds.
        """
        import pandas as pd  # lazy  # noqa: F401
        from pm_research.data.store import Store  # lazy

        wanted = set(condition_ids)
        df = Store(self.root).load_trades()
        # Keep only eligible conditions; keep string safety on token_id/outcome_index.
        df = df[df["condition_id"].isin(wanted)]
        tuples: Dict[str, List[Tuple[str, str, str]]] = {}
        first_ts: Dict[str, float] = {}
        for cid, grp in df.groupby("condition_id"):
            rows: List[Tuple[str, str, str]] = []
            for tok, oi in zip(grp["token_id"].astype(str), grp["outcome_index"].astype(str)):
                rows.append((str(cid), tok, oi))
            tuples[str(cid)] = rows
            # traded_at may be datetime-like or epoch; normalize via parse_ts.
            tvals = [parse_ts(v) for v in grp["traded_at"].tolist()]
            if tvals:
                first_ts[str(cid)] = min(tvals)
        return tuples, first_ts


class ArtifactWriter:
    """Real writer. Writes coverage-only artifacts under the S1 directory.

    NEVER writes under prices/. NEVER persists a reusable price series. The by-condition
    CSV carries statuses/gaps/token ids/diagnostics only (enforced by the row schema).
    """

    S1_SUBPATH = ("named_binary_probe", "price_source_s1")

    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir

    def s1_dir(self) -> str:
        return os.path.join(self.artifacts_dir, *self.S1_SUBPATH)

    def _ensure_dir(self) -> str:
        d = self.s1_dir()
        # Refuse to ever target a prices/ path (belt-and-suspenders).
        if "prices" in os.path.normpath(d).split(os.sep):
            raise RuntimeError("refusing to write under a prices/ path")
        os.makedirs(d, exist_ok=True)
        return d

    def write_text(self, filename: str, text: str) -> str:
        d = self._ensure_dir()
        path = os.path.join(d, filename)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        return path

    def write_json(self, filename: str, obj: Dict[str, Any]) -> str:
        import json

        return self.write_text(filename, json.dumps(obj, indent=2, sort_keys=True))

    def write_csv(self, filename: str, header: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
        import csv
        import io

        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(list(header))
        for r in rows:
            w.writerow(list(r))
        return self.write_text(filename, buf.getvalue())


# Output filenames (spec 7). Exposed so tests can assert the exact set.
S1_ARTIFACT_FILENAMES = (
    "price_source_s1_coverage.json",
    "price_source_s1_coverage.md",
    "price_source_s1_coverage_by_condition.csv",
    "price_source_s1_endpoint_shape.md",
    "price_source_s1_excluded.csv",
)

# by-condition CSV schema - statuses/gaps/token ids/diagnostics ONLY, never a price value.
BY_CONDITION_HEADER = (
    "condition_id",
    "subclass",
    "side_0_token",
    "side_1_token",
    "level_a_side_0",
    "level_a_side_1",
    "condition_reachability",     # both / one / neither
    "level_b_class",
    "nearest_gap_side_0_seconds",
    "nearest_gap_side_1_seconds",
    # Request-window diagnostics (so the orchestrator can verify the queried window per
    # condition, not just the first observed GET). Timestamps/counts only - never prices.
    "first_trade_ts",
    "decision_lower_ts",          # first_trade_ts + warmup_seconds
    "resolved_at_ts",
    "request_start_ts",
    "request_end_ts",
    "request_window_seconds",     # request_end_ts - request_start_ts
    "observed_point_count_side_0",
    "observed_point_count_side_1",
)
EXCLUDED_HEADER = ("condition_id", "subclass", "reason")

# Forbid any column name that would leak a price value into the ledger.
_FORBIDDEN_LEDGER_COLUMNS = frozenset(
    {"p", "price", "yes_price", "side_0_price", "side_1_price", "canonical_side_price", "series"}
)
assert not (_FORBIDDEN_LEDGER_COLUMNS & set(BY_CONDITION_HEADER)), (
    "by-condition ledger must not carry price values"
)


# ---------------------------------------------------------------------------
# Nearest-point gap diagnostic (Level B design input for S2; not a score)
# ---------------------------------------------------------------------------
def nearest_gap_seconds(
    points: Sequence[PricePoint],
    first_trade_ts: Optional[float],
    resolved_at_ts: float,
    warmup_seconds: int = WARMUP_SECONDS,
) -> Optional[float]:
    """Absolute time gap (seconds) between the decision timestamp lower bound and the
    nearest IN-WINDOW point (ts in [decision_lower, resolved_at)). None if no in-window
    point or no anchor. Diagnostic only - never a coverage verdict or a price."""
    if first_trade_ts is None:
        return None
    lower = first_trade_ts + warmup_seconds
    best: Optional[float] = None
    for pt in points:
        if pt.ts >= lower and pt.ts < resolved_at_ts:
            gap = abs(pt.ts - lower)
            if best is None or gap < best:
                best = gap
    return best


# ---------------------------------------------------------------------------
# Level C - validation-sample integrity checks (spec 4.3)
# ---------------------------------------------------------------------------
def level_c_validation(
    validation_pairs: Sequence[Tuple[str, SeriesResult, SeriesResult]],
) -> Dict[str, Any]:
    """Trust checks on a small spread sample (spec 4.3). Records diagnostics only:
    value-range in [0,1], side_0+side_1 distribution at coincident ts (NOT enforced =1),
    token-id echo integrity, timestamp monotonicity. Any precision/sci-notation issue is a
    hard SERIES_MALFORMED already caught upstream; here we surface trust flags."""
    checks = {
        "n_validated": len(validation_pairs),
        "value_range_ok": True,
        "token_echo_ok": True,
        "timestamps_monotone_ok": True,
        "complementarity_samples": [],  # diagnostic distribution of side_0 + side_1
    }
    for _cid, s0, s1 in validation_pairs:
        for s in (s0, s1):
            for pt in s.points:
                if not (0.0 <= pt.p <= 1.0):
                    checks["value_range_ok"] = False
                if str(pt.token_id) != str(s.token_id):
                    checks["token_echo_ok"] = False
            ts_seq = [pt.ts for pt in s.points]
            if any(b < a for a, b in zip(ts_seq, ts_seq[1:])):
                checks["timestamps_monotone_ok"] = False
        # Coincident-timestamp complementarity distribution (diagnostic only).
        by_ts0 = {pt.ts: pt.p for pt in s0.points}
        for pt in s1.points:
            if pt.ts in by_ts0:
                checks["complementarity_samples"].append(round(by_ts0[pt.ts] + pt.p, 6))
    return checks


# ---------------------------------------------------------------------------
# Pass-1 orchestration - the runnable coverage run (composes the pure logic)
# ---------------------------------------------------------------------------
@dataclass
class RunConfig:
    root: str = r"C:\b1\data"
    artifacts_dir: str = "artifacts"
    sample_size: int = DEFAULT_PASS1_SAMPLE_SIZE
    seed: int = DEFAULT_SEED
    interval: str = "max"
    fidelity: Optional[int] = None
    allow_batch: bool = False
    network_authorized: bool = False  # gates ALL fetch + ALL artifact writes
    quiet: bool = False              # suppress [S1] progress heartbeat on stderr
    progress_every: int = 25         # print a fetch-loop heartbeat every N sampled conditions


# ---------------------------------------------------------------------------
# Progress / heartbeat (stderr only; never stdout, never price data, never token lists)
# ---------------------------------------------------------------------------
def _fmt_elapsed(seconds: float) -> str:
    """Format elapsed seconds as HH:MM:SS for a heartbeat line (display only)."""
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _progress(quiet: bool, msg: str) -> None:
    """Emit one compact `[S1] ...` heartbeat line to STDERR so stdout stays
    machine-readable JSON. No-op when quiet. flush=True so long local runs show
    liveness immediately rather than buffering. NEVER prints a price series or a
    per-condition token list - counts and phase names only."""
    if quiet:
        return
    print(msg, file=sys.stderr, flush=True)


def _fetch_series_for_token(
    client: Any,
    token_id: str,
    start_ts: int,
    end_ts: int,
    cfg: "RunConfig",
) -> SeriesResult:
    """Single-token GET. (Batch is handled separately and equivalence-checked.)"""
    return client.get_prices_history(
        token_id, start_ts, end_ts, interval=cfg.interval, fidelity=cfg.fidelity
    )


def run_pass1_coverage(
    cfg: "RunConfig",
    loader: Any,
    client: Any,
    writer: Any,
) -> Dict[str, Any]:
    """Execute the S1 Pass-1 coverage run end-to-end, PASS 1 ONLY.

    Structural guarantees (each enforced below):
      * No fetch and NO artifact write unless cfg.network_authorized is True
        (-> returns a STOP_NOT_AUTHORIZED result, writes nothing).
      * Only the deterministic Pass-1 SAMPLE is fetched - never the full universe.
      * Pass 2 is never reachable from here.
      * resolved_at is used only as the window upper bound.
      * The by-condition ledger carries no price values.

    Returns a machine-readable result dict (the same object written to
    price_source_s1_coverage.json when authorized).
    """
    # ---- Hard gate: without explicit network authorization, do nothing + write nothing.
    if not cfg.network_authorized:
        return {
            "s1_verdict": STOP_NOT_AUTHORIZED,
            "authorized_scope": AUTHORIZED_SCOPE,
            "wrote_artifacts": False,
            "pass2_available": False,
            "note": "network + writes are hard-gated; provide the two explicit CLI flags.",
        }

    # ---- (1) P0 + (2) contract + (3) resolution rows.
    _progress(cfg.quiet, "[S1] loading P0/contract/resolution/trades...")
    p0 = loader.load_p0_preflight()
    try:
        final_p0_eligible = validate_p0(p0)  # requires P0_CLEAR + version equality
    except ValueError as exc:
        return _stop_result(str(exc), cfg.quiet)

    contract_conditions = loader.load_contract_conditions()
    resolution_rows = loader.load_resolution_rows()

    # ---- (5) Universe = contract INTERSECT resolution join (subclass cross-check inside).
    try:
        universe = build_universe(contract_conditions, resolution_rows)
    except ValueError as exc:
        return _stop_result(str(exc), cfg.quiet)
    _progress(cfg.quiet, f"[S1] universe built: {len(universe)} conditions")

    # ---- (4)+(6) Trades index + token-pair enumeration from trades (never winners).
    cids = [c.condition_id for c in universe]
    trades_by_condition, first_trade_ts = loader.load_trades_index(cids)
    try:
        resolved_conditions, unresolved_conditions = resolve_token_pairs(
            universe, trades_by_condition
        )
    except DataExportPrecisionLoss as exc:
        return _stop_result(f"{STOP_PRECISION_LOSS}: {exc}", cfg.quiet)
    except ValueError as exc:
        return _stop_result(str(exc), cfg.quiet)
    # Diagnostic total (also reused below in the JSON result / excluded ledger, computed once
    # so the heartbeat line and the final artifact never drift from each other).
    malformed_trade_rows_total = sum(
        c.malformed_trade_rows for c in resolved_conditions
    ) + sum(c.malformed_trade_rows for c in unresolved_conditions)
    _progress(
        cfg.quiet,
        f"[S1] token pairs resolved: {len(resolved_conditions)}/{len(universe)}, "
        f"unresolved {len(unresolved_conditions)}, malformed trade rows {malformed_trade_rows_total}",
    )

    # ---- (7) Deterministic Pass-1 stratified SAMPLE only.
    sample = build_pass1_sample(resolved_conditions, cfg.sample_size, cfg.seed)
    # Structural assertion: we only ever fetch the bounded sample, never the whole universe.
    if len(sample) > cfg.sample_size:
        return _stop_result(f"{STOP_VALIDATION_REQUIRED}: sample bound violated", cfg.quiet)
    if len(resolved_conditions) > cfg.sample_size and len(sample) >= len(resolved_conditions):
        return _stop_result(f"{STOP_VALIDATION_REQUIRED}: sample not a strict subset", cfg.quiet)
    _progress(cfg.quiet, f"[S1] sample selected: {len(sample)} conditions")

    # ---- (8) Fetch both side tokens for SAMPLED conditions only.
    shape_sink: List[Dict[str, Any]] = []
    # Attach the sink to the client if it supports shape capture (real client + test doubles).
    if hasattr(client, "shape_sink"):
        client.shape_sink = shape_sink
    per_condition_rows: List[List[Any]] = []
    level_b_classifications: List[Tuple[str, str]] = []  # (subclass, level_b_class)
    level_a_pool: List[str] = []
    validation_pairs: List[Tuple[str, SeriesResult, SeriesResult]] = []
    fetched_token_count = 0
    batch_equiv_results: List[bool] = []
    request_window_seconds_list: List[int] = []  # per-condition request window widths (diagnostic)
    # Invalid decision-window conditions (resolved_at missing OR <= first_trade_ts+warmup):
    # never fetched, never classified DECISION_PRICE_NEITHER; excluded + reported separately.
    invalid_window_conditions: List[ConditionRecord] = []
    invalid_window_by_subclass: Dict[str, int] = {}
    valid_window_by_subclass: Dict[str, int] = {}

    try:
        fetch_start = time.monotonic()
        total_sample = len(sample)
        for i, cond in enumerate(sample):
            # Heartbeat: always before the first fetch (i==0), then every progress_every
            # sampled conditions. Counts + elapsed time only - never a price series, never
            # a per-condition token list.
            if i == 0 or (cfg.progress_every > 0 and i % cfg.progress_every == 0):
                elapsed = _fmt_elapsed(time.monotonic() - fetch_start)
                _progress(
                    cfg.quiet,
                    f"[S1] fetching coverage: {i}/{total_sample} conditions, elapsed {elapsed}",
                )

            resolved_at_ts = _safe_resolved_at(cond.resolved_at)
            ft = first_trade_ts.get(cond.condition_id)
            decision_lower = (ft + WARMUP_SECONDS) if ft is not None else None

            # ---- Guard: a condition with no VALID decision window is not measurable coverage.
            # resolved_at missing OR resolved_at <= first_trade_ts + warmup => NO ex-ante window.
            # We do NOT query the endpoint and do NOT classify it DECISION_PRICE_NEITHER; it is
            # excluded and reported so it cannot masquerade as a real coverage negative. This is
            # the fix for the all-1-second / all-NEITHER / false-NOT_VIABLE artifact.
            if not valid_decision_window(ft, resolved_at_ts):
                invalid_window_conditions.append(cond)
                invalid_window_by_subclass[cond.subclass] = (
                    invalid_window_by_subclass.get(cond.subclass, 0) + 1
                )
                win_secs = (
                    "" if (resolved_at_ts is None or decision_lower is None)
                    else int(resolved_at_ts) - int(decision_lower)
                )
                per_condition_rows.append([
                    cond.condition_id, cond.subclass, cond.side_0_token, cond.side_1_token,
                    "NOT_QUERIED", "NOT_QUERIED", "n/a", NO_VALID_DECISION_WINDOW,
                    "", "",
                    "" if ft is None else int(ft),
                    "" if decision_lower is None else int(decision_lower),
                    "" if resolved_at_ts is None else int(resolved_at_ts),
                    "", "", win_secs, 0, 0,
                ])
                continue

            valid_window_by_subclass[cond.subclass] = (
                valid_window_by_subclass.get(cond.subclass, 0) + 1
            )
            # Request window spans the FULL decision window (validity already guaranteed above,
            # so this can never collapse to the pathological 1-second clamp).
            start_ts, end_ts = _decision_request_window(ft, resolved_at_ts)

            s0 = _fetch_series_for_token(client, cond.side_0_token, start_ts, end_ts, cfg)
            s1 = _fetch_series_for_token(client, cond.side_1_token, start_ts, end_ts, cfg)
            fetched_token_count += 2

            # Optional batch equivalence - only if explicitly enabled.
            if cfg.allow_batch:
                batched = client.post_batch_prices_history(
                    [cond.side_0_token, cond.side_1_token], start_ts, end_ts,
                    interval=cfg.interval, fidelity=cfg.fidelity,
                )
                eq0 = batch_single_equivalent(s0, batched.get(cond.side_0_token, s0))
                eq1 = batch_single_equivalent(s1, batched.get(cond.side_1_token, s1))
                batch_equiv_results.extend([eq0, eq1])

            level_a_pool.extend([s0.status, s1.status])

            both_present = s0.status == SERIES_PRESENT and s1.status == SERIES_PRESENT
            one_present = (s0.status == SERIES_PRESENT) ^ (s1.status == SERIES_PRESENT)
            reach = "both" if both_present else ("one" if one_present else "neither")

            # resolved_at_ts is guaranteed non-None here (validity guard above).
            lb = classify_decision_window(s0, s1, ft, resolved_at_ts)
            level_b_classifications.append((cond.subclass, lb))

            gap0 = nearest_gap_seconds(s0.points, ft, resolved_at_ts)
            gap1 = nearest_gap_seconds(s1.points, ft, resolved_at_ts)

            request_window_seconds = end_ts - start_ts
            request_window_seconds_list.append(request_window_seconds)
            per_condition_rows.append([
                cond.condition_id, cond.subclass, cond.side_0_token, cond.side_1_token,
                s0.status, s1.status, reach, lb,
                "" if gap0 is None else round(gap0, 3),
                "" if gap1 is None else round(gap1, 3),
                "" if ft is None else int(ft),
                "" if decision_lower is None else int(decision_lower),
                int(resolved_at_ts),
                start_ts,
                end_ts,
                request_window_seconds,
                len(s0.points),
                len(s1.points),
            ])
            validation_pairs.append((cond.condition_id, s0, s1))
        if total_sample:
            elapsed = _fmt_elapsed(time.monotonic() - fetch_start)
            _progress(
                cfg.quiet,
                f"[S1] fetching coverage: {len(request_window_seconds_list)}/{total_sample} "
                f"valid-window conditions fetched ({len(invalid_window_conditions)} skipped, "
                f"invalid window), elapsed {elapsed}",
            )
    except EndpointShapeError as exc:
        # Surface the deviation: build shape observations from whatever was captured
        # (including the deviating response), record them in the returned result, and
        # best-effort write price_source_s1_endpoint_shape.md so S2 review can see it.
        shape_obs = _build_shape_observations(shape_sink, deviation=str(exc))
        try:
            writer.write_text(
                "price_source_s1_endpoint_shape.md", _render_endpoint_shape_md(shape_obs)
            )
            wrote_shape = True
        except Exception:  # noqa: BLE001 - shape capture must never mask the stop verdict
            wrote_shape = False
        stop = _stop_result(f"{STOP_ENDPOINT_SHAPE_UNRECOGNIZED}: {exc}", cfg.quiet)
        stop["endpoint_shape_observations"] = shape_obs
        stop["endpoint_shape_written"] = wrote_shape
        return stop
    except DataExportPrecisionLoss as exc:
        return _stop_result(f"{STOP_PRECISION_LOSS}: {exc}", cfg.quiet)

    # ---- (10) Level C validation BEFORE trusting any all-one aggregate.
    all_one_a = all_one_status_guard(level_a_pool)
    val_sample = _spread_validation_sample(validation_pairs, sample, max_n=30)
    level_c = level_c_validation(val_sample)
    validation_required = bool(
        all_one_a and not (
            level_c["value_range_ok"]
            and level_c["token_echo_ok"]
            and level_c["timestamps_monotone_ok"]
        )
    )

    # ---- (9) Coverage rates per subclass (Level B binding).
    per_subclass: Dict[str, Dict[str, Any]] = {}
    for sub in ORIENTED_SUBCLASSES:
        both, measured, rate = subclass_coverage_rate(level_b_classifications, sub)
        per_subclass[sub] = {
            "both_sides": both,
            "measured": measured,
            "rate": round(rate, 6),
            "clears_threshold": bool(measured and rate >= SUBCLASS_BOTH_SIDES_THRESHOLD),
        }

    verdict = _pass1_verdict(per_subclass, level_a_pool, validation_required)

    # ---- Invalid-window override: if NOTHING in the sample had a valid decision window,
    # endpoint coverage was never measured. That is NOT a coverage negative — it is
    # inconclusive. Never report S1_SOURCE_NOT_VIABLE in that case.
    n_valid_window = len(request_window_seconds_list)
    n_invalid_window = len(invalid_window_conditions)
    if n_valid_window == 0:
        verdict = S1_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE

    # ---- Excluded ledger. (malformed_trade_rows_total was already computed once, right
    # after resolve_token_pairs, and is reused here so the heartbeat line and this ledger
    # never drift from each other.)
    excluded_rows: List[List[Any]] = []
    for c in unresolved_conditions:
        reason = TOKEN_PAIR_UNRESOLVED
        if c.malformed_trade_rows:
            reason = f"{TOKEN_PAIR_UNRESOLVED} (malformed_trade_rows={c.malformed_trade_rows})"
        excluded_rows.append([c.condition_id, c.subclass, reason])
    for cond, (sub, lb) in zip(sample, level_b_classifications):
        if lb == NO_TRADE_ANCHOR:
            excluded_rows.append([cond.condition_id, sub, NO_TRADE_ANCHOR])
    # Invalid decision-window conditions: excluded + reported with window diagnostics.
    for c in invalid_window_conditions:
        ft_c = first_trade_ts.get(c.condition_id)
        ra_c = _safe_resolved_at(c.resolved_at)
        dl_c = (ft_c + WARMUP_SECONDS) if ft_c is not None else None
        win = ("" if (ra_c is None or dl_c is None) else int(ra_c) - int(dl_c))
        excluded_rows.append([
            c.condition_id, c.subclass,
            f"{NO_VALID_DECISION_WINDOW} "
            f"(first_trade_ts={'' if ft_c is None else int(ft_c)}, "
            f"decision_lower_ts={'' if dl_c is None else int(dl_c)}, "
            f"resolved_at_ts={'' if ra_c is None else int(ra_c)}, "
            f"window_seconds={win})",
        ])

    # ---- Reconciliation (universe-level; the sample is an explicit subset this pass).
    universe_recon = reconcile(
        final_p0_eligible,
        {
            "resolved_pairs": len(resolved_conditions),
            "token_pair_unresolved": len(unresolved_conditions),
            "not_in_sample_this_pass": final_p0_eligible
            - len(resolved_conditions)
            - len(unresolved_conditions),
        },
    )

    # ---- Observed endpoint shape (from the capture sink) for the shape ledger.
    endpoint_shape_observations = _build_shape_observations(shape_sink)

    # ---- Request-window distribution (diagnostic; guards against the 1-second-window bug
    # being masked by an all-one aggregate or a single observed GET example).
    request_window = request_window_summary(request_window_seconds_list, sample)

    result = {
        "s1_verdict": verdict,
        "pass": 1,
        "authorized_scope": AUTHORIZED_SCOPE,
        "nb_contract_version": NB_CONTRACT_VERSION,
        "p0_state": p0.get("p0_state"),
        "final_p0_eligible": final_p0_eligible,
        "universe_resolved_pairs": len(resolved_conditions),
        "token_pair_unresolved": len(unresolved_conditions),
        "malformed_trade_rows_total": malformed_trade_rows_total,
        "request_window_summary": request_window,
        "decision_window_validity": {
            "sampled": len(sample),
            "valid_window": n_valid_window,
            "invalid_window": n_invalid_window,
            "valid_window_by_subclass": valid_window_by_subclass,
            "invalid_window_by_subclass": invalid_window_by_subclass,
            "note": (
                "Invalid = resolved_at missing OR resolved_at <= first_trade_ts+warmup. "
                "Invalid-window conditions are NOT fetched and NOT counted as "
                "DECISION_PRICE_NEITHER; they are excluded and reported separately. "
                "Coverage rates below are measured over VALID-window conditions only."
            ),
        },
        "sample_size_requested": cfg.sample_size,
        "sample_size_actual": len(sample),
        "fetched_token_count": fetched_token_count,
        "sampled_only": len(sample) <= cfg.sample_size
        and (len(resolved_conditions) <= cfg.sample_size or len(sample) < len(resolved_conditions)),
        "level_a_status_counts": _count(level_a_pool),
        "level_b_class_counts": _count([lb for _s, lb in level_b_classifications]),
        "per_subclass_coverage": per_subclass,
        "level_c_validation": level_c,
        "all_one_level_a": all_one_a,
        "validation_required": validation_required,
        "batch_enabled": cfg.allow_batch,
        "batch_equivalence_all_ok": (all(batch_equiv_results) if batch_equiv_results else None),
        "endpoint_shape_observations": endpoint_shape_observations,
        "universe_reconciliation": universe_recon,
        "named_binary_probe_blocked_observed": bool(
            p0.get("named_binary_probe_blocked_observed", True)
        ),
        "pass2_available": False,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    # ---- Set final-state fields BEFORE writing the JSON so the artifact reflects them.
    result["wrote_artifacts"] = True
    result["artifact_dir"] = writer.s1_dir()

    # ---- (11) Write coverage-only artifacts (only reached when authorized).
    _progress(cfg.quiet, "[S1] writing artifacts...")
    _write_all_artifacts(
        writer, result, per_condition_rows, excluded_rows, cfg, endpoint_shape_observations
    )
    _progress(cfg.quiet, f"[S1] done: verdict={verdict}")
    return result


def _safe_resolved_at(resolved_at: str) -> Optional[float]:
    try:
        return parse_ts(resolved_at)
    except ValueError:
        return None


def valid_decision_window(
    first_trade_ts: Optional[float],
    resolved_at_ts: Optional[float],
    warmup_seconds: int = WARMUP_SECONDS,
) -> bool:
    """A condition has a usable ex-ante decision window iff BOTH anchors exist AND
    resolved_at is strictly AFTER the decision lower bound:

        decision_lower = first_trade_ts + warmup_seconds
        valid  <=>  resolved_at_ts is not None
                    AND first_trade_ts is not None
                    AND resolved_at_ts > decision_lower

    If invalid, there is no interval `[decision_lower, resolved_at)` in which a decision-window
    point could ever exist, so the condition is NOT measurable coverage — it must be excluded
    and reported, never queried, and never classified DECISION_PRICE_NEITHER.
    """
    if first_trade_ts is None or resolved_at_ts is None:
        return False
    return resolved_at_ts > (first_trade_ts + warmup_seconds)


def _decision_request_window(
    first_trade_ts: Optional[float],
    resolved_at_ts: Optional[float],
    warmup_seconds: int = WARMUP_SECONDS,
) -> Tuple[int, int]:
    """Build the endpoint REQUEST window that must fully contain the decision window.

    Returns (start_ts, end_ts) as integer epoch seconds where:
        lower = first_trade_ts + warmup_seconds   -> request start = floor(lower)
        upper = resolved_at                        -> request end   = ceil(upper)

    The request is deliberately INCLUSIVE of the upper bound (ceil) so a decision-window
    point that sits just below resolved_at is actually returned by the endpoint; the
    leakage-safe cut (strictly `< resolved_at`) is applied later in classify_decision_window,
    NEVER by narrowing the request. This function never returns a 1-second window when a real
    resolved_at is available (that pathological narrow window was the bug).

    Degenerate inputs:
      * no trade anchor -> request from 0 (Level B will yield NO_TRADE_ANCHOR regardless).
      * no resolved_at  -> end = start + 1 (cannot bound the window; Level B can't classify it
                           as in-window, so this stays a non-usable diagnostic, not a false hit).
      * lower >= upper  -> clamp end to start + 1 so the request is still well-formed; the
                           window is effectively empty and Level B will not find an in-window
                           point (correctly), rather than silently querying a backwards range.
    """
    if first_trade_ts is None:
        lower = 0.0
    else:
        lower = first_trade_ts + warmup_seconds
    start_ts = int(math.floor(lower))
    if resolved_at_ts is None:
        return start_ts, start_ts + 1
    end_ts = int(math.ceil(resolved_at_ts))
    if end_ts <= start_ts:
        end_ts = start_ts + 1
    return start_ts, end_ts


def _stop_result(verdict: str, quiet: bool = True) -> Dict[str, Any]:
    _progress(quiet, f"[S1] done: verdict={verdict}")
    return {
        "s1_verdict": verdict,
        "authorized_scope": AUTHORIZED_SCOPE,
        "wrote_artifacts": False,
        "pass2_available": False,
        "note": "run halted with a typed stop state; no coverage artifacts written.",
    }


def _count(values: Sequence[str]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return out


def _median(values: Sequence[float]) -> Optional[float]:
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0


def request_window_summary(
    window_seconds: Sequence[int],
    sample: Sequence[ConditionRecord],
) -> Dict[str, Any]:
    """Compact request-window distribution so a single 1-second observed GET can never be
    mistaken for the whole sample. Counts/seconds only - no prices, no series.

    Guards specifically against the request-window bug: count_le_1 counts pathological
    ~1-second windows; count_gt_3600 counts windows wide enough to actually contain a
    decision-window point at first_trade_ts + 3600."""
    subclass_counts: Dict[str, int] = {}
    for c in sample:
        subclass_counts[c.subclass] = subclass_counts.get(c.subclass, 0) + 1
    if not window_seconds:
        return {
            "n": 0,
            "min_request_window_seconds": None,
            "median_request_window_seconds": None,
            "max_request_window_seconds": None,
            "count_request_window_seconds_le_1": 0,
            "count_request_window_seconds_le_60": 0,
            "count_request_window_seconds_gt_3600": 0,
            "sample_count_by_subclass": subclass_counts,
        }
    return {
        "n": len(window_seconds),
        "min_request_window_seconds": int(min(window_seconds)),
        "median_request_window_seconds": _median(window_seconds),
        "max_request_window_seconds": int(max(window_seconds)),
        "count_request_window_seconds_le_1": sum(1 for w in window_seconds if w <= 1),
        "count_request_window_seconds_le_60": sum(1 for w in window_seconds if w <= 60),
        "count_request_window_seconds_gt_3600": sum(1 for w in window_seconds if w > 3600),
        "sample_count_by_subclass": subclass_counts,
    }


def _spread_validation_sample(
    validation_pairs: Sequence[Tuple[str, SeriesResult, SeriesResult]],
    sample: Sequence[ConditionRecord],
    max_n: int = 30,
) -> List[Tuple[str, SeriesResult, SeriesResult]]:
    by_cid = {c.condition_id: c.subclass for c in sample}
    per_sub: Dict[str, List[Tuple[str, SeriesResult, SeriesResult]]] = {}
    for vp in validation_pairs:
        sub = by_cid.get(vp[0], "UNKNOWN")
        per_sub.setdefault(sub, []).append(vp)
    out: List[Tuple[str, SeriesResult, SeriesResult]] = []
    subs = list(per_sub.keys())
    i = 0
    while len(out) < max_n and any(per_sub[s] for s in subs):
        s = subs[i % len(subs)]
        if per_sub[s]:
            out.append(per_sub[s].pop())
        i += 1
    return out


def _pass1_verdict(
    per_subclass: Dict[str, Dict[str, Any]],
    level_a_pool: Sequence[str],
    validation_required: bool,
) -> str:
    if validation_required:
        return STOP_VALIDATION_REQUIRED
    measured_any = any(v["measured"] for v in per_subclass.values())
    if not measured_any:
        return S1_SOURCE_NOT_VIABLE
    clears = [v["clears_threshold"] for v in per_subclass.values() if v["measured"]]
    if clears and all(clears) and len(clears) == len(ORIENTED_SUBCLASSES):
        return S1_SOURCE_VIABLE
    if any(clears):
        return S1_SOURCE_PARTIAL
    return S1_SOURCE_NOT_VIABLE


def _write_all_artifacts(
    writer: Any,
    result: Dict[str, Any],
    per_condition_rows: Sequence[Sequence[Any]],
    excluded_rows: Sequence[Sequence[Any]],
    cfg: "RunConfig",
    endpoint_shape_observations: Sequence[str],
) -> None:
    writer.write_json("price_source_s1_coverage.json", result)
    writer.write_text("price_source_s1_coverage.md", _render_coverage_md(result))
    writer.write_csv(
        "price_source_s1_coverage_by_condition.csv", BY_CONDITION_HEADER, per_condition_rows
    )
    writer.write_text(
        "price_source_s1_endpoint_shape.md",
        _render_endpoint_shape_md(endpoint_shape_observations, result.get("request_window_summary")),
    )
    writer.write_csv("price_source_s1_excluded.csv", EXCLUDED_HEADER, excluded_rows)


def _render_coverage_md(result: Dict[str, Any]) -> str:
    lines = [
        "# S1 Price-Source Coverage - Pass 1 (coverage-only)",
        "",
        f"- verdict: **{result.get('s1_verdict')}**",
        f"- pass: {result.get('pass')}",
        f"- nb_contract_version: {result.get('nb_contract_version')}",
        f"- p0_state: {result.get('p0_state')}",
        f"- final_p0_eligible: {result.get('final_p0_eligible')}",
        f"- universe resolved pairs: {result.get('universe_resolved_pairs')}",
        f"- token-pair unresolved: {result.get('token_pair_unresolved')}",
        f"- malformed trade rows (skipped, diagnostic only): "
        f"{result.get('malformed_trade_rows_total')}",
        f"- sample size (actual/requested): "
        f"{result.get('sample_size_actual')}/{result.get('sample_size_requested')}",
        f"- fetched token count: {result.get('fetched_token_count')} "
        f"(sampled-only: {result.get('sampled_only')})",
        f"- Pass 2 available: {result.get('pass2_available')}",
        "",
        "## Level A status counts",
        "(Level A here = endpoint response for the queried decision window "
        "[floor(first_trade_ts+warmup), ceil(resolved_at)], not a broader 'series exists at "
        "all' probe. SERIES_EMPTY = no points in that window.)",
        f"{result.get('level_a_status_counts')}",
        "",
        "## Request-window summary (diagnostic — guards against the 1-second-window bug)",
        f"{result.get('request_window_summary')}",
        "",
        "## Decision-window validity (invalid = resolved_at missing or <= first_trade_ts+warmup)",
        "(Invalid-window conditions are NOT fetched and NOT counted as DECISION_PRICE_NEITHER; "
        "they are excluded and reported. Coverage is measured over valid-window conditions only.)",
        f"{result.get('decision_window_validity')}",
        "",
        "## Level B decision-window classes",
        f"{result.get('level_b_class_counts')}",
        "",
        "## Per-subclass both-sides coverage (Level B binding, threshold 0.95)",
    ]
    for sub, v in (result.get("per_subclass_coverage") or {}).items():
        lines.append(
            f"- {sub}: {v['both_sides']}/{v['measured']} = {v['rate']} "
            f"(clears: {v['clears_threshold']})"
        )
    lines += [
        "",
        "## Level C validation",
        f"{result.get('level_c_validation')}",
        "",
        "## Honest framing",
        "Pass 1 measures whether the CLOB /prices-history source *can* cover the P0 "
        "universe with a usable decision-window per-side price. A NOT_VIABLE / PARTIAL "
        "result is an acceptable, expected outcome and leaves P1 blocked with no yes_price "
        "fallback. Pass 1 success does NOT authorize Pass 2, S2, or the probe.",
    ]
    return "\n".join(lines) + "\n"


def _build_shape_observations(
    shape_sink: Sequence[Dict[str, Any]],
    deviation: Optional[str] = None,
) -> Dict[str, Any]:
    """Convert captured raw request/response entries into a STRUCTURAL shape record.

    Records the first observed single-token GET and the first batch POST (path, params,
    HTTP status, top-level keys, series key, first-point keys, point count, Level-A status),
    plus any recorded deviation. NEVER stores a reusable price series - keys/counts only.
    Token ids may appear (they are already in the coverage ledger).
    """
    obs: Dict[str, Any] = {
        "get_observed": None,
        "batch_observed": None,
        "deviation": deviation,
        "n_captured": len(shape_sink),
    }
    first_get = next((e for e in shape_sink if e.get("context") == "get"), None)
    first_batch = next((e for e in shape_sink if e.get("context") == "batch"), None)

    if first_get is not None:
        facts = observe_response_shape(
            first_get.get("http_status"),
            first_get.get("body"),
            str(first_get.get("payload", {}).get("market", "")),
        )
        obs["get_observed"] = {
            "path": first_get.get("path"),
            "params_used": first_get.get("payload_keys"),
            "params": first_get.get("payload"),
            "http_status": facts["http_status"],
            "top_level_keys": facts["top_level_keys"],
            "series_key": facts["series_key"],
            "point_count": facts["point_count"],
            "first_point_keys": facts["first_point_keys"],
            "level_a_status": facts["level_a_status"],
            "note": facts["note"],
        }
        if facts["level_a_status"] == STOP_ENDPOINT_SHAPE_UNRECOGNIZED and not obs["deviation"]:
            obs["deviation"] = facts["note"]

    if first_batch is not None:
        body = first_batch.get("body")
        histories_present = isinstance(body, dict) and "histories" in body
        obs["batch_observed"] = {
            "path": first_batch.get("path"),
            "payload_keys": first_batch.get("payload_keys"),
            "payload": first_batch.get("payload"),
            "http_status": first_batch.get("http_status"),
            "top_level_keys": sorted(str(k) for k in body.keys())
            if isinstance(body, dict) else None,
            "histories_key_present": histories_present,
        }
    return obs


def _render_endpoint_shape_md(observations: Any, request_window: Optional[Dict[str, Any]] = None) -> str:
    lines = [
        "# S1 Endpoint Shape - DOCUMENTED vs OBSERVED",
        "",
        "## DOCUMENTED SHAPE (spec 5)",
        "- GET /prices-history: market=<token_id>, startTs, endTs, interval, fidelity (camelCase).",
        "- POST /batch-prices-history: markets=[...], start_ts, end_ts, interval, fidelity (snake).",
        "- Response: history/prices = list of points, each with timestamp t and price p.",
        "- p is recorded as a SOURCE-DEFINED CLOB history price for the queried token; "
        "S1 performs no complementary-side conversion and asserts no canonical-probability meaning.",
        "- This file records STRUCTURE ONLY (keys, counts, statuses). No reusable price "
        "series is persisted. Token ids may appear (already in the coverage ledger).",
        "- **Level A scope note:** the Level A status recorded here reflects the endpoint "
        "response for the QUERIED decision window [floor(first_trade_ts+warmup), ceil(resolved_at)], "
        "not a broader 'does any history exist at all' probe. S1 performs no separate "
        "full-range reachability query, so SERIES_EMPTY means 'no points in the decision "
        "window', which is exactly what Level B needs — it does not by itself prove the token "
        "has no history anywhere. A future S2 build may add a broader reachability probe if "
        "that distinction matters.",
        "",
        "## Request-window summary (whole sample)",
        "The single observed GET below is ONE SAMPLE ONLY. To verify the request window across "
        "the whole sample - and that it is not the pathological ~1-second window - read this "
        "distribution (also in price_source_s1_coverage.json -> request_window_summary and the "
        "per-condition columns in price_source_s1_coverage_by_condition.csv):",
        f"{request_window if request_window is not None else '(summary not available on this stop path)'}",
        "",
        "## OBSERVED (this run)",
    ]
    # Back-compat: allow a plain list of strings (legacy), else the structured dict.
    if isinstance(observations, dict):
        get_o = observations.get("get_observed")
        batch_o = observations.get("batch_observed")
        dev = observations.get("deviation")

        lines.append("### Single-token GET")
        lines.append("(first observed GET — ONE SAMPLE ONLY; see the request-window summary "
                     "above for the whole-sample distribution)")
        if get_o:
            lines += [
                f"- path: {get_o.get('path')}",
                f"- params used: {get_o.get('params_used')}",
                f"- params (list sizes redacted): {get_o.get('params')}",
                f"- HTTP status: {get_o.get('http_status')}",
                f"- top-level response keys: {get_o.get('top_level_keys')}",
                f"- detected series key: {get_o.get('series_key')}",
                f"- first point keys: {get_o.get('first_point_keys')}",
                f"- point count: {get_o.get('point_count')}",
                f"- Level A status: {get_o.get('level_a_status')}",
            ]
            if get_o.get("note"):
                lines.append(f"- note: {get_o.get('note')}")
        else:
            lines.append("- (no single-token GET captured this run)")

        lines.append("")
        lines.append("### Batch POST")
        if batch_o:
            lines += [
                f"- path: {batch_o.get('path')}",
                f"- payload keys: {batch_o.get('payload_keys')}",
                f"- payload (list sizes redacted): {batch_o.get('payload')}",
                f"- HTTP status: {batch_o.get('http_status')}",
                f"- top-level response keys: {batch_o.get('top_level_keys')}",
                f"- histories key present: {batch_o.get('histories_key_present')}",
            ]
        else:
            lines.append("- (batch not exercised this run; enable with --allow-batch)")

        lines.append("")
        lines.append("### Deviation")
        lines.append(f"- {dev}" if dev else "- (none; responses parsed to the documented shape)")
    elif observations:
        lines.extend(f"- {o}" for o in observations)
    else:
        lines.append("- (no shape observations recorded)")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI (guards network behind explicit flags; Claude never runs the network path)
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="S1 price-source coverage - Pass 1 only (coverage-only; no writes to prices/)."
    )
    p.add_argument("--root", default=r"C:\b1\data", help="Local data store root (trades).")
    p.add_argument(
        "--artifacts-dir",
        default="artifacts",
        help="Artifacts root; S1 writes only under artifacts/named_binary_probe/price_source_s1/.",
    )
    p.add_argument("--sample-size", type=int, default=DEFAULT_PASS1_SAMPLE_SIZE)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--interval", default="max")
    p.add_argument("--fidelity", type=int, default=None)
    p.add_argument(
        "--i-authorize-s1-pass1-network-run",
        action="store_true",
        help="Explicit per-task network authorization (user-run on Windows box only).",
    )
    p.add_argument(
        "--confirm-external-host",
        default="",
        help="Must equal 'clob.polymarket.com' to arm the network path.",
    )
    p.add_argument(
        "--allow-batch",
        action="store_true",
        help="Permit POST /batch-prices-history as a candidate path (still checked vs single).",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the [S1] progress heartbeat on stderr (progress is ON by default).",
    )
    p.add_argument(
        "--progress-every",
        type=int,
        default=25,
        help="Print a fetch-loop heartbeat every N sampled conditions (default: 25).",
    )
    return p


def network_authorized_from_args(args: argparse.Namespace) -> bool:
    return bool(
        getattr(args, "i_authorize_s1_pass1_network_run", False)
        and getattr(args, "confirm_external_host", "") == "clob.polymarket.com"
    )


def build_run_config(args: argparse.Namespace) -> RunConfig:
    return RunConfig(
        root=args.root,
        artifacts_dir=args.artifacts_dir,
        sample_size=args.sample_size,
        seed=args.seed,
        interval=args.interval,
        fidelity=args.fidelity,
        allow_batch=bool(getattr(args, "allow_batch", False)),
        network_authorized=network_authorized_from_args(args),
        quiet=bool(getattr(args, "quiet", False)),
        progress_every=int(getattr(args, "progress_every", 25)),
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry. Composes the REAL loader/client/writer and runs Pass-1 coverage.

    Network + all artifact writes are hard-gated: without both explicit flags the run
    returns STOP_NOT_AUTHORIZED and writes nothing. This entry point is intended for the
    user's Windows box; Claude does not execute the authorized branch."""
    import json

    args = build_arg_parser().parse_args(argv)
    cfg = build_run_config(args)

    if not cfg.network_authorized:
        print(
            f"{STOP_NOT_AUTHORIZED}: S1 Pass-1 network run not authorized. "
            "This script performs no fetch and writes no artifacts without the explicit "
            "authorization flags. Provide --i-authorize-s1-pass1-network-run and "
            "--confirm-external-host clob.polymarket.com to arm the user-run network path."
        )
        return 2

    # Authorized branch (user-run only). Real, network-armed client.
    loader = StoreLoader(cfg.root, cfg.artifacts_dir)
    client = PricesHistoryClient(network_authorized=True, transport=None)
    writer = ArtifactWriter(cfg.artifacts_dir)

    result = run_pass1_coverage(cfg, loader, client, writer)
    print(json.dumps(
        {k: result[k] for k in ("s1_verdict", "wrote_artifacts", "pass2_available") if k in result},
        indent=2,
    ))
    if result.get("artifact_dir"):
        print(f"artifacts written under: {result['artifact_dir']}")
    # Non-zero exit on any typed stop verdict.
    stop_like = str(result.get("s1_verdict", "")).startswith("STOP_")
    return 3 if stop_like else 0


if __name__ == "__main__":
    raise SystemExit(main())
