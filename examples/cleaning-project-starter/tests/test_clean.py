import pandas as pd

from clean import clean_names, parse_money, rescale01


def test_rescale01_maps_smallest_to_0_and_largest_to_1():
    assert rescale01(pd.Series([0, 5, 10])).tolist() == [0, 0.5, 1]
    assert rescale01(pd.Series([-2, 0, 2])).tolist() == [0, 0.5, 1]


def test_clean_names_returns_lower_case_snake_case():
    assert clean_names(["First Name"]) == ["first_name"]
    assert clean_names(["Total ($)", " Zip-Code "]) == ["total", "zip_code"]


def test_parse_money_strips_dollar_signs_and_commas():
    assert parse_money(pd.Series(["$1,200.50"])).tolist() == [1200.5]
    assert parse_money(pd.Series(["75"])).tolist() == [75]
