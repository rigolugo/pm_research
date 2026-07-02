#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stage P1 — Named-Binary Offline Probe: decision-timestamp + feature assembly.

SCOPE (SPEC_named_binary_probe.md §11 Stage P1 — explicitly authorized):
    Build the ex-ante feature-assembly table for the NON-YES/NO named-binary
    universe (UP_DOWN, OVER_UNDER, NAMED_OTHER): the `first_price_after_warmup`
    decision timestamp and the canonical_side_price at that timestamp, one row
    per eligible condition. NO scoring.

HARD BOUNDARIES (§12 non-authorization list). This script does NOT:
    - score anything: no Brier / Brier skill / log-loss / calibration /
      reliability / edge / ROI / PnL / fees / sizing / execution            [P2+]
    - fit any calibrator / isotonic map / run rolling splits / emit a verdict [P2/P3]
    - do wallet discovery / OrdersMatched features / log_index / Dune live queries
    - paper trade / live trade
    - modify the audit gate, or flip `named_binary_probe_blocked`
    - define named-binary or orientation independently of the pinned contract

It CONSUMES (never re-implements):
    - artifacts/named_binary_probe/p0_preflight.json     (P0 verification, read-only)
    - named_binary_classification_contract.json          (eligibility + subclass)
    - named_binary_resolution_source_rows.parquet        (held-aside target only)
    - named_binary_audit_gate.json                       (read-only precondition)
    - pm_research/semantics/named_binary.py              (orientation 1.0)
    - pm_research/data/store.py load_trades / load_prices (ex-ante inputs)

Environment: Windows / Miniconda `pmresearch`.
    $env:PYTHONPATH="C:\\b1\\pm_research"
    python scripts\\named_binary_probe_p1_features.py --root C:\\b1\\data --artifacts-dir artifacts
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import sys
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Iterable, Optional

# ---------------------------------------------------------------------------
# Pinned constants
# ---------------------------------------------------------------------------
NB_CONTRACT_VERSION = "nb-contract-2026-06-28.1"
REQUIRED_GATE_STATE = "CLEAR_WITH_WARNINGS"
SUBCLASSES = ("UP_DOWN", "OVER_UNDER", "NAMED_OTHER")  # YES_NO excluded by design
YES_NO = "YES_NO"
DEFAULT_WARMUP_SECONDS = 3600  # 1h, mirrors Rank 1A first_price_after_warmup

STAGE = "P1_FEATURE_ASSEMBLY"
AUTHORIZED_SCOPE = "P1_FEATURE_ASSEMBLY_ONLY"
PROBE_EXECUTION_AUTHORIZED = False
SCORING_AUTHORIZED = False

# Valid p1_state enum (spec §9)
P1_CLEAR = "P1_CLEAR"
STOP_P0_NOT_CLEAR = "STOP_P0_NOT_CLEAR"
STOP_STALE_CONTRACT = "STOP_STALE_CONTRACT"
STOP_DATA_GATE_NOT_CLEAR = "STOP_DATA_GATE_NOT_CLEAR"
STOP_PRECISION_LOSS = "STOP_PRECISION_LOSS"
STOP_LEAKAGE_GUARD = "STOP_LEAKAGE_GUARD"
STOP_NO_FEATURE_ROWS = "STOP_NO_FEATURE_ROWS"
STOP_MISSING_OUTCOME_SOURCE = "STOP_MISSING_OUTCOME_SOURCE"


