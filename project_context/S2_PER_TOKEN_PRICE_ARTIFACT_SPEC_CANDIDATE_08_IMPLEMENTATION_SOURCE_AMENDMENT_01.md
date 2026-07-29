# S2 Candidate 08 Implementation-Source Authoring Amendment 01

## 1. Status

| Field | Value |
|---|---|
| Document ID | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08_IMPLEMENTATION_SOURCE_AMENDMENT_01` |
| Status | `SPEC_ONLY_AMENDMENT_CANDIDATE` |
| Authoring mode | `AMEND` |
| Prepared by | Professor |
| Independent reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Exact verified canonical `main` | `ddf41003fb16aa091c2a899d7c17754e89341cc7` |
| Accepted base specification | `S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08` |
| Accepted base node | `K011` |
| Requested Sentinel decision | `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION` |
| Authorization effect | `NONE` |

**Purpose.** Resolve the accepted Sentinel finding
`ACCEPT FINDING — S2_IMPLEMENTATION_SOURCE_AUTHORIZATION_BLOCKED_BY_PATH_LAYOUT_AND_REGISTRY_PROVENANCE`
without implementing source, changing accepted scientific behavior, or authorizing implementation or execution.

**Checkable completion sentence.** This amendment is complete when Sentinel can verify that one exact fourteen-file regular-package matrix is implementable in the canonical flat repository layout, the exact accepted Candidate-08 §23 registry and reducer projection have deterministic generated-literal identities and drift checks, K015 ordering is total, K016 self-identity is exactly null, and no implementation-source activity can start before a fresh post-amendment authorization chain exists.

## 2. Canonical base and evidence classification

### 2.1 Exact accepted inputs

| Item | Exact identity |
|---|---|
| Canonical `main` | `ddf41003fb16aa091c2a899d7c17754e89341cc7` |
| A002 path | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_A002_ACCEPTED_CONTROLLING_ARCHITECTURE_SET_RECORD_CANDIDATE_01.md` |
| A002 bytes / SHA-256 | `5854` / `87146e9e3a5d0501c04518ff0fd818c721c1b92cab684eec0b54d9605980a94c` |
| Accepted K008 path | `project_context/S2_PER_TOKEN_PRICE_ARTIFACT_SPEC_CANDIDATE_08.md` |
| Accepted K008 bytes / SHA-256 | `776003` / `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63` |
| K010 review | `nodes/K010/artifact.json`; `1504` bytes; SHA-256 `e34ddcf51b8b908570de9b4cd4af520114e46bc848cfc00110bf4874dfafa17b` |
| K011 acceptance | `nodes/K011/artifact.json`; `1134` bytes; SHA-256 `4f3f044d78d6ddc95d2c21dba3257f459e15810acc27f27cd36a1f2d8b0f264` |
| Canonical packaging file | `pyproject.toml`; flat package entry point `pm_research.cli:main`; no `src` mapping |
| Existing regular package root | `pm_research/__init__.py` |

A002 and Amendment 01 continue to control the accepted architecture. Architecture Candidates 01 and 02 remain blocked historical submissions and are not normative dependencies.

### 2.2 Accepted finding

The named Sentinel finding is treated as `ACCEPTED` review input. Its material technical predicates were independently confirmed from canonical files:

1. Candidate 08 §23 currently names fourteen paths under `src/pm_research/named_binary_probe/s2/`.
2. Canonical source uses the top-level regular package `pm_research/`.
3. Canonical `pyproject.toml` contains no `src`-layout mapping.
4. Candidate 08 does not specify how `schema_registry.py` and `state_reducers.py` preserve the exact §23 content.
5. `source_matrix.v1` orders K015 `file_matrix` by logical-path UTF-8.
6. K016 permits a nullable `/payload/self_identity` but does not choose one value for the implementation-source handoff.

## 3. Scope

### 3.1 In scope

This amendment changes only:

1. §23 top-level `implementation_source_matrix`;
2. §23 `artifact_profiles.source_matrix.v1` constraints and ordering interpretation;
3. §23 `nodes.K015.node_specific_constants.exact_source_file_matrix`;
4. §23 `nodes.K015.node_specific_invariants`;
5. §23 `nodes.K016.node_specific_constants` and `node_specific_invariants`;
6. implementation-source handoff citation language;
7. deterministic registry/reducer materialization and source-review obligations;
8. implementation-source authorization prerequisites and typed stops.

### 3.2 Out of scope

This amendment does not change:

