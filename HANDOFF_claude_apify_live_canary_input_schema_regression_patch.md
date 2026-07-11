# HANDOFF — Apify Live Canary: input_schema.json Regression Patch

**From:** Claude (implementation agent)
**To:** Orchestrator (ChatGPT) / user review
**Task:** Patch `.actor/input_schema.json` only, to restore the Apify-valid schema shape (nested `title`, root `editor`, no `items.title`), per the BLOCK decision. No logic change, no Apify run, no build, no network call.

---

## What was wrong, and what was fixed

`.actor/input_schema.json` had regressed against three shape requirements Apify had already enforced in earlier builds:

1. **Nested condition properties need `title`.** Fixed: `condition_id`, `nb_subclass`, `decision_ts`, `side_0_token_id`, `side_1_token_id`, `slug` (inside `conditions.items.properties`) now all have `title`, exactly as specified — `"Condition ID"`, `"Named-binary subclass"`, `"Decision timestamp"`, `"Side 0 token ID"`, `"Side 1 token ID"`, `"Gamma slug"`.
2. **Root properties need `editor`.** Fixed: all 13 named root properties (`max_conditions`, `fetch_gamma_metadata`, `gamma_lookup_type`, `gamma_base_url`, `clob_base_url`, `fetch_clob_book_shape`, `price_history_window_seconds`, `fidelity`, `global_request_cap`, `dry_run`, `live_canary_enabled`, `acknowledge_not_p1_evidence`, `live_include_current_endpoint_check`) now have `editor` set to exactly the value specified (`number`/`checkbox`/`select`/`textfield` as directed). The root `conditions` property already had `editor: "json"` from before and was left untouched.
3. **`conditions.items` itself must not have a `title`.** Confirmed: it was never added. `items` still has only `type`, `properties`, `required` — no `title` key, verified by a dedicated test (`test_conditions_items_itself_has_no_title`).

Also added `editor: "select"` to the nested `nb_subclass` property per the patch instructions (it already had an `enum`; the editor hint is new).

## What was NOT touched

Diffed every other file in the package against the prior delivered ZIP — all byte-identical:

- `src/main.py`, `src/validation.py`, `src/live_canary.py` — **unchanged**. No live-canary logic was touched.
- `tests/test_validation.py`, `tests/test_live_canary.py`, `tests/test_zero_network_integration.py` — **unchanged**.
- `.actor/actor.json`, `.actor/Dockerfile` — **unchanged**.
- `README.md` — **unchanged** (not required by this patch; left alone to keep the diff minimal and precisely scoped).

Only `.actor/input_schema.json` was modified, and one new file was added: `tests/test_input_schema_regression.py`.

## New file: `tests/test_input_schema_regression.py`

Loads the actual schema file (not a copy or hand-written fixture) and asserts, per the patch's item D:

- Every root property has `editor` (`test_every_root_property_has_editor`) and `title` (`test_every_root_property_has_title`).
- Every nested condition property has `title` (`test_every_nested_condition_property_has_title`) and `editor` (`test_every_nested_condition_property_has_editor`).
- `conditions.items` itself has no `title` key (`test_conditions_items_itself_has_no_title`).
- The exact `editor` value for every root property matches what was requested (`test_expected_root_property_editor_values`), and the exact `title`+`editor` for every nested property matches what was requested (`test_expected_nested_condition_title_and_editor_values`) — pinned, so a future edit that changes a value (even while keeping the key present) is caught, not just presence/absence.
- Two extra regression guards, beyond the letter of item D: `required` on `conditions.items` is unchanged (`["condition_id", "nb_subclass", "decision_ts", "side_0_token_id", "side_1_token_id"]`), and the four safety-relevant defaults (`dry_run: true`, `live_canary_enabled: false`, `acknowledge_not_p1_evidence: false`, `live_include_current_endpoint_check: false`) are unchanged — confirming this patch is shape-only and didn't accidentally touch a default.

## Test results

```
98 passed in 3.03s
```

- `test_validation.py`: 32/32 (unchanged)
- `test_live_canary.py`: 52/52 (unchanged)
- `test_zero_network_integration.py`: 3/3 (unchanged) — real subprocess Actor runs against local storage
- `test_input_schema_regression.py`: **11/11 (new)**

Verified three times: locally, from a re-staged copy, and from a freshly extracted ZIP (see below).

## Safety behavior preserved (item E) — confirmed unchanged

- `dry_run` defaults `true`.
- `live_canary_enabled` defaults `false`.
- `acknowledge_not_p1_evidence` defaults `false`.
- `live_include_current_endpoint_check` defaults `false`.
- No Gamma by default in live canary (unchanged code).
- Live hard request cap ≤ 12 (unchanged code).
- No `yes_price`, no `1 - price`, no `canonical_side_price`, no P1 artifact, no coverage/source-viability verdict — none of this logic was touched.

## Not authorized by this handoff

- No Apify run, no build, no deploy, no network call — none occurred in producing this patch.
- No `dry_run: false` run against real infrastructure.
- No P1/P2/P3/probe/scoring/gate change of any kind.

## Package contents

```
HANDOFF_claude_apify_live_canary_input_schema_regression_patch.md   (this file, at zip root)
apify_actors/polymarket_price_canary/.actor/actor.json                      (unchanged)
apify_actors/polymarket_price_canary/.actor/input_schema.json               (PATCHED)
apify_actors/polymarket_price_canary/.actor/Dockerfile                      (unchanged)
apify_actors/polymarket_price_canary/src/__init__.py                       (unchanged)
apify_actors/polymarket_price_canary/src/__main__.py                       (unchanged)
apify_actors/polymarket_price_canary/src/main.py                          (unchanged)
apify_actors/polymarket_price_canary/src/validation.py                    (unchanged)
apify_actors/polymarket_price_canary/src/live_canary.py                   (unchanged)
apify_actors/polymarket_price_canary/tests/test_validation.py             (unchanged, 32/32)
apify_actors/polymarket_price_canary/tests/test_live_canary.py            (unchanged, 52/52)
apify_actors/polymarket_price_canary/tests/test_zero_network_integration.py (unchanged, 3/3)
apify_actors/polymarket_price_canary/tests/test_input_schema_regression.py  (NEW, 11/11)
apify_actors/polymarket_price_canary/examples/input_dry_run_example.json   (unchanged)
apify_actors/polymarket_price_canary/requirements.txt                      (unchanged)
apify_actors/polymarket_price_canary/README.md                            (unchanged)
```

**File delivery only** — not a commit, not a build, not a run. Awaiting Orchestrator review.
