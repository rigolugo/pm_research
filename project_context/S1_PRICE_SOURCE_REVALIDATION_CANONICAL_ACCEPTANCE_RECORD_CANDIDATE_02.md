# S1 Price-Source Revalidation Canonical Acceptance Record — Candidate 02

## 1. Status

- candidate ID:
  `S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02`
- authoring mode: `DOCUMENTATION_ONLY_CANONICAL_RECORD_DRAFT`
- status: `DRAFT_FOR_SENTINEL_REVIEW`
- authority class: `PROPOSED_CANONICAL_DOCUMENTATION`
- author: Professor
- reviewer and decision owner: Sentinel
- decision date to memorialize: `2026-07-26`
- authorization effect: `NONE`

This candidate is not accepted, installed, canonical, or implementation-ready.
It memorializes a settled empirical Sentinel finding in draft canonical
documentation pending independent Sentinel review and later canonical
installation.
`S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_01` is
historical, blocked, non-controlling, and not proposed for canonical
installation.

## 2. Purpose and definition of done

Purpose: preserve the method-qualified revised-S1 finding and its reviewed
evidence identities in canonical project documentation without erasing the
historical S1 negative or implying price-artifact acceptance, P1 unblocking, or
downstream authorization.

Definition of done: Sentinel can verify from this candidate, its manifest, its
complete replacement files, and its checksums that the historical and revised
request methods, denominators, results, evidence identities, state effects, and
non-authorization boundaries are recorded exactly and without unrelated
canonical-state loss.

## 3. Canonical base and source precedence

- repository: `rigolugo/pm_research`
- branch verified: `main`
- expected and observed base commit:
  `aa378029469c518655ec22756243ee62318011b1`
- root bootstrap: `START_HERE.md`
- canonical bootstrap: `project_context/START_HERE.md`
- controlling hard constraints: `project_context/GUARDRAILS.md`
- controlling active state: `project_context/PROJECT_STATE.md`
- settled history: `project_context/DECISION_LOG.md`
- closed matters: `project_context/CLOSED_FINDINGS.md`
- artifact identities: `project_context/ARTIFACT_INDEX.md`
- canonical update workflow:
  `project_context/CHATGPT_CANONICAL_UPDATE_WORKFLOW.md`
- S1 specification:
  `project_context/SPEC_price_source_s1_coverage.md`
- historical accepted S1 result:
  `project_context/HANDOFF_orchestrator_s1_pass1_RESULT.md`

Source precedence:

1. Canonical repository state at the exact base controls existing project
   history, state, guardrails, contracts, and authorization.
2. The following empirical decision is a `SETTLED_SENTINEL_FINDING`:

   `ACCEPT FINDING — revised S1 establishes S1_SOURCE_VIABLE for the reviewed EC2 fidelity=1, no-interval request method.`

3. The empirical archive identities and results in this record are
   `REVIEWED_EXTERNAL_EVIDENCE`. Their hashes are recorded; the
   empirical archives are not represented as canonically stored.
4. This candidate MUST NOT redesign, broaden, or independently alter the
   settled finding.

## 4. In scope

This candidate records:

- the immutable historical S1 method-qualified negative;
- the revised reviewed request method;
- the unchanged 300-condition sample and 248/52 reconciliation;
- the incomplete main run and narrow continuation;
- final revised Pass-1 coverage and locked-threshold outcome;
- reviewed integrity and no-synthesis findings;
- exact evidence identities;
- the narrow state effect of `S1_SOURCE_VIABLE`;
- continued P1 and probe blocks;
- complete proposed replacements for only the four authorized canonical files.

## 5. Out of scope

This candidate does not:

- modify the canonical repository or any historical S1 record;
- accept or preserve an empirical archive in the repository;
- determine the causal effect of `interval=max`, explicit `fidelity=1`, or
  their interaction;
- validate the full P0 universe;
- build or accept a price artifact;
- authorize S2, Pass 2, full-universe requests, further networking, local-data
  execution, implementation, tests, P1/P2/P3, scoring, probe execution, or a
  gate change;
- change `named_binary_probe_blocked`;
- alter any Revision 23, Candidate 04, workspace-preparation, checkpoint, or
  implementation-authorization decision.

## 6. Immutable historical S1 finding

The historical accepted S1 method was:

- `interval=max`;
- fidelity omitted.

Its accepted sampled result remains:

`S1_SOURCE_NOT_VIABLE`

The original accepted S1-shape replay reproduced the historical Level-B results
for that request method. The historical finding remains valid evidence for that
method. It is not erased, invalidated, rewritten, or deleted by the revised
finding.

The revised finding supersedes only the historical negative's current gate
effect for deciding whether the separately reviewed revised method warrants
later S2 specification consideration.

## 7. Fixed sample and denominator reconciliation

The original stratified sample remains exactly `300` conditions.

| Population | Count | Disposition |
|---|---:|---|
| original stratified sample | 300 | fixed |
| accepted valid/query-eligible decision windows | 248 | revised S1 denominator |
| accepted invalid-window exclusions | 52 | retained exclusion |

