# P0 CLOB Canary Candidate 03 — Implementation-Source Installation Record — Candidate 01

## 1. Status

| Field | Value |
|---|---|
| Record ID | `P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALLATION_RECORD_CANDIDATE_01` |
| Original predecessor package | `P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALLATION_DOCUMENTATION_CANDIDATE_01` |
| Current updating package | `P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_POST_INSTALLATION_VERIFICATION_DOCUMENTATION_CANDIDATE_01` |
| Authoring mode | `MATERIALIZE` |
| Current record status | `POST_INSTALLATION_LIFECYCLE_UPDATE_REVIEW_CANDIDATE` |
| Prepared by | Professor |
| Independent reviewer and decision owner | Sentinel |
| Canonical repository | `rigolugo/pm_research` |
| Package-authoring base | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| Source-installation anchor commit | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| Accepted installation finding | `CANONICAL_REMOTE_INSTALLATION_VERIFIED` |
| Authorization effect | `NONE` |

This complete replacement preserves the predecessor record's historical pre-installation state and updates the current lifecycle after verified canonical remote installation.

**Checkable completion sentence:** Sentinel can verify that the predecessor-package state is retained only as explicitly historical, while every current lifecycle field identifies the exact verified installation commit, source identities, bounded validation findings, and unchanged non-authorization boundaries.

## 2. Purpose

This record has two purposes:

1. preserve what was true when the predecessor documentation package was authored before a source-installation commit existed; and
2. record that those pre-installation lifecycle conditions were superseded by the verified installation at `1a19e1ef715ceca7aef9d55f7aa2446961e13c35`.

This record does not claim that installation was already complete when the predecessor package was authored. It does not authorize further work.

## 3. Source precedence and epistemic classification

The canonical repository at `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` is `CANONICAL` for the installed paths and current project state.

The exact commit, parent, message, one-commit changed-path scope, current `main` equality, and Git blob identities are `OBSERVED_CANONICAL`.

The exact tree identity, ordinary fast-forward push evidence, local/direct/remote ref convergence, clean local status, installed content byte lengths and SHA-256 values, and accepted validation evidence are `SUBMITTED_ACCEPTED_INSTALLATION_EVIDENCE` for Sentinel verification and materialization.

The external Candidate 03 ZIP is provenance only. It is not a canonical repository member.

## 4. Historical predecessor-package state

When `P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALLATION_DOCUMENTATION_CANDIDATE_01` was authored at base `ed045a6ce0130c1c245e4a5bee98fe1b09be83cb`, the following statements were accurate:

| Historical predecessor boundary | Historical value |
|---|---|
| canonical installation | `CANONICAL_INSTALLATION_PENDING` |
| exact local commit | `NOT_CREATED_OR_REVIEWED` |
| push authorization | `NONE` |
| push execution | not performed |
| remote installation verification | `NOT_VERIFIED` |
| source status | accepted installation candidate, not yet canonical source |

Those values are historical facts about the predecessor package's authoring time. They MUST NOT be read as current state.

The predecessor package correctly did not contain source bytes, `.gitignore`, empirical outputs, raw responses, local data, or the external source ZIP. Its acceptance did not itself authorize a local commit or push.

## 5. Superseding verified installation

The historical pre-installation lifecycle was superseded by:

| Field | Exact value |
|---|---|
| source-installation anchor commit | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| parent | `ed045a6ce0130c1c245e4a5bee98fe1b09be83cb` |
| commit tree | `d8a530b598735fc9d98294698a21d4d072162414` |
| commit message | `Install Candidate 03 P0 CLOB diagnostic source and canonical validation record` |
| commit count from parent | `1` |
| canonical `main` verification | `IDENTICAL` to `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| installation method | one local commit and ordinary non-force fast-forward push to `origin/main` |
| merge | `NO` |
| amend | `NO` |
| force push | `NO` |
| tag | `NO` |
| ref convergence | local `HEAD`, `origin/main`, and direct `refs/heads/main` all resolved to `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| local status after push | clean |
| accepted finding | `CANONICAL_REMOTE_INSTALLATION_VERIFIED` |

The term **source-installation anchor commit** is deliberate. A later documentation-only commit may descend from `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` without changing the installed source identities. This record does not claim that `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` will always be the repository's latest commit.

## 6. Exact committed scope

The source-installation anchor commit contains exactly nine changed paths:

