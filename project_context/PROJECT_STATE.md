# PROJECT STATE

*Current objective, environment, active blockers, and authorization state.*

---

## Current objective

Stay Polymarket-native and preserve the accepted research-only guardrails.

The immediate project objective is to maintain the accepted Revision 23 +
Finding 4 contract as the authoritative basis for any future bounded local-curl
implementation decision. No implementation decision is active.

---

## Named-binary research state

### Semantics and realized outcomes

- Named-binary semantics/orientation: implemented, tested, and audit-gated.
- Orientation correctness: `1.0`.
- Token identity coverage: `0.99601`.
- YES/NO local resolutions: `8,521 / 8,521`.
- Non-YES/NO realized outcomes: accepted Dune payout-vector source.
- Resolved single-winner rows: `39,693`.
- Ambiguous multiple-winner exclusions: `253`.
- Non-YES/NO branch gate: `CLEAR_WITH_WARNINGS`.
- Legacy pooled-all gate: `BLOCKED_BY_RESOLUTION_MAPPING`.
- `named_binary_probe_blocked = true`.

### P0 and P1

- P0 preflight: `P0_CLEAR`.
- Final P0 eligible universe: `39,693`.
- Subclasses: UP_DOWN `22,012`; OVER_UNDER `1,003`; NAMED_OTHER `16,678`.
- P0 representativeness result:
  `P0_REPRESENTATIVENESS_CLEAR_WITH_LIMITATIONS`.
- P1 remains blocked because the accepted orientation contract requires two
  independently sourced per-side prices, while the local price store exposes only
  `[condition_id, ts, yes_price]`.
- `yes_price` is YES/NO-only and unsafe for UP_DOWN, OVER_UNDER, and NAMED_OTHER.
- No local per-side/per-token decision-time price artifact is accepted.

---

## Price-source candidate state

### S1 — CLOB `/prices-history`

Accepted sampled result: `S1_SOURCE_NOT_VIABLE`.

Both-side Level-B coverage cleared `0.95` in no subclass:

- UP_DOWN: `19 / 50 = 0.38`
- OVER_UNDER: `51 / 98 ≈ 0.5204`
- NAMED_OTHER: `65 / 100 = 0.65`

No Pass 2 or downstream phase is authorized.

### S1-ALT — local trade prints

Accepted sampled result: `S1ALT_SOURCE_NOT_VIABLE`.

- UP_DOWN: `13 / 50 = 0.26`
- OVER_UNDER: `40 / 98 ≈ 0.4082`
- NAMED_OTHER: `71 / 100 = 0.71`

No side synthesis or downstream phase is authorized.

### Option B — Data API `/trades`

Accepted corrected B0 result: `B0_MECHANICAL_TRUST_NOT_ESTABLISHED`.

- primary API rows: `13,009`
- total API rows across query modes: `17,853`
- local rows: `1,346`
- mismatches: `14,355`
- overlap matched: `0`
- overlap API/local mismatch: `7`
- overlap pagination partial: `3`

B1 remains unauthorized.

### Option C — decoded on-chain OrderFilled tables

- Original C1A accepted valid halt: `C1_ROW_EXPLOSION`.
- C1A-F1: reviewable mixed evidence only.
- C1A-F2: `C1F2_ARTIFACTS_INSUFFICIENT`.
- Option C is not accepted as viable.
- C1 is not design-clear.
- C1B, C2, P1/P2/P3, and probe execution remain unauthorized.

### Option D — L2 archive candidates

Accepted temporal in-range result:

- PMXT v2 pooled: `18,137 / 39,693 = 0.456932`
- Telonex L2 pooled: `37,749 / 39,693 = 0.951024`
- Telonex NAMED_OTHER: `0.918096`

PMXT v2 is closed/deprioritized for broad full-P0 coverage on timing grounds.
Telonex L2 may only proceed through a separately authorized SPEC-ONLY
vendor-coverage review. No vendor fetch or paid action is authorized.

---

## Revision 23 Finding 4 contract state

Revision 23 with Amendments 01–03 and Finding 4 is accepted and installed.

Installation base:

`f6cb60df66c2bbcdfb6d797119ed25ad79e06a11`

Linear installation commits:

1. `3f8cc54dc12a5335472f00f5ffcf5c0d56d8d1ba`
2. `c394b9ab5eb5dc07f8d716818e02507994ce41d7`
3. `e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Finding 4 installation commit:

`e83555ef23712cf6c846dc63a7103e0e0c7e4ed4`

Installed effective hashes:

- specification: `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`
- schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`
- request/authorization contract: `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`
- governing manifest: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- governing semantic hash: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`
- accepted checksum inventory: `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`

Installed path:

`project_context/implementation_handoffs/local_curl_rev23_i0/`

The installed tree includes:

- complete effective accepted contract;
- complete Finding 4 materialization/audit trail;
- preflight evidence;
- replacements and transformation evidence;
- authorization supersession record;
- implementation scope set to `DEFER — NOT AUTHORIZED`;
- disabled Claude implementation prompt.

No `pm_research/`, `tests/`, dependency, CLI/runtime, research-data, or empirical
path changed during installation.

---

## Authorization state

No implementation or source synchronization is authorized.

Specifically unauthorized:

- Claude source or test-source authoring;
- tests, Python/project execution, lint, coverage, CI, or imports;
- local research-data reads;
- network, API, RPC, vendor, curl, or request execution;
- replay, capture, analysis, result production, or empirical artifacts;
- P1/P2/P3, scoring, probe execution, or gate changes;
- wallet discovery, OrdersMatched expansion, `log_index`, PnL-by-role;
- paper trading, live trading, wallet-copying, or full indexers;
- Git writes by ChatGPT or Claude.

A new bounded implementation stage requires:

1. this Phase B canonical-document synchronization to be manually installed;
2. Sentinel verification of that documentation commit;
3. a separate explicit Gustavo implementation authorization;
4. a new Sentinel handoff with exact files, allowed activities, and prohibited activities.

---

## Environment

- Local execution environment: Windows / Miniconda.
- Project path: `C:/b1/pm_research`.
- Data path: `C:/b1/data`.
- Artifacts path: `C:/b1/pm_research/artifacts`.
- Local research data remains unavailable to agents unless separately authorized.

---

## Next possible step

Complete this Phase B documentation synchronization and return its commit SHA for
Sentinel verification.

After that verification, Gustavo may separately decide whether to authorize a
new bounded Finding 4 implementation-authoring stage. Nothing proceeds
automatically.
