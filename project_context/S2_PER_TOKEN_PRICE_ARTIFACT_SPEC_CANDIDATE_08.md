# S2 Per-Token Price Artifact Specification — Candidate 08

## 0. Formal status and decision request

| Field | Value |
|---|---|
| Document ID | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08` |
| Status | `THIRD_CORRECTED_SPECIFICATION_REVIEW_CANDIDATE` |
| Authoring mode | `SPECIFY` and `MATERIALIZE`; third bounded correction, no redesign of `A002` |
| Prepared by | Professor |
| Independent reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Canonical branch | `main` |
| Exact verified canonical commit | `70ab8455f33d44b2a690b8c5db58f8ebc545454e` |
| Controlling architecture node | `A002` |
| Exact A002 path | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md` |
| Exact A002 byte length | `5854` |
| Exact A002 SHA-256 | `87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c` |
| Gustavo drafting authorization | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_GUSTAVO_AUTHORIZATION_04` (`K006`) |
| Later Sentinel stage authorization | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_SENTINEL_AUTHORIZATION_05` (`K005`) |
| Drafting activity root | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_ROOT_05` (`K007`) |
| Run ID | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03` |
| Authorized activity | `CANDIDATE_08_THIRD_BOUNDED_SPEC_ONLY_CORRECTION` |
| Authorization effect | `NONE` |
| Requested Sentinel decision | `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` |

**Purpose.** Replace the blocked second-correction Candidate-08 bytes without changing accepted architecture `A002`. This third bounded correction closes K009 to one assigned profile, reconciles its external self-identity enum, standardizes alignment fields on `UInt64Dec`, fixes the universal 160-byte `RecordId` bound, makes NFC mandatory for every `RelativePath`, and makes raw K008/K009 extraction, profile, identity, and consistency validation conjunctive.

**Checkable completion sentence.** Sentinel can parse §23, validate the exact current authorization bytes, resolve zero unknown types, derive exactly the accepted 166 nodes and 678 direct edges, confirm disjoint P00–P18 and enum-valid global states, and verify that original/rebuild comparison covers only six partition payloads, one manifest payload, and one reconciliation payload while authorizing no later activity.

### 0.1 Normative K008 document payload

The following is the sole machine-extractable K008 document payload. Its `activity_root` is the only direct K008 `NodeRef`. No other field in this payload or elsewhere in K008 may create a K008 provenance edge.

<!-- NORMATIVE_K008_PAYLOAD -->
```json
{
  "document_id": "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08",
  "status": "THIRD_CORRECTED_SPECIFICATION_REVIEW_CANDIDATE",
  "canonical_commit": "70ab8455f33d44b2a690b8c5db58f8ebc545454e",
  "activity_root": {
    "node_id": "K007",
    "logical_path": "S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json",
    "byte_length": 4262,
    "sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099"
  },
  "normative_input_refs": [],
  "normative_sections": [
    "SECTION_00",
    "SECTION_01",
    "SECTION_02",
    "SECTION_03",
    "SECTION_04",
    "SECTION_05",
    "SECTION_06",
    "SECTION_07",
    "SECTION_08",
    "SECTION_09",
    "SECTION_10",
    "SECTION_11",
    "SECTION_12",
    "SECTION_13",
    "SECTION_14",
    "SECTION_15",
    "SECTION_16",
    "SECTION_17",
    "SECTION_18",
    "SECTION_19",
    "SECTION_20",
    "SECTION_21",
    "SECTION_22",
    "SECTION_23",
    "APPENDIX_A",
    "APPENDIX_B",
    "APPENDIX_C"
  ],
  "authorization_effect": "NONE"
}
```

### 0.2 Exact third-correction provenance

The exact K006, K005, and K007 raw bytes were verified before drafting. Their exact closed schemas materialize every actual field and nested field, including K006 `authorization_source`, the six-item correction boundary, the exact blocked-input identities, the strict-subset Sentinel activation, the eleven mandatory static checks in K007, and the explicit `COPILOT_ROLE_EXECUTION` prohibition. The following machine-readable object uses the closed `NonEdgeIdentityMetadata` type. Its field names are deliberately not `NodeRef` field names, and the §23 edge extractor MUST ignore it.

```json
{
  "identity_type": "NonEdgeIdentityMetadata",
  "records": {
    "A002": {
      "metadata_node_label": "A002",
      "metadata_logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
      "metadata_byte_length": 5854,
      "metadata_sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
    },
    "K006": {
      "metadata_node_label": "K006",
      "metadata_logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
      "metadata_byte_length": 4675,
      "metadata_sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
    },
    "K005": {
      "metadata_node_label": "K005",
      "metadata_logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
      "metadata_byte_length": 3753,
      "metadata_sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
    },
    "K007": {
      "metadata_node_label": "K007",
      "metadata_logical_path": "S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json",
      "metadata_byte_length": 4262,
      "metadata_sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099"
    }
  },
  "run_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
  "authority": "descriptive verification only; exact K008 direct edge remains K007"
}
```

The causal order is exact:

`A002 → K006 → K005 → K007 → K008/K009`

K008 has only the exact K007 direct edge. K007 itself binds exact A002, K006, and K005 `NodeRef` values. K009 directly binds K006, K005, K007, and corrected K008 as required by Appendix A. Reinterpreting this descriptive metadata as additional K008 direct edges is `PROVENANCE_EDGE_SET_MISMATCH`.

The exact blocked inputs for this correction are K008 `759608` bytes / `8f14caf480da85fab802105427e3841ca9d46f4d01c8e3643c63dc32ed85de8b` and K009 `13676` bytes / `901143eb6f4f44b73b2953c2311949b956c4569fee46bc8a6735f28762cfa102`. They remain blocked historical inputs.

The activity permits only canonical and exact blocked-text reads, second corrected specification and handoff drafting, checksum computation, and static document/schema/graph/state checks. It authorizes no implementation, test source, test execution, project import, research-data access, endpoint/network use, empirical result, canonical write, Git action, or downstream stage.

## 1. Authority, precedence, and evidence classes

### 1.1 Controlling source order

The following order is normative:

1. canonical repository bytes at commit `70ab8455f33d44b2a690b8c5db58f8ebc545454e`;
2. exact `A002`;
3. exact `A001`, identified by `A002`;
4. exact `S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md`;
5. exact `S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03_AMENDMENT_01.md`;
6. this Candidate 08 only after Sentinel accepts its exact bytes.

Amendment 01 controls on every conflict. Candidate 03 controls where Amendment 01 is silent. Architecture Normalization Candidates 01 and 02 are blocked historical submissions and MUST NOT be referenced as normative inputs, dependency edges, implementation guidance, fallback rules, or acceptance evidence.

### 1.2 Evidence labels

Material claims use these classes:

- `CANONICAL`: directly bound to canonical repository bytes.
- `ACCEPTED`: bound by an exact Sentinel acceptance record.
- `SUBMITTED`: supplied for review but not accepted.
- `COMPUTED`: deterministically derived from present exact inputs.
- `OBSERVED`: directly inspected in a future separately authorized activity.
- `INFERRED`: logically derived but not directly observed.
- `ASSUMED`: not verified; MUST NOT clear a gate.
- `RECALLED`: memory only; MUST NOT enter a normative record.

Missing evidence is never negative evidence. A copied identifier without the referenced bytes is not evidence of the referenced record.

### 1.3 Fixed project constraints

The specification MUST preserve all of the following:

- research-only purpose; no live trading, paper trading, wallet copying, or trading execution;
- exact universe `U0 = 39,693`;
- subclass totals `UP_DOWN=22,012`, `OVER_UNDER=1,003`, `NAMED_OTHER=16,678`;
- independent token-specific acquisition for both outcome indexes;
- no complement synthesis, `1-price`, `1-yes_price`, `1-p`, or winner-conditioned token enumeration;
- historical `interval=max`, fidelity-omitted method remains `S1_SOURCE_NOT_VIABLE`;
- revised `fidelity=1`, interval-omitted method is `S1_SOURCE_VIABLE` only for the reviewed 248-condition Pass-1 sample and reviewed EC2 route;
- no full-universe price-artifact validation has occurred;
- P1 remains blocked;
- `named_binary_probe_blocked = true`;
- valid exclusions, limitations, incomplete evidence, and blocking defects remain distinct;
- acceptance of a valid blocked or limited finding is non-authorizing.


### 1.4 GitHub Copilot CLI role-source context — administrative evidence only

The following canonical documents were read as bounded administrative capability context:

1. `project_context/GITHUB_COPILOT_CLI_ROLE_SOURCE_POINTER.md`;
2. `project_context/administrative_tools/github_copilot_cli/README_FIRST.md`;
3. `project_context/administrative_tools/github_copilot_cli/SENTINEL_CANONICAL_INSTALLATION_VERIFICATION.md`.

They identify `rigolugo/pm_copilot_roles` at immutable commit `a7df418216cb7355b003164b8b509e40081cdbdc` with canonical state `INSTALLED_AND_SENTINEL_VERIFIED`. Their authorization effect is `NONE`.

For this specification:

- the role-source identity IS administrative evidence only;
- no Copilot CLI role was invoked, installed, launched, adapted, or executed;
- the role-source repository and commit MUST NOT enter A002, Appendix A, any `NodeRef`, A003/A005/A007, K068/K072, any scientific payload, acquisition provenance, audit closure, gate record, or transition record;
- repository presence, capability findings, or synthetic evidence MUST NOT be interpreted as authorization for source authoring, test authoring, execution, research-data access, network activity, Git writes, or a later stage;
- the schema edge extractor MUST derive zero S2 edges from `AdministrativeRoleSourceContext`.

---

## 2. Scope and non-objectives

### 2.1 In scope

This specification closes:

- authorization, activity-root, deliverable, review, and handoff record schemas;
- global lifecycle, per-condition processing, and consumer-transition reducers;
- exact artifact path grammar and identity envelopes;
- complete 39,693-condition and subclass reconciliation;
- decision-window, token-pair, request-plan, acquisition, construction, alignment, rebuild, audit, review, and transition contracts;
- deterministic serialization, hashing, row identity, and build identity;
- scientific projections and activity-provenance wrappers;
- original/rebuild byte-comparison boundaries;
- nineteen audit checks and exact evidence closures;
- the exact gate reducer and Stage-10 branches;
- authoritative schema-implied provenance-edge equality.

### 2.2 Out of scope

This document MUST NOT be interpreted as authorization to:

- write implementation or test code;
- execute tests or project imports;
- read local research data;
- use network, API, RPC, vendor, or endpoint access;
- invoke, install, launch, adapt, or execute any GitHub Copilot CLI role;
- acquire or construct prices;
- run S4, S5, S6, S7, S8A, S8B, S8C, S9, or S10;
- create empirical evidence or results;
- draft implementation authorization;
- alter canonical files or Git state;
- progress P1, P2, P3, scoring, or probe execution.

---

## 3. Primitive types, encodings, and identity rules

### 3.1 Primitive types and JCS integer safety

| Type | Closed definition |
|---|---|
| `NodeId` | one exact identifier in Appendix A; ASCII |
| `GitCommit40` | lowercase regex `^[0-9a-f]{40}$` |
| `Sha256` | lowercase regex `^[0-9a-f]{64}$` |
| `JcsSafeUInt` | JSON integer `0..9007199254740991`; no negative zero, fraction, or exponent |
| `ByteLength` | `JcsSafeUInt`, unit bytes |
| `Count` | `JcsSafeUInt` |
| `UInt8` | JSON integer `0..255` |
| `UInt32` | JSON integer `0..4294967295` |
| `UInt64Dec` | canonical decimal string `0` or `[1-9][0-9]{0,19}`, numeric value `<=18446744073709551615` |
| `UtcMs` | JSON integer `0..253402300799999`, UTC milliseconds |
| `UtcSecond` | JSON integer `0..253402300799`, UTC seconds |
| `UniverseOrdinal` | JSON integer `0..39692` |
| `ConditionId` | lowercase regex `^0x[0-9a-f]{64}$` |
| `TokenId` | canonical base-10 uint256 string; no sign, point, exponent, whitespace, or leading zero; value `<=2^256-1` |
| `OutcomeIndex` | JSON integer `0` or `1` |
| `Subclass` | `UP_DOWN`, `OVER_UNDER`, or `NAMED_OTHER` |
| `CanonicalDecimalPrice` | string `0`, `1`, or `0.` followed by 1–76 digits with no trailing zero; exact value `[0,1]` |
| `TransportResult` | exact enum `HTTP_RESPONSE`, `TIMEOUT`, `DNS_FAILURE`, `CONNECTION_FAILURE`, `TLS_FAILURE`, `CONNECTION_RESET`, `RESOURCE_BOUND_REJECTION`, `LOCALLY_CANCELLED`, `UNKNOWN_TRANSPORT_FAILURE` |
| `RelativePath` | UTF-8 NFC, `/` separator, no leading `/`, `..`, empty segment, NUL, or backslash |
| `RecordId` | nonempty ASCII string, maximum 160 bytes |
| `Nullable<T>` | exactly JSON `null` or one valid `T` |

No conforming JSON record may contain an integer outside `JcsSafeUInt`. Full-range 64-bit unsigned values use `UInt64Dec`. Token identifiers remain canonical decimal strings. Binary floating point MUST NOT enter parsing, normalization, hash preimages, ordering, equality, limits, timestamps, prices, or retry calculations. The normative unknown-type scan over every schema field MUST return zero findings; any unresolved type is `GLOBAL_STATE_INVALID` for specification conformance.

### 3.2 Serialization profiles

1. Machine JSON uses RFC 8785 JCS, UTF-8 without BOM, no trailing newline.
2. JSONL uses one JCS object per line, UTF-8 without BOM, LF after every row including final.
3. Markdown uses UTF-8 without BOM and LF.
4. SHA-256 and byte length cover the same exact raw bytes.
5. Arrays retain specified order; objects serialize through JCS.
6. Raw endpoint JSON is parsed from exact UTF-8 bytes with number lexemes preserved before normalization; it need not itself be JCS.
7. ZIP is forbidden for scientific identity; K062 uses exact uncompressed POSIX ustar.

### 3.3 `NodeIdentity`

```json
{"node_id":"K000","logical_path":"nodes/K000/artifact.json","byte_length":0,"sha256":"0000000000000000000000000000000000000000000000000000000000000000"}
```

All four fields are required and non-null. `byte_length` is `ByteLength`. `NodeIdentity` identifies exact bytes but creates no edge by itself. A family identity lists each member path, byte length, and SHA-256 in exact profile order. `NodeRef` has the same four scalar fields but creates an edge only in a profile-declared typed reference slot or a declared schema-edge contract.

### 3.4 `NodeRef`, schema-edge contracts, and derived edges

A direct edge has exactly one of two storage forms:

1. `ARTIFACT_FIELD`: a serialized field declared `NodeRef`, `Nullable<NodeRef>`, or `NodeRefArrayElement`;
2. `SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED`: a typed derivation binding declared in the closed node profile for an activity-free scientific payload.

The second form is required because A003/A005/A007, K072, K073F/K096F, K074/K097, and K075/K098 MUST NOT serialize node IDs, dependencies, timestamps, or activity provenance into scientific bytes. Their direct edges remain explicit and machine-derived from typed `ref_bindings`, but those bindings are not part of the compared payload.

For record profiles, the envelope `dependencies` array MUST be generated from serialized semantic slots. For activity-free scientific profiles, no `dependencies` field is serialized. `NodeIdentity`, `ArtifactIdentity`, `ScientificPayloadIdentity`, `NonEdgeIdentityMetadata`, and `SchemaLiteral` never create K008 edges. Exact JSON values embedded under `exact_current_record_schemas` are `SchemaLiteral` validation data for external K006/K005/K007 bytes; the extractor MUST NOT traverse them as K008 provenance.

The extractor MUST emit one edge per `nodes.*.ref_bindings` entry, compare the result with Appendix A, and reject any missing, extra, duplicate, rank-invalid, or cyclic edge as `PROVENANCE_EDGE_SET_MISMATCH`. A copied `dependencies` array is never independent authority.

### 3.5 Scientific payloads and provenance envelopes

A complete activity record and its scientific payload are distinct byte objects.

- Activity-free scientific payloads serialize only their closed scientific schemas.
- Non-compared provenance envelopes and wrappers carry node IDs, record IDs, dependencies, creation timestamps, authorization/root identities, actors, environments, and physical output roots.
- K076 and K099 each bind exactly eight scientific payload identities: six partition members, one manifest payload, and one reconciliation payload.
- Original and rebuilt provenance envelopes are expected to differ and MUST NOT be compared.
- `created_at_utc_ms` is forbidden in A003, A005, A007, K072, every K073F/K096F member, K074/K097 scientific payload, K075/K098 scientific payload, deterministic row keys, and deterministic build preimages.

The universal record envelope applies only to record profiles that explicitly declare it. It does not apply to activity-free scientific payload profiles.

## 4. Exact path grammar

### 4.1 Workflow root

For a future accepted workflow:

```text
workflow_id = "s2wf-sha256-" + SHA256(UTF8(JCS({
  "schema_id":"pm_research.s2.workflow_identity.v1",
  "canonical_commit":K000,
  "controlling_architecture":A002
})))
```

The exact root is:

```text
artifacts/named_binary_probe/s2_per_token_price/<workflow_id>/
```

For every future node not listed as a canonical exception below, the decision-bearing node path is:

```text
nodes/<NodeId>/artifact.json
```

relative to the workflow root.

### 4.2 Canonical and current-deliverable exceptions

| Node | Exact path |
|---|---|
| `K000` | virtual Git object `git:commit:<GitCommit40>`; no file |
| `K001` | `nodes/K001/artifact.json` |
| `K002` | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md` |
| `A000` | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03_AMENDMENT_01.md` |
| `A001` | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A001_SENTINEL_COMBINED_ARCHITECTURE_REVIEW_RECORD_CANDIDATE_01.md` |
| `A002` | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md` |
| `K008` | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md` |
| `K009` | `HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md` |
| `K130` | `nodes/K130/artifact.md` |
| `K142E` | `nodes/K142E/S2_P1_CONSUMER_SPEC_CANDIDATE.md` |

### 4.3 Compound-family payload paths

| Node | Exact additional payload paths |
|---|---|
| `K056F` | `nodes/K056F/rows.jsonl`, `nodes/K056F/family_identity.json` |
| `K058F` | `nodes/K058F/attempts.jsonl`, `nodes/K058F/payloads/<request_id>/<attempt_ordinal>.bin`, `nodes/K058F/family_identity.json` |
| `K059F` | `nodes/K059F/terminals.jsonl`, `nodes/K059F/family_identity.json` |
| `K073F` | `nodes/K073F/partitions/<Subclass>/side_<OutcomeIndex>.jsonl`, exactly six paths; `nodes/K073F/family_identity.json` |
| `K096F` | `nodes/K096F/partitions/<Subclass>/side_<OutcomeIndex>.jsonl`, exactly six paths; `nodes/K096F/family_identity.json` |

All `logical_path` values in scientific manifests are relative to the node root and MUST NOT contain workflow IDs, activity roots, actors, environments, or timestamps.

---

## 5. Authorization and lifecycle record contracts

The complete closed profiles include `gustavo_authorization.v1`, `sentinel_authorization.v1`, `activity_root.v1`, `handoff.v1`, `review.v1`, and `acceptance.v1` in §23. K009 is assigned only to the stricter closed `candidate08_professor_handoff.v1`; it is not validated as `handoff.v1`. All roots and scopes are exact, duplicate-free ordered arrays. Scope expansion, wrong commit, missing bytes, time-order inversion, mismatched stage/actor/root, or a decision-bearing identity outside a typed reference slot is blocking.

### 5.1 Exact current records

| Node | Record ID | Path | Bytes | SHA-256 | Scope/effect | Predecessors |
|---|---|---|---:|---|---|---|
| `K006` | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_GUSTAVO_AUTHORIZATION_04` | `S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json` | `4675` | `52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f` | third bounded SPEC-only correction; no execution | exact A002 |
| `K005` | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_SENTINEL_AUTHORIZATION_05` | `S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json` | `3753` | `89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546` | strict subset of K006; `AUTHORIZE_STAGE` | exact A002, K006 |
| `K007` | `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_ROOT_05` | `S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json` | `4262` | `f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099` | active third-correction root; SPEC drafting only | exact A002, K006, K005 |

The §23 exact-current-record schemas reproduce every field and array element present in the supplied JSON values and reject any additional field. Validation requires exact raw length, SHA-256, UTF-8/JCS bytes, deep JSON equality, and exact semantic reference targets. These schemas do not retroactively require fields absent from the supplied records.

All three canonical commits equal `70ab8455f33d44b2a690b8c5db58f8ebc545454e`. Their exact timestamps satisfy `K006 < K005 < K007`. The run ID is exactly `S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03`.

### 5.2 Exact corrected activity ladder

| Prerequisite acceptance | Gustavo authorization | Later Sentinel authorization | Root | Deliverables/handoff |
|---|---|---|---|---|
| `A002` | `K006` | `K005` | `K007` | `K008`, `K009` |
| `K011` | `K013` | `K012` | `K014` | `K015`, `K016` |
| `K018` | `K020` | `K019` | `K021` | `K022`, `K023` |
| `K018` + `K025` | `K027` | `K026` | `K028` | `K029`, `K030` |
| `K032` | `K034` | `K033` | `K035` | `K036`–`K038`, `A003`, `A004`, `K039` |
| `K041` | `K043` | `K042` | `K044` | `K045`–`K047`, `K048` |
| `K041` + `K051` + `K052P` | `K054` | `K053` | `K055` | `K056F`–`K064`, `A005`–`A008`, `K065` |
| `K067` + `K068` | `K070` | `K069` | `K071` | `K072`–`K076`, `K077` |
| `K079` + `K082` + `K083P` | `K085` | `K084` | `K086` | `K087`, `K088`, `K089` |
| `K091` | `K093` | `K092` | `K094` | `K095`–`K101`, `K102` |
| `K104` | `K106` | `K105` | `K107` | `K108`–`K126`, `A009`, `K127`–`K131`, `K132` |
| `K137` | `K139` | `K138` | `K140` | `K141` and one Stage-10 branch |
| `K146E` | `K148` | `K147` | `K149` | future P1 only under later accepted contract |

No acceptance, authorization, result, policy, gate, or review creates a successor record automatically.

### 5.3 Handoff self-identity rule

A handoff MUST bind exact predecessor and deliverable NodeRefs but MUST NOT contain its own raw SHA-256. A raw self-hash inside the bytes would require solving `x=SHA256(bytes containing x)` and is not a realizable conformance requirement. K009's exact raw byte length is carried internally; its raw SHA-256 MUST be supplied only by the external delivery envelope and the later Sentinel review record. The registered `raw_sha256_binding_location` value is exactly `EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD`. Internally K009 carries a self-excluding projection identity computed from the complete normative K009 JSON object with `/payload/self_identity` removed. This preserves the accepted acyclic graph and does not weaken any predecessor identity.

## 6. Global lifecycle model

### 6.1 Complete vector

`G=(phase,phase_status,review_disposition,halt_code)` uses only the registered enums `GlobalPhase`, `GlobalPhaseStatus`, `ReviewDisposition`, and `Nullable<GlobalHaltCode>`. Every component is mandatory. `halt_code` is non-null iff `phase=HALTED`.

### 6.2 Exact finite reducer

The normative `global_state_reducer.v3` in §23 contains:

- one closed snapshot schema;
- a closed predicate DSL;
- explicit phase contracts with exact node IDs;
- one enum-valid output vector in every row;
- exact defect-halt rows for every closed base stop code;
- exact review-halt rows for every review phase and final disposition;
- explicit activity, review-pending, approved-waiting-root, branch, and terminal rows;
- an exact-clear reachability witness ending in K146E.

No row contains `X`, `successor_review(X)`, conditional prose inside a vector field, or a placeholder halt value. Evaluation order is defect halt, terminal completion, review halt, then normal state. The first and only matching row is the result. Zero or multiple matches is `GLOBAL_STATE_INVALID`.

Every lower-priority row requires the negation of higher-priority conditions. Latest-phase selection uses the fixed phase ordinal. Branch nodes are mutually exclusive. A valid approval never creates a later root; the prior review remains `COMPLETE` until the exact next Gustavo authorization, later Sentinel authorization, and activity root exist.

## 7. Per-condition processing model

### 7.1 Complete vector and classifier

For every `c∈U0`:

`P(c)=(position,window,token_pair,request,construction,alignment,effect)`

All seven components are mandatory and use the closed enums below:

- `position`: `INITIAL|TOKEN_PAIR|REQUEST|CONSTRUCTION|READY_ALIGNMENT|FINAL`
- `window`: `NOT_EVALUATED|QUERY_ELIGIBLE|VALID_EXCLUSION_INVALID_WINDOW|INCOMPLETE_MISSING_TRADE_ANCHOR|BLOCKED_RESOLUTION_BOUNDARY`
- `token_pair`: `NOT_EVALUATED|NOT_APPLICABLE_WINDOW|STABLE_INDEPENDENT_PAIR|UNRESOLVED|UNSTABLE|PRECISION_INVALID`
- `request`: `NOT_EVALUATED|NOT_APPLICABLE|PLANNED|IN_PROGRESS|COMPLETE_BOTH_TERMINALS|INCOMPLETE|BLOCKED`
- `construction`: `NOT_EVALUATED|NOT_APPLICABLE|BOTH_PARTITIONS_INCLUDED|ONE_PARTITION_INCLUDED|NO_PARTITION_INCLUDED|INCOMPLETE|BLOCKED`
- `alignment`: `NOT_EVALUATED|NOT_APPLICABLE|BOTH_SIDE_USABLE|ONE_SIDE_USABLE|NEITHER_SIDE_USABLE|INCOMPLETE|BLOCKED`
- `effect`: `ACTIVE|VALID_EXCLUSION|CLEAR_COMPONENT|LIMITATION|INCOMPLETE_EVIDENCE|BLOCKING_DEFECT`

The complete P00–P18 component sets are in §23 `condition_state_classes`. A vector matches class X iff every component value belongs to X's declared set. The registry is exhaustive over reachable reducer outputs and pairwise disjoint: where a class allows a set, no other class permits the same full seven-component tuple. A mechanical Cartesian expansion MUST report zero duplicate tuples and zero reachable unclassified tuples. Zero or multiple matches is `CONDITION_STATE_INVALID`.

### 7.2 Decision-window anchors

```text
decision_lower_ts_ms = first_trade_ts_ms + 3_600_000
decision_window = [decision_lower_ts_ms, resolved_at_ts_ms)
```

Precedence is exact:

1. missing, null, malformed, non-UTC, duplicate-conflicting, out-of-range, or precision-losing resolution value → P04;
2. otherwise missing/null first-trade anchor → P03;
3. otherwise malformed/conflicting first-trade or safe-integer overflow in warm-up addition → P04 with input-integrity reason;
4. otherwise `decision_lower_ts_ms >= resolved_at_ts_ms` → P02 valid exclusion;
5. otherwise → P01 query eligible.

Only two present, valid integer-millisecond anchors may create P02.

### 7.3 Token-pair reducer

For each query-eligible condition, reduce distinct source tuples `(condition_id,token_id,outcome_index)`. Exactly one distinct valid token at each outcome index, with distinct token IDs, creates `STABLE_INDEPENDENT_PAIR`. No tuple may contain or be selected by winner, payout, resolution label, price coverage, profitability, or later-stage evidence. Missing/non-bijective identity is `UNRESOLVED`; conflicts are `UNSTABLE`; invalid decimal token precision is `PRECISION_INVALID`; all produce P06.

### 7.4 Effect precedence

`BLOCKING_DEFECT > INCOMPLETE_EVIDENCE > LIMITATION > VALID_EXCLUSION > CLEAR_COMPONENT > ACTIVE`.

The highest evidenced effect is retained; lower evidence cannot hide it.

## 8. Population equations and denominators

For each subclass `s` and pooled:

```text
U0_s = V_s ⊎ Ew_s ⊎ Im_s ⊎ Br_s
T_s = V_s = Ts_s ⊎ Tu_s ⊎ Tunstable_s ⊎ Tprecision_s
P_s = Ts_s = Rc_s ⊎ Ri_s ⊎ Rb_s
Rc_s = C2_s ⊎ C1_s ⊎ C0_s ⊎ Ci_s ⊎ Cb_s
L_s = C2_s ⊎ C1_s ⊎ C0_s
L_s = B_s ⊎ O_s ⊎ N_s ⊎ Li_s ⊎ Lb_s
U0_s = E_s ⊎ I_s
```

Fixed subclass denominators:

```text
|U0_UP_DOWN| = 22,012
|U0_OVER_UNDER| = 1,003
|U0_NAMED_OTHER| = 16,678
39,693 = 22,012 + 1,003 + 16,678
```

Pooled equations are the disjoint union of subclass equations. Every condition appears exactly once in K037, K108, and K141. Applicable denominators narrow by explicit equations; no row disappears. Missing anchors, request failures, invalid identities, one-side outcomes, or neither-side outcomes MUST NOT be omitted from the complete denominator.

A valid exclusion remains present in all complete ledgers, is not request or alignment applicable, may coexist with exact global clear, and is always consumer-ineligible.

---

## 9. S4 local-input preparation and scientific processing ledger

### 9.1 Exact K036 consumed-input manifest

K036 contains exactly nine ordered rows with roles:

1. `CANONICAL_INPUT_SET` → exact K001;
2. `ACCEPTED_CANDIDATE08` → exact K011;
3. `P0_CLEAR_RECORD`;
4. `CONDITION_UNIVERSE`;
5. `CLASSIFICATION_ROWS`;
6. `RESOLUTION_ROWS`;
7. `FIRST_TRADE_ROWS`;
8. `TOKEN_OUTCOME_TUPLES`;
9. `S4_ACTIVITY_ROOT` → exact K035.

Every row requires `input_role`, exact `logical_path`, JCS-safe `ByteLength`, SHA-256, media type, row-schema ID, permitted-root classification, identity-binding mode, and `required=true`. The exact paths and schemas are materialized in §23 `nodes.K036.node_specific_constants.consumed_input_rows`: the canonical P0 row is fixed to the exact K000 canonical-read path; the five normalized local sources are fixed under one K035-declared input root; K001/K011/K035 use their exact workflow-node paths. Rows occur only in the declared order and are unique by role and path. Any missing/extra/aliased/case-folded row, wrong byte identity, unapproved root, stale contract, or schema mismatch blocks before row parsing.

### 9.2 Exact source schemas and deterministic parsing

The machine schemas are in §23 `row_schemas`.

- **Condition universe:** exactly 39,693 `ConditionUniverseRow` rows, ordinal `0..39692`, unique condition IDs, all `P0_ELIGIBLE`. Duplicate-identical rows are forbidden at finalization rather than silently retained; any duplicate ordinal or condition blocks.
- **Classification:** exactly one `ClassificationRow` per universe condition. Exact duplicates are idempotent during ingestion; differing subclass values block. Final materialization has one row per condition and fixed counts 22,012/1,003/16,678.
- **Resolution:** exactly one reduced `ResolutionSourceRow` per condition. Accepted non-null grammar is exactly `YYYY-MM-DD HH:MM:SS UTC` or `YYYY-MM-DD HH:MM:SS.fff UTC`; `.fff` is exactly three digits. Gregorian calendar validity, UTC suffix, range, and integer-millisecond conversion are mandatory. Null, missing, malformed, conflicting, more/less fractional precision, leap-second text, offset text, or floating conversion is `BLOCKED_RESOLUTION_BOUNDARY`.
- **First trade:** same strict timestamp grammar. Null/missing is `INCOMPLETE_MISSING_TRADE_ANCHOR`. Malformed or conflicting non-null input is blocking. No sub-millisecond rounding is permitted.
- **Token/outcome tuples:** exact fields `condition_id`, `token_id`, `outcome_index`; no additional fields. Exact duplicate tuples are idempotent during ingestion and removed before finalization. More than one token per outcome, same token on both outcomes, invalid token decimal, missing side, or any forbidden winner/result/price field blocks.

All joins are exact by `condition_id`; no case folding, whitespace trimming, fuzzy matching, or fallback key is allowed. Extra source rows outside U0 block. Missing classification blocks. Missing resolution blocks. Missing first trade is incomplete. Missing or conflicting token tuples for a valid window block.

### 9.3 K037, A003, A004, K038, K041

K037 has exactly 39,693 rows sorted by condition ID, unique by condition ID, and each row MUST match exactly one §23 P-class. Winner, payout, result, and selected-side fields are forbidden.

A003 serializes only the closed `A003_CONDITION_LEDGER_PROJECTION_V1` scientific payload: canonical commit, exact universe and subclass counts, row count, and ordered `ConditionProjectionRow` values. It has no node ID, record ID, dependencies, creation timestamp, authorization, root, actor, environment, physical path, handoff, or review identity. Its typed K037 derivation edge is a nonserialized schema-edge contract. A004 separately binds K035/K036/K037/A003 activity provenance.

K038 reconciles every §8 equation, source-row count, duplicate-reduction count, window state, token state, subclass total, and P-class count. Its status is `PASS` only when all equations and identities are complete; `FAIL` on any contradiction; `INCOMPLETE` only on missing evidence without contradiction. K041 may accept a conforming result or accepted finding but authorizes nothing and does not create S5.

## 10. S5 safe-span policy

### 10.1 Exact artifacts

K045 is the deterministic preflight plan: strictly increasing positive candidate spans, exact safety margin, immutable outcome-blind canary requests, method `GET /prices-history`, `fidelity=1`, `interval=null`, and explicit body/point/time bounds. K046 records every attempt. K047 closes the candidate matrix. K048 is the non-authorizing handoff. K049 proposes only the K047-selected value. K050 reviews it. K051 and K052P exist only after approval; K052N is the mutually exclusive negative branch.

### 10.2 Total per-attempt classifier

`TransportResult` is a closed enum. Every attempt first validates its row-domain invariants and then matches exactly one ordered rule in §23:

1. any cross-field domain violation → `INTEGRITY_FAILURE`;
2. identity conflict → `INTEGRITY_FAILURE`;
3. unauthorized route/host/credential use or redirect → `INTEGRITY_FAILURE`;
4. HTTP body over the authorized byte bound → `UNSAFE`;
5. `TIMEOUT`, `DNS_FAILURE`, `CONNECTION_FAILURE`, `TLS_FAILURE`, or `CONNECTION_RESET` → `INCOMPLETE`;
6. `RESOURCE_BOUND_REJECTION` → `UNSAFE`;
7. `LOCALLY_CANCELLED` or `UNKNOWN_TRANSPORT_FAILURE` → `INTEGRITY_FAILURE`;
8. HTTP 408, 425, 429, or 5xx → `INCOMPLETE`;
9. identity-matching HTTP 413 or 414 → `UNSAFE`;
10. every other non-200 response → `INTEGRITY_FAILURE`;
11. HTTP 200 wrong content type → `INTEGRITY_FAILURE`;
12. HTTP 200 malformed JSON, wrong shape, duplicate key, malformed point, forbidden field, or precision loss → `INTEGRITY_FAILURE`;
13. valid HTTP 200 response over the point bound → `UNSAFE`;
14. valid bounded HTTP 200 response, including exact `{"history":[]}` → `SAFE`.

The closed transport enum, domain-invalid catch-all, and complete HTTP partition prove totality. A zero-match or multi-match attempt is `PREFLIGHT_INTEGRITY_FAILURE`. No implementation discretion may relabel an observation.

### 10.3 Candidate reducer

For candidate set C, `C_safe` contains c iff every required canary has exactly one final SAFE observation and no contradiction. Precedence: integrity failure; missing/incomplete; no safe candidate; compute safe ceiling; apply exact margin; no candidate after margin; select maximum remaining candidate. Counts satisfy `expected_attempt_cells=|C|×|canaries|` and each cell ends in exactly one final classifier state. Only approved K050 may create K051/K052P. Every negative branch prohibits S6.

## 11. S6 deterministic request planning and acquisition

### 11.1 Deterministic independent plan

For each valid-window stable pair:

```text
query_envelope_start_s = max(0,floor(decision_lower_ts_ms/1000)-1)
query_envelope_end_s = ceil(resolved_at_ts_ms/1000)
```

Chunks are contiguous half-open second envelopes with the exact approved span. Each side is planned independently. Every row uses one real token ID, one outcome index, `GET /prices-history`, `fidelity=1`, `interval=null`, and the exact request-ID JCS preimage. Batch calls, complement generation, winner-conditioned ordering, or omitted side plans are forbidden.

A005 serializes only `A005_REQUEST_PLAN_PROJECTION_V1`: canonical commit, plan profile, approved span, condition/token/request counts, and ordered `RequestPlanProjectionRow` values. It contains no activity provenance. Its K056F and K057 derivation edges are nonserialized schema-edge contracts. A006 is the separate activity-provenance wrapper.

### 11.2 Exact endpoint response schema

A recognized successful response is:

```json
{"history":[{"t":1700000000,"p":"0.5"}]}
```

Normative rules:

- status exactly HTTP 200;
- content type token exactly `application/json`, optionally `; charset=utf-8`, tokens case-insensitive and OWS-tolerant; no other media type or charset;
- top level is an object with exactly one field `history`;
- `history` is an array in wire order;
- each point is an object with exactly fields `t` and `p`;
- `t` is a JSON integer `UtcSecond`;
- `p` is a JSON string or JSON number lexeme matching `0|1|0.[0-9]{1,76}`, no sign/exponent; exact lexeme is preserved and normalized without binary floating point;
- additional top-level or point fields are forbidden;
- the only recognized empty representation is HTTP 200 JSON `{"history":[]}` under these exact shape rules;
- missing/null history, empty body, `{}`, 204, 404, or a client-error body is not recognized empty;
- one malformed point blocks the entire response; point skipping is forbidden.

### 11.3 Total transport/HTTP/body-to-terminal mapping

K059F uses only:

`PAYLOAD_COMPLETE | EMPTY_COMPLETE | TRANSIENT_EXHAUSTED | MALFORMED_BLOCKING | IDENTITY_MISMATCH_BLOCKING | UNAUTHORIZED_BLOCKING`.

`NOT_FOUND_COMPLETE` and `CLIENT_REJECTED_COMPLETE` are forbidden. No client rejection is complete evidence.

The exact ordered mapping in §23 covers every `TransportResult` and every HTTP/body state. A cross-field-invalid attempt is `MALFORMED_BLOCKING`. Identity conflicts block next; authorization or redirect violations block after that. `TIMEOUT`, `DNS_FAILURE`, `CONNECTION_FAILURE`, `TLS_FAILURE`, and `CONNECTION_RESET` retry while attempts remain and become `TRANSIENT_EXHAUSTED` at the exact maximum. `LOCALLY_CANCELLED`, `RESOURCE_BOUND_REJECTION`, and `UNKNOWN_TRANSPORT_FAILURE` are `MALFORMED_BLOCKING` during full acquisition. Valid bounded HTTP 200 nonempty and exact-empty responses become the only complete terminals. HTTP 408/425/429/5xx retry or exhaust. HTTP 3xx/401/403 is unauthorized. Every remaining HTTP state, including 404, 413, 414, malformed 200, oversized body, excessive point count, and protocol-invalid status, is `MALFORMED_BLOCKING`.

A terminal is emitted only from an exact attempt row, never inferred. Zero or multiple mapping matches is an acquisition integrity failure.

### 11.4 Retry and `Retry-After`

For retry-eligible attempt n:

```text
base_ms = 5000 if n = 1, otherwise 20000
next_delay_ms = min(max(base_ms,retry_after_contribution_ms),60000)
```

`Retry-After` accepts either:

1. decimal seconds matching `^(0|[1-9][0-9]*)(\.[0-9]{1,3})?$`, multiplied exactly by 1000 using integer arithmetic; or
2. IMF-fixdate, converted to UTC epoch milliseconds and subtracted from exact `response_received_at_ms` of attempt n.

Past dates contribute 0. Invalid, multiple-valued, >3-fractional-digit, non-IMF date, or overflowing values are recorded as `INVALID_IGNORED` or `OVERFLOW_IGNORED` and contribute 0; they do not change the HTTP classification. Parsed values are capped at 60,000 ms. The delay applies only before attempt n+1. If n is max attempts, it is recorded but no delay occurs. Jitter is forbidden. Interpreting delay seconds directly as milliseconds is `STOP_RETRY_AFTER_UNIT_INVALID`.

### 11.5 Attempts, terminals, inventory, completion, archive, reconciliation

K058F attempt ordinals are contiguous from 1 and immutable. Payload identity fields are all-null or all-present. K059F has one terminal per finalized request. K060 inventories every attempt, terminal, and payload exactly once. K061 uses:

`planned = payload_complete + empty_complete + transient_exhausted + blocking_terminal`.

`COMPLETE` requires terminal count=planned, transient=0, blocking=0. `INCOMPLETE` requires no blocking and at least one missing/transient. `BLOCKED` requires at least one blocking terminal. K062/K063 retain exact deterministic ustar identity.

A007 serializes only `A007_RAW_PAYLOAD_ROOT_PROJECTION_V1`: canonical commit, raw profile, request/member counts, total payload bytes, and ordered raw payload entries. It excludes all activity provenance. Its K060/K061/K062/K063 derivation edges are nonserialized schema-edge contracts. A008 separately binds acquisition activity provenance. K064 reconciles every condition, side, request, attempt, terminal, payload, archive member, and scientific projection. K065 is non-authorizing.

### 11.6 Bounds, resume, and finalization

All numeric bounds are JCS-safe integers. Resume is permitted only under exact K055, K057, A005, endpoint identity, and authorizations; it may add only the next missing retry-eligible attempt. Final terminals are immutable. Recompute K060/K061 from raw evidence after interruption. Finalize once every plan row has one terminal and all identities reconcile. Any later conflict requires a new accepted correction and new dual-control root.

## 12. S7 scientific construction

### 12.1 Accepted construction contract K068

K068 binds exact Candidate 08 acceptance K011 and accepted implementation-source K018. It fixes:

- serialization profiles in §3;
- request and raw projection profiles;
- payload parser profile;
- duplicate reducer;
- partition layout;
- row schema;
- build-ID and row-key algorithms;
- reconciliation equations.

### 12.2 `deterministic_build_id`

The actual preimage is one closed object of registered type `BuildIdentityPreimage`:

```json
{
  "schema_id": "pm_research.s2.deterministic_build_identity.v3",
  "canonical_commit": "<GitCommit40 copied from K000 canonical_commit>",
  "construction_contract": {
    "node_id": "K068",
    "logical_path": "<K068 NodeIdentity logical_path>",
    "byte_length": "<K068 NodeIdentity ByteLength>",
    "sha256": "<K068 NodeIdentity Sha256>"
  },
  "s4_condition_ledger_projection": {
    "node_id": "A003",
    "logical_path": "<A003 NodeIdentity logical_path>",
    "byte_length": "<A003 NodeIdentity ByteLength>",
    "sha256": "<A003 NodeIdentity Sha256>"
  },
  "request_plan_projection": {
    "node_id": "A005",
    "logical_path": "<A005 NodeIdentity logical_path>",
    "byte_length": "<A005 NodeIdentity ByteLength>",
    "sha256": "<A005 NodeIdentity Sha256>"
  },
  "raw_payload_root_projection": {
    "node_id": "A007",
    "logical_path": "<A007 NodeIdentity logical_path>",
    "byte_length": "<A007 NodeIdentity ByteLength>",
    "sha256": "<A007 NodeIdentity Sha256>"
  },
  "serialization_profile_id": "pm_research.s2.serialization.v1",
  "construction_algorithm_id": "pm_research.s2.construction.v1"
}
```

Angle-bracket values above denote typed materialization slots, not serialized literal strings. The normative §23 constructor names every source field as `node_id`, `logical_path`, `byte_length`, or `sha256`; aliases `.id` and `.path` are forbidden.

```text
deterministic_build_id =
SHA256(UTF8(RFC8785_JCS(actual BuildIdentityPreimage object)))
```

No authorization, stage authorization, root, run ID, actor, host, environment, execution timestamp, physical output root, alignment policy, partition hash, descendant manifest/reconciliation hash, inventory hash, handoff ID, or review ID may enter the preimage.

### 12.3 Payload parsing and normalization

Each recognized payload MUST parse to an ordered source array of points with source timestamp seconds and price. For each raw point:

- source timestamp MUST be an integer `UtcSecond`;
- normalized timestamp is `price_ts_utc_ms = price_ts_utc_s * 1000`;
- price MUST normalize to `CanonicalDecimalPrice`;
- requested token identity comes only from A005/A007;
- raw-point ordinal is zero-based in the exact payload array;
- malformed point, unknown shape, precision loss, or identity mismatch is blocking.

Only rows satisfying:

```text
decision_lower_ts_ms <= price_ts_utc_ms < resolved_at_ts_ms
```

are scientifically included. No integer-second truncation of either anchor is permitted.

### 12.4 Deterministic source row and row key

```text
deterministic_source_row_id = SHA256(UTF8(JCS({
  "schema_id":"pm_research.s2.source_row_identity.v1",
  "request_id":request_id,
  "payload_member_sha256":payload_member_sha256,
  "raw_point_ordinal":raw_point_ordinal,
  "normalized_source_timestamp_ms":price_ts_utc_ms,
  "canonical_decimal_price":price
})))
```

```text
row_key_sha256 = SHA256(UTF8(JCS({
  "schema_id":"pm_research.s2.price_row_key.v2",
  "deterministic_build_id":deterministic_build_id,
  "condition_id":condition_id,
  "token_id":token_id,
  "outcome_index":outcome_index,
  "price_ts_utc_ms":price_ts_utc_ms,
  "deterministic_source_row_id":deterministic_source_row_id
})))
```

Original and rebuild compute both identities independently from A003, A005, and A007. Original output bytes are forbidden as a rebuild source.

### 12.5 Price-row schema and order

```json
{
  "schema_id":"pm_research.s2.per_token_price_row.v1",
  "deterministic_build_id":"Sha256",
  "condition_id":"ConditionId",
  "subclass":"Subclass",
  "token_id":"TokenId",
  "outcome_index":"OutcomeIndex",
  "price_ts_utc_s":"UtcSecond",
  "price_ts_utc_ms":"UtcMs",
  "price":"CanonicalDecimalPrice",
  "deterministic_source_row_id":"Sha256",
  "row_key_sha256":"Sha256"
}
```

Within each of the six fixed partition files, rows sort by:

```text
(condition_id UTF-8, price_ts_utc_ms integer, row_key_sha256 ASCII)
```

### 12.6 Duplicate and conflict reducer

- form groups by `(condition_id,token_id,outcome_index,price_ts_utc_ms)`;
- if a group contains more than one canonical price, emit `DUPLICATE_PRICE_CONFLICT` and block;
- if every point in a group has the same canonical price, retain exactly the point with lexicographically smallest `deterministic_source_row_id`; this is the sole overlap-deduplication tie-break;
- exact duplicate raw entries and duplicate-identical row bytes are idempotent;
- duplicate row keys with different bytes are blocking;
- the discarded same-price source identities are retained only in the non-byte-compared K076/K099 provenance inventories;
- no averaging, midpoint, interpolation, carry-forward, later-point preference, request-order preference, or arbitrary winner selection is permitted.

### 12.7 Construction disposition and separated bytes

For each request-complete condition:

- at least one included row on each side → `BOTH_PARTITIONS_INCLUDED`;
- rows on exactly one side → `ONE_PARTITION_INCLUDED`;
- rows on neither side → `NO_PARTITION_INCLUDED`;
- missing required raw evidence → construction incomplete;
- malformed, conflicting, or unauthorized evidence → construction blocked.

K073F materializes exactly six activity-free JSONL partition-member payloads. K074 materializes one activity-free scientific-manifest payload. K075 materializes one activity-free scientific-reconciliation payload. Their typed direct edges are schema-edge contracts and are not serialized into those payloads.

K076 is the separate original provenance wrapper. It carries the original node/record IDs, dependencies, timestamp, activity root, actor, environment, physical output root, and exact identities of all eight scientific payload units. K076 MUST NOT enter any scientific hash or byte comparison. K077 is created after K073F–K076 finalization.

## 13. Alignment policy and S8A

### 13.1 Policy interface

K080P candidate fields:

```text
selector = EXACT_COINCIDENT_PAIR | FIRST_AT_OR_AFTER_ANCHOR
max_side_staleness_ms = UInt64Dec
max_inter_side_skew_ms = UInt64Dec
tie_break_rule = EARLIEST_PRICE_TS_THEN_ROW_KEY_SHA256
```

Interpolation, carry, averaging, midpoint, and complement are forbidden.

Only a real K080P reviewed through K081P and accepted as K082 plus K083P may create K085, K084, and K086. Candidate absence uses K080A → K081A → K083A and halts. Rejection, deferral, or verification requirement uses K083R and halts.

### 13.2 Exact selectors

For both selectors, candidate rows must satisfy the exact millisecond boundary in §12.3.

`EXACT_COINCIDENT_PAIR`:

- form all side-0/side-1 pairs with equal source second;
- order by timestamp, side-0 row key, side-1 row key;
- choose the first pair whose two staleness values are within `max_side_staleness_ms`;
- skew is zero;
- no pair → `NEITHER_SIDE_USABLE::NO_COINCIDENT_PAIR`;
- pairs exist but all stale → `NEITHER_SIDE_USABLE::STALE_COINCIDENT_PAIR`;
- this selector never emits one-side usable.

`FIRST_AT_OR_AFTER_ANCHOR`:

- independently choose minimum `(price_ts_utc_s,row_key_sha256)` per side;
- `staleness_ms = price_ts_utc_s*1000 - decision_lower_ts_ms`;
- `inter_side_skew_ms = abs(side_0_ts_s-side_1_ts_s)*1000`;
- both selected, both within staleness, skew within limit → `BOTH_SIDE_USABLE`;
- exactly one valid selected side → `ONE_SIDE_USABLE::OTHER_SIDE_MISSING_OR_STALE`;
- neither valid → `NEITHER_SIDE_USABLE::NO_VALID_SIDE`;
- both individually valid but excessive skew → `NEITHER_SIDE_USABLE::INTER_SIDE_SKEW_EXCEEDED`.

### 13.3 K087 and K088

K087 has exactly one row per condition and records:

- construction category;
- accepted policy identity;
- selected row keys per side nullable;
- selected timestamps/prices nullable;
- staleness and skew nullable;
- alignment status and reason.

K088 reconciles all §8 alignment equations by subclass and pooled. One-side and neither-side outcomes are limitations, never negative evidence and never consumer eligible.

---

## 14. S8B deterministic rebuild

### 14.1 Exact isolation boundary

The isolated rebuild read set is exactly:

1. K068;
2. A003;
3. A005;
4. A007;
5. the fixed accepted construction-algorithm and serialization-profile definitions named by K068.

No K082, alignment policy, K073F, K074, K075, K076, K077, original physical path, original row key, original hash, prior comparison, handoff, authorization, root, actor, environment, or timestamp may be read. K095 records the authorized rebuild controller and proves the read set; it is not a scientific input. Reading K082 is `STOP_REBUILD_SOURCE_ISOLATION_VIOLATION` and cannot be excused as optional.

### 14.2 Rebuilt outputs and payload-only comparison

K096F independently reconstructs six activity-free partition-member payloads from only K068, A003, A005, A007, and fixed profiles. K097 reconstructs the activity-free manifest payload. K098 reconstructs the activity-free reconciliation payload. K099 is the separate rebuild provenance wrapper; it is expected to differ from K076.

K101 compares exactly eight payload byte pairs:

1. six K073F member payloads against the corresponding six K096F member payloads;
2. K074 scientific-manifest payload against K097 scientific-manifest payload;
3. K075 scientific-reconciliation payload against K098 scientific-reconciliation payload.

It MUST NOT compare complete node records or provenance envelopes. Original/rebuild `node_id`, `record_id`, `dependencies`, `created_at_utc_ms`, authorizations, activity roots, run IDs, actors, environments, physical roots, and wrappers are excluded.

PASS requires all eight exact byte-length and SHA-256 equalities. Any differing present payload is FAIL/blocking. Any absent expected payload with no contradiction is INCOMPLETE. K100 may inventory original outputs only after rebuild finalization and is never visible to the rebuild actor.

## 15. S8C audit, evidence closures, and gate

### 15.1 K108 complete effect ledger

K108 contains exactly 39,693 unique condition rows sorted by condition ID. Each row carries exact final P-class, evidence refs, effect, reason, and subclass. Counts of `CLEAR_COMPONENT`, `VALID_EXCLUSION`, `LIMITATION`, `INCOMPLETE_EVIDENCE`, and `BLOCKING_DEFECT` sum to 39,693.

### 15.2 Total closure schema

Every K109–K127 closure uses the exact §23 `audit_closure.v1` schema:

```text
population_count = applicable_count + not_applicable_count
applicable_count = pass_count + fail_count + incomplete_count
```

- `FAIL` iff `fail_count>0`; effect `BLOCKING_DEFECT`; non-null blocking stop.
- `INCOMPLETE` iff `fail_count=0` and (`incomplete_count>0` or population is zero when zero is forbidden); effect `INCOMPLETE_EVIDENCE`; non-null incomplete stop.
- `PASS` iff `fail_count=0`, `incomplete_count=0`, all evidence/schema/equations pass, and population is nonzero or zero is explicitly permitted; effect `CLEAR_COMPONENT`; null stop.

No other status/effect/stop combination is legal. Missing evidence is incomplete; malformed, contradictory, unauthorized, winner-leaking, synthesis-bearing, identity-invalid, or edge-invalid evidence fails. Details are unique by subject key and reconcile to counts.

### 15.3 Nineteen denominators

| Closure | Check | Denominator | Zero permitted |
|---|---|---|---|
| K109 | canonical base integrity | 5 exact identities | no |
| K110 | complete universe reconciliation | 39,693 conditions | no |
| K111 | decision-window integrity | 39,693 conditions | no |
| K112 | token-pair integrity | K037 query-eligible count | yes |
| K113 | span-policy integrity | candidate count × canary count | no |
| K114 | request-plan integrity | K057 plan rows | yes |
| K115 | terminal completeness | K057 plan rows | yes |
| K116 | raw-archive closure | K060 inventory entries | yes |
| K117 | independent token acquisition | 2 × stable-pair conditions | yes |
| K118 | no synthesis | plan rows + original rows + rebuilt rows | yes |
| K119 | original construction integrity | 39,693 conditions | no |
| K120 | duplicate-conflict integrity | duplicate timestamp groups | yes |
| K121 | alignment-policy integrity | 1 accepted policy chain | no |
| K122 | alignment execution | construction alignment-applicable count | yes |
| K123 | decision-time coverage | K037 alignment-applicable count | yes |
| K124 | deterministic build identity | 4 identity assertions | no |
| K125 | rebuild byte equality | 8 byte comparisons | no |
| K126 | condition-effect reconciliation | 39,693 conditions | no |
| K127 | authorization/handoff provenance | 59 exact predecessor records | no |

Each closure's exact evidence NodeRefs remain those in Appendix A. A009 is created after K108 and K109–K126 and before K127; K127 audits A009. K132 is later and is not a K127 predecessor.

### 15.4 K128–K132

K128 contains exactly K109–K127 in order, counts 19 statuses/effects, and reduces `FAIL > INCOMPLETE > PASS`. K129 combines K108 and K128 into exactly one gate state. K130 is a Markdown rendering of K129 only. K131 proves K108/K128/K129/K130 exact agreement. K132 is the final non-authorizing S8C handoff after all prior bytes.

Gate precedence is `BLOCKING > INCOMPLETE > LIMITATION > VALID_EXCLUSION > CLEAR`. `S2_GATE_CLEAR` requires all 19 PASS, K101 PASS, exact 39,693 closure, no limitation/incomplete/blocking effect, and every alignment-applicable condition BOTH_SIDE_USABLE. Valid exclusions may coexist with clear. Clear with limitations, incomplete, and blocked remain distinct and non-authorizing.

## 16. S9 review

K133 is derived only from exact K132 identity. K134 records Sentinel's review. K135 reconciles K129, K131, K132, and K134. K136 is the review handoff.

Permitted outcomes:

| Submitted result | Permitted disposition | Progression |
|---|---|---|
| conforming exact clear | `APPROVE`; create K137 | may await K139, K138, K140 |
| conforming clear with limitations | `ACCEPT_FINDING` | halt; no S10 or P1 |
| conforming blocked finding | `ACCEPT_FINDING` | halt; no S10 or P1 |
| incomplete evidence | `DEFER` or `NEEDS_VERIFICATION` | halt pending separately authorized correction |
| package/specification defect | `BLOCK` | halt |

K137 exists only for approved exact clear. Acceptance of evidence is not gate clearance. Gate clearance is not S10 authorization.

---

## 17. S10 consumer transition

### 17.1 Eleven-conjunct predicate

For each condition, eligibility requires all true:

1. valid decision window;
2. stable independent token pair;
3. complete request evidence;
4. complete construction;
5. scientific artifact inclusion;
6. real accepted alignment policy;
7. `BOTH_SIDE_USABLE`;
8. exact `S2_GATE_CLEAR`;
9. approved Sentinel clear review K137;
10. matching K037/K108/K129/K134/K135 identities;
11. valid K140 root formed from K139 Gustavo authorization followed by K138 Sentinel authorization.

Any false conjunct places the condition in `I`. Failure reasons are ordered by conjunct number and retained as a nonempty array.

```text
U0 = E ⊎ I
|E| + |I| = 39,693
```

K141 contains exactly 39,693 rows and pooled/subclass counts.

### 17.2 Ineligible branch

Exact order:

```text
K141 → K142I → K143I → K144I
```

No P1-consumer specification candidate exists. Sentinel may accept the ineligible finding; no P1 authorization follows.

### 17.3 Eligible branch

Exact order:

```text
K141 → K142E candidate bytes → K143E candidate-sealing record
     → K144E handoff → K145E review → K146E accepted transition
```

K143E and K144E MUST identify exact K142E path, byte length, and SHA-256. No `CANDIDATE_SEALED` claim may exist before K142E bytes.

Even after K146E, P1 remains blocked until separate Gustavo K148, later Sentinel K147, and root K149 exist under a later accepted contract. This specification does not create or authorize them.

`named_binary_probe_blocked = true` remains unchanged.

---

## 18. Closed typed stops

The following stop codes are closed and MUST NOT be silently mapped to another outcome:

```text
STOP_AUTHORIZATION_ORDER_INVALID
STOP_AUTHORIZATION_PROVENANCE_INVALID
AUTHORIZATION_PREREQUISITE_BYTES_MISSING
AUTHORIZATION_SCOPE_EXPANSION
GLOBAL_STATE_INVALID
CONDITION_STATE_INVALID
STOP_CANONICAL_BASE_MISMATCH
STOP_P0_NOT_CLEAR
STOP_STALE_CONTRACT
STOP_INPUT_IDENTITY_MISMATCH
STOP_UNIVERSE_RECONCILIATION_FAILED
STOP_RESOLUTION_BOUNDARY_INVALID
STOP_TRADE_ANCHOR_MISSING
STOP_TOKEN_ENUMERATION_UNRELIABLE
STOP_PRECISION_LOSS
PREFLIGHT_INTEGRITY_FAILURE
PREFLIGHT_INCOMPLETE
NO_SAFE_SPAN
NO_SAFE_SPAN_AFTER_MARGIN
STOP_REQUEST_PLAN_INVALID
STOP_REQUEST_TERMINALS_INCOMPLETE
STOP_RAW_ARCHIVE_INCOMPLETE
STOP_RAW_ARCHIVE_IDENTITY_MISMATCH
STOP_ENDPOINT_SHAPE_UNRECOGNIZED
STOP_FORBIDDEN_SYNTHESIS
DUPLICATE_PRICE_CONFLICT
SCIENTIFIC_PROJECTION_CONFLICT
SCIENTIFIC_RAW_PROJECTION_MISMATCH
ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN
STOP_DETERMINISTIC_BUILD_ID_MISMATCH
STOP_REBUILD_SOURCE_ISOLATION_VIOLATION
STOP_REBUILD_BYTE_MISMATCH
STOP_ALIGNMENT_POLICY_ABSENT
STOP_ALIGNMENT_POLICY_INVALID
STOP_ALIGNMENT_INCOMPLETE
PROVENANCE_EDGE_SET_MISMATCH
STOP_AUDIT_SELF_REFERENCE
STOP_GATE_RECONCILIATION_FAILED
STOP_S9_NOT_APPROVED_CLEAR
STOP_TRANSITION_RECONCILIATION_FAILED
STOP_CANDIDATE_SEAL_PREMATURE
STOP_P1_NOT_SEPARATELY_AUTHORIZED
ARCHITECTURE_CONTROL_SET_INVALID
STOP_DUPLICATE_IDENTITY_CONFLICT
STOP_RESOURCE_BOUND_EXCEEDED
STOP_RESUME_PROVENANCE_INVALID
STOP_RETRY_AFTER_UNIT_INVALID
STOP_ZERO_POPULATION_NOT_PERMITTED
STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED
STOP_UNEXPECTED_DELIVERABLE_PATH
```

A stop preserves all evidence already emitted. No retry, resume, or correction is permitted unless the stop definition marks the underlying request attempt retry-eligible or a separately accepted correction and new authorization root exists.

---

## 19. Required counterexamples

| Counterexample | Required result |
|---|---|
| Sentinel stage authorization before Gustavo authorization | `STOP_AUTHORIZATION_ORDER_INVALID`; no root |
| Gustavo authorization without later Sentinel activation | no root; lifecycle waits |
| accepted result automatically starts next stage | `GLOBAL_STATE_INVALID`; no progression |
| normative dependency on Candidate 01 or 02 | `ARCHITECTURE_CONTROL_SET_INVALID` / specification block |
| activity field enters A003, A005, A007, K073F/K074/K075, or rebuild equivalents | blocking scientific-identity failure |
| original and rebuild compute different row keys | K125 fail; gate blocked |
| missing or conflicting scientific projection | incomplete or `SCIENTIFIC_PROJECTION_CONFLICT`; no build |
| prerequisite acceptance ID exists but bytes cannot load | `AUTHORIZATION_PREREQUISITE_BYTES_MISSING`; K127 incomplete |
| missing/malformed resolution anchor | blocking boundary state, never invalid-window exclusion |
| valid anchors produce nonpositive window | immutable valid exclusion |
| no safe span | no K051/K052P; no S6 |
| absent alignment-policy candidate | K080A→K081A→K083A; halt |
| first-at-anchor yields one valid side | `ONE_SIDE_USABLE`; limitation; ineligible |
| no valid side or excessive skew | `NEITHER_SIDE_USABLE`; limitation; ineligible |
| audit evidence omits one required dependency | closure incomplete and `PROVENANCE_EDGE_SET_MISMATCH` |
| schema-derived edge set differs by one edge | specification failure; no acceptance |
| sealing record exists before K142E bytes | `STOP_CANDIDATE_SEAL_PREMATURE` |
| limited or incomplete result attempts P1 | `STOP_P1_NOT_SEPARATELY_AUTHORIZED`; no S10/P1 root |
| K132 is inserted into K127 | `STOP_AUDIT_SELF_REFERENCE`; cycle |
| winner token is used to enumerate a side | token-pair and no-synthesis checks fail |
| one side is computed as `1-price` | blocking no-synthesis failure |

---

## 20. Acceptance methods

Specification acceptance is static and does not authorize execution. Sentinel review SHOULD verify:

1. exact canonical commit and exact A002 identity;
2. all normative dependencies exclude Candidates 01 and 02;
3. all schemas are closed for types, nullability, units, bounds, and order;
4. every state vector reduces exactly once;
5. every population equation retains all 39,693 rows;
6. authorization order is Gustavo before later Sentinel for all thirteen activities;
7. all three scientific projections and three wrappers are explicit;
8. build and row identities exclude activity provenance;
9. original/rebuild comparison boundary is exact;
10. all nineteen evidence arrays match Appendix A;
11. Stage-10 branch order is exact;
12. Appendix-A schema edge equality has no missing or extra edge.

Future conformance methods may include static inspection, schema validation, unit tests, integration tests, invariant checks, byte comparisons, and separately authorized empirical runs. Naming those methods here authorizes none of them.

---

## 20.1 Third-correction raw-deliverable conformance gate

A submission has `STATIC_SUBMISSION_CLEAR` only when all eleven checks in §23 `static_validation_contract.mandatory_raw_deliverable_checks` return PASS against the sealed raw K008 and K009 bytes. Validation of K006/K005/K007 alone is insufficient. K008 and K009 extraction counts MUST each equal one; each extracted JSON value MUST validate its assigned closed profile; K009's self-excluding projection MUST verify; its binding-location enum MUST be registered; and prose/registry type, `RecordId`, and `RelativePath` rules MUST agree. Any failure yields `STATIC_SUBMISSION_BLOCKED` and the handoff MUST NOT claim static clear.

`RecordId` is exactly nonempty ASCII of 1..160 UTF-8 bytes everywhere. A 160-byte value is valid; a 161-byte value is invalid.

`RelativePath` is accepted only when the supplied string already equals Unicode NFC. A validator MUST reject, not normalize, a canonically equivalent non-NFC string because paths enter ordering and hash preimages.

The normative type scan excludes exact quoted authorization text stored as `SchemaLiteral`; quoted authorization wording is not a type declaration. Outside `SchemaLiteral`, every alignment-policy 64-bit field and every normative type reference uses registered `UInt64Dec`.

## 21. Required self-attack

| Attack | Failure constructed | Required defense / result |
|---|---|---|
| Different original/rebuild envelopes | K076 has node `K076`; K099 has node `K099` | expected; wrappers are not compared; only eight activity-free payload pairs are compared |
| Timestamp contamination | `created_at_utc_ms` inserted into A003 or K074 payload | closed scientific schema rejects field; deterministic identity changes and conformance blocks |
| Exact K006 rejected | generic authorization schema requires a field absent from supplied K006 | forbidden; exact-current-record schema deep-equals the supplied 4675-byte JCS object |
| Arbitrary projection container | arbitrary JSON stored as `normalized_value_jcs` for A003/A005/A007 | rejected; three distinct closed schemas require exact named fields and row types |
| Undefined build aliases | preimage uses `K068.id` or `K068.path` | rejected; only `node_id`, `logical_path`, `byte_length`, `sha256` exist |
| Unresolved schema type | field declares `JcsSafeUInt UtcSecond` or unregistered 64-bit integer type | unknown-type scan fails; zero findings required |
| Global-state placeholder | vector contains `X`, `successor_review(X)`, conditional prose, or non-enum halt | registry validation fails; all 153 reducer rows have exact enum-valid vectors |
| Hidden K008 edge | descriptive K006 identity uses NodeRef-shaped field names | forbidden; descriptive metadata uses `NonEdgeIdentityMetadata`; extractor derives only K007 |
| Unknown transport class | no-response class is outside the enum | parsing rejects it; `UNKNOWN_TRANSPORT_FAILURE` is the explicit catch-all and maps to integrity failure |
| Exact-clear unreachable | valid K129 clear and K137 approval cannot reach K146E | reducer includes explicit exact-clear witness ending in `COMPLETE/APPROVE` |
| Copilot evidence mistaken for authorization | installed role-source documentation is treated as permission to invoke a role | forbidden; `AdministrativeRoleSourceContext.authorization_effect=NONE`, K006/K005/K007 forbid `COPILOT_ROLE_EXECUTION`, and handoff records `NOT_PERFORMED` |
| Copilot identity enters S2 provenance | `a7df418216cb7355b003164b8b509e40081cdbdc` is inserted into A007, K068, K072, an audit closure, or Appendix A | static non-dependency scan fails; role-source edge and scientific-dependency counts must both be zero |
| Missing authorization bytes | IDs present but exact K006/K005/K007 raw file absent | stop `STOP_AUTHORIZATION_PROVENANCE_INVALID`; no drafting/root reliance |
| Untyped decision identity | policy hash placed in free-text notes | closed profiles reject or non-edge type excludes; edge equality must remain exact |
| Malformed HTTP 200 | one point missing `p` | entire response `MALFORMED_BLOCKING`; no point skipping |
| Ambiguous client rejection | HTTP 404 treated as empty | forbidden; no 4xx is complete evidence |
| Retry units | `Retry-After: 10` treated as 10 ms | exact result 10,000 ms before cap; wrong unit stops |
| JCS 64-bit precision loss | 18446744073709551615 represented as JSON number | schema rejects; must be `UInt64Dec` string |
| Hidden K082 dependency | rebuild reads accepted alignment policy | isolation violation; K082 absent from scientific read set |
| Audit non-reconciliation | population 100, applicable 80, N/A 10 | equation fails because 80+10≠100 |
| Double P-class | vector engineered to match P14 and P15 | mechanical expansion returns zero overlaps across 31 legal tuples |
| Missing schema-derived edge | a typed binding is absent from Appendix A | 166/678 equality scan reports mismatch and blocks |
| K009 missing required field | omit `payload.static_checks` | K009-specific closed profile rejects the payload even if graph checks pass |
| K009 undeclared field | add `payload.notes` | `additional_fields=false` rejects it |
| Self-binding enum mismatch | payload uses a constant absent from `HandoffSelfIdentity` | registered constant and payload must both equal `EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD` |
| Remaining unregistered 64-bit integer type alias | use unresolved bare 64-bit type instead of registered `UInt64Dec` | whole-document type scan returns zero unresolved references |
| RecordId split bound | accept a 200-byte ID in one contract | both prose and registry cap at 160 UTF-8 bytes; 200 bytes rejected everywhere |
| Non-NFC path equivalence | decomposed and NFC paths compare canonically but differ in bytes | decomposed input is rejected before ordering or hashing; no normalization-on-read |
| K008 extraction multiplicity | zero or two `NORMATIVE_K008_PAYLOAD` blocks | extraction count must equal one or submission blocks |
| K009 profile false positive | graph checks pass while K009 omits or adds fields | assigned-profile validation is independently mandatory |
| False static clear | K006/K005/K007 validate but delivered K008/K009 do not | raw deliverable identity, extraction, profile, self-projection, type, bound, and NFC checks are conjunctive prerequisites |
| Strongest alternative | compare full node envelopes and normalize away provenance | rejected because normalization could conceal identity differences; explicit payload/envelope separation is deterministic |

Any defense that relies on implementation convention rather than the normative registry is insufficient.

### 21.1 Open decisions

Empirical span values, endpoint host, authorized concurrency/rate bounds, actual alignment selector/limits, observed coverage, and final consumer subset remain future evidence or policy decisions. Their absence does not permit defaults and does not authorize execution.

## 22. Authorization statement

This Candidate 08 returns to Sentinel for specification review. Professor does not approve it. Approval would accept specification text only. It would not authorize implementation, tests, data access, network activity, acquisition, construction, alignment, rebuild, audit, transition, P1/P2/P3, scoring, probe execution, canonical installation, or Git activity.

**Requested Sentinel decision:** `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.

---

## 23. Normative machine-extractable schema registry

The following JSON is normative. It is a closed schema DSL, not an example. A conforming materializer MUST resolve every node through its `artifact_profile_id`, apply the profile plus node-specific constants and invariants, reject additional fields, and derive every direct provenance edge solely from typed `ref_bindings`. Activity-free scientific payload profiles serialize no provenance envelope; their edges are declared by `SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED`.

```json
{
  "schema_registry_id": "pm_research.s2.candidate08.complete_node_schema_registry.v5",
  "canonical_commit": "70ab8455f33d44b2a690b8c5db58f8ebc545454e",
  "integer_policy": {
    "JcsSafeUInt": "JSON integer 0..9007199254740991 only",
    "ByteLength": "JcsSafeUInt, unit bytes",
    "Count": "JcsSafeUInt",
    "UtcMs": "JcsSafeUInt 0..253402300799999",
    "UtcSecond": "JcsSafeUInt 0..253402300799",
    "UInt32": "JcsSafeUInt 0..4294967295",
    "UInt64Dec": "canonical decimal string 0 or [1-9][0-9]{0,19}, numeric <=18446744073709551615",
    "TokenId": "canonical decimal string uint256",
    "rule": "No JSON numeric integer outside JcsSafeUInt is conforming. No binary floating point enters hashes or comparisons."
  },
  "canonical_input_paths": [
    "START_HERE.md",
    "project_context/START_HERE.md",
    "project_context/GUARDRAILS.md",
    "project_context/PROJECT_STATE.md",
    "project_context/DECISION_LOG.md",
    "project_context/CLOSED_FINDINGS.md",
    "project_context/ARTIFACT_INDEX.md",
    "project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md",
    "project_context/DATA_CONTRACTS_named_binary_probe.md",
    "project_context/PRICE_INPUT_CONTRACT_named_binary_probe.md",
    "project_context/SPEC_named_binary_probe.md",
    "project_context/SPEC_price_source_s1_coverage.md",
    "project_context/S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02.md",
    "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md",
    "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03_AMENDMENT_01.md",
    "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A001_SENTINEL_COMBINED_ARCHITECTURE_REVIEW_RECORD_CANDIDATE_01.md",
    "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md"
  ],
  "implementation_source_matrix": [
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/__init__.py",
      "role": "package_export"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/types.py",
      "role": "closed_types_and_jcs"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/schema_registry.py",
      "role": "schema_registry_and_edge_derivation"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/state_reducers.py",
      "role": "global_condition_transition_state_reducers"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/s4_inputs.py",
      "role": "s4_input_parsers_and_reconciliation"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/safe_span.py",
      "role": "safe_span_classifier_and_reducer"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/prices_history_contract.py",
      "role": "endpoint_response_terminal_and_retry_contract"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/request_plan.py",
      "role": "deterministic_request_plan"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/acquisition.py",
      "role": "independent_token_acquisition_and_raw_closure"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/construction.py",
      "role": "scientific_construction_and_deduplication"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/alignment.py",
      "role": "accepted_policy_alignment"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/rebuild.py",
      "role": "isolated_rebuild_and_byte_comparison"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/audit.py",
      "role": "nineteen_audit_closures_and_gate"
    },
    {
      "logical_path": "src/pm_research/named_binary_probe/s2/transition.py",
      "role": "stage10_transition_reconciliation"
    }
  ],
  "test_source_matrix": [
    {
      "logical_path": "tests/named_binary_probe/s2/test_schema_registry.py",
      "role": "schema_and_678_edge_equality"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_state_reducers.py",
      "role": "global_and_p00_p18_totality"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_s4_inputs.py",
      "role": "s4_source_parsers_and_reconciliation"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_safe_span.py",
      "role": "safe_span_total_classifier"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_prices_history_contract.py",
      "role": "response_and_terminal_mapping"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_retry_after.py",
      "role": "retry_after_units_and_caps"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_request_plan.py",
      "role": "plan_determinism_and_independence"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_acquisition.py",
      "role": "attempt_terminal_inventory_completion"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_construction.py",
      "role": "construction_identity_and_duplicates"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_alignment.py",
      "role": "selector_and_millisecond_boundary"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_rebuild.py",
      "role": "isolation_and_exact_byte_comparison"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_audit.py",
      "role": "audit_totality_and_gate_reducer"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_transition.py",
      "role": "stage10_branches_and_u0_partition"
    },
    {
      "logical_path": "tests/named_binary_probe/s2/test_counterexamples.py",
      "role": "required_negative_cases"
    }
  ],
  "type_dsl": {
    "wrappers": {
      "Array<T>": "JSON array; item schema T; min/max from field",
      "Nullable<T>": "null or T",
      "Enum[a,b]": "exact member with scalar kind inferred",
      "Const[x]": "exact scalar x"
    },
    "unknown_type_rule": "reject",
    "primitive_keywords": {
      "Object": "JSON object schema described by sibling keys",
      "Array": "JSON array schema described by sibling keys"
    }
  },
  "type_registry": {
    "Utf8String": {
      "kind": "string",
      "min_length": 0,
      "max_utf8_bytes": 1048576,
      "normalization": "none unless a containing schema says otherwise"
    },
    "Boolean": {
      "kind": "boolean"
    },
    "JcsSafeUInt": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "ByteLength": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 9007199254740991,
      "unit": "bytes"
    },
    "Count": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "UInt32": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 4294967295
    },
    "UInt64Dec": {
      "kind": "string",
      "pattern": "^(0|[1-9][0-9]{0,19})$",
      "numeric_minimum": "0",
      "numeric_maximum": "18446744073709551615",
      "comparison": "length then lexicographic after canonical validation"
    },
    "UtcMs": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 253402300799999,
      "unit": "milliseconds since Unix epoch UTC"
    },
    "UtcSecond": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 253402300799,
      "unit": "seconds since Unix epoch UTC"
    },
    "GitCommit40": {
      "kind": "string",
      "pattern": "^[0-9a-f]{40}$"
    },
    "Sha256": {
      "kind": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "NodeId": {
      "kind": "string",
      "pattern": "^(K[0-9]{3}[A-Z]?|A[0-9]{3})$",
      "enum_source": "Appendix A node column"
    },
    "RecordId": {
      "kind": "string",
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,159}$",
      "min_utf8_bytes": 1,
      "max_utf8_bytes": 160,
      "encoding": "ASCII",
      "constraints": [
        "ASCII byte length equals character count",
        "reject 161 bytes or more"
      ]
    },
    "RelativePath": {
      "kind": "string",
      "min_length": 1,
      "max_utf8_bytes": 4096,
      "normalization": "NFC",
      "constraints": [
        "UTF-8",
        "input MUST equal Unicode NFC(input); normalization after acceptance is forbidden",
        "forward slash only",
        "not absolute",
        "no empty segment",
        "no dot or dot-dot segment",
        "no NUL",
        "no backslash"
      ]
    },
    "ConditionId": {
      "kind": "string",
      "pattern": "^0x[0-9a-f]{64}$"
    },
    "TokenId": {
      "kind": "string",
      "pattern": "^(0|[1-9][0-9]{0,77})$",
      "numeric_maximum": "115792089237316195423570985008687907853269984665640564039457584007913129639935"
    },
    "OutcomeIndex": {
      "kind": "integer",
      "enum": [
        0,
        1
      ]
    },
    "Subclass": {
      "kind": "string",
      "enum": [
        "UP_DOWN",
        "OVER_UNDER",
        "NAMED_OTHER"
      ]
    },
    "StrictUtcTimestampString": {
      "kind": "string",
      "patterns": [
        "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC$",
        "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3} UTC$"
      ],
      "constraints": [
        "Gregorian date valid",
        "seconds 00..59",
        "no leap second",
        "UTC literal exact",
        "conversion exact to UtcMs"
      ]
    },
    "PriceLexeme": {
      "kind": "union",
      "variants": [
        {
          "kind": "string",
          "pattern": "^(0|1|0\\.[0-9]{1,76})$"
        },
        {
          "kind": "json_number_lexeme",
          "pattern": "^(0|1|0\\.[0-9]{1,76})$"
        }
      ],
      "constraints": [
        "no sign",
        "no exponent",
        "no NaN or Infinity",
        "numeric range 0..1",
        "canonical result removes trailing fractional zeros; zero and one are 0 and 1"
      ]
    },
    "Position": {
      "kind": "string",
      "enum": [
        "INITIAL",
        "TOKEN_PAIR",
        "REQUEST",
        "CONSTRUCTION",
        "READY_ALIGNMENT",
        "FINAL"
      ]
    },
    "WindowState": {
      "kind": "string",
      "enum": [
        "NOT_EVALUATED",
        "QUERY_ELIGIBLE",
        "VALID_EXCLUSION_INVALID_WINDOW",
        "INCOMPLETE_MISSING_TRADE_ANCHOR",
        "BLOCKED_RESOLUTION_BOUNDARY"
      ]
    },
    "TokenPairState": {
      "kind": "string",
      "enum": [
        "NOT_EVALUATED",
        "NOT_APPLICABLE_WINDOW",
        "STABLE_INDEPENDENT_PAIR",
        "UNRESOLVED",
        "UNSTABLE",
        "PRECISION_INVALID"
      ]
    },
    "RequestState": {
      "kind": "string",
      "enum": [
        "NOT_EVALUATED",
        "NOT_APPLICABLE",
        "PLANNED",
        "IN_PROGRESS",
        "COMPLETE_BOTH_TERMINALS",
        "INCOMPLETE",
        "BLOCKED"
      ]
    },
    "ConstructionState": {
      "kind": "string",
      "enum": [
        "NOT_EVALUATED",
        "NOT_APPLICABLE",
        "BOTH_PARTITIONS_INCLUDED",
        "ONE_PARTITION_INCLUDED",
        "NO_PARTITION_INCLUDED",
        "INCOMPLETE",
        "BLOCKED"
      ]
    },
    "AlignmentState": {
      "kind": "string",
      "enum": [
        "NOT_EVALUATED",
        "NOT_APPLICABLE",
        "BOTH_SIDE_USABLE",
        "ONE_SIDE_USABLE",
        "NEITHER_SIDE_USABLE",
        "INCOMPLETE",
        "BLOCKED"
      ]
    },
    "Effect": {
      "kind": "string",
      "enum": [
        "ACTIVE",
        "VALID_EXCLUSION",
        "CLEAR_COMPONENT",
        "LIMITATION",
        "INCOMPLETE_EVIDENCE",
        "BLOCKING_DEFECT"
      ]
    },
    "GlobalPhase": {
      "kind": "string",
      "enum": [
        "ARCHITECTURE_REVIEW",
        "SPEC_DRAFTING",
        "SPEC_REVIEW",
        "IMPLEMENTATION_SOURCE",
        "SOURCE_REVIEW",
        "TEST_AUTHORING",
        "TEST_REVIEW",
        "TEST_EXECUTION",
        "TEST_RESULT_REVIEW",
        "S4_PREPARATION",
        "S4_REVIEW",
        "S5_PREFLIGHT",
        "SPAN_REVIEW",
        "S6_ACQUISITION",
        "S6_REVIEW",
        "S7_CONSTRUCTION",
        "S7_REVIEW",
        "ALIGNMENT_POLICY_REVIEW",
        "S8A_ALIGNMENT",
        "S8A_REVIEW",
        "S8B_REBUILD",
        "S8B_REVIEW",
        "S8C_AUDIT",
        "S9_RESULT_REVIEW",
        "S10_TRANSITION",
        "S10_REVIEW",
        "COMPLETE",
        "HALTED"
      ]
    },
    "GlobalPhaseStatus": {
      "kind": "string",
      "enum": [
        "NOT_STARTED",
        "IN_PROGRESS",
        "COMPLETE",
        "INCOMPLETE",
        "BLOCKED"
      ]
    },
    "ReviewDisposition": {
      "kind": "string",
      "enum": [
        "NOT_APPLICABLE",
        "PENDING",
        "APPROVE",
        "ACCEPT_FINDING",
        "BLOCK",
        "DEFER",
        "NEEDS_VERIFICATION"
      ]
    },
    "NodeRef": {
      "kind": "object",
      "required": [
        "node_id",
        "logical_path",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "node_id": "NodeId",
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "sha256 and byte_length identify exact bytes at logical_path",
        "node_id target equals binding target"
      ]
    },
    "DerivedNodeRefArray": {
      "kind": "array",
      "items": "NodeRef",
      "min_items": 0,
      "unique_by": "node_id",
      "ordering": "exact ref_bindings order",
      "authority": "derived only; cannot be supplied independently"
    },
    "ClosedPayloadByProfile": {
      "kind": "synthetic_parent",
      "rule": "allowed children are exactly profile fields below /payload; no additional child"
    },
    "FindingRow": {
      "kind": "object",
      "required": [
        "code",
        "severity",
        "statement"
      ],
      "fields": {
        "code": "RecordId",
        "severity": "Enum[INFO,LIMITATION,INCOMPLETE,BLOCKING]",
        "statement": "Utf8String"
      },
      "additional_fields": false,
      "constraints": []
    },
    "CountEntry": {
      "kind": "object",
      "required": [
        "key",
        "value"
      ],
      "fields": {
        "key": "RecordId",
        "value": "Count"
      },
      "additional_fields": false,
      "constraints": []
    },
    "ClosedCountObject": {
      "kind": "object",
      "required": [
        "entries"
      ],
      "fields": {
        "entries": "Array<CountEntry>"
      },
      "additional_fields": false,
      "constraints": [
        "entries key UTF-8 ascending",
        "keys unique"
      ]
    },
    "SubclassCounts": {
      "kind": "object",
      "required": [
        "UP_DOWN",
        "OVER_UNDER",
        "NAMED_OTHER",
        "total"
      ],
      "fields": {
        "UP_DOWN": "Count",
        "OVER_UNDER": "Count",
        "NAMED_OTHER": "Count",
        "total": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total=UP_DOWN+OVER_UNDER+NAMED_OTHER"
      ]
    },
    "EffectCounts": {
      "kind": "object",
      "required": [
        "ACTIVE",
        "VALID_EXCLUSION",
        "CLEAR_COMPONENT",
        "LIMITATION",
        "INCOMPLETE_EVIDENCE",
        "BLOCKING_DEFECT",
        "total"
      ],
      "fields": {
        "ACTIVE": "Count",
        "VALID_EXCLUSION": "Count",
        "CLEAR_COMPONENT": "Count",
        "LIMITATION": "Count",
        "INCOMPLETE_EVIDENCE": "Count",
        "BLOCKING_DEFECT": "Count",
        "total": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total is sum of six classes"
      ]
    },
    "HandoffSelfIdentity": {
      "kind": "object",
      "required": [
        "raw_byte_length",
        "self_excluding_projection_byte_length",
        "self_excluding_projection_sha256",
        "projection_rule",
        "raw_sha256_binding_location"
      ],
      "fields": {
        "raw_byte_length": "ByteLength",
        "self_excluding_projection_byte_length": "ByteLength",
        "self_excluding_projection_sha256": "Sha256",
        "projection_rule": "Const[OMIT_ENTIRE_SELF_IDENTITY_OBJECT_AND_ALL_MARKDOWN_PROSE]",
        "raw_sha256_binding_location": "Const[EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD]"
      },
      "additional_fields": false,
      "constraints": [
        "projection is RFC8785 JCS of the complete normative K009 JSON object with /payload/self_identity removed",
        "raw handoff sha256 MUST NOT appear in its own raw bytes",
        "raw_sha256_binding_location is exactly EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD"
      ]
    },
    "GustavoAuthorizationScope": {
      "kind": "object",
      "required": [
        "accepted_architecture_must_control",
        "allowed_deliverables",
        "allowed_operations",
        "blocked_submission_identities",
        "canonical_writes",
        "forbidden_operations",
        "implementation_or_execution_authorization",
        "scope_expansion"
      ],
      "fields": {
        "accepted_architecture_must_control": "Boolean",
        "allowed_deliverables": "Array<RelativePath>",
        "allowed_operations": "Array<RecordId>",
        "blocked_submission_identities": "Array<ArtifactIdentity>",
        "canonical_writes": "Boolean",
        "forbidden_operations": "Array<RecordId>",
        "implementation_or_execution_authorization": "Boolean",
        "scope_expansion": "Boolean"
      },
      "additional_fields": false,
      "constraints": [
        "allowed and forbidden operations disjoint",
        "allowed_deliverables unique",
        "blocked identities unique by logical_path"
      ]
    },
    "SentinelActivatedScope": {
      "kind": "object",
      "required": [
        "allowed_deliverables",
        "allowed_operations",
        "blocked_submission_identities",
        "correction_boundary",
        "forbidden_operations",
        "must_preserve_accepted_architecture",
        "scope_expansion",
        "scope_relation_to_k006"
      ],
      "fields": {
        "allowed_deliverables": "Array<RelativePath>",
        "allowed_operations": "Array<RecordId>",
        "blocked_submission_identities": "Array<ArtifactIdentity>",
        "correction_boundary": "Array<RecordId>",
        "forbidden_operations": "Array<RecordId>",
        "must_preserve_accepted_architecture": "Boolean",
        "scope_expansion": "Boolean",
        "scope_relation_to_k006": "Enum[EQUAL,STRICT_SUBSET]"
      },
      "additional_fields": false,
      "constraints": [
        "scope no wider than exact Gustavo scope"
      ]
    },
    "ActivityScope": {
      "kind": "object",
      "required": [
        "allowed_deliverables",
        "authorization_effect",
        "forbidden_operations",
        "required_return",
        "stop_conditions"
      ],
      "fields": {
        "allowed_deliverables": "Array<RelativePath>",
        "authorization_effect": "Enum[SPECIFICATION_DRAFTING_ONLY,IMPLEMENTATION_ONLY,TEST_AUTHORING_ONLY,TEST_EXECUTION_ONLY,LOCAL_DATA_ONLY,NETWORK_EXECUTION_ONLY,CONSTRUCTION_ONLY,ALIGNMENT_ONLY,REBUILD_ONLY,AUDIT_ONLY,TRANSITION_ONLY,FUTURE_P1_ONLY]",
        "forbidden_operations": "Array<RecordId>",
        "required_return": "RequiredReturn",
        "stop_conditions": "Array<RecordId>"
      },
      "additional_fields": false,
      "constraints": [
        "allowed deliverables exact intersection of authorizations"
      ]
    },
    "RequiredReturn": {
      "kind": "object",
      "required": [
        "destination",
        "implementation_or_execution_authorization",
        "include_exact_byte_lengths",
        "include_exact_sha256"
      ],
      "fields": {
        "destination": "RecordId",
        "implementation_or_execution_authorization": "Boolean",
        "include_exact_byte_lengths": "Boolean",
        "include_exact_sha256": "Boolean"
      },
      "additional_fields": false,
      "constraints": []
    },
    "ArtifactIdentity": {
      "kind": "object",
      "required": [
        "logical_path",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": []
    },
    "SourceFileRow": {
      "kind": "object",
      "required": [
        "logical_path",
        "role",
        "language",
        "required",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "logical_path": "RelativePath",
        "role": "RecordId",
        "language": "Enum[PYTHON]",
        "required": "Boolean",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "required=true"
      ]
    },
    "TestFileRow": {
      "kind": "object",
      "required": [
        "logical_path",
        "role",
        "language",
        "required",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "logical_path": "RelativePath",
        "role": "RecordId",
        "language": "Enum[PYTHON]",
        "required": "Boolean",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "required=true"
      ]
    },
    "TestResultRow": {
      "kind": "object",
      "required": [
        "test_id",
        "test_file_path",
        "status",
        "duration_ms",
        "failure_code",
        "evidence_sha256"
      ],
      "fields": {
        "test_id": "RecordId",
        "test_file_path": "RelativePath",
        "status": "Enum[PASS,FAIL,ERROR,SKIP]",
        "duration_ms": "UInt32",
        "failure_code": "Nullable<RecordId>",
        "evidence_sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "failure_code non-null iff FAIL or ERROR"
      ]
    },
    "TestSummary": {
      "kind": "object",
      "required": [
        "total",
        "pass",
        "fail",
        "error",
        "skip"
      ],
      "fields": {
        "total": "Count",
        "pass": "Count",
        "fail": "Count",
        "error": "Count",
        "skip": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total=pass+fail+error+skip"
      ]
    },
    "S4InputManifestRow": {
      "kind": "object",
      "required": [
        "input_role",
        "logical_path",
        "byte_length",
        "sha256",
        "media_type",
        "row_schema_id",
        "permitted_root_class",
        "required"
      ],
      "fields": {
        "input_role": "RecordId",
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256",
        "media_type": "RecordId",
        "row_schema_id": "RecordId",
        "permitted_root_class": "RecordId",
        "required": "Boolean"
      },
      "additional_fields": false,
      "constraints": [
        "required=true"
      ]
    },
    "S4LedgerRow": {
      "kind": "object",
      "required": [
        "condition_id",
        "subclass",
        "window_state",
        "decision_lower_ts_ms",
        "resolved_at_ts_ms",
        "token_0_id",
        "token_1_id",
        "token_pair_state",
        "p_class",
        "effect"
      ],
      "fields": {
        "condition_id": "ConditionId",
        "subclass": "Subclass",
        "window_state": "WindowState",
        "decision_lower_ts_ms": "Nullable<UtcMs>",
        "resolved_at_ts_ms": "Nullable<UtcMs>",
        "token_0_id": "Nullable<TokenId>",
        "token_1_id": "Nullable<TokenId>",
        "token_pair_state": "TokenPairState",
        "p_class": "Enum[P00,P01,P02,P03,P04,P05,P06]",
        "effect": "Effect"
      },
      "additional_fields": false,
      "constraints": [
        "exact P00..P06 vector",
        "winner/result fields forbidden"
      ]
    },
    "EquationResult": {
      "kind": "object",
      "required": [
        "equation_id",
        "left_value",
        "right_value",
        "status",
        "evidence_detail"
      ],
      "fields": {
        "equation_id": "RecordId",
        "left_value": "Count",
        "right_value": "Count",
        "status": "Enum[PASS,FAIL,INCOMPLETE]",
        "evidence_detail": "Utf8String"
      },
      "additional_fields": false,
      "constraints": []
    },
    "CanaryRequest": {
      "kind": "object",
      "required": [
        "candidate_span_seconds",
        "canary_id",
        "token_id",
        "outcome_index",
        "start_ts_s",
        "end_ts_s",
        "request_id"
      ],
      "fields": {
        "candidate_span_seconds": "UInt32",
        "canary_id": "RecordId",
        "token_id": "TokenId",
        "outcome_index": "OutcomeIndex",
        "start_ts_s": "UtcSecond",
        "end_ts_s": "UtcSecond",
        "request_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": [
        "start<end",
        "end-start=candidate_span_seconds"
      ]
    },
    "CanaryAttempt": {
      "kind": "object",
      "required": [
        "request_id",
        "attempt_ordinal",
        "transport_class",
        "http_status",
        "content_type",
        "body_length",
        "point_count",
        "payload_sha256",
        "classifier_result",
        "classifier_rule"
      ],
      "fields": {
        "request_id": "RecordId",
        "attempt_ordinal": "UInt32",
        "transport_class": "TransportResult",
        "http_status": "Nullable<UInt32>",
        "content_type": "Nullable<Utf8String>",
        "body_length": "Nullable<ByteLength>",
        "point_count": "Nullable<Count>",
        "payload_sha256": "Nullable<Sha256>",
        "classifier_result": "Enum[SAFE,UNSAFE,INCOMPLETE,INTEGRITY_FAILURE]",
        "classifier_rule": "UInt32"
      },
      "additional_fields": false,
      "constraints": [
        "classifier_rule is first matching safe_span_classifier precedence"
      ]
    },
    "S5Bounds": {
      "kind": "object",
      "required": [
        "max_attempts",
        "timeout_ms",
        "max_response_bytes",
        "max_points_per_payload",
        "max_retry_delay_ms"
      ],
      "fields": {
        "max_attempts": "UInt32",
        "timeout_ms": "UInt32",
        "max_response_bytes": "ByteLength",
        "max_points_per_payload": "Count",
        "max_retry_delay_ms": "UInt32"
      },
      "additional_fields": false,
      "constraints": [
        "all positive except max_retry_delay_ms may be zero"
      ]
    },
    "SafeSpanCandidateResult": {
      "kind": "object",
      "required": [
        "candidate_span_seconds",
        "required_canary_count",
        "safe_count",
        "unsafe_count",
        "incomplete_count",
        "integrity_failure_count",
        "result"
      ],
      "fields": {
        "candidate_span_seconds": "UInt32",
        "required_canary_count": "Count",
        "safe_count": "Count",
        "unsafe_count": "Count",
        "incomplete_count": "Count",
        "integrity_failure_count": "Count",
        "result": "Enum[SAFE,UNSAFE,INCOMPLETE,INTEGRITY_FAILURE]"
      },
      "additional_fields": false,
      "constraints": [
        "required=sum four counts",
        "integrity failure precedence then incomplete then unsafe then safe"
      ]
    },
    "RequestEcho": {
      "kind": "object",
      "required": [
        "method",
        "route",
        "token_id",
        "start_ts_s",
        "end_ts_s",
        "fidelity",
        "interval"
      ],
      "fields": {
        "method": "Const[GET]",
        "route": "Const[/prices-history]",
        "token_id": "TokenId",
        "start_ts_s": "UtcSecond",
        "end_ts_s": "UtcSecond",
        "fidelity": "Const[1]",
        "interval": "Const[null]"
      },
      "additional_fields": false,
      "constraints": []
    },
    "RawInventoryRow": {
      "kind": "object",
      "required": [
        "artifact_kind",
        "request_id",
        "attempt_ordinal",
        "logical_path",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "artifact_kind": "Enum[ATTEMPT,TERMINAL,PAYLOAD]",
        "request_id": "RecordId",
        "attempt_ordinal": "Nullable<UInt32>",
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": []
    },
    "RawInventoryCounts": {
      "kind": "object",
      "required": [
        "attempt_count",
        "terminal_count",
        "payload_count",
        "total"
      ],
      "fields": {
        "attempt_count": "Count",
        "terminal_count": "Count",
        "payload_count": "Count",
        "total": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total=sum three"
      ]
    },
    "AcquisitionCompletionCounts": {
      "kind": "object",
      "required": [
        "planned_count",
        "payload_complete_count",
        "empty_complete_count",
        "transient_exhausted_count",
        "blocking_terminal_count"
      ],
      "fields": {
        "planned_count": "Count",
        "payload_complete_count": "Count",
        "empty_complete_count": "Count",
        "transient_exhausted_count": "Count",
        "blocking_terminal_count": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "planned=payload+empty+transient+blocking"
      ]
    },
    "ArchiveMember": {
      "kind": "object",
      "required": [
        "logical_path",
        "byte_length",
        "sha256",
        "member_type",
        "mode_octal",
        "uid",
        "gid",
        "mtime"
      ],
      "fields": {
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256",
        "member_type": "Enum[REGULAR_FILE]",
        "mode_octal": "Const[0000644]",
        "uid": "Const[0]",
        "gid": "Const[0]",
        "mtime": "Const[0]"
      },
      "additional_fields": false,
      "constraints": []
    },
    "ConstructionProfileIds": {
      "kind": "object",
      "required": [
        "serialization_profile_id",
        "construction_algorithm_id",
        "row_schema_id",
        "duplicate_reducer_id"
      ],
      "fields": {
        "serialization_profile_id": "RecordId",
        "construction_algorithm_id": "RecordId",
        "row_schema_id": "RecordId",
        "duplicate_reducer_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": []
    },
    "S4InputContractSet": {
      "kind": "object",
      "required": [
        "condition_universe_schema_id",
        "classification_schema_id",
        "resolution_schema_id",
        "first_trade_schema_id",
        "token_tuple_schema_id"
      ],
      "fields": {
        "condition_universe_schema_id": "RecordId",
        "classification_schema_id": "RecordId",
        "resolution_schema_id": "RecordId",
        "first_trade_schema_id": "RecordId",
        "token_tuple_schema_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": []
    },
    "BuildIdentityContract": {
      "kind": "object",
      "required": [
        "schema_id",
        "preimage_order",
        "hash_algorithm",
        "serialization"
      ],
      "fields": {
        "schema_id": "RecordId",
        "preimage_order": "Array<Enum[K068,A003,A005,A007,FIXED_PROFILES]>",
        "hash_algorithm": "Const[SHA-256]",
        "serialization": "Const[RFC8785_JCS]"
      },
      "additional_fields": false,
      "constraints": [
        "preimage excludes activity provenance and K082"
      ]
    },
    "PartitionDefinition": {
      "kind": "object",
      "required": [
        "subclass",
        "outcome_index",
        "logical_path_template"
      ],
      "fields": {
        "subclass": "Subclass",
        "outcome_index": "OutcomeIndex",
        "logical_path_template": "RelativePath"
      },
      "additional_fields": false,
      "constraints": [
        "six unique subclass/outcome pairs"
      ]
    },
    "PerTokenPriceRowSchema": {
      "kind": "object",
      "required": [
        "schema_id",
        "field_order",
        "price_type",
        "row_key_preimage_id"
      ],
      "fields": {
        "schema_id": "RecordId",
        "field_order": "Array<RecordId>",
        "price_type": "RecordId",
        "row_key_preimage_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": []
    },
    "DuplicateReducerContract": {
      "kind": "object",
      "required": [
        "group_key_fields",
        "conflicting_price_result",
        "equal_price_keep_rule",
        "discarded_identity_location"
      ],
      "fields": {
        "group_key_fields": "Array<RecordId>",
        "conflicting_price_result": "Enum[BLOCK]",
        "equal_price_keep_rule": "Enum[LEXICOGRAPHIC_MIN_SOURCE_ROW_ID]",
        "discarded_identity_location": "Enum[PROVENANCE_WRAPPER_ONLY]"
      },
      "additional_fields": false,
      "constraints": []
    },
    "PartitionArtifact": {
      "kind": "object",
      "required": [
        "subclass",
        "outcome_index",
        "logical_path",
        "row_count",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "subclass": "Subclass",
        "outcome_index": "OutcomeIndex",
        "logical_path": "RelativePath",
        "row_count": "Count",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": []
    },
    "PartitionCounts": {
      "kind": "object",
      "required": [
        "partition_count",
        "row_count",
        "condition_count"
      ],
      "fields": {
        "partition_count": "Count",
        "row_count": "Count",
        "condition_count": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "partition_count=6"
      ]
    },
    "AlignmentLedgerRow": {
      "kind": "object",
      "required": [
        "condition_id",
        "policy_selector",
        "side_0_row_key",
        "side_1_row_key",
        "side_0_staleness_ms",
        "side_1_staleness_ms",
        "inter_side_skew_ms",
        "alignment_state",
        "effect",
        "reason_code"
      ],
      "fields": {
        "condition_id": "ConditionId",
        "policy_selector": "Enum[EXACT_COINCIDENT_PAIR,FIRST_AT_OR_AFTER_ANCHOR]",
        "side_0_row_key": "Nullable<Sha256>",
        "side_1_row_key": "Nullable<Sha256>",
        "side_0_staleness_ms": "Nullable<UInt64Dec>",
        "side_1_staleness_ms": "Nullable<UInt64Dec>",
        "inter_side_skew_ms": "Nullable<UInt64Dec>",
        "alignment_state": "AlignmentState",
        "effect": "Effect",
        "reason_code": "RecordId"
      },
      "additional_fields": false,
      "constraints": [
        "BOTH requires two row keys and metrics",
        "ONE requires exactly one row key",
        "NEITHER requires zero selected usable pair",
        "INCOMPLETE/BLOCKED metrics null unless evidenced before failure"
      ]
    },
    "ByteComparisonRow": {
      "kind": "object",
      "required": [
        "comparison_id",
        "original",
        "rebuilt",
        "status"
      ],
      "fields": {
        "comparison_id": "RecordId",
        "original": "ScientificPayloadIdentity",
        "rebuilt": "ScientificPayloadIdentity",
        "status": "Enum[PASS,FAIL,INCOMPLETE]"
      },
      "additional_fields": false,
      "constraints": [
        "PASS iff exact payload byte_length and sha256 equal and media_type/serialization_profile_id agree",
        "complete node envelopes and provenance wrappers are forbidden comparison inputs"
      ]
    },
    "EffectLedgerRow": {
      "kind": "object",
      "required": [
        "condition_id",
        "p_class",
        "effect",
        "reason_code"
      ],
      "fields": {
        "condition_id": "ConditionId",
        "p_class": "Enum[P00,P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18]",
        "effect": "Effect",
        "reason_code": "RecordId"
      },
      "additional_fields": false,
      "constraints": []
    },
    "AuditDetailRow": {
      "kind": "object",
      "required": [
        "subject_key",
        "status",
        "effect",
        "stop_code",
        "evidence_sha256"
      ],
      "fields": {
        "subject_key": "Utf8String",
        "status": "Enum[PASS,FAIL,INCOMPLETE,NOT_APPLICABLE]",
        "effect": "Enum[CLEAR_COMPONENT,BLOCKING_DEFECT,INCOMPLETE_EVIDENCE]",
        "stop_code": "Nullable<RecordId>",
        "evidence_sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": []
    },
    "AuditStatusCounts": {
      "kind": "object",
      "required": [
        "PASS",
        "FAIL",
        "INCOMPLETE",
        "total"
      ],
      "fields": {
        "PASS": "Count",
        "FAIL": "Count",
        "INCOMPLETE": "Count",
        "total": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total=19",
        "total=sum statuses"
      ]
    },
    "AuditEffectCounts": {
      "kind": "object",
      "required": [
        "CLEAR_COMPONENT",
        "BLOCKING_DEFECT",
        "INCOMPLETE_EVIDENCE",
        "total"
      ],
      "fields": {
        "CLEAR_COMPONENT": "Count",
        "BLOCKING_DEFECT": "Count",
        "INCOMPLETE_EVIDENCE": "Count",
        "total": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total=19",
        "total=sum effects"
      ]
    },
    "GateCounts": {
      "kind": "object",
      "required": [
        "condition_effect_counts",
        "audit_status_counts",
        "alignment_applicable_count",
        "both_side_usable_count"
      ],
      "fields": {
        "condition_effect_counts": "EffectCounts",
        "audit_status_counts": "AuditStatusCounts",
        "alignment_applicable_count": "Count",
        "both_side_usable_count": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "both<=alignment applicable"
      ]
    },
    "TransitionRow": {
      "kind": "object",
      "required": [
        "condition_id",
        "conjunct_results",
        "false_reason_codes",
        "transition_class"
      ],
      "fields": {
        "condition_id": "ConditionId",
        "conjunct_results": "Array<Boolean>",
        "false_reason_codes": "Array<RecordId>",
        "transition_class": "Enum[ELIGIBLE,INELIGIBLE]"
      },
      "additional_fields": false,
      "constraints": [
        "exactly 11 conjuncts",
        "eligible iff all true",
        "false reasons ordered by conjunct ordinal"
      ]
    },
    "TransitionCounts": {
      "kind": "object",
      "required": [
        "eligible",
        "ineligible",
        "total"
      ],
      "fields": {
        "eligible": "Count",
        "ineligible": "Count",
        "total": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "total=39693",
        "eligible+ineligible=total"
      ]
    },
    "AssertionResult": {
      "kind": "object",
      "required": [
        "assertion_id",
        "status",
        "expected_jcs",
        "observed_jcs",
        "stop_code"
      ],
      "fields": {
        "assertion_id": "RecordId",
        "status": "Enum[PASS,FAIL,INCOMPLETE]",
        "expected_jcs": "Utf8String",
        "observed_jcs": "Nullable<Utf8String>",
        "stop_code": "Nullable<RecordId>"
      },
      "additional_fields": false,
      "constraints": []
    },
    "NodeIdentity": {
      "kind": "object",
      "required": [
        "node_id",
        "logical_path",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "node_id": "NodeId",
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "identifies bytes but creates no edge unless field slot is declared NodeRef in artifact profile or schema_edge_contract"
      ]
    },
    "NonEdgeIdentityMetadata": {
      "kind": "object",
      "required": [
        "metadata_node_label",
        "metadata_logical_path",
        "metadata_byte_length",
        "metadata_sha256"
      ],
      "fields": {
        "metadata_node_label": "NodeId",
        "metadata_logical_path": "RelativePath",
        "metadata_byte_length": "ByteLength",
        "metadata_sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "non-authorizing descriptive metadata only",
        "field names cannot be interpreted as NodeRef",
        "edge extractor MUST ignore this type"
      ]
    },
    "TransportResult": {
      "kind": "string",
      "enum": [
        "HTTP_RESPONSE",
        "TIMEOUT",
        "DNS_FAILURE",
        "CONNECTION_FAILURE",
        "TLS_FAILURE",
        "CONNECTION_RESET",
        "LOCALLY_CANCELLED",
        "RESOURCE_BOUND_REJECTION",
        "UNKNOWN_TRANSPORT_FAILURE"
      ]
    },
    "UniverseOrdinal": {
      "kind": "integer",
      "minimum": 0,
      "maximum": 39692,
      "jcs_safe": true
    },
    "ScientificPayloadIdentity": {
      "kind": "object",
      "required": [
        "logical_path",
        "byte_length",
        "sha256",
        "media_type",
        "serialization_profile_id"
      ],
      "fields": {
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256",
        "media_type": "RecordId",
        "serialization_profile_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": [
        "identity covers activity-free scientific payload bytes only"
      ]
    },
    "ScientificPartitionIdentity": {
      "kind": "object",
      "required": [
        "subclass",
        "outcome_index",
        "logical_path",
        "row_count",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "subclass": "Subclass",
        "outcome_index": "OutcomeIndex",
        "logical_path": "RelativePath",
        "row_count": "Count",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "logical path unique",
        "six exact subclass/outcome members"
      ]
    },
    "ConditionProjectionRow": {
      "kind": "object",
      "required": [
        "condition_id",
        "subclass",
        "window_state",
        "decision_lower_ts_ms",
        "resolved_at_ts_ms",
        "token_0_id",
        "token_1_id",
        "token_pair_state",
        "p_class",
        "effect"
      ],
      "fields": {
        "condition_id": "ConditionId",
        "subclass": "Subclass",
        "window_state": "WindowState",
        "decision_lower_ts_ms": "Nullable<UtcMs>",
        "resolved_at_ts_ms": "Nullable<UtcMs>",
        "token_0_id": "Nullable<TokenId>",
        "token_1_id": "Nullable<TokenId>",
        "token_pair_state": "TokenPairState",
        "p_class": "Enum[P00,P01,P02,P03,P04,P05,P06]",
        "effect": "Effect"
      },
      "additional_fields": false,
      "constraints": [
        "row satisfies exact P00..P06 classifier",
        "winner, result, payout, selected side, and outcome label fields forbidden"
      ]
    },
    "RequestPlanProjectionRow": {
      "kind": "object",
      "required": [
        "request_id",
        "condition_id",
        "subclass",
        "token_id",
        "outcome_index",
        "chunk_ordinal",
        "start_ts_s",
        "end_ts_s",
        "method",
        "route",
        "fidelity",
        "interval"
      ],
      "fields": {
        "request_id": "RecordId",
        "condition_id": "ConditionId",
        "subclass": "Subclass",
        "token_id": "TokenId",
        "outcome_index": "OutcomeIndex",
        "chunk_ordinal": "UInt32",
        "start_ts_s": "UtcSecond",
        "end_ts_s": "UtcSecond",
        "method": "Const[GET]",
        "route": "Const[/prices-history]",
        "fidelity": "Const[1]",
        "interval": "Const[null]"
      },
      "additional_fields": false,
      "constraints": [
        "start_ts_s<end_ts_s",
        "request_id equals SHA256 of the exact request-plan preimage declared by K068",
        "rows independently enumerate both real token IDs; no complement or winner-conditioned enumeration"
      ]
    },
    "RawPayloadProjectionEntry": {
      "kind": "object",
      "required": [
        "request_id",
        "terminal_class",
        "payload_logical_path",
        "payload_byte_length",
        "payload_sha256",
        "point_count"
      ],
      "fields": {
        "request_id": "RecordId",
        "terminal_class": "Enum[PAYLOAD_COMPLETE,EMPTY_COMPLETE]",
        "payload_logical_path": "Nullable<RelativePath>",
        "payload_byte_length": "Nullable<ByteLength>",
        "payload_sha256": "Nullable<Sha256>",
        "point_count": "Count"
      },
      "additional_fields": false,
      "constraints": [
        "PAYLOAD_COMPLETE requires non-null payload identity and point_count>0",
        "EMPTY_COMPLETE requires all payload identity fields null and point_count=0"
      ]
    },
    "BuildIdentityPreimage": {
      "kind": "object",
      "required": [
        "schema_id",
        "canonical_commit",
        "construction_contract",
        "s4_condition_ledger_projection",
        "request_plan_projection",
        "raw_payload_root_projection",
        "serialization_profile_id",
        "construction_algorithm_id"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.deterministic_build_identity.v3]",
        "canonical_commit": "GitCommit40",
        "construction_contract": "NodeIdentity",
        "s4_condition_ledger_projection": "NodeIdentity",
        "request_plan_projection": "NodeIdentity",
        "raw_payload_root_projection": "NodeIdentity",
        "serialization_profile_id": "RecordId",
        "construction_algorithm_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": [
        "construction_contract.node_id=K068",
        "s4_condition_ledger_projection.node_id=A003",
        "request_plan_projection.node_id=A005",
        "raw_payload_root_projection.node_id=A007",
        "contains no activity provenance or K082"
      ]
    },
    "GustavoAuthorizationScopeV2": {
      "kind": "object",
      "required": [
        "allowed_deliverables",
        "allowed_operations",
        "authorization_statement",
        "blocked_submission_identities",
        "canonical_writes",
        "correction_boundary",
        "forbidden_operations",
        "implementation_or_execution_authorization",
        "scope_expansion"
      ],
      "fields": {
        "allowed_deliverables": "Array<RelativePath>",
        "allowed_operations": "Array<RecordId>",
        "authorization_statement": "Utf8String",
        "blocked_submission_identities": "Array<ArtifactIdentity>",
        "canonical_writes": "Boolean",
        "correction_boundary": "Array<RecordId>",
        "forbidden_operations": "Array<RecordId>",
        "implementation_or_execution_authorization": "Boolean",
        "scope_expansion": "Boolean"
      },
      "additional_fields": false,
      "constraints": [
        "allowed and forbidden operations disjoint",
        "allowed_deliverables unique",
        "blocked identities exact and unique by logical_path",
        "canonical_writes=false",
        "implementation_or_execution_authorization=false",
        "scope_expansion=false"
      ]
    },
    "ActivityScopeV2": {
      "kind": "object",
      "required": [
        "allowed_deliverables",
        "authorization_effect",
        "correction_boundary",
        "forbidden_operations",
        "required_return",
        "stop_conditions"
      ],
      "fields": {
        "allowed_deliverables": "Array<RelativePath>",
        "authorization_effect": "Enum[SPECIFICATION_DRAFTING_ONLY]",
        "correction_boundary": "Array<RecordId>",
        "forbidden_operations": "Array<RecordId>",
        "required_return": "RequiredReturn",
        "stop_conditions": "Array<RecordId>"
      },
      "additional_fields": false,
      "constraints": [
        "allowed deliverables exact intersection of K006 and K005",
        "correction_boundary exact supplied nine-item ordered list"
      ]
    },
    "GlobalHaltCode": {
      "kind": "string",
      "enum": [
        "ARCHITECTURE_CONTROL_SET_INVALID",
        "AUTHORIZATION_PREREQUISITE_BYTES_MISSING",
        "AUTHORIZATION_SCOPE_EXPANSION",
        "CONDITION_STATE_INVALID",
        "DUPLICATE_PRICE_CONFLICT",
        "GLOBAL_STATE_INVALID",
        "NO_SAFE_SPAN",
        "NO_SAFE_SPAN_AFTER_MARGIN",
        "PREFLIGHT_INCOMPLETE",
        "PREFLIGHT_INTEGRITY_FAILURE",
        "PROVENANCE_EDGE_SET_MISMATCH",
        "ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN",
        "SCIENTIFIC_PROJECTION_CONFLICT",
        "SCIENTIFIC_RAW_PROJECTION_MISMATCH",
        "STOP_ALIGNMENT_INCOMPLETE",
        "STOP_ALIGNMENT_POLICY_ABSENT",
        "STOP_ALIGNMENT_POLICY_INVALID",
        "STOP_ALIGNMENT_POLICY_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_ALIGNMENT_POLICY_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_ALIGNMENT_POLICY_REVIEW_DEFERRED",
        "STOP_ALIGNMENT_POLICY_REVIEW_NEEDS_VERIFICATION",
        "STOP_ARCHITECTURE_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_ARCHITECTURE_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_ARCHITECTURE_REVIEW_DEFERRED",
        "STOP_ARCHITECTURE_REVIEW_NEEDS_VERIFICATION",
        "STOP_AUDIT_SELF_REFERENCE",
        "STOP_AUTHORIZATION_ORDER_INVALID",
        "STOP_AUTHORIZATION_PROVENANCE_INVALID",
        "STOP_CANDIDATE_SEAL_PREMATURE",
        "STOP_CANONICAL_BASE_MISMATCH",
        "STOP_DETERMINISTIC_BUILD_ID_MISMATCH",
        "STOP_DUPLICATE_IDENTITY_CONFLICT",
        "STOP_ENDPOINT_SHAPE_UNRECOGNIZED",
        "STOP_FORBIDDEN_SYNTHESIS",
        "STOP_GATE_RECONCILIATION_FAILED",
        "STOP_INPUT_IDENTITY_MISMATCH",
        "STOP_P0_NOT_CLEAR",
        "STOP_P1_NOT_SEPARATELY_AUTHORIZED",
        "STOP_PRECISION_LOSS",
        "STOP_RAW_ARCHIVE_IDENTITY_MISMATCH",
        "STOP_RAW_ARCHIVE_INCOMPLETE",
        "STOP_REBUILD_BYTE_MISMATCH",
        "STOP_REBUILD_SOURCE_ISOLATION_VIOLATION",
        "STOP_REQUEST_PLAN_INVALID",
        "STOP_REQUEST_TERMINALS_INCOMPLETE",
        "STOP_RESOLUTION_BOUNDARY_INVALID",
        "STOP_RESOURCE_BOUND_EXCEEDED",
        "STOP_RESUME_PROVENANCE_INVALID",
        "STOP_RETRY_AFTER_UNIT_INVALID",
        "STOP_S10_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S10_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S10_REVIEW_DEFERRED",
        "STOP_S10_REVIEW_NEEDS_VERIFICATION",
        "STOP_S4_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S4_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S4_REVIEW_DEFERRED",
        "STOP_S4_REVIEW_NEEDS_VERIFICATION",
        "STOP_S6_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S6_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S6_REVIEW_DEFERRED",
        "STOP_S6_REVIEW_NEEDS_VERIFICATION",
        "STOP_S7_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S7_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S7_REVIEW_DEFERRED",
        "STOP_S7_REVIEW_NEEDS_VERIFICATION",
        "STOP_S8A_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S8A_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S8A_REVIEW_DEFERRED",
        "STOP_S8A_REVIEW_NEEDS_VERIFICATION",
        "STOP_S8B_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S8B_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S8B_REVIEW_DEFERRED",
        "STOP_S8B_REVIEW_NEEDS_VERIFICATION",
        "STOP_S9_NOT_APPROVED_CLEAR",
        "STOP_S9_RESULT_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_S9_RESULT_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_S9_RESULT_REVIEW_DEFERRED",
        "STOP_S9_RESULT_REVIEW_NEEDS_VERIFICATION",
        "STOP_SOURCE_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_SOURCE_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_SOURCE_REVIEW_DEFERRED",
        "STOP_SOURCE_REVIEW_NEEDS_VERIFICATION",
        "STOP_SPAN_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_SPAN_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_SPAN_REVIEW_DEFERRED",
        "STOP_SPAN_REVIEW_NEEDS_VERIFICATION",
        "STOP_SPEC_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_SPEC_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_SPEC_REVIEW_DEFERRED",
        "STOP_SPEC_REVIEW_NEEDS_VERIFICATION",
        "STOP_STALE_CONTRACT",
        "STOP_TEST_RESULT_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_TEST_RESULT_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_TEST_RESULT_REVIEW_DEFERRED",
        "STOP_TEST_RESULT_REVIEW_NEEDS_VERIFICATION",
        "STOP_TEST_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION",
        "STOP_TEST_REVIEW_BLOCKED_BY_SENTINEL",
        "STOP_TEST_REVIEW_DEFERRED",
        "STOP_TEST_REVIEW_NEEDS_VERIFICATION",
        "STOP_TOKEN_ENUMERATION_UNRELIABLE",
        "STOP_TRADE_ANCHOR_MISSING",
        "STOP_TRANSITION_RECONCILIATION_FAILED",
        "STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED",
        "STOP_UNEXPECTED_DELIVERABLE_PATH",
        "STOP_UNIVERSE_RECONCILIATION_FAILED",
        "STOP_ZERO_POPULATION_NOT_PERMITTED"
      ]
    },
    "GlobalDefect": {
      "kind": "object",
      "required": [
        "phase",
        "severity",
        "stop_code",
        "evidence_identity"
      ],
      "fields": {
        "phase": "GlobalPhase",
        "severity": "Enum[BLOCKING_DEFECT,INCOMPLETE_EVIDENCE]",
        "stop_code": "GlobalHaltCode",
        "evidence_identity": "ArtifactIdentity"
      },
      "additional_fields": false,
      "constraints": [
        "phase cannot be COMPLETE or HALTED",
        "stop_code non-null"
      ]
    },
    "NodeRefArrayElement": {
      "kind": "synthetic_binding_type",
      "base": "NodeRef",
      "rule": "one array element at an exact json_pointer; edge target fixed by ref_binding"
    },
    "CanonicalInputRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/CanonicalInputRow",
      "additional_fields": "as declared by row schema"
    },
    "ConditionUniverseRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/ConditionUniverseRow",
      "additional_fields": "as declared by row schema"
    },
    "ClassificationRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/ClassificationRow",
      "additional_fields": "as declared by row schema"
    },
    "ResolutionSourceRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/ResolutionSourceRow",
      "additional_fields": "as declared by row schema"
    },
    "FirstTradeSourceRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/FirstTradeSourceRow",
      "additional_fields": "as declared by row schema"
    },
    "TokenOutcomeTupleRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/TokenOutcomeTupleRow",
      "additional_fields": "as declared by row schema"
    },
    "RequestPlanRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/RequestPlanRow",
      "additional_fields": "as declared by row schema"
    },
    "PricesHistoryResponse": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/PricesHistoryResponse",
      "additional_fields": "as declared by row schema"
    },
    "RequestAttemptRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/RequestAttemptRow",
      "additional_fields": "as declared by row schema"
    },
    "RequestTerminalRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/RequestTerminalRow",
      "additional_fields": "as declared by row schema"
    },
    "AuditClosurePayload": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/AuditClosurePayload",
      "additional_fields": "as declared by row schema"
    },
    "GlobalStateVector": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/GlobalStateVector",
      "additional_fields": "as declared by row schema"
    },
    "ConditionStateVector": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/ConditionStateVector",
      "additional_fields": "as declared by row schema"
    },
    "PerTokenPriceRow": {
      "kind": "row_schema_ref",
      "schema_location": "/row_schemas/PerTokenPriceRow",
      "additional_fields": false
    },
    "CanonicalDecimalPrice": {
      "kind": "string",
      "pattern": "^(0|1|0\\.[0-9]{1,76})$",
      "constraints": [
        "numeric value in [0,1]",
        "fractional form has no trailing zero"
      ]
    },
    "SchemaLiteral": {
      "kind": "meta_schema_literal",
      "rule": "literal JSON used only to validate another artifact's exact bytes; never serialized as the containing node's decision/provenance payload and never creates an edge"
    },
    "Candidate08StaticChecksV3": {
      "kind": "object",
      "required": [
        "raw_k008_identity_match",
        "raw_k009_external_identity_match",
        "k008_normative_payload_count",
        "k009_normative_payload_count",
        "k008_assigned_profile_valid",
        "k009_assigned_profile_valid",
        "k009_self_projection_valid",
        "k009_self_identity_enum_registered",
        "prose_registry_type_agreement",
        "recordid_bound_agreement",
        "relativepath_nfc_agreement",
        "unknown_types",
        "missing_profiles",
        "binding_issues",
        "registry_node_count",
        "schema_derived_edge_count",
        "appendix_edge_count",
        "missing_edges",
        "extra_edges",
        "rank_violations",
        "cycles",
        "condition_state_classes",
        "condition_state_legal_tuples",
        "condition_state_overlap_count",
        "global_reducer_rows",
        "global_invalid_vectors",
        "global_placeholder_count",
        "safe_span_representative_cases",
        "safe_span_unmapped_or_multi_match",
        "terminal_representative_cases",
        "terminal_unmapped_or_multi_match",
        "scientific_payload_provenance_contamination_count",
        "authorization_exact_schema_matches",
        "exact_clear_witness_count",
        "copilot_role_source_edge_count",
        "copilot_role_source_scientific_dependency_count",
        "copilot_role_execution",
        "static_submission_gate"
      ],
      "fields": {
        "raw_k008_identity_match": "Boolean",
        "raw_k009_external_identity_match": "Boolean",
        "k008_normative_payload_count": "Count",
        "k009_normative_payload_count": "Count",
        "k008_assigned_profile_valid": "Boolean",
        "k009_assigned_profile_valid": "Boolean",
        "k009_self_projection_valid": "Boolean",
        "k009_self_identity_enum_registered": "Boolean",
        "prose_registry_type_agreement": "Boolean",
        "recordid_bound_agreement": "Boolean",
        "relativepath_nfc_agreement": "Boolean",
        "unknown_types": "Count",
        "missing_profiles": "Count",
        "binding_issues": "Count",
        "registry_node_count": "Count",
        "schema_derived_edge_count": "Count",
        "appendix_edge_count": "Count",
        "missing_edges": "Count",
        "extra_edges": "Count",
        "rank_violations": "Count",
        "cycles": "Count",
        "condition_state_classes": "Count",
        "condition_state_legal_tuples": "Count",
        "condition_state_overlap_count": "Count",
        "global_reducer_rows": "Count",
        "global_invalid_vectors": "Count",
        "global_placeholder_count": "Count",
        "safe_span_representative_cases": "Count",
        "safe_span_unmapped_or_multi_match": "Count",
        "terminal_representative_cases": "Count",
        "terminal_unmapped_or_multi_match": "Count",
        "scientific_payload_provenance_contamination_count": "Count",
        "authorization_exact_schema_matches": "Count",
        "exact_clear_witness_count": "Count",
        "copilot_role_source_edge_count": "Count",
        "copilot_role_source_scientific_dependency_count": "Count",
        "copilot_role_execution": "Enum[NOT_PERFORMED]",
        "static_submission_gate": "Enum[CLEAR,BLOCK]"
      },
      "additional_fields": false,
      "constraints": [
        "all eleven mandatory raw-deliverable checks must pass before static_submission_gate=CLEAR",
        "any false boolean, wrong identity, extraction count other than 1, profile failure, projection failure, type contradiction, bound contradiction, or normalization contradiction requires static_submission_gate=BLOCK"
      ]
    },
    "AdministrativeRoleSourceContextV1": {
      "kind": "object",
      "required": [
        "repository",
        "immutable_commit",
        "canonical_state",
        "evidence_only",
        "authorization_effect",
        "s2_dependency_effect",
        "role_execution_status",
        "required_reads"
      ],
      "fields": {
        "repository": "Utf8String",
        "immutable_commit": "GitCommit40",
        "canonical_state": "Enum[INSTALLED_AND_SENTINEL_VERIFIED]",
        "evidence_only": "Boolean",
        "authorization_effect": "Enum[NONE]",
        "s2_dependency_effect": "Enum[NONE]",
        "role_execution_status": "Enum[NOT_PERFORMED]",
        "required_reads": "Array<RelativePath>"
      },
      "additional_fields": false,
      "constraints": [
        "evidence_only=true",
        "no NodeRef fields",
        "role execution not authorized"
      ]
    },
    "Candidate08HandoffPayloadV1": {
      "kind": "object",
      "required": [
        "actions_not_performed",
        "actions_performed",
        "administrative_role_source_context",
        "authorization_effect",
        "blocked_input_identities",
        "control_refs",
        "deliverable_refs",
        "handoff_id",
        "run_id",
        "self_identity",
        "stage_code",
        "static_checks"
      ],
      "fields": {
        "actions_not_performed": "Array<RecordId>",
        "actions_performed": "Array<RecordId>",
        "administrative_role_source_context": "AdministrativeRoleSourceContextV1",
        "authorization_effect": "Enum[NONE]",
        "blocked_input_identities": "Array<ArtifactIdentity>",
        "control_refs": "Array<NodeRef>",
        "deliverable_refs": "Array<NodeRef>",
        "handoff_id": "RecordId",
        "run_id": "RecordId",
        "self_identity": "HandoffSelfIdentity",
        "stage_code": "RecordId",
        "static_checks": "Candidate08StaticChecksV3"
      },
      "additional_fields": false,
      "constraints": [
        "actions_performed and actions_not_performed are duplicate-free and disjoint",
        "control_refs exact order K006,K005,K007",
        "deliverable_refs exact singleton K008",
        "blocked_input_identities exact order blocked K008,blocked K009",
        "authorization_effect=NONE"
      ]
    }
  },
  "artifact_profiles": {
    "virtual_commit.v1": {
      "media_type": "application/vnd.git.commit",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/git_commit"
      ],
      "fields": {
        "/git_commit": {
          "type": "GitCommit40",
          "nullable": false
        }
      },
      "node_ref_slots": {},
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "node_id=K000",
        "git_commit=canonical_commit",
        "no_file_bytes"
      ]
    },
    "canonical_input_manifest.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/canonical_commit_ref",
        "/payload/entries"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/canonical_commit_ref": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/entries": {
          "type": "Array<CanonicalInputRow>",
          "min_items": 17,
          "max_items": 17,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/canonical_commit_ref": "single"
      },
      "additional_fields": false,
      "ordering": [
        "entries by logical_path UTF-8"
      ],
      "uniqueness": [
        "entries.logical_path"
      ],
      "equations": [
        "entry_count=17"
      ],
      "constraints": [
        "entries paths equal canonical_input_paths exactly",
        "every byte_length is JcsSafeUInt bytes",
        "every sha256 hashes exact canonical bytes at canonical_commit"
      ]
    },
    "document_candidate.v1": {
      "media_type": "text/markdown",
      "serialization": "UTF8_LF_NO_BOM",
      "required_fields": [
        "/document_id",
        "/status",
        "/canonical_commit",
        "/activity_root",
        "/normative_input_refs",
        "/normative_sections",
        "/authorization_effect"
      ],
      "fields": {
        "/document_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/activity_root": {
          "type": "Nullable<NodeRef>",
          "nullable": true
        },
        "/normative_input_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/normative_sections": {
          "type": "Array<RecordId>",
          "min_items": 1,
          "nullable": false
        },
        "/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/activity_root": "nullable_single",
        "/normative_input_refs": "array"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "UTF8 LF no BOM",
        "exact section order is normative",
        "no implementation or execution authorization",
        "K008 has activity_root=K007 and empty normative_input_refs",
        "K142E has activity_root=null and exact normative_input_refs"
      ]
    },
    "architecture_document.v1": {
      "media_type": "text/markdown",
      "serialization": "UTF8_LF_NO_BOM",
      "required_fields": [
        "/document_id",
        "/canonical_commit_ref",
        "/canonical_input_manifest",
        "/amended_base",
        "/authorization_effect"
      ],
      "fields": {
        "/document_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/canonical_commit_ref": {
          "type": "NodeRef",
          "nullable": false
        },
        "/canonical_input_manifest": {
          "type": "NodeRef",
          "nullable": false
        },
        "/amended_base": {
          "type": "Nullable<NodeRef>",
          "nullable": true
        },
        "/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/canonical_commit_ref": "single",
        "/canonical_input_manifest": "single",
        "/amended_base": "nullable_single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "architecture only",
        "no execution authorization"
      ]
    },
    "review.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/reviewed_submission",
        "/payload/reviewed_handoff",
        "/payload/evidence_refs",
        "/payload/reviewer",
        "/payload/disposition",
        "/payload/decision_code",
        "/payload/findings"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/reviewed_submission": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/reviewed_handoff": {
          "type": "Nullable<NodeRef>",
          "nullable": true
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/reviewer": {
          "type": "Enum[Sentinel]",
          "nullable": false
        },
        "/payload/disposition": {
          "type": "Enum[APPROVE,ACCEPT_FINDING,BLOCK,DEFER,NEEDS_VERIFICATION]",
          "nullable": false
        },
        "/payload/decision_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/findings": {
          "type": "Array<FindingRow>",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/reviewed_submission": "single",
        "/payload/reviewed_handoff": "nullable_single",
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "findings by code",
        "evidence_refs in node binding order"
      ],
      "uniqueness": [
        "findings.code",
        "evidence_refs.node_id"
      ],
      "equations": [],
      "constraints": [
        "APPROVE requires zero BLOCKING findings",
        "BLOCK requires >=1 BLOCKING finding",
        "ACCEPT_FINDING is non-authorizing"
      ]
    },
    "submission.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/source_handoff",
        "/payload/requested_decision",
        "/payload/submission_status",
        "/payload/authorization_effect"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/source_handoff": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/requested_decision": {
          "type": "Enum[APPROVE,BLOCK,DEFER,NEEDS_VERIFICATION]",
          "nullable": false
        },
        "/payload/submission_status": {
          "type": "Enum[SUBMITTED]",
          "nullable": false
        },
        "/payload/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/source_handoff": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "source_handoff is exact completed prior-stage handoff",
        "no review disposition or acceptance is prefilled",
        "authorization_effect=NONE"
      ]
    },
    "acceptance.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/accepted_submission",
        "/payload/review_record",
        "/payload/evidence_refs",
        "/payload/decision",
        "/payload/decision_code",
        "/payload/accepted_limitations",
        "/payload/successor_authorization"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/accepted_submission": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/review_record": {
          "type": "Nullable<NodeRef>",
          "nullable": true
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/decision": {
          "type": "Enum[APPROVE,ACCEPT_FINDING]",
          "nullable": false
        },
        "/payload/decision_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/accepted_limitations": {
          "type": "Array<FindingRow>",
          "nullable": false
        },
        "/payload/successor_authorization": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/accepted_submission": "single",
        "/payload/review_record": "nullable_single",
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "exact reviewed bytes equal accepted_submission",
        "review disposition equals decision",
        "successor_authorization=NONE"
      ]
    },
    "gustavo_authorization.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/prerequisite_acceptance",
        "/payload/activity_authorization_id",
        "/payload/stage_code",
        "/payload/permitted_actor",
        "/payload/permitted_activity",
        "/payload/permitted_input_roots",
        "/payload/permitted_output_roots",
        "/payload/scope_constraints",
        "/payload/status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/prerequisite_acceptance": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/additional_prerequisites": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false,
          "optional": true
        },
        "/payload/activity_authorization_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/stage_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/permitted_actor": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/permitted_activity": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/permitted_input_roots": {
          "type": "Array<RelativePath>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/permitted_output_roots": {
          "type": "Array<RelativePath>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/scope_constraints": {
          "type": "GustavoAuthorizationScope",
          "nullable": false
        },
        "/payload/status": {
          "type": "Enum[AUTHORIZED]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/prerequisite_acceptance": "single",
        "/payload/additional_prerequisites": "array"
      },
      "additional_fields": false,
      "ordering": [
        "roots UTF-8",
        "additional prerequisites in Appendix-A order"
      ],
      "uniqueness": [
        "permitted_input_roots",
        "permitted_output_roots",
        "additional_prerequisites.node_id"
      ],
      "equations": [],
      "constraints": [
        "additional_prerequisites absent iff empty",
        "authorization precedes Sentinel stage authorization",
        "implementation_or_execution_authorization explicit"
      ]
    },
    "sentinel_authorization.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/prerequisite_acceptance",
        "/payload/gustavo_authorization",
        "/payload/stage_authorization_id",
        "/payload/stage_code",
        "/payload/activated_actor",
        "/payload/activated_activity",
        "/payload/activated_input_roots",
        "/payload/activated_output_roots",
        "/payload/activated_scope_constraints",
        "/payload/decision"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/prerequisite_acceptance": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/additional_prerequisites": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false,
          "optional": true
        },
        "/payload/gustavo_authorization": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/stage_authorization_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/stage_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/activated_actor": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/activated_activity": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/activated_input_roots": {
          "type": "Array<RelativePath>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/activated_output_roots": {
          "type": "Array<RelativePath>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/activated_scope_constraints": {
          "type": "SentinelActivatedScope",
          "nullable": false
        },
        "/payload/decision": {
          "type": "Enum[AUTHORIZE_STAGE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/prerequisite_acceptance": "single",
        "/payload/additional_prerequisites": "array",
        "/payload/gustavo_authorization": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "additional_prerequisites absent iff empty",
        "created_at_utc_ms > Gustavo created_at_utc_ms",
        "scope is equal or strict subset",
        "canonical_commit equal across both records"
      ]
    },
    "activity_root.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/prerequisite_acceptance",
        "/payload/gustavo_authorization",
        "/payload/sentinel_stage_authorization",
        "/payload/activity_root_id",
        "/payload/stage_code",
        "/payload/run_id",
        "/payload/input_roots",
        "/payload/output_roots",
        "/payload/activity_scope"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/prerequisite_acceptance": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/additional_prerequisites": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false,
          "optional": true
        },
        "/payload/gustavo_authorization": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/sentinel_stage_authorization": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/activity_root_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/stage_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/run_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/input_roots": {
          "type": "Array<RelativePath>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/output_roots": {
          "type": "Array<RelativePath>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/activity_scope": {
          "type": "ActivityScope",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/prerequisite_acceptance": "single",
        "/payload/additional_prerequisites": "array",
        "/payload/gustavo_authorization": "single",
        "/payload/sentinel_stage_authorization": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "additional_prerequisites absent iff empty",
        "root time later than both authorizations",
        "same stage/actor/commit",
        "roots subset of both authorizations"
      ]
    },
    "handoff.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/control_refs",
        "/payload/deliverable_refs",
        "/payload/evidence_refs",
        "/payload/handoff_id",
        "/payload/stage_code",
        "/payload/actions_performed",
        "/payload/actions_not_performed",
        "/payload/effects",
        "/payload/self_identity",
        "/payload/authorization_effect"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/control_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/deliverable_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/handoff_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/stage_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/actions_performed": {
          "type": "Array<RecordId>",
          "nullable": false
        },
        "/payload/actions_not_performed": {
          "type": "Array<RecordId>",
          "nullable": false
        },
        "/payload/effects": {
          "type": "EffectCounts",
          "nullable": false
        },
        "/payload/self_identity": {
          "type": "Nullable<HandoffSelfIdentity>",
          "nullable": true
        },
        "/payload/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/control_refs": "array",
        "/payload/deliverable_refs": "array",
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "all ref arrays in node binding order"
      ],
      "uniqueness": [
        "all NodeRefs by node_id",
        "actions_performed",
        "actions_not_performed"
      ],
      "equations": [],
      "constraints": [
        "actions sets disjoint",
        "deliverable bytes preexist handoff",
        "raw handoff sha256 is bound only by an external delivery envelope or detached successor; self_identity may bind raw byte length and a projection that omits self_identity",
        "no successor authorization"
      ]
    },
    "source_matrix.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/file_matrix",
        "/payload/matrix_closed",
        "/payload/implementation_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/file_matrix": {
          "type": "Array<SourceFileRow>",
          "min_items": 14,
          "max_items": 14,
          "nullable": false
        },
        "/payload/matrix_closed": {
          "type": "Enum[true]",
          "nullable": false
        },
        "/payload/implementation_status": {
          "type": "Enum[CANDIDATE_ONLY]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [
        "file_matrix by logical_path UTF-8"
      ],
      "uniqueness": [
        "file_matrix.logical_path"
      ],
      "equations": [
        "file_count=14"
      ],
      "constraints": [
        "paths equal exact implementation_source_matrix",
        "no unlisted source path",
        "each row has path, role, language=PYTHON, byte_length, sha256, required=true"
      ]
    },
    "test_matrix.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/file_matrix",
        "/payload/matrix_closed",
        "/payload/execution_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/file_matrix": {
          "type": "Array<TestFileRow>",
          "min_items": 14,
          "max_items": 14,
          "nullable": false
        },
        "/payload/matrix_closed": {
          "type": "Enum[true]",
          "nullable": false
        },
        "/payload/execution_status": {
          "type": "Enum[NOT_EXECUTED]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [
        "file_matrix by logical_path UTF-8"
      ],
      "uniqueness": [
        "file_matrix.logical_path"
      ],
      "equations": [
        "file_count=14"
      ],
      "constraints": [
        "paths equal exact test_source_matrix",
        "no unlisted test path",
        "test authoring does not authorize execution"
      ]
    },
    "execution_result.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/result_rows",
        "/payload/summary"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/result_rows": {
          "type": "Array<TestResultRow>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/summary": {
          "type": "TestSummary",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [
        "summary.total=pass+fail+error+skip",
        "summary.total=len(result_rows)"
      ],
      "constraints": [
        "K028 transitively binds exact accepted test source",
        "every result row binds exact test file path and test ID",
        "no result may be inferred"
      ]
    },
    "s4_input_manifest.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/consumed_inputs",
        "/payload/input_contracts",
        "/payload/universe_count",
        "/payload/subclass_counts"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/consumed_inputs": {
          "type": "Array<S4InputManifestRow>",
          "min_items": 9,
          "max_items": 9,
          "nullable": false
        },
        "/payload/input_contracts": {
          "type": "S4InputContractSet",
          "nullable": false
        },
        "/payload/universe_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/subclass_counts": {
          "type": "SubclassCounts",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [
        "consumed_inputs by input_role order defined in registry"
      ],
      "uniqueness": [
        "consumed_inputs.input_role",
        "consumed_inputs.logical_path"
      ],
      "equations": [
        "universe_count=39693",
        "subclass sum=39693"
      ],
      "constraints": [
        "exact nine roles",
        "all byte identities verified before parsing",
        "unapproved roots forbidden"
      ]
    },
    "s4_ledger.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/input_manifest",
        "/payload/rows"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/input_manifest": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/rows": {
          "type": "Array<S4LedgerRow>",
          "min_items": 39693,
          "max_items": 39693,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/input_manifest": "single"
      },
      "additional_fields": false,
      "ordering": [
        "rows by condition_id UTF-8"
      ],
      "uniqueness": [
        "rows.condition_id"
      ],
      "equations": [
        "row_count=39693",
        "subclass counts fixed",
        "each row matches exactly one P00-P18 class"
      ],
      "constraints": [
        "winner fields forbidden",
        "every source identity traces to K036"
      ]
    },
    "provenance_wrapper.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/control_refs",
        "/payload/scientific_ref",
        "/payload/source_refs",
        "/payload/wrapper_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/control_refs": {
          "type": "Array<NodeRef>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/scientific_ref": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/source_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/wrapper_status": {
          "type": "Enum[COMPLETE,INCOMPLETE,BLOCKED]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/control_refs": "array",
        "/payload/scientific_ref": "single",
        "/payload/source_refs": "array"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "wrapper bytes never enter scientific identity",
        "all refs exact"
      ]
    },
    "reconciliation.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/counts",
        "/payload/equations",
        "/payload/status",
        "/payload/effect",
        "/payload/stop_code"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/counts": {
          "type": "ClosedCountObject",
          "nullable": false
        },
        "/payload/equations": {
          "type": "Array<EquationResult>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/status": {
          "type": "Enum[PASS,FAIL,INCOMPLETE]",
          "nullable": false
        },
        "/payload/effect": {
          "type": "Enum[CLEAR_COMPONENT,BLOCKING_DEFECT,INCOMPLETE_EVIDENCE,LIMITATION]",
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "equations by equation_id"
      ],
      "uniqueness": [
        "equations.equation_id"
      ],
      "equations": [],
      "constraints": [
        "PASS iff all equations true and all evidence complete",
        "FAIL iff contradiction or malformed evidence",
        "INCOMPLETE iff missing evidence and no contradiction"
      ]
    },
    "safe_span_plan.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/candidate_spans_seconds",
        "/payload/safety_margin_seconds",
        "/payload/canary_requests",
        "/payload/method",
        "/payload/bounds"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/candidate_spans_seconds": {
          "type": "Array<UInt32>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/safety_margin_seconds": {
          "type": "UInt32",
          "nullable": false
        },
        "/payload/canary_requests": {
          "type": "Array<CanaryRequest>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/method": {
          "type": "Const[GET /prices-history,fidelity=1,interval=null]",
          "nullable": false
        },
        "/payload/bounds": {
          "type": "S5Bounds",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [
        "candidate spans ascending",
        "canaries by condition_id,outcome_index,token_id"
      ],
      "uniqueness": [
        "candidate_spans_seconds",
        "canary request identity"
      ],
      "equations": [],
      "constraints": [
        "canary selection outcome/winner/coverage/profitability blind"
      ]
    },
    "safe_span_evidence.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/preflight_plan",
        "/payload/attempts"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/preflight_plan": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/attempts": {
          "type": "Array<CanaryAttempt>",
          "min_items": 1,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/preflight_plan": "single"
      },
      "additional_fields": false,
      "ordering": [
        "candidate_span,canary_request_id,attempt_ordinal"
      ],
      "uniqueness": [
        "candidate_span,canary_request_id,attempt_ordinal"
      ],
      "equations": [],
      "constraints": [
        "every attempt classified by total safe_span_classifier",
        "conflicting duplicate is integrity failure"
      ]
    },
    "safe_span_closure.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/preflight_plan",
        "/payload/preflight_evidence",
        "/payload/candidate_results",
        "/payload/closure_status",
        "/payload/approved_chunk_span_seconds"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/preflight_plan": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/preflight_evidence": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/candidate_results": {
          "type": "Array<SafeSpanCandidateResult>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/closure_status": {
          "type": "Enum[SAFE_POLICY_CANDIDATE,PREFLIGHT_INCOMPLETE,PREFLIGHT_INTEGRITY_FAILURE,NO_SAFE_SPAN,NO_SAFE_SPAN_AFTER_MARGIN]",
          "nullable": false
        },
        "/payload/approved_chunk_span_seconds": {
          "type": "Nullable<UInt32>",
          "nullable": true
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/preflight_plan": "single",
        "/payload/preflight_evidence": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [
        "attempt_expected=candidate_count*canary_count",
        "safe candidate iff every canary SAFE"
      ],
      "constraints": [
        "reducer precedence exact",
        "approved span non-null only SAFE_POLICY_CANDIDATE"
      ]
    },
    "span_policy_candidate.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/preflight_plan",
        "/payload/preflight_closure",
        "/payload/preflight_handoff",
        "/payload/candidate_spans_seconds",
        "/payload/safety_margin_seconds",
        "/payload/approved_chunk_span_seconds",
        "/payload/candidate_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/preflight_plan": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/preflight_closure": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/preflight_handoff": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/candidate_spans_seconds": {
          "type": "Array<UInt32>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/safety_margin_seconds": {
          "type": "UInt32",
          "nullable": false
        },
        "/payload/approved_chunk_span_seconds": {
          "type": "UInt32",
          "nullable": false
        },
        "/payload/candidate_status": {
          "type": "Enum[SUBMITTED]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/preflight_plan": "single",
        "/payload/preflight_closure": "single",
        "/payload/preflight_handoff": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "approved span equals closure output",
        "no empirical value invented"
      ]
    },
    "request_plan_family.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/s4_ledger",
        "/payload/span_policy",
        "/payload/activity_root",
        "/payload/rows"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/s4_ledger": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/span_policy": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/rows": {
          "type": "Array<RequestPlanRow>",
          "min_items": 0,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/s4_ledger": "single",
        "/payload/span_policy": "single",
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [
        "condition_id,outcome_index,chunk_ordinal,request_id"
      ],
      "uniqueness": [
        "request_id",
        "condition_id,outcome_index,chunk_ordinal"
      ],
      "equations": [],
      "constraints": [
        "two independent token sides per stable pair",
        "request_id exact hash preimage",
        "no batch requests"
      ]
    },
    "request_plan_manifest.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/request_plan_family",
        "/payload/row_count",
        "/payload/per_subclass_counts",
        "/payload/family_members"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/request_plan_family": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/row_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/per_subclass_counts": {
          "type": "ClosedCountObject",
          "nullable": false
        },
        "/payload/family_members": {
          "type": "Array<ArtifactIdentity>",
          "min_items": 2,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/request_plan_family": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [
        "row_count=sum(per_subclass_counts)",
        "family member count exact"
      ],
      "constraints": [
        "all rows covered exactly once"
      ]
    },
    "attempt_family.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/request_plan_manifest",
        "/payload/attempts"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/request_plan_manifest": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/attempts": {
          "type": "Array<RequestAttemptRow>",
          "min_items": 0,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/request_plan_manifest": "single"
      },
      "additional_fields": false,
      "ordering": [
        "request_id,attempt_ordinal"
      ],
      "uniqueness": [
        "request_id,attempt_ordinal"
      ],
      "equations": [],
      "constraints": [
        "ordinal contiguous from 1",
        "retry only eligible mapping",
        "payload identity all-or-null"
      ]
    },
    "terminal_family.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/request_plan_family",
        "/payload/attempt_family",
        "/payload/terminals"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/request_plan_family": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/attempt_family": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/terminals": {
          "type": "Array<RequestTerminalRow>",
          "min_items": 0,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/request_plan_family": "single",
        "/payload/attempt_family": "single"
      },
      "additional_fields": false,
      "ordering": [
        "request_id"
      ],
      "uniqueness": [
        "request_id"
      ],
      "equations": [],
      "constraints": [
        "exactly one terminal per finalized request",
        "terminal_mapping total",
        "CLIENT_REJECTED_COMPLETE and NOT_FOUND_COMPLETE forbidden/unreachable"
      ]
    },
    "inventory.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/attempt_family",
        "/payload/terminal_family",
        "/payload/entries",
        "/payload/counts"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/attempt_family": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/terminal_family": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/entries": {
          "type": "Array<RawInventoryRow>",
          "min_items": 0,
          "nullable": false
        },
        "/payload/counts": {
          "type": "RawInventoryCounts",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/attempt_family": "single",
        "/payload/terminal_family": "single"
      },
      "additional_fields": false,
      "ordering": [
        "entry_kind,request_id,attempt_ordinal,logical_path"
      ],
      "uniqueness": [
        "entry identity tuple"
      ],
      "equations": [
        "entry_count=len(entries)",
        "payload_count=sum terminal payloads"
      ],
      "constraints": [
        "all attempt/terminal/payload identities covered"
      ]
    },
    "completion.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/request_plan_manifest",
        "/payload/terminal_family",
        "/payload/inventory",
        "/payload/counts",
        "/payload/status",
        "/payload/stop_code"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/request_plan_manifest": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/terminal_family": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/inventory": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/counts": {
          "type": "AcquisitionCompletionCounts",
          "nullable": false
        },
        "/payload/status": {
          "type": "Enum[COMPLETE,INCOMPLETE,BLOCKED]",
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/request_plan_manifest": "single",
        "/payload/terminal_family": "single",
        "/payload/inventory": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [
        "planned=payload_complete+empty_complete+transient_exhausted+blocking",
        "terminal_count=planned when status COMPLETE or BLOCKED"
      ],
      "constraints": [
        "COMPLETE only no incomplete/blocking",
        "INCOMPLETE only missing/transient and no blocking",
        "BLOCKED iff blocking>0"
      ]
    },
    "archive.v1": {
      "media_type": "application/x-tar",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/provenance/evidence_refs",
        "/archive_profile_id",
        "/members"
      ],
      "fields": {
        "/provenance/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 3,
          "max_items": 3,
          "nullable": false
        },
        "/archive_profile_id": {
          "type": "Const[pm_research.s2.posix_ustar.v1]",
          "nullable": false
        },
        "/members": {
          "type": "Array<ArchiveMember>",
          "min_items": 3,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/provenance/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "provenance.json,inventory.json,completion.json,then payload paths UTF-8"
      ],
      "uniqueness": [
        "members.logical_path"
      ],
      "equations": [],
      "constraints": [
        "uncompressed POSIX ustar exact profile",
        "provenance.json is JCS and contains exact typed refs K055,K060,K061",
        "two final zero blocks"
      ]
    },
    "archive_identity.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/raw_archive",
        "/payload/archive_profile_id",
        "/payload/archive_byte_length",
        "/payload/archive_sha256"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/raw_archive": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/archive_profile_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/archive_byte_length": {
          "type": "ByteLength",
          "nullable": false
        },
        "/payload/archive_sha256": {
          "type": "Sha256",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/raw_archive": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "identity equals exact K062 bytes",
        "record does not hash itself"
      ]
    },
    "construction_contract.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/accepted_specification",
        "/payload/accepted_implementation_source",
        "/payload/profile_ids",
        "/payload/partition_matrix",
        "/payload/row_schema",
        "/payload/duplicate_reducer",
        "/payload/build_identity_contract",
        "/payload/rebuild_inputs"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/accepted_specification": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/accepted_implementation_source": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/profile_ids": {
          "type": "ConstructionProfileIds",
          "nullable": false
        },
        "/payload/partition_matrix": {
          "type": "Array<PartitionDefinition>",
          "min_items": 6,
          "max_items": 6,
          "nullable": false
        },
        "/payload/row_schema": {
          "type": "PerTokenPriceRowSchema",
          "nullable": false
        },
        "/payload/duplicate_reducer": {
          "type": "DuplicateReducerContract",
          "nullable": false
        },
        "/payload/build_identity_contract": {
          "type": "BuildIdentityContract",
          "nullable": false
        },
        "/payload/rebuild_inputs": {
          "type": "Array<Enum[K068,A003,A005,A007,FIXED_PROFILES]>",
          "min_items": 5,
          "max_items": 5,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/accepted_specification": "single",
        "/payload/accepted_implementation_source": "single"
      },
      "additional_fields": false,
      "ordering": [
        "partition_matrix subclass then outcome_index"
      ],
      "uniqueness": [
        "partition path",
        "rebuild_inputs"
      ],
      "equations": [],
      "constraints": [
        "K082 absent from rebuild_inputs",
        "activity provenance forbidden in scientific identities"
      ]
    },
    "alignment_policy.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/selector",
        "/payload/max_side_staleness_ms",
        "/payload/max_inter_side_skew_ms",
        "/payload/tie_break_rule",
        "/payload/status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/selector": {
          "type": "Enum[EXACT_COINCIDENT_PAIR,FIRST_AT_OR_AFTER_ANCHOR]",
          "nullable": false
        },
        "/payload/max_side_staleness_ms": {
          "type": "UInt64Dec",
          "nullable": false
        },
        "/payload/max_inter_side_skew_ms": {
          "type": "UInt64Dec",
          "nullable": false
        },
        "/payload/tie_break_rule": {
          "type": "Const[EARLIEST_PRICE_TS_THEN_ROW_KEY_SHA256]",
          "nullable": false
        },
        "/payload/status": {
          "type": "RecordId",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "no interpolation/carry/averaging/midpoint/complement",
        "decimal strings compare numerically"
      ]
    },
    "absence_record.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/absence_code",
        "/payload/effect",
        "/payload/successor_authorization"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/absence_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/effect": {
          "type": "Enum[INCOMPLETE_EVIDENCE,BLOCKING_DEFECT,LIMITATION]",
          "nullable": false
        },
        "/payload/successor_authorization": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "does not create phantom policy"
      ]
    },
    "alignment_ledger.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/s4_ledger",
        "/payload/scientific_manifest",
        "/payload/construction_reconciliation",
        "/payload/alignment_policy",
        "/payload/activity_root",
        "/payload/rows"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/s4_ledger": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/scientific_manifest": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/construction_reconciliation": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/alignment_policy": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/rows": {
          "type": "Array<AlignmentLedgerRow>",
          "min_items": 39693,
          "max_items": 39693,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/s4_ledger": "single",
        "/payload/scientific_manifest": "single",
        "/payload/construction_reconciliation": "single",
        "/payload/alignment_policy": "single",
        "/payload/activity_root": "single"
      },
      "additional_fields": false,
      "ordering": [
        "condition_id"
      ],
      "uniqueness": [
        "condition_id"
      ],
      "equations": [
        "row_count=39693"
      ],
      "constraints": [
        "millisecond boundary exact",
        "selector total",
        "one/neither are limitations"
      ]
    },
    "rebuild_isolation.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/control_refs",
        "/payload/construction_contract",
        "/payload/s4_projection",
        "/payload/request_plan_projection",
        "/payload/raw_payload_root",
        "/payload/fixed_profiles",
        "/payload/forbidden_reads"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/control_refs": {
          "type": "Array<NodeRef>",
          "min_items": 3,
          "nullable": false
        },
        "/payload/construction_contract": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/s4_projection": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/request_plan_projection": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/raw_payload_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/fixed_profiles": {
          "type": "Array<RecordId>",
          "min_items": 2,
          "nullable": false
        },
        "/payload/forbidden_reads": {
          "type": "Array<NodeId>",
          "min_items": 1,
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/control_refs": "array",
        "/payload/construction_contract": "single",
        "/payload/s4_projection": "single",
        "/payload/request_plan_projection": "single",
        "/payload/raw_payload_root": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [
        "fixed_profiles",
        "forbidden_reads"
      ],
      "equations": [],
      "constraints": [
        "scientific read set exactly K068,A003,A005,A007 plus fixed accepted algorithm and serialization profiles",
        "K082 and every alignment artifact forbidden",
        "original scientific outputs and all original activity provenance forbidden"
      ]
    },
    "byte_comparison.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/comparisons",
        "/payload/status",
        "/payload/stop_code"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/comparisons": {
          "type": "Array<ByteComparisonRow>",
          "min_items": 8,
          "max_items": 8,
          "nullable": false
        },
        "/payload/status": {
          "type": "Enum[PASS,FAIL,INCOMPLETE]",
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "six partition payload members then manifest payload then reconciliation payload"
      ],
      "uniqueness": [
        "comparison logical pair"
      ],
      "equations": [
        "comparison_count=8",
        "pass+fail+incomplete=8"
      ],
      "constraints": [
        "comparison rows refer to activity-free payload ArtifactIdentity values, never complete node records",
        "PASS iff six partition member payloads plus manifest payload plus reconciliation payload are byte-identical",
        "original and rebuild node IDs, record IDs, dependencies, timestamps, roots, and wrappers are expected to differ and are not compared",
        "FAIL if any compared present payload bytes differ",
        "INCOMPLETE if any expected payload identity or bytes are absent and no contradiction exists"
      ]
    },
    "effect_ledger.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/rows",
        "/payload/counts"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/rows": {
          "type": "Array<EffectLedgerRow>",
          "min_items": 39693,
          "max_items": 39693,
          "nullable": false
        },
        "/payload/counts": {
          "type": "EffectCounts",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "condition_id"
      ],
      "uniqueness": [
        "condition_id"
      ],
      "equations": [
        "row_count=39693",
        "effect counts sum=39693"
      ],
      "constraints": [
        "each row one final P class",
        "highest effect precedence retained"
      ]
    },
    "audit_closure.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/ordered_evidence",
        "/payload/check_id",
        "/payload/denominator_expression",
        "/payload/population_count",
        "/payload/applicable_count",
        "/payload/not_applicable_count",
        "/payload/pass_count",
        "/payload/fail_count",
        "/payload/incomplete_count",
        "/payload/zero_population_permitted",
        "/payload/status",
        "/payload/effect",
        "/payload/stop_code",
        "/payload/details"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/ordered_evidence": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/check_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/denominator_expression": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/population_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/applicable_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/not_applicable_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/pass_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/fail_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/incomplete_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/zero_population_permitted": {
          "type": "Boolean",
          "nullable": false
        },
        "/payload/status": {
          "type": "Enum[PASS,FAIL,INCOMPLETE]",
          "nullable": false
        },
        "/payload/effect": {
          "type": "Enum[CLEAR_COMPONENT,BLOCKING_DEFECT,INCOMPLETE_EVIDENCE]",
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        },
        "/payload/details": {
          "type": "Array<AuditDetailRow>",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/ordered_evidence": "array"
      },
      "additional_fields": false,
      "ordering": [
        "ordered_evidence exact Appendix A order",
        "details by subject key"
      ],
      "uniqueness": [
        "ordered_evidence.node_id",
        "details.subject_key"
      ],
      "equations": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete"
      ],
      "constraints": [
        "FAIL iff fail_count>0 and effect BLOCKING and stop non-null",
        "INCOMPLETE iff fail=0 and incomplete>0 or forbidden zero population",
        "PASS iff fail=incomplete=0 and zero rule satisfied and effect CLEAR and stop null"
      ]
    },
    "audit_summary.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/closures",
        "/payload/status_counts",
        "/payload/effect_counts",
        "/payload/summary_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/closures": {
          "type": "Array<NodeRef>",
          "min_items": 19,
          "max_items": 19,
          "nullable": false
        },
        "/payload/status_counts": {
          "type": "AuditStatusCounts",
          "nullable": false
        },
        "/payload/effect_counts": {
          "type": "AuditEffectCounts",
          "nullable": false
        },
        "/payload/summary_status": {
          "type": "Enum[PASS,FAIL,INCOMPLETE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/closures": "array"
      },
      "additional_fields": false,
      "ordering": [
        "closures K109..K127"
      ],
      "uniqueness": [
        "closures.node_id"
      ],
      "equations": [
        "closure_count=19",
        "pass+fail+incomplete=19"
      ],
      "constraints": [
        "closures[18].node_id=K127",
        "summary FAIL if any fail",
        "else INCOMPLETE if any incomplete",
        "else PASS"
      ]
    },
    "gate_record.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/activity_root",
        "/payload/effect_ledger",
        "/payload/audit_summary",
        "/payload/gate_state",
        "/payload/counts",
        "/payload/stop_code"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/effect_ledger": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/audit_summary": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/gate_state": {
          "type": "Enum[S2_GATE_CLEAR,S2_GATE_CLEAR_WITH_LIMITATIONS,S2_GATE_INCOMPLETE,S2_GATE_BLOCKED]",
          "nullable": false
        },
        "/payload/counts": {
          "type": "GateCounts",
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        }
      },
      "node_ref_slots": {
        "/payload/activity_root": "single",
        "/payload/effect_ledger": "single",
        "/payload/audit_summary": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [
        "condition effects sum=39693",
        "audit status sum=19"
      ],
      "constraints": [
        "blocking precedence",
        "incomplete precedence",
        "limitation precedence",
        "S2_GATE_CLEAR requires 19 PASS and all alignment-applicable BOTH_SIDE_USABLE"
      ]
    },
    "human_report.v1": {
      "media_type": "text/markdown",
      "serialization": "UTF8_LF_NO_BOM",
      "required_fields": [
        "/source_gate_record",
        "/rendered_sections",
        "/authorization_effect"
      ],
      "fields": {
        "/source_gate_record": {
          "type": "NodeRef",
          "nullable": false
        },
        "/rendered_sections": {
          "type": "Array<RecordId>",
          "min_items": 1,
          "nullable": false
        },
        "/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/source_gate_record": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "rendering only",
        "must not introduce facts absent from K129"
      ]
    },
    "transition_ledger.v1": {
      "media_type": "application/x-ndjson",
      "serialization": "EXACT_RAW_BYTES",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/rows",
        "/payload/eligible_count",
        "/payload/ineligible_count"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/rows": {
          "type": "Array<TransitionRow>",
          "min_items": 39693,
          "max_items": 39693,
          "nullable": false
        },
        "/payload/eligible_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/ineligible_count": {
          "type": "Count",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "condition_id"
      ],
      "uniqueness": [
        "condition_id"
      ],
      "equations": [
        "eligible+ineligible=39693",
        "U0=E disjoint-union I"
      ],
      "constraints": [
        "11 conjuncts evaluated in order",
        "all false reasons retained"
      ]
    },
    "branch_record.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/branch",
        "/payload/counts",
        "/payload/status",
        "/payload/authorization_effect"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/branch": {
          "type": "Enum[ELIGIBLE,INELIGIBLE]",
          "nullable": false
        },
        "/payload/counts": {
          "type": "TransitionCounts",
          "nullable": false
        },
        "/payload/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [
        "eligible+ineligible=39693"
      ],
      "constraints": [
        "exactly one branch exists",
        "ineligible branch creates no P1 candidate"
      ]
    },
    "seal.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/sealed_artifact",
        "/payload/seal_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/sealed_artifact": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/seal_status": {
          "type": "Enum[SEALED]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array",
        "/payload/sealed_artifact": "single"
      },
      "additional_fields": false,
      "ordering": [],
      "uniqueness": [],
      "equations": [],
      "constraints": [
        "artifact bytes preexist seal",
        "no premature seal"
      ]
    },
    "generic_evidence.v1": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/evidence_refs",
        "/payload/record_kind",
        "/payload/status",
        "/payload/counts",
        "/payload/assertions",
        "/payload/stop_code"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/evidence_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/record_kind": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/counts": {
          "type": "ClosedCountObject",
          "nullable": false
        },
        "/payload/assertions": {
          "type": "Array<AssertionResult>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        }
      },
      "node_ref_slots": {
        "/payload/evidence_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "assertions by assertion_id"
      ],
      "uniqueness": [
        "assertions.assertion_id"
      ],
      "equations": [],
      "constraints": [
        "all decision-bearing identities appear only as typed evidence_refs",
        "status determined by assertion precedence"
      ]
    },
    "a003_condition_projection.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "serialized_material": "ACTIVITY_FREE_SCIENTIFIC_PAYLOAD_ONLY",
      "scientific_payload_schema_id": "A003_CONDITION_LEDGER_PROJECTION_V1",
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "provenance_binding_rule": "typed ref_bindings are materialized only in the separate non-compared provenance envelope/wrapper; they are not fields of scientific payload bytes",
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "additional_fields": false
    },
    "a005_request_plan_projection.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "serialized_material": "ACTIVITY_FREE_SCIENTIFIC_PAYLOAD_ONLY",
      "scientific_payload_schema_id": "A005_REQUEST_PLAN_PROJECTION_V1",
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "provenance_binding_rule": "typed ref_bindings are materialized only in the separate non-compared provenance envelope/wrapper; they are not fields of scientific payload bytes",
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "additional_fields": false
    },
    "a007_raw_payload_root_projection.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "serialized_material": "ACTIVITY_FREE_SCIENTIFIC_PAYLOAD_ONLY",
      "scientific_payload_schema_id": "A007_RAW_PAYLOAD_ROOT_PROJECTION_V1",
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "provenance_binding_rule": "typed ref_bindings are materialized only in the separate non-compared provenance envelope/wrapper; they are not fields of scientific payload bytes",
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "additional_fields": false
    },
    "build_identity_payload.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "serialized_material": "ACTIVITY_FREE_SCIENTIFIC_PAYLOAD_ONLY",
      "required_fields": [
        "schema_id",
        "preimage",
        "deterministic_build_id"
      ],
      "fields": {
        "schema_id": {
          "type": "Const[pm_research.s2.build_identity_payload.v2]",
          "nullable": false
        },
        "preimage": {
          "type": "BuildIdentityPreimage",
          "nullable": false
        },
        "deterministic_build_id": {
          "type": "Sha256",
          "nullable": false
        }
      },
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "additional_fields": false,
      "constraints": [
        "deterministic_build_id=SHA256(UTF8(JCS(preimage)))",
        "preimage uses only declared field names",
        "no activity provenance or K082"
      ],
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ]
    },
    "partition_payload_family.v2": {
      "media_type": "application/x-ndjson",
      "serialization": "JCS_OBJECT_PER_LINE_UTF8_NO_BOM_LF_FINAL",
      "serialized_material": "SIX_ACTIVITY_FREE_SCIENTIFIC_PARTITION_MEMBERS",
      "scientific_payload_schema_id": "PARTITION_MEMBER_JSONL_V2",
      "member_count": 6,
      "member_order": [
        "UP_DOWN/0",
        "UP_DOWN/1",
        "OVER_UNDER/0",
        "OVER_UNDER/1",
        "NAMED_OTHER/0",
        "NAMED_OTHER/1"
      ],
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "provenance_binding_rule": "node family envelope and K076/K099 wrappers are not compared; only six member byte sequences are compared",
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "additional_fields": false
    },
    "scientific_manifest_payload.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "serialized_material": "ACTIVITY_FREE_SCIENTIFIC_PAYLOAD_ONLY",
      "scientific_payload_schema_id": "SCIENTIFIC_MANIFEST_PAYLOAD_V2",
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "provenance_binding_rule": "typed ref_bindings are materialized only in the separate non-compared provenance envelope/wrapper; they are not fields of scientific payload bytes",
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "additional_fields": false
    },
    "scientific_reconciliation_payload.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "serialized_material": "ACTIVITY_FREE_SCIENTIFIC_PAYLOAD_ONLY",
      "scientific_payload_schema_id": "SCIENTIFIC_RECONCILIATION_PAYLOAD_V2",
      "edge_binding_storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
      "provenance_binding_rule": "typed ref_bindings are materialized only in the separate non-compared provenance envelope/wrapper; they are not fields of scientific payload bytes",
      "forbidden_serialized_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "additional_fields": false
    },
    "scientific_provenance_wrapper.v2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/source_refs",
        "/payload/scientific_ref",
        "/payload/scientific_payload_identities",
        "/payload/activity_root",
        "/payload/actor",
        "/payload/environment",
        "/payload/physical_output_root",
        "/payload/wrapper_status"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/source_refs": {
          "type": "Array<NodeRef>",
          "min_items": 9,
          "max_items": 9,
          "nullable": false
        },
        "/payload/scientific_ref": {
          "type": "NodeRef",
          "nullable": false
        },
        "/payload/scientific_payload_identities": {
          "type": "Array<ScientificPayloadIdentity>",
          "min_items": 8,
          "max_items": 8,
          "nullable": false
        },
        "/payload/activity_root": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/actor": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/environment": {
          "type": "Utf8String",
          "nullable": false
        },
        "/payload/physical_output_root": {
          "type": "RelativePath",
          "nullable": false
        },
        "/payload/wrapper_status": {
          "type": "Enum[COMPLETE,INCOMPLETE,BLOCKED]",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/source_refs": "array",
        "/payload/scientific_ref": "single"
      },
      "additional_fields": false,
      "ordering": [
        "scientific_payload_identities: six partition members, manifest payload, reconciliation payload"
      ],
      "uniqueness": [
        "scientific_payload_identities.logical_path"
      ],
      "equations": [
        "array_length(scientific_payload_identities)=8"
      ],
      "constraints": [
        "wrapper is activity provenance and is never byte-compared",
        "payload identities bind exact activity-free bytes",
        "original and rebuild wrappers have different node_id, record_id, dependencies, created_at_utc_ms, roots, actors, and environments without causing comparison failure"
      ]
    },
    "candidate08_professor_handoff.v1": {
      "media_type": "text/markdown; charset=utf-8",
      "serialization": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/actions_not_performed",
        "/payload/actions_performed",
        "/payload/administrative_role_source_context",
        "/payload/authorization_effect",
        "/payload/blocked_input_identities",
        "/payload/control_refs",
        "/payload/deliverable_refs",
        "/payload/handoff_id",
        "/payload/run_id",
        "/payload/self_identity",
        "/payload/stage_code",
        "/payload/static_checks"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "Candidate08HandoffPayloadV1",
          "nullable": false
        },
        "/payload/actions_not_performed": {
          "type": "Array<RecordId>",
          "nullable": false
        },
        "/payload/actions_performed": {
          "type": "Array<RecordId>",
          "nullable": false
        },
        "/payload/administrative_role_source_context": {
          "type": "AdministrativeRoleSourceContextV1",
          "nullable": false
        },
        "/payload/authorization_effect": {
          "type": "Enum[NONE]",
          "nullable": false
        },
        "/payload/blocked_input_identities": {
          "type": "Array<ArtifactIdentity>",
          "min_items": 2,
          "max_items": 2,
          "nullable": false
        },
        "/payload/control_refs": {
          "type": "Array<NodeRef>",
          "min_items": 3,
          "max_items": 3,
          "nullable": false
        },
        "/payload/deliverable_refs": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "max_items": 1,
          "nullable": false
        },
        "/payload/handoff_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/run_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/self_identity": {
          "type": "HandoffSelfIdentity",
          "nullable": false
        },
        "/payload/stage_code": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/static_checks": {
          "type": "Candidate08StaticChecksV3",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/control_refs": "array",
        "/payload/deliverable_refs": "array"
      },
      "additional_fields": false,
      "ordering": [
        "dependencies and control_refs exact K006,K005,K007 order",
        "deliverable_refs exact singleton K008",
        "blocked_input_identities exact blocked K008 then blocked K009",
        "all action arrays retain declared order"
      ],
      "uniqueness": [
        "dependencies by node_id",
        "control_refs by node_id",
        "deliverable_refs by node_id",
        "actions_performed",
        "actions_not_performed"
      ],
      "equations": [
        "len(dependencies)=4",
        "len(control_refs)=3",
        "len(deliverable_refs)=1",
        "k008_normative_payload_count=1",
        "k009_normative_payload_count=1"
      ],
      "constraints": [
        "top-level key set and payload key set are exact; no undeclared field at any nested closed object",
        "schema_id=pm_research.s2.professor_review_handoff.v5",
        "record_id=HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW",
        "node_id=K009",
        "canonical_commit=70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "status=SUBMITTED_FOR_SENTINEL_SPECIFICATION_REVIEW",
        "payload.handoff_id=HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW",
        "payload.stage_code=CANDIDATE_08_SPEC_ONLY_DRAFTING",
        "payload.run_id=S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
        "payload.self_identity.raw_sha256_binding_location=EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD",
        "raw K009 sha256 is absent from raw K009 bytes and supplied externally",
        "static_submission_gate=CLEAR iff every mandatory raw-deliverable validation succeeds"
      ]
    },
    "exact_current_gustavo_authorization.v4": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "exact_record_schema_id": "pm_research.s2.exact_current_record.K006.v3",
      "edge_binding_storage": "ARTIFACT_FIELD",
      "node_ref_slots": {
        "/payload/prerequisite_acceptance": "single"
      },
      "additional_fields": false,
      "constraints": [
        "raw bytes MUST validate exact_current_record_schemas.K006",
        "dependencies MUST equal semantic ref slots and accepted edge order"
      ]
    },
    "exact_current_sentinel_authorization.v4": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "exact_record_schema_id": "pm_research.s2.exact_current_record.K005.v3",
      "edge_binding_storage": "ARTIFACT_FIELD",
      "node_ref_slots": {
        "/payload/prerequisite_acceptance": "single",
        "/payload/gustavo_authorization": "single"
      },
      "additional_fields": false,
      "constraints": [
        "raw bytes MUST validate exact_current_record_schemas.K005",
        "dependencies MUST equal semantic ref slots and accepted edge order"
      ]
    },
    "exact_current_activity_root.v4": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "exact_record_schema_id": "pm_research.s2.exact_current_record.K007.v3",
      "edge_binding_storage": "ARTIFACT_FIELD",
      "node_ref_slots": {
        "/payload/prerequisite_acceptance": "single",
        "/payload/gustavo_authorization": "single",
        "/payload/sentinel_stage_authorization": "single"
      },
      "additional_fields": false,
      "constraints": [
        "raw bytes MUST validate exact_current_record_schemas.K007",
        "dependencies MUST equal semantic ref slots and accepted edge order"
      ]
    }
  },
  "row_schemas": {
    "CanonicalInputRow": {
      "required": [
        "logical_path",
        "byte_length",
        "sha256"
      ],
      "fields": {
        "logical_path": "RelativePath",
        "byte_length": "ByteLength",
        "sha256": "Sha256"
      },
      "additional_fields": false,
      "constraints": [
        "path in canonical_input_paths"
      ]
    },
    "ConditionUniverseRow": {
      "required": [
        "schema_id",
        "condition_id",
        "universe_ordinal",
        "p0_disposition"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.condition_universe_row.v1]",
        "condition_id": "ConditionId",
        "universe_ordinal": "UniverseOrdinal",
        "p0_disposition": "Const[P0_ELIGIBLE]"
      },
      "additional_fields": false,
      "ordering": "universe_ordinal strictly increasing",
      "uniqueness": [
        "condition_id",
        "universe_ordinal"
      ]
    },
    "ClassificationRow": {
      "required": [
        "schema_id",
        "condition_id",
        "subclass"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.classification_row.v1]",
        "condition_id": "ConditionId",
        "subclass": "Subclass"
      },
      "additional_fields": false,
      "uniqueness": [
        "condition_id"
      ],
      "conflict_rule": "duplicate identical idempotent; any differing subclass BLOCKING"
    },
    "ResolutionSourceRow": {
      "required": [
        "schema_id",
        "condition_id",
        "resolved_at_raw"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.resolution_source_row.v1]",
        "condition_id": "ConditionId",
        "resolved_at_raw": "Nullable<StrictUtcTimestampString>"
      },
      "additional_fields": false,
      "uniqueness": [
        "condition_id after duplicate reduction"
      ],
      "parse_rule": "accept exactly YYYY-MM-DD HH:MM:SS UTC or YYYY-MM-DD HH:MM:SS.fff UTC; fractional digits exactly 3 when present; Gregorian valid; integer UTC ms; null/malformed is BLOCKED_RESOLUTION_BOUNDARY",
      "duplicate_rule": "identical raw rows idempotent; null+value or differing values conflict and block"
    },
    "FirstTradeSourceRow": {
      "required": [
        "schema_id",
        "condition_id",
        "first_trade_raw"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.first_trade_source_row.v1]",
        "condition_id": "ConditionId",
        "first_trade_raw": "Nullable<StrictUtcTimestampString>"
      },
      "additional_fields": false,
      "uniqueness": [
        "condition_id after duplicate reduction"
      ],
      "parse_rule": "same strict UTC grammar; null means INCOMPLETE_MISSING_TRADE_ANCHOR; malformed non-null blocks precision/input integrity",
      "duplicate_rule": "identical idempotent; differing values conflict and block"
    },
    "TokenOutcomeTupleRow": {
      "required": [
        "schema_id",
        "condition_id",
        "token_id",
        "outcome_index"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.token_outcome_tuple_row.v1]",
        "condition_id": "ConditionId",
        "token_id": "TokenId",
        "outcome_index": "OutcomeIndex"
      },
      "additional_fields": false,
      "uniqueness": [
        "condition_id,token_id,outcome_index"
      ],
      "duplicate_rule": "exact duplicates idempotent; >1 token per outcome or same token on both outcomes blocks",
      "forbidden_fields": [
        "winner",
        "winning_token",
        "payout",
        "resolution_result",
        "price",
        "profitability"
      ]
    },
    "RequestPlanRow": {
      "required": [
        "condition_id",
        "subclass",
        "token_id",
        "outcome_index",
        "chunk_ordinal",
        "start_ts_s",
        "end_ts_s",
        "http_method",
        "route",
        "fidelity",
        "interval",
        "request_id"
      ],
      "fields": {
        "condition_id": "ConditionId",
        "subclass": "Subclass",
        "token_id": "TokenId",
        "outcome_index": "OutcomeIndex",
        "chunk_ordinal": "UInt32",
        "start_ts_s": "UtcSecond",
        "end_ts_s": "UtcSecond",
        "http_method": "Const[GET]",
        "route": "Const[/prices-history]",
        "fidelity": "Const[1]",
        "interval": "Const[null]",
        "request_id": "RecordId"
      },
      "additional_fields": false,
      "constraints": [
        "start<end",
        "request_id exact hash of preceding fields"
      ]
    },
    "PricesHistoryResponse": {
      "top_level": {
        "type": "Object",
        "required": [
          "history"
        ],
        "additional_fields": false
      },
      "history": {
        "type": "Array",
        "min_items": 0,
        "max_items": "authorized max_points_per_payload",
        "order": "wire order retained"
      },
      "point": {
        "type": "Object",
        "required": [
          "t",
          "p"
        ],
        "additional_fields": false,
        "fields": {
          "t": "UtcSecond",
          "p": "PriceLexeme"
        }
      },
      "price_lexeme": "JSON string or JSON number token matching 0|1|0.[0-9]{1,76}; exponent, sign, trailing decimal point, >1, negative, NaN, Infinity forbidden; preserve lexeme then canonicalize by removing trailing fractional zeros; zero becomes 0",
      "empty_representation": "only HTTP 200 application/json body exactly parsing to {history:[]}",
      "malformed_point_rule": "one malformed point makes entire response MALFORMED_BLOCKING; no point skipping"
    },
    "RequestAttemptRow": {
      "required": [
        "request_id",
        "plan_row_key_sha256",
        "attempt_ordinal",
        "request_echo",
        "transport_result",
        "http_status",
        "response_received_at_ms",
        "content_type",
        "raw_request_identity",
        "raw_response_identity",
        "retry_after_raw",
        "retry_after_parse_status",
        "parsed_retry_after_ms",
        "next_delay_ms"
      ],
      "fields": {
        "request_id": "RecordId",
        "plan_row_key_sha256": "Sha256",
        "attempt_ordinal": "UInt32",
        "request_echo": "RequestEcho",
        "transport_result": "TransportResult",
        "transport_error": "Nullable<RecordId>",
        "http_status": "Nullable<UInt32>",
        "response_received_at_ms": "Nullable<UtcMs>",
        "content_type": "Nullable<Utf8String>",
        "raw_request_identity": "ArtifactIdentity",
        "raw_response_identity": "Nullable<ArtifactIdentity>",
        "retry_after_raw": "Nullable<Utf8String>",
        "retry_after_parse_status": "Enum[ABSENT,DELAY_SECONDS,HTTP_DATE,INVALID_IGNORED,OVERFLOW_IGNORED,PAST_DATE_ZERO]",
        "parsed_retry_after_ms": "UInt32",
        "next_delay_ms": "UInt32"
      },
      "additional_fields": false,
      "cross_fields": [
        "attempt_ordinal starts at 1 and is contiguous per request",
        "transport_result=HTTP_RESPONSE iff http_status,response_received_at_ms,raw_response_identity are non-null and transport_error is null",
        "transport_result!=HTTP_RESPONSE iff http_status,response_received_at_ms,content_type,raw_response_identity are null and transport_error is non-null",
        "parsed_retry_after_ms and next_delay_ms are UInt32 and each <=60000",
        "next_delay_ms applies only before attempt_ordinal+1; it is zero when terminal exists or attempts exhausted"
      ]
    },
    "RequestTerminalRow": {
      "required": [
        "request_id",
        "terminal_code",
        "final_attempt_ordinal",
        "final_attempt_identity",
        "payload_identity",
        "effect",
        "stop_code"
      ],
      "fields": {
        "request_id": "RecordId",
        "terminal_code": "Enum[PAYLOAD_COMPLETE,EMPTY_COMPLETE,TRANSIENT_EXHAUSTED,MALFORMED_BLOCKING,IDENTITY_MISMATCH_BLOCKING,UNAUTHORIZED_BLOCKING]",
        "final_attempt_ordinal": "UInt32",
        "final_attempt_identity": "ArtifactIdentity",
        "payload_identity": "Nullable<ArtifactIdentity>",
        "effect": "Enum[CLEAR_COMPONENT,INCOMPLETE_EVIDENCE,BLOCKING_DEFECT]",
        "stop_code": "Nullable<RecordId>"
      },
      "additional_fields": false,
      "forbidden_codes": [
        "NOT_FOUND_COMPLETE",
        "CLIENT_REJECTED_COMPLETE"
      ],
      "cross_fields": [
        "PAYLOAD_COMPLETE requires non-null payload identity, CLEAR_COMPONENT, null stop",
        "EMPTY_COMPLETE requires non-null raw response identity represented by payload_identity, CLEAR_COMPONENT, null stop",
        "TRANSIENT_EXHAUSTED requires null payload identity, INCOMPLETE_EVIDENCE, non-null stop",
        "blocking codes require BLOCKING_DEFECT and non-null stop"
      ]
    },
    "AuditClosurePayload": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "/schema_id",
        "/record_id",
        "/node_id",
        "/canonical_commit",
        "/dependencies",
        "/status",
        "/created_at_utc_ms",
        "/payload",
        "/payload/ordered_evidence",
        "/payload/check_id",
        "/payload/denominator_expression",
        "/payload/population_count",
        "/payload/applicable_count",
        "/payload/not_applicable_count",
        "/payload/pass_count",
        "/payload/fail_count",
        "/payload/incomplete_count",
        "/payload/zero_population_permitted",
        "/payload/status",
        "/payload/effect",
        "/payload/stop_code",
        "/payload/details"
      ],
      "fields": {
        "/schema_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/record_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/node_id": {
          "type": "NodeId",
          "nullable": false
        },
        "/canonical_commit": {
          "type": "GitCommit40",
          "nullable": false
        },
        "/dependencies": {
          "type": "DerivedNodeRefArray",
          "nullable": false
        },
        "/status": {
          "type": "RecordId",
          "nullable": false
        },
        "/created_at_utc_ms": {
          "type": "UtcMs",
          "nullable": false
        },
        "/payload": {
          "type": "ClosedPayloadByProfile",
          "nullable": false
        },
        "/payload/ordered_evidence": {
          "type": "Array<NodeRef>",
          "min_items": 1,
          "nullable": false
        },
        "/payload/check_id": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/denominator_expression": {
          "type": "RecordId",
          "nullable": false
        },
        "/payload/population_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/applicable_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/not_applicable_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/pass_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/fail_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/incomplete_count": {
          "type": "Count",
          "nullable": false
        },
        "/payload/zero_population_permitted": {
          "type": "Boolean",
          "nullable": false
        },
        "/payload/status": {
          "type": "Enum[PASS,FAIL,INCOMPLETE]",
          "nullable": false
        },
        "/payload/effect": {
          "type": "Enum[CLEAR_COMPONENT,BLOCKING_DEFECT,INCOMPLETE_EVIDENCE]",
          "nullable": false
        },
        "/payload/stop_code": {
          "type": "Nullable<RecordId>",
          "nullable": true
        },
        "/payload/details": {
          "type": "Array<AuditDetailRow>",
          "nullable": false
        }
      },
      "node_ref_slots": {
        "/payload/ordered_evidence": "array"
      },
      "additional_fields": false,
      "ordering": [
        "ordered_evidence exact Appendix A order",
        "details by subject key"
      ],
      "uniqueness": [
        "ordered_evidence.node_id",
        "details.subject_key"
      ],
      "equations": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete"
      ],
      "constraints": [
        "FAIL iff fail_count>0 and effect BLOCKING and stop non-null",
        "INCOMPLETE iff fail=0 and incomplete>0 or forbidden zero population",
        "PASS iff fail=incomplete=0 and zero rule satisfied and effect CLEAR and stop null"
      ]
    },
    "GlobalStateVector": {
      "fields": {
        "phase": "GlobalPhase",
        "phase_status": "GlobalPhaseStatus",
        "review_disposition": "ReviewDisposition",
        "halt_code": "Nullable<GlobalHaltCode>"
      },
      "additional_fields": false,
      "reducer": "global_state_reducer_v2",
      "cross_fields": [
        "phase=HALTED iff halt_code is non-null",
        "phase!=HALTED iff halt_code is null",
        "phase_status=BLOCKED for blocking halt codes",
        "phase_status=INCOMPLETE for incomplete halt codes",
        "every vector equals one exact output row of global_state_reducer.v3"
      ]
    },
    "ConditionStateVector": {
      "fields": {
        "position": "Position",
        "window": "WindowState",
        "token_pair": "TokenPairState",
        "request": "RequestState",
        "construction": "ConstructionState",
        "alignment": "AlignmentState",
        "effect": "Effect"
      },
      "additional_fields": false,
      "reducer": "condition_state_class_registry_v2"
    },
    "PerTokenPriceRow": {
      "required": [
        "schema_id",
        "deterministic_build_id",
        "condition_id",
        "subclass",
        "token_id",
        "outcome_index",
        "price_ts_utc_s",
        "price_ts_utc_ms",
        "price",
        "deterministic_source_row_id",
        "row_key_sha256"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.per_token_price_row.v1]",
        "deterministic_build_id": "Sha256",
        "condition_id": "ConditionId",
        "subclass": "Subclass",
        "token_id": "TokenId",
        "outcome_index": "OutcomeIndex",
        "price_ts_utc_s": "UtcSecond",
        "price_ts_utc_ms": "UtcMs",
        "price": "CanonicalDecimalPrice",
        "deterministic_source_row_id": "Sha256",
        "row_key_sha256": "Sha256"
      },
      "additional_fields": false,
      "ordering": "condition_id UTF-8, price_ts_utc_ms numeric, row_key_sha256 ASCII",
      "uniqueness": [
        "row_key_sha256"
      ],
      "cross_fields": [
        "price_ts_utc_ms=price_ts_utc_s*1000",
        "row_key_sha256 equals exact row-key preimage hash",
        "row contains no activity provenance"
      ]
    }
  },
  "safe_span_classifier": {
    "classifier_id": "pm_research.s2.safe_span_attempt_classifier.v4",
    "input_domain": {
      "transport_result": "TransportResult",
      "http_status": "Nullable<UInt32>",
      "identity_conflict": "Boolean",
      "authorization_or_route_violation": "Boolean",
      "redirect_followed_or_required": "Boolean",
      "body_length": "Nullable<ByteLength>",
      "body_exceeds_max_response_bytes": "Boolean",
      "content_type_status": "Enum[NOT_APPLICABLE,VALID_JSON_UTF8,INVALID]",
      "body_parse_status": "Enum[NOT_APPLICABLE,VALID_EMPTY,VALID_NONEMPTY,MALFORMED_JSON,WRONG_TOP_LEVEL,DUPLICATE_KEY,MALFORMED_POINT,FORBIDDEN_FIELD,PRECISION_LOSS]",
      "point_count": "Nullable<Count>",
      "point_count_exceeds_max": "Boolean"
    },
    "cross_field_domain_rules": [
      "transport_result=HTTP_RESPONSE iff http_status and body_length are non-null",
      "transport_result!=HTTP_RESPONSE iff http_status, body_length, content_type_status, body_parse_status, and point_count are NOT_APPLICABLE/null as typed",
      "HTTP status is JcsSafeUInt; status outside 100..599 is permitted only as protocol-invalid input and matches rule SS08",
      "body_exceeds_max_response_bytes is true iff body_length>authorized max_response_bytes",
      "point_count_exceeds_max is true iff point_count non-null and point_count>authorized max_points_per_payload"
    ],
    "ordered_rules": [
      {
        "rule_id": "SS00_DOMAIN_INVALID",
        "when": {
          "cross_field_domain_valid": false
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS01_IDENTITY_CONFLICT",
        "when": {
          "any_true": [
            "identity_conflict"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS02_AUTHORIZATION_OR_REDIRECT",
        "when": {
          "any_true": [
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "all_false": [
            "identity_conflict"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS03_OVERSIZED_BODY",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "body_exceeds_max_response_bytes": true,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "UNSAFE"
      },
      {
        "rule_id": "SS04_TRANSIENT_NO_RESPONSE",
        "when": {
          "transport_result_in": [
            "TIMEOUT",
            "DNS_FAILURE",
            "CONNECTION_FAILURE",
            "TLS_FAILURE",
            "CONNECTION_RESET"
          ],
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INCOMPLETE"
      },
      {
        "rule_id": "SS05_RESOURCE_BOUND_REJECTION",
        "when": {
          "transport_result": "RESOURCE_BOUND_REJECTION",
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "UNSAFE"
      },
      {
        "rule_id": "SS06_LOCAL_OR_UNKNOWN_TRANSPORT_FAILURE",
        "when": {
          "transport_result_in": [
            "LOCALLY_CANCELLED",
            "UNKNOWN_TRANSPORT_FAILURE"
          ],
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS07_HTTP_TRANSIENT",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status_in": [
            408,
            425,
            429
          ],
          "or_http_status_range": [
            500,
            599
          ],
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INCOMPLETE"
      },
      {
        "rule_id": "SS08_HTTP_SPAN_REJECTION",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status_in": [
            413,
            414
          ],
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "UNSAFE"
      },
      {
        "rule_id": "SS09_ALL_OTHER_NON_200",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status_not_equal": 200,
          "exclude_statuses": [
            408,
            413,
            414,
            425,
            429
          ],
          "exclude_http_status_range": [
            500,
            599
          ],
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS10_HTTP_200_CONTENT_TYPE",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status": 200,
          "content_type_status": "INVALID",
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS11_HTTP_200_MALFORMED_BODY",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status": 200,
          "content_type_status": "VALID_JSON_UTF8",
          "body_parse_status_in": [
            "MALFORMED_JSON",
            "WRONG_TOP_LEVEL",
            "DUPLICATE_KEY",
            "MALFORMED_POINT",
            "FORBIDDEN_FIELD",
            "PRECISION_LOSS"
          ],
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "INTEGRITY_FAILURE"
      },
      {
        "rule_id": "SS12_HTTP_200_EXCESSIVE_POINTS",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status": 200,
          "content_type_status": "VALID_JSON_UTF8",
          "body_parse_status_in": [
            "VALID_EMPTY",
            "VALID_NONEMPTY"
          ],
          "point_count_exceeds_max": true,
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "UNSAFE"
      },
      {
        "rule_id": "SS13_HTTP_200_VALID",
        "when": {
          "transport_result": "HTTP_RESPONSE",
          "http_status": 200,
          "content_type_status": "VALID_JSON_UTF8",
          "body_parse_status_in": [
            "VALID_EMPTY",
            "VALID_NONEMPTY"
          ],
          "point_count_exceeds_max": false,
          "body_exceeds_max_response_bytes": false,
          "all_false": [
            "identity_conflict",
            "authorization_or_route_violation",
            "redirect_followed_or_required"
          ],
          "cross_field_domain_valid": true
        },
        "result": "SAFE"
      }
    ],
    "totality_proof": [
      "SS00 maps every cross-field-invalid attempt to INTEGRITY_FAILURE before semantic classification",
      "TransportResult is closed and contains exactly HTTP_RESPONSE, TIMEOUT, DNS_FAILURE, CONNECTION_FAILURE, TLS_FAILURE, CONNECTION_RESET, LOCALLY_CANCELLED, RESOURCE_BOUND_REJECTION, and UNKNOWN_TRANSPORT_FAILURE",
      "every non-HTTP member appears in exactly one of SS04, SS05, or SS06 after SS01-SS02",
      "every HTTP response first partitions by oversized body, then transient statuses, span-rejection statuses, all other non-200 statuses, and status 200",
      "HTTP 200 partitions by content type, malformed body, excessive points, or valid bounded body",
      "ordered rules include explicit negations of higher-precedence booleans; exactly one rule matches every domain-valid attempt",
      "zero matches or multiple matches is PREFLIGHT_INTEGRITY_FAILURE"
    ]
  },
  "prices_history_terminal_mapping": {
    "mapping_id": "pm_research.s2.prices_history_terminal_mapping.v4",
    "transport_domain": "TransportResult",
    "terminal_enum": [
      "PAYLOAD_COMPLETE",
      "EMPTY_COMPLETE",
      "TRANSIENT_EXHAUSTED",
      "MALFORMED_BLOCKING",
      "IDENTITY_MISMATCH_BLOCKING",
      "UNAUTHORIZED_BLOCKING"
    ],
    "forbidden_complete_labels": [
      "NOT_FOUND_COMPLETE",
      "CLIENT_REJECTED_COMPLETE"
    ],
    "ordered_rules": [
      {
        "rule_id": "TM00_DOMAIN_INVALID",
        "when": "RequestAttemptRow cross-field domain invalid",
        "terminal": "MALFORMED_BLOCKING",
        "retry": false
      },
      {
        "rule_id": "TM01_IDENTITY",
        "when": "identity conflict",
        "terminal": "IDENTITY_MISMATCH_BLOCKING",
        "retry": false
      },
      {
        "rule_id": "TM02_AUTHORIZATION",
        "when": "authorization/host/route/credential violation or redirect followed/required",
        "terminal": "UNAUTHORIZED_BLOCKING",
        "retry": false
      },
      {
        "rule_id": "TM03_TRANSIENT_NO_RESPONSE_RETRY",
        "when": "transport_result in TIMEOUT,DNS_FAILURE,CONNECTION_FAILURE,TLS_FAILURE,CONNECTION_RESET and attempt_ordinal<max_attempts",
        "terminal": null,
        "retry": true
      },
      {
        "rule_id": "TM04_TRANSIENT_NO_RESPONSE_EXHAUSTED",
        "when": "same transient no-response class and attempt_ordinal=max_attempts",
        "terminal": "TRANSIENT_EXHAUSTED",
        "retry": false
      },
      {
        "rule_id": "TM05_LOCAL_RESOURCE_OR_UNKNOWN_TRANSPORT_FAILURE",
        "when": "transport_result in LOCALLY_CANCELLED,RESOURCE_BOUND_REJECTION,UNKNOWN_TRANSPORT_FAILURE",
        "terminal": "MALFORMED_BLOCKING",
        "retry": false
      },
      {
        "rule_id": "TM06_HTTP_VALID_NONEMPTY",
        "when": "HTTP_RESPONSE status=200 and exact valid nonempty PricesHistoryResponse within bounds",
        "terminal": "PAYLOAD_COMPLETE",
        "retry": false
      },
      {
        "rule_id": "TM07_HTTP_VALID_EMPTY",
        "when": "HTTP_RESPONSE status=200 and exact recognized empty PricesHistoryResponse within bounds",
        "terminal": "EMPTY_COMPLETE",
        "retry": false
      },
      {
        "rule_id": "TM08_HTTP_TRANSIENT_RETRY",
        "when": "HTTP_RESPONSE status in 408,425,429,500..599 and attempt_ordinal<max_attempts and body bound not crossed",
        "terminal": null,
        "retry": true
      },
      {
        "rule_id": "TM09_HTTP_TRANSIENT_EXHAUSTED",
        "when": "same HTTP transient class and attempt_ordinal=max_attempts and body bound not crossed",
        "terminal": "TRANSIENT_EXHAUSTED",
        "retry": false
      },
      {
        "rule_id": "TM10_HTTP_UNAUTHORIZED",
        "when": "HTTP_RESPONSE status in 300..399,401,403",
        "terminal": "UNAUTHORIZED_BLOCKING",
        "retry": false
      },
      {
        "rule_id": "TM11_ALL_REMAINING_HTTP",
        "when": "every remaining HTTP response, including oversized body, status outside 100..599, 1xx, non-200 2xx, every other 4xx including 404/413/414, malformed content type/JSON/top-level/point, excessive point count, or unrecognized empty shape",
        "terminal": "MALFORMED_BLOCKING",
        "retry": false
      }
    ],
    "complete_evidence_rule": "only TM06 and TM07 are complete evidence; no client rejection is accepted as complete",
    "totality_proof": "RequestAttemptRow domain-invalid inputs map through TM00; otherwise the closed nine-member TransportResult enum plus exhaustive HTTP partition yields exactly one rule"
  },
  "retry_after_contract": {
    "header_cardinality": "zero or one Retry-After field-value after combining is accepted; multiple comma-separated values are INVALID_IGNORED",
    "delay_seconds_grammar": "^(0|[1-9][0-9]*)(\\.[0-9]{1,3})?$ after OWS trim; exact seconds multiplied by 1000 using integer arithmetic; no sign/exponent",
    "http_date_grammar": "IMF-fixdate only; interpreted UTC; delay_ms=max(0,target_epoch_ms-response_received_at_ms)",
    "response_received_at_ms": "exact UTC wall-clock timestamp captured immediately after complete response headers are received in the attempt row; not request start or completion time",
    "overflow": "if decimal conversion or date epoch is outside JcsSafeUInt, status OVERFLOW_IGNORED and value contributes 0",
    "invalid": "status INVALID_IGNORED and value contributes 0",
    "past_http_date": "status PAST_DATE_ZERO and value 0",
    "cap": "parsed contribution min(value,60000)",
    "base": "5000 when attempt_ordinal=1; 20000 when attempt_ordinal>=2; computed piecewise without exponentiation",
    "next_delay": "min(max(base,parsed_contribution),60000)",
    "applies_to": "delay before attempt ordinal n+1 caused by retry-eligible attempt n; no delay is executed or inferred when n=max_attempts",
    "jitter": "forbidden"
  },
  "condition_state_classes": {
    "P00": {
      "position": [
        "INITIAL"
      ],
      "window": [
        "NOT_EVALUATED"
      ],
      "token_pair": [
        "NOT_EVALUATED"
      ],
      "request": [
        "NOT_EVALUATED"
      ],
      "construction": [
        "NOT_EVALUATED"
      ],
      "alignment": [
        "NOT_EVALUATED"
      ],
      "effect": [
        "ACTIVE"
      ]
    },
    "P01": {
      "position": [
        "TOKEN_PAIR"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "NOT_EVALUATED"
      ],
      "request": [
        "NOT_EVALUATED"
      ],
      "construction": [
        "NOT_EVALUATED"
      ],
      "alignment": [
        "NOT_EVALUATED"
      ],
      "effect": [
        "ACTIVE"
      ]
    },
    "P02": {
      "position": [
        "FINAL"
      ],
      "window": [
        "VALID_EXCLUSION_INVALID_WINDOW"
      ],
      "token_pair": [
        "NOT_APPLICABLE_WINDOW"
      ],
      "request": [
        "NOT_APPLICABLE"
      ],
      "construction": [
        "NOT_APPLICABLE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "VALID_EXCLUSION"
      ]
    },
    "P03": {
      "position": [
        "FINAL"
      ],
      "window": [
        "INCOMPLETE_MISSING_TRADE_ANCHOR"
      ],
      "token_pair": [
        "NOT_APPLICABLE_WINDOW"
      ],
      "request": [
        "NOT_APPLICABLE"
      ],
      "construction": [
        "NOT_APPLICABLE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "INCOMPLETE_EVIDENCE"
      ]
    },
    "P04": {
      "position": [
        "FINAL"
      ],
      "window": [
        "BLOCKED_RESOLUTION_BOUNDARY"
      ],
      "token_pair": [
        "NOT_APPLICABLE_WINDOW"
      ],
      "request": [
        "NOT_APPLICABLE"
      ],
      "construction": [
        "NOT_APPLICABLE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "BLOCKING_DEFECT"
      ]
    },
    "P05": {
      "position": [
        "REQUEST"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "NOT_EVALUATED"
      ],
      "construction": [
        "NOT_EVALUATED"
      ],
      "alignment": [
        "NOT_EVALUATED"
      ],
      "effect": [
        "ACTIVE"
      ]
    },
    "P06": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "UNRESOLVED",
        "UNSTABLE",
        "PRECISION_INVALID"
      ],
      "request": [
        "NOT_APPLICABLE"
      ],
      "construction": [
        "NOT_APPLICABLE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "BLOCKING_DEFECT"
      ]
    },
    "P07": {
      "position": [
        "REQUEST"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "PLANNED",
        "IN_PROGRESS"
      ],
      "construction": [
        "NOT_EVALUATED"
      ],
      "alignment": [
        "NOT_EVALUATED"
      ],
      "effect": [
        "ACTIVE"
      ]
    },
    "P08": {
      "position": [
        "CONSTRUCTION"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "NOT_EVALUATED"
      ],
      "alignment": [
        "NOT_EVALUATED"
      ],
      "effect": [
        "ACTIVE"
      ]
    },
    "P09": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "INCOMPLETE"
      ],
      "construction": [
        "NOT_APPLICABLE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "INCOMPLETE_EVIDENCE"
      ]
    },
    "P10": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "BLOCKED"
      ],
      "construction": [
        "NOT_APPLICABLE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "BLOCKING_DEFECT"
      ]
    },
    "P11": {
      "position": [
        "READY_ALIGNMENT"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BOTH_PARTITIONS_INCLUDED",
        "ONE_PARTITION_INCLUDED",
        "NO_PARTITION_INCLUDED"
      ],
      "alignment": [
        "NOT_EVALUATED"
      ],
      "effect": [
        "ACTIVE"
      ]
    },
    "P12": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "INCOMPLETE"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "INCOMPLETE_EVIDENCE"
      ]
    },
    "P13": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BLOCKED"
      ],
      "alignment": [
        "NOT_APPLICABLE"
      ],
      "effect": [
        "BLOCKING_DEFECT"
      ]
    },
    "P14": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BOTH_PARTITIONS_INCLUDED"
      ],
      "alignment": [
        "BOTH_SIDE_USABLE"
      ],
      "effect": [
        "CLEAR_COMPONENT"
      ]
    },
    "P15": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BOTH_PARTITIONS_INCLUDED",
        "ONE_PARTITION_INCLUDED"
      ],
      "alignment": [
        "ONE_SIDE_USABLE"
      ],
      "effect": [
        "LIMITATION"
      ]
    },
    "P16": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BOTH_PARTITIONS_INCLUDED",
        "ONE_PARTITION_INCLUDED",
        "NO_PARTITION_INCLUDED"
      ],
      "alignment": [
        "NEITHER_SIDE_USABLE"
      ],
      "effect": [
        "LIMITATION"
      ]
    },
    "P17": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BOTH_PARTITIONS_INCLUDED",
        "ONE_PARTITION_INCLUDED",
        "NO_PARTITION_INCLUDED"
      ],
      "alignment": [
        "INCOMPLETE"
      ],
      "effect": [
        "INCOMPLETE_EVIDENCE"
      ]
    },
    "P18": {
      "position": [
        "FINAL"
      ],
      "window": [
        "QUERY_ELIGIBLE"
      ],
      "token_pair": [
        "STABLE_INDEPENDENT_PAIR"
      ],
      "request": [
        "COMPLETE_BOTH_TERMINALS"
      ],
      "construction": [
        "BOTH_PARTITIONS_INCLUDED",
        "ONE_PARTITION_INCLUDED",
        "NO_PARTITION_INCLUDED"
      ],
      "alignment": [
        "BLOCKED"
      ],
      "effect": [
        "BLOCKING_DEFECT"
      ]
    }
  },
  "global_state_reducer": {
    "reducer_id": "pm_research.s2.global_state_reducer.v3",
    "vector_schema": "GlobalStateVector",
    "phase_order": [
      "ARCHITECTURE_REVIEW",
      "SPEC_DRAFTING",
      "SPEC_REVIEW",
      "IMPLEMENTATION_SOURCE",
      "SOURCE_REVIEW",
      "TEST_AUTHORING",
      "TEST_REVIEW",
      "TEST_EXECUTION",
      "TEST_RESULT_REVIEW",
      "S4_PREPARATION",
      "S4_REVIEW",
      "S5_PREFLIGHT",
      "SPAN_REVIEW",
      "S6_ACQUISITION",
      "S6_REVIEW",
      "S7_CONSTRUCTION",
      "S7_REVIEW",
      "ALIGNMENT_POLICY_REVIEW",
      "S8A_ALIGNMENT",
      "S8A_REVIEW",
      "S8B_REBUILD",
      "S8B_REVIEW",
      "S8C_AUDIT",
      "S9_RESULT_REVIEW",
      "S10_TRANSITION",
      "S10_REVIEW",
      "COMPLETE",
      "HALTED"
    ],
    "phase_contracts": {
      "ARCHITECTURE_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K002",
          "A000"
        ],
        "handoff_refs": [],
        "review_refs": [
          "A001"
        ],
        "accepted_refs": [
          "A002"
        ],
        "successor_activity": "SPEC_DRAFTING"
      },
      "SPEC_DRAFTING": {
        "kind": "ACTIVITY",
        "root_ref": "K007",
        "completion_refs": [
          "K008",
          "K009"
        ],
        "successor_review": "SPEC_REVIEW"
      },
      "SPEC_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K008",
          "K009"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K010"
        ],
        "accepted_refs": [
          "K011"
        ],
        "successor_activity": "IMPLEMENTATION_SOURCE"
      },
      "IMPLEMENTATION_SOURCE": {
        "kind": "ACTIVITY",
        "root_ref": "K014",
        "completion_refs": [
          "K015",
          "K016"
        ],
        "successor_review": "SOURCE_REVIEW"
      },
      "SOURCE_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K015",
          "K016"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K017"
        ],
        "accepted_refs": [
          "K018"
        ],
        "successor_activity": "TEST_AUTHORING"
      },
      "TEST_AUTHORING": {
        "kind": "ACTIVITY",
        "root_ref": "K021",
        "completion_refs": [
          "K022",
          "K023"
        ],
        "successor_review": "TEST_REVIEW"
      },
      "TEST_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K022",
          "K023"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K024"
        ],
        "accepted_refs": [
          "K025"
        ],
        "successor_activity": "TEST_EXECUTION"
      },
      "TEST_EXECUTION": {
        "kind": "ACTIVITY",
        "root_ref": "K028",
        "completion_refs": [
          "K029",
          "K030"
        ],
        "successor_review": "TEST_RESULT_REVIEW"
      },
      "TEST_RESULT_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K029",
          "K030"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K031"
        ],
        "accepted_refs": [
          "K032"
        ],
        "successor_activity": "S4_PREPARATION"
      },
      "S4_PREPARATION": {
        "kind": "ACTIVITY",
        "root_ref": "K035",
        "completion_refs": [
          "K036",
          "K037",
          "A003",
          "A004",
          "K038",
          "K039"
        ],
        "successor_review": "S4_REVIEW"
      },
      "S4_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K038",
          "K039"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K040"
        ],
        "accepted_refs": [
          "K041"
        ],
        "successor_activity": "S5_PREFLIGHT"
      },
      "S5_PREFLIGHT": {
        "kind": "ACTIVITY",
        "root_ref": "K044",
        "completion_refs": [
          "K045",
          "K046",
          "K047",
          "K048"
        ],
        "successor_review": "SPAN_REVIEW"
      },
      "SPAN_REVIEW": {
        "kind": "BRANCH_REVIEW",
        "submission_refs": [
          "K049",
          "K048"
        ],
        "positive_review_refs": [
          "K050"
        ],
        "positive_accepted_refs": [
          "K051",
          "K052P"
        ],
        "negative_completion_refs": [
          "K052N"
        ],
        "successor_activity": "S6_ACQUISITION"
      },
      "S6_ACQUISITION": {
        "kind": "ACTIVITY",
        "root_ref": "K055",
        "completion_refs": [
          "K056F",
          "K057",
          "A005",
          "A006",
          "K058F",
          "K059F",
          "K060",
          "K061",
          "K062",
          "K063",
          "A007",
          "A008",
          "K064",
          "K065"
        ],
        "successor_review": "S6_REVIEW"
      },
      "S6_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K064",
          "K065"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K066"
        ],
        "accepted_refs": [
          "K067"
        ],
        "successor_activity": "S7_CONSTRUCTION"
      },
      "S7_CONSTRUCTION": {
        "kind": "ACTIVITY",
        "root_ref": "K071",
        "completion_refs": [
          "K072",
          "K073F",
          "K074",
          "K075",
          "K076",
          "K077"
        ],
        "successor_review": "S7_REVIEW"
      },
      "S7_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K075",
          "K077"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K078"
        ],
        "accepted_refs": [
          "K079"
        ],
        "successor_activity": "ALIGNMENT_POLICY_REVIEW"
      },
      "ALIGNMENT_POLICY_REVIEW": {
        "kind": "DUAL_BRANCH_REVIEW",
        "present_submission_refs": [
          "K080P"
        ],
        "present_review_refs": [
          "K081P"
        ],
        "present_accepted_refs": [
          "K082",
          "K083P"
        ],
        "present_negative_refs": [
          "K083R"
        ],
        "absent_submission_refs": [
          "K080A"
        ],
        "absent_review_refs": [
          "K081A"
        ],
        "absent_completion_refs": [
          "K083A"
        ],
        "successor_activity": "S8A_ALIGNMENT"
      },
      "S8A_ALIGNMENT": {
        "kind": "ACTIVITY",
        "root_ref": "K086",
        "completion_refs": [
          "K087",
          "K088",
          "K089"
        ],
        "successor_review": "S8A_REVIEW"
      },
      "S8A_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K088",
          "K089"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K090"
        ],
        "accepted_refs": [
          "K091"
        ],
        "successor_activity": "S8B_REBUILD"
      },
      "S8B_REBUILD": {
        "kind": "ACTIVITY",
        "root_ref": "K094",
        "completion_refs": [
          "K095",
          "K096F",
          "K097",
          "K098",
          "K099",
          "K100",
          "K101",
          "K102"
        ],
        "successor_review": "S8B_REVIEW"
      },
      "S8B_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K101",
          "K102"
        ],
        "handoff_refs": [],
        "review_refs": [
          "K103"
        ],
        "accepted_refs": [
          "K104"
        ],
        "successor_activity": "S8C_AUDIT"
      },
      "S8C_AUDIT": {
        "kind": "ACTIVITY",
        "root_ref": "K107",
        "completion_refs": [
          "K108",
          "K109",
          "K110",
          "K111",
          "K112",
          "K113",
          "K114",
          "K115",
          "K116",
          "K117",
          "K118",
          "K119",
          "K120",
          "K121",
          "K122",
          "K123",
          "K124",
          "K125",
          "K126",
          "K127",
          "K128",
          "K129",
          "K130",
          "K131",
          "A009",
          "K132"
        ],
        "successor_review": "S9_RESULT_REVIEW"
      },
      "S9_RESULT_REVIEW": {
        "kind": "REVIEW",
        "submission_refs": [
          "K132",
          "K133"
        ],
        "handoff_refs": [
          "K136"
        ],
        "review_refs": [
          "K134"
        ],
        "reconciliation_refs": [
          "K135"
        ],
        "accepted_refs": [
          "K137"
        ],
        "successor_activity": "S10_TRANSITION"
      },
      "S10_TRANSITION": {
        "kind": "BRANCH_ACTIVITY",
        "root_ref": "K140",
        "common_refs": [
          "K141"
        ],
        "ineligible_completion_refs": [
          "K142I",
          "K143I"
        ],
        "eligible_completion_refs": [
          "K142E",
          "K143E",
          "K144E"
        ],
        "successor_review": "S10_REVIEW"
      },
      "S10_REVIEW": {
        "kind": "BRANCH_REVIEW",
        "ineligible_submission_refs": [
          "K143I"
        ],
        "ineligible_accepted_refs": [
          "K144I"
        ],
        "eligible_submission_refs": [
          "K144E"
        ],
        "eligible_review_refs": [
          "K145E"
        ],
        "eligible_accepted_refs": [
          "K146E"
        ],
        "successor_activity": "COMPLETE"
      },
      "COMPLETE": {
        "kind": "TERMINAL"
      },
      "HALTED": {
        "kind": "TERMINAL"
      }
    },
    "snapshot_schema": {
      "valid_node_ids": "unique Array<NodeId>",
      "invalid_evidence": "Array<GlobalDefect>",
      "final_review_dispositions": "map GlobalPhase to ReviewDisposition",
      "branch_selection": "Enum[NONE,POSITIVE,NEGATIVE,CANDIDATE_PRESENT,CANDIDATE_ABSENT,ELIGIBLE,INELIGIBLE]",
      "finalization_claimed_phases": "unique Array<GlobalPhase>"
    },
    "predicate_dsl": {
      "all_valid": "all named node IDs exist and validate",
      "all_absent": "none named node IDs exists",
      "not_all_valid": "at least one named node is absent or incomplete",
      "latest_reached_phase_eq": "compute highest phase_order ordinal with valid phase entry evidence; require exact equality",
      "review_disposition": "exact final disposition from named phase review record",
      "branch_eq": "exact branch enum",
      "no_defects": "invalid_evidence is empty",
      "selected_defect": "deterministic minimum by phase ordinal then UTF-8 lexical stop_code"
    },
    "ordered_precedence": [
      "defect_halt_rows",
      "terminal_complete_rows",
      "review_halt_rows",
      "normal_state_rows"
    ],
    "defect_halt_rows": [
      {
        "state_id": "G_HALT_DEFECT_STOP_AUTHORIZATION_ORDER_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_AUTHORIZATION_ORDER_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_AUTHORIZATION_ORDER_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_AUTHORIZATION_PROVENANCE_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_AUTHORIZATION_PROVENANCE_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_AUTHORIZATION_PROVENANCE_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_AUTHORIZATION_PREREQUISITE_BYTES_MISSING",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "AUTHORIZATION_PREREQUISITE_BYTES_MISSING",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "AUTHORIZATION_PREREQUISITE_BYTES_MISSING"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_AUTHORIZATION_SCOPE_EXPANSION",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "AUTHORIZATION_SCOPE_EXPANSION",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "AUTHORIZATION_SCOPE_EXPANSION"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_GLOBAL_STATE_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "GLOBAL_STATE_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "GLOBAL_STATE_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_CONDITION_STATE_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "CONDITION_STATE_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "CONDITION_STATE_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_CANONICAL_BASE_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_CANONICAL_BASE_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_CANONICAL_BASE_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_P0_NOT_CLEAR",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_P0_NOT_CLEAR",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_P0_NOT_CLEAR"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_STALE_CONTRACT",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_STALE_CONTRACT",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_STALE_CONTRACT"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_INPUT_IDENTITY_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_INPUT_IDENTITY_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_INPUT_IDENTITY_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_UNIVERSE_RECONCILIATION_FAILED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_UNIVERSE_RECONCILIATION_FAILED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_UNIVERSE_RECONCILIATION_FAILED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_RESOLUTION_BOUNDARY_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_RESOLUTION_BOUNDARY_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_RESOLUTION_BOUNDARY_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_TRADE_ANCHOR_MISSING",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_TRADE_ANCHOR_MISSING",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_TRADE_ANCHOR_MISSING"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_TOKEN_ENUMERATION_UNRELIABLE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_TOKEN_ENUMERATION_UNRELIABLE",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_TOKEN_ENUMERATION_UNRELIABLE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_PRECISION_LOSS",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_PRECISION_LOSS",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_PRECISION_LOSS"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_PREFLIGHT_INTEGRITY_FAILURE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "PREFLIGHT_INTEGRITY_FAILURE",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "PREFLIGHT_INTEGRITY_FAILURE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_PREFLIGHT_INCOMPLETE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "PREFLIGHT_INCOMPLETE",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "PREFLIGHT_INCOMPLETE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_NO_SAFE_SPAN",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "NO_SAFE_SPAN",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "NO_SAFE_SPAN"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_NO_SAFE_SPAN_AFTER_MARGIN",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "NO_SAFE_SPAN_AFTER_MARGIN",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "NO_SAFE_SPAN_AFTER_MARGIN"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_REQUEST_PLAN_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_REQUEST_PLAN_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_REQUEST_PLAN_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_REQUEST_TERMINALS_INCOMPLETE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_REQUEST_TERMINALS_INCOMPLETE",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_REQUEST_TERMINALS_INCOMPLETE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_RAW_ARCHIVE_INCOMPLETE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_RAW_ARCHIVE_INCOMPLETE",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_RAW_ARCHIVE_INCOMPLETE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_RAW_ARCHIVE_IDENTITY_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_RAW_ARCHIVE_IDENTITY_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_RAW_ARCHIVE_IDENTITY_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_ENDPOINT_SHAPE_UNRECOGNIZED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_ENDPOINT_SHAPE_UNRECOGNIZED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_ENDPOINT_SHAPE_UNRECOGNIZED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_FORBIDDEN_SYNTHESIS",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_FORBIDDEN_SYNTHESIS",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_FORBIDDEN_SYNTHESIS"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_DUPLICATE_PRICE_CONFLICT",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "DUPLICATE_PRICE_CONFLICT",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "DUPLICATE_PRICE_CONFLICT"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_SCIENTIFIC_PROJECTION_CONFLICT",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "SCIENTIFIC_PROJECTION_CONFLICT",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "SCIENTIFIC_PROJECTION_CONFLICT"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_SCIENTIFIC_RAW_PROJECTION_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "SCIENTIFIC_RAW_PROJECTION_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "SCIENTIFIC_RAW_PROJECTION_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "ROW_KEY_ACTIVITY_PROVENANCE_FORBIDDEN"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_DETERMINISTIC_BUILD_ID_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_DETERMINISTIC_BUILD_ID_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_DETERMINISTIC_BUILD_ID_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_REBUILD_SOURCE_ISOLATION_VIOLATION",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_REBUILD_SOURCE_ISOLATION_VIOLATION",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_REBUILD_SOURCE_ISOLATION_VIOLATION"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_REBUILD_BYTE_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_REBUILD_BYTE_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_REBUILD_BYTE_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_ALIGNMENT_POLICY_ABSENT",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_ALIGNMENT_POLICY_ABSENT",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_ALIGNMENT_POLICY_ABSENT"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_ALIGNMENT_POLICY_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_ALIGNMENT_POLICY_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_ALIGNMENT_POLICY_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_ALIGNMENT_INCOMPLETE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_ALIGNMENT_INCOMPLETE",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_ALIGNMENT_INCOMPLETE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_PROVENANCE_EDGE_SET_MISMATCH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "PROVENANCE_EDGE_SET_MISMATCH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "PROVENANCE_EDGE_SET_MISMATCH"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_AUDIT_SELF_REFERENCE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_AUDIT_SELF_REFERENCE",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_AUDIT_SELF_REFERENCE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_GATE_RECONCILIATION_FAILED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_GATE_RECONCILIATION_FAILED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_GATE_RECONCILIATION_FAILED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_S9_NOT_APPROVED_CLEAR",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_S9_NOT_APPROVED_CLEAR",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_S9_NOT_APPROVED_CLEAR"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_TRANSITION_RECONCILIATION_FAILED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_TRANSITION_RECONCILIATION_FAILED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_TRANSITION_RECONCILIATION_FAILED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_CANDIDATE_SEAL_PREMATURE",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_CANDIDATE_SEAL_PREMATURE",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_CANDIDATE_SEAL_PREMATURE"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_P1_NOT_SEPARATELY_AUTHORIZED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_P1_NOT_SEPARATELY_AUTHORIZED",
            "severity_equals": "INCOMPLETE_EVIDENCE"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_P1_NOT_SEPARATELY_AUTHORIZED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_ARCHITECTURE_CONTROL_SET_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "ARCHITECTURE_CONTROL_SET_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "ARCHITECTURE_CONTROL_SET_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_DUPLICATE_IDENTITY_CONFLICT",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_DUPLICATE_IDENTITY_CONFLICT",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_DUPLICATE_IDENTITY_CONFLICT"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_RESOURCE_BOUND_EXCEEDED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_RESOURCE_BOUND_EXCEEDED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_RESOURCE_BOUND_EXCEEDED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_RESUME_PROVENANCE_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_RESUME_PROVENANCE_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_RESUME_PROVENANCE_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_RETRY_AFTER_UNIT_INVALID",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_RETRY_AFTER_UNIT_INVALID",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_RETRY_AFTER_UNIT_INVALID"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_ZERO_POPULATION_NOT_PERMITTED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_ZERO_POPULATION_NOT_PERMITTED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_ZERO_POPULATION_NOT_PERMITTED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED"
        }
      },
      {
        "state_id": "G_HALT_DEFECT_STOP_UNEXPECTED_DELIVERABLE_PATH",
        "when": {
          "selected_defect": {
            "selection": "minimum phase_order ordinal, then UTF-8 lexical stop_code",
            "stop_code_equals": "STOP_UNEXPECTED_DELIVERABLE_PATH",
            "severity_equals": "BLOCKING_DEFECT"
          }
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": "STOP_UNEXPECTED_DELIVERABLE_PATH"
        }
      }
    ],
    "terminal_complete_rows": [
      {
        "state_id": "G_COMPLETE_ELIGIBLE",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K146E"
          ],
          "eligible_branch_only": true
        },
        "vector": {
          "phase": "COMPLETE",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_COMPLETE_INELIGIBLE",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K144I"
          ],
          "ineligible_branch_only": true
        },
        "vector": {
          "phase": "COMPLETE",
          "phase_status": "COMPLETE",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": null
        }
      }
    ],
    "review_halt_rows": [
      {
        "state_id": "G_HALT_ARCHITECTURE_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ARCHITECTURE_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_ARCHITECTURE_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_ARCHITECTURE_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ARCHITECTURE_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_ARCHITECTURE_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_ARCHITECTURE_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ARCHITECTURE_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_ARCHITECTURE_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_ARCHITECTURE_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ARCHITECTURE_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_ARCHITECTURE_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_SPEC_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPEC_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_SPEC_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_SPEC_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPEC_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_SPEC_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_SPEC_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPEC_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_SPEC_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_SPEC_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPEC_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_SPEC_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_SOURCE_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SOURCE_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_SOURCE_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_SOURCE_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SOURCE_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_SOURCE_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_SOURCE_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SOURCE_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_SOURCE_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_SOURCE_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SOURCE_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_SOURCE_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_TEST_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_TEST_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_TEST_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_TEST_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_TEST_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_TEST_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_TEST_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_TEST_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_TEST_RESULT_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_RESULT_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_TEST_RESULT_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_TEST_RESULT_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_RESULT_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_TEST_RESULT_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_TEST_RESULT_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_RESULT_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_TEST_RESULT_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_TEST_RESULT_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "TEST_RESULT_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_TEST_RESULT_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S4_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S4_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S4_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S4_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S4_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S4_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S4_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S4_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S4_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S4_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S4_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S4_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_SPAN_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPAN_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_SPAN_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_SPAN_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPAN_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_SPAN_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_SPAN_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPAN_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_SPAN_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_SPAN_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "SPAN_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_SPAN_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S6_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S6_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S6_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S6_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S6_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S6_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S6_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S6_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S6_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S6_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S6_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S6_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S7_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S7_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S7_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S7_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S7_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S7_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S7_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S7_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S7_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S7_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S7_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S7_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_ALIGNMENT_POLICY_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ALIGNMENT_POLICY_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_ALIGNMENT_POLICY_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_ALIGNMENT_POLICY_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ALIGNMENT_POLICY_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_ALIGNMENT_POLICY_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_ALIGNMENT_POLICY_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ALIGNMENT_POLICY_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_ALIGNMENT_POLICY_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_ALIGNMENT_POLICY_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "ALIGNMENT_POLICY_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_ALIGNMENT_POLICY_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S8A_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8A_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S8A_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S8A_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8A_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S8A_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S8A_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8A_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S8A_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S8A_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8A_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S8A_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S8B_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8B_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S8B_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S8B_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8B_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S8B_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S8B_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8B_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S8B_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S8B_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S8B_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S8B_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S9_RESULT_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S9_RESULT_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S9_RESULT_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S9_RESULT_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S9_RESULT_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S9_RESULT_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S9_RESULT_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S9_RESULT_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S9_RESULT_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S9_RESULT_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S9_RESULT_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S9_RESULT_REVIEW_NEEDS_VERIFICATION"
        }
      },
      {
        "state_id": "G_HALT_S10_REVIEW_ACCEPT_FINDING",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S10_REVIEW",
            "equals": "ACCEPT_FINDING"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "ACCEPT_FINDING",
          "halt_code": "STOP_S10_REVIEW_ACCEPTED_FINDING_NO_PROGRESSION"
        }
      },
      {
        "state_id": "G_HALT_S10_REVIEW_BLOCK",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S10_REVIEW",
            "equals": "BLOCK"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "BLOCKED",
          "review_disposition": "BLOCK",
          "halt_code": "STOP_S10_REVIEW_BLOCKED_BY_SENTINEL"
        }
      },
      {
        "state_id": "G_HALT_S10_REVIEW_DEFER",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S10_REVIEW",
            "equals": "DEFER"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "DEFER",
          "halt_code": "STOP_S10_REVIEW_DEFERRED"
        }
      },
      {
        "state_id": "G_HALT_S10_REVIEW_NEEDS_VERIFICATION",
        "when": {
          "no_identity_or_schema_defect": true,
          "review_disposition": {
            "phase": "S10_REVIEW",
            "equals": "NEEDS_VERIFICATION"
          },
          "terminal_exception_absent": true
        },
        "vector": {
          "phase": "HALTED",
          "phase_status": "INCOMPLETE",
          "review_disposition": "NEEDS_VERIFICATION",
          "halt_code": "STOP_S10_REVIEW_NEEDS_VERIFICATION"
        }
      }
    ],
    "normal_state_rows": [
      {
        "state_id": "G_INITIAL_ARCHITECTURE_NOT_STARTED",
        "when": {
          "no_defects": true,
          "all_absent": [
            "A001",
            "A002"
          ],
          "latest_reached_phase_eq": "ARCHITECTURE_REVIEW",
          "architecture_submission_complete": false
        },
        "vector": {
          "phase": "ARCHITECTURE_REVIEW",
          "phase_status": "NOT_STARTED",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_ARCHITECTURE_REVIEW_PENDING",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K002",
            "A000"
          ],
          "all_absent": [
            "A001",
            "A002"
          ],
          "latest_reached_phase_eq": "ARCHITECTURE_REVIEW",
          "architecture_submission_complete": true
        },
        "vector": {
          "phase": "ARCHITECTURE_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SPEC_DRAFTING_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K007"
          ],
          "not_all_valid": [
            "K008",
            "K009"
          ],
          "latest_reached_phase_eq": "SPEC_DRAFTING"
        },
        "vector": {
          "phase": "SPEC_DRAFTING",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SPEC_REVIEW_PENDING_AFTER_SPEC_DRAFTING",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K007",
            "K008",
            "K009"
          ],
          "review_record_absent_for_phase": "SPEC_REVIEW",
          "latest_reached_phase_eq": "SPEC_REVIEW"
        },
        "vector": {
          "phase": "SPEC_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_IMPLEMENTATION_SOURCE_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K014"
          ],
          "not_all_valid": [
            "K015",
            "K016"
          ],
          "latest_reached_phase_eq": "IMPLEMENTATION_SOURCE"
        },
        "vector": {
          "phase": "IMPLEMENTATION_SOURCE",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SOURCE_REVIEW_PENDING_AFTER_IMPLEMENTATION_SOURCE",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K014",
            "K015",
            "K016"
          ],
          "review_record_absent_for_phase": "SOURCE_REVIEW",
          "latest_reached_phase_eq": "SOURCE_REVIEW"
        },
        "vector": {
          "phase": "SOURCE_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_TEST_AUTHORING_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K021"
          ],
          "not_all_valid": [
            "K022",
            "K023"
          ],
          "latest_reached_phase_eq": "TEST_AUTHORING"
        },
        "vector": {
          "phase": "TEST_AUTHORING",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_TEST_REVIEW_PENDING_AFTER_TEST_AUTHORING",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K021",
            "K022",
            "K023"
          ],
          "review_record_absent_for_phase": "TEST_REVIEW",
          "latest_reached_phase_eq": "TEST_REVIEW"
        },
        "vector": {
          "phase": "TEST_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_TEST_EXECUTION_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K028"
          ],
          "not_all_valid": [
            "K029",
            "K030"
          ],
          "latest_reached_phase_eq": "TEST_EXECUTION"
        },
        "vector": {
          "phase": "TEST_EXECUTION",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_TEST_RESULT_REVIEW_PENDING_AFTER_TEST_EXECUTION",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K028",
            "K029",
            "K030"
          ],
          "review_record_absent_for_phase": "TEST_RESULT_REVIEW",
          "latest_reached_phase_eq": "TEST_RESULT_REVIEW"
        },
        "vector": {
          "phase": "TEST_RESULT_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S4_PREPARATION_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K035"
          ],
          "not_all_valid": [
            "K036",
            "K037",
            "A003",
            "A004",
            "K038",
            "K039"
          ],
          "latest_reached_phase_eq": "S4_PREPARATION"
        },
        "vector": {
          "phase": "S4_PREPARATION",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S4_REVIEW_PENDING_AFTER_S4_PREPARATION",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K035",
            "K036",
            "K037",
            "A003",
            "A004",
            "K038",
            "K039"
          ],
          "review_record_absent_for_phase": "S4_REVIEW",
          "latest_reached_phase_eq": "S4_REVIEW"
        },
        "vector": {
          "phase": "S4_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S5_PREFLIGHT_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K044"
          ],
          "not_all_valid": [
            "K045",
            "K046",
            "K047",
            "K048"
          ],
          "latest_reached_phase_eq": "S5_PREFLIGHT"
        },
        "vector": {
          "phase": "S5_PREFLIGHT",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SPAN_REVIEW_PENDING_AFTER_S5_PREFLIGHT",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K044",
            "K045",
            "K046",
            "K047",
            "K048"
          ],
          "review_record_absent_for_phase": "SPAN_REVIEW",
          "latest_reached_phase_eq": "SPAN_REVIEW"
        },
        "vector": {
          "phase": "SPAN_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S6_ACQUISITION_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K055"
          ],
          "not_all_valid": [
            "K056F",
            "K057",
            "A005",
            "A006",
            "K058F",
            "K059F",
            "K060",
            "K061",
            "K062",
            "K063",
            "A007",
            "A008",
            "K064",
            "K065"
          ],
          "latest_reached_phase_eq": "S6_ACQUISITION"
        },
        "vector": {
          "phase": "S6_ACQUISITION",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S6_REVIEW_PENDING_AFTER_S6_ACQUISITION",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K055",
            "K056F",
            "K057",
            "A005",
            "A006",
            "K058F",
            "K059F",
            "K060",
            "K061",
            "K062",
            "K063",
            "A007",
            "A008",
            "K064",
            "K065"
          ],
          "review_record_absent_for_phase": "S6_REVIEW",
          "latest_reached_phase_eq": "S6_REVIEW"
        },
        "vector": {
          "phase": "S6_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S7_CONSTRUCTION_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K071"
          ],
          "not_all_valid": [
            "K072",
            "K073F",
            "K074",
            "K075",
            "K076",
            "K077"
          ],
          "latest_reached_phase_eq": "S7_CONSTRUCTION"
        },
        "vector": {
          "phase": "S7_CONSTRUCTION",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S7_REVIEW_PENDING_AFTER_S7_CONSTRUCTION",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K071",
            "K072",
            "K073F",
            "K074",
            "K075",
            "K076",
            "K077"
          ],
          "review_record_absent_for_phase": "S7_REVIEW",
          "latest_reached_phase_eq": "S7_REVIEW"
        },
        "vector": {
          "phase": "S7_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8A_ALIGNMENT_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K086"
          ],
          "not_all_valid": [
            "K087",
            "K088",
            "K089"
          ],
          "latest_reached_phase_eq": "S8A_ALIGNMENT"
        },
        "vector": {
          "phase": "S8A_ALIGNMENT",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8A_REVIEW_PENDING_AFTER_S8A_ALIGNMENT",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K086",
            "K087",
            "K088",
            "K089"
          ],
          "review_record_absent_for_phase": "S8A_REVIEW",
          "latest_reached_phase_eq": "S8A_REVIEW"
        },
        "vector": {
          "phase": "S8A_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8B_REBUILD_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K094"
          ],
          "not_all_valid": [
            "K095",
            "K096F",
            "K097",
            "K098",
            "K099",
            "K100",
            "K101",
            "K102"
          ],
          "latest_reached_phase_eq": "S8B_REBUILD"
        },
        "vector": {
          "phase": "S8B_REBUILD",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8B_REVIEW_PENDING_AFTER_S8B_REBUILD",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K094",
            "K095",
            "K096F",
            "K097",
            "K098",
            "K099",
            "K100",
            "K101",
            "K102"
          ],
          "review_record_absent_for_phase": "S8B_REVIEW",
          "latest_reached_phase_eq": "S8B_REVIEW"
        },
        "vector": {
          "phase": "S8B_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8C_AUDIT_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K107"
          ],
          "not_all_valid": [
            "K108",
            "K109",
            "K110",
            "K111",
            "K112",
            "K113",
            "K114",
            "K115",
            "K116",
            "K117",
            "K118",
            "K119",
            "K120",
            "K121",
            "K122",
            "K123",
            "K124",
            "K125",
            "K126",
            "K127",
            "K128",
            "K129",
            "K130",
            "K131",
            "A009",
            "K132"
          ],
          "latest_reached_phase_eq": "S8C_AUDIT"
        },
        "vector": {
          "phase": "S8C_AUDIT",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S9_RESULT_REVIEW_PENDING_AFTER_S8C_AUDIT",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K107",
            "K108",
            "K109",
            "K110",
            "K111",
            "K112",
            "K113",
            "K114",
            "K115",
            "K116",
            "K117",
            "K118",
            "K119",
            "K120",
            "K121",
            "K122",
            "K123",
            "K124",
            "K125",
            "K126",
            "K127",
            "K128",
            "K129",
            "K130",
            "K131",
            "A009",
            "K132"
          ],
          "review_record_absent_for_phase": "S9_RESULT_REVIEW",
          "latest_reached_phase_eq": "S9_RESULT_REVIEW"
        },
        "vector": {
          "phase": "S9_RESULT_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S10_TRANSITION_INELIGIBLE_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K140",
            "K141"
          ],
          "branch_eq": "INELIGIBLE",
          "not_all_valid": [
            "K142I",
            "K143I"
          ],
          "opposite_branch_absent": true,
          "latest_reached_phase_eq": "S10_TRANSITION"
        },
        "vector": {
          "phase": "S10_TRANSITION",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S10_REVIEW_INELIGIBLE_PENDING",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K140",
            "K141",
            "K142I",
            "K143I"
          ],
          "branch_eq": "INELIGIBLE",
          "opposite_branch_absent": true,
          "review_record_absent_for_phase": "S10_REVIEW",
          "latest_reached_phase_eq": "S10_REVIEW"
        },
        "vector": {
          "phase": "S10_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S10_TRANSITION_ELIGIBLE_IN_PROGRESS",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K140",
            "K141"
          ],
          "branch_eq": "ELIGIBLE",
          "not_all_valid": [
            "K142E",
            "K143E",
            "K144E"
          ],
          "opposite_branch_absent": true,
          "latest_reached_phase_eq": "S10_TRANSITION"
        },
        "vector": {
          "phase": "S10_TRANSITION",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "NOT_APPLICABLE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S10_REVIEW_ELIGIBLE_PENDING",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K140",
            "K141",
            "K142E",
            "K143E",
            "K144E"
          ],
          "branch_eq": "ELIGIBLE",
          "opposite_branch_absent": true,
          "review_record_absent_for_phase": "S10_REVIEW",
          "latest_reached_phase_eq": "S10_REVIEW"
        },
        "vector": {
          "phase": "S10_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_ARCHITECTURE_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "ARCHITECTURE_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "A001",
            "A002"
          ],
          "latest_reached_phase_eq": "ARCHITECTURE_REVIEW",
          "all_absent": [
            "K007"
          ]
        },
        "vector": {
          "phase": "ARCHITECTURE_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SPEC_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "SPEC_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K010",
            "K011"
          ],
          "latest_reached_phase_eq": "SPEC_REVIEW",
          "all_absent": [
            "K014"
          ]
        },
        "vector": {
          "phase": "SPEC_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SOURCE_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "SOURCE_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K017",
            "K018"
          ],
          "latest_reached_phase_eq": "SOURCE_REVIEW",
          "all_absent": [
            "K021"
          ]
        },
        "vector": {
          "phase": "SOURCE_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_TEST_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "TEST_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K024",
            "K025"
          ],
          "latest_reached_phase_eq": "TEST_REVIEW",
          "all_absent": [
            "K028"
          ]
        },
        "vector": {
          "phase": "TEST_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_TEST_RESULT_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "TEST_RESULT_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K031",
            "K032"
          ],
          "latest_reached_phase_eq": "TEST_RESULT_REVIEW",
          "all_absent": [
            "K035"
          ]
        },
        "vector": {
          "phase": "TEST_RESULT_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S4_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "S4_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K040",
            "K041"
          ],
          "latest_reached_phase_eq": "S4_REVIEW",
          "all_absent": [
            "K044"
          ]
        },
        "vector": {
          "phase": "S4_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SPAN_REVIEW_APPROVED_WAITING_S6_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "SPAN_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K050",
            "K051",
            "K052P"
          ],
          "all_absent": [
            "K055"
          ],
          "latest_reached_phase_eq": "SPAN_REVIEW"
        },
        "vector": {
          "phase": "SPAN_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S6_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "S6_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K066",
            "K067"
          ],
          "latest_reached_phase_eq": "S6_REVIEW",
          "all_absent": [
            "K071"
          ]
        },
        "vector": {
          "phase": "S6_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S7_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "S7_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K078",
            "K079"
          ],
          "latest_reached_phase_eq": "S7_REVIEW"
        },
        "vector": {
          "phase": "S7_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_ALIGNMENT_POLICY_PRESENT_PENDING",
        "when": {
          "no_defects": true,
          "branch_eq": "CANDIDATE_PRESENT",
          "all_valid": [
            "K080P"
          ],
          "all_absent": [
            "K081P",
            "K082",
            "K083P",
            "K083R"
          ],
          "latest_reached_phase_eq": "ALIGNMENT_POLICY_REVIEW"
        },
        "vector": {
          "phase": "ALIGNMENT_POLICY_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_ALIGNMENT_POLICY_PRESENT_APPROVED_WAITING_S8A_ROOT",
        "when": {
          "no_defects": true,
          "branch_eq": "CANDIDATE_PRESENT",
          "review_disposition": {
            "phase": "ALIGNMENT_POLICY_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K081P",
            "K082",
            "K083P"
          ],
          "all_absent": [
            "K086"
          ],
          "latest_reached_phase_eq": "ALIGNMENT_POLICY_REVIEW"
        },
        "vector": {
          "phase": "ALIGNMENT_POLICY_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_ALIGNMENT_POLICY_ABSENCE_PENDING",
        "when": {
          "no_defects": true,
          "branch_eq": "CANDIDATE_ABSENT",
          "all_valid": [
            "K080A"
          ],
          "all_absent": [
            "K081A",
            "K083A"
          ],
          "latest_reached_phase_eq": "ALIGNMENT_POLICY_REVIEW"
        },
        "vector": {
          "phase": "ALIGNMENT_POLICY_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8A_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "S8A_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K090",
            "K091"
          ],
          "latest_reached_phase_eq": "S8A_REVIEW",
          "all_absent": [
            "K094"
          ]
        },
        "vector": {
          "phase": "S8A_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S8B_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "S8B_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K103",
            "K104"
          ],
          "latest_reached_phase_eq": "S8B_REVIEW",
          "all_absent": [
            "K107"
          ]
        },
        "vector": {
          "phase": "S8B_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_S9_RESULT_REVIEW_APPROVED_WAITING_SUCCESSOR_ROOT",
        "when": {
          "no_defects": true,
          "review_disposition": {
            "phase": "S9_RESULT_REVIEW",
            "equals": "APPROVE"
          },
          "all_valid": [
            "K134",
            "K137"
          ],
          "latest_reached_phase_eq": "S9_RESULT_REVIEW",
          "all_absent": [
            "K140"
          ]
        },
        "vector": {
          "phase": "S9_RESULT_REVIEW",
          "phase_status": "COMPLETE",
          "review_disposition": "APPROVE",
          "halt_code": null
        }
      },
      {
        "state_id": "G_SPAN_REVIEW_AWAITING_POLICY_CANDIDATE",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K045",
            "K046",
            "K047",
            "K048"
          ],
          "all_absent": [
            "K049",
            "K050",
            "K051",
            "K052P",
            "K052N"
          ],
          "latest_reached_phase_eq": "SPAN_REVIEW"
        },
        "vector": {
          "phase": "SPAN_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      },
      {
        "state_id": "G_ALIGNMENT_POLICY_REVIEW_AWAITING_SUBMISSION",
        "when": {
          "no_defects": true,
          "all_valid": [
            "K079"
          ],
          "all_absent": [
            "K080P",
            "K080A",
            "K081P",
            "K081A",
            "K082",
            "K083P",
            "K083R",
            "K083A"
          ],
          "latest_reached_phase_eq": "ALIGNMENT_POLICY_REVIEW"
        },
        "vector": {
          "phase": "ALIGNMENT_POLICY_REVIEW",
          "phase_status": "IN_PROGRESS",
          "review_disposition": "PENDING",
          "halt_code": null
        }
      }
    ],
    "totality_rule": "evaluate rows in ordered_precedence; exactly one row MUST match every prefix-closed branch-valid snapshot; zero or multiple matches is GLOBAL_STATE_INVALID",
    "disjointness_proof": [
      "defect rows require selected_defect and dominate all other rows",
      "terminal rows require exact mutually exclusive K146E or K144I accepted branch",
      "review halt rows require one exact non-progressing disposition and terminal_exception_absent",
      "normal rows require no_defects and one exact latest_reached_phase",
      "within one phase, present/absent, all_valid/not_all_valid, branch, and disposition predicates are complementary",
      "static enumeration of every prefix-closed phase/branch snapshot MUST yield duplicate_match_count=0 and unmapped_snapshot_count=0"
    ],
    "exact_clear_reachability_witness": {
      "required_valid_nodes": [
        "A009",
        "K129",
        "K131",
        "K132",
        "K133",
        "K134",
        "K135",
        "K136",
        "K137",
        "K140",
        "K141",
        "K142E",
        "K143E",
        "K144E",
        "K145E",
        "K146E"
      ],
      "required_values": {
        "K129.gate_state": "S2_GATE_CLEAR",
        "K134.review_disposition": "APPROVE",
        "K137.status": "APPROVED_CLEAR",
        "K141.branch": "ELIGIBLE",
        "K145E.review_disposition": "APPROVE"
      },
      "forbidden_nodes": [
        "K142I",
        "K143I",
        "K144I"
      ],
      "output_vector": {
        "phase": "COMPLETE",
        "phase_status": "COMPLETE",
        "review_disposition": "APPROVE",
        "halt_code": null
      }
    }
  },
  "nodes": {
    "K000": {
      "rank": 1000,
      "semantic_role": "canonical_git_commit",
      "artifact_profile_id": "virtual_commit.v1",
      "ref_bindings": [],
      "derived_direct_predecessors": [],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {},
        "exact_direct_predecessor_count": 0
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K001": {
      "rank": 1010,
      "semantic_role": "canonical_input_manifest",
      "artifact_profile_id": "canonical_input_manifest.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/canonical_commit_ref",
          "type": "NodeRef",
          "target_node_id": "K000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K000"
      ],
      "node_specific_constants": {
        "canonical_input_paths": [
          "START_HERE.md",
          "project_context/START_HERE.md",
          "project_context/GUARDRAILS.md",
          "project_context/PROJECT_STATE.md",
          "project_context/DECISION_LOG.md",
          "project_context/CLOSED_FINDINGS.md",
          "project_context/ARTIFACT_INDEX.md",
          "project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md",
          "project_context/DATA_CONTRACTS_named_binary_probe.md",
          "project_context/PRICE_INPUT_CONTRACT_named_binary_probe.md",
          "project_context/SPEC_named_binary_probe.md",
          "project_context/SPEC_price_source_s1_coverage.md",
          "project_context/S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02.md",
          "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md",
          "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03_AMENDMENT_01.md",
          "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A001_SENTINEL_COMBINED_ARCHITECTURE_REVIEW_RECORD_CANDIDATE_01.md",
          "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md"
        ],
        "entry_count": 17,
        "exact_ref_field_cardinalities": {
          "/payload/canonical_commit_ref": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "no missing or extra path",
        "all entries sort by path",
        "manifest commit equals K000",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K002": {
      "rank": 1020,
      "semantic_role": "architecture_candidate",
      "artifact_profile_id": "architecture_document.v1",
      "ref_bindings": [
        {
          "json_pointer": "/canonical_commit_ref",
          "type": "NodeRef",
          "target_node_id": "K000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/canonical_input_manifest",
          "type": "NodeRef",
          "target_node_id": "K001",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K000",
        "K001"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/canonical_commit_ref": 1,
          "/canonical_input_manifest": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A000": {
      "rank": 1021,
      "semantic_role": "architecture_amendment",
      "artifact_profile_id": "architecture_document.v1",
      "ref_bindings": [
        {
          "json_pointer": "/canonical_commit_ref",
          "type": "NodeRef",
          "target_node_id": "K000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/canonical_input_manifest",
          "type": "NodeRef",
          "target_node_id": "K001",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/amended_base",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K000",
        "K001",
        "K002"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/amended_base": 1,
          "/canonical_commit_ref": 1,
          "/canonical_input_manifest": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A001": {
      "rank": 1022,
      "semantic_role": "combined_architecture_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "A000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K002",
        "A000"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ],
      "represented_raw_artifact_media_type": "text/markdown; charset=utf-8",
      "normalized_envelope_rule": "review.v1 is the machine node envelope over exact raw A001 Markdown identity; ref_bindings are extracted from the exact reviewed-input table"
    },
    "A002": {
      "rank": 1023,
      "semantic_role": "accepted_controlling_architecture_set",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "A000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "A001",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K002",
        "A000",
        "A001"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/evidence_refs": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ],
      "represented_raw_artifact_media_type": "text/markdown; charset=utf-8",
      "normalized_envelope_rule": "acceptance.v1 is the machine node envelope over exact raw A002 Markdown identity; ref_bindings are extracted from controlling-set and prerequisite-review tables"
    },
    "K006": {
      "rank": 1050,
      "semantic_role": "gustavo_spec_drafting_authorization",
      "artifact_profile_id": "exact_current_gustavo_authorization.v4",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "A002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "A002"
      ],
      "node_specific_constants": {
        "record_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_GUSTAVO_AUTHORIZATION_04",
        "stage_code": "CANDIDATE_08_SPEC_ONLY_DRAFTING",
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1,
        "exact_node_identity": {
          "node_id": "K006",
          "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
          "byte_length": 4675,
          "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
        },
        "exact_node_identity_type": "NodeIdentity"
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K005": {
      "rank": 1060,
      "semantic_role": "sentinel_spec_drafting_authorization",
      "artifact_profile_id": "exact_current_sentinel_authorization.v4",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "A002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "A002",
        "K006"
      ],
      "node_specific_constants": {
        "record_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_SENTINEL_AUTHORIZATION_05",
        "stage_code": "CANDIDATE_08_SPEC_ONLY_DRAFTING",
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2,
        "exact_node_identity": {
          "node_id": "K005",
          "logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
          "byte_length": 3753,
          "sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
        },
        "exact_node_identity_type": "NodeIdentity"
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K007": {
      "rank": 1070,
      "semantic_role": "spec_drafting_activity_root",
      "artifact_profile_id": "exact_current_activity_root.v4",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "A002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "A002",
        "K006",
        "K005"
      ],
      "node_specific_constants": {
        "record_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_ROOT_05",
        "run_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3,
        "exact_node_identity": {
          "node_id": "K007",
          "logical_path": "S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json",
          "byte_length": 4262,
          "sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099"
        },
        "exact_node_identity_type": "NodeIdentity"
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K008": {
      "rank": 1080,
      "semantic_role": "candidate08_specification",
      "artifact_profile_id": "document_candidate.v1",
      "ref_bindings": [
        {
          "json_pointer": "/activity_root",
          "type": "NodeRef",
          "target_node_id": "K007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K007"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/activity_root": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "serialized normative payload contains exactly one dependency-bearing NodeRef at /activity_root targeting K007",
        "all descriptive correction-control identities use NonEdgeIdentityMetadata field names and cannot authorize or create provenance",
        "edge extractor includes only declared ref_bindings and deterministically excludes NonEdgeIdentityMetadata",
        "contains complete schema registry",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings"
      ],
      "payload_extraction_rule": "exactly one fenced JSON block immediately following NORMATIVE_K008_PAYLOAD; parse as JSON; validate document_candidate.v1; derive only K007 from /activity_root"
    },
    "K009": {
      "rank": 1090,
      "semantic_role": "candidate08_review_handoff",
      "artifact_profile_id": "candidate08_professor_handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K006",
        "K005",
        "K007",
        "K008"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 1
        },
        "exact_direct_predecessor_count": 4,
        "schema_id": "pm_research.s2.professor_review_handoff.v5",
        "record_id": "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW",
        "run_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
        "raw_sha256_binding_location": "EXTERNAL_DELIVERY_ENVELOPE_AND_SENTINEL_REVIEW_RECORD"
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ],
      "raw_media_type_override": "text/markdown; charset=utf-8",
      "raw_serialization_override": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
      "payload_extraction_rule": "exactly one fenced JSON block immediately following NORMATIVE_K009_PAYLOAD; parse as JSON and validate candidate08_professor_handoff.v1; prose remains review-significant but does not create NodeRef edges"
    },
    "K010": {
      "rank": 1100,
      "semantic_role": "candidate08_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K009",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K008",
        "K009"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K011": {
      "rank": 1110,
      "semantic_role": "accepted_candidate08",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K010",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K008",
        "K010"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K013": {
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
        }
      ],
      "derived_direct_predecessors": [
        "K011"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K012": {
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
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K013",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K011",
        "K013"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K014": {
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
        "K013",
        "K012"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K015": {
      "rank": 1150,
      "semantic_role": "implementation_source_candidate",
      "artifact_profile_id": "source_matrix.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K014",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K014"
      ],
      "node_specific_constants": {
        "exact_source_file_matrix": [
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/__init__.py",
            "role": "package_export",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/types.py",
            "role": "closed_types_and_jcs",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/schema_registry.py",
            "role": "schema_registry_and_edge_derivation",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/state_reducers.py",
            "role": "global_condition_transition_state_reducers",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/s4_inputs.py",
            "role": "s4_input_parsers_and_reconciliation",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/safe_span.py",
            "role": "safe_span_classifier_and_reducer",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/prices_history_contract.py",
            "role": "endpoint_response_terminal_and_retry_contract",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/request_plan.py",
            "role": "deterministic_request_plan",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/acquisition.py",
            "role": "independent_token_acquisition_and_raw_closure",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/construction.py",
            "role": "scientific_construction_and_deduplication",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/alignment.py",
            "role": "accepted_policy_alignment",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/rebuild.py",
            "role": "isolated_rebuild_and_byte_comparison",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/audit.py",
            "role": "nineteen_audit_closures_and_gate",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "src/pm_research/named_binary_probe/s2/transition.py",
            "role": "stage10_transition_reconciliation",
            "language": "PYTHON",
            "required": true
          }
        ],
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "matrix exact; no additional implementation source path",
        "all rows include exact byte_length and sha256 at submission",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K016": {
      "rank": 1160,
      "semantic_role": "implementation_source_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K013",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K012",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K014",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K015",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K013",
        "K012",
        "K014",
        "K015"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K017": {
      "rank": 1170,
      "semantic_role": "implementation_source_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K015",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K016",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K015",
        "K016"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K018": {
      "rank": 1180,
      "semantic_role": "accepted_implementation_source",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K015",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K017",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K015",
        "K017"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K020": {
      "rank": 1190,
      "semantic_role": "gustavo_test_source_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K018"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K019": {
      "rank": 1200,
      "semantic_role": "sentinel_test_source_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K020",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K018",
        "K020"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K021": {
      "rank": 1210,
      "semantic_role": "test_source_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K020",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K019",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K018",
        "K020",
        "K019"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K022": {
      "rank": 1220,
      "semantic_role": "test_source_candidate",
      "artifact_profile_id": "test_matrix.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K021",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K021"
      ],
      "node_specific_constants": {
        "exact_test_file_matrix": [
          {
            "logical_path": "tests/named_binary_probe/s2/test_schema_registry.py",
            "role": "schema_and_678_edge_equality",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_state_reducers.py",
            "role": "global_and_p00_p18_totality",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_s4_inputs.py",
            "role": "s4_source_parsers_and_reconciliation",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_safe_span.py",
            "role": "safe_span_total_classifier",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_prices_history_contract.py",
            "role": "response_and_terminal_mapping",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_retry_after.py",
            "role": "retry_after_units_and_caps",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_request_plan.py",
            "role": "plan_determinism_and_independence",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_acquisition.py",
            "role": "attempt_terminal_inventory_completion",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_construction.py",
            "role": "construction_identity_and_duplicates",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_alignment.py",
            "role": "selector_and_millisecond_boundary",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_rebuild.py",
            "role": "isolation_and_exact_byte_comparison",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_audit.py",
            "role": "audit_totality_and_gate_reducer",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_transition.py",
            "role": "stage10_branches_and_u0_partition",
            "language": "PYTHON",
            "required": true
          },
          {
            "logical_path": "tests/named_binary_probe/s2/test_counterexamples.py",
            "role": "required_negative_cases",
            "language": "PYTHON",
            "required": true
          }
        ],
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "matrix exact; no additional test source path",
        "all rows include exact byte_length and sha256 at submission",
        "execution_status NOT_EXECUTED",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K023": {
      "rank": 1230,
      "semantic_role": "test_source_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K020",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K019",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K021",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K022",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K020",
        "K019",
        "K021",
        "K022"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K024": {
      "rank": 1240,
      "semantic_role": "test_source_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K022",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K023",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K022",
        "K023"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K025": {
      "rank": 1250,
      "semantic_role": "accepted_test_source",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K022",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K024",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K022",
        "K024"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K027": {
      "rank": 1260,
      "semantic_role": "gustavo_test_execution_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K025",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K018",
        "K025"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K026": {
      "rank": 1270,
      "semantic_role": "sentinel_test_execution_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K025",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K027",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K018",
        "K025",
        "K027"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 1,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K028": {
      "rank": 1280,
      "semantic_role": "test_execution_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K025",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K027",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K026",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K018",
        "K025",
        "K027",
        "K026"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 1,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K029": {
      "rank": 1290,
      "semantic_role": "test_execution_result",
      "artifact_profile_id": "execution_result.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K028",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K028"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K030": {
      "rank": 1300,
      "semantic_role": "test_execution_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K027",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K026",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K028",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K029",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K027",
        "K026",
        "K028",
        "K029"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K031": {
      "rank": 1310,
      "semantic_role": "test_result_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K029",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K030",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K029",
        "K030"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K032": {
      "rank": 1320,
      "semantic_role": "accepted_test_result",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K029",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K031",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K029",
        "K031"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K034": {
      "rank": 1330,
      "semantic_role": "gustavo_s4_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K032",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K032"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K033": {
      "rank": 1340,
      "semantic_role": "sentinel_s4_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K032",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K034",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K032",
        "K034"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K035": {
      "rank": 1350,
      "semantic_role": "s4_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K032",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K034",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K033",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K032",
        "K034",
        "K033"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K036": {
      "rank": 1360,
      "semantic_role": "s4_input_manifest",
      "artifact_profile_id": "s4_input_manifest.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K035",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K035"
      ],
      "node_specific_constants": {
        "consumed_input_rows": [
          {
            "input_role": "CANONICAL_INPUT_SET",
            "logical_path": "nodes/K001/artifact.json",
            "media_type": "application/json",
            "row_schema_id": "pm_research.s2.canonical_input_manifest.v1",
            "permitted_root_class": "WORKFLOW_NODE_ROOT",
            "required": true,
            "identity_binding": "NODE_REF_K001"
          },
          {
            "input_role": "ACCEPTED_CANDIDATE08",
            "logical_path": "nodes/K011/artifact.json",
            "media_type": "application/json",
            "row_schema_id": "pm_research.s2.acceptance.v1",
            "permitted_root_class": "WORKFLOW_NODE_ROOT",
            "required": true,
            "identity_binding": "NODE_REF_K011"
          },
          {
            "input_role": "P0_CLEAR_RECORD",
            "logical_path": "canonical_read/rigolugo/pm_research/70ab8455f33d44b2a690b8c5db58f8ebc545454e/artifacts/named_binary_probe/p0_preflight.json",
            "media_type": "application/json",
            "row_schema_id": "pm_research.named_binary_probe.p0_preflight.v1",
            "permitted_root_class": "CANONICAL_AT_K000",
            "required": true,
            "identity_binding": "ARTIFACT_IDENTITY"
          },
          {
            "input_role": "CONDITION_UNIVERSE",
            "logical_path": "s4_local_inputs/condition_universe.ndjson",
            "media_type": "application/x-ndjson",
            "row_schema_id": "pm_research.s2.condition_universe_row.v1",
            "permitted_root_class": "K035_DECLARED_INPUT_ROOT",
            "required": true,
            "identity_binding": "ARTIFACT_IDENTITY"
          },
          {
            "input_role": "CLASSIFICATION_ROWS",
            "logical_path": "s4_local_inputs/classification_rows.ndjson",
            "media_type": "application/x-ndjson",
            "row_schema_id": "pm_research.s2.classification_row.v1",
            "permitted_root_class": "K035_DECLARED_INPUT_ROOT",
            "required": true,
            "identity_binding": "ARTIFACT_IDENTITY"
          },
          {
            "input_role": "RESOLUTION_ROWS",
            "logical_path": "s4_local_inputs/resolution_rows.ndjson",
            "media_type": "application/x-ndjson",
            "row_schema_id": "pm_research.s2.resolution_source_row.v1",
            "permitted_root_class": "K035_DECLARED_INPUT_ROOT",
            "required": true,
            "identity_binding": "ARTIFACT_IDENTITY"
          },
          {
            "input_role": "FIRST_TRADE_ROWS",
            "logical_path": "s4_local_inputs/first_trade_rows.ndjson",
            "media_type": "application/x-ndjson",
            "row_schema_id": "pm_research.s2.first_trade_source_row.v1",
            "permitted_root_class": "K035_DECLARED_INPUT_ROOT",
            "required": true,
            "identity_binding": "ARTIFACT_IDENTITY"
          },
          {
            "input_role": "TOKEN_OUTCOME_TUPLES",
            "logical_path": "s4_local_inputs/token_outcome_tuples.ndjson",
            "media_type": "application/x-ndjson",
            "row_schema_id": "pm_research.s2.token_outcome_tuple.v1",
            "permitted_root_class": "K035_DECLARED_INPUT_ROOT",
            "required": true,
            "identity_binding": "ARTIFACT_IDENTITY"
          },
          {
            "input_role": "S4_ACTIVITY_ROOT",
            "logical_path": "nodes/K035/artifact.json",
            "media_type": "application/json",
            "row_schema_id": "pm_research.s2.activity_root.v1",
            "permitted_root_class": "WORKFLOW_NODE_ROOT",
            "required": true,
            "identity_binding": "NODE_REF_K035"
          }
        ],
        "expected_row_count": 9,
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "row order is exactly consumed_input_rows order",
        "each row additionally carries exact JCS-safe byte_length and sha256 before parsing",
        "K001,K011,K035 exact NodeRefs appear at their fixed rows",
        "local paths are relative to one exact K035 declared input root and may not be remapped",
        "no missing, extra, aliased, or case-folded path",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K037": {
      "rank": 1370,
      "semantic_role": "s4_processing_ledger",
      "artifact_profile_id": "s4_ledger.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K035",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/input_manifest",
          "type": "NodeRef",
          "target_node_id": "K036",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K035",
        "K036"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/input_manifest": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A003": {
      "rank": 1371,
      "semantic_role": "s4_scientific_projection",
      "artifact_profile_id": "a003_condition_projection.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "K037"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/source_refs": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A004": {
      "rank": 1372,
      "semantic_role": "s4_provenance_wrapper",
      "artifact_profile_id": "provenance_wrapper.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K035",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K036",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/scientific_ref",
          "type": "NodeRef",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K035",
        "K036",
        "K037",
        "A003"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/scientific_ref": 1,
          "/payload/source_refs": 3
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K038": {
      "rank": 1380,
      "semantic_role": "s4_reconciliation",
      "artifact_profile_id": "reconciliation.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K035",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K035",
        "K037",
        "A003",
        "A004"
      ],
      "node_specific_constants": {
        "fixed_universe_count": 39693,
        "fixed_subclass_counts": {
          "UP_DOWN": 22012,
          "OVER_UNDER": 1003,
          "NAMED_OTHER": 16678
        },
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K039": {
      "rank": 1390,
      "semantic_role": "s4_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K034",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K033",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K035",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K036",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K034",
        "K033",
        "K035",
        "K036",
        "K037",
        "A003",
        "A004",
        "K038"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 4,
          "/payload/evidence_refs": 1
        },
        "exact_direct_predecessor_count": 8
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K040": {
      "rank": 1400,
      "semantic_role": "s4_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K039",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K038",
        "K039"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K041": {
      "rank": 1410,
      "semantic_role": "accepted_s4_result",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K040",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K038",
        "K040"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "acceptance may be APPROVE or ACCEPT_FINDING but never authorizes S5",
        "accepted submission and K040 review exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K043": {
      "rank": 1420,
      "semantic_role": "gustavo_s5_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K041"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K042": {
      "rank": 1430,
      "semantic_role": "sentinel_s5_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K043",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K041",
        "K043"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K044": {
      "rank": 1440,
      "semantic_role": "s5_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K043",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K042",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K041",
        "K043",
        "K042"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K045": {
      "rank": 1450,
      "semantic_role": "s5_deterministic_preflight_plan",
      "artifact_profile_id": "safe_span_plan.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K044",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K044"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "candidate spans strictly increasing positive UInt32",
        "canary set immutable and blind",
        "bounds explicit",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K046": {
      "rank": 1460,
      "semantic_role": "s5_preflight_evidence",
      "artifact_profile_id": "safe_span_evidence.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K044",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/preflight_plan",
          "type": "NodeRef",
          "target_node_id": "K045",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K044",
        "K045"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/preflight_plan": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "one total-classified attempt row per planned attempt",
        "raw response identity and receipt timestamp retained",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K047": {
      "rank": 1470,
      "semantic_role": "s5_preflight_closure",
      "artifact_profile_id": "safe_span_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K044",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/preflight_plan",
          "type": "NodeRef",
          "target_node_id": "K045",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/preflight_evidence",
          "type": "NodeRef",
          "target_node_id": "K046",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K044",
        "K045",
        "K046"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/preflight_evidence": 1,
          "/payload/preflight_plan": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "candidate reducer exact",
        "no missing observation can become UNSAFE",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K048": {
      "rank": 1480,
      "semantic_role": "s5_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K043",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K042",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K044",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K045",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K046",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K047",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K043",
        "K042",
        "K044",
        "K045",
        "K046",
        "K047"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 3
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K049": {
      "rank": 1490,
      "semantic_role": "span_policy_candidate",
      "artifact_profile_id": "span_policy_candidate.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/preflight_plan",
          "type": "NodeRef",
          "target_node_id": "K045",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/preflight_closure",
          "type": "NodeRef",
          "target_node_id": "K047",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/preflight_handoff",
          "type": "NodeRef",
          "target_node_id": "K048",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K045",
        "K047",
        "K048"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/preflight_closure": 1,
          "/payload/preflight_handoff": 1,
          "/payload/preflight_plan": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K050": {
      "rank": 1500,
      "semantic_role": "span_policy_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K048",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K049",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K048",
        "K049"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "APPROVE only SAFE_POLICY_CANDIDATE",
        "all other dispositions prohibit K051",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K051": {
      "rank": 1510,
      "semantic_role": "accepted_span_policy",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K049",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K050",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K049",
        "K050"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "approved span equals K047",
        "status accepted policy",
        "no successor authorization",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K052P": {
      "rank": 1520,
      "semantic_role": "positive_span_policy_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K050",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K050",
        "K051"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/deliverable_refs": 1,
          "/payload/evidence_refs": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "positive only; exact K051 accepted policy",
        "authorizes nothing",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K052N": {
      "rank": 1530,
      "semantic_role": "negative_span_policy_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K048",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K050",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K048",
        "K050"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "negative only; no K051/K052P refs",
        "authorizes nothing",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K054": {
      "rank": 1540,
      "semantic_role": "gustavo_s6_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K052P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K041",
        "K051",
        "K052P"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 2,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K053": {
      "rank": 1550,
      "semantic_role": "sentinel_s6_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K052P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K054",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K041",
        "K051",
        "K052P",
        "K054"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 2,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K055": {
      "rank": 1560,
      "semantic_role": "s6_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K052P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K054",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K053",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K041",
        "K051",
        "K052P",
        "K054",
        "K053"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 2,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K056F": {
      "rank": 1570,
      "semantic_role": "request_plan_family",
      "artifact_profile_id": "request_plan_family.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/s4_ledger",
          "type": "NodeRef",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/span_policy",
          "type": "NodeRef",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K051",
        "K055"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/s4_ledger": 1,
          "/payload/span_policy": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K057": {
      "rank": 1580,
      "semantic_role": "request_plan_manifest",
      "artifact_profile_id": "request_plan_manifest.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/request_plan_family",
          "type": "NodeRef",
          "target_node_id": "K056F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K056F"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/request_plan_family": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A005": {
      "rank": 1581,
      "semantic_role": "request_plan_scientific_projection",
      "artifact_profile_id": "a005_request_plan_projection.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K056F",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "K056F",
        "K057"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/source_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A006": {
      "rank": 1582,
      "semantic_role": "request_plan_provenance_wrapper",
      "artifact_profile_id": "provenance_wrapper.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K056F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/scientific_ref",
          "type": "NodeRef",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K056F",
        "K057",
        "A005"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/scientific_ref": 1,
          "/payload/source_refs": 3
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K058F": {
      "rank": 1590,
      "semantic_role": "request_attempt_family",
      "artifact_profile_id": "attempt_family.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/request_plan_manifest",
          "type": "NodeRef",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K057"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/request_plan_manifest": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K059F": {
      "rank": 1600,
      "semantic_role": "request_terminal_family",
      "artifact_profile_id": "terminal_family.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/request_plan_family",
          "type": "NodeRef",
          "target_node_id": "K056F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/attempt_family",
          "type": "NodeRef",
          "target_node_id": "K058F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K056F",
        "K058F"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/attempt_family": 1,
          "/payload/request_plan_family": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K060": {
      "rank": 1610,
      "semantic_role": "raw_evidence_inventory",
      "artifact_profile_id": "inventory.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/attempt_family",
          "type": "NodeRef",
          "target_node_id": "K058F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/terminal_family",
          "type": "NodeRef",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K058F",
        "K059F"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/attempt_family": 1,
          "/payload/terminal_family": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "inventory covers attempts, terminals, payloads exactly",
        "counts reconcile to K058F/K059F",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K061": {
      "rank": 1620,
      "semantic_role": "raw_completion_record",
      "artifact_profile_id": "completion.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/request_plan_manifest",
          "type": "NodeRef",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/terminal_family",
          "type": "NodeRef",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/inventory",
          "type": "NodeRef",
          "target_node_id": "K060",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K057",
        "K059F",
        "K060"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/inventory": 1,
          "/payload/request_plan_manifest": 1,
          "/payload/terminal_family": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "planned_count = complete_terminal_count + transient_exhausted_count + blocking_terminal_count",
        "COMPLETE iff every planned request has one complete terminal and no blocking/incomplete",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K062": {
      "rank": 1630,
      "semantic_role": "raw_archive",
      "artifact_profile_id": "archive.v1",
      "ref_bindings": [
        {
          "json_pointer": "/provenance/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/provenance/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K060",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/provenance/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K060",
        "K061"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/provenance/evidence_refs": 3
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K063": {
      "rank": 1640,
      "semantic_role": "detached_archive_identity",
      "artifact_profile_id": "archive_identity.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/raw_archive",
          "type": "NodeRef",
          "target_node_id": "K062",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K062"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/raw_archive": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A007": {
      "rank": 1641,
      "semantic_role": "raw_payload_scientific_root",
      "artifact_profile_id": "a007_raw_payload_root_projection.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K060",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/source_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K062",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/source_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K063",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "K060",
        "K061",
        "K062",
        "K063"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/source_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A008": {
      "rank": 1642,
      "semantic_role": "raw_payload_provenance_wrapper",
      "artifact_profile_id": "provenance_wrapper.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K060",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K062",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K063",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/scientific_ref",
          "type": "NodeRef",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K055",
        "K060",
        "K061",
        "K062",
        "K063",
        "A007"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/scientific_ref": 1,
          "/payload/source_refs": 5
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K064": {
      "rank": 1650,
      "semantic_role": "acquisition_reconciliation",
      "artifact_profile_id": "reconciliation.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K063",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "A003",
        "A004",
        "K057",
        "A005",
        "A006",
        "K059F",
        "K061",
        "K063",
        "A007",
        "A008"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 11
        },
        "exact_direct_predecessor_count": 11
      },
      "node_specific_invariants": [
        "reconciles S4, projections, plan, terminals, archive and raw root",
        "per-condition and subclass counts total",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K065": {
      "rank": 1660,
      "semantic_role": "acquisition_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K054",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K053",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K060",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K062",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K063",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K054",
        "K053",
        "K055",
        "K057",
        "A005",
        "A006",
        "K060",
        "K061",
        "K062",
        "K063",
        "A007",
        "A008",
        "K064"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 10
        },
        "exact_direct_predecessor_count": 13
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K066": {
      "rank": 1670,
      "semantic_role": "s6_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K065",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K064",
        "K065"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K067": {
      "rank": 1680,
      "semantic_role": "accepted_s6_result",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K066",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K064",
        "K066"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K068": {
      "rank": 1690,
      "semantic_role": "accepted_construction_contract",
      "artifact_profile_id": "construction_contract.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_specification",
          "type": "NodeRef",
          "target_node_id": "K011",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/accepted_implementation_source",
          "type": "NodeRef",
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K011",
        "K018"
      ],
      "node_specific_constants": {
        "rebuild_read_set": [
          "K068",
          "A003",
          "A005",
          "A007",
          "FIXED_ACCEPTED_ALGORITHM_AND_SERIALIZATION_PROFILES"
        ],
        "forbidden_optional_reads": [
          "K082"
        ],
        "exact_ref_field_cardinalities": {
          "/payload/accepted_implementation_source": 1,
          "/payload/accepted_specification": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "six exact partition definitions",
        "row and duplicate schemas closed",
        "no K082 or activity provenance in rebuild inputs",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K070": {
      "rank": 1700,
      "semantic_role": "gustavo_s7_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K067",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K068",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K067",
        "K068"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K069": {
      "rank": 1710,
      "semantic_role": "sentinel_s7_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K067",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K068",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K070",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K067",
        "K068",
        "K070"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 1,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K071": {
      "rank": 1720,
      "semantic_role": "s7_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K067",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K068",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K070",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K069",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K067",
        "K068",
        "K070",
        "K069"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 1,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K072": {
      "rank": 1730,
      "semantic_role": "deterministic_build_identity",
      "artifact_profile_id": "build_identity_payload.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/canonical_commit_ref",
          "type": "NodeRef",
          "target_node_id": "K000",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/construction_contract",
          "type": "NodeRef",
          "target_node_id": "K068",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/s4_projection",
          "type": "NodeRef",
          "target_node_id": "A003",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/request_plan_projection",
          "type": "NodeRef",
          "target_node_id": "A005",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/raw_payload_root",
          "type": "NodeRef",
          "target_node_id": "A007",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "K000",
        "K068",
        "A003",
        "A005",
        "A007"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/canonical_commit_ref": 1,
          "/payload/construction_contract": 1,
          "/payload/raw_payload_root": 1,
          "/payload/request_plan_projection": 1,
          "/payload/s4_projection": 1
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K073F": {
      "rank": 1740,
      "semantic_role": "original_partition_family",
      "artifact_profile_id": "partition_payload_family.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/raw_payload_root",
          "type": "NodeRef",
          "target_node_id": "A007",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/build_identity",
          "type": "NodeRef",
          "target_node_id": "K072",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "A007",
        "K072"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/build_identity": 1,
          "/payload/raw_payload_root": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K074": {
      "rank": 1750,
      "semantic_role": "original_scientific_manifest",
      "artifact_profile_id": "scientific_manifest_payload.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/build_identity",
          "type": "NodeRef",
          "target_node_id": "K072",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/partition_family",
          "type": "NodeRef",
          "target_node_id": "K073F",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "K072",
        "K073F"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/build_identity": 1,
          "/payload/partition_family": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "exact six partition identities",
        "activity-free",
        "manifest row count sum exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K075": {
      "rank": 1760,
      "semantic_role": "original_construction_reconciliation",
      "artifact_profile_id": "scientific_reconciliation_payload.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "A003",
        "A005",
        "A007",
        "K072",
        "K074"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 5
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "39,693 condition reconciliation",
        "construction categories disjoint and sum applicable population",
        "byte-compared with K098",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K076": {
      "rank": 1770,
      "semantic_role": "original_provenance_wrapper",
      "artifact_profile_id": "scientific_provenance_wrapper.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K070",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K069",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K071",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/scientific_ref",
          "type": "NodeRef",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K070",
        "K069",
        "K071",
        "A004",
        "A006",
        "A008",
        "K072",
        "K073F",
        "K074",
        "K075"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/scientific_ref": 1,
          "/payload/source_refs": 9
        },
        "exact_direct_predecessor_count": 10
      },
      "node_specific_invariants": [
        "wrapper is non-compared activity provenance",
        "wrapper binds exactly eight activity-free scientific payload identities",
        "complete wrapper equality is forbidden as a scientific comparison",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings"
      ]
    },
    "K077": {
      "rank": 1780,
      "semantic_role": "construction_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K070",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K069",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K071",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K076",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K070",
        "K069",
        "K071",
        "K074",
        "K075",
        "K076"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 3
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K078": {
      "rank": 1790,
      "semantic_role": "s7_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K077",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K075",
        "K077"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K079": {
      "rank": 1800,
      "semantic_role": "accepted_s7_result",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K078",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K075",
        "K078"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K080P": {
      "rank": 1810,
      "semantic_role": "alignment_policy_candidate",
      "artifact_profile_id": "alignment_policy.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K077",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K079",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K074",
        "K075",
        "K077",
        "K079"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K080A": {
      "rank": 1820,
      "semantic_role": "alignment_policy_absence",
      "artifact_profile_id": "absence_record.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K077",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K079",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K077",
        "K079"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K081P": {
      "rank": 1830,
      "semantic_role": "alignment_policy_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K080P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K080P"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K081A": {
      "rank": 1840,
      "semantic_role": "alignment_absence_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K080A",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K080A"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K082": {
      "rank": 1850,
      "semantic_role": "accepted_alignment_policy",
      "artifact_profile_id": "alignment_policy.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K080P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K081P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K080P",
        "K081P"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K083P": {
      "rank": 1860,
      "semantic_role": "positive_alignment_policy_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K081P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K081P",
        "K082"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K083R": {
      "rank": 1870,
      "semantic_role": "rejected_alignment_policy_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K080P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K081P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K080P",
        "K081P"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K083A": {
      "rank": 1880,
      "semantic_role": "absent_alignment_policy_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K080A",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K081A",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K080A",
        "K081A"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K085": {
      "rank": 1890,
      "semantic_role": "gustavo_s8a_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K079",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K083P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K079",
        "K082",
        "K083P"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 2,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K084": {
      "rank": 1900,
      "semantic_role": "sentinel_s8a_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K079",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K083P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K085",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K079",
        "K082",
        "K083P",
        "K085"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 2,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K086": {
      "rank": 1910,
      "semantic_role": "s8a_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K079",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/additional_prerequisites/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K083P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K085",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K084",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K079",
        "K082",
        "K083P",
        "K085",
        "K084"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/additional_prerequisites": 2,
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K087": {
      "rank": 1920,
      "semantic_role": "alignment_ledger",
      "artifact_profile_id": "alignment_ledger.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/s4_ledger",
          "type": "NodeRef",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/scientific_manifest",
          "type": "NodeRef",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/construction_reconciliation",
          "type": "NodeRef",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/alignment_policy",
          "type": "NodeRef",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K086",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K074",
        "K075",
        "K082",
        "K086"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/alignment_policy": 1,
          "/payload/construction_reconciliation": 1,
          "/payload/s4_ledger": 1,
          "/payload/scientific_manifest": 1
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "exactly 39,693 rows",
        "one accepted policy",
        "selected row keys and nullable metrics cross-field total",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K088": {
      "rank": 1930,
      "semantic_role": "alignment_reconciliation",
      "artifact_profile_id": "reconciliation.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K086",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K087",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K075",
        "K086",
        "K087"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "BOTH+ONE+NEITHER+INCOMPLETE+BLOCKED equals alignment-applicable",
        "one/neither are limitations",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K089": {
      "rank": 1940,
      "semantic_role": "alignment_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K084",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K085",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K086",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K087",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K084",
        "K085",
        "K086",
        "K087",
        "K088"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 2
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K090": {
      "rank": 1950,
      "semantic_role": "s8a_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K089",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K088",
        "K089"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K091": {
      "rank": 1960,
      "semantic_role": "accepted_s8a_result",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K090",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K088",
        "K090"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K093": {
      "rank": 1970,
      "semantic_role": "gustavo_s8b_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K091",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K091"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K092": {
      "rank": 1980,
      "semantic_role": "sentinel_s8b_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K091",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K093",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K091",
        "K093"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K094": {
      "rank": 1990,
      "semantic_role": "s8b_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K091",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K093",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K092",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K091",
        "K093",
        "K092"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K095": {
      "rank": 2000,
      "semantic_role": "rebuild_isolation_manifest",
      "artifact_profile_id": "rebuild_isolation.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K093",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K092",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K094",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/construction_contract",
          "type": "NodeRef",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/s4_projection",
          "type": "NodeRef",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/request_plan_projection",
          "type": "NodeRef",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/raw_payload_root",
          "type": "NodeRef",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K093",
        "K092",
        "K094",
        "K072",
        "A003",
        "A005",
        "A007"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/construction_contract": 1,
          "/payload/control_refs": 3,
          "/payload/raw_payload_root": 1,
          "/payload/request_plan_projection": 1,
          "/payload/s4_projection": 1
        },
        "exact_direct_predecessor_count": 7
      },
      "node_specific_invariants": [
        "isolated read set exactly K068,A003,A005,A007,fixed profiles",
        "K082 and all original outputs forbidden",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K096F": {
      "rank": 2010,
      "semantic_role": "rebuilt_partition_family",
      "artifact_profile_id": "partition_payload_family.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/raw_payload_root",
          "type": "NodeRef",
          "target_node_id": "A007",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/build_identity",
          "type": "NodeRef",
          "target_node_id": "K072",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "A007",
        "K072"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/build_identity": 1,
          "/payload/raw_payload_root": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K097": {
      "rank": 2020,
      "semantic_role": "rebuilt_scientific_manifest",
      "artifact_profile_id": "scientific_manifest_payload.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/build_identity",
          "type": "NodeRef",
          "target_node_id": "K072",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/partition_family",
          "type": "NodeRef",
          "target_node_id": "K096F",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "K072",
        "K096F"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/build_identity": 1,
          "/payload/partition_family": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "bytes must equal K074",
        "activity-free",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K098": {
      "rank": 2030,
      "semantic_role": "rebuilt_construction_reconciliation",
      "artifact_profile_id": "scientific_reconciliation_payload.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K097",
          "storage": "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED",
          "edge_authority": "TYPED_SCHEMA_BINDING"
        }
      ],
      "derived_direct_predecessors": [
        "A003",
        "A005",
        "A007",
        "K072",
        "K097"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 5
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "bytes must equal K075",
        "activity-free",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K099": {
      "rank": 2040,
      "semantic_role": "rebuild_provenance_wrapper",
      "artifact_profile_id": "scientific_provenance_wrapper.v2",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K093",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K092",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K094",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K095",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K096F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/source_refs/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K097",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/scientific_ref",
          "type": "NodeRef",
          "target_node_id": "K098",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K093",
        "K092",
        "K094",
        "K095",
        "A004",
        "A006",
        "A008",
        "K096F",
        "K097",
        "K098"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/scientific_ref": 1,
          "/payload/source_refs": 9
        },
        "exact_direct_predecessor_count": 10
      },
      "node_specific_invariants": [
        "wrapper is non-compared activity provenance",
        "wrapper binds exactly eight activity-free scientific payload identities",
        "complete wrapper equality is forbidden as a scientific comparison",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings"
      ]
    },
    "K100": {
      "rank": 2050,
      "semantic_role": "original_output_inventory_after_rebuild",
      "artifact_profile_id": "generic_evidence.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K094",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K072",
        "A003",
        "A005",
        "A007",
        "K073F",
        "K074",
        "K075",
        "K094"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 8
        },
        "exact_direct_predecessor_count": 8
      },
      "node_specific_invariants": [
        "created after rebuild outputs finalized",
        "inventories original only for comparison; not readable by rebuild actor",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K101": {
      "rank": 2060,
      "semantic_role": "rebuild_byte_comparison",
      "artifact_profile_id": "byte_comparison.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K096F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K097",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K098",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K099",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/11",
          "type": "NodeRefArrayElement",
          "target_node_id": "K100",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K072",
        "A003",
        "A005",
        "A007",
        "K073F",
        "K074",
        "K075",
        "K096F",
        "K097",
        "K098",
        "K099",
        "K100"
      ],
      "node_specific_constants": {
        "comparison_count": 8,
        "pairs": [
          "six K073F partition members ↔ six K096F members",
          "K074 ↔ K097",
          "K075 ↔ K098"
        ],
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 12
        },
        "exact_direct_predecessor_count": 12
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K102": {
      "rank": 2070,
      "semantic_role": "rebuild_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K093",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K092",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K094",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K095",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K099",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K100",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K101",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K093",
        "K092",
        "K094",
        "K095",
        "K099",
        "K100",
        "K101"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 4
        },
        "exact_direct_predecessor_count": 7
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K103": {
      "rank": 2080,
      "semantic_role": "s8b_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K101",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K102",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K101",
        "K102"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K104": {
      "rank": 2090,
      "semantic_role": "accepted_s8b_result",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K101",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K103",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K101",
        "K103"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K106": {
      "rank": 2100,
      "semantic_role": "gustavo_s8c_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K104",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K104"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K105": {
      "rank": 2110,
      "semantic_role": "sentinel_s8c_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K104",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K106",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K104",
        "K106"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K107": {
      "rank": 2120,
      "semantic_role": "s8c_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K104",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K106",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K105",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K104",
        "K106",
        "K105"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K108": {
      "rank": 2130,
      "semantic_role": "condition_effect_ledger",
      "artifact_profile_id": "effect_ledger.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K101",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K107",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K038",
        "K059F",
        "K064",
        "K075",
        "K088",
        "K101",
        "K107"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 8
        },
        "exact_direct_predecessor_count": 8
      },
      "node_specific_invariants": [
        "exactly one final effect per U0 condition",
        "counts sum 39,693",
        "every row references exact P class",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K109": {
      "rank": 2140,
      "semantic_role": "audit_closure_01",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K001",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K011",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K068",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K000",
        "K001",
        "A002",
        "K011",
        "K068"
      ],
      "node_specific_constants": {
        "check_id": "canonical_base_integrity",
        "denominator_expression": "CONST_5",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 5
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K110": {
      "rank": 2150,
      "semantic_role": "audit_closure_02",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K036",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K036",
        "K037",
        "A003",
        "A004",
        "K038",
        "K041"
      ],
      "node_specific_constants": {
        "check_id": "complete_universe_reconciliation",
        "denominator_expression": "CONST_39693",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 6
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K111": {
      "rank": 2160,
      "semantic_role": "audit_closure_03",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K038"
      ],
      "node_specific_constants": {
        "check_id": "decision_window_integrity",
        "denominator_expression": "CONST_39693",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K112": {
      "rank": 2170,
      "semantic_role": "audit_closure_04",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K038"
      ],
      "node_specific_constants": {
        "check_id": "token_pair_integrity",
        "denominator_expression": "K037.query_eligible_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K113": {
      "rank": 2180,
      "semantic_role": "audit_closure_05",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K045",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K046",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K047",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K049",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K050",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K052P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K045",
        "K046",
        "K047",
        "K049",
        "K050",
        "K051",
        "K052P"
      ],
      "node_specific_constants": {
        "check_id": "span_policy_integrity",
        "denominator_expression": "K045.candidate_count*K045.canary_request_count",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 7
        },
        "exact_direct_predecessor_count": 7
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K114": {
      "rank": 2190,
      "semantic_role": "audit_closure_06",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K052P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K056F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K051",
        "K052P",
        "K056F",
        "K057",
        "A005",
        "A006"
      ],
      "node_specific_constants": {
        "check_id": "request_plan_integrity",
        "denominator_expression": "K057.plan_row_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 6
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K115": {
      "rank": 2200,
      "semantic_role": "audit_closure_07",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K058F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K057",
        "A005",
        "A006",
        "K058F",
        "K059F",
        "K061",
        "K064"
      ],
      "node_specific_constants": {
        "check_id": "request_terminal_completeness",
        "denominator_expression": "K057.plan_row_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 7
        },
        "exact_direct_predecessor_count": 7
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K116": {
      "rank": 2210,
      "semantic_role": "audit_closure_08",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K060",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K061",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K062",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K063",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K060",
        "K061",
        "K062",
        "K063",
        "A007",
        "A008"
      ],
      "node_specific_constants": {
        "check_id": "raw_archive_closure",
        "denominator_expression": "K060.inventory_entry_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 6
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K117": {
      "rank": 2220,
      "semantic_role": "audit_closure_09",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K056F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K058F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K056F",
        "K057",
        "A005",
        "K058F",
        "K059F",
        "K064"
      ],
      "node_specific_constants": {
        "check_id": "independent_token_acquisition",
        "denominator_expression": "2*K037.stable_pair_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 6
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K118": {
      "rank": 2230,
      "semantic_role": "audit_closure_10",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K057",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K096F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K097",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K057",
        "A005",
        "K059F",
        "K073F",
        "K074",
        "K096F",
        "K097"
      ],
      "node_specific_constants": {
        "check_id": "no_synthesis_integrity",
        "denominator_expression": "K057.plan_row_count+K074.row_count+K097.row_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 7
        },
        "exact_direct_predecessor_count": 7
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K119": {
      "rank": 2240,
      "semantic_role": "audit_closure_11",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K076",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "A003",
        "A004",
        "A005",
        "A006",
        "A007",
        "A008",
        "K072",
        "K073F",
        "K074",
        "K075",
        "K076"
      ],
      "node_specific_constants": {
        "check_id": "original_construction_integrity",
        "denominator_expression": "CONST_39693",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 11
        },
        "exact_direct_predecessor_count": 11
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K120": {
      "rank": 2250,
      "semantic_role": "audit_closure_12",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K073F",
        "K074",
        "K075"
      ],
      "node_specific_constants": {
        "check_id": "duplicate_conflict_integrity",
        "denominator_expression": "K075.duplicate_group_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 3
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K121": {
      "rank": 2260,
      "semantic_role": "audit_closure_13",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K080P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K081P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K083P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K084",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K085",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K086",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K080P",
        "K081P",
        "K082",
        "K083P",
        "K084",
        "K085",
        "K086"
      ],
      "node_specific_constants": {
        "check_id": "alignment_policy_integrity",
        "denominator_expression": "CONST_1",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 7
        },
        "exact_direct_predecessor_count": 7
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K122": {
      "rank": 2270,
      "semantic_role": "audit_closure_14",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K087",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K074",
        "K075",
        "K082",
        "K087",
        "K088"
      ],
      "node_specific_constants": {
        "check_id": "alignment_execution_integrity",
        "denominator_expression": "K075.alignment_applicable_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 5
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K123": {
      "rank": 2280,
      "semantic_role": "audit_closure_15",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K087",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K087",
        "K088",
        "K108"
      ],
      "node_specific_constants": {
        "check_id": "decision_time_coverage",
        "denominator_expression": "K037.alignment_applicable_count",
        "zero_population_permitted": true,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K124": {
      "rank": 2290,
      "semantic_role": "audit_closure_16",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K000",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K068",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A004",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "A006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "A008",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/11",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/12",
          "type": "NodeRefArrayElement",
          "target_node_id": "K096F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/13",
          "type": "NodeRefArrayElement",
          "target_node_id": "K097",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/14",
          "type": "NodeRefArrayElement",
          "target_node_id": "K098",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K000",
        "K068",
        "A003",
        "A004",
        "A005",
        "A006",
        "A007",
        "A008",
        "K072",
        "K073F",
        "K074",
        "K075",
        "K096F",
        "K097",
        "K098"
      ],
      "node_specific_constants": {
        "check_id": "deterministic_build_identity",
        "denominator_expression": "CONST_4",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 15
        },
        "exact_direct_predecessor_count": 15
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K125": {
      "rank": 2300,
      "semantic_role": "audit_closure_17",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K072",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "A003",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "A005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "A007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K073F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K074",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K096F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K097",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K098",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K100",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/11",
          "type": "NodeRefArrayElement",
          "target_node_id": "K101",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K072",
        "A003",
        "A005",
        "A007",
        "K073F",
        "K074",
        "K075",
        "K096F",
        "K097",
        "K098",
        "K100",
        "K101"
      ],
      "node_specific_constants": {
        "check_id": "deterministic_rebuild_byte_equality",
        "denominator_expression": "CONST_8",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 12
        },
        "exact_direct_predecessor_count": 12
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K126": {
      "rank": 2310,
      "semantic_role": "audit_closure_18",
      "artifact_profile_id": "audit_closure.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/ordered_evidence/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K038",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K059F",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K064",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K075",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K088",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K101",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K038",
        "K059F",
        "K064",
        "K075",
        "K088",
        "K101",
        "K108"
      ],
      "node_specific_constants": {
        "check_id": "condition_effect_reconciliation",
        "denominator_expression": "CONST_39693",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 8
        },
        "exact_direct_predecessor_count": 8
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "A009": {
      "rank": 2315,
      "semantic_role": "s8c_pre_gate_activity_completion_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K106",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K105",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K107",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K109",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K110",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K111",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K112",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K113",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K114",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K115",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K116",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K117",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K118",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K119",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/11",
          "type": "NodeRefArrayElement",
          "target_node_id": "K120",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/12",
          "type": "NodeRefArrayElement",
          "target_node_id": "K121",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/13",
          "type": "NodeRefArrayElement",
          "target_node_id": "K122",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/14",
          "type": "NodeRefArrayElement",
          "target_node_id": "K123",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/15",
          "type": "NodeRefArrayElement",
          "target_node_id": "K124",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/16",
          "type": "NodeRefArrayElement",
          "target_node_id": "K125",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/17",
          "type": "NodeRefArrayElement",
          "target_node_id": "K126",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K106",
        "K105",
        "K107",
        "K108",
        "K109",
        "K110",
        "K111",
        "K112",
        "K113",
        "K114",
        "K115",
        "K116",
        "K117",
        "K118",
        "K119",
        "K120",
        "K121",
        "K122",
        "K123",
        "K124",
        "K125",
        "K126"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 1,
          "/payload/evidence_refs": 18
        },
        "exact_direct_predecessor_count": 22
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K127": {
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
          "target_node_id": "K018",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K025",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K032",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K041",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K051",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K052P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K067",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K068",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K079",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/11",
          "type": "NodeRefArrayElement",
          "target_node_id": "K082",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/12",
          "type": "NodeRefArrayElement",
          "target_node_id": "K083P",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/13",
          "type": "NodeRefArrayElement",
          "target_node_id": "K091",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/14",
          "type": "NodeRefArrayElement",
          "target_node_id": "K104",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/15",
          "type": "NodeRefArrayElement",
          "target_node_id": "K006",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/16",
          "type": "NodeRefArrayElement",
          "target_node_id": "K005",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/17",
          "type": "NodeRefArrayElement",
          "target_node_id": "K007",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/18",
          "type": "NodeRefArrayElement",
          "target_node_id": "K009",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/19",
          "type": "NodeRefArrayElement",
          "target_node_id": "K013",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/20",
          "type": "NodeRefArrayElement",
          "target_node_id": "K012",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/21",
          "type": "NodeRefArrayElement",
          "target_node_id": "K014",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/22",
          "type": "NodeRefArrayElement",
          "target_node_id": "K016",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/23",
          "type": "NodeRefArrayElement",
          "target_node_id": "K020",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/24",
          "type": "NodeRefArrayElement",
          "target_node_id": "K019",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/25",
          "type": "NodeRefArrayElement",
          "target_node_id": "K021",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/26",
          "type": "NodeRefArrayElement",
          "target_node_id": "K023",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/27",
          "type": "NodeRefArrayElement",
          "target_node_id": "K027",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/28",
          "type": "NodeRefArrayElement",
          "target_node_id": "K026",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/29",
          "type": "NodeRefArrayElement",
          "target_node_id": "K028",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/30",
          "type": "NodeRefArrayElement",
          "target_node_id": "K030",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/31",
          "type": "NodeRefArrayElement",
          "target_node_id": "K034",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/32",
          "type": "NodeRefArrayElement",
          "target_node_id": "K033",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/33",
          "type": "NodeRefArrayElement",
          "target_node_id": "K035",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/34",
          "type": "NodeRefArrayElement",
          "target_node_id": "K039",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/35",
          "type": "NodeRefArrayElement",
          "target_node_id": "K043",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/36",
          "type": "NodeRefArrayElement",
          "target_node_id": "K042",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/37",
          "type": "NodeRefArrayElement",
          "target_node_id": "K044",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/38",
          "type": "NodeRefArrayElement",
          "target_node_id": "K048",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/39",
          "type": "NodeRefArrayElement",
          "target_node_id": "K054",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/40",
          "type": "NodeRefArrayElement",
          "target_node_id": "K053",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/41",
          "type": "NodeRefArrayElement",
          "target_node_id": "K055",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/42",
          "type": "NodeRefArrayElement",
          "target_node_id": "K065",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/43",
          "type": "NodeRefArrayElement",
          "target_node_id": "K070",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/44",
          "type": "NodeRefArrayElement",
          "target_node_id": "K069",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/45",
          "type": "NodeRefArrayElement",
          "target_node_id": "K071",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/46",
          "type": "NodeRefArrayElement",
          "target_node_id": "K077",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/47",
          "type": "NodeRefArrayElement",
          "target_node_id": "K085",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/48",
          "type": "NodeRefArrayElement",
          "target_node_id": "K084",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/49",
          "type": "NodeRefArrayElement",
          "target_node_id": "K086",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/50",
          "type": "NodeRefArrayElement",
          "target_node_id": "K089",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/51",
          "type": "NodeRefArrayElement",
          "target_node_id": "K093",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/52",
          "type": "NodeRefArrayElement",
          "target_node_id": "K092",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/53",
          "type": "NodeRefArrayElement",
          "target_node_id": "K094",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/54",
          "type": "NodeRefArrayElement",
          "target_node_id": "K102",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/55",
          "type": "NodeRefArrayElement",
          "target_node_id": "K106",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/56",
          "type": "NodeRefArrayElement",
          "target_node_id": "K105",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/57",
          "type": "NodeRefArrayElement",
          "target_node_id": "K107",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/ordered_evidence/58",
          "type": "NodeRefArrayElement",
          "target_node_id": "A009",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "A002",
        "K011",
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
        "denominator_expression": "CONST_59",
        "zero_population_permitted": false,
        "exact_ref_field_cardinalities": {
          "/payload/ordered_evidence": 59
        },
        "exact_direct_predecessor_count": 59
      },
      "node_specific_invariants": [
        "population=applicable+not_applicable",
        "applicable=pass+fail+incomplete",
        "status/effect/stop combination exact",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K128": {
      "rank": 2330,
      "semantic_role": "audit_summary",
      "artifact_profile_id": "audit_summary.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K107",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K109",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K110",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K111",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K112",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K113",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K114",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K115",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K116",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/8",
          "type": "NodeRefArrayElement",
          "target_node_id": "K117",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/9",
          "type": "NodeRefArrayElement",
          "target_node_id": "K118",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/10",
          "type": "NodeRefArrayElement",
          "target_node_id": "K119",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/11",
          "type": "NodeRefArrayElement",
          "target_node_id": "K120",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/12",
          "type": "NodeRefArrayElement",
          "target_node_id": "K121",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/13",
          "type": "NodeRefArrayElement",
          "target_node_id": "K122",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/14",
          "type": "NodeRefArrayElement",
          "target_node_id": "K123",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/15",
          "type": "NodeRefArrayElement",
          "target_node_id": "K124",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/16",
          "type": "NodeRefArrayElement",
          "target_node_id": "K125",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/17",
          "type": "NodeRefArrayElement",
          "target_node_id": "K126",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/closures/18",
          "type": "NodeRefArrayElement",
          "target_node_id": "K127",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K107",
        "K109",
        "K110",
        "K111",
        "K112",
        "K113",
        "K114",
        "K115",
        "K116",
        "K117",
        "K118",
        "K119",
        "K120",
        "K121",
        "K122",
        "K123",
        "K124",
        "K125",
        "K126",
        "K127"
      ],
      "node_specific_constants": {
        "closure_nodes": [
          "K109",
          "K110",
          "K111",
          "K112",
          "K113",
          "K114",
          "K115",
          "K116",
          "K117",
          "K118",
          "K119",
          "K120",
          "K121",
          "K122",
          "K123",
          "K124",
          "K125",
          "K126",
          "K127"
        ],
        "closure_count": 19,
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/closures": 19
        },
        "exact_direct_predecessor_count": 20
      },
      "node_specific_invariants": [
        "19 exact closures",
        "summary counts sum 19",
        "precedence FAIL then INCOMPLETE then PASS",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K129": {
      "rank": 2340,
      "semantic_role": "s2_gate_record",
      "artifact_profile_id": "gate_record.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/activity_root",
          "type": "NodeRef",
          "target_node_id": "K107",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/effect_ledger",
          "type": "NodeRef",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/audit_summary",
          "type": "NodeRef",
          "target_node_id": "K128",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K107",
        "K108",
        "K128"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/activity_root": 1,
          "/payload/audit_summary": 1,
          "/payload/effect_ledger": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "gate count equations total",
        "S2_GATE_CLEAR requires 19 PASS and zero limitations/incomplete/blocking plus all alignment-applicable BOTH",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K130": {
      "rank": 2350,
      "semantic_role": "human_audit_report",
      "artifact_profile_id": "human_report.v1",
      "ref_bindings": [
        {
          "json_pointer": "/source_gate_record",
          "type": "NodeRef",
          "target_node_id": "K129",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K129"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/source_gate_record": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "human rendering only",
        "must exactly render K129; no new decision",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ],
      "raw_media_type_override": "text/markdown; charset=utf-8",
      "raw_serialization_override": "UTF8_LF_NO_BOM_FINAL_NEWLINE",
      "payload_extraction_rule": "fixed section/table grammar defined by human_report.v1"
    },
    "K131": {
      "rank": 2360,
      "semantic_role": "gate_reconciliation",
      "artifact_profile_id": "reconciliation.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K128",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K129",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K130",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K108",
        "K128",
        "K129",
        "K130"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "K108,K128,K129,K130 mutually consistent",
        "PASS only exact agreement",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K132": {
      "rank": 2370,
      "semantic_role": "s8c_final_review_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K106",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K105",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K107",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K128",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K129",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K130",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K131",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K106",
        "K105",
        "K107",
        "K108",
        "K128",
        "K129",
        "K130",
        "K131"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 5
        },
        "exact_direct_predecessor_count": 8
      },
      "node_specific_invariants": [
        "final S8C handoff after K127-K131",
        "not predecessor of K127",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K133": {
      "rank": 2380,
      "semantic_role": "s9_submission",
      "artifact_profile_id": "submission.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/source_handoff",
          "type": "NodeRef",
          "target_node_id": "K132",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K132"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/source_handoff": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "submission binds exact K132 only",
        "no review outcome prefilled",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K134": {
      "rank": 2390,
      "semantic_role": "s9_sentinel_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K132",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/reviewed_handoff",
          "type": "Nullable<NodeRef>",
          "target_node_id": "K133",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K132",
        "K133"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_handoff": 1,
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "review disposition total by K129 gate state",
        "only APPROVE exact clear can lead K137",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K135": {
      "rank": 2400,
      "semantic_role": "s9_reconciliation",
      "artifact_profile_id": "reconciliation.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K129",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K131",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K132",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K134",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K129",
        "K131",
        "K132",
        "K134"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "K129,K131,K132,K134 exact agreement",
        "no accepted-finding progression",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K136": {
      "rank": 2410,
      "semantic_role": "s9_review_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K134",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K135",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K134",
        "K135"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 2
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K137": {
      "rank": 2420,
      "semantic_role": "accepted_approved_clear_record",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K134",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K135",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K136",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K134",
        "K135",
        "K136"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/evidence_refs": 1,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "exists only APPROVE exact S2_GATE_CLEAR",
        "no S10 authorization",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K139": {
      "rank": 2430,
      "semantic_role": "gustavo_s10_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K137",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K137"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K138": {
      "rank": 2440,
      "semantic_role": "sentinel_s10_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K137",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K137",
        "K139"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K140": {
      "rank": 2450,
      "semantic_role": "s10_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K137",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K137",
        "K139",
        "K138"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K141": {
      "rank": 2460,
      "semantic_role": "stage10_transition_ledger",
      "artifact_profile_id": "transition_ledger.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K037",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K108",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K129",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K134",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K135",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/6",
          "type": "NodeRefArrayElement",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/7",
          "type": "NodeRefArrayElement",
          "target_node_id": "K140",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K037",
        "K108",
        "K129",
        "K134",
        "K135",
        "K139",
        "K138",
        "K140"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 8
        },
        "exact_direct_predecessor_count": 8
      },
      "node_specific_invariants": [
        "39,693 rows",
        "11 conjuncts exact",
        "E and I disjoint and sum U0",
        "false reasons ordered by conjunct number",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K142I": {
      "rank": 2470,
      "semantic_role": "ineligible_branch_record",
      "artifact_profile_id": "branch_record.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K140",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K141",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K139",
        "K138",
        "K140",
        "K141"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "exists iff ineligible_count>0 or eligible predicate not universal",
        "no P1 candidate",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K143I": {
      "rank": 2480,
      "semantic_role": "ineligible_branch_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K140",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K141",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K142I",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K139",
        "K138",
        "K140",
        "K141",
        "K142I"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 2
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "ineligible branch only",
        "no P1 authorization",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K144I": {
      "rank": 2490,
      "semantic_role": "accepted_ineligible_finding",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K143I",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K143I"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "accepted finding non-authorizing",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K142E": {
      "rank": 2500,
      "semantic_role": "p1_consumer_spec_candidate",
      "artifact_profile_id": "document_candidate.v1",
      "ref_bindings": [
        {
          "json_pointer": "/normative_input_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "A002",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/normative_input_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K011",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/normative_input_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/normative_input_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/normative_input_refs/4",
          "type": "NodeRefArrayElement",
          "target_node_id": "K140",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/normative_input_refs/5",
          "type": "NodeRefArrayElement",
          "target_node_id": "K141",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "A002",
        "K011",
        "K139",
        "K138",
        "K140",
        "K141"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/normative_input_refs": 6
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "exists only eligible_count=39693 and K137 exact",
        "candidate only",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ],
      "payload_extraction_rule": "exactly one fenced JSON block immediately following NORMATIVE_K142E_PAYLOAD; parse as JSON, validate document_candidate.v1, derive all normative_input_refs in Appendix-A order"
    },
    "K143E": {
      "rank": 2510,
      "semantic_role": "candidate_sealing_record",
      "artifact_profile_id": "seal.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K140",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/3",
          "type": "NodeRefArrayElement",
          "target_node_id": "K141",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sealed_artifact",
          "type": "NodeRef",
          "target_node_id": "K142E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K139",
        "K138",
        "K140",
        "K141",
        "K142E"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/evidence_refs": 4,
          "/payload/sealed_artifact": 1
        },
        "exact_direct_predecessor_count": 5
      },
      "node_specific_invariants": [
        "K142E bytes preexist seal",
        "exact path/length/hash",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K144E": {
      "rank": 2520,
      "semantic_role": "eligible_branch_handoff",
      "artifact_profile_id": "handoff.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/control_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K139",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K138",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/control_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K140",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K141",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K142E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/deliverable_refs/2",
          "type": "NodeRefArrayElement",
          "target_node_id": "K143E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K139",
        "K138",
        "K140",
        "K141",
        "K142E",
        "K143E"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/control_refs": 3,
          "/payload/deliverable_refs": 3
        },
        "exact_direct_predecessor_count": 6
      },
      "node_specific_invariants": [
        "eligible branch handoff; no P1 authorization",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K145E": {
      "rank": 2530,
      "semantic_role": "eligible_branch_review",
      "artifact_profile_id": "review.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/reviewed_submission",
          "type": "NodeRef",
          "target_node_id": "K144E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K144E"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/reviewed_submission": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "APPROVE required for K146E",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K146E": {
      "rank": 2540,
      "semantic_role": "accepted_eligible_transition",
      "artifact_profile_id": "acceptance.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/accepted_submission",
          "type": "NodeRef",
          "target_node_id": "K142E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/0",
          "type": "NodeRefArrayElement",
          "target_node_id": "K143E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/evidence_refs/1",
          "type": "NodeRefArrayElement",
          "target_node_id": "K144E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/review_record",
          "type": "NodeRef",
          "target_node_id": "K145E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K142E",
        "K143E",
        "K144E",
        "K145E"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/accepted_submission": 1,
          "/payload/evidence_refs": 2,
          "/payload/review_record": 1
        },
        "exact_direct_predecessor_count": 4
      },
      "node_specific_invariants": [
        "accepted transition only",
        "P1 remains blocked pending K148,K147,K149",
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K148": {
      "rank": 2550,
      "semantic_role": "gustavo_future_p1_authorization",
      "artifact_profile_id": "gustavo_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K146E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K146E"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 1
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K147": {
      "rank": 2560,
      "semantic_role": "sentinel_future_p1_authorization",
      "artifact_profile_id": "sentinel_authorization.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K146E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K148",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K146E",
        "K148"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1
        },
        "exact_direct_predecessor_count": 2
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    },
    "K149": {
      "rank": 2570,
      "semantic_role": "future_p1_activity_root",
      "artifact_profile_id": "activity_root.v1",
      "ref_bindings": [
        {
          "json_pointer": "/payload/prerequisite_acceptance",
          "type": "NodeRef",
          "target_node_id": "K146E",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/gustavo_authorization",
          "type": "NodeRef",
          "target_node_id": "K148",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        },
        {
          "json_pointer": "/payload/sentinel_stage_authorization",
          "type": "NodeRef",
          "target_node_id": "K147",
          "storage": "ARTIFACT_FIELD",
          "edge_authority": "TYPED_NODE_REF_FIELD"
        }
      ],
      "derived_direct_predecessors": [
        "K146E",
        "K148",
        "K147"
      ],
      "node_specific_constants": {
        "exact_ref_field_cardinalities": {
          "/payload/gustavo_authorization": 1,
          "/payload/prerequisite_acceptance": 1,
          "/payload/sentinel_stage_authorization": 1
        },
        "exact_direct_predecessor_count": 3
      },
      "node_specific_invariants": [
        "every typed reference field has exactly the cardinality and target sequence in ref_bindings; absent optional arrays mean cardinality zero"
      ]
    }
  },
  "edge_derivation": {
    "algorithm": [
      "for each node in rank order, resolve its artifact_profile_id",
      "validate every ref_binding target exists and target rank is strictly lower",
      "for storage=ARTIFACT_FIELD, validate exact NodeRef at json_pointer in serialized record",
      "for storage=SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED, validate binding is declared by the closed artifact profile and is absent from activity-free scientific payload bytes",
      "emit one directed edge (source_node_id,target_node_id) per ref_binding in listed order",
      "derive /dependencies only for record profiles that serialize a dependencies field; scientific payload profiles serialize no dependencies",
      "ignore NodeIdentity and NonEdgeIdentityMetadata fields; neither is edge-authoritative",
      "compare the emitted set and order-insensitive pair set with Appendix A",
      "fail PROVENANCE_EDGE_SET_MISMATCH on any missing, extra, duplicate, rank-invalid, or cyclic edge"
    ],
    "binding_storage_enum": [
      "ARTIFACT_FIELD",
      "SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED"
    ],
    "excluded_non_edge_types": [
      "NodeIdentity",
      "NonEdgeIdentityMetadata",
      "ArtifactIdentity",
      "ScientificPayloadIdentity",
      "SchemaLiteral",
      "AdministrativeRoleSourceContext"
    ],
    "declared_node_count": 166,
    "declared_edge_count": 678,
    "schema_derived_node_count": 166,
    "schema_derived_edge_count": 678,
    "missing_edges": [],
    "extra_edges": [],
    "rank_violations": [],
    "cycles": []
  },
  "non_authorizing_control_metadata": {
    "identity_type": "NonEdgeIdentityMetadata",
    "records": {
      "A002": {
        "metadata_node_label": "A002",
        "metadata_logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
        "metadata_byte_length": 5854,
        "metadata_sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
      },
      "K006": {
        "metadata_node_label": "K006",
        "metadata_logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
        "metadata_byte_length": 4675,
        "metadata_sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
      },
      "K005": {
        "metadata_node_label": "K005",
        "metadata_logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
        "metadata_byte_length": 3753,
        "metadata_sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
      },
      "K007": {
        "metadata_node_label": "K007",
        "metadata_logical_path": "S2_CANDIDATE_08_K007_SPEC_ONLY_DRAFTING_ROOT_05.json",
        "metadata_byte_length": 4262,
        "metadata_sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099"
      }
    },
    "run_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
    "authority": "descriptive verification only; exact K008 direct edge remains K007",
    "administrative_role_source_context": {
      "context_type": "AdministrativeRoleSourceContext",
      "repository": "rigolugo/pm_copilot_roles",
      "immutable_commit": "a7df418216cb7355b003164b8b509e40081cdbdc",
      "canonical_state": "INSTALLED_AND_SENTINEL_VERIFIED",
      "evidence_only": true,
      "role_execution_authorized": false,
      "required_reads": [
        "project_context/GITHUB_COPILOT_CLI_ROLE_SOURCE_POINTER.md",
        "project_context/administrative_tools/github_copilot_cli/README_FIRST.md",
        "project_context/administrative_tools/github_copilot_cli/SENTINEL_CANONICAL_INSTALLATION_VERIFICATION.md"
      ],
      "s2_architecture_dependency": false,
      "s2_scientific_dependency": false,
      "s2_provenance_dependency": false,
      "s2_build_identity_dependency": false,
      "s2_audit_dependency": false,
      "s2_gate_dependency": false,
      "authorization_effect": "NONE",
      "role_execution_status": "NOT_PERFORMED"
    }
  },
  "exact_current_record_schemas": {
    "K006": {
      "schema_id": "pm_research.s2.exact_current_record.K006.v3",
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "raw_byte_length": 4675,
      "raw_sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f",
      "closed_json_value": {
        "canonical_commit": "70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "created_at_utc_ms": 1785267538563,
        "dependencies": [
          {
            "byte_length": 5854,
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
            "node_id": "A002",
            "sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
          }
        ],
        "node_id": "K006",
        "payload": {
          "activity_authorization_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_GUSTAVO_AUTHORIZATION_04",
          "authorization_source": {
            "actor": "Gustavo",
            "exact_statement": "I authorize a third bounded Candidate 08 SPEC-only correction using these exact blocked inputs:\n\n* K008: 759608 bytes, SHA-256 `8f14caf480da85fab802105427e3841ca9d46f4d01c8e3643c63dc32ed85de8b`\n* K009: 13676 bytes, SHA-256 `901143eb6f4f44b73b2953c2311949b956c4569fee46bc8a6735f28762cfa102`\n\nThe correction is limited to:\n\n1. making K009 conform to one exact closed assigned profile;\n2. reconciling the K009 self-identity binding-location enum;\n3. replacing normative alignment-policy `UInt64` references with `UInt64Dec`;\n4. making the `RecordId` maximum identical in prose and the machine registry;\n5. making the `RelativePath` NFC rule identical in prose and the machine registry;\n6. adding mandatory raw K008/K009 payload-to-profile and identity validation to the static-validation contract.\n\nIt authorizes specification and handoff drafting, checksum computation, and static document/schema checks only.\n\nIt does not authorize implementation, test authoring or execution, project imports, local research-data access, network/API activity, empirical runs, acquisition, construction, alignment, rebuild, audit, transition, P1/P2/P3, scoring, probe execution, Copilot CLI role execution, canonical installation, or Git activity.",
            "source_context": "current Polymarket Research Orchestration project chat"
          },
          "permitted_activity": "CANDIDATE_08_THIRD_BOUNDED_SPEC_ONLY_CORRECTION",
          "permitted_actor": "Professor",
          "permitted_input_roots": [
            "canonical_read/rigolugo/pm_research/70ab8455f33d44b2a690b8c5db58f8ebc545454e/",
            "submitted_review/candidate08_blocked_03/"
          ],
          "permitted_output_roots": [
            "submitted_review/candidate08_correction_03/"
          ],
          "prerequisite_acceptance": {
            "byte_length": 5854,
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
            "node_id": "A002",
            "sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
          },
          "scope_constraints": {
            "allowed_deliverables": [
              "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
              "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md"
            ],
            "allowed_operations": [
              "READ_CANONICAL_TEXT",
              "READ_EXACT_BLOCKED_K008_K009",
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
            "blocked_submission_identities": [
              {
                "byte_length": 759608,
                "logical_path": "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
                "sha256": "8f14caf480da85fab802105427e3841ca9d46f4d01c8e3643c63dc32ed85de8b"
              },
              {
                "byte_length": 13676,
                "logical_path": "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md",
                "sha256": "901143eb6f4f44b73b2953c2311949b956c4569fee46bc8a6735f28762cfa102"
              }
            ],
            "canonical_writes": false,
            "correction_boundary": [
              "MAKE_K009_CONFORM_TO_ONE_EXACT_CLOSED_ASSIGNED_PROFILE",
              "RECONCILE_K009_SELF_IDENTITY_BINDING_LOCATION_ENUM",
              "REPLACE_NORMATIVE_ALIGNMENT_UINT64_WITH_UINT64DEC",
              "UNIFY_RECORDID_MAXIMUM_IN_PROSE_AND_MACHINE_REGISTRY",
              "UNIFY_RELATIVEPATH_NFC_RULE_IN_PROSE_AND_MACHINE_REGISTRY",
              "REQUIRE_RAW_K008_K009_PAYLOAD_PROFILE_AND_IDENTITY_VALIDATION"
            ],
            "forbidden_operations": [
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
              "GIT_BRANCH_COMMIT_PUSH_MERGE_TAG_RELEASE_OR_REF_UPDATE"
            ],
            "implementation_or_execution_authorization": false,
            "scope_expansion": false
          },
          "stage_code": "CANDIDATE_08_SPEC_ONLY_DRAFTING",
          "status": "AUTHORIZED"
        },
        "record_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_GUSTAVO_AUTHORIZATION_04",
        "schema_id": "pm_research.s2.gustavo_activity_authorization.v4",
        "status": "AUTHORIZED"
      },
      "validation_algorithm": [
        "read exact raw bytes from declared logical path",
        "require raw byte length and SHA-256 exact",
        "decode UTF-8 with no BOM and no trailing newline",
        "parse one JSON value with duplicate object keys rejected",
        "require parsed value deep-equal closed_json_value including array order and scalar types",
        "require raw bytes equal RFC8785 JCS serialization of closed_json_value",
        "reject any field absent from closed_json_value"
      ],
      "closed_json_value_type": "SchemaLiteral",
      "materialized_json_pointers": [
        "/canonical_commit",
        "/created_at_utc_ms",
        "/dependencies",
        "/dependencies/0",
        "/dependencies/0/byte_length",
        "/dependencies/0/logical_path",
        "/dependencies/0/node_id",
        "/dependencies/0/sha256",
        "/node_id",
        "/payload",
        "/payload/activity_authorization_id",
        "/payload/authorization_source",
        "/payload/authorization_source/actor",
        "/payload/authorization_source/exact_statement",
        "/payload/authorization_source/source_context",
        "/payload/permitted_activity",
        "/payload/permitted_actor",
        "/payload/permitted_input_roots",
        "/payload/permitted_input_roots/0",
        "/payload/permitted_input_roots/1",
        "/payload/permitted_output_roots",
        "/payload/permitted_output_roots/0",
        "/payload/prerequisite_acceptance",
        "/payload/prerequisite_acceptance/byte_length",
        "/payload/prerequisite_acceptance/logical_path",
        "/payload/prerequisite_acceptance/node_id",
        "/payload/prerequisite_acceptance/sha256",
        "/payload/scope_constraints",
        "/payload/scope_constraints/allowed_deliverables",
        "/payload/scope_constraints/allowed_deliverables/0",
        "/payload/scope_constraints/allowed_deliverables/1",
        "/payload/scope_constraints/allowed_operations",
        "/payload/scope_constraints/allowed_operations/0",
        "/payload/scope_constraints/allowed_operations/1",
        "/payload/scope_constraints/allowed_operations/2",
        "/payload/scope_constraints/allowed_operations/3",
        "/payload/scope_constraints/allowed_operations/4",
        "/payload/scope_constraints/allowed_operations/5",
        "/payload/scope_constraints/allowed_operations/6",
        "/payload/scope_constraints/allowed_operations/7",
        "/payload/scope_constraints/allowed_operations/8",
        "/payload/scope_constraints/allowed_operations/9",
        "/payload/scope_constraints/allowed_operations/10",
        "/payload/scope_constraints/blocked_submission_identities",
        "/payload/scope_constraints/blocked_submission_identities/0",
        "/payload/scope_constraints/blocked_submission_identities/0/byte_length",
        "/payload/scope_constraints/blocked_submission_identities/0/logical_path",
        "/payload/scope_constraints/blocked_submission_identities/0/sha256",
        "/payload/scope_constraints/blocked_submission_identities/1",
        "/payload/scope_constraints/blocked_submission_identities/1/byte_length",
        "/payload/scope_constraints/blocked_submission_identities/1/logical_path",
        "/payload/scope_constraints/blocked_submission_identities/1/sha256",
        "/payload/scope_constraints/canonical_writes",
        "/payload/scope_constraints/correction_boundary",
        "/payload/scope_constraints/correction_boundary/0",
        "/payload/scope_constraints/correction_boundary/1",
        "/payload/scope_constraints/correction_boundary/2",
        "/payload/scope_constraints/correction_boundary/3",
        "/payload/scope_constraints/correction_boundary/4",
        "/payload/scope_constraints/correction_boundary/5",
        "/payload/scope_constraints/forbidden_operations",
        "/payload/scope_constraints/forbidden_operations/0",
        "/payload/scope_constraints/forbidden_operations/1",
        "/payload/scope_constraints/forbidden_operations/2",
        "/payload/scope_constraints/forbidden_operations/3",
        "/payload/scope_constraints/forbidden_operations/4",
        "/payload/scope_constraints/forbidden_operations/5",
        "/payload/scope_constraints/forbidden_operations/6",
        "/payload/scope_constraints/forbidden_operations/7",
        "/payload/scope_constraints/forbidden_operations/8",
        "/payload/scope_constraints/forbidden_operations/9",
        "/payload/scope_constraints/forbidden_operations/10",
        "/payload/scope_constraints/forbidden_operations/11",
        "/payload/scope_constraints/forbidden_operations/12",
        "/payload/scope_constraints/forbidden_operations/13",
        "/payload/scope_constraints/forbidden_operations/14",
        "/payload/scope_constraints/forbidden_operations/15",
        "/payload/scope_constraints/forbidden_operations/16",
        "/payload/scope_constraints/forbidden_operations/17",
        "/payload/scope_constraints/forbidden_operations/18",
        "/payload/scope_constraints/forbidden_operations/19",
        "/payload/scope_constraints/implementation_or_execution_authorization",
        "/payload/scope_constraints/scope_expansion",
        "/payload/stage_code",
        "/payload/status",
        "/record_id",
        "/schema_id",
        "/status"
      ],
      "field_count_including_containers": 88,
      "cross_field_invariants": [
        "closed_json_value.canonical_commit=70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "dependencies equal the exact typed semantic references in accepted architecture order",
        "payload.prerequisite_acceptance deep-equals exact A002 NodeRef",
        "COPILOT_ROLE_EXECUTION is explicitly forbidden wherever the record carries forbidden_operations",
        "no administrative role-source identity is a typed NodeRef or S2 scientific/build/audit/gate dependency",
        "payload.authorization_source.actor=Gustavo",
        "payload.scope_constraints.canonical_writes=false",
        "payload.scope_constraints.implementation_or_execution_authorization=false",
        "payload.permitted_activity=CANDIDATE_08_THIRD_BOUNDED_SPEC_ONLY_CORRECTION"
      ]
    },
    "K005": {
      "schema_id": "pm_research.s2.exact_current_record.K005.v3",
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "raw_byte_length": 3753,
      "raw_sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546",
      "closed_json_value": {
        "canonical_commit": "70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "created_at_utc_ms": 1785267538564,
        "dependencies": [
          {
            "byte_length": 5854,
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
            "node_id": "A002",
            "sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
          },
          {
            "byte_length": 4675,
            "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
            "node_id": "K006",
            "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
          }
        ],
        "node_id": "K005",
        "payload": {
          "activated_activity": "CANDIDATE_08_THIRD_BOUNDED_SPEC_ONLY_CORRECTION",
          "activated_actor": "Professor",
          "activated_input_roots": [
            "canonical_read/rigolugo/pm_research/70ab8455f33d44b2a690b8c5db58f8ebc545454e/",
            "submitted_review/candidate08_blocked_03/"
          ],
          "activated_output_roots": [
            "submitted_review/candidate08_correction_03/"
          ],
          "activated_scope_constraints": {
            "allowed_deliverables": [
              "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
              "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md"
            ],
            "allowed_operations": [
              "READ_CANONICAL_TEXT",
              "READ_EXACT_BLOCKED_K008_K009",
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
            "blocked_submission_identities": [
              {
                "byte_length": 759608,
                "logical_path": "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
                "sha256": "8f14caf480da85fab802105427e3841ca9d46f4d01c8e3643c63dc32ed85de8b"
              },
              {
                "byte_length": 13676,
                "logical_path": "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md",
                "sha256": "901143eb6f4f44b73b2953c2311949b956c4569fee46bc8a6735f28762cfa102"
              }
            ],
            "correction_boundary": [
              "MAKE_K009_CONFORM_TO_ONE_EXACT_CLOSED_ASSIGNED_PROFILE",
              "RECONCILE_K009_SELF_IDENTITY_BINDING_LOCATION_ENUM",
              "REPLACE_NORMATIVE_ALIGNMENT_UINT64_WITH_UINT64DEC",
              "UNIFY_RECORDID_MAXIMUM_IN_PROSE_AND_MACHINE_REGISTRY",
              "UNIFY_RELATIVEPATH_NFC_RULE_IN_PROSE_AND_MACHINE_REGISTRY",
              "REQUIRE_RAW_K008_K009_PAYLOAD_PROFILE_AND_IDENTITY_VALIDATION"
            ],
            "forbidden_operations": [
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
              "GIT_BRANCH_COMMIT_PUSH_MERGE_TAG_RELEASE_OR_REF_UPDATE"
            ],
            "must_preserve_accepted_architecture": true,
            "scope_expansion": false,
            "scope_relation_to_k006": "STRICT_SUBSET"
          },
          "decision": "AUTHORIZE_STAGE",
          "gustavo_authorization": {
            "byte_length": 4675,
            "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
            "node_id": "K006",
            "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
          },
          "prerequisite_acceptance": {
            "byte_length": 5854,
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
            "node_id": "A002",
            "sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
          },
          "stage_authorization_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_SENTINEL_AUTHORIZATION_05",
          "stage_code": "CANDIDATE_08_SPEC_ONLY_DRAFTING"
        },
        "record_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_SENTINEL_AUTHORIZATION_05",
        "schema_id": "pm_research.s2.sentinel_narrow_stage_authorization.v4",
        "status": "AUTHORIZE_STAGE"
      },
      "validation_algorithm": [
        "read exact raw bytes from declared logical path",
        "require raw byte length and SHA-256 exact",
        "decode UTF-8 with no BOM and no trailing newline",
        "parse one JSON value with duplicate object keys rejected",
        "require parsed value deep-equal closed_json_value including array order and scalar types",
        "require raw bytes equal RFC8785 JCS serialization of closed_json_value",
        "reject any field absent from closed_json_value"
      ],
      "closed_json_value_type": "SchemaLiteral",
      "materialized_json_pointers": [
        "/canonical_commit",
        "/created_at_utc_ms",
        "/dependencies",
        "/dependencies/0",
        "/dependencies/0/byte_length",
        "/dependencies/0/logical_path",
        "/dependencies/0/node_id",
        "/dependencies/0/sha256",
        "/dependencies/1",
        "/dependencies/1/byte_length",
        "/dependencies/1/logical_path",
        "/dependencies/1/node_id",
        "/dependencies/1/sha256",
        "/node_id",
        "/payload",
        "/payload/activated_activity",
        "/payload/activated_actor",
        "/payload/activated_input_roots",
        "/payload/activated_input_roots/0",
        "/payload/activated_input_roots/1",
        "/payload/activated_output_roots",
        "/payload/activated_output_roots/0",
        "/payload/activated_scope_constraints",
        "/payload/activated_scope_constraints/allowed_deliverables",
        "/payload/activated_scope_constraints/allowed_deliverables/0",
        "/payload/activated_scope_constraints/allowed_deliverables/1",
        "/payload/activated_scope_constraints/allowed_operations",
        "/payload/activated_scope_constraints/allowed_operations/0",
        "/payload/activated_scope_constraints/allowed_operations/1",
        "/payload/activated_scope_constraints/allowed_operations/2",
        "/payload/activated_scope_constraints/allowed_operations/3",
        "/payload/activated_scope_constraints/allowed_operations/4",
        "/payload/activated_scope_constraints/allowed_operations/5",
        "/payload/activated_scope_constraints/allowed_operations/6",
        "/payload/activated_scope_constraints/allowed_operations/7",
        "/payload/activated_scope_constraints/allowed_operations/8",
        "/payload/activated_scope_constraints/allowed_operations/9",
        "/payload/activated_scope_constraints/allowed_operations/10",
        "/payload/activated_scope_constraints/blocked_submission_identities",
        "/payload/activated_scope_constraints/blocked_submission_identities/0",
        "/payload/activated_scope_constraints/blocked_submission_identities/0/byte_length",
        "/payload/activated_scope_constraints/blocked_submission_identities/0/logical_path",
        "/payload/activated_scope_constraints/blocked_submission_identities/0/sha256",
        "/payload/activated_scope_constraints/blocked_submission_identities/1",
        "/payload/activated_scope_constraints/blocked_submission_identities/1/byte_length",
        "/payload/activated_scope_constraints/blocked_submission_identities/1/logical_path",
        "/payload/activated_scope_constraints/blocked_submission_identities/1/sha256",
        "/payload/activated_scope_constraints/correction_boundary",
        "/payload/activated_scope_constraints/correction_boundary/0",
        "/payload/activated_scope_constraints/correction_boundary/1",
        "/payload/activated_scope_constraints/correction_boundary/2",
        "/payload/activated_scope_constraints/correction_boundary/3",
        "/payload/activated_scope_constraints/correction_boundary/4",
        "/payload/activated_scope_constraints/correction_boundary/5",
        "/payload/activated_scope_constraints/forbidden_operations",
        "/payload/activated_scope_constraints/forbidden_operations/0",
        "/payload/activated_scope_constraints/forbidden_operations/1",
        "/payload/activated_scope_constraints/forbidden_operations/2",
        "/payload/activated_scope_constraints/forbidden_operations/3",
        "/payload/activated_scope_constraints/forbidden_operations/4",
        "/payload/activated_scope_constraints/forbidden_operations/5",
        "/payload/activated_scope_constraints/forbidden_operations/6",
        "/payload/activated_scope_constraints/forbidden_operations/7",
        "/payload/activated_scope_constraints/forbidden_operations/8",
        "/payload/activated_scope_constraints/forbidden_operations/9",
        "/payload/activated_scope_constraints/forbidden_operations/10",
        "/payload/activated_scope_constraints/forbidden_operations/11",
        "/payload/activated_scope_constraints/forbidden_operations/12",
        "/payload/activated_scope_constraints/forbidden_operations/13",
        "/payload/activated_scope_constraints/forbidden_operations/14",
        "/payload/activated_scope_constraints/forbidden_operations/15",
        "/payload/activated_scope_constraints/forbidden_operations/16",
        "/payload/activated_scope_constraints/forbidden_operations/17",
        "/payload/activated_scope_constraints/forbidden_operations/18",
        "/payload/activated_scope_constraints/forbidden_operations/19",
        "/payload/activated_scope_constraints/must_preserve_accepted_architecture",
        "/payload/activated_scope_constraints/scope_expansion",
        "/payload/activated_scope_constraints/scope_relation_to_k006",
        "/payload/decision",
        "/payload/gustavo_authorization",
        "/payload/gustavo_authorization/byte_length",
        "/payload/gustavo_authorization/logical_path",
        "/payload/gustavo_authorization/node_id",
        "/payload/gustavo_authorization/sha256",
        "/payload/prerequisite_acceptance",
        "/payload/prerequisite_acceptance/byte_length",
        "/payload/prerequisite_acceptance/logical_path",
        "/payload/prerequisite_acceptance/node_id",
        "/payload/prerequisite_acceptance/sha256",
        "/payload/stage_authorization_id",
        "/payload/stage_code",
        "/record_id",
        "/schema_id",
        "/status"
      ],
      "field_count_including_containers": 94,
      "cross_field_invariants": [
        "closed_json_value.canonical_commit=70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "dependencies equal the exact typed semantic references in accepted architecture order",
        "payload.prerequisite_acceptance deep-equals exact A002 NodeRef",
        "COPILOT_ROLE_EXECUTION is explicitly forbidden wherever the record carries forbidden_operations",
        "no administrative role-source identity is a typed NodeRef or S2 scientific/build/audit/gate dependency",
        "payload.gustavo_authorization deep-equals exact K006 NodeRef",
        "payload.activated_scope_constraints.scope_relation_to_k006=STRICT_SUBSET",
        "payload.activated_activity=CANDIDATE_08_THIRD_BOUNDED_SPEC_ONLY_CORRECTION"
      ]
    },
    "K007": {
      "schema_id": "pm_research.s2.exact_current_record.K007.v3",
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "raw_byte_length": 4262,
      "raw_sha256": "f3efc8f95e15171ba5c14747dff1e169101c0d0ca16f6d45a8a4c1c71c406099",
      "closed_json_value": {
        "canonical_commit": "70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "created_at_utc_ms": 1785267538565,
        "dependencies": [
          {
            "byte_length": 5854,
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
            "node_id": "A002",
            "sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
          },
          {
            "byte_length": 4675,
            "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
            "node_id": "K006",
            "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
          },
          {
            "byte_length": 3753,
            "logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
            "node_id": "K005",
            "sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
          }
        ],
        "node_id": "K007",
        "payload": {
          "activity_root_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_ROOT_05",
          "activity_scope": {
            "allowed_deliverables": [
              "S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md",
              "HANDOFF_PROFESSOR_S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_REVIEW.md"
            ],
            "authorization_effect": "SPECIFICATION_DRAFTING_ONLY",
            "correction_boundary": [
              "MAKE_K009_CONFORM_TO_ONE_EXACT_CLOSED_ASSIGNED_PROFILE",
              "RECONCILE_K009_SELF_IDENTITY_BINDING_LOCATION_ENUM",
              "REPLACE_NORMATIVE_ALIGNMENT_UINT64_WITH_UINT64DEC",
              "UNIFY_RECORDID_MAXIMUM_IN_PROSE_AND_MACHINE_REGISTRY",
              "UNIFY_RELATIVEPATH_NFC_RULE_IN_PROSE_AND_MACHINE_REGISTRY",
              "REQUIRE_RAW_K008_K009_PAYLOAD_PROFILE_AND_IDENTITY_VALIDATION"
            ],
            "forbidden_operations": [
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
              "GIT_BRANCH_COMMIT_PUSH_MERGE_TAG_RELEASE_OR_REF_UPDATE"
            ],
            "mandatory_static_acceptance_checks": [
              "RAW_K008_BYTE_LENGTH_AND_SHA256_MATCH",
              "RAW_K009_BYTE_LENGTH_AND_EXTERNAL_SHA256_MATCH",
              "K008_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE",
              "K009_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE",
              "K008_PAYLOAD_VALIDATES_ASSIGNED_PROFILE",
              "K009_PAYLOAD_VALIDATES_ASSIGNED_PROFILE",
              "K009_SELF_EXCLUDING_PROJECTION_IDENTITY_MATCHES",
              "K009_SELF_IDENTITY_ENUM_VALUE_IS_REGISTERED",
              "NORMATIVE_TYPE_REFERENCES_RESOLVE_IN_PROSE_AND_REGISTRY",
              "RECORDID_BOUND_IS_IDENTICAL",
              "RELATIVEPATH_NFC_RULE_IS_IDENTICAL"
            ],
            "required_return": {
              "destination": "Sentinel",
              "implementation_or_execution_authorization": false,
              "include_exact_byte_lengths": true,
              "include_exact_sha256": true
            },
            "stop_conditions": [
              "STOP_CANONICAL_BASE_MISMATCH",
              "STOP_A002_IDENTITY_MISMATCH",
              "STOP_BLOCKED_INPUT_IDENTITY_MISMATCH",
              "STOP_AUTHORIZATION_PROVENANCE_INVALID",
              "STOP_AUTHORIZATION_SCOPE_EXPANSION",
              "STOP_K008_PROFILE_VALIDATION_FAILED",
              "STOP_K009_PROFILE_VALIDATION_FAILED",
              "STOP_K009_SELF_IDENTITY_MISMATCH",
              "STOP_NORMATIVE_TYPE_CONTRADICTION",
              "STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED",
              "STOP_UNEXPECTED_DELIVERABLE_PATH"
            ]
          },
          "gustavo_authorization": {
            "byte_length": 4675,
            "logical_path": "S2_CANDIDATE_08_K006_GUSTAVO_SPEC_ONLY_DRAFTING_AUTHORIZATION_04.json",
            "node_id": "K006",
            "sha256": "52bd367a8949e44de6594150c7b0bf3ed9c2cfe1813168fde935847c472aa56f"
          },
          "input_roots": [
            "canonical_read/rigolugo/pm_research/70ab8455f33d44b2a690b8c5db58f8ebc545454e/",
            "submitted_review/candidate08_blocked_03/"
          ],
          "output_roots": [
            "submitted_review/candidate08_correction_03/"
          ],
          "prerequisite_acceptance": {
            "byte_length": 5854,
            "logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
            "node_id": "A002",
            "sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
          },
          "run_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03",
          "sentinel_stage_authorization": {
            "byte_length": 3753,
            "logical_path": "S2_CANDIDATE_08_K005_SENTINEL_SPEC_ONLY_DRAFTING_AUTHORIZATION_05.json",
            "node_id": "K005",
            "sha256": "89d1e8f901b9cd64026799761f8a1c5c23657f4deb17fdaf6ec0790facfcb546"
          },
          "stage_code": "CANDIDATE_08_SPEC_ONLY_DRAFTING"
        },
        "record_id": "S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_ROOT_05",
        "schema_id": "pm_research.s2.activity_root.v4",
        "status": "ACTIVE_SPECIFICATION_CORRECTION_ROOT"
      },
      "validation_algorithm": [
        "read exact raw bytes from declared logical path",
        "require raw byte length and SHA-256 exact",
        "decode UTF-8 with no BOM and no trailing newline",
        "parse one JSON value with duplicate object keys rejected",
        "require parsed value deep-equal closed_json_value including array order and scalar types",
        "require raw bytes equal RFC8785 JCS serialization of closed_json_value",
        "reject any field absent from closed_json_value"
      ],
      "closed_json_value_type": "SchemaLiteral",
      "materialized_json_pointers": [
        "/canonical_commit",
        "/created_at_utc_ms",
        "/dependencies",
        "/dependencies/0",
        "/dependencies/0/byte_length",
        "/dependencies/0/logical_path",
        "/dependencies/0/node_id",
        "/dependencies/0/sha256",
        "/dependencies/1",
        "/dependencies/1/byte_length",
        "/dependencies/1/logical_path",
        "/dependencies/1/node_id",
        "/dependencies/1/sha256",
        "/dependencies/2",
        "/dependencies/2/byte_length",
        "/dependencies/2/logical_path",
        "/dependencies/2/node_id",
        "/dependencies/2/sha256",
        "/node_id",
        "/payload",
        "/payload/activity_root_id",
        "/payload/activity_scope",
        "/payload/activity_scope/allowed_deliverables",
        "/payload/activity_scope/allowed_deliverables/0",
        "/payload/activity_scope/allowed_deliverables/1",
        "/payload/activity_scope/authorization_effect",
        "/payload/activity_scope/correction_boundary",
        "/payload/activity_scope/correction_boundary/0",
        "/payload/activity_scope/correction_boundary/1",
        "/payload/activity_scope/correction_boundary/2",
        "/payload/activity_scope/correction_boundary/3",
        "/payload/activity_scope/correction_boundary/4",
        "/payload/activity_scope/correction_boundary/5",
        "/payload/activity_scope/forbidden_operations",
        "/payload/activity_scope/forbidden_operations/0",
        "/payload/activity_scope/forbidden_operations/1",
        "/payload/activity_scope/forbidden_operations/2",
        "/payload/activity_scope/forbidden_operations/3",
        "/payload/activity_scope/forbidden_operations/4",
        "/payload/activity_scope/forbidden_operations/5",
        "/payload/activity_scope/forbidden_operations/6",
        "/payload/activity_scope/forbidden_operations/7",
        "/payload/activity_scope/forbidden_operations/8",
        "/payload/activity_scope/forbidden_operations/9",
        "/payload/activity_scope/forbidden_operations/10",
        "/payload/activity_scope/forbidden_operations/11",
        "/payload/activity_scope/forbidden_operations/12",
        "/payload/activity_scope/forbidden_operations/13",
        "/payload/activity_scope/forbidden_operations/14",
        "/payload/activity_scope/forbidden_operations/15",
        "/payload/activity_scope/forbidden_operations/16",
        "/payload/activity_scope/forbidden_operations/17",
        "/payload/activity_scope/forbidden_operations/18",
        "/payload/activity_scope/forbidden_operations/19",
        "/payload/activity_scope/mandatory_static_acceptance_checks",
        "/payload/activity_scope/mandatory_static_acceptance_checks/0",
        "/payload/activity_scope/mandatory_static_acceptance_checks/1",
        "/payload/activity_scope/mandatory_static_acceptance_checks/2",
        "/payload/activity_scope/mandatory_static_acceptance_checks/3",
        "/payload/activity_scope/mandatory_static_acceptance_checks/4",
        "/payload/activity_scope/mandatory_static_acceptance_checks/5",
        "/payload/activity_scope/mandatory_static_acceptance_checks/6",
        "/payload/activity_scope/mandatory_static_acceptance_checks/7",
        "/payload/activity_scope/mandatory_static_acceptance_checks/8",
        "/payload/activity_scope/mandatory_static_acceptance_checks/9",
        "/payload/activity_scope/mandatory_static_acceptance_checks/10",
        "/payload/activity_scope/required_return",
        "/payload/activity_scope/required_return/destination",
        "/payload/activity_scope/required_return/implementation_or_execution_authorization",
        "/payload/activity_scope/required_return/include_exact_byte_lengths",
        "/payload/activity_scope/required_return/include_exact_sha256",
        "/payload/activity_scope/stop_conditions",
        "/payload/activity_scope/stop_conditions/0",
        "/payload/activity_scope/stop_conditions/1",
        "/payload/activity_scope/stop_conditions/2",
        "/payload/activity_scope/stop_conditions/3",
        "/payload/activity_scope/stop_conditions/4",
        "/payload/activity_scope/stop_conditions/5",
        "/payload/activity_scope/stop_conditions/6",
        "/payload/activity_scope/stop_conditions/7",
        "/payload/activity_scope/stop_conditions/8",
        "/payload/activity_scope/stop_conditions/9",
        "/payload/activity_scope/stop_conditions/10",
        "/payload/gustavo_authorization",
        "/payload/gustavo_authorization/byte_length",
        "/payload/gustavo_authorization/logical_path",
        "/payload/gustavo_authorization/node_id",
        "/payload/gustavo_authorization/sha256",
        "/payload/input_roots",
        "/payload/input_roots/0",
        "/payload/input_roots/1",
        "/payload/output_roots",
        "/payload/output_roots/0",
        "/payload/prerequisite_acceptance",
        "/payload/prerequisite_acceptance/byte_length",
        "/payload/prerequisite_acceptance/logical_path",
        "/payload/prerequisite_acceptance/node_id",
        "/payload/prerequisite_acceptance/sha256",
        "/payload/run_id",
        "/payload/sentinel_stage_authorization",
        "/payload/sentinel_stage_authorization/byte_length",
        "/payload/sentinel_stage_authorization/logical_path",
        "/payload/sentinel_stage_authorization/node_id",
        "/payload/sentinel_stage_authorization/sha256",
        "/payload/stage_code",
        "/record_id",
        "/schema_id",
        "/status"
      ],
      "field_count_including_containers": 108,
      "cross_field_invariants": [
        "closed_json_value.canonical_commit=70ab8455f33d44b2a690b8c5db58f8ebc545454e",
        "dependencies equal the exact typed semantic references in accepted architecture order",
        "payload.prerequisite_acceptance deep-equals exact A002 NodeRef",
        "COPILOT_ROLE_EXECUTION is explicitly forbidden wherever the record carries forbidden_operations",
        "no administrative role-source identity is a typed NodeRef or S2 scientific/build/audit/gate dependency",
        "payload.gustavo_authorization deep-equals exact K006 NodeRef",
        "payload.sentinel_stage_authorization deep-equals exact K005 NodeRef",
        "payload.run_id=S2_CANDIDATE_08_SPEC_ONLY_DRAFTING_CORRECTION_RUN_03"
      ]
    }
  },
  "scientific_payload_schemas": {
    "A003_CONDITION_LEDGER_PROJECTION_V1": {
      "artifact_node": "A003",
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "schema_id",
        "canonical_commit",
        "universe_count",
        "subclass_counts",
        "row_count",
        "rows"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.a003_condition_ledger_projection.v1]",
        "canonical_commit": "GitCommit40",
        "universe_count": "Count",
        "subclass_counts": "SubclassCounts",
        "row_count": "Count",
        "rows": "Array<ConditionProjectionRow>"
      },
      "additional_fields": false,
      "ordering": [
        "rows ascending by condition_id UTF-8 byte order"
      ],
      "uniqueness": [
        "rows.condition_id"
      ],
      "equations": [
        "universe_count=39693",
        "subclass_counts.UP_DOWN=22012",
        "subclass_counts.OVER_UNDER=1003",
        "subclass_counts.NAMED_OTHER=16678",
        "subclass_counts.total=39693",
        "row_count=universe_count=array_length(rows)"
      ],
      "identity_preimage": "the complete closed JCS object above; its external NodeIdentity SHA-256 equals SHA256(exact UTF-8 JCS bytes)",
      "excluded_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "nullability": "all required top-level fields are non-null; nested null is permitted only where the referenced registered row type is Nullable<T>"
    },
    "A005_REQUEST_PLAN_PROJECTION_V1": {
      "artifact_node": "A005",
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "schema_id",
        "canonical_commit",
        "plan_profile_id",
        "approved_chunk_span_seconds",
        "condition_count",
        "token_count",
        "request_count",
        "rows"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.a005_request_plan_projection.v1]",
        "canonical_commit": "GitCommit40",
        "plan_profile_id": "RecordId",
        "approved_chunk_span_seconds": "UInt32",
        "condition_count": "Count",
        "token_count": "Count",
        "request_count": "Count",
        "rows": "Array<RequestPlanProjectionRow>"
      },
      "additional_fields": false,
      "ordering": [
        "rows ascending by condition_id, outcome_index, chunk_ordinal, start_ts_s, request_id"
      ],
      "uniqueness": [
        "rows.request_id",
        "(condition_id,token_id,outcome_index,chunk_ordinal,start_ts_s,end_ts_s)"
      ],
      "equations": [
        "condition_count=count distinct rows.condition_id",
        "token_count=count distinct (condition_id,token_id,outcome_index)",
        "request_count=array_length(rows)",
        "token_count=2*condition_count for every query-eligible condition represented"
      ],
      "identity_preimage": "the complete closed JCS object above; its external NodeIdentity SHA-256 equals SHA256(exact UTF-8 JCS bytes)",
      "excluded_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "nullability": "all required top-level fields are non-null; nested null is permitted only where the referenced registered row type is Nullable<T>"
    },
    "A007_RAW_PAYLOAD_ROOT_PROJECTION_V1": {
      "artifact_node": "A007",
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "schema_id",
        "canonical_commit",
        "raw_profile_id",
        "planned_request_count",
        "complete_request_count",
        "payload_member_count",
        "payload_total_bytes",
        "entries"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.a007_raw_payload_root_projection.v1]",
        "canonical_commit": "GitCommit40",
        "raw_profile_id": "RecordId",
        "planned_request_count": "Count",
        "complete_request_count": "Count",
        "payload_member_count": "Count",
        "payload_total_bytes": "ByteLength",
        "entries": "Array<RawPayloadProjectionEntry>"
      },
      "additional_fields": false,
      "ordering": [
        "entries ascending by request_id"
      ],
      "uniqueness": [
        "entries.request_id",
        "non-null entries.payload_logical_path",
        "non-null entries.payload_sha256"
      ],
      "equations": [
        "complete_request_count=array_length(entries)",
        "planned_request_count=complete_request_count",
        "payload_member_count=count entries where terminal_class=PAYLOAD_COMPLETE",
        "payload_total_bytes=sum non-null payload_byte_length",
        "every entry terminal_class in {PAYLOAD_COMPLETE,EMPTY_COMPLETE}"
      ],
      "identity_preimage": "the complete closed JCS object above; its external NodeIdentity SHA-256 equals SHA256(exact UTF-8 JCS bytes)",
      "excluded_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ],
      "nullability": "all required top-level fields are non-null; nested null is permitted only where the referenced registered row type is Nullable<T>"
    },
    "PARTITION_MEMBER_JSONL_V2": {
      "media_type": "application/x-ndjson",
      "serialization": "JCS_OBJECT_PER_LINE_UTF8_NO_BOM_LF_FINAL",
      "row_schema": "PerTokenPriceRow",
      "additional_fields": false,
      "ordering": [
        "condition_id,price_ts_utc_ms,row_key_sha256"
      ],
      "identity_preimage": "exact member bytes",
      "excluded_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ]
    },
    "SCIENTIFIC_MANIFEST_PAYLOAD_V2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "schema_id",
        "canonical_commit",
        "deterministic_build_id",
        "members",
        "row_counts"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.scientific_manifest_payload.v2]",
        "canonical_commit": "GitCommit40",
        "deterministic_build_id": "Sha256",
        "members": "Array<ScientificPartitionIdentity>",
        "row_counts": "PartitionCounts"
      },
      "additional_fields": false,
      "ordering": [
        "members exact subclass order UP_DOWN,OVER_UNDER,NAMED_OTHER then outcome_index 0,1"
      ],
      "uniqueness": [
        "members.logical_path",
        "(members.subclass,members.outcome_index)"
      ],
      "equations": [
        "array_length(members)=6",
        "row_counts.partition_count=6",
        "row_counts.row_count=sum members.row_count"
      ],
      "identity_preimage": "complete closed JCS object",
      "excluded_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ]
    },
    "SCIENTIFIC_RECONCILIATION_PAYLOAD_V2": {
      "media_type": "application/json",
      "serialization": "RFC8785_JCS_UTF8_NO_BOM_NO_TRAILING_NEWLINE",
      "required_fields": [
        "schema_id",
        "canonical_commit",
        "deterministic_build_id",
        "population_count",
        "counts",
        "equations",
        "status",
        "effect",
        "stop_code"
      ],
      "fields": {
        "schema_id": "Const[pm_research.s2.scientific_reconciliation_payload.v2]",
        "canonical_commit": "GitCommit40",
        "deterministic_build_id": "Sha256",
        "population_count": "Count",
        "counts": "ClosedCountObject",
        "equations": "Array<EquationResult>",
        "status": "Enum[PASS,FAIL,INCOMPLETE]",
        "effect": "Enum[CLEAR_COMPONENT,BLOCKING_DEFECT,INCOMPLETE_EVIDENCE]",
        "stop_code": "Nullable<RecordId>"
      },
      "additional_fields": false,
      "ordering": [
        "counts.entries by key UTF-8; equations by equation_id"
      ],
      "uniqueness": [
        "counts.entries.key",
        "equations.equation_id"
      ],
      "equations": [
        "population_count=39693",
        "all declared construction categories are disjoint",
        "sum declared construction categories=population_count"
      ],
      "cross_field_invariants": [
        "PASS iff every equation PASS; effect=CLEAR_COMPONENT; stop_code=null",
        "FAIL iff at least one equation FAIL; effect=BLOCKING_DEFECT; stop_code non-null",
        "INCOMPLETE iff no FAIL and at least one equation INCOMPLETE; effect=INCOMPLETE_EVIDENCE; stop_code non-null"
      ],
      "identity_preimage": "complete closed JCS object",
      "excluded_fields": [
        "node_id",
        "record_id",
        "dependencies",
        "created_at_utc_ms",
        "authorization",
        "activity_root",
        "run_id",
        "actor",
        "environment",
        "physical_output_root",
        "handoff_identity",
        "review_identity"
      ]
    }
  },
  "controlling_architecture_metadata": {
    "identity_type": "NonEdgeIdentityMetadata",
    "value": {
      "metadata_node_label": "A002",
      "metadata_logical_path": "project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md",
      "metadata_byte_length": 5854,
      "metadata_sha256": "87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c"
    },
    "authority": "descriptive exact-byte verification only; no direct K008 edge"
  },
  "deterministic_build_preimage_contract": {
    "schema_id": "pm_research.s2.deterministic_build_preimage_contract.v3",
    "output_type": "BuildIdentityPreimage",
    "literal_closed_object_fields": {
      "schema_id": {
        "const": "pm_research.s2.deterministic_build_identity.v3"
      },
      "canonical_commit": {
        "source_node": "K000",
        "source_field": "canonical_commit",
        "type": "GitCommit40"
      },
      "construction_contract": {
        "source_node": "K068",
        "type": "NodeIdentity",
        "fields": [
          "node_id",
          "logical_path",
          "byte_length",
          "sha256"
        ]
      },
      "s4_condition_ledger_projection": {
        "source_node": "A003",
        "type": "NodeIdentity",
        "fields": [
          "node_id",
          "logical_path",
          "byte_length",
          "sha256"
        ]
      },
      "request_plan_projection": {
        "source_node": "A005",
        "type": "NodeIdentity",
        "fields": [
          "node_id",
          "logical_path",
          "byte_length",
          "sha256"
        ]
      },
      "raw_payload_root_projection": {
        "source_node": "A007",
        "type": "NodeIdentity",
        "fields": [
          "node_id",
          "logical_path",
          "byte_length",
          "sha256"
        ]
      },
      "serialization_profile_id": {
        "const": "pm_research.s2.serialization.v1"
      },
      "construction_algorithm_id": {
        "const": "pm_research.s2.construction.v1"
      }
    },
    "literal_jcs_shape": {
      "schema_id": "pm_research.s2.deterministic_build_identity.v3",
      "canonical_commit": {
        "type": "GitCommit40",
        "from": "K000.canonical_commit"
      },
      "construction_contract": {
        "node_id": {
          "const": "K068"
        },
        "logical_path": {
          "type": "RelativePath",
          "from": "K068.NodeIdentity.logical_path"
        },
        "byte_length": {
          "type": "ByteLength",
          "from": "K068.NodeIdentity.byte_length"
        },
        "sha256": {
          "type": "Sha256",
          "from": "K068.NodeIdentity.sha256"
        }
      },
      "s4_condition_ledger_projection": {
        "node_id": {
          "const": "A003"
        },
        "logical_path": {
          "type": "RelativePath",
          "from": "A003.NodeIdentity.logical_path"
        },
        "byte_length": {
          "type": "ByteLength",
          "from": "A003.NodeIdentity.byte_length"
        },
        "sha256": {
          "type": "Sha256",
          "from": "A003.NodeIdentity.sha256"
        }
      },
      "request_plan_projection": {
        "node_id": {
          "const": "A005"
        },
        "logical_path": {
          "type": "RelativePath",
          "from": "A005.NodeIdentity.logical_path"
        },
        "byte_length": {
          "type": "ByteLength",
          "from": "A005.NodeIdentity.byte_length"
        },
        "sha256": {
          "type": "Sha256",
          "from": "A005.NodeIdentity.sha256"
        }
      },
      "raw_payload_root_projection": {
        "node_id": {
          "const": "A007"
        },
        "logical_path": {
          "type": "RelativePath",
          "from": "A007.NodeIdentity.logical_path"
        },
        "byte_length": {
          "type": "ByteLength",
          "from": "A007.NodeIdentity.byte_length"
        },
        "sha256": {
          "type": "Sha256",
          "from": "A007.NodeIdentity.sha256"
        }
      },
      "serialization_profile_id": "pm_research.s2.serialization.v1",
      "construction_algorithm_id": "pm_research.s2.construction.v1"
    },
    "hash_equation": "deterministic_build_id=SHA256(UTF8(RFC8785_JCS(actual BuildIdentityPreimage object)))",
    "forbidden_aliases": [
      "id",
      "path"
    ],
    "forbidden_inputs": [
      "created_at_utc_ms",
      "authorization",
      "activity_root",
      "run_id",
      "actor",
      "environment",
      "physical_output_root",
      "handoff_identity",
      "review_identity",
      "K082"
    ]
  },
  "schema_literal_edge_rule": "objects inside exact_current_record_schemas.closed_json_value are SchemaLiteral validation data; the K008 edge extractor MUST NOT traverse them; their own K006/K005/K007 edges are derived only when validating those external records against their node ref_bindings",
  "static_validation_contract": {
    "required_checks": [
      "RAW_K008_BYTE_LENGTH_AND_SHA256_MATCH_SUBMITTED_IDENTITY",
      "RAW_K009_BYTE_LENGTH_AND_EXTERNALLY_SUPPLIED_SHA256_MATCH_SUBMITTED_IDENTITY",
      "K008_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE",
      "K009_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE",
      "K008_PAYLOAD_VALIDATES_DOCUMENT_CANDIDATE_V1",
      "K009_PAYLOAD_VALIDATES_CANDIDATE08_PROFESSOR_HANDOFF_V1",
      "K009_SELF_EXCLUDING_PROJECTION_IDENTITY_MATCHES",
      "K009_SELF_IDENTITY_ENUM_VALUE_IS_REGISTERED",
      "PROSE_AND_REGISTRY_TYPE_REFERENCES_AGREE",
      "RECORDID_BOUND_IS_160_UTF8_BYTES_EVERYWHERE",
      "RELATIVEPATH_NFC_IS_MANDATORY_EVERYWHERE",
      "exact K006/K005/K007 raw identity and JCS validation",
      "every node artifact_profile_id resolves",
      "every type reference resolves",
      "every ref_binding storage is valid for its profile",
      "schema-derived edges equal Appendix A",
      "rank violations and cycles absent",
      "P00-P18 tuple expansion has no overlap",
      "global reducer vectors are enum-valid and contain no placeholders",
      "safe-span representative domain enumeration yields exactly one rule",
      "terminal mapping representative domain enumeration yields exactly one rule",
      "activity-free scientific schemas contain no provenance fields",
      "exact-clear witness reduces to COMPLETE/APPROVE",
      "exact active K006/K005/K007 raw bytes and closed-schema deep equality",
      "Copilot role-source context is evidence-only and creates zero NodeRef edges",
      "Copilot role-source repository and commit absent from deterministic build preimage and all scientific payload schemas",
      "Copilot role execution status is NOT_PERFORMED"
    ],
    "required_results": {
      "node_count": 166,
      "edge_count": 678,
      "unknown_type_count": 0,
      "missing_profile_count": 0,
      "binding_issue_count": 0,
      "rank_violation_count": 0,
      "cycle_count": 0,
      "condition_state_class_count": 19,
      "condition_state_legal_tuple_count": 31,
      "condition_state_overlap_count": 0,
      "global_reducer_row_count": 153,
      "global_vector_invalid_count": 0,
      "safe_span_representative_unmapped_or_multi_match_count": 0,
      "terminal_representative_unmapped_count": 0,
      "scientific_payload_provenance_contamination_count": 0,
      "active_authorization_schema_matches": "3/3",
      "copilot_role_source_edge_count": 0,
      "copilot_role_source_scientific_dependency_count": 0,
      "copilot_role_execution": "NOT_PERFORMED",
      "raw_k008_identity_match": true,
      "raw_k009_external_identity_match": true,
      "k008_normative_payload_count": 1,
      "k009_normative_payload_count": 1,
      "k008_assigned_profile_valid": true,
      "k009_assigned_profile_valid": true,
      "k009_self_projection_valid": true,
      "k009_self_identity_enum_registered": true,
      "prose_registry_type_agreement": true,
      "recordid_max_utf8_bytes": 160,
      "recordid_bound_agreement": true,
      "relativepath_normalization": "NFC_REQUIRED_REJECT_NON_NFC",
      "relativepath_nfc_agreement": true,
      "static_submission_gate": "CLEAR"
    },
    "mandatory_raw_deliverable_checks": [
      "RAW_K008_BYTE_LENGTH_AND_SHA256_MATCH_SUBMITTED_IDENTITY",
      "RAW_K009_BYTE_LENGTH_AND_EXTERNALLY_SUPPLIED_SHA256_MATCH_SUBMITTED_IDENTITY",
      "K008_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE",
      "K009_NORMATIVE_PAYLOAD_EXTRACTS_EXACTLY_ONCE",
      "K008_PAYLOAD_VALIDATES_DOCUMENT_CANDIDATE_V1",
      "K009_PAYLOAD_VALIDATES_CANDIDATE08_PROFESSOR_HANDOFF_V1",
      "K009_SELF_EXCLUDING_PROJECTION_IDENTITY_MATCHES",
      "K009_SELF_IDENTITY_ENUM_VALUE_IS_REGISTERED",
      "PROSE_AND_REGISTRY_TYPE_REFERENCES_AGREE",
      "RECORDID_BOUND_IS_160_UTF8_BYTES_EVERYWHERE",
      "RELATIVEPATH_NFC_IS_MANDATORY_EVERYWHERE"
    ],
    "raw_deliverable_failure_effect": "ANY_FAILURE_BLOCKS_SUBMISSION_AND_PROHIBITS_STATIC_CLEAR"
  },
  "administrative_role_source_context": {
    "context_type": "AdministrativeRoleSourceContext",
    "repository": "rigolugo/pm_copilot_roles",
    "immutable_commit": "a7df418216cb7355b003164b8b509e40081cdbdc",
    "canonical_state": "INSTALLED_AND_SENTINEL_VERIFIED",
    "evidence_only": true,
    "role_execution_authorized": false,
    "required_reads": [
      "project_context/GITHUB_COPILOT_CLI_ROLE_SOURCE_POINTER.md",
      "project_context/administrative_tools/github_copilot_cli/README_FIRST.md",
      "project_context/administrative_tools/github_copilot_cli/SENTINEL_CANONICAL_INSTALLATION_VERIFICATION.md"
    ],
    "s2_architecture_dependency": false,
    "s2_scientific_dependency": false,
    "s2_provenance_dependency": false,
    "s2_build_identity_dependency": false,
    "s2_audit_dependency": false,
    "s2_gate_dependency": false,
    "authorization_effect": "NONE",
    "role_execution_status": "NOT_PERFORMED"
  }
}
```

## Appendix A — Authoritative direct-edge registry and schema-derived equality

An edge `Y→X` exists iff node Y has a typed `ref_binding` targeting X. The binding is either a serialized `ARTIFACT_FIELD` or an explicit `SCHEMA_EDGE_CONTRACT_NOT_SERIALIZED` for an activity-free scientific payload. `NodeIdentity`, `ArtifactIdentity`, `ScientificPayloadIdentity`, and `NonEdgeIdentityMetadata` never create edges. The table below is the accepted amended direct-edge registry. It contains exactly 166 source nodes/node families and 678 direct edges.

| Target | Amended rank | Exact ordered direct predecessors |
|---|---:|---|
| `K000` | `1000` | none |
| `K001` | `1010` | `K000` |
| `K002` | `1020` | `K000`, `K001` |
| `A000` | `1021` | `K000`, `K001`, `K002` |
| `A001` | `1022` | `K002`, `A000` |
| `A002` | `1023` | `K002`, `A000`, `A001` |
| `K006` | `1050` | `A002` |
| `K005` | `1060` | `A002`, `K006` |
| `K007` | `1070` | `A002`, `K006`, `K005` |
| `K008` | `1080` | `K007` |
| `K009` | `1090` | `K006`, `K005`, `K007`, `K008` |
| `K010` | `1100` | `K008`, `K009` |
| `K011` | `1110` | `K008`, `K010` |
| `K013` | `1120` | `K011` |
| `K012` | `1130` | `K011`, `K013` |
| `K014` | `1140` | `K011`, `K013`, `K012` |
| `K015` | `1150` | `K014` |
| `K016` | `1160` | `K013`, `K012`, `K014`, `K015` |
| `K017` | `1170` | `K015`, `K016` |
| `K018` | `1180` | `K015`, `K017` |
| `K020` | `1190` | `K018` |
| `K019` | `1200` | `K018`, `K020` |
| `K021` | `1210` | `K018`, `K020`, `K019` |
| `K022` | `1220` | `K021` |
| `K023` | `1230` | `K020`, `K019`, `K021`, `K022` |
| `K024` | `1240` | `K022`, `K023` |
| `K025` | `1250` | `K022`, `K024` |
| `K027` | `1260` | `K018`, `K025` |
| `K026` | `1270` | `K018`, `K025`, `K027` |
| `K028` | `1280` | `K018`, `K025`, `K027`, `K026` |
| `K029` | `1290` | `K028` |
| `K030` | `1300` | `K027`, `K026`, `K028`, `K029` |
| `K031` | `1310` | `K029`, `K030` |
| `K032` | `1320` | `K029`, `K031` |
| `K034` | `1330` | `K032` |
| `K033` | `1340` | `K032`, `K034` |
| `K035` | `1350` | `K032`, `K034`, `K033` |
| `K036` | `1360` | `K035` |
| `K037` | `1370` | `K035`, `K036` |
| `A003` | `1371` | `K037` |
| `A004` | `1372` | `K035`, `K036`, `K037`, `A003` |
| `K038` | `1380` | `K035`, `K037`, `A003`, `A004` |
| `K039` | `1390` | `K034`, `K033`, `K035`, `K036`, `K037`, `A003`, `A004`, `K038` |
| `K040` | `1400` | `K038`, `K039` |
| `K041` | `1410` | `K038`, `K040` |
| `K043` | `1420` | `K041` |
| `K042` | `1430` | `K041`, `K043` |
| `K044` | `1440` | `K041`, `K043`, `K042` |
| `K045` | `1450` | `K044` |
| `K046` | `1460` | `K044`, `K045` |
| `K047` | `1470` | `K044`, `K045`, `K046` |
| `K048` | `1480` | `K043`, `K042`, `K044`, `K045`, `K046`, `K047` |
| `K049` | `1490` | `K045`, `K047`, `K048` |
| `K050` | `1500` | `K048`, `K049` |
| `K051` | `1510` | `K049`, `K050` |
| `K052P` | `1520` | `K050`, `K051` |
| `K052N` | `1530` | `K048`, `K050` |
| `K054` | `1540` | `K041`, `K051`, `K052P` |
| `K053` | `1550` | `K041`, `K051`, `K052P`, `K054` |
| `K055` | `1560` | `K041`, `K051`, `K052P`, `K054`, `K053` |
| `K056F` | `1570` | `K037`, `K051`, `K055` |
| `K057` | `1580` | `K055`, `K056F` |
| `A005` | `1581` | `K056F`, `K057` |
| `A006` | `1582` | `K055`, `K056F`, `K057`, `A005` |
| `K058F` | `1590` | `K055`, `K057` |
| `K059F` | `1600` | `K055`, `K056F`, `K058F` |
| `K060` | `1610` | `K055`, `K058F`, `K059F` |
| `K061` | `1620` | `K055`, `K057`, `K059F`, `K060` |
| `K062` | `1630` | `K055`, `K060`, `K061` |
| `K063` | `1640` | `K062` |
| `A007` | `1641` | `K060`, `K061`, `K062`, `K063` |
| `A008` | `1642` | `K055`, `K060`, `K061`, `K062`, `K063`, `A007` |
| `K064` | `1650` | `K037`, `A003`, `A004`, `K057`, `A005`, `A006`, `K059F`, `K061`, `K063`, `A007`, `A008` |
| `K065` | `1660` | `K054`, `K053`, `K055`, `K057`, `A005`, `A006`, `K060`, `K061`, `K062`, `K063`, `A007`, `A008`, `K064` |
| `K066` | `1670` | `K064`, `K065` |
| `K067` | `1680` | `K064`, `K066` |
| `K068` | `1690` | `K011`, `K018` |
| `K070` | `1700` | `K067`, `K068` |
| `K069` | `1710` | `K067`, `K068`, `K070` |
| `K071` | `1720` | `K067`, `K068`, `K070`, `K069` |
| `K072` | `1730` | `K000`, `K068`, `A003`, `A005`, `A007` |
| `K073F` | `1740` | `A007`, `K072` |
| `K074` | `1750` | `K072`, `K073F` |
| `K075` | `1760` | `A003`, `A005`, `A007`, `K072`, `K074` |
| `K076` | `1770` | `K070`, `K069`, `K071`, `A004`, `A006`, `A008`, `K072`, `K073F`, `K074`, `K075` |
| `K077` | `1780` | `K070`, `K069`, `K071`, `K074`, `K075`, `K076` |
| `K078` | `1790` | `K075`, `K077` |
| `K079` | `1800` | `K075`, `K078` |
| `K080P` | `1810` | `K074`, `K075`, `K077`, `K079` |
| `K080A` | `1820` | `K077`, `K079` |
| `K081P` | `1830` | `K080P` |
| `K081A` | `1840` | `K080A` |
| `K082` | `1850` | `K080P`, `K081P` |
| `K083P` | `1860` | `K081P`, `K082` |
| `K083R` | `1870` | `K080P`, `K081P` |
| `K083A` | `1880` | `K080A`, `K081A` |
| `K085` | `1890` | `K079`, `K082`, `K083P` |
| `K084` | `1900` | `K079`, `K082`, `K083P`, `K085` |
| `K086` | `1910` | `K079`, `K082`, `K083P`, `K085`, `K084` |
| `K087` | `1920` | `K037`, `K074`, `K075`, `K082`, `K086` |
| `K088` | `1930` | `K037`, `K075`, `K086`, `K087` |
| `K089` | `1940` | `K084`, `K085`, `K086`, `K087`, `K088` |
| `K090` | `1950` | `K088`, `K089` |
| `K091` | `1960` | `K088`, `K090` |
| `K093` | `1970` | `K091` |
| `K092` | `1980` | `K091`, `K093` |
| `K094` | `1990` | `K091`, `K093`, `K092` |
| `K095` | `2000` | `K093`, `K092`, `K094`, `K072`, `A003`, `A005`, `A007` |
| `K096F` | `2010` | `A007`, `K072` |
| `K097` | `2020` | `K072`, `K096F` |
| `K098` | `2030` | `A003`, `A005`, `A007`, `K072`, `K097` |
| `K099` | `2040` | `K093`, `K092`, `K094`, `K095`, `A004`, `A006`, `A008`, `K096F`, `K097`, `K098` |
| `K100` | `2050` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K094` |
| `K101` | `2060` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K099`, `K100` |
| `K102` | `2070` | `K093`, `K092`, `K094`, `K095`, `K099`, `K100`, `K101` |
| `K103` | `2080` | `K101`, `K102` |
| `K104` | `2090` | `K101`, `K103` |
| `K106` | `2100` | `K104` |
| `K105` | `2110` | `K104`, `K106` |
| `K107` | `2120` | `K104`, `K106`, `K105` |
| `K108` | `2130` | `K037`, `K038`, `K059F`, `K064`, `K075`, `K088`, `K101`, `K107` |
| `K109` | `2140` | `K000`, `K001`, `A002`, `K011`, `K068` |
| `K110` | `2150` | `K036`, `K037`, `A003`, `A004`, `K038`, `K041` |
| `K111` | `2160` | `K037`, `K038` |
| `K112` | `2170` | `K037`, `K038` |
| `K113` | `2180` | `K045`, `K046`, `K047`, `K049`, `K050`, `K051`, `K052P` |
| `K114` | `2190` | `K051`, `K052P`, `K056F`, `K057`, `A005`, `A006` |
| `K115` | `2200` | `K057`, `A005`, `A006`, `K058F`, `K059F`, `K061`, `K064` |
| `K116` | `2210` | `K060`, `K061`, `K062`, `K063`, `A007`, `A008` |
| `K117` | `2220` | `K056F`, `K057`, `A005`, `K058F`, `K059F`, `K064` |
| `K118` | `2230` | `K057`, `A005`, `K059F`, `K073F`, `K074`, `K096F`, `K097` |
| `K119` | `2240` | `A003`, `A004`, `A005`, `A006`, `A007`, `A008`, `K072`, `K073F`, `K074`, `K075`, `K076` |
| `K120` | `2250` | `K073F`, `K074`, `K075` |
| `K121` | `2260` | `K080P`, `K081P`, `K082`, `K083P`, `K084`, `K085`, `K086` |
| `K122` | `2270` | `K074`, `K075`, `K082`, `K087`, `K088` |
| `K123` | `2280` | `K037`, `K087`, `K088`, `K108` |
| `K124` | `2290` | `K000`, `K068`, `A003`, `A004`, `A005`, `A006`, `A007`, `A008`, `K072`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098` |
| `K125` | `2300` | `K072`, `A003`, `A005`, `A007`, `K073F`, `K074`, `K075`, `K096F`, `K097`, `K098`, `K100`, `K101` |
| `K126` | `2310` | `K037`, `K038`, `K059F`, `K064`, `K075`, `K088`, `K101`, `K108` |
| `A009` | `2315` | `K106`, `K105`, `K107`, `K108`, `K109`, `K110`, `K111`, `K112`, `K113`, `K114`, `K115`, `K116`, `K117`, `K118`, `K119`, `K120`, `K121`, `K122`, `K123`, `K124`, `K125`, `K126` |
| `K127` | `2320` | `A002`, `K011`, `K018`, `K025`, `K032`, `K041`, `K051`, `K052P`, `K067`, `K068`, `K079`, `K082`, `K083P`, `K091`, `K104`, `K006`, `K005`, `K007`, `K009`, `K013`, `K012`, `K014`, `K016`, `K020`, `K019`, `K021`, `K023`, `K027`, `K026`, `K028`, `K030`, `K034`, `K033`, `K035`, `K039`, `K043`, `K042`, `K044`, `K048`, `K054`, `K053`, `K055`, `K065`, `K070`, `K069`, `K071`, `K077`, `K085`, `K084`, `K086`, `K089`, `K093`, `K092`, `K094`, `K102`, `K106`, `K105`, `K107`, `A009` |
| `K128` | `2330` | `K107`, `K109`, `K110`, `K111`, `K112`, `K113`, `K114`, `K115`, `K116`, `K117`, `K118`, `K119`, `K120`, `K121`, `K122`, `K123`, `K124`, `K125`, `K126`, `K127` |
| `K129` | `2340` | `K107`, `K108`, `K128` |
| `K130` | `2350` | `K129` |
| `K131` | `2360` | `K108`, `K128`, `K129`, `K130` |
| `K132` | `2370` | `K106`, `K105`, `K107`, `K108`, `K128`, `K129`, `K130`, `K131` |
| `K133` | `2380` | `K132` |
| `K134` | `2390` | `K132`, `K133` |
| `K135` | `2400` | `K129`, `K131`, `K132`, `K134` |
| `K136` | `2410` | `K134`, `K135` |
| `K137` | `2420` | `K134`, `K135`, `K136` |
| `K139` | `2430` | `K137` |
| `K138` | `2440` | `K137`, `K139` |
| `K140` | `2450` | `K137`, `K139`, `K138` |
| `K141` | `2460` | `K037`, `K108`, `K129`, `K134`, `K135`, `K139`, `K138`, `K140` |
| `K142I` | `2470` | `K139`, `K138`, `K140`, `K141` |
| `K143I` | `2480` | `K139`, `K138`, `K140`, `K141`, `K142I` |
| `K144I` | `2490` | `K143I` |
| `K142E` | `2500` | `A002`, `K011`, `K139`, `K138`, `K140`, `K141` |
| `K143E` | `2510` | `K139`, `K138`, `K140`, `K141`, `K142E` |
| `K144E` | `2520` | `K139`, `K138`, `K140`, `K141`, `K142E`, `K143E` |
| `K145E` | `2530` | `K144E` |
| `K146E` | `2540` | `K142E`, `K143E`, `K144E`, `K145E` |
| `K148` | `2550` | `K146E` |
| `K147` | `2560` | `K146E`, `K148` |
| `K149` | `2570` | `K146E`, `K148`, `K147` |

### Appendix A.1 Declarative equality attestation

The §23 registry was statically resolved from every semantic `ref_binding`. It is conforming only when an independent mechanical scan returns:

```json
{
  "declared_node_count":166,
  "declared_edge_count":678,
  "schema_derived_node_count":166,
  "schema_derived_edge_count":678,
  "missing_edges":[],
  "extra_edges":[],
  "rank_violations":[],
  "cycles":[]
}
```

Any nonempty array is `PROVENANCE_EDGE_SET_MISMATCH` and blocks specification acceptance or later implementation conformance.

## Appendix B — Node/path materialization rules

1. Nodes with fixed canonical paths use §4.2.
2. Every other singleton node uses `nodes/<NodeId>/artifact.json` under the exact workflow root.
3. K130 uses Markdown; K142E uses its exact candidate filename.
4. Family nodes use §4.3 and an exact family identity manifest.
5. A node's `logical_path`, byte length, and SHA-256 are immutable after first valid finalization.
6. Re-emitting identical bytes is idempotent. A same-path, different-byte result is blocking.
7. A review or acceptance record MUST bind exact predecessor bytes, not only IDs.
8. No optional file may be referenced when absent. Presence/absence branches use separate nodes.

## Appendix C — Canonical input-set K001

K001 is a JCS manifest, sorted by path, that binds exact raw byte length and SHA-256 for the following canonical paths at K000:

```text
START_HERE.md
project_context/START_HERE.md
project_context/GUARDRAILS.md
project_context/PROJECT_STATE.md
project_context/DECISION_LOG.md
project_context/CLOSED_FINDINGS.md
project_context/ARTIFACT_INDEX.md
project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md
project_context/DATA_CONTRACTS_named_binary_probe.md
project_context/PRICE_INPUT_CONTRACT_named_binary_probe.md
project_context/SPEC_named_binary_probe.md
project_context/SPEC_price_source_s1_coverage.md
project_context/S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02.md
project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03.md
project_context/S2_PER_TOKEN_PRICE_ARTIFACT_ARCHITECTURE_NORMALIZATION_CANDIDATE_03_AMENDMENT_01.md
project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A001_SENTINEL_COMBINED_ARCHITECTURE_REVIEW_RECORD_CANDIDATE_01.md
project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md
```

Failure to load or hash any required path is `STOP_CANONICAL_BASE_MISMATCH`. K001 is canonical provenance, not empirical evidence and not activity authorization.
