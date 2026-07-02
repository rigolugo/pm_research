"""Stage 3 — bulk named-binary resolution-source artifact builder.

Consumes the Stage 1 Dune CSVs + the Chat1 classification contract + the local
validated sides (derived by streaming trades through the existing mapping layer),
runs the Stage 2 resolution_source logic per eligible condition, and writes the
normalized source rows + conflicts + coverage + audit artifacts.

SCOPE: Stage 3 only. Does NOT modify or run the audit gate (Stage 4), runs no
probe, does no PnL/wallet/log_index/indexer work. Winners derive ONLY from payout
numerators, never prices. Resolution data is never fed back into classification.

Sides note: the slot->token mapping needs per-condition validated sides
(token_id, outcome_index, label). No standalone sides artifact exists, so sides
are rebuilt here by streaming trades through pm_research.semantics.mapping_audit
(the same authoritative path the audit uses). Streaming is chunked; the 16.5M-row
trade set is never materialized. If a condition has no clean sides, its winner
maps to SLOT_TOKEN_MAPPING_MISSING (excluded + counted), never guessed.

Usage:
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\build_named_binary_resolution_source.py ^
        --root C:\\b1\\data ^
        --csv-dir C:\\b1\\csv ^
        --contract artifacts\\named_binary_classification_contract.json ^
        --out-dir artifacts\\named_binary ^
        --resolution-csv nb_res_stage1_coverage.csv

The resolution CSV must carry condition_id + payoutnumerators (+ resolved_at,
contract_address) per resolved condition. The Stage 1 SAMPLE csv has this shape;
for the full build, export a Query-B-shaped query without the LIMIT (still
varchar-cast) to <csv-dir>. Pass its filename via --resolution-csv.
"""

from __future__ import annotations

import argparse
import csv as _csv
import glob
import json
import os
import sys
import time
from collections import defaultdict
from typing import Dict, Optional, Tuple

from pm_research.semantics import (
    ConditionAccumulator, audit_condition, MAP_OK,
    normalize_condition_id, parse_payout_vector, winner_from_payout,
    map_slot_to_token, resolve_one, DataExportPrecisionLoss,
    RESOLVED_SINGLE_WINNER, CONFLICT_STATUSES,
    AMBIGUOUS_ZERO_WINNER, AMBIGUOUS_MULTIPLE_WINNERS, MALFORMED_PAYOUT_VECTOR,
    CONDITION_ID_INVALID, SLOT_TOKEN_MAPPING_MISSING, TOKEN_INDEX_CONFLICT,
    PRECISION_LOSS,
)

SOURCE_TABLE = "polymarket_polygon.ctf_evt_conditionresolution"
_SCI = __import__("re").compile(r"^\s*-?\d+(\.\d+)?[eE][+-]?\d+\s*$")
_PRECISION_FIELDS = ("condition_id", "conditionid", "payoutnumerators",
                     "outcomeslotcount", "token_id", "tokenid", "payout",
                     "outcome_index")


def _scan_precision(row: Dict[str, str], path: str, lineno: int) -> None:
    for k, v in row.items():
        if v is None:
            continue
        kl = k.lower()
        if any(f in kl for f in _PRECISION_FIELDS):
            for piece in str(v).replace("[", " ").replace("]", " ").replace(",", " ").split():
                if _SCI.match(piece):
                    raise DataExportPrecisionLoss(
                        f"scientific notation in {k!r} at {path}:{lineno}: {piece!r}"
                    )


