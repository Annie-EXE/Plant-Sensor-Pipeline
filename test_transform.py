"""Test Script: Testing functions from transform.py"""
from datetime import datetime
import numpy as np
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from transform import (
    check_duplicates,
    get_conditions_sun,
    get_conditions_shade,
    flatten_data,
    transform_email_column_using_regex,
    transform_phone_column_using_regex,
    transform_scientific_name_column,
    transform_last_watered_column,
    transform_recording_taken_column,
    build_location_columns,
    get_valid_temperature,
    normalize_column_text
)


@pytest.mark.parametrize("conditions,expected_result", [
    (["part sun", "part shade"], "part sun"),
    (["part sun", "part sun"], "part sun"),
    (["part shade", "part shade"], "No Information"),
    (["part sun/full sun", "part shade"], "No Information")
])
def test_get_conditions_sun(conditions, expected_result):
    """
    Testing `get_conditions_sun` function
    """
    result = get_conditions_sun(conditions)
    assert isinstance(result, str)
    assert result == expected_result


@pytest.mark.parametrize("conditions,expected_result", [
    (["part sun", "part shade"], "part shade"),
    (["part sun", "part sun"], "No Information"),
    (["part shade", "part shade"], "part shade"),
    (["part sun", "part shade/filtered shade"], "No Information")
])
def test_get_conditions_shade(conditions, expected_result):
    """
    Testing `get_conditions_shade` function
    """
    result = get_conditions_shade(conditions)
    assert isinstance(result, str)
    assert result == expected_result


@pytest.mark.parametrize("conditions,expected_result", [
    (["part sun", "part shade"], False),
    (["part sun", "part sun"], True),
    (["part shade", "part shade"], True),
    (["part sun", "part shade/filtered shade"], False)
])
def test_check_duplicates_true(conditions, expected_result):
    """
    Testing `check_duplicates` function
    """
    result = check_duplicates(conditions)
    assert isinstance(result, bool)
    assert result == expected_result


def test_flatten_data_returns_correct_data(mock_nested_data, mock_flattened_data):
    """
    Test `flatten_data` creates a new dictionary and extracts nested data as expected

    Args:
        mock_nested_data (dict): A mock dictionary representing processed nested data
        retrieved from the API

        mock_flattened_data (list[dict]): A mock list of dictionaries where all nested
        data is extracted and flattened 
    """
    result = flatten_data([mock_nested_data])
    assert result == mock_flattened_data


def test_transform_email_column_using_regex():
    """
    Testing `transform_email_column_using_regex` function
    """
    mock_email_data = {
        "botanist_email": [
            "mockOne@example.com",
            "mockTwo@example.com Mock",
            "Mock mockThree@example.com",
            "Mock mockFour@example.com Mock"
        ]
    }
    mock_database = pd.DataFrame(mock_email_data)
    result_df = transform_email_column_using_regex(mock_database)

    expected_result = [
        "mockOne@example.com",
        "mockTwo@example.com",
        "mockThree@example.com",
        "mockFour@example.com"
    ]

    assert result_df["botanist_email"].tolist() == expected_result


def test_transform_phone_column_using_regex():
    """
    Testing `transform_phone_column_using_regex` function
    """
    mock_phone_data = [
        {"botanist_phone_number": "001.251-701-7428x7358"},
        {"botanist_phone_number": "001-197.304-0701x96926"},
        {"botanist_phone_number": "531)160(8892x4734"},
        {"botanist_phone_number": "9766126198"},
        {"botanist_phone_number": "+1-233-531-2626x72126"},
    ]

    mock_database = pd.DataFrame(mock_phone_data)
    result_df = transform_phone_column_using_regex(mock_database)

    expected_result = [
        "251-701-7428",
        "197-304-0701",
        "531-160-8892",
        "976-612-6198",
        "233-531-2626"
    ]

    assert result_df["botanist_phone_number"].tolist() == expected_result


def test_transform_scientific_name_column(mock_database):
    """
    Testing `transform_scientific_name_column` function
    """

    result_df = transform_scientific_name_column(mock_database)

    expected_result = ["Mock Scientific Name"]

    assert result_df["scientific_name"].tolist() == expected_result


def test_transform_last_watered_column(mock_database):
    """
    Testing `transform_last_watered_column` function
    """

    result_df = transform_last_watered_column(mock_database)

    expected_result = [datetime(2023, 1, 1, 0, 0, 0)]

    assert result_df["last_watered"].tolist() == expected_result


def test_transform_recording_taken_column(mock_database):
    """
    Testing `transform_recording_taken_column` function
    """

    result_df = transform_recording_taken_column(mock_database)

    expected_result = [datetime(2023, 1, 1, 0, 0, 0)]

    assert result_df["recording_time"].tolist() == expected_result


def test_build_location_columns(mock_database):
    """
    Testing `build_location_columns` function
    """
    result_df = build_location_columns(mock_database)

    expected_latitude = [0.0]
    expected_longitude = [0.0]
    expected_country = ["Mock Country"]

    assert result_df["plant_latitude"].tolist() == expected_latitude
    assert result_df["plant_longitude"].tolist() == expected_longitude
    assert result_df["plant_location"].tolist() == expected_country


@pytest.mark.parametrize("temperature,expected_result", [
    (-273.15, None),
    (5600, None),
    (37, 37.0)
])
def test_get_valid_temperature(temperature, expected_result):
    """
    Testing `get_valid_temperature` function
    """

    result = get_valid_temperature(temperature)

    assert result == expected_result


def test_normalize_column_text(mock_database):
    """
    Testing `normalize_column_text` function
    """
    result_df = transform_scientific_name_column(mock_database)
    result_df = build_location_columns(result_df)
    result_df = normalize_column_text(result_df)

    assert result_df["botanist_name"].tolist() == ["mock botanist"]
    assert result_df["plant_name"].tolist() == ["mock name"]
    assert result_df["plant_cycle"].tolist() == ["mock cycle"]
    assert result_df["plant_location"].tolist() == ["mock country"]
    assert result_df["scientific_name"].tolist() == ["mock scientific name"]
    assert result_df["sun_condition"].tolist() == ["mock sun detail"]
    assert result_df["shade_condition"].tolist() == ["mock shade detail"]
