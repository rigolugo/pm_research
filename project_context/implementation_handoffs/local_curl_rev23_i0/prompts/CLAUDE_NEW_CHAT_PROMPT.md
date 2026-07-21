Use the pm-research-implementing Skill. Skill invocation does not expand the authorization below.

# ACTIVE-AFTER-VERIFICATION CLAUDE HANDOFF — REV23 Finding 4 I0A Revision 09 R1

Authorization ID:
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01`.

## Activation gate

Do not begin until Gustavo manually commits the accepted canonical authorization
package and Sentinel supplies the exact verified installation commit SHA. Local
`HEAD` MUST equal that SHA. Until then return
`STOP_AUTHORIZATION_INSTALL_NOT_VERIFIED`.

The complete source gate is
`authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/SOURCE_GATE.md`.
It requires exactly the twelve authorized untracked paths, exact SHA-256 equality
with the immutable twelve-path baseline, and no thirteenth or other changed path.

## Governing identity

- repository: `rigolugo/pm_research`;
- controlling scope: `REV23_FINDING4_I0A_SCOPE_REVISION_09`;
- accepted scope archive SHA-256:
  `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`;
- canonical authorization base:
  `c4e8b1011c51272042decac4bc89e762d767a72a`;
- implementation-review archive SHA-256:
  `e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`;
- twelve-path baseline SHA-256:
  `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`;
- authorization directory:
  `project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_finding4_i0a_revision09_r1_source_resume_01/`.

## Sole writable path

`pm_research/local_curl_per_side/prepared_evidence.py`

Required starting SHA-256:

`8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`

The other eleven paths in
`REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt` are read-only and
MUST remain byte-identical throughout R1.

## Required R1 correction contract

Within the sole writable path, conform exactly to accepted Revision 09:

1. Narrow `_PrivateDescriptorSetInvariantCode` to exactly:
   - `PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID`;
   - `PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID`;
   - `PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID`;
   - `PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE`;
   - `PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID`.
2. Remove the obsolete private outcomes
   `PRIVATE_DESCRIPTOR_SET_LOGICAL_HASH_NULLABILITY_INVALID` and
   `PRIVATE_DESCRIPTOR_SET_PARTITION_BINDING_INVALID` from the enum, reducer,
   result handling, and every private branch.
3. Remove the obsolete silent-deferral comment and any corresponding silent
   deferral behavior.
4. Enforce the exact private reducer order:
   role cardinality, ordinal sequence, canonical-target uniqueness, sidecar
   relation, then valid. The private result domain is closed to those five
   outcomes. Every private failure returns `summaries=None`; only valid returns
   the complete ordinal-order summaries.
5. Correct `validate_prepared_descriptor_set` so every branch returns only a code
   in its accepted closed public result domain and follows its exact ordered
   precedence. Distinguish invalid or non-canonical JSON bytes
   (`ERR_CANONICAL_JSON_INVALID`) from selected-schema membership/type failures
   (`ERR_SELECTED_SCHEMA_INVALID`) and ordinal failures
   (`ERR_ORDINAL_SEQUENCE_INVALID`). Do not emit
   `ERR_CLAIM_SEMANTIC_SCHEMA_MISMATCH` from this function. Resolve any remaining
   nested partition-entry case from the accepted machine-readable contracts
   rather than inventing or collapsing result categories; stop and report a
   contradiction on genuine ambiguity. Same-ordinal partition path, identity,
   or logical-hash mismatch MUST use
   `ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH`. No private or out-of-domain code may
   escape the public function.
6. Revalidate by static source inspection the previously corrected:
   - cross-member comparison;
   - normalized path validation;
   - selected binding;
   - exact seven-cell partition-entry relation projection;
   - descriptor-set ordering;
   - same-ordinal partition binding;
   - complete payload traversal.
7. Preserve every public interface, signature, result domain, assurance tuple,
   return-payload rule, fixture byte, physical or logical hash, role row, frozen
   binding, and T001–T165 expected input/result identity.
8. Fixtures, static case inputs, and expected results MUST NOT be changed to
   accommodate implementation behavior.

Stop and return a finding rather than editing another source or test file,
changing a fixture, broadening a result domain, or inferring an unstated
fallback.

## Authorized activity

- read-only synchronization to the Sentinel-verified authorization-installation
  commit;
- canonical Revision 09 contract reads;
- source editing only in the sole writable path;
- static AST/source/JSON/text/bytes/SHA-256 inspection without importing or
  executing project/authored modules;
- `git status --short --untracked-files=all`, Git diff, exact path inventory, and
  checksums;
- one R1 source-only checkpoint.

## Prohibited

Test-source editing; test collection, discovery, or execution; project/authored
module imports or execution; compilation, lint, type checking, coverage, CI;
another source-file edit; dependencies, CLI, config, generated files, caches,
bytecode; implementation ZIP reconstruction; research data or empirical
artifacts; API/RPC/vendor/Dune/curl/general network activity; Git commits,
branches, pushes, PRs, merges, or remote writes; R2; P1/P2/P3; scoring; probe
execution; gate changes.

## Checkpoint deliverable

Submit only the existing edited
`pm_research/local_curl_per_side/prepared_evidence.py` as a source file.

Return the static source report, exact twelve-path inventory, diff summary, and
checksums as textual checkpoint content in chat. Do not create repository files
for those reports or inventories. Do not submit any test file and do not
reconstruct an implementation ZIP.
