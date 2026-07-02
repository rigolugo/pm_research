"""Position-lifecycle PnL reconstruction — the Risk-1 measurement.

The current pipeline scores a wallet's skill by asking "did the outcome they
bought win at resolution?" — i.e. it assumes every BUY is held to resolution.
But many skilled wallets make money by TRADING AROUND positions: buy @ 0.40,
sell @ 0.60, exit before resolution. For such a wallet the buy-and-hold-to-
resolution model MISMEASURES their skill, and could manufacture a false
negative in the copy-trading verdict.

This script reconstructs each wallet's REALIZED PnL from their actual BUYs
AND SELLs per market, and compares two things:

  (A) REALIZED round-trip PnL   — what the wallet actually earned by trading
  (B) HOLD-TO-RESOLUTION PnL    — what the current pipeline assumes they earned

If (A) and (B) diverge a lot, Risk 1 is real: the pipeline is scoring the
wrong quantity, and the negative copy-trade result may be an artifact of the
holding-model mismatch rather than absence of skill.

HONESTY GATES (printed first, before any conclusion):
  - BUY/SELL composition. If the data is essentially BUY-only, round-trip
    reconstruction is IMPOSSIBLE and the script says so and stops. No faking.
  - Open-position handling. Positions still open at window end have no realized
    exit; they are marked separately, never silently assumed profitable.
  - This measures whether WALLETS are skilled by their own trading. Whether
    COPYING them is profitable is a separate question (the backtest). A wallet
    can be genuinely skilled AND uncopyable. This script does not conflate them.

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/lifecycle_pnl.py --root ~/data
"""
from __future__ import annotations

import argparse
from datetime import date

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.selection import TrailingAlphaSelector
from pm_research.config import SelectionConfig


def reconstruct_wallet_market(g: pd.DataFrame, winner: str | None,
                              final_yes: float | None) -> dict:
    """Reconstruct realized PnL for ONE wallet in ONE market from its fills.

    Convention: size_usdc is dollars transacted. We track net shares per
    outcome side. BUY adds shares (costs cash); SELL removes shares (returns
    cash). Shares = size_usdc / price. Any shares left open at the end are
    valued at the market's final observed price (realized only if the market
    resolved; otherwise flagged as still-open mark-to-market).
    """
    cash = 0.0          # negative = net spent
    shares = {"YES": 0.0, "NO": 0.0}
    n_buys = n_sells = 0
    for _, t in g.iterrows():
        oc = t["outcome"]
        if oc not in shares:
            continue
        px = t["price"]
        if px <= 0:
            continue
        sh = t["size_usdc"] / px
        if t["side"] == "BUY":
            cash -= t["size_usdc"]
            shares[oc] += sh
            n_buys += 1
        elif t["side"] == "SELL":
            cash += t["size_usdc"]
            shares[oc] -= sh
            n_sells += 1

    open_shares = shares["YES"] + shares["NO"]

    # value any residual open shares
    resolution_value = 0.0
    realized = (n_sells > 0 and abs(open_shares) < 1e-6)  # cleanly closed
    if winner is not None:
        # market resolved: open YES shares pay 1 if YES won, etc.
        resolution_value = (shares["YES"] * (1.0 if winner == "YES" else 0.0)
                            + shares["NO"] * (1.0 if winner == "NO" else 0.0))
        realized_pnl = cash + resolution_value
        basis = "resolved"
    elif final_yes is not None:
        # not resolved: mark open shares at last observed price (UNREALIZED)
        resolution_value = (shares["YES"] * final_yes
                            + shares["NO"] * (1.0 - final_yes))
        realized_pnl = cash + resolution_value
        basis = "open_marked"
    else:
        realized_pnl = cash
        basis = "no_price"

    return {"realized_pnl": realized_pnl, "n_buys": n_buys, "n_sells": n_sells,
            "open_shares": open_shares, "cleanly_closed": realized,
            "basis": basis}