class ProbeStop(Exception):
    """Typed hard halt carrying a machine-readable p1_state code."""

    def __init__(self, code: str, detail: str = ""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------
# Precision discipline (string-safe; fail loud on scientific notation).
# ---------------------------------------------------------------------------
class DataExportPrecisionLoss(Exception):
    pass


def canonical_int(value: Any) -> str:
    """Normalize an integer-like token/asset/outcome id to a decimal string.

    Raises DataExportPrecisionLoss on scientific-notation / float-mangled ids
    (e.g. '5.20896e+76'). Never reconstruct a mangled 78-digit id.
    """
    if value is None:
        raise DataExportPrecisionLoss("null id")
    if isinstance(value, bool):
        raise DataExportPrecisionLoss("bool is not a valid id")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise DataExportPrecisionLoss(f"non-finite id: {value!r}")
        if value != int(value):
            raise DataExportPrecisionLoss(f"non-integer float id: {value!r}")
        if abs(value) >= 2 ** 53:
            raise DataExportPrecisionLoss(f"float id too large to be exact: {value!r}")
        return str(int(value))
    s = str(value).strip()
    if s == "":
        raise DataExportPrecisionLoss("empty id string")
    low = s.lower()
    if "e" in low or "+" in low or "." in s:
        if s in ("0.0", "-0.0"):
            return "0"
        raise DataExportPrecisionLoss(f"scientific-notation / float id: {s!r}")
    if low.startswith("0x"):
        raise DataExportPrecisionLoss(f"unexpected hex token id: {s!r}")
    neg = s.startswith("-")
    digits = s[1:] if neg else s
    if not digits.isdigit():
        raise DataExportPrecisionLoss(f"non-numeric id: {s!r}")
    norm = digits.lstrip("0") or "0"
    return ("-" + norm) if (neg and norm != "0") else norm


def assert_no_precision_loss(values: Iterable[Any], label: str) -> None:
    for v in values:
        try:
            canonical_int(v)
        except DataExportPrecisionLoss as exc:
            raise ProbeStop(STOP_PRECISION_LOSS, f"{label}: {exc}")


# ---------------------------------------------------------------------------
# Dependency-injection seams (tests inject in-memory frames; real loaders wired
# in build_real_loaders). Pure logic never imports pandas/pyarrow at import time.
# ---------------------------------------------------------------------------
@dataclass
class P1Loaders:
    load_p0: Callable[[], dict]
    load_contract: Callable[[], Any]
    load_gate: Callable[[], dict]
    load_resolution_rows: Callable[[], Any]
    load_prices: Callable[[Iterable[str]], Any]
    load_trades: Callable[[Iterable[str]], Any]
    canonical_side_price: Callable[[dict, dict], Any]


@dataclass
class P1Config:
    warmup_seconds: int = DEFAULT_WARMUP_SECONDS
    require_gate_clear: bool = True
    require_p0_clear: bool = True


@dataclass
class P1Result:
    stage: str = STAGE
    p1_state: str = P1_CLEAR
    authorized_scope: str = AUTHORIZED_SCOPE
    probe_execution_authorized: bool = PROBE_EXECUTION_AUTHORIZED
    scoring_authorized: bool = SCORING_AUTHORIZED
    named_binary_probe_blocked_observed: Optional[bool] = None
    nb_contract_version_expected: str = NB_CONTRACT_VERSION
    nb_contract_version_contract: Optional[str] = None
    nb_contract_version_resolution_source: Optional[str] = None
    decision_policy: str = "first_price_after_warmup"
    warmup_seconds: int = DEFAULT_WARMUP_SECONDS
    counts_p0_snapshot: dict = field(default_factory=dict)
    counts_p1_pooled: dict = field(default_factory=dict)
    counts_p1_by_subclass: dict = field(default_factory=dict)
    excluded_counts: dict = field(default_factory=dict)
    leakage_checks: dict = field(default_factory=dict)
    orientation_audit: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)
    created_at_utc: str = ""


# ---------------------------------------------------------------------------
# Decision timestamp
# ---------------------------------------------------------------------------
def first_price_after_warmup(price_rows_sorted, first_trade_ts, warmup_seconds):
    """First canonical-side price row at ts >= first_trade_ts + warmup_seconds.

    LEAKAGE: uses only first_trade_ts + a fixed warm-up; NEVER references
    resolution time (a lead-before-resolution would leak the outcome).
    Returns (decision_ts, price_row) or (None, None).
    """
    threshold = first_trade_ts + warmup_seconds
    for row in price_rows_sorted:
        if row["ts"] >= threshold:
            return row["ts"], row
    return None, None


