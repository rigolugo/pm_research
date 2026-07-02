"""Exit-mirroring backtest — the copyable-vs-uncopyable decider.

CONTEXT. The lifecycle analysis showed the selected wallets are profitable by
their ACTUAL trading (buys + sells) but look like losers under the pipeline's
hold-to-resolution assumption. Their profit lives in their EXITS. The open
question: can a latency-bound copier capture that, or is it uncopyable
market-making P&L?

This script runs the copy strategy two ways on the SAME signals and reports
both, so the comparison is apples-to-apples:

  HOLD model     : enter on consensus BUY, hold to resolution  (the original)
  EXIT-MIRROR    : enter on consensus BUY, AND exit when a quorum of the
                   leaders who entered subsequently SELLs that outcome —
                   at a latency-delayed, impact-adjusted price.

If EXIT-MIRROR flips the modeled-latency ROI positive while HOLD is negative,
the wallets' skill is COPYABLE via exit-mirroring and the project is alive.
If EXIT-MIRROR stays negative, the profit is microstructure / liquidity
provision -- uncopyable -- and the no-go stands, now well understood.

HONESTY NOTES baked in:
  - Both models pay the SAME entry latency + impact. The only difference is
    the exit path. No free lunch slipped into the exit.
  - Exits also pay latency + impact (you sell late and cross the spread too).
  - Positions never closed by a mirrored exit fall through to resolution, so
    EXIT-MIRROR is strictly a superset behaviour, not a different strategy.
  - This reuses the SAME selector, consensus, scoring, latency model and
    config as the real engine. It is not a more permissive re-parameterisation.

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/exit_mirror_backtest.py --root ~/data
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.config import BacktestConfig
from pm_research.selection import TrailingAlphaSelector
from pm_research.scoring import score
from pm_research.features import compute_features
from pm_research.consensus import detect, CooldownFilter
from pm_research.latency import LatencyModel, PriceBook, ZERO_LATENCY
from pm_research.metrics import summarize


@dataclass
class Pos:
    condition_id: str
    outcome: str
    shares: float
    entry_price: float
    cost_usdc: float
    opened_at: pd.Timestamp
    triggers: frozenset      # the universe wallets whose BUYs triggered entry


def _exit_quorum_time(trades, cid, outcome, triggers, after, cfg,
                      quorum_frac=0.5):
    """Earliest time at which >= quorum_frac of the triggering wallets have
    SOLD this outcome, after entry. None if they never collectively exit."""
    sells = trades[(trades["condition_id"] == cid)
                   & (trades["outcome"] == outcome)
                   & (trades["side"] == "SELL")
                   & (trades["wallet"].isin(triggers))
                   & (trades["traded_at"] > after)]
    if sells.empty:
        return None
    need = max(1, int(np.ceil(len(triggers) * quorum_frac)))
    # walk sells in time order, count distinct sellers, fire when quorum met
    seen = set()
    for _, s in sells.sort_values("traded_at").iterrows():
        seen.add(s["wallet"])
        if len(seen) >= need:
            return s["traded_at"]
    return None


def run(trades, resolutions, markets, cfg, root, latency, mirror_exits: bool):
    # Pass raw trades so worst_in_bar can price BOTH entry (buy) and exit (sell)
    # legs from real prints. mark-to-market still uses the neutral price_at().
    book = PriceBook(pd.DataFrame(), markets, prices_root=root, trades=trades)
    sel = TrailingAlphaSelector(cfg.selection)
    winner = dict(zip(resolutions["condition_id"], resolutions["winning_outcome"]))
    res_at = dict(zip(resolutions["condition_id"], resolutions["resolved_at"]))
    res_by_day = resolutions.assign(day=resolutions["resolved_at"].dt.floor("D"))

    cash = cfg.initial_capital
    open_pos: dict[tuple, Pos] = {}
    closed = []
    eq_idx, eq_val = [], []
    cooldown = CooldownFilter(cfg.consensus.cooldown_hours_per_market)
    universe, scores = [], pd.DataFrame()

    days = pd.date_range(pd.Timestamp(cfg.start, tz="UTC"),
                         pd.Timestamp(cfg.end, tz="UTC"), freq="D")
    last_rebalance = None
    n_signals = n_filled = n_latency = n_skipped = n_mirror_exits = 0

    def open_value(as_of):
        tot = 0.0
        for p in open_pos.values():
            q = book.price_at(p.condition_id, p.outcome, as_of)
            tot += p.shares * (q if q is not None else p.entry_price)
        return tot

    for day in days:
        as_of = day + pd.Timedelta(hours=23, minutes=59)

        if (last_rebalance is None or
                (day - last_rebalance).days >= cfg.selection.rebalance_interval_days):
            universe = sel.select(trades, resolutions, as_of)
            last_rebalance = day
            if universe:
                f = compute_features(trades, resolutions, as_of,
                                     cfg.selection.lookback_days)
                scores = score(f[f["wallet"].isin(universe)])

        # --- mirrored exits (only in exit-mirror mode) ---
        if mirror_exits and open_pos:
            for key in list(open_pos.keys()):
                p = open_pos[key]
                xt = _exit_quorum_time(trades, p.condition_id, p.outcome,
                                       p.triggers, p.opened_at, cfg)
                if xt is None or xt > as_of:
                    continue
                # exit pays latency + impact too: sell late, cross the spread.
                # SELL leg: side-aware worst_in_bar picks the adverse extreme for
                # a seller (YES sell -> bar-low; NO sell -> bar-high).
                exit_at = xt + pd.Timedelta(seconds=latency.cfg.detection_delay_seconds)
                px = book.fill_price_at(
                    p.condition_id, p.outcome, exit_at, side="sell",
                    intrabar_fill_policy=latency.cfg.intrabar_fill_policy)
                if px is None:
                    continue
                liq = book.liquidity(p.condition_id)
                impact = (min(latency.cfg.impact_cap,
                              latency.cfg.impact_k * p.cost_usdc / liq)
                          if liq > 0 else latency.cfg.impact_cap)
                # selling INTO the book: impact works against you (lower fill)
                exit_price = float(np.clip(px - impact, 0.001, 0.999))
                proceeds = p.shares * exit_price
                cash += proceeds
                closed.append({"condition_id": p.condition_id, "outcome": p.outcome,
                               "entry_price": p.entry_price, "cost_usdc": p.cost_usdc,
                               "payout_usdc": proceeds, "pnl_usdc": proceeds - p.cost_usdc,
                               "exit_kind": "mirrored_sell"})
                del open_pos[key]
                n_mirror_exits += 1

        # --- close positions whose markets resolved today ---
        rtoday = res_by_day[res_by_day["day"] == day]
        for _, r in rtoday.iterrows():
            for outcome in ("YES", "NO"):
                key = (r["condition_id"], outcome)
                p = open_pos.pop(key, None)
                if p is None:
                    continue
                payout = p.shares * (1.0 if outcome == r["winning_outcome"] else 0.0)
                cash += payout
                closed.append({"condition_id": p.condition_id, "outcome": p.outcome,
                               "entry_price": p.entry_price, "cost_usdc": p.cost_usdc,
                               "payout_usdc": payout, "pnl_usdc": payout - p.cost_usdc,
                               "exit_kind": "resolution"})

        # --- entries from consensus (identical to the real engine) ---
        if universe:
            equity_now = cash + open_value(as_of)
            for sig in detect(trades, universe, scores, as_of, cfg.consensus):
                n_signals += 1
                if not cooldown.admit(sig):
                    continue
                key = (sig.condition_id, sig.outcome)
                if key in open_pos or len(open_pos) >= cfg.risk.max_open_positions:
                    n_skipped += 1
                    continue
                wk = res_at.get(sig.condition_id)
                if wk is not None and sig.detected_at >= pd.Timestamp(wk):
                    n_skipped += 1
                    continue
                size = min(cfg.risk.size_fraction * equity_now, cash)
                if size < 1.0:
                    n_skipped += 1
                    continue
                fill = latency.apply(condition_id=sig.condition_id, outcome=sig.outcome,
                                     detected_at=sig.detected_at,
                                     leaders_avg_entry=sig.leaders_avg_entry,
                                     size_usdc=size, book=book)
                if not fill.filled:
                    n_latency += 1
                    continue
                # capture the triggering wallets for exit mirroring
                lo = sig.detected_at - pd.Timedelta(hours=cfg.consensus.window_hours)
                trig = frozenset(trades[(trades["condition_id"] == sig.condition_id)
                                        & (trades["outcome"] == sig.outcome)
                                        & (trades["side"] == "BUY")
                                        & (trades["wallet"].isin(universe))
                                        & (trades["traded_at"] > lo)
                                        & (trades["traded_at"] <= sig.detected_at)
                                        ]["wallet"].unique())
                shares = size / fill.fill_price
                open_pos[key] = Pos(sig.condition_id, sig.outcome, shares,
                                    fill.fill_price, size, fill.fill_at, trig)
                cash -= size
                n_filled += 1

        eq_idx.append(day)
        eq_val.append(cash + open_value(as_of))

    equity = pd.Series(eq_val, index=pd.DatetimeIndex(eq_idx), name="equity")
    log = pd.DataFrame(closed)
    pnls = log["pnl_usdc"] if len(log) else pd.Series(dtype=float)
    summ = summarize(equity, pnls)
    summ["_signals"] = n_signals
    summ["_filled"] = n_filled
    summ["_latency"] = n_latency
    summ["_skipped"] = n_skipped
    summ["_mirror_exits"] = n_mirror_exits
    return summ


def _print(label, s):
    print(f"\n== {label} ==")
    print(f"  signals/filled/lost_latency/skipped/mirror_exits : "
          f"{s['_signals']}/{s['_filled']}/{s['_latency']}/{s['_skipped']}/{s['_mirror_exits']}")
    for k in ("final_equity", "total_roi", "sharpe", "sortino",
              "max_drawdown", "profit_factor", "win_rate", "n_trades"):
        v = s.get(k)
        print(f"  {k:16s}: {v:.4f}" if isinstance(v, float) else f"  {k:16s}: {v}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)
    res = store.load_resolutions()
    markets = store.load_markets()
    cfg = BacktestConfig(start=args.start, end=args.end)
    # Side-aware fill pricing is now implemented (PriceBook.fill_price_at with
    # side="buy"/"sell"), and run() passes raw trades into PriceBook, so both the
    # entry (buy) and the mirrored exit (sell) legs price worst_in_bar correctly.
    # The earlier temporary intrabar_fill_policy="close" pin is therefore removed:
    # this script now uses the default policy (worst_in_bar). Mark-to-market still
    # uses the neutral price_at(). HOLD and EXIT-MIRROR both run under the same
    # config, so the comparison stays apples-to-apples.
    modeled = LatencyModel(cfg.latency)

    print("Running HOLD model (original: enter, hold to resolution)...")
    hold = run(trades, res, markets, cfg, args.root, modeled, mirror_exits=False)
    print("Running EXIT-MIRROR model (enter, exit when leaders sell)...")
    mirror = run(trades, res, markets, cfg, args.root, modeled, mirror_exits=True)

    _print("HOLD-TO-RESOLUTION (modeled latency)", hold)
    _print("EXIT-MIRROR (modeled latency)", mirror)

    print("\n=== VERDICT ===")
    dh, dm = hold["total_roi"], mirror["total_roi"]
    print(f"  hold ROI   : {dh:+.4f}")
    print(f"  mirror ROI : {dm:+.4f}")
    if dm > 0 and dh <= 0:
        print("  >>> EXIT-MIRRORING FLIPS THE EDGE POSITIVE.")
        print("  >>> The wallets' skill is COPYABLE by mirroring their exits.")
        print("  >>> This is a real, defensible path forward. Next: confirm on")
        print("  >>> a held-out date split and stress the exit quorum / delay.")
    elif dm > dh:
        print(f"  >>> Exit-mirroring improves ROI by {dm - dh:+.4f} but does not")
        print("  >>> (yet) clear zero. Partial capture of exit alpha. Worth")
        print("  >>> tuning the exit quorum/timing, but not yet a Go.")
    else:
        print("  >>> Exit-mirroring does NOT help. The wallets' profit is not")
        print("  >>> capturable by mirroring their sells at realistic latency —")
        print("  >>> consistent with market-making / liquidity-provision P&L.")
        print("  >>> The no-go stands, now for a well-understood reason: the")
        print("  >>> edge is uncopyable microstructure, not slow alpha.")
    print("\n  Both models paid identical entry latency+impact; exits paid")
    print("  latency+impact too. The difference is purely the exit path.")


if __name__ == "__main__":
    main()
