# REV23_AMENDMENT_03 — I0 Conformance and Token-Manifest Lifecycle

**Status:** `SPECIFICATION_COMPLETE — STATIC EFFECTIVE-FILE MATERIALIZATION COMPLETE FOR SENTINEL REVIEW`  
**Submission route:** Professor → Sentinel.  
**Canonical repository:** `rigolugo/pm_research`.  
**Pinned canonical commit:** `226085ca9ba7fa41a8b666005499827d6fa6b9c5`.  
**Effective baseline:** materialized `accepted_contract/` at the pinned commit, representing Revision 23 with Amendments 01 and 02 applied.

## 0. Authority boundary

This is a specification revision only. It authorizes no implementation, tests, local research-data reads, artifact recovery, deterministic regeneration, project-code execution, curl, subprocess launch, network request, replay, empirical artifact production, full-universe build, price construction, canonical-side price construction, side synthesis, price-store write, P1/P2/P3 continuation, probe execution, scoring, wallet work, OrdersMatched expansion, unrestricted `log_index`, PnL, live trading, paper trading, wallet copying, or gate change.

The standing project state remains unchanged: P0 is accepted and `P0_CLEAR`; P1 remains blocked; P2/P3 and probe execution remain unauthorized; `named_binary_probe_blocked = true`.

## 1. Objective and non-objectives

### 1.1 Objective

Amend only the following effective Revision 23 defects:

1. conflicting `partition_id` projections;
2. conflicting request-manifest schemas;
3. conflicting request-plan schemas;
4. string-versus-integer ambiguity in `pre_run_attempt_id.created_at_ns`;
5. incomplete HTTP write-out/header reconciliation;
6. the accepted token-manifest lifecycle contradiction, resolved only by relocating the sole token manifest to V5 pre-run scope.

### 1.2 Non-objectives

This amendment does not change Source B authority, Source D algorithms, Source B/Source D reconciliation semantics, fixed populations, denominators, thresholds, authorization modes, authorization authority, authorization-use lifecycle, capture lifecycle except mechanical references, compatibility analysis, strict analysis, pair mapping, result-label ordering, finalization, resume semantics, retry semantics, P1/P2/P3 state, probe authorization, or any guardrail.

## 2. Normative precedence

After Sentinel acceptance, this amendment supersedes only conflicting effective Revision 23 text and schema records within its stated scope.

The following are non-governing and forbidden:

- the old run-scoped token-manifest path;
- a dual token-manifest design;
- deferred token-manifest validation after V6;
- the six-input `partition_id` shorthand containing `partition_count`, `key_range`, or unqualified `logical_hash`;
- request fields named `token_id`;
- request-manifest or request-plan ordering by `request_id`;
- a string, decimal, float, or exponent-valued pre-run `created_at_ns`;
- any unhandled combination of registered HTTP write-out and selected-header states.

## 3. Typed-cell encoding

Storage types and logical hash tags are separate contracts. Every row-hash or semantic-hash projection uses an ordered JSON array. A non-null cell is exactly:

```json
{"n":"<field_name>","t":"<registered non-null logical tag>","v":<logical value>}
```

The only authorized non-null mappings for amended projections are:

| Storage type | Exact non-null `t` |
|---|---|
| `UINT8`, `UINT16`, `UINT32`, `UINT64` | `UINT` |
| `INT64` | `INT` |
| `UTC_NS` | `UTC_NS` |
| `STRING` | `STRING` |
| `BOOL` | `BOOL` |
| `SHA256` | `SHA256` |
| `STRING_LIST` | `STRING_LIST` |

Width-specific logical tags such as `UINT8`, `UINT16`, `UINT32`, `UINT64`, or `INT64` are forbidden. They remain storage-type names only.

Every null cell, regardless of its field's storage type or non-null logical tag, is exactly:

```json
{"n":"<field>","t":"NULL","v":null}
```

A null value carrying the field's non-null tag is invalid. A non-null value carrying `NULL` is invalid. Non-null fields cannot emit a null cell.

Canonical row JSON uses UTF-8, sorted object keys, compact separators, NFC logical strings, no NaN or infinity, and no trailing LF. Destination hashes are excluded. A logical relation hash orders destination-excluding row bytes by its registered ordering, joins adjacent rows with one byte LF, appends no trailing LF, and computes SHA-256. An empty relation hashes the empty byte string.

## 4. Accepted lifecycle correction

