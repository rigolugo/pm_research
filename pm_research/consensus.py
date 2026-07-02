"""Consensus detection → signals.

A consensus event: >= min_unique_traders from the current universe BUY the
same (market, outcome) within `window_hours`. Its weighted score is the mean
alpha score of participants (skill-weighted agreement), which becomes the
signal's raw confidence — explicitly *raw*: calibration maps it to a
probability later.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import ConsensusConfig


@dataclass(frozen=True)
class Signal:
    condition_id: str
    outcome: str                 # 'YES' | 'NO'
    raw_confidence: float        # NOT a probability until calibrated
    leaders_avg_entry: float
    first_entry_at: pd.Timestamp
    detected_at: pd.Timestamp    # when the consensus completed (last entry)
    n_traders: int


def detect(trades: pd.DataFrame, universe: list[str], scores: pd.DataFrame,
           as_of: pd.Timestamp, cfg: ConsensusConfig) -> list[Signal]:
    lo = as_of - pd.Timedelta(hours=cfg.window_hours)
    t = trades[(trades["traded_at"] > lo) & (trades["traded_at"] <= as_of)
               & (trades["side"] == "BUY") & (trades["wallet"].isin(universe))]
    if t.empty:
        return []
    alpha = dict(zip(scores["wallet"], scores["alpha_score"])) if len(scores) else {}
    out: list[Signal] = []
    for (cid, outcome), g in t.groupby(["condition_id", "outcome"]):
        uniq = g.drop_duplicates(subset="wallet")
        if len(uniq) < cfg.min_unique_traders:
            continue
        w = uniq["wallet"].map(lambda x: alpha.get(x, 0.0))
        weighted = float(w.mean())
        if weighted < cfg.min_weighted_score:
            continue
        out.append(Signal(
            condition_id=cid, outcome=outcome, raw_confidence=min(weighted, 1.0),
            leaders_avg_entry=float(uniq["price"].mean()),
            first_entry_at=uniq["traded_at"].min(),
            detected_at=uniq["traded_at"].max(),
            n_traders=int(len(uniq))))
    return sorted(out, key=lambda s: s.detected_at)


class CooldownFilter:
    """Suppress repeat signals for the same market within the cooldown."""

    def __init__(self, cooldown_hours: int):
        self.cooldown = pd.Timedelta(hours=cooldown_hours)
        self._last: dict[str, pd.Timestamp] = {}

    def admit(self, sig: Signal) -> bool:
        last = self._last.get(sig.condition_id)
        if last is not None and sig.detected_at - last < self.cooldown:
            return False
        self._last[sig.condition_id] = sig.detected_at
        return True
