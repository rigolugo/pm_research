# Known Findings

## Accepted preservation finding

The exact recovered checkpoint bytes remain preserved under evidence path only:

- SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes
- Git blob SHA: `d25a0fe58e84db526e6d68b4d14e764c59f6d46c`

The recovered file parses as Python source and contains the core Revision 09 R1
private descriptor-set corrections. This is preservation evidence, not an
implementation acceptance decision.

## Resolved specification-layer matters

Installed Revision 10 resolves:

1. T107 fixture reachability;
2. T153 fixture reachability;
3. Candidate 09's non-authoritative drafting status as an open blocker.

Those items are removed from the checkpoint blocker list. Their resolution does
not prove that the preserved implementation conforms to Revision 10.

## Open implementation and provenance matters

1. The accumulated correction-round lineage and activity-boundary evidence are incomplete.
2. The exact current twelve-path worktree inventory was submitted by Claude but is not independently materialized in this checkpoint.
3. Static implementation-conformance review against installed Revision 10 has not been completed.
4. The recovered source header still names Revision 08 despite later corrections; its materiality must be decided during conformance review.

## Required handling

- do not roll back the recovered payload;
- do not promote it to the executable source path automatically;
- do not select it as a Revision 10 implementation start without a separate decision;
- do not reuse historical Revision 09 or Revision 08 authorization;
- do not authorize another edit, test, execution, or downstream stage from checkpoint presence;
- preserve any later implementation state as a new immutable checkpoint rather than replacing this directory.
