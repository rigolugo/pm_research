# SPEC — Local-Curl Per-Side Dataset Verification — Revision 23

**Status:** `SPECIFICATION_REVISION_ONLY — REV23 Amendment 03 materialized for Professor → Sentinel review`.  
**Supersedes:** Revision 22 in full. No implementer may consult Revision 22 or any earlier revision to recover governing rules.  
**Project:** `rigolugo/pm_research`.  
**Reviewer / decision authority:** Sentinel.  
**Implementation agent after separate acceptance only:** Claude.  
**Execution authority after separate authorization only:** Gustavo.

## 0. Authority boundary and standing state

This is a specification revision only. It authorizes no implementation, tests, prefetch, local reads, artifact recovery, deterministic regeneration, Source D regeneration, curl discovery, curl execution, network activity, replay, empirical artifact generation, full-universe work, P1/P2/P3 continuation, probe execution, price construction, price-store writes, scoring, wallet work, `OrdersMatched`, unrestricted `log_index`, PnL, live trading, paper trading, or gate change.

Standing state remains unchanged:

- named-binary P0 is accepted and `P0_CLEAR`;
- P1 remains blocked on the absence of an accepted per-side/token-identity decision-time price input;
- P2/P3 and probe execution remain unauthorized;
- `named_binary_probe_blocked = true`;
- accepted S1 Pass 1 remains `S1_SOURCE_NOT_VIABLE`;
- accepted S1-ALT remains `S1ALT_SOURCE_NOT_VIABLE`;
- this possible local-curl replay is bounded diagnostic transport-comparison evidence only and cannot unblock P1.

## 1. Objective, retained accepted architecture, and Revision 23 scope

The objective is to define a deterministic, bounded, auditable contract for a possible future local Windows system-`curl` replay of the exact accepted S1 Pass-1 sample. The replay would preserve separate histories for two token identities in exact `outcome_index` order and compare current local-curl condition-pair measurement states with accepted S1 Level-B states.

Revision 23 retains all accepted Revision 22 components not explicitly changed here:

1. Source B remains mandatory authority for the accepted 300-condition S1 population, the exact 52 invalid-window subset, the 248 prior measured states, previous Level-A/Level-B labels, accepted endpoint-shape evidence, and exact token identity/order.
2. Source D remains independently regenerated through an allowlisted loader and filesystem/network-free pure function, with outputs and detached provenance committed before Source B opens.
3. Fixed populations remain: 300 sampled conditions, 52 invalid-window conditions, 248 query-eligible conditions, 600 token rows, 496 request rows, execution ordinals exactly `0..495`, subclass denominators `UP_DOWN=50`, `OVER_UNDER=98`, `NAMED_OTHER=100`.
4. The retained Source D internal contract is Revision 17, SHA-256 `0b2e0a4120a2e8b8f983e820cef1762f6503412db6c2039f82dbf63ae7e07388`.
5. The retained Requests-equivalence internal contract is Revision 18, SHA-256 `a5558f1805de7b2fe8d25fe37b22295ccd33c022436e8014b1892f38d9db4947`.
6. The retained curl subprocess internal contract is Revision 20, SHA-256 `ee65157b2a5de50a3d91a0eb9dbef33a9b04c7f66d6bbad9f62be519442bede5`.
7. The retained response-header extraction contract is Revision 21, SHA-256 `b010e18ee1da53b37bc70aa37b5e92ab35593b259140300b69174020ca710460`.
8. The retained response-header vectors are Revision 21, SHA-256 `00cb6e9be633fce678ac091d37d0353ff94de6de585ff6b28c7c1d40427fb38b`.
9. The retained compatibility edge vectors are Revision 21, SHA-256 `1403c0c87d337fb66b48e8ac4d60699978a317757d828961665381775d0f71cc`.
10. HTTP/1.1 system-curl invocation, absent-Content-Type handling, canonical/strict dual analysis, valid interruption treatment, fixed denominators, threshold mathematics, all-one safeguards, detached snapshots, result ordering, and finalization profiles remain governing except where Revision 23 explicitly separates pre-run halts from run-scoped stops and adds HTTP status cross-evidence reconciliation.

Revision 23 retains the accepted Revision 22 corrections and additionally closes the following areas:

- makes the specification package byte-self-contained by embedding every retained contract and vector artifact;
- replaces the partial registry with one complete, closed schema and lifecycle registry for every persisted artifact;
- establishes a noncircular detached pre-run attachment semantic object before `run_id` exists;
- binds a detached governing-package manifest into fingerprint readiness, run identity, authorization, pre-V7 validation, and final inventories;
- namespaces INITIAL, CONTINUATION, and REQUEST_SPECIFIC authorizations under immutable per-authorization directories;
- adds positive-evidence reservation cancellation through `REQUEST_RESERVATION_CANCELLED_NO_START`;
- removes impossible result branches and causal language unsupported by a separate causal-proof contract; and
- synchronizes all schemas, artifacts, matrices, stops, results, tests, and hashes.
- materializes REV23 Amendment 03: the sole token manifest is V5 pre-run, request/plan schemas are closed, pre-run time is integer, partition identity is singular, and HTTP reconciliation is total.


### 1.1 Self-contained governing bytes

The Revision 23 archive contains byte-identical copies of all retained governing artifacts at these package paths:

```text
contracts/SOURCE_D_ALGORITHM_CONTRACT_REV17.json
contracts/REQUESTS_JSON_EQUIVALENCE_CONTRACT_REV18.json
contracts/CURL_SUBPROCESS_CONTRACT_REV20.json
contracts/RESPONSE_HEADER_EXTRACTION_CONTRACT_REV21.json
contracts/RESPONSE_HEADER_EXTRACTION_VECTORS_REV21.json
contracts/CANONICAL_COMPATIBILITY_EDGE_VECTORS_REV21.json
policies/URL_SERIALIZATION_POLICY_REV22.json
policies/TRANSPORT_POLICY_REV22.json
policies/HTTP_STATUS_RECONCILIATION_VECTORS_REV22.json
```

The Requests Revision-18 file embeds its accepted 20-vector corpus. No earlier package is required to recover governing bytes. `SHA256SUMS.txt` covers every archive member except itself, and the package hash report covers the ZIP and all members. Retained internal revision numbers remain 17, 18, 20, 21, and 22 as applicable; only new replay artifacts use `spec_revision=23`.

## 2. Non-objectives and prohibited behavior

No `yes_price`, `1-price`, `1-p`, complementary-side synthesis, winner-conditioned token derivation, canonical-side price construction, reusable price-series artifact, price-store write, scoring, PnL, wallet copying, wallet discovery, trading, full indexer, full-universe build, `OrdersMatched` expansion, unrestricted `log_index`, or gate change is permitted.

This specification does not establish a price source. It defines a falsification-minded diagnostic replay contract only.

## 3. Evidence families and fixed populations

### 3.1 Source B authority

Source B consists of accepted S1 artifacts:

1. by-condition CSV with exactly 300 unique condition IDs;
2. excluded CSV with exactly 52 unique invalid-window condition IDs;
3. endpoint-shape Markdown emitted by the canonical accepted S1 writer;
4. pinned accepted S1 implementation evidence.

The excluded IDs must be the exact 52-ID subset of the 300 by-condition IDs. Those rows normalize to `PREV_INVALID`; the remaining 248 normalize to `PREV_BOTH`, `PREV_ONE`, or `PREV_NEITHER`. Required overlap is valid. Duplicates, missing/extra overlap, reason/status conflicts, schema drift, or endpoint-shape contradiction stop before any request can be authorized.

### 3.2 Source D independence

The Source D allowlisted loader may read only pinned P0, classification contract, resolution source, and inventoried local-trade files. It returns immutable in-memory structures. The pure regeneration function has no filesystem, Source B/A/C, environment, subprocess, or network interface. Source D outputs and detached provenance commit before the first Source B byte opens. Source B absence or mutation cannot change Source D hashes.

### 3.3 Fixed counts and denominators

- oriented universe: 39,693;
- sample conditions: 300;
- invalid-window conditions: 52;
- query-eligible conditions: 248;
- token rows: 600;
- request rows: 496;
- execution ordinals: exactly every integer `0..495`, each once;
- subclass denominators: `UP_DOWN=50`, `OVER_UNDER=98`, `NAMED_OTHER=100`.

No transport, HTTP, parse, identity, interruption, strict-audit, missing-evidence, pre-run stop, run stop, or finalization state can change a denominator.

## 4. Source D regeneration contract

### 4.1 Exact P0 projection

The loader returns exactly this nested object:

```json
{
  "p0_state": "P0_CLEAR",
  "counts_pooled": {"final_p0_eligible": 39693},
  "nb_contract_version_expected": "nb-contract-2026-06-28.1",
  "nb_contract_version_contract": "nb-contract-2026-06-28.1",
  "nb_contract_version_resolution_source": "nb-contract-2026-06-28.1"
}
```

`p0_projection_semantic_sha256` is SHA-256 of canonical compact JSON with sorted keys, UTF-8 bytes, and no trailing LF. No flattened alias, missing field, extra field, coercion, or default is allowed.

### 4.2 Pinned sampling authority

Sampling authority is `rigolugo/pm_research` at Git commit OID `67af34d1e44504b8cde848b71117bd88de827e29`, Git blob OID `fbdb9adc25dd2cb3fb8b5657c06c2934dd203c64`, path `scripts/price_source_s1_coverage.py`, functions `time_bucket` and `build_pass1_sample`, constants sample size `300`, seed `20260628`, and subclass order `UP_DOWN`, `OVER_UNDER`, `NAMED_OTHER`.

A Git commit/blob OID is exactly 40 lowercase hexadecimal characters and is not SHA-256. File/inventory hashes are separately named 64-hex SHA-256 fields.

### 4.3 Ordered pure algorithm

