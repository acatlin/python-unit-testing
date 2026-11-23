"""Checks that the output shown in the lessons still comes from a real run.

From the repo root, in an environment with pandas and pytest (and, for
Lesson 5, the package installed as tools/run_examples.py describes):

    python tools/check_outputs.py

It rebuilds each lesson's situation in a temporary folder (the starter project,
the mistyped expected value, the bug before its fix, and so on), runs the same
commands the lessons run, and then checks that every line of every
<figure class="code out"> block in lessons/ appears in what was printed.

This is a maintenance aid, not a CI check: the pages quote one particular set
of versions, so a new pytest or pandas can change the wording. When it reports
a line it cannot find, rerun the lesson's code by hand and update the page and
its colophon. Lines that are expected to differ between machines are ignored:
the `platform` and `rootdir:` lines, timings, and pip's install summary.
"""
from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
ENV = {**os.environ, "COLUMNS": "80", "PYTHONUTF8": "1", "NO_COLOR": "1"}

RESCALE = '''import pandas as pd

def rescale01(x):
    lo, hi = x.min(), x.max()
    return (x - lo) / (hi - lo)

'''

LESSON_1 = RESCALE + '''rescale01(pd.Series([0, 5, 10]))
assert rescale01(pd.Series([0, 5, 10])).tolist() == [0, 0.5, 1]
assert rescale01(pd.Series([0, 5, 10])).tolist() == [0, 0.5, 2]
rescale01(pd.Series([0, 5, 10])).tolist()
0.1 + 0.2 == 0.3
rescale01(pd.Series([0.1, 0.2, 0.3])).tolist()
import pytest
assert rescale01(pd.Series([0.1, 0.2, 0.3])).tolist() == pytest.approx([0, 0.5, 1])
assert rescale01(pd.Series([0.1, 0.2, 0.3])).tolist() == [0, 0.5, 1]
'''

LESSON_3_DEMO = '''import pandas as pd

from clean import rescale01, summarise_by


def test_ambiguous():
    result = rescale01(pd.Series([1, 2, 3]))
    expected = pd.Series([0, 0.5, 2])      # wrong on purpose
    assert result == expected


def test_vague():
    result = rescale01(pd.Series([1, 2, 3]))
    expected = pd.Series([0, 0.5, 2])      # wrong on purpose
    assert result.equals(expected)


def test_specific():
    result = rescale01(pd.Series([1, 2, 3]))
    expected = pd.Series([0, 0.5, 2])      # wrong on purpose
    pd.testing.assert_series_equal(result, expected)


def test_summarise_by_counts_rows_and_averages_within_each_group():
    staff = pd.DataFrame({
        "dept": ["a", "a", "b"],
        "pay": [10, 20, 60],
    })
    expected = pd.DataFrame({
        "dept": ["a", "b"],
        "n": [2, 1],
        "mean": [15.0, 50.0],
    })
    pd.testing.assert_frame_equal(summarise_by(staff, "dept", "pay"), expected)
'''

LESSON_3_TESTS = '''

def test_summarise_by_counts_rows_and_averages_within_each_group():
    staff = pd.DataFrame({
        "dept": ["a", "a", "b"],
        "pay": [10, 20, 60],
    })
    expected = pd.DataFrame({
        "dept": ["a", "b"],
        "n": [2, 1],
        "mean": [15.0, 60.0],
    })
    pd.testing.assert_frame_equal(summarise_by(staff, "dept", "pay"), expected)


def test_summarise_by_returns_a_data_frame_with_the_documented_columns():
    staff = pd.DataFrame({"dept": ["a", "a", "b"], "pay": [10, 20, 60]})
    out = summarise_by(staff, "dept", "pay")
    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["dept", "n", "mean"]


def test_rescale01_returns_one_float_per_input_value():
    x = rescale01(pd.Series([1, 2, 3]))
    assert x.dtype == "float64"
    assert len(x) == 3
    assert x.max() <= 1
'''

MISSING_TEST = '''

def test_rescale01_keeps_missing_values_missing():
    result = rescale01(pd.Series([1, None, 3]))
    expected = pd.Series([0, None, 1])
    pd.testing.assert_series_equal(result, expected)
'''

CONSTANT_TEST = '''

def test_rescale01_returns_zeros_when_every_value_is_the_same():
    assert rescale01(pd.Series([5, 5, 5])).tolist() == [0, 0, 0]
'''

ERROR_TEST = '''

def test_rescale01_rejects_a_column_that_is_not_numeric():
    with pytest.raises(TypeError, match="must be a numeric column"):
        rescale01(pd.Series(["a", "b"]))
'''

WARNING_DEMO = '''import pandas as pd

from clean import parse_money


def test_parse_money_turns_junk_into_missing():
    assert parse_money(pd.Series(["n/a"])).isna().all()
'''

CONSTANT_FIX = (
    "    lo, hi = x.min(), x.max()\n    return (x - lo) / (hi - lo)",
    "    lo, hi = x.min(), x.max()\n    if lo == hi:\n"
    "        return x * 0.0  # every value is the same: all zeros, missing kept\n"
    "    return (x - lo) / (hi - lo)",
)


