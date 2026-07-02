"""Direction-randomization skill test — the LBS/Yale method, adapted.

THE QUESTION (project §5.4): are there INDIVIDUAL directional traders whose
actions contain skill not explainable by luck — and does any such skill
PERSIST out-of-sample and clear trading costs?

THE METHOD (borrowed from the LBS/Yale Polymarket working paper, 2023-2025,
1.72M accounts). For each wallet, take its ACTUAL sequence of trades — same
markets, same timing, same sizes — and randomize ONLY the buy/sell direction,
many times, to build a luck-only null distribution of PnL. Compare the wallet's
ACTUAL realized PnL to that null. A one-sided p-value = fraction of random
shuffles that beat (or equal) actual.

Why this is sharper than Brier-skill-vs-price: it controls for the trader's OWN
market/timing/size selection. It asks "given exactly which markets, when, and
how much this trader bet, is the DIRECTION they chose better than coin-flips?"
That isolates directional skill from everything else.

FOUR GATES (all pre-registered, all reported):
  1. PER-WALLET NULL. Each wallet tested against its own randomization null,
     not against zero or against the market. p-value from >= N_PERM shuffles.
  2. MULTIPLE-COMPARISONS CORRECTION. Testing K wallets, ~5% beat a 0.05 null
     by chance. Benjamini-Hochberg FDR control + a Bonferroni reference. We
     report how many survive correction, not raw hit count.
  3. TRAIN/TEST PERSISTENCE. Skill is established on TRAIN, then the SAME
     wallets are re-tested on a held-out TEST window. The literature says
     ~60% of apparent winners don't repeat — so a wallet must pass on BOTH.
  4. FEE-AWARE EFFECT SIZE. Polymarket is negative-sum after taker fees.
     The fee is fee = C * feeRate * p * (1-p) (peaks at p=0.5, ~0 at the
     extremes), NOT a flat % of notional. A wallet's edge must clear this
     per-trade, not merely be > 0. We report PnL net of that fee.

PRE-REGISTERED EXPECTATION (from the external base rate): ~3% of the general
population is skilled. For a non-random, volume-selected pool this could be
higher (conviction->volume) or LOWER (skilled traders may be patient/low-volume
and missed by volume ranking). We expect a SMALL NUMBER OF INDIVIDUAL OUTLIERS
at most, not a population effect. Finding zero survivors is a valid result.

NO PnL/tradability claim is made for a survivor beyond "directionally skilled,
persistent, fee-clearing in this sample." Whether you can copy/follow them is a
further question this does not answer.

Run:
    ~/bot1/pm_research/.venv/bin/python -u scripts/randomization_skill_test.py --root ~/data
"""
from __future__ import annotations

import argparse
from datetime import date

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.wallet_classifier import classify


N_PERM = 10_000          # shuffles per wallet (paper used 10k)
MIN_RESOLVED_TRADES = 20 # need enough trades for a meaningful null
SEED = 12345


def trade_pnl_per_dollar(side: str, outcome: str, price: float,
                         winner: str) -> float:
    """Realized PnL per $1 staked, held to resolution.

    BUY  of winning outcome: receive 1.0 for price paid -> (1-price)/price
    BUY  of losing  outcome: lose the stake             -> -1.0
    SELL is the mirror (short the outcome).
    """
    if price <= 0 or price >= 1:
        return 0.0
    won = (outcome == winner)
    # per-dollar return of BUYING this outcome to resolution
    buy_ret = ((1.0 - price) / price) if won else -1.0
    return buy_ret if side == "BUY" else -buy_ret


def wallet_pnl(df: pd.DataFrame, winner: dict, directions: np.ndarray) -> float:
    """Total realized PnL (dollars) for a wallet given a direction vector
    (+1 = BUY, -1 = SELL) over its resolved trades."""
    total = 0.0
    for (idx, row), d in zip(df.iterrows(), directions):
        w = winner.get(row["condition_id"])
        if w is None:
            continue
        side = "BUY" if d > 0 else "SELL"
        per_dollar = trade_pnl_per_dollar(side, row["outcome"], row["price"], w)
        total += per_dollar * row["size_usdc"]
    return total