# ---------------------------------------------------------------------------
# P0 verification
# ---------------------------------------------------------------------------
def _verify_p0(p0: dict, cfg: P1Config, result: P1Result) -> None:
    if not p0:
        raise ProbeStop(STOP_P0_NOT_CLEAR, "p0_preflight.json missing or empty")
    p0_state = p0.get("p0_state")
    scope = p0.get("authorized_scope")
    result.counts_p0_snapshot = {
        "p0_state": p0_state,
        "authorized_scope": scope,
        "probe_execution_authorized": p0.get("probe_execution_authorized"),
        "named_binary_probe_blocked_observed": p0.get("named_binary_probe_blocked_observed"),
        "counts_pooled": p0.get("counts_pooled", {}),
        "counts_by_subclass": p0.get("counts_by_subclass", {}),
        "excluded_counts": p0.get("excluded_counts", {}),
    }
    if cfg.require_p0_clear and p0_state != "P0_CLEAR":
        raise ProbeStop(STOP_P0_NOT_CLEAR, f"p0_state={p0_state!r}, required 'P0_CLEAR'")
    if cfg.require_p0_clear and scope != "P0_PREFLIGHT_ONLY":
        raise ProbeStop(STOP_P0_NOT_CLEAR, f"authorized_scope={scope!r}, required 'P0_PREFLIGHT_ONLY'")
    # P0_CLEAR is NOT probe authorization; preserve its false marker.
    if p0.get("probe_execution_authorized") not in (False, None):
        result.notes.append(
            "WARNING: P0 reported probe_execution_authorized truthy; P1 ignores it "
            "and does not treat P0 as probe authorization."
        )


# ---------------------------------------------------------------------------
# Gate (read-only precondition)
# ---------------------------------------------------------------------------
def _check_gate(gate: dict, cfg: P1Config, result: P1Result) -> dict:
    blocked = gate.get("named_binary_probe_blocked", None)
    result.named_binary_probe_blocked_observed = blocked
    if blocked is not True:
        result.notes.append(
            f"WARNING: named_binary_probe_blocked observed {blocked!r} (expected True); "
            "P1 neither relies on nor alters this flag."
        )
    branch = gate.get("stage4_nonyesno_branch", {}) or {}
    state = branch.get("non_yesno_gate_state")
    if cfg.require_gate_clear and state != REQUIRED_GATE_STATE:
        raise ProbeStop(
            STOP_DATA_GATE_NOT_CLEAR,
            f"non_yesno_gate_state={state!r}, required {REQUIRED_GATE_STATE!r}",
        )
    return branch


def _scoreable_subclasses(branch: dict) -> set:
    per = branch.get("per_subclass_scoreable", {}) or {}
    return {sc for sc in SUBCLASSES if per.get(sc) is True}


