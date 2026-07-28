# GitHub Copilot CLI role-source acceptance record

## Decision

`APPROVE — GITHUB_COPILOT_CLI_ROLE_SOURCE_ACCEPTED`

Recorded on: `2026-07-28`

## Request and boundary

Gustavo approved a documentation-only update to `rigolugo/pm_research`
recording the reusable GitHub Copilot CLI roles repository and its immutable
commit as the accepted role source.

This record is administrative documentation only. It does not install the
roles into a runtime location, execute a launcher or test, modify research
source/test files, or authorize any project stage.

## Evidence

### CANONICAL — research repository base

This documentation candidate was prepared against exact canonical
`rigolugo/pm_research` main commit:

`9a0da006d9ea7e1f5e7a42f980fd831a1fea1037`

Stop on any base mismatch before installation.

### OBSERVED — reusable role repository

- repository: `rigolugo/pm_copilot_roles`;
- visibility at verification: `private`;
- default branch: `main`;
- accepted root commit:
  `a7df418216cb7355b003164b8b509e40081cdbdc`;
- root commit parent count: `0`;
- commit message: `Bootstrap validated GitHub Copilot CLI roles`;
- author and committer identity:
  `Rigo Lugo <rigolmr@gmail.com>`;
- local and remote `refs/heads/main` equality was verified before this record
  was prepared.

### VERIFIED — accepted package and content identity

- accepted bootstrap candidate:
  `PM_COPILOT_ROLES_REPOSITORY_BOOTSTRAP_CANDIDATE_02`;
- version: `0.1.0-candidate.2`;
- candidate ZIP SHA-256:
  `6facb7c109121e5886f4ca8a737631be1596b5c954eedfc45194f7b66276a50c`;
- repository paths in the accepted root commit: `53`;
- checksum-covered paths: `52 / 52 CLEAR`;
- `RELEASE_MANIFEST.json` SHA-256:
  `fc324be4f84dadd9e0821a6690df0dd17dda9dbb5a468ac9ca04222e783e692d`;
- `SHA256SUMS.txt` SHA-256:
  `8919cff890262b299a80dff6b9cf65919fa57fdadecb0e53b5be79e9dca9688f`;
- text policy: `* text=auto eol=lf`;
- unexpected paths: `0`;
- content equivalence after author-identity amendment: `CLEAR`.

## Accepted role family

The accepted source contains:

- `pm-static-inspector`;
- `pm-second-opinion-reviewer`;
- `pm-contract-mapper`;
- `pm-narrow-implementation-author`.

The accepted `pm_research` profile contains the tested project-specific
instructions and launchers. The reusable repository also separates general
role source from project adapters.

## Accepted bounded capability findings

For the `pm_research` profile, the following synthetic findings are accepted
as bounded capability evidence:

- `STATIC_INSPECTOR_READ_ONLY_CLEAR`;
- `SECOND_OPINION_REVIEWER_READ_ONLY_CLEAR`;
- `CONTRACT_MAPPER_BOUNDED_CLOSED_INVENTORY_CLEAR`;
- `NARROW_EXISTING_SOURCE_FILE_AUTHORING_CLEAR`;
- `NARROW_AUTHORIZED_NEW_SOURCE_FILE_AUTHORING_CLEAR`;
- `TEST_SOURCE_AUTHORING_ONLY_CLEAR`;
- `AMBIGUOUS_CONTRACT_STOP_CLEAR`;
- `REQUIRED_UNLISTED_DEPENDENCY_STOP_CLEAR`;
- `MULTI_FILE_ATOMIC_AUTHORING_CLEAR`;
- `DELETE_RENAME_MOVE_PROTECTION_CLEAR`.

These findings are evidence of the tested boundaries. They are not general
proof of correctness and do not authorize use on an unreviewed project or
contract.

## Explicit limitations

The following remain prohibited or unestablished:

- full-package contract mapping is not established;
- automatic project authorization;
- test execution by the narrow implementation author;
- network access by the narrow implementation author;
- local research-data access by the narrow implementation author;
- empirical or research artifact production by the narrow implementation
  author;
- Git writes by the narrow implementation author;
- silent transfer of `pm_research` acceptance to another project.

A new project must define a separate adapter and independently review and
revalidate its paths, canonical read order, owner/reviewer identities,
authorization envelope, launchers, and synthetic fixtures.

## Tool and role separation

The historical `project_context/COPILOT_HANDOFF_2026-06-29.md` describes a
former Microsoft 365 Copilot orchestration context. It remains historical and
non-controlling.

The accepted source in this record is GitHub Copilot CLI. It is an
administrative and bounded implementation-assistance tool. It is not the
project orchestrator. Sentinel remains the orchestrator and decision gate.

## Authorization effect

`NONE`

This acceptance record does not authorize:

- role installation or local runtime replacement;
- implementation or test-source authoring;
- test execution;
- local research-data access;
- network, API, RPC, vendor, Dune, or subprocess activity;
- artifact generation;
- Git commits, pushes, merges, tags, or releases;
- P1, P2, P3, scoring, probe execution, trading, or gate changes.

Every such boundary requires a separate exact authorization.

## Supersession and mutability

Mutable branch name `main` is informational. The accepted identity is the
immutable commit `a7df418216cb7355b003164b8b509e40081cdbdc`.

A later role commit does not supersede this record automatically. Any update
requires a new candidate, exact changed-file and capability review, Gustavo
authorization, Sentinel decision, and a new canonical acceptance record.

## Installation state

`ACCEPTED_PENDING_CANONICAL_INSTALLATION`

Canonical installation into `rigolugo/pm_research` must use the exact
documentation package base and changed-path inventory, followed by Sentinel
branch review, separate Gustavo merge authorization, and remote installation
verification.
