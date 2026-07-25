# Activity Boundaries and Stops

Canonical repository: `rigolugo/pm_research`  
Canonical base inspected: `cc2964840d197a40d1c4ef567b42eda762c0be0a`  
Controlling accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`  
Preserved checkpoint evidence: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`  
Checkpoint state: `NOT_ACCEPTED`; authorization effect: `NONE`; static result: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`.


## 1. Current state

All activities below are `NOT AUTHORIZED`. This document defines separation for possible future packages only.

| Activity | Possible future boundary | Current status | Required separate authorization |
|---|---|---|---|
| source authoring | exact three mandatory source files, one atomic stage | prohibited | Sentinel-accepted scope plus Gustavo authorization and selected start |
| test-source authoring | exact four mandatory test paths | prohibited | separate post-source proposal and Gustavo authorization |
| test execution/collection | exact named tests/commands/environment | prohibited | separate execution authorization |
| project import/compilation/lint/type/coverage/CI | none in this candidate | prohibited | explicit separate authorization |
| local-data reads | none | prohibited | explicit data-access authorization |
| curl/API/RPC/Dune/vendor/network/subprocess | none | prohibited | explicit operational authorization |
| artifact generation/regeneration | specification package only; no project artifacts | prohibited for project | explicit artifact-run authorization |
| Git writes/commit/branch/push | none | prohibited | Gustavo/manual workflow or separately assigned role |
| R2/P1/P2/P3/scoring/probe/gate change | none | prohibited | separate downstream decision |

## 2. Source-authoring preconditions

A later source package MUST identify and verify:

- canonical repository and exact commit;
- exact implementation starting identity for all three writable source files;
- branch and clean/dirty/untracked state;
- availability of all mandatory files;
- no unreviewed diff in any of the twelve paths;
- accepted Revision 10 package identity and this remediation package acceptance;
- exact allowed-new-files list `NONE`.

No historical hash is automatically reusable. The preserved checkpoint is inspection evidence only.

## 3. Mandatory halts

A future agent MUST halt without editing when:

- HEAD, branch, starting SHA, dirty state, or any mandatory file differs from authorization;
- any authorized path is missing or an unlisted path appears necessary;
- implementation would require a new file, dependency, configuration, export, CLI/runtime change, or adjacent refactor;
- canonical Revision 10 conflicts with this candidate;
- the selected start would require restoring, copying, or promoting checkpoint bytes without explicit authorization;
- exact UnitContext type semantics or selected-member iteration tie-break remains material and Sentinel has not decided it;
- path grammar cannot be consumed through registry typed bindings without a second parser;
- any old private result remains reachable after the proposed change;
- source authoring would require running tests, importing project modules, or generating artifacts.

A halt is a valid conformance outcome and MUST report the exact condition and observed identities. It MUST NOT manufacture a base, widen scope, or overwrite mismatched bytes.

## 4. Minimal-diff rule

Only changes strictly necessary for accepted Revision 10 are permitted. Unrelated refactoring, formatting, comments, docstrings, helpers, renaming, sorting, dependency changes, packaging/configuration edits, fixture movement, or cleanup are forbidden.

Necessary private helpers named by the accepted contract are not optional cleanup; they are required interfaces. Additional helpers not named or logically unavoidable require Sentinel review.

## 5. Review and evidence

Source authoring would emit only declarative implementation evidence: exact changed files/diff, starting and ending hashes, and activity statement. Static review is not execution. Test files, test output, coverage, runtime artifacts, and empirical results MUST NOT be bundled into a source-only stage.

No passing test result can retroactively cure an unauthorized write or wrong starting state.
