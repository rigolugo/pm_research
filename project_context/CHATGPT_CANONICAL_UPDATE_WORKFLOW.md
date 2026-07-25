# CHATGPT CANONICAL UPDATE WORKFLOW

*Manual-update rule for canonical project files.*

---

## Purpose

This file governs how canonical project-context file updates are prepared for the `pm_research` project.

It exists to prevent accidental direct repository writes and to keep the role split clean:

- ChatGPT = orchestrator/reviewer and canonical-document update preparer.
- Claude = implementation/spec-drafting agent.
- User = manual uploader/committer of canonical files.

---

## Canonical source of truth

The canonical source of truth remains the private GitHub repo:

`rigolugo/pm_research`

For every project chat, read first:

1. `START_HERE.md`
2. `project_context/START_HERE.md`
3. The required files listed there.

Old chats, memory, uploaded duplicates, local copies, archived notes, and public mirrors are not source of truth.

If anything conflicts with the private canonical repo, the private repo wins.

---

## Rule: ChatGPT must not write to GitHub

ChatGPT must not directly modify GitHub for this project.

Do **not** use GitHub write actions from ChatGPT, including:

- create file;
- update file;
- delete file;
- create branch;
- update branch/ref;
- open pull request;
- merge pull request;
- commit changes;
- otherwise mutate the repo.

ChatGPT may use GitHub read-only actions to inspect canonical files.

The user will manually upload, copy, commit, or otherwise apply file changes.

---

## Rule: complete replacement files, not patch snippets

When canonical files need updates, ChatGPT must:

1. Read the current canonical file from `rigolugo/pm_research`.
2. Prepare the updated content locally.
3. Provide the user with a downloadable package containing the **complete replacement file**, not only a patch snippet.
4. Identify exact target paths for manual upload.

This applies to files such as:

- `project_context/START_HERE.md`
- `project_context/PROJECT_STATE.md`
- `project_context/DECISION_LOG.md`
- `project_context/ARTIFACT_INDEX.md`
- `project_context/GUARDRAILS.md`
- accepted spec files
- handoff/index/context files
- any other canonical project file

Patch snippets may be included as explanatory notes, but the deliverable must include the full updated file whenever a canonical file is to be changed.

---

## Rule: do not ask Claude to update canonical repo files

Claude should not be prompted to update canonical project files in the repo.

Claude may still be asked to:

- draft a spec;
- implement code, if explicitly authorized;
- produce a handoff memo;
- return findings;
- generate candidate text for review.

But canonical source-of-truth docs should be updated through this ChatGPT manual-file workflow.

If Claude produces text that should become canonical, ChatGPT must review it, then prepare the full updated canonical files for the user to upload manually.

---

## Standard ChatGPT workflow for canonical doc updates

For any canonical documentation update:

1. Start with the required project decision label:
   - `APPROVE`
   - `BLOCK`
   - `DEFER`
   - `ACCEPT FINDING`
   - `NEEDS VERIFICATION`

2. Read the current canonical source files from GitHub.

3. Prepare complete replacement files locally.

4. Package the updated files into a downloadable ZIP.

5. Tell the user:
   - exact files included;
   - exact target repo paths;
   - whether the package is full-file replacement or new-file addition;
   - what was intentionally not changed;
   - that no GitHub write occurred.

6. If Claude needs to continue after the manual update, provide a short Claude prompt that asks Claude to verify/read/use the updated files, not to edit them.

---

## Canonical update delivery-method selection

Use the least complex delivery method that preserves the required review boundary.

### Browser branch — default for documentation-only work

A temporary GitHub browser branch is the default when all changed files are ordinary text documentation or specification files, no binary or ignored file is involved, and browser upload limits are not exceeded.

Required sequence:

1. create the temporary branch from the exact package base;
2. upload only the package's complete replacement and new files;
3. create one branch commit with the exact approved message;
4. return the exact branch commit to Sentinel;
5. do not merge or update canonical `main` until Sentinel verifies the commit and Gustavo separately authorizes the merge;
6. after merge, return the exact canonical commit for Sentinel installation verification.

A browser branch commit is not canonical installation. Sentinel branch review does not authorize merge automatically.

Direct browser commits to canonical `main` are exceptional and limited to trivial, low-risk corrections after explicit Sentinel approval. They are not the default for multi-file packages.

### Local Git — required for higher-risk or byte-gated work

Use local Git when any of the following applies:

- live source or test paths change;
- a binary, ZIP, ignored file, or non-text evidence artifact is committed;
- exact pre-publication byte, Git-mode, staged-blob, or commit-tree verification is decision-bearing;
- the change exceeds browser limits;
- authorized local tests or other local verification must be tied to the exact candidate commit;
- the accepted package explicitly requires a local commit gate.

