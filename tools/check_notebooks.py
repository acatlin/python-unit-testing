"""Executes the Colab notebooks in notebooks/ so they cannot rot.

From the repo root, in an environment with nbclient and ipykernel:

    python -m pip install nbclient ipykernel
    python tools/check_notebooks.py          # all five
    python tools/check_notebooks.py 2 4      # only these lessons

For each notebook it checks that:
  * the file is what tools/build_notebooks.py writes, and holds no output,
  * every cell runs; only cells tagged `raises-exception` (the assertions that
    fail on purpose in Lesson 1) may raise,
  * the results the lesson promises appear, in order (`3 passed`,
    `1 failed, 2 passed`, and so on),
  * the files the notebook writes match examples/: after Lesson 4 the same
    twelve tests and the same functions as examples/cleaning-project, after
    Lesson 5 the same files as examples/cleaner.

Each notebook runs in a temporary folder. Its first cell pins the pandas and
pytest versions the pages quote (in Colab that pandas is already there, so
only pytest is installed). pandas 2.2.3 has no build for Python 3.14, so run
this with Python 3.13 or older. The Lesson 5
notebook installs its package into the environment this script runs in; if
examples/cleaner was installed there (as tools/run_examples.py needs), it is
installed again afterwards.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_notebooks as build  # noqa: E402

ROOT = build.ROOT
EXAMPLES = build.EXAMPLES

# What each notebook must print, in this order.
EXPECTED = {
    1: ["dtype: float64", "AssertionError", "[0.0, 0.5, 1.0]", "False",
        "[0.0, 0.5000000000000001, 1.0]", "AssertionError"],
    2: ["3 passed", "test_clean_names_returns_lower_case_snake_case PASSED",
        "At index 1 diff: 'zip_code' != 'zip-code'", "1 failed, 2 passed", "3 passed",
        "No module named 'clean'", "3 passed", "collected 0 items", "no tests ran", "3 passed"],
    3: ["4 passed", "The truth value of a Series is ambiguous", "assert False",
        "At positional index 2, first diff: 1.0 != 2.0", "3 failed", "6 passed"],
    4: ["7 passed", "8 passed", "NaN", "assert [nan, nan, nan] == [0, 0, 0]",
        "1 failed, 8 passed", "9 passed", "Regex pattern did not match",
        "unsupported operand type(s) for -: 'str' and 'str'", "1 failed, 9 passed",
        "10 passed", "12 passed", "1 value(s) could not be parsed as money",
        "13 passed, 1 warning", "12 passed"],
    5: ["cleaner/src/cleaner/__init__.py", "Successfully installed", "cleaner-0.1.0",
        "configfile: pyproject.toml", "12 passed", "['first_name', 'zip_code']",
        "5 passed, 7 deselected", "12 passed"],
}


def output_text(nb) -> str:
    parts = []
    for cell in nb.cells:
        for out in cell.get("outputs", []):
            if out.output_type == "stream":
                parts.append(out.text)
            elif out.output_type == "error":
                parts.append(f"{out.ename}: {out.evalue}")
            elif "text/plain" in out.get("data", {}):
                parts.append(out.data["text/plain"])
    return "\n".join(parts)


def functions(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {node.name: ast.dump(node) for node in tree.body if isinstance(node, ast.FunctionDef)}


def same_text(a: Path, b: Path) -> bool:
    return a.read_text(encoding="utf-8").strip() == b.read_text(encoding="utf-8").strip()


def compare_files(n: int, work: Path) -> list[str]:
    problems = []
    if n == 4:
        for name in ("clean.py", "tests/test_clean.py"):
            got = functions(work / "cleaning-project" / name)
            want = functions(EXAMPLES / "cleaning-project" / name)
            if got != want:
                diff = sorted(set(got) ^ set(want)) or sorted(k for k in got if got[k] != want[k])
                problems.append(f"{name} differs from examples/cleaning-project: {diff}")
    if n == 5:
        for name in ("pyproject.toml", "src/cleaner/clean.py", "tests/test_clean.py"):
            if not same_text(work / "cleaner" / name, EXAMPLES / "cleaner" / name):
                problems.append(f"{name} differs from examples/cleaner")
    return problems


def check(n: int) -> list[str]:
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    path = build.notebook_path(n)
    rel = path.relative_to(ROOT).as_posix()
    if not path.exists():
        return [f"{rel} is missing: run python tools/build_notebooks.py"]
    saved = path.read_text(encoding="utf-8")
    if saved != build.render(n):
        return [f"{rel} is not what tools/build_notebooks.py writes: run it again"]
    if any(c.get("outputs") for c in json.loads(saved)["cells"]):
        return [f"{rel} was saved with output"]

    nb = nbformat.reads(saved, as_version=4)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp).resolve()
        client = NotebookClient(nb, timeout=900, kernel_name="python3",
                                resources={"metadata": {"path": str(work)}})
        try:
            client.execute()
        except CellExecutionError as err:
            return [f"{rel}: a cell failed that should not have:\n{err}"]
        problems = compare_files(n, work)

    text = output_text(nb)
    pos = 0
    for want in EXPECTED[n]:
        found = text.find(want, pos)
        if found < 0:
            where = "at all" if want not in text else "in the expected place"
            problems.append(f"{rel}: did not print {want!r} {where}")
        else:
            pos = found + len(want)
    if problems and os.environ.get("NOTEBOOK_DEBUG"):
        print(text)
    return problems


def main(argv: list[str]) -> int:
    if importlib.util.find_spec("nbclient") is None or importlib.util.find_spec("ipykernel") is None:
        print("FAILED: this check needs nbclient and ipykernel. Run:\n"
              "  python -m pip install nbclient ipykernel")
        return 1

    # `!python` and `!pytest` in the notebooks must be the ones of this environment.
    os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]
    os.environ.update(COLUMNS="80", NO_COLOR="1", PYTHONUTF8="1", PIP_DISABLE_PIP_VERSION_CHECK="1")

    lessons = [int(a) for a in argv] or list(build.LESSONS)
    spec = importlib.util.find_spec("cleaner")
    restore = spec is not None and spec.origin is not None and EXAMPLES in Path(spec.origin).parents

    problems = 0
    try:
        for n in lessons:
            found = check(n)
            name = build.notebook_path(n).name
            print(f"{name}: {'OK' if not found else 'FAILED'}", flush=True)
            for p in found:
                print(f"  {p}")
            problems += len(found)
    finally:
        if 5 in lessons and restore:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--no-deps", "-e",
                            str(EXAMPLES / "cleaner")], check=True)
            print("Reinstalled examples/cleaner in editable mode.")

    print(f"Checked {len(lessons)} notebook(s): "
          f"{'OK' if not problems else str(problems) + ' problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
