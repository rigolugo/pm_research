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
