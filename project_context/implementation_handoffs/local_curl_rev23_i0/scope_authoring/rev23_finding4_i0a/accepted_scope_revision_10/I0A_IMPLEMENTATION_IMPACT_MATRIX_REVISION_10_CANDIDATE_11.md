# I0A Implementation-Impact Matrix — Revision 10 Candidate 11

## Status and authority

Accepted Revision 09 controls. Candidate 10, ZIP SHA-256 `d5aa07180aae9685b21499d50e944ba5962379c77aa9cd5661ba7bde3dfb8979`, is the direct non-authoritative drafting predecessor. Candidate 09 and earlier candidates are non-controlling historical drafting or review evidence. Candidate 11 is not accepted and authorizes nothing.

Canonical repository HEAD inspected: `d3bd79f8fdb81c95340761aac27b3e3580d3e23d`.

## Current checkpoint state

- historical Revision 09 R1 authorized starting SHA-256: `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07`;
- latest canonically preserved implementation evidence: `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`;
- checkpoint ID: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4`;
- preservation state: `CANONICALLY_PRESERVED`;
- conformance: `BLOCKED_PENDING_CONTRACT_AND_PROVENANCE_REVIEW`;
- acceptance: `NOT_ACCEPTED`;
- authorization effect: `NONE`;
- Revision 10 implementation starting point: `NOT_AUTHORIZED_AND_NOT_YET_SELECTED`.

Candidate 11 creates no rollback, restore, overwrite, promotion, or implementation-start instruction.

## Exact twelve-path future-impact matrix

| Path | Historical R1 baseline SHA-256 | Latest preserved checkpoint SHA-256 | Current status | Candidate 11 implementation starting SHA | Future change | Reason | Class | Requirement | Later authorization |
|---|---|---|---|---|---|---|---|---|---|
| `pm_research/local_curl_per_side/__init__.py` | `200019940bbd2c2b8dbac7d322722c7eae43926264c1438ec4a60cfc26e12c93` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No public symbol or re-export change is required; private helpers remain unexported. | `SOURCE` | `NOT_IMPLICATED` | no |
| `pm_research/local_curl_per_side/canonical.py` | `60f3141184753d294b8e708a77f381bdd40d04e39c6d1101f2cc14de9a9704b3` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Materialize four Revision 10 public result codes and their total empty-assurance mappings. | `SOURCE` | `MANDATORY` | yes |
| `pm_research/local_curl_per_side/claim_hashes.py` | `e9153abcbdb073a37d516056ff6fd657742c4d87620f557363855b3c6d728a3d` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No accepted hash projection or constructor algorithm changes. | `SOURCE` | `NOT_IMPLICATED` | no |
| `pm_research/local_curl_per_side/finding4_registry.py` | `06fd23245017fb538d06841d2b2b61f309f533959d16449ace588ccb6080e529` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Materialize semantic-family path mapping, sole path decomposition, exact four-field SchemaBinding key, and unchanged resolver domain. | `SOURCE` | `MANDATORY` | yes |
| `pm_research/local_curl_per_side/governing_package.py` | `75c9b5a19023d737d016bfd0e3e5b9b62ea7730355da7d555aa073192df79fec` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | Pinned governing-package bytes and validation behavior remain unchanged. | `SOURCE` | `NOT_IMPLICATED` | no |
| `pm_research/local_curl_per_side/prepared_evidence.py` | `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` | `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da` | `R1_CHECKPOINT_CANONICALLY_PRESERVED_NOT_ACCEPTED` | `UNSELECTED_PENDING_SENTINEL_DECISION_AND_GUSTAVO_AUTHORIZATION` | yes | Potential later materialization of UnitContext, global path reduction, reuse/family/run binding, descriptor-set propagation, selected-sidecar ordering, typed projection, and caller pass-through. This is planning evidence only. The preserved fcf406c4 checkpoint is not accepted or authorized, the historical 8b8e9320 start is not the current implementation starting point, and no restore or overwrite is directed. | `SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_canonical_i0a.py` | `9122ee3a0a4aa93f485a7dc35dbd7420e59b07eeed646007baff4ef5ac652bcd` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Conformance coverage for new public result-code and assurance inventories. | `TEST_SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | `4e2c8d6d663238c8bd7d3a4f40047bf0888b2ccf64cd5fcf37ce85cd2f158878` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No hash helper behavior changes. | `TEST_SOURCE` | `NOT_IMPLICATED` | no |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | `fe7a602684b4861db1cb825c0b70f712c9242ef61386d1a76f80ea8f4fed42f8` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Conformance coverage for family mapping, path decomposition, binding key, direct resolver domain, and typed impossibility boundary. | `TEST_SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | `c1b6a221a997e9c7d5aae0bf5c5bf98f38d0d1e8183bcabbebc8c7f1ac0550e4` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | no | No governing-package behavior changes. | `TEST_SOURCE` | `NOT_IMPLICATED` | no |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | `c8e69789fc63eebff3d87f14ca6c94748872483e8fcffd541243ffa32e114679` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Contract closure, private types, precedence, authority chain, fixture namespace, case counts, and twelve-path consistency. | `TEST_SOURCE` | `MANDATORY` | yes |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | `c9c5f9e09136f70902dc70e809d82177303319f431f532126b5aee8d04c2ae37` | `NOT_APPLICABLE` | `R1_READ_ONLY_BASELINE` | `NOT_APPLICABLE` | yes | Behavioral and seam coverage for T166–T230, including sidecar-first unit reachability and delegated failures. | `TEST_SOURCE` | `MANDATORY` | yes |

Canonical row-array SHA-256: `0f0dbcde71d358380280e519e4f6c95987a2b8493d31cb640a9ec27ac9df211b`.

This matrix is planning evidence only. It does not authorize any edit, test, execution, rollback, restoration, overwrite, promotion, or implementation start.
