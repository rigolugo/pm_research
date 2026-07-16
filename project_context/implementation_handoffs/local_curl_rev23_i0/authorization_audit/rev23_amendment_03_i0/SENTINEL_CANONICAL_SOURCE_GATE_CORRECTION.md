# Sentinel Canonical Source-Gate Correction — REV23 Amendment 03 I0

Decision: **ACCEPT FINDING**

Accepted stop: `STOP_CANONICAL_SOURCE_UNAVAILABLE`.

## Evidence accepted

Claude reported a clean local repository at:

`226085ca9ba7fa41a8b666005499827d6fa6b9c5`

The local object database did not contain `fad41de515572ca30b4440b060a69dd6bfc57e2b`; the Amendment 03 authorization files were absent; and the task expressly prohibited fetch, pull, reset, re-clone, or other source synchronization. No code or test file was authored and no project/test/data/network execution occurred.

## Canonical facts

- Accepted-contract commit: `fad41de515572ca30b4440b060a69dd6bfc57e2b`.
- First canonical commit containing the Amendment 03 I0 authorization: `d737aa9e12cbfa584b275e128c8624e01af72f61`.
- The original handoff incorrectly required working `HEAD=fad41de515572ca30b4440b060a69dd6bfc57e2b` while requiring authorization records that exist only from `d737aa9e12cbfa584b275e128c8624e01af72f61` onward.

The original exact-HEAD rule is superseded by this correction.

## Corrected source gate

Before implementation authoring begins:

1. Gustavo must separately authorize canonical source synchronization for the Claude sandbox.
2. The resulting local `HEAD` must be `d737aa9e12cbfa584b275e128c8624e01af72f61` or a descendant.
3. `d737aa9e12cbfa584b275e128c8624e01af72f61` must exist locally and satisfy `git merge-base --is-ancestor d737aa9e12cbfa584b275e128c8624e01af72f61 HEAD`.
4. The working tree must be clean before authoring.
5. Exact accepted-contract hashes must equal the registered Amendment 03 values:
   - specification `d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9`;
   - schema registry `e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19`;
   - request/authorization contract `8095bb923742e8f7eafac61a1de52d9ff4e5537f8a03bb52af62eb795c9f0f7f`;
   - governing semantic hash `6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b`;
   - governing-manifest file hash `b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa`.
6. `git diff --name-only d737aa9e12cbfa584b275e128c8624e01af72f61..HEAD` must contain no path under:
   - `project_context/implementation_handoffs/local_curl_rev23_i0/accepted_contract/`;
   - `pm_research/`;
   - `tests/`;
   - dependency, packaging, CLI, workflow, or runtime-configuration files.
7. Every authorized new source/test-source path must be absent before authoring.
8. Any mismatch, pre-existing authorized path, or material drift requires a new stop to Sentinel.

The actual synchronized local `HEAD` becomes the implementation package baseline and must be recorded in the implementation manifest and used for the patch.

## Authorization state

The bounded Amendment 03 I0 source/test-source authoring decision remains valid in principle but is operationally blocked until the source gate passes.

This correction does not authorize source synchronization. It does not authorize tests, Python/project execution, local-data reads, unrelated network/curl activity, replay, empirical artifacts, CLI/dependency changes, Git publication, P1/P2/P3, probe, scoring, price construction, wallet/PnL/trading, or gate changes.
