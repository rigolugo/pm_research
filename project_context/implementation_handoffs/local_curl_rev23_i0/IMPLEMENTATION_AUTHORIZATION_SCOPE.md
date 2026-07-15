# REV23 I0 Implementation Authorization Status

Decision: **DEFER — NO ACTIVE IMPLEMENTATION AUTHORIZATION**

Authorizing authority for any future implementation: Gustavo.
Review authority: Sentinel.
Implementation agent: Claude only after a new explicit authorization.

## Accepted governing contract

The accepted specification is the effective Revision 23 contract in `accepted_contract/`, consisting of the frozen Revision 23 package plus `REV23_AMENDMENT_01`, `REV23_AMENDMENT_02`, and accepted `REV23_AMENDMENT_03`.

Critical accepted hashes:

- effective specification: `d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9`
- effective schema registry: `e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19`
- effective request/authorization contract: `8095bb923742e8f7eafac61a1de52d9ff4e5537f8a03bb52af62eb795c9f0f7f`
- governing-package semantic hash: `6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b`
- governing-package manifest complete-file hash: `b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa`

## Superseded historical authorization

Gustavo previously authorized one narrow I0 source/test-source package against the Amendments-01/02 contract bytes. Amendment 03 changes governing interfaces and hashes. That prior authorization is therefore superseded/inactive and does not authorize corrections or new files against the current contract.

The prior Claude implementation package was blocked and was not accepted as conformant.

## Current boundary

No implementation, implementation correction, source authoring, test-source authoring, test execution, Python/project-code execution, lint, coverage, CI, local research-data read, artifact recovery, curl discovery, subprocess/network access, reservation/request execution, replay, empirical capture, compatibility/strict analysis, results/finalization, CLI/dependency change, Git publication, P1/P2/P3, probe, scoring, price construction, side synthesis, wallet/PnL/trading, or gate change is authorized.

Repository source reads and static hash inspection remain allowed only for Sentinel/Professor review and canonical verification; they do not authorize Claude implementation.

## Required sequence for any future implementation

1. Manual canonical upload and commit.
2. Sentinel verifies the new commit and exact accepted hashes.
3. Gustavo explicitly authorizes a bounded implementation stage in the current chat.
4. Sentinel issues a new handoff with exact authorized files, allowed new files, test-source status, test-execution status, local-data status, network/subprocess status, artifact status, and Git-write status.
5. Claude uses the `pm-research-implementing` Skill only under that new handoff.

Until all five steps occur, Claude must stop without editing code.
