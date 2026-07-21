# Sentinel Review — Revision 09 R1 Authorization Installation Revision 02

Review authorization ID
`REV23_FINDING4_I0A_REVISION_09_R1_SOURCE_RESUME_01` against canonical base
`c4e8b1011c51272042decac4bc89e762d767a72a`.

Verify:

1. Revision 09 is recorded as canonically installed and verified at the canonical
   base.
2. The R1 authorization is accepted but inactive until Gustavo manually commits
   this exact package and Sentinel verifies the resulting commit.
3. The immutable baseline file
   `REV23_FINDING4_I0A_R1_TWELVE_PATH_BASELINE_SHA256SUMS.txt` contains exactly
   twelve unique rows and has SHA-256
   `061e6d2cc03ee60e4b47838e4a2c3d2ac4785201d72fd26c708aefc3263ef6f7`.
4. Baseline provenance records implementation-review archive SHA-256
   `e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`
   and later `prepared_evidence.py` SHA-256
   `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`.
5. The source gate requires exactly twelve authorized untracked paths, exact hash
   equality, no thirteenth or other changed path, and permits post-gate writes
   only to `prepared_evidence.py`.
6. The active Claude prompt begins with the required implementing-skill line and
   contains the complete R1 remediation contract without changing fixtures or
   expected results.
7. Test-source editing, tests, project execution, another source edit, R2,
   implementation ZIP reconstruction, research data, empirical work, general
   network activity, Claude Git writes, and gate changes remain unauthorized.
8. Checkpoint reports, inventories, diff summaries, and checksums are chat text,
   not repository files.
9. Authorization-directory, focused R1, complete handoff, package, and detached
   checksum inventories close exactly.
10. No `pm_research/` or `tests/` payload path is included in this documentation
    package and unrelated canonical content is preserved.

Decision required: `APPROVE`, `BLOCK`, `DEFER`, or `NEEDS VERIFICATION`.

Approval authorizes only Gustavo's manual documentation commit. The R1 prompt
becomes active only after Sentinel verifies that resulting commit.

---

## Historical pre-R1 Sentinel prompt

# Sentinel Review — REV23 Finding 4 I0A Revision 09 Canonical Installation

## Revision 09 installation review

Review the documentation-only manual-upload installation package against canonical base `1e963bb6e8387aff071d697a416fa558956e571e` and accepted archive `4b05f25bf8f5c9e6295af94fdc801baa6d046df42fd007a877d08d736b7960a0`. Verify exact 14-member byte identity, immutable Revision 08 preservation, historical manifest/decision copies, full-file preservation of canonical history and indexes, complete checksum inventories, inactive Claude prompt, and absence of Revision 09 implementation authorization or source/test paths.

Decision required: `APPROVE` or `BLOCK`. Approval permits only Gustavo's manual documentation commit and subsequent Sentinel verification. It does not authorize implementation, tests, project execution, data access, network/vendor work, empirical artifacts, agent Git writes, or downstream stages.

---

## Historical Revision 08 Sentinel status — preserved verbatim

# Sentinel review status — REV23 Finding 4 I0A

Revision 08 scope is accepted and canonical at commit `2a08c0c8af7ba8a3ea43b019be3a1aa98096fdff`.
Gustavo has authorized bounded implementation-source and unexecuted test-source
authoring. Sentinel authorization package:

`authorization_audit/rev23_finding4_i0a/`

Authorization ID: `REV23_FINDING4_I0A_IMPLEMENTATION_AUTHORING_01`.

Current boundary: verify the manual canonical installation commit containing the
active authorization package. After verification, Claude may author only the
exact twelve paths under the declared activity boundaries. Test execution,
project imports/execution, research-data reads, empirical work, general network
access, Git history/remote writes, P1/P2/P3, scoring, probe execution, and gate
changes remain unauthorized.

Future Sentinel review compares Claude's implementation ZIP against the accepted
Revision 08 scope and active package, not Claude's explanation. Passing static
checks does not authorize test execution.