# ---------------------------------------------------------------------------
# Core assembly
# ---------------------------------------------------------------------------
def assemble_features(loaders: P1Loaders, cfg: Optional[P1Config] = None):
    cfg = cfg or P1Config()
    result = P1Result(
        warmup_seconds=cfg.warmup_seconds,
        created_at_utc=_dt.datetime.now(_dt.timezone.utc).isoformat(),
    )

    # ---- 1. P0 verification (read + require P0_CLEAR) ----
    p0 = loaders.load_p0()
    _verify_p0(p0, cfg, result)

    # ---- 2. Contract: version pin ----
    contract = loaders.load_contract()
    _assert_nonempty(contract, "classification contract", STOP_MISSING_OUTCOME_SOURCE)
    c_versions = set(_col(contract, "nb_contract_version"))
    result.nb_contract_version_contract = next(iter(c_versions)) if len(c_versions) == 1 else str(sorted(c_versions))
    if c_versions != {NB_CONTRACT_VERSION}:
        raise ProbeStop(STOP_STALE_CONTRACT, f"contract version {c_versions} != {{{NB_CONTRACT_VERSION!r}}}")

    # ---- 3. Gate: read-only precondition ----
    gate = loaders.load_gate()
    branch = _check_gate(gate, cfg, result)
    scoreable = _scoreable_subclasses(branch)

    # ---- 4. Resolution-source rows: version pin + held-aside target ----
    res_rows = loaders.load_resolution_rows()
    _assert_nonempty(res_rows, "resolution-source rows", STOP_MISSING_OUTCOME_SOURCE)
    r_versions = set(_col(res_rows, "nb_contract_version"))
    result.nb_contract_version_resolution_source = next(iter(r_versions)) if len(r_versions) == 1 else str(sorted(r_versions))
    if r_versions != {NB_CONTRACT_VERSION}:
        raise ProbeStop(STOP_STALE_CONTRACT, f"resolution-source version {r_versions} != {{{NB_CONTRACT_VERSION!r}}}")
    # Precision-scan held-aside target token ids (never reconstruct).
    for col in ("resolved_winning_token_id",):
        vals = _col_optional(res_rows, col)
        if vals:
            assert_no_precision_loss(vals, col)

    res_index = {r["condition_id"]: r for r in _iter_rows(res_rows)}

    # ---- 5. Build eligible universe (non-YES/NO, scoreable, RESOLVED_SINGLE_WINNER) ----
    eligible = []
    excl_yes_no = 0
    excl_not_eligible = 0
    excl_not_scoreable = 0
    excl_no_resolution = 0
    excl_ambiguous_or_missing = 0
    for row in _iter_rows(contract):
        cid = row["condition_id"]
        sub = row["subclass"]
        is_eligible = bool(row.get("eligible", True))
        if sub == YES_NO:
            excl_yes_no += 1
            continue
        if sub not in SUBCLASSES or not is_eligible:
            excl_not_eligible += 1
            continue
        if sub not in scoreable:
            excl_not_scoreable += 1
            continue
        rr = res_index.get(cid)
        if rr is None:
            excl_no_resolution += 1
            continue
        status = rr.get("status")
        if status != "RESOLVED_SINGLE_WINNER":
            # AMBIGUOUS_MULTIPLE_WINNERS / anything else -> excluded + counted
            excl_ambiguous_or_missing += 1
            continue
        eligible.append((cid, sub, rr))

    if not eligible:
        raise ProbeStop(STOP_NO_FEATURE_ROWS, "no eligible+scoreable+resolved conditions")

    # ---- 6. Prices + trades for eligible conditions ----
    cids = [c for (c, _, _) in eligible]
    prices = loaders.load_prices(cids)
    trades = loaders.load_trades(cids)
    prices_by_cid = _group_by_condition(prices) if prices is not None else {}
    trades_by_cid = _group_by_condition(trades) if trades is not None else {}

    per_sub = {sc: {"eligible": 0, "assembled": 0,
                    "no_trade_anchor": 0, "no_decision_price": 0,
                    "orientation_unresolved": 0, "y1": 0, "y0": 0}
               for sc in SUBCLASSES}
    feature_rows = []
    leakage_excluded = 0
    orientation_token_checked = 0
    orientation_label_only_flagged = 0

    for cid, sub, rr in eligible:
        per_sub[sub]["eligible"] += 1
        t_rows = trades_by_cid.get(cid)
        p_rows = prices_by_cid.get(cid)

        if not t_rows:
            per_sub[sub]["no_trade_anchor"] += 1
            continue
        first_trade_ts = min(r["ts"] for r in t_rows)

        if not p_rows:
            per_sub[sub]["no_decision_price"] += 1
            continue
        sorted_prices = sorted(
            ({"ts": r["ts"], "yes_price": r["yes_price"],
              "token_id": r.get("token_id"), "outcome_index": r.get("outcome_index")}
             for r in p_rows),
            key=lambda x: x["ts"],
        )
        decision_ts, decision_row = first_price_after_warmup(
            sorted_prices, first_trade_ts, cfg.warmup_seconds
        )
        if decision_ts is None:
            per_sub[sub]["no_decision_price"] += 1
            continue

        # ---- LEAKAGE GUARDS ----
        # selected price ts must be <= decision_ts (it IS decision_ts by construction)
        if decision_row["ts"] > decision_ts:
            raise ProbeStop(STOP_LEAKAGE_GUARD, f"{cid}: selected price ts after decision_ts")
        resolution_ts = rr.get("resolved_at")
        if resolution_ts is not None and not (decision_ts < resolution_ts):
            leakage_excluded += 1
            continue  # excluded + counted; never a feature row

        # ---- Orientation via semantics layer (consume, do not reimplement) ----
        contract_row = {"condition_id": cid, "subclass": sub}
        oriented = loaders.canonical_side_price(contract_row, decision_row)
        p_hat = _extract_price(oriented)
        if p_hat is None or not (0.0 <= p_hat <= 1.0):
            per_sub[sub]["orientation_unresolved"] += 1
            result.notes.append(f"{cid}: canonical_side_price missing/out-of-range -> excluded")
            continue

        # Orientation audit fields (detect label-only inversion / token mismatch)
        oriented_token = _oriented_field(oriented, "canonical_side_token_id")
        oriented_outcome_index = _oriented_field(oriented, "canonical_side_outcome_index")
        label_only = _oriented_field(oriented, "label_only_orientation")
        if oriented_token is not None:
            orientation_token_checked += 1
        if label_only is True:
            orientation_label_only_flagged += 1

        # ---- Held-aside target metadata (NOT used to choose the row) ----
        y_target = _oriented_side_is_winner(rr, oriented, contract_row)

        feature_rows.append({
            "condition_id": cid,
            "subclass": sub,
            "first_trade_ts": first_trade_ts,
            "decision_ts": decision_ts,
            "warmup_seconds": cfg.warmup_seconds,
            "canonical_side_price": p_hat,
            "raw_yes_price": decision_row.get("yes_price"),
            "selected_price_ts": decision_row["ts"],
            "selected_token_id": _safe_id(decision_row.get("token_id")),
            "selected_outcome_index": _safe_id(decision_row.get("outcome_index")),
            "canonical_side_token_id": _safe_id(oriented_token),
            "canonical_side_outcome_index": _safe_id(oriented_outcome_index),
            # target-only metadata, explicitly NOT a feature:
            "resolved_winning_token_id": _safe_id(rr.get("resolved_winning_token_id")),
            "resolved_outcome_index": _safe_id(rr.get("resolved_outcome_index")),
            "y_target_target_only_not_feature": y_target,
            "nb_contract_version": NB_CONTRACT_VERSION,
        })
        per_sub[sub]["assembled"] += 1
        if y_target == 1:
            per_sub[sub]["y1"] += 1
        elif y_target == 0:
            per_sub[sub]["y0"] += 1

    # ---- All-one-direction guard (217/0, 10/0 red-flag class) ----
    for sub in SUBCLASSES:
        a = per_sub[sub]["assembled"]
        y1, y0 = per_sub[sub]["y1"], per_sub[sub]["y0"]
        # only trip when the target is actually determinable for the whole sample
        determined = y1 + y0
        if a >= 2 and determined >= 2 and (y1 == 0 or y0 == 0):
            raise ProbeStop(
                STOP_LEAKAGE_GUARD,
                f"all-one-direction held-aside target for {sub}: "
                f"assembled={a} y1={y1} y0={y0} — validate before proceeding.",
            )

    if not feature_rows:
        # Every eligible condition fell out (no anchor / no price / leakage) ->
        # distinguish an all-missing-decision case, per spec §7.
        all_no_decision = all(
            per_sub[s]["assembled"] == 0 for s in SUBCLASSES
        )
        if all_no_decision and leakage_excluded == 0:
            raise ProbeStop(STOP_NO_FEATURE_ROWS, "no feature rows after decision-timestamp assembly")
        raise ProbeStop(STOP_LEAKAGE_GUARD, "no feature rows; leakage exclusions present — validate")

    if leakage_excluded > 0:
        result.notes.append(
            f"{leakage_excluded} condition(s) had decision_ts >= resolution_ts; "
            "EXCLUDED from features (leakage guard)."
        )

    # ---- Counts + audits ----
    result.counts_p1_pooled = {
        "eligible_conditions": len(eligible),
        "assembled_feature_rows": len(feature_rows),
        "no_trade_anchor": sum(per_sub[s]["no_trade_anchor"] for s in SUBCLASSES),
        "no_decision_price": sum(per_sub[s]["no_decision_price"] for s in SUBCLASSES),
        "orientation_unresolved": sum(per_sub[s]["orientation_unresolved"] for s in SUBCLASSES),
        "leakage_excluded_decision_ge_resolution": leakage_excluded,
    }
    result.counts_p1_by_subclass = per_sub
    result.excluded_counts = {
        "YES_NO": excl_yes_no,
        "NOT_ELIGIBLE_OR_UNUSABLE": excl_not_eligible,
        "NOT_SCOREABLE_SUBCLASS": excl_not_scoreable,
        "NO_RESOLUTION_ROW": excl_no_resolution,
        "AMBIGUOUS_OR_NON_SINGLE_WINNER": excl_ambiguous_or_missing,
        "NO_TRADE_ANCHOR": result.counts_p1_pooled["no_trade_anchor"],
        "NO_DECISION_PRICE": result.counts_p1_pooled["no_decision_price"],
        "LEAKAGE_DECISION_GE_RESOLUTION": leakage_excluded,
        "ORIENTATION_UNRESOLVED": result.counts_p1_pooled["orientation_unresolved"],
    }
    result.leakage_checks = {
        "decision_policy": "first_price_after_warmup",
        "decision_ts_strictly_before_resolution": leakage_excluded == 0,
        "resolution_time_used_to_choose_row": False,
        "selected_price_ts_le_decision_ts": True,
        "near_final_price_used": False,
        "all_one_direction_guard": "PASSED_OR_NOT_TRIGGERED",
    }
    result.orientation_audit = {
        "orientation_source": "pm_research.semantics.named_binary",
        "token_identity_checked_rows": orientation_token_checked,
        "label_only_orientation_flagged": orientation_label_only_flagged,
        "reimplemented_orientation": False,
    }
    result.p1_state = P1_CLEAR
    return result, feature_rows


