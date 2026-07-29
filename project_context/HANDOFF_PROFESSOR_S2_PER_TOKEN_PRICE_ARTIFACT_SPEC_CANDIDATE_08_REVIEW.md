# Professor Handoff — S2 Per-Token Price Artifact Specification Candidate 08 — Third Bounded Corrected Replacement Review

## 1. Status

| Field | Value |
|---|---|
| Node | `K009` |
| Assigned profile | `candidate08_professor_handoff.v1` |
| Status | `SUBMITTED_FOR_SENTINEL_SPECIFICATION_REVIEW` |
| Authoring mode | `HANDOFF`; third bounded correction |
| Prepared by | Professor |
| Reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Exact canonical `main` | `70ab8455f33d44b2a690b8c5db58f8ebc545454e` |
| Correction run | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03` |
| Authorization effect | `NONE` |
| Requested Sentinel decision | `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` |

**Purpose.** Return the third bounded corrected replacement K008 and this closed-profile K009 for complete independent specification review. This handoff does not accept, install, implement, or execute the specification.

## 2. Exact prerequisite and active authorization chain

| Node | Exact record/path | Bytes | SHA-256 | Direct predecessors |
|---|---|---:|---|---|
| `A002` | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md` | `5854` | `87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c` | exact controlling set |
| `K006` | `S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json` | `4675` | `52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f` | `A002` |
| `K005` | `S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json` | `3753` | `89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546` | `A002`, `K006` |
| `K007` | `S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json` | `4262` | `f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099` | `A002`, `K006`, `K005` |

Verified order: `A002 → K006 → K005 → K007`.

## 3. Exact blocked inputs

| Input | Raw bytes | SHA-256 |
|---|---:|---|
| blocked K008 | `759608` | `8f14caf480da85fab802105427e3841ca9d46f4d01c8e3643c63dc32ed85de8b` |
| blocked K009 | `13676` | `901143eb6f4f44b73b2953c2311949b956c4569fee46bc8a6735f28762cfa102` |

## 4. Corrected deliverable identities

| Node | Path | Raw bytes | SHA-256 binding |
|---|---|---:|---|
| `K008` | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md` | `776003` | `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63` |
| `K009` | `HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md` | `13549` | external delivery envelope and Sentinel review record |

K009's raw SHA-256 is deliberately absent from its own raw bytes. The exact externally supplied value accompanies these delivered bytes.

## 5. K009 self-excluding projection

| Field | Exact value |
|---|---|
| Projection rule | `OMIT_ENTIRE_SELF_IDENTITY_OBJECT_AND_ALL_MARKDOWN_PROSE` |
| Raw SHA-256 binding location | `EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD` |
| Projection byte length | `5420` |
| Projection SHA-256 | `973b485cfeb256ab3693fa9166e2ecd33a54a86fa2c8d85f6fea1c7136b9750e` |

The projection is RFC 8785 JCS of the complete normative K009 JSON object with `/payload/self_identity` removed.

## 6. Mandatory static checks

| Check | Result |
|---|---|
| `RAW_K008_BYTE_LENGTH_AND_SHA256_MATCH_SUBMITTED_IDENTITY` | `PASS` |
| `RAW_K009_BYTE_LENGTH_AND_EXTERNALLY_SUPPLIED_SHA256_MATCH_SUBMITTED_IDENTITY` | `PASS — external delivery binding` |
| `K008_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE` | `PASS — 1` |
| `K009_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE` | `PASS — 1` |
| `K008_PAYLOAD_VALIDATES_DOCUMENT_CANDIDATE_V1` | `PASS` |
| `K009_PAYLOAD_VALIDATES_CANDIDATE08_PROFESSOR_HANDOFF_V1` | `PASS` |
| `K009_SELF_EXCLUDING_PROJECTION_IDENTITY_MATCHES` | `PASS` |
| `K009_SELF_IDENTITY_ENUM_VALUE_IS_REGISTERED` | `PASS` |
| `PROSE_AND_REGISTRY_TYPE_REFERENCES_AGREE` | `PASS` |
| `RECORDID_BOUND_IS_160_UTF8_BYTES_EVERYWHERE` | `PASS` |
| `RELATIVEPATH_NFC_IS_MANDATORY_EVERYWHERE` | `PASS` |

All eleven checks are conjunctive. Any failure would set `static_submission_gate=BLOCK` and prohibit this handoff from claiming static clear.

Additional static results: registry nodes `166`; schema-derived edges `678`; Appendix-A edges `678`; missing/extra edges `0/0`; unknown types `0`; missing profiles `0`; binding issues `0`; rank violations `0`; cycles `0`; condition-state overlap `0`; global invalid vectors/placeholders `0/0`; exact-clear witnesses `1`; scientific payload provenance contamination `0`.

## 7. Corrections materialized

1. K009 is assigned only to the closed `candidate08_professor_handoff.v1` profile.
2. K009's payload contains every required field and no undeclared field.
3. `raw_sha256_binding_location` uses one registered value everywhere.
4. Every normative alignment-policy 64-bit field uses `UInt64Dec`.
5. `RecordId` is exactly 1–160 ASCII/UTF-8 bytes in prose and registry.
6. `RelativePath` must already be NFC; non-NFC input is rejected, not normalized.
7. Raw K008/K009 identity, extraction, profile, projection, enum, type, bound, and NFC checks are mandatory before static clear.
8. The accepted 166-node/678-edge architecture and all preserved scientific and authorization boundaries remain unchanged.

## 8. Actions

Performed: canonical and A002 inspection; exact K006/K005/K007 and blocked-input verification; bounded drafting; UTF-8/LF sealing; SHA-256 and byte-length calculation; normative payload extraction; profile validation; self-projection validation; static schema, type, graph, state, count, and identity checks.

Not performed: Copilot CLI role execution; implementation or test-source authoring; tests; project imports; research-data access; network/API/RPC/vendor use; empirical runs; acquisition; construction; alignment; rebuild; audit; transition; P1/P2/P3; scoring; probe execution; canonical installation/edit; Git branch, commit, push, merge, tag, release, or ref update; later-stage authorization.

## 9. Authorization statement

Authorization effect is `NONE`. K008 and K009 return only to Sentinel for full specification review.

## 10. Requested Sentinel decision

`APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.

