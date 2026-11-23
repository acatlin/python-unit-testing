"""Writes the Google Colab notebooks in notebooks/, one per lesson.

From the repo root (any Python 3.11 or later; no packages needed):

    python tools/build_notebooks.py

The notebooks are generated, not edited by hand, so that the files they write
(clean.py, tests/test_clean.py, pyproject.toml) are the ones in examples/ and
the ones tools/check_outputs.py runs. Change the text here, run this script,
then run tools/check_notebooks.py, which executes every notebook.

Each notebook is the code of one lesson in the order the page gives it:
`%%writefile` cells stand in for the editor, `!` lines for the terminal.
They are saved without output.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_outputs as steps  # noqa: E402  (the lesson scenarios, shared)

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
OUT = ROOT / "notebooks"

# The versions the lesson pages quote. Colab ships older ones (see RESOURCES.md),
# so every notebook installs these first.
PANDAS = "3.1.1"
PYTEST = "9.2.0"

SITE = "https://acatlin.github.io/python-unit-testing/"
COLAB = "https://colab.research.google.com/github/acatlin/python-unit-testing/blob/main/notebooks/"

LESSONS = {
    1: ("0001-first-assertion", "Your first assertion"),
    2: ("0002-test-functions-and-test-files", "Test functions and test files"),
    3: ("0003-choosing-assertions", "Choosing the right assertion"),
    4: ("0004-edge-cases-errors-and-bugs", "Edge cases, errors and bugs"),
    5: ("0005-from-project-to-package", "From project to package"),
}

PROJECT = "cleaning-project"
CLEAN = f"{PROJECT}/clean.py"
TESTS = f"{PROJECT}/tests/test_clean.py"
DEMO = f"{PROJECT}/tests/test_demo.py"
RUN = f"!cd {PROJECT} && python -m pytest"


def read(path: str) -> str:
    return (EXAMPLES / path).read_text(encoding="utf-8")


def swap(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"build_notebooks.py is out of date: {old!r} not found")
    return text.replace(old, new, 1)


# --- the files at each stage of the course ---------------------------------

CLEAN_START = read("cleaning-project-starter/clean.py")
CLEAN_CONSTANT = swap(CLEAN_START, *steps.CONSTANT_FIX)
CLEAN_FINISHED = swap(
    CLEAN_CONSTANT,
    "    lo, hi = x.min(), x.max()\n    if lo == hi:",
    "    if not pd.api.types.is_numeric_dtype(x):\n"
    '        raise TypeError("x must be a numeric column")\n'
    "    lo, hi = x.min(), x.max()\n    if lo == hi:",
)

IMPORT_3 = "from clean import clean_names, parse_money, rescale01\n"
IMPORT_4 = "from clean import clean_names, parse_money, rescale01, summarise_by\n"

TESTS_START = read("cleaning-project-starter/tests/test_clean.py")
TESTS_AFTER_2 = TESTS_START + steps.THOUSANDS_TEST
_cut = steps.LESSON_3_TESTS.index("\n\ndef test_rescale01_returns_one_float")
SUMMARISE_TESTS = steps.LESSON_3_TESTS[:_cut] + "\n"
TESTS_WITH_SUMMARISE = swap(TESTS_AFTER_2, IMPORT_3, IMPORT_4) + SUMMARISE_TESTS
TESTS_AFTER_3 = swap(TESTS_AFTER_2, IMPORT_3, IMPORT_4) + steps.LESSON_3_TESTS
TESTS_WITH_IMPORTS = swap(
    TESTS_AFTER_3 + steps.MISSING_TEST + steps.CONSTANT_TEST,
    "import pandas as pd\n",
    "import warnings\n\nimport pandas as pd\nimport pytest\n",
) + steps.ERROR_TEST

SERIES_DEMO = steps.LESSON_3_DEMO[: steps.LESSON_3_DEMO.index("\n\ndef test_summarise_by")]
SERIES_DEMO = swap(SERIES_DEMO, "from clean import rescale01, summarise_by", "from clean import rescale01")


# --- cells ------------------------------------------------------------------

def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n")}


def code(text: str, fails: bool = False) -> dict:
    meta = {"tags": ["raises-exception"]} if fails else {}
    return {"cell_type": "code", "metadata": meta, "execution_count": None,
            "outputs": [], "source": text.strip("\n")}


def write(path: str, content: str) -> dict:
    return code(f"%%writefile {path}\n" + content.strip("\n"))


def add(path: str, content: str) -> dict:
    # Two blank lines first, so the new test is set apart from the one above it.
    return code(f"%%writefile -a {path}\n\n\n" + content.strip("\n"))


def intro(n: int) -> dict:
    slug, title = LESSONS[n]
    return md(f"""