1. Validate exact P0 projection, `P0_CLEAR`, count 39,693, and all three contract-version fields.
2. Validate contract records, exact version, unique condition IDs, bool/exact `True|False` eligibility, and retained oriented eligible subclasses.
3. Join retained `RESOLVED_SINGLE_WINNER` rows; reject duplicate retained IDs, version mismatch, subclass mismatch, or missing `resolved_at`; never use winner identity.
4. Preserve every local trade row and physical provenance ordinal; do not deduplicate.
5. Classify token/outcome as missing only for `None`, binary-float NaN, empty/whitespace, or case-insensitive textual `nan|none`. Every other value reaches canonical integer validation; precision loss stops.
6. For each valid row, insert the **original stripped token string** into the set for validated outcome index 0 or 1. Require exactly one original string per outcome. Only then compare selected side tokens numerically. Numeric equality is unresolved; otherwise emit original strings unchanged. Same-outcome `"1"/"01"` and `"1"/"1.0"` are unresolved by cardinality. Cross-side sole `"1"/"01"` is unresolved by numeric equality.
7. Derive first trade as the minimum pinned `parse_ts` result across every trade row in the condition, including token/outcome-malformed rows. Any `traded_at` parse failure stops.
8. Classify every condition as resolved or unresolved pair and require `resolved_pair_count + unresolved_pair_count = 39,693`. Stop only when `unresolved_pair_count * 5 > 39,693`.
9. Call pinned `time_bucket`. Any `resolved_at` parse failure maps to `UNKNOWN` and does not stop sample construction.
10. Call pinned `build_pass1_sample(resolved_conditions, 300, 20260628)` directly. Require 300 unique IDs and 100 per subclass.
11. Apply decision-window precedence: missing first trade; else missing/unparsable resolution; else nonpositive window; else eligible. Preserve exact nanosecond anchors independently. Integer request bounds are floor/ceil envelopes only.
12. Emit outcome 0 then outcome 1 for each selected condition, exactly 600 token rows. Filter query-eligible rows without reordering to exactly 496 request rows. Exactly 52 conditions and 104 token rows are invalid.
13. Commit Source D token/request outputs and detached provenance under the pre-run attempt before Source B opens.

The package artifact `SOURCE_D_ALGORITHM_CONTRACT_REV17.json` and runtime installed path `contracts/source_d_algorithm_contract.json` must be byte-identical. Their SHA-256 is `0b2e0a4120a2e8b8f983e820cef1762f6503412db6c2039f82dbf63ae7e07388`.

## 5. Source B schema and normalization

By-condition exact header:

```text
condition_id,subclass,side_0_token,side_1_token,level_a_side_0,level_a_side_1,condition_reachability,level_b_class,nearest_gap_side_0_seconds,nearest_gap_side_1_seconds,first_trade_ts,decision_lower_ts,resolved_at_ts,request_start_ts,request_end_ts,request_window_seconds,observed_point_count_side_0,observed_point_count_side_1
```

Excluded exact header:

```text
condition_id,subclass,reason
```

CSV is strict UTF-8 with optional BOM only at byte zero, comma delimiter, quote `"`, doubled quotes, no escape character, exact field counts, LF/CRLF preserved, and embedded newline only inside quoted fields. Persist raw header/row bytes, newline bytes, cell lexemes, and zero-based raw row ordinal before normalization.

Level-A domain is `SERIES_PRESENT`, `SERIES_EMPTY`, `SERIES_ERROR_TRANSIENT`, `SERIES_ERROR_NOTFOUND`, `SERIES_MALFORMED`, `NOT_QUERIED`. Reachability is `both`, `one`, `neither`, `n/a`. Level-B maps exactly: `BOTH -> PREV_BOTH`, `ONE -> PREV_ONE`, `NEITHER -> PREV_NEITHER`, `NO_VALID_DECISION_WINDOW_AFTER_WARMUP -> PREV_INVALID`.

Excluded reason grammar is exactly:

```regex
^NO_VALID_DECISION_WINDOW_AFTER_WARMUP \(first_trade_ts=(|-?[0-9]+), decision_lower_ts=(|-?[0-9]+), resolved_at_ts=(|-?[0-9]+), window_seconds=(|-?[0-9]+)\)$
```

Invalid reason precedence is missing first trade, missing resolution, nonpositive decision window. Embedded arithmetic must reconcile exactly.

Endpoint-shape parsing locates the observed `### Single-token GET` bullet block and accepts only the registered restricted flat Python-literal grammar. Path must be `/prices-history`, `interval` must be `max`, and fidelity inclusion/value comes only from accepted observed parameters. Missing, malformed, or contradictory endpoint evidence stops policy establishment.

## 6. Source B / Source D reconciliation

`reconciliation/source_b_source_d_reconciliation.parquet` has exactly 600 rows keyed `(condition_id, outcome_index)`. It compares membership, subclass, original token string, eligibility, emitted-second anchor projections, integer request window, invalid reason, and Source D row hash. Exact Source D nanoseconds remain linked through Source D row hashes. Every dimension is total and all 600 rows must be `RECONCILED`.

`reconciliation_logical_sha256` is the logical hash of destination-excluding reconciliation rows ordered by unsigned UTF-8 condition ID then numeric outcome index. `source_b_normalization_logical_sha256` hashes two typed component entries—300 condition rows then 52 excluded rows—in component ordinal order.

## 7. Typed rows, row hashes, logical hashes, and semantic identities

### 7.1 Typed row encoding

Storage types and logical hash tags are separate. The accepted non-null mapping remains `UINT8|UINT16|UINT32|UINT64 -> UINT`, signed integer storage -> `INT`, `UTC_NS -> UTC_NS`, and `STRING|BOOL|SHA256|STRING_LIST` to the same-named tag. Width-specific logical tags are forbidden.

Every null cell is exactly:

```json
{"n":"<field>","t":"NULL","v":null}
```

Null never retains a non-null tag. Canonical row JSON and logical relation hashing remain unchanged. Raw evidence Base64 is a logical `STRING`; decoded raw bytes are not Unicode-normalized.

The exact amended projections are:

#### Token-manifest row projection

| Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---|---|---|---|---|
| `schema_version` | `STRING` | `STRING` | forbidden | registered field contract |
| `spec_revision` | `UINT16` | `UINT` | forbidden | registered field contract |
| `condition_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `subclass` | `STRING` | `STRING` | forbidden | registered field contract |
| `outcome_index` | `UINT8` | `UINT` | forbidden | registered field contract |
| `token_id_lexeme` | `STRING` | `STRING` | forbidden | registered field contract |
| `query_eligible` | `BOOL` | `BOOL` | forbidden | registered field contract |
| `invalid_window_state` | `STRING` | `STRING` | forbidden | registered field contract |
| `invalid_window_reason` | `STRING` | `STRING` | `NULL` | registered field contract |
| `compatibility_first_trade_ts_float_hex` | `STRING` | `STRING` | `NULL` | registered field contract |
| `compatibility_decision_lower_ts_float_hex` | `STRING` | `STRING` | `NULL` | registered field contract |
| `compatibility_resolved_at_ts_float_hex` | `STRING` | `STRING` | `NULL` | registered field contract |
| `exact_first_trade_ts_ns` | `UTC_NS` | `UTC_NS` | `NULL` | registered field contract |
| `exact_decision_lower_ts_ns` | `UTC_NS` | `UTC_NS` | `NULL` | registered field contract |
| `exact_resolved_at_ts_ns` | `UTC_NS` | `UTC_NS` | `NULL` | registered field contract |
| `request_start_ts` | `INT64` | `INT` | `NULL` | registered field contract |
| `request_end_ts` | `INT64` | `INT` | `NULL` | registered field contract |
| `source_d_token_row_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `source_b_source_d_reconciliation_row_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |

#### Request-manifest row projection

| Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---|---|---|---|---|
| `schema_version` | `STRING` | `STRING` | forbidden | registered field contract |
| `spec_revision` | `UINT16` | `UINT` | forbidden | registered field contract |
| `request_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `execution_ordinal` | `UINT16` | `UINT` | forbidden | registered field contract |
| `condition_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `subclass` | `STRING` | `STRING` | forbidden | registered field contract |
| `outcome_index` | `UINT8` | `UINT` | forbidden | registered field contract |
| `token_id_lexeme` | `STRING` | `STRING` | forbidden | registered field contract |
| `compatibility_first_trade_ts_float_hex` | `STRING` | `STRING` | forbidden | registered field contract |
| `compatibility_decision_lower_ts_float_hex` | `STRING` | `STRING` | forbidden | registered field contract |
| `compatibility_resolved_at_ts_float_hex` | `STRING` | `STRING` | forbidden | registered field contract |
| `exact_first_trade_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | registered field contract |
| `exact_decision_lower_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | registered field contract |
| `exact_resolved_at_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | registered field contract |
| `request_start_ts` | `INT64` | `INT` | forbidden | registered field contract |
| `request_end_ts` | `INT64` | `INT` | forbidden | registered field contract |
| `token_manifest_row_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |

#### Request-plan row projection

| Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---|---|---|---|---|
| `schema_version` | `STRING` | `STRING` | forbidden | registered field contract |
| `spec_revision` | `UINT16` | `UINT` | forbidden | registered field contract |
| `request_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `execution_ordinal` | `UINT16` | `UINT` | forbidden | registered field contract |
| `condition_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `subclass` | `STRING` | `STRING` | forbidden | registered field contract |
| `outcome_index` | `UINT8` | `UINT` | forbidden | registered field contract |
| `token_id_lexeme` | `STRING` | `STRING` | forbidden | registered field contract |
| `compatibility_first_trade_ts_float_hex` | `STRING` | `STRING` | forbidden | registered field contract |
| `compatibility_decision_lower_ts_float_hex` | `STRING` | `STRING` | forbidden | registered field contract |
| `compatibility_resolved_at_ts_float_hex` | `STRING` | `STRING` | forbidden | registered field contract |
| `exact_decision_lower_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | registered field contract |
| `exact_resolved_at_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | registered field contract |
| `request_start_ts` | `INT64` | `INT` | forbidden | registered field contract |
| `request_end_ts` | `INT64` | `INT` | forbidden | registered field contract |
| `parameter_order` | `STRING_LIST` | `STRING_LIST` | forbidden | registered field contract |
| `conditional_fidelity_state` | `STRING` | `STRING` | forbidden | registered field contract |
| `exact_url` | `STRING` | `STRING` | forbidden | registered field contract |
| `exact_url_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `url_policy_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `transport_policy_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `subprocess_contract_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `request_manifest_row_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |

