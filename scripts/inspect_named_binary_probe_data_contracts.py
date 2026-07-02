#!/usr/bin/env python
"""READ-ONLY inspection for the named-binary probe data-contract layer.

Purpose: capture the EXACT real schemas / API surfaces that P1 must consume, so
the DATA_CONTRACTS_named_binary_probe.md file records them instead of any future
chat inferring them from memory. This is the direct fix for the P1 failure
(assumed artifact/API shapes that were never documented).

STRICTLY READ-ONLY. This script:
  - reads artifacts + inspects module signatures ONLY,
  - writes ONE report file (its own output) and nothing else,
  - does NOT modify any artifact, gate, script, or test,
  - does NOT score, split, compute Brier/log-loss/calibration/reliability,
  - does NOT compute decision timestamps or canonical_side_price,
  - does NOT touch log_index, wallets, OrdersMatched, or PnL,
  - does NOT flip named_binary_probe_blocked.

It only loads trades/prices IF --probe-store-shapes is passed, and even then it
reads at most a tiny head to report column names/dtypes — it computes no
features. Default run does NOT touch trades/prices at all.

Usage (PowerShell, env pmresearch):
  $env:PYTHONPATH="C:\\b1\\pm_research"
  cd C:\\b1\\pm_research
  python scripts\\inspect_named_binary_probe_data_contracts.py `
      --root C:\\b1\\data --artifacts-dir artifacts `
      --out artifacts\\named_binary_probe\\data_contract_inspection.txt

Paste the produced .txt (and stdout) back into the chat.
"""

from __future__ import annotations

import argparse
import inspect
import io
import json
import os
import sys
import traceback


def _sec(title, buf):
    buf.write("\n" + "=" * 78 + "\n")
    buf.write(f"## {title}\n")
    buf.write("=" * 78 + "\n")


def _short(v, n=24):
    s = str(v)
    return s if len(s) <= n else s[:12] + "..." + s[-6:]


# ---------------------------------------------------------------------------
# 1. classification contract JSON
# ---------------------------------------------------------------------------

def inspect_contract(artifacts_dir, buf):
    _sec("1. named_binary_classification_contract.json", buf)
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_classification_contract.json"
    )
    buf.write(f"path: {path}\n")
    if not os.path.exists(path):
        buf.write("MISSING\n")
        return
    with open(path, "r", encoding="utf-8") as fh:
        obj = json.load(fh)
    buf.write(f"top_level_type: {type(obj).__name__}\n")
    if isinstance(obj, dict):
        buf.write(f"top_level_keys: {list(obj.keys())}\n")
        for k in ("nb_contract_version", "contract_version", "version"):
            if k in obj:
                buf.write(f"version_field[{k}]: {obj[k]}\n")
        # locate where condition records live
        records = None
        record_holder = None
        for key in ("conditions", "rows", "records", "contract", "items"):
            val = obj.get(key)
            if isinstance(val, list) and val:
                records, record_holder = val, key
                break
            if isinstance(val, dict) and val:
                records = list(val.values())
                record_holder = f"{key} (dict-keyed by condition_id)"
                break
        buf.write(f"records_holder: {record_holder}\n")
        if records is None:
            buf.write("records: NOT a list/dict under common keys — DUMP top-level:\n")
            buf.write(json.dumps({k: type(v).__name__ for k, v in obj.items()},
                                 indent=2) + "\n")
            return
        buf.write(f"record_count: {len(records)}\n")
        sample = records[0]
        if isinstance(sample, dict):
            buf.write(f"record_keys: {list(sample.keys())}\n")
            # identify likely fields
            id_fields = [k for k in sample if "condition" in k.lower()
                         or k.lower() in ("id", "cid")]
            sub_fields = [k for k in sample if "subclass" in k.lower()
                          or "category" in k.lower() or "class" in k.lower()]
            elig_fields = [k for k in sample if "elig" in k.lower()]
            buf.write(f"likely_condition_id_fields: {id_fields}\n")
            buf.write(f"likely_subclass_fields: {sub_fields}\n")
            buf.write(f"likely_eligibility_fields: {elig_fields}\n")
            # subclass vocabulary
            for sf in (sub_fields or []):
                vocab = sorted({str(r.get(sf)) for r in records
                                if isinstance(r, dict)})
                buf.write(f"subclass_vocab[{sf}] ({len(vocab)}): {vocab}\n")
            # eligibility value distribution
            for ef in (elig_fields or []):
                from collections import Counter
                dist = Counter(str(r.get(ef)) for r in records
                               if isinstance(r, dict))
                buf.write(f"eligibility_dist[{ef}]: {dict(dist)}\n")
            # per-subclass eligible counts (best-effort)
            if sub_fields:
                sf = sub_fields[0]
                from collections import Counter
                by_sc = Counter(str(r.get(sf)) for r in records
                                if isinstance(r, dict))
                buf.write(f"per_subclass_record_counts[{sf}]: {dict(by_sc)}\n")
            # sample record with long ids shortened
            shortened = {k: _short(v) for k, v in sample.items()}
            buf.write("sample_record (ids shortened):\n")
            buf.write(json.dumps(shortened, indent=2) + "\n")
        else:
            buf.write(f"record_type: {type(sample).__name__} (unexpected)\n")
    else:
        buf.write(f"top_level is {type(obj).__name__}; first-item type: "
                  f"{type(obj[0]).__name__ if obj else 'empty'}\n")


