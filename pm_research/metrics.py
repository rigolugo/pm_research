"""Standard performance metrics over an equity curve and trade log."""
from __future__ import annotations

import numpy as np
import pandas as pd

PERIODS_PER_YEAR = 365  # daily equity curve


def daily_returns(equity: pd.Series) -> pd.Series:
    return equity.pct_change().dropna()


def sharpe(returns: pd.Series, risk_free: float = 0.0) -> float:
    if len(returns) < 2 or float(returns.std(ddof=1)) == 0.0:
        return 0.0
    ex = returns - risk_free / PERIODS_PER_YEAR
    return float(ex.mean() / ex.std(ddof=1) * np.sqrt(PERIODS_PER_YEAR))


def sortino(returns: pd.Series, risk_free: float = 0.0) -> float:
    ex = returns - risk_free / PERIODS_PER_YEAR
    downside = ex[ex < 0]
    if len(returns) < 2 or len(downside) == 0:
        return 0.0
    dd = float(np.sqrt((downside ** 2).mean()))
    if dd == 0.0:
        return 0.0
    return float(ex.mean() / dd * np.sqrt(PERIODS_PER_YEAR))


def max_drawdown(equity: pd.Series) -> float:
    """Max peak-to-trough drawdown as a positive fraction (0.25 = -25%)."""
    if len(equity) == 0:
        return 0.0
    peak = equity.cummax()
    dd = (peak - equity) / peak
    return float(dd.max())


def profit_factor(pnls: pd.Series) -> float:
    wins = float(pnls[pnls > 0].sum())
    losses = float(-pnls[pnls < 0].sum())
    if losses == 0.0:
        return float("inf") if wins > 0 else 0.0
    return wins / losses


def summarize(equity: pd.Series, trade_pnls: pd.Series) -> dict:
    r = daily_returns(equity)
    total_roi = float(equity.iloc[-1] / equity.iloc[0] - 1.0) if len(equity) else 0.0
    return {
        "final_equity": float(equity.iloc[-1]) if len(equity) else 0.0,
        "total_roi": total_roi,
        "sharpe": sharpe(r),
        "sortino": sortino(r),
        "max_drawdown": max_drawdown(equity),
        "profit_factor": profit_factor(trade_pnls),
        "win_rate": float((trade_pnls > 0).mean()) if len(trade_pnls) else 0.0,
        "n_trades": int(len(trade_pnls)),
    }
