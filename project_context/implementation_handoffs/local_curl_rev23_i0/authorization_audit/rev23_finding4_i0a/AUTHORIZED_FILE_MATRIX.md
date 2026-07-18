# Authorized File Matrix — REV23 Finding 4 I0A

Status: **ACTIVE AFTER SENTINEL VERIFICATION OF THE AUTHORIZATION-INSTALL COMMIT**

| Exact path | Exact responsibility | Initial state |
|---|---|---|
| `pm_research/local_curl_per_side/__init__.py` | side-effect-free re-exports of declared public symbols only; no private helper/type export | create only |
| `pm_research/local_curl_per_side/canonical.py` | closed enums/dataclasses and exact typed-cell/typed-row byte constructors; no grammar tables or grammar imports | create only |
| `pm_research/local_curl_per_side/governing_package.py` | fixed governing-package complete-file-SHA validation only | create only |
| `pm_research/local_curl_per_side/finding4_registry.py` | sole grammar/placeholder ownership; public path validation; strict accepted-registry parser/index; frozen binding resolution | create only |
| `pm_research/local_curl_per_side/prepared_evidence.py` | descriptor, descriptor-set, physical, structural-member, selected-payload, complete-unit, and dispatch validation | create only |
| `pm_research/local_curl_per_side/claim_hashes.py` | total A0 digest constructors over already typed/validated inputs | create only |
| `tests/local_curl_per_side/test_canonical_i0a.py` | typed cells/rows and canonical field precedence | create only |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | fixed governing bytes | create only |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | strict registry parser, duplicate-key rejection, grammars, placeholders, and binding | create only |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | descriptors, structural members, sidecars, complete unit, and dispatch | create only |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | total digest helpers | create only |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | exports, imports, result domains, assurance tuples, and precedence | create only |

No other repository path may be created, edited, deleted, renamed, or generated.
All twelve paths are create-only at the source gate. If any already exists,
Claude must return `STOP_AUTHORIZED_PATH_ALREADY_EXISTS` without changing it.