# ---------------------------------------------------------------------------
# Held-aside target (payout-vector winner ONLY; never price)
# ---------------------------------------------------------------------------
def _oriented_side_is_winner(res_row: dict, oriented: Any, contract_row: dict):
    if isinstance(oriented, dict) and oriented.get("oriented_side_won") is not None:
        return 1 if bool(oriented["oriented_side_won"]) else 0
    if res_row.get("oriented_side_won") is not None:
        return 1 if bool(res_row["oriented_side_won"]) else 0
    win_tok = res_row.get("resolved_winning_token_id")
    canon_tok = _oriented_field(oriented, "canonical_side_token_id") or contract_row.get("canonical_side_token_id")
    if win_tok is not None and canon_tok is not None:
        return 1 if canonical_int(win_tok) == canonical_int(canon_tok) else 0
    return None  # undeterminable target — excluded from y1/y0 tally


# ---------------------------------------------------------------------------
# Frame helpers (work for pandas DataFrame or list[dict])
# ---------------------------------------------------------------------------
def _is_pandas(obj) -> bool:
    return hasattr(obj, "iterrows") and hasattr(obj, "columns")


def _assert_nonempty(obj, label, stop_code):
    if obj is None:
        raise ProbeStop(stop_code, f"{label} is None")
    if _is_pandas(obj):
        if len(obj) == 0:
            raise ProbeStop(stop_code, f"{label} is empty")
    elif not obj:
        raise ProbeStop(stop_code, f"{label} is empty")