| # | Status | Path | Git blob SHA |
|---:|---|---|---|
| 1 | M | `.gitignore` | `b4d26e15ac1b3de27af48d38d5024fd2c4cc830c` |
| 2 | A | `pm_research/data/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| 3 | A | `pm_research/data/store.py` | `711052cdb3ff2644758f0b138016fceaca3c3169` |
| 4 | M | `project_context/ARTIFACT_INDEX.md` | `b9b807957ae4a8597e5769ea20eaa3e51c2f16b5` |
| 5 | M | `project_context/DECISION_LOG.md` | `d2c8b8ab5f7fa51fe74316d0f456dad32de2c3e9` |
| 6 | A | `project_context/P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALLATION_RECORD_CANDIDATE_01.md` | `d4c5bc0e85617d3a88119e56eb2ec88eabb58c6a` |
| 7 | M | `project_context/PROJECT_STATE.md` | `a4e8bb205394a534062a9ecdd994b9b0703e3140` |
| 8 | M | `project_context/START_HERE.md` | `0d07399a6fe1a48b38ef285f860fbb69893a0257` |
| 9 | A | `scripts/p0_per_token_price_source_scale_diagnostic_01.py` | `c72a6b582e6523fcffc1cf64ce0a25ab114154a9` |

Git blob SHA values are Git object identities. They MUST NOT be confused with SHA-256 content identities.

## 7. Accepted external Candidate 03 package

Provenance package:

`P0_CLOB_CANARY_IMPLEMENTATION_SOURCE_INSTALL_CANDIDATE_03.zip`

| Field | Exact value |
|---|---|
| Bytes | `20023` |
| SHA-256 | `7a6d63d804a85bcbdf20917b2bc067fe08ae1f4fd77a69c7d1a1f46ed0b45b94` |
| Static review status | `STATIC_REVIEW_ACCEPTED` |
| Canonical repository member | `NO` |

The external ZIP identifies the accepted source candidate. It was not committed to the repository.

## 8. Installed Candidate 03 source identities

| Path | Bytes | SHA-256 | Git blob SHA |
|---|---:|---|---|
| `.gitignore` | `2328` | `0790b0f98f1367195ff5142e4e1de0f651a73b160465f13ef25313945d41522f` | `b4d26e15ac1b3de27af48d38d5024fd2c4cc830c` |
| `scripts/p0_per_token_price_source_scale_diagnostic_01.py` | `63237` | `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006` | `c72a6b582e6523fcffc1cf64ce0a25ab114154a9` |
| `pm_research/data/__init__.py` | `0` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `pm_research/data/store.py` | `5079` | `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95` | `711052cdb3ff2644758f0b138016fceaca3c3169` |

The exact installed `.gitignore` exception is:

`!scripts/p0_per_token_price_source_scale_diagnostic_01.py`

The installed Store is read-only trade loading. It creates no directories; has no save/write methods; loads no markets, resolutions, prices, or coverage data; depends on no `schemas.py`; and defines no `yes_price` or complement-price semantics.

The installed diagnostic independently acquires one token ID per side and forbids `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, complement synthesis, and winning-token enumeration as substitutes for independent side acquisition.

## 9. Historical empirical source distinction

The earlier accepted dry run and earlier two 100-request canaries were executed using:

| Historical input | Bytes | SHA-256 |
|---|---:|---|
| historical diagnostic script | `66241` | `4dd784d3bd5e636ba05e0bd13702f6b24f3e03206d45881a2d6de88bfedcac00` |
| historical compatibility Store | `8788` | `7fa3078e78c2ba993ba3a825c2f6042dd33445d0079592aba3cde86e09b7dc92` |
| historical `schemas.py` | `4878` | `75ec05646f458d72d2fba7481ee8a78c67a3099d4025eb9826af3ad9ac30396c` |

Historical repository base:

`e675a47ec2c8f6cd769c2673afc16d96e5622ccd`

Those historical findings remain controlled by `project_context/P0_CLOB_CANARY_NETWORK_SENSITIVITY_CANONICAL_RECORD_CANDIDATE_01.md`.

Candidate 03 MUST NOT be described as the source of that historical evidence. The earlier network-sensitivity documentation package itself installed no source and did not contain Candidate 03.

## 10. Accepted Candidate 03 corrections

Sentinel accepted Candidate 03 with these source properties:

1. permanent exact-Git-HEAD runtime gate removed;
2. obsolete canonical-base stop and override argument removed;
3. Store narrowed to read-only trade loading;
4. Store performs no directory creation;
5. Store has no save or write methods;
6. Store has no markets, resolutions, prices, or coverage API;
7. Store has no `schemas.py` dependency;
8. no `yes_price` or complement-price semantics;
9. `schemas.py` excluded;
10. one narrow `.gitignore` exception for the diagnostic script.

## 11. Accepted local non-network validation