#### HTTP reconciliation row projection

| Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---|---|---|---|---|
| `schema_version` | `STRING` | `STRING` | forbidden | registered field contract |
| `spec_revision` | `UINT16` | `UINT` | forbidden | registered field contract |
| `run_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `authorization_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `request_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `execution_ordinal` | `UINT16` | `UINT` | forbidden | registered field contract |
| `attempt_number` | `UINT32` | `UINT` | forbidden | registered field contract |
| `reservation_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `capture_completed_event_row_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `write_out_stdout_raw_base64` | `STRING` | `STRING` | forbidden | registered field contract |
| `stdout_evidence_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `header_evidence_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| `write_out_http_code_lexeme` | `STRING` | `STRING` | `NULL` | registered field contract |
| `write_out_http_status_int` | `UINT16` | `UINT` | `NULL` | registered field contract |
| `write_out_http_code_state` | `STRING` | `STRING` | forbidden | registered field contract |
| `selected_header_status_state` | `STRING` | `STRING` | forbidden | registered field contract |
| `selected_header_status_int` | `UINT16` | `UINT` | `NULL` | registered field contract |
| `status_reconciliation_state` | `STRING` | `STRING` | forbidden | registered field contract |
| `issue_code` | `STRING` | `STRING` | `NULL` | registered field contract |

#### Partition-ID semantic projection

| Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---|---|---|---|---|
| `run_id` | `STRING` | `STRING` | forbidden | registered field contract |
| `audit_family` | `STRING` | `STRING` | forbidden | registered field contract |
| `partition_ordinal` | `UINT64` | `UINT` | forbidden | registered field contract |
| `row_count` | `UINT64` | `UINT` | forbidden | registered field contract |
| `first_key_canonical_json` | `STRING` | `STRING` | `NULL` | registered field contract |
| `last_key_canonical_json` | `STRING` | `STRING` | `NULL` | registered field contract |
| `partition_logical_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |

### 7.2 Identities and projections

- `request_id = "req_" + SHA256(typed condition_id, outcome_index, token_id_lexeme, exact_decision_lower_ts_ns, exact_resolved_at_ts_ns, request_start_ts, request_end_ts)`.
- `request_execution_order_sha256` hashes typed `(execution_ordinal, request_id)` rows ordered by `execution_ordinal`, one LF separator, no trailing LF. Ordinals are exactly `0..495`.
- `request_manifest_row_sha256` hashes all request-manifest fields excluding destination hashes.
- `request_plan_row_sha256` hashes all request-plan fields excluding destination hashes and must bind the equal request-manifest row hash.
- `fingerprint_semantic_sha256` hashes the closed fingerprint semantic object excluding itself, `run_id`, and destination hashes.
- `pre_run_attempt_id = "pra_" + SHA256(canonical compact sorted-key JSON of the exact five-field object `schema_version`, `spec_revision`, `attempt_kind`, `nonce_hex`, and integer `created_at_ns`)`. String, decimal, float, exponent, Boolean, or null `created_at_ns` is invalid.
- `run_id = "run_" + SHA256(canonical compact JSON of the exact twelve-field §8.5 projection, in this semantic field order: `schema_version`, `spec_revision`, `pre_run_nonce_hex`, `pre_run_created_at_ns`, `pre_run_attempt_id`, `detached_pre_run_attachment_semantic_sha256`, `governing_package_manifest_semantic_sha256`, `fingerprint_semantic_sha256`, `request_manifest_logical_sha256`, `request_plan_logical_sha256`, `request_execution_order_sha256`, and `initial_496_request_set_sha256`; sorted object keys, UTF-8, no trailing LF). The destination `run_id` is excluded.
- `reservation_id = "res_" + SHA256(typed run_id, authorization_id, authorization_record_file_sha256, authorized_request_set_file_sha256, request_id, execution_ordinal, attempt_number, request_plan_row_sha256)`.
- `partition_id = "part_" + SHA256(typed run_id, audit_family, partition_ordinal, row_count, first_key_canonical_json, last_key_canonical_json, partition_logical_sha256)`. This seven-field projection is sole and exact; `audit_family` is restricted to the partition-specific domain `capture|analysis_compatibility|analysis_strict`, not the broader global audit-family enum; audit rows do not contain partition ID.
- `stop_inventory_semantic_sha256` and `pre_run_stop_inventory_semantic_sha256` sort typed inventory entries by artifact-path UTF-8 bytes and exclude the inventory file, marker file, and destination semantic hash.
- `effective_argv_sha256` is defined in §11.4.
- `initial_496_request_set_sha256 = SHA256` of exactly 496 canonical typed `(execution_ordinal, request_id)` entries ordered by execution ordinal `0..495`, joined with one LF and no trailing LF.
- Authorization-specific request-set semantic and complete-file hashes are defined in §12.
- `authorization_use_event_row_sha256` is defined in §13.
- `http_status_reconciliation_row_sha256` is defined in §15.

Same identity with different semantic bytes is `STOP_SEMANTIC_ID_COLLISION`. Resume recomputes every identity.

## 8. Lifecycle: detached pre-run establishment, run identity, and finalization

### 8.1 Stage sequence and identity availability

The stage order is fixed:

```text
V0 pre-run identity and canonical-input inventory
V1 isolated Source D reconstruction and provenance
V2 Source B raw capture and normalization
V3 600-row Source B/Source D reconciliation
V4 32-field policy establishment
V5 token manifest, request manifest, request plan, plan hashes, and fingerprint readiness
V5A detached pre-run attachment semantic object
V5B detached governing-package manifest validation
V6 run-identity construction and run-scoped attachment persistence
V7 external authorization validation and request reservation
V8 capture and HTTP-status reconciliation
V9 compatibility/strict analysis, dispositions, pairs, comparison, thresholds, result
V10 stop or replay finalization
```

`pre_run_attempt_id` exists from V0. `run_id` does not exist and must be null in every V0–V5 stop artifact. No run-scoped destination path, authorization, reservation, capture, or run-finalization marker may be created before V6 succeeds.

### 8.2 Pre-run attempt identity

The semantic projection is the ordered closed object:

```json
{
  "schema_version":"local_curl_pre_run_attempt_identity.v23",
  "spec_revision":23,
  "attempt_kind":"LOCAL_CURL_PRE_RUN_ATTEMPT",
  "nonce_hex":"<64 lowercase hex>",
  "created_at_ns":0
}
```

`pre_run_attempt_id = "pra_" + SHA256(canonical compact sorted-key JSON bytes of that object)`. The identifier is excluded from its own semantic projection. Same ID with different semantic bytes is `STOP_PRE_RUN_ID_COLLISION`.

### 8.3 Detached pre-run attachment semantic object

After V0–V5 artifacts are committed and before `run_id` exists, produce exactly one:

```text
pre_run_attempts/<pre_run_attempt_id>/attachments/detached_pre_run_attachment_semantic.json
```

Its closed fields are:

```text
schema_version = local_curl_detached_pre_run_attachment_semantic.v23
spec_revision = 23
pre_run_attempt_id
entries[] ordered by (stage_ordinal, artifact_path unsigned UTF-8)
  stage = V0|V1|V2|V3|V4|V5
  stage_ordinal = 0..5
  artifact_path = pre-run-root-relative path only
  artifact_file_sha256
  artifact_logical_sha256 nullable only when the artifact has no registered logical hash
  artifact_schema_ref
