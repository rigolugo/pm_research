#!/usr/bin/env python
"""S0 PRICE-INPUT INSPECTION (READ-ONLY).

Question: can the local `prices` artifact support non-YES/NO canonical-side price
assembly for the named-binary probe? `OrientationContract.canonical_side_price`
needs TWO per-side prices in outcome_index order; local `load_prices()` returns
only [condition_id, ts, yes_price] (one scalar). This script establishes, FROM
SOURCE AND DATA (never from assumption), what `yes_price` means and whether
per-side prices exist anywhere locally.

STRICTLY READ-ONLY. Reads code text + a tiny data sample; writes only the --out
report. No artifact/gate/test/script modification, no scoring, no features, no
canonical price computed, no probe. Does NOT flip named_binary_probe_blocked.

CRITICAL DISCIPLINE: this script does NOT decide that yes_price == side_0 or that
side_1 == 1 - yes_price. It only surfaces the evidence (price-build source, value
ranges, per-condition row multiplicity) so a human/orchestrator can decide from
proof. It explicitly refuses to infer complementarity.

Usage (PowerShell, env pmresearch):
  $env:PYTHONPATH="C:\\b1\\pm_research"
  cd C:\\b1\\pm_research
  python scripts\\inspect_price_input_s0.py `
      --root C:\\b1\\data --artifacts-dir artifacts --repo . `
      --out artifacts\\named_binary_probe\\price_input_s0_inspection.txt

Paste the produced .txt back into the chat.
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
import traceback


def _sec(title, buf):
    buf.write("\n" + "=" * 78 + "\n")
    buf.write(f"## {title}\n")
    buf.write("=" * 78 + "\n")


def _short(v, n=28):
    s = str(v)
    return s if len(s) <= n else s[:16] + "..." + s[-8:]


# ---------------------------------------------------------------------------
# Q1: where are prices generated? Scan repo for writers of the prices parquet.
# ---------------------------------------------------------------------------

def q1_price_provenance(repo, buf):
    _sec("Q1. price-artifact provenance (who writes `prices`)", buf)
    # Signals that a file writes/produces the prices table.
    writer_pats = [
        r"save_prices", r"PRICES_COLS", r"yes_price", r"to_parquet\(",
        r"prices\.parquet", r"\bprices\b.*parquet", r"def .*price",
        r"build.*price", r"backfill.*price", r"ingest.*price",
    ]
    rx = re.compile("|".join(writer_pats))
    hits = {}
    for base, _dirs, files in os.walk(repo):
        if any(skip in base for skip in (".git", "site-packages", "__pycache__")):
            continue
        for f in files:
            if not f.endswith(".py"):
                continue
            fp = os.path.join(base, f)
            try:
                txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            rel = os.path.relpath(fp, repo)
            for i, line in enumerate(txt.splitlines(), 1):
                if rx.search(line):
                    hits.setdefault(rel, []).append((i, line.strip()[:150]))
    if not hits:
        buf.write("NO price-writer / yes_price references found in repo .py files.\n")
        buf.write("=> price provenance is NOT in the repo; it may be an external "
                  "backfill/ingest. Cannot establish yes_price meaning from code.\n")
        return
    # Prioritize files that both mention save_prices/PRICES_COLS and yes_price.
    buf.write("files referencing price writing / yes_price (rel path -> hits):\n")
    for rel in sorted(hits):
        lines = hits[rel]
        strong = any("save_prices" in t or "PRICES_COLS" in t for _, t in lines)
        buf.write(f"\n--- {rel}{'  [STRONG: writes prices]' if strong else ''}\n")
        for i, t in lines[:40]:
            buf.write(f"  {i}: {t}\n")
    buf.write("\nNEXT: open the STRONG files and read the function that builds the "
              "yes_price column; that source is the ONLY authority on what "
              "yes_price means for non-YES/NO conditions.\n")


# ---------------------------------------------------------------------------
# Q1b: dump store.py price-related source verbatim (load_prices / save_prices).
# ---------------------------------------------------------------------------

def q1b_store_source(buf):
    _sec("Q1b. pm_research/data/store.py price methods (verbatim)", buf)
    try:
        from pm_research.data import store as st
    except Exception as e:
        buf.write(f"IMPORT FAILED: {e}\n{traceback.format_exc()}\n")
        return
    import inspect as _insp
    path = getattr(st, "__file__", None)
    buf.write(f"file: {path}\n")
    for name in ("load_prices", "save_prices", "has_prices", "coverage_ok"):
        obj = getattr(getattr(st, "Store", object), name, None)
        if obj is None:
            buf.write(f"[{name}] not found on Store\n")
            continue
        try:
            buf.write(f"\n----- Store.{name} -----\n")
            buf.write(_insp.getsource(obj) + "\n")
        except (OSError, TypeError) as e:
            buf.write(f"[{name}] source unavailable: {e}\n")
    # schema constant
    try:
        from pm_research.data import schemas as sch
        if hasattr(sch, "PRICES_COLS"):
            buf.write(f"schemas.PRICES_COLS: {sch.PRICES_COLS}\n")
    except Exception as e:
        buf.write(f"schemas note: {e}\n")


# ---------------------------------------------------------------------------
# Q3: any local artifact with per-token / per-side prices?
# ---------------------------------------------------------------------------

def q3_per_side_artifacts(root, artifacts_dir, buf):
    _sec("Q3. search local data/artifacts for per-token / per-side price columns", buf)
    try:
        import pandas as pd
    except ImportError as e:
        buf.write(f"pandas unavailable: {e}\n")
        return
    side_signal_cols = {"token_id", "outcome_index", "side_0_price", "side_1_price",
                        "side_price", "token_price", "price_0", "price_1",
                        "outcome", "asset_id"}
    roots = [p for p in {root, artifacts_dir,
                         os.path.join(artifacts_dir, "named_binary")} if p]
    seen = 0
    for r in roots:
        if not r or not os.path.isdir(r):
            continue
        for base, _dirs, files in os.walk(r):
            for f in files:
                if not (f.endswith(".parquet") or f.endswith(".csv")):
                    continue
                fp = os.path.join(base, f)
                seen += 1
                try:
                    if f.endswith(".parquet"):
                        cols = list(pd.read_parquet(fp).head(0).columns)
                    else:
                        cols = list(pd.read_csv(fp, nrows=0).columns)
                except Exception as e:
                    buf.write(f"  [{os.path.relpath(fp, r)}] unreadable: {e}\n")
                    continue
                overlap = side_signal_cols.intersection(set(cols))
                has_price = any("price" in c.lower() for c in cols)
                if has_price or overlap:
                    buf.write(f"  {os.path.relpath(fp, r)}: cols={cols}"
                              f"{'  <-- per-side/token signal: ' + str(sorted(overlap)) if overlap else ''}\n")
    if seen == 0:
        buf.write("no parquet/csv found under provided roots.\n")
    buf.write("\nNOTE: presence of token_id/outcome_index on a PRICE-bearing table "
              "would be the only local way to get per-side prices. A trades table "
              "having token_id is NOT a price series.\n")


# ---------------------------------------------------------------------------
# Q2 evidence: sample non-YES/NO prices (values + row multiplicity). NO decision.
# ---------------------------------------------------------------------------

def q2_price_sample(root, artifacts_dir, buf, n_conditions=8):
    _sec("Q2. evidence sample: yes_price for non-YES/NO conditions "
         "(values + per-condition multiplicity ONLY — no complementarity inferred)",
         buf)
    try:
        import pandas as pd
        from pm_research.data.store import Store
    except Exception as e:
        buf.write(f"import failed: {e}\n")
        return

    # pick non-YES/NO condition_ids from the resolution-source parquet
    res_path = os.path.join(artifacts_dir, "named_binary",
                            "named_binary_resolution_source_rows.parquet")
    if not os.path.exists(res_path):
        buf.write(f"resolution rows missing: {res_path}\n")
        return
    res = pd.read_parquet(res_path)
    res = res[res["subclass"].isin(["UP_DOWN", "OVER_UNDER", "NAMED_OTHER"])]
    sample_cids = list(res["condition_id"].astype(str).head(n_conditions))
    buf.write(f"sample non-YES/NO condition_ids ({len(sample_cids)}): "
              f"{[_short(c) for c in sample_cids]}\n")

    try:
        prices = Store(root).load_prices()
    except Exception as e:
        buf.write(f"load_prices failed: {e}\n")
        return
    buf.write(f"prices columns: {list(prices.columns)}\n")
    buf.write(f"prices dtypes: "
              f"{{{', '.join(f'{c}:{prices[c].dtype}' for c in prices.columns)}}}\n")

    sub = prices[prices["condition_id"].astype(str).isin(sample_cids)]
    buf.write(f"price rows for sample conditions: {len(sub)}\n")
    if "yes_price" in sub.columns and len(sub):
        yp = pd.to_numeric(sub["yes_price"], errors="coerce")
        buf.write(f"yes_price range over sample: min={yp.min()} max={yp.max()} "
                  f"mean={round(float(yp.mean()), 4) if len(yp) else 'na'}\n")
        buf.write("(range within [0,1] is consistent with a probability but does "
                  "NOT prove which side it is — do not infer.)\n")
    # KEY STRUCTURAL EVIDENCE: how many distinct price series per condition?
    if len(sub):
        per_cond = sub.groupby("condition_id").size()
        buf.write(f"rows per sampled condition: min={per_cond.min()} "
                  f"max={per_cond.max()} (this is a TIME series count, not sides)\n")
        # Is there ANY column that distinguishes two sides within one condition?
        extra = [c for c in sub.columns if c not in ("condition_id", "ts", "yes_price")]
        buf.write(f"columns beyond [condition_id, ts, yes_price]: {extra}\n")
        if not extra:
            buf.write("=> NO per-side discriminator column present. A single "
                      "yes_price time series per condition; the OTHER side's price "
                      "is NOT stored and must NOT be reconstructed as 1-yes_price "
                      "without price-build proof of complementarity.\n")
    buf.write("\nSHOWING first few sample rows (values shortened):\n")
    for _, r in sub.head(6).iterrows():
        buf.write("  " + ", ".join(f"{c}={_short(r[c])}" for c in sub.columns) + "\n")


# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="S0 read-only price-input inspection.")
    ap.add_argument("--root", default="C:\\b1\\data")
    ap.add_argument("--artifacts-dir", default="artifacts")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    buf = io.StringIO()
    buf.write("S0 PRICE-INPUT INSPECTION (READ-ONLY)\n")
    buf.write(f"root={args.root} artifacts_dir={args.artifacts_dir} repo={args.repo}\n")
    buf.write("Discipline: this script surfaces evidence only. It does NOT infer "
              "side_1 = 1 - yes_price and does NOT decide which side yes_price is.\n")

    for fn in (
        lambda: q1_price_provenance(args.repo, buf),
        lambda: q1b_store_source(buf),
        lambda: q3_per_side_artifacts(args.root, args.artifacts_dir, buf),
        lambda: q2_price_sample(args.root, args.artifacts_dir, buf),
    ):
        try:
            fn()
        except Exception as e:
            buf.write(f"\n[SECTION ERROR] {e}\n{traceback.format_exc()}\n")

    _sec("SUMMARY TEMPLATE (fill from evidence above — do not guess)", buf)
    buf.write(
        "Q1 price source path: <STRONG file(s) that write yes_price>\n"
        "Q2 meaning of yes_price for non-YES/NO: <ONLY if the price-build code "
        "states it; else UNKNOWN>\n"
        "Q3 per-side/per-token price artifact exists?: <yes+path / no>\n"
        "Q4 can canonical_side_price be fed correctly?: <yes / no>\n"
        "Q5 verdict: <P1 can proceed / P1 remains BLOCKED on price input>\n"
    )

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
