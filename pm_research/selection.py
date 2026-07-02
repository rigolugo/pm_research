"""Wallet-universe selection — the survivorship-bias killer.

The selector sees ONLY data as of `as_of`. It never reads a current
leaderboard and never sees a hand-picked winner list. Backtests call it at
every rebalance date; live calls it weekly. Same code path, both worlds.
"""
from __future__ import annotations

import pandas as pd

from .config import SelectionConfig
from .features import compute_features
from .scoring import score


class TrailingAlphaSelector:
    """Top-N wallets by alpha score over trailing resolved performance."""

    def __init__(self, cfg: SelectionConfig):
        self.cfg = cfg

    def select(self, trades: pd.DataFrame, resolutions: pd.DataFrame,
               as_of: pd.Timestamp) -> list[str]:
        f = compute_features(trades, resolutions, as_of, self.cfg.lookback_days)
        if f.empty:
            return []
        eligible = f[(f["resolved_trades"] >= self.cfg.min_resolved_trades)
                     & (f["volume_usdc"] >= self.cfg.min_volume_usdc)]
        if eligible.empty:
            return []
        s = score(eligible)
        return s.head(self.cfg.universe_size)["wallet"].tolist()


class ManualListSelector:
    """The original fixed list. Allowed live; backtests using it must be
    labeled biased — the engine tags results accordingly."""

    BIASED = True

    def __init__(self, wallets: list[str]):
        self.wallets = list(wallets)

    def select(self, trades: pd.DataFrame, resolutions: pd.DataFrame,
               as_of: pd.Timestamp) -> list[str]:
        return list(self.wallets)
