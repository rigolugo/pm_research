"""Fast probe-validity gate for Rank 1A (pooled YES/NO binary forecast-vs-price).

Answers ONLY: is the 8,537-condition usable YES/NO binary universe clean and
independent enough to begin the probe? Does NOT test strategy, does NOT build
the probe. Streams trades one parquet at a time — never materializes 16.5M rows.

Two gates:
  OVERLAP  — do suspicious rows (cardinality contradictions, token->multi-
             condition, true duplicate collisions) touch the USABLE set?
  CONCENTR — is the usable set dominated by a few mega-conditions per split?

Final verdict in:
  CLEAR_WITH_WARNINGS_FOR_RANK1A / BLOCKED_BY_PROBE_OVERLAP /
  BLOCKED_BY_DEDUP_UNCERTAINTY / BLOCKED_BY_CONCENTRATION /
  NEED_FULL_PROBE_DIAGNOSTICS
"""
from __future__ import annotations

import argparse
import json
import pathlib

import pandas as pd

from pm_research.data.store import Store
from pm_research.data import schemas
from pm_research.splits import rolling_train_test_splits

# reuse the audit's classification (single source of truth for "usable")
import importlib.util
_ams_spec = importlib.util.spec_from_file_location(
    "audit_market_structure",
    str(pathlib.Path(__file__).resolve().parent / "audit_market_structure.py"))
_ams = importlib.util.module_from_spec(_ams_spec)
_ams_spec.loader.exec_module(_ams)

SIZE_TOL = 0.01   # USDC; absorbs sub-cent float noise when comparing fills


