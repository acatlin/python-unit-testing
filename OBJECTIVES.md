# Mastery objectives: evidence map and gaps

Instructor-facing. The student-facing checklist is [`reference/mastery-objectives.html`](reference/mastery-objectives.html) ([live page](https://acatlin.github.io/python-unit-testing/reference/mastery-objectives.html)). Keep the objective wording in the two files identical.

## How to read this

- Each objective is one observable "can do" statement with a single mastery criterion. There are no levels.
- Evidence is labelled by kind:
  - **Doing**: a "Try it" step, where the student writes or runs code. "Guided" means the step has the student copy or follow code from the page instead of writing their own.
  - **Recognition**: a multiple-choice quiz question.
- Evidence ids refer to items by position:
  - `L4-T2` is Lesson 4, "Try it" step 2.
  - `L3-Q2` is Lesson 3, "Check yourself" question 2.
  - `L2-W1` is Lesson 2, warm-up question 1.
- The ids exist only in this file and on the student page. The lesson HTML has no matching `id` attributes, so inserting or reordering a step or question changes the ids below.
- Objective numbers are `lesson.sequence`. An objective sits under the lesson that introduces it, even when a later lesson supplies evidence.

Inventory: 19 taught objectives, 18 "Try it" steps, 32 quiz questions (24 "Check yourself", 8 warm-ups). Every question is mapped to at least one objective. Every step is mapped except L1-T1, which is set-up (define the function, import pandas and pytest).

## Lesson 1: Your first assertion

| # | Objective (you can…) | Lesson section | Doing | Recognition | Gaps |
|---|---|---|---|---|---|
| 1.1 | Write an `assert` statement that passes, with the function call on the left of `==` and an expected value you worked out yourself on the right. | Say what you expect | L1-T2, L1-T3 | L1-Q2 | Every task uses `rescale01()`. Nothing asks for a function of the student's own, which the lesson's "By the end you can" promises. |
| 1.2 | Tell a pass from a failure at the console and, after a failure, find the element that disagrees by running the left side on its own, and say whether the function or the expected value is wrong. | Say what you expect; Watch one fail | L1-T3, L1-T4 | L1-Q1, L2-W1 | No question shows a traceback and asks the student to read it. |
| 1.3 | Choose between a bare `==` and `== pytest.approx()` and predict which one passes, for floating-point noise and for a whole number against its decimal (`1` and `1.0`). | Equal, or close enough? | L1-T5 | L1-Q3, L2-W2 | The `1` and `1.0` case is one sentence in the lesson and is never assessed. |
| 1.4 | Explain what a written test gives you that a look at console output does not, and what it does not guarantee. | The check that disappears | none | L1-Q4 | Recognition only. |

## Lesson 2: Test functions and test files

| # | Objective (you can…) | Lesson section | Doing | Recognition | Gaps |
|---|---|---|---|---|---|
| 2.1 | Write a test function about one behaviour, with a name that says what the function should do. | Group assertions into a test (L2); One behaviour per test (L4) | L2-T3, L3-T3, L4-T2, L4-T3 | L2-Q1 | L2-Q1 covers only the `test` prefix. No question covers the quality of a name, one behaviour per test, or the duplicate-name trap. |
| 2.2 | Lay out a plain project with `clean.py` and `tests/`, and create a test file that pytest will find and that imports the functions it tests. | Give tests a home; The test file | L2-T1 (guided), L2-T4 | L2-Q2, L3-W1, L3-W2 | L2-T1 allows a download, so building the layout by hand is optional. The `from clean import …` line is not assessed on its own. L3-W2 (assertion, test, file) is about the hierarchy, which is only loosely evidence for layout. |
| 2.3 | Run every test in a plain project with one command, and fix a run that stops with `ModuleNotFoundError: No module named 'clean'`. | Run everything; Common trap | L2-T2 | L2-Q3, L2-Q5, L4-W2 | No step triggers the trap. |
| 2.4 | Read a pytest report: say what the last line counts and, for a failure, which test it is, where it is, why it failed, and whether the code or the test is wrong. | Run everything; Reading a failure | L2-T3 (counts only), L4-T1, L5-T2 | L2-Q4 | No Lesson 2 step produces a failure inside a test file. No question shows a report and asks where or why. "A test stops at its first failing assertion" is not assessed. |

## Lesson 3: Choosing the right assertion

| # | Objective (you can…) | Lesson section | Doing | Recognition | Gaps |
|---|---|---|---|---|---|
| 3.1 | Pick the check that fits what is being compared (`==`, `pytest.approx()`, `assert_series_equal()`, `assert_frame_equal()`, or a plain `assert` on a length, dtype, type or bound), and say what its failure message gains over `.equals()`. | Why not `==` for everything?; The working set | L3-T3 | L3-Q1, L3-Q3, L3-Q4, L4-W1 | `set()`, `re.fullmatch()` and `assert not` appear only in the table and are never assessed. The "truth value of a Series is ambiguous" crash is shown but not assessed. |
| 3.2 | Test the values of a function that returns a data frame: build a tiny input by hand, call the function, and compare the result with an expected data frame you typed by hand, with dtypes that match. | Testing a function that returns a data frame; Common trap | L3-T1 (guided), L3-T2 | L3-Q2, L3-Q5 | Students never write a data-frame test of their own. Arrange, act, assert is not assessed. |
| 3.3 | Test the structure of a result (its type and its column names) in a separate test that builds everything it needs. | Structure checks | L3-T1 (guided) | L3-Q3 | Self-contained tests are not assessed. The only doing evidence is copying. |

## Lesson 4: Edge cases, errors and bugs

| # | Objective (you can…) | Lesson section | Doing | Recognition | Gaps |
|---|---|---|---|---|---|
| 4.1 | For a function that takes a column, list the edge cases (missing values, all values the same, a single value, empty input, the wrong type), decide what should happen for each, and record each decision as a test. | Ask what could go wrong | L4-T1 (guided), L4-T2, L4-T3 | L4-Q4 | Empty input (`pd.Series([], dtype="float64")`) is in the table but never tested or assessed. A single value appears only in L4-T2. L4-Q4 names three of the five cases. Why a missing value needs `assert_series_equal()` is not assessed. L4-T3 uses `clean_names()`, which takes a list of names, so it is edge-case practice but not for a column. |
| 4.2 | On finding a bug, write a test that fails, fix the function, and run every test again. | A bug, caught test-first | L4-T1 (guided), L5-T3 | L4-Q3, L5-W2 | The only bug is the one the page walks through. Running all the tests again, not just the new one, is not assessed. L5-T3 is fail-first for a new function, not for a bug. |
| 4.3 | Test that a function stops with a specific error by giving `pytest.raises()` an exception type and a `match` pattern, and explain why `pytest.raises(Exception)` can pass while testing nothing. | Expecting an error; Common trap | L4-T1 (guided) | L4-Q1, L4-Q2, L5-W1 | No task has the student write an error test of their own. |
| 4.4 | State with `pytest.warns()` when a function should warn and with `warnings.simplefilter("error")` when it should not, and treat a warning count on the last line of a report as something to investigate. | Warnings | L4-T1 (guided) | L4-Q5 | L4-Q5 covers only the warning count. Neither form is assessed, and there is no independent task. |

## Lesson 5: From project to package

| # | Objective (you can…) | Lesson section | Doing | Recognition | Gaps |
|---|---|---|---|---|---|
| 5.1 | Turn a plain project into a package with a `src/` layout, an `__init__.py` and a `pyproject.toml`, install it in editable mode in a virtual environment, and run every test with `pytest`. | Build it | L5-T1 | L5-Q2 | Creating and activating the virtual environment is not assessed by any question. |
| 5.2 | Say what the editable install does in place of `python -m pytest`, and what changes in the test file's import line. | What changes, and what does not; What you now have | L5-T1 | L5-Q1, L5-Q3 | Reactivating the environment in a new terminal (the trap) and the reason for `src/` are not assessed. |
| 5.3 | Declare dependencies in `pyproject.toml`: put a package under `dependencies` or in a dependency group according to whether your functions need it or only your tests do. | Build it, step 2; What you now have | L5-T1 | L5-Q4 | `[build-system]` and `[tool.pytest]` are explained but not assessed. |
| 5.4 | Work in the package loop (edit, `pytest`, and `-k`, `--lf` or `-x` to narrow a run) and add a new function test-first in a new module with its own test file. | The working loop | L5-T2, L5-T3 | L5-Q5 | `-k` and `-x` are not practised in any step. Only `--lf` is practised and assessed. |

## Gaps that recur

These are the patterns behind the Gaps column, in the order I would fix them.

1. **Guided doing.** L3-T1 and L4-T1 carry most of the doing evidence for objectives 3.2, 3.3, 4.3 and 4.4, and both have the student follow the page. Each of those objectives needs one step where the student writes the test unprompted.
2. **No function of the student's own.** Every task uses the four course helpers. `MISSION.md` says "for a function of their own, without a template".
3. **Reading failures is under-assessed.** No question shows a traceback or a pytest report and asks where, what or why (objectives 1.2 and 2.4).
4. **Taught but never assessed.** One behaviour per test, the duplicate-name trap, self-contained tests, arrange/act/assert, empty input, `pytest.warns()` and the no-warning form, activating a virtual environment, `[tool.pytest]`, `-k` and `-x`, and three rows of the Lesson 3 table.

## Differences from the R course that change the evidence map

The R course (`acatlin/r-unit-testing`) is the model for this one. Three differences are worth knowing when comparing the two maps.

- **pytest counts tests; testthat counts expectations.** L2-T3 therefore has the student add an assertion (count unchanged) and then a test (count goes up), which also gives Lesson 2 a step that writes a new test. The R course has no such step.
- **Lesson 1 has a fifth step (L1-T5)** on `pytest.approx()`, so objective 1.3 has doing evidence in its own lesson. In the R course that evidence comes from Lesson 3.
- **Objective 3.2 includes dtypes.** `assert_frame_equal()` is strict about dtype by default, where `expect_equal()` treats `2` and `2L` as equal, so L3-T2 and L3-Q2 belong to 3.2 here and to 1.3 in the R course.

## Extension objectives (not yet taught)

Lesson 5 promises parametrised tests, fixtures and `conftest.py`, skipping, and coverage. Running tests on GitHub Actions is added here. None has a lesson, a "Try it" step or a quiz question yet, so all evidence columns are empty. Each objective points at the reading a lesson should be built from; full "use for" notes are in `RESOURCES.md`.

| # | Objective (you can…) | Recommended reading |
|---|---|---|
| P1 | Turn several tests that differ only in their input and expected value into one test with `@pytest.mark.parametrize`, and say how many tests pytest then reports. | [pytest, "`@pytest.mark.parametrize`: parametrizing test functions"](https://docs.pytest.org/en/stable/how-to/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions) |
| P2 | When a parametrised test fails, read the values in square brackets after its name to tell which case failed. | [The same section](https://docs.pytest.org/en/stable/how-to/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions) |
| F1 | Move set-up that several tests repeat into a function marked `@pytest.fixture`, and have a test request it by naming it as an argument. | [pytest, "How to use fixtures", "Requesting fixtures"](https://docs.pytest.org/en/stable/how-to/fixtures.html#requesting-fixtures) |
| F2 | Share a fixture between test files by putting it in `conftest.py`. | [pytest, "How to use fixtures", "Scope: sharing fixtures…"](https://docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session) |
| F3 | Write files in a test only inside the temporary folder that the built-in `tmp_path` fixture provides. | [pytest, "The `tmp_path` fixture"](https://docs.pytest.org/en/stable/how-to/tmp_path.html#the-tmp-path-fixture) |
| K1 | Skip a test under a stated condition with `@pytest.mark.skip`, `@pytest.mark.skipif` or `pytest.importorskip()`, and list the skips and their reasons with `pytest -rs`. | [pytest, "Skipping test functions"](https://docs.pytest.org/en/stable/how-to/skipping.html#skipping-test-functions) |
| K2 | Say how a skip differs from an expected failure (`xfail`), and find the count of each on the last line of the report. | [pytest, "How to use skip and xfail to deal with tests that cannot succeed"](https://docs.pytest.org/en/stable/how-to/skipping.html) |
| C1 | Measure which lines your tests run with `coverage run -m pytest` and `coverage report -m`, and use the `Missing` column to find lines that no test runs. | [Coverage.py, "Quick start"](https://coverage.readthedocs.io/en/latest/) |
| C2 | Open the report made by `coverage html` and use the lines it marks as missed to choose the next test to write. | [Coverage.py, "Quick start"](https://coverage.readthedocs.io/en/latest/) |
| G1 | Add a workflow that installs your package and runs `pytest` on every push, using the `checkout` and `setup-python` actions, and say which Python versions it runs on. | [GitHub Docs, "Building and testing Python"](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) |
| G2 | When a GitHub Actions run fails, find the failing test in the log, reproduce it on your own computer, fix it, and push until the run passes. | [GitHub Docs, "Testing with pytest and pytest-cov"](https://docs.github.com/en/actions/tutorials/build-and-test-code/python#testing-with-pytest-and-pytest-cov) |

### Notes for whoever writes these lessons

- **Parametrising replaces snapshots in the list.** The R course's first extension topic is snapshot tests. pytest has no built-in snapshot expectation, so the Python course puts `@pytest.mark.parametrize` there instead: it is built in, and it is the natural next step after Lesson 4, where the test file fills up with near-identical edge-case tests. Snapshot testing moves to "Later candidates".
- **One behaviour per test versus parametrising.** Lesson 4 teaches several short named tests. P1 has to explain that a parametrised test is still one behaviour, checked over several inputs, and that each input is reported as its own test.
- **Self-contained tests versus fixtures.** Lesson 3 teaches that each test builds what it needs. F1 has to explain when a fixture is worth the loss.
- **Two ways to measure coverage.** Coverage.py's own page says "Many people choose to use the pytest-cov plugin, but for most purposes, it is unnecessary", so C1 uses `coverage run -m pytest`. The pytest-cov README warns that `coverage run -m pytest` and `pytest --cov` "do not necessarily import code the same way", because only the first adds the working directory to `sys.path`. With the Lesson 5 package (installed, `src/` layout) both work.
- **C2 is worded narrowly.** No source read so far says what coverage does not tell you. Find one before a lesson claims that a covered line is not necessarily a tested behaviour.
- **CI needs the install step.** The GitHub Docs examples run `pip install pytest` and then `pytest`. For the Lesson 5 package the workflow has to run `python -m pip install -e . --group dev` first. This repository's own `.github/workflows/check.yml` does that and can serve as the worked example.
- **Not yet read.** The pytest fixtures reference, the `conftest.py` discovery rules, Coverage.py's configuration and exclusion pages, and the full GitHub Actions workflow syntax.

## Later candidates (no objectives yet)

- **Mocking.** pytest's [`monkeypatch` fixture](https://docs.pytest.org/en/stable/how-to/monkeypatch.html). The page has been fetched but not read closely.
- **Test-first development as a full method.** Lessons 4 and 5 teach the fail-first step for bugs and new functions only.
- **Snapshot tests.** Needs a third-party plugin. No source has been read.
- **Validating data, not functions.** No source has been read.
- **Property-based testing with Hypothesis**, which the Scientific Python Development Guide recommends for finding edge cases. No source has been read.
