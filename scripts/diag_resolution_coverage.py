"""Diagnostic 2: are non-YES/NO eligible conditions UNRESOLVED-yet or
STRUCTURALLY ABSENT from the resolutions schema?

This decides whether the named-binary branch is blocked by (a) markets that
simply haven't resolved yet [time will fix] or (b) a resolutions feed that only
records YES/NO outcomes [structural; named-binary cannot be tested against it].

Read-only. No gate, no probe.

Usage:
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\diag_resolution_coverage.py --root C:\\b1\\data
"""

from __future__ import annotations

import argparse
import glob
import os
from collections import Counter

import pyarrow.parquet as pq

from pm_research.semantics import ConditionAccumulator, audit_condition, MAP_OK
from pm_research.semantics import classify_condition


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--chunksize", type=int, default=200_000)
    args = ap.parse_args()

    # resolutions: condition -> resolved_at present?
    rd = pq.read_table(os.path.join(args.root, "resolutions.parquet")).to_pydict()
    res_cids = set(str(c) for c in rd["condition_id"])
    resolved_at = rd.get("resolved_at", [None] * len(rd["condition_id"]))
    res_has_date = {
        str(rd["condition_id"][i]) for i in range(len(rd["condition_id"]))
        if resolved_at[i] is not None
    }

    # build eligible + subclass
    files = sorted(glob.glob(os.path.join(args.root, "trades", "*.parquet")))
    cols = ["condition_id", "token_id", "outcome_index", "outcome"]
    accs = {}
    for path in files:
        pf = pq.ParquetFile(path)
        use = [c for c in cols if c in set(pf.schema.names)]
        for batch in pf.iter_batches(batch_size=args.chunksize, columns=use):
            d = batch.to_pydict()
            n = len(d["condition_id"])
            outs = d.get("outcome", [None] * n)
            for i in range(n):
                cid = d["condition_id"][i]
                if cid is None or str(cid).strip() == "":
                    continue
                scid = str(cid)
                a = accs.get(scid)
                if a is None:
                    a = ConditionAccumulator(scid); accs[scid] = a
                a.observe(d["token_id"][i], d["outcome_index"][i], outs[i])

    # subclass breakdown of eligible, split by whether a resolution row exists
    by_subclass_total = Counter()
    by_subclass_with_res = Counter()
    for cid, acc in accs.items():
        m = audit_condition(acc)
        if m.status != MAP_OK:
            continue
        row = classify_condition(m)
        if not row.nb_eligible:
            continue
        sub = row.nb_subclass
        by_subclass_total[sub] += 1
        if cid in res_cids:
            by_subclass_with_res[sub] += 1

    print("=== eligible conditions by subclass: with-resolution / total ===")
    for sub in sorted(by_subclass_total):
        tot = by_subclass_total[sub]
        wr = by_subclass_with_res[sub]
        pct = (100.0 * wr / tot) if tot else 0.0
        print(f"   {sub:14s}  {wr:6d} / {tot:6d}  ({pct:5.1f}% have a resolution row)")

    print()
    print("Interpretation:")
    print("  If YES_NO has a high % and the named subclasses are ~0%, the")
    print("  resolutions feed is YES/NO-only (STRUCTURAL). Named-binary cannot be")
    print("  tested against realized outcomes from this file.")
    print("  If named subclasses also have substantial coverage, the earlier 0%")
    print("  was purely the schema-threshold bug and named-binary IS testable.")


if __name__ == "__main__":
    main()
