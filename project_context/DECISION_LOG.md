# DECISION LOG

*Settled decisions and pending review boundaries.*

---

## S2 Candidate 08 controlling decisions

1. K011 remains the accepted Candidate-08 specification acceptance:
   `1134` bytes /
   `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`.
2. A010 is the exact accepted Candidate-04 Markdown:
   `135500` bytes /
   `aea6aab26249ef84d8714197ab22d95f2701d6744ea6fa38c81fb1a390943950`, rank `1115`, direct predecessors exactly `[K011]`.
3. The accepted implementation-source authorization order is:
   `K011 -> A010 -> K013 -> K012 -> K014 -> K015/K016`.
4. K013 is exact installed canonical material:
   `3099` bytes /
   `e6ff152bf10d1f828ed0f9267ff3ea5a1ac7efc7cedc5866879cc958b108f32c`, installed at `6c891a61e7408f7977b72b2ccf52472412cd7e04`, direct predecessors
   exactly `[K011, A010]`.
5. A fresh K012 must be created only after exact K013 bytes exist.
6. K012 rank is `1130`, semantic role is
   `sentinel_implementation_source_authorization`, profile is
   `sentinel_authorization.v1`, and exact ordered direct predecessors are
   `[K011, A010, K013]`.
7. K012's `created_at_utc_ms` must be strictly greater than K013's.
8. K012 scope must equal or be a strict subset of K013. It must not add a
   path, operation, actor, activity, root, or permission.
9. The exact implementation-source matrix contains fourteen paths beneath
   `pm_research/named_binary_probe_s2`; no path may be added, removed, renamed,
   relocated, or reclassified.
10. Candidate preparation, checksumming, ZIP sealing, and Sentinel review have
    authorization effect `NONE`.
11. K012 review material is not consumable until Sentinel acceptance and every
    required canonical installation and exact installation-verification
    boundary are completed.
12. K014 is a separate later activity root and is not prepared by this package.
13. K015 and K016 are not prepared by this package.
14. No implementation source, test source, test execution, project import,
    local research-data access, subprocess execution, networking, empirical
    execution, project/research artifact generation, canonical installation,
    or Git action is authorized or performed by this package.

## Fresh K012 Candidate 01 decision request

Proposed artifact:

- path: `nodes/K012/artifact.json`;
- bytes: `3449`;
- SHA-256: `be5417097bd3f09a12a4b5092eacdaf85c81562d88c299b75e2fab4101f1e45c`;
- record ID: `S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_CANDIDATE_01`;
- schema/profile:
  `pm_research.s2.sentinel_authorization.v1` /
  `sentinel_authorization.v1`;
- embedded contract commit: `0b755fb71175370638ec87175aee85cf4710f54d`;
- package preparation base: `6c891a61e7408f7977b72b2ccf52472412cd7e04`;
- status: `REVIEW_CANDIDATE_NOT_CONSUMABLE`;
- requested Sentinel decision:
  `APPROVE — S2_CANDIDATE_08_K012_SENTINEL_IMPLEMENTATION_SOURCE_STAGE_AUTHORIZATION_CANDIDATE_01_ACCEPTED`.

Professor does not issue that decision.

## Matrix decision

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

The table is normative for this candidate's scope preservation. It contains no
source bytes and authorizes no implementation.

## Closed false-unblock paths

The following interpretations are rejected:

- installed K013 alone authorizes source authoring;
- proposed K012 is equivalent to accepted or installed K012;
- K012 payload decision `AUTHORIZE_STAGE` makes the review candidate consumable;
- K012 permits K014 creation automatically;
- K012 permits implementation without K014;
- documentation installation is implementation authorization;
- exact matrix names permit unlisted helpers or configuration files;
- an accepted source stage would permit tests, imports, data, subprocess,
  network, empirical work, or downstream phases;
- any price can be synthesized as `1-price`, `1-yes_price`, or a complement.

## Preserved research decisions

- final P0 eligible universe: `39,693`;
- P1 remains blocked;
- P2/P3 remain unauthorized;
- `named_binary_probe_blocked = true`;
- no accepted S2 per-token price artifact;
- no scoring or probe execution;
- complement synthesis prohibited.

## Requested review

Requested Sentinel decision: `APPROVE`, `BLOCK`, `DEFER`, or
`NEEDS VERIFICATION`.
