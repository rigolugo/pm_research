# Finding 4 packaging producer-consumer matrix

| Artifact | Producer | Consumer | Status |
|---|---|---|---|
| Frozen eleven direct targets | Approved nine-source materialization plus approved preflight | Sentinel packaging review | byte-frozen |
| `accepted_contract_materialized/` | deterministic packaging stage | Sentinel | candidate only |
| `replacements/` | deterministic copy of exact target bytes | reconstruction reviewer | exact |
| RFC 6902 schema patch | deterministic baseline-to-target serializer | schema reconstruction reviewer | exact root replacement |
| governing manifest, sidecar, accepted checksum inventory | deterministic hash cascade | Sentinel | packaging dependent |
| package manifest and `SHA256SUMS.txt` | deterministic outer inventory | Sentinel | packaging dependent |
