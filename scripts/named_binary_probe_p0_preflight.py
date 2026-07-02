#!/usr/bin/env python
"""Stage P0 preflight for the named-binary offline forecast-vs-price probe.

SCOPE: Stage P0 ONLY (per SPEC_named_binary_probe.md §11 Stage P0 and
PROJECT_STATE "Next possible step"). This module is READ-ONLY except for the
three P0 artifacts it writes under artifacts/named_binary_probe/.

It verifies the non-YES/NO named-binary probe universe *before any metric
exists*. It does NOT:
  - score, compute Brier / log-loss / calibration / reliability / edge / PnL,
  - load trades or prices, build decision timestamps, or compute
    canonical_side_price,
  - join outcomes into feature rows or build train/test splits,
  - run any Dune/network call, touch log_index, or do wallet logic,
  - modify the named-binary audit gate, or flip `named_binary_probe_blocked`.

It is NOT probe authorization. `named_binary_probe_blocked` is observed and
echoed from the gate, never changed. `probe_execution_authorized` is hard-wired
False.

p0_state is one of:
  P0_CLEAR
  STOP_MISSING_OUTCOME_SOURCE
  STOP_STALE_CONTRACT
  STOP_PRECISION_LOSS
  STOP_DATA_GATE_NOT_CLEAR
  STOP_COUNT_RECONCILIATION_FAILED
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Pinned constants
# ---------------------------------------------------------------------------

EXPECTED_CONTRACT_VERSION = "nb-contract-2026-06-28.1"
NON_YESNO_SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")
EXCLUDED_SUBCLASS = "YES_NO"
EXPECTED_GATE_STATE = "CLEAR_WITH_WARNINGS"
RESOLVED_STATUS = "RESOLVED_SINGLE_WINNER"
AMBIGUOUS_STATUS = "AMBIGUOUS_MULTIPLE_WINNERS"

STAGE = "P0_PREFLIGHT"
AUTHORIZED_SCOPE = "P0_PREFLIGHT_ONLY"

# Token-id / payout fields whose values must be precision-safe integer strings.
PRECISION_SENSITIVE_FIELDS = (
    "resolved_winning_token_id",
    "resolved_outcome_index",
)

# Scientific-notation / float-mangling signature. Matches "5.20896e+76",
# "1E+20", "0.0", etc. Anything that is not a clean (optionally signed) integer
# string for a token-id column is treated as precision loss.
_SCI_NOTATION_RE = re.compile(r"[eE]")
_CLEAN_INT_RE = re.compile(r"^-?\d+$")


class DataExportPrecisionLoss(Exception):
    """Raised when a precision-sensitive field shows scientific-notation or a
    float-mangled value (e.g. '5.20896e+76', '0.0'). Per DUNE_DATA_NOTES §5 we
    never reconstruct; we fail loud."""


class P0Stop(Exception):
    """Internal control-flow exception carrying a typed P0 stop state."""

    def __init__(self, state: str, message: str):
        super().__init__(message)
        self.state = state
        self.message = message


# ---------------------------------------------------------------------------
# Precision discipline
# ---------------------------------------------------------------------------

def canonical_int(value) -> str:
    """Normalize an integer-like value to a canonical full-precision string.

    Accepts clean integer strings ("0", "520896...") and Python ints. Rejects
    scientific notation and float-mangled forms by raising
    DataExportPrecisionLoss. Mirrors the project's canonical-int discipline
    (DECISION_LOG asset-id precision fix; DUNE_DATA_NOTES §4/§5).
    """
    if value is None:
        raise DataExportPrecisionLoss("token-id/payout field is None")
    if isinstance(value, bool):
        raise DataExportPrecisionLoss(f"unexpected bool token id: {value!r}")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # Any float is a precision red flag for a 78-digit token id.
        raise DataExportPrecisionLoss(
            f"float token id (precision already lost): {value!r}"
        )
    s = str(value).strip()
    if s == "":
        raise DataExportPrecisionLoss("empty token-id/payout field")
    if _SCI_NOTATION_RE.search(s):
        raise DataExportPrecisionLoss(f"scientific-notation token id: {s!r}")
    if not _CLEAN_INT_RE.match(s):
        # e.g. "0.0", "5.2e+76" already caught above, "abc", "12.0"
        raise DataExportPrecisionLoss(f"non-integer token-id form: {s!r}")
    return s


def _assert_precision_safe(rows, fields) -> None:
    """Validate every precision-sensitive field across rows; raise on the first
    precision-loss signature."""
    for r in rows:
        for f in fields:
            if f not in r:
                continue
            v = r[f]
            if v is None:
                # A null token id is a coverage matter, not precision loss; the
                # row will not be RESOLVED_SINGLE_WINNER if it lacks a winner.
                continue
            canonical_int(v)  # raises DataExportPrecisionLoss on bad form


# ---------------------------------------------------------------------------
# Loaders (read-only; no trades/prices, no Dune, no network)
# ---------------------------------------------------------------------------

def _read_json(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_contract(artifacts_dir: str) -> dict:
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_classification_contract.json"
    )
    if not os.path.exists(path):
        raise P0Stop(
            "STOP_MISSING_OUTCOME_SOURCE",
            f"classification contract not found: {path}",
        )
    return _read_json(path)


def _load_gate(artifacts_dir: str) -> dict:
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_audit_gate.json"
    )
    if not os.path.exists(path):
        raise P0Stop(
            "STOP_DATA_GATE_NOT_CLEAR",
            f"named-binary audit gate not found: {path}",
        )
    return _read_json(path)


def _load_resolution_source_rows(artifacts_dir: str):
    """Load the Stage 3 RESOLVED_SINGLE_WINNER rows as a list of dicts using
    dtype=str for token/id columns. Uses pandas/pyarrow if available; the rows
    are a versioned artifact, never a live Dune query."""
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_resolution_source_rows.parquet"
    )
    if not os.path.exists(path):
        raise P0Stop(
            "STOP_MISSING_OUTCOME_SOURCE",
            f"resolution-source rows not found: {path}",
        )
    try:
        import pandas as pd
    except ImportError as e:  # pragma: no cover - environment guard
        raise P0Stop(
            "STOP_MISSING_OUTCOME_SOURCE",
            f"pandas unavailable to read resolution-source rows: {e}",
        )

    df = pd.read_parquet(path)
    if df is None or len(df) == 0:
        raise P0Stop(
            "STOP_MISSING_OUTCOME_SOURCE",
            f"resolution-source rows present but empty: {path}",
        )
    # Force token/id fields to str so a parquet-stored float can't slip through.
    for f in PRECISION_SENSITIVE_FIELDS:
        if f in df.columns:
            df[f] = df[f].astype("string")
    return df.to_dict(orient="records")


def _load_conflicts_csv(artifacts_dir: str):
    """Optional: Stage 3 conflicts (for excluded-count reconciliation). Returns
    list of dicts or None if absent."""
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_resolution_conflicts.csv"
    )
    if not os.path.exists(path):
        return None
    try:
        import pandas as pd
    except ImportError:  # pragma: no cover
        return None
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return df.to_dict(orient="records")


# ---------------------------------------------------------------------------
# Version + gate assertions
# ---------------------------------------------------------------------------

def _contract_version(contract: dict) -> str:
    v = contract.get("nb_contract_version")
    if not v:
        raise P0Stop(
            "STOP_STALE_CONTRACT",
            "contract missing nb_contract_version",
        )
    return v


def _resolution_source_version(rows) -> str:
    versions = {
        str(r.get("nb_contract_version"))
        for r in rows
        if r.get("nb_contract_version") not in (None, "")
    }
    if not versions:
        raise P0Stop(
            "STOP_STALE_CONTRACT",
            "resolution-source rows carry no nb_contract_version",
        )
    if len(versions) > 1:
        raise P0Stop(
            "STOP_STALE_CONTRACT",
            f"resolution-source rows carry mixed nb_contract_version: {sorted(versions)}",
        )
    return versions.pop()


def _assert_versions(contract_version: str, source_version: str) -> None:
    if contract_version != EXPECTED_CONTRACT_VERSION:
        raise P0Stop(
            "STOP_STALE_CONTRACT",
            f"contract version {contract_version!r} != expected "
            f"{EXPECTED_CONTRACT_VERSION!r}",
        )
    if source_version != EXPECTED_CONTRACT_VERSION:
        raise P0Stop(
            "STOP_STALE_CONTRACT",
            f"resolution-source version {source_version!r} != expected "
            f"{EXPECTED_CONTRACT_VERSION!r}",
        )
    if contract_version != source_version:
        raise P0Stop(
            "STOP_STALE_CONTRACT",
            f"contract version {contract_version!r} != resolution-source "
            f"version {source_version!r}",
        )


def _extract_branch(gate: dict) -> dict:
    branch = gate.get("stage4_nonyesno_branch")
    if not isinstance(branch, dict):
        raise P0Stop(
            "STOP_DATA_GATE_NOT_CLEAR",
            "gate missing stage4_nonyesno_branch (run audit with --resolution-source)",
        )
    return branch


def _assert_gate_clear(branch: dict) -> None:
    state = branch.get("non_yesno_gate_state")
    if state != EXPECTED_GATE_STATE:
        raise P0Stop(
            "STOP_DATA_GATE_NOT_CLEAR",
            f"non_yesno_gate_state {state!r} != {EXPECTED_GATE_STATE!r}",
        )


def _scoreable_subclasses(branch: dict) -> dict:
    """Read per-subclass scoreability from the gate; never assume it."""
    per = branch.get("per_subclass_scoreable")
    if not isinstance(per, dict):
        raise P0Stop(
            "STOP_DATA_GATE_NOT_CLEAR",
            "gate branch missing per_subclass_scoreable map",
        )
    return {k: bool(v) for k, v in per.items()}


# ---------------------------------------------------------------------------
# Eligibility counting (no scoring, no features)
# ---------------------------------------------------------------------------

def _count_contract_eligible(contract: dict) -> dict:
    """Count contract-eligible conditions per non-YES/NO subclass.

    The contract carries per-condition subclass + eligibility. We tolerate a few
    shapes: a list under 'conditions'/'rows', or a dict keyed by condition_id.
    YES_NO is excluded. Only conditions flagged eligible (if an eligibility flag
    exists) are counted; absent a flag, subclass membership is the criterion.
    """
    records = None
    if isinstance(contract.get("conditions"), list):
        records = contract["conditions"]
    elif isinstance(contract.get("rows"), list):
        records = contract["rows"]
    elif isinstance(contract.get("conditions"), dict):
        records = list(contract["conditions"].values())

    counts = {sc: 0 for sc in NON_YESNO_SUBCLASSES}
    counts_yes_no_excluded = 0

    if records is None:
        # No per-condition detail in the contract JSON. Reconciliation against
        # contract-eligible will be reported as not-exact rather than failing.
        return {"counts": counts, "yes_no_excluded": counts_yes_no_excluded,
                "has_per_condition": False}

    for rec in records:
        if not isinstance(rec, dict):
            continue
        sc = rec.get("subclass") or rec.get("nb_subclass")
        if sc == EXCLUDED_SUBCLASS:
            counts_yes_no_excluded += 1
            continue
        if sc not in NON_YESNO_SUBCLASSES:
            continue
        elig = rec.get("eligible")
        if elig is None:
            elig = rec.get("probe_eligible")
        if elig is False:
            continue
        counts[sc] += 1

    return {"counts": counts, "yes_no_excluded": counts_yes_no_excluded,
            "has_per_condition": True}


def _count_resolved_from_source(rows):
    """Count RESOLVED_SINGLE_WINNER rows per non-YES/NO subclass from the
    resolution-source parquet. That artifact holds RESOLVED_SINGLE_WINNER rows
    ONLY (ARTIFACT_INDEX), so this is the resolved count, NOT source_rows.
    YES_NO and other-subclass rows are excluded + counted separately."""
    resolved = {sc: 0 for sc in NON_YESNO_SUBCLASSES}
    yes_no_rows_excluded = 0
    other_subclass_rows = 0
    non_resolved_in_source = {sc: 0 for sc in NON_YESNO_SUBCLASSES}

    for r in rows:
        sc = r.get("subclass") or r.get("nb_subclass")
        if sc == EXCLUDED_SUBCLASS:
            yes_no_rows_excluded += 1
            continue
        if sc not in NON_YESNO_SUBCLASSES:
            other_subclass_rows += 1
            continue
        status = r.get("status")
        if status == RESOLVED_STATUS:
            resolved[sc] += 1
        else:
            # The source-rows parquet is resolved-only by construction; any
            # non-resolved status here is unexpected. Count it (never fold into
            # resolved) so reconciliation can surface it rather than hiding it.
            non_resolved_in_source[sc] += 1

    return {
        "resolved": resolved,
        "non_resolved_in_source": non_resolved_in_source,
        "yes_no_rows_excluded": yes_no_rows_excluded,
        "other_subclass_rows": other_subclass_rows,
    }


def _count_ambiguous(conflicts, branch, scoreable):
    """Determine ambiguous_multiple_winners per non-YES/NO subclass.

    Preference order (never silently guesses):
      1. From named_binary_resolution_conflicts.csv (Stage 3 conflicts) when
         available — count rows whose status is AMBIGUOUS_MULTIPLE_WINNERS.
      2. Else, from the gate per_subclass_breakdown ambiguous field — used
         explicitly and flagged as gate_breakdown_only.
      3. Else, zero, flagged unavailable.

    Returns (ambiguous_by_sub, ambiguous_source_tag).
    """
    amb = {sc: 0 for sc in NON_YESNO_SUBCLASSES}

    if conflicts is not None:
        for r in conflicts:
            sc = r.get("subclass") or r.get("nb_subclass")
            if sc not in NON_YESNO_SUBCLASSES:
                continue
            status = (r.get("status") or "").strip()
            if status == AMBIGUOUS_STATUS:
                amb[sc] += 1
        return amb, "conflicts_csv"

    breakdown = branch.get("per_subclass_breakdown")
    if isinstance(breakdown, dict):
        found_any = False
        for sc in NON_YESNO_SUBCLASSES:
            sc_bd = breakdown.get(sc)
            if isinstance(sc_bd, dict):
                val = sc_bd.get("AMBIGUOUS_MULTIPLE_WINNERS")
                if val is None:
                    val = sc_bd.get("ambiguous_multiple_winners")
                if val is not None:
                    amb[sc] = int(val)
                    found_any = True
        if found_any:
            return amb, "gate_breakdown_only"

    return amb, "unavailable"


def _tally_counts(contract_elig, resolved_info, ambiguous_by_sub, scoreable):
    """Assemble corrected per-subclass and pooled counts.

    Definitions (aligned to Stage 4):
      resolved_single_winner  = resolved rows from source parquet
      ambiguous_multiple_winners = from conflicts/gate (§_count_ambiguous)
      source_rows            = resolved + ambiguous   (rows FOUND in the source)
      missing_source_rows    = contract_eligible - source_rows   (>= 0)
      final_p0_eligible      = resolved_single_winner for scoreable subclasses,
                               else 0 (non-scoreable subclass contributes 0)
    """
    by_sub = {}
    notes = []
    for sc in NON_YESNO_SUBCLASSES:
        resolved = resolved_info["resolved"][sc]
        ambiguous = ambiguous_by_sub[sc]
        source_rows = resolved + ambiguous
        elig = contract_elig["counts"].get(sc)
        is_scoreable = scoreable.get(sc, False)

        if elig is None:
            missing = None
        else:
            missing = elig - source_rows
            if missing < 0:
                # source_rows exceed contract_eligible — an upstream
                # inconsistency; keep the negative visible for reconciliation
                # rather than clamping silently.
                notes.append(
                    f"{sc}: source_rows ({source_rows}) exceed contract_eligible "
                    f"({elig}); missing_source_rows negative — reported, not clamped."
                )

        final_eligible = resolved if is_scoreable else 0

        by_sub[sc] = {
            "contract_eligible": elig,
            "source_rows": source_rows,
            "resolved_single_winner": resolved,
            "ambiguous_multiple_winners": ambiguous,
            "missing_source_rows": missing,
            "non_scoreable": (0 if is_scoreable else resolved + ambiguous),
            "final_p0_eligible": final_eligible,
        }

    # Pooled = sum of subclass counts (after YES_NO exclusion). None-safe.
    def _psum(key):
        vals = [by_sub[sc][key] for sc in NON_YESNO_SUBCLASSES]
        if any(v is None for v in vals):
            return None
        return sum(vals)

    pooled = {
        "contract_eligible": _psum("contract_eligible"),
        "source_rows": _psum("source_rows"),
        "resolved_single_winner": _psum("resolved_single_winner"),
        "ambiguous_multiple_winners": _psum("ambiguous_multiple_winners"),
        "missing_source_rows": _psum("missing_source_rows"),
        "non_scoreable": _psum("non_scoreable"),
        "final_p0_eligible": _psum("final_p0_eligible"),
    }

    return {"by_subclass": by_sub, "pooled": pooled, "notes": notes}


# ---------------------------------------------------------------------------
# Reconciliation against Stage 4 gate fields
# ---------------------------------------------------------------------------

def _reconcile(tally: dict, branch: dict, ambiguous_source: str) -> dict:
    """Compare P0-computed per-subclass counts against the gate's
    per_subclass_breakdown, like-for-like. Mismatches are reported, not silently
    accepted; a hard mismatch on a core field raises
    STOP_COUNT_RECONCILIATION_FAILED.

    Fields compared (when present in the gate breakdown):
      contract_eligible, source_rows, resolved_single_winner,
      ambiguous_multiple_winners, missing_source_rows, final_p0_eligible.

    `ambiguous_source` records where ambiguous came from. When it is
    'gate_breakdown_only', the ambiguous (and its derived source_rows /
    missing_source_rows) were taken FROM the gate, so comparing them back to the
    gate is a tautology — those fields are still reported but not treated as an
    independent check.
    """
    breakdown = branch.get("per_subclass_breakdown")
    result = {
        "exact": None,
        "ambiguous_source": ambiguous_source,
        "checked_fields": [],
        "tautological_fields": [],
        "mismatches": [],
        "note": "",
    }

    if not isinstance(breakdown, dict):
        result["exact"] = False
        result["note"] = (
            "gate lacks per_subclass_breakdown row-level detail; "
            "reconciliation not exact (reported, not failed)."
        )
        return result

    field_map = {
        "contract_eligible": ("eligible", "contract_eligible"),
        "source_rows": ("source_rows",),
        "resolved_single_winner": ("resolved_single_winner",),
        "ambiguous_multiple_winners": (
            "AMBIGUOUS_MULTIPLE_WINNERS",
            "ambiguous_multiple_winners",
        ),
        "missing_source_rows": ("missing_source_rows",),
        "final_p0_eligible": ("final_p0_eligible",),
    }
    # Core fields whose disagreement is a hard failure.
    core_fields = {
        "contract_eligible",
        "source_rows",
        "resolved_single_winner",
        "ambiguous_multiple_winners",
        "missing_source_rows",
    }
    # When ambiguous came from the gate, these are gate-derived → not independent.
    gate_derived = (
        {"ambiguous_multiple_winners", "source_rows", "missing_source_rows"}
        if ambiguous_source == "gate_breakdown_only"
        else set()
    )

    hard_mismatch = False
    for sc in NON_YESNO_SUBCLASSES:
        gate_sc = breakdown.get(sc)
        if not isinstance(gate_sc, dict):
            result["mismatches"].append(
                {"subclass": sc, "issue": "no gate breakdown for subclass"}
            )
            hard_mismatch = True
            continue
        ours = tally["by_subclass"][sc]
        for our_key, gate_keys in field_map.items():
            gate_val = None
            for gk in gate_keys:
                if gk in gate_sc:
                    gate_val = gate_sc[gk]
                    break
            if gate_val is None:
                continue
            our_val = ours.get(our_key)
            if our_val is None:
                # e.g. contract_eligible unavailable → cannot compare this field.
                continue
            tag = f"{sc}.{our_key}"
            if our_key in gate_derived:
                result["tautological_fields"].append(tag)
                continue
            result["checked_fields"].append(tag)
            if int(gate_val) != int(our_val):
                mm = {
                    "subclass": sc,
                    "field": our_key,
                    "p0": int(our_val),
                    "gate": int(gate_val),
                }
                result["mismatches"].append(mm)
                if our_key in core_fields:
                    hard_mismatch = True

    result["exact"] = not result["mismatches"]
    if hard_mismatch:
        raise P0Stop(
            "STOP_COUNT_RECONCILIATION_FAILED",
            f"P0 counts disagree with gate breakdown: {result['mismatches']}",
        )
    if result["mismatches"]:
        result["note"] = "soft mismatches only (non-core fields); reported, not failed."
    return result


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_preflight(artifacts_dir: str) -> dict:
    """Execute Stage P0 and return the p0_preflight result dict. Raises nothing;
    a stop is captured as the returned p0_state."""
    created = _dt.datetime.now(_dt.timezone.utc).isoformat()

    base = {
        "stage": STAGE,
        "authorized_scope": AUTHORIZED_SCOPE,
        "probe_execution_authorized": False,
        "named_binary_probe_blocked_observed": None,
        "nb_contract_version_expected": EXPECTED_CONTRACT_VERSION,
        "nb_contract_version_contract": None,
        "nb_contract_version_resolution_source": None,
        "gate_snapshot": {},
        "counts_pooled": {},
        "counts_by_subclass": {},
        "excluded_counts": {},
        "reconciliation": {},
        "notes": [],
        "created_at_utc": created,
    }

    try:
        contract = _load_contract(artifacts_dir)
        gate = _load_gate(artifacts_dir)
        rows = _load_resolution_source_rows(artifacts_dir)
        conflicts = _load_conflicts_csv(artifacts_dir)

        # Precision discipline first — fail loud before any counting.
        try:
            _assert_precision_safe(rows, PRECISION_SENSITIVE_FIELDS)
        except DataExportPrecisionLoss as e:
            raise P0Stop("STOP_PRECISION_LOSS", str(e))

        # Versions.
        contract_version = _contract_version(contract)
        source_version = _resolution_source_version(rows)
        base["nb_contract_version_contract"] = contract_version
        base["nb_contract_version_resolution_source"] = source_version
        _assert_versions(contract_version, source_version)

        # Gate.
        branch = _extract_branch(gate)
        _assert_gate_clear(branch)
        scoreable = _scoreable_subclasses(branch)

        # Observe (never flip) the standing block marker.
        blocked_observed = gate.get("named_binary_probe_blocked")
        if blocked_observed is None:
            blocked_observed = branch.get("named_binary_probe_blocked")
        base["named_binary_probe_blocked_observed"] = blocked_observed

        base["gate_snapshot"] = {
            "non_yesno_gate_state": branch.get("non_yesno_gate_state"),
            "non_yesno_scoreable": branch.get("non_yesno_scoreable"),
            "non_yesno_pooled_map_rate": branch.get("non_yesno_pooled_map_rate"),
            "pooled_threshold": branch.get("pooled_threshold"),
            "subclass_threshold": branch.get("subclass_threshold"),
            "per_subclass_map_rate": branch.get("per_subclass_map_rate"),
            "per_subclass_scoreable": scoreable,
            "base_gate_state": gate.get("gate_state") or gate.get("base_gate_state"),
            "source_winner_count": branch.get("source_winner_count")
            or gate.get("source_winner_count"),
        }

        # Counts (corrected definitions).
        #   resolved  = RESOLVED_SINGLE_WINNER rows in the source parquet
        #   ambiguous = from conflicts CSV (preferred) or gate breakdown
        #   source_rows = resolved + ambiguous
        #   missing = contract_eligible - source_rows
        contract_elig = _count_contract_eligible(contract)
        resolved_info = _count_resolved_from_source(rows)
        ambiguous_by_sub, ambiguous_source = _count_ambiguous(
            conflicts, branch, scoreable
        )
        tally = _tally_counts(
            contract_elig, resolved_info, ambiguous_by_sub, scoreable
        )
        base["notes"].extend(tally.get("notes", []))

        base["counts_by_subclass"] = {
            sc: dict(tally["by_subclass"][sc]) for sc in NON_YESNO_SUBCLASSES
        }
        base["counts_pooled"] = dict(tally["pooled"])

        base["excluded_counts"] = {
            "ambiguous_source": ambiguous_source,
            "yes_no_excluded_contract": contract_elig["yes_no_excluded"],
            "yes_no_rows_excluded_source": resolved_info["yes_no_rows_excluded"],
            "other_subclass_rows_excluded": resolved_info["other_subclass_rows"],
            "non_resolved_rows_in_source": resolved_info["non_resolved_in_source"],
            "ambiguous_multiple_winners_pooled": tally["pooled"][
                "ambiguous_multiple_winners"
            ],
            "missing_source_rows_pooled": tally["pooled"]["missing_source_rows"],
            "non_scoreable_pooled": tally["pooled"]["non_scoreable"],
        }
        if not contract_elig["has_per_condition"]:
            base["notes"].append(
                "Contract JSON lacked per-condition records; contract_eligible "
                "counts are null, so source_rows/missing/reconciliation against "
                "contract_eligible are not exact."
            )
        if ambiguous_source == "gate_breakdown_only":
            base["notes"].append(
                "Conflicts CSV absent; ambiguous_multiple_winners taken from gate "
                "per_subclass_breakdown (ambiguous_source=gate_breakdown_only). "
                "Ambiguous-derived fields are not independently reconciled."
            )
        elif ambiguous_source == "unavailable":
            base["notes"].append(
                "No ambiguous source available (no conflicts CSV, no gate "
                "breakdown ambiguous field); ambiguous counted as 0 — flagged."
            )

        # Reconciliation (may raise STOP_COUNT_RECONCILIATION_FAILED).
        base["reconciliation"] = _reconcile(tally, branch, ambiguous_source)

        base["p0_state"] = "P0_CLEAR"
        base["notes"].append(
            "P0 preflight only. No scoring, no features, no probe authorization. "
            "named_binary_probe_blocked observed and unchanged."
        )

    except P0Stop as stop:
        base["p0_state"] = stop.state
        base["notes"].append(f"HALT {stop.state}: {stop.message}")

    return base


# ---------------------------------------------------------------------------
# Artifact emission
# ---------------------------------------------------------------------------

def _write_json(out_dir: str, result: dict) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "p0_preflight.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=False)
    return path


def _write_md(out_dir: str, result: dict) -> str:
    path = os.path.join(out_dir, "p0_preflight.md")
    state = result.get("p0_state")
    lines = []
    lines.append("# Named-Binary Probe — Stage P0 Preflight")
    lines.append("")
    lines.append(f"- **p0_state:** `{state}`")
    lines.append(f"- **authorized_scope:** `{result['authorized_scope']}`")
    lines.append(
        f"- **probe_execution_authorized:** `{result['probe_execution_authorized']}`"
    )
    lines.append(
        f"- **named_binary_probe_blocked_observed:** "
        f"`{result['named_binary_probe_blocked_observed']}` (observed, never flipped)"
    )
    lines.append(f"- **created_at_utc:** {result['created_at_utc']}")
    lines.append("")
    lines.append("## Contract version")
    lines.append(f"- expected: `{result['nb_contract_version_expected']}`")
    lines.append(f"- contract: `{result['nb_contract_version_contract']}`")
    lines.append(
        f"- resolution-source: `{result['nb_contract_version_resolution_source']}`"
    )
    lines.append("")
    lines.append("## Gate snapshot")
    for k, v in (result.get("gate_snapshot") or {}).items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Counts (pooled)")
    for k, v in (result.get("counts_pooled") or {}).items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Counts by subclass")
    for sc, d in (result.get("counts_by_subclass") or {}).items():
        lines.append(f"### {sc}")
        for k, v in d.items():
            lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Excluded counts")
    for k, v in (result.get("excluded_counts") or {}).items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Reconciliation")
    rec = result.get("reconciliation") or {}
    lines.append(f"- exact: {rec.get('exact')}")
    if rec.get("note"):
        lines.append(f"- note: {rec['note']}")
    if rec.get("mismatches"):
        lines.append(f"- mismatches: {rec['mismatches']}")
    lines.append("")
    lines.append("## Notes")
    for n in result.get("notes", []):
        lines.append(f"- {n}")
    lines.append("")
    lines.append(
        "_Stage P0 is read-only except for these artifacts. It does not score, "
        "build features, or authorize the probe._"
    )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def _write_excluded_csv(out_dir: str, result: dict) -> str:
    path = os.path.join(out_dir, "p0_excluded_counts.csv")
    header = [
        "subclass",
        "source_rows",
        "resolved_single_winner",
        "ambiguous_multiple_winners",
        "missing_source_rows",
        "non_scoreable",
        "final_p0_eligible",
    ]
    rows_out = [",".join(header)]
    for sc, d in (result.get("counts_by_subclass") or {}).items():
        rows_out.append(
            ",".join(
                str(d.get(col, "")) if col != "subclass" else sc for col in header
            )
        )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows_out) + "\n")
    return path


def emit_artifacts(artifacts_dir: str, result: dict) -> dict:
    out_dir = os.path.join(artifacts_dir, "named_binary_probe")
    paths = {
        "json": _write_json(out_dir, result),
        "md": _write_md(out_dir, result),
        "csv": _write_excluded_csv(out_dir, result),
    }
    return paths


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Stage P0 preflight for the named-binary offline probe "
        "(read-only; no scoring; not probe authorization).",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Data root (e.g. C:\\b1\\data). Accepted for command-shape "
        "compatibility; P0 reads NO trades/prices and does not use it.",
    )
    parser.add_argument(
        "--artifacts-dir",
        default="artifacts",
        help="Artifacts directory (default: artifacts).",
    )
    args = parser.parse_args(argv)

    result = run_preflight(args.artifacts_dir)
    paths = emit_artifacts(args.artifacts_dir, result)

    print(f"[P0] p0_state = {result['p0_state']}")
    print(f"[P0] wrote {paths['json']}")
    print(f"[P0] wrote {paths['md']}")
    print(f"[P0] wrote {paths['csv']}")
    print(
        f"[P0] probe_execution_authorized = {result['probe_execution_authorized']} | "
        f"named_binary_probe_blocked_observed = "
        f"{result['named_binary_probe_blocked_observed']}"
    )

    # Exit 0 on P0_CLEAR, non-zero on any stop, so a pipeline notices a halt.
    return 0 if result["p0_state"] == "P0_CLEAR" else 2


if __name__ == "__main__":
    sys.exit(main())
