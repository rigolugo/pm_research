"""Resolution-schema audit (build order step 4).

Determines empirically what RESOLUTIONS_COLS.winning_outcome means, then
normalizes every usable condition to:
    resolved_winning_token_id
    resolved_winning_outcome_index
    resolved_winning_label

Decision 3 / OQ-3 discipline:
  - Explicit ``winning_outcome`` is the PRIMARY candidate source.
  - Price->1.0 convergence is CORROBORATION ONLY, never the definition.
  - A winner that cannot be mapped unambiguously to exactly one of the two
    outcome tokens => the condition is UNUSABLE.
  - When convergence CONTRADICTS the explicit winner, the disagreement is
    SURFACED (counted/reported), never silently overridden.

We test three interpretations of winning_outcome against the validated sides
from the mapping layer:
  - "outcome_index"  : winning_outcome is the integer index (0/1)
  - "token_id"       : winning_outcome is the winning token id (canonical string)
  - "label"          : winning_outcome is the outcome label string
The interpretation that maps unambiguously for the overwhelming majority is
declared the schema, with the disagreement rate reported. If none clears the
threshold, the gate returns BLOCKED_BY_RESOLUTION_MAPPING.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# resolution_map_status codes
RES_OK = "OK"
RES_FAIL_UNMAPPABLE = "FAIL_RESOLUTION_UNMAPPABLE"
RES_FAIL_AMBIGUOUS = "FAIL_RESOLUTION_AMBIGUOUS"

SchemaName = str  # one of: "outcome_index", "token_id", "label"
_INTERPRETATIONS: Tuple[SchemaName, ...] = ("outcome_index", "token_id", "label")


@dataclass
class ConditionSides:
    """The validated sides for one condition, from the mapping layer."""
    condition_id: str
    # ordered by outcome_index: (token_id, outcome_index, label)
    sides: Tuple[Tuple[str, int, Optional[str]], ...]


@dataclass
class ResolutionRow:
    condition_id: str
    winning_outcome_raw: object  # as stored, untrusted type
    # optional corroboration: token_id that price converged to 1.0 on, if known
    converged_token_id: Optional[str] = None


def _norm_label(s: Optional[str]) -> str:
    if s is None:
        return ""
    return " ".join(str(s).strip().lower().split())


def _try_map(interp: SchemaName, raw, sides) -> Optional[Tuple[str, int, Optional[str]]]:
    """Try to map one raw winning_outcome to exactly one side under ``interp``.

    Returns the matched side tuple, or None if it does not map to exactly one.
    """
    if raw is None:
        return None
    matches: List[Tuple[str, int, Optional[str]]] = []
    if interp == "outcome_index":
        try:
            target = int(raw)
        except (TypeError, ValueError):
            return None
        for tok, idx, lab in sides:
            if idx == target:
                matches.append((tok, idx, lab))
    elif interp == "token_id":
        target = str(raw).strip()
        if target in {"", "nan", "none"}:
            return None
        for tok, idx, lab in sides:
            if tok == target:
                matches.append((tok, idx, lab))
    elif interp == "label":
        target = _norm_label(raw)
        if target == "":
            return None
        for tok, idx, lab in sides:
            if _norm_label(lab) == target:
                matches.append((tok, idx, lab))
    return matches[0] if len(matches) == 1 else None


@dataclass
class SchemaAuditResult:
    chosen_schema: Optional[SchemaName]
    per_interpretation_success: Dict[SchemaName, float]
    convergence_disagreement_rate: Optional[float]
    n_evaluated: int


def determine_schema(
    rows: List[ResolutionRow],
    sides_by_condition: Dict[str, ConditionSides],
    min_success: float = 0.99,
) -> SchemaAuditResult:
    """Pick the winning_outcome interpretation from the CLEANLY-MAPPABLE subset.

    Issue-A fix: schema selection must not require one interpretation to clear a
    fraction of the ENTIRE mixed eligible universe. In a mixed universe, rows
    whose winner maps under NO interpretation (e.g. a team market whose
    resolutions row says "NO", matching neither team) are *unresolvable
    conditions*, not evidence against the schema. Counting them in the
    denominator drove the label interpretation below 99% and collapsed a perfect
    YES/NO result (8,521/8,521) to a reported 0%.

    Corrected logic:
      - For each interpretation, count how many eligible rows it maps.
      - The chosen schema is the interpretation that maps the MOST rows (the
        dominant interpretation on the subset that maps at all).
      - ``min_success`` is now applied as a confidence guard on the AGREEMENT
        among rows that map under SOME interpretation: of rows that any
        interpretation resolves, the chosen one must account for >= min_success
        of them (i.e. one interpretation dominates rather than a muddled split).
      - Rows that map under no interpretation are simply unresolvable; they do
        NOT veto schema selection and they remain blocked downstream.

    ``per_interpretation_success`` is reported as the fraction of ALL eligible
    rows each interpretation maps (transparent, unchanged denominator for
    reporting), so the caller still sees the true overall coverage.
    """
    n = 0
    success_counts = {interp: 0 for interp in _INTERPRETATIONS}
    any_map = 0  # rows that map under at least one interpretation
    eligible_rows = [r for r in rows if r.condition_id in sides_by_condition]
    for r in eligible_rows:
        n += 1
        sides = sides_by_condition[r.condition_id].sides
        mapped_any = False
        for interp in _INTERPRETATIONS:
            if _try_map(interp, r.winning_outcome_raw, sides) is not None:
                success_counts[interp] += 1
                mapped_any = True
        if mapped_any:
            any_map += 1

    if n == 0:
        return SchemaAuditResult(None, {i: 0.0 for i in _INTERPRETATIONS}, None, 0)

    # Reported rates: fraction of ALL eligible rows each interpretation maps.
    rates = {i: success_counts[i] / n for i in _INTERPRETATIONS}

    # Selection: dominant interpretation on the cleanly-mappable subset.
    best = max(success_counts, key=success_counts.get)
    if any_map == 0:
        chosen = None
    else:
        dominance = success_counts[best] / any_map
        chosen = best if (success_counts[best] > 0 and dominance >= min_success) else None

    # Convergence corroboration: among rows where we both mapped a winner under
    # the chosen schema AND have a converged_token_id, how often do they disagree?
    disagree = 0
    have_both = 0
    if chosen is not None:
        for r in eligible_rows:
            if r.converged_token_id is None:
                continue
            sides = sides_by_condition[r.condition_id].sides
            mapped = _try_map(chosen, r.winning_outcome_raw, sides)
            if mapped is None:
                continue
            have_both += 1
            if mapped[0] != str(r.converged_token_id).strip():
                disagree += 1
    disagreement_rate = (disagree / have_both) if have_both else None

    return SchemaAuditResult(chosen, rates, disagreement_rate, n)


def resolve_condition(
    interp: SchemaName,
    raw,
    sides: Tuple[Tuple[str, int, Optional[str]], ...],
) -> Tuple[str, Optional[Tuple[str, int, Optional[str]]]]:
    """Normalize one condition's resolution under the chosen schema.

    Returns (status, side|None). Unmappable -> RES_FAIL_UNMAPPABLE.
    """
    mapped = _try_map(interp, raw, sides)
    if mapped is None:
        return RES_FAIL_UNMAPPABLE, None
    return RES_OK, mapped