### 11.1 Exact validated source

- script SHA-256: `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006`;
- Store SHA-256: `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95`.

### 11.2 Controls

- `dry_run = true`;
- `execute_network = false`;
- `save_raw = false`;
- `executed_requests = 0`;
- no raw directory;
- no request-results JSONL;
- no condition filter;
- no subclass filter;
- no maximum-condition restriction;
- no maximum-request restriction.

### 11.3 Reconciliation

| Field | Count |
|---|---:|
| `final_p0_rows_loaded` | `39693` |
| `token_pair_clear_conditions` | `39693` |
| `request_eligible_conditions` | `18624` |
| `request_eligible_token_sides` | `37248` |
| `INVALID_DECISION_WINDOW` | `21069` |
| `REQUEST_ELIGIBLE` | `18624` |
| request-manifest rows | `37248` |

Required invariants:

- `21069 + 18624 = 39693`;
- `18624 × 2 = 37248`.

All specified checks passed:

`failed = []`

Accepted finding:

`LOCAL_NON_NETWORK_VALIDATION_CLEAR`

This establishes local planning and reconciliation equivalence only. No dry-run output-file identity was supplied or invented.

## 12. Accepted bounded network canary

### 12.1 Exact source

- script SHA-256: `2083a847a25d56589e79c0120f0ed8338c657ff539e7a7948dad6111a12d8006`;
- Store SHA-256: `68ff4e4b4f60e6726dc961ccb67572a4b03e1e9bbb40716844e67390d952fd95`.

### 12.2 Run controls

| Control | Value |
|---|---|
| endpoint base | `https://clob.polymarket.com` |
| endpoint path | `/prices-history` |
| `execute_network` | `true` |
| `dry_run` | `false` |
| `save_raw` | `false` |
| `max_requests` | `100` |
| `max_conditions` | `null` |
| `condition_id_filter` | `[]` |
| `subclass_filter` | `[]` |
| `resume` | `false` |
| `retry_count` | `0` |
| `fidelity` | `1` |
| `interval` | omitted |
| `timeout_seconds` | `30` |
| `sleep_seconds` | `0` |
| token acquisition | one independent request per token side |
| complement synthesis | prohibited and unused |
| winner-based token enumeration | prohibited and unused |

Started: `2026-07-30T09:15:13Z`

Completed: `2026-07-30T09:25:28Z`

### 12.3 Outcome

| Field | Count |
|---|---:|
| `executed_requests` | `100` |
| HTTP 200 | `100` |
| `TRANSPORT_OK` | `100` |
| `SERIES_PRESENT` | `100` |
| `in_window_present_sides` | `100` |
| `in_window_empty_sides` | `0` |
| `condition_both_sides_present` | `50` |
| `condition_one_side_present` | `0` |
| `condition_neither_side_present` | `0` |
| `condition_side_not_measurable` | `0` |
| `error_response_count` | `0` |
| `malformed_response_count` | `0` |
| `skipped_resumed_rows` | `0` |
| `condition_incomplete_bounded_run` | `18574` |

Planning reconciliation remained `39693 / 18624 / 37248 / 21069 / 18624`.

All verification checks passed:

`failed = []`

Accepted finding:

`BOUNDED_100_REQUEST_NETWORK_CANARY_CLEAR`

## 13. Local bounded-canary evidence identities

| Local evidence file | Bytes | SHA-256 |
|---|---:|---|
| `run_metadata.json` | `2115` | `c70519868568e68e99ce43f1fa7f4bf0c09a49d4d6298be6a5e9a6b1dd2bea8c` |
| `manifest/request_manifest_summary.json` | `1728` | `a375fecf654866d90c437db8d1af6f1ea777f8b8f626ccc49a9a9aabbf73ff8b` |
| `manifest/request_manifest.csv` | `15749521` | `e60caa4de2a0e4ad09244bd7b9084dd2c3eb1810bc2ca8e43c1adb810e0d5f5f` |
| `results/request_results_summary.json` | `1573` | `d12581fe9e26e8285741260b5723d51f62efea77719bbcccaec21adb8ce01fe2` |
| `results/request_results.jsonl` | `121528` | `95ae11153b8cc0dab2f22de290aef334c8af9f2218c92b81a2712574d31c9126` |

These are local empirical evidence identities only. They are not canonical repository members and MUST NOT be included in this documentation package or proposed for repository installation.

`results/request_results.jsonl` MUST NOT be called immutable raw-response evidence. `save_raw = false`, and no raw directory existed.

## 14. Current lifecycle