The sole token-manifest artifact is relocated to:

```text
artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_manifest/token_manifest.parquet
```

The old path is prohibited and must be absent from the artifact catalog, artifact registry, schema usage, producer-consumer matrix, traceability matrix, detached attachment rules, and all consumers:

```text
artifacts/local_curl_per_side/runs/<run_id>/request_manifest/token_manifest.parquet
```

The fixed order is:

1. V1 commits `source_d_token_rows.parquet`;
2. V3 commits the 600-row Source B/Source D reconciliation;
3. V5 commits the 600-row token manifest;
4. V5 commits the 496-row request manifest;
5. V5 commits the request plan and request-plan hashes;
6. V5A includes the token manifest and all other registered V0–V5 artifacts;
7. V6 computes the unchanged twelve-field `run_id`.

No run-scoped destination is read or written before V6. No run-scoped token-manifest copy exists. The token manifest is bound into `run_id` noncircularly through the existing detached pre-run attachment semantic hash and through the request-manifest/request-plan hashes already present in the unchanged run-identity projection.

## 5. Closed token-manifest contract

### 5.1 Identity, cardinality, key, and ordering

```text
schema_version = local_curl_token_manifest.v23
artifact = pre_run_attempts/<pre_run_attempt_id>/request_manifest/token_manifest.parquet
cardinality = exactly 600 rows
primary key = (condition_id, outcome_index)
ordering = condition_id unsigned UTF-8 bytes, then outcome_index numeric
additional fields = forbidden
```

There are exactly 300 distinct condition IDs. Every condition has exactly two rows with outcome indices exactly `{0,1}`.

### 5.2 Exact field order, storage types, logical tags, and nullability

| # | Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---:|---|---|---|---|---|
| 1 | `schema_version` | `STRING` | `STRING` | forbidden | `local_curl_token_manifest.v23` |
| 2 | `spec_revision` | `UINT16` | `UINT` | forbidden | `23` |
| 3 | `condition_id` | `STRING` | `STRING` | forbidden | `^0x[0-9a-f]{64}$` |
| 4 | `subclass` | `STRING` | `STRING` | forbidden | registered oriented subclass |
| 5 | `outcome_index` | `UINT8` | `UINT` | forbidden | `0|1` |
| 6 | `token_id_lexeme` | `STRING` | `STRING` | forbidden | exact original reconciled lexeme |
| 7 | `query_eligible` | `BOOL` | `BOOL` | forbidden | accepted reconciliation only |
| 8 | `invalid_window_state` | `STRING` | `STRING` | forbidden | `QUERY_ELIGIBLE|INVALID_WINDOW` |
| 9 | `invalid_window_reason` | `STRING` | `STRING` | `NULL` | null iff eligible |
| 10 | `compatibility_first_trade_ts_float_hex` | `STRING` | `STRING` | `NULL` | copies evidence exactly |
| 11 | `compatibility_decision_lower_ts_float_hex` | `STRING` | `STRING` | `NULL` | copies evidence exactly |
| 12 | `compatibility_resolved_at_ts_float_hex` | `STRING` | `STRING` | `NULL` | copies evidence exactly |
| 13 | `exact_first_trade_ts_ns` | `UTC_NS` | `UTC_NS` | `NULL` | copies Source D exactly |
| 14 | `exact_decision_lower_ts_ns` | `UTC_NS` | `UTC_NS` | `NULL` | copies Source D exactly |
| 15 | `exact_resolved_at_ts_ns` | `UTC_NS` | `UTC_NS` | `NULL` | copies Source D exactly |
| 16 | `request_start_ts` | `INT64` | `INT` | `NULL` | non-null only when eligible |
| 17 | `request_end_ts` | `INT64` | `INT` | `NULL` | non-null only when eligible |
| 18 | `source_d_token_row_sha256` | `SHA256` | `SHA256` | forbidden | recomputed exact source row |
| 19 | `source_b_source_d_reconciliation_row_sha256` | `SHA256` | `SHA256` | forbidden | recomputed exact reconciliation row |
| 20 | `token_manifest_row_sha256` | `SHA256` | `SHA256` | forbidden | destination; excluded from own projection |

For `query_eligible=true`, `invalid_window_state=QUERY_ELIGIBLE`, `invalid_window_reason=null`, all three compatibility timestamps, all three exact timestamps, and both request bounds are non-null; bounds satisfy `0 <= request_start_ts < request_end_ts <= 253402300799`.

