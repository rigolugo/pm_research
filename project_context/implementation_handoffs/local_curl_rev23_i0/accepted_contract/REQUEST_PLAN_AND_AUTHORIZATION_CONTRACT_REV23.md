# REQUEST-PLAN AND AUTHORIZATION CONTRACT — Revision 23

This companion is governing with `SPEC_local_curl_per_side_price_dataset_verification_REV23.md`. It is specification only and authorizes no implementation or execution.

## 1. Fixed V5 token, request-manifest, and request-plan contract

V5 uses one acyclic chain: committed V1 Source D token rows → committed V3 reconciliation → `artifacts/local_curl_per_side/pre_run_attempts/<pre_run_attempt_id>/request_manifest/token_manifest.parquet` (600 rows) → request manifest (496 rows) → request plan and hashes (496 rows). The prohibited path `artifacts/local_curl_per_side/runs/<run_id>/request_manifest/token_manifest.parquet` must not exist. No run-scoped copy or deferred validation is permitted.

The token manifest is keyed and ordered by `(condition_id,outcome_index)`, references exact recomputed Source D and reconciliation rows, requires `RECONCILED`, derives eligibility only from accepted reconciliation, and preserves the exact token lexeme including `.0`. The request manifest references one exact eligible token row and uses the 18-field `local_curl_request_manifest.v23` schema. The request plan uses the 24-field `local_curl_request_plan.v23` schema, binds the exact request-manifest row hash, includes the closed parameter-order/fidelity pair, and preserves token lexemes through exact URL serialization.

Both request relations contain exactly 496 rows. Request ordinals are exactly `0..495`; logical relation hashes use execution-ordinal order. Request IDs, row hashes, logical hashes, the URL-set hash, and execution-order hash all recompute from the registered typed projections.

## 2. Detached pre-run binding

Before a run exists, V0–V5 artifacts—including the relocated V5 token manifest, request manifest, request plan, plan hashes, and fingerprint readiness—are bound by `detached_pre_run_attachment_semantic_sha256`. The attachment object contains only pre-run-relative paths and complete file hashes plus required logical hashes. It excludes `run_id`, run destinations, its destination hash, and sidecar hashes.

`GOVERNING_PACKAGE_MANIFEST_REV23.json` independently binds the exact specification package bytes. Its semantic hash is required by fingerprint readiness, run identity, every authorization, pre-V7 validation, and final inventories.

## 3. Initial request-set hash used by run identity

The initial set is all 496 request-plan rows. `initial_496_request_set_sha256` is SHA-256 of exactly 496 canonical typed `(execution_ordinal, request_id)` entries ordered by execution ordinal `0..495`, joined with one LF and no trailing LF. It contains no authorization mode, `authorization_id`, or `run_id`. After run establishment, the Gustavo INITIAL authorization must contain the identical ordered entries and recompute the identical entry-set hash.

## 4. Per-authorization immutable namespace

For every authorization:

```text
runs/<run_id>/authorization/records/<authorization_id>/authorization_record.json
runs/<run_id>/authorization/records/<authorization_id>/authorization_record.sha256
runs/<run_id>/authorization/records/<authorization_id>/authorized_request_set.json
runs/<run_id>/authorization/records/<authorization_id>/authorized_request_set.sha256
```

No path may be reused. The directory name must equal the record’s semantic authorization ID. Initial, continuation, and request-specific authorizations coexist.

## 5. Request-set object and hashes

The request-set schema is closed. Its semantic projection includes `spec_revision=23`, run ID, mode, request-plan logical hash, execution-order hash, governing-package manifest semantic hash, every retained/policy contract file hash, exact ordered entries, entry-set hash, and maximum request count. It excludes `authorization_id`, its semantic-hash destination, and complete-file-hash destinations.

After the request-set semantic hash and `authorization_id` are computed, the stored request-set file includes the authorization ID. The complete JSON file then receives an independent file SHA-256 sidecar. Every authorization-use and capture row includes the exact request-set complete-file hash.

Mode rules:

| Mode | Exact request set | Count |
|---|---|---:|
| `INITIAL_REPLAY` | all 496 frozen plan rows | 496 |
| `CONTINUATION_REPLAY` | never-started or positively cancelled-no-start rows only | 1..496 |
| `REQUEST_SPECIFIC_REPLAY` | exactly one prior-start request | 1 |

## 6. Authorization semantic ID and complete-file hash

The two-phase construction order is exact:

1. Compute the request-set semantic hash without `authorization_id`.
2. Compute the external Gustavo `authorization_id` from the closed authorization-ID semantic projection. That projection includes `authorized_request_set_semantic_sha256` and excludes `authorization_id`, `authorized_request_set_file_sha256`, the complete authorization-file hash, and sidecar destinations.
3. Store the request-set file with the computed authorization ID and compute its complete-file SHA-256.
4. Store that request-set complete-file hash in the authorization record as a non-ID-projection field, then compute `authorization_record.sha256`.

The implementation may validate but may not create, edit, repair, or replace Gustavo’s record.

## 7. Reservation state machine and positive cancellation proof

The authorization-use event states are `ACTIVATED`, `REQUEST_RESERVED`, `REQUEST_START_CONFIRMED`, `REQUEST_START_AMBIGUOUS`, `REQUEST_TERMINAL_RECORDED`, `REQUEST_RESERVATION_CANCELLED_NO_START`, `EXPIRED_UNUSED`, and `CLOSED`. Their exact predecessors and required/prohibited fields are closed in the schema patch. START_CONFIRMED and START_AMBIGUOUS bind the exact matching STARTED capture-row hash; TERMINAL_RECORDED binds both that STARTED row and the exact matching terminal-row hash. All authorization, reservation, request, ordinal, attempt, authorization-record-hash, and request-set-hash values must match across use and capture rows.

Cancellation from `REQUEST_RESERVED` binds one immutable capture-audit snapshot covering the complete reservation interval and proving zero matching STARTED rows and zero matching terminal rows. The durable launch rule is that process launch occurs only after a committed STARTED row. Cancellation also requires irreversible reservation closure and an explicit old-authorization unusable flag. Missing, stale, partial, interval-incomplete, or contradictory evidence is `RESERVATION_START_STATUS_UNPROVEN` and is not continuation eligibility.

## 8. Cross-file invariants

1. Directory authorization ID, record authorization ID, stored request-set authorization ID, and all use/capture references are equal; the request-set semantic projection itself excludes authorization ID.
2. Run ID, request-plan logical hash, execution-order hash, governing-package hash, fingerprint hash, and every contract hash are equal across the run identity, fingerprint readiness, authorization record, request set, pre-V7 metadata, and final inventory.
3. Request-set semantic hash is computed first without authorization ID; authorization ID is computed second without request-set complete-file hash; stored request-set file hash is computed third; authorization complete-file hash is computed last. All hashes recompute independently.
4. Authorization records and request sets are immutable and never overwritten.
5. No reservation can start before ACTIVATED and REQUEST_RESERVED rows commit.
6. A cancelled reservation can never later produce a STARTED or terminal row under the old authorization.
7. Missing evidence never becomes negative proof or a false continuation unblock.


# REV23 Finding 4 authorization supersession boundary


If Sentinel accepts and the Finding 4 candidate is canonically installed, every existing Amendment 03 I0 implementation/source-sync authorization, source gate, prompt, and derived inventory is superseded and inactive. No implementation authorization carries forward implicitly. A later implementation stage requires a new explicit Gustavo authorization pinned to the then-current canonical commit and complete governing hashes. This candidate itself authorizes no implementation, source synchronization, tests, execution, network, replay, empirical work, downstream phase, or gate change.