Invariant:

`248 + 52 = 300`

No resampling, replacement, or outcome-based selection occurred.

The valid-window subclass denominators remained:

| Subclass | Denominator |
|---|---:|
| UP_DOWN | 50 |
| OVER_UNDER | 98 |
| NAMED_OTHER | 100 |
| combined | 248 |

Invariant:

`50 + 98 + 100 = 248`

The `52` invalid-window exclusions MUST remain visible and MUST NOT enter a
valid-window coverage denominator as negatives or positives.

## 8. Revised reviewed request method

For each valid-window condition, the main revalidation used:

- one independently queried token ID per side;
- `startTs = decision_lower_ts - 1`;
- `endTs = resolved_at_ts`;
- `fidelity = 1`;
- `interval` omitted;
- zero retries;
- no side synthesis;
- evaluation window `decision_lower_ts <= t < resolved_at_ts`.

Both sides were obtained through independent token-specific requests.

The following were not used:

- `yes_price`;
- `1 - price`;
- `1 - yes_price`;
- `1 - p`;
- complement synthesis;
- winning-token enumeration.

Complementarity was diagnostic only. It did not provide, reconstruct, replace,
or validate either side.

## 9. Main revalidation result

The main revalidation planned and completed exactly:

`248 valid-window conditions × 2 independently queried sides = 496 requests`

Observed outcomes:

| Outcome | Count |
|---|---:|
| HTTP 200 | 494 |
| HTTP 400 | 2 |
| total | 496 |

The two HTTP 400 responses were the two sides of one NAMED_OTHER condition. The
deterministic error was:

`invalid filters: 'startTs' and 'endTs' interval is too long`

The correct intermediate state was:

`S1_REVALIDATION_INCOMPLETE`

The incomplete main run MUST NOT be represented as a false viability or
non-viability verdict.

## 10. Narrow continuation

The separately reviewed continuation:

- targeted only the single unresolved NAMED_OTHER condition;
- independently queried both token sides;
- used two fixed overlapping chunks per side;
- issued exactly four requests;
- received four HTTP 200 responses;
- used `fidelity=1`;
- omitted `interval`;
- used zero retries;
- unioned each side's chunk histories;
- overlap-deduplicated the union;
- applied the unchanged global half-open evaluation window only after union and
  deduplication.

The continuation was a bounded completion for the deterministic request-length
failure. It was not a rerun, resampling operation, adaptive retry, outcome-based
selection, or change to the global evaluation window.

The remaining condition closed as:

`DECISION_PRICE_BOTH_SIDES`

## 11. Final revised Pass-1 result

| Subclass | Both sides | Denominator | Rate | Clears 0.95 |
|---|---:|---:|---:|---|
| UP_DOWN | 50 | 50 | 100% | yes |
| OVER_UNDER | 98 | 98 | 100% | yes |
| NAMED_OTHER | 100 | 100 | 100% | yes |
| combined valid-window sample | 248 | 248 | 100% | yes |

Every subclass cleared the locked `0.95` threshold.

The method-qualified revised result is:

`S1_SOURCE_VIABLE`

This result applies only to:

- the unchanged existing stratified Pass-1 sample;
- its `248` accepted valid/query-eligible windows;
- the reviewed EC2 execution route;
- the reviewed `fidelity=1`, no-`interval` request method, including the narrow
  fixed-chunk continuation required for the one deterministic length failure.

It is not full-universe validation.

It does not establish whether the difference from the historical result was
caused by:

- `interval=max`;
- explicit `fidelity=1`;
- omission of `interval`;
- an interaction among those settings;
- another method-specific behavior not isolated by this revalidation.

## 12. Reviewed integrity findings

The reviewed evidence reported:

- no malformed points;
- no prices outside `[0,1]`;
- no timestamp-order violations;
- no conflicting duplicate timestamps.

These are reviewed findings for the identified evidence only. This record does
not reopen or reprocess the archives and does not manufacture new empirical
evidence.

## 13. Evidence identities

### 13.1 Original accepted S1-shape replay

| Evidence | SHA-256 |
|---|---|
| manifest | `90c29244c77fdf326e06bf8a504d0c0d65e508a6d31a1ef04f8ddc34c938b3c9` |
| replay script | `d915b5ccb78bb1f3e73465205248f713866368d86738369eaf9b1ef256146210` |
| replay archive | `de283c8c70f34331014cb994eae06bf4cb4a4b3b0d490d2fd6c12a73a21b2042` |

Accepted replay label:

`REPLAY_ORIGINAL_S1_SHAPE_BOTH_SIDE_IN_WINDOW_MIXED`

### 13.2 Revised 248-condition revalidation

