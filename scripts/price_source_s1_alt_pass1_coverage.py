"""
S1-ALT Pass 1 — Option A local trade-print coverage test.

Governing spec: project_context/SPEC_price_source_alt_trade_prints.md
  (APPROVED / SPEC ONLY, precision-loss correction applied).
Predecessor: project_context/SPEC_price_source_s1_coverage.md (S1, ACCEPTED,
  verdict S1_SOURCE_NOT_VIABLE) and
  project_context/HANDOFF_orchestrator_s1_pass1_RESULT.md.

WHAT THIS SCRIPT IS
--------------------
A coverage-only feasibility measurement for ONE candidate per-side / token-identity
price source: local trade prints, read via `Store(root).load_trades()`. It answers,
for the SAME 300-condition Pass-1 sample used by the accepted S1 CLOB run:

    For each side token of each sampled condition, is there a usable trade-print
    price observation inside the leakage-safe decision window
    [first_trade_ts + warmup_seconds, resolved_at)?

It never builds a price artifact, never computes canonical_side_price, never scores
anything, never continues P1/P2/P3, never runs the named-binary probe, and never
touches wallets / OrdersMatched / log_index / PnL. `named_binary_probe_blocked` is
only ever observed, never assigned in this file (grep-checkable).

WHAT THIS SCRIPT IS NOT
------------------------
- Not network code. It never imports `requests`/`urllib`/`socket` and never
  constructs a URL. Only `Store(root).load_trades()` (local parquet) and the local
  JSON/CSV/parquet artifacts named on the CLI are read.
- Not Option B (Polymarket Data API `/trades`) or Option C (on-chain event
  reconstruction). Those are out of scope by the approved spec and by this task's
  explicit authorization.
- Not Pass 2, not an S2 build, not a P1/P2/P3 step, not the probe.

SAFE-BY-DEFAULT
----------------
Running this script with NO flags does nothing: it does not import pandas, does
not import `pm_research`, does not touch the filesystem beyond argument parsing,
and prints a plain STOP_NOT_AUTHORIZED message. Two explicit, separate flags are
required before anything happens:

    --i-authorize-s1-alt-pass1-local-run   gates ALL real reads (Store.load_trades,
                                            the resolution parquet, the two S1
                                            reproduction CSVs, the P0/contract JSON).
    --write-artifacts                      gates persisting any output file. Without
                                            it, an authorized run still computes the
                                            full coverage result (so it can be
                                            inspected on stdout) but writes nothing
                                            to disk.

This is deliberately stricter than a single combined flag: the task's own
implementation requirement ("default to a safe non-execution / non-artifact-writing
mode") describes two distinct properties, so this script enforces both
independently rather than conflating them.

PRECISION-LOSS SCOPE (per the orchestrator-approved correction)
-----------------------------------------------------------------
Precision-loss handling applies ONLY to identifiers: `token_id`, `outcome_index`,
and any other integer-like identifier requiring digit-exact identity. A `price` is
validated solely as a finite numeric value in [0, 1]; scientific-notation
*formatting* of a numeric price is NOT an error and is NOT precision loss.

SETUP/SCHEMA STOPS vs DATA FINDINGS (per the orchestrator BLOCK patch)
-----------------------------------------------------------------------
The classification contract JSON and the resolution-source parquet are REQUIRED
pinned inputs. A missing, unreadable, or malformed required input (or one missing
its required columns / version field) halts with a typed SETUP stop --
STOP_CONTRACT_SCHEMA or STOP_RESOLUTION_SOURCE_SCHEMA -- BEFORE any coverage
classification, so a broken setup can never masquerade as a data finding such as
S1ALT_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE. A present-but-WRONG version
remains the distinguishable STOP_STALE_CONTRACT. Row-level gaps in a VALID
resolution-source table (a sampled condition absent, or its `resolved_at`
missing/unparseable) stay per-condition NO_VALID_DECISION_WINDOW_AFTER_WARMUP
exclusions -- reported, never coverage negatives, never global stops.

NO SYNTHESIS
-------------
No `yes_price`, no `1 - price`, no `1 - p`, no `1 - yes_price`, no complement-fill
between sides, and no use of the `side` (BUY/SELL) field or any label to construct
or flip a price. Each side's decision-time observation comes only from prints of
that side's own token, selected by token identity in outcome_index order.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Protocol

# ---------------------------------------------------------------------------
# Constants (pinned; reused, never redefined)
# ---------------------------------------------------------------------------

NB_CONTRACT_VERSION_EXPECTED = "nb-contract-2026-06-28.1"
ORIENTED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
LEVEL_B_THRESHOLD = 0.95

# warmup_seconds = 3600 == Rank 1A `--warmup-hours 1.0` (DATA_CONTRACTS §7).
# No shared constant exists to import; this duplication is accepted project
# convention, carried forward unchanged from S1.
DEFAULT_WARMUP_SECONDS = 3600.0

# Pinned, SETTLED figures from the accepted S1 Pass 1 finding (DECISION_LOG.md /
# HANDOFF_orchestrator_s1_pass1_RESULT.md /
# HANDOFF_orchestrator_s1_pass1_invalid_decision_window.md). The reconstructed
# sample must match these exactly, or the run halts with
# STOP_SAMPLE_IRREPRODUCIBLE rather than improvise a replacement sample.
#
# IMPORTANT — accepted S1 two-ledger shape (verified against the RESULT +
# invalid-decision-window handoffs): the accepted S1 code writes EVERY sampled
# condition into the by-condition ledger (RESULT: "by-condition rows == full
# sample"), and additionally writes each of the 52 invalid-window conditions
# into the excluded ledger. So:
#   - the by-condition ledger has all 300 rows: 248 measured (a real Level-B
#     class) + 52 NO_VALID_DECISION_WINDOW_AFTER_WARMUP;
#   - the excluded ledger has the 52 invalid-window conditions (same ids);
#   - the 52-id overlap between the two files is EXPECTED, not a defect.
# The sample is therefore the UNION of condition_ids across both files (300
# unique), with the valid/invalid split taken from each condition's status, not
# from raw file row counts.
S1_PASS1_EXPECTED_SAMPLE_SIZE = 300
S1_PASS1_EXPECTED_MEASURED_TOTAL = 248
S1_PASS1_EXPECTED_EXCLUDED_TOTAL = 52
S1_PASS1_EXPECTED_MEASURED_BY_SUBCLASS = {
    "UP_DOWN": 50,
    "OVER_UNDER": 98,
    "NAMED_OTHER": 100,
}
S1_PASS1_EXPECTED_EXCLUDED_REASON = "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"

# Verified against ARTIFACT_INDEX.md: the accepted S1 excluded ledger's `reason`
# field may bundle the exclusion CLASS together with parenthesized diagnostic
# details in the same string, e.g.
#   "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts=..., decision_lower_ts=...,
#    resolved_at_ts=..., window_seconds=-3444)"
# (ARTIFACT_INDEX: "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (with first_trade_ts /
# decision_lower_ts / resolved_at_ts / window_seconds)"). Reconstruction must
# decide on the leading CLASS token, never on the raw bundled string, while
# still preserving the raw string for audit.
_REASON_CLASS_RE = re.compile(r"^([^\s(]+)")


def _normalize_excluded_reason(raw_reason: Any) -> str:
    """
    Extract the leading reason CLASS from a raw excluded-ledger `reason` value,
    which may bundle parenthesized/whitespace-separated diagnostic details in
    the same field. Splits at the first whitespace or '(' character, whichever
    comes first; never mutates or drops the raw value -- callers keep the raw
    string for diagnostics/ledger output and use only this normalized class for
    decisions.

    Examples:
      "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"
        -> "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"
      "NO_VALID_DECISION_WINDOW_AFTER_WARMUP (first_trade_ts=1, window_seconds=-3444)"
        -> "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"
      "TOKEN_PAIR_UNRESOLVED (malformed_trade_rows=3)" -> "TOKEN_PAIR_UNRESOLVED"
    """
    if raw_reason is None:
        return ""
    s = str(raw_reason).strip()
    m = _REASON_CLASS_RE.match(s)
    return m.group(1) if m else s

# The invalid-window status token, as written by accepted S1 into BOTH the
# by-condition ledger (status / level_b_class column) and the excluded ledger
# (reason column).
S1_INVALID_WINDOW_STATUS = "NO_VALID_DECISION_WINDOW_AFTER_WARMUP"

# Candidate column names that carry a by-condition row's classification, in
# priority order. The accepted S1 by-condition ledger names it `level_b_class`
# (ARTIFACT_INDEX §price_source_s1); this tool's own ledger uses `status`. We
# accept either so the reconstructor is robust to which accepted-artifact
# variant is supplied, without ever guessing a value.
S1_BY_CONDITION_STATUS_COLUMNS = ("level_b_class", "status")

# A by-condition row is a MEASURED (valid-window) row iff its status names one
# of the real Level-B classes. Anything explicitly marked invalid-window is NOT
# measured. Any other/blank value is unrecognized -> irreproducible (never
# silently assumed measured).
S1_MEASURED_LEVEL_B_CLASSES = (
    "DECISION_PRICE_BOTH_SIDES",
    "DECISION_PRICE_ONE_SIDE",
    "DECISION_PRICE_NEITHER",
)

ARTIFACT_SUBDIR = Path("named_binary_probe") / "price_source_s1_alt"

BY_CONDITION_HEADER = [
    "condition_id",
    "subclass",
    "side_0_token",
    "side_1_token",
    "status",
    "level_b_class",
    "first_trade_ts",
    "decision_lower_ts",
    "resolved_at_ts",
    "side_0_observation_ts",
    "side_0_gap_seconds",
    "side_0_print_count_total",
    "side_1_observation_ts",
    "side_1_gap_seconds",
    "side_1_print_count_total",
]

# Forbidden-column guard: no price/probability column may ever appear in the
# by-condition ledger. Asserted at write time and exercised by tests.
_FORBIDDEN_LEDGER_SUBSTRINGS = ("price", "yes_price", "canonical", "prob", "_p_", "series")

EXCLUDED_HEADER = ["condition_id", "subclass", "reason", "detail"]


# ---------------------------------------------------------------------------
# Typed stop / status strings (all typed; no bare exceptions cross the CLI
# boundary uncaught)
# ---------------------------------------------------------------------------

STOP_NOT_AUTHORIZED = "STOP_NOT_AUTHORIZED"
STOP_P0_NOT_CLEAR = "STOP_P0_NOT_CLEAR"
STOP_CONTRACT_SCHEMA = "STOP_CONTRACT_SCHEMA"
STOP_RESOLUTION_SOURCE_SCHEMA = "STOP_RESOLUTION_SOURCE_SCHEMA"
STOP_STALE_CONTRACT = "STOP_STALE_CONTRACT"
STOP_SAMPLE_IRREPRODUCIBLE = "STOP_SAMPLE_IRREPRODUCIBLE"
STOP_PRECISION_LOSS = "STOP_PRECISION_LOSS"
STOP_TOKEN_ENUMERATION_UNRELIABLE = "STOP_TOKEN_ENUMERATION_UNRELIABLE"
STOP_VALIDATION_REQUIRED = "STOP_VALIDATION_REQUIRED"

# Required pinned inputs -- a setup/schema failure on either of these must halt
# BEFORE any coverage classification, so that a missing/malformed required
# artifact can never masquerade as a data finding (e.g. as
# S1ALT_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE).
REQUIRED_RESOLUTION_SOURCE_COLUMNS = ("condition_id", "resolved_at", "status", "nb_contract_version")

VERDICT_VIABLE = "S1ALT_SOURCE_VIABLE"
VERDICT_PARTIAL = "S1ALT_SOURCE_PARTIAL"
VERDICT_NOT_VIABLE = "S1ALT_SOURCE_NOT_VIABLE"
VERDICT_INCONCLUSIVE_NO_VALID_WINDOW = "S1ALT_INCONCLUSIVE_NO_VALID_DECISION_WINDOW_SAMPLE"

# Fraction of TOKEN_PAIR_UNRESOLVED (of the 300-condition sample) above which the
# enumeration basis is treated as unreliable rather than trustworthy.
TOKEN_ENUMERATION_UNRELIABLE_FRACTION = 0.5


class IdentifierPrecisionLoss(Exception):
    """
    Raised only for a genuinely present-but-mangled STRICT identifier
    (`token_id` -- a precision-critical 78-digit integer) -- e.g. scientific
    notation or a bare Python float standing in for a 78-digit integer.

    NOT raised for `outcome_index` (a bounded {0,1} integer slot field; see
    `canonical_outcome_index` -- a domain/shape violation there is not
    precision loss). Never raised for price, and never raised for a merely
    missing/blank/NaN value (that is handled by `_is_missing_field` and
    counted, not stopped). Per project discipline (DUNE_DATA_NOTES §5) this is
    always a hard stop for the whole run -- precision is unrecoverable and must
    never be silently reconstructed.
    """


# ---------------------------------------------------------------------------
# Pure-logic primitives (no I/O; fully unit-testable without pandas/Store)
# ---------------------------------------------------------------------------


def _is_missing_field(value: Any) -> bool:
    """True for None, blank/whitespace string, case-insensitive 'nan'/'none'
    string, or a real float NaN. False for any other value, including a
    non-null float that is NOT NaN (that is a precision-loss candidate, not a
    missing value) -- mirrors the accepted S1 `_is_missing_field` behavior."""
    if value is None:
        return True
    if isinstance(value, float) and value != value:  # NaN check
        return True
    if isinstance(value, str):
        s = value.strip()
        if s == "" or s.lower() in ("nan", "none"):
            return True
    return False


_SCI_NOTATION_RE = re.compile(r"^-?\d*\.?\d+[eE][+-]?\d+$")


def _precision_loss_message(reason: str, field_name: str, condition_id: Optional[str], raw_value: Any) -> str:
    """
    Builds an unambiguous STOP_PRECISION_LOSS diagnostic message: the reason,
    the FIELD NAME that triggered it, the CONDITION_ID if available, and the
    RAW offending value -- so a future failure is never ambiguous about which
    field, which condition, or what value caused it.
    """
    parts = [reason, f"field={field_name}"]
    if condition_id is not None:
        parts.append(f"condition_id={condition_id}")
    parts.append(f"raw_value={raw_value!r}")
    return ", ".join(parts)


def canonical_identifier(
    value: Any, *, field_name: str = "identifier", condition_id: Optional[str] = None
) -> str:
    """
    Normalize a non-missing STRICT identifier (`token_id` -- a precision-
    critical 78-digit integer) to a canonical string. Caller MUST have already
    excluded missing values via `_is_missing_field` -- this function assumes a
    present value.

    NOT for `outcome_index` -- that is a bounded {0,1} integer SLOT field with
    exact-float-safe forms, handled by the separate, more lenient
    `canonical_outcome_index` below. Using this strict function for
    `outcome_index` was the v4 bug (a legitimate `0.0`/`1.0` slot value was
    wrongly treated as identifier precision loss); this function is now scoped
    to `token_id` only.

    Precision-loss scope: strict identifiers ONLY. Raises
    IdentifierPrecisionLoss (with field name / condition_id / raw value in the
    message, via `_precision_loss_message`) for:
      - a string in scientific-notation numeric form (e.g. "5.20896e+76"),
      - any bare Python float (an identifier should never be a float; a float
        here means something upstream already lost precision),
      - any other type it does not recognize as string-safe.
    Never applied to price (see `valid_price` below), and never applied to
    `outcome_index` (see `canonical_outcome_index` below).
    """
    if isinstance(value, str):
        s = value.strip()
        if _SCI_NOTATION_RE.match(s):
            raise IdentifierPrecisionLoss(
                _precision_loss_message("scientific-notation identifier string", field_name, condition_id, value)
            )
        return s
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        raise IdentifierPrecisionLoss(
            _precision_loss_message("float identifier not string-safe", field_name, condition_id, value)
        )
    raise IdentifierPrecisionLoss(
        _precision_loss_message(f"unsupported identifier type {type(value)!r}", field_name, condition_id, value)
    )


def canonical_outcome_index(value: Any) -> str:
    """
    Normalize a non-missing `outcome_index` value. Unlike `canonical_identifier`
    (used for `token_id`, a precision-critical 78-digit identifier),
    `outcome_index` is a BOUNDED INTEGER SLOT field with exactly two valid
    values -- side_0 / side_1, per DATA_CONTRACTS_named_binary_probe.md §5-6
    ("resolved_winning_outcome_index -- string (e.g. "0", "1")"; orientation
    order "index 0 = side_0, index 1 = side_1"). Small integers (0 and 1) have
    EXACT float representation, so accepting 0.0/1.0/"0.0"/"1.0" alongside
    0/1/"0"/"1" is safe and is NOT precision loss -- there is no digit-exact
    identity at stake the way there is for a 78-digit token_id.

    Returns "0" or "1" for exactly these accepted forms: int 0/1; float 0.0/1.0
    (exact); str "0"/"1"/"0.0"/"1.0" (after stripping whitespace). Deliberately
    narrow -- only the forms explicitly reviewed as safe are accepted; this is
    NOT a general numeric-string parser (e.g. "1e0" or "+1.0" are NOT accepted,
    to keep the accepted-forms set exactly auditable).

    For anything else PRESENT but invalid -- non-integral (0.5), out-of-range
    (2, 2.0, "2"), or any unsupported type -- returns a display string
    guaranteed to never equal "0" or "1", so the caller's existing
    `idx not in ("0", "1")` malformed-row check catches it and counts it,
    exactly like today's handling of an out-of-range string. This function
    NEVER raises IdentifierPrecisionLoss -- a domain/shape violation on this
    bounded slot field is not precision loss, and per the task's "Prefer a
    typed schema stop if this happens during token-pair enumeration": a
    condition where invalid outcome_index values dominate still surfaces via
    the existing STOP_TOKEN_ENUMERATION_UNRELIABLE systemic guard (a
    genuinely typed, schema-level stop), while a single anomalous row does not
    halt the whole run.
    """
    if isinstance(value, bool):
        return f"invalid_bool:{value!r}"
    if isinstance(value, int):
        return str(value) if value in (0, 1) else f"out_of_range:{value!r}"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return f"non_finite:{value!r}"
        if value == 0.0:
            return "0"
        if value == 1.0:
            return "1"
        return f"non_integral_or_out_of_range:{value!r}"
    if isinstance(value, str):
        s = value.strip()
        if s in ("0", "0.0"):
            return "0"
        if s in ("1", "1.0"):
            return "1"
        return s
    return f"unsupported_type:{type(value)!r}:{value!r}"


def valid_price(value: Any) -> Optional[float]:
    """
    Returns a finite float in [0, 1] if `value` is a valid price observation,
    else None. This is the ONLY requirement for price. Scientific-notation
    FORMATTING of a numeric price (e.g. the string "4.2e-1" or a float that
    reprs in exponential form) is explicitly NOT an error here -- it is not
    checked at all, because precision-loss handling does not apply to price.
    """
    if value is None:
        return None
    if isinstance(value, str) and _is_missing_field(value):
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    if f < 0.0 or f > 1.0:
        return None
    return f


_TS_STRPTIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
)


def parse_ts(value: Any) -> float:
    """
    Shared timestamp parser for `traded_at` and `resolved_at`. Returns POSIX
    seconds (UTC). Raises ValueError on anything it cannot confidently parse
    as UTC -- it never guesses and never silently coerces; callers decide how
    to count/exclude a parse failure (a single bad row is not a run-level
    stop). Accepts:
      - pandas Timestamp / python datetime (duck-typed via `.to_pydatetime`,
        or a plain `datetime.datetime`); naive values are treated as UTC;
      - epoch numeric (int/float, or a numeric string);
      - the real accepted resolution-source string form
        "YYYY-MM-DD HH:MM:SS.mmm UTC" (millisecond fractional seconds) and
        the whole-second form "YYYY-MM-DD HH:MM:SS UTC";
      - bare ISO forms (with/without 'T', with/without fractional seconds);
      - date-only "YYYY-MM-DD".
    Rejects any explicit non-UTC timezone suffix (fail loud, do not guess).
    """
    if value is None:
        raise ValueError("timestamp is None")
    if isinstance(value, float) and value != value:
        raise ValueError("timestamp is NaN")

    # pandas.Timestamp / datetime-like duck typing
    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()
    if isinstance(value, _dt.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=_dt.timezone.utc)
        else:
            value = value.astimezone(_dt.timezone.utc)
        return value.timestamp()

    if isinstance(value, bool):
        raise ValueError(f"unsupported timestamp type bool: {value!r}")

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        s = value.strip()
        if s == "":
            raise ValueError("empty timestamp string")
        # epoch numeric string
        try:
            return float(s)
        except ValueError:
            pass
        if s.endswith(" UTC"):
            body = s[: -len(" UTC")].strip()
        elif s.endswith("UTC"):
            body = s[: -3].strip()
        else:
            m = re.search(r"\s+([A-Za-z]{2,5})$", s)
            if m and m.group(1).upper() != "UTC":
                raise ValueError(f"non-UTC timezone suffix rejected: {value!r}")
            body = s
        for fmt in _TS_STRPTIME_FORMATS:
            try:
                dt = _dt.datetime.strptime(body, fmt)
                return dt.replace(tzinfo=_dt.timezone.utc).timestamp()
            except ValueError:
                continue
        raise ValueError(f"unparseable timestamp: {value!r}")

    raise ValueError(f"unsupported timestamp type {type(value)!r}: {value!r}")


@dataclass(frozen=True)
class TradeRow:
    """A single raw trade-print observation, exactly as read from Store.load_trades()
    (TRADES_COLS subset relevant here). No cleaning is performed by the loader --
    all missing/malformed/precision handling happens in the pure functions below,
    so tests can inject raw, dirty values directly."""

    token_id: Any
    outcome_index: Any
    price: Any
    traded_at: Any


@dataclass
class TokenPairResult:
    side_0_token: Optional[str]
    side_1_token: Optional[str]
    status: str  # "RESOLVED" | "TOKEN_PAIR_UNRESOLVED"
    reason_detail: Optional[str]
    malformed_row_count: int


def enumerate_token_pair(rows: List[TradeRow], condition_id: Optional[str] = None) -> TokenPairResult:
    """
    Locked enumeration basis (per SPEC_price_source_s1_coverage.md §3.1, reused
    unchanged): distinct (token_id, outcome_index) tuples from trades. Requires
    exactly two distinct, stable, string-safe side tokens -- one per
    outcome_index in {"0", "1"}. `resolved_winning_token_id` is never consulted
    here (it is not even passed in) -- outcome-conditioned pair sources are
    forbidden.

    `token_id` uses the STRICT `canonical_identifier` (78-digit precision-
    critical identifier: any bare float or scientific-notation string is
    precision loss). `outcome_index` uses the separate, more lenient
    `canonical_outcome_index` (a bounded {0,1} integer slot field: exact-float
    forms like 0.0/1.0/"0.0"/"1.0" are safe and accepted, never precision
    loss) -- see the v5 patch note on both functions above for why they must
    NOT share the strict rule.

    Missing token_id/outcome_index -> row skipped and counted (malformed),
    never a stop. A genuinely present-but-mangled token_id ->
    IdentifierPrecisionLoss propagates to the caller (whole-run hard stop,
    STOP_PRECISION_LOSS, with field/condition_id/raw-value diagnostics) --
    this function does not swallow it. An outcome_index that is present but
    does not normalize to "0"/"1" (non-integral, out-of-range, or unsupported
    type) is counted as malformed (row exclusion), consistent with existing
    schema policy -- never raises. `condition_id`, if supplied, is threaded
    into any STOP_PRECISION_LOSS diagnostic for the token_id it was found on.
    """
    malformed = 0
    candidates: Dict[str, set] = {"0": set(), "1": set()}
    saw_any_valid = False

    for row in rows:
        if _is_missing_field(row.token_id) or _is_missing_field(row.outcome_index):
            malformed += 1
            continue
        # canonical_identifier raises IdentifierPrecisionLoss for a genuine
        # mangled token_id; that must propagate (not be caught here).
        # canonical_outcome_index never raises -- an invalid slot value is
        # simply not "0"/"1" and falls through to the malformed-row count.
        tok = canonical_identifier(row.token_id, field_name="token_id", condition_id=condition_id)
        idx = canonical_outcome_index(row.outcome_index)
        if idx not in ("0", "1"):
            malformed += 1
            continue
        candidates[idx].add(tok)
        saw_any_valid = True

    if not saw_any_valid:
        return TokenPairResult(None, None, "TOKEN_PAIR_UNRESOLVED", "ALL_ROWS_MISSING_KEY", malformed)

    n0, n1 = len(candidates["0"]), len(candidates["1"])
    if n0 != 1 or n1 != 1:
        detail = f"side_0_candidates={n0},side_1_candidates={n1}"
        return TokenPairResult(None, None, "TOKEN_PAIR_UNRESOLVED", detail, malformed)

    side_0 = next(iter(candidates["0"]))
    side_1 = next(iter(candidates["1"]))
    if side_0 == side_1:
        return TokenPairResult(None, None, "TOKEN_PAIR_UNRESOLVED", "SIDE_0_EQUALS_SIDE_1", malformed)

    return TokenPairResult(side_0, side_1, "RESOLVED", None, malformed)


def valid_decision_window(
    first_trade_ts: Optional[float], resolved_at_ts: Optional[float], warmup_seconds: float
) -> bool:
    """valid <=> both anchors present AND resolved_at_ts > first_trade_ts + warmup.
    Strict inequality (leakage-safe), identical rule to the accepted S1 fix."""
    if first_trade_ts is None or resolved_at_ts is None:
        return False
    return resolved_at_ts > (first_trade_ts + warmup_seconds)


@dataclass
class SideObservation:
    ts: Optional[float]
    gap_seconds: Optional[float]
    print_count_total_valid: int
    invalid_price_row_count: int
    malformed_row_count: int


def first_print_in_window(
    rows_for_token: List[TradeRow], decision_lower_ts: float, resolved_at_ts: float
) -> SideObservation:
    """
    Side k's decision-time observation is the FIRST print of side k's own token
    with traded_at in [decision_lower_ts, resolved_at_ts) -- strict upper bound
    (leakage-safe: a print at/after resolved_at never counts). No complement-fill,
    no synthesis: this only ever looks at rows already filtered to side k's own
    token by the caller. Only the timestamp of the winning print and diagnostic
    counts are returned -- the price VALUE itself is never carried into the
    result (no price series is ever persisted).
    """
    best_ts: Optional[float] = None
    total_valid = 0
    invalid_price = 0
    malformed = 0

    for row in rows_for_token:
        if _is_missing_field(row.traded_at):
            malformed += 1
            continue
        try:
            ts = parse_ts(row.traded_at)
        except ValueError:
            malformed += 1
            continue
        price = valid_price(row.price)
        if price is None:
            invalid_price += 1
            continue
        total_valid += 1
        if decision_lower_ts <= ts < resolved_at_ts:
            if best_ts is None or ts < best_ts:
                best_ts = ts

    gap = (best_ts - decision_lower_ts) if best_ts is not None else None
    return SideObservation(
        ts=best_ts,
        gap_seconds=gap,
        print_count_total_valid=total_valid,
        invalid_price_row_count=invalid_price,
        malformed_row_count=malformed,
    )


def classify_level_b(obs0: SideObservation, obs1: SideObservation) -> str:
    has0 = obs0.ts is not None
    has1 = obs1.ts is not None
    if has0 and has1:
        return "DECISION_PRICE_BOTH_SIDES"
    if has0 or has1:
        return "DECISION_PRICE_ONE_SIDE"
    return "DECISION_PRICE_NEITHER"


def rows_for_side(rows: List[TradeRow], side_token: str, condition_id: Optional[str] = None) -> List[TradeRow]:
    """Per-token isolation: side k's rows are selected ONLY by matching token_id
    identity (never by `side`/label). Rows with a missing/mangled token_id were
    already excluded from pairing; here we simply re-filter the raw row set to
    this side's resolved token, tolerating (and skipping) any row whose
    token_id is missing (already counted upstream during pairing).
    `condition_id`, if supplied, is threaded into any (defensive, should be
    unreachable in practice) STOP_PRECISION_LOSS diagnostic."""
    out = []
    for row in rows:
        if _is_missing_field(row.token_id):
            continue
        try:
            tok = canonical_identifier(row.token_id, field_name="token_id", condition_id=condition_id)
        except IdentifierPrecisionLoss:
            # A row that survived pairing (using the SAME canonicalization) can
            # only reach here as string-safe; re-raising keeps the guarantee
            # explicit rather than silently dropping a mangled row post hoc.
            raise
        if tok == side_token:
            out.append(row)
    return out


# ---------------------------------------------------------------------------
# Sample reconstruction (Option A must reuse the exact accepted S1 Pass-1
# 300-condition sample; STOP_SAMPLE_IRREPRODUCIBLE if it cannot be, never an
# improvised replacement)
# ---------------------------------------------------------------------------


@dataclass
class SampleReconstructionResult:
    ok: bool
    sample: Dict[str, str] = field(default_factory=dict)  # condition_id -> subclass
    measured_count: int = 0
    excluded_count: int = 0  # invalid-window exclusions (from the accepted S1 split)
    measured_by_subclass: Dict[str, int] = field(default_factory=dict)
    # condition_ids the accepted S1 run classified as invalid-window
    # (NO_VALID_DECISION_WINDOW_AFTER_WARMUP). Carried so the orchestration can
    # keep them excluded/reported and NEVER let them become coverage negatives,
    # even if the local trades happen to admit a window this pass.
    invalid_window_ids: FrozenSet[str] = field(default_factory=frozenset)
    # condition_id -> the RAW (un-normalized) excluded-ledger reason string, for
    # audit/ledger-output purposes only. Decisions are made on the normalized
    # class (see _normalize_excluded_reason), never on this raw value.
    invalid_window_raw_reasons: Dict[str, str] = field(default_factory=dict)
    failure_reason: Optional[str] = None
    failure_detail: Optional[str] = None


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def _pick_status_column(header_row: Dict[str, str]) -> Optional[str]:
    for col in S1_BY_CONDITION_STATUS_COLUMNS:
        if col in header_row:
            return col
    return None


def reconstruct_s1_pass1_sample(
    by_condition_csv_path: Path, excluded_csv_path: Path
) -> SampleReconstructionResult:
    """
    Reconstruct the exact accepted S1 Pass-1 300-condition sample from the two
    accepted S1 artifacts, preserving the accepted valid-window / invalid-window
    split. Every pinned invariant is taken from the SETTLED
    DECISION_LOG / RESULT / invalid-decision-window findings. Any genuine
    deviation -> ok=False with a typed failure_reason; the caller halts with
    STOP_SAMPLE_IRREPRODUCIBLE and must NOT improvise a replacement sample.

    Accepted S1 two-ledger shape (see the module-level constants block):
      - the by-condition ledger carries the FULL sample (measured rows with a
        real Level-B class, PLUS invalid-window rows marked
        NO_VALID_DECISION_WINDOW_AFTER_WARMUP);
      - the excluded ledger carries the 52 invalid-window conditions;
      - so the same 52 ids appearing in BOTH files is EXPECTED and is NOT an
        irreproducibility failure.
    The sample is the UNION of condition_ids across both files; the
    valid/invalid split is read from each condition's status, not from raw file
    row counts. This tolerates either accepted-artifact variant (invalid rows
    present in the by-condition file, as in the real run, or only in the
    excluded file), and only the derived UNION and split must match the pins.
    """
    if not by_condition_csv_path.is_file():
        return SampleReconstructionResult(
            ok=False, failure_reason="missing_file", failure_detail=str(by_condition_csv_path)
        )
    if not excluded_csv_path.is_file():
        return SampleReconstructionResult(
            ok=False, failure_reason="missing_file", failure_detail=str(excluded_csv_path)
        )

    try:
        by_condition_rows = _read_csv_rows(by_condition_csv_path)
    except (OSError, csv.Error) as exc:
        return SampleReconstructionResult(ok=False, failure_reason="unreadable_file", failure_detail=str(exc))
    try:
        excluded_rows = _read_csv_rows(excluded_csv_path)
    except (OSError, csv.Error) as exc:
        return SampleReconstructionResult(ok=False, failure_reason="unreadable_file", failure_detail=str(exc))

    if not by_condition_rows or "condition_id" not in by_condition_rows[0] or "subclass" not in by_condition_rows[0]:
        return SampleReconstructionResult(
            ok=False, failure_reason="missing_columns", failure_detail="by_condition_csv needs condition_id,subclass"
        )
    if not excluded_rows or "condition_id" not in excluded_rows[0] or "reason" not in excluded_rows[0]:
        return SampleReconstructionResult(
            ok=False, failure_reason="missing_columns", failure_detail="excluded_csv needs condition_id,reason"
        )

    status_col = _pick_status_column(by_condition_rows[0])
    if status_col is None:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="missing_columns",
            failure_detail=f"by_condition_csv needs one of {S1_BY_CONDITION_STATUS_COLUMNS} to identify the valid/invalid split",
        )

    # Duplicate condition_ids WITHIN a single file are still a genuine defect --
    # each ledger should list a condition at most once.
    by_ids = [r["condition_id"] for r in by_condition_rows]
    if len(by_ids) != len(set(by_ids)):
        return SampleReconstructionResult(
            ok=False, failure_reason="duplicate_condition_id", failure_detail="in by_condition file"
        )
    excl_ids = [r["condition_id"] for r in excluded_rows]
    if len(excl_ids) != len(set(excl_ids)):
        return SampleReconstructionResult(
            ok=False, failure_reason="duplicate_condition_id", failure_detail="in excluded file"
        )

    # Every excluded row must be an invalid-window exclusion (that is the only
    # exclusion kind the accepted S1 split records into a sample that must
    # reconstruct to exactly 300 with a 248/52 valid/invalid split; any other
    # reason means these are not the accepted S1 Pass-1 artifacts). The raw
    # `reason` value may bundle diagnostic details after the class token (see
    # _normalize_excluded_reason) -- decisions are made on the normalized
    # class; the raw string is preserved for audit and echoed in any failure.
    invalid_window_raw_reasons: Dict[str, str] = {}
    for r in excluded_rows:
        raw_reason = r["reason"]
        normalized = _normalize_excluded_reason(raw_reason)
        if normalized != S1_PASS1_EXPECTED_EXCLUDED_REASON:
            return SampleReconstructionResult(
                ok=False,
                failure_reason="unexpected_excluded_reason",
                failure_detail=f"condition_id={r['condition_id']} reason={raw_reason!r} normalized={normalized!r}",
            )
        invalid_window_raw_reasons[r["condition_id"]] = raw_reason
    excluded_invalid_ids = set(excl_ids)

    # Classify each by-condition row's status. Recognize measured Level-B
    # classes and the invalid-window token; anything else is unrecognized and
    # makes the sample irreproducible (never silently assumed measured).
    by_condition_status: Dict[str, str] = {}
    by_condition_subclass: Dict[str, str] = {}
    unrecognized: List[str] = []
    for r in by_condition_rows:
        cid = r["condition_id"]
        raw = (r.get(status_col) or "").strip()
        by_condition_subclass[cid] = r["subclass"]
        if raw in S1_MEASURED_LEVEL_B_CLASSES:
            by_condition_status[cid] = "MEASURED"
        elif raw == S1_INVALID_WINDOW_STATUS:
            by_condition_status[cid] = "INVALID_WINDOW"
        else:
            unrecognized.append(f"{cid}:{raw!r}")
    if unrecognized:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="unrecognized_by_condition_status",
            failure_detail=f"{len(unrecognized)} rows, e.g. {unrecognized[:3]}",
        )

    # Cross-file consistency: any id the excluded file calls invalid-window that
    # ALSO appears in the by-condition file must be marked INVALID_WINDOW there
    # too. A conflict (excluded says invalid, by-condition says measured) is a
    # real, unreconcilable status conflict -> irreproducible.
    conflicts = [
        cid
        for cid in (excluded_invalid_ids & set(by_condition_status))
        if by_condition_status[cid] != "INVALID_WINDOW"
    ]
    if conflicts:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="status_conflict",
            failure_detail=f"{len(conflicts)} ids excluded as invalid-window but measured in by-condition, e.g. {conflicts[:3]}",
        )

    # Union of condition_ids across both files = the reconstructed sample.
    all_ids = set(by_condition_status) | excluded_invalid_ids

    # Determine the invalid-window set (union of: excluded-file ids, and any
    # by-condition rows explicitly marked invalid-window) and the measured set
    # (the remainder). An id present only in the by-condition file as MEASURED
    # is measured; an id present only in the excluded file is invalid-window.
    invalid_ids = set(excluded_invalid_ids)
    for cid, st in by_condition_status.items():
        if st == "INVALID_WINDOW":
            invalid_ids.add(cid)
    measured_ids = {cid for cid in all_ids if cid not in invalid_ids}

    # Pinned totals.
    total_unique = len(all_ids)
    if total_unique != S1_PASS1_EXPECTED_SAMPLE_SIZE:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="total_mismatch",
            failure_detail=(
                f"unique_sample={total_unique} expected={S1_PASS1_EXPECTED_SAMPLE_SIZE} "
                f"(measured={len(measured_ids)}, invalid_window={len(invalid_ids)})"
            ),
        )
    if len(invalid_ids) != S1_PASS1_EXPECTED_EXCLUDED_TOTAL:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="invalid_window_count_mismatch",
            failure_detail=f"got={len(invalid_ids)} expected={S1_PASS1_EXPECTED_EXCLUDED_TOTAL}",
        )
    if len(measured_ids) != S1_PASS1_EXPECTED_MEASURED_TOTAL:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="measured_count_mismatch",
            failure_detail=f"got={len(measured_ids)} expected={S1_PASS1_EXPECTED_MEASURED_TOTAL}",
        )

    # Every measured id must carry a subclass from the by-condition ledger (the
    # measured set is defined from by-condition rows, so this holds by
    # construction, but assert it rather than assume).
    missing_subclass = [cid for cid in measured_ids if cid not in by_condition_subclass]
    if missing_subclass:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="measured_missing_subclass",
            failure_detail=f"{len(missing_subclass)} measured ids absent from by-condition ledger, e.g. {missing_subclass[:3]}",
        )

    # Measured subclass breakdown is derived from MEASURED rows only (invalid
    # rows in the by-condition file must not inflate a subclass tally).
    measured_by_subclass: Dict[str, int] = {}
    for cid in measured_ids:
        sc = by_condition_subclass[cid]
        measured_by_subclass[sc] = measured_by_subclass.get(sc, 0) + 1
    if measured_by_subclass != S1_PASS1_EXPECTED_MEASURED_BY_SUBCLASS:
        return SampleReconstructionResult(
            ok=False,
            failure_reason="measured_subclass_breakdown_mismatch",
            failure_detail=f"got={measured_by_subclass} expected={S1_PASS1_EXPECTED_MEASURED_BY_SUBCLASS}",
        )

    # Build the sample map (condition_id -> subclass). Prefer the by-condition
    # subclass; fall back to the excluded file's subclass for any invalid id
    # present only there.
    excluded_subclass = {r["condition_id"]: (r.get("subclass") or "") for r in excluded_rows}
    sample: Dict[str, str] = {}
    for cid in all_ids:
        if cid in by_condition_subclass:
            sample[cid] = by_condition_subclass[cid]
        else:
            sample[cid] = excluded_subclass.get(cid, "")

    return SampleReconstructionResult(
        ok=True,
        sample=sample,
        measured_count=len(measured_ids),
        excluded_count=len(invalid_ids),
        measured_by_subclass=measured_by_subclass,
        invalid_window_ids=frozenset(invalid_ids),
        invalid_window_raw_reasons=invalid_window_raw_reasons,
    )


# ---------------------------------------------------------------------------
# Injected abstractions (so the orchestration is testable with fakes -- no
# pandas, no Store, no real filesystem needed in the pure-logic test suite)
# ---------------------------------------------------------------------------


@dataclass
class ContractVersionResult:
    """Structured result of loading the classification-contract version pin.
    ok=False means a SETUP/SCHEMA failure (missing/unreadable/malformed file, or
    missing `nb_contract_version` field) -> STOP_CONTRACT_SCHEMA. A present but
    WRONG version is ok=True with the observed version; the orchestration turns
    the mismatch into STOP_STALE_CONTRACT -- the two failure classes must stay
    distinguishable."""

    ok: bool
    version: Optional[str] = None
    failure_reason: Optional[str] = None
    failure_detail: Optional[str] = None


@dataclass
class ResolutionSourceResult:
    """Structured result of loading the resolution-source parquet. ok=False
    means a SETUP/SCHEMA failure (missing/unreadable/malformed file, missing
    required columns, empty table, or an entirely-null version column) ->
    STOP_RESOLUTION_SOURCE_SCHEMA. Row-level problems (a sampled condition
    absent from the table, or its `resolved_at` missing/unparseable) are NOT
    schema failures -- they stay per-condition
    NO_VALID_DECISION_WINDOW_AFTER_WARMUP exclusions downstream."""

    ok: bool
    version: Optional[str] = None
    resolved_at_by_cid: Dict[str, Any] = field(default_factory=dict)
    failure_reason: Optional[str] = None
    failure_detail: Optional[str] = None


class Loader(Protocol):
    def load_sample_manifest(self) -> SampleReconstructionResult: ...

    def load_p0_state(self) -> Optional[str]: ...

    def load_contract_version(self) -> ContractVersionResult: ...

    def load_resolution_source(self, condition_ids: FrozenSet[str]) -> ResolutionSourceResult: ...

    def load_trades_for_conditions(
        self, condition_ids: FrozenSet[str]
    ) -> Dict[str, List[TradeRow]]: ...

    def observed_trades_columns(self) -> List[str]: ...


class Writer(Protocol):
    def write_all(self, result: Dict[str, Any], by_condition_rows: List[List[Any]], excluded_rows: List[List[Any]], source_shape_text: str) -> None: ...


# ---------------------------------------------------------------------------
# Real (production) loader / writer -- ALL heavy imports (pandas, pm_research)
# are LAZY, imported only inside these methods, so importing this module (or
# running it unauthorized) never touches pandas/Store/the filesystem.
# ---------------------------------------------------------------------------


class StoreLoader:
    """Real, local-only loader. Every method that touches disk is only ever
    called from the authorized branch of the orchestration."""

    def __init__(
        self,
        root: str,
        p0_preflight_json: Path,
        classification_contract_json: Path,
        resolution_source_parquet: Path,
        s1_by_condition_csv: Path,
        s1_excluded_csv: Path,
    ) -> None:
        self.root = root
        self.p0_preflight_json = p0_preflight_json
        self.classification_contract_json = classification_contract_json
        self.resolution_source_parquet = resolution_source_parquet
        self.s1_by_condition_csv = s1_by_condition_csv
        self.s1_excluded_csv = s1_excluded_csv
        self._observed_columns: List[str] = []

    def load_sample_manifest(self) -> SampleReconstructionResult:
        return reconstruct_s1_pass1_sample(self.s1_by_condition_csv, self.s1_excluded_csv)

    def load_p0_state(self) -> Optional[str]:
        if not self.p0_preflight_json.is_file():
            return None
        with self.p0_preflight_json.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("p0_state")

    def load_contract_version(self) -> ContractVersionResult:
        if not self.classification_contract_json.is_file():
            return ContractVersionResult(
                ok=False,
                failure_reason="missing_file",
                failure_detail=str(self.classification_contract_json),
            )
        try:
            with self.classification_contract_json.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError) as exc:  # ValueError covers json.JSONDecodeError
            return ContractVersionResult(
                ok=False, failure_reason="unreadable_or_malformed", failure_detail=str(exc)
            )
        if not isinstance(data, dict):
            return ContractVersionResult(
                ok=False,
                failure_reason="malformed_top_level",
                failure_detail=f"expected dict, got {type(data).__name__}",
            )
        version = data.get("nb_contract_version")
        if version is None or (isinstance(version, str) and version.strip() == ""):
            return ContractVersionResult(
                ok=False,
                failure_reason="missing_version_field",
                failure_detail="nb_contract_version absent or empty",
            )
        # ok=True even if the version is WRONG -- staleness is the
        # orchestration's distinguishable STOP_STALE_CONTRACT, not a schema stop.
        return ContractVersionResult(ok=True, version=str(version))

    def load_resolution_source(self, condition_ids: FrozenSet[str]) -> ResolutionSourceResult:
        # File-existence check deliberately precedes the lazy pandas import so a
        # missing required artifact is reported identically on a box with or
        # without pandas installed.
        if not self.resolution_source_parquet.is_file():
            return ResolutionSourceResult(
                ok=False,
                failure_reason="missing_file",
                failure_detail=str(self.resolution_source_parquet),
            )

        # Lazy import: pandas/pyarrow only touched here, only when authorized.
        import pandas as pd  # noqa: WPS433 (intentional lazy import)

        try:
            df = pd.read_parquet(self.resolution_source_parquet)
        except Exception as exc:  # noqa: BLE001 - any parquet-engine failure is a schema stop
            return ResolutionSourceResult(
                ok=False, failure_reason="unreadable_or_malformed", failure_detail=str(exc)
            )

        missing_cols = [c for c in REQUIRED_RESOLUTION_SOURCE_COLUMNS if c not in df.columns]
        if missing_cols:
            return ResolutionSourceResult(
                ok=False,
                failure_reason="missing_columns",
                failure_detail=f"missing={missing_cols} present={list(df.columns)}",
            )

        if len(df) == 0:
            return ResolutionSourceResult(
                ok=False,
                failure_reason="empty_table",
                failure_detail="resolution-source parquet has zero rows",
            )

        # Version pin is computed from the FULL table (a required pinned input
        # must be version-checkable regardless of which conditions were sampled).
        version_values = [v for v in df["nb_contract_version"].unique().tolist() if not _is_missing_field(v)]
        if not version_values:
            return ResolutionSourceResult(
                ok=False,
                failure_reason="missing_version_values",
                failure_detail="nb_contract_version column has no non-null values",
            )
        version = (
            str(version_values[0])
            if len(version_values) == 1
            else "MIXED:" + ",".join(map(str, version_values))
        )

        df = df[df["status"] == "RESOLVED_SINGLE_WINNER"]
        df = df[df["condition_id"].isin(condition_ids)]
        # Row-level behavior preserved: a sampled condition absent here, or one
        # whose resolved_at is missing/unparseable, is handled downstream as a
        # per-condition NO_VALID_DECISION_WINDOW_AFTER_WARMUP exclusion, never a
        # schema stop.
        resolved_at_by_cid = dict(zip(df["condition_id"], df["resolved_at"]))
        return ResolutionSourceResult(ok=True, version=version, resolved_at_by_cid=resolved_at_by_cid)

    def load_trades_for_conditions(
        self, condition_ids: FrozenSet[str]
    ) -> Dict[str, List[TradeRow]]:
        # Lazy import: pandas/pm_research.Store only touched here.
        from pm_research.data.store import Store  # noqa: WPS433

        store = Store(self.root)
        df = store.load_trades()
        self._observed_columns = list(df.columns)
        df = df[df["condition_id"].isin(condition_ids)]

        out: Dict[str, List[TradeRow]] = {cid: [] for cid in condition_ids}
        for rec in df.to_dict("records"):
            cid = rec.get("condition_id")
            if cid not in out:
                continue
            out[cid].append(
                TradeRow(
                    token_id=rec.get("token_id"),
                    outcome_index=rec.get("outcome_index"),
                    price=rec.get("price"),
                    traded_at=rec.get("traded_at"),
                )
            )
        return out

    def observed_trades_columns(self) -> List[str]:
        return list(self._observed_columns)


class ArtifactWriter:
    """Real writer. Refuses any path containing a `prices/` segment (defense in
    depth: this candidate must never write into the local prices store), and
    writes only under artifacts/named_binary_probe/price_source_s1_alt/."""

    def __init__(self, artifacts_root: Path) -> None:
        self.artifacts_root = artifacts_root
        self.out_dir = artifacts_root / ARTIFACT_SUBDIR

    def _assert_safe_path(self, path: Path) -> None:
        parts = {p.lower() for p in path.parts}
        if "prices" in parts:
            raise RuntimeError(f"refusing to write under a prices/ path: {path}")

    def write_all(
        self,
        result: Dict[str, Any],
        by_condition_rows: List[List[Any]],
        excluded_rows: List[List[Any]],
        source_shape_text: str,
    ) -> None:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        json_path = self.out_dir / "price_source_s1_alt_coverage.json"
        md_path = self.out_dir / "price_source_s1_alt_coverage.md"
        by_cond_path = self.out_dir / "price_source_s1_alt_coverage_by_condition.csv"
        excluded_path = self.out_dir / "price_source_s1_alt_excluded.csv"
        shape_path = self.out_dir / "price_source_s1_alt_source_shape.md"

        for p in (json_path, md_path, by_cond_path, excluded_path, shape_path):
            self._assert_safe_path(p)

        with json_path.open("w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)

        with md_path.open("w", encoding="utf-8") as fh:
            fh.write(render_markdown_summary(result))

        _assert_no_forbidden_columns(BY_CONDITION_HEADER)
        with by_cond_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(BY_CONDITION_HEADER)
            for row in by_condition_rows:
                w.writerow(row)

        with excluded_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(EXCLUDED_HEADER)
            for row in excluded_rows:
                w.writerow(row)

        with shape_path.open("w", encoding="utf-8") as fh:
            fh.write(source_shape_text)


def _assert_no_forbidden_columns(header: List[str]) -> None:
    for col in header:
        low = col.lower()
        for bad in _FORBIDDEN_LEDGER_SUBSTRINGS:
            if bad in low and low not in ("status",):
                raise AssertionError(f"forbidden ledger column detected: {col!r} (contains {bad!r})")


def render_markdown_summary(result: Dict[str, Any]) -> str:
    lines = [
        "# S1-ALT Pass 1 — Option A Local Trade-Print Coverage",
        "",
        f"**Status:** `{result.get('status')}`",
        "",
        "Coverage-only. No price series persisted. No yes_price / 1-price / 1-yes_price "
        "synthesis. named_binary_probe_blocked observed, never flipped.",
        "",
        "## Sample reconstruction",
        f"- reconstructed: {result.get('sample_reconstruction', {}).get('reconstructed')}",
        f"- measured: {result.get('sample_reconstruction', {}).get('measured_file_count')}",
        f"- excluded: {result.get('sample_reconstruction', {}).get('excluded_file_count')}",
        "",
        "## Per-subclass Level-B coverage (binding; threshold 0.95)",
    ]
    for subclass, stats in (result.get("per_subclass_coverage") or {}).items():
        lines.append(
            f"- {subclass}: {stats.get('both_sides')}/{stats.get('measured')} "
            f"= {stats.get('rate')} (clears: {stats.get('clears_threshold')})"
        )
    lines.append("")
    lines.append(f"**Verdict:** `{result.get('verdict')}`")
    lines.append("")
    if result.get("all_one_status_detected"):
        lines.append(
            "**Note:** the Level-B aggregate was all-one-status; a Level-C spot check "
            "was run before this verdict was trusted (see `level_c_validation`)."
        )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


@dataclass
class RunConfig:
    execute: bool
    write_artifacts: bool
    warmup_seconds: float = DEFAULT_WARMUP_SECONDS
    quiet: bool = True
    progress_every: int = 25


def _progress(quiet: bool, msg: str) -> None:
    if not quiet:
        print(f"[S1-ALT] {msg}", file=sys.stderr, flush=True)


def _utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_reconciliation(
    sample_size: int,
    measured: int,
    token_pair_unresolved: int,
    no_trade_anchor: int,
    no_valid_decision_window: int,
    s1_invalid_window: int,
) -> Dict[str, Any]:
    """Every sampled condition lands in exactly one bucket; the buckets must sum
    to the reconstructed sample size. `s1_invalid_window` is the count of
    conditions pre-excluded because the accepted S1 run classified them
    invalid-window (kept excluded, never coverage negatives);
    `no_valid_decision_window` is the count this pass found invalid from local
    data among the remaining conditions. Both are reported separately for audit,
    and both fold into the reconciliation total."""
    total = (
        measured
        + token_pair_unresolved
        + no_trade_anchor
        + no_valid_decision_window
        + s1_invalid_window
    )
    return {
        "sample_size": sample_size,
        "measured": measured,
        "token_pair_unresolved": token_pair_unresolved,
        "no_trade_anchor": no_trade_anchor,
        "no_valid_decision_window": no_valid_decision_window,
        "s1_invalid_window": s1_invalid_window,
        "reconciled": total == sample_size,
    }


def run_pass1_alt_coverage(cfg: RunConfig, loader: Loader, writer: Optional[Writer]) -> Dict[str, Any]:
    base_result: Dict[str, Any] = {
        "task": "S1_ALT_PASS1_LOCAL_TRADE_PRINT_COVERAGE",
        "candidate": "OPTION_A_LOCAL_TRADE_PRINTS",
        "nb_contract_version_expected": NB_CONTRACT_VERSION_EXPECTED,
        "warmup_seconds": cfg.warmup_seconds,
        "threshold": LEVEL_B_THRESHOLD,
        "named_binary_probe_blocked_observed": True,
        "no_price_series_persisted": True,
        "wrote_artifacts": False,
        "artifact_dir": None,
        "created_at_utc": _utc_now_iso(),
    }

    if not cfg.execute:
        base_result["status"] = STOP_NOT_AUTHORIZED
        base_result["authorized"] = False
        return base_result

    base_result["authorized"] = True
    _progress(cfg.quiet, "loading P0/contract/sample-manifest...")

    p0_state = loader.load_p0_state()
    if p0_state != "P0_CLEAR":
        base_result["status"] = STOP_P0_NOT_CLEAR
        base_result["p0_state_observed"] = p0_state
        _progress(cfg.quiet, f"done: status={STOP_P0_NOT_CLEAR}")
        return base_result

    contract_result = loader.load_contract_version()
    if not contract_result.ok:
        base_result["status"] = STOP_CONTRACT_SCHEMA
        base_result["contract_schema_failure"] = {
            "failure_reason": contract_result.failure_reason,
            "failure_detail": contract_result.failure_detail,
        }
        _progress(cfg.quiet, f"done: status={STOP_CONTRACT_SCHEMA} ({contract_result.failure_reason})")
        return base_result
    if contract_result.version != NB_CONTRACT_VERSION_EXPECTED:
        base_result["status"] = STOP_STALE_CONTRACT
        base_result["nb_contract_version_observed"] = contract_result.version
        _progress(cfg.quiet, f"done: status={STOP_STALE_CONTRACT}")
        return base_result

    sample_result = loader.load_sample_manifest()
    base_result["sample_reconstruction"] = {
        "reconstructed": sample_result.ok,
        "measured_file_count": sample_result.measured_count,
        "excluded_file_count": sample_result.excluded_count,
        "measured_by_subclass": sample_result.measured_by_subclass,
        "failure_reason": sample_result.failure_reason,
        "failure_detail": sample_result.failure_detail,
    }
    if not sample_result.ok:
        base_result["status"] = STOP_SAMPLE_IRREPRODUCIBLE
        _progress(cfg.quiet, f"done: status={STOP_SAMPLE_IRREPRODUCIBLE} ({sample_result.failure_reason})")
        return base_result

    sample = sample_result.sample  # condition_id -> subclass
    condition_ids = frozenset(sample.keys())
    # Authoritative from the accepted S1 split: these conditions were classified
    # invalid-window by the accepted S1 run and MUST stay excluded/reported as
    # NO_VALID_DECISION_WINDOW_AFTER_WARMUP here -- never re-measured, never a
    # coverage negative, regardless of what the local trades admit this pass.
    s1_invalid_window_ids = sample_result.invalid_window_ids
    # Raw (un-normalized) accepted-S1 excluded-reason strings, preserved for
    # audit/ledger-output only -- never consulted for any decision (task
    # point 3). Falls back to a plain marker when no raw string is available
    # (e.g. an id classified invalid-window via the by-condition ledger alone).
    s1_invalid_window_raw_reasons = sample_result.invalid_window_raw_reasons
    _progress(cfg.quiet, f"sample reconstructed: {len(condition_ids)} conditions")

    resolution_result = loader.load_resolution_source(condition_ids)
    if not resolution_result.ok:
        base_result["status"] = STOP_RESOLUTION_SOURCE_SCHEMA
        base_result["resolution_source_schema_failure"] = {
            "failure_reason": resolution_result.failure_reason,
            "failure_detail": resolution_result.failure_detail,
        }
        _progress(
            cfg.quiet,
            f"done: status={STOP_RESOLUTION_SOURCE_SCHEMA} ({resolution_result.failure_reason})",
        )
        return base_result
    if resolution_result.version != NB_CONTRACT_VERSION_EXPECTED:
        base_result["status"] = STOP_STALE_CONTRACT
        base_result["nb_contract_version_resolution_source_observed"] = resolution_result.version
        _progress(cfg.quiet, f"done: status={STOP_STALE_CONTRACT}")
        return base_result
    resolved_at_by_cid = resolution_result.resolved_at_by_cid

    _progress(cfg.quiet, "loading local trades for sampled conditions...")
    trades_by_cid = loader.load_trades_for_conditions(condition_ids)

    excluded_rows: List[List[Any]] = []
    by_condition_rows: List[List[Any]] = []
    level_b_counts = {"DECISION_PRICE_BOTH_SIDES": 0, "DECISION_PRICE_ONE_SIDE": 0, "DECISION_PRICE_NEITHER": 0}
    per_subclass: Dict[str, Dict[str, int]] = {s: {"both_sides": 0, "measured": 0} for s in ORIENTED_SUBCLASSES}
    token_pair_unresolved_count = 0
    no_trade_anchor_count = 0
    no_valid_window_count = 0
    s1_invalid_window_count = 0
    measured_count = 0
    malformed_trade_rows_total = 0
    invalid_price_rows_total = 0

    try:
        n_done = 0
        for condition_id in sorted(condition_ids):
            subclass = sample[condition_id]

            # Authoritative S1 invalid-window pre-exclusion (task point 4/5):
            # keep the accepted split. These conditions are excluded/reported as
            # NO_VALID_DECISION_WINDOW_AFTER_WARMUP without consulting local
            # trades at all, so they can never become coverage negatives.
            if condition_id in s1_invalid_window_ids:
                s1_invalid_window_count += 1
                raw_detail = s1_invalid_window_raw_reasons.get(condition_id, "s1_accepted_invalid_window")
                excluded_rows.append(
                    [condition_id, subclass, "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", raw_detail]
                )
                by_condition_rows.append(
                    [condition_id, subclass, "", "", "NO_VALID_DECISION_WINDOW_AFTER_WARMUP",
                     "", "", "", "", "", "", "", "", "", ""]
                )
                n_done += 1
                continue

            rows = trades_by_cid.get(condition_id, [])

            if not rows:
                no_trade_anchor_count += 1
                excluded_rows.append([condition_id, subclass, "NO_TRADE_ANCHOR", ""])
                by_condition_rows.append(
                    [condition_id, subclass, "", "", "NO_TRADE_ANCHOR", "", "", "", "", "", "", "", "", "", ""]
                )
                n_done += 1
                continue

            valid_trade_ts = []
            for r in rows:
                if _is_missing_field(r.traded_at):
                    malformed_trade_rows_total += 1
                    continue
                try:
                    valid_trade_ts.append(parse_ts(r.traded_at))
                except ValueError:
                    malformed_trade_rows_total += 1
            first_trade_ts = min(valid_trade_ts) if valid_trade_ts else None

            if first_trade_ts is None:
                no_trade_anchor_count += 1
                excluded_rows.append([condition_id, subclass, "NO_TRADE_ANCHOR", ""])
                by_condition_rows.append(
                    [condition_id, subclass, "", "", "NO_TRADE_ANCHOR", "", "", "", "", "", "", "", "", "", ""]
                )
                n_done += 1
                continue

            pair_result = enumerate_token_pair(rows, condition_id=condition_id)  # may raise IdentifierPrecisionLoss
            malformed_trade_rows_total += pair_result.malformed_row_count

            if pair_result.status == "TOKEN_PAIR_UNRESOLVED":
                token_pair_unresolved_count += 1
                excluded_rows.append([condition_id, subclass, "TOKEN_PAIR_UNRESOLVED", pair_result.reason_detail or ""])
                by_condition_rows.append(
                    [condition_id, subclass, "", "", "TOKEN_PAIR_UNRESOLVED", "", first_trade_ts, "", "", "", "", "", "", "", ""]
                )
                n_done += 1
                continue

            resolved_at_raw = resolved_at_by_cid.get(condition_id)
            resolved_at_ts: Optional[float]
            try:
                resolved_at_ts = None if resolved_at_raw is None else parse_ts(resolved_at_raw)
            except ValueError:
                resolved_at_ts = None

            if not valid_decision_window(first_trade_ts, resolved_at_ts, cfg.warmup_seconds):
                no_valid_window_count += 1
                excluded_rows.append(
                    [
                        condition_id,
                        subclass,
                        "NO_VALID_DECISION_WINDOW_AFTER_WARMUP",
                        f"first_trade_ts={first_trade_ts},resolved_at_ts={resolved_at_ts}",
                    ]
                )
                by_condition_rows.append(
                    [
                        condition_id, subclass, pair_result.side_0_token, pair_result.side_1_token,
                        "NO_VALID_DECISION_WINDOW_AFTER_WARMUP", "", first_trade_ts, first_trade_ts + cfg.warmup_seconds,
                        resolved_at_ts, "", "", "", "", "", "",
                    ]
                )
                n_done += 1
                continue

            decision_lower_ts = first_trade_ts + cfg.warmup_seconds
            rows_0 = rows_for_side(rows, pair_result.side_0_token, condition_id=condition_id)
            rows_1 = rows_for_side(rows, pair_result.side_1_token, condition_id=condition_id)
            obs0 = first_print_in_window(rows_0, decision_lower_ts, resolved_at_ts)
            obs1 = first_print_in_window(rows_1, decision_lower_ts, resolved_at_ts)
            invalid_price_rows_total += obs0.invalid_price_row_count + obs1.invalid_price_row_count
            malformed_trade_rows_total += obs0.malformed_row_count + obs1.malformed_row_count

            level_b_class = classify_level_b(obs0, obs1)
            level_b_counts[level_b_class] += 1
            measured_count += 1
            per_subclass.setdefault(subclass, {"both_sides": 0, "measured": 0})
            per_subclass[subclass]["measured"] += 1
            if level_b_class == "DECISION_PRICE_BOTH_SIDES":
                per_subclass[subclass]["both_sides"] += 1

            by_condition_rows.append(
                [
                    condition_id, subclass, pair_result.side_0_token, pair_result.side_1_token,
                    "MEASURED", level_b_class, first_trade_ts, decision_lower_ts, resolved_at_ts,
                    obs0.ts, obs0.gap_seconds, obs0.print_count_total_valid,
                    obs1.ts, obs1.gap_seconds, obs1.print_count_total_valid,
                ]
            )

            n_done += 1
            if n_done % cfg.progress_every == 0:
                _progress(cfg.quiet, f"processed {n_done}/{len(condition_ids)} conditions")

    except IdentifierPrecisionLoss as exc:
        base_result["status"] = STOP_PRECISION_LOSS
        base_result["precision_loss_detail"] = str(exc)
        _progress(cfg.quiet, f"done: status={STOP_PRECISION_LOSS}")
        return base_result

    # Token-enumeration reliability guard
    unresolved_fraction = token_pair_unresolved_count / len(condition_ids) if condition_ids else 0.0
    if unresolved_fraction > TOKEN_ENUMERATION_UNRELIABLE_FRACTION:
        base_result["status"] = STOP_TOKEN_ENUMERATION_UNRELIABLE
        base_result["token_pair_unresolved_count"] = token_pair_unresolved_count
        base_result["token_pair_unresolved_fraction"] = unresolved_fraction
        _progress(cfg.quiet, f"done: status={STOP_TOKEN_ENUMERATION_UNRELIABLE}")
        return base_result

    # All-invalid-window guard (mirrors S1's inconclusive verdict)
    if measured_count == 0:
        base_result["status"] = VERDICT_INCONCLUSIVE_NO_VALID_WINDOW
        base_result["verdict"] = VERDICT_INCONCLUSIVE_NO_VALID_WINDOW
        base_result["universe_reconciliation"] = _build_reconciliation(
            len(condition_ids), measured_count, token_pair_unresolved_count,
            no_trade_anchor_count, no_valid_window_count, s1_invalid_window_count,
        )
        base_result["malformed_trade_rows_total"] = malformed_trade_rows_total
        base_result["invalid_price_rows_total"] = invalid_price_rows_total
        _progress(cfg.quiet, f"done: status={VERDICT_INCONCLUSIVE_NO_VALID_WINDOW}")
        if cfg.write_artifacts and writer is not None:
            base_result["wrote_artifacts"] = True
            writer.write_all(base_result, by_condition_rows, excluded_rows, _render_source_shape(loader))
        return base_result

    # All-one-status guard: never trust a uniform Level-B aggregate on faith.
    non_zero_classes = [k for k, v in level_b_counts.items() if v > 0]
    all_one_status = len(non_zero_classes) == 1
    level_c = _level_c_spot_check(by_condition_rows)

    per_subclass_coverage: Dict[str, Any] = {}
    all_clear = True
    any_clear = False
    for subclass in ORIENTED_SUBCLASSES:
        stats = per_subclass.get(subclass, {"both_sides": 0, "measured": 0})
        m = stats["measured"]
        b = stats["both_sides"]
        rate = (b / m) if m > 0 else None
        clears = (rate is not None) and (rate >= LEVEL_B_THRESHOLD)
        per_subclass_coverage[subclass] = {
            "both_sides": b,
            "measured": m,
            "rate": rate,
            "clears_threshold": clears,
        }
        if not clears:
            all_clear = False
        if clears:
            any_clear = True

    if all_clear:
        verdict = VERDICT_VIABLE
    elif any_clear:
        verdict = VERDICT_PARTIAL
    else:
        verdict = VERDICT_NOT_VIABLE

    base_result["status"] = verdict
    base_result["verdict"] = verdict
    base_result["level_b_class_counts"] = level_b_counts
    base_result["per_subclass_coverage"] = per_subclass_coverage
    base_result["all_one_status_detected"] = all_one_status
    base_result["level_c_validation"] = level_c
    base_result["universe_reconciliation"] = _build_reconciliation(
        len(condition_ids), measured_count, token_pair_unresolved_count,
        no_trade_anchor_count, no_valid_window_count, s1_invalid_window_count,
    )
    base_result["malformed_trade_rows_total"] = malformed_trade_rows_total
    base_result["invalid_price_rows_total"] = invalid_price_rows_total

    _progress(cfg.quiet, f"done: verdict={verdict}")

    if cfg.write_artifacts and writer is not None:
        base_result["wrote_artifacts"] = True
        writer.write_all(base_result, by_condition_rows, excluded_rows, _render_source_shape(loader))

    return base_result


def _level_c_spot_check(by_condition_rows: List[List[Any]]) -> Dict[str, Any]:
    """
    A small, deterministic integrity spot-check over measured rows: gaps must be
    non-negative, decision_lower_ts <= resolved_at_ts, and side tokens (when
    present) must be distinct. This does not touch price values (none are
    carried in by_condition_rows) -- it only checks the structural/timestamp
    invariants already computed. A failure here is a code-correctness signal,
    not a coverage finding.
    """
    checked = 0
    failures: List[str] = []
    for row in by_condition_rows:
        (
            condition_id, subclass, side_0, side_1, status, level_b_class,
            first_trade_ts, decision_lower_ts, resolved_at_ts,
            obs0_ts, obs0_gap, obs0_cnt, obs1_ts, obs1_gap, obs1_cnt,
        ) = row
        if status != "MEASURED":
            continue
        checked += 1
        if side_0 == side_1:
            failures.append(f"{condition_id}: side_0 == side_1")
        if isinstance(decision_lower_ts, (int, float)) and isinstance(resolved_at_ts, (int, float)):
            if decision_lower_ts > resolved_at_ts:
                failures.append(f"{condition_id}: decision_lower_ts > resolved_at_ts")
        if isinstance(obs0_gap, (int, float)) and obs0_gap < 0:
            failures.append(f"{condition_id}: side_0 gap negative")
        if isinstance(obs1_gap, (int, float)) and obs1_gap < 0:
            failures.append(f"{condition_id}: side_1 gap negative")
    return {"checked": checked, "failures": failures, "passed": len(failures) == 0}


def _render_source_shape(loader: Loader) -> str:
    cols = []
    try:
        cols = loader.observed_trades_columns()
    except Exception:  # pragma: no cover - defensive only
        cols = []
    lines = [
        "# S1-ALT Pass 1 — observed local trades source shape",
        "",
        "No price values recorded below -- structural/column facts only.",
        "",
        f"Observed `Store.load_trades()` columns: {cols!r}" if cols else "Observed columns: (not captured)",
        "",
        "Expected per DATA_CONTRACTS_named_binary_probe.md §5 "
        "(TRADES_COLS = trade_id, wallet, condition_id, outcome, side, price, "
        "size_usdc, traded_at, tx_hash, token_id, outcome_index).",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="S1-ALT Pass 1 (Option A: local trade-print) coverage-only tool. "
        "Safe by default -- see module docstring."
    )
    p.add_argument("--root", type=str, default=None, help="Local data root passed to Store(root).")
    p.add_argument("--artifacts-dir", type=str, default="artifacts", help="Artifacts root directory.")
    p.add_argument(
        "--p0-preflight-json",
        type=str,
        default="artifacts/named_binary_probe/p0_preflight.json",
    )
    p.add_argument(
        "--classification-contract-json",
        type=str,
        default="artifacts/named_binary/named_binary_classification_contract.json",
    )
    p.add_argument(
        "--resolution-source-parquet",
        type=str,
        default="artifacts/named_binary/named_binary_resolution_source_rows.parquet",
    )
    p.add_argument(
        "--s1-by-condition-csv",
        type=str,
        default="artifacts/named_binary_probe/price_source_s1/price_source_s1_coverage_by_condition.csv",
    )
    p.add_argument(
        "--s1-excluded-csv",
        type=str,
        default="artifacts/named_binary_probe/price_source_s1/price_source_s1_excluded.csv",
    )
    p.add_argument("--warmup-seconds", type=float, default=DEFAULT_WARMUP_SECONDS)
    p.add_argument(
        "--i-authorize-s1-alt-pass1-local-run",
        action="store_true",
        help="Required to read any real local data (Store.load_trades, resolution "
        "parquet, S1 reproduction CSVs, P0/contract JSON). Without this flag, the "
        "script does nothing and prints STOP_NOT_AUTHORIZED.",
    )
    p.add_argument(
        "--write-artifacts",
        action="store_true",
        help="Required (in addition to the run authorization flag) to persist any "
        "output file. Without it, an authorized run still computes the full "
        "result and prints it, but writes nothing to disk.",
    )
    p.add_argument("--quiet", action="store_true", help="Suppress the stderr progress heartbeat.")
    p.add_argument("--progress-every", type=int, default=25)
    return p


def build_run_config(args: argparse.Namespace) -> RunConfig:
    return RunConfig(
        execute=bool(args.i_authorize_s1_alt_pass1_local_run),
        write_artifacts=bool(args.write_artifacts),
        warmup_seconds=args.warmup_seconds,
        quiet=bool(args.quiet),
        progress_every=args.progress_every,
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    cfg = build_run_config(args)

    if not cfg.execute:
        print(
            json.dumps(
                {
                    "status": STOP_NOT_AUTHORIZED,
                    "message": "Not authorized. Pass --i-authorize-s1-alt-pass1-local-run "
                    "to read local data, and --write-artifacts to also persist output "
                    "files. No data was read; nothing was written.",
                },
                indent=2,
            )
        )
        return 2

    if not args.root:
        print(
            json.dumps(
                {"status": "STOP_MISSING_ROOT", "message": "--root is required when authorized."}, indent=2
            )
        )
        return 2

    loader = StoreLoader(
        root=args.root,
        p0_preflight_json=Path(args.p0_preflight_json),
        classification_contract_json=Path(args.classification_contract_json),
        resolution_source_parquet=Path(args.resolution_source_parquet),
        s1_by_condition_csv=Path(args.s1_by_condition_csv),
        s1_excluded_csv=Path(args.s1_excluded_csv),
    )
    writer = ArtifactWriter(Path(args.artifacts_dir)) if cfg.write_artifacts else None

    result = run_pass1_alt_coverage(cfg, loader, writer)
    print(json.dumps(result, indent=2, sort_keys=True, default=str))

    status = result.get("status")
    if status in (
        VERDICT_VIABLE,
        VERDICT_PARTIAL,
        VERDICT_NOT_VIABLE,
        VERDICT_INCONCLUSIVE_NO_VALID_WINDOW,
    ):
        return 0
    if status == STOP_NOT_AUTHORIZED:
        return 2
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
