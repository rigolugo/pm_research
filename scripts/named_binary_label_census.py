"""Frequency-ranked label-pair census (feeds the version-pinned lexicon).

Build-order step 2 input. Runs AFTER the mapping layer logic exists, because the
label pairs must be anchored to validated identity (condition_id + the two
outcome tokens/indices) before they can be trusted even as classification hints.

Output: artifacts/named_binary_label_pair_census.csv with columns
    label_a, label_b, n_conditions, example_condition_id
sorted by n_conditions descending. A human hand-classifies the head into
pm_research/semantics/lexicon.py and bumps NB_CONTRACT_VERSION; the tail stays
UNUSABLE.

This script does NOT classify and does NOT orient. It only enumerates. It runs
no probe and touches no PnL.

Usage:
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\named_binary_label_census.py --root C:\\b1\\data --out-dir artifacts
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from collections import defaultdict
from typing import Dict, Set, Tuple

from pm_research.semantics import ConditionAccumulator, audit_condition, MAP_OK


def _rss_mb():
    """Resident memory in MB if psutil is available, else None (no hard dep)."""
    try:
        import psutil
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


class Ticker:
    """Periodic stderr progress line: rows, conditions, elapsed, files, RSS.

    Flushes immediately so a stuck/thrashing run is visible in real time. Writes
    to stderr so it never contaminates the artifact/JSON stdout.
    """

    def __init__(self, every_rows=500_000, label="census"):
        self.every = every_rows
        self.label = label
        self.t0 = time.time()
        self.last = 0

    def maybe(self, rows, conditions, files_done=None, files_total=None):
        if rows - self.last < self.every:
            return
        self.last = rows
        self.emit(rows, conditions, files_done, files_total)

    def emit(self, rows, conditions, files_done=None, files_total=None):
        elapsed = time.time() - self.t0
        rate = rows / elapsed if elapsed > 0 else 0
        rss = _rss_mb()
        parts = [
            f"[{self.label}]",
            f"rows={rows:,}",
            f"conds={conditions:,}",
            f"elapsed={elapsed:,.0f}s",
            f"rate={rate:,.0f}/s",
        ]
        if files_total:
            parts.append(f"files={files_done}/{files_total}")
        if rss is not None:
            parts.append(f"rss={rss:,.0f}MB")
        print(" ".join(parts), file=sys.stderr, flush=True)


def iter_trade_batches(root: str, chunksize: int):
    """Yield (file_index, file_total, column_dict) per record batch.

    Batch-level iteration avoids building a dict per row (much faster) and lets
    the caller report file progress. Streams sharded files one at a time.
    """
    import glob
    import pyarrow.parquet as pq
    cols = ["condition_id", "token_id", "outcome_index", "outcome"]
    files = sorted(glob.glob(os.path.join(root, "trades", "*.parquet")))
    if not files:
        raise FileNotFoundError(
            f"no trade shards found at {os.path.join(root, 'trades', '*.parquet')}"
        )
    total = len(files)
    for fi, path in enumerate(files, 1):
        pf = pq.ParquetFile(path)
        avail = set(pf.schema.names)
        use = [c for c in cols if c in avail]
        for batch in pf.iter_batches(batch_size=chunksize, columns=use):
            yield fi, total, batch.to_pydict()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out-dir", default="artifacts")
    ap.add_argument("--chunksize", type=int, default=200_000)
    ap.add_argument("--tick-rows", type=int, default=500_000,
                    help="emit a progress line every N rows (stderr)")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    ticker = Ticker(every_rows=args.tick_rows, label="census")
    accs: Dict[str, ConditionAccumulator] = {}
    total_rows = 0
    last_fi = 0

    for fi, ftot, d in iter_trade_batches(args.root, args.chunksize):
        n = len(d["condition_id"])
        cids = d["condition_id"]
        toks = d["token_id"]
        idxs = d["outcome_index"]
        outs = d.get("outcome", [None] * n)
        for i in range(n):
            cid = cids[i]
            if cid is None or str(cid).strip() == "":
                continue
            label = outs[i]
            if label is not None and str(label).strip() == "":
                label = None
            scid = str(cid)
            acc = accs.get(scid)
            if acc is None:
                acc = ConditionAccumulator(scid)
                accs[scid] = acc
            acc.observe(toks[i], idxs[i], label)
        total_rows += n
        ticker.maybe(total_rows, len(accs), files_done=fi, files_total=ftot)
        last_fi = fi
    ticker.emit(total_rows, len(accs), files_done=last_fi, files_total=ftot)

    # Only census conditions whose identity mapping is clean (exactly two tokens,
    # stable). Labels on unstable conditions are not trustworthy hints.
    pair_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    pair_example: Dict[Tuple[str, str], str] = {}
    for cid, acc in accs.items():
        m = audit_condition(acc)
        if m.status != MAP_OK:
            continue
        labels = sorted((str(s[2]) if s[2] is not None else "") for s in m.sides)
        key = (labels[0], labels[1])
        pair_counts[key] += 1
        pair_example.setdefault(key, cid)

    rows = sorted(pair_counts.items(), key=lambda kv: kv[1], reverse=True)
    out_path = os.path.join(args.out_dir, "named_binary_label_pair_census.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["label_a", "label_b", "n_conditions", "example_condition_id"])
        for (la, lb), n in rows:
            w.writerow([la, lb, n, pair_example[(la, lb)]])

    print(f"wrote {out_path} ({len(rows)} distinct label pairs over "
          f"{sum(pair_counts.values())} cleanly-mapped conditions)")


if __name__ == "__main__":
    main()
