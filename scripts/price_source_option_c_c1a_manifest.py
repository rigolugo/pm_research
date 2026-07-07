"""Option C, C1A - fixed selector manifest builder.

CODE / TEST ONLY. No network call. No Dune call. No live query execution.

Governing specs:
- project_context/SPEC_price_source_option_c_onchain.md (Revision 3, C0 accepted /
  C1 guardrail block record)
- project_context/SPEC_price_source_option_c_onchain_C1R_addendum.md (Patch 1,
  selector-manifest design, section 4)

Authorization: this file builds and validates a fixed C1A selector manifest from
LOCAL data only (the project's own `trades` store + the already-accepted
named-binary contract/resolution-source artifacts). It performs NO Dune query, NO
API call, NO RPC call. Its only output is a manifest file plus a Dune SQL query
TEXT for the user to paste into Dune manually, per the documented flow in
project_context/DUNE_DATA_NOTES.md section 7. Claude does not execute this path.

What this file IS:
  - A validator/builder that takes a small (3-5), user-supplied, fixed candidate
    condition list (with fixed decision-time windows and fixed row-cap requests,
    all chosen in advance - never selected dynamically here) and resolves each
    condition's two side token_ids from LOCAL trades only, using the same
    outcome-independent enumeration discipline already accepted for S1
    (`SPEC_price_source_s1_coverage.md` section 3.1): distinct local
    `(condition_id, token_id, outcome_index)` tuples, exactly two stable
    string-safe tokens required, `resolved_winning_token_id` never read.

What this file is NOT (hard non-goals, enforced):
  - No Dune/API/RPC call. No CSV fetch. Fetching is a separate, user-run step.
  - No price, no `canonical_side_price`, no target, no score, no probe feature.
  - No dynamic condition/token selection: only validates a fixed input list.
  - `resolved_winning_token_id` is NEVER read by this module at all - not even
    for cross-checking - because token-pair *selection* is the exact operation
    the addendum forbids that field from touching (C1R addendum section 4.1).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Pinned constants
# ---------------------------------------------------------------------------
PHASE = "OPTION_C_C1A_SELECTOR_MANIFEST"
AUTHORIZED_SCOPE = "OPTION_C_C1A_MANIFEST_BUILD_ONLY_NO_NETWORK"
NB_CONTRACT_VERSION = "nb-contract-2026-06-28.1"

ORIENTED_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")  # no YES_NO, no UNUSABLE

MIN_C1A_CONDITIONS = 3
MAX_C1A_CONDITIONS = 5

# Absolute C1R-level cap ceilings (C1R addendum section 7.1). A manifest request
# may specify equal-or-lower caps; it may never exceed these without a fresh
# addendum revision.
PER_CONDITION_ROW_CAP_CEILING = 2000
GLOBAL_ROW_CAP_CEILING = 6000

CONDITION_ID_RE = re.compile(r"^0x[0-9a-f]{64}$")
_SCI_RE = re.compile(r"[eE]")
_INT_RE = re.compile(r"^[0-9]+$")

# Strict identifier check for source_table_version: lowercase dotted identifier
# (schema.table), 2-3 segments, no quotes/semicolons/whitespace/comments -
# defense against rendering an arbitrary/unsafe string into SQL text (patch
# requirement: "do not render arbitrary strings into SQL").
SOURCE_TABLE_VERSION_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){1,2}$")

# Small allowlist, not just a format check: only the two decoded OrderFilled
# tables named in DUNE_DATA_NOTES.md section 3 are in scope for C1A. This also
# structurally keeps C1A from ever touching OrdersMatched tables.
ALLOWED_SOURCE_TABLES = frozenset(
    {
        "polymarket_polygon.ctfexchange_evt_orderfilled",
        "polymarket_polygon.negriskctfexchange_evt_orderfilled",
    }
)

# ---------------------------------------------------------------------------
# Typed stop / status codes (C1R addendum section 9)
# ---------------------------------------------------------------------------
STOP_CANDIDATE_COUNT_OUT_OF_RANGE = "STOP_CANDIDATE_COUNT_OUT_OF_RANGE"
STOP_SUBCLASS_NOT_ORIENTED = "STOP_SUBCLASS_NOT_ORIENTED"
STOP_STATUS_NOT_SINGLE_WINNER = "STOP_STATUS_NOT_SINGLE_WINNER"
STOP_ROW_CAP_CEILING_EXCEEDED = "STOP_ROW_CAP_CEILING_EXCEEDED"
STOP_MANIFEST_FIELD_MISSING = "STOP_MANIFEST_FIELD_MISSING"
STOP_STALE_CONTRACT = "STOP_STALE_CONTRACT"
STOP_SOURCE_TABLE_VERSION_INVALID = "STOP_SOURCE_TABLE_VERSION_INVALID"

C1_SELECTOR_TOKEN_PAIR_UNRESOLVED = "C1_SELECTOR_TOKEN_PAIR_UNRESOLVED"
C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO = "C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO"
C1_SELECTOR_TOKEN_PRECISION_LOSS = "C1_SELECTOR_TOKEN_PRECISION_LOSS"
C1_SELECTOR_USES_WINNER_TOKEN_ONLY = "C1_SELECTOR_USES_WINNER_TOKEN_ONLY"
C1_SELECTOR_OUTCOME_CONDITIONED = "C1_SELECTOR_OUTCOME_CONDITIONED"

MANIFEST_OK = "OK"

REQUIRED_INPUT_FIELDS = (
    "condition_id",
    "window_start_utc",
    "window_end_utc",
    "source_table_version",
)
# Forbidden input keys: if a caller's candidate record carries any of these, the
# input itself is treated as outcome-conditioned/winner-sourced and rejected -
# defense in depth on top of this module simply never reading such a field.
FORBIDDEN_INPUT_KEYS = {
    "resolved_winning_token_id",
    "resolved_winning_outcome_index",
    "resolved_winning_label",
    "winner_token_id",
    "winning_token_id",
}


class DataExportPrecisionLoss(ValueError):
    """Fail-loud on scientific notation / float-mangled token ids (never a soft
    TOKEN_PAIR_UNRESOLVED - precision loss is a distinct, harder failure)."""


class OutcomeConditionedInputError(ValueError):
    """Raised if a candidate record carries any outcome/winner-sourced field.
    Token-pair selection must never depend on which side won (C1R addendum 4.1)."""


# ---------------------------------------------------------------------------
# Precision-safe integer canonicalization (mirrors the accepted S1 helper,
# `scripts/price_source_s1_coverage.py::canonical_int` - not imported directly
# because scripts/ is not a package; kept self-contained on purpose, same as
# every other script in this project).
# ---------------------------------------------------------------------------
def canonical_int(value: Any) -> int:
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


def parse_ts_utc(value: Any) -> float:
    """Parse a fixed window bound to epoch seconds. Accepts epoch numbers or
    ISO-8601 / 'YYYY-MM-DD HH:MM:SS[ UTC]' strings. Fails loud otherwise."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    s = str(value).strip()
    if re.match(r"^[0-9]+(\.[0-9]+)?$", s):
        return float(s)
    s2 = s.replace(" UTC", "").replace("Z", "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s2, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            continue
    raise ValueError(f"unparseable window bound: {value!r}")


# ---------------------------------------------------------------------------
# Token-pair enumeration from LOCAL trades only (mirrors accepted S1 section 3.1
# discipline exactly - never from winners).
# ---------------------------------------------------------------------------
def enumerate_token_pair(
    trade_tuples: Sequence[Tuple[str, Any, Any]],
) -> Tuple[Optional[str], Optional[str], str]:
    """Given distinct (condition_id, token_id, outcome_index) tuples for ONE
    condition from LOCAL trades, return (side_0_token, side_1_token, status).

    status is one of: MANIFEST_OK, C1_SELECTOR_TOKEN_PAIR_UNRESOLVED (no
    qualifying data), C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO (data present but
    the token count per side is not exactly one-and-one, or the two sides
    collapse to the same token).

    Raises DataExportPrecisionLoss on scientific-notation / float-mangled ids -
    precision loss is never silently downgraded to a soft unresolved status.
    """
    if not trade_tuples:
        return None, None, C1_SELECTOR_TOKEN_PAIR_UNRESOLVED

    by_index: Dict[int, set] = {}
    for _cid, token_id, outcome_index in trade_tuples:
        if token_id is None or outcome_index is None:
            return None, None, C1_SELECTOR_TOKEN_PAIR_UNRESOLVED
        _ = canonical_int(token_id)  # precision discipline first; raises on sci-notation
        idx = canonical_int(outcome_index)
        if idx not in (0, 1):
            return None, None, C1_SELECTOR_TOKEN_PAIR_UNRESOLVED
        by_index.setdefault(idx, set()).add(str(token_id).strip())

    if set(by_index.keys()) != {0, 1}:
        return None, None, C1_SELECTOR_TOKEN_PAIR_UNRESOLVED
    if len(by_index[0]) != 1 or len(by_index[1]) != 1:
        return None, None, C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO

    s0 = next(iter(by_index[0]))
    s1 = next(iter(by_index[1]))
    if canonical_int(s0) == canonical_int(s1):
        return None, None, C1_SELECTOR_TOKEN_PAIR_NOT_EXACTLY_TWO
    return s0, s1, MANIFEST_OK


# ---------------------------------------------------------------------------
# Manifest row
# ---------------------------------------------------------------------------
@dataclass
class ManifestRow:
    condition_id: str
    nb_subclass: Optional[str] = None
    side_0_token_id: Optional[str] = None
    side_1_token_id: Optional[str] = None
    outcome_index_0: str = "0"
    outcome_index_1: str = "1"
    window_start_utc: str = ""
    window_end_utc: str = ""
    decision_time_basis: str = "fixed_manifest_window"
    per_condition_row_cap: int = PER_CONDITION_ROW_CAP_CEILING
    global_row_cap: int = GLOBAL_ROW_CAP_CEILING
    # The Dune query's LIMIT is intentionally per_condition_row_cap + 1, never
    # the cap itself - an exact-cap LIMIT would silently truncate at the cap
    # and make row-explosion undetectable (patch requirement 1). This field
    # records the actual rendered LIMIT for provenance/audit; the TRUE cap
    # enforced by the canary script's client-side check is always
    # per_condition_row_cap, never this value.
    dune_query_limit: int = PER_CONDITION_ROW_CAP_CEILING + 1
    selector_source: str = "local_trades_distinct_condition_token_outcome_index"
    source_table_version: str = ""
    token_pair_validation_status: str = "PENDING"


def reject_outcome_conditioned_input(candidate: Dict[str, Any]) -> None:
    """Structural guard: a candidate condition record must never carry an
    outcome/winner-sourced field. This is checked even though this module's
    own code paths never read such a field, as defense in depth against a
    caller wiring one in by mistake (C1_SELECTOR_OUTCOME_CONDITIONED /
    C1_SELECTOR_USES_WINNER_TOKEN_ONLY)."""
    present = FORBIDDEN_INPUT_KEYS & set(candidate.keys())
    if present:
        raise OutcomeConditionedInputError(
            f"{C1_SELECTOR_USES_WINNER_TOKEN_ONLY} / {C1_SELECTOR_OUTCOME_CONDITIONED}: "
            f"candidate for {candidate.get('condition_id')!r} carries forbidden "
            f"outcome-sourced field(s): {sorted(present)}"
        )


def validate_source_table_version(value: Any) -> str:
    """Strict, allowlisted source table identifier. Never render an unvalidated
    string into SQL text (patch requirement). Returns the validated string."""
    s = str(value).strip()
    if not SOURCE_TABLE_VERSION_RE.match(s):
        raise ValueError(f"{STOP_SOURCE_TABLE_VERSION_INVALID}: bad format {value!r}")
    if s not in ALLOWED_SOURCE_TABLES:
        raise ValueError(
            f"{STOP_SOURCE_TABLE_VERSION_INVALID}: {value!r} not in allowlist {sorted(ALLOWED_SOURCE_TABLES)}"
        )
    return s


def validate_candidate_list(candidates: Sequence[Dict[str, Any]]) -> None:
    n = len(candidates)
    if not (MIN_C1A_CONDITIONS <= n <= MAX_C1A_CONDITIONS):
        raise ValueError(
            f"{STOP_CANDIDATE_COUNT_OUT_OF_RANGE}: got {n} candidates, "
            f"required {MIN_C1A_CONDITIONS}-{MAX_C1A_CONDITIONS}"
        )
    seen = set()
    for c in candidates:
        reject_outcome_conditioned_input(c)
        missing = [f for f in REQUIRED_INPUT_FIELDS if not c.get(f)]
        if missing:
            raise ValueError(f"{STOP_MANIFEST_FIELD_MISSING}: {c.get('condition_id')!r} missing {missing}")
        cid = c["condition_id"]
        if not CONDITION_ID_RE.match(str(cid)):
            raise ValueError(f"{STOP_MANIFEST_FIELD_MISSING}: bad condition_id format {cid!r}")
        if cid in seen:
            raise ValueError(f"{STOP_MANIFEST_FIELD_MISSING}: duplicate condition_id {cid!r} in candidate list")
        seen.add(cid)
        # Never render an unvalidated source_table_version string into SQL.
        validate_source_table_version(c["source_table_version"])
        # Window sanity: parseable and start < end.
        ws = parse_ts_utc(c["window_start_utc"])
        we = parse_ts_utc(c["window_end_utc"])
        if not (ws < we):
            raise ValueError(
                f"{STOP_MANIFEST_FIELD_MISSING}: window_start_utc must precede "
                f"window_end_utc for {cid!r}"
            )
        pcap = int(c.get("per_condition_row_cap", PER_CONDITION_ROW_CAP_CEILING))
        gcap = int(c.get("global_row_cap", GLOBAL_ROW_CAP_CEILING))
        if pcap > PER_CONDITION_ROW_CAP_CEILING:
            raise ValueError(
                f"{STOP_ROW_CAP_CEILING_EXCEEDED}: per_condition_row_cap {pcap} > "
                f"ceiling {PER_CONDITION_ROW_CAP_CEILING} for {cid!r}"
            )
        if gcap > GLOBAL_ROW_CAP_CEILING:
            raise ValueError(
                f"{STOP_ROW_CAP_CEILING_EXCEEDED}: global_row_cap {gcap} > "
                f"ceiling {GLOBAL_ROW_CAP_CEILING} for {cid!r}"
            )


def validate_subclass_and_status(
    condition_id: str,
    contract_map: Dict[str, str],
    resolution_status: Dict[str, str],
) -> str:
    """Subclass/status cross-check ONLY - never reads winner token. Mirrors the
    accepted S1 `build_universe` join, restricted to the fields it actually
    needs (subclass gating + single-winner status), same non-goal as S1: the
    resolution row's `resolved_winning_token_id` is never touched here."""
    sub = contract_map.get(condition_id)
    if sub not in ORIENTED_SUBCLASSES:
        raise ValueError(f"{STOP_SUBCLASS_NOT_ORIENTED}: {condition_id!r} subclass={sub!r}")
    status = resolution_status.get(condition_id)
    if status != "RESOLVED_SINGLE_WINNER":
        raise ValueError(f"{STOP_STATUS_NOT_SINGLE_WINNER}: {condition_id!r} status={status!r}")
    return sub


def build_manifest(
    candidates: Sequence[Dict[str, Any]],
    contract_map: Dict[str, str],
    resolution_status: Dict[str, str],
    trades_by_condition: Dict[str, Sequence[Tuple[str, Any, Any]]],
) -> Tuple[List[ManifestRow], List[ManifestRow]]:
    """Pure-logic manifest build. Returns (resolved_rows, excluded_rows).

    `trades_by_condition` must already be scoped to LOCAL trades within each
    condition's fixed window by the caller (see StoreLoader below for the real,
    lazy-imported path) - this function does no I/O itself.
    """
    validate_candidate_list(candidates)

    resolved: List[ManifestRow] = []
    excluded: List[ManifestRow] = []

    for c in candidates:
        cid = c["condition_id"]
        pcap = int(c.get("per_condition_row_cap", PER_CONDITION_ROW_CAP_CEILING))
        row = ManifestRow(
            condition_id=cid,
            window_start_utc=str(c["window_start_utc"]),
            window_end_utc=str(c["window_end_utc"]),
            per_condition_row_cap=pcap,
            global_row_cap=int(c.get("global_row_cap", GLOBAL_ROW_CAP_CEILING)),
            dune_query_limit=pcap + 1,
            source_table_version=str(c.get("source_table_version", "")),
        )
        try:
            sub = validate_subclass_and_status(cid, contract_map, resolution_status)
            row.nb_subclass = sub
        except ValueError as exc:
            row.token_pair_validation_status = str(exc).split(":")[0]
            excluded.append(row)
            continue

        tuples = trades_by_condition.get(cid, [])
        try:
            s0, s1, status = enumerate_token_pair(tuples)
        except DataExportPrecisionLoss as exc:
            row.token_pair_validation_status = C1_SELECTOR_TOKEN_PRECISION_LOSS
            excluded.append(row)
            continue

        row.side_0_token_id = s0
        row.side_1_token_id = s1
        row.token_pair_validation_status = status
        (resolved if status == MANIFEST_OK else excluded).append(row)

    if len(resolved) < MIN_C1A_CONDITIONS:
        raise ValueError(
            f"{STOP_CANDIDATE_COUNT_OUT_OF_RANGE}: only {len(resolved)} condition(s) "
            f"resolved a valid token pair (need >= {MIN_C1A_CONDITIONS}); see excluded rows"
        )
    return resolved, excluded


# ---------------------------------------------------------------------------
# Dune query text generation (TEXT ONLY - never executed here)
# ---------------------------------------------------------------------------
def render_dune_query(rows: Sequence[ManifestRow]) -> str:
    """Render the fixed, bounded Dune SQL text implied by the manifest. This is
    TEXT ONLY: it is not sent anywhere by this module. The user pastes it into
    the Dune query editor manually, runs it, and fetches the CSV per the
    documented flow (project_context/DUNE_DATA_NOTES.md section 7).

    The LIMIT rendered here is deliberately per_condition_row_cap + 1
    (`dune_query_limit`), never the cap itself. A LIMIT set to exactly the cap
    would silently truncate at the cap and make row-explosion undetectable -
    the canary script could never tell "exactly N rows exist" apart from
    "more than N rows exist but Dune only gave us N." Over-fetching by one lets
    the canary's client-side check prove the cap was not exceeded rather than
    merely hiding any excess (patch requirement 1).

    Each per-condition block is wrapped as `select * from ( ... limit N )`
    before being combined with UNION ALL. A bare `limit N` attached directly to
    a branch of a UNION ALL is not reliably scoped to that branch alone in
    Trino/Presto (Dune's engine) - it can bind to the union's overall result
    instead of the individual branch, which would silently defeat the
    per-condition over-fetch bound this query depends on. Wrapping each branch
    in its own subquery makes the LIMIT unambiguously apply to that condition
    only (second BLOCK fix)."""
    global_cap = min((r.global_row_cap for r in rows), default=GLOBAL_ROW_CAP_CEILING)
    lines: List[str] = []
    lines.append("-- C1A bounded canary query - GENERATED TEXT, paste into Dune manually.")
    lines.append("-- Source table/version must match each condition's source_table_version below.")
    lines.append("-- One UNION ALL block per fixed condition; every predicate is fixed at manifest time.")
    lines.append("-- LIMIT is per_condition_row_cap + 1 (over-fetch by one), NOT the cap itself - this")
    lines.append("-- lets the canary script prove the cap was not exceeded instead of silently hiding it.")
    lines.append("-- Each condition's LIMIT is scoped by wrapping it in its own subquery ('select * from")
    lines.append("-- (... limit N)') so it cannot bind to the union's overall result instead of just")
    lines.append("-- this condition's branch.")
    lines.append("")
    per_condition_sql = []
    for r in rows:
        # Defense in depth: re-validate even though validate_candidate_list
        # already checked this at manifest-build time - a manifest JSON file
        # could in principle be hand-edited between build and render.
        safe_table = validate_source_table_version(r.source_table_version)
        inner_select = (
            "  select\n"
            "    '{cid}' as condition_id,\n"
            "    cast(evt_tx_hash as varchar) as tx_hash,\n"
            "    evt_block_time as block_time,\n"
            "    cast(makerassetid as varchar) as makerAssetId,\n"
            "    cast(takerassetid as varchar) as takerAssetId,\n"
            "    cast(makeramountfilled as varchar) as makerAmountFilled,\n"
            "    cast(takeramountfilled as varchar) as takerAmountFilled,\n"
            "    '{source_table_version}' as source_provenance\n"
            "  from {source_table_version}\n"
            "  where evt_block_time between timestamp '{ws}' and timestamp '{we}'\n"
            "    and (\n"
            "      cast(makerassetid as varchar) in ('{t0}', '{t1}')\n"
            "      or cast(takerassetid as varchar) in ('{t0}', '{t1}')\n"
            "    )\n"
            "  limit {limit}"
        ).format(
            cid=r.condition_id,
            source_table_version=safe_table,
            ws=datetime.fromtimestamp(parse_ts_utc(r.window_start_utc), tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            we=datetime.fromtimestamp(parse_ts_utc(r.window_end_utc), tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            t0=r.side_0_token_id,
            t1=r.side_1_token_id,
            limit=r.dune_query_limit,
        )
        block_sql = "select * from (\n{inner}\n)".format(inner=inner_select)
        per_condition_sql.append(block_sql)
    lines.append("\nunion all\n\n".join(per_condition_sql))
    lines.append("")
    lines.append(f"-- Global row cap ceiling for this manifest: {global_cap} (enforced client-side")
    lines.append("-- by the C1A canary script after CSV export, via a running global count against")
    lines.append("-- global_row_cap - Dune's per-block LIMIT above is the per-condition over-fetch")
    lines.append("-- bound only, not a substitute for the global check.)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Lazy, real-data loader (Claude does not execute this path)
# ---------------------------------------------------------------------------
class StoreLoader:
    """Real loader. Imports (pandas / Store / json) are LAZY so this module has
    no hard dependency and pure-logic tests can import it in a bare environment.
    Claude does not execute this path - it is a user-run task on the local
    Windows/Miniconda box, same discipline as every prior price-source script
    in this project."""

    def __init__(self, root: str, artifacts_dir: str):
        self.root = root
        self.artifacts_dir = artifacts_dir

    def _art(self, *parts: str) -> str:
        return os.path.join(self.artifacts_dir, *parts)

    def load_contract_map(self) -> Dict[str, str]:
        path = self._art("named_binary", "named_binary_classification_contract.json")
        with open(path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        out: Dict[str, str] = {}
        for rec in doc.get("conditions", []):
            if rec.get("nb_contract_version") != NB_CONTRACT_VERSION:
                raise ValueError(STOP_STALE_CONTRACT)
            if str(rec.get("nb_eligible")) != "True":
                continue
            out[rec["condition_id"]] = rec.get("nb_subclass")
        return out

    def load_resolution_status(self) -> Dict[str, str]:
        import pandas as pd  # lazy

        path = self._art("named_binary", "named_binary_resolution_source_rows.parquet")
        df = pd.read_parquet(path).astype(str)
        # Only condition_id + status are read here - resolved_winning_token_id
        # exists in this parquet but is never selected/returned by this method.
        return dict(zip(df["condition_id"], df["status"]))

    def load_trades_for_conditions(
        self, condition_ids: Sequence[str], windows: Dict[str, Tuple[float, float]]
    ) -> Dict[str, List[Tuple[str, str, str]]]:
        from pm_research.data.store import Store  # lazy

        wanted = set(condition_ids)
        df = Store(self.root).load_trades()
        df = df[df["condition_id"].isin(wanted)]
        out: Dict[str, List[Tuple[str, str, str]]] = {}
        for cid, grp in df.groupby("condition_id"):
            cid = str(cid)
            if cid not in windows:
                continue
            ws, we = windows[cid]
            # Token-pair enumeration is scoped to each condition's OWN fixed
            # window, consistent with the manifest being a fixed, pre-named
            # window per condition rather than "all local trades ever."
            rows = []
            for tok, oi, ts in zip(
                grp["token_id"].astype(str), grp["outcome_index"].astype(str), grp["traded_at"]
            ):
                try:
                    t = parse_ts_utc(ts)
                except ValueError:
                    continue
                if ws <= t <= we:
                    rows.append((cid, tok, oi))
            out[cid] = rows
        return out


# ---------------------------------------------------------------------------
# Output writers (persist-before-halt discipline)
# ---------------------------------------------------------------------------
def write_manifest_outputs(
    out_dir: str,
    resolved: Sequence[ManifestRow],
    excluded: Sequence[ManifestRow],
) -> None:
    os.makedirs(out_dir, exist_ok=True)
    manifest_json = {
        "phase": PHASE,
        "authorized_scope": AUTHORIZED_SCOPE,
        "resolved_count": len(resolved),
        "excluded_count": len(excluded),
        "conditions": [asdict(r) for r in resolved],
    }
    with open(os.path.join(out_dir, "c1a_selector_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest_json, fh, indent=2)

    fieldnames = list(asdict(resolved[0]).keys()) if resolved else list(ManifestRow.__annotations__.keys())
    with open(os.path.join(out_dir, "c1a_selector_manifest.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in resolved:
            w.writerow(asdict(r))

    with open(os.path.join(out_dir, "c1a_selector_excluded.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in excluded:
            w.writerow(asdict(r))

    if resolved:
        with open(os.path.join(out_dir, "c1a_dune_query.sql"), "w", encoding="utf-8") as fh:
            fh.write(render_dune_query(resolved))


# ---------------------------------------------------------------------------
# CLI (real run is a user-run task; Claude does not invoke this)
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build and validate the fixed C1A selector manifest from local data only. "
        "No network. No Dune call. Real execution is a user-run task."
    )
    p.add_argument("--root", default=r"C:\b1\data", help="Local data store root (trades).")
    p.add_argument("--artifacts-dir", default="artifacts", help="Local artifacts root.")
    p.add_argument(
        "--candidates",
        required=True,
        help="Path to a JSON file: a fixed list of 3-5 candidate conditions, each with "
        "condition_id, window_start_utc, window_end_utc, and optional "
        "per_condition_row_cap/global_row_cap/source_table_version overrides.",
    )
    p.add_argument("--out-dir", default=os.path.join("artifacts", "named_binary_probe", "price_source_option_c_c1a"))
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    with open(args.candidates, "r", encoding="utf-8") as fh:
        candidates = json.load(fh)

    loader = StoreLoader(args.root, args.artifacts_dir)
    contract_map = loader.load_contract_map()
    resolution_status = loader.load_resolution_status()

    windows = {
        c["condition_id"]: (parse_ts_utc(c["window_start_utc"]), parse_ts_utc(c["window_end_utc"]))
        for c in candidates
    }
    trades_by_condition = loader.load_trades_for_conditions(
        [c["condition_id"] for c in candidates], windows
    )

    resolved, excluded = build_manifest(candidates, contract_map, resolution_status, trades_by_condition)
    write_manifest_outputs(args.out_dir, resolved, excluded)
    print(f"C1A selector manifest: {len(resolved)} resolved, {len(excluded)} excluded -> {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