def randomization_pvalue(df: pd.DataFrame, winner: dict, rng) -> dict:
    """Actual PnL vs luck-only null (randomized direction). One-sided p =
    P(random >= actual). Also returns net-of-fee actual PnL hook upstream."""
    n = len(df)
    actual_dir = np.where(df["side"].values == "BUY", 1, -1).astype(int)
    actual = wallet_pnl(df, winner, actual_dir)

    # vectorize the per-trade per-dollar BUY return once; shuffle signs only
    buy_per_dollar = np.array([
        trade_pnl_per_dollar("BUY", o, p, winner.get(c))
        if winner.get(c) is not None else 0.0
        for o, p, c in zip(df["outcome"], df["price"], df["condition_id"])
    ])
    stake = df["size_usdc"].values
    base = buy_per_dollar * stake          # PnL if every trade were a BUY

    # random directions: +1/-1 per trade; PnL = sum(dir * base)
    rand_dirs = rng.choice(np.array([1, -1]), size=(N_PERM, n))
    rand_pnls = rand_dirs @ base           # (N_PERM,)

    ge = int(np.sum(rand_pnls >= actual))
    pval = (ge + 1) / (N_PERM + 1)         # add-one (never 0)
    return {"actual_pnl": actual, "p_value": pval,
            "null_mean": float(rand_pnls.mean()),
            "null_std": float(rand_pnls.std())}


def net_of_fee_pnl(df: pd.DataFrame, winner: dict, fee_rate: float) -> float:
    """Actual realized PnL minus Polymarket's taker fee.

    Polymarket fee = C * feeRate * p * (1 - p), charged per trade, where C is
    the trade notional and p is the trade price. The effective fee is NOT a
    flat % of notional: it peaks at p=0.5 (max ~feeRate*0.25 of notional) and
    falls to ~0 near p=0 or p=1. This matters for a skill test because where a
    wallet trades on the probability curve changes its true fee burden — a
    near-certainty bettor pays almost nothing; a coin-flip bettor pays the max.

    feeRate is category-dependent on Polymarket (Sports 0.03, Fin/Pol/Tech
    0.04, Econ/Cult/Wx 0.05, Crypto ~0.072, Geopolitics 0). Category metadata
    is unavailable for most markets here, so a single feeRate is applied as a
    conservative approximation; pass the rate matching your dominant category.
    """
    actual_dir = np.where(df["side"].values == "BUY", 1, -1).astype(int)
    gross = wallet_pnl(df, winner, actual_dir)
    p = df["price"].values
    notional = df["size_usdc"].values
    fee = float(np.sum(notional * fee_rate * p * (1.0 - p)))
    return gross - fee


def benjamini_hochberg(pvals: list[float], alpha: float = 0.05) -> np.ndarray:
    """Return boolean mask of hypotheses surviving BH-FDR at level alpha."""
    p = np.asarray(pvals)
    n = len(p)
    if n == 0:
        return np.array([], dtype=bool)
    order = np.argsort(p)
    thresh = alpha * (np.arange(1, n + 1) / n)
    passed = p[order] <= thresh
    if not passed.any():
        return np.zeros(n, dtype=bool)
    kmax = np.max(np.where(passed)[0])
    cutoff = p[order][kmax]
    return p <= cutoff


