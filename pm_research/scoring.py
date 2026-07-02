"""Scoring: cross-trader percentile ranks → alpha score.

Ranks are computed WITHIN the frame passed in (i.e. within the as-of
universe), never against all-time data — that's part of the point-in-time
contract.
"""
from __future__ import annotations

import pandas as pd

WEIGHTS = {"roi_pct": 0.45, "win_rate_pct": 0.30,
           "conviction_pct": 0.10, "automation_penalty": 0.15}


def score(features: pd.DataFrame) -> pd.DataFrame:
    """Input: features.compute_features output. Output adds alpha_score ∈ [0,1]."""
    if features.empty:
        out = features.copy()
        out["alpha_score"] = pd.Series(dtype=float)
        return out
    f = features.copy()
    f["roi_pct"] = f["roi"].rank(pct=True)
    f["win_rate_pct"] = f["win_rate"].rank(pct=True)
    f["conviction_pct"] = f["conviction"].rank(pct=True)
    f["automation_penalty"] = 1.0 - f["automation_proxy"].clip(0, 1)
    for c in ["roi_pct", "win_rate_pct", "conviction_pct"]:
        f[c] = f[c].fillna(0.0)
    f["alpha_score"] = sum(w * f[c] for c, w in WEIGHTS.items())
    return f.sort_values("alpha_score", ascending=False).reset_index(drop=True)