entry_count
```

The semantic bytes are canonical compact JSON with sorted keys and no trailing LF. They include `pre_run_attempt_id` and every attached V0–V5 artifact path and complete file hash. They include logical hashes wherever the registry marks one required. They exclude `run_id`, all `runs/<run_id>/...` paths, the semantic hash destination field, file-hash sidecars, and all run-scoped destination hashes.

`detached_pre_run_attachment_semantic_sha256` is computed first from that projection and persisted in a separate sidecar object. Mutation, omission, duplicate path, extra path, ordering drift, or logical-hash mismatch is `STOP_DETACHED_PRE_RUN_ATTACHMENT_INVALID`.

### 8.4 Detached governing-package manifest

`GOVERNING_PACKAGE_MANIFEST_REV23.json` is package-level and detached from any run. It lists exact package-relative paths, roles, internal revisions where applicable, and complete file SHA-256 values for the governing specification, complete schema registry, request-plan/authorization contract, artifact registry, producer-consumer matrix, traceability matrix, stop table, result-label table, handoff, unresolved questions, change ledger, and every retained/new contract, policy, and vector artifact.

To avoid a hash cycle, the manifest excludes itself, its sidecar, `HASHES_REV23.json`, `SHA256SUMS.txt`, the ZIP, and ZIP sidecars. Its semantic projection excludes `governing_package_manifest_semantic_sha256`; the field is then populated with SHA-256 of canonical compact sorted-key JSON bytes of the projection. The complete manifest file has an independent SHA-256 sidecar.

The manifest semantic hash is required in fingerprint readiness, the fingerprint semantic object, run identity, every Gustavo authorization, pre-V7 validation, run-scoped attachment manifest, and every stop/replay final inventory. Revision number alone is never an authorization binding.

### 8.5 Run identity

The exact run-identity semantic object is:

```text
schema_version = local_curl_run_identity_semantic.v23
spec_revision = 23
pre_run_nonce_hex
pre_run_created_at_ns
pre_run_attempt_id
detached_pre_run_attachment_semantic_sha256
governing_package_manifest_semantic_sha256
fingerprint_semantic_sha256
request_manifest_logical_sha256
request_plan_logical_sha256
request_execution_order_sha256
initial_496_request_set_sha256
```

The field order above is semantic and explicit even though canonical JSON sorts keys. `run_id = "run_" + SHA256(canonical semantic bytes)`. `run_id` and destination hashes are excluded from the semantic object. Same `run_id` with different semantic bytes is `STOP_SEMANTIC_ID_COLLISION`.

After `run_id` is computed, persist:

```text
runs/<run_id>/identity/run_identity.json
runs/<run_id>/attachments/pre_run_attachment_manifest.json
```

The run-scoped attachment manifest references the already-computed detached attachment hash, the pre-run attempt ID, the package-manifest semantic hash, and exact pre-run source paths. It cannot alter or re-hash a different bound semantic object.

### 8.6 Pre-run and run finalization

A V0–V6-pre-identity failure emits a typed pre-run stop with `run_id=null`, zero requests guaranteed, and no run finalization profile. If its pre-run inventory commits atomically, it may emit `PRE_RUN_STOP_FINALIZED.json`; otherwise it emits only `PRE_RUN_STOP_FINALIZATION_FAILED.json` outside any finalized directory.

After V6, a structural stop may use the stop profile only if its stop envelope and inventory commit atomically. A replay result may use the replay profile only if structural prerequisites are valid and its replay inventory commits atomically. Atomicity unsupported or promotion failure leaves halted-unfinalized residue and no finalized marker. A post-finalization write is rejected and recorded only in the external operational audit ledger; the immutable run directory is not changed and the same `run_id` is never finalized twice.

## 9. Policy establishment and fingerprint

The registered policy set contains exactly 32 fields. `policy_resolution` contains exactly 32 rows keyed by `policy_field`; row-key set equals the registered field set. `validator_result` is string enum `VALID|INVALID`, never Boolean.

The policy-observation ledger contains exactly 68 rows: one row per `(policy_field, required evidence source)` pair registered in `policy_required_observations`. Presence states are `PRESENT_VALID`, `PRESENT_INVALID`, `ABSENT`, and `UNREADABLE`. `ABSENT` and `UNREADABLE` persist expected path but no fabricated file hash, byte size, locator, raw value, normalized value, or observed type.

For each resolution row:

1. `required_evidence_source_ids` equals the registered ordered source list exactly;
2. `observed_row_hashes` has the same length and order;
3. every hash resolves to the unique `PRESENT_VALID` observation row for that field/source pair;
4. `resolution_basis` equals the exact registered enum value `REVISION23_FIXED_TRANSPORT_AND_PACKAGE_CONTRACT`;
5. `resolution_state=RESOLVED`, `validator_result=VALID`, `defensive_default_used=false`, and resolved canonical JSON equals the frozen target-object value.

`policy_established=true` iff all conditions hold for all 32 rows and no contradiction group, invalid/unreadable/absent evidence, duplicate, omitted/extra source, omitted/extra hash, or frozen-object mismatch exists.

The run-policy fingerprint semantic projection contains exactly:

```json
{
  "component_hashes": "<closed component object>",
  "policy_established": true,
  "schema_version": "local_curl_run_policy_fingerprint.v23",
  "spec_revision": 23
}
```

It is canonical compact JSON with sorted keys, UTF-8, no trailing LF. `fingerprint_semantic_sha256`, `run_id`, and destination fields are excluded.

The closed component object requires:

```text
source_d_algorithm_contract_sha256 = 0b2e0a4120a2e8b8f983e820cef1762f6503412db6c2039f82dbf63ae7e07388
requests_json_equivalence_contract_file_sha256 = a5558f1805de7b2fe8d25fe37b22295ccd33c022436e8014b1892f38d9db4947
subprocess_contract_file_sha256 = ee65157b2a5de50a3d91a0eb9dbef33a9b04c7f66d6bbad9f62be519442bede5
response_header_extraction_contract_file_sha256 = b010e18ee1da53b37bc70aa37b5e92ab35593b259140300b69174020ca710460
response_header_extraction_vectors_file_sha256 = 00cb6e9be633fce678ac091d37d0353ff94de6de585ff6b28c7c1d40427fb38b
compatibility_edge_vectors_file_sha256 = 1403c0c87d337fb66b48e8ac4d60699978a317757d828961665381775d0f71cc
url_serialization_policy_file_sha256 = a148c2ac31e31c981bcafbb91e7416018a57796e6e41f7e522d2d249b5ad479a
transport_policy_file_sha256 = 78644908a852fba0dda2068b7b08a92c4b8a8a575fb2153876f9d478c5f1d2ca
http_status_reconciliation_vectors_file_sha256 = 65b937d9e85d589e6c06f2e50095731f2f537a07dc02758e484375c79254fb11
schema_registry_file_sha256 = bb5e03e91b26ecc14b6a3579b7118dc776caada3d988edaa1c342669e466bc22
```

Missing component, extra component, mutation, destination-field inclusion, or `run_id` inclusion is `STOP_FINGERPRINT_INVALID`.

## 10. Closed token-manifest, request-manifest, and request-plan contract

### 10.1 Sole V5 token manifest

The sole token manifest is `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_manifest/token_manifest.parquet`. `artifacts/local_curl_per_side/runs/<run_id>/request_manifest/token_manifest.parquet` is prohibited. There is no run-scoped copy, dual artifact, or deferred post-V6 validation. V5 commits the token manifest after V3 reconciliation and before the request manifest. V5A includes its exact path, complete-file hash, and logical hash before V6 computes the unchanged twelve-field `run_id`.

The token manifest is `local_curl_token_manifest.v23`, exactly 600 rows, exactly 300 conditions with outcome indices `{0,1}`, keyed and ordered by `(condition_id,outcome_index)`, and closed to exactly these fields in order:

```text
schema_version
spec_revision
condition_id
subclass
outcome_index
token_id_lexeme
query_eligible
invalid_window_state
invalid_window_reason
compatibility_first_trade_ts_float_hex
compatibility_decision_lower_ts_float_hex
compatibility_resolved_at_ts_float_hex
exact_first_trade_ts_ns
exact_decision_lower_ts_ns
exact_resolved_at_ts_ns
request_start_ts
request_end_ts
source_d_token_row_sha256
source_b_source_d_reconciliation_row_sha256
token_manifest_row_sha256
```

Each source hash resolves uniquely in the same pre-run attempt and recomputes from its registered destination-excluding projection. Both referenced rows have the same typed key, and the reconciliation row is `RECONCILED`. Query eligibility, invalid-window reason, exact/compatibility timestamps, and bounds derive only from accepted reconciliation and Source D evidence. Source presence alone cannot establish eligibility. `token_id_lexeme` is the exact original reconciled lexeme, including `.0`; winner-conditioned derivation is forbidden. Any path, count, key, provenance, typed-equality, conditional-nullability, row-hash, logical-hash, or complete-file-hash defect is `STOP_MANIFEST_COUNT_OR_HASH_INVALID` at V5 with zero requests guaranteed.

### 10.2 Request manifest

The request manifest is `local_curl_request_manifest.v23`, exactly 496 rows, with unique `request_id`, `execution_ordinal`, and `(condition_id,outcome_index)`. Ordinals are exactly `0..495`; the logical order is numeric execution ordinal. Its exact 18 fields are:

```text
schema_version
spec_revision
request_id
execution_ordinal
condition_id
subclass
outcome_index
token_id_lexeme
compatibility_first_trade_ts_float_hex
compatibility_decision_lower_ts_float_hex
compatibility_resolved_at_ts_float_hex
exact_first_trade_ts_ns
exact_decision_lower_ts_ns
exact_resolved_at_ts_ns
request_start_ts
request_end_ts
token_manifest_row_sha256
request_manifest_row_sha256
```

`token_id` is forbidden. Every row binds exactly one recomputed token-manifest row with `query_eligible=true`, `invalid_window_state=QUERY_ELIGIBLE`, and null invalid-window reason; fields copied from it are typed-equal. An unrelated eligible row hash is invalid. Request ID uses the registered seven-field typed identity. Rows are assigned ordinals after sorting by condition ID unsigned UTF-8, outcome index numeric, token lexeme unsigned UTF-8, then request ID unsigned UTF-8.

### 10.3 Exact URL serializer

The complete URL policy remains `URL_SERIALIZATION_POLICY_REV22.json`, SHA-256 `a148c2ac31e31c981bcafbb91e7416018a57796e6e41f7e522d2d249b5ad479a`. The `market` value is the exact `token_id_lexeme`; numeric normalization and `.0` removal are forbidden. Parameter order is exactly `market,startTs,endTs,interval` with conditional trailing `fidelity`. The existing byte-level percent-encoding, host, path, integer, interval, and no-trailing-byte rules remain unchanged.

### 10.4 Request plan

The request plan is `local_curl_request_plan.v23`, exactly 496 rows in execution-ordinal order, one-to-one with the request manifest. Its exact 24 fields are:

```text
schema_version
spec_revision
request_id
execution_ordinal
condition_id
subclass
outcome_index
token_id_lexeme
compatibility_first_trade_ts_float_hex
compatibility_decision_lower_ts_float_hex
compatibility_resolved_at_ts_float_hex
exact_decision_lower_ts_ns
exact_resolved_at_ts_ns
request_start_ts
request_end_ts
parameter_order
conditional_fidelity_state
exact_url
exact_url_sha256
url_policy_sha256
transport_policy_sha256
subprocess_contract_sha256
request_manifest_row_sha256
request_plan_row_sha256
```

The valid parameter vectors are exactly `["market","startTs","endTs","interval"]` and `["market","startTs","endTs","interval","fidelity"]`, paired respectively with `FIDELITY_OMITTED` and `FIDELITY_INCLUDED`. Every copied field is typed-equal to the matched manifest row; request and manifest hashes recompute. URL, policy, transport, and subprocess hashes are exact. Plan defects are `STOP_REQUEST_PLAN_INVALID`; ordering defects are `STOP_REQUEST_EXECUTION_ORDER_INVALID`.

## 11. Transport and effective argv binding

The retained curl subprocess contract is `CURL_SUBPROCESS_CONTRACT_REV20.json`, installed byte-identically at `policy/curl_subprocess_contract.json`, SHA-256 `ee65157b2a5de50a3d91a0eb9dbef33a9b04c7f66d6bbad9f62be519442bede5`. It contains the exact 19-element argv and protocol contract. Governing replay spec revision is 22; curl-contract internal revision remains 20.

`--disable` remains ordinal 1 and `--http1.1` remains ordinal 2. Authorized protocol is always `HTTP/1.1`.

### 11.1 Effective argv projection

For each capture STARTED event, after only the five registered dynamic-slot substitutions allowed by the curl subprocess contract, construct typed rows:

```text
(argv_ordinal:int, argv_value:string)
```

for every ordinal `0..18` in order. `argv_value` is the exact Unicode string passed to process creation after proxy-removal and path/URL substitution. Run-relative evidence paths use the canonical slash-separated relative path recorded in the capture event; the process-launch native path is separately recorded and not hashed into `effective_argv_sha256` unless the subprocess contract identifies it as a dynamic argv value.

`effective_argv_sha256 = SHA256(LF-join(canonical typed-row JSON bytes in ordinal order), no trailing LF)`. It must equal the STARTED row field and the reservation-bound expected hash. Any mismatch is `STOP_EFFECTIVE_ARGV_MISMATCH`.

## 12. Namespaced authorized request sets and authorization identity

### 12.1 Immutable paths

Every authorization uses a unique directory and never overwrites another authorization:

```text
authorization/records/<authorization_id>/authorization_record.json
authorization/records/<authorization_id>/authorization_record.sha256
authorization/records/<authorization_id>/authorized_request_set.json
authorization/records/<authorization_id>/authorized_request_set.sha256
```

INITIAL, CONTINUATION, and REQUEST_SPECIFIC authorizations may coexist for one `run_id`. All four files are immutable after creation.

### 12.2 Authorized request-set semantic projection

The request-set semantic projection is computed before `authorization_id` exists. It contains the following closed fields and excludes `authorization_id`, `authorized_request_set_semantic_sha256`, and every complete-file-hash destination:

```text
schema_version = local_curl_authorized_request_set.v23
spec_revision = 23
run_id
authorization_mode
request_plan_logical_sha256
request_execution_order_sha256
governing_package_manifest_semantic_sha256
source_d_algorithm_contract_file_sha256
requests_json_equivalence_contract_file_sha256
curl_subprocess_contract_file_sha256
response_header_extraction_contract_file_sha256
response_header_extraction_vectors_file_sha256
compatibility_edge_vectors_file_sha256
url_serialization_policy_file_sha256
transport_policy_file_sha256
http_status_reconciliation_vectors_file_sha256
entries[] ordered by execution_ordinal
authorized_request_entries_sha256
maximum_request_count
```

Each entry is exactly `(execution_ordinal:uint16, request_id:req_<sha256>)`. `authorized_request_set_semantic_sha256` hashes this canonical projection. Mode rules remain exact: INITIAL contains all 496 rows; CONTINUATION contains only positively proven no-start reservations or never-reserved never-started rows under a new external authorization; REQUEST_SPECIFIC contains exactly one prior-start request. `maximum_request_count` equals entry count and satisfies the mode cap.

### 12.3 Two-phase Gustavo authorization and request-set construction

The construction order is mandatory and noncircular:

1. Compute `authorized_request_set_semantic_sha256` from §12.2 with no `authorization_id`.
2. Compute `authorization_id = "auth_" + SHA256(canonical authorization-ID semantic bytes)`. That projection includes `authorized_request_set_semantic_sha256` and excludes `authorization_id`, `authorized_request_set_file_sha256`, `authorization_record_file_sha256`, and sidecar destination fields.
3. Persist `authorized_request_set.json` with the computed `authorization_id`; compute its independent complete-file SHA-256 and sidecar.
4. Persist the complete authorization record with `authorized_request_set_file_sha256` as a non-ID-projection field; compute the independent `authorization_record_file_sha256` sidecar.

Every authorization-use and capture row references both exact complete-file hashes. Cross-file mismatch, missing sidecar, path/ID mismatch, or same semantic ID with different semantic bytes stops before reservation.

## 13. Authorization-use lifecycle and reservation-before-start recovery

The append-only authorization-use relation is namespaced by `authorization_id` and ordered by contiguous `event_ordinal`. Its closed state domain is:

```text
ACTIVATED
REQUEST_RESERVED
REQUEST_START_CONFIRMED
REQUEST_START_AMBIGUOUS
REQUEST_TERMINAL_RECORDED
REQUEST_RESERVATION_CANCELLED_NO_START
EXPIRED_UNUSED
CLOSED
```

`REQUEST_RESERVATION_CANCELLED_NO_START` is terminal for one reservation. It is reachable only from `REQUEST_RESERVED`, never after a start-confirmed, start-ambiguous, or terminal event. It requires one immutable `capture_audit_snapshot_sha256` covering the complete reservation interval from reservation commit through cancellation commit and proving:

```text
capture_started_row_count = 0
terminal_capture_row_count = 0
process launch is durably permitted only after a committed STARTED capture row
reservation_irrevocably_closed = true
old_authorization_reservation_usable = false
cancellation_reason_code = POSITIVE_PROOF_NO_START
```

Missing, unreadable, partial, stale, interval-incomplete, or contradictory capture evidence is `RESERVATION_START_STATUS_UNPROVEN`; it is not proof of no start and does not make the request continuation-eligible.

Only after the cancellation event is finalized may a new, external Gustavo CONTINUATION authorization include that request. The old authorization can never reactivate or reuse the cancelled reservation. A cancelled reservation creates no capture attempt and does not alter request attempt numbering.

Other state rules remain strict: one ACTIVATED per authorization; one reservation tuple per `(authorization_id,request_id,attempt_number)`; START_CONFIRMED and START_AMBIGUOUS each bind `capture_start_event_row_sha256` to the exact matching committed STARTED capture row; TERMINAL_RECORDED binds both that STARTED row and `capture_terminal_event_row_sha256` to the exact matching INTERRUPTED or COMPLETED row. Authorization ID, authorization-record hash, authorized-request-set hash, reservation ID, request ID, execution ordinal, and attempt number must be identical across authorization-use and capture rows. EXPIRED_UNUSED applies only when no reservation exists; CLOSED is final. Every predecessor, multiplicity, field-presence, hash, and expiry rule is specified in the schema registry.

## 14. Capture attempts, selected attempts, and dispositions

### 14.1 Capture events

`capture_events` is a closed discriminated union on `capture_event_state`.

**STARTED** has ordinal 0 within an attempt. It is committed before process launch and contains authorization ID, authorization-record complete-file hash, authorized-request-set complete-file hash, reservation/fingerprint/request-plan references, the retained subprocess-contract hash, complete 19-element effective argv and `effective_argv_sha256`, exact URL hash, and proxy-removal list. Curl completion, exit, HTTP code, header/body/stderr evidence, oversize, and interruption fields are prohibited. `process_id` is nullable because immutable events are not backfilled.

**INTERRUPTED** has ordinal 1 and exactly one of `WRAPPER_TIMEOUT`, `RUNNER_EXCEPTION_AFTER_START`, or `LAUNCH_EXCEPTION_START_AMBIGUOUS`. Exit-code and HTTP-code evidence are absent. Wrapper-timeout and runner-exception require a process ID; launch-ambiguous requires it null. Each body/header/stderr evidence group is either fully absent or fully captured. Partial group evidence is malformed and triggers `STOP_CAPTURE_EVENT_SCHEMA_INVALID`.

**COMPLETED** has ordinal 1 and one of `EXIT_0`, `EXIT_28_TIMEOUT`, or `EXIT_OTHER_NONZERO`, with exact exit-code mapping. Body/header/stderr/stdout evidence is complete and hash-addressed. Exact stdout bytes are persisted as canonical RFC 4648 Base64 in `http_status_stdout_raw_base64` and included in the capture row hash. For every completion category, the bytes mechanically derive exactly one of `HTTP_CODE_000`, `HTTP_CODE_100_599`, or `HTTP_CODE_INVALID`; no completed category excludes malformed or out-of-range bytes. All nine completion-category × write-out-state pairs remain valid `COMPLETED` capture states long enough to persist exactly one HTTP reconciliation row. No compatibility or strict body analysis may occur before that row.

| Completion category | Exit code | Derived capture write-out state | Capture validity | Mandatory next step | Compatibility/strict body analysis before reconciliation |
|---|---:|---|---|---|---:|
| `EXIT_0` | `0` | `HTTP_CODE_000` | valid `COMPLETED` capture | persist reconciliation row → apply selected-header derivation and 12-cell table; no direct C02/C03 route | no |
| `EXIT_0` | `0` | `HTTP_CODE_100_599` | valid `COMPLETED` capture | persist reconciliation row → apply selected-header derivation and 12-cell table; no direct C07–C23 route | no |
| `EXIT_0` | `0` | `HTTP_CODE_INVALID` | valid `COMPLETED` capture | persist reconciliation row → `STOP_HTTP_WRITEOUT_INVALID`; no body analysis | no |
| `EXIT_28_TIMEOUT` | `28` | `HTTP_CODE_000` | valid `COMPLETED` capture | persist reconciliation row → apply selected-header derivation and 12-cell table; no direct C02/C03 route | no |
| `EXIT_28_TIMEOUT` | `28` | `HTTP_CODE_100_599` | valid `COMPLETED` capture | persist reconciliation row → apply selected-header derivation and 12-cell table; no direct C07–C23 route | no |
| `EXIT_28_TIMEOUT` | `28` | `HTTP_CODE_INVALID` | valid `COMPLETED` capture | persist reconciliation row → `STOP_HTTP_WRITEOUT_INVALID`; no body analysis | no |
| `EXIT_OTHER_NONZERO` | `nonzero !=28` | `HTTP_CODE_000` | valid `COMPLETED` capture | persist reconciliation row → apply selected-header derivation and 12-cell table; no direct C02/C03 route | no |
| `EXIT_OTHER_NONZERO` | `nonzero !=28` | `HTTP_CODE_100_599` | valid `COMPLETED` capture | persist reconciliation row → apply selected-header derivation and 12-cell table; no direct C07–C23 route | no |
| `EXIT_OTHER_NONZERO` | `nonzero !=28` | `HTTP_CODE_INVALID` | valid `COMPLETED` capture | persist reconciliation row → `STOP_HTTP_WRITEOUT_INVALID`; no body analysis | no |

`HTTP_CODE_INVALID` maps to reconciliation write-out state `INVALID`; after the required reconciliation row is persisted, it produces `STOP_HTTP_WRITEOUT_INVALID` before any compatibility or strict body analysis. `HTTP_CODE_000` and `HTTP_CODE_100_599` proceed only to selected-header derivation and the existing twelve-combination reconciliation table. The capture lifecycle never routes directly to C02, C03, or C07–C23.

Attempt numbers are contiguous `1..N`. Every attempt has one STARTED and zero or one terminal. Every capture state includes the exact `authorized_request_set_file_sha256`; it must equal the matching authorization-use row and authorization namespace. Duplicate/conflicting terminals, ordinal errors, authorization or request-set mismatches, partial evidence, hash failures, or unauthorized attempts are structural capture stops. Resume never overwrites an attempt; a new request-specific attempt is `max prior attempt + 1`.

### 14.2 Selected attempt and dispositions

Selection uses highest attempt N only and never falls back:

| Highest attempt | Disposition | Measurement | Strict state | Replay permitted | Closure stop |
|---|---|---|---|---:|---:|
| none | `NEVER_STARTED` | inconclusive | null | false | true |
| STARTED only | `STARTED_ONLY_UNRESOLVED` | inconclusive | null | false | true |
| valid INTERRUPTED plus matching C04/C05/C06 compatibility row | `INTERRUPTED_SELECTED` | inconclusive | `STRICT_NOT_EVALUATED_NONCOMPLETED` | true | false |
| COMPLETED lacking valid status reconciliation or analysis | `COMPLETED_UNANALYZED` | inconclusive | null | false | true |
| COMPLETED with valid status reconciliation and both analyses | `COMPLETED_ANALYZED_SELECTED` | compatibility result | strict result | true | false |

Valid interruption remains empirical unresolved evidence in the 496-token vector and fixed 248 pairs. It does not require request-specific replay before result evaluation. Never-started, started-only, and completed-unanalyzed remain `STOP_REQUEST_POPULATION_INCOMPLETE` closure states.

## 15. Write-out/header HTTP status reconciliation

Revision 23 adds an independent structural reconciliation before C14–C23 body processing.

Every selected `COMPLETED` capture requires this reconciliation regardless of curl completion category or derived write-out state. The lifecycle cannot route directly to C02, C03, or C07–C23. `HTTP_CODE_INVALID` is persisted through the reconciliation row and stops there; only non-invalid write-out evidence may reach the existing selected-header reconciliation and compatibility precedence.

### 15.1 Sole schema version and persisted row

The sole schema version is `local_curl_http_status_reconciliation.v23`. No `_row.v23` alias or any other value is accepted.

For every selected COMPLETED capture, persist one row in `analysis/http_status_reconciliation.parquet` with this exact field order:

```text
schema_version
spec_revision
run_id
authorization_id
request_id
execution_ordinal
attempt_number
reservation_id
capture_completed_event_row_sha256
write_out_stdout_raw_base64
stdout_evidence_sha256
header_evidence_sha256
write_out_http_code_lexeme
write_out_http_status_int
write_out_http_code_state
selected_header_status_state
selected_header_status_int
status_reconciliation_state
issue_code
http_status_reconciliation_row_sha256
```

`http_status_reconciliation_row_sha256` hashes every preceding field using the registered typed-cell projection. Nullable lexeme, integer, and issue fields use `t:"NULL",v:null` when null.

### 15.2 Write-out evidence derivation

`capture_completed_event_row_sha256` resolves uniquely to the selected COMPLETED capture. `write_out_stdout_raw_base64` equals its `http_status_stdout_raw_base64` exactly. It is canonical standard RFC 4648 Base64 with required padding; decode-then-reencode equality is mandatory. `stdout_evidence_sha256` is SHA-256 of the decoded bytes.

For decoded bytes `B`, apply exactly:

1. malformed length/content (`len(B) != 3` or any non-ASCII-digit byte) → lexeme null, `INVALID`, integer null;
2. `B == b"000"` → lexeme `"000"`, `VALID_000`, integer null;
3. three ASCII digits with decimal `100..599` → exact lexeme, `VALID_STATUS`, equal integer;
4. three ASCII digits in `001..099` or `600..999` → exact lexeme, `INVALID`, integer null.

The mapping is total and mutually exclusive for every byte sequence. Raw bytes, Base64, hash, lexeme, state, and integer are mechanically derived and cross-checked; independent caller assertions are forbidden.

Required rejection examples include `404` paired with integer `200`; `000` labeled `VALID_STATUS`; `200` labeled `VALID_000`; `999` labeled `VALID_STATUS`; two-byte, four-byte, non-digit, Unicode-digit, and non-ASCII evidence; and any lexeme/hash/integer inconsistent with registered bytes.

### 15.3 Selected-header derivation

`header_evidence_sha256` equals the selected COMPLETED capture's `header_sha256`, and the exact complete registered header bytes must recompute it. Run the retained response-header extraction contract at SHA-256 `b010e18ee1da53b37bc70aa37b5e92ab35593b259140300b69174020ca710460`. The persisted state/integer equals this ordered adapter output:

1. unavailable, oversize, truncated, unreadable, or hash-mismatched exact evidence → `HEADER_EVIDENCE_INVALID`, null;
2. parser `selected_http_status_code` non-null → `VALID_STATUS`, exact parser integer `100..599`;
3. null status plus `HEADER_NO_FINAL_RESPONSE_BLOCK` → `NO_SELECTED_FINAL_HEADER`, null;
4. null status plus `HEADER_STATUS_LINE_INVALID` → `INVALID_STATUS_LINE`, null;
5. other null-status parser output → `HEADER_EVIDENCE_INVALID`, null.

No independently supplied state or integer may override parser output.

### 15.4 Preserved total reconciliation rule

After both evidence derivations, apply the unchanged twelve Cartesian combinations and valid/valid subcases:

| Write-out | Header / integer subcase | Integer nullability and range | State | Issue | Structural stop | Permitted continuation | C14–C23 |
|---|---|---|---|---|---|---|---:|
| `INVALID` | `VALID_STATUS` | write null; header non-null `100..599` | `NOT_RECONCILABLE_STOP` | `HTTP_WRITEOUT_INVALID` | `STOP_HTTP_WRITEOUT_INVALID` | none | no |
| `INVALID` | `NO_SELECTED_FINAL_HEADER` | both null | `NOT_RECONCILABLE_STOP` | `HTTP_WRITEOUT_INVALID` | `STOP_HTTP_WRITEOUT_INVALID` | none | no |
| `INVALID` | `INVALID_STATUS_LINE` | both null | `NOT_RECONCILABLE_STOP` | `HTTP_WRITEOUT_INVALID` | `STOP_HTTP_WRITEOUT_INVALID` | none | no |
| `INVALID` | `HEADER_EVIDENCE_INVALID` | both null | `NOT_RECONCILABLE_STOP` | `HTTP_WRITEOUT_INVALID` | `STOP_HTTP_WRITEOUT_INVALID` | none | no |
| `VALID_STATUS` | `VALID_STATUS`, equal | both non-null `100..599`; equal | `RECONCILED` | null | none | `C14_C23_ELIGIBLE` | yes |
| `VALID_STATUS` | `VALID_STATUS`, `200/404` | both non-null `100..599` | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_200_HEADER_404` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_STATUS` | `VALID_STATUS`, `404/200` | both non-null `100..599` | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_404_HEADER_200` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_STATUS` | `VALID_STATUS`, other unequal | both non-null `100..599` | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_HEADER_UNEQUAL` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_STATUS` | `NO_SELECTED_FINAL_HEADER` | write non-null `100..599`; header null | `RECONCILED` | `NO_SELECTED_FINAL_HEADER` | none | `C01_C13_FRONT_END_ONLY` | no |
| `VALID_STATUS` | `INVALID_STATUS_LINE` | write non-null `100..599`; header null | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_VALID_HEADER_STATUS_INVALID` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_STATUS` | `HEADER_EVIDENCE_INVALID` | write non-null `100..599`; header null | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_VALID_HEADER_STATUS_INVALID` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_000` | `VALID_STATUS` | write null; header non-null `100..599` | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_000_HEADER_PRESENT` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_000` | `NO_SELECTED_FINAL_HEADER` | both null | `RECONCILED` | `NO_SELECTED_FINAL_HEADER` | none | `C01_C13_FRONT_END_ONLY` | no |
| `VALID_000` | `INVALID_STATUS_LINE` | both null | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_000_HEADER_EVIDENCE_INVALID` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |
| `VALID_000` | `HEADER_EVIDENCE_INVALID` | both null | `MISMATCH_STOP` | `HTTP_STATUS_WRITEOUT_000_HEADER_EVIDENCE_INVALID` | `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` | none | no |