- A002 scientific or state architecture;
- the 39,693-condition population or subclass counts;
- independent token-specific acquisition;
- synthesis and winner-leakage prohibitions;
- safe-span, endpoint, retry, construction, alignment, rebuild, audit, gate, or Stage-10 behavior;
- the accepted K008 raw bytes;
- any existing canonical file;
- implementation or test source;
- any execution or empirical state.

## 4. Exact path and package model

### 4.1 Selected model

The implementation-source package MUST be the regular Python subpackage:

`pm_research.named_binary_probe_s2`

Its repository directory MUST be:

`pm_research/named_binary_probe_s2/`

This is a one-level regular subpackage beneath the existing regular package root `pm_research`. The matrix includes its own `__init__.py`.

The implementation MUST NOT:

- create or use a `src/` directory;
- use `pm_research.named_binary_probe.s2`;
- depend on an implicit namespace package;
- omit the new subpackage `__init__.py`;
- modify `pm_research/__init__.py`;
- modify `pyproject.toml`;
- insert repository paths into `sys.path`;
- use dynamic import-path mutation;
- claim wheel or sdist inclusion as accepted evidence.

The package's internal imports MUST be either explicit relative imports within
`pm_research.named_binary_probe_s2` or absolute imports beginning with
`pm_research.named_binary_probe_s2`.

This amendment defines repository source-tree implementability only. Distribution-build inclusion is not evaluated or authorized. A later requirement to change packaging configuration MUST stop as `STOP_PACKAGING_SCOPE_NOT_AUTHORIZED` and return to Sentinel.

### 4.2 Exact proposed implementation-source matrix

The exact matrix contains fourteen rows and is already ordered by
`logical_path.encode("utf-8")` ascending. All paths are NFC ASCII and therefore have one UTF-8 representation.

```json
[
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
```

Set equation:

`K015_PATH_SET = exactly the fourteen logical_path values above`

Role equation:

`role_by_path[p] = the role paired with p above`

No role may be reassigned during sorting. No fifteenth source path, package initializer, configuration file, generated file, compatibility shim, or helper is permitted by this amendment.

## 5. Normative §23 replacements

### 5.1 Replace top-level `implementation_source_matrix`

The §23 top-level `implementation_source_matrix` MUST be replaced in full by the exact array in §4.2.

### 5.2 Amend `artifact_profiles.source_matrix.v1`

Retain all existing fields and replace/add these constraints:

```json
{
  "ordering": [
    "file_matrix ascending by logical_path UTF-8 bytes after required NFC validation"
  ],
  "uniqueness": [
    "file_matrix.logical_path"
  ],
  "equations": [
    "file_count=14"
  ],
  "constraints": [
    "file_matrix path-role pairs equal the exact implementation_source_matrix",
    "no unlisted source path",
    "each row has logical_path, role, language=PYTHON, byte_length, sha256, required=true",
    "logical_path is already NFC and is not normalized during emission",
    "roles remain attached to paths before and after ordering",
    "K015 ordering is independent of role order and authoring order"
  ]
}
```

The profile-order algorithm is exact:

1. validate each submitted row against its exact path-role constant;
2. reject duplicate or unlisted paths;
3. reject a role mismatch;
4. reject non-NFC path text;
5. sort rows ascending by raw UTF-8 bytes of `logical_path`;
6. emit the sorted array;
7. require emitted path sequence to equal the §4.2 sequence exactly.

### 5.3 Replace `nodes.K015.node_specific_constants.exact_source_file_matrix`

Replace that constant in full with the exact array in §4.2.

Add:

```json
{
  "package_model": {
    "repository_package_root": "pm_research",
    "implementation_subpackage": "pm_research.named_binary_probe_s2",
    "repository_directory": "pm_research/named_binary_probe_s2",
    "regular_package_required": true,
    "namespace_package_permitted": false,
    "src_layout_permitted": false,
    "pyproject_change_permitted": false
  },
  "file_count": 14,
  "k015_emit_order": "LOGICAL_PATH_UTF8_ASCENDING"
}
```

### 5.4 Replace/add `nodes.K015.node_specific_invariants`

K015 MUST satisfy all of the following:

1. its `file_matrix` contains exactly fourteen rows;
2. its emitted sequence equals §4.2 exactly;
3. every role remains bound to its exact path;
4. every row contains the submitted raw file byte length and SHA-256;
5. no source path outside §4.2 exists in the implementation-source candidate;
6. no source path uses `src/`;
7. no namespace-package or packaging-configuration fallback is used;
8. matrix validation precedes K016 creation.

Any violation is `STOP_K015_SOURCE_MATRIX_INVALID`.