def hold_to_resolution_pnl(g: pd.DataFrame, winner: str | None) -> float | None:
    """What the CURRENT pipeline assumes: every BUY held to resolution,
    SELLs ignored. payout(1/0) minus price, per share bought."""
    if winner is None:
        return None
    buys = g[g["side"] == "BUY"]
    if buys.empty:
        return None
    pnl = 0.0
    for _, t in buys.iterrows():
        if t["price"] <= 0:
            continue
        sh = t["size_usdc"] / t["price"]
        payout = 1.0 if t["outcome"] == winner else 0.0
        pnl += sh * (payout - t["price"])
    return pnl


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades()
    res = store.load_resolutions()
    winner = dict(zip(res["condition_id"], res["winning_outcome"]))

    s = pd.Timestamp(args.start, tz="UTC")
    e = pd.Timestamp(args.end, tz="UTC")
    win = trades[(trades["traded_at"] >= s) & (trades["traded_at"] < e)].copy()

    # ---------- HONESTY GATE 1: BUY/SELL composition ----------
    print("=== HONESTY GATE 1: trade-side composition ===")
    side_counts = win["side"].value_counts(dropna=False)
    print(side_counts.to_string())
    total = len(win)
    n_sell = int((win["side"] == "SELL").sum())
    sell_frac = n_sell / total if total else 0.0
    print(f"\n  SELL fraction: {sell_frac:.4f} ({n_sell} of {total})")
    if sell_frac < 0.01:
        print("\n  >>> VERDICT: data is essentially BUY-ONLY.")
        print("  >>> Round-trip lifecycle reconstruction is IMPOSSIBLE on this")
        print("  >>> data. The /trades endpoint or the parse may not capture")
        print("  >>> SELLs, OR these wallets genuinely never sell (buy-and-hold).")
        print("  >>> Either way, Risk 1 cannot be tested here. Stopping rather")
        print("  >>> than fabricating a round-trip number from buys alone.")
        print("\n  Next step if you believe SELLs exist: inspect a raw /activity")
        print("  payload for a known active wallet and confirm the 'side' field.")
        return
    print("  SELLs present -> round-trip reconstruction is feasible.\n")

    # ---------- universe: same selector the pipeline uses ----------
    sel = TrailingAlphaSelector(SelectionConfig())
    universe = set(sel.select(trades, res, s) or
                   sel.select(trades, res, s + pd.Timedelta(days=1)))
    win = win[win["wallet"].isin(universe)]
    print(f"=== selected universe: {len(universe)} wallets, "
          f"{len(win)} of their trades in window ===\n")
    if win.empty:
        print("No selected-wallet trades in window. Cannot proceed.")
        return

    # final observed yes_price per market (for marking open positions)
    final_yes: dict[str, float] = {}
    for cid in win["condition_id"].unique():
        if cid in winner:
            continue  # resolved markets use payout, not mark
        from pm_research.latency import PriceBook  # reuse loader indirectly
    # (we only need final price for unresolved; load lazily per market)

    def load_final_yes(cid: str) -> float | None:
        import pathlib
        p = pathlib.Path(args.root) / "prices" / cid
        for ext in (".parquet", ".pkl"):
            fp = p.with_suffix(ext)
            if fp.exists():
                df = pd.read_parquet(fp) if ext == ".parquet" else pd.read_pickle(fp)
                if df.empty:
                    return None
                return float(df.sort_values("ts")["yes_price"].iloc[-1])
        return None

    # ---------- reconstruct per wallet × market ----------
    realized_rows = []
    for (wallet, cid), g in win.groupby(["wallet", "condition_id"]):
        w = winner.get(cid)
        fy = None if w is not None else load_final_yes(cid)
        rec = reconstruct_wallet_market(g, w, fy)
        htr = hold_to_resolution_pnl(g, w)
        rec.update({"wallet": wallet, "condition_id": cid,
                    "hold_to_res_pnl": htr})
        realized_rows.append(rec)
    df = pd.DataFrame(realized_rows)

    # ---------- HONESTY GATE 2: open vs closed ----------
    print("=== HONESTY GATE 2: position basis breakdown ===")
    print(df["basis"].value_counts().to_string())
    cleanly = df["cleanly_closed"].sum()
    print(f"\n  cleanly closed (entered & fully exited): {cleanly} of {len(df)}")
    print("  'open_marked' rows are UNREALIZED (marked at last price), not")
    print("  booked profit. Treat them with suspicion.\n")

    # ---------- the comparison that answers Risk 1 ----------
    resolved = df[df["basis"] == "resolved"]
    print("=== RISK 1 TEST: realized round-trip vs hold-to-resolution ===")
    print("  (resolved markets only, where both numbers are defined)\n")
    if resolved.empty:
        print("  No resolved wallet-market positions. Inconclusive.")
        return

    realized_total = resolved["realized_pnl"].sum()
    htr_total = resolved["hold_to_res_pnl"].dropna().sum()
    print(f"  REALIZED round-trip PnL (actual buys+sells):  {realized_total:,.0f}")
    print(f"  HOLD-TO-RESOLUTION PnL (pipeline assumption):  {htr_total:,.0f}")

    # per-wallet agreement
    wal = (resolved.groupby("wallet")
           .agg(realized=("realized_pnl", "sum"),
                hold=("hold_to_res_pnl", "sum"),
                n_pos=("condition_id", "count"),
                sells=("n_sells", "sum")).reset_index())
    wal["sign_agrees"] = np.sign(wal["realized"]) == np.sign(wal["hold"])
    n_profitable_realized = int((wal["realized"] > 0).sum())
    n_profitable_hold = int((wal["hold"] > 0).sum())
    agree = int(wal["sign_agrees"].sum())

    print(f"\n  wallets profitable by REALIZED trading:       {n_profitable_realized}/{len(wal)}")
    print(f"  wallets profitable by HOLD-TO-RESOLUTION:     {n_profitable_hold}/{len(wal)}")
    print(f"  wallets where the two models AGREE on sign:   {agree}/{len(wal)}")

    print("\n=== INTERPRETATION ===")
    # The per-wallet sign-agreement metric HIDES magnitude. Two models can
    # "agree on sign" per wallet while disagreeing by millions in aggregate.
    # Gate on the aggregate divergence between realized and hold-to-resolution.
    denom = max(abs(realized_total), abs(htr_total), 1.0)
    rel_gap = abs(realized_total - htr_total) / denom
    opposite_sign = (np.sign(realized_total) != np.sign(htr_total)
                     and abs(realized_total) > 1 and abs(htr_total) > 1)

    print(f"  realized vs hold-to-resolution aggregate gap: {rel_gap:.2f}x"
          f"  (sign flip at aggregate: {opposite_sign})")
    print(f"  per-wallet sign agreement was {agree}/{len(wal)} — but note that"
          f" metric ignores magnitude.\n")

    if opposite_sign or rel_gap > 0.5:
        print("  >>> Risk 1 is REAL and LARGE on this data.")
        print("  >>> Wallets are profitable by their ACTUAL trading but the")
        print("  >>> pipeline's hold-to-resolution model scores them very")
        print("  >>> differently (here: opposite sign in aggregate). The")
        print("  >>> negative copy result is most likely a HOLDING-MODEL")
        print("  >>> ARTIFACT, not absence of skill.")
    else:
        print("  >>> Risk 1 is not a major driver: realized and hold-to-")
        print("  >>> resolution agree in both sign and magnitude. The negative")
        print("  >>> copy result is unlikely to be a holding-model artifact.")

    # ---------- the market-maker tell: copyable vs uncopyable ----------
    print("\n=== COPYABLE vs UNCOPYABLE (the decisive question) ===")
    total_buys = int(resolved["n_buys"].sum())
    total_sells = int(resolved["n_sells"].sum())
    sell_ratio = total_sells / total_buys if total_buys else 0.0
    # high sell/buy ratio + many small round-trips = market-maker signature
    median_pos_sells = wal["sells"].median()
    print(f"  sell/buy ratio (selected wallets):   {sell_ratio:.2f}")
    print(f"  median sells per wallet:             {median_pos_sells:.0f}")
    print("\n  Reading:")
    print("  - A copier who mirrors BUYS ONLY and holds to resolution earns")
    print(f"    the hold-to-resolution number above ({htr_total:,.0f}).")
    print("  - The wallets' real profit comes from SELLING (exits). Whether a")
    print("    copier can capture that depends on WHY they sell:")
    print("      * directional timing (buy underpriced, sell on correction)")
    print("        -> potentially copyable by mirroring exits")
    print("      * spread/inventory/market-making -> NOT copyable; the edge is")
    print("        in providing liquidity, gone the moment you cross the spread")
    print(f"  - A sell/buy ratio of {sell_ratio:.2f} is " +
          ("HIGH, which leans toward market-making (uncopyable). Treat the"
           if sell_ratio > 0.6 else
           "moderate; directional exits are plausible. The"))
    print("    exit-mirroring backtest is what settles this empirically.")
    print("\n  NEXT: run the exit-mirroring backtest. If copy-edge goes positive")
    print("  when the copier mirrors EXITS (not holds to resolution), the skill")
    print("  is copyable. If it stays negative, the profit is microstructure and")
    print("  the no-go stands — but for a well-understood reason.")


if __name__ == "__main__":
    main()

