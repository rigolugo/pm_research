# Implementation Checkpoints — Evidence-Only Canonical Progress

## Purpose

This directory preserves exact implementation progress across chat changes,
session limits, model changes, and review rounds without promoting unaccepted
bytes into executable source paths.

The private repository remains authoritative. A checkpoint is canonical evidence
only when its files are present in the repository and match their recorded
checksums.

## Authority boundary

Checkpoint presence means only that exact bytes and their provenance were
preserved. It does not mean that the implementation conforms, is accepted, may be
executed, or may be used as the starting point for further edits.

Every checkpoint separates four states:

1. `preservation_state` — whether exact bytes were captured and verified;
2. `conformance_state` — whether Sentinel reviewed the implementation against the controlling contract;
3. `acceptance_state` — whether Sentinel accepted the implementation;
4. `authorization_effect` — whether the checkpoint authorizes any action.

No checkpoint may carry implementation, test, execution, data, network, Git,
R2, P1/P2/P3, scoring, probe, or gate-change authorization merely because it is
newer than an accepted baseline.

## Required read order

1. `CHECKPOINT_INDEX.json`
2. `LATEST_PRESERVED_CHECKPOINT.json`
3. `LATEST_ACCEPTED_CHECKPOINT.json`
4. the selected checkpoint's `README_FIRST.md`
5. its `CHECKPOINT_MANIFEST.json`
6. `BASELINE_AND_LINEAGE.md`
7. `ACTIVITY_BOUNDARY_STATUS.md`
8. `KNOWN_FINDINGS.md`
9. `SHA256SUMS.txt`
10. `payload_exact/` only when exact byte inspection is required

Read governing scope and authorization files before this directory. The
checkpoint cannot override them.

## Payload rule

Files under `payload_exact/` mirror their intended executable path for identity
and recovery only. They are not executable project files and must not be
imported, run, tested, or copied into the live source tree without a separate
Sentinel decision and Gustavo authorization.

## Capture cadence

Prepare a canonical checkpoint at a material handoff boundary, including:

- before changing implementation chats or models;
- before a known session limit or context reset;
- after a material Sentinel-directed correction round;
- before sending a prompt whose expected starting hash differs from the latest preserved checkpoint;
- before rollback, restoration, rebase, or supersession;
- when an agent reports readiness for Sentinel review;
- when Gustavo requests that current progress be preserved.

Claude returns exact files and textual evidence. ChatGPT reviews the submission
and prepares complete canonical files. Gustavo manually commits them. Claude
must not update this directory directly.

## Current preserved checkpoint

- checkpoint ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`
- exact payload SHA-256: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`
- payload size: `112338` bytes
- acceptance state: `NOT_ACCEPTED`
- authorization effect: `NONE`
- installation package base: `80430225af793b10864ef2b43486d718c9872dee`
- preservation state: `CANONICALLY_PRESERVED`
- canonical installation state: `INSTALLED_AND_SENTINEL_VERIFIED`
- verified installation commit: `58acbac493840c45d84c6b7e33c583d722f4d559`

## Current governing contract

- controlling specification: `REV23_FINDING4_I0A_SCOPE_REVISION_10`
- verified scope-installation commit: `3d6fbe5eda504c32d94fed72be99adb9485fe1b1`
- current checkpoint conformance state: `BLOCKED_PENDING_PROVENANCE_AND_REVISION10_IMPLEMENTATION_CONFORMANCE_REVIEW`

Former T107/T153/Candidate 09 specification blockers are resolved. Checkpoint
acceptance remains blocked on provenance and implementation-conformance review.
