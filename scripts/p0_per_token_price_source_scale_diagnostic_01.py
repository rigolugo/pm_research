#!/usr/bin/env python3
"""P0_PER_TOKEN_PRICE_SOURCE_SCALE_DIAGNOSTIC_01 — DIAGNOSTIC_ONLY_NON_AUTHORIZING.

Diagnostic question
-------------------
Does the already-reviewed revised S1 per-token/per-side CLOB `/prices-history`
method still work when scaled from the reviewed 248-condition stratified sample
to the current wallet-derived P0 eligible universe (`39,693` conditions)?

This file measures that question. It establishes nothing else.

What this file is NOT
---------------------
* NOT S2 artifact construction. It writes no price artifact, no price store,
  no P1 input, no canonical file, and no gate change.
* NOT P1/P2/P3, scoring, PnL, probe execution, wallet copying, paper trading,
  or live trading.
* NOT full-universe *validation*. A completed run is diagnostic evidence only;
  Sentinel decides what, if anything, it establishes.
* NOT a Git writer. It never commits, pushes, branches, tags, or updates refs.

Preserved accepted method (PROJECT_STATE §"S1 — CLOB /prices-history" and
`S1_PRICE_SOURCE_REVALIDATION_EVIDENCE_MANIFEST_CANDIDATE_02.json /revised_method`)
--------------------------------------------------------------------------------
* one independently queried token id per side; `outcome_index` 0 and 1 stay separate;
* `startTs = decision_lower_ts - 1`;
* `endTs   = resolved_at_ts`;
* `fidelity = 1`;
* `interval` OMITTED;
* retry count `0`;
* evaluation window is the unchanged half-open
  `decision_lower_ts <= t < resolved_at_ts`;
* `decision_lower_ts = first_trade_ts + 3600` (WARMUP_SECONDS), where
  `first_trade_ts = min(traded_at)` per condition
  (DATA_CONTRACTS §5; `scripts/price_source_s1_coverage.py`);
* side synthesis is FORBIDDEN and not used: no `yes_price`, no `1 - price`,
  no `1 - yes_price`, no `1 - p`, no complement synthesis;
* `resolved_winning_token_id` is NEVER a token-pair source.

Semantic anti-drift rule
------------------------
Timestamp parsing, precision-safe integer canonicalization, and endpoint
response -> Level-A status mapping are IMPORTED from the accepted module
`scripts/price_source_s1_coverage.py`. They are never re-implemented here. If
that module cannot be imported, this script STOPS
(`STOP_CANONICAL_HELPERS_UNAVAILABLE`) rather than using a private copy that
could drift from the accepted semantics.

Network
-------
No request is issued unless `--execute-network` is passed explicitly. Default
behaviour is `--dry-run`-equivalent: build the manifest and summaries, touch no
network. Only the CLOB `/prices-history` endpoint is contacted. No Dune, no
Apify, no Polygonscan, no RPC, no market-metadata endpoint, no vendor or web
discovery.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Identity / pinned constants (consumed, never redefined)
# ---------------------------------------------------------------------------
DIAGNOSTIC_ID = "P0_PER_TOKEN_PRICE_SOURCE_SCALE_DIAGNOSTIC_01"
NON_AUTHORIZING = "DIAGNOSTIC_ONLY_NON_AUTHORIZING"
NON_AUTHORIZING_STATEMENT = (
    "DIAGNOSTIC_ONLY_NON_AUTHORIZING: this run is bounded research data acquisition. "
    "It is not S2 artifact construction, not price-artifact acceptance, not full-universe "
    "validation, not P1/P2/P3, not scoring, not probe execution, not a gate change, and it "
    "authorizes no further stage. Sentinel decides what the output establishes."
)

NB_CONTRACT_VERSION = "nb-contract-2026-06-28.1"
WARMUP_SECONDS = 3600  # decision_lower_ts = first_trade_ts + WARMUP_SECONDS
ORIENTED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
EXPECTED_FINAL_P0_ELIGIBLE = 39693

DEFAULT_ENDPOINT_BASE = "https://clob.polymarket.com"
PRICES_HISTORY_PATH = "/prices-history"
REQUEST_FIDELITY = 1
REQUEST_INTERVAL_POLICY = "OMITTED"
RETRY_COUNT = 0  # accepted revised method: zero retries

FORBIDDEN_SHORTCUTS_NOT_USED = [
    "yes_price",
    "1 - price",
    "1 - yes_price",
    "1 - p",
    "COMPLEMENT_SYNTHESIS",
    "WINNING_TOKEN_ENUMERATION",
]

# ---------------------------------------------------------------------------
# Condition-level disposition labels
# ---------------------------------------------------------------------------
TOKEN_PAIR_CLEAR = "TOKEN_PAIR_CLEAR"
TOKEN_PAIR_MISSING_SIDE_0 = "TOKEN_PAIR_MISSING_SIDE_0"
TOKEN_PAIR_MISSING_SIDE_1 = "TOKEN_PAIR_MISSING_SIDE_1"
TOKEN_PAIR_AMBIGUOUS_SIDE_0 = "TOKEN_PAIR_AMBIGUOUS_SIDE_0"
TOKEN_PAIR_AMBIGUOUS_SIDE_1 = "TOKEN_PAIR_AMBIGUOUS_SIDE_1"
MISSING_FIRST_TRADE_TS = "MISSING_FIRST_TRADE_TS"
MISSING_RESOLVED_AT = "MISSING_RESOLVED_AT"
MALFORMED_FIRST_TRADE_TS = "MALFORMED_FIRST_TRADE_TS"
MALFORMED_RESOLVED_AT = "MALFORMED_RESOLVED_AT"
INVALID_DECISION_WINDOW = "INVALID_DECISION_WINDOW"
REQUEST_ELIGIBLE = "REQUEST_ELIGIBLE"

# Two additional explicit labels. The required label set above cannot express
# these two observed states, and collapsing them into a required label would be
# a silent reinterpretation. They are reported separately and never merged.
TOKEN_PAIR_IDENTICAL_SIDES = "TOKEN_PAIR_IDENTICAL_SIDES"
TOKEN_PAIR_OUTCOME_INDEX_INVALID = "TOKEN_PAIR_OUTCOME_INDEX_INVALID"

DISPOSITION_LABELS = (
    TOKEN_PAIR_CLEAR,
    TOKEN_PAIR_MISSING_SIDE_0,
    TOKEN_PAIR_MISSING_SIDE_1,
    TOKEN_PAIR_AMBIGUOUS_SIDE_0,
    TOKEN_PAIR_AMBIGUOUS_SIDE_1,
    TOKEN_PAIR_IDENTICAL_SIDES,
    TOKEN_PAIR_OUTCOME_INDEX_INVALID,
    MISSING_FIRST_TRADE_TS,
    MISSING_RESOLVED_AT,
    MALFORMED_FIRST_TRADE_TS,
    MALFORMED_RESOLVED_AT,
    INVALID_DECISION_WINDOW,
    REQUEST_ELIGIBLE,
)

# Condition-level coverage labels (accepted Level-B vocabulary, unchanged).
DECISION_PRICE_BOTH_SIDES = "DECISION_PRICE_BOTH_SIDES"
DECISION_PRICE_ONE_SIDE = "DECISION_PRICE_ONE_SIDE"
DECISION_PRICE_NEITHER = "DECISION_PRICE_NEITHER"
CONDITION_NOT_EXECUTED = "CONDITION_NOT_EXECUTED"
CONDITION_INCOMPLETE_BOUNDED_RUN = "CONDITION_INCOMPLETE_BOUNDED_RUN"
# A side that errored / returned an unrecognized shape was NOT measured. Counting it
# as DECISION_PRICE_NEITHER would repeat the exact defect the accepted S1 work called
# out: an unqueryable condition must never be reported as a real negative.
CONDITION_SIDE_NOT_MEASURABLE = "CONDITION_SIDE_NOT_MEASURABLE"

# Transport statuses (this script's own transport vocabulary).
TRANSPORT_OK = "TRANSPORT_OK"
TRANSPORT_HTTP_ERROR = "TRANSPORT_HTTP_ERROR"
TRANSPORT_TIMEOUT = "TRANSPORT_TIMEOUT"
TRANSPORT_CONNECTION_ERROR = "TRANSPORT_CONNECTION_ERROR"
TRANSPORT_JSON_UNPARSEABLE = "TRANSPORT_JSON_UNPARSEABLE"

# In-window dispositions.
IN_WINDOW_PRESENT = "IN_WINDOW_PRESENT"
IN_WINDOW_EMPTY = "IN_WINDOW_EMPTY"
IN_WINDOW_NOT_EVALUABLE = "IN_WINDOW_NOT_EVALUABLE"

# Typed stops (halt the run; nothing is silently degraded).
STOP_CANONICAL_HELPERS_UNAVAILABLE = "STOP_CANONICAL_HELPERS_UNAVAILABLE"
STOP_P0_NOT_CLEAR = "STOP_P0_NOT_CLEAR"
STOP_STALE_CONTRACT = "STOP_STALE_CONTRACT"
STOP_TRADES_STORE_UNAVAILABLE = "STOP_TRADES_STORE_UNAVAILABLE"
STOP_RESOLUTION_SCHEMA = "STOP_RESOLUTION_SCHEMA"
STOP_PRECISION_LOSS = "STOP_PRECISION_LOSS"
STOP_OUTPUT_ROOT_FORBIDDEN = "STOP_OUTPUT_ROOT_FORBIDDEN"
STOP_ENDPOINT_HOST_FORBIDDEN = "STOP_ENDPOINT_HOST_FORBIDDEN"
STOP_INPUT_MISSING = "STOP_INPUT_MISSING"
STOP_RESULTS_EXIST = "STOP_RESULTS_EXIST"

# Level-A statuses are imported from the accepted module (see _Canonical).


class DiagnosticHalt(RuntimeError):
    """Typed halt. Carries a stop label; never downgraded to a soft status."""

    def __init__(self, label: str, detail: str = "") -> None:
        super().__init__(f"{label}: {detail}" if detail else label)
        self.label = label
        self.detail = detail


# ---------------------------------------------------------------------------
# Canonical helper import (anti-drift; no private re-implementation)
# ---------------------------------------------------------------------------
class _Canonical:
    """Handle onto the accepted S1 helper semantics."""

    module_path: str = ""
    parse_ts = None
    canonical_int = None
    is_string_safe_token = None
    map_response_to_status = None
    EndpointShapeError = None
    DataExportPrecisionLoss = None
    SERIES_PRESENT = "SERIES_PRESENT"
    SERIES_EMPTY = "SERIES_EMPTY"
    SERIES_ERROR_TRANSIENT = "SERIES_ERROR_TRANSIENT"
    SERIES_ERROR_NOTFOUND = "SERIES_ERROR_NOTFOUND"
    SERIES_MALFORMED = "SERIES_MALFORMED"
    STOP_ENDPOINT_SHAPE_UNRECOGNIZED = "STOP_ENDPOINT_SHAPE_UNRECOGNIZED"
    WARMUP_SECONDS = WARMUP_SECONDS


CANON = _Canonical()


def load_canonical_helpers(repo_root: str) -> None:
    """Import the accepted helper semantics from scripts/price_source_s1_coverage.py.

    Hard stop if unavailable. A local copy of parse_ts / canonical_int /
    map_response_to_status would be a drift surface, and drift in those three is
    exactly what produced earlier S1 defects (parse_ts millisecond/UTC patch,
    NaN handling, request-window fix).
    """
    module_path = os.path.join(repo_root, "scripts", "price_source_s1_coverage.py")
    if not os.path.isfile(module_path):
        raise DiagnosticHalt(
            STOP_CANONICAL_HELPERS_UNAVAILABLE,
            f"expected accepted helper module at {module_path}",
        )
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "pm_research_s1_coverage_helpers", module_path
    )
    if spec is None or spec.loader is None:
        raise DiagnosticHalt(STOP_CANONICAL_HELPERS_UNAVAILABLE, module_path)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec_module so module-level dataclass decorators in the
    # accepted helper can resolve sys.modules[cls.__module__].
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)  # module top level is constants + defs only
    except Exception as exc:  # noqa: BLE001
        sys.modules.pop(spec.name, None)
        raise DiagnosticHalt(STOP_CANONICAL_HELPERS_UNAVAILABLE, repr(exc)) from exc

    required = (
        "parse_ts",
        "canonical_int",
        "is_string_safe_token",
        "map_response_to_status",
        "EndpointShapeError",
        "DataExportPrecisionLoss",
        "SERIES_PRESENT",
        "SERIES_EMPTY",
        "SERIES_ERROR_TRANSIENT",
        "SERIES_ERROR_NOTFOUND",
        "SERIES_MALFORMED",
        "STOP_ENDPOINT_SHAPE_UNRECOGNIZED",
        "WARMUP_SECONDS",
        "NB_CONTRACT_VERSION",
        "EXPECTED_FINAL_P0_ELIGIBLE",
    )
    missing = [name for name in required if not hasattr(mod, name)]
    if missing:
        raise DiagnosticHalt(
            STOP_CANONICAL_HELPERS_UNAVAILABLE, f"missing symbols: {missing}"
        )

    # Pinned-constant equality: refuse to run against a drifted contract/warmup.
    if getattr(mod, "NB_CONTRACT_VERSION") != NB_CONTRACT_VERSION:
        raise DiagnosticHalt(
            STOP_STALE_CONTRACT,
            f"module NB_CONTRACT_VERSION={getattr(mod, 'NB_CONTRACT_VERSION')!r}",
        )
    if int(getattr(mod, "WARMUP_SECONDS")) != WARMUP_SECONDS:
        raise DiagnosticHalt(
            STOP_STALE_CONTRACT,
            f"module WARMUP_SECONDS={getattr(mod, 'WARMUP_SECONDS')!r}",
        )
    if int(getattr(mod, "EXPECTED_FINAL_P0_ELIGIBLE")) != EXPECTED_FINAL_P0_ELIGIBLE:
        raise DiagnosticHalt(
            STOP_STALE_CONTRACT,
            f"module EXPECTED_FINAL_P0_ELIGIBLE={getattr(mod, 'EXPECTED_FINAL_P0_ELIGIBLE')!r}",
        )

    for name in required:
        setattr(CANON, name, getattr(mod, name))
    CANON.module_path = module_path


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------
def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _resolve(path: str) -> str:
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))


def _is_within(child: str, parent: str) -> bool:
    child_r, parent_r = _resolve(child), _resolve(parent)
    return child_r == parent_r or child_r.startswith(parent_r + os.sep)


# ---------------------------------------------------------------------------
# Local input loading (read-only)
# ---------------------------------------------------------------------------
def load_p0_preflight(artifacts_root: str) -> Tuple[Dict[str, Any], int]:
    path = os.path.join(artifacts_root, "named_binary_probe", "p0_preflight.json")
    if not os.path.isfile(path):
        raise DiagnosticHalt(STOP_INPUT_MISSING, path)
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    if doc.get("p0_state") != "P0_CLEAR":
        raise DiagnosticHalt(STOP_P0_NOT_CLEAR, f"p0_state={doc.get('p0_state')!r}")
    expected_v = doc.get("nb_contract_version_expected", NB_CONTRACT_VERSION)
    if expected_v != NB_CONTRACT_VERSION:
        raise DiagnosticHalt(STOP_STALE_CONTRACT, f"expected={expected_v!r}")
    for key in ("nb_contract_version_contract", "nb_contract_version_resolution_source"):
        if doc.get(key) != NB_CONTRACT_VERSION:
            raise DiagnosticHalt(STOP_STALE_CONTRACT, f"{key}={doc.get(key)!r}")
    counts = doc.get("counts_pooled", {}) or {}
    final_eligible = int(counts.get("final_p0_eligible", EXPECTED_FINAL_P0_ELIGIBLE))
    return doc, final_eligible


def load_contract_conditions(artifacts_root: str) -> Dict[str, str]:
    """condition_id -> nb_subclass, for eligible oriented conditions only.

    The classification contract is authoritative for classification and eligibility.
    """
    path = os.path.join(
        artifacts_root, "named_binary", "named_binary_classification_contract.json"
    )
    if not os.path.isfile(path):
        raise DiagnosticHalt(STOP_INPUT_MISSING, path)
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    if doc.get("nb_contract_version") != NB_CONTRACT_VERSION:
        raise DiagnosticHalt(
            STOP_STALE_CONTRACT, f"contract doc version={doc.get('nb_contract_version')!r}"
        )
    out: Dict[str, str] = {}
    for rec in doc.get("conditions", []) or []:
        if rec.get("nb_contract_version") != NB_CONTRACT_VERSION:
            raise DiagnosticHalt(
                STOP_STALE_CONTRACT, f"row version={rec.get('nb_contract_version')!r}"
            )
        raw_eligible = rec.get("nb_eligible")
        if isinstance(raw_eligible, bool):
            eligible = raw_eligible
        else:
            s = str(raw_eligible).strip()
            if s == "True":
                eligible = True
            elif s == "False":
                eligible = False
            else:
                raise DiagnosticHalt(
                    STOP_STALE_CONTRACT, f"unexpected nb_eligible={raw_eligible!r}"
                )
        if not eligible:
            continue
        sub = rec.get("nb_subclass")
        if sub not in ORIENTED_SUBCLASSES:  # excludes YES_NO / UNUSABLE
            continue
        out[str(rec["condition_id"])] = str(sub)
    return out


def load_resolution_rows(artifacts_root: str) -> List[Dict[str, Any]]:
    """RESOLVED_SINGLE_WINNER rows; `resolved_at` kept raw (never blanket-stringified)."""
    path = os.path.join(
        artifacts_root, "named_binary", "named_binary_resolution_source_rows.parquet"
    )
    if not os.path.isfile(path):
        raise DiagnosticHalt(STOP_INPUT_MISSING, path)
    import pandas as pd  # lazy

    df = pd.read_parquet(path)
    if "resolved_at" not in df.columns:
        raise DiagnosticHalt(
            STOP_RESOLUTION_SCHEMA,
            f"no 'resolved_at' column; present={list(df.columns)}",
        )
    string_safe_cols = [c for c in df.columns if c != "resolved_at"]
    for c in string_safe_cols:
        df[c] = df[c].astype(str)
    resolved_col = df["resolved_at"].tolist()
    records = df[string_safe_cols].to_dict("records")
    for rec, ra in zip(records, resolved_col):
        rec["resolved_at"] = None if pd.isna(ra) else ra
    return records


def build_universe(
    contract_map: Dict[str, str], resolution_rows: Sequence[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Eligible contract conditions INNER-JOIN resolved single-winner rows.

    The winner columns are never read as a token-pair source; `resolved_at` is
    carried only as the coverage-window upper bound.
    """
    universe: List[Dict[str, Any]] = []
    seen = set()
    for row in resolution_rows:
        if row.get("status") != "RESOLVED_SINGLE_WINNER":
            continue
        if row.get("nb_contract_version") != NB_CONTRACT_VERSION:
            raise DiagnosticHalt(
                STOP_STALE_CONTRACT, f"resolution row version={row.get('nb_contract_version')!r}"
            )
        cid = str(row["condition_id"])
        if cid not in contract_map or cid in seen:
            continue
        seen.add(cid)
        c_sub = contract_map[cid]
        r_sub = row.get("subclass")
        if c_sub != r_sub:
            raise DiagnosticHalt(
                STOP_STALE_CONTRACT,
                f"subclass mismatch for {cid}: contract={c_sub} resolution={r_sub}",
            )
        universe.append(
            {"condition_id": cid, "subclass": c_sub, "resolved_at_raw": row.get("resolved_at")}
        )
    universe.sort(key=lambda r: r["condition_id"])
    return universe


