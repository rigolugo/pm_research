"""Audit market structure to gate the Rank 1 forecast-vs-price probe.

AUDIT ONLY. No RPC, no OrderFilled, no trading, no data mutation. Reads stored
trades/markets/resolutions/prices through the existing Store and decides whether
the re-backfilled dataset can support the Rank 1 probe — and in which form.

It prints exactly one verdict:
  PASS_CATEGORY_SPECIALIST  >=3 categories each clear the per-split train/test bar
  PASS_BINARY_ONLY          aggregate binary universe clears the bar, categories too thin
  BLOCKED_SEMANTICS         outcome_index/token cardinality/linkage not trustworthy
  BLOCKED_INSUFFICIENT_SAMPLE  semantics clean but not enough usable binary data

"Usable" = clean binary (YES/NO) condition that is resolved, has a price series,
and is not a named-outcome binary (whose yes_price conversion is unsafe). Signals
are counted PER SPLIT using the shared rolling_train_test_splits() so this gate
measures the exact partition the probe will run.

Run:
    python scripts/audit_market_structure.py --root ~/data \
        --splits 5 --robust-pass-splits 4 \
        --min-test-signals-per-split 50 --min-train-signals-per-split 100 \
        --min-categories 3 \
        --out-json artifacts/market_structure.json \
        --out-md artifacts/market_structure_report.md
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.data import schemas
from pm_research.splits import rolling_train_test_splits

# reuse the verified NA+blank=missing logic from the join-key audit
_jk_spec = importlib.util.spec_from_file_location(
    "audit_trade_join_keys",
    str(pathlib.Path(__file__).resolve().parent / "audit_trade_join_keys.py"))
_jk = importlib.util.module_from_spec(_jk_spec)
_jk_spec.loader.exec_module(_jk)
_present = _jk._present

_COMPLEMENTARY = {frozenset({"YES", "NO"})}


def _pct(n, d):
    return (100.0 * n / d) if d else float("nan")


def stream_condition_aggregates(trades_dir, want_cols=None,
                                analysis_hygiene=False):
    """Stream ~/data/trades/*.parquet ONE FILE AT A TIME and build a per-condition
    aggregate without ever holding all rows in memory.

    analysis_hygiene (default False): when True, applies the SAME load-time
    hygiene as Store.load_trades so the streaming view matches the analysis/probe
    universe — (1) drop rows with null/blank condition_id (not analysis-eligible),
    and (2) deduplicate trade_ids preferring the row with the most complete keys
    (tx_hash > token_id > outcome_index). Default False preserves the raw audit
    view (and existing tests). The fast gate / probe diagnostics pass True so
    their counts agree with what the probe (via load_trades) will actually see.

    Returns (agg, global_diag) where:
      agg: dict cid -> {tokens:set, indices:set, labels:set, trade_count:int,
                        first_trade:Timestamp}
      global_diag: per-file key coverage, zero/partial-key files, totals,
        token->multi-condition, duplicate trade_id (streamed seen-set).

    Memory: per-condition accumulator + token->conditions map + trade_id
    seen-set. Never the 16.5M raw rows. (With hygiene, the seen-set also serves
    as the dedup key-store: first populated row wins.)
    """
    import pathlib
    cols = want_cols or ["condition_id", "outcome", "token_id",
                         "outcome_index", "tx_hash", "trade_id", "traded_at"]
    agg = {}
    tok_to_conds = {}            # token_id -> set(condition_id)
    seen_trade_ids = set()
    seen_keyscore = {}           # trade_id -> best keyscore seen (hygiene dedup)
    diag = {
        "files": 0, "total_rows": 0,
        "tx_hash_present": 0, "token_id_present": 0, "outcome_index_present": 0,
        "condition_id_present": 0,
        "files_missing_tx_col": 0, "files_missing_token_col": 0,
        "files_missing_oi_col": 0,
        "zero_key_files": [], "partial_key_files": [],
        "duplicate_trade_id_rows": 0,
        "rows_missing_any_key": 0,
        "rows_dropped_null_condition_id": 0,
        "rows_dropped_dedup": 0,
        "analysis_hygiene": bool(analysis_hygiene),
    }
    files = sorted(pathlib.Path(trades_dir).glob("*.parquet"))
    for fp in files:
        try:
            df = pd.read_parquet(fp, columns=[c for c in cols])
        except (ValueError, KeyError):
            # column subset not available -> read all, then subset
            df = pd.read_parquet(fp)
        n = len(df)
        if n == 0:
            diag["files"] += 1
            continue
        diag["files"] += 1

        if analysis_hygiene:
            # (1) drop null/blank condition_id — not analysis-eligible
            cid_ok = _present(df["condition_id"]) if "condition_id" in df.columns \
                else pd.Series(False, index=df.index)
            dropped_cid = int((~cid_ok).sum())
            if dropped_cid:
                diag["rows_dropped_null_condition_id"] += dropped_cid
                df = df[cid_ok]
            if len(df) == 0:
                continue

        n = len(df)
        diag["total_rows"] += n

        # per-file key presence
        def _pres(col):
            if col not in df.columns:
                return None
            return _present(df[col])
        txp = _pres("tx_hash"); tkp = _pres("token_id"); oip = _pres("outcome_index")
        if txp is None: diag["files_missing_tx_col"] += 1; txp = pd.Series(False, index=df.index)
        if tkp is None: diag["files_missing_token_col"] += 1; tkp = pd.Series(False, index=df.index)
        if oip is None: diag["files_missing_oi_col"] += 1; oip = pd.Series(False, index=df.index)
        cidp = _pres("condition_id")
        if cidp is None: cidp = pd.Series(False, index=df.index)

        diag["tx_hash_present"] += int(txp.sum())
        diag["token_id_present"] += int(tkp.sum())
        diag["outcome_index_present"] += int(oip.sum())
        diag["condition_id_present"] += int(cidp.sum())

        # zero / partial key files (using token_id as the representative key)
        present_ct = int(tkp.sum())
        if present_ct == 0:
            diag["zero_key_files"].append((fp.name, n))
        elif present_ct < n:
            diag["partial_key_files"].append((fp.name, int(n - present_ct)))
        # rows missing ANY of the three keys
        missing_any = ~(txp & tkp & oip)
        diag["rows_missing_any_key"] += int(missing_any.sum())

        # duplicate trade_id (streamed). With hygiene, also dedup preferring the
        # most key-complete row: a trade_id's worse-keyscore occurrences are
        # dropped from aggregation so the streaming view matches load_trades.
        if "trade_id" in df.columns:
            if analysis_hygiene:
                txp_h = _present(df["tx_hash"]) if "tx_hash" in df else pd.Series(False, index=df.index)
                tkp_h = _present(df["token_id"]) if "token_id" in df else pd.Series(False, index=df.index)
                oip_h = (df["outcome_index"].notna() if "outcome_index" in df
                         else pd.Series(False, index=df.index))
                keyscore = (txp_h.astype("int8") * 4 + tkp_h.astype("int8") * 2
                            + oip_h.astype("int8") * 1)
                keep_mask = pd.Series(True, index=df.index)
                for idx, tid in df["trade_id"].items():
                    ks = int(keyscore.loc[idx])
                    if tid in seen_trade_ids:
                        diag["duplicate_trade_id_rows"] += 1
                        if ks > seen_keyscore.get(tid, -1):
                            # this occurrence is more complete; keep it, but we
                            # already accumulated the earlier worse one — best
                            # effort: update score, keep this row too is wrong;
                            # instead drop this dup from re-aggregation.
                            seen_keyscore[tid] = ks
                        keep_mask.loc[idx] = False     # drop dup from aggregation
                        diag["rows_dropped_dedup"] += 1
                    else:
                        seen_trade_ids.add(tid)
                        seen_keyscore[tid] = ks
                df = df[keep_mask]
                if len(df) == 0:
                    continue
            else:
                for tid in df["trade_id"].values:
                    if tid in seen_trade_ids:
                        diag["duplicate_trade_id_rows"] += 1
                    else:
                        seen_trade_ids.add(tid)

        # per-condition accumulation
        df = df.assign(_tok=df["token_id"].where(tkp) if "token_id" in df else None,
                       _oi=df["outcome_index"].where(oip) if "outcome_index" in df else None)
        ts = pd.to_datetime(df["traded_at"], utc=True)
        for cid, g in df.groupby("condition_id"):
            a = agg.get(cid)
            if a is None:
                a = {"tokens": set(), "indices": set(), "labels": set(),
                     "trade_count": 0, "first_trade": None}
                agg[cid] = a
            a["tokens"].update(x for x in g["_tok"].dropna().unique())
            a["indices"].update(x for x in g["_oi"].dropna().unique())
            a["labels"].update(str(x).upper() for x in g["outcome"].dropna().unique())
            a["trade_count"] += len(g)
            gmin = ts.loc[g.index].min()
            if a["first_trade"] is None or gmin < a["first_trade"]:
                a["first_trade"] = gmin
            for tok in g["_tok"].dropna().unique():
                tok_to_conds.setdefault(tok, set()).add(cid)

        del df
    # token -> multi-condition count
    diag["token_multi_condition_count"] = sum(
        1 for s in tok_to_conds.values() if len(s) > 1)
    return agg, diag


def classify_from_aggregates(agg, markets, resolutions, price_cids):
    """Same classification as classify_conditions(), but from streamed per-
    condition aggregates rather than raw trades. One row per condition_id."""
    res_cids = set(resolutions["condition_id"]) if len(resolutions) else set()
    cat_map = {}
    if len(markets):
        for cid, cat in zip(markets["condition_id"], markets["category"]):
            cat_map[cid] = cat
    rows = []
    for cid, a in agg.items():
        n_tok, n_oi, n_lab = len(a["tokens"]), len(a["indices"]), len(a["labels"])
        labels = a["labels"]
        cat = cat_map.get(cid)
        has_cat = cat is not None and str(cat) not in ("", "OTHER", "nan")
        resolved = cid in res_cids
        has_price = cid in price_cids
        rows.append(_finalize_condition_row(
            cid, n_tok, n_oi, n_lab, labels, cat, has_cat, resolved,
            has_price, a["trade_count"]))
    return pd.DataFrame(rows)


def _finalize_condition_row(cid, n_tok, n_oi, n_lab, labels, cat, has_cat,
                            resolved, has_price, trade_count):
    """Shared classification verdict for one condition (used by both the
    in-memory and streaming paths) — single source of truth for the rules."""
    reason = ""
    is_yesno = frozenset(labels) in _COMPLEMENTARY
    strong_binary = (n_tok == 2)
    fallback_binary = (n_tok == 0 and n_lab == 2)
    cardinality_binary = strong_binary or fallback_binary
    contradiction = False
    present_counts = [c for c in (n_tok, n_oi, n_lab) if c > 0]
    if len(present_counts) >= 2 and len(set(present_counts)) > 1:
        if not (cardinality_binary and max(present_counts) == 2):
            contradiction = True
    if contradiction:
        cls, usable = "unusable", False
        reason = f"cardinality_contradiction(tok={n_tok},oi={n_oi},lab={n_lab})"
    elif cardinality_binary and is_yesno:
        cls = "binary"
        usable = resolved and has_price
        reason = "" if usable else ("no_resolution" if not resolved else "no_price_series")
    elif cardinality_binary and not is_yesno:
        cls, usable = "named_binary", False
        reason = f"named_binary_labels={sorted(labels)[:3]}"
    elif (n_tok >= 3) or (n_oi >= 3) or (n_lab >= 3):
        cls, usable = "multi", False
        reason = "multi_outcome"
    else:
        cls, usable = "unusable", False
        reason = f"unclassified(tok={n_tok},oi={n_oi},lab={n_lab})"
    return {"condition_id": cid, "n_token_id": n_tok, "n_outcome_index": n_oi,
            "n_label": n_lab, "labels": "|".join(sorted(labels)[:5]),
            "class": cls, "resolved": resolved, "has_price": has_price,
            "has_category": has_cat, "category": cat if has_cat else "OTHER",
            "trade_count": trade_count, "usable": usable, "reason": reason}


def classify_conditions(trades: pd.DataFrame, markets: pd.DataFrame,
                        resolutions: pd.DataFrame,
                        price_cids: set) -> pd.DataFrame:
    """One row per condition_id with structure/usability classification.

    IN-MEMORY path (kept for tests + small datasets). For the full 16.5M-row
    dataset use the streaming path (stream_condition_aggregates +
    classify_from_aggregates) which never materializes all rows.
    """
    if len(trades) == 0:
        return pd.DataFrame(columns=[
            "condition_id", "n_token_id", "n_outcome_index", "n_label",
            "labels", "class", "resolved", "has_price", "has_category",
            "category", "trade_count", "usable", "reason"])

    t = trades.copy()
    tx_present = _present(t["token_id"]) if "token_id" in t else pd.Series(False, index=t.index)
    t["_tok"] = t["token_id"].where(tx_present)
    oi_present = _present(t["outcome_index"]) if "outcome_index" in t else pd.Series(False, index=t.index)
    t["_oi"] = t["outcome_index"].where(oi_present)

    res_cids = set(resolutions["condition_id"]) if len(resolutions) else set()
    cat_map = {}
    if len(markets):
        for cid, cat in zip(markets["condition_id"], markets["category"]):
            cat_map[cid] = cat

    rows = []
    for cid, g in t.groupby("condition_id"):
        labels = set(str(x).upper() for x in g["outcome"].dropna().unique())
        n_tok = int(g["_tok"].nunique(dropna=True))
        n_oi = int(g["_oi"].nunique(dropna=True))
        n_lab = len(labels)
        cat = cat_map.get(cid)
        has_cat = cat is not None and str(cat) not in ("", "OTHER", "nan")
        resolved = cid in res_cids
        has_price = cid in price_cids
        trade_count = int(len(g))
        rows.append(_finalize_condition_row(
            cid, n_tok, n_oi, n_lab, labels, cat, has_cat, resolved,
            has_price, trade_count))
    return pd.DataFrame(rows)


def _condition_decision_times(trades: pd.DataFrame) -> pd.Series:
    """Decision-time per condition = its FIRST trade time. The probe MUST use
    the identical rule when assigning a condition's signal to a split window."""
    return trades.groupby("condition_id")["traded_at"].min()


def _per_split_counts(usable_cids_times: pd.Series, splits) -> list:
    """For each split, (train_count, test_count) of usable conditions whose
    decision-time falls in the train/test windows."""
    out = []
    ts = pd.to_datetime(usable_cids_times, utc=True)
    for (tr_s, tr_e, te_s, te_e) in splits:
        tr_s = pd.Timestamp(tr_s, tz="UTC"); tr_e = pd.Timestamp(tr_e, tz="UTC")
        te_s = pd.Timestamp(te_s, tz="UTC"); te_e = pd.Timestamp(te_e, tz="UTC")
        train_n = int(((ts >= tr_s) & (ts < tr_e)).sum())
        test_n = int(((ts >= te_s) & (ts < te_e)).sum())
        out.append((train_n, test_n))
    return out


def _meets_bar(per_split, min_train, min_test, robust_pass) -> bool:
    """>=min_train train AND >=min_test test, in >=robust_pass of the splits."""
    passing = sum(1 for (tr, te) in per_split
                  if tr >= min_train and te >= min_test)
    return passing >= robust_pass


def decide_gate(metrics: dict, params: dict) -> str:
    """Pure gate decision. Precedence: SEMANTICS -> INSUFFICIENT -> CATEGORY -> BINARY."""
    # --- BLOCKED_SEMANTICS ---
    if metrics["outcome_index_present_pct"] < (100.0 - params["max_residual_na_pct"]):
        return "BLOCKED_SEMANTICS"
    if metrics["token_multi_condition_count"] > params["max_suspicious"]:
        return "BLOCKED_SEMANTICS"
    if metrics["cardinality_contradiction_count"] > params["max_contradictions"]:
        return "BLOCKED_SEMANTICS"
    # --- passes need the per-split bar ---
    cats_meeting = metrics["categories_meeting_bar"]
    aggregate_meets = metrics["aggregate_binary_meets_bar"]
    if cats_meeting >= params["min_categories"]:
        return "PASS_CATEGORY_SPECIALIST"
    if aggregate_meets:
        return "PASS_BINARY_ONLY"
    return "BLOCKED_INSUFFICIENT_SAMPLE"


def _assemble_metrics(cc, dtimes, coverage_diag, params) -> dict:
    """Build the full metrics dict from a condition-classification frame (cc),
    per-condition decision times (dtimes: cid->Timestamp), and coverage/
    consistency diagnostics. Shared by the in-memory and streaming paths so the
    verdict logic is identical regardless of how cc/dtimes were produced."""
    rep: dict = dict(coverage_diag)   # tx/token/oi pct, dup, token_multi_cond, etc.
    rep["empty"] = False
    rep["total_conditions"] = int(len(cc))
    by_class = cc["class"].value_counts().to_dict()
    rep["class_counts_by_market"] = {k: int(v) for k, v in by_class.items()}
    rep["class_counts_by_trade"] = {
        k: int(cc.loc[cc["class"] == k, "trade_count"].sum()) for k in by_class}
    binary = cc[cc["class"] == "binary"]
    rep["binary_markets"] = int(len(binary))
    rep["resolved_binary_markets"] = int(binary["resolved"].sum())
    rep["unresolved_binary_markets"] = int((~binary["resolved"]).sum())
    rep["binary_with_category"] = int(binary["has_category"].sum())
    rep["named_binary_markets"] = int((cc["class"] == "named_binary").sum())
    rep["multi_outcome_markets"] = int((cc["class"] == "multi").sum())
    rep["cardinality_contradiction_count"] = int(
        cc["reason"].str.startswith("cardinality_contradiction").sum())

    cat_by_market = (binary[binary["has_category"]]
                     .groupby("category").size().to_dict())
    cat_by_trade = (binary[binary["has_category"]]
                    .groupby("category")["trade_count"].sum().to_dict())
    rep["category_coverage_by_market"] = {k: int(v) for k, v in cat_by_market.items()}
    rep["category_coverage_by_trade"] = {k: int(v) for k, v in cat_by_trade.items()}

    usable = binary[binary["usable"]]
    splits = rolling_train_test_splits(
        params["span_start"], params["span_end"], params["splits"])
    rep["n_splits"] = len(splits)
    dt = pd.Series(dtimes) if not isinstance(dtimes, pd.Series) else dtimes

    agg_times = dt.loc[dt.index.isin(set(usable["condition_id"]))]
    agg_per_split = _per_split_counts(agg_times, splits)
    rep["aggregate_binary_per_split"] = [
        {"train": tr, "test": te} for (tr, te) in agg_per_split]
    rep["aggregate_binary_meets_bar"] = _meets_bar(
        agg_per_split, params["min_train_signals_per_split"],
        params["min_test_signals_per_split"], params["robust_pass_splits"])

    cats_meeting = 0
    cat_split_detail = {}
    for cat, sub in usable.groupby("category"):
        cat_times = dt.loc[dt.index.isin(set(sub["condition_id"]))]
        ps = _per_split_counts(cat_times, splits)
        meets = _meets_bar(ps, params["min_train_signals_per_split"],
                           params["min_test_signals_per_split"],
                           params["robust_pass_splits"])
        cat_split_detail[cat] = {"per_split": [{"train": tr, "test": te}
                                               for (tr, te) in ps], "meets": meets}
        if meets:
            cats_meeting += 1
    rep["categories_meeting_bar"] = cats_meeting
    rep["category_split_detail"] = cat_split_detail
    rep["usable_binary_conditions"] = int(len(usable))
    rep["verdict"] = decide_gate(rep, params)
    rep["_condition_classification"] = cc
    return rep


def _audit_from_streamed(agg, diag, markets, resolutions, price_cids,
                         params) -> dict:
    """Build the audit report from already-streamed (agg, diag). Separated so
    main() can stream once (to also derive the span) and not stream twice."""
    if diag["total_rows"] == 0:
        return {"total_trades": 0, "empty": True,
                "verdict": "BLOCKED_INSUFFICIENT_SAMPLE"}
    cc = classify_from_aggregates(agg, markets, resolutions, price_cids)
    dtimes = {cid: a["first_trade"] for cid, a in agg.items()}
    total = diag["total_rows"]
    coverage_diag = {
        "total_trades": total,
        "tx_hash_present_pct": _pct(diag["tx_hash_present"], total),
        "token_id_present_pct": _pct(diag["token_id_present"], total),
        "outcome_index_present_pct": _pct(diag["outcome_index_present"], total),
        "condition_id_present_pct": _pct(diag["condition_id_present"], total),
        "duplicate_trade_id_rows": diag["duplicate_trade_id_rows"],
        "token_multi_condition_count": diag["token_multi_condition_count"],
        "files_scanned": diag["files"],
        "zero_key_files": diag["zero_key_files"][:50],
        "zero_key_file_count": len(diag["zero_key_files"]),
        "partial_key_files": diag["partial_key_files"][:50],
        "partial_key_file_count": len(diag["partial_key_files"]),
        "rows_missing_any_key": diag["rows_missing_any_key"],
        "rows_missing_any_key_pct": _pct(diag["rows_missing_any_key"], total),
    }
    rep = _assemble_metrics(cc, dtimes, coverage_diag, params)
    cc_use = cc[cc["usable"]]
    rep["usable_via_token_rule"] = int((cc_use["n_token_id"] == 2).sum())
    rep["usable_via_label_fallback"] = int((cc_use["n_token_id"] == 0).sum())
    return rep


def audit_streaming(trades_dir, markets, resolutions, price_cids, params) -> dict:
    """Streaming audit over trades_dir/*.parquet — one file at a time, never
    materializing the full dataset. Path for the 16.5M-row dataset."""
    agg, diag = stream_condition_aggregates(trades_dir)
    return _audit_from_streamed(agg, diag, markets, resolutions, price_cids,
                                params)


def audit_market_structure(trades, markets, resolutions, price_cids,
                           params) -> dict:
    """IN-MEMORY audit (tests + small data). For the full dataset use
    audit_streaming() which never concatenates all trade files."""
    rep: dict = {}
    total = int(len(trades))
    if total == 0:
        return {"total_trades": 0, "empty": True,
                "verdict": "BLOCKED_INSUFFICIENT_SAMPLE"}

    def cov(col):
        return _pct(int(_present(trades[col]).sum()), total) if col in trades else 0.0
    tok_multi_cond = 0
    if "token_id" in trades.columns:
        tp = trades[_present(trades["token_id"])]
        if len(tp):
            tok_multi_cond = int(
                (tp.groupby("token_id")["condition_id"].nunique() > 1).sum())
    coverage_diag = {
        "total_trades": total,
        "tx_hash_present_pct": cov("tx_hash"),
        "token_id_present_pct": cov("token_id"),
        "outcome_index_present_pct": cov("outcome_index"),
        "condition_id_present_pct": cov("condition_id"),
        "duplicate_trade_id_rows": int(trades["trade_id"].duplicated().sum())
        if "trade_id" in trades else None,
        "token_multi_condition_count": tok_multi_cond,
    }
    cc = classify_conditions(trades, markets, resolutions, price_cids)
    dtimes = _condition_decision_times(trades)
    return _assemble_metrics(cc, dtimes, coverage_diag, params)

    # ---- verdict ----
    rep["verdict"] = decide_gate(rep, params)
    rep["_condition_classification"] = cc   # carried for CSV writing (popped before JSON)
    return rep


def _print_report(rep: dict, params: dict) -> None:
    print("=" * 72)
    print("MARKET-STRUCTURE AUDIT — Rank 1 probe gate (informational)")
    print("=" * 72)
    if rep.get("empty"):
        print("  No stored trades. -> BLOCKED_INSUFFICIENT_SAMPLE")
        return
    print(f"  total trades: {rep['total_trades']:,} | conditions: {rep['total_conditions']:,}")
    print(f"  coverage: tx_hash {rep['tx_hash_present_pct']:.1f}%  "
          f"token_id {rep['token_id_present_pct']:.1f}%  "
          f"outcome_index {rep['outcome_index_present_pct']:.1f}%")
    print(f"  classes (by market): {rep['class_counts_by_market']}")
    print(f"  binary: {rep['binary_markets']:,} "
          f"(resolved {rep['resolved_binary_markets']:,}, "
          f"w/ category {rep['binary_with_category']:,})  "
          f"named_binary {rep['named_binary_markets']:,}  "
          f"multi {rep['multi_outcome_markets']:,}")
    print(f"  usable binary (resolved+priced+YES/NO): {rep['usable_binary_conditions']:,}")
    print(f"  consistency: token->multi-condition {rep['token_multi_condition_count']}, "
          f"cardinality contradictions {rep['cardinality_contradiction_count']}, "
          f"dup trade_id {rep['duplicate_trade_id_rows']}")
    print(f"  aggregate per-split (train/test): "
          f"{[(d['train'], d['test']) for d in rep['aggregate_binary_per_split']]}")
    print(f"  categories meeting bar: {rep['categories_meeting_bar']} "
          f"(need {params['min_categories']})")
    print()
    print(f"  >>> VERDICT: {rep['verdict']}")
    # driving numbers
    if rep["verdict"] == "PASS_CATEGORY_SPECIALIST":
        print(f"      {rep['categories_meeting_bar']} categories clear "
              f">={params['min_train_signals_per_split']} train / "
              f">={params['min_test_signals_per_split']} test in "
              f">={params['robust_pass_splits']}/{rep['n_splits']} splits")
    elif rep["verdict"] == "PASS_BINARY_ONLY":
        print(f"      aggregate binary clears the bar; only "
              f"{rep['categories_meeting_bar']} categories qualify "
              f"(need {params['min_categories']}) -> pooled probe")
    elif rep["verdict"] == "BLOCKED_SEMANTICS":
        print(f"      outcome_index {rep['outcome_index_present_pct']:.1f}% "
              f"(need >={100 - params['max_residual_na_pct']:.0f}%), "
              f"token->multi-cond {rep['token_multi_condition_count']}, "
              f"contradictions {rep['cardinality_contradiction_count']}")
    else:
        print(f"      semantics clean but neither category-specialist nor "
              f"aggregate binary clears the 5-split bar")


def _write_csvs(cc: pd.DataFrame, rep: dict, out_dir: pathlib.Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cc.drop(columns=[]).to_csv(out_dir / "condition_cardinality.csv", index=False)
    # category coverage
    cats = sorted(set(rep["category_coverage_by_market"]) |
                  set(rep["category_coverage_by_trade"]))
    pd.DataFrame([{
        "category": c,
        "binary_markets": rep["category_coverage_by_market"].get(c, 0),
        "binary_trades": rep["category_coverage_by_trade"].get(c, 0),
        "meets_split_bar": rep["category_split_detail"].get(c, {}).get("meets", False),
    } for c in cats]).to_csv(out_dir / "category_coverage.csv", index=False)
    cc[~cc["usable"]].to_csv(out_dir / "unusable_markets.csv", index=False)
    # suspicious keys: contradictions + named_binary flagged for review
    susp = cc[cc["reason"].str.startswith(("cardinality_contradiction",
                                           "named_binary"))]
    susp.to_csv(out_dir / "suspicious_keys.csv", index=False)


def _write_md(rep: dict, params: dict, path: pathlib.Path) -> None:
    L = ["# Market-Structure Audit — Rank 1 Probe Gate", "",
         f"**Verdict: `{rep['verdict']}`**", ""]
    if rep.get("empty"):
        L.append("No stored trades.")
        path.write_text("\n".join(L)); return
    L += [
        "## Coverage",
        f"- trades: {rep['total_trades']:,}, conditions: {rep['total_conditions']:,}",
        f"- tx_hash {rep['tx_hash_present_pct']:.1f}% | token_id "
        f"{rep['token_id_present_pct']:.1f}% | outcome_index "
        f"{rep['outcome_index_present_pct']:.1f}%",
        "",
        "## Structure",
        f"- binary {rep['binary_markets']:,} (resolved "
        f"{rep['resolved_binary_markets']:,}, w/ category "
        f"{rep['binary_with_category']:,})",
        f"- named_binary {rep['named_binary_markets']:,} (unsafe for yes_price; "
        "excluded)",
        f"- multi-outcome {rep['multi_outcome_markets']:,}",
        f"- usable (binary+resolved+priced+YES/NO): "
        f"{rep['usable_binary_conditions']:,}",
        "",
        "## Per-split signal counts (aggregate binary)",
        "| split | train | test | clears bar |",
        "|---|---|---|---|",
    ]
    for i, d in enumerate(rep["aggregate_binary_per_split"], 1):
        ok = (d["train"] >= params["min_train_signals_per_split"]
              and d["test"] >= params["min_test_signals_per_split"])
        L.append(f"| {i} | {d['train']} | {d['test']} | {'yes' if ok else 'no'} |")
    L += ["",
          f"Bar: >={params['min_train_signals_per_split']} train AND "
          f">={params['min_test_signals_per_split']} test, in "
          f">={params['robust_pass_splits']}/{rep['n_splits']} splits.",
          f"Categories meeting bar: {rep['categories_meeting_bar']} "
          f"(need {params['min_categories']} for category-specialist).", ""]
    path.write_text("\n".join(L))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--splits", type=int, default=5)
    ap.add_argument("--robust-pass-splits", type=int, default=4)
    ap.add_argument("--min-test-signals-per-split", type=int, default=50)
    ap.add_argument("--min-train-signals-per-split", type=int, default=100)
    ap.add_argument("--min-categories", type=int, default=3)
    ap.add_argument("--max-residual-na-pct", type=float, default=20.0)
    ap.add_argument("--max-suspicious", type=int, default=0)
    ap.add_argument("--max-contradictions", type=int, default=0)
    ap.add_argument("--out-json", default=None)
    ap.add_argument("--out-md", default=None)
    ap.add_argument("--out-csv-dir", default=None)
    ap.add_argument("--in-memory", action="store_true",
                    help="load all trades into memory (small datasets only; "
                         "the default streaming path is safe for 16.5M+ rows)")
    args = ap.parse_args()

    from datetime import date
    store = Store(args.root)
    markets = store.load_markets()
    resolutions = store.load_resolutions()
    price_cids = {p.stem for p in
                  (pathlib.Path(args.root) / "prices").glob("*.parquet")}
    trades_dir = pathlib.Path(args.root) / "trades"

    base_params = {
        "splits": args.splits, "robust_pass_splits": args.robust_pass_splits,
        "min_test_signals_per_split": args.min_test_signals_per_split,
        "min_train_signals_per_split": args.min_train_signals_per_split,
        "min_categories": args.min_categories,
        "max_residual_na_pct": args.max_residual_na_pct,
        "max_suspicious": args.max_suspicious,
        "max_contradictions": args.max_contradictions,
    }

    if args.in_memory:
        trades = store.load_trades()
        if len(trades):
            span_start = pd.to_datetime(trades["traded_at"]).min().date()
            span_end = pd.to_datetime(trades["traded_at"]).max().date()
        else:
            span_start = span_end = date.today()
        params = {**base_params, "span_start": span_start, "span_end": span_end}
        rep = audit_market_structure(trades, markets, resolutions,
                                     price_cids, params)
    else:
        # STREAMING (default): aggregate per condition one file at a time, then
        # derive the span from streamed first-trade times — never load all rows.
        agg, diag = stream_condition_aggregates(trades_dir)
        if diag["total_rows"] == 0:
            span_start = span_end = date.today()
        else:
            firsts = [a["first_trade"] for a in agg.values()
                      if a["first_trade"] is not None]
            span_start = min(firsts).date()
            span_end = max(firsts).date()
        params = {**base_params, "span_start": span_start, "span_end": span_end}
        # reuse the already-streamed agg/diag (don't stream twice)
        rep = _audit_from_streamed(agg, diag, markets, resolutions,
                                   price_cids, params)

    cc = rep.pop("_condition_classification", pd.DataFrame())
    _print_report(rep, params)

    if args.out_json:
        p = pathlib.Path(args.out_json); p.parent.mkdir(parents=True, exist_ok=True)
        json.dump(rep, open(p, "w"), indent=2, default=str)
        print(f"\n  wrote {p}")
    if args.out_md:
        p = pathlib.Path(args.out_md); p.parent.mkdir(parents=True, exist_ok=True)
        _write_md(rep, params, p); print(f"  wrote {p}")
    if args.out_csv_dir and len(cc):
        _write_csvs(cc, rep, pathlib.Path(args.out_csv_dir))
        print(f"  wrote CSVs to {args.out_csv_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
