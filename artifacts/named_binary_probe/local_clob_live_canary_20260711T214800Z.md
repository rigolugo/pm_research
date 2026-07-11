# Local CLOB Live Canary

- Disclaimer: `LOCAL_CLOB_CANARY_NOT_P1_EVIDENCE`
- Execution origin: `LOCAL_WINDOWS_PYTHON_URLLIB`
- Requests made: `6`
- Candidate rows: `0`
- Condition summaries: `3`
- Retries: `0`
- Proxies/browser emulation/custom anti-bot headers: `none configured`

## Requests

| Subclass | Side | HTTP | Classification | Points | Candidate | Gap seconds |
|---|---:|---:|---|---:|---:|---:|
| UP_DOWN | 0 | 403 | LOCAL_CLOB_CANARY_ENDPOINT_ERROR | 0 | null | null |
| UP_DOWN | 1 | 403 | LOCAL_CLOB_CANARY_ENDPOINT_ERROR | 0 | null | null |
| OVER_UNDER | 0 | 403 | LOCAL_CLOB_CANARY_ENDPOINT_ERROR | 0 | null | null |
| OVER_UNDER | 1 | 403 | LOCAL_CLOB_CANARY_ENDPOINT_ERROR | 0 | null | null |
| NAMED_OTHER | 0 | 403 | LOCAL_CLOB_CANARY_ENDPOINT_ERROR | 0 | null | null |
| NAMED_OTHER | 1 | 403 | LOCAL_CLOB_CANARY_ENDPOINT_ERROR | 0 | null | null |

## Condition pairs

| Subclass | Side 0 | Side 1 | Pair status |
|---|---|---|---|
| UP_DOWN | ERROR | ERROR | BOTH_SIDES_MISSING_OR_BLOCKED |
| OVER_UNDER | ERROR | ERROR | BOTH_SIDES_MISSING_OR_BLOCKED |
| NAMED_OTHER | ERROR | ERROR | BOTH_SIDES_MISSING_OR_BLOCKED |

## Non-meanings

This diagnostic does not establish P0 coverage, reverse `S1_SOURCE_NOT_VIABLE`, create a P1 artifact, compute `canonical_side_price`, authorize P1/P2/P3/probe/scoring, or change any project gate.
