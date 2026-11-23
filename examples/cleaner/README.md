# cleaner

The package built in Lesson 5 of [Unit Testing in Python](https://acatlin.github.io/python-unit-testing/lessons/0005-from-project-to-package.html). It holds four small data-cleaning functions and their tests.

To run the tests, open a terminal in this folder and make a virtual environment.

On Windows:

```
python -m venv .venv
.venv\Scripts\activate
```

On macOS and Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Then, on any system:

```sh
python -m pip install -e . --group dev
pytest
```

You should see `12 passed`.
