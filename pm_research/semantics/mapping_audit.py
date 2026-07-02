"""Canonical mapping layer + mapping audit (build order step 1).

Builds, per condition_id, a validated mapping:
    condition_id <-> { (token_id, outcome_index, outcome_label) for each side }

markets.parquet (clobTokenIds / outcome order) is an INPUT CANDIDATE, never
unquestioned truth. The mapping is validated against token ids observed in the
trades/prices stream. A condition that fails any check is UNUSABLE and excluded.

The five checks (spec §3.2):
  1. token_id <-> condition_id stability   (a token maps to exactly one condition)
  2. token_id <-> outcome_index stability  (a token maps to exactly one index)
  3. outcome_index <-> label stability     (index<->label is 1:1 in the condition)
  4. exactly two outcome tokens for the condition
  5. resolution-reachability is checked in resolution_schema.py (forward ref);
     this module exposes the per-condition token set it needs.

This module operates on ACCUMULATED per-condition aggregates, not raw rows, so it
is O(conditions) in memory, never O(trades). The streaming accumulation lives in
the script; here we validate an already-accumulated structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple


# mapping_status codes
MAP_OK = "OK"
FAIL_TOKEN_CONDITION = "FAIL_TOKEN_CONDITION_STABILITY"
FAIL_TOKEN_INDEX = "FAIL_TOKEN_INDEX_STABILITY"
FAIL_INDEX_LABEL = "FAIL_INDEX_LABEL_STABILITY"
FAIL_TOKEN_COUNT = "FAIL_NOT_EXACTLY_TWO_TOKENS"


@dataclass
class ConditionAccumulator:
    """Per-condition aggregate accumulated over the streamed chunks.

    All token_ids are kept as canonical strings (full-precision integer strings),
    never floats, to avoid the scientific-notation precision-loss class of bug
    documented in DECISION_LOG. Comparison is string-exact.
    """

    condition_id: str
    # token_id -> set of outcome_index values seen for that token
    token_to_indices: Dict[str, Set[int]] = field(default_factory=dict)
    # outcome_index -> set of labels seen for that index
    index_to_labels: Dict[int, Set[str]] = field(default_factory=dict)
    # token_id -> set of labels seen (for side naming)
    token_to_labels: Dict[str, Set[str]] = field(default_factory=dict)

    def observe(self, token_id: str, outcome_index: Optional[int], label: Optional[str]) -> None:
        token_id = _canon_token(token_id)
        if token_id is None:
            return
        self.token_to_indices.setdefault(token_id, set())
        self.token_to_labels.setdefault(token_id, set())
        if outcome_index is not None:
            self.token_to_indices[token_id].add(int(outcome_index))
            self.index_to_labels.setdefault(int(outcome_index), set())
            if label is not None and str(label) != "":
                self.index_to_labels[int(outcome_index)].add(str(label))
        if label is not None and str(label) != "":
            self.token_to_labels[token_id].add(str(label))


def _canon_token(token_id) -> Optional[str]:
    """Canonicalize a token id to a full-precision integer string.

    Mirrors the canonical_int discipline from the OrdersMatched work: reject
    scientific notation loudly-ish (return None so the condition fails the count
    check rather than silently matching the wrong token).
    """
    if token_id is None:
        return None
    s = str(token_id).strip()
    if s == "" or s.lower() in {"nan", "none"}:
        return None
    if "e" in s.lower() or "." in s:
        # Precision-loss shape (e.g. '5.20896e+76' or '0.0'); do not trust it.
        # '0' is valid (USDC side); but '0.0' is the float-export artifact.
        if s in {"0", "-0"}:
            return "0"
        return None
    return s


@dataclass
class MappingResult:
    condition_id: str
    status: str
    token_ids: Tuple[str, ...] = ()
    # ordered sides: (token_id, outcome_index, label) sorted by outcome_index
    sides: Tuple[Tuple[str, int, Optional[str]], ...] = ()
    failed_check: Optional[str] = None


def audit_condition(acc: ConditionAccumulator) -> MappingResult:
    """Run the four structural mapping checks on one accumulated condition.

    (Check 5, resolution-reachability, is applied later by the resolution audit
    using the ``sides`` exposed here.)
    """
    cid = acc.condition_id

    # Check 4 first: exactly two outcome tokens.
    tokens = sorted(acc.token_to_indices.keys())
    if len(tokens) != 2:
        return MappingResult(cid, FAIL_TOKEN_COUNT, tuple(tokens),
                             failed_check=FAIL_TOKEN_COUNT)

    # Check 2: token <-> outcome_index stability (each token exactly one index).
    for tok in tokens:
        idxs = acc.token_to_indices[tok]
        if len(idxs) != 1:
            return MappingResult(cid, FAIL_TOKEN_INDEX, tuple(tokens),
                                 failed_check=FAIL_TOKEN_INDEX)

    # The two tokens must occupy two distinct indices.
    tok_index = {tok: next(iter(acc.token_to_indices[tok])) for tok in tokens}
    if len(set(tok_index.values())) != 2:
        return MappingResult(cid, FAIL_TOKEN_INDEX, tuple(tokens),
                             failed_check=FAIL_TOKEN_INDEX)

    # Check 3: outcome_index <-> label stability (each index at most one label).
    for idx, labels in acc.index_to_labels.items():
        if len(labels) > 1:
            return MappingResult(cid, FAIL_INDEX_LABEL, tuple(tokens),
                                 failed_check=FAIL_INDEX_LABEL)

    # Build ordered sides by outcome_index.
    sides = []
    for tok in tokens:
        idx = tok_index[tok]
        labels = acc.index_to_labels.get(idx, set())
        label = next(iter(labels)) if len(labels) == 1 else None
        sides.append((tok, idx, label))
    sides.sort(key=lambda s: s[1])

    return MappingResult(cid, MAP_OK, tuple(tokens), tuple(sides))


def audit_token_condition_stability(
    token_to_conditions: Dict[str, Set[str]]
) -> Dict[str, str]:
    """Check 1 is GLOBAL (cross-condition): a token id must map to exactly one
    condition_id across the whole dataset. Returns {condition_id: failed_check}
    for every condition that shares a token with another condition.

    Built from a global token->conditions accumulator (script-side). Any token
    seen under >1 condition fails ALL conditions it touches (the ambiguity is
    not localizable to one side).
    """
    failures: Dict[str, str] = {}
    for tok, conds in token_to_conditions.items():
        if len(conds) > 1:
            for cid in conds:
                failures[cid] = FAIL_TOKEN_CONDITION
    return failures
