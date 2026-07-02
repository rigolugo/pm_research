"""Named-binary semantics layer.

Public surface consumed by scripts/audit_named_binary_semantics.py and, for the
contract version, by Chat2 (Dune wallet discovery) which asserts version equality.

The layer ends at the audit gate. No probe, no PnL, no wallet logic.
"""

from .lexicon import (
    NB_CONTRACT_VERSION,
    NBSubclass,
    classify_label_pair,
)
from .mapping_audit import (
    ConditionAccumulator,
    MappingResult,
    audit_condition,
    audit_token_condition_stability,
    MAP_OK,
)
from .resolution_schema import (
    ConditionSides,
    ResolutionRow,
    determine_schema,
    resolve_condition,
    RES_OK,
)
from .named_binary import (
    ClassificationRow,
    classify_condition,
    OrientationContract,
    build_orientation,
    orientation_is_clean,
    GateInput,
    GateThresholds,
    GateResult,
    run_audit_gate,
    GATE_CLEAR,
    GATE_CLEAR_WARN,
    GATE_BLOCK_MAPPING,
    GATE_BLOCK_RESOLUTION,
    GATE_BLOCK_ORIENTATION,
    GATE_BLOCK_COVERAGE,
)
from .resolution_source import (
    normalize_condition_id,
    parse_payout_vector,
    winner_from_payout,
    map_slot_to_token,
    resolve_one,
    WinnerResult,
    ResolvedWinner,
    DataExportPrecisionLoss,
    RESOLVED_SINGLE_WINNER,
    AMBIGUOUS_ZERO_WINNER,
    AMBIGUOUS_MULTIPLE_WINNERS,
    MALFORMED_PAYOUT_VECTOR,
    CONDITION_ID_INVALID,
    SLOT_TOKEN_MAPPING_MISSING,
    TOKEN_INDEX_CONFLICT,
    PRECISION_LOSS,
    CONFLICT_STATUSES,
)

__all__ = [
    "NB_CONTRACT_VERSION",
    "NBSubclass",
    "classify_label_pair",
    "ConditionAccumulator",
    "MappingResult",
    "audit_condition",
    "audit_token_condition_stability",
    "MAP_OK",
    "ConditionSides",
    "ResolutionRow",
    "determine_schema",
    "resolve_condition",
    "RES_OK",
    "ClassificationRow",
    "classify_condition",
    "OrientationContract",
    "build_orientation",
    "orientation_is_clean",
    "GateInput",
    "GateThresholds",
    "GateResult",
    "run_audit_gate",
    "GATE_CLEAR",
    "GATE_CLEAR_WARN",
    "GATE_BLOCK_MAPPING",
    "GATE_BLOCK_RESOLUTION",
    "GATE_BLOCK_ORIENTATION",
    "GATE_BLOCK_COVERAGE",
]
