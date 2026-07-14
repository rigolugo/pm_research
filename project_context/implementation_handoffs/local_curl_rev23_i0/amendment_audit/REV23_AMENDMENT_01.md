# REV23_AMENDMENT_01

**Baseline package:** `local_curl_per_side_dataset_verification_REV23_package.zip`  
**Frozen baseline ZIP SHA-256:** `87f2335d5ee9762f03d665136ef6d330554495a39bd10856a6385f1e3d8b1b93`  
**Scope:** specification-only amendment against the exact submitted Revision 23 package. This is not Revision 24 and is not a replacement package.

## 1. Governing amendment files

Apply the two unified diffs and the RFC 6902 JSON Patch to the three exact baseline files named by the patch artifacts. No other Revision 23 file is modified.

## 2. Corrections

### A. Stale Revision 22 definitions removed

The specification now uses `spec_revision=23` for pre-run identity, the exact twelve-field §8.5 run-identity projection, fingerprint schema `local_curl_run_policy_fingerprint.v23`, fingerprint revision 23, policy basis `REVISION23_FIXED_TRANSPORT_AND_PACKAGE_CONTRACT`, and baseline schema-registry SHA-256 `54b03b63dd65be462591e63ab3308153c10cc9de5c75e56f564612efe3f7cfcd`. The redundant artifact-registry fingerprint-component line is removed.

### B. Identity and hash projections unified

`semantic_hashes.run_id` is identical to `run_identity_semantic_v23`; request ID uses `token_id_lexeme`; reservation ID uses one eight-field projection; the fingerprint semantic projection contains only `schema_version`, `spec_revision`, `policy_established`, and `component_hashes`, excluding its destination and `run_id`; authorization-use row-hash projections are synchronized; conflicting legacy support schemas are explicitly non-governing; and `initial_496_request_set_sha256` is fully defined as the LF-joined typed 496-entry hash.

### C. Authorization/request-set cycle removed

The request-set semantic hash excludes `authorization_id`. The authorization-ID projection includes the request-set semantic hash and excludes the request-set complete-file hash and `authorization_id`. The stored request set receives `authorization_id` only after ID computation; its complete-file hash is then stored as a non-ID field in the complete authorization record.

### D. Authorization-use and capture bindings closed

Authorization-use rows gain exact STARTED and terminal capture-row hashes. All eight states have closed predecessor, required, prohibited, and exact-value contracts. START-confirmed/ambiguous and terminal-recorded states bind the exact capture rows. Every capture state gains `authorized_request_set_file_sha256`, and all shared authorization/reservation/request/ordinal/attempt values must match.

### E. Cancellation proof simplified

The obsolete process-launch count and process-launch journal snapshot fields are removed. Positive no-start proof uses one immutable capture-audit snapshot covering the complete reservation interval, zero matching STARTED and terminal rows, the durable launch-after-STARTED enforcement rule, irreversible closure, and old-reservation unusability. Missing, stale, partial, interval-incomplete, or contradictory evidence remains `RESERVATION_START_STATUS_UNPROVEN`.

## 3. Baseline and amended target hashes

| Target | Baseline SHA-256 | Amended SHA-256 |
|---|---|---|
| `SPEC_local_curl_per_side_price_dataset_verification_REV23.md` | `d39ed18ac45f3d4aaf1fb01430da834a94b8400d59a30a22663c0cb3fc9c6032` | `94e42dfb48912392197250ec96500e3bdadcfa8de5331ad81cfcfb9d85835dc3` |
| `SCHEMA_REGISTRY_REV23.json` | `54b03b63dd65be462591e63ab3308153c10cc9de5c75e56f564612efe3f7cfcd` | `ce1ede1a27b438f6a8f6c04bf7c1642d74a2419719050e2f6bd85cb6ef949aca` |
| `REQUEST_PLAN_AND_AUTHORIZATION_CONTRACT_REV23.md` | `d6b98ee6167e8063709ace39f79236bb6e68a8aae2722f304626ac5b62323e04` | `4f0834b48d08fcfdaf32970d2542e61ab7c1263bb7ec727de1f02f2c1a7fbd37` |

The amended schema-registry hash above identifies the locally materialized result of applying the JSON Patch using the baseline registry's canonical compact sorted-key JSON serialization with no trailing LF. The specification's frozen `schema_registry_file_sha256` value remains the explicitly requested baseline Revision 23 value.

## 4. Authorization boundary

This amendment is specification only. It authorizes no implementation, tests, local reads, artifact recovery, deterministic regeneration, Source D regeneration, curl discovery, curl or network execution, replay, empirical run, empirical artifact generation, full-universe work, price construction, canonical-side price construction, side synthesis, price-store writes, P1/P2/P3 continuation, probe execution, scoring, wallet discovery or copying, OrdersMatched expansion, unrestricted `log_index`, PnL work, live trading, paper trading, or gate change. P1 remains blocked and `named_binary_probe_blocked` remains true.