# Lesson {n}: {title}

This notebook goes with [Lesson {n} of *Unit Testing in Python*]({SITE}lessons/{slug}.html). The explanations are on that page. The code is here, ready to run.

- Run the cells from top to bottom, one at a time: click a cell and press Shift+Enter.
- This is your own copy. Change anything you like; nothing you do here alters the course. To keep your work, choose File, then Save a copy in Drive.
""")


def setup(extra_versions: str = "") -> list[dict]:
    return [
        md("""
## Set up

Colab comes with older versions of pandas and pytest than the lesson page was written with. The next cell installs the versions the page uses, so that what you see here matches it. It can take a minute.

pip may end with a message that other packages in Colab want the older pandas. This notebook does not use them, so carry on. If Colab asks you to restart the session, do that, then continue from the cell after this one.
"""),
        code(f'%pip install -q "pandas=={PANDAS}" "pytest=={PYTEST}"'),
        md("Check what you have. A line that starts with `!` goes to the computer's command line, not to Python: it is this notebook's stand-in for the terminal."),
        code("!python --version\n!python -m pytest --version\n"
             "!python -c \"import pandas; print('pandas', pandas.__version__)\"" + extra_versions),
    ]


FILES_NOTE = md(f"""
## How files and commands work here

The lesson has you save files in an editor and type commands in a terminal. A notebook has neither, so two stand-ins do the job.

- **`%%writefile name`** on the first line of a cell saves the rest of the cell as a file, in place of running it. To change the file, edit the cell and run it again. (You can also open the file from the folder icon at the left edge of Colab.)
- **`!`** at the start of a line sends it to the command line. Every `!` line starts in the notebook's own folder, so the commands below begin with `cd {PROJECT} &&` to step into the project first.

**What will look different from the lesson page.** The page shows output captured on Windows with Python 3.14. Colab runs Linux with its own Python. So the `platform` line says `linux` and another Python version, `rootdir:` is a folder under `/content`, paths are written with `/` in place of `\\`, the rules of `=` signs may be wider or narrower, and the timings differ. The results are the same: the dots and `F`s, the lines marked `E`, and the counts on the last line.
""")

MAKE_PROJECT = code(f'import os\n\nos.makedirs("{PROJECT}/tests", exist_ok=True)')


def try_cell(hint: str) -> dict:
    return code(f"# {hint}")


# --- the five notebooks ------------------------------------------------------

def lesson_1() -> list[dict]:
    return [
        intro(1),
        *setup(),
        md("""
## The check that disappears

A small helper that rescales a numeric column so its smallest value becomes 0 and its largest becomes 1. Run it and look at the result.
"""),
        code("""
import pandas as pd

def rescale01(x):
    lo, hi = x.min(), x.max()
    return (x - lo) / (hi - lo)

rescale01(pd.Series([0, 5, 10]))
"""),
        md("""
## Say what you expect

The same check written down as an assertion. Run it: nothing is printed. **Silence means the assertion passed.**
"""),
        code("assert rescale01(pd.Series([0, 5, 10])).tolist() == [0, 0.5, 1]"),
        md("""
## Watch one fail

The expected value is wrong on purpose, so **this cell is meant to fail**. A notebook lays the error out differently from the console shown on the lesson page; what matters is the same: it ends with `AssertionError`.

