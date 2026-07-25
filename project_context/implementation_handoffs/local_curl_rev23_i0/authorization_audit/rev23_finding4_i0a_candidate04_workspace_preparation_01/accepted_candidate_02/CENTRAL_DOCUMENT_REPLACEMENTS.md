# Proposed Narrow Central Documentation Replacements

## Status

`PROPOSAL FOR SENTINEL REVIEW — NOT CANONICAL — NO EXECUTION EFFECT`

The exact canonical base is
`689e546e588d557c96f28bc722c3f159d635f2c1`. The repository MUST NOT be
modified by this package. Sentinel controls any later canonical replacement
package under `project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`.

## Required synchronization facts

Any complete central-document replacements prepared by Sentinel MUST make only
these state changes:

1. Candidate 04 installation:
   `INSTALLED_PENDING_SENTINEL_VERIFICATION` →
   `INSTALLED_AND_SENTINEL_VERIFIED`.
2. installation commit:
   `PENDING_RETURN_TO_SENTINEL` →
   `689e546e588d557c96f28bc722c3f159d635f2c1`.
3. current workflow state:
   `C04_SPEC_ACCEPTED_PENDING_EXTERNAL_CANONICAL_INSTALLATION` →
   `C04_SPEC_CANONICALLY_INSTALLED_NOT_AUTHORIZED`.
4. controlling next possible action:
   Sentinel review of this workspace-preparation package, with Gustavo's
   present authorization recorded as `PACKAGE_AUTHORING_ONLY`.
5. workspace execution authorization:
   `NONE`.
6. active workspace-execution Sentinel handoff:
   `NONE`.
7. source authoring, test-scope review, test-workspace preparation, test
   authoring, local commit creation, push, remote materialization, tests,
   execution, data/network activity, and every downstream stage:
   `UNAUTHORIZED`.

## Central paths requiring complete replacement if Sentinel accepts

- `project_context/START_HERE.md`
- `project_context/PROJECT_STATE.md`
- `project_context/DECISION_LOG.md`
- `project_context/ARTIFACT_INDEX.md`
- `project_context/implementation_handoffs/local_curl_rev23_i0/README_FIRST.md`

Sentinel MAY add one focused handoff-index or checksum-index replacement only
if the current canonical index structure requires it to identify this accepted
package. No other central path is proposed.

## Mandatory preserved facts

Replacements MUST preserve:

- Candidate 04's accepted identity, 19-member accepted-package identity, and
  acceptance decision;
- the accepted source archive identity (`REV23_FINDING4_I0A_PROVENANCE_CAPTURE.zip`,
  SHA-256 `942d7d00c3d98ea91c09a7bad7023044119839d9f227e4bbbd33f8c21b5f17d9`,
  `487764` bytes, `17` total archive members, `12` payload members, `12`
  payload checksum entries, and `12` payload checksum matches), kept distinct
  from the exact twelve captured payload paths;
- `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE` as open;
- the old remediation-source gate as `FAILED_INACTIVE`;
- checkpoint `fcf406c4...` as `NOT_ACCEPTED`, evidence-only, and non-authorizing;
- historical Revision 08 and Revision 09 authorizations as inactive;
- all named-binary, P0/P1, price-source, and research guardrails unchanged;
- no active Claude implementation prompt.

## Stop condition

If Sentinel cannot produce complete replacement files from the exact canonical
base without changing an unrelated fact, the synchronization MUST stop for a
new Sentinel decision. This proposal is not an instruction to patch fragments
into canonical files.