Every unequal valid pair stops. Every derived `INVALID` branch first persists this reconciliation row and then triggers `STOP_HTTP_WRITEOUT_INVALID`; it cannot enter C01–C23. Only non-invalid write-out evidence reaches the remaining table cells. Only equal valid integers can reach C14–C23. No-selected-final-header branches remain restricted to C01–C13 front-end continuation. These rules apply identically to `EXIT_0`, `EXIT_28_TIMEOUT`, and `EXIT_OTHER_NONZERO`.

## 16. Canonical-S1 compatibility JSON adapter and analysis

The retained 20-vector Requests-equivalence corpus remains byte-identical at SHA-256 `a5558f1805de7b2fe8d25fe37b22295ccd33c022436e8014b1892f38d9db4947`. The retained response-header extraction contract/vector files remain byte-identical at SHA-256 `b010e18ee1da53b37bc70aa37b5e92ab35593b259140300b69174020ca710460` and `00cb6e9be633fce678ac091d37d0353ff94de6de585ff6b28c7c1d40427fb38b`.

Every compatibility row has `authorized_http_protocol=HTTP/1.1`. Observed selected protocol is separate and nullable.

- C01–C13: front-end transport/HTTP/header evidence branches. Header/protocol/adapter metadata may be not evaluated according to the branch.
- C14 valid unsupported metadata or malformed field after valid status line: adapter metadata structural-invalid or unsupported. Invalid-status-line runtime rows are defensive-unreachable after §15.
- C15: eligible metadata plus body UTF-8 failure.
- C16: UTF-8 success and JSON failure.
- C17–C20: decoded top-level/series/empty cases.
- C21: whole-series point-processing failure, including nonfinite price or Python `OverflowError`.
- C22/C23: complete valid nonempty series with positive/zero exact-window counts.