If you chose Run all, Colab stops at this cell. Carry on from the next one by hand.
"""),
        code("assert rescale01(pd.Series([0, 5, 10])).tolist() == [0, 0.5, 2]", fails=True),
        md("Python does not show the two values that disagreed. To see the actual value, run the left side by itself."),
        code("rescale01(pd.Series([0, 5, 10])).tolist()"),
        md("## Equal, or close enough?"),
        code("0.1 + 0.2 == 0.3"),
        code("rescale01(pd.Series([0.1, 0.2, 0.3])).tolist()"),
        md("With `pytest.approx()` around the expected value, `==` ignores tiny floating-point differences. This cell is silent: it passes."),
        code("""
import pytest

assert rescale01(pd.Series([0.1, 0.2, 0.3])).tolist() == pytest.approx([0, 0.5, 1])
"""),
        md("The same check with a bare `==`. **This cell is meant to fail**, for a reason that has nothing to do with a bug."),
        code("assert rescale01(pd.Series([0.1, 0.2, 0.3])).tolist() == [0, 0.5, 1]", fails=True),
        md("""
## Try it

Work out each expected value in your head or on paper *before* you run anything. That is the whole point.

1. `rescale01()`, pandas and pytest are already defined and imported by the cells above.
2. Write an assertion for `rescale01(pd.Series([-2, 0, 2]))`. It should be silent.
"""),
        try_cell("step 2: your assertion"),
        md("3. Write one for `rescale01(pd.Series([10, 20, 30, 50]))`. If it fails, run the left side by itself, compare, and decide who is wrong: the function, or your arithmetic."),
        try_cell("step 3: your assertion"),
        md("4. Break one of your assertions on purpose, read the error, and repair it."),
        md("5. Write one for `rescale01(pd.Series([0.2, 0.4, 0.6]))`, first with a bare `==` and then with `pytest.approx()`. Say which one passes before you run each."),
        try_cell("step 5: with a bare =="),
        try_cell("step 5: with pytest.approx()"),
        md(f"Now go back to the [lesson page]({SITE}lessons/{LESSONS[1][0]}.html) for the quiz."),
    ]


def lesson_2() -> list[dict]:
    broken = swap(TESTS_START, '["total", "zip_code"]', '["total", "zip-code"]')
    return [
        intro(2),
        *setup(),
        FILES_NOTE,
        md(f"""
## Give tests a home

Make the project folder with a `tests/` folder inside it, then save the two files: `clean.py` with the functions, and `tests/test_clean.py` with the tests.
"""),
        MAKE_PROJECT,
        write(CLEAN, CLEAN_START),
        write(TESTS, TESTS_START),
        md("## Run everything\n\nOne command, from the project folder. You should see `3 passed`."),
        code(RUN),
        md("Add `-v` and pytest lists every test by name."),
        code(RUN + " -v"),
        md("""
## Reading a failure

Suppose you had typed the expected name as `"zip-code"`. The next cell saves the test file with that mistake in it, and the one after runs the tests. Read the report in three steps: **what** (the name under `FAILURES`), **where** (the line marked `>`), **why** (the lines marked `E`).
"""),
        write(TESTS, broken),
        code(RUN),
        md("The function was fine and the test was mistyped. Put the test file right and run again."),
        write(TESTS, TESTS_START),
        code(RUN),
        md("""
## The common trap

Plain `pytest`, without `python -m`, cannot find `clean.py`. The run stops with `ModuleNotFoundError: No module named 'clean'`. Nothing is wrong with the tests.
"""),
        code(f"!cd {PROJECT} && pytest"),
        md("""
## Try it

Steps 1 and 2 of the lesson are done: you have the project and have seen `3 passed`.

3. In the cell that saves `tests/test_clean.py` (the one just above "The common trap"), add a third assertion to the `parse_money()` test, for the input `"$3,000"`. Run that cell, then the cell below. The count is still 3, because pytest counts tests. Now move that assertion into a new test of its own, with a name that says what it checks, and watch the count become 4.
"""),
        code(RUN),
        md("4. Rename the test file to `clean_tests.py` and run again. You should see `collected 0 items` and `no tests ran`. The third cell renames it back."),
        code(f'os.rename("{TESTS}", "{PROJECT}/tests/clean_tests.py")'),
        code(RUN),
        code(f'os.rename("{PROJECT}/tests/clean_tests.py", "{TESTS}")'),
        code(RUN),
        md(f"Now go back to the [lesson page]({SITE}lessons/{LESSONS[2][0]}.html) for the quiz. The Lesson 3 notebook starts from this project with the fourth test already added."),
    ]


def lesson_3() -> list[dict]:
    return [
        intro(3),
        *setup(),
        FILES_NOTE,
        md("""
