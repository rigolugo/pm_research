"""CLI: backfill real data, or run the synthetic / real backtest.

  python -m pm_research.cli synth-backtest            # edge check on synthetic world
  python -m pm_research.cli backfill --wallets w1 w2 --start 2025-01-01 --end 2025-12-31 --root ./data
  python -m pm_research.cli backtest --root ./data --start 2025-03-01 --end 2025-12-31
"""
from __future__ import annotations

import argparse
import json
from datetime import date

import pandas as pd

from .backtest import BacktestEngine
from .config import BacktestConfig, LatencyConfig
from .data.backfill import Backfiller
from .data.store import Store
from .data.synthetic import WorldConfig, generate
from .latency import ZERO_LATENCY, LatencyModel
from .selection import TrailingAlphaSelector


def _print_result(label: str, res) -> None:
    s = res.summary
    print(f"\n== {label} ==")
    print(f"  biased_selection : {res.biased_selection}")
    print(f"  signals/filled/lost_latency/skipped : "
          f"{res.n_signals}/{res.n_filled}/{res.n_lost_to_latency}/{res.n_skipped_risk}")
    for k in ("final_equity", "total_roi", "sharpe", "sortino",
              "max_drawdown", "profit_factor", "win_rate", "n_trades"):
        v = s[k]
        print(f"  {k:16s}: {v:.4f}" if isinstance(v, float) else f"  {k:16s}: {v}")


def _run_pair(trades, markets, resolutions, prices, cfg: BacktestConfig,
              prices_root: str | None = None) -> None:
    sel = TrailingAlphaSelector(cfg.selection)
    modeled = BacktestEngine(trades, markets, resolutions, prices, sel, cfg,
                             prices_root=prices_root).run()
    zero = BacktestEngine(trades, markets, resolutions, prices, sel, cfg,
                          latency_model=LatencyModel(ZERO_LATENCY),
                          prices_root=prices_root).run()
    _print_result("ZERO-LATENCY (upper bound — do not believe)", zero)
    _print_result("MODELED LATENCY (the number that counts)", modeled)
    gap = zero.summary["total_roi"] - modeled.summary["total_roi"]
    print(f"\n  latency cost: {gap:.4f} ROI given away to detection delay + impact")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="pm_research")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("synth-backtest", help="run engine on synthetic world with known edge")
    sp.add_argument("--seed", type=int, default=7)

    bp = sub.add_parser("backfill", help="trades + markets + resolutions + prices")
    bp.add_argument("--wallets", nargs="+", required=True)
    bp.add_argument("--start", type=date.fromisoformat, required=True)
    bp.add_argument("--end", type=date.fromisoformat, required=True)
    bp.add_argument("--root", default="./data")
    bp.add_argument("--provider", choices=["urllib", "polymarket-apis", "aiopolymarket"],
                    default="urllib",
                    help="urllib = zero-dependency reference implementation")
    bp.add_argument("--price-freq", default="1h")
    bp.add_argument("--skip-bots-over", type=int, default=None,
                    help="skip deep-history walk for wallets over N trades (bots)")
    bp.add_argument("--resume", action="store_true",
                    help="skip wallets already covered for [start, end] in --root "
                         "(incl. bot-skip markers); lets a killed run continue")

    dp = sub.add_parser("discover", help="build candidate wallet pool from high-volume markets")
    dp.add_argument("--markets", type=int, default=40)
    dp.add_argument("--per-market-pages", type=int, default=20)
    dp.add_argument("--min-trades", type=int, default=10)
    dp.add_argument("--min-volume", type=float, default=1000.0)
    dp.add_argument("--max-trades-per-day", type=float, default=200.0)
    dp.add_argument("--top", type=int, default=250)
    dp.add_argument("--out", default="wallets.txt")
    dp.add_argument("--csv", default="candidates.csv")

    tp = sub.add_parser("backtest")
    tp.add_argument("--root", default="./data")
    tp.add_argument("--start", type=date.fromisoformat, required=True)
    tp.add_argument("--end", type=date.fromisoformat, required=True)

    args = ap.parse_args(argv)

    if args.cmd == "synth-backtest":
        from .config import ConsensusConfig, RiskConfig, SelectionConfig
        w = generate(WorldConfig(seed=args.seed))
        cfg = BacktestConfig(
            start=w.trades["traded_at"].min().date(),
            end=w.resolutions["resolved_at"].max().date(),
            seed=args.seed,
            # the synthetic world is sparser than production reality, so the
            # eligibility gates are scaled down to match its trade density
            selection=SelectionConfig(universe_size=12, min_resolved_trades=5,
                                      min_volume_usdc=100.0),
            consensus=ConsensusConfig(min_unique_traders=3, min_weighted_score=0.4),
            risk=RiskConfig(size_fraction=0.02, max_open_positions=30))
        _run_pair(w.trades, w.markets, w.resolutions, w.prices, cfg)

    elif args.cmd == "discover":
        from .data.discovery import DiscoveryConfig, discover
        cfg = DiscoveryConfig(top_markets=args.markets,
                              per_market_pages=args.per_market_pages,
                              min_trades=args.min_trades,
                              min_volume_usdc=args.min_volume,
                              max_trades_per_day=args.max_trades_per_day,
                              top_n=args.top)
        cand = discover(Backfiller(Store("./_discovery_tmp")), cfg)
        cand.to_csv(args.csv, index=False)
        with open(args.out, "w") as f:
            f.write("\n".join(cand["wallet"]) + "\n")
        print(f"{len(cand)} candidates -> {args.out} (stats in {args.csv})")
        if len(cand):
            print(cand.head(10).to_string(index=False))

    elif args.cmd == "backfill":
        store = Store(args.root)
        if args.provider == "urllib":
            report = Backfiller(store, max_wallet_trades=args.skip_bots_over
                                ).backfill_full(
                args.wallets, args.start, args.end, price_freq=args.price_freq,
                resume=args.resume)
        else:
            if args.resume:
                raise SystemExit("--resume is only supported with --provider urllib")
            if args.provider == "polymarket-apis":
                from .data.providers import PolymarketApisProvider as P
            else:
                from .data.providers import AiopolymarketProvider as P
            p = P(store)
            counts = {w: p.backfill_wallet(w, args.start, args.end)
                      for w in args.wallets}
            trades = store.load_trades(args.wallets)
            cids = sorted(trades["condition_id"].unique().tolist())
            nm, nr = p.backfill_markets(cids)
            np_ = p.backfill_prices_from_prints(cids, freq=args.price_freq)
            report = {"trades_per_wallet": counts, "markets": nm,
                      "resolutions": nr, "price_rows": np_,
                      "condition_ids": len(cids)}
        print(json.dumps(report, indent=2))

    elif args.cmd == "backtest":
        store = Store(args.root)
        trades = store.load_trades()
        wallets = sorted(trades["wallet"].unique().tolist())
        ok, gaps = store.coverage_ok(wallets, args.start, args.end)
        if not ok:
            raise SystemExit(f"REFUSING TO RUN: backfill coverage gaps for {gaps}")
        cfg = BacktestConfig(start=args.start, end=args.end)
        # lazy per-market price loading -- avoids 15M-row frame in RAM
        _run_pair(trades, store.load_markets(), store.load_resolutions(),
                  pd.DataFrame(columns=["condition_id", "ts", "yes_price"]),
                  cfg, prices_root=args.root)


if __name__ == "__main__":
    main()