For `query_eligible=false`, `invalid_window_state=INVALID_WINDOW`, `invalid_window_reason` is the exact accepted reconciliation reason, and both request bounds are null. Missing evidence is never converted to eligibility. Other nullable timestamps copy the source/reconciliation null exactly; no default or fabrication is permitted. Every such null is encoded with `t:"NULL"` and `v:null`.

### 5.3 Provenance and equality

For each token-manifest row:

1. `source_d_token_row_sha256` resolves to exactly one row in the same pre-run attempt's `source_d_token_rows.parquet`;
2. that Source D row hash recomputes from its registered destination-excluding projection;
3. `source_b_source_d_reconciliation_row_sha256` resolves to exactly one row in the same pre-run attempt's 600-row reconciliation;
4. that reconciliation row hash recomputes;
5. both referenced rows have the same typed `(condition_id,outcome_index)` key;
6. the reconciliation state is exactly `RECONCILED`;
7. every copied field is typed-equal to both governing source values wherever both carry the field;
8. `token_id_lexeme` is the exact reconciled original lexeme, including any retained `.0`;
9. query eligibility, invalid-window state/reason, compatibility timestamps, exact timestamps, and request bounds are the accepted reconciliation outputs;
10. winner identity, labels, resolution winner, price, or outcome-conditioned derivation never enters this artifact.

A correct hash that identifies an unrelated source or reconciliation row fails.

### 5.4 Hashes and lifecycle

`token_manifest_row_sha256` hashes fields 1–19 in exact order.  
`token_manifest_logical_sha256` orders by `(condition_id,outcome_index)` and hashes the exact destination-excluding row bytes.  
The complete Parquet file has an independent SHA-256 of stored bytes.

Producer: `V5 token-manifest builder`.  
Consumers: `V5 request-manifest builder`, `V5A detached attachment builder`, `V6 run-identity validator`, `authorization validator`, `Sentinel`.

Any path, cardinality, key-set, ordering, source-row, reconciliation-row, equality, eligibility, nullability, row-hash, logical-hash, or complete-file-hash defect triggers `STOP_MANIFEST_COUNT_OR_HASH_INVALID` at V5 with zero requests guaranteed.

Counterexamples that must fail include: old run-scoped path; 599/601 rows; one-sided condition; duplicate key; `.0` removal; source hash from another row; reconciliation hash from another row; unrecomputed source hash; eligible despite invalid reconciliation; invalid row with fabricated bounds; eligible row with null bound; winner-derived token; logical ordering by request ID.

## 6. Closed request-manifest contract

### 6.1 Cardinality, key, and order

```text
schema_version = local_curl_request_manifest.v23
cardinality = exactly 496
primary key = request_id
uniqueness = request_id; execution_ordinal; (condition_id,outcome_index)
ordinal set = exactly 0..495
additional fields = forbidden
```

### 6.2 Exact fields, storage types, and logical tags

| # | Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---:|---|---|---|---|---|
| 1 | `schema_version` | `STRING` | `STRING` | forbidden | `local_curl_request_manifest.v23` |
| 2 | `spec_revision` | `UINT16` | `UINT` | forbidden | `23` |
| 3 | `request_id` | `STRING` | `STRING` | forbidden | `^req_[0-9a-f]{64}$` |
| 4 | `execution_ordinal` | `UINT16` | `UINT` | forbidden | `0..495` |
| 5 | `condition_id` | `STRING` | `STRING` | forbidden | exact token-manifest value |
| 6 | `subclass` | `STRING` | `STRING` | forbidden | exact token-manifest value |
| 7 | `outcome_index` | `UINT8` | `UINT` | forbidden | `0|1` |
| 8 | `token_id_lexeme` | `STRING` | `STRING` | forbidden | exact token-manifest lexeme |
| 9 | `compatibility_first_trade_ts_float_hex` | `STRING` | `STRING` | forbidden | exact token-manifest value |
| 10 | `compatibility_decision_lower_ts_float_hex` | `STRING` | `STRING` | forbidden | exact token-manifest value |
| 11 | `compatibility_resolved_at_ts_float_hex` | `STRING` | `STRING` | forbidden | exact token-manifest value |
| 12 | `exact_first_trade_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | exact token-manifest value |
| 13 | `exact_decision_lower_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | exact token-manifest value |
| 14 | `exact_resolved_at_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | exact token-manifest value |
| 15 | `request_start_ts` | `INT64` | `INT` | forbidden | exact token-manifest value |
| 16 | `request_end_ts` | `INT64` | `INT` | forbidden | exact token-manifest value |
| 17 | `token_manifest_row_sha256` | `SHA256` | `SHA256` | forbidden | recomputed referenced row |
| 18 | `request_manifest_row_sha256` | `SHA256` | `SHA256` | forbidden | destination; excluded from own projection |

`token_id` is forbidden. Every request-manifest field is non-null; a `NULL` cell is therefore invalid.

### 6.3 Provenance and identities

Every row references one and only one token-manifest row whose hash recomputes, whose `query_eligible=true`, whose `invalid_window_state=QUERY_ELIGIBLE`, and whose `invalid_window_reason=null`.

Fields 5–16 are typed-equal to the referenced token row. A hash belonging to any unrelated eligible row is rejected.

Request ID is recomputed as:

```text
"req_" + SHA256(typed condition_id,
                typed outcome_index,
                typed token_id_lexeme,
                typed exact_decision_lower_ts_ns,
                typed exact_resolved_at_ts_ns,
                typed request_start_ts,
                typed request_end_ts)