def load_trade_sides_and_anchors(
    data_root: str, condition_ids: Sequence[str]
) -> Tuple[Dict[str, Dict[int, set]], Dict[str, int], Dict[str, float], Dict[str, int]]:
    """Read local trade rows through the canonical Store(root) data-root contract.

    Returns:
      sides_by_condition[cid][outcome_index] -> set of distinct token_id lexemes
      invalid_index_rows[cid]                -> count of rows whose outcome_index is not 0/1
      first_trade_ts[cid]                    -> min(traded_at) as epoch seconds
      malformed_rows[cid]                    -> rows skipped for missing/NaN token/index

    Token id lexemes are preserved as original strings. A *real* non-null
    scientific-notation / float-mangled token id is precision loss and halts the
    run — it is never softened into a missing row.
    """
    try:
        from pm_research.data.store import Store  # lazy; canonical data-root contract
    except Exception as exc:  # noqa: BLE001
        raise DiagnosticHalt(
            STOP_TRADES_STORE_UNAVAILABLE,
            f"pm_research.data.store.Store not importable ({exc!r}); "
            "the accepted local trades access path is Store(root).load_trades()",
        ) from exc

    wanted = set(condition_ids)
    df = Store(data_root).load_trades()
    for col in ("condition_id", "token_id", "outcome_index", "traded_at"):
        if col not in getattr(df, "columns", []):
            raise DiagnosticHalt(
                STOP_RESOLUTION_SCHEMA,
                f"trades table lacks column {col!r}; present={list(getattr(df, 'columns', []))}",
            )
    df = df[df["condition_id"].isin(wanted)]

    sides: Dict[str, Dict[int, set]] = defaultdict(lambda: defaultdict(set))
    invalid_index_rows: Dict[str, int] = defaultdict(int)
    malformed_rows: Dict[str, int] = defaultdict(int)
    first_ts: Dict[str, float] = {}

    for cid, grp in df.groupby("condition_id"):
        cid_s = str(cid)
        for tok, oi in zip(grp["token_id"].tolist(), grp["outcome_index"].tolist()):
            if _is_missing_field(tok) or _is_missing_field(oi):
                malformed_rows[cid_s] += 1
                continue
            try:
                CANON.canonical_int(tok)  # token identity: strict, fails loud
            except CANON.DataExportPrecisionLoss as exc:  # type: ignore[misc]
                raise DiagnosticHalt(
                    STOP_PRECISION_LOSS,
                    f"condition {cid_s}: {exc}. Precision is already lost in the local "
                    "export; a 78-digit id must never be reconstructed from a mangled float.",
                ) from exc
            # outcome_index is a side selector, not an identity — normalized separately.
            idx = normalize_outcome_index(oi)
            if idx is None:
                malformed_rows[cid_s] += 1
                continue
            if idx not in (0, 1):
                invalid_index_rows[cid_s] += 1
                continue
            sides[cid_s][idx].add(str(tok).strip())
        tvals: List[float] = []
        for v in grp["traded_at"].tolist():
            try:
                parsed = float(CANON.parse_ts(v))
            except (ValueError, TypeError):
                malformed_rows[cid_s] += 1
                continue
            # A NaN/inf traded_at would poison min() silently; count it instead.
            if not math.isfinite(parsed):
                malformed_rows[cid_s] += 1
                continue
            tvals.append(parsed)
        if tvals:
            first_ts[cid_s] = min(tvals)
    return sides, invalid_index_rows, first_ts, malformed_rows


