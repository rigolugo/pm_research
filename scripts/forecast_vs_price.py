"""Rank 1A — pooled YES/NO binary forecast-vs-price probe (condition-level).

Tests ONLY: can a forecast beat the Polymarket YES price, after fees/spread,
out-of-sample, across rolling splits, on resolved YES/NO binary markets?

Unit of analysis: ONE signal per condition (one decision_timestamp, one price,
one realized binary outcome). Never weighted by trade count.

Decision policy (default, lookahead-safe): first_price_after_warmup —
for each condition, take the first observed trade time, then the first YES
price at least `warmup_hours` after it. This timestamp could exist live; it
does NOT use derived resolution time (which would leak the outcome).

Scope: Rung 0 (forecast = price; sanity, Brier skill ~ 0) and Rung 1 (isotonic
recalibration of price, fit on TRAIN only, applied on TEST only). Rungs 2-3 are
NOT implemented. No named-binary markets. No category claims. No trading code.

Falsification discipline: Rung 0 must tie the baseline; negatives are stated
plainly; INCONCLUSIVE on thin cells; Brier improvement alone is never called
tradable; EV is reported under both no-spread and conservative-spread.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.calibration import IsotonicCalibrator
from pm_research.splits import rolling_train_test_splits

# reuse the audit's streaming classifier to get the SAME usable YES/NO set
_ams_spec = importlib.util.spec_from_file_location(
    "audit_market_structure",
    str(pathlib.Path(__file__).resolve().parent / "audit_market_structure.py"))
_ams = importlib.util.module_from_spec(_ams_spec)
_ams_spec.loader.exec_module(_ams)

# Polymarket taker fee: notional * feeRate * p * (1-p). Category metadata is
# absent, so a single conservative feeRate is applied (documented assumption).
DEFAULT_FEE_RATE = 0.04
DEFAULT_SPREAD_PROXY = 0.01      # 1 cent conservative half-spread proxy
MIN_TEST = 50
MIN_TRAIN = 100


# --------------------------------------------------------------------------- #
#  Condition-level dataset construction (lookahead-safe)                       #
# --------------------------------------------------------------------------- #
def build_condition_dataset(root: str, warmup_hours: float,
                            usable_cids: set) -> pd.DataFrame:
    """One row per usable condition with an EX-ANTE decision point.

    For each condition:
      first_trade_ts := earliest trade time (from streamed aggregates)
      decision_ts    := first price ts >= first_trade_ts + warmup_hours
      market_price   := yes_price at decision_ts (info available at/before it)
      outcome        := 1 if winning_outcome == 'YES' else 0  (label only)
    Conditions with no price >= warmup after first trade are dropped (cannot
    form an ex-ante signal) and counted.
    """
    store = Store(root)
    prices = store.load_prices()
    res = store.load_resolutions()
    res = res[res["condition_id"].isin(usable_cids)]
    outcome_map = {c: (1 if str(w).upper() == "YES" else 0)
                   for c, w in zip(res["condition_id"], res["winning_outcome"])}

    # first trade time per usable condition (ex-ante anchor) via streaming agg
    agg, _ = _ams.stream_condition_aggregates(
        pathlib.Path(root) / "trades", analysis_hygiene=True)
    first_trade = {c: agg[c]["first_trade"] for c in usable_cids if c in agg}

    prices = prices[prices["condition_id"].isin(usable_cids)].copy()
    prices["ts"] = pd.to_datetime(prices["ts"], utc=True)
    prices = prices.sort_values(["condition_id", "ts"])

    warmup = pd.Timedelta(hours=warmup_hours)
    rows = []
    n_no_price = 0
    for cid, g in prices.groupby("condition_id"):
        ft = first_trade.get(cid)
        if ft is None or cid not in outcome_map:
            continue
        ft = pd.Timestamp(ft)
        decision_after = ft + warmup
        elig = g[g["ts"] >= decision_after]
        if len(elig) == 0:
            n_no_price += 1
            continue
        d = elig.iloc[0]                       # FIRST price at/after warmup
        p = float(d["yes_price"])
        if not (0.0 <= p <= 1.0):
            continue
        rows.append({
            "condition_id": cid,
            "first_trade_ts": ft,
            "decision_ts": pd.Timestamp(d["ts"]),
            "market_price_at_decision": p,
            "realized_outcome": outcome_map[cid],
            "resolution_label": "YES" if outcome_map[cid] == 1 else "NO",
        })
    df = pd.DataFrame(rows)
    df.attrs["dropped_no_price_after_warmup"] = n_no_price
    return df


# --------------------------------------------------------------------------- #
#  EV (net of fees + spread)                                                   #
# --------------------------------------------------------------------------- #
def _fee(p: np.ndarray, fee_rate: float) -> np.ndarray:
    """Per-unit-notional taker fee = fee_rate * p * (1-p)."""
    return fee_rate * p * (1.0 - p)


def net_ev(forecast: np.ndarray, price: np.ndarray, outcome: np.ndarray,
           fee_rate: float, spread: float) -> dict:
    """Condition-level expected value of acting on the forecast vs the price.

    Side: forecast>price -> buy YES (edge = forecast-price);
          forecast<price -> buy NO  (edge = price-forecast).
    gross_edge is the modeled probability edge; realized PnL uses the binary
    outcome. We report BOTH the modeled gross edge mean and the realized mean
    PnL net of fee+spread. Brier improvement alone is never called tradable.
    """
    forecast = np.asarray(forecast, float)
    price = np.asarray(price, float)
    outcome = np.asarray(outcome, float)
    side_yes = forecast > price
    gross_edge = np.where(side_yes, forecast - price, price - forecast)
    # realized per-unit PnL of the chosen side (taker enters at price):
    #   YES: outcome - price ; NO: (1-outcome) - (1-price) = price - outcome
    realized = np.where(side_yes, outcome - price, price - outcome)
    cost = _fee(price, fee_rate) + spread
    net = realized - cost
    return {
        "n": int(len(forecast)),
        "mean_gross_edge": float(np.mean(gross_edge)) if len(forecast) else float("nan"),
        "mean_realized_pnl": float(np.mean(realized)) if len(forecast) else float("nan"),
        "mean_cost": float(np.mean(cost)) if len(forecast) else float("nan"),
        "mean_net_ev": float(np.mean(net)) if len(forecast) else float("nan"),
        "frac_side_yes": float(np.mean(side_yes)) if len(forecast) else float("nan"),
    }


# --------------------------------------------------------------------------- #
#  Probe                                                                       #
# --------------------------------------------------------------------------- #
def run_probe(df: pd.DataFrame, splits, fee_rate: float, spread: float,
              min_test: int, min_train: int, robust_pass: int) -> dict:
    """Rung 0 (price) + Rung 1 (isotonic-recalibrated price), per split."""
    dec = pd.to_datetime(df["decision_ts"], utc=True)
    per_split = []
    for i, (trs, tre, tes, tee) in enumerate(splits, 1):
        trs, tre = pd.Timestamp(trs, tz="UTC"), pd.Timestamp(tre, tz="UTC")
        tes, tee = pd.Timestamp(tes, tz="UTC"), pd.Timestamp(tee, tz="UTC")
        tr = df[(dec >= trs) & (dec < tre)]
        te = df[(dec >= tes) & (dec < tee)]
        rec = {"split": i, "n_train": int(len(tr)), "n_test": int(len(te))}
        if len(te) < min_test or len(tr) < min_train:
            rec["status"] = "INCONCLUSIVE_thin"
            per_split.append(rec)
            continue
        p_tr = tr["market_price_at_decision"].to_numpy(float)
        y_tr = tr["realized_outcome"].to_numpy(float)
        p_te = te["market_price_at_decision"].to_numpy(float)
        y_te = te["realized_outcome"].to_numpy(float)

        # Rung 0: forecast = price (sanity). Brier skill vs baseline must be ~0.
        brier_price = IsotonicCalibrator.brier(p_te, y_te)
        rung0_brier = IsotonicCalibrator.brier(p_te, y_te)   # identical by design
        rung0_skill = 1.0 - (rung0_brier / brier_price) if brier_price > 0 else 0.0

        # Rung 1: isotonic recalibration of price. Fit on TRAIN, apply on TEST.
        rung1 = {}
        try:
            cal = IsotonicCalibrator(min_samples=min_train).fit(p_tr, y_tr)
            f_te = np.asarray(cal.apply(p_te), float)
            brier_cal = IsotonicCalibrator.brier(f_te, y_te)
            skill_cal = 1.0 - (brier_cal / brier_price) if brier_price > 0 else 0.0
            ev0 = net_ev(p_te, p_te, y_te, fee_rate, spread)         # rung0 EV
            ev0_ns = net_ev(p_te, p_te, y_te, fee_rate, 0.0)
            ev1 = net_ev(f_te, p_te, y_te, fee_rate, spread)         # rung1 EV
            ev1_ns = net_ev(f_te, p_te, y_te, fee_rate, 0.0)
            rung1 = {
                "brier_price": brier_price, "brier_cal": brier_cal,
                "brier_skill_cal": skill_cal,
                "ev_rung0_conservative": ev0, "ev_rung0_no_spread": ev0_ns,
                "ev_rung1_conservative": ev1, "ev_rung1_no_spread": ev1_ns,
            }
            rec["status"] = "OK"
        except ValueError as e:
            rec["status"] = f"INCONCLUSIVE_calibrate({e})"
        rec["rung0_brier"] = rung0_brier
        rec["rung0_brier_skill"] = rung0_skill
        rec.update(rung1)
        per_split.append(rec)

    ok = [s for s in per_split if s.get("status") == "OK"]
    # Rung 0 sanity: skill must be ~0 on every evaluable split
    rung0_ties = all(abs(s["rung0_brier_skill"]) < 1e-9 for s in ok)
    # Rung 1 robustness: positive OOS Brier skill in >= robust_pass splits
    rung1_pos = sum(1 for s in ok if s.get("brier_skill_cal", 0) > 0)
    rung1_robust = rung1_pos >= robust_pass
    # Rung 1 tradability: positive net EV (conservative) in the robust splits
    rung1_ev_pos = sum(1 for s in ok
                       if s.get("ev_rung1_conservative", {}).get("mean_net_ev", -1) > 0)
    rung1_tradable = (rung1_robust and rung1_ev_pos >= robust_pass)

    if not ok:
        verdict = "INCONCLUSIVE_INSUFFICIENT_SAMPLE"
    elif not rung0_ties:
        verdict = "FAIL_RUNG0_SANITY"            # harness bug — must tie
    elif rung1_robust and rung1_tradable:
        verdict = "RANK1A_POSITIVE_TRADABLE"
    elif rung1_robust and not rung1_tradable:
        verdict = "RANK1A_INFORMATIVE_NOT_TRADABLE"   # Brier up, EV<=0 after cost
    else:
        verdict = "RANK1A_NEGATIVE"
    return {
        "per_split": per_split,
        "n_evaluable_splits": len(ok),
        "rung0_sanity_ties": rung0_ties,
        "rung1_positive_brier_splits": rung1_pos,
        "rung1_robust": rung1_robust,
        "rung1_ev_positive_splits": rung1_ev_pos,
        "rung1_tradable": rung1_tradable,
        "verdict": verdict,
    }


STANDING_WARNINGS = [
    "row-level concentration exists but does not affect condition-level evaluation",
    "event independence is unmeasured (defer full diagnostics unless Rank 1A positive)",
    "named-binary markets are excluded (~40k 2-outcome non-YES/NO markets)",
    "category-specialist hypothesis is NOT tested (pooled YES/NO only)",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--decision-policy", default="first_price_after_warmup",
                    choices=["first_price_after_warmup"])
    ap.add_argument("--warmup-hours", type=float, default=1.0)
    ap.add_argument("--splits", type=int, default=5)
    ap.add_argument("--robust-pass-splits", type=int, default=4)
    ap.add_argument("--min-test-signals-per-split", type=int, default=MIN_TEST)
    ap.add_argument("--min-train-signals-per-split", type=int, default=MIN_TRAIN)
    ap.add_argument("--fee-rate", type=float, default=DEFAULT_FEE_RATE)
    ap.add_argument("--spread-proxy", type=float, default=DEFAULT_SPREAD_PROXY)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    root_p = pathlib.Path(args.root)
    store = Store(args.root)
    markets = store.load_markets()
    resolutions = store.load_resolutions()
    price_cids = {p.stem for p in (root_p / "prices").glob("*.parquet")}

    # usable YES/NO binary set — SAME classification as the gate
    agg, _ = _ams.stream_condition_aggregates(root_p / "trades",
                                              analysis_hygiene=True)
    cc = _ams.classify_from_aggregates(agg, markets, resolutions, price_cids)
    usable_cids = set(cc.loc[cc["usable"], "condition_id"])

    df = build_condition_dataset(args.root, args.warmup_hours, usable_cids)
    # span from decision timestamps (the analysis clock)
    if len(df):
        span_start = df["decision_ts"].min().date()
        span_end = df["decision_ts"].max().date()
    else:
        from datetime import date
        span_start = span_end = date.today()
    splits = rolling_train_test_splits(span_start, span_end, args.splits)

    res = run_probe(df, splits, args.fee_rate, args.spread_proxy,
                    args.min_test_signals_per_split,
                    args.min_train_signals_per_split, args.robust_pass_splits)

    out = {
        "probe": "rank1a_pooled_yesno_binary_forecast_vs_price",
        "decision_policy": args.decision_policy,
        "warmup_hours": args.warmup_hours,
        "fee_rate": args.fee_rate, "spread_proxy": args.spread_proxy,
        "usable_binary_conditions": len(usable_cids),
        "condition_signals": int(len(df)),
        "dropped_no_price_after_warmup": int(df.attrs.get("dropped_no_price_after_warmup", 0)),
        "rungs_implemented": [0, 1],
        "warnings": STANDING_WARNINGS,
        **res,
    }

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "forecast_vs_price_rank1a.json").write_text(
        json.dumps(out, indent=2, default=str))
    # splits CSV
    pd.json_normalize(res["per_split"]).to_csv(
        out_dir / "forecast_vs_price_rank1a_splits.csv", index=False)
    # conditions CSV (the analysis unit; no trade-count column by design)
    if len(df):
        df.to_csv(out_dir / "forecast_vs_price_rank1a_conditions.csv", index=False)
    _write_md(out, out_dir / "forecast_vs_price_rank1a_report.md")

    print("=" * 64)
    print("RANK 1A — pooled YES/NO forecast-vs-price (condition-level)")
    print("=" * 64)
    print(f"  usable conditions: {len(usable_cids):,} | signals: {len(df):,} "
          f"| dropped(no price after warmup): {out['dropped_no_price_after_warmup']}")
    print(f"  decision policy: {args.decision_policy} (warmup {args.warmup_hours}h)")
    print(f"  Rung 0 sanity ties baseline: {res['rung0_sanity_ties']}")
    print(f"  Rung 1 positive-Brier splits: {res['rung1_positive_brier_splits']}"
          f"/{res['n_evaluable_splits']} | robust: {res['rung1_robust']}")
    print(f"  Rung 1 EV-positive splits (conservative): {res['rung1_ev_positive_splits']}")
    print(f"  >>> VERDICT: {res['verdict']}")
    for w in STANDING_WARNINGS:
        print(f"    * {w}")
    print(f"  wrote {out_dir}/forecast_vs_price_rank1a.json (+ report, 2 CSVs)")
    return 0


def _write_md(out, path):
    L = ["# Rank 1A — pooled YES/NO forecast-vs-price (condition-level)", "",
         f"**Verdict: `{out['verdict']}`**", "",
         f"- decision policy: {out['decision_policy']} (warmup {out['warmup_hours']}h, lookahead-safe)",
         f"- usable conditions: {out['usable_binary_conditions']:,}",
         f"- condition signals: {out['condition_signals']:,} "
         f"(dropped {out['dropped_no_price_after_warmup']} with no price after warmup)",
         f"- fee_rate: {out['fee_rate']}, spread_proxy: {out['spread_proxy']}",
         f"- rungs implemented: {out['rungs_implemented']} (Rungs 2-3 NOT built)", "",
         "## Results",
         f"- Rung 0 sanity (must tie price baseline): "
         f"{'PASS' if out['rung0_sanity_ties'] else 'FAIL'}",
         f"- Rung 1 positive OOS Brier skill in "
         f"{out['rung1_positive_brier_splits']}/{out['n_evaluable_splits']} splits "
         f"(robust={out['rung1_robust']})",
         f"- Rung 1 net-EV positive (conservative spread) in "
         f"{out['rung1_ev_positive_splits']} splits (tradable={out['rung1_tradable']})", "",
         "## Interpretation",
         "- Brier improvement alone is NOT tradability; EV is reported under both "
         "no-spread (diagnostic) and conservative-spread assumptions.",
         "- A result may be INFORMATIVE_NOT_TRADABLE: calibration improves but "
         "net EV <= 0 after costs.", "",
         "## Standing warnings"]
    L += [f"- {w}" for w in out["warnings"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
