# Static consistency report — REV23 Finding 4 final mechanical packaging

Status: `COMPLETE_FOR_SENTINEL_REVIEW_NOT_ACCEPTED`

## Checks

- **PASS** — all nine source inputs exact and ordered. Evidence: `SOURCE_INPUTS_SHA256SUMS.txt`.
- **PASS** — eleven direct targets match frozen hashes. Evidence: `TARGET_SHA256SUMS.txt`.
- **PASS** — ten unchanged targets byte-identical. Evidence: `BASELINE_TARGET_INTEGRITY.json`.
- **PASS** — schema registry frozen hash and size. Evidence: `approved preflight`.
- **PASS** — support schema set count 18. Evidence: `SUPPORT_SCHEMA_COVERAGE.json`.
- **PASS** — prepared role domain/matrix count 30 and exact equality. Evidence: `PREPARED_ROLE_MATRIX.json`.
- **PASS** — prepared structural member count exactly 8. Evidence: `PATH_GRAMMAR_REGISTRY.json`.
- **PASS** — prepared object member is nonstructural and descriptor selected. Evidence: `PATH_GRAMMAR_REGISTRY.json`.
- **PASS** — zero unresolved schema references. Evidence: `SCHEMA_REFERENCE_AUDIT.json`.
- **PASS** — all Section 26 obligations concrete. Evidence: `SECTION_26_COVERAGE_MATRIX.json`.
- **PASS** — RFC 6902 patch reconstructs exact schema bytes. Evidence: `SCHEMA_REGISTRY_REV23.finding4.rfc6902.json`.
- **PASS** — governing manifest semantic hash recomputes. Evidence: `GOVERNING_PACKAGE_MANIFEST_REV23.json`.
- **PASS** — governing manifest sidecar binds exact file. Evidence: `GOVERNING_PACKAGE_MANIFEST_REV23.sha256`.
- **PASS** — accepted checksum inventory complete and exact. Evidence: `ACCEPTED_CONTRACT_SHA256SUMS.txt`.
- **PASS** — all authorization flags false. Evidence: `MATERIALIZATION_STATUS.json`.
- **PASS** — named_binary_probe_blocked preserved. Evidence: `MATERIALIZATION_STATUS.json`.

## Hash anchors

- Frozen schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689` (864789 bytes)
- Frozen effective amendment: `ffe8d209e3a5a7b8b0df1996f67172d781e0dd163a5d070501f1147eed5941d1`
- Governing manifest file: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- Governing manifest semantic hash: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`
- Accepted checksum inventory: `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`

## Hash-cycle closure

The governing manifest excludes itself, its sidecar, and package-level checksum/archive objects. `PACKAGE_MANIFEST.json` excludes itself and `SHA256SUMS.txt`; `SHA256SUMS.txt` excludes itself. The archive sidecar is detached. No circular hash is present.

## Archive policy

The deterministic archive is created only after all internal files pass validation. It contains one root directory, sorted relative paths, fixed timestamps, regular files only, and no absolute, traversal, or symlink entries. The detached sidecar is computed from the final archive bytes after archive closure.

## Authorization boundary

This report validates specification materialization and packaging only. It authorizes no implementation, tests, project execution, local research-data access, network/curl activity, replay, empirical work, source synchronization, Git write, downstream phase, or gate change. `named_binary_probe_blocked=true`.