## The project so far

This is the project as Lesson 2 left it: `clean.py`, and a test file with four tests (the three you were given and the one you wrote for `"$3,000"`). You should see `4 passed`.
"""),
        MAKE_PROJECT,
        write(CLEAN, CLEAN_START),
        write(TESTS, TESTS_AFTER_2),
        code(RUN),
        md("""
## Why not `==` for everything?

Three ways to compare two columns, each in a test of its own, saved in a scratch file. The expected value is wrong on purpose, so **all three are meant to fail**. Compare what each report tells you: a crash (`ValueError`), a bare `False`, and a message that says which value differs.
"""),
        write(DEMO, SERIES_DEMO),
        code(RUN + " tests/test_demo.py"),
        md("That file has done its job. Delete it."),
        code(f'os.remove("{DEMO}")'),
        md("""
## Testing a function that returns a data frame

`summarise_by()` is already in `clean.py`. Here is the test file with its two tests added at the end, and `summarise_by` added to the import line. You should see `6 passed`.
"""),
        write(TESTS, TESTS_WITH_SUMMARISE),
        code(RUN),
        md("""
## See the failure for yourself

In the cell that saves the test file, change the expected mean for "b" from `60.0` to `50.0`. Run that cell, then run the tests below. pandas names the column and the row that disagree. Put `60.0` back afterwards.
"""),
        code(RUN),
        md("""
## Try it

Step 1 of the lesson is done.

2. In the expected data frame, change `"mean": [15.0, 60.0]` to `"mean": [15, 60]` (whole numbers in place of decimals). Save the file and run the tests. Does `assert_frame_equal()` still pass? Read the message. Now add the argument `check_dtype=False` to the call and run again. Put the decimals back when you have finished.
"""),
        code(RUN),
        md(f"""
3. Write a new test for `rescale01()` with three assertions: the result has dtype `"float64"`, has the same length as the input, and its largest value is at most 1.

To add a test without retyping the file, start a cell with `%%writefile -a {TESTS}`. The `-a` means append: the cell is added to the end of the file. Leave two blank lines under that first line, and run the cell once only (running it twice adds the test twice).
"""),
        try_cell("step 3: your new test"),
        code(RUN),
        md(f"Now go back to the [lesson page]({SITE}lessons/{LESSONS[3][0]}.html) for the quiz. The Lesson 4 notebook starts from this project with that seventh test already added."),
    ]


def lesson_4() -> list[dict]:
    return [
        intro(4),
        *setup(),
        FILES_NOTE,
        md("""
## The project so far

The project as Lesson 3 left it: seven tests, all passing.
"""),
        MAKE_PROJECT,
        write(CLEAN, CLEAN_START),
        write(TESTS, TESTS_AFTER_3),
        code(RUN),
        md(f"""
## Ask what could go wrong

Missing values first. The decision: they stay missing, and the rest are rescaled as usual.

The next cell starts with `%%writefile -a`. The `-a` means append: the cell is added to the end of the test file, the way you would type a new test under the others. **Run each `-a` cell once only.** Run one twice and the test is in the file twice. If you get in a muddle, go back to the last cell that saves the whole test file and run the cells from there in order.
"""),
        add(TESTS, steps.MISSING_TEST),
        md("It passes already (`8 passed`). That is a fine outcome: the behaviour is now written down."),
        code(RUN),
        md("""
## A bug, caught test-first

What does `rescale01()` do with a column where every value is the same? Ask Python, from the project folder.
"""),
        code(f'!cd {PROJECT} && python -c "import pandas as pd; from clean import rescale01; '
             'print(rescale01(pd.Series([5, 5, 5])))"'),
        md("""
Zero divided by zero: `NaN`, with no error and no warning. That is a bug.

### Step 1: write the test and watch it fail