def load_resolution_csv(paths) -> Dict[str, Dict[str, str]]:
    """Read one or more Dune resolution CSVs with dtype=str (csv yields strings).

    ``paths`` may be a single path or a list of paths (for paginated/split
    exports). Fails loudly on scientific notation. Returns
    {normalized_condition_id: row}. Duplicate condition_ids with DIFFERENT payout
    vectors are surfaced separately (conflict detection)."""
    if isinstance(paths, str):
        paths = [paths]
    out: Dict[str, Dict[str, str]] = {}
    dupes: Dict[str, set] = defaultdict(set)
    total_data_rows = 0
    for path in paths:
        with open(path, newline="", encoding="utf-8") as f:
            reader = _csv.DictReader(f)
            for i, row in enumerate(reader, 2):
                total_data_rows += 1
                _scan_precision(row, path, i)
                raw_cid = row.get("condition_id") or row.get("conditionid")
                cid = normalize_condition_id(raw_cid)
                if cid is None:
                    out.setdefault("__INVALID__:" + str(raw_cid), row)
                    continue
                payout = row.get("payoutnumerators", "")
                dupes[cid].add(payout.strip())
                out[cid] = row
    for cid, vset in dupes.items():
        if len(vset) > 1 and cid in out:
            out[cid]["__dup_conflict__"] = "1"
    out["__total_data_rows__"] = {"n": str(total_data_rows)}  # sentinel for guard
    return out


