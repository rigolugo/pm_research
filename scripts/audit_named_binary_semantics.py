"""Named-binary semantics audit (orchestration entry point).

Runs the approved build order over the local dataset and writes the contract +
gate + report artifacts. STREAMS trades/prices in chunks; never materializes the
full 16.5M-row dataset.

THE LAYER ENDS AT THE AUDIT GATE. This script runs NO probe, NO PnL, NO wallet
logic. It classifies, maps, orients, resolves, and gates. Nothing further.

Usage (Windows / PowerShell):
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\audit_named_binary_semantics.py --root C:\\b1\\data --out-dir artifacts

Build order:
    1. canonical mapping layer + mapping audit
    2. (lexicon is version-pinned in pm_research/semantics/lexicon.py; the
       label-pair census that feeds it is produced by named_binary_label_census.py)
    3. classification-contract artifacts
    4. resolution-schema audit
    5. canonical_side_price / oriented_price
    6. audit gate
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from typing import Dict, Set

from pm_research.semantics import (
    NB_CONTRACT_VERSION,
    ConditionAccumulator,
    audit_condition,
    audit_token_condition_stability,
    MAP_OK,
    classify_condition,
    build_orientation,
    orientation_is_clean,
    NBSubclass,
    ConditionSides,
    ResolutionRow,
    determine_schema,
    resolve_condition,
    RES_OK,
    GateInput,
    GateThresholds,
    run_audit_gate,
    GATE_CLEAR,
    GATE_CLEAR_WARN,
    GATE_BLOCK_RESOLUTION,
)


def _rss_mb():
    try:
        import psutil
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


class Ticker:
    """Periodic stderr progress line. Writes to stderr so the paste-back JSON on
    stdout stays clean."""

    def __init__(self, every_rows=500_000, label="audit"):
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
        parts = [f"[{self.label}]", f"rows={rows:,}", f"conds={conditions:,}",
                 f"elapsed={elapsed:,.0f}s", f"rate={rate:,.0f}/s"]
        if files_total:
            parts.append(f"files={files_done}/{files_total}")
        if rss is not None:
            parts.append(f"rss={rss:,.0f}MB")
        print(" ".join(parts), file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- #
# Chunked readers. Prefer an existing iterator in store.py; fall back to a
# pyarrow/pandas chunked read. NEVER load all trades at once.
# --------------------------------------------------------------------------- #
def iter_trade_batches(root: str, chunksize: int):
    """Yield (file_index, file_total, column_dict) per record batch.

    Streams the SHARDED per-wallet parquet files under root/trades/*.parquet,
    one file at a time, batch by batch. Batch-level (not row-level) so the caller
    can tick file progress and avoid per-row dict overhead. Memory stays bounded
    regardless of total row count.

    Confirmed schema (Copilot review): trades carry the outcome LABEL on the same
    row as identity: condition_id, token_id, outcome_index, outcome.
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
            yield fi, total, path, batch.to_pydict()


def load_label_hints(root: str) -> Dict:
    """DEPRECATED / unused for label source.

    Confirmed schema (Copilot review): the outcome LABEL is on the trade row
    (``outcome`` column), already anchored to identity. We therefore read labels
    in the streaming pass, not from markets.parquet. Kept as a no-op so any
    external caller/import does not break; returns {}.
    """
    return {}


def load_resolutions(root: str):
    """Read resolutions.parquet into a list of ResolutionRow.

    Local resolutions carry condition_id + winning_outcome (+ resolved_at). Read
    string-safe (no float near identifiers). Returns [] if the file is absent so
    the audit degrades to "no local resolutions" rather than crashing.
    """
    import os as _os
    path = _os.path.join(root, "resolutions.parquet")
    if not _os.path.exists(path):
        return []
    import pyarrow.parquet as pq
    tbl = pq.read_table(path)
    cols = set(tbl.column_names)
    if "condition_id" not in cols:
        raise SystemExit(
            f"resolutions.parquet missing condition_id; have {sorted(cols)}")
    d = tbl.to_pydict()
    n = len(d["condition_id"])
    wo = d.get("winning_outcome", [None] * n)
    rows = []
    for i in range(n):
        cid = d["condition_id"][i]
        if cid is None or str(cid).strip() == "":
            continue
        rows.append(ResolutionRow(
            condition_id=str(cid),
            winning_outcome_raw=wo[i],
        ))
    return rows


def load_resolution_source(path: str) -> Dict[str, Dict[str, object]]:
    """Stage 4: load the normalized Stage 3 resolution-source rows.

    Returns {condition_id: {token_id, outcome_index, label, subclass, status}}
    for rows with status == RESOLVED_SINGLE_WINNER only. All token/condition
    fields are read as strings (the parquet was written string-safe). Raises
    loudly if the file is missing or lacks required columns.
    """
    if not os.path.exists(path):
        raise SystemExit(f"--resolution-source file not found: {path}")
    import pyarrow.parquet as pq
    tbl = pq.read_table(path)
    cols = set(tbl.column_names)
    required = {"condition_id", "resolved_winning_token_id",
                "resolved_winning_outcome_index", "status"}
    missing = required - cols
    if missing:
        raise SystemExit(
            f"--resolution-source missing required columns: {sorted(missing)}; "
            f"have {sorted(cols)}")
    d = tbl.to_pydict()
    n = len(d["condition_id"])
    out: Dict[str, Dict[str, object]] = {}
    for i in range(n):
        if str(d["status"][i]) != "RESOLVED_SINGLE_WINNER":
            continue
        cid = str(d["condition_id"][i])
        try:
            idx = int(d["resolved_winning_outcome_index"][i])
        except (TypeError, ValueError):
            continue
        out[cid] = {
            "token_id": str(d["resolved_winning_token_id"][i]),
            "outcome_index": idx,
            "label": d.get("resolved_winning_label", [None] * n)[i],
            "subclass": d.get("subclass", [None] * n)[i],
        }
    return out


def load_source_conflict_counts(source_rows_path: str) -> Dict[str, Dict[str, int]]:
    """Stage 4: read the Stage 3 conflicts CSV (co-located with the source rows
    parquet) to get per-subclass AMBIGUOUS_MULTIPLE_WINNERS counts.

    The source-rows parquet holds ONLY RESOLVED_SINGLE_WINNER rows, so the
    ambiguous (and other) conflict counts live in
    named_binary_resolution_conflicts.csv. Returns
    {subclass: {status: count}}; empty dict if the file is absent (the breakdown
    then reports ambiguous=0 and attributes the remainder to missing_source_rows,
    which is still correct arithmetic but less granular). This NEVER labels a
    missing source row as an ambiguous conflict.
    """
    import csv as _csv
    conf_path = os.path.join(os.path.dirname(source_rows_path),
                             "named_binary_resolution_conflicts.csv")
    out: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    if not os.path.exists(conf_path):
        return {}
    with open(conf_path, newline="", encoding="utf-8") as f:
        reader = _csv.DictReader(f)
        for row in reader:
            sub = (row.get("subclass") or "").strip()
            status = (row.get("status") or "").strip()
            if sub and status:
                out[sub][status] += 1
    return {s: dict(v) for s, v in out.items()}


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="data path (trades/prices/markets/resolutions)")
    ap.add_argument("--out-dir", default="artifacts")
    ap.add_argument("--chunksize", type=int, default=200_000)
    ap.add_argument("--tick-rows", type=int, default=500_000,
                    help="emit a progress line every N rows (stderr)")
    ap.add_argument("--lexicon-version", default=None,
                    help="if set, assert NB_CONTRACT_VERSION matches; abort on mismatch")
    ap.add_argument("--resolution-source", default=None,
                    help="optional Stage 3 normalized resolution-source parquet "
                         "(named_binary_resolution_source_rows.parquet). When "
                         "supplied, non-YES/NO winners are taken from this source; "
                         "absent => local resolutions.parquet only (default).")
    args = ap.parse_args()

    if args.lexicon_version and args.lexicon_version != NB_CONTRACT_VERSION:
        raise SystemExit(
            f"lexicon version mismatch: expected {args.lexicon_version}, "
            f"loaded {NB_CONTRACT_VERSION}"
        )

    os.makedirs(args.out_dir, exist_ok=True)

    # ---- Step 1: stream trades, accumulate per-condition + global token map ----
    ticker = Ticker(every_rows=args.tick_rows, label="audit")
    accs: Dict[str, ConditionAccumulator] = {}
    token_to_conditions: Dict[str, Set[str]] = defaultdict(set)
    total_rows = 0
    rows_with_token = 0
    rows_with_index = 0
    last_fi = ftot = 0

    for fi, ftot, path, d in iter_trade_batches(args.root, args.chunksize):
        n = len(d["condition_id"])
        cids = d["condition_id"]
        toks = d["token_id"]
        idxs = d["outcome_index"]
        outs = d.get("outcome", [None] * n)
        for i in range(n):
            cid = cids[i]
            if cid is None or str(cid).strip() == "":
                continue
            tok = toks[i]
            # Precision-loss guard (DECISION_LOG asset-id lesson): a 78-digit
            # token must arrive as str/int, never float. A float here means the
            # column was read lossily -> abort loudly rather than match the
            # wrong token.
            if isinstance(tok, float):
                raise TypeError(
                    "token_id read as float (precision loss); read the token_id "
                    f"column as string/object, not float. offending file: {path}"
                )
            idx = idxs[i]
            label = outs[i]
            if label is not None and str(label).strip() == "":
                label = None
            if tok is not None and str(tok).strip() not in {"", "nan"}:
                rows_with_token += 1
                token_to_conditions[str(tok).strip()].add(str(cid))
            if idx is not None:
                rows_with_index += 1
            scid = str(cid)
            acc = accs.get(scid)
            if acc is None:
                acc = ConditionAccumulator(scid)
                accs[scid] = acc
            acc.observe(tok, idx, label)
        total_rows += n
        ticker.maybe(total_rows, len(accs), files_done=fi, files_total=ftot)
        last_fi = fi
    ticker.emit(total_rows, len(accs), files_done=last_fi, files_total=ftot)

    token_id_coverage = (rows_with_token / total_rows) if total_rows else 0.0
    outcome_index_coverage = (rows_with_index / total_rows) if total_rows else 0.0

    # ---- Step 1 (cont): mapping audit ----
    global_token_failures = audit_token_condition_stability(token_to_conditions)
    mappings = {}
    for cid, acc in accs.items():
        m = audit_condition(acc)
        if cid in global_token_failures and m.status == MAP_OK:
            # global token-condition ambiguity overrides a locally-clean mapping
            from pm_research.semantics.mapping_audit import MappingResult, FAIL_TOKEN_CONDITION
            m = MappingResult(cid, FAIL_TOKEN_CONDITION, m.token_ids,
                              failed_check=FAIL_TOKEN_CONDITION)
        mappings[cid] = m

    # ---- Step 3: classification ----
    classification = {cid: classify_condition(m) for cid, m in mappings.items()}
    named_binary_eligible = sum(1 for r in classification.values() if r.nb_eligible)

    # ---- Step 4: resolution-schema audit ----
    sides_by_condition = {
        cid: ConditionSides(cid, m.sides)
        for cid, m in mappings.items() if m.status == MAP_OK
    }
    res_rows = load_resolutions(args.root)
    schema_res = determine_schema(res_rows, sides_by_condition,
                                  min_success=GateThresholds().resolution_success_min)

    # normalize resolutions for eligible conditions under the chosen schema
    res_status: Dict[str, str] = {}
    res_winner: Dict[str, object] = {}
    if schema_res.chosen_schema is not None:
        raw_by_cid = {r.condition_id: r.winning_outcome_raw for r in res_rows}
        for cid, sides in sides_by_condition.items():
            if not classification[cid].nb_eligible:
                continue
            raw = raw_by_cid.get(cid)
            status, side = resolve_condition(schema_res.chosen_schema, raw, sides.sides)
            res_status[cid] = status
            if status == RES_OK and side is not None:
                res_winner[cid] = {"token_id": side[0], "outcome_index": side[1], "label": side[2]}
    eligible_with_sides = [c for c in sides_by_condition if classification[c].nb_eligible]

    # ---- Stage 4: overlay the Stage 3 resolution source (non-YES/NO) ----
    # Default behavior (no --resolution-source) is UNCHANGED: res_status holds only
    # local YES/NO mappings, non-YES/NO stays unresolved, gate stays blocked.
    # When supplied, non-YES/NO winners come from the source; YES/NO local path is
    # preserved exactly (the source carries no YES_NO rows). Conflicts from Stage 3
    # are excluded (not added as RES_OK) and counted.
    source_winner: Dict[str, Dict[str, object]] = {}
    source_conflict_counts: Dict[str, int] = defaultdict(int)
    using_source = bool(args.resolution_source)
    if using_source:
        source_winner = load_resolution_source(args.resolution_source)
        for cid in eligible_with_sides:
            sub = classification[cid].nb_subclass
            if sub == NBSubclass.YES_NO.value:
                continue  # YES/NO stays on the local path; never overridden
            sw = source_winner.get(cid)
            if sw is None:
                continue  # no source winner (uncovered or a Stage 3 conflict)
            # confirm the source winner's token/index agrees with local sides
            sides = sides_by_condition[cid].sides
            ok = any(s[0] == sw["token_id"] and s[1] == sw["outcome_index"]
                     for s in sides)
            if ok:
                res_status[cid] = RES_OK
                res_winner[cid] = {"token_id": sw["token_id"],
                                   "outcome_index": sw["outcome_index"],
                                   "label": sw["label"], "from_source": True}
            else:
                source_conflict_counts["SOURCE_TOKEN_INDEX_MISMATCH"] += 1

    res_success_rate = (
        sum(1 for c in eligible_with_sides if res_status.get(c) == RES_OK)
        / len(eligible_with_sides)
    ) if eligible_with_sides else 0.0

    # Per-subclass resolution mapping rates (Issue-A reporting requirement).
    # For each subclass: eligible count, how many have a resolution row, how many
    # actually map the winner to a side. Makes the YES/NO-resolvable vs
    # non-YES/NO-not-resolvable distinction explicit and machine-readable.
    raw_by_cid_all = {r.condition_id: r.winning_outcome_raw for r in res_rows}
    sub_eligible: Dict[str, int] = defaultdict(int)
    sub_with_res: Dict[str, int] = defaultdict(int)
    sub_mapped: Dict[str, int] = defaultdict(int)
    for cid in eligible_with_sides:
        sub = classification[cid].nb_subclass
        sub_eligible[sub] += 1
        # "with_resolution_row": a local raw row OR a Stage 3 source winner
        if cid in raw_by_cid_all or (using_source and cid in source_winner):
            sub_with_res[sub] += 1
        if res_status.get(cid) == RES_OK:
            sub_mapped[sub] += 1
    per_subclass_resolution = {
        sub: {
            "eligible": sub_eligible[sub],
            "with_resolution_row": sub_with_res[sub],
            "winner_maps_to_side": sub_mapped[sub],
            "map_rate_of_eligible": (sub_mapped[sub] / sub_eligible[sub]) if sub_eligible[sub] else 0.0,
        }
        for sub in sorted(sub_eligible)
    }
    # Resolvability verdict per subclass: resolvable iff any eligible condition's
    # winner maps to a side (via local YES/NO path OR the Stage 3 source overlay).
    resolvable_by_subclass = {sub: (sub_mapped[sub] > 0) for sub in sorted(sub_eligible)}
    non_yesno_resolvable = any(
        v for s, v in resolvable_by_subclass.items() if s != NBSubclass.YES_NO.value
    )
    # Gate policy: non-YES/NO scoreability may come ONLY from the Stage 3 source.
    # Without --resolution-source, non_yesno_resolvable must be False (default
    # blocked behavior). With it, non-YES/NO becomes scoreable from the source.
    non_yesno_scoreable_from_source = bool(using_source and non_yesno_resolvable)
    # keep the old key name for backward-compatible artifact readers
    locally_resolvable = resolvable_by_subclass

    # ---- Step 5: orientation ----
    orientation_clean = 0
    orientation_total = 0
    blocked_reason_counts: Dict[str, int] = defaultdict(int)
    usable_conditions = []
    for cid in eligible_with_sides:
        sub = classification[cid].nb_subclass
        contract = build_orientation(mappings[cid], sub)
        orientation_total += 1
        clean = orientation_is_clean(contract)
        if clean:
            orientation_clean += 1
        else:
            blocked_reason_counts["PRICE_ORIENTATION"] += 1
        # usable = eligible AND resolution OK AND orientation clean
        if res_status.get(cid) == RES_OK and clean:
            usable_conditions.append(cid)
        else:
            if res_status.get(cid) != RES_OK:
                blocked_reason_counts["RESOLUTION_MAPPING"] += 1
    orientation_correctness_rate = (
        orientation_clean / orientation_total) if orientation_total else 0.0

    # count UNUSABLE / mapping exclusions
    for cid, r in classification.items():
        if not r.nb_eligible and r.exclusion_reason:
            blocked_reason_counts[r.exclusion_reason] += 1

    # ---- Step 6: audit gate ----
    gi = GateInput(
        total_conditions=len(accs),
        named_binary_eligible=named_binary_eligible,
        usable_named_binary_conditions=len(usable_conditions),
        token_id_coverage=token_id_coverage,
        outcome_index_coverage=outcome_index_coverage,
        resolution_mapping_success_rate=res_success_rate,
        orientation_correctness_rate=orientation_correctness_rate,
        blocked_reason_counts=dict(blocked_reason_counts),
        resolution_schema_chosen=schema_res.chosen_schema,
    )
    gate = run_audit_gate(gi)

    # ---- Stage 4 gate policy enforcement (explicit invariant) ----
    # The base gate keys on resolution_mapping_success_rate. With the Stage 3
    # source overlay that rate rises because non-YES/NO now maps. We must enforce,
    # explicitly and independently of the rate, that:
    #   (a) YES/NO alone NEVER clears named-binary, and
    #   (b) non-YES/NO scoreability may clear ONLY when it comes from the Stage 3
    #       source (using_source AND non_yesno_resolvable).
    # A CLEAR* state means "outcome source/audit usable" -- it does NOT authorize
    # a probe (named_binary_probe_blocked stays True regardless).
    base_gate_state = gate.gate_state
    gate_state = base_gate_state
    cleared = isinstance(base_gate_state, str) and base_gate_state.startswith("CLEAR")
    if cleared and not non_yesno_scoreable_from_source:
        # The legacy pooled-all gate could only CLEAR via the pooled rate. If it
        # did but non-YES/NO scoreability is not source-backed, force blocked --
        # YES/NO alone must never clear named-binary.
        gate_state = GATE_BLOCK_RESOLUTION
    # gate_policy_note is set AFTER the non-YES/NO branch is computed (below), so it
    # can describe both the legacy pooled-all gate and the branch result without
    # contradiction.

    # ---- Stage 4: explicit non-YES/NO branch gate (orchestrator policy) ----
    # The legacy pooled-ALL gate_state stays honest (we do NOT force it to CLEAR;
    # YES_NO sparsity legitimately holds it at BLOCKED_BY_RESOLUTION_MAPPING).
    # Separately, we compute a non-YES/NO branch result on the Stage 3 source.
    #
    # Threshold policy (orchestrator-specified):
    #   - non-YES/NO POOLED exact-winner rate must be >= 0.99
    #   - EACH non-YES/NO subclass must be >= 0.95
    #   - ambiguous payout rows remain excluded + counted
    #   - if both hold -> non_yesno_gate_state = CLEAR_WITH_WARNINGS
    #   - any subclass < 0.95 -> that subclass marked not scoreable
    # A CLEAR_WITH_WARNINGS here means "non-YES/NO outcome source/audit usable"; it
    # does NOT authorize a probe (named_binary_probe_blocked stays True).
    NONYESNO_POOLED_MIN = 0.99
    NONYESNO_SUBCLASS_MIN = 0.95
    nonyesno_subs = [s for s in sorted(sub_eligible) if s != NBSubclass.YES_NO.value]
    nonyesno_eligible = sum(sub_eligible[s] for s in nonyesno_subs)
    nonyesno_mapped = sum(sub_mapped[s] for s in nonyesno_subs)
    nonyesno_pooled_map_rate = (
        nonyesno_mapped / nonyesno_eligible) if nonyesno_eligible else 0.0

    nonyesno_per_subclass_rate = {
        s: ((sub_mapped[s] / sub_eligible[s]) if sub_eligible[s] else 0.0)
        for s in nonyesno_subs
    }
    # ---- Correct per-subclass breakdown (missing source rows vs ambiguous) ----
    # The previous code labeled (eligible - resolved) entirely as "ambiguous",
    # which wrongly counts conditions that simply had NO source row as ambiguous
    # conflicts. Separate them:
    #   resolved_single_winner = sub_mapped[s]  (winners overlaid this run)
    #   AMBIGUOUS_MULTIPLE_WINNERS = from the Stage 3 conflicts CSV per subclass
    #   source_rows  = resolved_single_winner + ambiguous (+ any other Stage 3
    #                  conflict statuses for this subclass)
    #   missing_source_rows = eligible - source_rows  (no source row at all)
    #   total_not_scoreable = missing_source_rows + ambiguous = eligible - resolved
    src_conflicts = (load_source_conflict_counts(args.resolution_source)
                     if using_source else {})
    nonyesno_breakdown: Dict[str, Dict[str, object]] = {}
    for s in nonyesno_subs:
        eligible_s = sub_eligible[s]
        resolved_s = sub_mapped[s]
        sub_conf = src_conflicts.get(s, {})
        ambiguous_s = int(sub_conf.get("AMBIGUOUS_MULTIPLE_WINNERS", 0))
        other_conf_s = sum(v for k, v in sub_conf.items()
                           if k != "AMBIGUOUS_MULTIPLE_WINNERS")
        source_rows_s = resolved_s + ambiguous_s + other_conf_s
        missing_s = eligible_s - source_rows_s
        if missing_s < 0:
            # defensive: never report negative; clamp and note (would only happen
            # if the conflicts CSV double-counts -- not expected).
            missing_s = 0
            source_rows_s = eligible_s
        total_not_scoreable_s = eligible_s - resolved_s
        exact_winner_rate_s = (resolved_s / source_rows_s) if source_rows_s else 0.0
        scoreable_rate_s = (resolved_s / eligible_s) if eligible_s else 0.0
        nonyesno_breakdown[s] = {
            "eligible": eligible_s,
            "source_rows": source_rows_s,
            "resolved_single_winner": resolved_s,
            "missing_source_rows": missing_s,
            "AMBIGUOUS_MULTIPLE_WINNERS": ambiguous_s,
            "other_source_conflicts": other_conf_s,
            "total_not_scoreable": total_not_scoreable_s,
            "exact_winner_rate": round(exact_winner_rate_s, 5),
            "scoreable_rate": round(scoreable_rate_s, 5),
        }

    nonyesno_scoreable_by_subclass = {
        s: (nonyesno_per_subclass_rate[s] >= NONYESNO_SUBCLASS_MIN)
        for s in nonyesno_subs
    }
    nonyesno_pooled_ok = nonyesno_pooled_map_rate >= NONYESNO_POOLED_MIN
    nonyesno_all_subclasses_ok = all(nonyesno_scoreable_by_subclass.values()) \
        if nonyesno_subs else False
    nonyesno_scoreable = bool(
        using_source and nonyesno_pooled_ok and nonyesno_all_subclasses_ok)
    if nonyesno_scoreable:
        non_yesno_gate_state = GATE_CLEAR_WARN
    else:
        non_yesno_gate_state = GATE_BLOCK_RESOLUTION

    stage4_nonyesno_branch = {
        "non_yesno_gate_state": non_yesno_gate_state,
        "non_yesno_scoreable": nonyesno_scoreable,
        "non_yesno_pooled_map_rate": round(nonyesno_pooled_map_rate, 5),
        "pooled_threshold": NONYESNO_POOLED_MIN,
        "pooled_meets_threshold": bool(nonyesno_pooled_ok),
        "subclass_threshold": NONYESNO_SUBCLASS_MIN,
        "per_subclass_map_rate": {
            s: round(nonyesno_per_subclass_rate[s], 5) for s in nonyesno_subs},
        "per_subclass_scoreable": nonyesno_scoreable_by_subclass,
        # Corrected breakdown: missing_source_rows are NOT ambiguous conflicts.
        "per_subclass_breakdown": nonyesno_breakdown,
        "requires_source": True,
        "using_source": using_source,
        "interpretation": (
            "Non-YES/NO branch evaluated on the Stage 3 source. Pooled exact-winner "
            "rate %.5f (threshold %.2f), each subclass vs %.2f: %s. When pooled>=%.2f "
            "AND every subclass>=%.2f, non_yesno_gate_state=CLEAR_WITH_WARNINGS. "
            "NAMED_OTHER ~0.987 clears the 0.95 subclass floor (NOT 0.99). Per-"
            "subclass total_not_scoreable splits into missing_source_rows (no Stage 3 "
            "row) and AMBIGUOUS_MULTIPLE_WINNERS (split/tie payouts excluded) -- "
            "these are distinct and not conflated. The legacy pooled-ALL gate_state "
            "stays BLOCKED (YES_NO sparsity); this branch is separate. "
            "CLEAR_WITH_WARNINGS does NOT authorize a probe." % (
                nonyesno_pooled_map_rate, NONYESNO_POOLED_MIN, NONYESNO_SUBCLASS_MIN,
                {s: round(nonyesno_per_subclass_rate[s], 4) for s in nonyesno_subs},
                NONYESNO_POOLED_MIN, NONYESNO_SUBCLASS_MIN)
        ),
    }

    # gate_policy_note: describe BOTH the legacy pooled-all gate_state and the
    # non-YES/NO branch result, so the two never appear to contradict.
    gate_policy_note = (
        "Legacy pooled-ALL gate_state=%s (honest; YES_NO local coverage ~%.2f keeps "
        "the pooled rate below floor). Non-YES/NO branch: non_yesno_gate_state=%s, "
        "non_yesno_scoreable=%s (pooled %.5f vs %.2f; each subclass vs %.2f). %s "
        "Clearing the non-YES/NO branch means the outcome source/audit is usable; it "
        "does NOT authorize a named-binary probe (named_binary_probe_blocked=True)."
        % (
            gate_state,
            (sub_mapped.get(NBSubclass.YES_NO.value, 0)
             / sub_eligible[NBSubclass.YES_NO.value])
            if sub_eligible.get(NBSubclass.YES_NO.value) else 0.0,
            non_yesno_gate_state, nonyesno_scoreable,
            nonyesno_pooled_map_rate, NONYESNO_POOLED_MIN, NONYESNO_SUBCLASS_MIN,
            ("All non-YES/NO subclasses scoreable." if nonyesno_scoreable
             else "At least one non-YES/NO subclass not scoreable or pooled<floor.")
        )
    )

    # ---- write artifacts ----
    contract = {
        "nb_contract_version": NB_CONTRACT_VERSION,
        "resolution_schema": schema_res.chosen_schema,
        "conditions": [
            {
                "condition_id": cid,
                "nb_subclass": r.nb_subclass,
                "nb_eligible": r.nb_eligible,
                "nb_contract_version": r.nb_contract_version,
                "exclusion_reason": r.exclusion_reason,
            }
            for cid, r in classification.items()
        ],
    }
    _write_json(os.path.join(args.out_dir, "named_binary_classification_contract.json"), contract)
    _write_text(os.path.join(args.out_dir, "named_binary_classification_contract.md"),
                _contract_md(contract, named_binary_eligible, len(usable_conditions)))

    gate_payload = {
        "gate_state": gate_state,
        "base_gate_state": base_gate_state,
        "gate_policy_note": gate_policy_note,
        "thresholds_version": gate.thresholds_version,
        "total_conditions": gi.total_conditions,
        "named_binary_eligible": gi.named_binary_eligible,
        "usable_named_binary_conditions": gi.usable_named_binary_conditions,
        "token_id_coverage": gi.token_id_coverage,
        "outcome_index_coverage": gi.outcome_index_coverage,
        "resolution_mapping_success_rate": gi.resolution_mapping_success_rate,
        "orientation_correctness_rate": gi.orientation_correctness_rate,
        "blocked_reason_counts": gi.blocked_reason_counts,
        "nb_contract_version": NB_CONTRACT_VERSION,
        "resolution_schema_chosen": schema_res.chosen_schema,
        "convergence_disagreement_rate": schema_res.convergence_disagreement_rate,
        "per_subclass_resolution": per_subclass_resolution,
        "locally_resolvable_by_subclass": locally_resolvable,
        "resolvable_by_subclass": resolvable_by_subclass,
        "non_yesno_named_binary_resolvable": non_yesno_resolvable,
        # ---- Stage 4 fields ----
        "using_resolution_source": using_source,
        "resolution_source_path": args.resolution_source if using_source else None,
        "non_yesno_scoreable_from_source": non_yesno_scoreable_from_source,
        "stage4_nonyesno_branch": stage4_nonyesno_branch,
        "source_winner_count": len(source_winner) if using_source else 0,
        "source_conflict_counts": dict(source_conflict_counts),
        "per_subclass_source_coverage": {
            sub: {
                "eligible": sub_eligible[sub],
                "source_winners": sum(
                    1 for c in eligible_with_sides
                    if classification[c].nb_subclass == sub
                    and using_source and c in source_winner),
            }
            for sub in sorted(sub_eligible)
        } if using_source else {},
        # The probe is ALWAYS blocked here. A CLEAR* gate means the outcome
        # source/audit is usable; it never authorizes a probe.
        "named_binary_probe_blocked": True,
        "resolvability_note": (
            (
                "Non-YES/NO named-binary (UP_DOWN, OVER_UNDER, NAMED_OTHER) is now "
                "scoreable from the Stage 3 resolution source "
                "(named_binary_resolution_source_rows.parquet). YES/NO remains on "
                "the local resolutions path. AMBIGUOUS_MULTIPLE_WINNERS rows are "
                "excluded + counted. Gate is CLEAR* only in the sense that the "
                "outcome source/audit is usable; the named-binary probe remains "
                "BLOCKED and unauthorized -- clearing the gate does NOT authorize "
                "a probe."
            ) if non_yesno_scoreable_from_source else (
                "YES_NO is resolvable against local resolutions.parquet. "
                "Non-YES/NO named-binary (UP_DOWN, OVER_UNDER, NAMED_OTHER) is NOT "
                "resolvable from local resolutions (winning_outcome is YES/NO-only). "
                "Supply --resolution-source (Stage 3 rows) to make non-YES/NO "
                "scoreable. The named-binary probe remains BLOCKED."
            )
        ),
        "detail": gate.detail,
    }
    _write_json(os.path.join(args.out_dir, "named_binary_audit_gate.json"), gate_payload)
    _write_text(os.path.join(args.out_dir, "named_binary_audit_gate.md"), _gate_md(gate_payload))
    _write_text(os.path.join(args.out_dir, "named_binary_semantics_report.md"),
                _report_md(gate_payload, schema_res))

    # per-subclass resolution coverage CSV
    import csv as _csv
    cov_path = os.path.join(args.out_dir, "named_binary_resolution_mapping_coverage.csv")
    with open(cov_path, "w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["nb_subclass", "eligible", "with_resolution_row",
                    "winner_maps_to_side", "map_rate_of_eligible",
                    "locally_resolvable"])
        for sub, d in per_subclass_resolution.items():
            w.writerow([sub, d["eligible"], d["with_resolution_row"],
                        d["winner_maps_to_side"], f"{d['map_rate_of_eligible']:.6f}",
                        locally_resolvable[sub]])

    # ---- paste-back summary to stdout ----
    print(json.dumps({
        "gate_state": gate.gate_state,
        "total_conditions": gi.total_conditions,
        "named_binary_eligible": gi.named_binary_eligible,
        "usable_named_binary_conditions": gi.usable_named_binary_conditions,
        "token_id_coverage": round(gi.token_id_coverage, 5),
        "outcome_index_coverage": round(gi.outcome_index_coverage, 5),
        "resolution_mapping_success_rate": round(gi.resolution_mapping_success_rate, 5),
        "orientation_correctness_rate": round(gi.orientation_correctness_rate, 5),
        "resolution_schema_chosen": schema_res.chosen_schema,
        "per_subclass_map_rate": {
            sub: round(d["map_rate_of_eligible"], 5)
            for sub, d in per_subclass_resolution.items()
        },
        "non_yesno_named_binary_resolvable": non_yesno_resolvable,
        "named_binary_probe_blocked": True,
        "blocked_reason_counts": gi.blocked_reason_counts,
        "nb_contract_version": NB_CONTRACT_VERSION,
    }, indent=2))


def _write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


def _write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _contract_md(contract, eligible, usable):
    lines = [
        "# Named-Binary Classification Contract",
        "",
        f"- `nb_contract_version`: `{contract['nb_contract_version']}`",
        f"- resolution_schema: `{contract['resolution_schema']}`",
        f"- named_binary_eligible: {eligible}",
        f"- usable_named_binary_conditions: {usable}",
        "",
        "Chat2 (Dune wallet discovery) MUST assert `nb_contract_version` equality "
        "against this file and consume the classification verbatim.",
    ]
    return "\n".join(lines) + "\n"


def _gate_md(p):
    lines = [
        "# Named-Binary Audit Gate",
        "",
        f"**gate_state: `{p['gate_state']}`**  (thresholds `{p['thresholds_version']}`)",
        "",
        f"- total_conditions: {p['total_conditions']}",
        f"- named_binary_eligible: {p['named_binary_eligible']}",
        f"- usable_named_binary_conditions: {p['usable_named_binary_conditions']}",
        f"- token_id_coverage: {p['token_id_coverage']:.5f}",
        f"- outcome_index_coverage: {p['outcome_index_coverage']:.5f}",
        f"- resolution_mapping_success_rate: {p['resolution_mapping_success_rate']:.5f}",
        f"- orientation_correctness_rate: {p['orientation_correctness_rate']:.5f}",
        f"- resolution_schema_chosen: `{p['resolution_schema_chosen']}`",
        f"- convergence_disagreement_rate: {p['convergence_disagreement_rate']}",
        f"- nb_contract_version: `{p['nb_contract_version']}`",
        "",
        "## blocked_reason_counts",
    ]
    for k, v in (p["blocked_reason_counts"] or {}).items():
        lines.append(f"- {k}: {v}")

    lines += ["", "## per-subclass resolution mapping",
              "", "| subclass | eligible | with_res_row | winner_maps | map_rate | locally_resolvable |",
              "|---|---|---|---|---|---|"]
    for sub, d in (p.get("per_subclass_resolution") or {}).items():
        lr = p.get("locally_resolvable_by_subclass", {}).get(sub)
        lines.append(
            f"| {sub} | {d['eligible']} | {d['with_resolution_row']} | "
            f"{d['winner_maps_to_side']} | {d['map_rate_of_eligible']:.4f} | {lr} |"
        )

    lines += ["",
              f"**named_binary_probe_blocked: {p.get('named_binary_probe_blocked')}**",
              f"**non_yesno_named_binary_resolvable: {p.get('non_yesno_named_binary_resolvable')}**",
              "",
              p.get("resolvability_note", ""),
              "",
              "NOTE: this is a SEMANTICS/usability gate. No probe runs until this "
              "gate is CLEAR* AND a probe is separately authorized. For non-YES/NO "
              "named-binary, a probe is moot until a realized-outcome source exists."]
    return "\n".join(lines) + "\n"


def _report_md(p, schema_res):
    return (
        "# Named-Binary Semantics Report\n\n"
        f"Gate: **{p['gate_state']}**. "
        f"Usable named-binary conditions: {p['usable_named_binary_conditions']} "
        f"of {p['named_binary_eligible']} eligible "
        f"({p['total_conditions']} total).\n\n"
        f"Resolution schema chosen: `{p['resolution_schema_chosen']}` "
        f"(per-interpretation success: {schema_res.per_interpretation_success}).\n\n"
        "Orientation reads token identity, never display label. "
        "yes_price is defined only for YES_NO; other subclasses carry "
        "side_0/side_1 with no YES-equivalent.\n\n"
        "The layer ends here. No probe, no PnL, no wallet logic was run.\n"
    )


if __name__ == "__main__":
    main()