| Evidence | SHA-256 |
|---|---|
| source ledger | `44752917daf26d489e737d62541813221e7ec5291ca5d41f6f8e7ed2414000ea` |
| runner | `464755a4bcf640bb160e3bd73c5105af69d56967be76be124f458ecb3eecb584` |
| incomplete-run archive | `8ac9b723c864e997332c8da9e9f867cf71886627c8ed26b21fad4b21a54e6ad3` |

Reviewed internal checksum entries: `1997`.

Intermediate label:

`S1_REVALIDATION_INCOMPLETE`

### 13.3 Narrow continuation

| Evidence | SHA-256 |
|---|---|
| continuation runner | `1959f6d49a67d6583db10971d84af1bcf117be99c26b761e4c299b16492c3d1e` |
| continuation archive | `8d25d874984b88ce2ca3d6a5e9a09d394e5f97f3ada97483c271e35dc89f115c` |

Reviewed internal checksum entries: `27`.

Continuation label:

`S1_REVALIDATION_CONTINUATION_COMPLETE_BOTH_SIDES`

These hashes identify reviewed external evidence. They do not assert that the
empirical archives or their internal members are stored in the canonical
repository.

## 14. Decision and state semantics

The following distinctions are mandatory:

| Question | State |
|---|---|
| historical method disposition | `S1_SOURCE_NOT_VIABLE` retained for `interval=max`, fidelity omitted |
| revised reviewed method disposition | `S1_SOURCE_VIABLE` for `fidelity=1`, `interval` omitted |
| full-universe validation | not established |
| causal parameter attribution | not established |
| source viability | established only for the reviewed sample, method, and EC2 route |
| canonical-side decision-time price artifact built | no |
| price artifact accepted | no |
| P1 | blocked |
| `named_binary_probe_blocked` | `true`, unchanged |
| authorization effect | `NONE` |

Source viability is not an accepted price artifact.

No canonical-side decision-time price artifact has been built or accepted.
P1 therefore remains blocked on an accepted per-side/token-identity
decision-time price artifact.

## 15. Authorization statement

This record and its candidate package authorize no:

- S2 or Pass 2;
- full-universe requests;
- price-artifact construction;
- P1, P2, or P3;
- scoring or probe execution;
- further network or vendor access;
- local research-data access or execution;
- implementation or tests;
- gate change;
- canonical installation, merge, push, commit, branch, or ref update.

After this record is accepted, canonically installed, and Sentinel-verified,
Gustavo may separately decide whether to authorize Professor to draft an S2
SPEC-ONLY candidate. That authorization is not included here.

## 16. Proposed canonical changed-path allowlist

Complete replacements:

- `project_context/START_HERE.md`
- `project_context/PROJECT_STATE.md`
- `project_context/DECISION_LOG.md`
- `project_context/ARTIFACT_INDEX.md`

New proposed immutable documentation:

- `project_context/S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02.md`
- `project_context/S1_PRICE_SOURCE_REVALIDATION_EVIDENCE_MANIFEST_CANDIDATE_02.json`
- `project_context/HANDOFF_PROFESSOR_S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_02_REVIEW.md`

No other canonical repository path is proposed to change.

## 17. Assumptions and open decisions

No load-bearing architecture or data-contract assumption is introduced.

The empirical Sentinel finding is settled. Candidate 02 and its proposed
canonical documentation remain `DRAFT_FOR_SENTINEL_REVIEW` until Sentinel
independently verifies the package and a later canonical installation occurs.
`S1_PRICE_SOURCE_REVALIDATION_CANONICAL_ACCEPTANCE_RECORD_CANDIDATE_01`
remains blocked and non-controlling and MUST NOT be installed.

Open decision owner: Sentinel.

Decision required: whether this candidate faithfully memorializes the settled
finding and is suitable for a later separately authorized canonical
installation package.

Stop condition: any mismatch in base commit, historical-result preservation,
sample reconciliation, method identity, evidence hash, state effect, or
authorization boundary requires `BLOCK` or `NEEDS VERIFICATION`; it MUST NOT be
silently corrected through inference.

## 18. Acceptance evidence

Candidate conformance is established only if Sentinel independently verifies:

1. canonical base `aa378029469c518655ec22756243ee62318011b1`;
2. seven-path changed-path allowlist and no unrelated replacement drift;
3. exact 300/248/52 and 50/98/100 reconciliation;
4. exact historical and revised method qualification;
5. exact 496/494/2 and continuation 4/4 request counts;
6. exact final 50/50, 98/98, 100/100, and 248/248 coverage;
7. all eight evidence SHA-256 identities;
8. manifest JSON validity and agreement with this record;
9. package checksum count and checksum matches;
10. explicit P1/probe blocks and absence of S2, execution, implementation, test,
    networking, or gate-change authority.

These are static documentation, schema, checksum, diff, and semantic-review
methods only. No empirical rerun or archive reprocessing is authorized by this
candidate.

## 19. Requested Sentinel decision

`APPROVE`, `BLOCK`, `DEFER`, `ACCEPT FINDING`, or `NEEDS VERIFICATION`.

Professor requests `APPROVE` only if Sentinel independently verifies every
boundary above.