def build_sides(root: str, chunksize: int, only: Optional[set],
                cache_path: Optional[str] = None,
                rebuild: bool = False) -> Dict[str, Tuple]:
    """Stream trades, build validated sides per condition via the mapping layer.

    Returns {condition_id: sides} for conditions whose mapping passed (MAP_OK).
    If ``only`` is provided, accumulate only those condition_ids (memory bound to
    the eligible set). If ``cache_path`` exists and not ``rebuild``, load sides
    from cache instead of re-streaming 16.5M trades (~135s)."""
    if cache_path and os.path.exists(cache_path) and not rebuild:
        try:
            import pyarrow.parquet as pq
            d = pq.read_table(cache_path).to_pydict()
            sides = {}
            for cid, tok0, idx0, lab0, tok1, idx1, lab1 in zip(
                d["condition_id"], d["t0"], d["i0"], d["l0"],
                d["t1"], d["i1"], d["l1"]):
                sides[cid] = ((tok0, int(idx0), lab0), (tok1, int(idx1), lab1))
            print(f"[sides] loaded {len(sides):,} from cache {cache_path}",
                  file=sys.stderr)
            return sides
        except Exception as e:
            print(f"[sides] cache read failed ({e}); rebuilding", file=sys.stderr)

    accs: Dict[str, ConditionAccumulator] = {}
    files = sorted(glob.glob(os.path.join(root, "trades", "*.parquet")))
    if not files:
        raise FileNotFoundError(
            f"no trade shards at {os.path.join(root, 'trades', '*.parquet')}")
    import pyarrow.parquet as pq
    cols = ["condition_id", "token_id", "outcome_index", "outcome"]
    t0 = time.time()
    seen = 0
    for fi, path in enumerate(files, 1):
        pf = pq.ParquetFile(path)
        use = [c for c in cols if c in set(pf.schema.names)]
        for batch in pf.iter_batches(batch_size=chunksize, columns=use):
            d = batch.to_pydict()
            n = len(d["condition_id"])
            outs = d.get("outcome", [None] * n)
            for i in range(n):
                cid = d["condition_id"][i]
                if cid is None or str(cid).strip() == "":
                    continue
                scid = str(cid)
                if only is not None and scid not in only:
                    continue
                tok = d["token_id"][i]
                if isinstance(tok, float):
                    raise TypeError(f"token_id read as float (precision loss): {path}")
                a = accs.get(scid)
                if a is None:
                    a = ConditionAccumulator(scid); accs[scid] = a
                a.observe(tok, d["outcome_index"][i], outs[i])
            seen += n
        if fi % 25 == 0 or fi == len(files):
            print(f"[sides] files={fi}/{len(files)} rows={seen:,} "
                  f"conds={len(accs):,} elapsed={time.time()-t0:,.0f}s",
                  file=sys.stderr, flush=True)
    sides = {}
    for cid, acc in accs.items():
        m = audit_condition(acc)
        if m.status == MAP_OK:
            sides[cid] = m.sides

    if cache_path:
        try:
            import pyarrow as pa, pyarrow.parquet as pq
            rows = [(cid, s[0][0], s[0][1], s[0][2], s[1][0], s[1][1], s[1][2])
                    for cid, s in sides.items() if len(s) == 2]
            tbl = pa.table({
                "condition_id": pa.array([r[0] for r in rows], pa.string()),
                "t0": pa.array([r[1] for r in rows], pa.string()),
                "i0": pa.array([str(r[2]) for r in rows], pa.string()),
                "l0": pa.array([r[3] for r in rows], pa.string()),
                "t1": pa.array([r[4] for r in rows], pa.string()),
                "i1": pa.array([str(r[5]) for r in rows], pa.string()),
                "l1": pa.array([r[6] for r in rows], pa.string()),
            })
            pq.write_table(tbl, cache_path)
            print(f"[sides] cached {len(rows):,} -> {cache_path}", file=sys.stderr)
        except Exception as e:
            print(f"[sides] cache write skipped ({e})", file=sys.stderr)
    return sides


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--csv-dir", required=True)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--out-dir", default=r"artifacts\named_binary")
    ap.add_argument("--resolution-csv", default="nb_res_stage1_coverage.csv",
                    help="filename OR glob under --csv-dir with condition_id + "
                         "payoutnumerators (per-condition rows). Glob/multiple "
                         "files are concatenated (for paginated exports).")
    ap.add_argument("--chunksize", type=int, default=200_000)
    ap.add_argument("--sides-cache", default=None,
                    help="parquet path to cache/reuse the streamed sides "
                         "(default: <out-dir>/_sides_cache.parquet)")
    ap.add_argument("--rebuild-sides", action="store_true",
                    help="force re-stream sides even if the cache exists")
    ap.add_argument("--min-coverage-warn", type=float, default=0.5,
                    help="warn if overall source coverage of eligible is below this")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    # ---- contract: eligible conditions + subclass ----
    with open(args.contract, "r", encoding="utf-8") as f:
        contract = json.load(f)
    nb_version = contract.get("nb_contract_version")
    subclass_by_cid: Dict[str, str] = {}
    for r in contract.get("conditions", []):
        if r.get("nb_eligible"):
            subclass_by_cid[str(r["condition_id"])] = r["nb_subclass"]
    eligible = set(subclass_by_cid)
    print(f"eligible conditions: {len(eligible):,}", file=sys.stderr)

    # ---- resolution rows (Dune CSV; supports glob / multiple files) ----
    pattern = os.path.join(args.csv_dir, args.resolution_csv)
    res_files = sorted(glob.glob(pattern))
    if not res_files:
        # not a glob: treat as a literal filename
        literal = os.path.join(args.csv_dir, args.resolution_csv)
        if os.path.exists(literal):
            res_files = [literal]
    if not res_files:
        raise SystemExit(f"resolution CSV not found: {pattern}")
    res_by_cid = load_resolution_csv(res_files)
    total_data_rows = int(res_by_cid.pop("__total_data_rows__", {"n": "0"})["n"])
    n_res = sum(1 for k in res_by_cid if not k.startswith("__INVALID__"))
    print(f"resolution files: {len(res_files)} | data rows read: {total_data_rows:,} "
          f"| distinct conditions: {n_res:,}", file=sys.stderr)

    # ---- TRUNCATION GUARD: a suspiciously round cap or far-short row count ----
    _ROUND_CAPS = {1000, 5000, 10000, 20000, 25000, 32000, 50000}
    if total_data_rows in _ROUND_CAPS:
        print(f"WARNING: resolution rows = {total_data_rows:,}, a common Dune API "
              f"page cap. The export is likely TRUNCATED. Paginate "
              f"(limit+offset) or split by subclass and re-fetch, then concatenate "
              f"(this builder accepts a glob via --resolution-csv).",
              file=sys.stderr)
    # coverage sanity vs eligible (Stage 1 established ~40k non-YES/NO source rows)
    if eligible and n_res < 0.05 * len(eligible):
        print(f"WARNING: only {n_res:,} resolution conditions vs {len(eligible):,} "
              f"eligible (<5%). Likely wrong CSV (aggregate not per-condition) or "
              f"truncated export.", file=sys.stderr)

    # ---- sides (stream trades for the eligible set only; cached) ----
    cache_path = args.sides_cache or os.path.join(args.out_dir, "_sides_cache.parquet")
    sides_by_cid = build_sides(args.root, args.chunksize, only=eligible,
                               cache_path=cache_path, rebuild=args.rebuild_sides)
    print(f"validated sides: {len(sides_by_cid):,}", file=sys.stderr)

    # ---- resolve each eligible condition ----
    resolved_rows = []
    conflict_rows = []
    per_sub = defaultdict(lambda: defaultdict(int))   # subclass -> status -> count
    per_sub_eligible = defaultdict(int)
    per_sub_source = defaultdict(int)

    for cid, sub in subclass_by_cid.items():
        per_sub_eligible[sub] += 1
        row = res_by_cid.get(cid)
        if row is None:
            # no resolution row at all -> not a conflict, just uncovered
            continue
        per_sub_source[sub] += 1
        # duplicate-different-payout conflict takes precedence
        if row.get("__dup_conflict__") == "1":
            status = TOKEN_INDEX_CONFLICT  # represented as a hard conflict
            per_sub[sub]["DUPLICATE_DIFFERENT_PAYOUT"] += 1
            conflict_rows.append((cid, sub, "DUPLICATE_DIFFERENT_PAYOUT",
                                  row.get("payoutnumerators", "")))
            continue
        sides = sides_by_cid.get(cid)
        rr = resolve_one(cid, row.get("payoutnumerators", ""), sides if sides else ())
        per_sub[sub][rr.status] += 1
        if rr.status == RESOLVED_SINGLE_WINNER:
            resolved_rows.append({
                "condition_id": cid,
                "subclass": sub,
                "resolved_winning_token_id": rr.resolved_winning_token_id,
                "resolved_winning_outcome_index": rr.resolved_winning_outcome_index,
                "resolved_winning_label": rr.resolved_winning_label,
                "resolved_at": row.get("resolved_at", ""),
                "source_table": SOURCE_TABLE,
                "status": rr.status,
                "nb_contract_version": nb_version,
            })
        else:
            conflict_rows.append((cid, sub, rr.status,
                                  row.get("payoutnumerators", "")))

    # ---- write artifacts ----
    _write_rows_parquet(os.path.join(args.out_dir,
                        "named_binary_resolution_source_rows.parquet"), resolved_rows)
    _write_conflicts(os.path.join(args.out_dir,
                     "named_binary_resolution_conflicts.csv"), conflict_rows)
    coverage = _write_coverage(os.path.join(args.out_dir,
                     "named_binary_resolution_mapping_coverage.csv"),
                     per_sub_eligible, per_sub_source, per_sub)
    _write_audit(args.out_dir, nb_version, len(resolved_rows), len(conflict_rows),
                 coverage, res_files)

    # ---- stdout summary ----
    print(json.dumps({
        "nb_contract_version": nb_version,
        "resolved_single_winner_rows": len(resolved_rows),
        "conflict_rows": len(conflict_rows),
        "coverage": coverage,
    }, indent=2, default=str))


