# Administrative tools — read first

This directory contains canonical identity, capability, provenance, and
authorization-boundary records for reusable administrative tools used around
the research project.

Administrative-tool acceptance does not authorize research implementation,
tests, execution, local-data access, networking, Git writes, P1/P2/P3,
scoring, probe execution, trading, or automatic gate changes.

Tool-specific records must preserve product identity. In particular:

- Microsoft 365 Copilot historical orchestration records are distinct from
  GitHub Copilot CLI agent-role records.
- A reusable tool repository may contain project adapters, but acceptance for
  one adapter does not transfer automatically to another project.
- Exact repository commit identity controls over mutable branch names or local
  copies.

Current child read order when GitHub Copilot CLI is relevant:

1. `github_copilot_cli/README_FIRST.md`
2. `github_copilot_cli/GITHUB_COPILOT_CLI_ROLE_SOURCE_ACCEPTANCE_RECORD.md`
3. `github_copilot_cli/GITHUB_COPILOT_CLI_ROLE_SOURCE_MANIFEST.json`
4. `github_copilot_cli/GITHUB_COPILOT_CLI_ROLE_SOURCE_SHA256SUMS.txt`