## 6. Normative registry and reducer materialization

### 6.1 Selected mechanism

The implementation MUST use generated literal constants embedded in
`pm_research/named_binary_probe_s2/schema_registry.py`.

It MUST NOT:

- read K008 at runtime;
- parse Markdown at runtime;
- fetch K008 from GitHub or another network source;
- use an environment-selected registry;
- maintain a second hand-edited registry;
- silently regenerate from different K008 bytes.

### 6.2 Exact K008 extraction contract

The source-authoring materializer MUST:

1. read only the exact accepted K008 bytes identified in §2.1;
2. verify raw byte length `776003`;
3. verify raw SHA-256 `b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63`;
4. decode strict UTF-8;
5. require no BOM and LF line endings;
6. locate exactly one heading line:
   `## 23. Normative machine-extractable schema registry`;
7. locate the first fenced `json` block after that heading;
8. require the block to parse as one JSON object;
9. require no second §23 registry block;
10. serialize the parsed object as RFC 8785 JCS UTF-8, no BOM, no trailing newline.

The exact accepted §23 JCS identity is:

| Field | Value |
|---|---|
| Byte length | `479463` |
| SHA-256 | `82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff` |

### 6.3 `schema_registry.py` obligations

`schema_registry.py` MUST contain exactly one generated base64 literal whose decoded bytes are the §23 JCS bytes in §6.2.

The module MUST declare these exact constants:

```text
SOURCE_K008_BYTE_LENGTH = 776003
SOURCE_K008_SHA256 = "b6d8b4dde25a67d8e4386762e320600f0778580aee290d3552949c77102e0e63"
REGISTRY_JCS_BYTE_LENGTH = 479463
REGISTRY_JCS_SHA256 = "82038603fb5cfd564b8563731e772c03d29c6ff6bdc862040ea26e0463ec97ff"
REGISTRY_GENERATION_PROFILE = "K008_SECTION_23_FIRST_JSON_BLOCK_RFC8785_JCS_V1"
```

The generated base64 literal MAY be split into adjacent ASCII source chunks for formatting. Concatenation order is source order. No chunk may be selected conditionally.

The module's public registry object MUST be derived only from the decoded literal and MUST be exposed as an immutable/frozen structure. No caller may mutate the normative object.

### 6.4 Reducer projection and `state_reducers.py`

The reducer projection is the closed JCS object:

```json
{
  "condition_state_classes": "<exact value from registry key condition_state_classes>",
  "global_state_reducer": "<exact value from registry key global_state_reducer>"
}
```

The quoted placeholders above denote exact key selection, not serialized placeholder strings. The projection algorithm constructs an object containing exactly those two keys and their complete values from the decoded registry, then RFC 8785 JCS-serializes it.

Exact reducer-projection identity:

| Field | Value |
|---|---|
| Byte length | `66232` |
| SHA-256 | `266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c` |

`state_reducers.py` MUST import the immutable registry accessor from
`schema_registry.py`. It MUST NOT contain a duplicate registry or reducer literal.

It MUST declare:

```text
REDUCER_PROJECTION_JCS_BYTE_LENGTH = 66232
REDUCER_PROJECTION_JCS_SHA256 = "266d540dfd8481cd084d155ae8cb6f08b740f2c4aead70d9d5e5f9c1588da63c"
```

All implemented global and condition reducers MUST be traceable to the selected projection. A reducer branch absent from the projection MUST NOT be invented.

### 6.5 Drift prevention and source-review obligations

Before Sentinel may accept K015, source review MUST statically establish:

1. exact K008 source identity constants;
2. unique §23 extraction profile;
3. decoded registry literal length and SHA-256;
4. parsed registry top-level key set;
5. reducer-projection length and SHA-256;
6. absence of runtime K008 reads;
7. absence of network registry acquisition;
8. absence of duplicate normative reducer literals;
9. no hand-edited semantic delta from §23;
10. exact matrix and role conformance.

A mismatch MUST produce one typed stop and no accepted K015:

- `STOP_REGISTRY_SOURCE_IDENTITY_MISMATCH`;
- `STOP_REGISTRY_EXTRACTION_AMBIGUOUS`;
- `STOP_REGISTRY_JCS_IDENTITY_MISMATCH`;
- `STOP_REDUCER_PROJECTION_IDENTITY_MISMATCH`;
- `STOP_GENERATED_LITERAL_DRIFT`.

Static source review may inspect text, AST, literal bytes, hashes, and JSON. This amendment does not authorize imports or execution.

## 7. Correct implementation handoff citation

