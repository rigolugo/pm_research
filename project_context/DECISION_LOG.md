# DECISION LOG

*Settled decisions and pending review boundaries.*

---

## S2 Candidate 08 controlling decisions

1. K011 remains accepted at `1134` bytes /
   `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`.
2. A010 remains accepted, installed, and verified at `135500`
   bytes / `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950`, rank `1115`, predecessor `[K011]`.
3. K013 remains accepted, installed, and verified at `3099`
   bytes / `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c`, rank `1120`, predecessors `[K011, A010]`.
4. K012 is accepted, installed at `0872d4578fd2c0fc5147c77af606b9f807c7bc2b`, and independently verified at
   `3449` bytes / `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c`, Git blob `796a4d1af1f5765890544f029e51b7b27878d24d`,
   rank `1130`, predecessors `[K011, A010, K013]`.
5. The accepted order is `K011 -> A010 -> K013 -> K012 -> K014 -> K015/K016`.
6. K014 rank is `1140`, role is `implementation_source_activity_root`,
   profile is `activity_root.v1`, and ordered predecessors are
   `[K011, A010, K013, K012]`.
7. K014 must be fresh after K012 and bind the exact four predecessor bytes.
8. K013 and K012 embed `0b755fb71175370638ec87175aee85cf4710f54d`; K014 uses that same commit.
9. K014 roots and scope equal the K013/K012 intersection.
10. The implementation matrix contains exactly fourteen paths under
    `pm_research/named_binary_probe_s2`.
11. Candidate preparation, checksums, ZIP sealing, and review have effect `NONE`.
12. K014 is not consumable before Sentinel acceptance, separate Gustavo
    installation authorization, installed-identity verification, and a
    separate Sentinel implementation handoff.
13. K015 and K016 remain unmaterialized.
14. No implementation, tests, imports, data, subprocess, network, empirical
    work, research artifact, installation, or Git activity is authorized or
    performed by this package.

## Fresh K014 decision request

- path: `nodes/K014/artifact.json`;
- bytes: `4302`;
- SHA-256: `7d54c1cabd1be53abc677425e5b7ce781d362bef2918c31bd844a0fa316b9fc2`;
- Git blob: `cc35df982377286e0940c9dddd5cee01a51e4ace`;
- embedded contract commit: `0b755fb71175370638ec87175aee85cf4710f54d`;
- preparation base: `0872d4578fd2c0fc5147c77af606b9f807c7bc2b`;
- status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`;
- requested Sentinel decision:
  `APPROVE — S2_CANDIDATE_08_K014_IMPLEMENTATION_SOURCE_ACTIVITY_ROOT_CANDIDATE_01_ACCEPTED`.

Professor does not issue that decision.

## Exact matrix decision

| # | Path | Role | Language | Required |
|---:|---|---|---|---|
| 1 | `pm_research/named_binary_probe_s2/__init__.py` | `package_export` | `PYTHON` | `true` |
| 2 | `pm_research/named_binary_probe_s2/acquisition.py` | `independent_token_acquisition_and_raw_closure` | `PYTHON` | `true` |
| 3 | `pm_research/named_binary_probe_s2/alignment.py` | `accepted_policy_alignment` | `PYTHON` | `true` |
| 4 | `pm_research/named_binary_probe_s2/audit.py` | `nineteen_audit_closures_and_gate` | `PYTHON` | `true` |
| 5 | `pm_research/named_binary_probe_s2/construction.py` | `scientific_construction_and_deduplication` | `PYTHON` | `true` |
| 6 | `pm_research/named_binary_probe_s2/prices_history_contract.py` | `endpoint_response_terminal_and_retry_contract` | `PYTHON` | `true` |
| 7 | `pm_research/named_binary_probe_s2/rebuild.py` | `isolated_rebuild_and_byte_comparison` | `PYTHON` | `true` |
| 8 | `pm_research/named_binary_probe_s2/request_plan.py` | `deterministic_request_plan` | `PYTHON` | `true` |
| 9 | `pm_research/named_binary_probe_s2/s4_inputs.py` | `s4_input_parsers_and_reconciliation` | `PYTHON` | `true` |
| 10 | `pm_research/named_binary_probe_s2/safe_span.py` | `safe_span_classifier_and_reducer` | `PYTHON` | `true` |
| 11 | `pm_research/named_binary_probe_s2/schema_registry.py` | `schema_registry_and_edge_derivation` | `PYTHON` | `true` |
| 12 | `pm_research/named_binary_probe_s2/state_reducers.py` | `global_condition_transition_state_reducers` | `PYTHON` | `true` |
| 13 | `pm_research/named_binary_probe_s2/transition.py` | `stage10_transition_reconciliation` | `PYTHON` | `true` |
| 14 | `pm_research/named_binary_probe_s2/types.py` | `closed_types_and_jcs` | `PYTHON` | `true` |

## Closed false-unblock paths

Rejected interpretations include: K012 alone starts implementation; proposed
K014 equals accepted/installed/verified K014; K014 bypasses a separate handoff;
K014 creates K015/K016 automatically; a fifteenth file, `src/`, namespace
package, or packaging change is allowed; source scope permits tests, data,
network, subprocess, empirical work, scoring, probes, gates, or downstream
phases; repository commit replaces the embedded contract commit; documentation
installation is implementation; or prices may be synthesized by complement.

## Preserved research decisions

P0 final eligible remains `39,693`; P1 is blocked; P2/P3 are unauthorized;
`named_binary_probe_blocked = true`; no S2 price artifact, scoring, probe, or
complement synthesis is accepted.

Requested Sentinel decision: `APPROVE`, `BLOCK`, `DEFER`, or
`NEEDS VERIFICATION`.