Required sequence:

1. install exact authorized bytes at the exact base;
2. create one local commit only;
3. stop before push;
4. return the exact local commit to Sentinel;
5. Sentinel reviews the parent, message, changed paths, statuses, modes, and committed blobs;
6. Gustavo separately authorizes the exact push;
7. perform one ordinary non-force fast-forward push only;
8. return the remote commit for Sentinel installation verification.

Local commit authorization is not push authorization. Sentinel approval of a local commit is not push authorization. A push or merge never follows automatically.

---

## Commit, review, push, and canonical verification are separate boundaries

The following are distinct and must not be inferred from one another:

1. package acceptance;
2. package installation or local/branch commit authorization;
3. exact commit review;
4. push or merge authorization;
5. push or merge execution;
6. canonical remote installation verification.

If the remote base changes before a push or merge, stop. Do not pull, merge, rebase, reset, restore, force, repair, or widen scope automatically.

Every approved push must identify the exact reviewed commit, exact parent/remote base, exact branch or refspec, exact changed paths, and non-force behavior.

---

## Planned reusable manifest-driven local Git tool

A future reusable administrative tool may reside outside the research repository at:

`C:\b1\tools\pm_canonical_git\`

Preferred design:

- PowerShell implementation engine;
- optional thin `.cmd` launchers;
- separate install and push runners;
- package-specific closed JSON authorization files;
- separately versioned tool repository or immutable release archive;
- exact tool release and SHA-256 recorded in each operation authorization;
- structured results written outside `pm_research`.

Decision-bearing values must be explicit in JSON, including:

- required repository and base commit;
- package path and SHA-256;
- exact replacement and new-file paths;
- commit message;
- reviewed local commit;
- exact remote parent, branch, and refspec;
- force behavior;
- authorized action.

Environment variables may provide convenience defaults such as tool, package, or repository directories. They must not control decision-bearing authorization fields.

The install runner must always stop before push. The push runner must require a separate exact push authorization. A combined install-and-push mode and an install `-Push` switch are prohibited.

The presence, design, or accepted release of this tool authorizes nothing. Tool specification, implementation, synthetic pilot execution, real repository use, local commit, and push each require their own accepted and authorized boundary.

No executable tool is included or authorized by this documentation rule.

---

## Canonical implementation-progress checkpoints

Material implementation progress must not depend only on a chat session, model
memory, untracked local files, or an agent's private workspace.

When exact work must be preserved before acceptance, ChatGPT prepares an
**evidence-only checkpoint** under the relevant canonical handoff directory:

`implementation_checkpoints/<checkpoint_id>/`

The checkpoint must:

1. store exact submitted bytes under `payload_exact/`, never at the executable source path;
2. record byte length and SHA-256;
3. record governing scope, authorization ID, source gate, and strongest available baseline;
4. separate preservation, conformance, acceptance, and authorization states;
5. label missing lineage or activity evidence as unknown rather than infer it;
6. include a checksum inventory;
7. update the checkpoint index and latest-preserved pointer;
8. state explicitly that checkpoint presence authorizes nothing.

Checkpoint capture is required at material handoff boundaries, including before
changing implementation chats or models, before a known session limit, after a
material correction round, before rollback or restoration, and whenever an
agent reports readiness for Sentinel review.

Claude returns exact files and textual evidence only. ChatGPT reviews and
packages the canonical checkpoint. The user manually commits it. Sentinel then
verifies the exact installation commit.

A preserved checkpoint must not be promoted to the executable source path unless:

- the governing specification is accepted;
- Sentinel accepts implementation conformance;
- Gustavo explicitly authorizes promotion or the next implementation stage.

Preservation does not imply conformance, acceptance, execution permission, test
permission, or downstream-phase authorization.

---

## Claude prompt constraint

Any future prompt to Claude that references canonical docs should include this constraint when relevant:

```text
Do not update canonical project-context files in the repo.
If a canonical doc update is needed, return a handoff/finding only.
ChatGPT will prepare complete replacement files for the user to upload manually.
```

---

## Non-authorization

This workflow rule authorizes no research execution.

It does not authorize:

- implementation;
- tests;
- local data runs;
- network/API/RPC/vendor calls;
- Dune runs;
- price-source builds;
- P1/P2/P3 continuation;
- probe execution;
- scoring;
- wallet discovery;
- OrdersMatched expansion;
- `log_index` work;
- PnL-by-role;
- paper trading;
- live trading;
- wallet-copying;
- gate changes.

All project guardrails remain in force.
