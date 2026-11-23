"""Data-cleaning helpers: the starting point for Lesson 2.

Each function is small on purpose: small functions are easy to test.
"""

import re
import warnings

import pandas as pd


def rescale01(x):
    """Rescale a numeric column so its smallest value is 0 and its largest is 1."""
    lo, hi = x.min(), x.max()
    return (x - lo) / (hi - lo)


def clean_names(names):
    """Turn messy column names into lower-case snake_case."""
    cleaned = []
    for name in names:
        name = re.sub(r"[^a-z0-9]+", "_", name.lower())
        cleaned.append(name.strip("_"))
    return cleaned


def parse_money(x):
    """Convert a column of strings such as "$1,200.50" to numbers."""
    digits = x.str.replace(r"[$,]", "", regex=True)
    numbers = pd.to_numeric(digits, errors="coerce").astype("float64")
    n_bad = int(numbers.isna().sum() - x.isna().sum())
    if n_bad > 0:
        warnings.warn(f"{n_bad} value(s) could not be parsed as money", stacklevel=2)
    return numbers


def summarise_by(data, group, value):
    """Count rows and average one column within each group."""
    return data.groupby(group, as_index=False).agg(
        n=(value, "size"),
        mean=(value, "mean"),
    )