def evaluate_window(trades, winner, wallets, rng, fee_rate):
    """Per-wallet randomization test over one date window's resolved trades."""
    rows = []
    for w in wallets:
        g = trades[(trades["wallet"] == w)
                   & (trades["condition_id"].isin(winner))].copy()
        if len(g) < MIN_RESOLVED_TRADES:
            continue
        r = randomization_pvalue(g, winner, rng)
        r["wallet"] = w
        r["n_trades"] = len(g)
        r["net_fee_pnl"] = net_of_fee_pnl(g, winner, fee_rate)
        rows.append(r)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--start", type=date.fromisoformat, default=date(2025, 6, 1))
    ap.add_argument("--end", type=date.fromisoformat, default=date(2026, 6, 1))
    ap.add_argument("--fee-rate", type=float, default=0.05,
                    help="Polymarket feeRate for fee = C*feeRate*p*(1-p). "
                         "By category: Sports 0.03, Fin/Pol/Tech 0.04, "
                         "Econ/Cult/Wx 0.05 (default, conservative middle), "
                         "Crypto ~0.072, Geopolitics 0.")
    ap.add_argument("--directional-only", action="store_true", default=True,
                    help="restrict to DIRECTIONAL wallets (exclude market makers)")
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades().sort_values("traded_at").reset_index(drop=True)
    res = store.load_resolutions()
    winner = dict(zip(res["condition_id"], res["winning_outcome"]))

    # population: directional wallets only (market makers excluded)
    cls = classify(trades)
    if args.directional_only:
        pool = list(cls[cls["label"] == "DIRECTIONAL"]["wallet"])
    else:
        pool = list(cls[cls["label"] != "UNKNOWN"]["wallet"])
    print(f"=== testing {len(pool)} directional wallets ===")
    print(f"  N_PERM={N_PERM}, fee_rate={args.fee_rate} (fee=C*feeRate*p*(1-p)), "
          f"min_trades={MIN_RESOLVED_TRADES}\n")
    if not pool:
        print("No directional wallets. Inconclusive.")
        return

    mid = pd.Timestamp(args.start, tz="UTC") + (
        pd.Timestamp(args.end, tz="UTC") - pd.Timestamp(args.start, tz="UTC")) / 2
    s = pd.Timestamp(args.start, tz="UTC")
    e = pd.Timestamp(args.end, tz="UTC")
    tr_tr = trades[(trades["traded_at"] >= s) & (trades["traded_at"] < mid)]
    tr_te = trades[(trades["traded_at"] >= mid) & (trades["traded_at"] < e)]

    rng = np.random.default_rng(SEED)
    print(f"--- TRAIN window {s.date()}..{mid.date()} ---")
    train = evaluate_window(tr_tr, winner, pool, rng, args.fee_rate)
    if train.empty:
        print("  no wallets with enough resolved train trades. Inconclusive.")
        return

    # gate 1: per-wallet null. gate 2: BH-FDR correction across tested wallets.
    train = train.sort_values("p_value").reset_index(drop=True)
    train["bh_pass"] = benjamini_hochberg(train["p_value"].tolist(), alpha=0.05)
    bonferroni = 0.05 / len(train)
    train["bonferroni_pass"] = train["p_value"] <= bonferroni

    n_raw = int((train["p_value"] <= 0.05).sum())
    n_bh = int(train["bh_pass"].sum())
    n_bonf = int(train["bonferroni_pass"].sum())
    print(f"  wallets tested: {len(train)}")
    print(f"  raw p<=0.05:                 {n_raw}  "
          f"(expect ~{0.05*len(train):.1f} by chance alone)")
    print(f"  survive BH-FDR (alpha=0.05): {n_bh}")
    print(f"  survive Bonferroni:          {n_bonf}")
    # fee gate among BH survivors
    bh_survivors = train[train["bh_pass"]]
    fee_clear = bh_survivors[bh_survivors["net_fee_pnl"] > 0]
    print(f"  of BH survivors, fee-clearing (net>0 @ feeRate={args.fee_rate}): "
          f"{len(fee_clear)}\n")

    if bh_survivors.empty:
        print("=== VERDICT: NO skilled directional wallets on TRAIN ===")
        print("  After multiple-comparisons correction, no wallet's directional")
        print("  PnL exceeds its own luck-only null. Consistent with the")
        print("  external finding that skill is rare (~3%) and that a volume-")
        print("  ranked pool may miss patient skilled traders. Honest stop.")
        return

    # gate 3: persistence. re-test the TRAIN survivors on held-out TEST.
    cand = list(bh_survivors["wallet"])
    print(f"--- TEST window {mid.date()}..{e.date()} (held out) ---")
    print(f"  re-testing {len(cand)} train survivors\n")
    rng2 = np.random.default_rng(SEED + 1)
    test = evaluate_window(tr_te, winner, cand, rng2, args.fee_rate)
    if test.empty:
        print("  survivors have too few resolved TEST trades to confirm.")
        print("  INCONCLUSIVE for persistence — cannot rule in or out.")
        return

    test["persist_pass"] = test["p_value"] <= 0.05
    test["fee_pass"] = test["net_fee_pnl"] > 0
    merged = test.merge(bh_survivors[["wallet", "p_value", "net_fee_pnl"]],
                        on="wallet", suffixes=("_test", "_train"))
    final = merged[(merged["persist_pass"]) & (merged["fee_pass"])]

    print("  per-survivor (train -> test):")
    for _, r in merged.iterrows():
        tag = ("PERSISTS+FEE-CLEARS" if r["persist_pass"] and r["fee_pass"]
               else "persists, fails fee" if r["persist_pass"]
               else "did NOT persist")
        print(f"    {r['wallet'][:12]}  train_p={r['p_value_train']:.4f}  "
              f"test_p={r['p_value_test']:.4f}  "
              f"test_net_fee={r['net_fee_pnl_test']:,.0f}  -> {tag}")

    print("\n=== VERDICT (single-split gate) ===")
    if len(final):
        print(f"  {len(final)} wallet(s) pass the single-split four-gate test.")
        print("  But a single train/test split + a lenient (uncorrected)")
        print("  persistence threshold is FRAGILE evidence — the literature's")
        print("  ~60% non-repeat rate means one survivor here is a CANDIDATE,")
        print("  not a confirmed signal. Proceeding to hardened verification.\n")
    else:
        print("  No wallet passes even the single-split gate. Honest stop:")
        print("  apparent train skill did not persist. (Re-discovery by")
        print("  profitability/sharpness ranking is the only remaining lever,")
        print("  pre-registered against the ~3% base rate.)")
        return

    # ================= HARDENED MULTI-SPLIT VERIFICATION =================
    # A candidate that is genuinely skilled should survive MANY independent
    # train/test partitions, not just the one midpoint split. We pre-register
    # the rule BEFORE looking: across K rolling splits, the candidate must
    # beat its own randomization null at a Bonferroni-corrected threshold
    # (alpha/K) AND clear fees on EACH split's test half. Pass >= ceil(0.7*K)
    # splits -> ROBUST. Fewer -> fragile (single-split skill was likely luck).
    K = 5
    alpha_split = 0.05 / K            # Bonferroni across the K splits
    need = int(np.ceil(0.7 * K))      # pre-stated strong-majority rule
    candidates = list(final["wallet"])
    print("=== HARDENED VERIFICATION (pre-registered, decided before looking) ===")
    print(f"  K={K} independent rolling splits; per-split threshold "
          f"alpha={alpha_split:.3f} (Bonferroni); must clear fees each split;")
    print(f"  ROBUST rule: pass >= {need} of {K} splits.\n")

    # build K splits: rolling train/test boundaries across the full window
    span = e - s
    # test halves are the last ~40% at K evenly spaced boundaries
    boundaries = [s + span * frac for frac in np.linspace(0.45, 0.70, K)]

    rng3 = np.random.default_rng(SEED + 7)
    robust = []
    for w in candidates:
        passes = 0
        detail = []
        for bi, b in enumerate(boundaries):
            tr_w = trades[(trades["traded_at"] >= s) & (trades["traded_at"] < b)]
            te_w = trades[(trades["traded_at"] >= b) & (trades["traded_at"] < e)]
            gw_tr = tr_w[(tr_w["wallet"] == w) & (tr_w["condition_id"].isin(winner))]
            gw_te = te_w[(te_w["wallet"] == w) & (te_w["condition_id"].isin(winner))]
            if len(gw_tr) < MIN_RESOLVED_TRADES or len(gw_te) < MIN_RESOLVED_TRADES:
                detail.append(f"s{bi}:insuff")
                continue
            r_tr = randomization_pvalue(gw_tr, winner, rng3)
            r_te = randomization_pvalue(gw_te, winner, rng3)
            fee_te = net_of_fee_pnl(gw_te, winner, args.fee_rate)
            ok = (r_tr["p_value"] <= alpha_split
                  and r_te["p_value"] <= alpha_split
                  and fee_te > 0)
            passes += int(ok)
            detail.append(f"s{bi}:{'P' if ok else 'x'}"
                          f"(te_p={r_te['p_value']:.3f},fee={fee_te:,.0f})")
        verdict = "ROBUST" if passes >= need else "FRAGILE"
        robust.append((w, passes, verdict))
        print(f"  {w[:12]}  {passes}/{K} splits passed -> {verdict}")
        for d in detail:
            print(f"      {d}")

    n_robust = sum(1 for _, _, v in robust if v == "ROBUST")
    print("\n=== FINAL VERDICT ===")
    if n_robust:
        print(f"  {n_robust} wallet(s) are ROBUST: skilled vs own null on a")
        print(f"  strong majority of independent splits at a corrected")
        print(f"  threshold, clearing fees each time. This is as strong as")
        print(f"  in-sample evidence gets for individual skill. It is STILL")
        print(f"  prediction skill, not a tradable edge — the wallet's signal")
        print(f"  must then be shown capturable at latency (prior: hard, given")
        print(f"  everything we've learned about execution costs).")
    else:
        print("  NO wallet is robust across multiple splits. The single-split")
        print("  survivor(s) did not hold up — consistent with high per-wallet")
        print("  variance and the literature's non-persistence finding. The")
        print("  honest conclusion: this volume-ranked directional pool contains")
        print("  no individual skill robust enough to trust. The remaining lever")
        print("  is a profitability/sharpness-ranked re-discovery, pre-registered")
        print("  against the ~3% base rate — NOT loosening any threshold here.")


if __name__ == "__main__":
    main()
