# Implementation Authorization Scope — REV23 Finding 4

Decision: **DEFER — SCOPE PREPARATION ONLY; IMPLEMENTATION NOT AUTHORIZED**

Canonical scope-preparation anchor:

`d17684a5798724ecbc40b85ca8b1e5ebdb8c3b98`

The prior Amendment 03 I0 authorization is `SUPERSEDED_INACTIVE`.

A bounded Finding 4 I0A scope may be drafted for Gustavo's review. Drafting,
reviewing, or storing that proposal does not authorize Claude to synchronize
sources, author files, write tests, execute code, or produce an implementation
package.

## Current activity status

- Scope preparation: AUTHORIZED for Sentinel only.
- Source synchronization: NOT AUTHORIZED.
- Source authoring: NOT AUTHORIZED.
- Test-source authoring: NOT AUTHORIZED.
- Test execution: NOT AUTHORIZED.
- Python/project-code execution or import: NOT AUTHORIZED.
- Local research-data reads: NOT AUTHORIZED.
- Network/API/RPC/vendor/curl: NOT AUTHORIZED.
- Replay or empirical work: NOT AUTHORIZED.
- Git history or remote writes by ChatGPT/Claude: NOT AUTHORIZED.
- P1/P2/P3, scoring, probe execution, and gate changes: NOT AUTHORIZED.

Claude must return `STOP_IMPLEMENTATION_NOT_AUTHORIZED` unless Gustavo later
issues a separate explicit implementation decision and Sentinel installs a new
active authorization package.
