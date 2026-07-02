"""Rank 1A price-bucket diagnostic (DIAGNOSTIC ONLY — not a strategy).

Reuses the existing Rank 1A condition-level dataset and asks ONE question: is
the Rung 1 negative UNIFORM across the probability range, or does pooled
efficiency hide a localized weakness (e.g. in the longshot tails)?

For each price bucket it re-runs the same Rung 0 (sanity) + Rung 1 (isotonic
recalibration, fit on TRAIN only, applied on TEST only) per split, and reports
Brier skill + net EV (no-spread and conservative). It then labels the overall
picture. NO bucket is ever called a strategy; isolated positives are flagged as
noise. Multiple-bucket testing inflates false positives, so the bar is the same
≥4/5-split persistence on BOTH Brier and EV.

Guardrails: no live/paper trading, no named-binary, no category claims, no
post-hoc green-slice win. This does NOT implement Rung 2.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib

import numpy as np
import pandas as pd

from pm_research.calibration import IsotonicCalibrator
from pm_research.splits import rolling_train_test_splits

# reuse the probe's EV + dataset builder + classification (single source)
_fvp_spec = importlib.util.spec_from_file_location(
    "forecast_vs_price",
    str(pathlib.Path(__file__).resolve().parent / "forecast_vs_price.py"))
_fvp = importlib.util.module_from_spec(_fvp_spec)
_fvp_spec.loader.exec_module(_fvp)

from pm_research.data.store import Store

BUCKETS = [(0.00, 0.05), (0.05, 0.10), (0.10, 0.20), (0.20, 0.40),
           (0.40, 0.60), (0.60, 0.80), (0.80, 0.90), (0.90, 0.95),
           (0.95, 1.00)]
MIN_TEST = 50
MIN_TRAIN = 100
ROBUST = 4


def _bucket_label(lo, hi):
    return f"{lo:.2f}-{hi:.2f}"


def _eval_bucket(sub, splits, fee_rate, spread, min_test, min_train, robust):
    """Run Rung 0 + Rung 1 on one bucket across splits."""
    dec = pd.to_datetime(sub["decision_ts"], utc=True)
    per_split = []
    for i, (trs, tre, tes, tee) in enumerate(splits, 1):
        trs, tre = pd.Timestamp(trs, tz="UTC"), pd.Timestamp(tre, tz="UTC")
        tes, tee = pd.Timestamp(tes, tz="UTC"), pd.Timestamp(tee, tz="UTC")
        tr = sub[(dec >= trs) & (dec < tre)]
        te = sub[(dec >= tes) & (dec < tee)]
        rec = {"split": i, "n_train": int(len(tr)), "n_test": int(len(te))}
        if len(te) < min_test or len(tr) < min_train:
            rec["status"] = "INCONCLUSIVE_thin"
            per_split.append(rec)
            continue
        p_tr = tr["market_price_at_decision"].to_numpy(float)
        y_tr = tr["realized_outcome"].to_numpy(float)
        p_te = te["market_price_at_decision"].to_numpy(float)
        y_te = te["realized_outcome"].to_numpy(float)
        brier_price = IsotonicCalibrator.brier(p_te, y_te)
        rec["rung0_brier_skill"] = 0.0   # forecast=price by construction
        try:
            cal = IsotonicCalibrator(min_samples=min_train).fit(p_tr, y_tr)
            f_te = np.asarray(cal.apply(p_te), float)
            brier_cal = IsotonicCalibrator.brier(f_te, y_te)
            skill = 1.0 - (brier_cal / brier_price) if brier_price > 0 else 0.0
            ev_cons = _fvp.net_ev(f_te, p_te, y_te, fee_rate, spread)
            ev_ns = _fvp.net_ev(f_te, p_te, y_te, fee_rate, 0.0)
            rec.update({
                "status": "OK", "brier_price": brier_price,
                "brier_cal": brier_cal, "brier_skill_cal": skill,
                "net_ev_conservative": ev_cons["mean_net_ev"],
                "net_ev_no_spread": ev_ns["mean_net_ev"],
            })
        except ValueError as e:
            rec["status"] = f"INCONCLUSIVE_calibrate"
            rec["detail"] = str(e)
        per_split.append(rec)

    ok = [s for s in per_split if s.get("status") == "OK"]
    pos_brier = sum(1 for s in ok if s.get("brier_skill_cal", 0) > 0)
    pos_ev = sum(1 for s in ok if s.get("net_ev_conservative", -1) > 0)
    robust_brier = pos_brier >= robust
    robust_ev = pos_ev >= robust
    n_total = int(len(sub))
    n_eval = len(ok)
    if n_eval == 0:
        verdict = "INCONCLUSIVE"
    elif robust_brier and robust_ev:
        verdict = "LOCALIZED_CANDIDATE"
    elif pos_brier >= 1 or pos_ev >= 1:
        verdict = "NO_ACTIONABLE_BUCKET"     # some positive but not persistent
    else:
        verdict = "UNIFORM_NEGATIVE"
    return {
        "n_total": n_total, "n_evaluable_splits": n_eval,
        "positive_brier_splits": pos_brier, "ev_positive_splits": pos_ev,
        "robust_brier": robust_brier, "robust_ev": robust_ev,
        "bucket_verdict": verdict, "per_split": per_split,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--conditions-csv", default=None,
                    help="reuse existing Rank 1A conditions CSV; if absent, "
                         "rebuild the condition-level dataset")
    ap.add_argument("--warmup-hours", type=float, default=1.0)
    ap.add_argument("--splits", type=int, default=5)
    ap.add_argument("--robust-pass-splits", type=int, default=ROBUST)
    ap.add_argument("--min-test-signals-per-split", type=int, default=MIN_TEST)
    ap.add_argument("--min-train-signals-per-split", type=int, default=MIN_TRAIN)
    ap.add_argument("--fee-rate", type=float, default=_fvp.DEFAULT_FEE_RATE)
    ap.add_argument("--spread-proxy", type=float, default=_fvp.DEFAULT_SPREAD_PROXY)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    # reuse existing conditions CSV when available (no universe rebuild)
    csv_path = (pathlib.Path(args.conditions_csv) if args.conditions_csv
                else out_dir / "forecast_vs_price_rank1a_conditions.csv")
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df["decision_ts"] = pd.to_datetime(df["decision_ts"], utc=True)
        rebuilt = False
    else:
        # rebuild only if necessary
        store = Store(args.root); root_p = pathlib.Path(args.root)
        markets = store.load_markets(); resolutions = store.load_resolutions()
        price_cids = {p.stem for p in (root_p / "prices").glob("*.parquet")}
        agg, _ = _fvp._ams.stream_condition_aggregates(
            root_p / "trades", analysis_hygiene=True)
        cc = _fvp._ams.classify_from_aggregates(agg, markets, resolutions, price_cids)
        usable = set(cc.loc[cc["usable"], "condition_id"])
        df = _fvp.build_condition_dataset(args.root, args.warmup_hours, usable)
        rebuilt = True

    span_start = df["decision_ts"].min().date()
    span_end = df["decision_ts"].max().date()
    splits = rolling_train_test_splits(span_start, span_end, args.splits)

    # --- per-bucket evaluation (merge thin adjacent buckets) ----------------
    price = df["market_price_at_decision"].to_numpy(float)
    bucket_results = {}
    pending = None     # for merge bookkeeping
    rows_csv = []
    for (lo, hi) in BUCKETS:
        mask = (price >= lo) & (price < hi if hi < 1.0 else price <= hi)
        sub = df[mask]
        label = _bucket_label(lo, hi)
        merged_from = None
        if len(sub) < args.min_test_signals_per_split * args.splits and pending is not None:
            # merge with previous pending thin bucket
            prev_label, prev_sub, prev_lo = pending
            sub = pd.concat([prev_sub, sub])
            label = f"{prev_lo:.2f}-{hi:.2f}"
            merged_from = [prev_label, _bucket_label(lo, hi)]
            pending = None
        # if still thin, hold for merge with next
        if len(sub) < args.min_test_signals_per_split * args.splits:
            pending = (label, sub, lo)
            continue
        r = _eval_bucket(sub, splits, args.fee_rate, args.spread_proxy,
                         args.min_test_signals_per_split,
                         args.min_train_signals_per_split,
                         args.robust_pass_splits)
        if merged_from:
            r["merged_from"] = merged_from
        bucket_results[label] = r
        rows_csv.append({"bucket": label, "merged": bool(merged_from),
                         "n_total": r["n_total"],
                         "positive_brier_splits": r["positive_brier_splits"],
                         "ev_positive_splits": r["ev_positive_splits"],
                         "robust_brier": r["robust_brier"],
                         "robust_ev": r["robust_ev"],
                         "bucket_verdict": r["bucket_verdict"]})
    if pending is not None:
        # leftover thin bucket -> evaluate as-is, will likely be INCONCLUSIVE
        label, sub, lo = pending
        r = _eval_bucket(sub, splits, args.fee_rate, args.spread_proxy,
                         args.min_test_signals_per_split,
                         args.min_train_signals_per_split, args.robust_pass_splits)
        r["thin_leftover"] = True
        bucket_results[label] = r
        rows_csv.append({"bucket": label, "merged": False, "n_total": r["n_total"],
                         "positive_brier_splits": r["positive_brier_splits"],
                         "ev_positive_splits": r["ev_positive_splits"],
                         "robust_brier": r["robust_brier"],
                         "robust_ev": r["robust_ev"],
                         "bucket_verdict": r["bucket_verdict"]})

    # --- overall label ------------------------------------------------------
    verdicts = [r["bucket_verdict"] for r in bucket_results.values()]
    any_localized = any(v == "LOCALIZED_CANDIDATE" for v in verdicts)
    any_no_action = any(v == "NO_ACTIONABLE_BUCKET" for v in verdicts)
    all_inconclusive = all(v == "INCONCLUSIVE" for v in verdicts) if verdicts else True
    if any_localized:
        overall = "LOCALIZED_CANDIDATE"
    elif all_inconclusive:
        overall = "INCONCLUSIVE_BUCKETS"
    elif any_no_action:
        overall = "NO_ACTIONABLE_BUCKET"
    else:
        overall = "UNIFORM_NEGATIVE"

    out = {
        "diagnostic": "rank1a_price_bucket",
        "reused_conditions_csv": (not rebuilt),
        "condition_signals": int(len(df)),
        "fee_rate": args.fee_rate, "spread_proxy": args.spread_proxy,
        "overall_label": overall,
        "buckets": bucket_results,
        "guardrails": [
            "diagnostic only — no bucket is a strategy",
            "no post-hoc green-slice win declared",
            "no live/paper trading", "no named-binary markets",
            "no category-specialist claim",
            "multiple-bucket testing inflates false positives; bar is >=4/5 "
            "persistence on BOTH Brier and EV",
        ],
    }
    (out_dir / "rank1a_price_bucket_diagnostic.json").write_text(
        json.dumps(out, indent=2, default=str))
    pd.DataFrame(rows_csv).to_csv(
        out_dir / "rank1a_price_bucket_diagnostic.csv", index=False)
    _write_md(out, out_dir / "rank1a_price_bucket_diagnostic.md")

    print("=" * 64)
    print("RANK 1A PRICE-BUCKET DIAGNOSTIC (diagnostic only)")
    print("=" * 64)
    print(f"  signals: {len(df):,} | reused CSV: {not rebuilt}")
    for label, r in bucket_results.items():
        print(f"  [{label}] n={r['n_total']:>5} "
              f"brier+ {r['positive_brier_splits']}/{r['n_evaluable_splits']} "
              f"ev+ {r['ev_positive_splits']}/{r['n_evaluable_splits']} "
              f"-> {r['bucket_verdict']}")
    print(f"  >>> OVERALL: {overall}")
    print(f"  wrote {out_dir}/rank1a_price_bucket_diagnostic.json (+ md, csv)")
    return 0


def _write_md(out, path):
    L = ["# Rank 1A Price-Bucket Diagnostic (diagnostic only)", "",
         f"**Overall: `{out['overall_label']}`**", "",
         f"- condition signals: {out['condition_signals']:,}",
         f"- fee_rate {out['fee_rate']}, spread_proxy {out['spread_proxy']}", "",
         "## Per-bucket", "",
         "| bucket | n_total | brier+ splits | ev+ splits | robust | verdict |",
         "|---|---|---|---|---|---|"]
    for label, r in out["buckets"].items():
        L.append(f"| {label} | {r['n_total']} | "
                 f"{r['positive_brier_splits']}/{r['n_evaluable_splits']} | "
                 f"{r['ev_positive_splits']}/{r['n_evaluable_splits']} | "
                 f"{r['robust_brier'] and r['robust_ev']} | "
                 f"{r['bucket_verdict']} |")
    L += ["", "## Guardrails"]
    L += [f"- {g}" for g in out["guardrails"]]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
