"""Stage 2 — pure resolution-source logic for non-YES/NO named-binary outcomes.

This module is PURE LOGIC over already-loaded values. It does NOT:
  - read the full Stage 1 CSVs in a production builder (that is Stage 3),
  - modify the audit gate (Stage 4),
  - run any probe.

It provides:
  1. precision helpers (reject scientific notation, never parse through float),
  2. condition_id normalization (Dune varbinary-derived or already-0x),
  3. payout-vector parsing ('[0 1]', '[1 0]', comma variants, array(varchar)),
  4. winner derivation (exactly-one-nonzero-slot or conflict),
  5. slot -> token mapping against the validated local sides,
  6. an explicit status model; conflicts are excluded + counted, never silent.

Winners derive ONLY from payout numerators, NEVER from prices. Resolution data is
never used in classification (this module imports nothing from the classifier and
exposes no path back into it).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple


# --------------------------------------------------------------------------- #
# Status model (spec section 6)
# --------------------------------------------------------------------------- #
RESOLVED_SINGLE_WINNER = "RESOLVED_SINGLE_WINNER"
AMBIGUOUS_ZERO_WINNER = "AMBIGUOUS_ZERO_WINNER"
AMBIGUOUS_MULTIPLE_WINNERS = "AMBIGUOUS_MULTIPLE_WINNERS"
MALFORMED_PAYOUT_VECTOR = "MALFORMED_PAYOUT_VECTOR"
CONDITION_ID_INVALID = "CONDITION_ID_INVALID"
SLOT_TOKEN_MAPPING_MISSING = "SLOT_TOKEN_MAPPING_MISSING"
TOKEN_INDEX_CONFLICT = "TOKEN_INDEX_CONFLICT"
PRECISION_LOSS = "PRECISION_LOSS"

CONFLICT_STATUSES = frozenset({
    AMBIGUOUS_ZERO_WINNER, AMBIGUOUS_MULTIPLE_WINNERS, MALFORMED_PAYOUT_VECTOR,
    CONDITION_ID_INVALID, SLOT_TOKEN_MAPPING_MISSING, TOKEN_INDEX_CONFLICT,
    PRECISION_LOSS,
})


class DataExportPrecisionLoss(Exception):
    """Raised when a numeric field shows scientific notation (precision already
    lost). Mirrors the asset-id precision discipline from DECISION_LOG."""


# --------------------------------------------------------------------------- #
# Precision helpers
# --------------------------------------------------------------------------- #
_SCI = re.compile(r"^\s*-?\d+(\.\d+)?[eE][+-]?\d+\s*$")
_INT_STR = re.compile(r"^-?\d+$")
_HEX64 = re.compile(r"^0x[0-9a-f]{64}$")


def reject_scientific_notation(value: str, field: str = "value") -> None:
    """Raise loudly if value is in scientific notation. No float parsing."""
    if value is None:
        return
    s = str(value).strip()
    if _SCI.match(s):
        raise DataExportPrecisionLoss(
            f"scientific notation in {field}: {s!r} -- re-export with the uint256 "
            f"field cast to varchar; do not reconstruct."
        )


def safe_int_str(value: str, field: str = "value") -> str:
    """Return a canonical integer STRING (never via float).

    Accepts a full-precision integer string. Rejects scientific notation loudly.
    '0' / '00' normalize to '0'. Anything non-integer -> ValueError (caller maps
    to the right status)."""
    reject_scientific_notation(value, field)
    s = str(value).strip()
    if not _INT_STR.match(s):
        raise ValueError(f"non-integer {field}: {s!r}")
    neg = s.startswith("-")
    digits = s[1:] if neg else s
    digits = digits.lstrip("0") or "0"
    return ("-" + digits) if (neg and digits != "0") else digits


def is_nonzero_int_str(value: str) -> bool:
    """True iff the integer-string is non-zero. String-safe (no float)."""
    return safe_int_str(value) not in ("0",)


# --------------------------------------------------------------------------- #
# Condition ID normalization (spec section 2)
# --------------------------------------------------------------------------- #
def normalize_condition_id(raw: str) -> Optional[str]:
    """Normalize to '0x' + 64 lowercase hex chars, or None if malformed.

    Handles already-normalized '0x...' (any case), Dune varbinary-derived strings
    that may render with/without 0x, and surrounding whitespace. Rejects anything
    that isn't exactly 32 bytes of hex.
    """
    if raw is None:
        return None
    s = str(raw).strip().lower()
    body = s[2:] if s.startswith("0x") else s
    if len(body) != 64 or re.search(r"[^0-9a-f]", body):
        return None
    return "0x" + body


# --------------------------------------------------------------------------- #
# Payout-vector parsing (spec section 3)
# --------------------------------------------------------------------------- #
def parse_payout_vector(raw: str) -> Optional[List[str]]:
    """Parse an exported payoutnumerators string into a list of integer STRINGS.

    Accepts observed Dune array(varchar) export forms:
      '[0 1]'  (space-separated, Trino array display)
      '[1, 0]' (comma-separated)
      '[0  1]' (extra whitespace)
      '0 1' / '0,1' (bare, no brackets)
    Returns a list of canonical integer strings, or None if malformed.
    Rejects scientific notation in any element (loud). Never parses via float.
    """
    if raw is None:
        return None
    s = str(raw).strip()
    if s == "":
        return None
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1].strip()
    if s == "":
        return None
    parts = [p for p in re.split(r"[,\s]+", s) if p != ""]
    if not parts:
        return None
    out: List[str] = []
    for p in parts:
        reject_scientific_notation(p, "payoutnumerators element")
        try:
            out.append(safe_int_str(p, "payoutnumerators element"))
        except ValueError:
            return None
    return out


# --------------------------------------------------------------------------- #
# Winner derivation (spec section 4)
# --------------------------------------------------------------------------- #
@dataclass
class WinnerResult:
    status: str
    winning_slot: Optional[int] = None
    nonzero_slot_count: Optional[int] = None


def winner_from_payout(vector: Sequence[str], expect_binary: bool = True) -> WinnerResult:
    """Derive the winning slot from a payout vector of integer strings.

    Binary rule:
      exactly one nonzero slot -> RESOLVED_SINGLE_WINNER (that slot)
      zero nonzero            -> AMBIGUOUS_ZERO_WINNER
      more than one nonzero   -> AMBIGUOUS_MULTIPLE_WINNERS
    A non-binary vector length (when expect_binary) -> MALFORMED_PAYOUT_VECTOR.
    Never inspects prices.
    """
    if vector is None:
        return WinnerResult(MALFORMED_PAYOUT_VECTOR)
    if expect_binary and len(vector) != 2:
        return WinnerResult(MALFORMED_PAYOUT_VECTOR, nonzero_slot_count=None)

    nonzero_slots = []
    for idx, v in enumerate(vector):
        try:
            if is_nonzero_int_str(v):
                nonzero_slots.append(idx)
        except (ValueError, DataExportPrecisionLoss):
            return WinnerResult(MALFORMED_PAYOUT_VECTOR)

    n = len(nonzero_slots)
    if n == 1:
        return WinnerResult(RESOLVED_SINGLE_WINNER, nonzero_slots[0], n)
    if n == 0:
        return WinnerResult(AMBIGUOUS_ZERO_WINNER, None, 0)
    return WinnerResult(AMBIGUOUS_MULTIPLE_WINNERS, None, n)


# --------------------------------------------------------------------------- #
# Slot -> token mapping (spec section 5)
# --------------------------------------------------------------------------- #
@dataclass
class ResolvedWinner:
    status: str
    resolved_winning_token_id: Optional[str] = None
    resolved_winning_outcome_index: Optional[int] = None
    resolved_winning_label: Optional[str] = None


def map_slot_to_token(
    winning_slot: int,
    sides: Sequence[Tuple[str, int, Optional[str]]],
) -> ResolvedWinner:
    """Map a winning payout slot to the local side's token / index / label.

    sides is the validated, outcome_index-ordered side list from the mapping
    layer: ((token_id, outcome_index, label), (token_id, outcome_index, label)).
    The payout-vector slot index corresponds to outcome_index.

    Returns RESOLVED_SINGLE_WINNER with token/index/label if the slot maps
    cleanly; SLOT_TOKEN_MAPPING_MISSING if no side has that outcome_index;
    TOKEN_INDEX_CONFLICT if two sides claim the index, the token is empty, or the
    matched index disagrees with the slot.
    """
    if sides is None or len(sides) == 0:
        return ResolvedWinner(SLOT_TOKEN_MAPPING_MISSING)

    match = None
    for tok, idx, lab in sides:
        if idx == winning_slot:
            if match is not None:
                return ResolvedWinner(TOKEN_INDEX_CONFLICT)
            match = (tok, idx, lab)
    if match is None:
        return ResolvedWinner(SLOT_TOKEN_MAPPING_MISSING)

    tok, idx, lab = match
    if tok is None or str(tok).strip() == "":
        return ResolvedWinner(TOKEN_INDEX_CONFLICT)
    if idx != winning_slot:
        return ResolvedWinner(TOKEN_INDEX_CONFLICT)
    return ResolvedWinner(RESOLVED_SINGLE_WINNER, str(tok), idx, lab)


# --------------------------------------------------------------------------- #
# End-to-end (single condition) -- convenience, still pure
# --------------------------------------------------------------------------- #
def resolve_one(
    raw_condition_id: str,
    raw_payout: str,
    sides: Sequence[Tuple[str, int, Optional[str]]],
) -> ResolvedWinner:
    """Resolve a single condition from raw Dune fields + validated local sides.

    Pure: takes raw strings (as read dtype=str) and the local sides; returns a
    ResolvedWinner carrying a status from the section-6 model. Used by tests and,
    later, by the Stage 3 builder -- but builds no artifact here.
    """
    cid = normalize_condition_id(raw_condition_id)
    if cid is None:
        return ResolvedWinner(CONDITION_ID_INVALID)

    try:
        vector = parse_payout_vector(raw_payout)
    except DataExportPrecisionLoss:
        return ResolvedWinner(PRECISION_LOSS)
    if vector is None:
        return ResolvedWinner(MALFORMED_PAYOUT_VECTOR)

    wr = winner_from_payout(vector, expect_binary=True)
    if wr.status != RESOLVED_SINGLE_WINNER:
        return ResolvedWinner(wr.status)

    return map_slot_to_token(wr.winning_slot, sides)
