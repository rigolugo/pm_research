# Upload manifest — Apify transport-isolation acceptance

Target branch: `apify-price-canary-dry-run`

Upload these paths exactly:

- `SPEC_apify_transport_isolation_canary.md`
- `HANDOFF_orchestrator_apify_transport_isolation_spec.md`
- `artifacts/named_binary_probe/FINDING_apify_live_canary_endpoint_blocked.md`
- `artifacts/named_binary_probe/local_clob_live_canary_20260711T214800Z.json`
- `artifacts/named_binary_probe/local_clob_live_canary_20260711T214800Z.md`
- `artifacts/named_binary_probe/local_clob_curl_canary_20260711T215418Z.json`
- `artifacts/named_binary_probe/local_clob_curl_canary_20260711T215418Z.md`

Decision: `APPROVE — SPEC ONLY`

No implementation, Actor modification, build, deployment, package installation,
network request, retry, broader sample, P1/P2/P3/probe/scoring continuation, or
gate change is authorized.
