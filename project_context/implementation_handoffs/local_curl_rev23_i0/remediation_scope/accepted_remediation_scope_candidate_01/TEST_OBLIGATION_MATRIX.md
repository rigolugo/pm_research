# Test Obligation Matrix

## Status

This matrix specifies future test-source obligations. Test-source authoring and test execution are both currently unauthorized and require separate decisions.

Canonical repository: `rigolugo/pm_research`  
Canonical base inspected: `cc2964840d197a40d1c4ef567b42eda762c0be0a`  
Controlling accepted scope: `REV23_FINDING4_I0A_SCOPE_REVISION_10`  
Preserved checkpoint evidence: `REV23_FINDING4_I0A_R1_CP_0001_FCF406C4` / `fcf406c4f447945d386467256c07455695db23801400f12be49203ffc2fe35da`  
Checkpoint state: `NOT_ACCEPTED`; authorization effect: `NONE`; static result: `BLOCK — REVISION10_STATIC_CONFORMANCE_BLOCKED`.


| ID | Exact test path | Contract requirement | Positive case | Negative case | Counterexample | Precedence case | Authorization-boundary case |
|---|---|---|---|---|---|---|---|
| T-CAN-01 | `tests/local_curl_per_side/test_canonical_i0a.py` | four codes exist exactly once and all non-success mappings are empty | enumerate each new code and exact result | duplicate/missing code or non-empty assurance fails | string constant outside enum is insufficient | inventory order matches accepted effective domain | test must not import/execute project outside later test authorization |
| T-REG-01 | `tests/local_curl_per_side/test_finding4_registry_i0a.py` | sole matcher returns typed bindings | valid path for every affected grammar, including multi-component analysis family | lexical and selected-grammar faults return null bindings | reject alias path, first-run scanning, caller grammar, extra/missing placeholder | lexical outranks grammar while all fields are inspected | source scan/static assertion finds no second parser/export |
| T-REG-02 | same | four-field SchemaBinding selection | exactly one binding for each accepted key | zero/multiple -> role disposition error | actual logical hash nullability cannot alter selection | binding before path reduction | resolver direct `ERR_BINDING_QUERY_INVALID` remains reachable; wrapper typed path excludes it |
| T-CTX-01 | `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | closed UnitContext validation | all three families and sequence endpoints 0 and `2^64-1` | null, alias, bool, non-int, negative, overflow | malformed context plus malformed JSON/path still returns context error | unsupported unit kind precedes context; context precedes all later faults | direct cases for object, set, structural, selected, unit, dispatch |
| T-PRE-01 | same | pre-binding inspects both fields and reducer is global | all descriptors valid yields exact ordered tuple | each private class maps to correct public code | lexical fault on later descriptor outranks grammar on earlier; duplicate ordinals retained in evidence | lexical > grammar > reuse > family | no assurance retained on reduction failure |
| T-REUSE-01 | same | exact reuse source/target equality | byte-equal paths pass | grammar-valid unequal paths -> new reuse code | unequal path must not become role disposition or family/run result | any lexical/grammar anywhere outranks reuse | non-reuse mode does not emit reuse code |
| T-FAM-01 | same | semantic family binding | correct capture/compatibility/strict mappings | grammar-valid wrong family -> new family code | `analysis/compatibility` cannot be semantic field; `analysis_compatibility` cannot appear as path alias | reuse outranks family; family outranks run/nullability | family-neutral schema cannot override context |
| T-RUN-01 | same | claim/target/source run equality | all equal, including reuse equal-path case | any grammar-valid mismatch -> new run code | must not map to path grammar or plan/unit mismatch | family mismatch outranks run; run outranks nullability | single descriptor excludes run code because claim run absent |
| T-SET-01 | same | narrowed private reducer | fixed roles, unique targets, valid sidecars -> private valid | each allowed private failure | enum/input reflection proves old ordinal code and `expected_role_counts` absent | public ordinal then variable partition count before private fixed count | direct helper cannot decide ordinal/variable count/same-ordinal binding |
| T-SEL-01 | same | exact 19-predicate selected-wrapper order | valid sidecar with independent selected and paired physical proof | each predicate's direct failure | selected valid/paired invalid cannot reuse selected observation; final semantic mismatch only after both physical successes | pairwise and multifault cases for predicates 1-19; preserve accepted T215/T218 behavior | direct old BindingQuery construction rejected by static inspection |
| T-PROJ-01 | `tests/local_curl_per_side/test_i0a_public_contract.py` and `test_prepared_evidence_i0a.py` | typed projection makes wrapper query invalid impossible | sidecar full paired tuple; non-sidecar all null | helper invocation outside preconditions is prohibited | partial paired tuple or caller-supplied bool cannot be constructed through helper | resolver bytes/kind already passed; reachable domain excludes those errors | helper private/unexported; no thirteenth path |
| T-UNIT-01 | `tests/local_curl_per_side/test_prepared_evidence_i0a.py` | unit routes wrapper-eligible JSON members through selected wrapper | valid unit with sidecar and target JSON objects | wrapper reference/implementation/physical/final semantic failures propagate unchanged | direct object reconciliation monkeypatch/counterexample cannot bypass wrapper | sidecar-first failure masks later non-sidecar failure; within-class order per Sentinel decision | preserve accepted T221/T222/T229/T230 delegation reachability partition |
| T-STATIC-01 | `tests/local_curl_per_side/test_i0a_public_contract.py` | package/static closure | domains, private types, 23 call edges, 12-path matrix, T001-T230 identities remain coherent | missing edge/domain/path fails | passing behavioral tests cannot compensate for wrong static contract | exact callable stage order comparisons | no source/test path outside seven proposed writable paths |
| T-SCOPE-01 | all four mandatory test paths | false-unblock prevention | all G1-G8 requirements traced | any one gap unresolved blocks conformance | checkpoint one-file payload cannot be marked conformant | static source review before test authoring/execution | assert tests were not executed during source/test drafting unless separately authorized |

## Additional rules

- Existing accepted T001-T230 identities MUST NOT be renumbered or silently redefined. Known load-bearing cases T107, T153, T177, T204, T205, T215, T218, T221, T222, T229, and T230 MUST retain their accepted purpose and precedence.
- Negative tests MUST prove older result mappings are not reachable for the four new conditions.
- Counterexamples MUST use grammar-valid inputs where the distinction from path failure is material.
- A test that passes by monkeypatching the wrong owner, duplicating path parsing in test code, or constructing an impossible public state is non-conforming.
- Test-source authoring does not authorize execution. Test execution does not authorize local data, network, subprocess, artifacts, or gates unless separately named.
