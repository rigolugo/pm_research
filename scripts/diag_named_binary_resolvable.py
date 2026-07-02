"""Diagnostic 3: of NON-YES/NO eligible conditions that HAVE a resolution row,
how many actually map the winner to one of the two sides?

This is the linchpin for whether ANY named-binary market is testable against
realized outcomes in this resolutions file. The earlier sample showed team
markets with a resolution row resolving to 'NO' (which matches neither team) —
this counts that exactly across the whole non-YES/NO eligible set.

Read-only. No gate, no probe.

Usage:
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\diag_named_binary_resolvable.py --root C:\\b1\\data
"""

from __future__ import annotations

import argparse
import glob
import os
from collections import Counter

import pyarrow.parquet as pq

from pm_research.semantics import (
    ConditionAccumulator, audit_condition, MAP_OK, classify_condition,
)


def _norm(s):
    return " ".join(str(s).strip().lower().split()) if s is not None else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--chunksize", type=int, default=200_000)
    args = ap.parse_args()

    rd = pq.read_table(os.path.join(args.root, "resolutions.parquet")).to_pydict()
    wo_by_cid = {str(rd["condition_id"][i]): rd["winning_outcome"][i]
                 for i in range(len(rd["condition_id"]))}

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

    # For each subclass: of those WITH a resolution row, how many map to a side?
    has_res = Counter()
    maps_to_side = Counter()
    winner_values_when_unmapped = Counter()
    for cid, acc in accs.items():
        m = audit_condition(acc)
        if m.status != MAP_OK:
            continue
        row = classify_condition(m)
        if not row.nb_eligible:
            continue
        if cid not in wo_by_cid:
            continue
        sub = row.nb_subclass
        has_res[sub] += 1
        raw = wo_by_cid[cid]
        side_labels = {_norm(s[2]) for s in m.sides if s[2]}
        if _norm(raw) in side_labels and _norm(raw) != "":
            maps_to_side[sub] += 1
        else:
            winner_values_when_unmapped[(sub, str(raw))] += 1

    print("=== of eligible-WITH-resolution, how many map winner -> a side ===")
    for sub in sorted(has_res):
        hr = has_res[sub]
        mp = maps_to_side[sub]
        print(f"   {sub:14s}  maps {mp:6d} / {hr:6d} with-resolution")

    print()
    print("=== winner value distribution WHEN it fails to map (top 15) ===")
    for (sub, val), n in winner_values_when_unmapped.most_common(15):
        print(f"   {sub:14s}  winner={val!r:8}  x{n}")


if __name__ == "__main__":
    main()
