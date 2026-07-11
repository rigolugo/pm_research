# Local CLOB curl/libcurl Canary

- Disclaimer: `LOCAL_CLOB_CURL_CANARY_NOT_P1_EVIDENCE`
- Execution origin: `LOCAL_WINDOWS_CURL_EXE_LIBCURL`
- curl executable: `C:\Windows\system32\curl.exe`
- Requests made: `6`
- Candidate rows: `6`
- Condition summaries: `3`
- Attempts per request: `1`
- Retries: `0`
- Custom headers / user-agent override / proxies / cookies / browser emulation: `none`

## Requests

| Subclass | Side | curl exit | HTTP | Classification | Points | Candidate | Gap seconds |
|---|---:|---:|---:|---|---:|---:|---:|
| UP_DOWN | 0 | 0 | 200 | LOCAL_CLOB_CURL_CANARY_USABLE_SHAPE | 4 | 0.995 | -3360 |
| UP_DOWN | 1 | 0 | 200 | LOCAL_CLOB_CURL_CANARY_USABLE_SHAPE | 4 | 0.005 | -3359 |
| OVER_UNDER | 0 | 0 | 200 | LOCAL_CLOB_CURL_CANARY_USABLE_SHAPE | 120 | 0.49 | 3 |
| OVER_UNDER | 1 | 0 | 200 | LOCAL_CLOB_CURL_CANARY_USABLE_SHAPE | 120 | 0.51 | 0 |
| NAMED_OTHER | 0 | 0 | 200 | LOCAL_CLOB_CURL_CANARY_USABLE_SHAPE | 120 | 0.54 | -14 |
| NAMED_OTHER | 1 | 0 | 200 | LOCAL_CLOB_CURL_CANARY_USABLE_SHAPE | 120 | 0.46 | -13 |

## Condition pairs

| Subclass | Side 0 | Side 1 | Pair status |
|---|---|---|---|
| UP_DOWN | PRESENT | PRESENT | BOTH_SIDES_PRESENT |
| OVER_UNDER | PRESENT | PRESENT | BOTH_SIDES_PRESENT |
| NAMED_OTHER | PRESENT | PRESENT | BOTH_SIDES_PRESENT |

## Interpretation boundary

This diagnostic tests only whether replacing Python `urllib` with `curl.exe`/libcurl changes endpoint reachability for the exact same six request URLs. It does not establish P0 coverage, reverse `S1_SOURCE_NOT_VIABLE`, create a P1 artifact, compute `canonical_side_price`, authorize P1/P2/P3/probe/scoring, or change any project gate.