# ---------------------------------------------------------------------------
# 2. resolution_source_rows.parquet
# ---------------------------------------------------------------------------

def inspect_resolution_rows(artifacts_dir, buf):
    _sec("2. named_binary_resolution_source_rows.parquet", buf)
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_resolution_source_rows.parquet"
    )
    buf.write(f"path: {path}\n")
    if not os.path.exists(path):
        buf.write("MISSING\n")
        return
    try:
        import pandas as pd
    except ImportError as e:
        buf.write(f"pandas unavailable: {e}\n")
        return
    df = pd.read_parquet(path)
    buf.write(f"row_count: {len(df)}\n")
    buf.write(f"columns: {list(df.columns)}\n")
    buf.write("dtypes:\n")
    for c in df.columns:
        buf.write(f"  {c}: {df[c].dtype}\n")
    for col in ("status", "subclass", "nb_subclass", "source_table"):
        if col in df.columns:
            vals = sorted({str(v) for v in df[col].dropna().unique()})
            buf.write(f"unique[{col}] ({len(vals)}): {vals}\n")
    # winner columns
    winner_cols = [c for c in df.columns if "winner" in c.lower()
                   or "won" in c.lower() or "outcome_index" in c.lower()
                   or "token" in c.lower()]
    buf.write(f"winner_related_columns: {winner_cols}\n")
    buf.write(f"has_oriented_side_won: {'oriented_side_won' in df.columns}\n")
    # nb_contract_version values
    for vf in ("nb_contract_version", "contract_version"):
        if vf in df.columns:
            vv = sorted({str(v) for v in df[vf].dropna().unique()})
            buf.write(f"version_values[{vf}]: {vv}\n")
    # per-subclass status crosstab (counts only)
    sc_col = "subclass" if "subclass" in df.columns else (
        "nb_subclass" if "nb_subclass" in df.columns else None)
    if sc_col and "status" in df.columns:
        ct = df.groupby([sc_col, "status"]).size().reset_index(name="n")
        buf.write("per_subclass_status_counts:\n")
        for _, r in ct.iterrows():
            buf.write(f"  {r[sc_col]} / {r['status']}: {r['n']}\n")
    elif sc_col:
        buf.write("per_subclass_counts:\n")
        for k, n in df[sc_col].value_counts().items():
            buf.write(f"  {k}: {n}\n")
    # one sample row, ids shortened
    if len(df):
        row0 = {c: _short(df.iloc[0][c]) for c in df.columns}
        buf.write("sample_row (ids shortened):\n")
        buf.write(json.dumps(row0, indent=2, default=str) + "\n")


# ---------------------------------------------------------------------------
# 3. resolution_conflicts.csv
# ---------------------------------------------------------------------------

def inspect_conflicts(artifacts_dir, buf):
    _sec("3. named_binary_resolution_conflicts.csv", buf)
    path = os.path.join(
        artifacts_dir, "named_binary", "named_binary_resolution_conflicts.csv"
    )
    buf.write(f"path: {path}\n")
    if not os.path.exists(path):
        buf.write("MISSING (P0 falls back to gate per_subclass_breakdown)\n")
        return
    try:
        import pandas as pd
    except ImportError as e:
        buf.write(f"pandas unavailable: {e}\n")
        return
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    buf.write(f"row_count: {len(df)}\n")
    buf.write(f"columns: {list(df.columns)}\n")
    for col in ("status", "subclass", "nb_subclass"):
        if col in df.columns:
            vals = sorted({str(v) for v in df[col].unique()})
            buf.write(f"unique[{col}] ({len(vals)}): {vals}\n")
    sc_col = "subclass" if "subclass" in df.columns else (
        "nb_subclass" if "nb_subclass" in df.columns else None)
    if sc_col and "status" in df.columns:
        ct = df.groupby([sc_col, "status"]).size().reset_index(name="n")
        buf.write("per_subclass_status_counts:\n")
        for _, r in ct.iterrows():
            buf.write(f"  {r[sc_col]} / {r['status']}: {r['n']}\n")
    elif sc_col:
        buf.write("per_subclass_counts:\n")
        for k, n in df[sc_col].value_counts().items():
            buf.write(f"  {k}: {n}\n")
    if len(df):
        row0 = {c: _short(df.iloc[0][c]) for c in df.columns}
        buf.write("sample_row (ids shortened):\n")
        buf.write(json.dumps(row0, indent=2, default=str) + "\n")