def normalize_outcome_index(value: Any) -> Optional[int]:
    """Normalize a trade-row `outcome_index` to an int side selector, or None.

    `outcome_index` is a SIDE SELECTOR over a two-element set, not an identity.
    It carries no precision a float can destroy: 0 and 1 are exactly representable
    in float64, so a pandas object column holding `0.0` / `1.0` denotes the same
    sides as `0` / `1` and is accepted. This is the opposite of `token_id`, where a
    float has already destroyed digits and must never be reconstructed.

    Returns None for a value that does not normalize to an exact integer (e.g.
    `1.5`, scientific notation, unparseable text); the caller counts those as
    malformed rows. Values that normalize to an integer outside the permitted side
    set are returned as-is so the caller can preserve the distinct
    TOKEN_PAIR_OUTCOME_INDEX_INVALID observation. Missing / NaN is handled earlier
    by `_is_missing_field` and never reaches here. This function never sees, and
    never relaxes anything about, `token_id`.
    """
    if isinstance(value, bool):
        return None
    # int and numpy integer types (both implement __index__); exact by construction.
    if hasattr(value, "__index__"):
        try:
            return int(value.__index__())
        except (ValueError, TypeError):
            return None
    # float and numpy.float64 (a float subclass): accept only integer-valued finites.
    if isinstance(value, float):
        if not math.isfinite(value) or float(value) % 1 != 0.0:
            return None
        return int(value)
    # Remaining forms (str, Decimal, ...) go through the accepted string-safe path,
    # which accepts "0" / "1" / "0.0" and rejects "1.5" and scientific notation.
    try:
        return int(CANON.canonical_int(value))
    except CANON.DataExportPrecisionLoss:  # type: ignore[misc]
        return None


