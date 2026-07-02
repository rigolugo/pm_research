"""Fallback test runner: `python -m tests.run` — no pytest required.

Discovers tests/test_*.py, runs every test_* function, prints a report and
exits non-zero on failure. The suite itself stays pytest-compatible
(`pytest` works identically once installed).
"""
from __future__ import annotations

import importlib
import sys
import time
import traceback
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))
    modules = sorted(p.stem for p in (root / "tests").glob("test_*.py"))
    passed, failed = 0, []
    t0 = time.time()
    for mod_name in modules:
        mod = importlib.import_module(f"tests.{mod_name}")
        for name in sorted(dir(mod)):
            if not name.startswith("test_"):
                continue
            fn = getattr(mod, name)
            if not callable(fn):
                continue
            try:
                fn()
                passed += 1
                print(f"PASS  {mod_name}::{name}")
            except Exception:
                failed.append(f"{mod_name}::{name}")
                print(f"FAIL  {mod_name}::{name}")
                traceback.print_exc()
    dt = time.time() - t0
    print(f"\n{passed} passed, {len(failed)} failed in {dt:.1f}s")
    if failed:
        print("FAILED:", *failed, sep="\n  ")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
