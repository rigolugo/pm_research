"""Case-level enumeration of the fast-gate blockers. DIAGNOSIS ONLY — changes
no thresholds, excludes nothing. Streams trades one parquet at a time.

Writes:
  probe_blockers_token_multi_condition.csv
  probe_blockers_duplicate_collisions.csv
  probe_blockers_concentration.csv
  probe_blockers_summary.json

The summary models a HYPOTHETICAL exclusion (the blocker conditions) and reports
what the verdict WOULD be after exclusion — without performing it.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib

import pandas as pd

from pm_research.data.store import Store
from pm_research.splits import rolling_train_test_splits

_ams_spec = importlib.util.spec_from_file_location(
    "audit_market_structure",
    str(pathlib.Path(__file__).resolve().parent / "audit_market_structure.py"))
_ams = importlib.util.module_from_spec(_ams_spec)
_ams_spec.loader.exec_module(_ams)

SIZE_TOL = 0.01


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--splits", type=int, default=5)
    ap.add_argument("--robust-pass-splits", type=int, default=4)
    ap.add_argument("--min-test-signals-per-split", type=int, default=50)
    ap.add_argument("--min-train-signals-per-split", type=int, default=100)
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    root_p = pathlib.Path(args.root)
    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    store = Store(args.root)
    markets = store.load_markets()
    resolutions = store.load_resolutions()
    price_cids = {p.stem for p in (root_p / "prices").glob("*.parquet")}

    # --- classify (same source of truth as audit/fast gate) ------------------
    agg, diag = _ams.stream_condition_aggregates(root_p / "trades")
    cc = _ams.classify_from_aggregates(agg, markets, resolutions, price_cids)
    usable_cids = set(cc.loc[cc["usable"], "condition_id"])
    cc_idx = cc.set_index("condition_id")

    # label/title/category maps (best-effort; columns may not all exist)
    title_map, slug_map, cat_map = {}, {}, {}
    if len(markets):
        for _, m in markets.iterrows():
            c = m.get("condition_id")
            cat_map[c] = m.get("category")
            title_map[c] = m.get("title") if "title" in markets.columns else None
            slug_map[c] = m.get("slug") if "slug" in markets.columns else None

    # token -> set(conditions)
    tok_to_conds = {}
    for cid, a in agg.items():
        for tok in a["tokens"]:
            tok_to_conds.setdefault(tok, set()).add(cid)

    # === 1. token_multi_condition blockers (touching usable) =================
    tmc_rows = []
    for tok, conds in tok_to_conds.items():
        if len(conds) <= 1:
            continue
        if not (conds & usable_cids):
            continue                      # only those touching usable
        for c in conds:
            a = agg.get(c, {})
            tmc_rows.append({
                "token_id": tok,
                "condition_id": c,
                "is_usable_binary": c in usable_cids,
                "n_conditions_sharing_token": len(conds),
                "labels": "|".join(sorted(a.get("labels", []))[:4]),
                "class": cc_idx.loc[c, "class"] if c in cc_idx.index else "?",
                "trade_count": a.get("trade_count", 0),
                "first_trade": a.get("first_trade"),
                "category": cat_map.get(c),
                "title": title_map.get(c),
            })
    tmc = pd.DataFrame(tmc_rows)
    # heuristic verdict per token group
    if len(tmc):
        def _tok_verdict(g):
            labs = set(g["labels"])
            if len(labs) == 1:
                return "likely_data_artifact_same_market"
            return "possible_true_semantic_conflict"
        verdicts = tmc.groupby("token_id").apply(_tok_verdict)
        tmc["conflict_assessment"] = tmc["token_id"].map(verdicts)
    tmc.to_csv(out_dir / "probe_blockers_token_multi_condition.csv", index=False)
    tmc_usable_conds = set(tmc.loc[tmc["is_usable_binary"], "condition_id"]) if len(tmc) else set()

    # === 2. duplicate collisions (stream; keep canonical tuple per id) =======
    cols = ["trade_id", "condition_id", "token_id", "outcome_index", "tx_hash",
            "outcome", "side", "price", "size_usdc", "wallet"]
    first_seen = {}        # trade_id -> dict(canonical fields + size + wallet)
    coll_rows = []
    usable_obs = {}        # cid -> usable row count (for concentration)
    for fp in sorted((root_p / "trades").glob("*.parquet")):
        try:
            df = pd.read_parquet(fp, columns=cols)
        except (ValueError, KeyError):
            df = pd.read_parquet(fp)
        if len(df) == 0:
            continue
        inu = df["condition_id"].isin(usable_cids)
        if inu.any():
            for cid, n in df.loc[inu, "condition_id"].value_counts().items():
                usable_obs[cid] = usable_obs.get(cid, 0) + int(n)
        for r in df.itertuples(index=False):
            tid = r.trade_id
            cur = {"tx_hash": getattr(r, "tx_hash", None), "token_id": r.token_id,
                   "condition_id": r.condition_id,
                   "outcome_index": getattr(r, "outcome_index", None),
                   "outcome": getattr(r, "outcome", None),
                   "side": getattr(r, "side", None),
                   "price": round(float(r.price), 6),
                   "size": float(getattr(r, "size_usdc", 0) or 0),
                   "wallet": getattr(r, "wallet", None)}
            if tid not in first_seen:
                first_seen[tid] = cur
                continue
            prev = first_seen[tid]
            canon_prev = (prev["tx_hash"], prev["token_id"], prev["condition_id"],
                          prev["outcome_index"], prev["side"], prev["price"])
            canon_cur = (cur["tx_hash"], cur["token_id"], cur["condition_id"],
                         cur["outcome_index"], cur["side"], cur["price"])
            in_usable = (cur["condition_id"] in usable_cids or
                         prev["condition_id"] in usable_cids)
            if canon_cur != canon_prev:
                ctype = "true_collision"
            elif abs(cur["size"] - prev["size"]) > SIZE_TOL:
                ctype = "float_noise_only"
            elif cur["wallet"] != prev["wallet"]:
                ctype = "harmless_cross_wallet_duplicate"
            else:
                ctype = "unresolved"
            # only record collisions/noise (skip the ~12k benign cross-wallet to keep CSV small,
            # but DO record any that touch usable for evidence)
            if ctype in ("true_collision", "float_noise_only") or (in_usable and ctype != "harmless_cross_wallet_duplicate"):
                coll_rows.append({
                    "trade_id": tid, "collision_type": ctype,
                    "touches_usable_binary": in_usable,
                    "tx_hash_a": prev["tx_hash"], "tx_hash_b": cur["tx_hash"],
                    "token_id_a": prev["token_id"], "token_id_b": cur["token_id"],
                    "condition_id_a": prev["condition_id"], "condition_id_b": cur["condition_id"],
                    "outcome_index_a": prev["outcome_index"], "outcome_index_b": cur["outcome_index"],
                    "outcome_a": prev["outcome"], "outcome_b": cur["outcome"],
                    "side_a": prev["side"], "side_b": cur["side"],
                    "price_a": prev["price"], "price_b": cur["price"],
                    "size_a": prev["size"], "size_b": cur["size"],
                    "wallet_a": prev["wallet"], "wallet_b": cur["wallet"],
                })
        del df
    coll = pd.DataFrame(coll_rows)
    coll.to_csv(out_dir / "probe_blockers_duplicate_collisions.csv", index=False)
    true_coll_usable_conds = set()
    if len(coll):
        m = (coll["collision_type"] == "true_collision") & coll["touches_usable_binary"]
        for _, r in coll[m].iterrows():
            for c in (r["condition_id_a"], r["condition_id_b"]):
                if c in usable_cids:
                    true_coll_usable_conds.add(c)

    # === 3. concentration ====================================================
    obs = pd.Series(usable_obs, dtype="int64").sort_values(ascending=False)
    total_obs = int(obs.sum()); n = len(obs)
    k1 = max(1, int(round(n * 0.01)))
    top1pct_cids = set(obs.head(k1).index)
    dt = pd.to_datetime(pd.Series({c: agg[c]["first_trade"] for c in usable_cids}), utc=True)
    splits = rolling_train_test_splits(
        _span(agg)[0], _span(agg)[1], args.splits)

    def split_membership(cid):
        t = dt.get(cid)
        if t is None:
            return ""
        labels = []
        for i, (trs, tre, tes, tee) in enumerate(splits, 1):
            if pd.Timestamp(tes, tz="UTC") <= t < pd.Timestamp(tee, tz="UTC"):
                labels.append(f"test{i}")
            if pd.Timestamp(trs, tz="UTC") <= t < pd.Timestamp(tre, tz="UTC"):
                labels.append(f"train{i}")
        return "|".join(labels)

    conc_rows = []
    for c, ocount in obs.items():
        conc_rows.append({
            "condition_id": c, "usable_obs_count": int(ocount),
            "share_of_total_usable_obs": ocount / total_obs if total_obs else 0,
            "in_top_1pct": c in top1pct_cids,
            "split_membership": split_membership(c),
            "labels": "|".join(sorted(agg[c]["labels"])[:4]),
            "category": cat_map.get(c), "title": title_map.get(c),
            "slug": slug_map.get(c),
            "resolved": True, "priced": True,   # usable implies both
        })
    conc = pd.DataFrame(conc_rows)
    conc.to_csv(out_dir / "probe_blockers_concentration.csv", index=False)

    # === 4. fix-by-exclusion model ===========================================
    exclude = tmc_usable_conds | true_coll_usable_conds
    post_usable = usable_cids - exclude
    post_obs = obs.drop(labels=[c for c in exclude if c in obs.index], errors="ignore")
    post_total = int(post_obs.sum()); post_n = len(post_obs)
    post_k1 = max(1, int(round(post_n * 0.01)))
    post_top1 = float(post_obs.head(post_k1).sum()) / post_total if post_total else 0.0
    post_top10 = float(post_obs.head(10).sum()) / post_total if post_total else 0.0

    post_dt = dt.drop(labels=[c for c in exclude if c in dt.index], errors="ignore")
    post_per_split = []
    post_max_share = []
    for (trs, tre, tes, tee) in splits:
        test_c = post_dt[(post_dt >= pd.Timestamp(tes, tz="UTC")) &
                         (post_dt < pd.Timestamp(tee, tz="UTC"))].index
        train_c = post_dt[(post_dt >= pd.Timestamp(trs, tz="UTC")) &
                          (post_dt < pd.Timestamp(tre, tz="UTC"))].index
        post_per_split.append({"train": len(train_c), "test": len(test_c)})
        if len(test_c):
            to = post_obs.reindex(test_c).fillna(0)
            post_max_share.append(round(float(to.max()) / float(to.sum()) if to.sum() else 0, 4))
        else:
            post_max_share.append(0.0)

    post_overlap_clean = True   # exclusion removes the overlap conditions by construction
    post_block_conc = (any(s > 0.10 for s in post_max_share) or post_top1 > 0.20)
    post_bar_ok = sum(1 for d in post_per_split
                      if d["train"] >= args.min_train_signals_per_split
                      and d["test"] >= args.min_test_signals_per_split) >= args.robust_pass_splits

    if post_block_conc:
        post_verdict = "BLOCKED_BY_CONCENTRATION"
    elif not post_bar_ok:
        post_verdict = "NEED_FULL_PROBE_DIAGNOSTICS"
    else:
        post_verdict = "CLEAR_WITH_WARNINGS_FOR_RANK1A"

    # concentration alone fixable by exclusion? (overlap/dedup are; concentration
    # is driven by top1% conditions, NOT the blocker set — so report honestly)
    can_fix_by_exclusion = (post_verdict == "CLEAR_WITH_WARNINGS_FOR_RANK1A")

    summary = {
        "token_multi_condition_in_usable_binary": len(tmc_usable_conds),
        "true_duplicate_collisions_in_usable_binary": len(true_coll_usable_conds),
        "top_1pct_condition_share": float(obs.head(k1).sum()) / total_obs if total_obs else 0,
        "top_10_condition_share": float(obs.head(10).sum()) / total_obs if total_obs else 0,
        "conditions_to_exclude_count": len(exclude),
        "post_exclusion_unique_conditions_per_split": [d["test"] for d in post_per_split],
        "post_exclusion_per_split": post_per_split,
        "post_exclusion_max_single_share_per_split": post_max_share,
        "post_exclusion_top_1pct_share": post_top1,
        "post_exclusion_top_10_share": post_top10,
        "post_exclusion_verdict": post_verdict,
        "can_fix_by_exclusion": can_fix_by_exclusion,
        "note": ("concentration is driven by the top-1% highest-observation "
                 "conditions, which are NOT the overlap/dedup blocker set; "
                 "excluding only the blockers will NOT resolve concentration "
                 "unless the blockers happen to be the mega-conditions."),
    }
    (out_dir / "probe_blockers_summary.json").write_text(
        json.dumps(summary, indent=2, default=str))

    print("=" * 64)
    print("PROBE BLOCKER DIAGNOSTIC (case-level, diagnosis only)")
    print("=" * 64)
    print(f"  token->multi-condition usable conditions: {len(tmc_usable_conds)}")
    print(f"  true-collision usable conditions:        {len(true_coll_usable_conds)}")
    print(f"  top_1pct share: {summary['top_1pct_condition_share']:.4f} "
          f"(block >0.20)")
    print(f"  conditions_to_exclude (overlap+dedup):   {len(exclude)}")
    print(f"  POST-exclusion top_1pct: {post_top1:.4f}")
    print(f"  POST-exclusion max single-share/split: {post_max_share}")
    print(f"  POST-exclusion per-split: {[(d['train'],d['test']) for d in post_per_split]}")
    print(f"  can_fix_by_exclusion: {can_fix_by_exclusion}")
    print(f"  >>> POST-EXCLUSION VERDICT: {post_verdict}")
    print(f"  wrote 3 CSVs + probe_blockers_summary.json to {out_dir}")
    return 0


def _span(agg):
    firsts = [a["first_trade"] for a in agg.values() if a["first_trade"] is not None]
    from datetime import date
    return (min(firsts).date(), max(firsts).date()) if firsts else (date.today(), date.today())


if __name__ == "__main__":
    raise SystemExit(main())