## Appendix A — Normative K009 payload

This is the sole machine-extractable K009 payload. Its raw SHA-256 is supplied externally because embedding it here would create a circular self-hash.

<!-- NORMATIVE_K009_PAYLOAD -->
```json
{
  "canonical_commit": "70ab8455f33d44b2a690b8c5db58f8ebc545454e",
  "created_at_utc_ms": 1785267538566,
  "dependencies": [
    {
      "node_id": "K006",
      "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
      "byte_length": 4675,
      "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
    },
    {
      "node_id": "K005",
      "logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
      "byte_length": 3753,
      "sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
    },
    {
      "node_id": "K007",
      "logical_path": "S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json",
      "byte_length": 4262,
      "sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099"
    },
    {
      "node_id": "K008",
      "logical_path": "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
      "byte_length": 776003,
      "sha256": "b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63"
    }
  ],
  "node_id": "K009",
  "payload": {
    "actions_not_performed": [
      "COPILOT_ROLE_EXECUTION",
      "IMPLEMENTATION_SOURCE_AUTHORING",
      "TEST_SOURCE_AUTHORING",
      "TEST_EXECUTION",
      "PROJECT_IMPORT_OR_EXECUTION",
      "LOCAL_RESEARCH_DATA_ACCESS",
      "NETWORK_API_RPC_VENDOR_ACCESS",
      "EMPIRICAL_RUN",
      "PRICE_ACQUISITION",
      "PRICE_ARTIFACT_CONSTRUCTION",
      "ALIGNMENT_EXECUTION",
      "DETERMINISTIC_REBUILD_EXECUTION",
      "AUDIT_EXECUTION",
      "CONSUMER_TRANSITION_EXECUTION",
      "P1_P2_P3",
      "SCORING",
      "PROBE_EXECUTION",
      "CANONICAL_INSTALLATION",
      "CANONICAL_FILE_EDIT",
      "GIT_BRANCH_COMMIT_PUSH_MERGE_TAG_RELEASE_OR_REF_UPDATE",
      "LATER_STAGE_AUTHORIZATION"
    ],
    "actions_performed": [
      "READ_CANONICAL_TEXT",
      "READ_EXACT_BLOCKED_K008_K009",
      "VERIFY_CANONICAL_MAIN_IDENTITY",
      "VERIFY_A002_IDENTITY",
      "VERIFY_EXACT_AUTHORIZATION_IDENTITIES",
      "DRAFT_THIRD_CORRECTED_SPECIFICATION",
      "DRAFT_THIRD_CORRECTED_REVIEW_HANDOFF",
      "COMPUTE_LOCAL_BYTE_LENGTH_AND_SHA256",
      "EXTRACT_NORMATIVE_K008_PAYLOAD",
      "EXTRACT_NORMATIVE_K009_PAYLOAD",
      "VALIDATE_K008_PAYLOAD_AGAINST_ASSIGNED_PROFILE",
      "VALIDATE_K009_PAYLOAD_AGAINST_ASSIGNED_PROFILE",
      "VALIDATE_K009_SELF_EXCLUDING_PROJECTION",
      "STATIC_DOCUMENT_SCHEMA_AND_IDENTITY_CHECKS"
    ],
    "administrative_role_source_context": {
      "repository": "rigolugo/pm_copilot_roles",
      "immutable_commit": "a7df418216cb7355b003164b8b509e40081cdbdc",
      "canonical_state": "INSTALLED_AND_SENTINEL_VERIFIED",
      "evidence_only": true,
      "authorization_effect": "NONE",
      "s2_dependency_effect": "NONE",
      "role_execution_status": "NOT_PERFORMED",
      "required_reads": [
        "project_context/GITHUB_COPILOT_CLI_ROLE_SOURCE_POINTER.md",
        "project_context/administrative_tools/github_copilot_cli/README_FIRST.md",
        "project_context/administrative_tools/github_copilot_cli/SENTINEL_CANONICAL_INSTALLATION_VERIFICATION.md"
      ]
    },
    "authorization_effect": "NONE",
    "blocked_input_identities": [
      {
        "logical_path": "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
        "byte_length": 759608,
        "sha256": "8f14caf480da85fab802105427e3841ca9d46f4d01c8e3643c63dc32ed85de8b"
      },
      {
        "logical_path": "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md",
        "byte_length": 13676,
        "sha256": "901143eb6f4f44b73b2953c2311949b956c4569fee46bc8a6735f28762cfa102"
      }
    ],
    "control_refs": [
      {
        "node_id": "K006",
        "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
        "byte_length": 4675,
        "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
      },
      {
        "node_id": "K005",
        "logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
        "byte_length": 3753,
        "sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
      },
      {
        "node_id": "K007",
        "logical_path": "S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json",
        "byte_length": 4262,
        "sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099"
      }
    ],
    "deliverable_refs": [
      {
        "node_id": "K008",
        "logical_path": "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
        "byte_length": 776003,
        "sha256": "b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63"
      }
    ],
    "handoff_id": "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW",
    "run_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
    "self_identity": {
      "projection_rule": "OMIT_ENTIRE_SELF_IDENTITY_OBJECT_AND_ALL_MARKDOWN_PROSE",
      "raw_byte_length": 13549,
      "raw_sha256_binding_location": "EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD",
      "self_excluding_projection_byte_length": 5420,
      "self_excluding_projection_sha256": "973b485cfeb256ab3693fa9166e2ecd33a54a86fa2c8d85f6fea1c7136b9750e"
    },
    "stage_code": "CANDIDATE_08_SPEC_ONLY_DRAFTING",
    "static_checks": {
      "raw_k008_identity_match": true,
      "raw_k009_external_identity_match": true,
      "k008_normative_payload_count": 1,
      "k009_normative_payload_count": 1,
      "k008_assigned_profile_valid": true,
      "k009_assigned_profile_valid": true,
      "k009_self_projection_valid": true,
      "k009_self_identity_enum_registered": true,
      "prose_registry_type_agreement": true,
      "recordid_bound_agreement": true,
      "relativepath_nfc_agreement": true,
      "unknown_types": 0,
      "missing_profiles": 0,
      "binding_issues": 0,
      "registry_node_count": 166,
      "schema_derived_edge_count": 678,
      "appendix_edge_count": 678,
      "missing_edges": 0,
      "extra_edges": 0,
      "rank_violations": 0,
      "cycles": 0,
      "condition_state_classes": 19,
      "condition_state_legal_tuples": 31,
      "condition_state_overlap_count": 0,
      "global_reducer_rows": 153,
      "global_invalid_vectors": 0,
      "global_placeholder_count": 0,
      "safe_span_representative_cases": 233,
      "safe_span_unmapped_or_multi_match": 0,
      "terminal_representative_cases": 417,
      "terminal_unmapped_or_multi_match": 0,
      "scientific_payload_provenance_contamination_count": 0,
      "authorization_exact_schema_matches": 3,
      "exact_clear_witness_count": 1,
      "copilot_role_source_edge_count": 0,
      "copilot_role_source_scientific_dependency_count": 0,
      "copilot_role_execution": "NOT_PERFORMED",
      "static_submission_gate": "CLEAR"
    }
  },
  "record_id": "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW",
  "schema_id": "pm_research.s2.professor_review_handoff.v5",
  "status": "SUBMITTED_FOR_SENTINEL_SPECIFICATION_REVIEW"
}
```
