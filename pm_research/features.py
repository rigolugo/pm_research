"""Per-trader features, computed strictly point-in-time.

`compute_features(trades, resolutions, as_of, lookback_days)` returns one row
per wallet using ONLY trades with traded_at <= as_of and resolutions with
resolved_at <= as_of. That guarantee is what the no-lookahead tests enforce.

Phase 1 keeps the feature set to what scoring/selection actually consume.
The long tail of v1's 40-feature vector returns in phase 2 if (and only if)
the core loop shows edge.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FEATURE_COLS = ["wallet", "resolved_trades", "total_trades", "volume_usdc",
                "roi", "win_rate", "avg_entry_price", "conviction",
                "market_concentration", "trades_per_day", "automation_proxy"]


def _point_in_time(trades: pd.DataFrame, resolutions: pd.DataFrame,
                   as_of: pd.Timestamp, lookback_days: int):
    lo = as_of - pd.Timedelta(days=lookback_days)
    t = trades[(trades["traded_at"] > lo) & (trades["traded_at"] <= as_of)].copy()
    r = resolutions[resolutions["resolved_at"] <= as_of]
    return t, r


def compute_features(trades: pd.DataFrame, resolutions: pd.DataFrame,
                     as_of: pd.Timestamp, lookback_days: int = 90) -> pd.DataFrame:
    t, r = _point_in_time(trades, resolutions, as_of, lookback_days)
    if t.empty:
        return pd.DataFrame(columns=FEATURE_COLS)

    t = t.merge(r[["condition_id", "winning_outcome"]], on="condition_id", how="left")
    t["resolved"] = t["winning_outcome"].notna()
    t["won"] = t["resolved"] & (t["outcome"] == t["winning_outcome"])
    # per-trade ROI for a BUY: payout(1 or 0) per share vs price paid.
    payout = t["won"].astype(float)
    t["trade_roi"] = np.where(t["resolved"], (payout - t["price"]) / t["price"], np.nan)

    rows = []
    span_days = max(lookback_days, 1)
    for wallet, g in t.groupby("wallet"):
        res = g[g["resolved"]]
        n_res = len(res)
        vol = float(g["size_usdc"].sum())
        # volume-weighted ROI over resolved trades
        roi = (float(np.average(res["trade_roi"], weights=res["size_usdc"]))
               if n_res else np.nan)
        win_rate = float(res["won"].mean()) if n_res else np.nan
        avg_entry = float(g["price"].mean())
        # conviction: willingness to buy genuinely uncertain prices
        conviction = float(1.0 - abs(g["price"] - 0.5).mean() * 2.0)
        share = g.groupby("condition_id")["size_usdc"].sum() / vol if vol else pd.Series(dtype=float)
        hhi = float((share ** 2).sum()) if len(share) else 0.0
        freq = len(g) / span_days
        # crude automation proxy: very high frequency + near-certain entries
        near_certain = float(((g["price"] < 0.05) | (g["price"] > 0.95)).mean())
        automation = float(min(1.0, freq / 50.0) * 0.5 + near_certain * 0.5)
        rows.append({"wallet": wallet, "resolved_trades": n_res,
                     "total_trades": len(g), "volume_usdc": vol, "roi": roi,
                     "win_rate": win_rate, "avg_entry_price": avg_entry,
                     "conviction": conviction, "market_concentration": hhi,
                     "trades_per_day": freq, "automation_proxy": automation})
    return pd.DataFrame(rows, columns=FEATURE_COLS)