All zeros is a sensible answer. Say so, and run. **This run is meant to fail**: `1 failed, 8 passed`.
"""),
        add(TESTS, steps.CONSTANT_TEST),
        code(RUN),
        md("### Step 2: fix the function\n\nTwo new lines in `rescale01()`."),
        write(CLEAN, CLEAN_CONSTANT),
        md("### Step 3: run everything again\n\nThe new test passes, and so does every old one: `9 passed`."),
        code(RUN),
        md("""
## Expecting an error

For the wrong type, the right behaviour is to stop with a clear message. The test names the type of error and a piece of its message. `pytest.raises()` belongs to pytest, so the file needs `import pytest` at the top; `import warnings` goes in at the same time, for the section after this one.

Imports go at the top of a file, where `-a` cannot reach, so this cell saves the whole test file again: the nine tests so far, the new imports, and the new test at the end.
"""),
        write(TESTS, TESTS_WITH_IMPORTS),
        md("**This run is meant to fail** (`1 failed, 9 passed`). The error is of the right type, but its message is a cryptic one from deep inside the arithmetic."),
        code(RUN),
        md("The test is red, so improve the function: check the input at the top."),
        write(CLEAN, CLEAN_FINISHED),
        code(RUN),
        md("""
## Warnings

Two more tests: one says that junk input warns, the other that well-formed input is quiet. After them you have the twelve tests of the finished project.
"""),
        add(TESTS, steps.WARNING_TESTS),
        code(RUN),
        md("""
A warning that no test asked for does not fail the test, but it is not hidden either. Here is a scratch file with one test that calls `parse_money(pd.Series(["n/a"]))` outside `pytest.warns()`. Look for the `warnings summary` and the count on the last line: `13 passed, 1 warning`.
"""),
        write(DEMO, steps.WARNING_DEMO),
        code(RUN),
        code(f'os.remove("{DEMO}")'),
        md("""
## Try it

Step 1 of the lesson is what you have just done.

2. What should `rescale01(pd.Series([7]))`, a single value, return? Decide, write the test in a `%%writefile -a` cell, and run it.
"""),
        try_cell("step 2: your test"),
        code(RUN),
        md("""
3. What does `clean_names()` do with `[""]`, with `["123 Go!"]`, or with a bare string such as `"First Name"` in place of a list? Try them in the cell below, decide whether you are happy with each result, and write a test that records your decision.
"""),
        code(f'!cd {PROJECT} && python -c "from clean import clean_names; print(clean_names([\'\']))"'),
        try_cell("step 3: your test"),
        code(RUN),
        md(f"Now go back to the [lesson page]({SITE}lessons/{LESSONS[4][0]}.html) for the quiz."),
    ]


def lesson_5() -> list[dict]:
    pkg = "cleaner"
    return [
        intro(5),
        md("""
## How this notebook differs from the lesson page

On the page, step 3 makes a virtual environment, so that the package and its tools are kept apart from everything else on your computer. A Colab runtime already is one: a fresh machine that is yours alone and is thrown away when you disconnect. So this notebook skips step 3 and installs the package straight into the runtime. Switching an environment on would not last here in any case, because every `!` line starts a new shell.

On your own computer, do not skip it. The commands are at the end of this notebook.
"""),
        *setup("\n!python -m pip --version"),
        md("`pip install --group`, used below, needs pip 25.1 or newer. The last line above tells you which pip you have."),
        md(f"""
## How files and commands work here

- **`%%writefile name`** on the first line of a cell saves the rest of the cell as a file, in place of running it. To change the file, edit the cell and run it again.
- **`!`** at the start of a line sends it to the command line. Every `!` line starts in the notebook's own folder, so the commands below begin with `cd {pkg} &&` to step into the package first.

**What will look different from the lesson page.** The page shows output captured on Windows with Python 3.14. Colab runs Linux with its own Python. So the `platform` line says `linux` and another Python version, `rootdir:` is `/content/{pkg}`, paths are written with `/`, the timings differ, and pip's list of what it installed is shorter, because Colab has most of those packages already.
"""),
        md("""
## Build it

### Step 1: make the folders

