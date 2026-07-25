# Implementation Authorization Scope

## Current stop

`STOP_IMPLEMENTATION_NOT_AUTHORIZED`

## Controlling specification

- scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- installed and Sentinel-verified at:
  `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- static-conformance finding:
  `REVISION10_STATIC_CONFORMANCE_BLOCKED`
- finding review base:
  `3cf0871ae97d112324031190822756379d1236e8`

## Checkpoint status

- checkpoint: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- payload SHA-256:
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- preservation: `CANONICALLY_PRESERVED`
- acceptance: `NOT_ACCEPTED`
- controlling implementation: `false`
- authorization effect: `NONE`
- Revision 10 implementation starting SHA:
  `NOT_AUTHORIZED_AND_NOT_SELECTED`

The historical Revision 09 R1 source-resume authorization and historical
Revision 08 implementation authorization do not carry forward.

## Authorized now

Only documentation-only manual installation by Gustavo of the static-conformance
record package at the exact declared base, followed by Sentinel verification of
the resulting commit.

This does not authorize Claude or any implementation agent to write Git history
or modify canonical files.

## Not authorized

- implementation or implementation-source authoring;
- test-source authoring or test execution;
- source synchronization or selection of starting bytes;
- rollback, restoration, overwrite, promotion, or checkpoint continuation;
- project imports, compilation, lint, typing, coverage, CI, or execution;
- local research-data reads;
- vendor/API/RPC/Dune/curl/general project-network access;
- subprocess or empirical artifact production;
- dependencies, CLI, runtime, or configuration changes;
- Git writes by Claude;
- R2, P1, P2, P3, scoring, probe execution, or gate changes.

## Future boundary

Any remediation requires a separate accepted implementation scope or amendment,
Gustavo authorization, Sentinel handoff, exact canonical base, exact starting
bytes, exact writable paths, and explicit activity-boundary statuses.

This document does not select that future starting point and does not prepare a
Claude implementation prompt.
