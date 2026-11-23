# cleaner

The package built in Lesson 5 of [Unit Testing in Python](https://acatlin.github.io/python-unit-testing/lessons/0005-from-project-to-package.html). It holds four small data-cleaning functions and their tests.

To run the tests, open a terminal in this folder:

```sh
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS and Linux
python -m pip install -e . --group dev
pytest
```

You should see `12 passed`.