def _write_rows_parquet(path, rows):
    try:
        import pyarrow as pa, pyarrow.parquet as pq
        if not rows:
            # write an empty table with the stable schema
            cols = ["condition_id", "subclass", "resolved_winning_token_id",
                    "resolved_winning_outcome_index", "resolved_winning_label",
                    "resolved_at", "source_table", "status", "nb_contract_version"]
            tbl = pa.table({c: pa.array([], type=pa.string()) for c in cols})
        else:
            keys = list(rows[0].keys())
            tbl = pa.table({k: pa.array([str(r[k]) if r[k] is not None else None
                                         for r in rows], type=pa.string())
                            for k in keys})
        pq.write_table(tbl, path)
    except ImportError:
        # fallback: csv next to it if pyarrow unavailable
        with open(path.replace(".parquet", ".csv"), "w", newline="", encoding="utf-8") as f:
            if rows:
                w = _csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
                w.writerows(rows)


def _write_conflicts(path, conflict_rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["condition_id", "subclass", "status", "payoutnumerators"])
        w.writerows(conflict_rows)


def _write_coverage(path, elig, source, per_sub):
    coverage = {}
    conflict_types = [AMBIGUOUS_ZERO_WINNER, AMBIGUOUS_MULTIPLE_WINNERS,
                      MALFORMED_PAYOUT_VECTOR, CONDITION_ID_INVALID,
                      SLOT_TOKEN_MAPPING_MISSING, TOKEN_INDEX_CONFLICT,
                      PRECISION_LOSS, "DUPLICATE_DIFFERENT_PAYOUT"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["subclass", "eligible", "source_rows", "resolved_single_winner"]
                   + conflict_types + ["exact_winner_rate", "coverage_rate"])
        for sub in sorted(elig):
            e = elig[sub]; s = source[sub]
            rsw = per_sub[sub].get(RESOLVED_SINGLE_WINNER, 0)
            confs = [per_sub[sub].get(ct, 0) for ct in conflict_types]
            exact = (rsw / s) if s else 0.0
            cov = (s / e) if e else 0.0
            w.writerow([sub, e, s, rsw] + confs + [f"{exact:.6f}", f"{cov:.6f}"])
            coverage[sub] = {"eligible": e, "source_rows": s,
                             "resolved_single_winner": rsw,
                             "exact_winner_rate": round(exact, 6),
                             "coverage_rate": round(cov, 6),
                             "conflicts": {ct: per_sub[sub].get(ct, 0)
                                           for ct in conflict_types if per_sub[sub].get(ct, 0)}}
    return coverage


