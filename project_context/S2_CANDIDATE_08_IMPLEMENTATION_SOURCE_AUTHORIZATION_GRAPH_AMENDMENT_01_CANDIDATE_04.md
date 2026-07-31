# S2 Candidate 08 Implementation-Source Authorization-Graph Amendment 01 — Candidate 04

## 0. Status

| Field | Value |
|---|---|
| Document ID | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04` |
| Prospective graph node | `A010` |
| Status | `NARROWLY_CORRECTED_SPEC_ONLY_GRAPH_AMENDMENT_REVIEW_CANDIDATE` |
| Authoring mode | `AMEND` |
| Prepared by | Professor |
| Independent reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Exact verified canonical `main` | `90c0059c0e86b7afd44fcf9f17223d68eab1a9e0` |
| Exact accepted Amendment-01 installation commit | `e675a47ec2c8f6cd769c2673afc16d96e5622ccd` |
| Accepted base specification | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08` |
| Accepted base node | `K011` |
| Blocked predecessor | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_03` |
| Authorization effect | `NONE` |
| Requested Sentinel decision | `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` |

**Purpose.** Correct blocked Candidate 03 only by separating the exact-base end-to-end materializer from the verified-working-copy operation engine. Candidate 04 preserves Candidate 03's common-first operation classifier and all accepted graph, reducer, A010, implementation-matrix, and authorization behavior.

**Checkable completion sentence.** Sentinel can verify that every end-to-end materializer invocation first binds the immutable base registry at `479463` bytes / `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`, then binds the exact `45347`-byte overlay / `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a`, invokes the operation engine exactly once on one isolated copy, validates the exact `1266`-byte effective-registry bundle / `075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67`, publishes only `167 / 683` with K127 population `60` and the unchanged `66232`-byte reducer projection, classifies synthetic operation-engine counterexamples separately, and leaves authorization effect `NONE`.

### 0.1 Normative A010 payload

The following is the sole machine-extractable A010 payload. The `governed_amendment_identity` object is closed typed governance identity data and creates no graph edge.

<!-- NORMATIVE_A010_PAYLOAD -->
```json
{
  "document_id": "S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04",
  "status": "SPEC_ONLY_GRAPH_AMENDMENT_REVIEW_CANDIDATE",
  "canonical_commit": "90c0059c0e86b7afd44fcf9f17223d68eab1a9e0",
  "activity_root": null,
  "normative_input_refs": [
    {
      "node_id": "K011",
      "logical_path": "nodes/K011/artifact.json",
      "byte_length": 1134,
      "sha256": "4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649"
    }
  ],
  "governed_amendment_identity": {
    "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md",
    "byte_length": 24599,
    "sha256": "8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63",
    "installation_commit": "e675a47ec2c8f6cd769c2673afc16d96e5622ccd",
    "authorization_effect": "NONE"
  },
  "normative_sections": [
    "SECTION_00_STATUS",
    "SECTION_01_AUTHORITY",
    "SECTION_02_SCOPE",
    "SECTION_03_BASE_REGISTRY_OVERLAY",
    "SECTION_04_A010",
    "SECTION_05_AUTHORIZATION_NODES",
    "SECTION_06_K015_K016",
    "SECTION_07_K127",
    "SECTION_08_GRAPH_COUNTS",
    "SECTION_09_STOP_REGISTRATION",
    "SECTION_10_CHANGED_LOCATIONS",
    "SECTION_11_ACCEPTANCE",
    "SECTION_12_COMPATIBILITY",
    "SECTION_13_SECURITY",
    "SECTION_14_SELF_ATTACK",
    "SECTION_15_DECISION"
  ],
  "authorization_effect": "NONE"
}
```

Candidate 03 is blocked and non-controlling. Candidate 04 supersedes Candidate 03 only if Sentinel accepts these exact Candidate-04 bytes.

---

## 1. Canonical authority and evidence classification

### 1.1 Exact canonical base

Canonical `main` was verified as:

`90c0059c0e86b7afd44fcf9f17223d68eab1a9e0`

The accepted Implementation-Source Amendment 01 installation commit is:

`e675a47ec2c8f6cd769c2673afc16d96e5622ccd`

The installation commit is an ancestor of the authoring base. Any unexplained canonical-base difference is `STOP_CANONICAL_BASE_MISMATCH`.

### 1.2 Exact accepted identities

| Item | Logical path | Bytes | SHA-256 / commit | Classification |
|---|---|---:|---|---|
| K011 | `nodes/K011/artifact.json` | `1134` | `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649` | `CANONICAL` |
| Accepted Implementation-Source Amendment 01 | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md` | `24599` | `8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63` | `CANONICAL` and `ACCEPTED` |
| Amendment-01 installation | repository commit | — | `e675a47ec2c8f6cd769c2673afc16d96e5622ccd` | `CANONICAL` |
| Accepted Candidate-08 §23 base-registry JCS | exact first JSON block under §23 | `479463` | `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff` | `ACCEPTED` |
| Accepted reducer projection | exact `condition_state_classes` plus `global_state_reducer` projection | `66232` | `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c` | `ACCEPTED` |
| Blocked Candidate 03 | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_03.md` | `124860` | `28299322ea7e27a65193cd8c5fe7db447ee7e851a85bdaf516ff34be3218da9c` | `SUBMITTED` |
| Candidate-04 overlay | §3.4 | `45347` | `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a` | `SUBMITTED` |
| Candidate-04 effective-registry bundle | §3.7 | `1266` | `075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67` | `COMPUTED` from exact submitted overlay |

The malformed 63-character derivative K011 string ending in `...f264` is not a `Sha256`, is not an alternate identity, and MUST NOT enter A010, the overlay, any successor NodeRef, K127, or an acceptance predicate. Correcting derivative summary documents remains outside this task.

### 1.3 Precedence

1. Canonical repository bytes at `90c0059c0e86b7afd44fcf9f17223d68eab1a9e0` control.
2. Exact K011 bytes and original Candidate-08 installation controls control K011 identity.
3. Accepted Candidate 08 controls as the immutable base.
4. Accepted installed Implementation-Source Amendment 01 controls its named implementation-source locations.
5. This Candidate-04 overlay and two-layer materialization contract control only the exact operations, materializer/engine boundary, and prose/Appendix replacements listed here after Sentinel acceptance.
6. Unlisted Candidate-08 and Amendment-01 requirements remain unchanged.

No `RECALLED` or `ASSUMED` claim creates a normative field, graph edge, identity, count, or stop.

---

## 2. Scope

### 2.1 In scope

This amendment defines:

1. exactly one governance node, `A010`, at rank `1115`;
2. a dedicated closed `amendment_governance.v1` profile;
3. the exact accepted Amendment-01 identity inside A010's machine payload;
4. an immutable accepted base-registry literal;
5. one independently identified graph-overlay literal;
6. an exact assertive ordered overlay algorithm;
7. one exact effective-registry bundle identity;
8. exact future generated-literal and static source-review obligations;
9. K013, K012, K014, and K127 graph amendments;
10. exact K127 population `60`;
11. exact effective graph `167 / 683`;
12. exact closed overlay stop-code type and inventory;
13. exhaustive graph-count and graph-role replacement locations.

### 2.2 Out of scope

This amendment does not:

- modify the accepted base-registry JCS bytes;
- claim the base registry contains A010 or `167 / 683`;
- modify `condition_state_classes` or `global_state_reducer`;
- rewrite accepted Candidate-08, accepted Amendment 01, historical installation records, or settled decision entries;
- correct derivative K011 summary documents;
- create a third hand-edited semantic registry literal;
- change K015 or K016 direct-predecessor boundaries;
- change the accepted fourteen-file implementation matrix except by applying accepted Amendment-01 path replacements through the overlay;
- materialize A010, K013, K012, K014, K015, or K016;
- authorize implementation, tests, imports, execution, research-data access, networking, canonical edits, or Git writes.

---

## 3. Exact immutable-base-plus-overlay registry model

### 3.1 Immutable base literal

Future `schema_registry.py` MUST preserve one exact immutable base-registry literal:

| Field | Exact value |
|---|---|
| Source | accepted Candidate-08 §23 first fenced JSON object |
| JCS byte length | `479463` |
| JCS SHA-256 | `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff` |
| Mutable | `NO` |
| Contains A010 | `NO` |
| Graph counts contained in base | `166 / 678` |
| K127 population contained in base | `59` |

The base literal MUST be decoded, parsed with duplicate keys rejected, and verified before any overlay operation. The base literal MUST NOT be regenerated from Markdown at runtime.

### 3.2 Overlay schemas

The overlay uses these closed types.

#### `RegistryOverlayOperationV1`

| Field | Type | Rule |
|---|---|---|
| `ordinal` | `Count` | exact contiguous integer `0..26` |
| `operation` | enum | `ASSERT_ABSENT_ADD` or `ASSERT_EQUAL_REPLACE` |
| `json_pointer` | `Utf8String` | exact RFC 6901 pointer; unique across operations |
| `expected_old_state` | enum | `ABSENT` for add, `PRESENT` for replace |
| `expected_old_jcs_sha256` | `Nullable<Sha256>` | null only for add; exact target-value JCS hash for replace |
| `new_value_jcs_sha256` | `Sha256` | SHA-256 of RFC 8785 JCS of `new_value` |
| `new_value` | JSON value | exact replacement or addition value |

Additional fields are forbidden. Array order is normative. Duplicate JSON object keys are forbidden.

#### `RegistryGraphOverlayV1`

| Field | Type | Exact rule |
|---|---|---|
| `schema_id` | constant | `pm_research.s2.registry_graph_overlay.v1` |
| `overlay_id` | constant | `S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_OVERLAY_04` |
| `base_registry_identity` | closed object | exact `479463` / `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff` base |
| `serialization` | constant | `RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE` |
| `application_profile_id` | constant | `EXACT_BASE_MATERIALIZER_VERIFIED_WORKING_COPY_ENGINE_V3` |
| `operation_count` | constant | `27` |
| `operations` | array | exact literal order and values in §3.4 |
| `stop_code_type` | closed enum | exact eleven codes in §9 |
| `stop_inventory` | closed inventory | exact count `11`; zero unregistered |
| `source_review_contract` | closed object | exact two-layer materializer/engine static requirements in the literal |
| `postconditions` | closed object | exact verified base, one operation-engine invocation, `167 / 683`, K127 `60`, no partial publication, unchanged reducer, `NONE` |

Additional fields are forbidden.

### 3.3 Overlay identity prerequisite

The exact graph-overlay JCS identity is:

| Field | Exact value |
|---|---|
| Byte length | `45347` |
| SHA-256 | `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a` |
| Operation count | `27` |
| Duplicate target count | `0` |
| Authorization effect | `NONE` |

The overlay identity is externally bound by this amendment candidate, its handoff, and checksum inventory. It is not self-embedded in the overlay literal.

### 3.4 Exact overlay literal

The following object is normative. Its RFC 8785 JCS bytes, not this indented rendering, have the identity in §3.3.

```json
{
  "schema_id": "pm_research.s2.registry_graph_overlay.v1",
  "overlay_id": "S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_OVERLAY_04",
  "base_registry_identity": {
    "schema_registry_id": "pm_research.s2.candidate08.complete_node_schema_registry.v5",
    "byte_length": 479463,
    "sha256": "82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff"
  },
  "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
  "application_profile_id": "EXACT_BASE_MATERIALIZER_VERIFIED_WORKING_COPY_ENGINE_V3",
  "operation_count": 27,
  "operations": [
    {
      "ordinal": 0,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/implementation_source_matrix",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "935a4f9917b2d255d9b7c6fd446554e448cda50e523249f77cfe3113d5a80dd9",
      "new_value_jcs_sha256": "256cf3796da06fe3e6def7b84b4a9f6b5d20c535ceb7b8917f75726800c2be43",
      "new_value": [
        {
          "logical_path": "pm_research/named_binary_probe_s2/__init__.py",
          "role": "package_export",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/acquisition.py",
          "role": "independent_token_acquisition_and_raw_closure",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/alignment.py",
          "role": "accepted_policy_alignment",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/audit.py",
          "role": "nineteen_audit_closures_and_gate",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/construction.py",
          "role": "scientific_construction_and_deduplication",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/prices_history_contract.py",
          "role": "endpoint_response_terminal_and_retry_contract",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/rebuild.py",
          "role": "isolated_rebuild_and_byte_comparison",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/request_plan.py",
          "role": "deterministic_request_plan",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/s4_inputs.py",
          "role": "s4_input_parsers_and_reconciliation",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/safe_span.py",
          "role": "safe_span_classifier_and_reducer",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/schema_registry.py",
          "role": "schema_registry_and_edge_derivation",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/state_reducers.py",
          "role": "global_condition_transition_state_reducers",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/transition.py",
          "role": "stage10_transition_reconciliation",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/types.py",
          "role": "closed_types_and_jcs",
          "language": "PYTHON",
          "required": true
        }
      ]
    },
    {
      "ordinal": 1,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/artifact_profiles/source_matrix.v1/ordering",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "e759377aa8d85c4afb7eab70fa5f44bf1c16729a1b7523827c8348600835d00b",
      "new_value_jcs_sha256": "84752688f325efc44a4b63fd48ed02552d40354e104561e0d7c5a5bb4fd6caa8",
      "new_value": [
        "file_matrix ascending by logical_path UTF-8 bytes after required NFC validation"
      ]
    },
    {
      "ordinal": 2,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/artifact_profiles/source_matrix.v1/constraints",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "0a868496c05defd4bb323b31102b1d2115ba6c456ed19d221e29eacd8b6b1297",
      "new_value_jcs_sha256": "4d17a1dd03f4038cfd239e6cef87b203212260d86f59ca09c6eedcce667fe799",
      "new_value": [
        "file_matrix path-role pairs equal the exact implementation_source_matrix",
        "no unlisted source path",
        "each row has logical_path, role, language=PYTHON, byte_length, sha256, required=true",
        "logical_path is already NFC and is not normalized during emission",
        "roles remain attached to paths before and after ordering",
        "K015 ordering is independent of role order and authoring order"
      ]
    },
    {
      "ordinal": 3,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K015/node_specific_constants/exact_source_file_matrix",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "fa0488deb1971ab57e1314ba61451acee0d4e891255843ef8c53d7a3c70878a7",
      "new_value_jcs_sha256": "256cf3796da06fe3e6def7b84b4a9f6b5d20c535ceb7b8917f75726800c2be43",
      "new_value": [
        {
          "logical_path": "pm_research/named_binary_probe_s2/__init__.py",
          "role": "package_export",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/acquisition.py",
          "role": "independent_token_acquisition_and_raw_closure",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/alignment.py",
          "role": "accepted_policy_alignment",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/audit.py",
          "role": "nineteen_audit_closures_and_gate",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/construction.py",
          "role": "scientific_construction_and_deduplication",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/prices_history_contract.py",
          "role": "endpoint_response_terminal_and_retry_contract",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/rebuild.py",
          "role": "isolated_rebuild_and_byte_comparison",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/request_plan.py",
          "role": "deterministic_request_plan",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/s4_inputs.py",
          "role": "s4_input_parsers_and_reconciliation",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/safe_span.py",
          "role": "safe_span_classifier_and_reducer",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/schema_registry.py",
          "role": "schema_registry_and_edge_derivation",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/state_reducers.py",
          "role": "global_condition_transition_state_reducers",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/transition.py",
          "role": "stage10_transition_reconciliation",
          "language": "PYTHON",
          "required": true
        },
        {
          "logical_path": "pm_research/named_binary_probe_s2/types.py",
          "role": "closed_types_and_jcs",
          "language": "PYTHON",
          "required": true
        }
      ]
    },
    {
      "ordinal": 4,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/nodes/K015/node_specific_constants/package_model",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "9c833f5d7c2e2f3ab89569e920798fe12d28ef8d3cbc049bec205de9e09c887b",
      "new_value": {
        "repository_package_root": "pm_research",
        "implementation_subpackage": "pm_research.named_binary_probe_s2",
        "repository_directory": "pm_research/named_binary_probe_s2",
        "regular_package_required": true,
        "namespace_package_permitted": false,
        "src_layout_permitted": false,
        "pyproject_change_permitted": false
      }
    },
    {
      "ordinal": 5,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/nodes/K015/node_specific_constants/file_count",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "8527a891e224136950ff32ca212b45bc93f69fbb801c3b1ebedac52775f99e61",
      "new_value": 14
    },
    {
      "ordinal": 6,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/nodes/K015/node_specific_constants/k015_emit_order",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "7c0745fab19e995c707c1ccfff4569db82e4e1dc146e8cbf2a60eab5f3ec7891",
      "new_value": "LOGICAL_PATH_UTF8_ASCENDING"
    },
    {
      "ordinal": 7,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K015/node_specific_invariants",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "16ceb4a5fb242c66edc9c14dc81ac92079d7d3ec8e9845d2b01ca795eb884ba6",
      "new_value_jcs_sha256": "f429cc3826c9b01ddc24724ed34e0766635152d8b2ed98804704db18990ab189",
      "new_value": [
        "file_matrix contains exactly fourteen rows",
        "emitted path-role sequence equals the exact amended implementation_source_matrix",
        "every role remains bound to its exact path",
        "every row contains submitted raw file byte_length and sha256",
        "no source path outside the exact fourteen-path matrix exists",
        "no source path uses src/",
        "no namespace-package or packaging-configuration fallback is used",
        "matrix validation precedes K016 creation",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    {
      "ordinal": 8,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/nodes/K016/node_specific_constants/self_identity_rule",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "077aebeab5bbfc0690e80c0755bf5dff10f647e9769bffe8d2ab876d9e23c634",
      "new_value": "MUST_BE_NULL"
    },
    {
      "ordinal": 9,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K016/node_specific_invariants",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "aba0f212a8c80289b9385ad005a4196207ad3eb85a1149cf9c1857bcbd6c6aa5",
      "new_value_jcs_sha256": "43463f51e875c78ecd17a39e18e7dacdd7be01173eab0bde7f971753ba5f938a",
      "new_value": [
        "/payload/self_identity is exactly null",
        "K016 does not embed its own raw sha256",
        "K016 does not use a self-excluding projection",
        "K017 or an external delivery envelope binds exact K016 logical_path byte_length and sha256",
        "K016 is non-authorizing and reports implementation source only",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    {
      "ordinal": 10,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/type_registry/GovernedAmendmentIdentity",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "ded425e2064aa7f2b1b48339cadf72dcb454b91b320e54afc86f7574dcb6d298",
      "new_value": {
        "kind": "object",
        "required": [
          "logical_path",
          "byte_length",
          "sha256",
          "installation_commit",
          "authorization_effect"
        ],
        "fields": {
          "logical_path": "Const[project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md]",
          "byte_length": "Const[24599]",
          "sha256": "Const[8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63]",
          "installation_commit": "Const[e675a47ec2c8f6cd769c2673afc16d96e5622ccd]",
          "authorization_effect": "Const[NONE]"
        },
        "additional_fields": false,
        "constraints": [
          "all five fields are mandatory and non-null",
          "missing malformed additional conflicting or alternate amendment identity is invalid",
          "identity fields are typed governance identity data and create no provenance edge"
        ]
      }
    },
    {
      "ordinal": 11,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/type_registry/RegistryOverlayStopCode",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "e85b35e5478c726df11fd6f13982187445d2a11d0c259c797663d82a8f6ac9c6",
      "new_value": {
        "kind": "string",
        "enum": [
          "STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH",
          "STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH",
          "STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID",
          "STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET",
          "STOP_REGISTRY_OVERLAY_TARGET_MISSING",
          "STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE",
          "STOP_REGISTRY_OVERLAY_ALREADY_APPLIED",
          "STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH",
          "STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH",
          "STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH",
          "STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID"
        ]
      }
    },
    {
      "ordinal": 12,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/registry_overlay_stop_inventory",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "b761ce7a3797401d6114b5311942fd8b33355cfe20c53100e7ebd496bdc520ac",
      "new_value": {
        "schema_id": "pm_research.s2.registry_overlay_stop_inventory.v1",
        "stop_code_type": "RegistryOverlayStopCode",
        "stop_code_count": 11,
        "entries": [
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH",
            "trigger": "before any overlay or operation-engine evaluation, the externally supplied or selected registry JCS bytes differ in byte length or SHA-256 from the exact immutable accepted base identity",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH",
            "trigger": "after exact base verification, the supplied overlay JCS bytes, closed schema, or any embedded operation new-value hash differs from the exact overlay contract",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID",
            "trigger": "after exact base and overlay identity/schema/hash verification, operation ordinals are not the exact contiguous sequence or supplied operation order differs from the literal",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET",
            "trigger": "after exact base and overlay identity/schema/hash/order verification, two operations target the same JSON Pointer",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_TARGET_MISSING",
            "trigger": "the required parent does not exist for any operation, or an ASSERT_EQUAL_REPLACE target is absent after the common exact-new check",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE",
            "trigger": "an ASSERT_ABSENT_ADD target exists and differs from new_value, or an ASSERT_EQUAL_REPLACE current-target JCS SHA-256 differs from expected_old_jcs_sha256 after the common exact-new check",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_REGISTRY_OVERLAY_ALREADY_APPLIED",
            "trigger": "inside the verified-working-copy operation engine, the target exists and deep-equals the exact new_value; this common check precedes expected-old state or expected-old hash enforcement and is never used to classify an externally altered base input",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH",
            "trigger": "after graph and reducer postconditions pass, the serialized effective-registry bundle differs from its exact byte length or SHA-256, or atomic commit/exposure would publish a partial or non-identical result",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH",
            "trigger": "after one successful operation-engine invocation, the resolved semantic graph is not exactly 167 nodes, 683 direct edges, K127 population 60, and zero missing/extra/rank/cycle defects",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH",
            "trigger": "after graph reconciliation, the post-overlay projection of condition_state_classes and global_state_reducer differs from 66232 bytes and the accepted SHA-256",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          },
          {
            "stop_code": "STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID",
            "trigger": "A010 governed amendment identity is missing malformed additional conflicting or not the exact accepted installed identity",
            "effect": "HALT_NO_EFFECTIVE_REGISTRY"
          }
        ],
        "unregistered_stop_code_count": 0
      }
    },
    {
      "ordinal": 13,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/artifact_profiles/amendment_governance.v1",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "74a0a5ed842b98dd95dac5398ee608f390759f74030844d45acc915157ec0ac8",
      "new_value": {
        "media_type": "text/markdown",
        "serialization": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
        "required_fields": [
          "/document_id",
          "/status",
          "/canonical_commit",
          "/activity_root",
          "/normative_input_refs",
          "/governed_amendment_identity",
          "/normative_sections",
          "/authorization_effect"
        ],
        "fields": {
          "/document_id": {
            "type": "Const[S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04]",
            "nullable": false
          },
          "/status": {
            "type": "Const[SPEC_ONLY_GRAPH_AMENDMENT_REVIEW_CANDIDATE]",
            "nullable": false
          },
          "/canonical_commit": {
            "type": "Const[90c0059c0e86b7afd44fcf9f17223d68eab1a9e0]",
            "nullable": false
          },
          "/activity_root": {
            "type": "Const[null]",
            "nullable": true
          },
          "/normative_input_refs": {
            "type": "Array<NodeRef>",
            "min_items": 1,
            "max_items": 1,
            "nullable": false
          },
          "/governed_amendment_identity": {
            "type": "GovernedAmendmentIdentity",
            "nullable": false
          },
          "/normative_sections": {
            "type": "Array<RecordId>",
            "min_items": 1,
            "nullable": false
          },
          "/authorization_effect": {
            "type": "Const[NONE]",
            "nullable": false
          }
        },
        "node_ref_slots": {
          "/normative_input_refs": "array"
        },
        "non_edge_identity_slots": {
          "/governed_amendment_identity": "GovernedAmendmentIdentity"
        },
        "additional_fields": false,
        "ordering": [
          "normative_input_refs exact singleton K011",
          "normative_sections exact document order"
        ],
        "uniqueness": [
          "normative_input_refs.node_id",
          "normative_sections"
        ],
        "equations": [
          "array_length(normative_input_refs)=1"
        ],
        "constraints": [
          "activity_root is exactly null",
          "normative_input_refs[0] is exact K011 1134 bytes and authoritative SHA-256",
          "governed_amendment_identity exactly equals the accepted installed Amendment-01 identity",
          "governed_amendment_identity creates no direct edge",
          "authorization_effect=NONE",
          "no implementation or execution authorization"
        ]
      }
    },
    {
      "ordinal": 14,
      "operation": "ASSERT_ABSENT_ADD",
      "json_pointer": "/nodes/A010",
      "expected_old_state": "ABSENT",
      "expected_old_jcs_sha256": null,
      "new_value_jcs_sha256": "e747d28eaf6c8e5956e0dc1b791cc8ecf1f085931565932fb17196a79b4ccee4",
      "new_value": {
        "rank": 1115,
        "semantic_role": "implementation_source_authorization_graph_amendment_governance",
        "artifact_profile_id": "amendment_governance.v1",
        "ref_bindings": [
          {
            "json_pointer": "/normative_input_refs/0",
            "type": "NodeRefArrayElement",
            "target_node_id": "K011",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          }
        ],
        "derived_direct_predecessors": [
          "K011"
        ],
        "node_specific_constants": {
          "exact_ref_field_cardinalities": {
            "/normative_input_refs": 1
          },
          "exact_direct_predecessor_count": 1,
          "exact_governed_amendment_identity": {
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md",
            "byte_length": 24599,
            "sha256": "8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63",
            "installation_commit": "e675a47ec2c8f6cd769c2673afc16d96e5622ccd",
            "authorization_effect": "NONE"
          }
        },
        "node_specific_invariants": [
          "A010 validates amendment_governance.v1",
          "A010 has exactly one graph predecessor K011",
          "governed_amendment_identity is exact and creates no graph edge",
          "authorization_effect is NONE",
          "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
        ],
        "raw_media_type_override": "text/markdown; charset=utf-8",
        "raw_serialization_override": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
        "payload_extraction_rule": "exactly one fenced JSON block immediately following NORMATIVE_A010_PAYLOAD; parse as JSON; validate amendment_governance.v1; derive only K011 from /normative_input_refs/0"
      }
    },
    {
      "ordinal": 15,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K013",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "4d0b7c11df21825f44bad1d7cfcda18577c8bdcf07ac59fcaf6af955c88536ff",
      "new_value_jcs_sha256": "7b72e78d2079187971937d53281d968f0a222fe99ef24f5c1e514a6c48040209",
      "new_value": {
        "rank": 1120,
        "semantic_role": "gustavo_implementation_source_authorization",
        "artifact_profile_id": "gustavo_authorization.v1",
        "ref_bindings": [
          {
            "json_pointer": "/payload/prerequisite_acceptance",
            "type": "NodeRef",
            "target_node_id": "K011",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/additional_prerequisites/0",
            "type": "NodeRefArrayElement",
            "target_node_id": "A010",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          }
        ],
        "derived_direct_predecessors": [
          "K011",
          "A010"
        ],
        "node_specific_constants": {
          "exact_ref_field_cardinalities": {
            "/payload/prerequisite_acceptance": 1,
            "/payload/additional_prerequisites": 1
          },
          "exact_direct_predecessor_count": 2
        },
        "node_specific_invariants": [
          "additional_prerequisites is present and equals [A010]",
          "K011 remains the prerequisite_acceptance",
          "fresh bytes are created only after exact accepted and canonically installed A010 identity exists",
          "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
        ]
      }
    },
    {
      "ordinal": 16,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K012",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "11eb91f5b0b915e8f7b8eb57ab1e0db22323281800ba7557005ba79a92b0cff5",
      "new_value_jcs_sha256": "4f7c441aa13f21b806ffb27936756fb26eae2d7b9f0dd56d90a7bc86007d1669",
      "new_value": {
        "rank": 1130,
        "semantic_role": "sentinel_implementation_source_authorization",
        "artifact_profile_id": "sentinel_authorization.v1",
        "ref_bindings": [
          {
            "json_pointer": "/payload/prerequisite_acceptance",
            "type": "NodeRef",
            "target_node_id": "K011",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/additional_prerequisites/0",
            "type": "NodeRefArrayElement",
            "target_node_id": "A010",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/gustavo_authorization",
            "type": "NodeRef",
            "target_node_id": "K013",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          }
        ],
        "derived_direct_predecessors": [
          "K011",
          "A010",
          "K013"
        ],
        "node_specific_constants": {
          "exact_ref_field_cardinalities": {
            "/payload/prerequisite_acceptance": 1,
            "/payload/additional_prerequisites": 1,
            "/payload/gustavo_authorization": 1
          },
          "exact_direct_predecessor_count": 3
        },
        "node_specific_invariants": [
          "additional_prerequisites is present and equals [A010]",
          "K011 remains the prerequisite_acceptance",
          "K013 exact bytes preexist K012 and bind the same K011 and A010 identities",
          "K012 created_at_utc_ms is greater than K013 created_at_utc_ms",
          "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
        ]
      }
    },
    {
      "ordinal": 17,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K014",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "556cdf06e494a96ac9fc22782dd54e2d8df6557799669bf8a4f9db740c0ba784",
      "new_value_jcs_sha256": "0361a30699082c0111f9cac7060ed4a7cf6c66d7f792602d19466a1604220293",
      "new_value": {
        "rank": 1140,
        "semantic_role": "implementation_source_activity_root",
        "artifact_profile_id": "activity_root.v1",
        "ref_bindings": [
          {
            "json_pointer": "/payload/prerequisite_acceptance",
            "type": "NodeRef",
            "target_node_id": "K011",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/additional_prerequisites/0",
            "type": "NodeRefArrayElement",
            "target_node_id": "A010",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/gustavo_authorization",
            "type": "NodeRef",
            "target_node_id": "K013",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/sentinel_stage_authorization",
            "type": "NodeRef",
            "target_node_id": "K012",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          }
        ],
        "derived_direct_predecessors": [
          "K011",
          "A010",
          "K013",
          "K012"
        ],
        "node_specific_constants": {
          "exact_ref_field_cardinalities": {
            "/payload/prerequisite_acceptance": 1,
            "/payload/additional_prerequisites": 1,
            "/payload/gustavo_authorization": 1,
            "/payload/sentinel_stage_authorization": 1
          },
          "exact_direct_predecessor_count": 4
        },
        "node_specific_invariants": [
          "additional_prerequisites is present and equals [A010]",
          "K011 remains the prerequisite_acceptance",
          "K013 and K012 exact bytes preexist K014 and bind the same K011 and A010 identities",
          "K014 created_at_utc_ms is greater than both K013 and K012 created_at_utc_ms",
          "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
        ]
      }
    },
    {
      "ordinal": 18,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/test_source_matrix/0/role",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "c03eb174f8b5936ee87f40372e51ebb90b5dbc13565e9742c51fbdeea56bae3e",
      "new_value_jcs_sha256": "99f7298fccde73e621974a9b04883210bf01f3651b01ebf9d9ee106a0c4eb96a",
      "new_value": "schema_and_683_edge_equality"
    },
    {
      "ordinal": 19,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K022/node_specific_constants/exact_test_file_matrix/0/role",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "c03eb174f8b5936ee87f40372e51ebb90b5dbc13565e9742c51fbdeea56bae3e",
      "new_value_jcs_sha256": "99f7298fccde73e621974a9b04883210bf01f3651b01ebf9d9ee106a0c4eb96a",
      "new_value": "schema_and_683_edge_equality"
    },
    {
      "ordinal": 20,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/nodes/K127",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "c65d29f5c3b4a3183c1e228b73b0e296bad3198e56639a0c1d5b6132c5898679",
      "new_value_jcs_sha256": "c6dec1bb8f87aa582ccd1a91c74c0949b53453ee0026127cfbb0a506dbe9adf3",
      "new_value": {
        "rank": 2320,
        "semantic_role": "authorization_and_handoff_provenance_closure",
        "artifact_profile_id": "audit_closure.v1",
        "ref_bindings": [
          {
            "json_pointer": "/payload/ordered_evidence/0",
            "type": "NodeRefArrayElement",
            "target_node_id": "A002",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/1",
            "type": "NodeRefArrayElement",
            "target_node_id": "K011",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/2",
            "type": "NodeRefArrayElement",
            "target_node_id": "A010",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/3",
            "type": "NodeRefArrayElement",
            "target_node_id": "K018",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/4",
            "type": "NodeRefArrayElement",
            "target_node_id": "K025",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/5",
            "type": "NodeRefArrayElement",
            "target_node_id": "K032",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/6",
            "type": "NodeRefArrayElement",
            "target_node_id": "K041",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/7",
            "type": "NodeRefArrayElement",
            "target_node_id": "K051",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/8",
            "type": "NodeRefArrayElement",
            "target_node_id": "K052P",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/9",
            "type": "NodeRefArrayElement",
            "target_node_id": "K067",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/10",
            "type": "NodeRefArrayElement",
            "target_node_id": "K068",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/11",
            "type": "NodeRefArrayElement",
            "target_node_id": "K079",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/12",
            "type": "NodeRefArrayElement",
            "target_node_id": "K082",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/13",
            "type": "NodeRefArrayElement",
            "target_node_id": "K083P",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/14",
            "type": "NodeRefArrayElement",
            "target_node_id": "K091",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/15",
            "type": "NodeRefArrayElement",
            "target_node_id": "K104",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/16",
            "type": "NodeRefArrayElement",
            "target_node_id": "K006",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/17",
            "type": "NodeRefArrayElement",
            "target_node_id": "K005",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/18",
            "type": "NodeRefArrayElement",
            "target_node_id": "K007",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/19",
            "type": "NodeRefArrayElement",
            "target_node_id": "K009",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/20",
            "type": "NodeRefArrayElement",
            "target_node_id": "K013",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/21",
            "type": "NodeRefArrayElement",
            "target_node_id": "K012",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/22",
            "type": "NodeRefArrayElement",
            "target_node_id": "K014",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/23",
            "type": "NodeRefArrayElement",
            "target_node_id": "K016",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/24",
            "type": "NodeRefArrayElement",
            "target_node_id": "K020",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/25",
            "type": "NodeRefArrayElement",
            "target_node_id": "K019",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/26",
            "type": "NodeRefArrayElement",
            "target_node_id": "K021",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/27",
            "type": "NodeRefArrayElement",
            "target_node_id": "K023",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/28",
            "type": "NodeRefArrayElement",
            "target_node_id": "K027",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/29",
            "type": "NodeRefArrayElement",
            "target_node_id": "K026",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/30",
            "type": "NodeRefArrayElement",
            "target_node_id": "K028",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/31",
            "type": "NodeRefArrayElement",
            "target_node_id": "K030",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/32",
            "type": "NodeRefArrayElement",
            "target_node_id": "K034",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/33",
            "type": "NodeRefArrayElement",
            "target_node_id": "K033",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/34",
            "type": "NodeRefArrayElement",
            "target_node_id": "K035",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/35",
            "type": "NodeRefArrayElement",
            "target_node_id": "K039",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/36",
            "type": "NodeRefArrayElement",
            "target_node_id": "K043",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/37",
            "type": "NodeRefArrayElement",
            "target_node_id": "K042",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/38",
            "type": "NodeRefArrayElement",
            "target_node_id": "K044",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/39",
            "type": "NodeRefArrayElement",
            "target_node_id": "K048",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/40",
            "type": "NodeRefArrayElement",
            "target_node_id": "K054",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/41",
            "type": "NodeRefArrayElement",
            "target_node_id": "K053",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/42",
            "type": "NodeRefArrayElement",
            "target_node_id": "K055",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/43",
            "type": "NodeRefArrayElement",
            "target_node_id": "K065",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/44",
            "type": "NodeRefArrayElement",
            "target_node_id": "K070",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/45",
            "type": "NodeRefArrayElement",
            "target_node_id": "K069",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/46",
            "type": "NodeRefArrayElement",
            "target_node_id": "K071",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/47",
            "type": "NodeRefArrayElement",
            "target_node_id": "K077",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/48",
            "type": "NodeRefArrayElement",
            "target_node_id": "K085",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/49",
            "type": "NodeRefArrayElement",
            "target_node_id": "K084",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/50",
            "type": "NodeRefArrayElement",
            "target_node_id": "K086",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/51",
            "type": "NodeRefArrayElement",
            "target_node_id": "K089",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/52",
            "type": "NodeRefArrayElement",
            "target_node_id": "K093",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/53",
            "type": "NodeRefArrayElement",
            "target_node_id": "K092",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/54",
            "type": "NodeRefArrayElement",
            "target_node_id": "K094",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/55",
            "type": "NodeRefArrayElement",
            "target_node_id": "K102",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/56",
            "type": "NodeRefArrayElement",
            "target_node_id": "K106",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/57",
            "type": "NodeRefArrayElement",
            "target_node_id": "K105",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/58",
            "type": "NodeRefArrayElement",
            "target_node_id": "K107",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          },
          {
            "json_pointer": "/payload/ordered_evidence/59",
            "type": "NodeRefArrayElement",
            "target_node_id": "A009",
            "storage": "ARTIFACT_FIELD",
            "edge_authority": "TYPED_NODE_REF_FIELD"
          }
        ],
        "derived_direct_predecessors": [
          "A002",
          "K011",
          "A010",
          "K018",
          "K025",
          "K032",
          "K041",
          "K051",
          "K052P",
          "K067",
          "K068",
          "K079",
          "K082",
          "K083P",
          "K091",
          "K104",
          "K006",
          "K005",
          "K007",
          "K009",
          "K013",
          "K012",
          "K014",
          "K016",
          "K020",
          "K019",
          "K021",
          "K023",
          "K027",
          "K026",
          "K028",
          "K030",
          "K034",
          "K033",
          "K035",
          "K039",
          "K043",
          "K042",
          "K044",
          "K048",
          "K054",
          "K053",
          "K055",
          "K065",
          "K070",
          "K069",
          "K071",
          "K077",
          "K085",
          "K084",
          "K086",
          "K089",
          "K093",
          "K092",
          "K094",
          "K102",
          "K106",
          "K105",
          "K107",
          "A009"
        ],
        "node_specific_constants": {
          "check_id": "authorization_and_handoff_provenance",
          "denominator_expression": "CONST_60",
          "zero_population_permitted": false,
          "exact_ref_field_cardinalities": {
            "/payload/ordered_evidence": 60
          },
          "exact_direct_predecessor_count": 60
        },
        "node_specific_invariants": [
          "population=applicable+not_applicable",
          "applicable=pass+fail+incomplete",
          "status/effect/stop combination exact",
          "ordered_evidence[2] is A010",
          "A010 exact accepted and installed bytes are required for PASS",
          "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
        ]
      }
    },
    {
      "ordinal": 21,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/edge_derivation/declared_node_count",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "e0f05da93a0f5a86a3be5fc0e301606513c9f7e59dac2357348aa0f2f47db984",
      "new_value_jcs_sha256": "73d3f1ba062585bce51f77d70a26be88c44b55d70f81b8bd7e2ded030ca4454a",
      "new_value": 167
    },
    {
      "ordinal": 22,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/edge_derivation/declared_edge_count",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "cebe3d9d614ba5c19f633566104315854a11353a333bf96f16b5afa0e90abdc4",
      "new_value_jcs_sha256": "07bed92aab16ecdd9c886a79e44f0c0b02d70c746c593eaa3b8acf24e687bcd8",
      "new_value": 683
    },
    {
      "ordinal": 23,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/edge_derivation/schema_derived_node_count",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "e0f05da93a0f5a86a3be5fc0e301606513c9f7e59dac2357348aa0f2f47db984",
      "new_value_jcs_sha256": "73d3f1ba062585bce51f77d70a26be88c44b55d70f81b8bd7e2ded030ca4454a",
      "new_value": 167
    },
    {
      "ordinal": 24,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/edge_derivation/schema_derived_edge_count",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "cebe3d9d614ba5c19f633566104315854a11353a333bf96f16b5afa0e90abdc4",
      "new_value_jcs_sha256": "07bed92aab16ecdd9c886a79e44f0c0b02d70c746c593eaa3b8acf24e687bcd8",
      "new_value": 683
    },
    {
      "ordinal": 25,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/static_validation_contract/required_results/node_count",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "e0f05da93a0f5a86a3be5fc0e301606513c9f7e59dac2357348aa0f2f47db984",
      "new_value_jcs_sha256": "73d3f1ba062585bce51f77d70a26be88c44b55d70f81b8bd7e2ded030ca4454a",
      "new_value": 167
    },
    {
      "ordinal": 26,
      "operation": "ASSERT_EQUAL_REPLACE",
      "json_pointer": "/static_validation_contract/required_results/edge_count",
      "expected_old_state": "PRESENT",
      "expected_old_jcs_sha256": "cebe3d9d614ba5c19f633566104315854a11353a333bf96f16b5afa0e90abdc4",
      "new_value_jcs_sha256": "07bed92aab16ecdd9c886a79e44f0c0b02d70c746c593eaa3b8acf24e687bcd8",
      "new_value": 683
    }
  ],
  "stop_code_type": {
    "kind": "string",
    "enum": [
      "STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH",
      "STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH",
      "STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID",
      "STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET",
      "STOP_REGISTRY_OVERLAY_TARGET_MISSING",
      "STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE",
      "STOP_REGISTRY_OVERLAY_ALREADY_APPLIED",
      "STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH",
      "STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH",
      "STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH",
      "STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID"
    ]
  },
  "stop_inventory": {
    "schema_id": "pm_research.s2.registry_overlay_stop_inventory.v1",
    "stop_code_type": "RegistryOverlayStopCode",
    "stop_code_count": 11,
    "entries": [
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH",
        "trigger": "before any overlay or operation-engine evaluation, the externally supplied or selected registry JCS bytes differ in byte length or SHA-256 from the exact immutable accepted base identity",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH",
        "trigger": "after exact base verification, the supplied overlay JCS bytes, closed schema, or any embedded operation new-value hash differs from the exact overlay contract",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID",
        "trigger": "after exact base and overlay identity/schema/hash verification, operation ordinals are not the exact contiguous sequence or supplied operation order differs from the literal",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET",
        "trigger": "after exact base and overlay identity/schema/hash/order verification, two operations target the same JSON Pointer",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_TARGET_MISSING",
        "trigger": "the required parent does not exist for any operation, or an ASSERT_EQUAL_REPLACE target is absent after the common exact-new check",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE",
        "trigger": "an ASSERT_ABSENT_ADD target exists and differs from new_value, or an ASSERT_EQUAL_REPLACE current-target JCS SHA-256 differs from expected_old_jcs_sha256 after the common exact-new check",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_REGISTRY_OVERLAY_ALREADY_APPLIED",
        "trigger": "inside the verified-working-copy operation engine, the target exists and deep-equals the exact new_value; this common check precedes expected-old state or expected-old hash enforcement and is never used to classify an externally altered base input",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH",
        "trigger": "after graph and reducer postconditions pass, the serialized effective-registry bundle differs from its exact byte length or SHA-256, or atomic commit/exposure would publish a partial or non-identical result",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH",
        "trigger": "after one successful operation-engine invocation, the resolved semantic graph is not exactly 167 nodes, 683 direct edges, K127 population 60, and zero missing/extra/rank/cycle defects",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH",
        "trigger": "after graph reconciliation, the post-overlay projection of condition_state_classes and global_state_reducer differs from 66232 bytes and the accepted SHA-256",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      },
      {
        "stop_code": "STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID",
        "trigger": "A010 governed amendment identity is missing malformed additional conflicting or not the exact accepted installed identity",
        "effect": "HALT_NO_EFFECTIVE_REGISTRY"
      }
    ],
    "unregistered_stop_code_count": 0
  },
  "source_review_contract": {
    "schema_id": "pm_research.s2.registry_overlay_static_source_review.v3",
    "review_mode": "STATIC_SOURCE_REVIEW_ONLY",
    "required_checks": [
      "LAYER1_EXACT_BASE_IDENTITY_VERIFIED_BEFORE_OVERLAY_OR_ENGINE",
      "LAYER1_EXTERNAL_OR_SELECTED_NONBASE_REGISTRY_STOPS_AT_BASE_IDENTITY",
      "LAYER1_OVERLAY_IDENTITY_SCHEMA_AND_EMBEDDED_HASHES_VERIFIED",
      "LAYER1_OVERLAY_ORDINALS_CONTIGUOUS_AND_ORDER_EXACT",
      "LAYER1_OVERLAY_TARGETS_UNIQUE",
      "LAYER1_ONE_ISOLATED_COPY_FROM_VERIFIED_BASE",
      "LAYER1_OPERATION_ENGINE_INVOKED_EXACTLY_ONCE",
      "ZERO_OPERATION_ENGINE_INVOCATIONS_NO_EFFECTIVE_REGISTRY",
      "EXACTLY_ONE_REGISTERED_STOP_PER_DEFINED_FAILURE_STATE",
      "LAYER1_GRAPH_REDUCER_BUNDLE_POSTCONDITIONS_BEFORE_EXPOSURE",
      "FRESH_MATERIALIZER_INVOCATION_RESTARTS_FROM_EXACT_IMMUTABLE_BASE",
      "LAYER2_VERIFIED_WORKING_COPY_ONLY",
      "LAYER2_TOTAL_OPERATION_CLASSIFIER_PRECEDENCE_EXACT",
      "LAYER2_OPERATIONS_EVALUATED_IN_EXACT_ORDINAL_ORDER",
      "LAYER2_FIRST_CLASSIFIED_DEFECT_EMITS_EXACTLY_ONE_REGISTERED_STOP",
      "LAYER2_COMPLETE_ISOLATED_COPY_DISCARDED_ON_ANY_DEFECT",
      "LAYER2_SYNTHETIC_COUNTEREXAMPLES_NOT_EXTERNAL_BASE_INPUTS",
      "LAYER2_SECOND_INVOCATION_DEFENSIVE_NONPUBLISHING_ONLY",
      "LAYER2_DEFENSIVE_SECOND_INVOCATION_OPERATION0_ALREADY_APPLIED",
      "COMMIT_ONLY_AFTER_ALL_27_OPERATIONS_AND_POSTCONDITIONS",
      "ANY_POSTCONDITION_FAILURE_EMITS_APPLICABLE_EFFECTIVE_REGISTRY_STOP",
      "END_TO_END_AND_SYNTHETIC_PROOFS_SEPARATED",
      "EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MATCH",
      "EFFECTIVE_GRAPH_EXACT_167_NODES_683_EDGES",
      "K127_ORDERED_EVIDENCE_COUNT_EXACT_60",
      "MISSING_EXTRA_RANK_CYCLE_COUNTS_ZERO",
      "REDUCER_PROJECTION_IDENTITY_UNCHANGED",
      "OVERLAY_STOP_CODES_ALL_REGISTERED",
      "NO_RUNTIME_MARKDOWN_PARSE",
      "NO_NETWORK_REGISTRY_RETRIEVAL",
      "NO_ENVIRONMENT_SELECTED_OVERLAY",
      "NO_HAND_EDITED_EFFECTIVE_REGISTRY",
      "NO_UNVERIFIED_REGENERATION"
    ],
    "required_results": {
      "base_registry_byte_length": 479463,
      "base_registry_sha256": "82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff",
      "materializer_base_identity_gate_precedence": 1,
      "overlay_control_precedence": 2,
      "operation_classifier_precedence": 3,
      "graph_reconciliation_precedence": 4,
      "reducer_projection_precedence": 5,
      "effective_bundle_identity_precedence": 6,
      "commit_exposure_precedence": 7,
      "overlay_operation_count": 27,
      "overlay_duplicate_target_count": 0,
      "overlay_ordinal_error_count": 0,
      "materializer_operation_engine_invocation_count": 1,
      "fresh_materializer_prior_effective_registry_reuse_count": 0,
      "external_nonbase_operation_classifier_entry_count": 0,
      "defensive_second_engine_invocation_publish_count": 0,
      "effective_node_count": 167,
      "effective_edge_count": 683,
      "k127_ordered_evidence_count": 60,
      "missing_edge_count": 0,
      "extra_edge_count": 0,
      "rank_violation_count": 0,
      "cycle_count": 0,
      "reducer_projection_byte_length": 66232,
      "reducer_projection_sha256": "266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c",
      "registered_overlay_stop_code_count": 11,
      "unregistered_overlay_stop_code_count": 0,
      "operation_classifier_unmapped_assertion_count": 0,
      "partial_effective_registry_publish_count": 0,
      "atomic_commit_after_postconditions": true,
      "zero_engine_invocation_publish_count": 0,
      "defined_failure_multi_stop_count": 0
    },
    "failure_effect": "EMIT_HIGHEST_PRECEDENCE_REGISTERED_STOP_DISCARD_SESSION_NO_EXPOSURE",
    "execution_authorization": false
  },
  "postconditions": {
    "materializer_base_identity_verified": true,
    "operation_engine_invocation_count": 1,
    "application_count": 1,
    "effective_node_count": 167,
    "effective_direct_edge_count": 683,
    "k127_ordered_evidence_count": 60,
    "missing_edges": [],
    "extra_edges": [],
    "rank_violations": [],
    "cycles": [],
    "reducer_projection_identity": {
      "byte_length": 66232,
      "sha256": "266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c"
    },
    "partial_result_publish_count": 0,
    "authorization_effect": "NONE"
  }
}
```

### 3.5 Required two-layer materialization contract

The registry mechanism has two explicit layers. They are not interchangeable.

#### 3.5.1 Layer 1 — exact end-to-end materializer

A conforming future end-to-end materializer MUST perform these steps in exact order:

1. Select or receive the candidate base-registry JCS bytes.
2. Before parsing the overlay, constructing a working copy, inspecting an operation target, or invoking the operation engine, verify the base-registry JCS byte length and SHA-256 as exactly `479463` / `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`.
3. If the selected or supplied registry bytes differ in any way, emit only `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH`, expose no result, and halt. No overlay or operation-level stop may override this result.
4. Parse the verified base with duplicate object keys rejected. The exact verified base remains immutable.
5. Select or receive the overlay JCS bytes and verify exactly `45347` / `ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a`.
6. Validate the overlay closed schema, every embedded `new_value_jcs_sha256`, the exact stop enum and inventory, and `operation_count = array_length(operations) = 27`. Any overlay-byte, schema, or embedded-hash defect emits only `STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH`.
7. Validate ordinals as the exact contiguous sequence `0..26` in literal order. Failure emits only `STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID`.
8. Validate that all 27 `json_pointer` targets are unique. Failure emits only `STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET`.
9. Create exactly one isolated deep working copy from the exact verified base. No externally altered registry and no prior effective registry may be substituted.
10. Invoke the Layer-2 operation engine exactly once against that isolated copy.
11. If the engine emits a stop, discard the complete isolated copy and expose no result.
12. If the engine completes all 27 operations, validate the resolved graph as exactly `167` nodes, `683` direct edges, K127 population `60`, and zero missing, extra, rank-invalid, or cyclic edges. Failure emits only `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH`.
13. After graph reconciliation, extract exactly `condition_state_classes` and `global_state_reducer`, serialize the two-key projection as RFC 8785 JCS, and verify `66232` / `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`. Failure emits only `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH`.
14. Deep-freeze the resolved semantic registry.
15. Construct and verify the exact effective-registry bundle in §3.7. Failure emits only `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH`.
16. Commit and expose the isolated result atomically only after steps 1–15 succeed. A partial or non-atomic exposure is forbidden and is classified as `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH`; no partial result remains visible.

A fresh end-to-end materializer invocation MUST restart from the exact immutable base bytes in step 1. It MUST NOT use a prior effective registry as its input. A later fresh invocation that again starts from the exact base is not a second overlay application to the prior result; it is a new verified materializer session and independently follows steps 1–16.

#### 3.5.2 Layer 2 — verified-working-copy operation engine

The operation engine MAY receive only the isolated working copy created by Layer 1 after exact base verification. It MUST NOT accept an externally supplied registry, a prior effective registry, or an unverified object.

For each operation in exact ordinal order, the engine MUST resolve the required parent and inspect target state without mutating anything, then apply this total classifier:

1. **Common rule 1:** if the required parent does not exist, emit `STOP_REGISTRY_OVERLAY_TARGET_MISSING`.
2. **Common rule 2:** if the target exists and deep-equals the exact `new_value`, emit `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED`.
3. For `ASSERT_ABSENT_ADD` after the common rules:
   1. if the target exists and differs from `new_value`, emit `STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE`;
   2. if the target is absent, verify `SHA256(JCS(new_value)) = new_value_jcs_sha256` and stage the addition.
4. For `ASSERT_EQUAL_REPLACE` after the common rules:
   1. if the target is absent, emit `STOP_REGISTRY_OVERLAY_TARGET_MISSING`;
   2. if `SHA256(JCS(current_target)) != expected_old_jcs_sha256`, emit `STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE`;
   3. otherwise verify `SHA256(JCS(new_value)) = new_value_jcs_sha256` and stage the replacement.
5. No target-state assertion failure may exist outside rules 1–4.
6. Stop at the first classified defect, emit exactly one registered stop, discard the complete isolated copy including all staged prior changes, and publish nothing.
7. After a successful classifier and new-value hash check, apply only the current operation to the isolated copy and continue.

The end-to-end materializer MUST invoke this engine exactly once. A second invocation on the same already-amended working copy is permitted solely as a synthetic defensive-classification check outside the publishing materializer path. Such a second invocation:

- is not a fresh materializer invocation;
- does not re-run base verification;
- receives the same already-amended isolated copy;
- reaches operation `0`, whose target deep-equals the exact operation-0 `new_value`;
- emits `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED`;
- publishes no result and cannot replace the successful first materializer result.

#### 3.5.3 Complete stop precedence

When more than one hypothetical defect could be described, the first applicable level below controls and all lower levels are not evaluated:

1. **Base identity:** any selected or supplied non-exact base emits `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH`.
2. **Overlay controls, in sub-order:** byte identity, closed schema, or embedded new-value hash defect emits `STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH`; otherwise ordinal/order defect emits `STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID`; otherwise duplicate target emits `STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET`.
3. **Operation classifier inside the verified session:** the exact common-first and operation-specific mapping in §3.5.2.
4. **Graph reconciliation:** `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH`.
5. **Reducer projection:** `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH`.
6. **Effective-bundle identity:** `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH`.
7. **Commit/exposure:** reached only after levels 1–6 pass; any partial or non-atomic exposure is classified as `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH` and leaves no published result.

Every defined failure state emits exactly one registered stop. No normalization, best-effort repair, skipped operation, operation reordering, implicit idempotency, environment-selected behavior, fallback, partial publication, or multi-stop emission is permitted.

### 3.6 Separated materializer and classifier proofs

#### 3.6.1 End-to-end materializer outcomes

| End-to-end input or state | Required result |
|---|---|
| exact immutable base plus exact overlay, one engine invocation | success only at exact `167 / 683`, K127 `60`, unchanged reducer projection, exact bundle; atomic exposure permitted |
| selected or supplied base bytes altered in any way | `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH`; overlay and engine are not evaluated |
| zero operation-engine invocations | no effective registry may publish |
| operation engine emits any classified defect | exactly that one registered stop; complete isolated copy discarded |
| graph postcondition failure | `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH` |
| reducer postcondition failure | `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH` |
| effective-bundle or atomic-exposure failure | `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH`; no partial result |
| a later fresh materializer invocation | starts again from the exact immutable base; it is not a second application to a prior effective registry |

#### 3.6.2 Synthetic operation-classifier counterexamples

These cases are evaluated only against explicitly synthetic working-copy states derived after Layer-1 base verification. They are not externally altered accepted-base inputs and cannot publish an effective registry.

| Synthetic working-copy state | Required engine result |
|---|---|
| target exists and deep-equals exact `new_value` | `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED` |
| `ASSERT_ABSENT_ADD` target exists and conflicts with `new_value` | `STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE` |
| `ASSERT_EQUAL_REPLACE` target absent while required parent exists | `STOP_REGISTRY_OVERLAY_TARGET_MISSING` |
| required parent absent | `STOP_REGISTRY_OVERLAY_TARGET_MISSING` |
| replace target present with correct expected-old hash | verify new-value hash and stage replacement |
| add target absent | verify new-value hash and stage addition |

#### 3.6.3 Defensive second-engine invocation

After one complete engine application to the same isolated working copy, a synthetic second engine invocation reaches operation `0` and emits `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED`. This proof does not re-run Layer 1, does not characterize a fresh materializer invocation, and publishes no result.

The graph arithmetic for one successful Layer-1 session remains exact:

```text
base nodes = 166
base edges = 678
A010 node = +1
A010 -> K011 = +1 edge
K013 -> A010 = +1 edge
K012 -> A010 = +1 edge
K014 -> A010 = +1 edge
K127 -> A010 = +1 edge

effective nodes = 167
effective edges = 683
```

The common exact-new check still precedes expected-old state and expected-old hash enforcement inside Layer 2. The Layer-1 base identity gate ensures that an externally altered base can never be mislabeled with an operation-level stop.

### 3.7 Exact effective post-overlay registry JCS

The effective registry remains a **closed composite registry bundle**, not a third flattened semantic literal. Candidate 04 additionally binds the exact materializer-session boundary: exact base verification precedes overlay and engine evaluation, one engine invocation occurs within the session, no prior effective registry is reused, and exposure occurs only after graph, reducer, and bundle postconditions.

The bundle field `application_count = 1` means one successful operation-engine application inside the materializer session represented by the bundle. It is not a global count across fresh materializer invocations.

Exact effective-registry bundle identity:

| Field | Exact value |
|---|---|
| JCS byte length | `1266` |
| JCS SHA-256 | `075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67` |
| Materializer input | exact immutable base |
| Operation-engine invocation count | `1` |
| Prior effective-registry reuse count | `0` |
| Effective graph | `167 / 683` |
| K127 population | `60` |
| Reducer projection | unchanged |
| Authorization effect | `NONE` |

Exact RFC 8785 JCS bytes:

```json
{"application_count":1,"application_profile_id":"EXACT_BASE_MATERIALIZER_VERIFIED_WORKING_COPY_ENGINE_V3","authorization_effect":"NONE","base_registry_identity":{"byte_length":479463,"schema_registry_id":"pm_research.s2.candidate08.complete_node_schema_registry.v5","sha256":"82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff"},"graph_overlay_identity":{"byte_length":45347,"overlay_id":"S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_OVERLAY_04","sha256":"ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a"},"materializer_session":{"base_verified_before_overlay":true,"fresh_invocation_source":"EXACT_IMMUTABLE_BASE","operation_engine_invocation_count":1,"prior_effective_registry_reuse_count":0,"result_exposure":"AFTER_GRAPH_REDUCER_AND_BUNDLE_POSTCONDITIONS"},"reducer_projection_identity":{"byte_length":66232,"sha256":"266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c"},"resolved_semantic_registry":{"cycles":[],"direct_edge_count":683,"extra_edges":[],"k127_ordered_evidence_count":60,"missing_edges":[],"node_count":167,"rank_violations":[],"representation":"DEEP_FROZEN_RESULT_OF_ONE_ENGINE_INVOCATION_FROM_EXACT_VERIFIED_BASE"},"schema_id":"pm_research.s2.effective_registry_bundle.v2"}
```

A flattened hand-edited full-registry literal is forbidden. A future source file MAY serialize the bundle for identity checking, but the only generated semantic literals permitted are the immutable base and exact overlay.

### 3.8 Reducer-projection byte-identity proof

The overlay operation target set contains no pointer equal to or descending from:

- `/condition_state_classes`;
- `/global_state_reducer`.

The accepted reducer projection is defined only from those two complete base-registry values. Therefore one successful engine application within a verified exact-base materializer session leaves the projection value unchanged. A conforming materializer MUST nevertheless serialize and verify the post-overlay projection as:

`66232` bytes / `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`

Any mismatch is `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH`. The accepted scientific state classes and reducer semantics are not amended.

### 3.9 Future `schema_registry.py` obligations

Within the accepted fourteen-file boundary, future `pm_research/named_binary_probe_s2/schema_registry.py` MUST contain exactly:

1. one generated base64 literal decoding to the immutable base-registry JCS bytes;
2. one generated base64 literal decoding to the exact overlay JCS bytes.

It MUST declare exact constants:

```text
BASE_REGISTRY_JCS_BYTE_LENGTH = 479463
BASE_REGISTRY_JCS_SHA256 = "82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff"
GRAPH_OVERLAY_JCS_BYTE_LENGTH = 45347
GRAPH_OVERLAY_JCS_SHA256 = "ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a"
EFFECTIVE_REGISTRY_BUNDLE_JCS_BYTE_LENGTH = 1266
EFFECTIVE_REGISTRY_BUNDLE_JCS_SHA256 = "075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67"
REDUCER_PROJECTION_JCS_BYTE_LENGTH = 66232
REDUCER_PROJECTION_JCS_SHA256 = "266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c"
REGISTRY_OVERLAY_APPLICATION_PROFILE = "EXACT_BASE_MATERIALIZER_VERIFIED_WORKING_COPY_ENGINE_V3"
```

It MUST NOT:

- contain a third semantic-registry literal;
- hand-edit the base or resolved semantic object;
- parse Candidate-08 or amendment Markdown at runtime;
- retrieve a registry or overlay from a network source;
- select an overlay from an environment variable, command-line option, config file, current Git branch, or current commit;
- silently regenerate either literal from different bytes;
- continue after any identity, schema, old-value, order, count, graph, stop-registration, or reducer mismatch.

Future static source review MUST establish every required check and exact result in `overlay.source_review_contract`. Naming that review does not authorize source authoring, imports, or execution.

---

## 4. A010 closed governed-amendment payload

### 4.1 Dedicated type

Add exact `type_registry.GovernedAmendmentIdentity`:

```json
{
  "kind": "object",
  "required": [
    "logical_path",
    "byte_length",
    "sha256",
    "installation_commit",
    "authorization_effect"
  ],
  "fields": {
    "logical_path": "Const[project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md]",
    "byte_length": "Const[24599]",
    "sha256": "Const[8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63]",
    "installation_commit": "Const[e675a47ec2c8f6cd769c2673afc16d96e5622ccd]",
    "authorization_effect": "Const[NONE]"
  },
  "additional_fields": false,
  "constraints": [
    "all five fields are mandatory and non-null",
    "missing malformed additional conflicting or alternate amendment identity is invalid",
    "identity fields are typed governance identity data and create no provenance edge"
  ]
}
```

The five identity fields are typed non-edge fields. They MUST NOT be traversed by the edge extractor.

### 4.2 Dedicated profile

Add exact `artifact_profiles.amendment_governance.v1`:

```json
{
  "media_type": "text/markdown",
  "serialization": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
  "required_fields": [
    "/document_id",
    "/status",
    "/canonical_commit",
    "/activity_root",
    "/normative_input_refs",
    "/governed_amendment_identity",
    "/normative_sections",
    "/authorization_effect"
  ],
  "fields": {
    "/document_id": {
      "type": "Const[S2_CANDIDATE_08_IMPLEMENTATION_SOURCE_AUTHORIZATION_GRAPH_AMENDMENT_01_CANDIDATE_04]",
      "nullable": false
    },
    "/status": {
      "type": "Const[SPEC_ONLY_GRAPH_AMENDMENT_REVIEW_CANDIDATE]",
      "nullable": false
    },
    "/canonical_commit": {
      "type": "Const[90c0059c0e86b7afd44fcf9f17223d68eab1a9e0]",
      "nullable": false
    },
    "/activity_root": {
      "type": "Const[null]",
      "nullable": true
    },
    "/normative_input_refs": {
      "type": "Array<NodeRef>",
      "min_items": 1,
      "max_items": 1,
      "nullable": false
    },
    "/governed_amendment_identity": {
      "type": "GovernedAmendmentIdentity",
      "nullable": false
    },
    "/normative_sections": {
      "type": "Array<RecordId>",
      "min_items": 1,
      "nullable": false
    },
    "/authorization_effect": {
      "type": "Const[NONE]",
      "nullable": false
    }
  },
  "node_ref_slots": {
    "/normative_input_refs": "array"
  },
  "non_edge_identity_slots": {
    "/governed_amendment_identity": "GovernedAmendmentIdentity"
  },
  "additional_fields": false,
  "ordering": [
    "normative_input_refs exact singleton K011",
    "normative_sections exact document order"
  ],
  "uniqueness": [
    "normative_input_refs.node_id",
    "normative_sections"
  ],
  "equations": [
    "array_length(normative_input_refs)=1"
  ],
  "constraints": [
    "activity_root is exactly null",
    "normative_input_refs[0] is exact K011 1134 bytes and authoritative SHA-256",
    "governed_amendment_identity exactly equals the accepted installed Amendment-01 identity",
    "governed_amendment_identity creates no direct edge",
    "authorization_effect=NONE",
    "no implementation or execution authorization"
  ]
}
```

The profile rejects:

- a missing governed identity;
- malformed path, byte length, SHA-256, commit, or authorization effect;
- any additional field;
- an alternate amendment path or identity;
- a conflict between payload and exact profile constants;
- a non-null activity root;
- zero, two, duplicate, or non-K011 normative input refs.

### 4.3 Exact A010 node entry

```json
{
  "rank": 1115,
  "semantic_role": "implementation_source_authorization_graph_amendment_governance",
  "artifact_profile_id": "amendment_governance.v1",
  "ref_bindings": [
    {
      "json_pointer": "/normative_input_refs/0",
      "type": "NodeRefArrayElement",
      "target_node_id": "K011",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    }
  ],
  "derived_direct_predecessors": [
    "K011"
  ],
  "node_specific_constants": {
    "exact_ref_field_cardinalities": {
      "/normative_input_refs": 1
    },
    "exact_direct_predecessor_count": 1,
    "exact_governed_amendment_identity": {
      "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01.md",
      "byte_length": 24599,
      "sha256": "8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63",
      "installation_commit": "e675a47ec2c8f6cd769c2673afc16d96e5622ccd",
      "authorization_effect": "NONE"
    }
  },
  "node_specific_invariants": [
    "A010 validates amendment_governance.v1",
    "A010 has exactly one graph predecessor K011",
    "governed_amendment_identity is exact and creates no graph edge",
    "authorization_effect is NONE",
    "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
  ],
  "raw_media_type_override": "text/markdown; charset=utf-8",
  "raw_serialization_override": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
  "payload_extraction_rule": "exactly one fenced JSON block immediately following NORMATIVE_A010_PAYLOAD; parse as JSON; validate amendment_governance.v1; derive only K011 from /normative_input_refs/0"
}
```

A010 has exactly one graph predecessor: K011. The governed Amendment-01 identity does not create a second edge or node.

A010 is available to successors only after Sentinel accepts exact Candidate-04 bytes, a separately authorized canonical installation occurs, and Sentinel verifies the exact installed A010 NodeRef. Until then, `AUTHORIZATION_PREREQUISITE_BYTES_MISSING` blocks K013.

---

## 5. Exact K013, K012, and K014 replacements

Existing profile-level `additional_prerequisites` support remains mechanically sufficient.

### 5.1 K013

```json
{
  "rank": 1120,
  "semantic_role": "gustavo_implementation_source_authorization",
  "artifact_profile_id": "gustavo_authorization.v1",
  "ref_bindings": [
    {
      "json_pointer": "/payload/prerequisite_acceptance",
      "type": "NodeRef",
      "target_node_id": "K011",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/additional_prerequisites/0",
      "type": "NodeRefArrayElement",
      "target_node_id": "A010",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    }
  ],
  "derived_direct_predecessors": [
    "K011",
    "A010"
  ],
  "node_specific_constants": {
    "exact_ref_field_cardinalities": {
      "/payload/prerequisite_acceptance": 1,
      "/payload/additional_prerequisites": 1
    },
    "exact_direct_predecessor_count": 2
  },
  "node_specific_invariants": [
    "additional_prerequisites is present and equals [A010]",
    "K011 remains the prerequisite_acceptance",
    "fresh bytes are created only after exact accepted and canonically installed A010 identity exists",
    "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
  ]
}
```

K013 retains K011 and adds A010. K013 MUST be fresh and post-A010 installation.

### 5.2 K012

```json
{
  "rank": 1130,
  "semantic_role": "sentinel_implementation_source_authorization",
  "artifact_profile_id": "sentinel_authorization.v1",
  "ref_bindings": [
    {
      "json_pointer": "/payload/prerequisite_acceptance",
      "type": "NodeRef",
      "target_node_id": "K011",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/additional_prerequisites/0",
      "type": "NodeRefArrayElement",
      "target_node_id": "A010",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/gustavo_authorization",
      "type": "NodeRef",
      "target_node_id": "K013",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    }
  ],
  "derived_direct_predecessors": [
    "K011",
    "A010",
    "K013"
  ],
  "node_specific_constants": {
    "exact_ref_field_cardinalities": {
      "/payload/prerequisite_acceptance": 1,
      "/payload/additional_prerequisites": 1,
      "/payload/gustavo_authorization": 1
    },
    "exact_direct_predecessor_count": 3
  },
  "node_specific_invariants": [
    "additional_prerequisites is present and equals [A010]",
    "K011 remains the prerequisite_acceptance",
    "K013 exact bytes preexist K012 and bind the same K011 and A010 identities",
    "K012 created_at_utc_ms is greater than K013 created_at_utc_ms",
    "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
  ]
}
```

K012 retains K011, adds A010, and binds exact fresh K013. K013 precedes K012.

### 5.3 K014

```json
{
  "rank": 1140,
  "semantic_role": "implementation_source_activity_root",
  "artifact_profile_id": "activity_root.v1",
  "ref_bindings": [
    {
      "json_pointer": "/payload/prerequisite_acceptance",
      "type": "NodeRef",
      "target_node_id": "K011",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/additional_prerequisites/0",
      "type": "NodeRefArrayElement",
      "target_node_id": "A010",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/gustavo_authorization",
      "type": "NodeRef",
      "target_node_id": "K013",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/sentinel_stage_authorization",
      "type": "NodeRef",
      "target_node_id": "K012",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    }
  ],
  "derived_direct_predecessors": [
    "K011",
    "A010",
    "K013",
    "K012"
  ],
  "node_specific_constants": {
    "exact_ref_field_cardinalities": {
      "/payload/prerequisite_acceptance": 1,
      "/payload/additional_prerequisites": 1,
      "/payload/gustavo_authorization": 1,
      "/payload/sentinel_stage_authorization": 1
    },
    "exact_direct_predecessor_count": 4
  },
  "node_specific_invariants": [
    "additional_prerequisites is present and equals [A010]",
    "K011 remains the prerequisite_acceptance",
    "K013 and K012 exact bytes preexist K014 and bind the same K011 and A010 identities",
    "K014 created_at_utc_ms is greater than both K013 and K012 created_at_utc_ms",
    "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
  ]
}
```

K014 retains K011, adds A010, and binds exact fresh K013 and K012. Both authorizations precede K014.

### 5.4 Exact materialization order

```text
accepted K011
  -> Sentinel-accepted and canonically verified A010
  -> fresh K013 Gustavo authorization
  -> fresh K012 Sentinel stage authorization
  -> fresh K014 activity root
  -> K015/K016
```

K013 MUST NOT reference K012. A010 MUST NOT reference K013, K012, or K014. K012 before K013 or K014 before either authorization is `STOP_AUTHORIZATION_ORDER_INVALID`.

---

## 6. Preserved K015 and K016 boundaries

| Node | Exact direct predecessors | Count |
|---|---|---:|
| `K015` | `K014` | `1` |
| `K016` | `K013`, `K012`, `K014`, `K015` | `4` |

No direct A010 edge from K015 or K016 is permitted.

The overlay materializes the accepted Amendment-01 fourteen-path package, K015 sorting/path rules, and K016 `self_identity = null` rule without altering those direct-predecessor sets.

The exact fourteen implementation paths remain:

1. `pm_research/named_binary_probe_s2/__init__.py` — `package_export`
2. `pm_research/named_binary_probe_s2/acquisition.py` — `independent_token_acquisition_and_raw_closure`
3. `pm_research/named_binary_probe_s2/alignment.py` — `accepted_policy_alignment`
4. `pm_research/named_binary_probe_s2/audit.py` — `nineteen_audit_closures_and_gate`
5. `pm_research/named_binary_probe_s2/construction.py` — `scientific_construction_and_deduplication`
6. `pm_research/named_binary_probe_s2/prices_history_contract.py` — `endpoint_response_terminal_and_retry_contract`
7. `pm_research/named_binary_probe_s2/rebuild.py` — `isolated_rebuild_and_byte_comparison`
8. `pm_research/named_binary_probe_s2/request_plan.py` — `deterministic_request_plan`
9. `pm_research/named_binary_probe_s2/s4_inputs.py` — `s4_input_parsers_and_reconciliation`
10. `pm_research/named_binary_probe_s2/safe_span.py` — `safe_span_classifier_and_reducer`
11. `pm_research/named_binary_probe_s2/schema_registry.py` — `schema_registry_and_edge_derivation`
12. `pm_research/named_binary_probe_s2/state_reducers.py` — `global_condition_transition_state_reducers`
13. `pm_research/named_binary_probe_s2/transition.py` — `stage10_transition_reconciliation`
14. `pm_research/named_binary_probe_s2/types.py` — `closed_types_and_jcs`

No fifteenth source file, `src/` layout, namespace-package behavior, or `pyproject.toml` modification is permitted.

---

## 7. Definitive K127 reconciliation

### 7.1 Decision

A010 remains a direct K127 evidence item immediately after K011. No existing K127 evidence item is removed, and all preexisting items retain their relative order.

### 7.2 Exact ordered evidence

| Index | Node |
|---:|---|
| `0` | `A002` |
| `1` | `K011` |
| `2` | `A010` |
| `3` | `K018` |
| `4` | `K025` |
| `5` | `K032` |
| `6` | `K041` |
| `7` | `K051` |
| `8` | `K052P` |
| `9` | `K067` |
| `10` | `K068` |
| `11` | `K079` |
| `12` | `K082` |
| `13` | `K083P` |
| `14` | `K091` |
| `15` | `K104` |
| `16` | `K006` |
| `17` | `K005` |
| `18` | `K007` |
| `19` | `K009` |
| `20` | `K013` |
| `21` | `K012` |
| `22` | `K014` |
| `23` | `K016` |
| `24` | `K020` |
| `25` | `K019` |
| `26` | `K021` |
| `27` | `K023` |
| `28` | `K027` |
| `29` | `K026` |
| `30` | `K028` |
| `31` | `K030` |
| `32` | `K034` |
| `33` | `K033` |
| `34` | `K035` |
| `35` | `K039` |
| `36` | `K043` |
| `37` | `K042` |
| `38` | `K044` |
| `39` | `K048` |
| `40` | `K054` |
| `41` | `K053` |
| `42` | `K055` |
| `43` | `K065` |
| `44` | `K070` |
| `45` | `K069` |
| `46` | `K071` |
| `47` | `K077` |
| `48` | `K085` |
| `49` | `K084` |
| `50` | `K086` |
| `51` | `K089` |
| `52` | `K093` |
| `53` | `K092` |
| `54` | `K094` |
| `55` | `K102` |
| `56` | `K106` |
| `57` | `K105` |
| `58` | `K107` |
| `59` | `A009` |

### 7.3 Exact K127 node replacement

```json
{
  "rank": 2320,
  "semantic_role": "authorization_and_handoff_provenance_closure",
  "artifact_profile_id": "audit_closure.v1",
  "ref_bindings": [
    {
      "json_pointer": "/payload/ordered_evidence/0",
      "type": "NodeRefArrayElement",
      "target_node_id": "A002",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/1",
      "type": "NodeRefArrayElement",
      "target_node_id": "K011",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/2",
      "type": "NodeRefArrayElement",
      "target_node_id": "A010",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/3",
      "type": "NodeRefArrayElement",
      "target_node_id": "K018",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/4",
      "type": "NodeRefArrayElement",
      "target_node_id": "K025",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/5",
      "type": "NodeRefArrayElement",
      "target_node_id": "K032",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/6",
      "type": "NodeRefArrayElement",
      "target_node_id": "K041",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/7",
      "type": "NodeRefArrayElement",
      "target_node_id": "K051",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/8",
      "type": "NodeRefArrayElement",
      "target_node_id": "K052P",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/9",
      "type": "NodeRefArrayElement",
      "target_node_id": "K067",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/10",
      "type": "NodeRefArrayElement",
      "target_node_id": "K068",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/11",
      "type": "NodeRefArrayElement",
      "target_node_id": "K079",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/12",
      "type": "NodeRefArrayElement",
      "target_node_id": "K082",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/13",
      "type": "NodeRefArrayElement",
      "target_node_id": "K083P",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/14",
      "type": "NodeRefArrayElement",
      "target_node_id": "K091",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/15",
      "type": "NodeRefArrayElement",
      "target_node_id": "K104",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/16",
      "type": "NodeRefArrayElement",
      "target_node_id": "K006",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/17",
      "type": "NodeRefArrayElement",
      "target_node_id": "K005",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/18",
      "type": "NodeRefArrayElement",
      "target_node_id": "K007",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/19",
      "type": "NodeRefArrayElement",
      "target_node_id": "K009",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/20",
      "type": "NodeRefArrayElement",
      "target_node_id": "K013",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/21",
      "type": "NodeRefArrayElement",
      "target_node_id": "K012",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/22",
      "type": "NodeRefArrayElement",
      "target_node_id": "K014",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/23",
      "type": "NodeRefArrayElement",
      "target_node_id": "K016",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/24",
      "type": "NodeRefArrayElement",
      "target_node_id": "K020",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/25",
      "type": "NodeRefArrayElement",
      "target_node_id": "K019",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/26",
      "type": "NodeRefArrayElement",
      "target_node_id": "K021",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/27",
      "type": "NodeRefArrayElement",
      "target_node_id": "K023",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/28",
      "type": "NodeRefArrayElement",
      "target_node_id": "K027",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/29",
      "type": "NodeRefArrayElement",
      "target_node_id": "K026",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/30",
      "type": "NodeRefArrayElement",
      "target_node_id": "K028",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/31",
      "type": "NodeRefArrayElement",
      "target_node_id": "K030",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/32",
      "type": "NodeRefArrayElement",
      "target_node_id": "K034",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/33",
      "type": "NodeRefArrayElement",
      "target_node_id": "K033",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/34",
      "type": "NodeRefArrayElement",
      "target_node_id": "K035",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/35",
      "type": "NodeRefArrayElement",
      "target_node_id": "K039",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/36",
      "type": "NodeRefArrayElement",
      "target_node_id": "K043",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/37",
      "type": "NodeRefArrayElement",
      "target_node_id": "K042",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/38",
      "type": "NodeRefArrayElement",
      "target_node_id": "K044",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/39",
      "type": "NodeRefArrayElement",
      "target_node_id": "K048",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/40",
      "type": "NodeRefArrayElement",
      "target_node_id": "K054",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/41",
      "type": "NodeRefArrayElement",
      "target_node_id": "K053",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/42",
      "type": "NodeRefArrayElement",
      "target_node_id": "K055",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/43",
      "type": "NodeRefArrayElement",
      "target_node_id": "K065",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/44",
      "type": "NodeRefArrayElement",
      "target_node_id": "K070",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/45",
      "type": "NodeRefArrayElement",
      "target_node_id": "K069",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/46",
      "type": "NodeRefArrayElement",
      "target_node_id": "K071",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/47",
      "type": "NodeRefArrayElement",
      "target_node_id": "K077",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/48",
      "type": "NodeRefArrayElement",
      "target_node_id": "K085",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/49",
      "type": "NodeRefArrayElement",
      "target_node_id": "K084",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/50",
      "type": "NodeRefArrayElement",
      "target_node_id": "K086",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/51",
      "type": "NodeRefArrayElement",
      "target_node_id": "K089",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/52",
      "type": "NodeRefArrayElement",
      "target_node_id": "K093",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/53",
      "type": "NodeRefArrayElement",
      "target_node_id": "K092",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/54",
      "type": "NodeRefArrayElement",
      "target_node_id": "K094",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/55",
      "type": "NodeRefArrayElement",
      "target_node_id": "K102",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/56",
      "type": "NodeRefArrayElement",
      "target_node_id": "K106",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/57",
      "type": "NodeRefArrayElement",
      "target_node_id": "K105",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/58",
      "type": "NodeRefArrayElement",
      "target_node_id": "K107",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    },
    {
      "json_pointer": "/payload/ordered_evidence/59",
      "type": "NodeRefArrayElement",
      "target_node_id": "A009",
      "storage": "ARTIFACT_FIELD",
      "edge_authority": "TYPED_NODE_REF_FIELD"
    }
  ],
  "derived_direct_predecessors": [
    "A002",
    "K011",
    "A010",
    "K018",
    "K025",
    "K032",
    "K041",
    "K051",
    "K052P",
    "K067",
    "K068",
    "K079",
    "K082",
    "K083P",
    "K091",
    "K104",
    "K006",
    "K005",
    "K007",
    "K009",
    "K013",
    "K012",
    "K014",
    "K016",
    "K020",
    "K019",
    "K021",
    "K023",
    "K027",
    "K026",
    "K028",
    "K030",
    "K034",
    "K033",
    "K035",
    "K039",
    "K043",
    "K042",
    "K044",
    "K048",
    "K054",
    "K053",
    "K055",
    "K065",
    "K070",
    "K069",
    "K071",
    "K077",
    "K085",
    "K084",
    "K086",
    "K089",
    "K093",
    "K092",
    "K094",
    "K102",
    "K106",
    "K105",
    "K107",
    "A009"
  ],
  "node_specific_constants": {
    "check_id": "authorization_and_handoff_provenance",
    "denominator_expression": "CONST_60",
    "zero_population_permitted": false,
    "exact_ref_field_cardinalities": {
      "/payload/ordered_evidence": 60
    },
    "exact_direct_predecessor_count": 60
  },
  "node_specific_invariants": [
    "population=applicable+not_applicable",
    "applicable=pass+fail+incomplete",
    "status/effect/stop combination exact",
    "ordered_evidence[2] is A010",
    "A010 exact accepted and installed bytes are required for PASS",
    "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
  ]
}
```

K127's exact population is `60`. Its equations remain:

```text
population_count = applicable_count + not_applicable_count
applicable_count = pass_count + fail_count + incomplete_count
```

Missing accepted/installed A010 bytes produce the already registered `AUTHORIZATION_PREREQUISITE_BYTES_MISSING`. An absent, extra, duplicate, misordered, or identity-conflicting K127 edge produces `PROVENANCE_EDGE_SET_MISMATCH`.

---

## 8. Exact graph reconciliation

| Item | Base | Delta | Effective |
|---|---:|---:|---:|
| Nodes | `166` | `+1` | `167` |
| Direct edges | `678` | `+5` | `683` |
| K127 ordered evidence | `59` | `+1` | `60` |
| K015 direct predecessors | `1` | `0` | `1` |
| K016 direct predecessors | `4` | `0` | `4` |

Exact changed Appendix-A rows:

| Target | Amended rank | Exact ordered direct predecessors |
|---|---:|---|
| `A010` | `1115` | `K011` |
| `K013` | `1120` | `K011`, `A010` |
| `K012` | `1130` | `K011`, `A010`, `K013` |
| `K014` | `1140` | `K011`, `A010`, `K013`, `K012` |
| `K127` | `2320` | exact 60-entry sequence in §7.2 |

The graph is conforming only when all are exact:

```json
{
  "declared_node_count": 167,
  "declared_edge_count": 683,
  "schema_derived_node_count": 167,
  "schema_derived_edge_count": 683,
  "missing_edges": [],
  "extra_edges": [],
  "rank_violations": [],
  "cycles": []
}
```

No empirical or runtime claim is made. This is declarative graph arithmetic over exact typed bindings.

---

## 9. Closed stop registration

### 9.1 New overlay stop-code type and inventory

Every new stop introduced by this amendment belongs to the closed `RegistryOverlayStopCode` enum. The exact enum and exact inventory are embedded in the overlay and added to the effective registry by operations 11 and 12.

| Ordinal | Stop code | Exact trigger | Effect |
|---:|---|---|---|
| `0` | `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH` | before any overlay or operation-engine evaluation, the externally supplied or selected registry JCS bytes differ in byte length or SHA-256 from the exact immutable accepted base identity | `HALT_NO_EFFECTIVE_REGISTRY` |
| `1` | `STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH` | after exact base verification, the supplied overlay JCS bytes, closed schema, or any embedded operation new-value hash differs from the exact overlay contract | `HALT_NO_EFFECTIVE_REGISTRY` |
| `2` | `STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID` | after exact base and overlay identity/schema/hash verification, operation ordinals are not the exact contiguous sequence or supplied operation order differs from the literal | `HALT_NO_EFFECTIVE_REGISTRY` |
| `3` | `STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET` | after exact base and overlay identity/schema/hash/order verification, two operations target the same JSON Pointer | `HALT_NO_EFFECTIVE_REGISTRY` |
| `4` | `STOP_REGISTRY_OVERLAY_TARGET_MISSING` | the required parent does not exist for any operation, or an ASSERT_EQUAL_REPLACE target is absent after the common exact-new check | `HALT_NO_EFFECTIVE_REGISTRY` |
| `5` | `STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE` | an ASSERT_ABSENT_ADD target exists and differs from new_value, or an ASSERT_EQUAL_REPLACE current-target JCS SHA-256 differs from expected_old_jcs_sha256 after the common exact-new check | `HALT_NO_EFFECTIVE_REGISTRY` |
| `6` | `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED` | inside the verified-working-copy operation engine, the target exists and deep-equals the exact new_value; this common check precedes expected-old state or expected-old hash enforcement and is never used to classify an externally altered base input | `HALT_NO_EFFECTIVE_REGISTRY` |
| `7` | `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH` | after graph and reducer postconditions pass, the serialized effective-registry bundle differs from its exact byte length or SHA-256, or atomic commit/exposure would publish a partial or non-identical result | `HALT_NO_EFFECTIVE_REGISTRY` |
| `8` | `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH` | after one successful operation-engine invocation, the resolved semantic graph is not exactly 167 nodes, 683 direct edges, K127 population 60, and zero missing/extra/rank/cycle defects | `HALT_NO_EFFECTIVE_REGISTRY` |
| `9` | `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH` | after graph reconciliation, the post-overlay projection of condition_state_classes and global_state_reducer differs from 66232 bytes and the accepted SHA-256 | `HALT_NO_EFFECTIVE_REGISTRY` |
| `10` | `STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID` | A010 governed amendment identity is missing malformed additional conflicting or not the exact accepted installed identity | `HALT_NO_EFFECTIVE_REGISTRY` |

Exact counts:

```text
RegistryOverlayStopCode enum members = 11
registry_overlay_stop_inventory entries = 11
registered_overlay_stop_code_count = 11
unregistered_overlay_stop_code_count = 0
```

The Layer-1 base stop has absolute precedence over overlay and operation-engine stops. The operation-level stops are reachable only inside a verified materializer session. These stops govern static registry-literal materialization and source review. They do not enter `GlobalDefect`, do not modify `GlobalHaltCode`, and do not alter the reducer projection.

### 9.2 Reused existing registered stops

| Condition | Existing exact stop | Registration |
|---|---|---|
| canonical base mismatch | `STOP_CANONICAL_BASE_MISMATCH` | existing `GlobalHaltCode` |
| K011 or accepted Amendment-01 exact raw identity mismatch | `STOP_INPUT_IDENTITY_MISMATCH` | existing `GlobalHaltCode` |
| accepted/installed A010 bytes unavailable to a successor | `AUTHORIZATION_PREREQUISITE_BYTES_MISSING` | existing `GlobalHaltCode` |
| K013/K012/K014 temporal order invalid | `STOP_AUTHORIZATION_ORDER_INVALID` | existing `GlobalHaltCode` |
| successor bindings disagree on K011 or A010 | `STOP_AUTHORIZATION_PROVENANCE_INVALID` | existing `GlobalHaltCode` |
| effective graph or Appendix equality mismatch | `PROVENANCE_EDGE_SET_MISMATCH` | existing `GlobalHaltCode` |
| any prohibited activity attempted | `STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED` | existing `GlobalHaltCode` |

No other normative stop code appears in this amendment. Zero unregistered stop codes are permitted.

---

## 10. Exhaustive graph-count and graph-role replacement table

A static search of accepted Candidate-08 text identified the following distinct graph-count-bearing or graph-role-bearing locations. Each is amended exactly as shown; no generic “where applicable” replacement is normative.

| Exact location | Old value | New value | Mechanism |
|---|---|---|---|
| Candidate-08 opening checkable completion sentence | `166 nodes and 678 direct edges` | `167 nodes and 683 direct edges` | prose replacement |
| Candidate-08 §21 missing-schema-edge counterexample | `166/678 equality scan` | `167/683 equality scan` | prose replacement |
| §23 `/test_source_matrix/0/role` | `schema_and_678_edge_equality` | `schema_and_683_edge_equality` | overlay op 18 |
| §23 `/nodes/K022/node_specific_constants/exact_test_file_matrix/0/role` | `schema_and_678_edge_equality` | `schema_and_683_edge_equality` | overlay op 19 |
| §23 `/edge_derivation/declared_node_count` | `166` | `167` | overlay op 21 |
| §23 `/edge_derivation/declared_edge_count` | `678` | `683` | overlay op 22 |
| §23 `/edge_derivation/schema_derived_node_count` | `166` | `167` | overlay op 23 |
| §23 `/edge_derivation/schema_derived_edge_count` | `678` | `683` | overlay op 24 |
| §23 `/static_validation_contract/required_results/node_count` | `166` | `167` | overlay op 25 |
| §23 `/static_validation_contract/required_results/edge_count` | `678` | `683` | overlay op 26 |
| Appendix A count declaration | `166 source nodes/node families and 678 direct edges` | `167 source nodes/node families and 683 direct edges` | prose replacement |
| Appendix A row after K011 | no `A010` row | `A010 | 1115 | K011` | row insertion |
| Appendix A K013 row | `K011` | `K011, A010` | row replacement |
| Appendix A K012 row | `K011, K013` | `K011, A010, K013` | row replacement |
| Appendix A K014 row | `K011, K013, K012` | `K011, A010, K013, K012` | row replacement |
| Appendix A K127 row | 59-node sequence without A010 | 60-node sequence with A010 immediately after K011 | row replacement |
| Final Appendix-A equality object `declared_node_count` | `166` | `167` | prose JSON replacement |
| Final Appendix-A equality object `declared_edge_count` | `678` | `683` | prose JSON replacement |
| Final Appendix-A equality object `schema_derived_node_count` | `166` | `167` | prose JSON replacement |
| Final Appendix-A equality object `schema_derived_edge_count` | `678` | `683` | prose JSON replacement |

Both test-matrix role locations become exactly:

`schema_and_683_edge_equality`

The overlay handles §23 values. The effective amendment separately controls the opening prose, counterexample prose, Appendix-A declaration/rows, and final Appendix equality object. Accepted Candidate-08 raw bytes remain immutable.

The complete 27-operation registry table and this changed-location table are also returned as the separate reconciliation deliverable.

---

## 11. Acceptance evidence

Sentinel can review Candidate 04 through static inspection:

1. verify canonical `main = 90c0059c0e86b7afd44fcf9f17223d68eab1a9e0`;
2. verify blocked Candidate 03 exact `124860 / 28299322ea7e27a65193cd8c5fe7db447ee7e851a85bdaf516ff34be3218da9c`;
3. verify K011 exact `1134 / 4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f2649`;
4. verify Amendment 01 exact `24599 / 8b60bbc0f3390c0b2d1a336b33d2c2f1dc54846e1f2906aff58639dad1defd63` and installation commit `e675a47ec2c8f6cd769c2673afc16d96e5622ccd`;
5. verify base registry exact `479463 / 82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff`;
6. independently JCS-serialize the overlay and verify `45347 / ae5074afdf35c5424da515e7d61a8113a0f9df2948c294dcdf9d43b98ccd8a9a`;
7. independently reproduce all 27 `new_value_jcs_sha256` values, including operation `12 = b761ce7a3797401d6114b5311942fd8b33355cfe20c53100e7ebd496bdc520ac` and operation `13 = 74a0a5ed842b98dd95dac5398ee608f390759f74030844d45acc915157ec0ac8`;
8. verify the Layer-1 base identity gate precedes every overlay and operation-level classification;
9. verify the Layer-1 overlay identity/schema/hash, order, and duplicate-target sub-precedence;
10. verify one isolated copy is created only from the exact verified base and the operation engine is invoked exactly once;
11. verify the Layer-2 common-first classifier and both operation-specific branches;
12. verify first-defect single-stop emission, complete isolated-copy discard, no partial publication, and atomic exposure only after all postconditions;
13. verify the end-to-end outcomes are separated from the synthetic operation-classifier counterexamples;
14. verify a fresh materializer invocation starts from the exact base and is not a second application to a prior result;
15. verify a synthetic second engine invocation on the same already-amended copy reaches operation `0`, emits `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED`, and publishes nothing;
16. independently JCS-serialize the effective bundle and verify `1266 / 075e27248944c9236d243dc6cdc50b310ff581cd6f1934d1ab8af119763e2c67`;
17. verify A010 payload/profile exactness and only one K011 edge;
18. verify K013/K012/K014 order and exact additional prerequisite;
19. verify K015/K016 direct boundaries unchanged;
20. verify exact K127 60-entry order and derive exactly `167 / 683`;
21. verify all graph discrepancy arrays empty;
22. verify the post-overlay reducer projection remains `66232 / 266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c`;
23. verify all 11 overlay stops registered and zero unregistered;
24. verify the exhaustive changed-location table remains unchanged except for Candidate-04 overlay-dependent identities and the materializer/engine source-review contract;
25. verify authorization effect `NONE`.

These methods authorize no implementation, import, test, execution, data read, network access, or Git action.

## 12. Compatibility and migration

- The accepted base-registry literal remains byte-identical.
- The accepted reducer projection remains byte-identical.
- Accepted Candidate-08 and Amendment-01 files remain unchanged.
- A010 is additive and one-node only.
- Pre-A010 K013/K012/K014 bytes are stale and non-authorizing.
- K015/K016 shapes and direct graph boundaries remain compatible.
- Future `schema_registry.py` retains exactly two generated literals: immutable base plus overlay.
- Every fresh end-to-end materializer invocation starts from the immutable base and invokes the operation engine exactly once.
- A prior effective registry is never a materializer input and cannot trigger an operation-level stop.
- The public effective semantic view changes only after complete graph, reducer, bundle, and atomic-exposure success.
- Downstream source review must bind the effective-registry bundle identity, not claim the base contains amendments.
- P1 remains blocked and `named_binary_probe_blocked = true`.

---

## 13. Security and authorization boundary

This candidate contains no credentials, secrets, wallet material, endpoint authorization, research data, or executable permission.

It authorizes none of the following:

- implementation-source authoring;
- test-source authoring;
- project imports, compilation, linting, type checking, coverage, or tests;
- project execution;
- local research-data access;
- network, API, RPC, vendor, Dune, curl, or endpoint activity;
- A010, K013, K012, K014, K015, or K016 materialization;
- acquisition, construction, alignment, rebuild, audit, transition, or empirical work;
- P1, P2, P3, scoring, or probe execution;
- gate changes;
- canonical edits or installation;
- branch, commit, push, merge, tag, release, ref update, or any Git write.

Authorization effect:

`NONE`

---

## 14. Self-attack

| Attack | Required result |
|---|---|
| Supply a registry differing by one byte from the exact base | Layer 1 emits `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH`; overlay and engine are not evaluated |
| Supply a prior effective registry as the base | `STOP_REGISTRY_OVERLAY_BASE_IDENTITY_MISMATCH`, not `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED` |
| Start a fresh materializer invocation after a prior successful invocation | restart from the exact immutable base; one new verified session may independently succeed |
| Invoke the operation engine zero times | no effective registry may publish |
| Invoke the engine twice on the same already-amended isolated copy in the defensive classifier path | operation `0` emits `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED`; no second result publishes |
| Describe the defensive second-engine proof as a fresh materializer invocation | reject source-review contract; the two layers are conflated |
| Feed a synthetic exact-new target to the verified-copy classifier | `STOP_REGISTRY_OVERLAY_ALREADY_APPLIED` |
| Insert a conflicting value at an add target in a synthetic working copy | `STOP_REGISTRY_OVERLAY_WRONG_OLD_VALUE` |
| Remove a replace target while retaining its parent in a synthetic working copy | `STOP_REGISTRY_OVERLAY_TARGET_MISSING` |
| Remove a required parent in a synthetic working copy | `STOP_REGISTRY_OVERLAY_TARGET_MISSING` |
| Reorder two operations | `STOP_REGISTRY_OVERLAY_OPERATION_ORDER_INVALID` after base and overlay identity/schema/hash controls |
| Duplicate a target pointer | `STOP_REGISTRY_OVERLAY_DUPLICATE_TARGET` |
| Change one overlay byte or embedded new-value hash | `STOP_REGISTRY_OVERLAY_LITERAL_IDENTITY_MISMATCH` |
| Fail graph reconciliation after engine success | `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH` |
| Alter reducer projection after graph success | `STOP_EFFECTIVE_REGISTRY_REDUCER_PROJECTION_MISMATCH` |
| Alter the bundle or attempt partial/non-atomic exposure | `STOP_EFFECTIVE_REGISTRY_BUNDLE_IDENTITY_MISMATCH`; no partial result |
| Hand-edit a flattened effective registry | source-review rejection; no accepted source |
| Omit governed Amendment-01 identity from A010 | `STOP_A010_GOVERNED_AMENDMENT_IDENTITY_INVALID` |
| Put governed identity only in prose | profile failure |
| Interpret governed identity as a NodeRef | `PROVENANCE_EDGE_SET_MISMATCH` |
| Add A010 directly to K015 or K016 | `PROVENANCE_EDGE_SET_MISMATCH` |
| Omit or move A010 in K127 | `PROVENANCE_EDGE_SET_MISMATCH` |
| Keep either test role at `678` | effective-registry identity/count review failure |
| Keep any graph count at `166/678` in an amended location | `STOP_EFFECTIVE_REGISTRY_GRAPH_RECONCILIATION_MISMATCH` |
| Introduce an unregistered stop | source-review stop-registration failure |
| Treat acceptance as implementation authorization | `STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED` |

**Strongest alternative design.** Store a second complete flattened `167 / 683` registry literal. That would simplify materialization but duplicate the accepted semantic registry and create a hand-edit/drift surface. The selected immutable-base-plus-exact-overlay model remains unchanged. Candidate 04 only separates its exact-base materializer from its verified-working-copy engine so external input defects cannot be misclassified as operation states.

Candidate 03 correctly defined the common-first target classifier but described a second application without separating a fresh exact-base materializer invocation from a defensive second engine invocation on the same working copy. Candidate 04 corrects only that boundary, its proof language, source-review contract, stop triggers, and deterministically dependent identities. The exact composite bundle plus the deep-frozen, atomically exposed semantic view remains the effective registry.

---

## 15. Requested Sentinel decision

`APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.

Approval accepts these exact SPEC-only Candidate-04 bytes for a later separately authorized canonical installation package. It does not install A010, activate the overlay in source, materialize an authorization chain, or authorize any operational activity.