def run(root: str, params: dict) -> dict:
    root_p = pathlib.Path(root)
    store = Store(root)
    markets = store.load_markets()
    resolutions = store.load_resolutions()
    price_cids = {p.stem for p in (root_p / "prices").glob("*.parquet")}

    # --- Pass 1: stream to classify conditions and get the USABLE set ---------
    agg, diag = _ams.stream_condition_aggregates(root_p / "trades", analysis_hygiene=True)
    cc = _ams.classify_from_aggregates(agg, markets, resolutions, price_cids)
    usable_cids = set(cc.loc[cc["usable"], "condition_id"])
    contra_cids = set(cc.loc[
        cc["reason"].str.startswith("cardinality_contradiction"), "condition_id"])

    # token -> set(condition): rebuild from agg's tokens (already accumulated)
    tok_to_conds: dict = {}
    for cid, a in agg.items():
        for tok in a["tokens"]:
            tok_to_conds.setdefault(tok, set()).add(cid)
    multi_tok_conds = set()
    for tok, conds in tok_to_conds.items():
        if len(conds) > 1:
            multi_tok_conds |= conds          # every condition touched by a shared token

    rep: dict = {
        "provisional_verdict": "PASS_POOLED_YESNO_BINARY_PROBE_PROVISIONAL",
        "total_trades": diag["total_rows"],
        "usable_binary_conditions": len(usable_cids),
        # overlap
        "contradictions_total": len(contra_cids),
        "contradictions_in_usable_binary": len(contra_cids & usable_cids),
        "token_multi_condition_total": diag["token_multi_condition_count"],
        "token_multi_condition_in_usable_binary":
            len(multi_tok_conds & usable_cids),
    }

    # --- Pass 2: stream again, this time collecting per-USABLE-condition obs
    # counts + decision times, and the canonical fill tuples for DUPLICATE
    # trade_ids only (bounded: ~12k dup ids, not 16.5M rows). -----------------
    dup_seen: dict = {}          # trade_id -> first canonical tuple (only for collisions check)
    dup_ids_total = 0
    dup_ids_in_usable = 0
    true_collisions_in_usable = 0
    float_noise_total = 0
    float_noise_in_usable = 0
    seen_ids: set = set()
    usable_obs: dict = {}        # cid -> usable trade row count
    usable_first: dict = {cid: agg[cid]["first_trade"] for cid in usable_cids}

    cols = ["trade_id", "condition_id", "token_id", "outcome_index", "tx_hash",
            "side", "price", "size_usdc", "wallet"]
    for fp in sorted((root_p / "trades").glob("*.parquet")):
        try:
            df = pd.read_parquet(fp, columns=cols)
        except (ValueError, KeyError):
            df = pd.read_parquet(fp)
        if len(df) == 0:
            continue
        # usable obs count (row-level, within usable conditions)
        in_us = df["condition_id"].isin(usable_cids)
        if in_us.any():
            vc = df.loc[in_us, "condition_id"].value_counts()
            for cid, n in vc.items():
                usable_obs[cid] = usable_obs.get(cid, 0) + int(n)
        # duplicate trade_id handling (NA-tolerant canonical compare).
        # Skip null-condition rows (not analysis-eligible). A "true collision"
        # requires two DIFFERENT NON-NULL values in a fill-identity field; an
        # NA-vs-value difference is the same fill with one missing key (a benign
        # cross-wallet duplicate), NOT a collision.
        def _present_scalar(v):
            return v is not None and not (isinstance(v, float) and pd.isna(v)) \
                and str(v).strip() not in ("", "nan", "None")

        for r in df.itertuples(index=False):
            tid = r.trade_id
            if not _present_scalar(r.condition_id):
                continue                          # null-cid: not analysis-eligible
            canon = {"tx_hash": getattr(r, "tx_hash", None), "token_id": r.token_id,
                     "condition_id": r.condition_id,
                     "outcome_index": getattr(r, "outcome_index", None),
                     "side": getattr(r, "side", None),
                     "price": round(float(r.price), 6)}
            size = float(getattr(r, "size_usdc", 0) or 0)
            if tid in seen_ids:
                dup_ids_total += 1
                prev_canon, prev_size = dup_seen[tid]
                is_usable = (r.condition_id in usable_cids
                             or prev_canon["condition_id"] in usable_cids)
                if is_usable:
                    dup_ids_in_usable += 1
                # true collision: any field where BOTH sides are present AND differ
                hard_diff = False
                for k in ("tx_hash", "token_id", "condition_id", "outcome_index",
                          "side", "price"):
                    a, b = prev_canon[k], canon[k]
                    if _present_scalar(a) and _present_scalar(b) and a != b:
                        hard_diff = True
                        break
                size_diff = abs(size - prev_size) > SIZE_TOL
                if hard_diff:
                    if is_usable:
                        true_collisions_in_usable += 1
                elif size_diff:
                    float_noise_total += 1
                    if is_usable:
                        float_noise_in_usable += 1
                # merge: keep the more-populated canonical (fill NA from the other)
                merged = dict(prev_canon)
                for k, v in canon.items():
                    if not _present_scalar(merged.get(k)) and _present_scalar(v):
                        merged[k] = v
                dup_seen[tid] = (merged, prev_size)
            else:
                seen_ids.add(tid)
                dup_seen[tid] = (canon, size)
        del df

    rep["duplicate_trade_ids_total"] = dup_ids_total
    rep["duplicate_trade_ids_in_usable_binary"] = dup_ids_in_usable
    rep["true_duplicate_collisions_in_usable_binary"] = true_collisions_in_usable
    rep["float_noise_cases_total"] = float_noise_total
    rep["float_noise_cases_in_usable_binary"] = float_noise_in_usable

    # --- Concentration over the usable set ------------------------------------
    obs = pd.Series(usable_obs, dtype="int64").sort_values(ascending=False)
    total_obs = int(obs.sum())
    n_cond = len(obs)

    def share(frac):
        k = max(1, int(round(n_cond * frac)))
        return float(obs.head(k).sum()) / total_obs if total_obs else 0.0

    rep["usable_total_observations"] = total_obs
    rep["top_10_condition_share"] = (float(obs.head(10).sum()) / total_obs
                                     if total_obs else 0.0)
    rep["top_1pct_condition_share"] = share(0.01)
    rep["top_5pct_condition_share"] = share(0.05)
    rep["top_10pct_condition_share"] = share(0.10)
    rep["top10_conditions"] = [{"condition_id": c, "obs": int(n)}
                               for c, n in obs.head(10).items()]

    # per-split: condition-level counts + max single-condition share + dedup-adj
    splits = rolling_train_test_splits(params["span_start"], params["span_end"],
                                       params["splits"])
    dt = pd.Series(usable_first)
    dt = pd.to_datetime(dt, utc=True)
    per_split = []
    max_single_share = []
    for (trs, tre, tes, tee) in splits:
        tes_t = pd.Timestamp(tes, tz="UTC"); tee_t = pd.Timestamp(tee, tz="UTC")
        trs_t = pd.Timestamp(trs, tz="UTC"); tre_t = pd.Timestamp(tre, tz="UTC")
        test_cids = dt[(dt >= tes_t) & (dt < tee_t)].index
        train_cids = dt[(dt >= trs_t) & (dt < tre_t)].index
        # condition-level signal counts (what the probe uses)
        test_n = len(test_cids); train_n = len(train_cids)
        # max single-condition share of TEST signals by row-obs
        if test_n:
            test_obs = obs.reindex(test_cids).fillna(0)
            mss = float(test_obs.max()) / float(test_obs.sum()) if test_obs.sum() else 0.0
        else:
            mss = 0.0
        per_split.append({"train_conditions": train_n, "test_conditions": test_n})
        max_single_share.append(round(mss, 4))
    rep["condition_level_counts_per_split"] = per_split
    rep["max_single_condition_share_per_split"] = max_single_share
    rep["unique_conditions_per_split"] = [d["test_conditions"] for d in per_split]
    # duplicate-adjusted == condition-level (we count conditions, not rows)
    rep["duplicate_adjusted_counts_per_split"] = per_split

    # --- Gate logic -----------------------------------------------------------
    overlap_clean = (rep["contradictions_in_usable_binary"] == 0 and
                     rep["token_multi_condition_in_usable_binary"] == 0)
    dedup_clean = (rep["true_duplicate_collisions_in_usable_binary"] == 0)
    split_bar_ok = sum(
        1 for d in per_split
        if d["train_conditions"] >= params["min_train_signals_per_split"]
        and d["test_conditions"] >= params["min_test_signals_per_split"]
    ) >= params["robust_pass_splits"]

    # CONCENTRATION — Rank 1A is CONDITION-LEVEL (one signal per condition), so
    # the BLOCKING metric is per-split single-condition dominance of the SIGNAL
    # count, NOT the row-level (trade-count) top-1% share. A row-level skew does
    # not affect a condition-level probe; it is recorded as a WARNING only.
    block_conc = any(s > 0.10 for s in max_single_share)   # condition-level block
    warnings = []
    if rep["top_1pct_condition_share"] > 0.20:
        warnings.append("row_level_top_1pct_share>0.20 "
                        f"({rep['top_1pct_condition_share']:.3f}) — does NOT "
                        "affect condition-level evaluation")
    if rep["top_10_condition_share"] > 0.10:
        warnings.append(f"top_10_condition_share elevated "
                        f"({rep['top_10_condition_share']:.3f})")
    # always-on standing warnings for Rank 1A scope
    warnings.append("event_independence_unmeasured — defer full probe "
                    "diagnostics until Rank 1A is positive")
    warnings.append("named_binary_excluded — ~40k 2-outcome non-YES/NO markets "
                    "not in the probe universe")
    warnings.append("category_specialist_not_tested — pooled YES/NO only "
                    "(no category metadata)")
    rep["warnings"] = warnings

    if not overlap_clean:
        verdict = "BLOCKED_BY_PROBE_OVERLAP"
    elif not dedup_clean:
        verdict = "BLOCKED_BY_DEDUP_UNCERTAINTY"
    elif block_conc:
        verdict = "BLOCKED_BY_CONCENTRATION"
    elif not split_bar_ok:
        verdict = "NEED_FULL_PROBE_DIAGNOSTICS"
    else:
        verdict = "CLEAR_WITH_WARNINGS_FOR_RANK1A"

    rep["overlap_verdict"] = "CLEAN" if overlap_clean else "DIRTY"
    rep["dedup_verdict"] = "CLEAN" if dedup_clean else "COLLISIONS"
    rep["concentration_verdict"] = (
        "BLOCK" if block_conc
        else "CONDITION_LEVEL_CLEAR" if not warnings
        else "CLEAR_WITH_WARNINGS")
    rep["split_bar_ok"] = split_bar_ok
    rep["fast_gate_verdict"] = verdict
    rep["_cc"] = cc
    rep["_obs"] = obs
    rep["_contra_cids"] = contra_cids
    rep["_multi_tok_conds"] = multi_tok_conds
    rep["_usable_cids"] = usable_cids
    return rep


