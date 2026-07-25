# Provenance Gap Handling

Canonical repository: `rigolugo/pm_research`  
Canonical base inspected: `cc2964840d197a40d1c4ef567b42eda762c0be0a`  
Controlling accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`  
Preserved checkpoint evidence: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`  
Checkpoint state: `NOT_ACCEPTED`; authorization effect: `NONE`; static result: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`.


## 1. Separation rule

The remediation package addresses verified implementation-contract defects only. It does not establish or imply closure of either provenance gap. Absence of captured evidence is not evidence that activity or worktree bytes did not exist.

## 2. `MULTI_ROUND_ACTIVITY_LINEAGE_INCOMPLETE`

### Exact status

The exact current checkpoint bytes are observed, but the submitted narrative of multiple corrective rounds lacks complete round-by-round starts, ends, prompts, activity records, and Sentinel decisions.

### Effect on later authorization

- It affects checkpoint history, checkpoint result review, and any proposal to reuse checkpoint-derived lineage as trusted implementation provenance.
- It need not block a wholly new remediation from independently selected, independently captured starting bytes, provided the later authorization expressly does not rely on checkpoint lineage.
- It MUST block any claim that all historical rounds were accepted or that checkpoint bytes can be promoted based on lineage.

### Possible closure evidence

Complete round inventory with prompt/package identity, starting and ending SHA-256 per round, exact changed paths, activity logs, authorizations, Sentinel decisions, and custody chain. Alternatively, Sentinel may accept the gap as permanently historical while forbidding checkpoint-derived continuation; that is not factual closure.

### Authority

Gustavo authorizes any verification activity. Sentinel reviews evidence and decides whether it closes, bounds, or leaves the gap open.

## 3. `CURRENT_TWELVE_PATH_WORKTREE_NOT_INDEPENDENTLY_CAPTURED`

### Exact status

The checkpoint captured one payload, not an independent exact byte inventory of the complete twelve-path implementation worktree. Current worktree hash set and dirty/untracked state are unknown.

### Effect on later authorization

This gap directly affects any later implementation authorization that intends to use an existing local worktree, because exact starting bytes and scope cleanliness must be established. It can be closed or bypassed only by independently selecting and capturing a fresh authorized base and exact path hashes.

### Possible closure evidence

An independent, read-only capture of repository commit, branch, status, dirty/untracked files, and SHA-256/size for all twelve exact paths, plus custody identity and timestamp. If the executable paths are not present in canonical Git, the later authorization must identify the separately supplied starting-byte package and verify each member.

### Authority

Gustavo authorizes capture. Sentinel reviews identity, completeness, and whether the captured state may be selected. Professor cannot select it.

## 4. Non-conversion rules

- Closing either provenance gap cannot make the one-file checkpoint conformant to Revision 10.
- Implementation remediation cannot prove historical lineage.
- An unexplained missing artifact is `UNKNOWN`, not `ABSENT`.
- No package acceptance authorizes network, shell, project execution, Git writes, or forensic activity.