No partial malformed-point dropping is permitted. For finite timestamps, Python binary-float comparison uses `lower <= t < upper`. NAN/POS_INF/NEG_INF are outside the window and do not alone make a series malformed. Price must be finite.

`counts_by_branch` contains all C01–C23 keys and sums to 496 compatibility rows. C04–C06 are capture-derived interrupted rows. All other branches are completed rows that passed status reconciliation. `observed_http11_count` counts only rows with observed HTTP/1.1 selected line and need not equal 496.

## 17. Strict audit

Strict audit consumes raw captured bytes independently and never supplies transport-reproduction measurement states.

For each selected COMPLETED attempt that passed status reconciliation, strict audit applies S01–S12 in order: front-end evidence/HTTP states; strict UTF-8; duplicate-key-rejecting lexical JSON; top-level object; exactly one of `history|prices`; array shape; all-or-none point validation; exact timestamp nanoseconds; exact non-exponent Decimal price finite in `[0,1]`; point-level `token_id` identity with total echo precedence. No partial malformed-point prefix is committed.

For each `INTERRUPTED_SELECTED` request, no response-dependent strict row is fabricated. Its disposition carries `STRICT_NOT_EVALUATED_NONCOMPLETED`. Completed strict disagreement forces `strict_audit_replay_state=STRICT_AUDIT_INCONCLUSIVE`. Diagnostic deviation or interrupted non-evaluation alone cannot manufacture a transport-caused difference.

