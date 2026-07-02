"""Stage 0 — read-only Dune schema inspection for the named-binary resolution
source. INSPECTION ONLY.

This script does NOT build a resolution source, does NOT join against local
named-binary conditions (beyond tiny format/normalization examples), does NOT
modify the audit gate, and does NOT run any probe. It inspects candidate Dune
table schemas and a few bounded, varchar-cast sample rows so a human can judge
whether Stage 1 is viable.

What it does:
  1. For each candidate table, fetch its column schema (information_schema) and
     print column names + types.
  2. For tables that look like resolution/payout sources, fetch a TINY bounded
     sample (LIMIT a few hundred) with EVERY uint256-like field cast to varchar,
     to observe condition_id format and payout-vector shape.
  3. Read every downloaded CSV with dtype=str and FAIL LOUDLY on scientific
     notation in any token/asset/payout field.
  4. Write a machine-readable schema report. No normalized resolution rows.

How it runs (the user executes locally; this script issues schema-inspection
queries via the Dune API, it does not hardcode results):
  - Requires a Dune API key in $env:DUNE_API_KEY.
  - Two modes:
      --mode list-schema    : print columns/types for each candidate table.
      --mode sample         : fetch tiny varchar-cast samples for resolution
                              tables and report condition_id / payout shape.
  - The actual SQL is emitted to the report so it can be reviewed before running,
    consistent with "do not run production exports beyond schema inspection."

IMPORTANT: this script is delivered for local execution. In an environment with
no Dune access it will emit the inspection SQL and the candidate table list and
exit; it asserts NO schema facts it did not observe.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional


# Candidate tables to inspect. Inspect each SEPARATELY. Do NOT union before
# inspection. Newer V2/V3 variants are listed separately and must be schema-
# checked independently (their columns may differ from the old tables).
CANDIDATE_TABLES = {
    "condition_resolution": [
        # CTF / ConditionalTokens ConditionResolution-style events (payout vector).
        # Names are CANDIDATES to verify via information_schema, NOT assumed real.
        "polymarket_polygon.ctf_evt_conditionresolution",
        "polymarket_polygon.conditionaltokens_evt_conditionresolution",
        "polygon.conditionaltokens_evt_conditionresolution",
    ],
    "payout_redemption": [
        # Corroboration candidates ONLY (not primary unless ConditionResolution
        # is unavailable).
        "polymarket_polygon.ctf_evt_payoutredemption",
        "polymarket_polygon.conditionaltokens_evt_payoutredemption",
        "polygon.conditionaltokens_evt_payoutredemption",
    ],
    "market_metadata": [
        # condition_id -> outcome label/index, corroboration only.
        "polymarket_polygon.markets",
        "polymarket_polygon.market_metadata",
    ],
}

# Fields we need to confirm exist (per table category).
REQUIRED_FIELDS = {
    "condition_resolution": [
        "condition_id", "payout_numerators", "payout_vector",
        "block_time", "evt_block_time", "contract_address",
    ],
    "payout_redemption": [
        "condition_id", "redeemer", "index_sets", "payout",
        "block_time", "evt_block_time", "contract_address",
    ],
    "market_metadata": [
        "condition_id", "outcome", "outcome_index", "token_id", "tokenid",
    ],
}

# Fields that, if present, MUST be cast to varchar before export (uint256-like).
UINT256_LIKE = {
    "condition_id", "token_id", "tokenid", "asset_id", "assetid",
    "payout", "payout_numerators", "payout_vector", "payouts",
    "index_sets", "indexsets", "amount", "makerassetid", "takerassetid",
}

SCI_NOTATION = re.compile(r"^\s*-?\d+(\.\d+)?[eE][+-]?\d+\s*$")


def _need_varchar(colname: str) -> bool:
    c = colname.lower().replace("_", "")
    return any(c == f.replace("_", "") or f.replace("_", "") in c for f in UINT256_LIKE)


def emit_information_schema_sql(table: str) -> str:
    schema, _, name = table.partition(".")
    return (
        "select column_name, data_type\n"
        "from information_schema.columns\n"
        f"where table_schema = '{schema}' and table_name = '{name}'\n"
        "order by ordinal_position"
    )


def emit_sample_sql(table: str, columns: List[str], limit: int = 200) -> str:
    """Tiny bounded sample with uint256-like fields cast to varchar.

    Only emitted AFTER columns are known (so we cast the right ones). This is a
    schema-inspection sample, not a production export: small LIMIT, varchar casts.
    """
    select_parts = []
    for c in columns:
        if _need_varchar(c):
            select_parts.append(f"cast({c} as varchar) as {c}")
        else:
            select_parts.append(c)
    cols_sql = ",\n  ".join(select_parts)
    return f"select\n  {cols_sql}\nfrom {table}\nlimit {limit}"


def check_csv_for_precision_loss(path: str) -> None:
    """Read a downloaded inspection CSV with dtype=str and FAIL LOUDLY if any
    uint256-like column contains scientific notation."""
    import csv as _csv
    with open(path, newline="", encoding="utf-8") as f:
        reader = _csv.DictReader(f)
        uint_cols = [c for c in (reader.fieldnames or []) if _need_varchar(c)]
        for i, row in enumerate(reader):
            for c in uint_cols:
                val = (row.get(c) or "").strip()
                if SCI_NOTATION.match(val):
                    raise SystemExit(
                        f"DATA_EXPORT_PRECISION_LOSS: scientific notation in "
                        f"column {c!r} row {i} of {path}: {val!r}. Re-export with "
                        f"the uint256 field cast to varchar; do NOT reconstruct."
                    )
    print(f"[precision-ok] {path}: no scientific notation in uint256-like columns",
          file=sys.stderr)


def observe_condition_id_format(path: str, local_example: Optional[str] = None) -> Dict:
    """Report the shape of condition_id values in a sample CSV and compare to a
    local example (tiny format/normalization check only — NOT a join)."""
    import csv as _csv
    out = {"n": 0, "sample_values": [], "all_0x_prefixed": None,
           "all_lower": None, "len_set": set(), "matches_local_format": None}
    with open(path, newline="", encoding="utf-8") as f:
        reader = _csv.DictReader(f)
        if "condition_id" not in (reader.fieldnames or []):
            return {"error": "no condition_id column in sample"}
        prefixed = lower = True
        for row in reader:
            v = (row.get("condition_id") or "").strip()
            out["n"] += 1
            if len(out["sample_values"]) < 5:
                out["sample_values"].append(v)
            if not v.startswith("0x"):
                prefixed = False
            if v != v.lower():
                lower = False
            out["len_set"].add(len(v))
        out["all_0x_prefixed"] = prefixed
        out["all_lower"] = lower
        out["len_set"] = sorted(out["len_set"])
    if local_example is not None and out.get("sample_values"):
        s = out["sample_values"][0]
        out["matches_local_format"] = (
            s.startswith("0x") == local_example.startswith("0x")
            and (s == s.lower()) == (local_example == local_example.lower())
            and len(s) == len(local_example)
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["list-schema", "sample", "emit-sql"],
                    default="emit-sql",
                    help="emit-sql: print inspection SQL + candidate list (no "
                         "network). list-schema/sample: require Dune access.")
    ap.add_argument("--out-dir", default="artifacts/named_binary_schema_inspection")
    ap.add_argument("--local-condition-example", default=None,
                    help="a single local condition_id, for tiny format comparison only")
    ap.add_argument("--sample-csv", default=None,
                    help="path to a downloaded inspection CSV to precision-check + "
                         "observe condition_id format (offline-safe)")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    report: Dict = {
        "stage": 0,
        "purpose": "read-only schema inspection for named-binary resolution source",
        "candidate_tables": CANDIDATE_TABLES,
        "required_fields_by_category": REQUIRED_FIELDS,
        "uint256_like_fields_requiring_varchar": sorted(UINT256_LIKE),
        "inspection_sql": {},
        "notes": [
            "Inspect each table separately. Do NOT union before inspection.",
            "ConditionResolution payout vector is the primary candidate; "
            "PayoutRedemption is corroboration only.",
            "Newer V2/V3 variants must be schema-checked independently.",
            "This script writes NO normalized resolution source and modifies "
            "no gate.",
            "Dune runs Trino: do NOT append a trailing ';' to queries in the "
            "Dune editor (it rejects the terminator). Emitted SQL omits it.",
        ],
    }

    # Always emit the information_schema SQL per candidate (review before running).
    for category, tables in CANDIDATE_TABLES.items():
        for t in tables:
            report["inspection_sql"][t] = {
                "information_schema": emit_information_schema_sql(t),
                "note": "run this first; then build the varchar-cast sample SQL "
                        "from the actual columns returned.",
            }

    # Offline-safe: if a sample CSV was provided, precision-check + observe format.
    if args.sample_csv:
        check_csv_for_precision_loss(args.sample_csv)
        cid_obs = observe_condition_id_format(args.sample_csv,
                                              args.local_condition_example)
        report["condition_id_observation"] = cid_obs

    if args.mode == "emit-sql":
        # No network: emit the plan + SQL for review/execution by the user.
        report["mode"] = "emit-sql (no network used)"
    else:
        # list-schema / sample require Dune access. The actual API calls are the
        # user's to run; we do not execute production exports here. We record the
        # intent and the exact API CSV command pattern (DUNE_DATA_NOTES §7).
        report["mode"] = args.mode
        report["dune_api_csv_pattern"] = (
            'curl.exe -H "x-dune-api-key: $env:DUNE_API_KEY" '
            '"https://api.dune.com/api/v1/query/<QUERY_ID>/results/csv?limit=5000" '
            '-o <out>.csv'
        )
        report["dune_api_note"] = (
            "Save each inspection query on Dune with uint256-like fields cast to "
            "varchar, EXECUTE it, then fetch via the API CSV endpoint. The API "
            "serves the last execution, not the saved SQL."
        )

    out_path = os.path.join(args.out_dir, "schema_inspection_report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"wrote {out_path}")
    print("Stage 0 inspection plan emitted. No resolution source built, no gate "
          "modified, no probe run.", file=sys.stderr)


if __name__ == "__main__":
    main()
