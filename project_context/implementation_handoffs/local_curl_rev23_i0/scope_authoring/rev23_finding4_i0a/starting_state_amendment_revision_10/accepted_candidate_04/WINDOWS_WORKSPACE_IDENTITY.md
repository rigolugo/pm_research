# Windows Isolated-Workspace File Identity — Candidate 04

## 1. Status

`SPEC ONLY — NOT ACCEPTED — AUTHORIZATION EFFECT NONE`

## 2. Platform and location

The proposed authoring workspace is a Windows filesystem staging root outside:

- the canonical repository checkout;
- every other Git checkout or linked worktree;
- the accepted capture evidence directory;
- every project data or artifact directory.

The root MUST contain no `.git` file or directory, index, object database, refs, hooks, submodule metadata, or worktree metadata.

## 3. Workspace member identity

A workspace member is identified only by the tuple:

```text
(exact repository-relative path, REGULAR_FILE, exact size_bytes, exact lowercase SHA-256)
```

Git mode is not part of isolated-workspace identity. The string `100644` MUST NOT be required, inferred, synthesized, or reported for the isolated workspace.

The exact twelve member identities are controlled by `EXACT_PATH_AND_BYTE_MATRIX.json`.

## 4. Windows alias and substitution prohibitions

For every member and every ancestor below the staging root, the workspace gate MUST reject:

- symbolic links;
- directory junctions;
- mount-point or other reparse-point aliases;
- alternate path aliases, including a distinct spelling that resolves to the same object;
- hard-link substitution or a link count indicating the file is shared with another path;
- case-folded duplicate paths;
- short-name or alternate-stream substitution;
- non-regular files, directories at member paths, devices, sockets, or named pipes;
- any path that escapes the staging root after canonical Windows path resolution.

The gate MUST verify the final resolved path remains beneath the exact staging root and that all twelve declared paths are unique under case-insensitive Windows path comparison.

## 5. Exact checks

A workspace-preparation clear requires:

1. initially zero members;
2. exact twelve relative paths;
3. every path resolves beneath the staging root;
4. every member is a regular file;
5. exact size and SHA-256;
6. no link, junction, reparse point, hard link, alias, duplicate, backup, cache, bytecode, generated, temporary, or extra member;
7. no Git metadata;
8. no repository file creation or modification.

A failure maps to the first applicable workspace predicate and stop in `WORKFLOW_DOMAIN.json`.

## 6. Later canonical materialization

Git mode `100644` is reserved exclusively for later canonical source or test materialization verification.

At that later stage, Sentinel verifies that each newly created Git path:

- is an exact declared CREATE action;
- is a Git regular file;
- has Git mode `100644`;
- has exact accepted bytes;
- was created only by Gustavo's separately authorized manual installation.

This later Git-mode rule does not retroactively add Git metadata or mode semantics to the isolated Windows workspace.

## 7. Non-authorization

No workspace was created and no capture was extracted for implementation by Candidate 04.