def _write_artifacts(rep, out_dir: pathlib.Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    cc = rep.pop("_cc"); obs = rep.pop("_obs")
    contra = rep.pop("_contra_cids"); multitok = rep.pop("_multi_tok_conds")
    usable = rep.pop("_usable_cids")
    # JSON
    (out_dir / "probe_fast_gate.json").write_text(
        json.dumps(rep, indent=2, default=str))
    # concentration CSV
    pd.DataFrame([{"condition_id": c, "usable_obs": int(n),
                   "share": (n / rep["usable_total_observations"]
                             if rep["usable_total_observations"] else 0)}
                  for c, n in obs.items()]).to_csv(
        out_dir / "probe_fast_gate_condition_concentration.csv", index=False)
    # suspicious-overlap CSV (rows that touch usable — should be empty)
    overlap_rows = []
    for c in (contra & usable):
        overlap_rows.append({"condition_id": c, "issue": "cardinality_contradiction"})
    for c in (multitok & usable):
        overlap_rows.append({"condition_id": c, "issue": "token_multi_condition"})
    pd.DataFrame(overlap_rows or [{"condition_id": "(none)", "issue": "(none)"}]
                 ).to_csv(out_dir / "probe_fast_gate_suspicious_overlap.csv",
                          index=False)
    # MD report
    L = ["# Fast Probe Gate — Rank 1A (pooled YES/NO binary)", "",
         f"**Fast-gate verdict: `{rep['fast_gate_verdict']}`**", "",
         f"provisional: {rep['provisional_verdict']}", "",
         "## Overlap",
         f"- contradictions in usable: {rep['contradictions_in_usable_binary']} "
         f"(of {rep['contradictions_total']})",
         f"- token->multi-condition in usable: "
         f"{rep['token_multi_condition_in_usable_binary']} "
         f"(of {rep['token_multi_condition_total']})",
         f"- true duplicate collisions in usable: "
         f"{rep['true_duplicate_collisions_in_usable_binary']}",
         f"- float-noise cases in usable: "
         f"{rep['float_noise_cases_in_usable_binary']} "
         f"(of {rep['float_noise_cases_total']})",
         f"- overlap verdict: **{rep['overlap_verdict']}**, "
         f"dedup verdict: **{rep['dedup_verdict']}**", "",
         "## Concentration",
         f"- top-10 condition share: {rep['top_10_condition_share']:.3f}",
         f"- top-1% share: {rep['top_1pct_condition_share']:.3f}",
         f"- top-5% share: {rep['top_5pct_condition_share']:.3f}",
         f"- top-10% share: {rep['top_10pct_condition_share']:.3f}",
         f"- max single-condition share per split: "
         f"{rep['max_single_condition_share_per_split']}",
         f"- unique usable conditions per split: "
         f"{rep['unique_conditions_per_split']}",
         f"- concentration verdict: **{rep['concentration_verdict']}**", ""]
    (out_dir / "probe_fast_gate_report.md").write_text("\n".join(L))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--splits", type=int, default=5)
    ap.add_argument("--robust-pass-splits", type=int, default=4)
    ap.add_argument("--min-test-signals-per-split", type=int, default=50)
    ap.add_argument("--min-train-signals-per-split", type=int, default=100)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    store = Store(args.root)
    # span from streamed first-trade times (computed inside run via agg)
    # quick span: peek at min/max via the audit's streamed agg is done in run();
    # here we need span first, so stream once for span cheaply:
    agg, _ = _ams.stream_condition_aggregates(pathlib.Path(args.root) / "trades", analysis_hygiene=True)
    firsts = [a["first_trade"] for a in agg.values() if a["first_trade"] is not None]
    from datetime import date
    span_start = min(firsts).date() if firsts else date.today()
    span_end = max(firsts).date() if firsts else date.today()
    del agg

    params = {"splits": args.splits, "robust_pass_splits": args.robust_pass_splits,
              "min_test_signals_per_split": args.min_test_signals_per_split,
              "min_train_signals_per_split": args.min_train_signals_per_split,
              "span_start": span_start, "span_end": span_end}

    rep = run(args.root, params)
    out_dir = pathlib.Path(args.out_dir)
    verdict = rep["fast_gate_verdict"]

    print("=" * 64)
    print("FAST PROBE GATE — Rank 1A (pooled YES/NO binary)")
    print("=" * 64)
    print(f"  usable binary conditions: {rep['usable_binary_conditions']:,}")
    print(f"  -- overlap --")
    print(f"  contradictions in usable: {rep['contradictions_in_usable_binary']}"
          f" / {rep['contradictions_total']}")
    print(f"  token->multi-cond in usable: "
          f"{rep['token_multi_condition_in_usable_binary']}"
          f" / {rep['token_multi_condition_total']}")
    print(f"  true dup collisions in usable: "
          f"{rep['true_duplicate_collisions_in_usable_binary']}")
    print(f"  float-noise in usable: {rep['float_noise_cases_in_usable_binary']}"
          f" / {rep['float_noise_cases_total']}")
    print(f"  -- concentration --")
    print(f"  top-10 share: {rep['top_10_condition_share']:.3f} | "
          f"top-1%: {rep['top_1pct_condition_share']:.3f}")
    print(f"  max single-condition share/split: "
          f"{rep['max_single_condition_share_per_split']}")
    print(f"  unique conditions/split: {rep['unique_conditions_per_split']}")
    print(f"  overlap={rep['overlap_verdict']} dedup={rep['dedup_verdict']} "
          f"concentration={rep['concentration_verdict']}")
    if rep.get("warnings"):
        print("  -- warnings (non-blocking) --")
        for w in rep["warnings"]:
            print(f"    * {w}")
    print()
    print(f"  >>> FAST-GATE VERDICT: {verdict}")

    _write_artifacts(rep, out_dir)
    print(f"  wrote {out_dir}/probe_fast_gate.json (+ report, 2 CSVs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
