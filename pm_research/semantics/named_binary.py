"""Named-binary semantics: classification, orientation, audit gate.

Build-order pieces 3, 5, 6 live here; pieces 1 and 4 are in mapping_audit.py and
resolution_schema.py and are consumed here.

Orientation contract (Decision 2):
  - YES_NO     -> canonical side = YES   ; yes_price == canonical_side_price
  - OVER_UNDER -> canonical side = OVER
  - UP_DOWN    -> canonical side = UP
  - TEAM_VS_TEAM / NAMED_OTHER -> side_0 / side_1 by outcome_index order;
    NO YES-equivalent. ``yes_price`` is UNDEFINED (None) for these.

Orientation reads TOKEN IDENTITY (the validated side whose label matches the
canonical label), never the live display label. A flipped label cannot move an
oriented price (no-label-only-inversion).

The layer ends at the audit gate. No probe, no PnL, no wallet logic here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .lexicon import (
    NB_CONTRACT_VERSION,
    NBSubclass,
    ORIENTED_SUBCLASSES,
    CANONICAL_LABEL,
    classify_label_pair,
    _norm,
)
from .mapping_audit import MappingResult, MAP_OK
from .resolution_schema import RES_OK


# ---------------------------------------------------------------------------
# Gate states (spec §6.1)
# ---------------------------------------------------------------------------
GATE_CLEAR = "CLEAR_FOR_NAMED_BINARY_SEMANTICS"
GATE_CLEAR_WARN = "CLEAR_WITH_WARNINGS"
GATE_BLOCK_MAPPING = "BLOCKED_BY_MAPPING_AMBIGUITY"
GATE_BLOCK_RESOLUTION = "BLOCKED_BY_RESOLUTION_MAPPING"
GATE_BLOCK_ORIENTATION = "BLOCKED_BY_PRICE_ORIENTATION"
GATE_BLOCK_COVERAGE = "BLOCKED_BY_INSUFFICIENT_COVERAGE"


# ---------------------------------------------------------------------------
# Classification (build order step 3)
# ---------------------------------------------------------------------------
@dataclass
class ClassificationRow:
    condition_id: str
    nb_subclass: str
    nb_eligible: bool
    nb_contract_version: str
    exclusion_reason: Optional[str] = None


def classify_condition(mapping: MappingResult) -> ClassificationRow:
    """Classify one condition given its mapping result.

    A condition is named-binary-eligible only if the mapping passed (exactly two
    tokens, stable identity) AND the label pair matches exactly one subclass.
    """
    cid = mapping.condition_id
    if mapping.status != MAP_OK:
        return ClassificationRow(cid, NBSubclass.UNUSABLE.value, False,
                                 NB_CONTRACT_VERSION, exclusion_reason=mapping.status)

    # sides ordered by outcome_index; labels may be None
    labels = [s[2] for s in mapping.sides]
    sub = classify_label_pair(labels[0], labels[1])
    if sub == NBSubclass.UNUSABLE:
        return ClassificationRow(cid, sub.value, False, NB_CONTRACT_VERSION,
                                 exclusion_reason="LABEL_PAIR_UNMATCHED")
    return ClassificationRow(cid, sub.value, True, NB_CONTRACT_VERSION)


# ---------------------------------------------------------------------------
# Orientation / canonical_side_price (build order step 5)
# ---------------------------------------------------------------------------
@dataclass
class OrientationContract:
    """Per-condition oriented price contract. ``yes_price`` is a YES/NO-only view."""
    condition_id: str
    nb_subclass: str
    side_0_token: str
    side_1_token: str
    canonical_token: Optional[str]   # token of the canonical side; None for non-oriented
    canonical_side_name: str         # 'YES'|'OVER'|'UP'|'side_0'
    has_yes_equivalent: bool

    def yes_price(self, side_0_price: float, side_1_price: float) -> Optional[float]:
        """yes_price is defined ONLY for YES_NO. For every other subclass it is
        None and callers must not synthesize it."""
        if self.nb_subclass != NBSubclass.YES_NO.value:
            return None
        return self.canonical_side_price(side_0_price, side_1_price)

    def canonical_side_price(self, side_0_price: float, side_1_price: float) -> float:
        """Price of the canonical side, selected by TOKEN IDENTITY.

        side_0_price/side_1_price are the prices of side_0_token/side_1_token
        respectively (ordered by outcome_index). The canonical side is chosen by
        which token is canonical, never by the label at call time.
        """
        if self.canonical_token == self.side_0_token:
            return side_0_price
        if self.canonical_token == self.side_1_token:
            return side_1_price
        # Non-oriented subclass: canonical side is side_0 by convention.
        return side_0_price


def build_orientation(mapping: MappingResult, nb_subclass: str) -> OrientationContract:
    """Construct the orientation contract from validated sides + subclass.

    Picks the canonical token by matching the subclass's canonical *label* to a
    side ONCE, here, recording the resulting TOKEN. After this, orientation is by
    token; the label is never consulted again.
    """
    s0_token, _s0_idx, s0_label = mapping.sides[0]
    s1_token, _s1_idx, s1_label = mapping.sides[1]

    sub = NBSubclass(nb_subclass)
    if sub in ORIENTED_SUBCLASSES:
        want = CANONICAL_LABEL[sub]  # 'yes' | 'over' | 'up'
        canonical_token = None
        if _norm(s0_label) == want:
            canonical_token = s0_token
        elif _norm(s1_label) == want:
            canonical_token = s1_token
        # If the canonical label can't be found on either side, orientation is
        # not establishable from identity -> caller treats as orientation failure.
        side_name = {"yes": "YES", "over": "OVER", "up": "UP"}[want]
        return OrientationContract(
            condition_id=mapping.condition_id,
            nb_subclass=nb_subclass,
            side_0_token=s0_token,
            side_1_token=s1_token,
            canonical_token=canonical_token,
            canonical_side_name=side_name,
            has_yes_equivalent=(sub == NBSubclass.YES_NO),
        )

    # Non-oriented: side_0 is canonical-by-convention, NOT a YES-equivalent.
    return OrientationContract(
        condition_id=mapping.condition_id,
        nb_subclass=nb_subclass,
        side_0_token=s0_token,
        side_1_token=s1_token,
        canonical_token=s0_token,
        canonical_side_name="side_0",
        has_yes_equivalent=False,
    )


def orientation_is_clean(contract: OrientationContract) -> bool:
    """An oriented subclass must have found its canonical token by identity.
    Non-oriented subclasses are always 'clean' (side_0 convention)."""
    sub = NBSubclass(contract.nb_subclass)
    if sub in ORIENTED_SUBCLASSES:
        return contract.canonical_token is not None
    return True


# ---------------------------------------------------------------------------
# Audit gate (build order step 6)
# ---------------------------------------------------------------------------
@dataclass
class GateThresholds:
    token_id_coverage_min: float = 0.99
    outcome_index_coverage_min: float = 0.99
    orientation_clear_min: float = 0.99
    orientation_warn_min: float = 0.95
    resolution_success_min: float = 0.99
    version: str = "gate-thresholds-2026-06-28.1"


@dataclass
class GateInput:
    total_conditions: int
    named_binary_eligible: int
    usable_named_binary_conditions: int
    token_id_coverage: float
    outcome_index_coverage: float
    resolution_mapping_success_rate: float
    orientation_correctness_rate: float
    blocked_reason_counts: Dict[str, int] = field(default_factory=dict)
    resolution_schema_chosen: Optional[str] = None


@dataclass
class GateResult:
    gate_state: str
    thresholds_version: str
    detail: Dict[str, object]


def run_audit_gate(gi: GateInput, th: Optional[GateThresholds] = None) -> GateResult:
    """Aggregate per-condition outcomes into a universe gate state.

    Precedence (spec §6.5): mapping ambiguity and resolution-mapping blocks take
    precedence over orientation/coverage. CLEAR_WITH_WARNINGS admits only the
    clean per-condition usable subset (per-condition failures already excluded
    upstream; the warning is purely universe-level).
    """
    th = th or GateThresholds()
    detail: Dict[str, object] = {
        "thresholds": th.version,
        "resolution_schema_chosen": gi.resolution_schema_chosen,
    }

    # Block precedence 1: resolution schema could not be chosen at all.
    if gi.resolution_schema_chosen is None:
        return GateResult(GATE_BLOCK_RESOLUTION, th.version, detail)

    # Block precedence 2: resolution mapping success below floor.
    if gi.resolution_mapping_success_rate < th.resolution_success_min:
        detail["resolution_mapping_success_rate"] = gi.resolution_mapping_success_rate
        return GateResult(GATE_BLOCK_RESOLUTION, th.version, detail)

    # Block precedence 3: mapping ambiguity dominates if there are no usable
    # conditions left after mapping/identity exclusions.
    if gi.usable_named_binary_conditions == 0:
        return GateResult(GATE_BLOCK_MAPPING, th.version, detail)

    # Coverage block.
    coverage_ok = (
        gi.token_id_coverage >= th.token_id_coverage_min
        and gi.outcome_index_coverage >= th.outcome_index_coverage_min
    )

    # Orientation bands.
    o = gi.orientation_correctness_rate
    if o < th.orientation_warn_min:
        return GateResult(GATE_BLOCK_ORIENTATION, th.version, detail)

    if not coverage_ok:
        return GateResult(GATE_BLOCK_COVERAGE, th.version, detail)

    # Clear vs warn: orientation in [warn_min, clear_min) -> warnings;
    # also warn if coverage exactly meets floor but any soft warning is present.
    if o < th.orientation_clear_min:
        detail["warning"] = "orientation_in_warning_band"
        return GateResult(GATE_CLEAR_WARN, th.version, detail)

    return GateResult(GATE_CLEAR, th.version, detail)
