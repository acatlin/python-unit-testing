# Unit Testing in Python

A short course that teaches first-semester graduate data science students to write unit tests by hand with [pytest](https://docs.pytest.org/).

**Read it here: https://acatlin.github.io/python-unit-testing/**

It is the Python parallel of [Unit Testing in R](https://acatlin.github.io/r-unit-testing/) ([repository](https://github.com/acatlin/r-unit-testing)): the same five lessons, the same data-cleaning examples and the same page design, with pytest and pandas in place of testthat and dplyr.

## Lessons

1. [Your first assertion](https://acatlin.github.io/python-unit-testing/lessons/0001-first-assertion.html)
2. [Test functions and test files](https://acatlin.github.io/python-unit-testing/lessons/0002-test-functions-and-test-files.html)
3. [Choosing the right assertion](https://acatlin.github.io/python-unit-testing/lessons/0003-choosing-assertions.html)
4. [Edge cases, errors and bugs](https://acatlin.github.io/python-unit-testing/lessons/0004-edge-cases-errors-and-bugs.html)
5. [From project to package](https://acatlin.github.io/python-unit-testing/lessons/0005-from-project-to-package.html)

Reference: [cheat sheet](https://acatlin.github.io/python-unit-testing/reference/cheat-sheet.html) · [glossary](https://acatlin.github.io/python-unit-testing/reference/glossary.html) · [mastery objectives](https://acatlin.github.io/python-unit-testing/reference/mastery-objectives.html)

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` | Course home page |
| `lessons/` | One HTML page per lesson, each with a quiz |
| `reference/` | Printable cheat sheet, glossary, and the student checklist of mastery objectives |
| `OBJECTIVES.md` | Instructor view of the mastery objectives: the evidence for each one, the gaps, and the objectives for lessons not yet written |
| `assets/` | Shared stylesheet and script (code colouring, quizzes) used by every page |
| `examples/cleaning-project-starter/` | The project students begin with in Lesson 2 |
| `examples/cleaning-project/` | The same project after Lesson 4 |
| `examples/cleaner/` | The package built in Lesson 5 |
| `tools/` | Checks run locally and in CI |
| `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/` | Course design notes and sources |

The site is plain static HTML served by GitHub Pages from the root of `main`. There is no build step.

## Checking changes

```sh
python tools/check_site.py      # quiz rules and internal links
python tools/run_examples.py    # runs every example's tests
```

The second command needs pandas and pytest, and the Lesson 5 package installed in editable mode. In a virtual environment:

```sh
python -m pip install -e examples/cleaner --group examples/cleaner/pyproject.toml:dev
```

Both checks run on every push in GitHub Actions (`.github/workflows/check.yml`), on Python 3.11 and 3.14.

Quiz rules enforced by the checker: four options per question, exactly one correct, and all options the same number of words and of similar length, so the answer cannot be guessed from its shape.

## Sources

The lessons follow the [pytest documentation](https://docs.pytest.org/en/stable/), the [pandas testing reference](https://pandas.pydata.org/docs/reference/testing.html), the [Scientific Python Development Guide](https://learn.scientific-python.org/development/principles/testing/) and the [Python Packaging User Guide](https://packaging.python.org/en/latest/). All code and output shown was run with Python 3.14.4, pytest 9.2.0 and pandas 3.1.1. See `RESOURCES.md`.