Any implementation-source authoring instruction, K016 handoff, Sentinel source review, or later acceptance record MUST cite both exact locations:

1. Candidate 08 §23 top-level `implementation_source_matrix`, as amended by this document;
2. Candidate 08 §23 `nodes.K015.node_specific_constants.exact_source_file_matrix`, as amended by this document.

`Appendix A` is the authoritative direct-edge registry only. It MUST NOT be cited as the location of the implementation-source file matrix.

Use of `Appendix A` as matrix authority is `STOP_IMPLEMENTATION_MATRIX_CITATION_INVALID`.

## 8. K016 self-identity

For implementation-source handoff K016:

`/payload/self_identity = null`

This choice is mandatory.

Rules:

1. K016 MUST NOT embed its own raw SHA-256.
2. K016 MUST NOT use a self-excluding projection.
3. The later K017 review record or external delivery envelope MUST bind exact K016 path, raw byte length, and raw SHA-256.
4. A populated object, omitted field, empty object, or string is invalid.
5. K016 remains non-authorizing and MUST report implementation source only; it cannot authorize tests or execution.

Violation is `STOP_K016_SELF_IDENTITY_INVALID`.

## 9. Authorization-chain implications

### 9.1 Current state

Current implementation-source authorization remains:

`NONE`

No K013, K012, K014, K015, or K016 created before acceptance of this amendment may be treated as active.

### 9.2 Required future order

A future implementation-source authoring activity MAY be considered only after:

1. Sentinel accepts this exact amendment;
2. the accepted amendment identity and canonical installation are independently verified;
3. Gustavo issues a fresh, bounded implementation-source authorization;
4. Sentinel issues the later narrow-stage authorization after reading Gustavo's exact bytes;
5. an activity root is created after both authorizations.

Required order:

`K011 base acceptance + accepted amendment → fresh K013 → fresh K012 → fresh K014 → K015/K016`

The future K013, K012, and K014 records MUST each bind:

- exact K011;
- exact accepted amendment record;
- canonical commit containing the accepted amendment;
- exact fourteen-path matrix identity;
- implementation-source-only scope;
- all prohibited actions in §12.

No chat-only, stale, pre-amendment, or matrix-mismatched authorization may carry forward.

This amendment does not assign the future amendment-acceptance node identifier and does not create or revise K013/K012/K014 bytes. Sentinel MUST materialize the exact amendment acceptance identity before any activity authorization. A later authorization package MUST represent that exact governance dependency explicitly; hidden or descriptive-only amendment identities are prohibited.

If the accepted graph representation requires an additional governance edge, that graph change requires separate Sentinel acceptance before K014. This amendment MUST NOT be used to manufacture a hidden provenance edge.

## 10. Stop conditions

| Stop code | Trigger | Effect |
|---|---|---|
| `STOP_CANONICAL_BASE_MISMATCH` | canonical `main` differs from §2.1 | no amendment reliance |
| `STOP_A002_IDENTITY_MISMATCH` | A002 bytes or SHA differ | halt |
| `STOP_ACCEPTED_K008_IDENTITY_MISMATCH` | K008 bytes or SHA differ | halt |
| `STOP_AMENDMENT_NOT_ACCEPTED` | implementation chain attempted before Sentinel acceptance | no K013 |
| `STOP_AMENDMENT_INSTALLATION_NOT_VERIFIED` | accepted amendment not verified at canonical commit | no K013 |
| `STOP_IMPLEMENTATION_MATRIX_CITATION_INVALID` | Appendix A cited as matrix source | block handoff |
| `STOP_K015_SOURCE_MATRIX_INVALID` | path, role, count, order, or required field mismatch | no K016 |
| `STOP_NAMESPACE_PACKAGE_FORBIDDEN` | implicit namespace behavior used | reject K015 |
| `STOP_PACKAGING_SCOPE_NOT_AUTHORIZED` | pyproject/build configuration change required | return to Sentinel |
| `STOP_REGISTRY_SOURCE_IDENTITY_MISMATCH` | wrong K008 source | reject K015 |
| `STOP_REGISTRY_EXTRACTION_AMBIGUOUS` | §23 extraction not unique | reject K015 |
| `STOP_REGISTRY_JCS_IDENTITY_MISMATCH` | registry literal mismatch | reject K015 |
| `STOP_REDUCER_PROJECTION_IDENTITY_MISMATCH` | reducer projection mismatch | reject K015 |
| `STOP_GENERATED_LITERAL_DRIFT` | hand-edited or duplicate normative content | reject K015 |
| `STOP_K016_SELF_IDENTITY_INVALID` | K016 self-identity not exactly null | reject K016 |
| `STOP_AUTHORIZATION_CHAIN_INCOMPLETE` | fresh K013/K012/K014 order or identity incomplete | no source authoring |
| `STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED` | any prohibited activity is attempted | halt and preserve evidence |

