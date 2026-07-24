# Baseline and Lineage

## Exact identities

- original R1 required starting SHA-256:
  `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`
- original R1 starting bytes available: `false`
- strongest recovered historical comparison base SHA-256:
  `835a60c93a6ef82f2605a5fccd2a68ff88d7b67928f83a5218163a45bb16d807`
- strongest recovered historical comparison base size:
  `63327` bytes
- implementation-review archive SHA-256:
  `e1a809600107796667c415a3b3a922040072f26be4ff9a97b99c294a25d5b7af`
- recovered current checkpoint SHA-256:
  `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- recovered current checkpoint size:
  `112338` bytes

## Lineage status

Claude reported that the current bytes resulted from eight corrective rounds in
the same local R1 worktree. Exact round-by-round starting hashes, ending hashes,
prompt identities, and Sentinel acceptance states have not been completely
recovered.

Evidence classification:

- exact current bytes and hash: `OBSERVED`
- strongest historical baseline bytes and hash: `OBSERVED`
- original `8b8e9320...` bytes: `UNAVAILABLE`
- eight-round count: `SUBMITTED`
- round-by-round lineage: `INCOMPLETE`
- claim that every round was Sentinel-accepted: `NOT ESTABLISHED`

The checkpoint therefore preserves the latest known bytes without reconstructing
or inventing missing lineage.
