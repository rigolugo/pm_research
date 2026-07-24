# Known Findings

## Accepted preservation finding

The exact recovered checkpoint bytes are preserved under evidence path only:

- SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- size: `112338` bytes

The recovered file parses as Python source and contains the core Revision 09 R1
private descriptor-set corrections. This is preservation evidence, not an
implementation acceptance decision.

## Open technical and provenance matters

1. The accepted Revision 09 T107 fixture is intercepted by selected-schema path
   validation before its intended cross-member mismatch.
2. The accepted Revision 09 T153 fixture is intercepted by role/path grammar
   validation before its intended duplicate-target result.
3. Candidate 09 appears to revise those reachability fixtures but remains
   non-authoritative until Sentinel decides it.
4. The recovered source header still names Revision 08 despite later Revision 09
   corrections.
5. The accumulated correction-round lineage and activity boundary evidence are
   incomplete.
6. The exact current twelve-path worktree inventory was submitted by Claude but
   is not independently materialized in this checkpoint.

## Required handling

- do not roll back the recovered payload;
- do not promote it to the executable source path automatically;
- do not use Candidate 09 retroactively as implementation authority;
- do not authorize another edit from checkpoint presence;
- review Candidate 09 separately;
- preserve any later implementation state as a new immutable checkpoint rather
  than replacing this directory.