def _col(obj, name):
    if _is_pandas(obj):
        return list(obj[name])
    return [r[name] for r in obj]


def _col_optional(obj, name):
    if _is_pandas(obj):
        return [v for v in obj[name] if v is not None] if name in obj.columns else []
    return [r[name] for r in obj if name in r and r[name] is not None]


def _iter_rows(obj):
    if _is_pandas(obj):
        for _, r in obj.iterrows():
            yield dict(r)
    else:
        for r in obj:
            yield dict(r)


def _group_by_condition(obj):
    out = {}
    for r in _iter_rows(obj):
        out.setdefault(r["condition_id"], []).append(r)
    return out


def _extract_price(oriented):
    if oriented is None:
        return None
    if isinstance(oriented, (int, float)):
        return float(oriented)
    if isinstance(oriented, dict):
        for k in ("canonical_side_price", "oriented_price", "price", "yes_price"):
            if oriented.get(k) is not None:
                return float(oriented[k])
    return None


def _oriented_field(oriented, key):
    if isinstance(oriented, dict):
        return oriented.get(key)
    return None


def _safe_id(v):
    if v is None:
        return None
    try:
        return canonical_int(v)
    except DataExportPrecisionLoss:
        raise ProbeStop(STOP_PRECISION_LOSS, f"id field: {v!r}")


