# HANDOFF — REV23 Amendment 03 I0 Implementation Authorized / Source-Gated

Decision: **APPROVE — NARROW IMPLEMENTATION AUTHORING; BLOCKED ON SOURCE SYNC**

Accepted-contract commit: `fad41de515572ca30b4440b060a69dd6bfc57e2b`  
First authorization-anchor commit: `d737aa9e12cbfa584b275e128c8624e01af72f61`  
Authorization date: `2026-07-15`  
Authorizing authority: Gustavo  
Review authority: Sentinel  
Implementation agent: Claude

Revision 23 with Amendments 01, 02, and 03 remains the accepted specification. Gustavo separately authorized one bounded Amendment 03 I0 pure deterministic contract-core implementation package.

Claude correctly returned `STOP_CANONICAL_SOURCE_UNAVAILABLE` from a clean local clone at `226085ca9ba7fa41a8b666005499827d6fa6b9c5`. Sentinel accepts the stop. The original handoff incorrectly required working `HEAD=fad41de515572ca30b4440b060a69dd6bfc57e2b`, although the authorization files exist only from `d737aa9e12cbfa584b275e128c8624e01af72f61` onward.

The controlling files are:

- `project_context/implementation_handoffs/local_curl_rev23_i0/IMPLEMENTATION_AUTHORIZATION_SCOPE.md`
- `project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SENTINEL_CANONICAL_SOURCE_GATE_CORRECTION.md`
- `project_context/implementation_handoffs/local_curl_rev23_i0/authorization_audit/rev23_amendment_03_i0/SOURCE_SYNC_AUTHORIZATION_STATUS.md`

Authorized in principle: exact source and unexecuted test-source files listed in the scope, plus static package reports and checksums.

Operational block: no authoring may begin until a separate explicit Gustavo decision authorizes canonical source synchronization and Claude's local repository passes the corrected source gate. The actual implementation baseline will be the verified synchronized local `HEAD`, which must be `d737aa9e12cbfa584b275e128c8624e01af72f61` or a descendant and preserve all exact accepted-contract hashes and path constraints.

Still unauthorized: source synchronization, test/Python/project execution, local research-data reads, network/API/RPC/vendor/curl activity, request execution, empirical artifacts, full orchestration, CLI/dependency changes, Git publication, P1/P2/P3, probe, scoring, price construction, side synthesis, wallet/PnL/trading, and gate changes.

Claude must use the `pm-research-implementing` Skill. Skill invocation does not expand authorization.