```

All 496 rows are sorted by condition ID unsigned UTF-8, outcome index numeric, token lexeme unsigned UTF-8, then request ID unsigned UTF-8; ordinals 0–495 are assigned in that order.

`request_manifest_row_sha256` hashes fields 1–17.  
`request_manifest_logical_sha256` orders rows by numeric execution ordinal 0–495.  
Any defect triggers `STOP_MANIFEST_COUNT_OR_HASH_INVALID`; order/ordinal/order-hash defects additionally map to `STOP_REQUEST_EXECUTION_ORDER_INVALID`.

## 7. Closed request-plan contract

### 7.1 Cardinality and membership

```text
schema_version = local_curl_request_plan.v23
cardinality = exactly 496
primary key = request_id
membership = exact one-to-one request-manifest membership
ordinal set = exactly 0..495
additional fields = forbidden
```

### 7.2 Exact fields, storage types, and logical tags

| # | Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---:|---|---|---|---|---|
| 1 | `schema_version` | `STRING` | `STRING` | forbidden | `local_curl_request_plan.v23` |
| 2 | `spec_revision` | `UINT16` | `UINT` | forbidden | `23` |
| 3 | `request_id` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 4 | `execution_ordinal` | `UINT16` | `UINT` | forbidden | exact manifest value |
| 5 | `condition_id` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 6 | `subclass` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 7 | `outcome_index` | `UINT8` | `UINT` | forbidden | exact closed request-plan field |
| 8 | `token_id_lexeme` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 9 | `compatibility_first_trade_ts_float_hex` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 10 | `compatibility_decision_lower_ts_float_hex` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 11 | `compatibility_resolved_at_ts_float_hex` | `STRING` | `STRING` | forbidden | exact closed request-plan field |
| 12 | `exact_decision_lower_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | exact closed request-plan field |
| 13 | `exact_resolved_at_ts_ns` | `UTC_NS` | `UTC_NS` | forbidden | exact closed request-plan field |
| 14 | `request_start_ts` | `INT64` | `INT` | forbidden | exact closed request-plan field |
| 15 | `request_end_ts` | `INT64` | `INT` | forbidden | exact closed request-plan field |
| 16 | `parameter_order` | `STRING_LIST` | `STRING_LIST` | forbidden | exact four- or five-key ordered vector |
| 17 | `conditional_fidelity_state` | `STRING` | `STRING` | forbidden | `FIDELITY_INCLUDED|FIDELITY_OMITTED` |
| 18 | `exact_url` | `STRING` | `STRING` | forbidden | exact retained serializer output |
| 19 | `exact_url_sha256` | `SHA256` | `SHA256` | forbidden | exact closed request-plan field |
| 20 | `url_policy_sha256` | `SHA256` | `SHA256` | forbidden | exact closed request-plan field |
| 21 | `transport_policy_sha256` | `SHA256` | `SHA256` | forbidden | exact closed request-plan field |
| 22 | `subprocess_contract_sha256` | `SHA256` | `SHA256` | forbidden | exact closed request-plan field |
| 23 | `request_manifest_row_sha256` | `SHA256` | `SHA256` | forbidden | recomputed matched row |
| 24 | `request_plan_row_sha256` | `SHA256` | `SHA256` | forbidden | destination; excluded from own projection |