def _is_missing_field(value: Any) -> bool:
    """MISSING/malformed (None / empty / NaN / 'nan') — not precision loss."""
    if value is None:
        return True
    if isinstance(value, float):
        return value != value  # NaN
    s = str(value).strip()
    if s == "":
        return True
    if s.lower() in ("nan", "none", "nat"):
        return True
    return False


# ---------------------------------------------------------------------------
# Disposition + decision-window reconstruction
# ---------------------------------------------------------------------------
def classify_condition(
    cid: str,
    resolved_at_raw: Any,
    sides: Dict[int, set],
    invalid_index_row_count: int,
    first_trade_ts: Optional[float],
) -> Dict[str, Any]:
    """Return the condition record with a single deterministic disposition label.

    Precedence (fixed, documented, never reordered):
      1. token-pair structure (side 0 before side 1; missing before ambiguous),
      2. identical-side / invalid-outcome-index degeneracies,
      3. first_trade_ts presence,
      4. resolved_at presence/parseability,
      5. decision-window validity,
      6. REQUEST_ELIGIBLE.
    Per-side states are also emitted separately so no information is collapsed.
    """
    rec: Dict[str, Any] = {
        "condition_id": cid,
        "side_0_token": "",
        "side_1_token": "",
        "side_0_state": "",
        "side_1_state": "",
        "side_0_candidate_count": len(sides.get(0, ())),
        "side_1_candidate_count": len(sides.get(1, ())),
        "invalid_outcome_index_rows": int(invalid_index_row_count),
        "first_trade_ts": "" if first_trade_ts is None else first_trade_ts,
        "decision_lower_ts": "",
        "resolved_at_ts": "",
        "disposition": "",
    }

    def side_state(n: int) -> str:
        count = len(sides.get(n, ()))
        if count == 0:
            return "MISSING"
        if count > 1:
            return "AMBIGUOUS"
        return "CLEAR"

    s0_state, s1_state = side_state(0), side_state(1)
    rec["side_0_state"], rec["side_1_state"] = s0_state, s1_state
    if s0_state == "CLEAR":
        rec["side_0_token"] = next(iter(sides[0]))
    if s1_state == "CLEAR":
        rec["side_1_token"] = next(iter(sides[1]))

    # Checked BEFORE the missing/ambiguous checks: a condition whose only trade
    # rows carry an out-of-range outcome_index is a different observation from a
    # condition with no trade rows at all, and must not be collapsed into
    # TOKEN_PAIR_MISSING_SIDE_0.
    if (
        invalid_index_row_count
        and rec["side_0_candidate_count"] == 0
        and rec["side_1_candidate_count"] == 0
    ):
        rec["disposition"] = TOKEN_PAIR_OUTCOME_INDEX_INVALID
        return rec

    if s0_state == "MISSING":
        rec["disposition"] = TOKEN_PAIR_MISSING_SIDE_0
        return rec
    if s1_state == "MISSING":
        rec["disposition"] = TOKEN_PAIR_MISSING_SIDE_1
        return rec
    if s0_state == "AMBIGUOUS":
        rec["disposition"] = TOKEN_PAIR_AMBIGUOUS_SIDE_0
        return rec
    if s1_state == "AMBIGUOUS":
        rec["disposition"] = TOKEN_PAIR_AMBIGUOUS_SIDE_1
        return rec
    if CANON.canonical_int(rec["side_0_token"]) == CANON.canonical_int(rec["side_1_token"]):
        rec["disposition"] = TOKEN_PAIR_IDENTICAL_SIDES
        return rec

    # Token pair is clear from here on.
    if first_trade_ts is None:
        rec["disposition"] = MISSING_FIRST_TRADE_TS
        return rec
    if not math.isfinite(float(first_trade_ts)):
        rec["disposition"] = MALFORMED_FIRST_TRADE_TS
        return rec

    decision_lower_ts = float(first_trade_ts) + WARMUP_SECONDS
    rec["decision_lower_ts"] = decision_lower_ts

    if resolved_at_raw is None or _is_missing_field(resolved_at_raw):
        rec["disposition"] = MISSING_RESOLVED_AT
        return rec
    try:
        resolved_at_ts = CANON.parse_ts(resolved_at_raw)
    except (ValueError, TypeError):
        rec["disposition"] = MALFORMED_RESOLVED_AT
        return rec
    if not math.isfinite(float(resolved_at_ts)):
        rec["disposition"] = MALFORMED_RESOLVED_AT
        return rec
    rec["resolved_at_ts"] = resolved_at_ts

    # Accepted validity rule: resolved_at strictly AFTER the decision lower bound.
    if not (resolved_at_ts > decision_lower_ts):
        rec["disposition"] = INVALID_DECISION_WINDOW
        return rec

    rec["disposition"] = REQUEST_ELIGIBLE
    return rec


def request_window(decision_lower_ts: float, resolved_at_ts: float) -> Tuple[int, int, bool]:
    """Accepted revised method: startTs = decision_lower_ts - 1, endTs = resolved_at_ts.

    The endpoint takes integer epoch seconds. Anchors derived from the local
    exports are integral in every documented form (`"2025-03-06 00:00:00 UTC"`,
    `".000"` millisecond precision), so rounding is normally a no-op. When an
    anchor is NOT integral this function applies a fixed, declared policy —
    floor on the start, ceil on the end — so the requested range can never be
    narrower than the half-open evaluation window, and it reports the fact via
    the third return value so non-integral anchors are counted, not hidden.
    """
    non_integral = (float(decision_lower_ts) % 1 != 0.0) or (float(resolved_at_ts) % 1 != 0.0)
    start_ts = int(math.floor(decision_lower_ts)) - 1
    end_ts = int(math.ceil(resolved_at_ts))
    return start_ts, end_ts, non_integral