def _write_audit(out_dir, nb_version, n_rows, n_conf, coverage, res_files):
    payload = {
        "stage": 3,
        "nb_contract_version": nb_version,
        "source_table": SOURCE_TABLE,
        "resolution_csv": [os.path.basename(p) for p in (
            res_files if isinstance(res_files, (list, tuple)) else [res_files])],
        "resolved_single_winner_rows": n_rows,
        "conflict_rows": n_conf,
        "per_subclass": coverage,
        "notes": [
            "Winners derive ONLY from payout numerators, never prices.",
            "Conflicts are excluded + counted, never silently passed.",
            "No audit-gate integration (Stage 4), no probe.",
        ],
    }
    with open(os.path.join(out_dir, "named_binary_resolutions_source_audit.json"),
              "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    lines = ["# Named-Binary Resolution Source Audit (Stage 3)", "",
             f"- nb_contract_version: `{nb_version}`",
             f"- source: `{SOURCE_TABLE}`",
             f"- resolved_single_winner rows: {n_rows}",
             f"- conflict rows: {n_conf}", "",
             "## per-subclass", "",
             "| subclass | eligible | source_rows | resolved | exact_winner_rate | coverage_rate |",
             "|---|---|---|---|---|---|"]
    for sub, c in coverage.items():
        lines.append(f"| {sub} | {c['eligible']} | {c['source_rows']} | "
                     f"{c['resolved_single_winner']} | {c['exact_winner_rate']} | "
                     f"{c['coverage_rate']} |")
    lines += ["", "Winners derive only from payout numerators (never prices). "
              "Conflicts excluded + counted. No gate integration, no probe."]
    with open(os.path.join(out_dir, "named_binary_resolutions_source_audit.md"),
              "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