# ---------------------------------------------------------------------------
# Real-loader wiring (runtime only; local repo + pyarrow)
# ---------------------------------------------------------------------------
def build_real_loaders(root: str, artifacts_dir: str) -> P1Loaders:
    """Wire P1 to the local repo. Exact shape (confirmed against the live repo):

        pm_research.data.store.Store(root)
            .load_trades(wallets=None) -> DataFrame   # full trade set; wallet filter only
            .load_prices()             -> DataFrame[condition_id, ts, yes_price]
        pm_research.semantics.named_binary.canonical_side_price(contract_row, price_row)

    Notes on this store's contract:
      - There is no per-condition push-down filter on load_trades/load_prices, so P1
        loads each once and filters by the (small) eligible condition_id set in-memory.
        `load_trades()` materializes the full trade set (~16.5M rows); this is the
        memory-heavy step. We filter immediately and keep only eligible-condition rows.
      - The prices schema is [condition_id, ts, yes_price] — no token_id/outcome_index
        on price rows. Orientation therefore comes entirely from the semantics layer
        keyed on the condition (as designed); the per-price token audit fields stay null.
        P1 tolerates their absence (no assumption that price rows carry token columns).
    """
    import pandas as pd  # runtime only
    from pm_research.data.store import Store  # type: ignore
    from pm_research.semantics import named_binary as nb  # type: ignore

    store = Store(root)

    nb_art = os.path.join(artifacts_dir, "named_binary")
    probe_art = os.path.join(artifacts_dir, "named_binary_probe")
    p0_path = os.path.join(probe_art, "p0_preflight.json")
    contract_path = os.path.join(nb_art, "named_binary_classification_contract.json")
    gate_path = os.path.join(nb_art, "named_binary_audit_gate.json")
    res_path = os.path.join(nb_art, "named_binary_resolution_source_rows.parquet")

    def load_p0():
        with open(p0_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def load_contract():
        with open(contract_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        recs = data["conditions"] if isinstance(data, dict) and "conditions" in data else data
        df = pd.DataFrame(recs)
        if "nb_contract_version" not in df.columns:
            df["nb_contract_version"] = (
                data.get("nb_contract_version", NB_CONTRACT_VERSION)
                if isinstance(data, dict) else NB_CONTRACT_VERSION
            )
        return df

    def load_gate():
        with open(gate_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def load_resolution_rows():
        df = pd.read_parquet(res_path)
        for c in ("resolved_winning_token_id", "canonical_side_token_id"):
            if c in df.columns:
                df[c] = df[c].astype("string")
        return df

    def _prices(cids):
        want = set(cids)
        df = store.load_prices()  # [condition_id, ts, yes_price]
        df = df[df["condition_id"].isin(want)]
        # Ensure optional token columns exist so downstream .get() is uniform.
        for opt in ("token_id", "outcome_index"):
            if opt not in df.columns:
                df[opt] = None
        return df

    def _trades(cids):
        want = set(cids)
        # load_trades(wallets=None) returns the full set; filter to eligible conditions.
        df = store.load_trades()  # hygiene (null-condition drop, dedup) applied by store
        return df[df["condition_id"].isin(want)]

    def _canon(contract_row, price_row):
        return nb.canonical_side_price(contract_row, price_row)

    return P1Loaders(load_p0, load_contract, load_gate, load_resolution_rows,
                     _prices, _trades, _canon)


# ---------------------------------------------------------------------------
# Artifact emission
# ---------------------------------------------------------------------------
def write_artifacts(result: P1Result, feature_rows: list, out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "p1_feature_assembly.json")
    md_path = os.path.join(out_dir, "p1_feature_assembly.md")
    feat_path = os.path.join(out_dir, "p1_features.parquet")
    excl_path = os.path.join(out_dir, "p1_excluded_conditions.csv")
    feat_csv_fallback = os.path.join(out_dir, "p1_features.csv")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(asdict(result), fh, indent=2, default=str)

    wrote_feat = None
    try:
        import pandas as pd  # runtime only
        pd.DataFrame(feature_rows).to_parquet(feat_path, index=False)
        wrote_feat = feat_path
    except Exception:
        import csv
        if feature_rows:
            with open(feat_csv_fallback, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(feature_rows[0].keys()))
                w.writeheader()
                w.writerows(feature_rows)
            wrote_feat = feat_csv_fallback

    import csv as _csv
    with open(excl_path, "w", newline="", encoding="utf-8") as fh:
        w = _csv.writer(fh)
        w.writerow(["reason", "count"])
        for k, v in result.excluded_counts.items():
            w.writerow([k, v])

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(_render_md(result))

    return {"json": json_path, "md": md_path, "features": wrote_feat, "excluded": excl_path}


def _render_md(result: P1Result) -> str:
    L = []
    L.append("# Named-Binary Probe — Stage P1 (feature assembly)\n")
    L.append(f"- stage: **{result.stage}**")
    L.append(f"- p1_state: **{result.p1_state}**")
    L.append(f"- authorized_scope: {result.authorized_scope}")
    L.append(f"- probe_execution_authorized: {result.probe_execution_authorized}")
    L.append(f"- scoring_authorized: {result.scoring_authorized}")
    L.append(f"- named_binary_probe_blocked (observed, not flipped): {result.named_binary_probe_blocked_observed}")
    L.append(f"- nb_contract_version (expected/contract/resolution): "
             f"{result.nb_contract_version_expected} / {result.nb_contract_version_contract} / "
             f"{result.nb_contract_version_resolution_source}")
    L.append(f"- decision_policy: {result.decision_policy} (warmup_seconds={result.warmup_seconds})")
    L.append(f"- created_at_utc: {result.created_at_utc}")
    L.append("\n## P0 snapshot\n")
    for k, v in result.counts_p0_snapshot.items():
        if k not in ("counts_pooled", "counts_by_subclass", "excluded_counts"):
            L.append(f"- {k}: {v}")
    L.append("\n## P1 pooled counts\n")
    for k, v in result.counts_p1_pooled.items():
        L.append(f"- {k}: {v}")
    L.append("\n## Per-subclass\n")
    L.append("| subclass | eligible | assembled | no_trade_anchor | no_decision_price | orientation_unresolved | y1 | y0 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for sc in SUBCLASSES:
        s = result.counts_p1_by_subclass.get(sc, {})
        L.append(f"| {sc} | {s.get('eligible',0)} | {s.get('assembled',0)} | "
                 f"{s.get('no_trade_anchor',0)} | {s.get('no_decision_price',0)} | "
                 f"{s.get('orientation_unresolved',0)} | {s.get('y1',0)} | {s.get('y0',0)} |")
    L.append("\n## Excluded counts\n")
    for k, v in result.excluded_counts.items():
        L.append(f"- {k}: {v}")
    L.append("\n## Leakage checks\n")
    for k, v in result.leakage_checks.items():
        L.append(f"- {k}: {v}")
    L.append("\n## Orientation audit\n")
    for k, v in result.orientation_audit.items():
        L.append(f"- {k}: {v}")
    if result.notes:
        L.append("\n## Notes\n")
        for n in result.notes:
            L.append(f"- {n}")
    L.append("\n## Scope boundary\n")
    L.append("P1 assembles decision-timestamp + canonical_side_price (C0 input) only. "
             "No scoring, no calibrator fit, no splits, no verdict (P2/P3). The held-aside "
             "target (`y_target_target_only_not_feature`) is metadata, never a feature, and "
             "is never used to choose the decision row. Probe execution remains NOT AUTHORIZED; "
             "`named_binary_probe_blocked` is observed, not flipped.")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Named-binary probe Stage P1 feature assembly (no scoring).")
    ap.add_argument("--root", default="C:\\b1\\data", help="Data root passed to load_trades/load_prices.")
    ap.add_argument("--artifacts-dir", default="artifacts", help="Artifacts dir (contains named_binary/ and named_binary_probe/).")
    ap.add_argument("--warmup-seconds", type=int, default=DEFAULT_WARMUP_SECONDS)
    args = ap.parse_args(argv)

    out_dir = os.path.join(args.artifacts_dir, "named_binary_probe")
    cfg = P1Config(warmup_seconds=args.warmup_seconds)

    try:
        loaders = build_real_loaders(args.root, args.artifacts_dir)
        result, feature_rows = assemble_features(loaders, cfg)
    except ProbeStop as stop:
        os.makedirs(out_dir, exist_ok=True)
        # Emit the typed halt into the standard json artifact for auditability.
        halt = P1Result(p1_state=stop.code, created_at_utc=_dt.datetime.now(_dt.timezone.utc).isoformat())
        halt.notes.append(stop.detail)
        with open(os.path.join(out_dir, "p1_feature_assembly.json"), "w", encoding="utf-8") as fh:
            json.dump(asdict(halt), fh, indent=2, default=str)
        print(f"[P1 HALT] {stop.code}: {stop.detail}", file=sys.stderr)
        return 2

    paths = write_artifacts(result, feature_rows, out_dir)
    print(f"[P1 OK] {result.p1_state}: assembled {result.counts_p1_pooled.get('assembled_feature_rows')} feature rows")
    for k, v in paths.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
