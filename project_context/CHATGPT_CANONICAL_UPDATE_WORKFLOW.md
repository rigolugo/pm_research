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