## 11. Acceptance evidence

Sentinel can review this amendment by static inspection:

1. compare canonical package layout with §4;
2. compare both amended matrix locations for exact equality;
3. verify fourteen paths and exact roles;
4. independently sort paths by UTF-8 and compare exact sequence;
5. independently extract accepted K008 §23 and verify the two JCS identities;
6. verify the generated-literal and reducer-projection obligations are deterministic;
7. verify K016 self-identity is exactly null;
8. verify implementation-handoff citations name the two §23 locations;
9. verify no existing implementation authorization is activated;
10. verify all non-authorizations remain explicit.

Naming future source-review methods does not authorize source authoring, imports, or execution.

## 12. Explicit non-authorization

This amendment authorizes none of the following:

- implementation-source authoring;
- test-source authoring;
- test execution;
- project imports or execution;
- compilation, linting, type checking, or coverage;
- local research-data access;
- network, API, RPC, vendor, Dune, curl, or endpoint access;
- dependency or packaging changes;
- acquisition, construction, alignment, rebuild, audit, or transition execution;
- empirical artifact generation;
- P1, P2, or P3;
- scoring or probe execution;
- gate changes;
- canonical installation or canonical-file edits;
- branch creation, commits, pushes, merges, tags, releases, or ref changes;
- any later-stage authorization.

Authorization effect:

`NONE`

## 13. Required self-attack

| Attack | Required result |
|---|---|
| Remove `pm_research/named_binary_probe_s2/__init__.py` | `STOP_NAMESPACE_PACKAGE_FORBIDDEN` |
| Retain one `src/` path | `STOP_K015_SOURCE_MATRIX_INVALID` |
| Add a fifteenth helper or packaging file | `STOP_K015_SOURCE_MATRIX_INVALID` |
| Sort rows by role or authoring order | ordering mismatch |
| Reassign a role after sorting | role-map mismatch |
| Extract registry from nonaccepted K008 | `STOP_REGISTRY_SOURCE_IDENTITY_MISMATCH` |
| Parse K008 at runtime | source review rejection |
| Duplicate reducer literals in `state_reducers.py` | `STOP_GENERATED_LITERAL_DRIFT` |
| Alter one registry byte while preserving valid JSON | `STOP_REGISTRY_JCS_IDENTITY_MISMATCH` |
| Cite Appendix A for the matrix | `STOP_IMPLEMENTATION_MATRIX_CITATION_INVALID` |
| Populate K016 self-identity | `STOP_K016_SELF_IDENTITY_INVALID` |
| Reuse pre-amendment K013/K012/K014 | `STOP_AUTHORIZATION_CHAIN_INCOMPLETE` |
| Treat this amendment as source authorization | `STOP_UNAUTHORIZED_ACTIVITY_ATTEMPTED` |

**Strongest alternative design.** Preserve import name `pm_research.named_binary_probe.s2` by adding a parent `pm_research/named_binary_probe/__init__.py`. That alternative requires a fifteenth implementation path and changes the accepted `source_matrix.v1` cardinality. The selected one-level regular subpackage preserves the fourteen-role matrix and avoids namespace-package behavior and packaging changes.

## 14. Changed specification sections

| Accepted Candidate-08 location | Amendment effect |
|---|---|
| §23 `implementation_source_matrix` | full replacement with §4.2 |
| §23 `artifact_profiles.source_matrix.v1` | ordering and exact path-role constraints amended by §5.2 |
| §23 `nodes.K015.node_specific_constants.exact_source_file_matrix` | full replacement with §4.2 |
| §23 `nodes.K015.node_specific_invariants` | amended by §5.4 |
| §23 `nodes.K016.node_specific_constants` | add `self_identity_rule = MUST_BE_NULL` |
| §23 `nodes.K016.node_specific_invariants` | add §8 rules |
| Implementation-source handoff language | replace Appendix-A matrix citation with §7 locations |
| Implementation-source source-review obligations | add §6 |
| Implementation-source authorization prerequisites | add §9 |

All other Candidate-08 requirements remain unchanged.

## 15. Requested Sentinel decision

`APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`

Approval would accept this amendment text only. It would not authorize implementation, tests, imports, execution, data access, networking, Git activity, canonical installation, P1/P2/P3, scoring, probe execution, or a gate change.