The valid parameter vectors are exactly:

```json
["market","startTs","endTs","interval"]
```

```json
["market","startTs","endTs","interval","fidelity"]
```

`FIDELITY_OMITTED` requires the first; `FIDELITY_INCLUDED` requires the second. The retained URL policy is unchanged. `.0` token lexemes are preserved exactly. No alias, numeric coercion, fallback, normalization, width-specific logical tag, or null cell is permitted.

Every plan field copied from the manifest is typed-equal; the manifest row hash and request ID recompute. URL, policy, transport, and subprocess hashes recompute or match their exact governing bytes.

`request_plan_row_sha256` hashes fields 1–23.  
`request_plan_logical_sha256` orders by execution ordinal.  
`request_plan_url_set_sha256` hashes typed `(execution_ordinal,request_id,exact_url_sha256)` entries.  
`request_execution_order_sha256` hashes typed `(execution_ordinal,request_id)` entries.

Defects trigger `STOP_REQUEST_PLAN_INVALID`; execution-order defects trigger `STOP_REQUEST_EXECUTION_ORDER_INVALID`.

## 8. Pre-run identity

The sole governing semantic object has exactly five fields:

| Field | JSON type | Exact requirement |
|---|---|---|
| `schema_version` | string | `local_curl_pre_run_attempt_identity.v23` |
| `spec_revision` | integer | `23` |
| `attempt_kind` | string | `LOCAL_CURL_PRE_RUN_ATTEMPT` |
| `nonce_hex` | string | exactly 64 lowercase hexadecimal characters |
| `created_at_ns` | integer | signed UTC nanoseconds |

Canonical bytes are compact sorted-key UTF-8 JSON with no trailing LF. `pre_run_attempt_id` is excluded:

```text
pre_run_attempt_id = "pra_" + lowercase_hex(SHA256(canonical semantic bytes))
```

A string, decimal, float, exponent, Boolean, or null `created_at_ns` is invalid.

## 9. Partition identity and snapshot binding

### 9.1 Sole governing identity

```text
schema_id = local_curl_snapshot_partition_identity.v23
prefix = part_
audit_family domain = capture|analysis_compatibility|analysis_strict
```

The broader global `audit_family` enum remains available only to non-partition audit objects. It is not a valid domain reference for `partition_id`.

Exact projection:

| # | Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---:|---|---|---|---|---|
| 1 | `run_id` | `STRING` | `STRING` | forbidden | non-null |
| 2 | `audit_family` | `STRING` | `STRING` | forbidden | exact `enum:partition_audit_family` |
| 3 | `partition_ordinal` | `UINT64` | `UINT` | forbidden | non-null |
| 4 | `row_count` | `UINT64` | `UINT` | forbidden | non-null |
| 5 | `first_key_canonical_json` | `STRING` | `STRING` | `NULL` | null iff empty |
| 6 | `last_key_canonical_json` | `STRING` | `STRING` | `NULL` | null iff empty |
| 7 | `partition_logical_sha256` | `SHA256` | `SHA256` | forbidden | non-null |

```text
partition_id = "part_" + lowercase_hex(SHA256(exact typed-row bytes))
```

Excluded: partition ID, path, size, complete-file hash, snapshot row hash, containing snapshot hash, and all destinations.

For nonempty partitions, first key must not sort after last key. For empty partitions, both keys are null and each is encoded with `t:"NULL",v:null`; the logical hash is SHA-256 of empty bytes.

### 9.2 Required evidence reconciliation

The persisted snapshot-partition entry and containing audit snapshot must reconcile:

- exact `run_id`;
- exact audit family derived from the containing snapshot path and manifest;
- exact partition ordinal;
- actual relation row count;
- actual first and last keys under the registered partition key;
- independently recomputed partition logical hash;
- exact partition ID recomputation;
- exact path, size, and complete-file SHA-256;
- unique ordinal and no overlapping or inverted key ranges;
- containing snapshot partition-entry logical hash and count.

A shorthand or alternate projection is forbidden. Any defect maps to the family-specific snapshot stop and, for projection defects, `STOP_ROW_HASH_PROJECTION_INVALID` or `STOP_SEMANTIC_ID_COLLISION`.

## 10. Total HTTP status reconciliation

### 10.1 One governing schema version and exact fields

