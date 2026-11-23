# Unit Testing in Python Resources

All entries below were fetched and read on 2026-11-23 unless marked otherwise.

## Knowledge

- [Docs: pytest, "Get Started"](https://docs.pytest.org/en/stable/getting-started.html) (documents pytest 9.2.0, the version used to run all course code)
  Use for: installing into a virtual environment, the first test, the `test_*.py` or `*_test.py` rule, `pytest.raises()`, `pytest.approx()`, assertion introspection.
- [Docs: pytest, "How to write and report assertions in tests"](https://docs.pytest.org/en/stable/how-to/assert.html)
  The primary source for Lessons 1, 3 and 4. Use for: plain `assert`, what pytest shows for a failed comparison, `pytest.approx()`, `pytest.raises()` as a context manager, the `match` argument (matched with `re.search()`).
- [Docs: pytest API reference](https://docs.pytest.org/en/stable/reference/reference.html), entries [`pytest.approx`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.approx), [`pytest.raises`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises), [`pytest.warns`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.warns)
  Use for: the default tolerances of `approx` (relative `1e-6`, absolute `1e-12`), how it compares with `math.isclose` and `numpy.isclose`, and the warning that `pytest.raises(Exception)` "will catch ANY exception raised".
- [Docs: pytest, "Good Integration Practices"](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
  The primary source for Lessons 2 and 5. Use for: test discovery rules, the `src/` layout with `tests/` outside it, `pyproject.toml` with `[dependency-groups]`, `pip install -e . --group dev` (pip 25.1 or newer), `importlib` import mode for new projects, strict mode.
- [Docs: pytest, "How to invoke pytest"](https://docs.pytest.org/en/stable/how-to/usage.html) and ["pytest import mechanisms and sys.path/PYTHONPATH"](https://docs.pytest.org/en/stable/explanation/pythonpath.html)
  Use for: `python -m pytest` adding the current directory to `sys.path`, `-k`, running one file or one test by node id, and what each import mode does.
- [Docs: pytest, "Configuration"](https://docs.pytest.org/en/stable/reference/customize.html)
  Use for: the `[tool.pytest]` table in `pyproject.toml` (pytest 9.0 and later) versus `[tool.pytest.ini_options]` (6.0 and later), `pytest.toml`, and how the rootdir is found.
- [Docs: pytest, "How to capture warnings"](https://docs.pytest.org/en/stable/how-to/capture-warnings.html)
  Use for: the warnings summary, `pytest.warns()` with `match`, the documented way to assert that no warning is raised, `-W error` and the `filterwarnings` setting.
- [Docs: pytest, "Anatomy of a test"](https://docs.pytest.org/en/stable/explanation/anatomy.html)
  Use for: arrange, act, assert, cleanup.
- [Docs: pytest, "How to re-run failed tests…"](https://docs.pytest.org/en/stable/how-to/cache.html) and ["How to handle test failures"](https://docs.pytest.org/en/stable/how-to/failures.html)
  Use for: `--lf` and `-x`.
- [Docs: pandas API reference, `assert_frame_equal()`](https://pandas.pydata.org/docs/reference/api/pandas.testing.assert_frame_equal.html) and [`assert_series_equal()`](https://pandas.pydata.org/docs/reference/api/pandas.testing.assert_series_equal.html) (documents pandas 3.1)
  Use for: `check_dtype` (default `True`), `check_exact`, `rtol` (default `1e-5`) and `atol` (default `1e-8`), `check_like`, and the dtype example in the docstring.
- [Docs: pandas user guide, "Working with missing data"](https://pandas.pydata.org/docs/user_guide/missing_data.html) and ["Frequently Asked Questions"](https://pandas.pydata.org/docs/user_guide/gotchas.html)
  Use for: `np.nan == np.nan` being `False`, and why `if` or `assert` on a Series raises "The truth value of a Series is ambiguous".
- [Docs: pandas contributing guide, "Test-driven development"](https://pandas.pydata.org/docs/development/contributing_codebase.html#test-driven-development)
  Use for: writing the failing test before the code, said by the pandas project about its own work.
- [Guide: Scientific Python Development Guide, "Testing recommendations"](https://learn.scientific-python.org/development/principles/testing/)
  The source for why to test and what makes a good test. Use for: the four advantages of testing, "Check that your test fails when it should!", "Test one thing at a time", test files named `test_{file under test}.py`, unit tests that are "simple, isolated, and run very quickly".
- [Guide: Scientific Python Development Guide, "Test" tutorial](https://learn.scientific-python.org/development/tutorials/test/) and ["Testing with pytest"](https://learn.scientific-python.org/development/guides/pytest/)
  Use for: "a test stops at the first failing assertion", the commonly used switches (`-v`, `-x`, `-k`, `--lf`), "pytest is used almost exclusively", and a recommended pytest configuration (`filterwarnings = ["error"]`, `strict = true`).
- [Docs: Python Packaging User Guide, "Packaging Python Projects"](https://packaging.python.org/en/latest/tutorials/packaging-projects/), ["Writing your pyproject.toml"](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), ["src layout vs flat layout"](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/), ["Install packages in a virtual environment using pip and venv"](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) and the [Dependency Groups specification](https://packaging.python.org/en/latest/specifications/dependency-groups/)
  Use for: the `src/` tree, why `__init__.py` is recommended, the `[build-system]`, `[project]` and `[dependency-groups]` tables, `dependencies` versus `optional-dependencies`, creating and activating `.venv`, and having to reactivate in a new shell. The [`venv` page of the Python documentation](https://docs.python.org/3/library/venv.html) is the source for the PowerShell execution-policy fix.
- [Docs: pip, "Local project installs"](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs)
  Use for: what an editable install is and when a reinstall is needed.
- [Docs: Python language reference, "The assert statement"](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) and [Python tutorial, "Floating-Point Arithmetic: Issues and Limitations"](https://docs.python.org/3/tutorial/floatingpoint.html)
  Use for: what `assert` does (and that `python -O` removes it), and why `0.1 + 0.2` is not `0.3`.
- [Docs: Google Colab, "Using Google Colab with GitHub"](https://colab.research.google.com/github/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb) (the notebook in `googlecolab/colabtools`)
  Use for: the link form `https://colab.research.google.com/github/<user>/<repo>/blob/<branch>/<path>.ipynb` ("Colab can load public github notebooks directly, with no required authorization step"), and that opening one gives "a new editable view of the notebook", saved with File, Save a copy in Drive.
- [Data: `googlecolab/backend-info`](https://github.com/googlecolab/backend-info), files `pip-freeze.txt` and `apt-list.txt` (last changed 2026-11-20)
  Use for: what Colab ships. On 2026-11-23: Python 3.13.18, pandas 2.2.3, pytest 8.4.2, pip 26.2.2, numpy 2.4.6. The README warns the files can be a day or two ahead of the live runtime.
- [Docs: Google Colab, "Frequently Asked Questions - Past Runtime Versions"](https://research.google.com/colaboratory/runtime-version-faq.html)
  Use for: "we recommend using the latest runtime version… and adding code to your notebook to install specific versions of libraries that you need", which is why each notebook starts with a `%pip install` of pinned versions and does not pin a runtime.
- [Docs: IPython, "Built-in magic commands"](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
  Use for: `%%writefile [-a] filename`: "Write the contents of the cell to a file. The file will be overwritten unless the -a (--append) flag is specified."
- For the extension: pytest ["How to parametrize fixtures and test functions"](https://docs.pytest.org/en/stable/how-to/parametrize.html), ["How to use fixtures"](https://docs.pytest.org/en/stable/how-to/fixtures.html), ["How to use temporary directories and files in tests"](https://docs.pytest.org/en/stable/how-to/tmp_path.html), ["How to use skip and xfail…"](https://docs.pytest.org/en/stable/how-to/skipping.html); [Coverage.py](https://coverage.readthedocs.io/en/latest/) (documents 7.17.5) and the [pytest-cov README](https://pytest-cov.readthedocs.io/en/latest/readme.html); [GitHub Docs, "Building and testing Python"](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
  Skimmed, not studied. Use for: the objectives in `OBJECTIVES.md`. Read each one properly before writing its lesson.

## Wisdom (Communities)

- [pytest discussions on GitHub](https://github.com/pytest-dev/pytest/discussions)
  Named on pytest's ["Contact channels"](https://docs.pytest.org/en/stable/contact.html) page "for general questions". Use for: judgement questions (how much to test, how to structure tests for an analysis project).
- [pytest issue tracker](https://github.com/pytest-dev/pytest/issues)
  Use for: checking whether surprising behaviour is a known bug. Read before posting.
- The class itself: instructor and classmates. Use for: comparing edge-case decisions, reviewing each other's tests.

## Gaps

- pytest's contact page also points to Stack Overflow's `pytest` tag. It was not fetched for verification, so it is not linked from the lessons.
- No source yet for testing analysis scripts and Jupyter notebooks (as opposed to functions). Needed if the extension goes there.
- The pandas reference does not say in words that `assert_series_equal()` treats missing values in the same position as equal. Lesson 4 states it on the strength of a run, and says so in its margin note.
- The Scientific Python guide's taxonomy puts extensive edge-case testing in a separate suite from unit tests ("Avoid the temptation to test edge-cases!" in unit tests). This course does not divide tests into suites, and Lesson 4 teaches edge cases in the same file. If a student reads the guide and asks, that is the difference.
- No source yet for the limits of coverage, and none read for snapshot testing, mocking beyond a skim, data validation, or Hypothesis.
- The notebooks have not been run in a real Colab session. Colab's "Overview of Colab features" notebook, which documents `!` commands, could not be fetched (404 at the path tried), so the statement that each `!` line runs in its own shell rests on IPython's behaviour, seen in the local runs.
- Editor integration (the Testing panel in VS Code and Positron, PyCharm's runner) has not been checked against official documentation, so the lessons use the terminal only.

## Findings from running the code (not in the docs above)

- In the plain project, bare `pytest` fails at collection with `ModuleNotFoundError: No module named 'clean'`, because the default import mode puts `tests/` on `sys.path`, not the project folder. `python -m pytest` from the project folder works.
- pytest's summary counts tests. A second assertion in a test does not change the count, and a test stops at its first failing assertion.
- Two test functions with the same name in one file: only the second is collected, with no warning.
- A file named `clean_tests.py` is not collected: `collected 0 items`, `no tests ran`, exit code 5.
- `rescale01(pd.Series([0.1, 0.2, 0.3])).tolist()` is `[0.0, 0.5000000000000001, 1.0]`, a natural example of floating-point noise for Lesson 1.
- `rescale01(pd.Series([5, 5, 5]))` returns `NaN` with no error and no warning: pandas suppresses the divide-by-zero warning that NumPy would give.
- With pandas 3, a column of text has dtype `str` (it was `object` in pandas 2), and subtracting one from another raises `TypeError: unsupported operand type(s) for -: 'str' and 'str'`.
- `pd.api.types.is_numeric_dtype()` is `True` for a boolean column, so the finished `rescale01()` lets `pd.Series([True, False])` through and it fails inside NumPy with a different cryptic `TypeError`. A good extra edge case for a strong student.
- `clean_names("First Name")`, a bare string instead of a list, returns one entry per character. Used in L4-T3.
- `pd.to_numeric()` returns `int64` when every value is whole, so `parse_money()` ends with `.astype("float64")` to return decimals every time.
- A failing `assert_series_equal()` or `assert_frame_equal()` on values prints a few lines of pandas internals (`pandas/_libs/testing.pyx … ???`) above the `E` lines. A dtype mismatch does not. The lessons show the `E` lines only.
- In the package, `pytest` run from `src/` collects nothing, because `testpaths` only applies when pytest is started from the folder that holds `pyproject.toml`.
- At the console, a failed `assert` shows `File "<stdin>"` when the input is piped in, which is how the Lesson 1 output was captured. An interactive console or a notebook names the input differently; the last line, `AssertionError`, is the same.
