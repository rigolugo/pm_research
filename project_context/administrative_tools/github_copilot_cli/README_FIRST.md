# GitHub Copilot CLI roles — read first

## Product identity

These records apply only to **GitHub Copilot CLI** custom agents, skills,
launchers, hooks, authorization templates, and synthetic capability tests.

They do not describe or reactivate the former Microsoft 365 Copilot
orchestrator.

## Accepted role-source identity

- repository: `rigolugo/pm_copilot_roles`;
- repository visibility at acceptance: `private`;
- default branch: `main`;
- accepted immutable root commit:
  `a7df418216cb7355b003164b8b509e40081cdbdc`;
- commit message: `Bootstrap validated GitHub Copilot CLI roles`;
- accepted bootstrap candidate:
  `PM_COPILOT_ROLES_REPOSITORY_BOOTSTRAP_CANDIDATE_02`;
- candidate ZIP SHA-256:
  `6facb7c109121e5886f4ca8a737631be1596b5c954eedfc45194f7b66276a50c`.

## Canonical installation state

- state: `INSTALLED_AND_SENTINEL_VERIFIED`;
- verified `pm_research` commit:
  `319a122d55422ac95b827beea524b8a1f06409ee`;
- exact parent:
  `9a0da006d9ea7e1f5e7a42f980fd831a1fea1037`;
- installation-verification record:
  `SENTINEL_CANONICAL_INSTALLATION_VERIFICATION.md`.

The immutable acceptance record and manifest retain
`ACCEPTED_PENDING_CANONICAL_INSTALLATION` as the accurate pre-installation
state of Candidate 01. The Sentinel installation-verification record controls
the current canonical installation-state presentation.

## Read order

1. `SENTINEL_CANONICAL_INSTALLATION_VERIFICATION.md`
2. `GITHUB_COPILOT_CLI_ROLE_SOURCE_ACCEPTANCE_RECORD.md`
3. `GITHUB_COPILOT_CLI_ROLE_SOURCE_MANIFEST.json`
4. `GITHUB_COPILOT_CLI_ROLE_SOURCE_SHA256SUMS.txt`
5. In the role repository at the accepted commit: `START_HERE.md`,
   `README.md`, `docs/SECURITY_AND_AUTHORIZATION.md`,
   `docs/CAPABILITY_MATRIX.md`, `docs/PROJECT_ADAPTERS.md`, and the exact
   role/profile files relevant to the requested task.

## Authority boundary

Sentinel remains the project orchestrator and decision gate. Repository
presence, canonical documentation installation, local role installation, a
launcher, or a synthetic test result authorizes nothing by itself.

Each real task still requires its own accepted contract, exact project base,
bounded paths, explicit activity boundaries, Gustavo authorization, and
Sentinel authorization where required.