The sole governing schema version is:

```text
local_curl_http_status_reconciliation.v23
```

That exact value appears in the table schema, `schema_version` field domain, HTTP row-hash projection `schema_id`, effective specification, traceability, and proposed assertions. The deprecated `_row` spelling is forbidden. There is no alias or dual acceptance.

| # | Field | Storage type | Non-null `t` | Null `t` | Constraint |
|---:|---|---|---|---|---|
| 1 | `schema_version` | `STRING` | `STRING` | forbidden | exact `local_curl_http_status_reconciliation.v23` only |
| 2 | `spec_revision` | `UINT16` | `UINT` | forbidden | registered field contract |
| 3 | `run_id` | `STRING` | `STRING` | forbidden | registered field contract |
| 4 | `authorization_id` | `STRING` | `STRING` | forbidden | registered field contract |
| 5 | `request_id` | `STRING` | `STRING` | forbidden | registered field contract |
| 6 | `execution_ordinal` | `UINT16` | `UINT` | forbidden | registered field contract |
| 7 | `attempt_number` | `UINT32` | `UINT` | forbidden | registered field contract |
| 8 | `reservation_id` | `STRING` | `STRING` | forbidden | registered field contract |
| 9 | `capture_completed_event_row_sha256` | `SHA256` | `SHA256` | forbidden | registered field contract |
| 10 | `write_out_stdout_raw_base64` | `STRING` | `STRING` | forbidden | canonical RFC 4648 Base64 of exact stdout bytes; non-null |
| 11 | `stdout_evidence_sha256` | `SHA256` | `SHA256` | forbidden | SHA-256 of decoded raw stdout bytes |
| 12 | `header_evidence_sha256` | `SHA256` | `SHA256` | forbidden | equals bound capture header SHA-256 |
| 13 | `write_out_http_code_lexeme` | `STRING` | `STRING` | `NULL` | exact ASCII decode iff raw bytes are three ASCII digits; otherwise null |
| 14 | `write_out_http_status_int` | `UINT16` | `UINT` | `NULL` | decimal lexeme only for `VALID_STATUS`; otherwise null |
| 15 | `write_out_http_code_state` | `STRING` | `STRING` | forbidden | mechanically derived `VALID_STATUS|VALID_000|INVALID` |
| 16 | `selected_header_status_state` | `STRING` | `STRING` | forbidden | mechanically derived from retained header parser |
| 17 | `selected_header_status_int` | `UINT16` | `UINT` | `NULL` | parser integer for `VALID_STATUS`; otherwise null |
| 18 | `status_reconciliation_state` | `STRING` | `STRING` | forbidden | registered field contract |
| 19 | `issue_code` | `STRING` | `STRING` | `NULL` | registered field contract |
| 20 | `http_status_reconciliation_row_sha256` | `SHA256` | `SHA256` | forbidden | destination; excluded from own projection |

### 10.2 Exact persisted raw stdout representation

Every selected COMPLETED capture persists its exact stdout bytes as canonical RFC 4648 Base64 in `http_status_stdout_raw_base64`. The reconciliation row copies that exact Base64 lexeme into `write_out_stdout_raw_base64`; decode-then-reencode must reproduce the stored lexeme exactly. Empty bytes are represented by the empty Base64 string. `stdout_evidence_sha256` is the lowercase SHA-256 of the decoded bytes. Both fields are row-hash-bound.

Let `B` be the decoded raw bytes. Derive the remaining fields in this exact order:

1. If `len(B) != 3` or any byte is outside ASCII `0x30..0x39`, set lexeme null, state `INVALID`, and integer null.
2. If `B == b"000"`, set lexeme `"000"`, state `VALID_000`, and integer null.
3. If `B` is exactly three ASCII digits and its decimal value is `100..599`, set the lexeme to the exact ASCII decoding, state `VALID_STATUS`, and integer to that decimal value.
4. Otherwise `B` is a three-ASCII-digit value in `001..099` or `600..999`; preserve its exact lexeme, set state `INVALID`, and integer null.

These ordered cases are total and mutually exclusive over every finite byte sequence. Raw bytes, Base64 lexeme, stdout hash, write-out lexeme, state, and integer are mechanically reconciled outputs. None may be trusted as an independent caller assertion. Malformed evidence is never replaced by normalized text.

Counterexamples:

- `WRITE_404_INT_200`: raw Base64 `NDA0`, supplied lexeme `404`, state `VALID_STATUS`, integer `200` — reject because integer must equal decimal lexeme and registered raw bytes.
- `WRITE_000_LABELED_VALID_STATUS`: raw Base64 `MDAw`, supplied lexeme `000`, state `VALID_STATUS`, integer `None` — reject because 000 maps only to VALID_000.
- `WRITE_200_LABELED_VALID_000`: raw Base64 `MjAw`, supplied lexeme `200`, state `VALID_000`, integer `None` — reject because 200 maps only to VALID_STATUS with integer 200.
- `WRITE_999_LABELED_VALID_STATUS`: raw Base64 `OTk5`, supplied lexeme `999`, state `VALID_STATUS`, integer `999` — reject because three-digit out-of-range evidence maps to INVALID with null integer.
- `WRITE_TWO_BYTES`: raw Base64 `MjA=`, supplied lexeme `020`, state `VALID_STATUS`, integer `20` — reject because two raw bytes map to INVALID with null lexeme and integer.
- `WRITE_FOUR_BYTES`: raw Base64 `MjAwMA==`, supplied lexeme `200`, state `VALID_STATUS`, integer `200` — reject because four raw bytes map to INVALID with null lexeme and integer.
- `WRITE_NONDIGIT_ASCII`: raw Base64 `Mk8w`, supplied lexeme `200`, state `VALID_STATUS`, integer `200` — reject because ASCII letter O makes the evidence malformed; expected lexeme and integer are null.
- `WRITE_UNICODE_DIGITS`: raw Base64 `2aLZoNmg`, supplied lexeme `200`, state `VALID_STATUS`, integer `200` — reject because Unicode digits are not three ASCII digit bytes; expected lexeme and integer are null.
- `WRITE_NONASCII_BYTES`: raw Base64 `/wCA`, supplied lexeme `000`, state `VALID_000`, integer `None` — reject because non-ASCII bytes map to INVALID with null lexeme and integer.
- `WRITE_REGISTERED_BYTES_LEXEME_MISMATCH`: raw Base64 `NDA0`, supplied lexeme `200`, state `VALID_STATUS`, integer `200` — reject because lexeme must be decoded from registered bytes without normalization.

### 10.3 Selected-header parser binding

`capture_completed_event_row_sha256` resolves uniquely to the selected COMPLETED capture. `header_evidence_sha256` equals that row's `header_sha256`; the exact complete registered header bytes must hash to it. The retained response-header extraction contract is fixed at SHA-256 `b010e18ee1da53b37bc70aa37b5e92ab35593b259140300b69174020ca710460` with retained vectors SHA-256 `00cb6e9be633fce678ac091d37d0353ff94de6de585ff6b28c7c1d40427fb38b`.

Apply this exact ordered adapter to the retained parser output:

1. Missing, unreadable, oversize, truncated, or hash-mismatched registered header evidence → `HEADER_EVIDENCE_INVALID`, integer null.
2. Non-null parser `selected_http_status_code` → `VALID_STATUS`, integer exactly that parser value in `100..599`.
3. Null parser status with `HEADER_NO_FINAL_RESPONSE_BLOCK` → `NO_SELECTED_FINAL_HEADER`, integer null.
4. Null parser status with `HEADER_STATUS_LINE_INVALID` → `INVALID_STATUS_LINE`, integer null.
5. Any remaining null-status parser output → `HEADER_EVIDENCE_INVALID`, integer null.

The persisted selected-header state and integer must equal this adapter output. Caller-supplied state or integer cannot override parser output.

### 10.4 Preserved twelve-combination reconciliation table

Evidence derivation occurs first. The already accepted twelve Cartesian write-out/header combinations then apply without change; no wildcard is valid. `VALID_STATUS/VALID_STATUS` retains four exhaustive integer subcases.

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

Only equal valid integers can reach C14–C23. No-selected-final-header branches remain limited to C01–C13 front-end continuation. All other branches stop exactly as previously materialized.

### 10.5 Completed-capture lifecycle closure

The lifecycle contract is total over the exact Cartesian product of three curl completion categories and three mechanically derived capture write-out states. Exact stdout bytes are always persisted as canonical Base64 and hash-bound before classification.

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

