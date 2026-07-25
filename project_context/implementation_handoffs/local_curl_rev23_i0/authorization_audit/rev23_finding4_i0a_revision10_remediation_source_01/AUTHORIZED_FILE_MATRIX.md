# Authorized File Matrix — Revision 10 Remediation Source Stage

Authorization ID: `REV23_FINDING4_I0A_REVISION_10_REMEDIATION_SOURCE_AUTHORING_01`  
Package-preparation base: `a4fb0e64056b58a229da481664e4234e3215cd91`  
Activation: conditional on canonical installation and local source-gate acceptance.

| Exact path | Class | Starting SHA-256 | Activity after activation | Status |
|---|---|---|---|---|
| `pm_research/local_curl_per_side/__init__.py` | source | `200019940bbd2c2b8dbac7d322722c7eae43926264c1438ec4a60cfc26e12c93` | read-only baseline verification | PROHIBITED FROM EDIT |
| `pm_research/local_curl_per_side/canonical.py` | source | `60f3141184753d294b8e708a77f381bdd40d04e39c6d1101f2cc14de9a9704b3` | minimum Revision 10 source authoring | WRITABLE — ATOMIC THREE-PATH STAGE |
| `pm_research/local_curl_per_side/claim_hashes.py` | source | `e9153abcbdb073a37d516056ff6fd657742c4d87620f557363855b3c6d728a3d` | read-only baseline verification | PROHIBITED FROM EDIT |
| `pm_research/local_curl_per_side/finding4_registry.py` | source | `06fd23245017fb538d06841d2b2b61f309f533959d16449ace588ccb6080e529` | minimum Revision 10 source authoring | WRITABLE — ATOMIC THREE-PATH STAGE |
| `pm_research/local_curl_per_side/governing_package.py` | source | `75c9b5a19023d737d016bfd0e3e5b9b62ea7730355da7d555aa073192df79fec` | read-only baseline verification | PROHIBITED FROM EDIT |
| `pm_research/local_curl_per_side/prepared_evidence.py` | source | `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` | minimum Revision 10 source authoring | WRITABLE — ATOMIC THREE-PATH STAGE |
| `tests/local_curl_per_side/test_canonical_i0a.py` | test source | `9122ee3a0a4aa93f485a7dc35dbd7420e59b07eeed646007baff4ef5ac652bcd` | read-only baseline verification | PROHIBITED FROM EDIT |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | test source | `4e2c8d6d663238c8bd7d3a4f40047bf0888b2ccf64cd5fcf37ce85cd2f158878` | read-only baseline verification | PROHIBITED FROM EDIT |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | test source | `fe7a602684b4861db1cb825c0b70f712c9242ef61386d1a76f80ea8f4fed42f8` | read-only baseline verification | PROHIBITED FROM EDIT |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | test source | `c1b6a221a997e9c7d5aae0bf5c5bf98f38d0d1e8183bcabbebc8c7f1ac0550e4` | read-only baseline verification | PROHIBITED FROM EDIT |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | test source | `c8e69789fc63eebff3d87f14ca6c94748872483e8fcffd541243ffa32e114679` | read-only baseline verification | PROHIBITED FROM EDIT |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | test source | `c9c5f9e09136f70902dc70e809d82177303319f431f532126b5aee8d04c2ae37` | read-only baseline verification | PROHIBITED FROM EDIT |

## Allowed new repository files

`NONE`.

Every repository path outside this exact twelve-path closure is prohibited. The nine read-only paths must remain byte-identical. Test-source authoring is a separate later decision.

## Atomicity

All three writable source files must be returned together for review. A partial candidate is a valid halt or incomplete handoff, not a conforming implementation.