## 18. Request-to-side and condition-pair states

Every request receives one current side status:

```text
CURRENT_SIDE_BOTH_EVIDENCE_PRESENT
CURRENT_SIDE_SERIES_EMPTY
CURRENT_SIDE_ENDPOINT_ERROR
CURRENT_SIDE_MALFORMED
CURRENT_SIDE_IDENTITY_MISMATCH
CURRENT_SIDE_OVERSIZE
CURRENT_SIDE_INTERRUPTED
CURRENT_SIDE_INCONCLUSIVE
```

Only valid nonempty series with at least one exact-window point and valid identity can contribute to `CURRENT_SIDE_PRESENT`. Empty series, generic 404, parse defects, identity mismatch, oversize, non-200, interruption, and status-reconciliation defects cannot become negative absence.

Each query-eligible condition receives one pair state from its two side statuses:

```text
CURRENT_BOTH
CURRENT_ONE
CURRENT_NEITHER
CURRENT_MEASUREMENT_INCONCLUSIVE
```

`CURRENT_BOTH` requires both sides present. `CURRENT_ONE` requires exactly one side present and the other definitively empty under compatibility rules. `CURRENT_NEITHER` requires both sides definitively empty. Any endpoint, parse, identity, oversize, interruption, status-reconciliation, or strict-blocking uncertainty yields `CURRENT_MEASUREMENT_INCONCLUSIVE`.

## 19. Previous/current comparison mapping

Previous classes: `PREV_BOTH`, `PREV_ONE`, `PREV_NEITHER`, `PREV_INVALID`. Current classes: `CURRENT_BOTH`, `CURRENT_ONE`, `CURRENT_NEITHER`, `CURRENT_INVALID`, `CURRENT_MEASUREMENT_INCONCLUSIVE`.

The 4×5 mapping is total and mutually exclusive:

| Previous \ Current | BOTH | ONE | NEITHER | INVALID | INCONCLUSIVE |
|---|---|---|---|---|---|
| `PREV_BOTH` | `REPRODUCED_BOTH` | `CONFIRMED_DIFFERENCE_LOSS` | `CONFIRMED_DIFFERENCE_LOSS` | `SCHEMA_RECONCILIATION_STOP` | `COMPARISON_INCONCLUSIVE` |
| `PREV_ONE` | `CONFIRMED_DIFFERENCE_GAIN` | `REPRODUCED_ONE` | `CONFIRMED_DIFFERENCE_LOSS` | `SCHEMA_RECONCILIATION_STOP` | `COMPARISON_INCONCLUSIVE` |
| `PREV_NEITHER` | `CONFIRMED_DIFFERENCE_GAIN` | `CONFIRMED_DIFFERENCE_GAIN` | `REPRODUCED_NEITHER` | `SCHEMA_RECONCILIATION_STOP` | `COMPARISON_INCONCLUSIVE` |
| `PREV_INVALID` | `SCHEMA_RECONCILIATION_STOP` | `SCHEMA_RECONCILIATION_STOP` | `SCHEMA_RECONCILIATION_STOP` | `REPRODUCED_INVALID` | `SCHEMA_RECONCILIATION_STOP` |

The 52 invalid-window rows are never requested. If any requested row maps to `CURRENT_INVALID`, Source B/D or request-plan construction is defective and stops. Missing evidence cannot become a negative finding.

## 20. Threshold mathematics and all-one safeguards

For each subclass with fixed denominator `D`:

```text
confirmed_both_numerator = count(current pair state == CURRENT_BOTH for query-eligible rows in subclass)
unresolved_count = count(CURRENT_MEASUREMENT_INCONCLUSIVE for query-eligible rows in subclass)
lower_rate = confirmed_both_numerator / D
upper_rate = (confirmed_both_numerator + unresolved_count) / D
```

Threshold is 0.95 per subclass:

```text
if lower_rate >= 0.95 -> CLEARS_THRESHOLD
else if upper_rate < 0.95 -> FAILS_THRESHOLD
else -> THRESHOLD_INCONCLUSIVE
```

Before result labels, evaluate all-one safeguards:

1. if all 496 current side terminal states have one sole value, result is `LOCAL_CURL_REPLAY_INCONCLUSIVE`;
2. if all 248 current condition-pair states have one sole value, result is `LOCAL_CURL_REPLAY_INCONCLUSIVE`;
3. if any subclass threshold is `THRESHOLD_INCONCLUSIVE`, result is `LOCAL_CURL_REPLAY_INCONCLUSIVE`.

A below-threshold difference label is forbidden while any subclass remains threshold-inconclusive.

## 21. Ordered result-label logic

The labels are comparison statements against the pinned accepted-S1 compatibility target; they are not causal attributions. No label may use “transport-caused” unless a separately accepted causal-proof contract exists.

Evaluate exactly in this order:

1. Any finalized pre-run stop: emit the typed pre-run stop code only; no `run_id` result.
2. Any unfinalized pre-run or run finalization residue: `UNFINALIZED_OPERATIONAL_RESIDUE`; no empirical replay label.
3. Any run-scoped structural stop: emit the typed stop code only; no empirical replay label.
4. Any incomplete closure disposition (`NEVER_STARTED`, `STARTED_ONLY_UNRESOLVED`, `COMPLETED_UNANALYZED`, or unproven reservation status): `STOP_REQUEST_POPULATION_INCOMPLETE`.
5. All-one 496-token vector or all-one 248-pair vector: `LOCAL_CURL_REPLAY_INCONCLUSIVE`.
6. Any strict completed-response compatibility disagreement: `LOCAL_CURL_REPLAY_INCONCLUSIVE`.
7. Any subclass `THRESHOLD_INCONCLUSIVE`: `LOCAL_CURL_REPLAY_THRESHOLD_INCONCLUSIVE`.
8. Exact accepted-S1 negative reproduction: all 248 comparisons are exact, current subclass both-side numerators are exactly `19/50`, `51/98`, `65/100`, no unresolved pair exists, and all subclasses fail -> `LOCAL_CURL_REPLAY_REPRODUCES_S1_NEGATIVE`.
9. Confirmed differences while still below threshold: comparison is complete, at least one confirmed transition exists, no subclass is threshold-inconclusive, and at least one subclass fails -> `LOCAL_CURL_REPLAY_DIFFERS_FROM_S1_BELOW_THRESHOLD`.
10. Clear sample coverage versus the pinned compatibility target: all subclasses clear, comparison is complete, and every confirmed transition is a gain with no confirmed loss -> `LOCAL_CURL_REPLAY_SAMPLE_COVERAGE_CLEAR`.
11. Clear coverage with nonmonotone comparison differences: all subclasses clear, comparison is complete, and at least one confirmed loss exists alongside sufficient gains -> `LOCAL_CURL_REPLAY_COVERAGE_CLEAR_WITH_COMPARISON_DIFFERENCES`.
12. Otherwise -> `LOCAL_CURL_REPLAY_INCONCLUSIVE`.