Every one of the nine pairs requires exactly one HTTP reconciliation row. `HTTP_CODE_INVALID` remains a validly represented `COMPLETED` capture state through that row, maps to reconciliation state `INVALID`, and then produces `STOP_HTTP_WRITEOUT_INVALID` before compatibility or strict body analysis. `HTTP_CODE_000` and `HTTP_CODE_100_599` may proceed only to the retained selected-header derivation and the unchanged twelve-combination table. No completed lifecycle summary may route directly to C02, C03, or C07–C23.

## 11. Static acyclicity proof

The provenance graph is:

```text
V1 source_d_token_row
      \
       -> V3 reconciliation -> V5 token_manifest -> V5 request_manifest
      /                                             -> V5 request_plan/hashes
V2 Source B normalized row                           -> V5A detached attachment
                                                       -> V6 run_id
```

All edges point from an earlier committed stage to a later stage. No node requires `run_id` before V6. The token-manifest path contains only `pre_run_attempt_id`. V5A includes its complete-file and logical hashes. The unchanged V6 projection consumes the detached attachment hash plus request-manifest/request-plan/order hashes. No edge returns to V1–V5. The graph is acyclic.

## 12. Required governing-file synchronization

The following effective files require target-byte updates:

- `SPEC_local_curl_per_side_price_dataset_verification_REV23.md`;
- `SCHEMA_REGISTRY_REV23.json`;
- `REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md`;
- `ARTIFACT_REGISTRY_REV23.md`;
- `ARTIFACT_PRODUCER_CONSUMER_MATRIX_REV23.md`;
- `TRACEABILITY_MATRIX_REV23.md`;
- `STOP_STATE_TABLE_REV23.md`;
- `CHANGE_LEDGER_REV22_to_REV23.md`;
- `UNRESOLVED_QUESTIONS_REV23.md`;
- `GOVERNING_PACKAGE_MANIFEST_REV23.json`;
- `GOVERNING_PACKAGE_MANIFEST_REV23.sha256`;
- `ACCEPTED_CONTRACT_SHA256SUMS.txt`.

`RESULT_LABEL_DECISION_TABLE_REV23.md` is mechanically unchanged because every new HTTP branch is a structural stop before result labeling and no result-label order changes.

## 13. Proposed conformance tests — not authorized to execute

Tests must cover positive and counterexample cases for:

- 600-row token manifest, exact 300×2 key set, path, ordering, hashes, and V5A inclusion;
- unrelated but valid source/reconciliation hash rejection;
- false eligibility rejection;
- `.0` preservation through token, request, plan, and URL;
- exact 496 request membership and 0–495 ordinals;
- request and plan row/logical/order hash recomputation;
- integer pre-run `created_at_ns` and rejection of every other JSON type;
- all three and only three partition families, nonempty/empty partitions, `NULL` key encoding, actual/snapshot reconciliation, and alternate-projection rejection;
- all 12 HTTP state combinations with exact required-null/non-null fields and ranges, plus all four valid/valid integer subcases, including generic unequal pairs absent from retained vectors;
- absence of the old run-scoped token-manifest path in all materialized governing files;
- storage-to-logical-tag closure for every amended projection and rejection of width-specific tags;
- exact `{"n":"<field>","t":"NULL","v":null}` encoding for every nullable amended field;
- reconstruction of every target byte from its designated unified diff, complete replacement, or RFC 6902 plus canonical serialization.
- exact sole HTTP reconciliation schema version `local_curl_http_status_reconciliation.v23` and rejection of every alias;
- total raw-stdout classification over arbitrary bytes, including exact three-byte, out-of-range, malformed-length, non-digit, Unicode-digit, and non-ASCII counterexamples;
- exact equality among registered stdout bytes, canonical Base64, stdout SHA-256, nullable lexeme, derived state, and derived integer;
- exact selected-header state/integer equality with the retained parser adapter over hash-verified registered header bytes;
- preservation of all twelve reconciliation outer combinations after evidence derivation;
- preserved prior handoff as an exact prefix with no stale governing HTTP alternative.

Specification acceptance does not authorize test authoring or execution.

## 14. Preserved state and authorization boundary

Source B and Source D rules, populations, denominators, thresholds, authorization authority, capture semantics, compatibility/strict branches, result ordering, finalization, P1/P2/P3 state, probe authorization, and project guardrails remain unchanged.

This amendment is specification revision only. It authorizes no implementation, tests, local reads, artifact recovery, deterministic regeneration, network/curl execution, empirical run, full-universe build, downstream phase, or gate change.
