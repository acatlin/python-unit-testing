import re
import warnings

import pandas as pd
import pytest

from clean import clean_names, parse_money, rescale01, summarise_by

# rescale01() ---------------------------------------------------------------


def test_rescale01_maps_smallest_to_0_and_largest_to_1():
    assert rescale01(pd.Series([0, 5, 10])).tolist() == [0, 0.5, 1]
    assert rescale01(pd.Series([-2, 0, 2])).tolist() == [0, 0.5, 1]


def test_rescale01_returns_one_float_per_input_value():
    x = rescale01(pd.Series([1, 2, 3]))
    assert x.dtype == "float64"
    assert len(x) == 3


def test_rescale01_keeps_missing_values_missing():
    result = rescale01(pd.Series([1, None, 3]))
    expected = pd.Series([0, None, 1])
    pd.testing.assert_series_equal(result, expected)


def test_rescale01_returns_zeros_when_every_value_is_the_same():
    assert rescale01(pd.Series([5, 5, 5])).tolist() == [0, 0, 0]


def test_rescale01_rejects_a_column_that_is_not_numeric():
    with pytest.raises(TypeError, match="must be a numeric column"):
        rescale01(pd.Series(["a", "b"]))


# clean_names() -------------------------------------------------------------


def test_clean_names_returns_lower_case_snake_case():
    assert clean_names(["First Name"]) == ["first_name"]
    assert clean_names(["Total ($)", " Zip-Code "]) == ["total", "zip_code"]


def test_clean_names_output_has_only_letters_digits_and_underscores():
    for name in clean_names(["First Name", "Total ($)"]):
        assert re.fullmatch(r"[a-z0-9_]+", name)


# parse_money() -------------------------------------------------------------


def test_parse_money_strips_dollar_signs_and_commas():
    assert parse_money(pd.Series(["$1,200.50"])).tolist() == [1200.5]
    assert parse_money(pd.Series(["75"])).tolist() == [75]


def test_parse_money_warns_when_a_value_cannot_be_parsed():
    with pytest.warns(UserWarning, match="could not be parsed"):
        parse_money(pd.Series(["n/a"]))


def test_parse_money_is_quiet_when_every_value_parses():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        parse_money(pd.Series(["$5"]))


# summarise_by() ------------------------------------------------------------


def test_summarise_by_counts_rows_and_averages_within_each_group():
    staff = pd.DataFrame({
        "dept": ["a", "a", "b"],
        "pay": [10, 20, 60],
    })
    expected = pd.DataFrame({
        "dept": ["a", "b"],
        "n": [2, 1],
        "mean": [15.0, 60.0],
    })
    pd.testing.assert_frame_equal(summarise_by(staff, "dept", "pay"), expected)


def test_summarise_by_returns_a_data_frame_with_the_documented_columns():
    staff = pd.DataFrame({"dept": ["a", "a", "b"], "pay": [10, 20, 60]})
    out = summarise_by(staff, "dept", "pay")
    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["dept", "n", "mean"]
