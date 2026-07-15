# Sentinel Accepted Specification Decision — Revision 23 Amendments 01–03

Decision: **APPROVE**

Revision 23 with `REV23_AMENDMENT_01`, `REV23_AMENDMENT_02`, and `REV23_AMENDMENT_03` is accepted as the governing SPEC ONLY contract.

Blocking findings at specification acceptance: none.

## Effective hashes

- specification: `d4271f3bfb29924c3937a0569d3cee585ef32125604785ba474e837a2ca642b9`
- schema registry: `e9590fac64ce245dbebd7f0e0bcaca5cf8b263e907e202dbba779f1be9157f19`
- request-plan and authorization contract: `8095bb923742e8f7eafac61a1de52d9ff4e5537f8a03bb52af62eb795c9f0f7f`
- governing-package semantic hash: `6510bee82e4047bc3e035cfa27732556b313300f19368c8f02ed7cb8eda5c86b`
- governing-manifest complete-file hash: `b2627541175ca3ccb225491c1a684e0d7c00eed20d40e30cd65da23136528afa`

## Authorization boundary

This acceptance authorizes specification installation only. It does not authorize implementation, correction of the prior Claude package, source/test-source authoring, tests, execution, local reads, curl/subprocess/network activity, replay, empirical artifacts, P1/P2/P3, probe, scoring, wallet/PnL/trading, or gate changes.

The prior narrow I0 implementation authorization applied only to the Amendments-01/02 bytes and remains superseded.

After canonical commit `fad41de515572ca30b4440b060a69dd6bfc57e2b` was verified, Gustavo separately authorized one bounded Amendment 03 I0 implementation-authoring stage on `2026-07-15`. That separate authorization is controlled exclusively by `IMPLEMENTATION_AUTHORIZATION_SCOPE.md`; it does not arise from specification acceptance and does not authorize tests or execution.

The accepted specification remains non-empirical and does not unblock P1. `named_binary_probe_blocked = true`.
