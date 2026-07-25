# Authorized File Matrix — Inactive Future Proposal

## Status

`REVIEW CANDIDATE — NO PATH IS CURRENTLY AUTHORIZED`

Canonical repository: `rigolugo/pm_research`  
Canonical base inspected: `cc2964840d197a40d1c4ef567b42eda762c0be0a`  
Controlling accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`  
Preserved checkpoint evidence: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`  
Checkpoint state: `NOT_ACCEPTED`; authorization effect: `NONE`; static result: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`.


## Exact twelve-path closure

| Exact path | Class | Revision 10 status | Future activity proposed | Stage | Mandatory/conditional | Rule |
|---|---|---|---|---|---|---|
| `pm_research/local_curl_per_side/__init__.py` | source | not implicated | none | none | prohibited | No exports/re-exports change. |
| `pm_research/local_curl_per_side/canonical.py` | source | mandatory | minimum source authoring | atomic source | mandatory | Four codes and total mappings only. |
| `pm_research/local_curl_per_side/claim_hashes.py` | source | not implicated | none | none | prohibited | No hash algorithm change. |
| `pm_research/local_curl_per_side/finding4_registry.py` | source | mandatory | minimum source authoring | atomic source | mandatory | Sole parser, family mapping, SchemaBinding. |
| `pm_research/local_curl_per_side/governing_package.py` | source | not implicated | none | none | prohibited | Pins/validation unchanged. |
| `pm_research/local_curl_per_side/prepared_evidence.py` | source | mandatory | minimum source authoring | atomic source | mandatory | Context, reductions, reducer, wrapper, unit delegation. |
| `tests/local_curl_per_side/test_canonical_i0a.py` | test source | mandatory | test-source authoring only | later test-source | mandatory if test authoring is authorized | Inventory/mappings. |
| `tests/local_curl_per_side/test_claim_hashes_i0a.py` | test source | not implicated | none | none | prohibited | No hash changes. |
| `tests/local_curl_per_side/test_finding4_registry_i0a.py` | test source | mandatory | test-source authoring only | later test-source | mandatory if test authoring is authorized | Parser/types/binding. |
| `tests/local_curl_per_side/test_governing_package_i0a.py` | test source | not implicated | none | none | prohibited | No governing-package changes. |
| `tests/local_curl_per_side/test_i0a_public_contract.py` | test source | mandatory | test-source authoring only | later test-source | mandatory if test authoring is authorized | Static closure and domains. |
| `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | test source | mandatory | test-source authoring only | later test-source | mandatory if test authoring is authorized | Behavioral/precedence/delegation. |

## Allowed new files

Future implementation/test scope: `NONE`.

This local review package's Markdown/JSON/checksum members are authoring artifacts outside the canonical repository and do not alter the future implementation file boundary.

## Global prohibition

Every repository path outside the exact twelve rows is prohibited. Within the twelve, the five `not implicated` paths are also prohibited. Directory wildcards, adjacent cleanup, generated snapshots, fixtures in new paths, dependency files, configuration files, and documentation edits are not permitted.

## Starting-state requirement

This candidate does not select starting bytes. A later authorization package MUST identify the exact repository commit, branch, dirty/untracked state, and starting SHA-256 for every writable path. A mismatch is a mandatory halt, not permission to restore or overwrite.
