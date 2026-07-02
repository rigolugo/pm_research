"""Audit TRADES join-key readiness for FUTURE OrderFilled matching.

AUDIT ONLY. This does not ingest OrderFilled, does not touch RPC, does not call
any external service, does not infer or backfill missing keys, and does not
mutate stored data. It reads stored trades through the existing Store and
reports the data-quality of the two future join keys added by the prerequisite
patch:

    tx_hash   (Data API transactionHash)
    token_id  (Data API asset / CLOB token id)

Older stored trades predate those columns; Store.load_trades() normalises them
to NA on load, and freshly-parsed-but-absent values are "" — BOTH are treated
as missing here. The report answers: how populated are the keys, is missingness
concentrated anywhere, and are there cardinality risks for a future
TRADES <-> OrderFilled join. It reports quality; it does NOT certify
join correctness.

Interpretation rules baked in:
  - tx_hash with multiple token_id values is NOT bad (one tx can fill several
    assets) -> counted, not flagged as error.
  - token_id with multiple condition_id values IS suspicious -> flagged.
  - trade_id remains the row-level dedup key.
  - tx_hash alone need not be unique; (tx_hash, token_id) may still repeat.

Exit code: 0 on successful audit (regardless of missingness); nonzero only on
an actual runtime error. Old data lacking keys is informational, not a failure.

Run:
    ~/bot1/pm_research/.venv/bin/python scripts/audit_trade_join_keys.py --root ~/data
    (optional) --out-json artifacts/trade_join_key_audit.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from pm_research.data.store import Store
from pm_research.data import schemas


def _present(s: pd.Series) -> pd.Series:
    """Boolean mask of 'present' values: not NA AND not blank/whitespace.

    Treats both pd.NA/None/NaN and empty/whitespace strings as MISSING, since
    old frames normalise to NA and the parser defaults absent fields to "".
    """
    notna = s.notna()
    # stringify only the non-na entries to test for blank; avoids NA coercion
    asstr = s.astype("string")
    nonblank = asstr.str.strip().ne("") & asstr.notna()
    return notna & nonblank


def _pct(n: int, d: int) -> float:
    return (100.0 * n / d) if d else float("nan")


def audit(trades: pd.DataFrame) -> dict:
    """Compute the full audit report dict from a TRADES frame."""
    rep: dict = {}
    total = int(len(trades))
    rep["total_trades"] = total
    if total == 0:
        rep["empty"] = True
        return rep
    rep["empty"] = False

    has_tx = "tx_hash" in trades.columns
    has_tok = "token_id" in trades.columns
    rep["has_tx_hash_column"] = has_tx
    rep["has_token_id_column"] = has_tok

    tx_present = _present(trades["tx_hash"]) if has_tx else pd.Series([False] * total)
    tok_present = _present(trades["token_id"]) if has_tok else pd.Series([False] * total)
    both = tx_present & tok_present

    rep["tx_hash_present"] = int(tx_present.sum())
    rep["tx_hash_present_pct"] = _pct(int(tx_present.sum()), total)
    rep["token_id_present"] = int(tok_present.sum())
    rep["token_id_present_pct"] = _pct(int(tok_present.sum()), total)
    rep["both_present"] = int(both.sum())
    rep["both_present_pct"] = _pct(int(both.sum()), total)

    # ---- missingness by dimension (only over rows MISSING both) -----------
    missing_either = ~both
    rep["missing_either_count"] = int(missing_either.sum())
    dims = {}
    work = trades.copy()
    work["_missing"] = missing_either.values
    if "wallet" in work.columns:
        by = work.groupby("wallet")["_missing"].mean().sort_values(ascending=False)
        dims["by_wallet_top_missing"] = {k: round(float(v), 4)
                                         for k, v in by.head(10).items()}
        dims["wallets_fully_missing"] = int((by >= 0.999).sum())
        dims["wallets_fully_present"] = int((by <= 0.001).sum())
    if "traded_at" in work.columns:
        day = pd.to_datetime(work["traded_at"], utc=True).dt.floor("D")
        by = work.assign(_day=day).groupby("_day")["_missing"].mean()
        # report the date boundary where keys start being present, if any
        present_days = by[by < 0.5].index
        if len(present_days):
            dims["earliest_mostly_present_day"] = str(present_days.min().date())
        dims["days_fully_missing"] = int((by >= 0.999).sum())
        dims["days_fully_present"] = int((by <= 0.001).sum())
    if "condition_id" in work.columns:
        by = work.groupby("condition_id")["_missing"].mean()
        dims["conditions_fully_missing"] = int((by >= 0.999).sum())
        dims["conditions_fully_present"] = int((by <= 0.001).sum())
        dims["conditions_mixed"] = int(((by > 0.001) & (by < 0.999)).sum())
    if "outcome" in work.columns:
        by = work.groupby("outcome")["_missing"].mean()
        n_outcomes = int(len(by))
        dims["distinct_outcomes"] = n_outcomes
        # Only emit the per-outcome breakdown when outcomes are few (genuinely
        # binary-ish). Real data has many NAMED outcomes (team/player names in
        # sports/match markets), which would flood the report with hundreds of
        # entries — so for many-outcome data we report a summary instead.
        if n_outcomes <= 6:
            dims["by_outcome_missing"] = {k: round(float(v), 4)
                                          for k, v in by.items()}
        else:
            dims["by_outcome_missing_summary"] = {
                "distinct_outcomes": n_outcomes,
                "outcomes_fully_missing": int((by >= 0.999).sum()),
                "outcomes_fully_present": int((by <= 0.001).sum()),
                "note": ("many named outcomes (not just YES/NO) — per-outcome "
                         "detail suppressed; see distinct_outcomes"),
            }
            # NB: a binary-YES/NO assumption elsewhere in the pipeline may not
            # hold for these named-outcome markets — worth a separate check.
    rep["missingness_by_dimension"] = dims

    # ---- cardinality / quality diagnostics (over present rows) ------------
    q: dict = {}
    pres = trades[both].copy()
    q["rows_with_both_keys"] = int(len(pres))
    if len(pres):
        q["unique_tx_hash"] = int(pres["tx_hash"].nunique())
        q["unique_token_id"] = int(pres["token_id"].nunique())
        q["unique_tx_token_pairs"] = int(
            pres.groupby(["tx_hash", "token_id"]).ngroups)
        # tx_hash -> multiple token_id : EXPECTED (one tx, several assets); count only
        tx_multi = (pres.groupby("tx_hash")["token_id"].nunique() > 1).sum()
        q["tx_hash_with_multiple_token_id"] = int(tx_multi)
        q["tx_hash_with_multiple_token_id_note"] = (
            "expected/benign: one transaction can fill multiple assets")
        # token_id -> multiple condition_id : SUSPICIOUS -> flag
        if "condition_id" in pres.columns:
            tok_multi_cond = pres.groupby("token_id")["condition_id"].nunique()
            flagged = tok_multi_cond[tok_multi_cond > 1]
            q["token_id_with_multiple_condition_id"] = int(len(flagged))
            q["token_id_multi_condition_FLAGGED"] = (len(flagged) > 0)
            q["token_id_multi_condition_examples"] = list(
                map(str, flagged.head(5).index))
    # ---- duplicate diagnostics (over ALL rows) ----------------------------
    q["duplicate_trade_id_rows"] = int(
        trades["trade_id"].duplicated().sum()) if "trade_id" in trades else None
    fp_cols = [c for c in ("tx_hash", "token_id", "price", "size_usdc",
                           "traded_at") if c in trades.columns]
    if set(("tx_hash", "token_id")).issubset(fp_cols):
        # fingerprint dup count over rows where both keys present
        if len(pres):
            dup = pres.duplicated(subset=fp_cols).sum()
            q["duplicate_fingerprint_rows"] = int(dup)
            q["duplicate_fingerprint_cols"] = fp_cols
            q["duplicate_fingerprint_note"] = (
                "(tx_hash, token_id, price, size, time) may legitimately repeat "
                "if one tx partially fills the same asset multiple times")
    rep["join_key_quality"] = q
    return rep


def _print_report(rep: dict) -> None:
    print("=" * 70)
    print("TRADES JOIN-KEY AUDIT (tx_hash / token_id) — informational")
    print("=" * 70)
    if rep.get("empty"):
        print("  No stored trades found. Nothing to audit.")
        return
    t = rep["total_trades"]
    print(f"  total trades: {t:,}")
    print(f"  tx_hash present : {rep['tx_hash_present']:,} "
          f"({rep['tx_hash_present_pct']:.1f}%)")
    print(f"  token_id present: {rep['token_id_present']:,} "
          f"({rep['token_id_present_pct']:.1f}%)")
    print(f"  BOTH present    : {rep['both_present']:,} "
          f"({rep['both_present_pct']:.1f}%)")
    print()
    dims = rep.get("missingness_by_dimension", {})
    if dims:
        print("  --- missingness concentration ---")
        for k in ("wallets_fully_missing", "wallets_fully_present",
                  "days_fully_missing", "days_fully_present",
                  "earliest_mostly_present_day", "conditions_fully_missing",
                  "conditions_fully_present", "conditions_mixed"):
            if k in dims:
                print(f"    {k}: {dims[k]}")
        if "by_outcome_missing" in dims:
            print(f"    by_outcome_missing: {dims['by_outcome_missing']}")
        elif "by_outcome_missing_summary" in dims:
            s = dims["by_outcome_missing_summary"]
            print(f"    outcomes: {s['distinct_outcomes']} distinct "
                  f"({s['outcomes_fully_missing']} fully-missing, "
                  f"{s['outcomes_fully_present']} fully-present) "
                  f"[per-outcome detail suppressed: many named outcomes]")
    print()
    q = rep.get("join_key_quality", {})
    if q.get("rows_with_both_keys"):
        print("  --- join-key quality (rows with both keys) ---")
        print(f"    rows with both keys      : {q['rows_with_both_keys']:,}")
        print(f"    unique tx_hash           : {q['unique_tx_hash']:,}")
        print(f"    unique token_id          : {q['unique_token_id']:,}")
        print(f"    unique (tx,token) pairs  : {q['unique_tx_token_pairs']:,}")
        print(f"    tx_hash w/ multi token_id: {q['tx_hash_with_multiple_token_id']:,}"
              f"  ({q['tx_hash_with_multiple_token_id_note']})")
        if "token_id_with_multiple_condition_id" in q:
            flag = "  <-- SUSPICIOUS" if q["token_id_multi_condition_FLAGGED"] else ""
            print(f"    token_id w/ multi condition_id: "
                  f"{q['token_id_with_multiple_condition_id']}{flag}")
            if q.get("token_id_multi_condition_examples"):
                print(f"      examples: {q['token_id_multi_condition_examples']}")
        if "duplicate_fingerprint_rows" in q:
            print(f"    duplicate fingerprint rows: {q['duplicate_fingerprint_rows']:,} "
                  f"{q['duplicate_fingerprint_note']}")
    dti = q.get("duplicate_trade_id_rows")
    if dti is not None:
        print(f"    duplicate trade_id rows  : {dti:,} (should be 0 after dedup)")
    print()
    # ---- verdict line ----
    bp = rep["both_present_pct"]
    print("  --- readiness (informational, NOT a certification) ---")
    if bp >= 99.0:
        print("    Keys populated on ~all trades. Join feasible (verify mapping "
              "separately).")
    elif bp <= 1.0:
        print("    Keys essentially absent: stored trades predate the schema "
              "change. A RE-BACKFILL is needed to populate tx_hash/token_id.")
    else:
        print(f"    PARTIAL ({bp:.1f}% have both): mixed old/new data. A "
              "re-backfill is needed to complete coverage before relying on the "
              "join.")
    if q.get("token_id_multi_condition_FLAGGED"):
        print("    WARNING: some token_id map to multiple condition_id — inspect "
              "before trusting token->market mapping.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--out-json", default=None,
                    help="optional path to write the audit report as JSON")
    args = ap.parse_args()

    store = Store(args.root)
    trades = store.load_trades()
    rep = audit(trades)
    _print_report(rep)

    if args.out_json:
        outp = Path(args.out_json)
        outp.parent.mkdir(parents=True, exist_ok=True)
        with open(outp, "w") as fh:
            json.dump(rep, fh, indent=2, default=str)
        print(f"\n  wrote {outp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
