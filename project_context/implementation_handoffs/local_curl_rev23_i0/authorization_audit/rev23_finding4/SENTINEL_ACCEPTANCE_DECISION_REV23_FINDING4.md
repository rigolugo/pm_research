# Sentinel Acceptance Decision — REV23 Finding 4

Decision: **APPROVE**

Sentinel accepts the materialized REV23 Finding 4 package and its detached archive binding.

## Accepted package

- canonical archive name: `REV23_FINDING4_MATERIALIZED_PACKAGE.zip`
- size: `949069` bytes
- SHA-256: `9ec22f611a1f6b8a598725e0b60b7591503fd6271ae79eb366359e7e312099f8`
- review scope completed: specification conformance, frozen preflight, target-byte equality, transformation reconstruction, package integrity, and detached-sidecar binding

## Effective contract hashes

- effective specification: `e52f70bb243bc431880c2eaabba7403f7a5d786b70d8a5e903b9026b4bde7a76`
- schema registry: `c9e8fe1b2c64f64e9cefd76e820c9589708723485ff7e54f4f69e3fe4ed49689`
- request-plan and authorization contract: `926d1503f20965f2573e2b24d79e747438254f77200b2060bcb741f6279556d0`
- governing-package semantic SHA-256: `a1368d6f109bb6c1812c9f92d5dd72d4717287fd80fc441726a788a69ad07d9f`
- governing-manifest complete-file SHA-256: `8cd3c6c93b6f1bba1906b1b2b3f67f6e87846991368bb34b5da52044adbc1f38`
- accepted-contract checksum inventory SHA-256: `be9fe20717a0dc54bd7c73558ea201eb90265bd760e1f7fb78202654cca533f9`

## Canonical installation state

This decision accepts the package bytes. Canonical installation remains **pending manual upload and post-commit Sentinel verification**.

The canonical installation commit must be a descendant of
`f6cb60df66c2bbcdfb6d797119ed25ad79e06a11` and must contain only the
authorized canonical-document/package changes.

## Authorization boundary

Finding 4 acceptance and installation do not authorize implementation,
test-source authoring, test execution, project-code execution, local research-data
reads, source synchronization, network/curl, replay, empirical work, P1/P2/P3,
scoring, probe execution, or gate changes.

The earlier Amendment 03 I0 implementation authorization is superseded for the
new Finding 4 contract. A new bounded implementation decision requires separate,
explicit Gustavo authorization after canonical installation is verified.

`named_binary_probe_blocked = true`.
