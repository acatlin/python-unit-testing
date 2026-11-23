# Working notes

## Who the lessons are for
The learner in this workspace is Andy's students, not Andy. Lessons speak to a first-semester graduate data science student. The "ask your teacher" reminder in each lesson therefore points to instructor, classmates, or an AI assistant.

## What Andy asked for (2026-11-23)
- A parallel version, for Python, of everything in the R course repo (`../r_tests`, `acatlin/r-unit-testing`).
- A separate GitHub repo with GitHub Pages enabled. Always push everything to `main`.

## Decisions carried over from the R course (Andy, 2026-11-20)
- Setting: scripts and plain projects first (lessons 1 to 4), package workflow last (lesson 5).
- Examples: data-cleaning helpers (`rescale01()`, `clean_names()`, `parse_money()`, `summarise_by()`).
- Students write tests by hand.
- Each page has a short multiple-choice quiz.
- The course will be extended once these five lessons are working.

## Decisions made while translating (Claude, 2026-11-23; Andy has not reviewed these)
- Repo: public, `acatlin/python-unit-testing`, GitHub Pages from `main` (root), named to match `r-unit-testing`.
- Tools: pytest for testing and pandas for data frames, as the counterparts of testthat and dplyr/tibble.
- The helpers take pandas objects: `rescale01()` and `parse_money()` take a Series, `clean_names()` a list of names, `summarise_by()` a data frame with column names given as strings.
- `parse_money()` issues its own warning with `warnings.warn()`. In R the warning came free from `as.numeric()`; pandas has no equivalent, and Lesson 4 needs a function that warns.
- Plain project layout: `clean.py` at the top and `tests/test_clean.py`, run with `python -m pytest`. There is no counterpart of `run-tests.R` or `local_edition(3)`; the one chore a plain project has is making `clean.py` importable.
- Lesson 5 builds the package by hand (`src/` layout, `pyproject.toml`, `venv`, `pip install -e . --group dev`), following pytest's "Good Integration Practices". Python has no single counterpart of usethis; uv and similar tools are out of scope.
- `devtools::load_all()` and `devtools::check()` have no direct counterpart. The working loop in Lesson 5 uses `pytest -k`, `--lf` and `-x` instead.
- Extension topics: parametrised tests take the place of snapshot tests (see `OBJECTIVES.md`).

## Conventions
- Every lesson links `assets/course.css` and `assets/course.js`; no page-specific CSS or JS. The stylesheet is the same file as the R course's. If the design changes, change both.
- Lesson files: `lessons/000N-dash-case.html`. Each has: eyebrow, h1, lede, "By the end you can", warm-up quiz on the previous lesson (from lesson 2), teaching sections with margin citations, "Try it", "Check yourself" quiz, primary source box, ask box, pager.
- Code figures: `class="code py"` for Python, `code sh` for terminal commands, `code toml` for settings files (all three get a copy button), `code out` for output, with `pass` or `fail` to colour the edge.
- Quiz options: exactly four, one `data-correct`, equal word counts, similar character lengths. `python tools/check_site.py` enforces this and checks links.
- Glossary terms (`reference/glossary.html`) are used in one sense everywhere. Add new terms there first. "Assertion" is the counterpart of the R course's "expectation"; "test name" of "description".
- Actual on the left, expected on the right: `assert actual == expected`, `assert_frame_equal(actual, expected)`. pandas reports them as `[left]` and `[right]`.
- All output shown is real. Capture pytest output with `COLUMNS=80`. Replace the folder after `rootdir:` (and in warning locations) with `C:\Users\you\…` and say so in the page colophon. Timings and the `platform` line are left as captured. Note the versions in the colophon. `python tools/check_outputs.py` rebuilds each lesson's scenario along the path a student follows and checks every output block against it; update its scenario when a lesson's steps change.
- Example code lives in `examples/` and is run by `tools/run_examples.py` (also in CI). `examples/cleaning-project/clean.py` and `examples/cleaner/src/cleaner/clean.py` differ only in the first line of the docstring; the two `test_clean.py` files differ only in the import line. The finished test file holds exactly the 12 tests a student has after following Lessons 2 to 4.
- New lessons: add to the nav in every page header, to `index.html`, and to the cheat sheet.
- Mastery objectives live in two files with identical wording: `reference/mastery-objectives.html` (students) and `OBJECTIVES.md` (instructor: evidence map and gaps). Evidence ids are positional (`L3-Q2`, `L2-W1`, `L4-T3`), so adding, removing or reordering a "Try it" step or quiz question means updating both files. A new lesson moves its objectives from "not yet taught" into a lesson table.

## Ideas for the extension
- Parametrised tests (`@pytest.mark.parametrize`) for the edge-case tests of Lesson 4.
- Fixtures, `conftest.py`, and `tmp_path` for clean-up.
- Skipping (`skip`, `skipif`, `importorskip`) and expected failures (`xfail`).
- Coverage with Coverage.py.
- Running tests on GitHub Actions.
- Turning warnings into errors for the whole project (`filterwarnings = ["error"]` in `[tool.pytest]`), as the Scientific Python guide recommends. Left out of Lesson 5 so that a new deprecation warning in pandas cannot break a student's first package.
- Testing data, not just functions, as a contrast.
