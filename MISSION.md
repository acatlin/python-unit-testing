# Mission: Unit Testing in Python (a course for graduate data science students)

## Why
Andy is building a short web course that teaches first-semester graduate data science students to write unit tests for their own Python code by hand, using pytest. The students arrive able to write functions and pandas pipelines and leave able to state, as runnable code, what those functions should do. The course is the Python parallel of Unit Testing in R (`acatlin/r-unit-testing`): same five lessons, same examples, same page design. It is delivered as GitHub Pages and will be extended after the first five lessons are working.

## Success looks like
- A student can write `assert` statements and `test_` functions for a function of their own, without a template.
- A student can lay out `clean.py` and `tests/`, run every test with one command, and read a failure report to decide whether the code or the test is wrong.
- A student picks the check that fits what is being compared (`==`, `pytest.approx()`, `assert_series_equal()`, `assert_frame_equal()`) and can test a function that returns a data frame.
- A student who finds a bug writes a failing test before fixing it, and tests edge cases (missing, constant, empty, wrong type) and errors.
- A student can move the same functions and tests into an installable package and run `pytest`.
- Every page has a short multiple-choice quiz, and the site is live at https://acatlin.github.io/python-unit-testing/.

## Constraints
- Audience: some Python and basic pandas; possibly no experience of unit testing or of any Python testing package.
- Students write tests by hand. No AI-generated tests in this part of the course.
- Delivery: static HTML on GitHub Pages, repo `acatlin/python-unit-testing`, everything pushed to `main`.
- Every code block and output shown must come from a real run, and claims must cite official documentation.
- Lessons are short (20 to 30 minutes) and each has a quiz.
- Stay parallel to the R course: a lesson added to one should have a counterpart in the other, unless the tool has no counterpart (see `NOTES.md`).

## Out of scope
- For the first five lessons: parametrised tests, fixtures and `conftest.py`, mocking, skipping, code coverage, continuous integration, and test-driven development as a full method. These are candidates for the extension.
- Other testing tools (`unittest`, `doctest`, nose) and testing notebooks or web apps.
- Project tools that wrap pip and venv (uv, Poetry, Hatch, conda environments). Lesson 5 uses `venv` and `pip` only, as the first option in the pytest documentation does.
