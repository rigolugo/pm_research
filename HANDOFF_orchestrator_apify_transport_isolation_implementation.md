# HANDOFF — Apify Transport-Isolation Canary: Documentation-Corrected Implementation Package

**From:** Claude (implementation agent)
**To:** Orchestrator (ChatGPT) / user review
**Task:** Documentation/comment patch only. **No executable behavior changed. No tests changed. No identity manifest changed.** No build, deploy, run, curl invocation, package install, or network request. No Dockerfile, requirements, accepted spec, accepted finding, or `project_context/*` file touched.

---

## What changed this round

**Only README, handoff, and comment/docstring text changed.** Executable files are byte-identical to the prior patched package — confirmed by diff:

```
src/main.py:                         UNCHANGED
src/transport_isolation_canary.py:   comment/docstring text only (one block, see below) -- no logic changed
src/live_canary.py:                  UNCHANGED
src/validation.py:                   UNCHANGED
.actor/Dockerfile:                   UNCHANGED
.actor/actor.json:                   UNCHANGED
.actor/input_schema.json:            UNCHANGED
requirements.txt:                    UNCHANGED
tests/test_validation.py:            UNCHANGED
tests/test_live_canary.py:           UNCHANGED
tests/test_zero_network_integration.py:      UNCHANGED
tests/test_input_schema_regression.py:       UNCHANGED
tests/test_transport_isolation_canary.py:    UNCHANGED
```

`README.md` and this handoff were rewritten for accuracy; one comment block in `src/transport_isolation_canary.py` (the `MANIFEST_RELATIVE_PATH` constant's preceding comment) was corrected — text only, no code line changed, verified below.

---

## 1. README test counts corrected

Replaced all "87 tests total" / "3 real end-to-end Actor runs" references with the exact current inventory, verified this task via `pytest --collect-only` per file (not assumed from memory):

```text
194 tests total

test_validation.py: 32
test_live_canary.py: 52
test_zero_network_integration.py: 6
test_input_schema_regression.py: 11
test_transport_isolation_canary.py: 93
```

Folder-layout comment and the "Running the tests" description section both updated consistently — the latter previously omitted descriptions for `test_input_schema_regression.py` and `test_transport_isolation_canary.py` entirely; both are now described.

**Orchestrator reproduction — stated precisely, not overclaimed:**
- Claude's own result, this sandbox: `194 passed in 4.83s`.
- The Orchestrator independently reproduced 188 of these 194 tests — all non-integration tests, including all 93 transport-isolation tests.
- The six Actor subprocess integration tests in `test_zero_network_integration.py` were **not** independently reproduced by the Orchestrator, because the Orchestrator's review environment lacked the `apify` package those specific tests require to invoke `python3 -m src`.

(194 − 6 = 188, consistent with the six integration tests living entirely in `test_zero_network_integration.py`.)

---

## 2. README curl-preflight description corrected

Now states the run hard-stops with zero data requests unless **all** of `curl_version`, `libcurl_version`, `tls_backend`, a non-empty `curl_supported_protocols`, and `"https"` present in that list are captured — matching the actual accepted preflight logic (already correct in the source docstring from the prior patch; only the README had drifted). The existing "no package installed / Dockerfile not touched" boundary sentence immediately following is unchanged, confirmed by diff.

---

## 3. Manifest comments corrected

`src/transport_isolation_canary.py`'s comment above `MANIFEST_RELATIVE_PATH` previously said the manifest is "currently absent until the Orchestrator/user supplies and accepts it." Corrected to state: this implementation package includes the accepted identity-only manifest at this path, with its SHA-256 (`b6a39d08e4d88e660bff69b7b9315ef0450fbc16f639598ea412ad6809b7567c`) noted directly in the comment; runtime packaging into the Actor's actual build/container context remains unresolved; absence at runtime still causes the accepted `STOP_APIFY_TRANSPORT_MANIFEST_MISSING_OR_INVALID` zero-process stop. **No second manifest, no hardcoded identities, and no hash-enforcement code path were added** — this is a comment-only change; `load_fixed_manifest()`'s actual logic is byte-identical to the prior patch (confirmed by diff, the constant's value and every function below it are untouched).

