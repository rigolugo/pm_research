"""Option C, C1A-F1 - deterministic, outcome-independent selector policy.

CODE / TEST ONLY. No network call. No Dune call. No live query execution. No run.

Governing spec:
- project_context/SPEC_price_source_option_c_c1a_followup.md (C1A-F1 selector-policy
  addendum; sections 6.2-6.6 and 8). This module implements ONLY the deterministic
  selector-policy machinery that spec defines. It selects a fixed 3-5 condition
  candidate set from an already-accepted, already-bounded local selector pool. It
  does NOT build a manifest query, does NOT fetch Dune, does NOT run a canary.

Where this fits in the pipeline (design intent, not executed here):
    [accepted bounded pool]                    <- already accepted, bounded
        -> C1A-F1 selector (this module)        <- picks 3-5 candidate condition_ids
        -> C1A manifest builder (existing)      <- resolves token pairs, renders SQL TEXT
        -> [user-run Dune step, separately authorized only]
        -> C1A canary reconciliation (existing) <- caps + cap+1 discipline

This module stops at the first arrow's output: a fixed, reproducible candidate list
plus a selector-policy provenance record. Every downstream step remains separately
gated and is NOT authorized by this file.

Default selector pool (spec section 6.2, hard requirement):
  The already-accepted small S1/S1-ALT eligible pool / C1A-compatible measured pool.
  This module MUST NOT scan or profile the full ~288K-condition universe, and MUST
  NOT build a reusable volume-profiling artifact. The pool is small and fixed; this
  module only *reads/uses* it and *ranks within it*.

APPROVED LOCAL-DENSITY METRICS (spec section 6.3 item 3 - the ONLY density inputs):
  - local_trade_rows_in_window
  - local_distinct_tx_hash_count_in_window
  - window_seconds
  These are derived from LOCAL TRADE ROWS (spec section 6.2 item 2), under one
  deterministic fixed-window rule applied to every candidate. They are selector
  diagnostics only - not query filters, not constants, not guarantees of on-chain
  OrderFilled volume.

REJECTED as density inputs (Orchestrator BLOCK, this patch):
  S1 CLOB `/prices-history` coverage diagnostics are NOT local-trade density and
  must never rank C1A-F1 candidates. This module explicitly refuses to use
  `observed_point_count_side_0`, `observed_point_count_side_1`, nearest-gap fields,
  or any CLOB-price-history point count as a density input. Those are diagnostics of
  a different, already-rejected source (Option A / S1), not local trade-store rows.

Two allowed density-input shapes (spec "Allowed implementation shapes"):
  1) A bounded pool file that ALREADY contains the approved local-density fields
     (`local_trade_rows_in_window`, `local_distinct_tx_hash_count_in_window`,
     `window_seconds`) - read directly, no trade recomputation. (No pandas needed.)
  2) Compute the approved fields from `Store.load_trades()` restricted ONLY to the
     bounded-pool condition IDs, inside the deterministic fixed window. Lazy pandas/
     Store import; Claude does not execute this path.

Outcome-independence (spec sections 5.7, 6.2, 8): the selector reads ONLY
non-winner, non-outcome, non-price identity/eligibility/density fields. It NEVER
reads resolved_winning_*, payout vectors, outcome labels, PnL, score, price,
yes_price, 1 - price, or any outcome-conditioned field. Presence of any such field
is a hard reject.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Pinned constants
# ---------------------------------------------------------------------------
PHASE = "OPTION_C_C1A_F1_SELECTOR"
AUTHORIZED_SCOPE = "OPTION_C_C1A_F1_SELECTOR_POLICY_ONLY_NO_NETWORK_NO_RUN"

# Versioned selector-policy string - a REQUIRED input to the deterministic hash
# tie-breaker (spec 6.2 item 5 / 6.3 item 7). Bump if policy semantics change.
# Bumped in this patch because the density metric changed from S1 CLOB point
# counts to approved local-trade-row density.
SELECTOR_POLICY_VERSION = "c1a-f1-selector-2026-07-08.2-localtrade-density"

ORIENTED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")  # no YES_NO, no UNUSABLE

MIN_C1A_CONDITIONS = 3
MAX_C1A_CONDITIONS = 5

# C1A caps and cap+1 discipline are PRESERVED (spec 6.5). This module never raises
# them and never emits a query; these are recorded into provenance ONLY so
# downstream metadata references stay consistent with the accepted ceilings.
PER_CONDITION_ROW_CAP_CEILING = 2000
GLOBAL_ROW_CAP_CEILING = 6000
DUNE_QUERY_LIMIT_OVER_FETCH = PER_CONDITION_ROW_CAP_CEILING + 1  # cap + 1, provenance only

CONDITION_ID_RE = re.compile(r"^0x[0-9a-f]{64}$")
_SCI_RE = re.compile(r"[eE]")
_INT_RE = re.compile(r"^[0-9]+$")

# ---------------------------------------------------------------------------
# Approved vs. rejected density fields
# ---------------------------------------------------------------------------
# The ONLY approved local-density fields (spec 6.3 item 3).
APPROVED_DENSITY_FIELDS = (
    "local_trade_rows_in_window",
    "local_distinct_tx_hash_count_in_window",
    "window_seconds",
)

# S1 CLOB `/prices-history` coverage diagnostics and other non-local-trade density
# proxies. These MUST NOT be used to rank C1A-F1 candidates (Orchestrator BLOCK).
# If any appears as a *density* input path, the selector refuses it. (They are not
# in FORBIDDEN_INPUT_KEYS because they are not winner/price/score leakage - they
# are simply the WRONG density source - so they get a distinct, explicit refusal.)
REJECTED_DENSITY_FIELDS = frozenset(
    {
        "observed_point_count_side_0",
        "observed_point_count_side_1",
        "nearest_gap_side_0_seconds",
        "nearest_gap_side_1_seconds",
        "price_history_point_count",
        "clob_point_count",
        "clob_density",
    }
)

# The bounded pool identity/eligibility columns this selector may consume. Note:
# S1's observed_point_count_* / nearest_gap_* columns are DELIBERATELY absent here,
# so a plain S1 coverage CSV can still be used to define the *bounded condition set*
# and static identity, but its CLOB point counts can never reach density logic.
ALLOWED_IDENTITY_COLUMNS = frozenset(
    {
        "condition_id",
        "subclass",
        "side_0_token",
        "side_1_token",
        "condition_reachability",   # both / one / neither (coarse static feasibility)
        "level_b_class",            # coarse static feasibility label
    }
)

# Forbidden input keys: winner/outcome/price/score leakage (spec 8 reject cond.
# 7, 8, 9). Presence is a hard stop regardless of whether logic would read it.
FORBIDDEN_INPUT_KEYS = frozenset(
    {
        "resolved_winning_token_id",
        "resolved_winning_outcome_index",
        "resolved_winning_label",
        "winner_token_id",
        "winning_token_id",
        "payout_numerators",
        "payout_vector",
        "pnl",
        "profit",
        "score",
        "brier",
        "log_loss",
        "price",
        "yes_price",
        "side_0_price",
        "side_1_price",
        "canonical_side_price",
        "p",
    }
)

# ---------------------------------------------------------------------------
# Typed status / stop codes (spec section 6.6 + reject conditions)
# ---------------------------------------------------------------------------
SELECTOR_OK = "OK"
C1F_SELECTOR_REJECTED = "C1F_SELECTOR_REJECTED"

REJECT_OUTCOME_CONDITIONED_FIELD = "REJECT_OUTCOME_CONDITIONED_FIELD"
REJECT_SUBCLASS_NOT_ORIENTED = "REJECT_SUBCLASS_NOT_ORIENTED"
REJECT_TOKEN_PAIR_NOT_TWO_STABLE = "REJECT_TOKEN_PAIR_NOT_TWO_STABLE"
REJECT_TOKEN_PRECISION_LOSS = "REJECT_TOKEN_PRECISION_LOSS"
REJECT_CONDITION_ID_MALFORMED = "REJECT_CONDITION_ID_MALFORMED"
REJECT_NOT_REACHABLE_BOTH = "REJECT_NOT_REACHABLE_BOTH"
REJECT_DENSITY_UNPARSEABLE = "REJECT_DENSITY_UNPARSEABLE"
REJECT_DENSITY_MISSING = "REJECT_DENSITY_MISSING"
REJECT_PRIOR_C1A_HOLDOUT = "REJECT_PRIOR_C1A_HOLDOUT"

FAIL_POOL_TOO_SMALL = "FAIL_POOL_TOO_SMALL"
FAIL_NO_ELIGIBLE_CANDIDATES = "FAIL_NO_ELIGIBLE_CANDIDATES"
FAIL_COUNT_OUT_OF_RANGE = "FAIL_COUNT_OUT_OF_RANGE"
FAIL_FORBIDDEN_POOL_SOURCE = "FAIL_FORBIDDEN_POOL_SOURCE"
FAIL_REJECTED_DENSITY_FIELD = "FAIL_REJECTED_DENSITY_FIELD"


class OutcomeConditionedInputError(ValueError):
    """Raised if a record carries any winner/outcome/price/score field."""


class RejectedDensitySourceError(ValueError):
    """Raised if S1 CLOB point counts / nearest-gap / other non-local-trade
    density proxies are supplied as the C1A-F1 density input (Orchestrator BLOCK)."""


class DensityPrecisionError(ValueError):
    """Raised on scientific-notation / float-mangled numeric density fields."""


class SelectorPolicyError(ValueError):
    """Raised when the selector policy cannot produce a valid manifest under the
    stated rules (maps to C1F_SELECTOR_REJECTED)."""


# ---------------------------------------------------------------------------
# Precision-safe integer parsing (mirrors accepted S1/C1A canonical_int)
# ---------------------------------------------------------------------------
def canonical_count(value: Any) -> int:
    if value is None:
        raise DensityPrecisionError("canonical_count received None")
    if isinstance(value, bool):
        raise DensityPrecisionError(f"bool is not a count: {value!r}")
    if isinstance(value, float):
        raise DensityPrecisionError(f"float count not string-safe: {value!r}")
    s = str(value).strip()
    if s == "":
        raise DensityPrecisionError("canonical_count received empty string")
    if _SCI_RE.search(s):
        raise DensityPrecisionError(f"scientific notation (precision lost): {s!r}")
    if "." in s:
        head, _, tail = s.partition(".")
        if tail.strip("0") != "" or not _INT_RE.match(head or "0"):
            raise DensityPrecisionError(f"non-integer count: {s!r}")
        s = head if head != "" else "0"
    if not _INT_RE.match(s):
        raise DensityPrecisionError(f"non-integer count: {s!r}")
    return int(s)


def is_string_safe_token(value: Any) -> bool:
    if value is None or isinstance(value, (bool, float)):
        return False
    s = str(value).strip()
    if s == "" or _SCI_RE.search(s):
        return False
    return bool(_INT_RE.match(s))


# ---------------------------------------------------------------------------
# Deterministic tie-breaker (spec 6.2 item 5 / 6.3 item 7)
# ---------------------------------------------------------------------------
def tie_break_key(condition_id: str, policy_version: str = SELECTOR_POLICY_VERSION) -> str:
    payload = f"{condition_id}|{policy_version}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------
@dataclass
class PoolCandidate:
    condition_id: str
    subclass: str
    side_0_token: str
    side_1_token: str
    condition_reachability: str
    level_b_class: str
    # Approved local-trade density fields (spec 6.3 item 3). NOT CLOB point counts.
    local_trade_rows_in_window: int
    local_distinct_tx_hash_count_in_window: int
    window_seconds: int
    tie_break: str = ""

    @property
    def density_rank_value(self) -> Tuple[int, int]:
        """Primary density ordering key: local trade rows, then distinct tx count.
        Both derive from LOCAL TRADE ROWS only (never CLOB point counts)."""
        return (
            self.local_trade_rows_in_window,
            self.local_distinct_tx_hash_count_in_window,
        )


@dataclass
class CandidateReject:
    condition_id: str
    subclass: str
    reason: str


@dataclass
class SelectedCondition:
    condition_id: str
    subclass: str
    side_0_token: str
    side_1_token: str
    local_trade_rows_in_window: int
    local_distinct_tx_hash_count_in_window: int
    window_seconds: int
    density_band: str                  # LOW / MEDIUM / HIGH within the eligible set
    stratum_role: str                  # SUBCLASS_PRIMARY / SENTINEL
    tie_break: str
    density_source: str                # PRECOMPUTED_LOCAL_POOL_FILE / COMPUTED_FROM_LOCAL_TRADES
    per_condition_row_cap: int = PER_CONDITION_ROW_CAP_CEILING
    global_row_cap: int = GLOBAL_ROW_CAP_CEILING
    dune_query_limit_over_fetch: int = DUNE_QUERY_LIMIT_OVER_FETCH  # cap + 1


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------
def reject_outcome_conditioned_record(record: Dict[str, Any]) -> None:
    present = FORBIDDEN_INPUT_KEYS & {str(k) for k in record.keys()}
    if present:
        raise OutcomeConditionedInputError(
            f"{REJECT_OUTCOME_CONDITIONED_FIELD}: record for "
            f"{record.get('condition_id')!r} carries forbidden outcome/price/score "
            f"field(s): {sorted(present)}"
        )


def refuse_rejected_density_fields(field_names: Sequence[str], where: str) -> None:
    """Hard-refuse any S1 CLOB point-count / nearest-gap / non-local-trade density
    proxy used as a DENSITY input (Orchestrator BLOCK). Identity use of an S1 CSV
    is fine; density use of its CLOB columns is not."""
    present = REJECTED_DENSITY_FIELDS & {str(f) for f in field_names}
    if present:
        raise RejectedDensitySourceError(
            f"{FAIL_REJECTED_DENSITY_FIELD}: {where} supplies rejected density "
            f"field(s) {sorted(present)}. C1A-F1 density must come from local trade "
            f"rows only ({', '.join(APPROVED_DENSITY_FIELDS)}), never S1 CLOB "
            f"price-history point counts or nearest-gap diagnostics."
        )


def assert_pool_source_is_bounded(pool_path: str, allow_broader: bool = False) -> None:
    """Spec 6.2 / reject cond. 14, 15: refuse obviously universe-wide / profiling
    sources by filename unless the caller explicitly opts into a separately
    authorized broader local-only pool. Name/shape guard, not a data guard."""
    base = os.path.basename(pool_path).lower()
    banned_markers = ("universe", "all_conditions", "full_", "volume_profile", "profile_all", "288k")
    if not allow_broader and any(m in base for m in banned_markers):
        raise SelectorPolicyError(
            f"{FAIL_FORBIDDEN_POOL_SOURCE}: pool source {base!r} looks like a "
            f"full-universe / volume-profiling source. C1A-F1 must start from the "
            f"already-accepted small S1/S1-ALT bounded pool. Broader local-only "
            f"computation requires separate Orchestrator authorization and an "
            f"explicit allow_broader override, not a silent path swap."
        )


# ---------------------------------------------------------------------------
# Bounded-pool identity reader (defines the candidate condition SET + identity)
# ---------------------------------------------------------------------------
def read_bounded_pool_identity(pool_csv_path: str, allow_broader: bool = False) -> List[Dict[str, str]]:
    """Read the bounded pool CSV for identity/eligibility ONLY. Keeps just the
    ALLOWED_IDENTITY_COLUMNS - which deliberately EXCLUDE S1 CLOB point counts /
    nearest-gap columns, so those can never reach density logic from this path.

    Also hard-rejects a header carrying winner/price leakage. This function does
    NOT read or return any density field; density is supplied separately by an
    approved local-density source (precomputed-file path or local-trades path)."""
    assert_pool_source_is_bounded(pool_csv_path, allow_broader=allow_broader)
    rows: List[Dict[str, str]] = []
    with open(pool_csv_path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = set(reader.fieldnames or [])
        forbidden = FORBIDDEN_INPUT_KEYS & header
        if forbidden:
            raise OutcomeConditionedInputError(
                f"{REJECT_OUTCOME_CONDITIONED_FIELD}: pool CSV header carries "
                f"forbidden outcome/price field(s): {sorted(forbidden)}"
            )
        for raw in reader:
            rows.append({k: v for k, v in raw.items() if k in ALLOWED_IDENTITY_COLUMNS})
    return rows


# ---------------------------------------------------------------------------
# Approved density source A: a bounded PRECOMPUTED local-only pool file that
# ALREADY carries the approved local-trade density fields.
# ---------------------------------------------------------------------------
def read_precomputed_local_density(
    density_csv_path: str, allow_broader: bool = False
) -> Dict[str, Dict[str, int]]:
    """Read a bounded, precomputed LOCAL-ONLY density file keyed by condition_id.

    Required columns: condition_id + APPROVED_DENSITY_FIELDS. The file must NOT
    carry any REJECTED_DENSITY_FIELDS (S1 CLOB point counts etc.) - if it does,
    this refuses it, so a mislabeled S1 coverage CSV cannot sneak CLOB density in.
    Returns {condition_id: {approved_field: int}}.
    """
    assert_pool_source_is_bounded(density_csv_path, allow_broader=allow_broader)
    with open(density_csv_path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = list(reader.fieldnames or [])
        refuse_rejected_density_fields(header, where=f"precomputed density file {os.path.basename(density_csv_path)!r}")
        missing = set(APPROVED_DENSITY_FIELDS) - set(header)
        if "condition_id" not in header or missing:
            raise SelectorPolicyError(
                f"{REJECT_DENSITY_MISSING}: precomputed density file must contain "
                f"condition_id + {list(APPROVED_DENSITY_FIELDS)}; missing {sorted(missing)}"
            )
        out: Dict[str, Dict[str, int]] = {}
        for raw in reader:
            cid = str(raw.get("condition_id", "")).strip()
            try:
                out[cid] = {
                    "local_trade_rows_in_window": canonical_count(raw.get("local_trade_rows_in_window")),
                    "local_distinct_tx_hash_count_in_window": canonical_count(
                        raw.get("local_distinct_tx_hash_count_in_window")
                    ),
                    "window_seconds": canonical_count(raw.get("window_seconds")),
                }
            except DensityPrecisionError:
                out[cid] = {}  # marked unparseable; evaluate_candidate will reject
        return out


# ---------------------------------------------------------------------------
# Approved density source B: compute the approved fields from Store.load_trades()
# restricted ONLY to the bounded-pool condition IDs, inside a deterministic
# fixed window. Lazy pandas/Store import; Claude does not execute this path.
# ---------------------------------------------------------------------------
def compute_local_density_from_trades(
    root: str,
    condition_ids: Sequence[str],
    windows: Dict[str, Tuple[float, float]],
) -> Dict[str, Dict[str, int]]:
    """Compute approved local-trade density for a BOUNDED set of condition IDs.

    Hard scope (spec + reject cond. 14, 15):
      - Loads trades and immediately restricts to the bounded pool condition IDs.
        This is NOT a full ~288K-universe scan: only the small pool set is kept.
      - Counts local trade ROWS in the fixed window and DISTINCT local tx_hash in
        the same window; computes window_seconds. No CLOB point counts anywhere.
      - Does NOT persist any reusable profiling artifact; returns an in-memory dict
        for immediate selection only.

    Returns {condition_id: {approved_field: int}}. Lazy imports keep this module
    dependency-free for pure-logic tests; Claude does not execute this path.
    """
    from pm_research.data.store import Store  # lazy

    wanted = set(condition_ids)
    df = Store(root).load_trades()
    # Restrict to bounded pool FIRST - never profile the whole universe.
    df = df[df["condition_id"].isin(wanted)]

    out: Dict[str, Dict[str, int]] = {}
    for cid, grp in df.groupby("condition_id"):
        cid = str(cid)
        if cid not in windows:
            continue
        ws, we = windows[cid]
        rows_in_window = 0
        tx_hashes: set = set()
        for tx, ts in zip(grp["tx_hash"].astype(str), grp["traded_at"]):
            try:
                t = _parse_ts_epoch(ts)
            except ValueError:
                continue
            if ws <= t <= we:
                rows_in_window += 1
                tx_hashes.add(tx)
        out[cid] = {
            "local_trade_rows_in_window": rows_in_window,
            "local_distinct_tx_hash_count_in_window": len(tx_hashes),
            "window_seconds": int(round(we - ws)),
        }
    return out


def _parse_ts_epoch(value: Any) -> float:
    """Minimal epoch parser for traded_at values (datetime-like / epoch / ISO).
    Mirrors the accepted C1A parser's tolerance; kept local to avoid importing a
    non-package script."""
    from datetime import datetime, timezone

    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.timestamp()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    s = str(value).strip()
    if re.match(r"^[0-9]+(\.[0-9]+)?$", s):
        return float(s)
    norm = s
    if norm.endswith(" UTC"):
        norm = norm[:-4] + "+00:00"
    if norm.endswith("Z"):
        norm = norm[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(norm)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except ValueError:
        raise ValueError(f"unparseable traded_at: {value!r}")


# ---------------------------------------------------------------------------
# Eligibility (identity from pool row + density from an approved source)
# ---------------------------------------------------------------------------
def evaluate_candidate(
    identity_record: Dict[str, Any],
    density: Optional[Dict[str, int]],
    require_reachable_both: bool = True,
    prior_c1a_condition_ids: Optional[Sequence[str]] = None,
    policy_version: str = SELECTOR_POLICY_VERSION,
) -> Tuple[Optional[PoolCandidate], Optional[CandidateReject]]:
    """Build a PoolCandidate from an identity record + an APPROVED local-density
    dict, or a typed CandidateReject.

    `density` must carry ONLY approved local-trade fields (built by
    read_precomputed_local_density or compute_local_density_from_trades). If it
    carries a rejected S1 CLOB field, that is refused loudly (defense in depth).
    """
    reject_outcome_conditioned_record(identity_record)

    cid = str(identity_record.get("condition_id", "")).strip()
    subclass = str(identity_record.get("subclass", "")).strip()

    if not CONDITION_ID_RE.match(cid):
        return None, CandidateReject(cid, subclass, REJECT_CONDITION_ID_MALFORMED)
    if subclass not in ORIENTED_SUBCLASSES:
        return None, CandidateReject(cid, subclass, REJECT_SUBCLASS_NOT_ORIENTED)
    if prior_c1a_condition_ids and cid in set(prior_c1a_condition_ids):
        return None, CandidateReject(cid, subclass, REJECT_PRIOR_C1A_HOLDOUT)

    tok0 = str(identity_record.get("side_0_token", "")).strip()
    tok1 = str(identity_record.get("side_1_token", "")).strip()
    if not (is_string_safe_token(tok0) and is_string_safe_token(tok1)):
        if (tok0 and _SCI_RE.search(tok0)) or (tok1 and _SCI_RE.search(tok1)):
            return None, CandidateReject(cid, subclass, REJECT_TOKEN_PRECISION_LOSS)
        return None, CandidateReject(cid, subclass, REJECT_TOKEN_PAIR_NOT_TWO_STABLE)
    if tok0 == tok1:
        return None, CandidateReject(cid, subclass, REJECT_TOKEN_PAIR_NOT_TWO_STABLE)

    reachability = str(identity_record.get("condition_reachability", "")).strip().lower()
    if require_reachable_both and reachability != "both":
        return None, CandidateReject(cid, subclass, REJECT_NOT_REACHABLE_BOTH)

    # Density must be present and approved-only.
    if not density:
        return None, CandidateReject(cid, subclass, REJECT_DENSITY_MISSING)
    refuse_rejected_density_fields(density.keys(), where=f"density for {cid!r}")
    missing = set(APPROVED_DENSITY_FIELDS) - set(density.keys())
    if missing:
        return None, CandidateReject(cid, subclass, REJECT_DENSITY_MISSING)
    try:
        rows_w = canonical_count(density["local_trade_rows_in_window"])
        tx_w = canonical_count(density["local_distinct_tx_hash_count_in_window"])
        wsec = canonical_count(density["window_seconds"])
    except DensityPrecisionError:
        return None, CandidateReject(cid, subclass, REJECT_DENSITY_UNPARSEABLE)

    cand = PoolCandidate(
        condition_id=cid,
        subclass=subclass,
        side_0_token=tok0,
        side_1_token=tok1,
        condition_reachability=reachability,
        level_b_class=str(identity_record.get("level_b_class", "")).strip(),
        local_trade_rows_in_window=rows_w,
        local_distinct_tx_hash_count_in_window=tx_w,
        window_seconds=wsec,
        tie_break=tie_break_key(cid, policy_version),
    )
    return cand, None


# ---------------------------------------------------------------------------
# Density banding (spec 6.3 item 5 / 6.4) - WEAK proxy only, local-trade rows
# ---------------------------------------------------------------------------
def assign_density_bands(candidates: Sequence[PoolCandidate]) -> Dict[str, str]:
    """LOW / MEDIUM / HIGH tertile bands by local-TRADE-ROW density (then distinct
    tx, then tie_break). Ordinal within-pool only; NOT a predictor of Dune volume,
    NOT a ratio/threshold/cap/filter (spec 6.4)."""
    if not candidates:
        return {}
    ordered = sorted(candidates, key=lambda c: (c.density_rank_value, c.tie_break))
    n = len(ordered)
    bands: Dict[str, str] = {}
    for i, c in enumerate(ordered):
        frac = i / n
        if frac < 1.0 / 3.0:
            bands[c.condition_id] = "LOW"
        elif frac < 2.0 / 3.0:
            bands[c.condition_id] = "MEDIUM"
        else:
            bands[c.condition_id] = "HIGH"
    return bands


# ---------------------------------------------------------------------------
# Deterministic stratified selection (spec 6.3)
# ---------------------------------------------------------------------------
def select_conditions(
    candidates: Sequence[PoolCandidate],
    max_conditions: int = MAX_C1A_CONDITIONS,
    min_conditions: int = MIN_C1A_CONDITIONS,
    allow_sentinel: bool = True,
    density_source: str = "UNSPECIFIED",
    policy_version: str = SELECTOR_POLICY_VERSION,
) -> List[SelectedCondition]:
    if not (MIN_C1A_CONDITIONS <= min_conditions <= max_conditions <= MAX_C1A_CONDITIONS):
        raise SelectorPolicyError(
            f"{FAIL_COUNT_OUT_OF_RANGE}: require "
            f"{MIN_C1A_CONDITIONS} <= min({min_conditions}) <= max({max_conditions}) "
            f"<= {MAX_C1A_CONDITIONS}"
        )
    if not candidates:
        raise SelectorPolicyError(f"{FAIL_NO_ELIGIBLE_CANDIDATES}: empty eligible set")

    bands = assign_density_bands(candidates)

    def sort_key(c: PoolCandidate) -> Tuple[Tuple[int, int], str]:
        return (c.density_rank_value, c.tie_break)

    def to_selected(c: PoolCandidate, role: str) -> SelectedCondition:
        return SelectedCondition(
            condition_id=c.condition_id,
            subclass=c.subclass,
            side_0_token=c.side_0_token,
            side_1_token=c.side_1_token,
            local_trade_rows_in_window=c.local_trade_rows_in_window,
            local_distinct_tx_hash_count_in_window=c.local_distinct_tx_hash_count_in_window,
            window_seconds=c.window_seconds,
            density_band=bands[c.condition_id],
            stratum_role=role,
            tie_break=c.tie_break,
            density_source=density_source,
        )

    chosen: List[SelectedCondition] = []
    chosen_ids: set = set()

    # Step 2: one lowest-density primary per oriented subclass (fixed order).
    for subclass in ORIENTED_SUBCLASSES:
        in_sub = sorted((c for c in candidates if c.subclass == subclass), key=sort_key)
        if not in_sub or len(chosen) >= max_conditions:
            continue
        chosen.append(to_selected(in_sub[0], "SUBCLASS_PRIMARY"))
        chosen_ids.add(in_sub[0].condition_id)

    # Step 3: at most one MEDIUM sentinel if below min.
    if allow_sentinel and len(chosen) < min_conditions:
        medium = sorted(
            (c for c in candidates if c.condition_id not in chosen_ids and bands[c.condition_id] == "MEDIUM"),
            key=sort_key,
        )
        if medium:
            chosen.append(to_selected(medium[0], "SENTINEL"))
            chosen_ids.add(medium[0].condition_id)

    # Step 4: deterministic fill, lowest density first.
    if len(chosen) < min_conditions:
        for c in sorted((c for c in candidates if c.condition_id not in chosen_ids), key=sort_key):
            if len(chosen) >= max_conditions:
                break
            chosen.append(to_selected(c, "SUBCLASS_PRIMARY"))
            chosen_ids.add(c.condition_id)

    # Step 5: enforce hard 3-5 bound.
    if len(chosen) < min_conditions:
        raise SelectorPolicyError(
            f"{FAIL_POOL_TOO_SMALL}: only {len(chosen)} eligible condition(s) "
            f"selectable; need at least {min_conditions}. Do NOT relax caps, reuse "
            f"the exploding condition, or broaden the pool without separate "
            f"Orchestrator authorization."
        )
    if len(chosen) > max_conditions:
        chosen = chosen[:max_conditions]

    chosen.sort(key=lambda s: ((s.local_trade_rows_in_window, s.local_distinct_tx_hash_count_in_window), s.tie_break))
    return chosen


# ---------------------------------------------------------------------------
# Provenance (spec 6.2, 6.5) - NOT a query, NOT a run
# ---------------------------------------------------------------------------
def build_selector_provenance(
    selected: Sequence[SelectedCondition],
    rejected: Sequence[CandidateReject],
    pool_source_name: str,
    density_source: str,
    require_reachable_both: bool,
    prior_c1a_holdout_ids: Optional[Sequence[str]],
    policy_version: str = SELECTOR_POLICY_VERSION,
) -> Dict[str, Any]:
    return {
        "phase": PHASE,
        "authorized_scope": AUTHORIZED_SCOPE,
        "selector_policy_version": policy_version,
        "pool_source": os.path.basename(pool_source_name),
        "pool_source_is_bounded_accepted_pool": True,
        "scanned_full_universe": False,
        "built_reusable_volume_profile": False,
        "density_source": density_source,  # PRECOMPUTED_LOCAL_POOL_FILE / COMPUTED_FROM_LOCAL_TRADES
        "density_fields_used": list(APPROVED_DENSITY_FIELDS),
        "density_fields_rejected_and_never_used": sorted(REJECTED_DENSITY_FIELDS),
        "used_s1_clob_point_counts_as_density": False,
        "require_reachable_both": require_reachable_both,
        "prior_c1a_holdout_applied": bool(prior_c1a_holdout_ids),
        "prior_c1a_holdout_uniform_whole_manifest": bool(prior_c1a_holdout_ids),
        "selected_count": len(selected),
        "rejected_count": len(rejected),
        "min_conditions": MIN_C1A_CONDITIONS,
        "max_conditions": MAX_C1A_CONDITIONS,
        "per_condition_row_cap_ceiling": PER_CONDITION_ROW_CAP_CEILING,
        "global_row_cap_ceiling": GLOBAL_ROW_CAP_CEILING,
        "dune_query_limit_over_fetch_cap_plus_one": DUNE_QUERY_LIMIT_OVER_FETCH,
        "caps_raised": False,
        "used_dune_count_scout": False,
        "used_local_tx_hash_filter": False,
        "used_winner_or_outcome_field": False,
        "used_price_or_score_field": False,
        "used_ordersmatched_or_wallet_or_pnl": False,
        "deterministic_tie_breaker": "sha256(condition_id|selector_policy_version)",
        "selected": [asdict(s) for s in selected],
        "rejected": [asdict(r) for r in rejected],
        "no_run_authorized": True,
    }


# ---------------------------------------------------------------------------
# Orchestration (pure, over already-read identity rows + approved density map)
# ---------------------------------------------------------------------------
def run_selector(
    identity_rows: Sequence[Dict[str, Any]],
    density_by_condition: Dict[str, Dict[str, int]],
    density_source: str,
    pool_source_name: str = "bounded_pool",
    max_conditions: int = MAX_C1A_CONDITIONS,
    min_conditions: int = MIN_C1A_CONDITIONS,
    require_reachable_both: bool = True,
    prior_c1a_holdout_ids: Optional[Sequence[str]] = None,
    allow_sentinel: bool = True,
    policy_version: str = SELECTOR_POLICY_VERSION,
) -> Tuple[List[SelectedCondition], List[CandidateReject], Dict[str, Any]]:
    if density_source not in ("PRECOMPUTED_LOCAL_POOL_FILE", "COMPUTED_FROM_LOCAL_TRADES"):
        raise SelectorPolicyError(
            f"density_source must be an approved local-trade source, got {density_source!r}"
        )
    candidates: List[PoolCandidate] = []
    rejected: List[CandidateReject] = []
    for record in identity_rows:
        cid = str(record.get("condition_id", "")).strip()
        cand, rej = evaluate_candidate(
            record,
            density=density_by_condition.get(cid),
            require_reachable_both=require_reachable_both,
            prior_c1a_condition_ids=prior_c1a_holdout_ids,
            policy_version=policy_version,
        )
        if cand is not None:
            candidates.append(cand)
        elif rej is not None:
            rejected.append(rej)

    selected = select_conditions(
        candidates,
        max_conditions=max_conditions,
        min_conditions=min_conditions,
        allow_sentinel=allow_sentinel,
        density_source=density_source,
        policy_version=policy_version,
    )
    provenance = build_selector_provenance(
        selected, rejected, pool_source_name, density_source,
        require_reachable_both, prior_c1a_holdout_ids, policy_version,
    )
    return selected, rejected, provenance


# ---------------------------------------------------------------------------
# Output writer
# ---------------------------------------------------------------------------
def write_selector_outputs(
    out_dir: str,
    selected: Sequence[SelectedCondition],
    rejected: Sequence[CandidateReject],
    provenance: Dict[str, Any],
) -> None:
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "c1a_f1_selector_provenance.json"), "w", encoding="utf-8") as fh:
        json.dump(provenance, fh, indent=2, sort_keys=True)
    with open(os.path.join(out_dir, "c1a_f1_selected_conditions.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([
            "condition_id", "subclass", "side_0_token", "side_1_token",
            "local_trade_rows_in_window", "local_distinct_tx_hash_count_in_window",
            "window_seconds", "density_band", "stratum_role", "tie_break",
            "density_source", "per_condition_row_cap", "global_row_cap",
            "dune_query_limit_over_fetch",
        ])
        for s in selected:
            w.writerow([
                s.condition_id, s.subclass, s.side_0_token, s.side_1_token,
                s.local_trade_rows_in_window, s.local_distinct_tx_hash_count_in_window,
                s.window_seconds, s.density_band, s.stratum_role, s.tie_break,
                s.density_source, s.per_condition_row_cap, s.global_row_cap,
                s.dune_query_limit_over_fetch,
            ])
    with open(os.path.join(out_dir, "c1a_f1_selector_excluded.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["condition_id", "subclass", "reason"])
        for r in rejected:
            w.writerow([r.condition_id, r.subclass, r.reason])


# ---------------------------------------------------------------------------
# CLI (user-run, local-only; Claude does not execute this path)
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "C1A-F1 deterministic selector policy (CODE/TEST ONLY, local-only, no "
            "network, no run). Ranks by APPROVED local-trade density only "
            "(local_trade_rows_in_window / local_distinct_tx_hash_count_in_window / "
            "window_seconds) - never S1 CLOB point counts."
        )
    )
    p.add_argument("--pool-csv", required=True,
                   help="Bounded pool CSV for candidate identity/eligibility (small S1/S1-ALT pool).")
    p.add_argument("--density-mode", choices=("precomputed", "local-trades"), required=True,
                   help="'precomputed': read approved density from --density-csv; "
                        "'local-trades': compute from Store.load_trades() restricted to the bounded pool.")
    p.add_argument("--density-csv", default="",
                   help="Precomputed local-only density CSV (condition_id + approved density fields). "
                        "Required when --density-mode precomputed.")
    p.add_argument("--root", default="", help="Data root for Store.load_trades() (local-trades mode).")
    p.add_argument("--windows-json", default="",
                   help="JSON {condition_id: [window_start_epoch, window_end_epoch]} for local-trades mode.")
    p.add_argument("--out-dir", default=os.path.join("artifacts", "named_binary_probe", "price_source_option_c_c1a_f1"))
    p.add_argument("--max-conditions", type=int, default=MAX_C1A_CONDITIONS)
    p.add_argument("--min-conditions", type=int, default=MIN_C1A_CONDITIONS)
    p.add_argument("--no-require-reachable-both", action="store_true")
    p.add_argument("--prior-c1a-holdout", default="",
                   help="Comma-separated prior C1A condition_ids to exclude UNIFORMLY (whole manifest).")
    p.add_argument("--no-sentinel", action="store_true")
    p.add_argument("--allow-broader-pool", action="store_true",
                   help="Opt-in for a separately authorized broader local-only pool (not default).")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:  # pragma: no cover
    args = build_arg_parser().parse_args(argv)
    holdout = [c.strip() for c in args.prior_c1a_holdout.split(",") if c.strip()]

    identity_rows = read_bounded_pool_identity(args.pool_csv, allow_broader=args.allow_broader_pool)

    if args.density_mode == "precomputed":
        if not args.density_csv:
            raise SystemExit("--density-csv is required when --density-mode precomputed")
        density_by_condition = read_precomputed_local_density(args.density_csv, allow_broader=args.allow_broader_pool)
        density_source = "PRECOMPUTED_LOCAL_POOL_FILE"
    else:
        if not (args.root and args.windows_json):
            raise SystemExit("--root and --windows-json are required when --density-mode local-trades")
        with open(args.windows_json, "r", encoding="utf-8") as fh:
            raw_windows = json.load(fh)
        windows = {str(k): (float(v[0]), float(v[1])) for k, v in raw_windows.items()}
        cids = [str(r.get("condition_id", "")).strip() for r in identity_rows]
        density_by_condition = compute_local_density_from_trades(args.root, cids, windows)
        density_source = "COMPUTED_FROM_LOCAL_TRADES"

    selected, rejected, provenance = run_selector(
        identity_rows,
        density_by_condition,
        density_source=density_source,
        pool_source_name=args.pool_csv,
        max_conditions=args.max_conditions,
        min_conditions=args.min_conditions,
        require_reachable_both=not args.no_require_reachable_both,
        prior_c1a_holdout_ids=holdout or None,
        allow_sentinel=not args.no_sentinel,
    )
    write_selector_outputs(args.out_dir, selected, rejected, provenance)
    print(
        f"[{PHASE}] selected={len(selected)} rejected={len(rejected)} "
        f"density_source={density_source} policy={SELECTOR_POLICY_VERSION} (NO RUN AUTHORIZED)"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
