"""Version-pinned named-binary classification lexicon.

This module is the single source of truth for:
  - the named-binary subclasses (the only allowed values of ``nb_subclass``),
  - the canonical-side convention per subclass,
  - the label-pair -> subclass rules,
  - ``NB_CONTRACT_VERSION``.

Per the approved spec (named_binary_semantics_spec.md):
  - Labels are CLASSIFICATION HINTS ONLY. They never orient price. Orientation
    reads token identity via the mapping layer. A flipped label must not flip an
    oriented price (enforced by the no-label-only-inversion test).
  - Subclass assignment requires an exact, clean match of the two outcome labels
    to exactly one rule. Anything ambiguous or unmatched -> UNUSABLE.
  - The lexicon is built from a frequency-ranked label-pair census; the head is
    hand-classified, the tail is UNUSABLE. Bumping the lexicon MUST bump
    NB_CONTRACT_VERSION so downstream (Chat2) can assert version equality.

IMPORTANT: this is the *seed* lexicon. The hand-classified head from the real
census (scripts/named_binary_label_census.py output) is appended here in a
reviewable diff. The rules below cover the structural / canonical patterns that
are stable regardless of the census; extend TEAM_OR_NAMED matching via the
census, not by loosening the YES_NO / OVER_UNDER / UP_DOWN rules.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Optional

# Bump this whenever the lexicon or any classification rule changes.
NB_CONTRACT_VERSION = "nb-contract-2026-06-28.1"


class NBSubclass(str, Enum):
    YES_NO = "YES_NO"
    OVER_UNDER = "OVER_UNDER"
    UP_DOWN = "UP_DOWN"
    TEAM_VS_TEAM = "TEAM_VS_TEAM"
    NAMED_OTHER = "NAMED_OTHER"
    UNUSABLE = "UNUSABLE"


# Subclasses that have a YES-equivalent canonical side.
#   YES_NO -> YES, OVER_UNDER -> OVER, UP_DOWN -> UP.
# TEAM_VS_TEAM / NAMED_OTHER have NO YES-equivalent: side_0 / side_1 only.
ORIENTED_SUBCLASSES = frozenset(
    {NBSubclass.YES_NO, NBSubclass.OVER_UNDER, NBSubclass.UP_DOWN}
)

# The canonical "reference" label for each oriented subclass. The canonical side
# is resolved to a TOKEN via the mapping layer; this only records which label
# *names* the canonical side so the mapping can pick the matching token.
CANONICAL_LABEL = {
    NBSubclass.YES_NO: "yes",
    NBSubclass.OVER_UNDER: "over",
    NBSubclass.UP_DOWN: "up",
}


def _norm(label: str) -> str:
    """Normalize a single outcome label for matching: lowercase, strip,
    collapse internal whitespace. Does NOT alter token identity in any way."""
    if label is None:
        return ""
    return re.sub(r"\s+", " ", str(label).strip().lower())


# Exact two-label pair rules for the structural subclasses. Each is a frozenset
# of the two normalized labels -> subclass.
_PAIR_RULES = {
    frozenset({"yes", "no"}): NBSubclass.YES_NO,
    frozenset({"over", "under"}): NBSubclass.OVER_UNDER,
    frozenset({"up", "down"}): NBSubclass.UP_DOWN,
}

# Labels that, if present, indicate a non-binary / unusable structure even when
# only two tokens are seen (defensive; the two-token gate is the primary guard).
_UNUSABLE_LABEL_TOKENS = frozenset({"", "scalar", "n/a", "tbd", "other"})


def classify_label_pair(label_a: Optional[str], label_b: Optional[str]) -> NBSubclass:
    """Classify a *single* condition from its two outcome labels.

    Caller guarantees exactly two labels (the two-token gate runs first in the
    mapping audit). Returns a subclass; ambiguous / unmatched -> UNUSABLE.

    This function NEVER inspects token ids or prices. It is a pure label->subclass
    hint. Orientation happens elsewhere on token identity.
    """
    a = _norm(label_a)
    b = _norm(label_b)

    if a in _UNUSABLE_LABEL_TOKENS or b in _UNUSABLE_LABEL_TOKENS:
        return NBSubclass.UNUSABLE
    if a == b:
        # Two identical labels cannot form a clean binary pair.
        return NBSubclass.UNUSABLE

    pair = frozenset({a, b})

    # Structural rules first (exact pair match).
    sub = _PAIR_RULES.get(pair)
    if sub is not None:
        return sub

    # If exactly one of yes/no/over/under/up/down appears but not its partner,
    # the pair is malformed (e.g. {"yes","maybe"}): exclude rather than guess.
    structural_tokens = {"yes", "no", "over", "under", "up", "down"}
    if (a in structural_tokens) != (b in structural_tokens):
        return NBSubclass.UNUSABLE
    if a in structural_tokens and b in structural_tokens:
        # Both structural but not a recognized pair, e.g. {"yes","up"}.
        return NBSubclass.UNUSABLE

    # Neither label is a structural token: two named outcomes.
    # TEAM_VS_TEAM vs NAMED_OTHER is a head-census refinement. The seed rule
    # treats two distinct non-empty named labels as NAMED_OTHER; the census head
    # promotes recognized team/person-vs-person pairs to TEAM_VS_TEAM. Both are
    # orientation-identical (side_0 / side_1, no YES-equivalent), so a
    # mislabel between the two is not a price-orientation risk.
    return NBSubclass.NAMED_OTHER
