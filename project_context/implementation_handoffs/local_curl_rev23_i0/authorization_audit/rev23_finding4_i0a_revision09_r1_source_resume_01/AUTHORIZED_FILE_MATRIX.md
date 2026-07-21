# Authorized File Matrix

| Path | Stage status | Required starting SHA-256 |
|---|---|---|
| `pm_research/local_curl_per_side/__init__.py` | READ-ONLY | `200019940bbd2c2b8dbac7d322722c7eae43926264c1438ec4a60cfc26e12c93` |
| `pm_research/local_curl_per_side/canonical.py` | READ-ONLY | `60f3141184753d294b8e708a77f381bdd40d04e39c6d1101f2cc14de9a9704b3` |
| `pm_research/local_curl_per_side/claim_hashes.py` | READ-ONLY | `e9153abcbdb073a37d516056ff6fd657742c4d87620f557363855b3c6d728a3d` |
| `pm_research/local_curl_per_side/finding4_registry.py` | READ-ONLY | `06fd23245017fb538d06841d2b2b61f309f533959d16449ace588ccb6080e529` |
| `pm_research/local_curl_per_side/governing_package.py` | READ-ONLY | `75c9b5a19023d737d016bfd0e3e5b9b62ea7730355da7d555aa073192df79fec` |
| `pm_research/local_curl_per_side/prepared_evidence.py` | SOLE WRITABLE PATH after activation | `8b8e9320fb4a30245914e93fb99bdbbadee685ad0fd62cc79098adec05004d07` |
| `tests/local_curl_per_side/test_canonical_i0a.py` | READ-ONLY | `9122ee3a0a4aa93f485a7dc35dbd7420e59b07eeed646007baff4ef5ac652bcd` |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | READ-ONLY | `4e2c8d6d663238c8bd7d3a4f40047bf0888b2ccf64cd5fcf37ce85cd2f158878` |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | READ-ONLY | `fe7a602684b4861db1cb825c0b70f712c9242ef61386d1a76f80ea8f4fed42f8` |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | READ-ONLY | `c1b6a221a997e9c7d5aae0bf5c5bf98f38d0d1e8183bcabbebc8c7f1ac0550e4` |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | READ-ONLY | `c8e69789fc63eebff3d87f14ca6c94748872483e8fcffd541243ffa32e114679` |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | READ-ONLY | `c9c5f9e09136f70902dc70e809d82177303319f431f532126b5aee8d04c2ae37` |

Every repository path outside these twelve baseline paths is prohibited from
creation, editing, deletion, rename, or generation during R1. Test-source
editing is not authorized. The matrix contains exactly one writable path.
