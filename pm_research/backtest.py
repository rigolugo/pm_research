"""Event-loop backtest engine. The whole point of phase 1.

Daily steps over [config.start, config.end]:
  1. (weekly) re-select the wallet universe AS OF that day — no fixed winner
     lists; ManualListSelector runs are tagged biased_selection=True.
  2. score the universe point-in-time.
  3. detect consensus among universe trades in the trailing window.
  4. size (bootstrap fraction, or fractional Kelly if a fitted calibrator is
     supplied) and fill through the LatencyModel.
  5. close positions at resolution payout; mark to market daily.

Run it twice — once with ZERO_LATENCY, once with the modeled config — and
believe only the second number.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .calibration import IsotonicCalibrator
from .config import BacktestConfig
from .consensus import CooldownFilter, Signal, detect
from .features import compute_features
from .latency import LatencyModel, PriceBook
from .metrics import summarize
from .scoring import score


@dataclass
class Position:
    condition_id: str
    outcome: str
    shares: float
    entry_price: float
    cost_usdc: float
    opened_at: pd.Timestamp
    signal_raw_confidence: float


@dataclass
class BacktestResult:
    config: dict
    summary: dict
    equity: pd.Series
    trade_log: pd.DataFrame          # one row per closed position
    n_signals: int = 0
    n_filled: int = 0
    n_lost_to_latency: int = 0
    n_skipped_risk: int = 0
    biased_selection: bool = False
    universe_history: list = field(default_factory=list)


def _kelly_fraction(p: float, entry_price: float, fraction: float) -> float:
    """Binary-market fractional Kelly. b = (1-price)/price."""
    b = (1.0 - entry_price) / entry_price
    f_star = p - (1.0 - p) / b
    return max(0.0, f_star) * fraction


class BacktestEngine:
    def __init__(self, trades: pd.DataFrame, markets: pd.DataFrame,
                 resolutions: pd.DataFrame, prices: pd.DataFrame,
                 selector, config: BacktestConfig,
                 calibrator: IsotonicCalibrator | None = None,
                 latency_model: LatencyModel | None = None,
                 prices_root: str | None = None):
        self.trades = trades.sort_values("traded_at").reset_index(drop=True)
        self.markets = markets
        self.resolutions = resolutions
        self.selector = selector
        self.cfg = config
        self.calibrator = calibrator
        self.book = PriceBook(prices, markets, prices_root=prices_root,
                              trades=self.trades)
        self.latency = latency_model or LatencyModel(config.latency)
        self._res_by_day = resolutions.assign(
            day=resolutions["resolved_at"].dt.floor("D"))
        self._winner = dict(zip(resolutions["condition_id"],
                                resolutions["winning_outcome"]))

    # ------------------------------------------------------------------
    def run(self) -> BacktestResult:
        cfg = self.cfg
        cash = cfg.initial_capital
        open_pos: dict[tuple[str, str], Position] = {}
        closed_rows: list[dict] = []
        equity_idx, equity_val = [], []
        cooldown = CooldownFilter(cfg.consensus.cooldown_hours_per_market)
        universe: list[str] = []
        scores = pd.DataFrame()
        result = BacktestResult(config=cfg.to_dict(), summary={}, equity=pd.Series(dtype=float),
                                trade_log=pd.DataFrame(),
                                biased_selection=bool(getattr(self.selector, "BIASED", False)))

        days = pd.date_range(pd.Timestamp(cfg.start, tz="UTC"),
                             pd.Timestamp(cfg.end, tz="UTC"), freq="D")
        last_rebalance: pd.Timestamp | None = None

        for day in days:
            as_of = day + pd.Timedelta(hours=23, minutes=59)

            # 1. universe selection (point-in-time, weekly)
            if (last_rebalance is None or
                    (day - last_rebalance).days >= cfg.selection.rebalance_interval_days):
                universe = self.selector.select(self.trades, self.resolutions, as_of)
                last_rebalance = day
                result.universe_history.append((day, list(universe)))
                if universe:
                    f = compute_features(self.trades, self.resolutions, as_of,
                                         cfg.selection.lookback_days)
                    scores = score(f[f["wallet"].isin(universe)])

            # 2. close positions whose markets resolved today
            resolved_today = self._res_by_day[self._res_by_day["day"] == day]
            for _, r in resolved_today.iterrows():
                for outcome in ("YES", "NO"):
                    key = (r["condition_id"], outcome)
                    pos = open_pos.pop(key, None)
                    if pos is None:
                        continue
                    payout = pos.shares * (1.0 if outcome == r["winning_outcome"] else 0.0)
                    pnl = payout - pos.cost_usdc
                    cash += payout
                    closed_rows.append({
                        "condition_id": pos.condition_id, "outcome": pos.outcome,
                        "entry_price": pos.entry_price, "cost_usdc": pos.cost_usdc,
                        "payout_usdc": payout, "pnl_usdc": pnl,
                        "raw_confidence": pos.signal_raw_confidence,
                        "was_correct": outcome == r["winning_outcome"],
                        "opened_at": pos.opened_at, "closed_at": r["resolved_at"]})

            # 3. signals from consensus in the trailing window
            if universe:
                equity_now = cash + self._open_value(open_pos, as_of)
                for sig in detect(self.trades, universe, scores, as_of, cfg.consensus):
                    result.n_signals += 1
                    if not cooldown.admit(sig):
                        continue
                    status, cash = self._try_open(sig, cash, equity_now, open_pos)
                    if status == "filled":
                        result.n_filled += 1
                    elif status == "latency":
                        result.n_lost_to_latency += 1
                    else:
                        result.n_skipped_risk += 1

            # 4. mark to market
            equity_idx.append(day)
            equity_val.append(cash + self._open_value(open_pos, as_of))

        equity = pd.Series(equity_val, index=pd.DatetimeIndex(equity_idx), name="equity")
        trade_log = pd.DataFrame(closed_rows)
        pnls = trade_log["pnl_usdc"] if len(trade_log) else pd.Series(dtype=float)
        result.equity = equity
        result.trade_log = trade_log
        result.summary = summarize(equity, pnls)
        return result

    # ------------------------------------------------------------------
    def _try_open(self, sig: Signal, cash: float, equity_now: float,
                  open_pos: dict) -> tuple[str, float]:
        cfg = self.cfg
        key = (sig.condition_id, sig.outcome)
        if key in open_pos or len(open_pos) >= cfg.risk.max_open_positions:
            return "risk", cash
        # resolved markets can't be entered
        winner_known_at = self.resolutions.loc[
            self.resolutions["condition_id"] == sig.condition_id, "resolved_at"]
        if len(winner_known_at) and sig.detected_at >= winner_known_at.iloc[0]:
            return "risk", cash

        # sizing
        if cfg.risk.use_kelly and self.calibrator is not None and self.calibrator.ready:
            p = float(self.calibrator.apply(sig.raw_confidence))
            frac = _kelly_fraction(p, sig.leaders_avg_entry, cfg.risk.kelly_fraction)
            if frac <= 0.0:
                return "risk", cash  # negative edge post-calibration
            frac = min(frac, cfg.risk.max_position_fraction)
        else:
            frac = cfg.risk.size_fraction  # bootstrap humility
        size_usdc = min(frac * equity_now, cash)
        if size_usdc < 1.0:
            return "risk", cash

        fill = self.latency.apply(condition_id=sig.condition_id, outcome=sig.outcome,
                                  detected_at=sig.detected_at,
                                  leaders_avg_entry=sig.leaders_avg_entry,
                                  size_usdc=size_usdc, book=self.book)
        if not fill.filled:
            return "latency", cash
        shares = size_usdc / fill.fill_price
        open_pos[key] = Position(sig.condition_id, sig.outcome, shares,
                                 fill.fill_price, size_usdc, fill.fill_at,
                                 sig.raw_confidence)
        return "filled", cash - size_usdc

    def _open_value(self, open_pos: dict, as_of: pd.Timestamp) -> float:
        total = 0.0
        for pos in open_pos.values():
            p = self.book.price_at(pos.condition_id, pos.outcome, as_of)
            total += pos.shares * (p if p is not None else pos.entry_price)
        return total
