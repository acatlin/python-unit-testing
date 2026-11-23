# Audience starts with Python and basic pandas, and no testing experience

The students are first-semester graduate data science students. For the R course Andy described them (2026-11-20) as having some familiarity with R and basic tidyverse and possibly no experience of unit testing. This course assumes the same students with the Python equivalents: some Python and basic pandas, and possibly no experience of unit testing or of any Python testing package. That is an inference from the request to build a parallel course (2026-11-23), not something Andy stated; confirm it with him.

Lessons can assume a student can write a function, build a `pd.Series` and a `pd.DataFrame`, and use `groupby()`. They must not assume knowledge of packages, `pyproject.toml`, virtual environments, the import system (`sys.path`), `with` blocks beyond having seen one, or regular expressions beyond a literal phrase. One helper uses `re.sub()` with a character class; it is not explained or tested on.

## Implications
- Students may work in notebooks. Lesson 1 works in a console or a notebook cell. From Lesson 2 on they need a terminal and plain `.py` files, which may itself be new. The lessons say "open a terminal in the project folder" and do not teach the terminal.
- Package development is new material, so it comes last and is introduced as "your project is already most of a package". Virtual environments are introduced there in one step, with one command to create and one to activate.
- Lessons 1 to 5 establish: assertions, test functions, test files, `python -m pytest`, the working set of checks, edge cases, `pytest.raises()` and `pytest.warns()`, test-first bug fixing, and the installed package. Extension lessons can build on all of these.
- Students who installed Python through Anaconda already have pandas and pytest and may have pandas 2, where a text column prints as `object` instead of `str`. No output shown in the lessons depends on that.
- No evidence yet of what students actually retain; revise after the course runs once.