def run(args: list[str], cwd: Path, stdin: str | None = None) -> str:
    result = subprocess.run(
        [sys.executable, *args], cwd=cwd, env=ENV, input=stdin,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout + result.stderr


def pytest(cwd: Path, *args: str) -> str:
    return run(["-m", "pytest", "-p", "no:cacheprovider", *args], cwd)


def console(cwd: Path, lines: str) -> str:
    return run(["-i", "-q"], cwd, stdin=lines)


def replace_in(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"check_outputs.py is out of date: {old!r} not in {path}")
    path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


def append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(text)


def fresh_project(tmp: Path, name: str) -> Path:
    project = tmp / name / "cleaning-project"
    shutil.copytree(
        EXAMPLES / "cleaning-project-starter", project,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
    )
    return project


def collect_real_output(tmp: Path) -> str:
    out: list[str] = []

    # Lesson 1: the console.
    out.append(console(tmp, LESSON_1))

    # Lesson 2: the starter project, passing, verbose, and with a mistyped expected value.
    project = fresh_project(tmp, "lesson2")
    tests = project / "tests" / "test_clean.py"
    out.append(pytest(project))
    out.append(pytest(project, "-v"))
    replace_in(tests, '["total", "zip_code"]', '["total", "zip-code"]')
    out.append(pytest(project))

    # Lesson 3: comparing columns and data frames.
    project = fresh_project(tmp, "lesson3")
    (project / "tests" / "test_demo.py").write_text(LESSON_3_DEMO, encoding="utf-8", newline="\n")
    out.append(pytest(project, "tests/test_demo.py"))

    # Lesson 4: the project as it stands at the end of Lesson 3, then step by step.
    project = fresh_project(tmp, "lesson4")
    tests = project / "tests" / "test_clean.py"
    code = project / "clean.py"
    replace_in(tests, "from clean import clean_names, parse_money, rescale01\n",
               "from clean import clean_names, parse_money, rescale01, summarise_by\n")
    append(tests, LESSON_3_TESTS)
    append(tests, MISSING_TEST)
    out.append(console(project, "import pandas as pd\nfrom clean import rescale01\n"
                                "rescale01(pd.Series([5, 5, 5]))\n"))
    append(tests, CONSTANT_TEST)
    out.append(pytest(project))                      # the bug, caught
    replace_in(code, *CONSTANT_FIX)
    replace_in(tests, "import pandas as pd\n", "import pandas as pd\nimport pytest\n")
    append(tests, ERROR_TEST)
    out.append(pytest(project))                      # the cryptic error
    replace_in(code, "    lo, hi = x.min(), x.max()\n    if lo == hi:",
               "    if not pd.api.types.is_numeric_dtype(x):\n"
               '        raise TypeError("x must be a numeric column")\n'
               "    lo, hi = x.min(), x.max()\n    if lo == hi:")
    (project / "tests" / "test_demo.py").write_text(WARNING_DEMO, encoding="utf-8", newline="\n")
    out.append(pytest(project))                      # a warning nobody asked for

    text = "\n".join(out)
    for name in ("lesson2", "lesson3", "lesson4"):
        text = text.replace(str(tmp / name), r"C:\Users\you")

    # Lesson 5: the finished package (must be installed in this environment).
    package = pytest(EXAMPLES / "cleaner")
    return text + "\n" + package.replace(str(EXAMPLES), r"C:\Users\you")


IGNORED = re.compile(r"^(platform |rootdir: |Successfully installed )")
PROMPTS = re.compile(r"^(?:>>> |\.\.\. )+")


def normalise(line: str) -> str:
    line = PROMPTS.sub("", line.rstrip())
    line = re.sub(r"in \d+\.\d+s", "in N.NNs", line)
    line = line.replace("\\", "/")
    return line.strip("= ").strip()


def shown_blocks() -> list[tuple[str, str]]:
    blocks = []
    pattern = re.compile(
        r'<figure class="code out[^"]*">\s*<figcaption>(.*?)</figcaption>\s*<pre>(.*?)</pre>', re.S)
    for page in sorted((ROOT / "lessons").glob("*.html")):
        for caption, pre in pattern.findall(page.read_text(encoding="utf-8")):
            caption = html.unescape(re.sub(r"<[^>]+>", "", caption)).strip()
            blocks.append((f"{page.name}: {caption}", html.unescape(pre)))
    return blocks


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        real = collect_real_output(Path(tmp).resolve())
    real_lines = {normalise(line) for line in real.splitlines()}

    problems = 0
    blocks = shown_blocks()
    for where, text in blocks:
        for line in text.splitlines():
            if not line.strip() or IGNORED.match(line):
                continue
            if normalise(line) not in real_lines:
                problems += 1
                print(f"NOT FOUND in a real run ({where}):\n    {line}")
    print(f"Checked {len(blocks)} output blocks in lessons/: "
          f"{'OK' if not problems else str(problems) + ' line(s) not reproduced'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