| Lifecycle boundary | Current state |
|---|---|
| source candidate | `STATIC_REVIEW_ACCEPTED` |
| local non-network validation | `LOCAL_NON_NETWORK_VALIDATION_CLEAR` |
| bounded 100-request network canary | `BOUNDED_100_REQUEST_NETWORK_CANARY_CLEAR` |
| canonical remote installation | `CANONICAL_REMOTE_INSTALLATION_VERIFIED` |
| source-installation anchor commit | `1a19e1ef715ceca7aef9d55f7aa2446961e13c35` |
| validation execution authorization | `CONSUMED` |
| further execution authorization | `NONE` |
| accepted per-token price artifact | `NONE` |
| P1 | `BLOCKED` |
| P2 | `UNAUTHORIZED` |
| P3 | `UNAUTHORIZED` |
| scoring | `UNAUTHORIZED` |
| probe execution | `UNAUTHORIZED` |
| `named_binary_probe_blocked` | `true` |

## 15. Required conclusions and limitations

This record may establish only that Candidate 03:

- is canonically installed at the exact source-installation anchor commit;
- has verified remote installation;
- matches the accepted Candidate 03 installed source identities;
- preserves the accepted local full-universe reconciliation and deterministic request plan;
- loads local trades through the narrowed read-only Store;
- completed one bounded 100-request run against `/prices-history`;
- had both token sides present for all `50` bounded conditions;
- used no prohibited complement or winner-derived shortcut.

It MUST NOT claim:

- full `37248`-request source viability;
- long-run transport stability;
- full-universe price acquisition;
- immutable raw-evidence closure;
- S2 artifact construction;
- price-artifact acceptance;
- P1 readiness or unblock;
- P2/P3 authorization;
- scoring or probe readiness;
- any gate change;
- authorization for another diagnostic or endpoint request.

## 16. Preserved guardrails and state

The following remain exact:

- research project only;
- P0 `P0_CLEAR`;
- final P0 eligible `39693`;
- request-eligible conditions `18624`;
- request-eligible token sides `37248`;
- P1 `BLOCKED`;
- P2/P3, scoring, and probe execution `UNAUTHORIZED`;
- `named_binary_probe_blocked = true`;
- accepted per-token price artifact `NONE`;
- `yes_price`, `1 - price`, `1 - yes_price`, `1 - p`, complement synthesis, and winner-derived token enumeration remain prohibited unblock paths;
- no stage follows automatically from source installation or bounded validation.

## 17. Documentation lifecycle distinction

The following identities and lifecycles MUST remain distinct:

1. source-installation anchor commit: `1a19e1ef715ceca7aef9d55f7aa2446961e13c35`;
2. future documentation-installation commit: not created, not supplied, and not authorized by this package;
3. current source lifecycle: through `CANONICAL_REMOTE_INSTALLATION_VERIFIED`;
4. current documentation package lifecycle: `REVIEW_CANDIDATE`, pending Sentinel decision and any later separately authorized installation.

This record does not invent a future documentation-installation commit.

## 18. Acceptance evidence

Sentinel SHOULD verify:

1. canonical `main` equals `1a19e1ef715ceca7aef9d55f7aa2446961e13c35`;
2. parent equals `ed045a6ce0130c1c245e4a5bee98fe1b09be83cb`;
3. tree equals `d8a530b598735fc9d98294698a21d4d072162414`;
4. commit message matches exactly;
5. the commit is one commit ahead of the parent;
6. the changed-path set is exactly the nine paths in §6;
7. all nine Git blob identities match;
8. installed source bytes and SHA-256 identities match §8;
9. `.gitignore` contains exactly the narrow diagnostic exception;
10. historical source attribution remains separate;
11. local and bounded validation counts reconcile;
12. local empirical files are absent from the package and repository proposal;
13. no full-scale, artifact, P1, scoring, probe, or gate conclusion is claimed;
14. all historical pre-installation fields are explicitly historical and all current fields are updated.

## 19. Authorization statement

This record and package authorize no source or test edit, `.gitignore` change, staging, local commit, exact commit review, push, merge, amend, branch, tag, reset, ref update, import, test, compilation, linting, type checking, coverage, local research-data read, network/API/RPC/vendor/Dune/endpoint activity, raw-response access or copying, raw saving, diagnostic execution, another dry run or canary, full diagnostic, S2 artifact construction, price-artifact construction or acceptance, P1/P2/P3, scoring, probe execution, or gate change.

Authorization effect:

`NONE`

## 20. Requested Sentinel decision

`APPROVE`

Approval would accept this updated lifecycle record as a documentation review candidate only. It would not authorize its installation or any further technical or empirical activity.