def build_request_url(endpoint_base: str, token_id: str, start_ts: int, end_ts: int) -> str:
    """One token id, camelCase startTs/endTs, fidelity=1, interval OMITTED."""
    params = [
        ("market", str(token_id)),  # market = the token id
        ("startTs", str(int(start_ts))),
        ("endTs", str(int(end_ts))),
        ("fidelity", str(int(REQUEST_FIDELITY))),
    ]
    return (
        endpoint_base.rstrip("/") + PRICES_HISTORY_PATH + "?" + urllib.parse.urlencode(params)
    )


# ---------------------------------------------------------------------------
# Network execution (bounded; only when --execute-network)
# ---------------------------------------------------------------------------
def fetch_once(
    url: str, timeout_seconds: float, user_agent: str
) -> Tuple[Optional[int], Optional[bytes], str, str]:
    """Single GET, zero retries. Returns (http_status, body_bytes, transport_status, error_text)."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            return int(resp.status), resp.read(), TRANSPORT_OK, ""
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read()
        except Exception:  # noqa: BLE001
            body = None
        return int(exc.code), body, TRANSPORT_HTTP_ERROR, str(exc.reason)[:500]
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        status = TRANSPORT_TIMEOUT if isinstance(reason, TimeoutError) else TRANSPORT_CONNECTION_ERROR
        return None, None, status, str(reason)[:500]
    except TimeoutError as exc:
        return None, None, TRANSPORT_TIMEOUT, str(exc)[:500]


def classify_failure_reason(
    http_status: Optional[int],
    transport_status: str,
    level_a_status: str,
    error_text: str,
    body_text: str = "",
) -> str:
    """Deterministic failure label. The known accepted long-window 400 is named.

    The reviewed revalidation recorded a deterministic HTTP 400 whose message
    (`invalid filters: 'startTs' and 'endTs' interval is too long`) appears in the
    RESPONSE BODY, not in the HTTP reason phrase, so both are searched.
    """
    blob = ((error_text or "") + " " + (body_text or "")).lower()
    if http_status == 400 and "interval is too long" in blob:
        return "HTTP_400_START_END_INTERVAL_TOO_LONG"
    if transport_status == TRANSPORT_TIMEOUT:
        return "TRANSPORT_TIMEOUT"
    if transport_status == TRANSPORT_CONNECTION_ERROR:
        return "TRANSPORT_CONNECTION_ERROR"
    if transport_status == TRANSPORT_JSON_UNPARSEABLE:
        return "RESPONSE_JSON_UNPARSEABLE"
    if level_a_status == CANON.STOP_ENDPOINT_SHAPE_UNRECOGNIZED:
        return "RESPONSE_SHAPE_UNRECOGNIZED"
    if level_a_status == CANON.SERIES_MALFORMED:
        return "RESPONSE_POINTS_MALFORMED"
    if http_status is not None and http_status >= 400:
        return f"HTTP_{int(http_status)}"
    return ""


def evaluate_in_window(points: Iterable[Any], lower: float, upper: float) -> Tuple[int, Optional[float], Optional[float]]:
    """Half-open evaluation, unchanged: lower <= t < upper. No synthesis, no complement."""
    in_ts: List[float] = []
    for pt in points:
        ts = float(getattr(pt, "ts"))
        if lower <= ts < upper:
            in_ts.append(ts)
    if not in_ts:
        return 0, None, None
    return len(in_ts), min(in_ts), max(in_ts)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------
MANIFEST_COLUMNS = [
    "condition_id",
    "subclass",
    "outcome_index",
    "token_id",
    "first_trade_ts",
    "decision_lower_ts",
    "resolved_at_ts",
    "request_start_ts",
    "request_end_ts",
    "request_fidelity",
    "request_interval_policy",
    "request_url_or_params",
    "manifest_row_status",
]

CONDITION_COLUMNS = [
    "condition_id",
    "subclass",
    "disposition",
    "side_0_state",
    "side_1_state",
    "side_0_candidate_count",
    "side_1_candidate_count",
    "invalid_outcome_index_rows",
    "malformed_trade_rows",
    "side_0_token",
    "side_1_token",
    "first_trade_ts",
    "decision_lower_ts",
    "resolved_at_ts",
    "window_seconds",
    "non_integral_anchor",
    "side_0_executed",
    "side_1_executed",
    "side_0_in_window_points",
    "side_1_in_window_points",
    "condition_coverage_status",
]

SUBCLASS_COLUMNS = [
    "subclass",
    "universe_conditions",
    "token_pair_clear_conditions",
    "request_eligible_conditions",
    "request_eligible_token_sides",
    "executed_requests",
    "in_window_present_sides",
    "in_window_empty_sides",
    "both_sides_present_conditions",
    "one_side_present_conditions",
    "neither_side_present_conditions",
    "side_not_measurable_conditions",
    "incomplete_conditions",
]


def _write_csv(path: str, columns: Sequence[str], rows: Iterable[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_json(path: str, payload: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")


def _raw_path_non_clobbering(raw_dir: str, condition_id: str, outcome_index: int) -> str:
    """Never silently overwrite a raw response file."""
    base_dir = os.path.join(raw_dir, condition_id)
    os.makedirs(base_dir, exist_ok=True)
    candidate = os.path.join(base_dir, f"outcome_{outcome_index}.json")
    n = 1
    while os.path.exists(candidate):
        candidate = os.path.join(base_dir, f"outcome_{outcome_index}.{n}.json")
        n += 1
    return candidate


def load_prior_results(results_path: str) -> Tuple[set, Dict[str, Dict[int, Optional[int]]]]:
    """Restore completed (condition_id, outcome_index) keys AND their measured
    in-window counts, so a resumed run's condition-level rollup covers earlier
    rows instead of silently reporting only this session's requests."""
    done: set = set()
    prior: Dict[str, Dict[int, Optional[int]]] = defaultdict(dict)
    if not os.path.isfile(results_path):
        return done, prior
    with open(results_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            cid = row.get("condition_id")
            oi = row.get("outcome_index")
            if cid is None or oi is None:
                continue
            cid_s, oi_i = str(cid), int(oi)
            done.add((cid_s, oi_i))
            value = row.get("in_window_point_count")
            prior[cid_s][oi_i] = None if value is None else int(value)
    return done, prior


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def run(args: argparse.Namespace) -> int:
    print(NON_AUTHORIZING)
    print(NON_AUTHORIZING_STATEMENT)

    repo_root = _resolve(args.repo_root)
    data_root = _resolve(args.data_root)
    artifacts_root = _resolve(args.artifacts_root)
    output_root = _resolve(args.output_root)
    out_dir = os.path.join(output_root, "p0_per_token_price_source_scale_diagnostic_01")

    # --- write-boundary guard -------------------------------------------------
    for forbidden, label in ((repo_root, "repo-root"), (artifacts_root, "artifacts-root"), (data_root, "data-root")):
        if _is_within(out_dir, forbidden):
            raise DiagnosticHalt(
                STOP_OUTPUT_ROOT_FORBIDDEN,
                f"output would land inside {label} ({forbidden}); choose an output root "
                "outside the repository, the artifacts tree, and the data store",
            )

    # --- endpoint host guard --------------------------------------------------
    parsed_endpoint = urllib.parse.urlparse(args.endpoint_base)
    if parsed_endpoint.scheme != "https" or not parsed_endpoint.netloc:
        raise DiagnosticHalt(STOP_ENDPOINT_HOST_FORBIDDEN, f"endpoint-base={args.endpoint_base!r}")
    if args.execute_network and parsed_endpoint.netloc != urllib.parse.urlparse(
        DEFAULT_ENDPOINT_BASE
    ).netloc:
        raise DiagnosticHalt(
            STOP_ENDPOINT_HOST_FORBIDDEN,
            f"network execution is limited to {DEFAULT_ENDPOINT_BASE}; got {args.endpoint_base!r}",
        )

    # --- canonical helper semantics ------------------------------------------
    load_canonical_helpers(repo_root)

    execute_network = bool(args.execute_network) and not bool(args.dry_run)
    started_at = _utc_now()

    manifest_dir = os.path.join(out_dir, "manifest")
    results_dir = os.path.join(out_dir, "results")
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(manifest_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    if args.save_raw and execute_network:
        os.makedirs(raw_dir, exist_ok=True)

    # --- inputs ---------------------------------------------------------------
    p0_doc, final_p0_eligible_declared = load_p0_preflight(artifacts_root)
    contract_map = load_contract_conditions(artifacts_root)
    resolution_rows = load_resolution_rows(artifacts_root)
    universe = build_universe(contract_map, resolution_rows)
    final_p0_rows_loaded = len(universe)

    if args.subclass:
        universe = [c for c in universe if c["subclass"] in set(args.subclass)]
    if args.condition_id:
        wanted = set(args.condition_id)
        universe = [c for c in universe if c["condition_id"] in wanted]
    if args.max_conditions is not None:
        universe = universe[: max(0, int(args.max_conditions))]

    sides_map, invalid_idx_map, first_ts_map, malformed_map = load_trade_sides_and_anchors(
        data_root, [c["condition_id"] for c in universe]
    )

    # --- classification + manifest -------------------------------------------
    condition_records: List[Dict[str, Any]] = []
    manifest_rows: List[Dict[str, Any]] = []
    disposition_counts: Counter = Counter()
    disposition_by_subclass: Dict[str, Counter] = defaultdict(Counter)
    non_integral_anchor_count = 0

    for cond in universe:
        cid = cond["condition_id"]
        rec = classify_condition(
            cid=cid,
            resolved_at_raw=cond["resolved_at_raw"],
            sides=sides_map.get(cid, {}),
            invalid_index_row_count=invalid_idx_map.get(cid, 0),
            first_trade_ts=first_ts_map.get(cid),
        )
        rec["subclass"] = cond["subclass"]
        rec["malformed_trade_rows"] = malformed_map.get(cid, 0)
        rec["window_seconds"] = ""
        rec["non_integral_anchor"] = ""
        rec["side_0_executed"] = 0
        rec["side_1_executed"] = 0
        rec["side_0_in_window_points"] = ""
        rec["side_1_in_window_points"] = ""
        rec["condition_coverage_status"] = CONDITION_NOT_EXECUTED

        disposition_counts[rec["disposition"]] += 1
        disposition_by_subclass[rec["subclass"]][rec["disposition"]] += 1

        if rec["disposition"] == REQUEST_ELIGIBLE:
            lower = float(rec["decision_lower_ts"])
            upper = float(rec["resolved_at_ts"])
            start_ts, end_ts, non_integral = request_window(lower, upper)
            rec["window_seconds"] = upper - lower
            rec["non_integral_anchor"] = int(bool(non_integral))
            if non_integral:
                non_integral_anchor_count += 1
            for outcome_index in (0, 1):
                token_id = rec["side_0_token"] if outcome_index == 0 else rec["side_1_token"]
                manifest_rows.append(
                    {
                        "condition_id": cid,
                        "subclass": rec["subclass"],
                        "outcome_index": outcome_index,
                        "token_id": token_id,
                        "first_trade_ts": rec["first_trade_ts"],
                        "decision_lower_ts": lower,
                        "resolved_at_ts": upper,
                        "request_start_ts": start_ts,
                        "request_end_ts": end_ts,
                        "request_fidelity": REQUEST_FIDELITY,
                        "request_interval_policy": REQUEST_INTERVAL_POLICY,
                        "request_url_or_params": build_request_url(
                            args.endpoint_base, token_id, start_ts, end_ts
                        ),
                        "manifest_row_status": REQUEST_ELIGIBLE,
                    }
                )
        condition_records.append(rec)

    # Deterministic order: condition_id ascending, outcome_index 0 before 1.
    manifest_rows.sort(key=lambda r: (r["condition_id"], int(r["outcome_index"])))
    condition_records.sort(key=lambda r: r["condition_id"])

    _write_csv(os.path.join(manifest_dir, "request_manifest.csv"), MANIFEST_COLUMNS, manifest_rows)

    token_pair_clear = sum(
        1
        for r in condition_records
        if r["disposition"]
        not in (
            TOKEN_PAIR_MISSING_SIDE_0,
            TOKEN_PAIR_MISSING_SIDE_1,
            TOKEN_PAIR_AMBIGUOUS_SIDE_0,
            TOKEN_PAIR_AMBIGUOUS_SIDE_1,
            TOKEN_PAIR_IDENTICAL_SIDES,
            TOKEN_PAIR_OUTCOME_INDEX_INVALID,
        )
    )
    request_eligible_conditions = disposition_counts[REQUEST_ELIGIBLE]

    manifest_summary = {
        "diagnostic_id": DIAGNOSTIC_ID,
        "non_authorizing": NON_AUTHORIZING,
        "final_p0_rows_loaded": final_p0_rows_loaded,
        "final_p0_eligible_declared_by_preflight": final_p0_eligible_declared,
        "expected_final_p0_eligible": EXPECTED_FINAL_P0_ELIGIBLE,
        "final_p0_rows_reconcile_to_expected": final_p0_rows_loaded == EXPECTED_FINAL_P0_ELIGIBLE,
        "universe_after_filters": len(universe),
        "token_pair_clear_conditions": token_pair_clear,
        "request_eligible_conditions": request_eligible_conditions,
        "request_eligible_token_sides": len(manifest_rows),
        "upper_bound_token_sides_if_all_eligible": 2 * len(universe),
        "non_integral_anchor_conditions": non_integral_anchor_count,
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "disposition_counts_by_subclass": {
            sub: dict(sorted(counts.items())) for sub, counts in sorted(disposition_by_subclass.items())
        },
        "request_method": {
            "query_unit": "ONE_INDEPENDENT_TOKEN_ID_PER_SIDE",
            "startTs": "decision_lower_ts - 1",
            "endTs": "resolved_at_ts",
            "fidelity": REQUEST_FIDELITY,
            "interval": REQUEST_INTERVAL_POLICY,
            "retry_count": RETRY_COUNT,
            "evaluation_window": "decision_lower_ts <= t < resolved_at_ts",
            "warmup_seconds": WARMUP_SECONDS,
            "request_window_rounding_policy": "start=floor(decision_lower_ts)-1; end=ceil(resolved_at_ts)",
        },
        "forbidden_shortcuts_not_used": FORBIDDEN_SHORTCUTS_NOT_USED,
        "filters": {
            "subclass": list(args.subclass or []),
            "condition_id": list(args.condition_id or []),
            "max_conditions": args.max_conditions,
            "max_requests": args.max_requests,
        },
    }
    _write_json(os.path.join(manifest_dir, "request_manifest_summary.json"), manifest_summary)

    # --- network stage --------------------------------------------------------
    results_path = os.path.join(results_dir, "request_results.jsonl")
    executed = 0
    http_counts: Counter = Counter()
    transport_counts: Counter = Counter()
    level_a_counts: Counter = Counter()
    failure_counts: Counter = Counter()
    in_window_present = 0
    in_window_empty = 0
    malformed_responses = 0
    error_responses = 0
    per_condition_exec: Dict[str, Dict[int, Optional[int]]] = defaultdict(dict)

    if args.resume:
        resume_keys, prior_exec = load_prior_results(results_path)
        per_condition_exec.update(prior_exec)
    else:
        resume_keys, prior_exec = set(), {}
        if execute_network and os.path.isfile(results_path):
            raise DiagnosticHalt(
                STOP_RESULTS_EXIST,
                f"{results_path} already exists; rerun with --resume or choose a fresh "
                "--output-root. Prior results are never silently truncated.",
            )
    skipped_resumed = 0

    if execute_network:
        mode = "a" if (args.resume and os.path.isfile(results_path)) else "w"
        with open(results_path, mode, encoding="utf-8") as sink:
            for row in manifest_rows:
                if args.max_requests is not None and executed >= int(args.max_requests):
                    break
                key = (row["condition_id"], int(row["outcome_index"]))
                if key in resume_keys:
                    skipped_resumed += 1
                    continue

                url = row["request_url_or_params"]
                t0 = time.time()
                http_status, body_bytes, transport_status, error_text = fetch_once(
                    url, float(args.timeout_seconds), args.user_agent
                )
                elapsed_ms = int((time.time() - t0) * 1000)
                executed += 1

                body_sha = ""
                raw_saved_path = ""
                if body_bytes is not None:
                    body_sha = _sha256_bytes(body_bytes)
                    if args.save_raw:
                        raw_saved_path = _raw_path_non_clobbering(
                            raw_dir, row["condition_id"], int(row["outcome_index"])
                        )
                        with open(raw_saved_path, "wb") as raw_fh:
                            raw_fh.write(body_bytes)

                parsed_body: Any = None
                if body_bytes is not None:
                    try:
                        parsed_body = json.loads(body_bytes.decode("utf-8"))
                    except (ValueError, UnicodeDecodeError) as exc:
                        transport_status = TRANSPORT_JSON_UNPARSEABLE
                        error_text = error_text or str(exc)[:500]

                level_a_status = ""
                point_count_total = ""
                in_window_count: Optional[int] = None
                first_in_window: Optional[float] = None
                last_in_window: Optional[float] = None
                in_window_disposition = IN_WINDOW_NOT_EVALUABLE

                if transport_status != TRANSPORT_JSON_UNPARSEABLE:
                    try:
                        series = CANON.map_response_to_status(
                            http_status, parsed_body, str(row["token_id"])
                        )
                        level_a_status = series.status
                        point_count_total = len(series.points)
                        if level_a_status == CANON.SERIES_PRESENT:
                            in_window_count, first_in_window, last_in_window = evaluate_in_window(
                                series.points,
                                float(row["decision_lower_ts"]),
                                float(row["resolved_at_ts"]),
                            )
                            in_window_disposition = (
                                IN_WINDOW_PRESENT if in_window_count > 0 else IN_WINDOW_EMPTY
                            )
                        elif level_a_status == CANON.SERIES_EMPTY:
                            in_window_count = 0
                            in_window_disposition = IN_WINDOW_EMPTY
                    except CANON.EndpointShapeError as exc:  # type: ignore[misc]
                        # Measurement-scoped: recorded per row and counted, never
                        # turned into a synthesized price and never a silent pass.
                        level_a_status = CANON.STOP_ENDPOINT_SHAPE_UNRECOGNIZED
                        error_text = error_text or str(exc)[:500]

                body_text = ""
                if body_bytes is not None:
                    body_text = body_bytes[:2000].decode("utf-8", errors="replace")
                failure_reason = classify_failure_reason(
                    http_status, transport_status, level_a_status, error_text, body_text
                )

                http_counts[str(http_status) if http_status is not None else "NONE"] += 1
                transport_counts[transport_status] += 1
                if level_a_status:
                    level_a_counts[level_a_status] += 1
                if failure_reason:
                    failure_counts[failure_reason] += 1
                if in_window_disposition == IN_WINDOW_PRESENT:
                    in_window_present += 1
                elif in_window_disposition == IN_WINDOW_EMPTY:
                    in_window_empty += 1
                if level_a_status in (CANON.SERIES_MALFORMED, CANON.STOP_ENDPOINT_SHAPE_UNRECOGNIZED):
                    malformed_responses += 1
                if transport_status != TRANSPORT_OK or (
                    http_status is not None and http_status >= 400
                ):
                    error_responses += 1

                per_condition_exec[row["condition_id"]][int(row["outcome_index"])] = (
                    in_window_count if in_window_count is not None else None
                )

                sink.write(
                    json.dumps(
                        {
                            "diagnostic_id": DIAGNOSTIC_ID,
                            "non_authorizing": NON_AUTHORIZING,
                            "condition_id": row["condition_id"],
                            "subclass": row["subclass"],
                            "outcome_index": int(row["outcome_index"]),
                            "token_id": row["token_id"],
                            "decision_lower_ts": row["decision_lower_ts"],
                            "resolved_at_ts": row["resolved_at_ts"],
                            "request_start_ts": row["request_start_ts"],
                            "request_end_ts": row["request_end_ts"],
                            "request_fidelity": REQUEST_FIDELITY,
                            "request_interval_policy": REQUEST_INTERVAL_POLICY,
                            "request_url": url,
                            "requested_at_utc": _utc_now(),
                            "elapsed_ms": elapsed_ms,
                            "http_status": http_status,
                            "transport_status": transport_status,
                            "level_a_status": level_a_status,
                            "point_count_total": point_count_total,
                            "in_window_point_count": in_window_count,
                            "first_in_window_ts": first_in_window,
                            "last_in_window_ts": last_in_window,
                            "in_window_disposition": in_window_disposition,
                            "failure_reason": failure_reason,
                            "error_text": error_text,
                            "raw_response_sha256": body_sha,
                            "raw_response_path": raw_saved_path,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
                sink.flush()
                if args.sleep_seconds:
                    time.sleep(float(args.sleep_seconds))

    # --- condition-level rollup ----------------------------------------------
    both_sides = one_side = neither_side = incomplete = not_measurable = 0
    for rec in condition_records:
        if rec["disposition"] != REQUEST_ELIGIBLE or not execute_network:
            continue
        exec_map = per_condition_exec.get(rec["condition_id"], {})
        rec["side_0_executed"] = int(0 in exec_map)
        rec["side_1_executed"] = int(1 in exec_map)
        rec["side_0_in_window_points"] = exec_map.get(0, "")
        rec["side_1_in_window_points"] = exec_map.get(1, "")
        if not (rec["side_0_executed"] and rec["side_1_executed"]):
            rec["condition_coverage_status"] = CONDITION_INCOMPLETE_BOUNDED_RUN
            incomplete += 1
            continue
        if any(exec_map.get(i) is None for i in (0, 1)):
            rec["condition_coverage_status"] = CONDITION_SIDE_NOT_MEASURABLE
            not_measurable += 1
            continue
        present = sum(1 for i in (0, 1) if int(exec_map[i]) > 0)
        if present == 2:
            rec["condition_coverage_status"] = DECISION_PRICE_BOTH_SIDES
            both_sides += 1
        elif present == 1:
            rec["condition_coverage_status"] = DECISION_PRICE_ONE_SIDE
            one_side += 1
        else:
            rec["condition_coverage_status"] = DECISION_PRICE_NEITHER
            neither_side += 1

    _write_csv(
        os.path.join(results_dir, "condition_summary.csv"), CONDITION_COLUMNS, condition_records
    )

    # --- subclass rollup ------------------------------------------------------
    sub_rows: List[Dict[str, Any]] = []
    for sub in ORIENTED_SUBCLASSES:
        recs = [r for r in condition_records if r["subclass"] == sub]
        if not recs:
            continue
        sub_eligible = [r for r in recs if r["disposition"] == REQUEST_ELIGIBLE]
        sub_rows.append(
            {
                "subclass": sub,
                "universe_conditions": len(recs),
                "token_pair_clear_conditions": sum(
                    1
                    for r in recs
                    if r["disposition"]
                    not in (
                        TOKEN_PAIR_MISSING_SIDE_0,
                        TOKEN_PAIR_MISSING_SIDE_1,
                        TOKEN_PAIR_AMBIGUOUS_SIDE_0,
                        TOKEN_PAIR_AMBIGUOUS_SIDE_1,
                        TOKEN_PAIR_IDENTICAL_SIDES,
                        TOKEN_PAIR_OUTCOME_INDEX_INVALID,
                    )
                ),
                "request_eligible_conditions": len(sub_eligible),
                "request_eligible_token_sides": 2 * len(sub_eligible),
                "executed_requests": sum(
                    int(r["side_0_executed"]) + int(r["side_1_executed"]) for r in recs
                ),
                "in_window_present_sides": sum(
                    1
                    for r in recs
                    for v in (r["side_0_in_window_points"], r["side_1_in_window_points"])
                    if isinstance(v, int) and v > 0
                ),
                "in_window_empty_sides": sum(
                    1
                    for r in recs
                    for v in (r["side_0_in_window_points"], r["side_1_in_window_points"])
                    if isinstance(v, int) and v == 0
                ),
                "both_sides_present_conditions": sum(
                    1 for r in recs if r["condition_coverage_status"] == DECISION_PRICE_BOTH_SIDES
                ),
                "one_side_present_conditions": sum(
                    1 for r in recs if r["condition_coverage_status"] == DECISION_PRICE_ONE_SIDE
                ),
                "neither_side_present_conditions": sum(
                    1 for r in recs if r["condition_coverage_status"] == DECISION_PRICE_NEITHER
                ),
                "side_not_measurable_conditions": sum(
                    1
                    for r in recs
                    if r["condition_coverage_status"] == CONDITION_SIDE_NOT_MEASURABLE
                ),
                "incomplete_conditions": sum(
                    1
                    for r in recs
                    if r["condition_coverage_status"] == CONDITION_INCOMPLETE_BOUNDED_RUN
                ),
            }
        )
    _write_csv(os.path.join(results_dir, "subclass_summary.csv"), SUBCLASS_COLUMNS, sub_rows)

    results_summary = {
        "diagnostic_id": DIAGNOSTIC_ID,
        "non_authorizing": NON_AUTHORIZING,
        "non_authorizing_statement": NON_AUTHORIZING_STATEMENT,
        "execute_network": execute_network,
        "dry_run": bool(args.dry_run),
        "final_p0_rows_loaded": final_p0_rows_loaded,
        "token_pair_clear_conditions": token_pair_clear,
        "request_eligible_conditions": request_eligible_conditions,
        "request_eligible_token_sides": len(manifest_rows),
        "executed_requests": executed,
        "skipped_resumed_rows": skipped_resumed,
        "http_status_counts": dict(sorted(http_counts.items())),
        "transport_status_counts": dict(sorted(transport_counts.items())),
        "level_a_status_counts": dict(sorted(level_a_counts.items())),
        "in_window_present_sides": in_window_present,
        "in_window_empty_sides": in_window_empty,
        "malformed_response_count": malformed_responses,
        "error_response_count": error_responses,
        "condition_both_sides_present": both_sides,
        "condition_one_side_present": one_side,
        "condition_neither_side_present": neither_side,
        "condition_side_not_measurable": not_measurable,
        "condition_incomplete_bounded_run": incomplete,
        "top_failure_reasons": [
            {"failure_reason": k, "count": v} for k, v in failure_counts.most_common(20)
        ],
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "forbidden_shortcuts_not_used": FORBIDDEN_SHORTCUTS_NOT_USED,
    }
    _write_json(os.path.join(results_dir, "request_results_summary.json"), results_summary)

    # --- run metadata ---------------------------------------------------------
    run_metadata = {
        "diagnostic_id": DIAGNOSTIC_ID,
        "script_path": os.path.abspath(__file__),
        "script_sha256": _sha256_file(os.path.abspath(__file__)),
        "canonical_helper_module": CANON.module_path,
        "canonical_helper_module_sha256": _sha256_file(CANON.module_path),
        "started_at_utc": started_at,
        "completed_at_utc": _utc_now(),
        "repo_root": repo_root,
        "data_root": data_root,
        "artifacts_root": artifacts_root,
        "output_root": output_root,
        "output_dir": out_dir,
        "endpoint_base": args.endpoint_base,
        "endpoint_path": PRICES_HISTORY_PATH,
        "execute_network": execute_network,
        "dry_run": bool(args.dry_run),
        "max_conditions": args.max_conditions,
        "max_requests": args.max_requests,
        "subclass_filter": list(args.subclass or []),
        "condition_id_filter": list(args.condition_id or []),
        "resume": bool(args.resume),
        "save_raw": bool(args.save_raw),
        "sleep_seconds": float(args.sleep_seconds),
        "timeout_seconds": float(args.timeout_seconds),
        "user_agent": args.user_agent,
        "retry_count": RETRY_COUNT,
        "request_fidelity": REQUEST_FIDELITY,
        "request_interval_policy": REQUEST_INTERVAL_POLICY,
        "warmup_seconds": WARMUP_SECONDS,
        "nb_contract_version": NB_CONTRACT_VERSION,
        "p0_state": p0_doc.get("p0_state"),
        "executed_requests": executed,
        "forbidden_shortcuts_not_used": FORBIDDEN_SHORTCUTS_NOT_USED,
        "non_authorizing": NON_AUTHORIZING,
        "non_authorizing_statement": NON_AUTHORIZING_STATEMENT,
    }
    _write_json(os.path.join(out_dir, "run_metadata.json"), run_metadata)

    print(json.dumps({k: results_summary[k] for k in (
        "final_p0_rows_loaded",
        "token_pair_clear_conditions",
        "request_eligible_conditions",
        "request_eligible_token_sides",
        "executed_requests",
        "in_window_present_sides",
        "in_window_empty_sides",
        "condition_both_sides_present",
        "condition_one_side_present",
        "condition_neither_side_present",
        "condition_side_not_measurable",
    )}, indent=2))
    print(f"outputs under: {out_dir}")
    print(NON_AUTHORIZING)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            f"{DIAGNOSTIC_ID} — {NON_AUTHORIZING}. Scales the reviewed revised S1 "
            "per-token/per-side CLOB /prices-history method to the current P0 eligible universe."
        )
    )
    p.add_argument("--repo-root", required=True, help="Checkout root of rigolugo/pm_research.")
    p.add_argument("--data-root", required=True, help="Local data store root passed to Store(root).")
    p.add_argument("--artifacts-root", required=True, help="Artifacts root (read-only).")
    p.add_argument("--output-root", required=True, help="Diagnostic output root; must be OUTSIDE repo/artifacts/data.")
    p.add_argument("--endpoint-base", default=DEFAULT_ENDPOINT_BASE, help=f"Default {DEFAULT_ENDPOINT_BASE}.")
    p.add_argument("--execute-network", action="store_true", help="Required to issue any request.")
    p.add_argument("--dry-run", action="store_true", help="Manifest + summaries only; overrides --execute-network.")
    p.add_argument("--max-conditions", type=int, default=None)
    p.add_argument("--max-requests", type=int, default=None)
    p.add_argument("--subclass", action="append", choices=list(ORIENTED_SUBCLASSES), default=None)
    p.add_argument("--condition-id", action="append", default=None)
    p.add_argument("--sleep-seconds", type=float, default=0.0)
    p.add_argument("--timeout-seconds", type=float, default=30.0)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--save-raw", action="store_true")
    p.add_argument("--user-agent", default=f"pm_research-{DIAGNOSTIC_ID.lower()}/1")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        return run(args)
    except DiagnosticHalt as halt:
        print(f"{halt.label}: {halt.detail}", file=sys.stderr)
        print(NON_AUTHORIZING, file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
