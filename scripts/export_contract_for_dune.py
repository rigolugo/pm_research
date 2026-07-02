"""Export the Chat1 named-binary classification contract to a Dune-upload-ready
CSV for the Stage 1 Query C coverage join.

LOCAL FILE I/O ONLY. No Dune, no network, no probe, no gate, no source build.

Reads:
    artifacts/named_binary/named_binary_classification_contract.json
Writes (default under C:\\b1\\csv\\):
    nb_contract_for_dune.csv  with columns:
        condition_id, subclass, eligible, nb_contract_version

Why this exists: Query C joins the resolution table against the Chat1 contract,
which currently lives only as a local JSON artifact. Dune needs it as an uploaded
dataset. The JOIN KEY is condition_id, and Query C produces it Dune-side as
'0x' || lower(to_hex(conditionid)) -> a 0x-prefixed lowercase 66-char hex string.
If the contract's condition_id is not in that exact format, EVERY join row misses
and Query C reports a misleading 0% coverage. So this script VALIDATES the format
and fails loudly on any mismatch rather than letting a key-format bug masquerade
as "no coverage."

Usage:
    python scripts\\export_contract_for_dune.py ^
        --contract artifacts\\named_binary\\named_binary_classification_contract.json ^
        --out C:\\b1\\csv\\nb_contract_for_dune.csv

Options:
    --eligible-only      only export rows with nb_eligible = true (default: true)
    --non-yesno-only     further restrict to non-YES/NO subclasses (the coverage
                         question of interest). Default: false (export all eligible).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

# Local condition_id format: 0x + 64 lowercase hex chars = length 66.
_CID_RE = re.compile(r"^0x[0-9a-f]{64}$")

# Expected subclass vocabulary (from the pinned lexicon). Used only to sanity-
# check the contract, not to reclassify anything.
_KNOWN_SUBCLASSES = {
    "YES_NO", "OVER_UNDER", "UP_DOWN", "TEAM_VS_TEAM", "NAMED_OTHER", "UNUSABLE",
}
_NON_YESNO = {"OVER_UNDER", "UP_DOWN", "TEAM_VS_TEAM", "NAMED_OTHER"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", required=True,
                    help="path to named_binary_classification_contract.json")
    ap.add_argument("--out", default=r"C:\b1\csv\nb_contract_for_dune.csv")
    ap.add_argument("--eligible-only", action="store_true", default=True)
    ap.add_argument("--all-rows", dest="eligible_only", action="store_false",
                    help="export every row, not just eligible (overrides default)")
    ap.add_argument("--non-yesno-only", action="store_true", default=False,
                    help="restrict to non-YES/NO subclasses")
    args = ap.parse_args()

    if not os.path.exists(args.contract):
        raise SystemExit(f"contract not found: {args.contract}")

    with open(args.contract, "r", encoding="utf-8") as f:
        contract = json.load(f)

    top_version = contract.get("nb_contract_version")
    rows = contract.get("conditions", [])
    if not rows:
        raise SystemExit("contract has no 'conditions' list; nothing to export")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    # Validation counters
    n_total = 0
    n_written = 0
    n_bad_format = 0
    bad_examples = []
    version_mismatch = 0
    subclass_counts = {}
    unknown_subclasses = set()

    out_rows = []
    for r in rows:
        n_total += 1
        cid = str(r.get("condition_id", "")).strip()
        sub = str(r.get("nb_subclass", "")).strip()
        elig = bool(r.get("nb_eligible", False))
        ver = str(r.get("nb_contract_version", "")).strip()

        if args.eligible_only and not elig:
            continue
        if args.non_yesno_only and sub not in _NON_YESNO:
            continue

        # Validate join key format — this is the load-bearing check.
        if not _CID_RE.match(cid):
            n_bad_format += 1
            if len(bad_examples) < 10:
                bad_examples.append(cid)
            continue

        if sub not in _KNOWN_SUBCLASSES:
            unknown_subclasses.add(sub)
        if top_version and ver and ver != top_version:
            version_mismatch += 1

        subclass_counts[sub] = subclass_counts.get(sub, 0) + 1
        out_rows.append((cid, sub, "true" if elig else "false",
                         ver or top_version or ""))
        n_written += 1

    # Fail loudly if the join key is malformed — a format bug here becomes a
    # silent 0% coverage in Query C, exactly what we must not allow.
    if n_bad_format > 0:
        print(f"ERROR: {n_bad_format} condition_id values are NOT in the expected "
              f"Dune join format (0x + 64 lowercase hex). Examples: {bad_examples}",
              file=sys.stderr)
        print("These would silently MISS the Query C join and report false 0% "
              "coverage. Fix the contract's condition_id format before uploading.",
              file=sys.stderr)
        raise SystemExit(2)

    if version_mismatch:
        print(f"WARNING: {version_mismatch} rows have a per-row nb_contract_version "
              f"!= top-level {top_version!r}.", file=sys.stderr)
    if unknown_subclasses:
        print(f"WARNING: unexpected subclasses present: {sorted(unknown_subclasses)}",
              file=sys.stderr)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["condition_id", "subclass", "eligible", "nb_contract_version"])
        w.writerows(out_rows)

    print(f"wrote {args.out}")
    print(f"  contract version : {top_version}")
    print(f"  rows in contract : {n_total}")
    print(f"  rows written     : {n_written}"
          f" ({'eligible only' if args.eligible_only else 'all rows'}"
          f"{', non-YES/NO only' if args.non_yesno_only else ''})")
    print(f"  by subclass      : "
          + ", ".join(f"{k}={v}" for k, v in sorted(subclass_counts.items())))
    print(f"  condition_id fmt : all {n_written} rows are 0x+64-lowercase-hex (validated)")
    print("\nNext: upload this CSV to Dune as a dataset, then in Query C replace")
    print("  from query_NNNNNNN")
    print("with")
    print("  from dune.<your_team>.dataset_<name>")
    print("Then RUN Query C in Dune before fetching the API CSV.")


if __name__ == "__main__":
    main()