**Manifest content and SHA-256 unchanged this round:**

```
b6a39d08e4d88e660bff69b7b9315ef0450fbc16f639598ea412ad6809b7567c
```

---

## 4. Runner-test statement corrected

The prior handoff and README both claimed `SubprocessCurlRunner` "was never instantiated in any test." **This was inaccurate.** `SubprocessCurlRunner` **is** instantiated once, in `test_curl_command_construction_exact_and_safe` (`tests/test_transport_isolation_canary.py`) — verified this task by direct `grep`. The corrected statement, now in both the README and here:

> No real curl subprocess was invoked. The command-construction unit test instantiates `SubprocessCurlRunner` only after monkeypatching `subprocess.run` to a non-executing fake, allowing exact argv inspection without launching curl.

Every other test in the suite uses `FakeCurlRunner`/`PoisonedCurlRunner` stand-ins and never touches `SubprocessCurlRunner` at all.

---

## 5. Dry-run wording corrected

The prior handoff's blanket "no Actor build, deployment, dry run, or live run occurred" was potentially misleading — offline tests genuinely did invoke `python3 -m src` in dry-run and preflight-halt scenarios (that's exactly what `test_zero_network_integration.py`'s six subprocess tests do). Corrected statement:

> No operational/manual Actor dry run, Apify-hosted run, build, deployment, or live run occurred. Offline tests invoked `python3 -m src` only for zero-network dry-run and preflight-halt integration cases.

None of those six test subprocess invocations made any CLOB, Polymarket, Gamma, or Apify data request — confirmed both structurally (the scenarios exercised are default input, explicit `dry_run: true`, missing live-canary acknowledgement, mode-ambiguity, missing transport-isolation acknowledgement, and manifest-absence — none reach a fetch/curl call by construction) and empirically (this sandbox's network egress policy doesn't permit the relevant hosts at all, as a second line of defense).

---

## 6. Deployment limitations preserved, not solved

Left explicitly unresolved, as instructed:
- Whether the fixed manifest is correctly packaged into the Actor's actual build/container context at runtime.
- Whether the Actor's base image (`apify/actor-python:3.11`, per the unmodified `.actor/Dockerfile`) contains the system `curl` executable.
- Any stale Dockerfile comments — the Dockerfile itself is outside this package's authorization to modify, so its content (including any commentary within it) is untouched.

---

## Test command and Claude result (this task)

```bash
cd apify_actors/polymarket_price_canary
python3 -m pytest tests/ -q
```

```
194 passed in 4.83s
```

Re-run this task to confirm the documentation-only nature of the patch — identical result to the prior patched package, as expected since no executable file changed. Verified twice: once in my working sandbox, once from a freshly re-staged/extracted copy of this exact ZIP.

---

## Confirmations

- **No real curl process was invoked.** See item 4 above for the corrected, precise statement of what the one `SubprocessCurlRunner` instantiation in the test suite actually does (and doesn't do).
- **No operational Actor run occurred** — no Apify-hosted dry run, live run, build, or deployment. See item 5 above for the precise scope of what the offline `python3 -m src` test invocations did.
- **No Dockerfile or dependency change.** `.actor/Dockerfile` and `requirements.txt` are byte-identical to the prior patched package.
- **No build or deployment.** No Apify project was touched, built, or deployed at any point in producing this documentation correction.
- **Manifest content and SHA-256 unchanged.** No second manifest, no hardcoded identity, no hash-enforcement code added.
- **No tests changed.** All five test files are byte-identical to the prior patched package.

---

## Recommended Orchestrator decision

```text
REVIEW DOCUMENTATION-CORRECTED IMPLEMENTATION PACKAGE ONLY
```

No run or deployment follows from this handoff. Awaiting Orchestrator review.
