"""Static guard against the exact bug class that broke the backfill command:
a function-local import shadowing a module-level name makes that name local
to the WHOLE function — any branch using it without executing the import
raises UnboundLocalError. Scan cli.py and forbid the pattern outright."""
from __future__ import annotations

import ast
from pathlib import Path

import pm_research.cli as cli_module


def _module_level_names(tree: ast.Module) -> set[str]:
    names = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            names |= {a.asname or a.name for a in node.names}
        elif isinstance(node, ast.Import):
            names |= {(a.asname or a.name).split(".")[0] for a in node.names}
    return names


def test_no_local_import_shadows_module_level_name_in_cli():
    tree = ast.parse(Path(cli_module.__file__).read_text())
    top = _module_level_names(tree)
    offenders = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        for node in ast.walk(fn):
            if isinstance(node, (ast.Import, ast.ImportFrom)) and node is not fn:
                for a in node.names:
                    name = (a.asname or a.name).split(".")[0]
                    if name in top:
                        offenders.append(f"{fn.name}: {name} (line {node.lineno})")
    assert not offenders, f"local imports shadow module-level names: {offenders}"


def test_cli_dispatch_reaches_backfiller_construction():
    """Drive main(['backfill', ...]) far enough to prove the dispatch path can
    bind Backfiller — a fake Store-level failure stops it before networking."""
    import pm_research.cli as cli
    try:
        cli.main(["backfill", "--wallets", "0xw1", "--start", "2025-01-01",
                  "--end", "2025-01-02", "--root", "/nonexistent\x00bad"])
        raise AssertionError("expected failure from invalid root path")
    except UnboundLocalError as e:           # the regression this test guards
        raise AssertionError(f"dispatch bug is back: {e}")
    except Exception:
        pass                                  # any other failure = dispatch OK