# ---------------------------------------------------------------------------
# 4. p0_preflight.json
# ---------------------------------------------------------------------------

def inspect_p0(artifacts_dir, buf):
    _sec("4. p0_preflight.json", buf)
    path = os.path.join(artifacts_dir, "named_binary_probe", "p0_preflight.json")
    buf.write(f"path: {path}\n")
    if not os.path.exists(path):
        buf.write("MISSING\n")
        return
    with open(path, "r", encoding="utf-8") as fh:
        obj = json.load(fh)
    buf.write(f"top_level_keys: {list(obj.keys())}\n")
    for k in ("stage", "p0_state", "authorized_scope",
              "probe_execution_authorized", "named_binary_probe_blocked_observed",
              "nb_contract_version_expected", "nb_contract_version_contract",
              "nb_contract_version_resolution_source"):
        buf.write(f"{k}: {obj.get(k)}\n")
    buf.write("counts_pooled:\n")
    buf.write(json.dumps(obj.get("counts_pooled", {}), indent=2) + "\n")
    buf.write("counts_by_subclass:\n")
    buf.write(json.dumps(obj.get("counts_by_subclass", {}), indent=2) + "\n")
    buf.write("gate_snapshot keys: "
              f"{list((obj.get('gate_snapshot') or {}).keys())}\n")
    buf.write("reconciliation keys: "
              f"{list((obj.get('reconciliation') or {}).keys())}\n")


# ---------------------------------------------------------------------------
# 5. pm_research.data.store
# ---------------------------------------------------------------------------

def _sig(obj):
    try:
        return str(inspect.signature(obj))
    except (TypeError, ValueError):
        return "<no signature>"


def inspect_store(buf):
    _sec("5. pm_research.data.store", buf)
    try:
        from pm_research.data import store as st
    except Exception as e:
        buf.write(f"IMPORT FAILED: {e}\n{traceback.format_exc()}\n")
        return
    buf.write(f"module_file: {getattr(st, '__file__', '?')}\n")
    names = [n for n in dir(st) if not n.startswith("_")]
    buf.write(f"public_names: {names}\n")
    for fn in ("load_trades", "load_prices", "load_resolutions", "load_markets"):
        if hasattr(st, fn):
            buf.write(f"{fn}{_sig(getattr(st, fn))}\n")
    if hasattr(st, "Store"):
        buf.write(f"Store.__init__{_sig(st.Store.__init__)}\n")
        methods = [m for m in dir(st.Store) if not m.startswith("_")]
        buf.write(f"Store methods: {methods}\n")
    # schema constants if present
    try:
        from pm_research.data import schemas as sch
        for cname in ("TRADES_COLS", "PRICES_COLS", "RESOLUTIONS_COLS",
                      "MARKETS_COLS"):
            if hasattr(sch, cname):
                buf.write(f"schemas.{cname}: {getattr(sch, cname)}\n")
    except Exception as e:
        buf.write(f"schemas import note: {e}\n")


# ---------------------------------------------------------------------------
# 6. pm_research.semantics.named_binary
# ---------------------------------------------------------------------------

def inspect_semantics(buf):
    _sec("6. pm_research.semantics.named_binary", buf)
    try:
        from pm_research.semantics import named_binary as nb
    except Exception as e:
        buf.write(f"IMPORT FAILED: {e}\n{traceback.format_exc()}\n")
        return
    buf.write(f"module_file: {getattr(nb, '__file__', '?')}\n")
    names = [n for n in dir(nb) if not n.startswith("_")]
    buf.write(f"public_names: {names}\n")
    # functions/classes of interest
    for n in names:
        obj = getattr(nb, n)
        if inspect.isfunction(obj) or inspect.isclass(obj):
            kind = "class" if inspect.isclass(obj) else "func"
            if any(tok in n.lower() for tok in
                   ("price", "orient", "canonical", "side", "classif")):
                buf.write(f"[{kind}] {n}{_sig(obj)}\n")
                doc = (inspect.getdoc(obj) or "").strip().splitlines()
                if doc:
                    buf.write(f"    doc: {doc[0]}\n")
    # look for the lexicon version + orientation audit field names
    try:
        from pm_research.semantics import lexicon as lex
        if hasattr(lex, "NB_CONTRACT_VERSION"):
            buf.write(f"lexicon.NB_CONTRACT_VERSION: {lex.NB_CONTRACT_VERSION}\n")
    except Exception as e:
        buf.write(f"lexicon import note: {e}\n")