These branches are reachable, ordered, mutually exclusive, and total over structurally valid replay evidence. Exact accepted-S1 reproduction necessarily reproduces the accepted below-threshold counts and can never enter a clear-threshold branch. Operational residue and structural stops are not empirical labels. No result authorizes P1, price construction, Pass 2, probe execution, or a gate change.

## 22. Artifact paths and registry summary

Package members are self-contained and listed in `GOVERNING_PACKAGE_MANIFEST_REV23.json` and `SHA256SUMS.txt`. Runtime artifact root remains:

```text
artifacts/local_curl_per_side/
```

Pre-run artifacts are rooted at `pre_run_attempts/<pre_run_attempt_id>/` and include identity, Source D tables/provenance, Source B raw/normalized evidence/provenance, 600-row reconciliation, policy observations/resolutions, 496-row manifest/plan, plan hashes, fingerprint readiness, detached attachment semantic object/sidecar, and pre-run stop artifacts.

Established runs are rooted at `runs/<run_id>/` and include identity, run-scoped attachment manifest, namespaced authorization records, authorization-use events, capture events, HTTP-status reconciliation, compatibility/strict analyses, 496 selected dispositions, 248 pair states, comparison/threshold summaries, result or stop state, inventories, and mutually exclusive finalization markers.

Authorization paths are exactly:

```text
runs/<run_id>/authorization/records/<authorization_id>/authorization_record.json
runs/<run_id>/authorization/records/<authorization_id>/authorization_record.sha256
runs/<run_id>/authorization/records/<authorization_id>/authorized_request_set.json
runs/<run_id>/authorization/records/<authorization_id>/authorized_request_set.sha256
```

The complete exact path, schema, producer, consumer, mutability, cardinality, ordering, snapshot, hash, and finalization contracts are in `SCHEMA_REGISTRY_REV23.json`, `ARTIFACT_REGISTRY_REV23.md`, and `ARTIFACT_PRODUCER_CONSUMER_MATRIX_REV23.md`. Every registered artifact has exactly one governing schema, exactly one producer, at least one consumer, and one noncontradictory lifecycle.

## 23. Resume, retry, duplicate handling, and immutability

Resume recomputes every file hash, row hash, logical hash, semantic identity, pre-run attachment hash, authorization request-set hash, and effective argv hash before continuing.

Duplicate attempts are allowed only by a separate valid authorization mode:

- continuation may target never-started rows and reservations finalized as `REQUEST_RESERVATION_CANCELLED_NO_START` only;
- request-specific replay may target exactly one eligible prior-start row;
- no replay may overwrite an existing attempt;
- `duplicate_group_id = "dup_" + SHA256(typed run_id, request_id, sorted attempt_numbers, reason_code)` binds related attempts.

A crash after STARTED but before terminal remains started-only unresolved and cannot be silently retried as never-started. Missing evidence can never be converted into `REQUEST_RESERVATION_CANCELLED_NO_START`. A crash after capture commitment resumes analysis without replaying the request.

## 24. Stop-state table

The complete stop table is in `STOP_STATE_TABLE_REV23.md`. Required highlights:

- V0–V5 failures are pre-run stops with `run_id=null`, zero requests guaranteed, no run finalization profile.
- V6 identity-construction failure is `STOP_RUN_ESTABLISHMENT_FAILED`, pre-run, zero requests guaranteed, no run finalization profile.
- V7+ structural failures are run-scoped stops and require run stop finalization if inventory succeeds.
- Stop-inventory construction failure leaves unfinalized residue and emits no final stop marker.
- `STOP_HTTP_STATUS_EVIDENCE_MISMATCH` occurs before C14–C23 and is run-scoped.
- `STOP_AUTHORIZATION_CAPTURE_RECONCILIATION_FAILED` occurs when authorization-use and capture event bindings diverge.
- `STOP_AUTHORIZED_REQUEST_SET_INVALID` occurs before request reservation and guarantees zero requests under that authorization.

## 25. Proposed acceptance tests

Acceptance tests are specification requirements only and are not authorized by this revision. The complete proposed suite includes:

1. Archive self-containment: every retained contract/vector path exists, bytes match its registered hash, and deletion of all earlier packages does not affect validation.
2. Governing package manifest: exact path/hash set, semantic recomputation, self-exclusion, extra/missing entry rejection, and complete-file sidecar validation.
3. Complete registry: every persisted artifact resolves to exactly one schema, producer, and nonempty consumer set; every schema has declared use; no unrestricted placeholder field exists.
4. V0–V5 stops have `run_id=null` and cannot create run-scoped paths.
5. Detached pre-run attachment: include every V0–V5 artifact exactly once; reject run paths, destination hashes, missing logical hashes, mutation, and ordering drift.
6. Run identity: recompute from the exact closed object; mutate each component independently; reject run-ID collision and run attachment mismatch.
7. URL serializer, request-manifest/plan equality, ordinals `0..495`, token lexical preservation, request bounds, URL/policy/subprocess hashes, and execution-order hash counterexamples.
8. Namespaced authorization: INITIAL, CONTINUATION, and REQUEST_SPECIFIC records coexist without overwrite; semantic ID, complete file hash, request-set semantic hash, request-set file hash, package/fingerprint/plan bindings, and all cross-file equalities are tested.
9. Reservation cancellation: positive zero-start evidence succeeds; missing capture snapshot, missing launch snapshot, partial interval, contradictory STARTED row, launch evidence, terminal evidence, or later old-authorization use fails.
10. Authorization-use/capture reconciliation: predecessor, multiplicity, reservation, attempt, hash, expiry, and terminal rules are total.
11. The sole HTTP reconciliation schema version is exactly `local_curl_http_status_reconciliation.v23` in the table, field domain, row-hash projection, and every proposed assertion; aliases fail.
12. Arbitrary stdout bytes map to exactly one write-out state, and raw Base64/hash/lexeme/state/integer inconsistency fails, including all registered counterexamples.
13. Selected-header state/integer equal the retained parser adapter output over exact registered header bytes; caller override fails.
14. All twelve reconciliation combinations remain total after evidence derivation, with unchanged outputs, stops, continuations, and C14–C23 reachability.
15. HTTP status reconciliation vectors and retained compatibility/strict vector corpora remain byte-identical and are proposed for exact execution only after separate authorization.
16. Selected attempt, valid interruption, disposition, fixed 496 token vector, 248 pair vector, threshold lower/upper bounds, and all-one safeguards reconcile.
17. Result-label tests prove exact S1 negative reproduction is below threshold; clear labels are unreachable from exact reproduction; gain-only clear and nonmonotone-clear branches are separately reachable; threshold-inconclusive precedes below-threshold differences.
18. Finalization atomicity, post-finalization external audit, no second finalization, and immutable detached snapshots are enforced.
19. Token-manifest lifecycle, exact 600-row provenance, exact 496-row request/plan membership, integer pre-run identity, storage/logical-tag separation, exact NULL encoding, the sole seven-field partition identity with only three partition families, all 12 HTTP outer cells and valid/valid subcases, and absence of the prohibited run-scoped token path are tested.
20. Complete non-authorization boundary remains present in the specification and Sentinel handoff.

## 26. Requirements traceability

The full matrix is `TRACEABILITY_MATRIX_REV23.md`. Every requirement maps to a spec section, schema/invariant, stop or decision rule, and proposed acceptance test.

## 27. Unresolved questions

None. Any later implementation ambiguity returns to Sentinel and Professor for a reviewed amendment. Professor cannot approve this specification, authorize implementation, or authorize execution.

## 28. Non-authorization statement

Specification revision only. Implementation is not authorized. Tests are not authorized. Prefetch is not authorized. Local reads and artifact recovery are not authorized. Deterministic regeneration and Source D regeneration are not authorized. Curl discovery is not authorized. Curl/network execution is not authorized. Replay is not authorized. Empirical artifact generation is not authorized. Full-universe work is not authorized. P1/P2/P3 continuation is not authorized. Probe execution is not authorized. Price construction, canonical-side price computation, side synthesis, `yes_price`, `1 - price`, `1 - p`, and price-store writes are not authorized. Scoring, wallet discovery, wallet copying, OrdersMatched expansion, unrestricted `log_index`, PnL, live trading, paper trading, and gate changes are not authorized. P1 remains blocked and `named_binary_probe_blocked` remains true.


# REV23 Finding 4 — effective snapshot/partition/cancellation amendment

The complete effective contract is the sibling governing file `REV23_SNAPSHOT_PARTITION_CANCELLATION_AMENDMENT.md`, complete-file SHA-256 `ffe8d209e3a5a7b8b0df1996f67172d781e0dd163a5d070501f1147eed5941d1`. It is incorporated by reference as a governing part of Revision 23 and supersedes only the snapshot, partition, capture-fence, reservation-cancellation proof, CONTINUATION freshness, Finding 4 inventory/finalization, and Amendment 03 I0 authorization-carry-forward clauses it expressly changes.

All token-manifest, 600/496/496 population, request, URL, HTTP, denominator, threshold, result-label, P1/P2/P3, probe, and gate behavior remains unchanged. No implementation authorization follows from this candidate.
