# HANDOFF — Professor → Sentinel — Local-Curl Per-Side Dataset Verification Revision 23

## Submission

Complete Revision 23 specification package for independent Sentinel review. Professor does not approve its own work. Revision 23 supersedes Revision 22 as a governing package while retaining every accepted Revision 22 architecture component not expressly corrected.

## Principal corrections

1. The archive is byte-self-contained and embeds every retained contract/vector and Revision-22 policy/vector file.
2. `SCHEMA_REGISTRY_REV23.json` is a complete closed registry: every persisted artifact has one exact schema, producer, consumer set, cardinality, ordering, hash projection, and lifecycle.
3. A detached V0–V5 attachment semantic object is computed before `run_id`; run identity then binds its hash without circular run paths.
4. A detached governing-package manifest binds exact package bytes into fingerprint readiness, run identity, Gustavo authorization, pre-V7 validation, and final inventories.
5. Authorization records and request sets use immutable per-authorization directories and independent semantic/complete-file hashes.
6. `REQUEST_RESERVATION_CANCELLED_NO_START` requires positive complete no-start evidence before a new continuation authorization may target the request.
7. Result labels are reachable, mutually exclusive, ordered, comparison-based, and free of unsupported causal attribution.

## Sentinel review focus

Sentinel should independently verify self-containment; retained byte hashes; registry closure; absence of schema/hash cycles; detached/run identity ordering; package-manifest binding; authorization namespace/cross-file equality; no-start proof sufficiency; complete state mappings; fixed denominators; result reachability; finalization immutability; and all project guardrails.

## Requested decision

`APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` for this specification package only.

## Required closing boundary

Specification revision only; implementation not authorized; tests not authorized; local reads and artifact recovery not authorized; deterministic regeneration not authorized; network or curl execution not authorized; empirical run not authorized; full-universe build not authorized; P1 remains blocked unless the canonical repository states otherwise; `named_binary_probe_blocked` remains true unless separately changed through an accepted and authorized gate decision.

This is a specification revision only. Implementation is not authorized. Tests are not authorized. Prefetch is not authorized. Local reads and artifact recovery are not authorized. Deterministic regeneration and Source D regeneration are not authorized. Curl discovery is not authorized. Curl execution and network execution are not authorized. Replay is not authorized. Empirical artifact generation is not authorized. Full-universe work is not authorized. Price construction, canonical-side price construction, side synthesis, `yes_price`, `1 - price`, `1 - p`, and price-store writes are not authorized. P1, P2, and P3 continuation are not authorized. Probe execution is not authorized. Scoring, wallet discovery or copying, OrdersMatched expansion, unrestricted `log_index`, PnL work, live trading, paper trading, and gate changes are not authorized. P1 remains blocked and `named_binary_probe_blocked` remains true.

## REV23 Amendment 03 effective-contract addendum

This addendum supersedes only the Revision 23 interfaces expressly identified below. Every prior handoff statement not expressly superseded remains unchanged and governing.

### Superseded by Amendment 03

- the run-scoped token-manifest lifecycle is replaced by the accepted V5 pre-run token-manifest lifecycle with exact 600/496/496 populations;
- amended typed projections use the accepted storage-to-logical-tag mapping and exact `NULL` encoding;
- partition identity is the accepted seven-field projection with exactly three partition families;
- the HTTP reconciliation schema version is solely `local_curl_http_status_reconciliation.v23`;
- curl stdout evidence is canonical Base64 raw bytes whose SHA-256, nullable lexeme, state, and integer are mechanically derived;
- selected-header state and integer are mechanically derived from retained response-header extraction contract SHA-256 `b010e18ee1da53b37bc70aa37b5e92ab35593b259140300b69174020ca710460`;
- the previously materialized twelve HTTP reconciliation combinations remain unchanged after evidence derivation.
- every `COMPLETED` curl category permits `HTTP_CODE_000`, `HTTP_CODE_100_599`, and `HTTP_CODE_INVALID`; all nine pairs persist HTTP reconciliation first, invalid then stops, and no lifecycle summary bypasses reconciliation;

### Explicitly unchanged

The prior handoff's self-containment, closed registry, detached pre-run attachment, noncircular twelve-field run identity, package-manifest binding, immutable authorization namespaces, no-start proof, result-label ordering, fixed denominators and thresholds, finalization, guardrails, and all authorization boundaries remain unchanged. Token-manifest relocation, cardinalities, provenance direction, integer pre-run timestamp, request provenance, partition identity, logical tags, null encoding, lifecycle states, and downstream gates are not changed by this correction.

### Key corrected target hashes

- `SCHEMA_REGISTRY_REV23.json`: `e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19`
- `SPEC_local_curl_per_side_price_dataset_verification_REV23.md`: `d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9`

### Package-level target hashes

- `GOVERNING_PACKAGE_MANIFEST_REV23.json`: `b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa`
- governing manifest semantic SHA-256: `6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b`

### Requested Sentinel decision

`APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` for this specification revision only.

### Amendment 03 closing authority statement

- specification revision only;
- implementation not authorized;
- tests and test authoring not authorized;
- local reads and artifact recovery not authorized;
- deterministic regeneration not authorized;
- network or curl execution not authorized;
- empirical run not authorized;
- full-universe build not authorized;
- P1 remains blocked unless the canonical repository states otherwise;
- `named_binary_probe_blocked` remains true unless separately changed through an accepted and authorized gate decision.