# ---------------------------------------------------------------------------
# 7. scripts/forecast_vs_price.py (Rank 1A) — warm-up policy reuse
# ---------------------------------------------------------------------------

def inspect_rank1a(root_repo, buf):
    _sec("7. scripts/forecast_vs_price.py — warm-up / decision policy", buf)
    path = os.path.join(root_repo, "scripts", "forecast_vs_price.py")
    buf.write(f"path: {path}\n")
    if not os.path.exists(path):
        buf.write("MISSING at scripts/forecast_vs_price.py — search repo:\n")
    hits = []
    for base, _dirs, files in os.walk(root_repo):
        if ".git" in base or "site-packages" in base:
            continue
        for f in files:
            if f.endswith(".py"):
                fp = os.path.join(base, f)
                try:
                    txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                for kw in ("warmup", "warm_up", "warmup_seconds",
                           "first_price_after_warmup", "3600"):
                    if kw in txt:
                        # record file + the matching lines
                        for i, line in enumerate(txt.splitlines(), 1):
                            if kw in line:
                                hits.append((os.path.relpath(fp, root_repo),
                                             kw, i, line.strip()[:120]))
    if not hits:
        buf.write("NO warmup/3600/first_price_after_warmup references found.\n")
        buf.write("=> P1 must PIN warmup_seconds=3600 per documented Rank 1A "
                  "policy (DECISION_LOG first_price_after_warmup).\n")
    else:
        buf.write("references (file / keyword / line# / text):\n")
        seen = set()
        for fp, kw, ln, txt in hits:
            key = (fp, ln)
            if key in seen:
                continue
            seen.add(key)
            buf.write(f"  {fp}:{ln} [{kw}] {txt}\n")


# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="READ-ONLY data-contract inspection "
                                             "for the named-binary probe.")
    ap.add_argument("--root", default="C:\\b1\\data",
                    help="data root (unused unless --probe-store-shapes)")
    ap.add_argument("--artifacts-dir", default="artifacts")
    ap.add_argument("--repo", default=".",
                    help="repo root for scripts/pm_research search (default cwd)")
    ap.add_argument("--out", default=None, help="write report to this path too")
    ap.add_argument("--probe-store-shapes", action="store_true",
                    help="OPTIONAL: read a tiny head of trades/prices to report "
                         "columns/dtypes ONLY (no features, no metrics).")
    args = ap.parse_args(argv)

    buf = io.StringIO()
    buf.write("NAMED-BINARY PROBE — DATA-CONTRACT INSPECTION (READ-ONLY)\n")
    buf.write(f"artifacts_dir={args.artifacts_dir} repo={args.repo}\n")

    for fn in (
        lambda: inspect_contract(args.artifacts_dir, buf),
        lambda: inspect_resolution_rows(args.artifacts_dir, buf),
        lambda: inspect_conflicts(args.artifacts_dir, buf),
        lambda: inspect_p0(args.artifacts_dir, buf),
        lambda: inspect_store(buf),
        lambda: inspect_semantics(buf),
        lambda: inspect_rank1a(args.repo, buf),
    ):
        try:
            fn()
        except Exception as e:
            buf.write(f"\n[SECTION ERROR] {e}\n{traceback.format_exc()}\n")

    if args.probe_store_shapes:
        _sec("5b. store shapes (tiny head only — columns/dtypes, NO features)", buf)
        try:
            from pm_research.data import store as st
            s = st.Store(args.root) if hasattr(st, "Store") else None
            for name, loader in (("trades", getattr(st, "load_trades", None)),
                                 ("prices", getattr(st, "load_prices", None))):
                if loader is None:
                    continue
                try:
                    # try Store-method first, else module fn; read minimal
                    df = None
                    if s is not None and hasattr(s, f"load_{name}"):
                        df = getattr(s, f"load_{name}")()
                    else:
                        df = loader(args.root)
                    buf.write(f"{name}.columns: {list(df.columns)}\n")
                    buf.write(f"{name}.dtypes: "
                              f"{{{', '.join(f'{c}:{df[c].dtype}' for c in df.columns)}}}\n")
                    del df
                except Exception as e:
                    buf.write(f"{name} shape probe skipped: {e}\n")
        except Exception as e:
            buf.write(f"store shape probe failed: {e}\n")

    report = buf.getvalue()
    print(report)
    if args.out:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"\n[written] {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
