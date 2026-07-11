"""
Regression test for .actor/input_schema.json.

Earlier Apify builds proved three shape requirements the hard way:
  1. Nested condition properties (inside conditions.items.properties)
     require `title`.
  2. Root-level properties require `editor`.
  3. `items` itself (conditions.items) must NOT have a `title` -- Apify
     rejected that.

This test loads the actual schema file (not a copy or a hand-written
fixture) and asserts all three, so a future edit can't silently regress
any of them again. Pure JSON/dict assertions -- no network, no Apify
import, no dependency on any other module in this package.
"""

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / ".actor" / "input_schema.json"


def _load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_schema_file_is_valid_json():
    schema = _load_schema()
    assert isinstance(schema, dict)
    assert "properties" in schema


def test_every_root_property_has_editor():
    schema = _load_schema()
    root_properties = schema["properties"]
    assert len(root_properties) > 0
    missing_editor = [name for name, spec in root_properties.items() if "editor" not in spec]
    assert missing_editor == [], f"root properties missing 'editor': {missing_editor}"


def test_every_root_property_has_title():
    schema = _load_schema()
    root_properties = schema["properties"]
    missing_title = [name for name, spec in root_properties.items() if "title" not in spec]
    assert missing_title == [], f"root properties missing 'title': {missing_title}"


def test_every_nested_condition_property_has_title():
    schema = _load_schema()
    nested_properties = schema["properties"]["conditions"]["items"]["properties"]
    assert len(nested_properties) > 0
    missing_title = [name for name, spec in nested_properties.items() if "title" not in spec]
    assert missing_title == [], f"nested condition properties missing 'title': {missing_title}"


def test_every_nested_condition_property_has_editor():
    schema = _load_schema()
    nested_properties = schema["properties"]["conditions"]["items"]["properties"]
    missing_editor = [name for name, spec in nested_properties.items() if "editor" not in spec]
    assert missing_editor == [], f"nested condition properties missing 'editor': {missing_editor}"


def test_conditions_items_itself_has_no_title():
    schema = _load_schema()
    items_object = schema["properties"]["conditions"]["items"]
    assert "title" not in items_object, (
        "conditions.items must NOT have its own 'title' -- Apify rejected "
        "this in an earlier build; do not re-add it"
    )


def test_expected_root_property_editor_values():
    """Pins the exact editor values requested in this patch, so a future
    edit that changes one to something else (even if still present) gets
    caught."""
    schema = _load_schema()
    root_properties = schema["properties"]
    expected = {
        "max_conditions": "number",
        "fetch_gamma_metadata": "checkbox",
        "gamma_lookup_type": "select",
        "gamma_base_url": "textfield",
        "clob_base_url": "textfield",
        "fetch_clob_book_shape": "checkbox",
        "price_history_window_seconds": "number",
        "fidelity": "textfield",
        "global_request_cap": "number",
        "dry_run": "checkbox",
        "live_canary_enabled": "checkbox",
        "acknowledge_not_p1_evidence": "checkbox",
        "live_include_current_endpoint_check": "checkbox",
    }
    for name, expected_editor in expected.items():
        assert name in root_properties, f"expected root property {name!r} not found in schema"
        assert root_properties[name]["editor"] == expected_editor, (
            f"root property {name!r} has editor={root_properties[name]['editor']!r}, "
            f"expected {expected_editor!r}"
        )


def test_expected_nested_condition_title_and_editor_values():
    """Pins the exact title/editor values requested in this patch."""
    schema = _load_schema()
    nested_properties = schema["properties"]["conditions"]["items"]["properties"]
    expected = {
        "condition_id": ("Condition ID", "textfield"),
        "nb_subclass": ("Named-binary subclass", "select"),
        "decision_ts": ("Decision timestamp", "textfield"),
        "side_0_token_id": ("Side 0 token ID", "textfield"),
        "side_1_token_id": ("Side 1 token ID", "textfield"),
        "slug": ("Gamma slug", "textfield"),
    }
    for name, (expected_title, expected_editor) in expected.items():
        assert name in nested_properties, f"expected nested property {name!r} not found in schema"
        assert nested_properties[name]["title"] == expected_title, (
            f"nested property {name!r} has title={nested_properties[name]['title']!r}, "
            f"expected {expected_title!r}"
        )
        assert nested_properties[name]["editor"] == expected_editor, (
            f"nested property {name!r} has editor={nested_properties[name]['editor']!r}, "
            f"expected {expected_editor!r}"
        )


def test_required_conditions_fields_unchanged():
    """Regression guard: the patch must not touch which nested fields are
    required, only add title/editor metadata."""
    schema = _load_schema()
    required = schema["properties"]["conditions"]["items"]["required"]
    assert required == ["condition_id", "nb_subclass", "decision_ts", "side_0_token_id", "side_1_token_id"]


def test_safety_defaults_unchanged():
    """Regression guard: this patch is schema-shape-only; safety defaults
    must be untouched."""
    schema = _load_schema()
    root_properties = schema["properties"]
    assert root_properties["dry_run"]["default"] is True
    assert root_properties["live_canary_enabled"]["default"] is False
    assert root_properties["acknowledge_not_p1_evidence"]["default"] is False
    assert root_properties["live_include_current_endpoint_check"]["default"] is False


def test_conditions_root_property_unaffected():
    """The root 'conditions' array property itself (not its nested items)
    already had title+editor before this patch and must be untouched."""
    schema = _load_schema()
    conditions_spec = schema["properties"]["conditions"]
    assert conditions_spec["title"] == "Fixed condition manifest (max 5)"
    assert conditions_spec["editor"] == "json"


# ---------------------------------------------------------------------------
# Plain-script runner (no pytest required)
# ---------------------------------------------------------------------------

def _main() -> int:
    import inspect
    module = sys.modules[__name__]
    test_fns = [
        obj for name, obj in vars(module).items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    for fn in test_fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nALL {len(test_fns)} SCHEMA REGRESSION TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
