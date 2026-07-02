"""Diagnostic: why is resolution_mapping_success_rate == 0.0?

Read-only. No classification, no gate, no probe. Just inspects the join between
eligible conditions and resolutions, and what winning_outcome actually contains.

Usage:
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\diag_resolution_mapping.py --root C:\\b1\\data
"""

from __future__ import annotations

import argparse
import glob
import os
from collections import Counter

import pyarrow.parquet as pq

from pm_research.semantics import ConditionAccumulator, audit_condition, MAP_OK


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--chunksize", type=int, default=200_000)
    args = ap.parse_args()

    # ---- 1. What does winning_outcome actually contain? ----
    res_path = os.path.join(args.root, "resolutions.parquet")
    rtbl = pq.read_table(res_path)
    rd = rtbl.to_pydict()
    res_cids = set(str(c) for c in rd["condition_id"])
    wo = rd.get("winning_outcome", [])
    wo_counter = Counter(str(x) for x in wo)
    print("=== resolutions.parquet ===")
    print("columns:", rtbl.column_names)
    print("n resolutions:", len(rd["condition_id"]))
    print("distinct winning_outcome values (top 20):")
    for val, n in wo_counter.most_common(20):
        print(f"   {val!r}: {n}")
    print()

    # ---- 2. Build eligible (cleanly-mapped, exactly-two-token) conditions ----
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
                    a = ConditionAccumulator(scid)
                    accs[scid] = a
                a.observe(d["token_id"][i], d["outcome_index"][i], outs[i])

    eligible = {}
    for cid, acc in accs.items():
        m = audit_condition(acc)
        if m.status == MAP_OK:
            eligible[cid] = m
    print("=== eligible (cleanly two-token mapped) ===")
    print("n eligible:", len(eligible))

    # ---- 3. The join: how many eligible have a resolution row at all? ----
    elig_cids = set(eligible.keys())
    in_both = elig_cids & res_cids
    print("eligible WITH a resolution row:", len(in_both))
    print("eligible WITHOUT any resolution row:", len(elig_cids - res_cids))
    print()

    # ---- 4. For those in both, does winning_outcome match a side label/index/token? ----
    raw_by_cid = {str(rd["condition_id"][i]): str(wo[i]) for i in range(len(wo))}
    sample = list(in_both)[:2000]
    label_hit = index_hit = token_hit = none_hit = 0
    examples = []
    for cid in sample:
        m = eligible[cid]
        raw = raw_by_cid.get(cid)
        side_labels = {(_norm(s[2]) if s[2] else "") for s in m.sides}
        side_idx = {str(s[1]) for s in m.sides}
        side_tok = {s[0] for s in m.sides}
        hit = None
        if raw is not None and _norm(raw) in side_labels and _norm(raw) != "":
            label_hit += 1; hit = "label"
        elif raw is not None and raw in side_idx:
            index_hit += 1; hit = "index"
        elif raw is not None and raw in side_tok:
            token_hit += 1; hit = "token"
        else:
            none_hit += 1; hit = "NONE"
        if len(examples) < 12:
            examples.append((cid[:14], raw, [s[2] for s in m.sides], [s[1] for s in m.sides], hit))
    print(f"=== match test on {len(sample)} in-both conditions ===")
    print(f"label_hit={label_hit} index_hit={index_hit} token_hit={token_hit} NONE={none_hit}")
    print("examples (cid, winning_outcome_raw, side_labels, side_indices, hit):")
    for e in examples:
        print("  ", e)


def _norm(s):
    if s is None:
        return ""
    return " ".join(str(s).strip().lower().split())


if __name__ == "__main__":
    main()
