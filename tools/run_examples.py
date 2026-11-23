"""Runs every example project so the code shown in the lessons stays correct.

From the repo root:

    python tools/run_examples.py

The two plain projects are run the way the lessons run them: `python -m pytest`
from the project folder. The package in examples/cleaner has to be installed
first, as Lesson 5 teaches:

    python -m pip install -e examples/cleaner --group examples/cleaner/pyproject.toml:dev

Warnings that no test asked for are treated as errors (`-W error`).
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"

# (folder, number of tests the lessons say it has)
PLAIN_PROJECTS = [("cleaning-project-starter", 3), ("cleaning-project", 12)]
PACKAGE = ("cleaner", 12)


def run_pytest(folder: Path, expected_tests: int) -> bool:
    print(f"\n== {folder.relative_to(ROOT).as_posix()}", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-W", "error", "-q", "-p", "no:cacheprovider"],
        cwd=folder,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(result.stdout.rstrip())
    if result.stderr.strip():
        print(result.stderr.rstrip())
    if result.returncode != 0:
        print(f"FAILED: pytest exited with code {result.returncode}")
        return False
    if f"{expected_tests} passed" not in result.stdout:
        print(f"FAILED: expected exactly {expected_tests} tests to pass")
        return False
    return True


def main() -> int:
    ok = True
    for name, n_tests in PLAIN_PROJECTS:
        ok = run_pytest(EXAMPLES / name, n_tests) and ok

    name, n_tests = PACKAGE
    if importlib.util.find_spec("cleaner") is None:
        print(f"\n== examples/{name} (package)")
        print(
            "FAILED: the package is not installed in this environment. Run:\n"
            "  python -m pip install -e examples/cleaner "
            "--group examples/cleaner/pyproject.toml:dev"
        )
        ok = False
    else:
        ok = run_pytest(EXAMPLES / name, n_tests) and ok

    print("\nAll example tests passed." if ok else "\nSome example checks failed.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