`src/cleaner/` for the code and `tests/` for the tests, then the files: `clean.py` as you finished it in Lesson 4 (only the first line, the description, has changed), an empty `__init__.py` next to it, and the test file.
"""),
        code(f'import os\n\nos.makedirs("{pkg}/src/{pkg}", exist_ok=True)\n'
             f'os.makedirs("{pkg}/tests", exist_ok=True)\n'
             f'open("{pkg}/src/{pkg}/__init__.py", "w").close()   # an empty file'),
        write(f"{pkg}/src/{pkg}/clean.py", read("cleaner/src/cleaner/clean.py")),
        md("""
The test file is the one from Lesson 4 with **one line changed** (step 5 on the page): the import now says `from cleaner.clean import …`, because the functions live in the module `clean` inside the package `cleaner`.
"""),
        write(f"{pkg}/tests/test_clean.py", read("cleaner/tests/test_clean.py")),
        md("### Step 2: write the settings file"),
        write(f"{pkg}/pyproject.toml", read("cleaner/pyproject.toml")),
        md("Here is what you have made. Compare it with the tree on the lesson page."),
        code(f'from pathlib import Path\n\n'
             f'for path in sorted(Path("{pkg}").rglob("*")):\n'
             f'    if path.is_file() and "__pycache__" not in path.parts:\n'
             f'        print(path.as_posix())'),
        md("""
### Step 3: the virtual environment

Skipped in Colab; see the top of this notebook.

### Step 4: install your package

In editable mode (`-e`), together with the `dev` group. The dot means "the project in this folder". Look for `Successfully installed cleaner-0.1.0` at the end.
"""),
        code(f"!cd {pkg} && python -m pip install -e . --group dev"),
        md("### Step 6: run the tests\n\nPlain `pytest` is enough now. You should see `12 passed`."),
        code(f"!cd {pkg} && pytest"),
        md("""
## What the editable install did

Python can now import your code from any folder. This line runs in the notebook's folder, not inside `cleaner/`.
"""),
        code("!python -c \"from cleaner.clean import clean_names; "
             "print(clean_names(['First Name', ' Zip-Code ']))\""),
        md("## The working loop\n\nOnly the tests whose names contain a word:"),
        code(f"!cd {pkg} && pytest -k rescale01"),
        md("Stop at the first failure (there is none yet):"),
        code(f"!cd {pkg} && pytest -x"),
        md("""
## Try it

Step 1 of the lesson is what you have just done.

2. Break `clean_names()` on purpose: in the cell that saves `clean.py`, delete `.lower()`, and run that cell. Nothing needs reinstalling, because the install is editable. Run `pytest` below and read the report. Run `pytest --lf` and notice how many tests it collects. Undo the change and run everything again.
"""),
        code(f"!cd {pkg} && pytest"),
        code(f"!cd {pkg} && pytest --lf"),
        md(f"""
3. Add a new function to the package test-first: write a failing test, then make it pass. An idea: `squish()`, which trims a string and collapses runs of spaces into one. Put it in a new file with `%%writefile {pkg}/src/{pkg}/text.py`, and its tests in `%%writefile {pkg}/tests/test_text.py`.
"""),
        try_cell("step 3: start with the test file"),
        try_cell("step 3: then the function"),
        code(f"!cd {pkg} && pytest"),
        md(f"""
## On your own computer

There, do step 3. In a terminal in the top `cleaner` folder:

**Windows**

```
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -e . --group dev
pytest
```

**macOS and Linux**

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e . --group dev
pytest
```

Now go back to the [lesson page]({SITE}lessons/{LESSONS[5][0]}.html) for the quiz.
"""),
    ]


BUILDERS = {1: lesson_1, 2: lesson_2, 3: lesson_3, 4: lesson_4, 5: lesson_5}


def notebook_path(n: int) -> Path:
    return OUT / f"{LESSONS[n][0]}.ipynb"


def render(n: int) -> str:
    cells = [{**cell, "source": cell["source"].splitlines(keepends=True)}
             for cell in BUILDERS[n]()]
    nb = {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n"


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for n in LESSONS:
        path = notebook_path(n)
        path.write_text(render(n), encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
