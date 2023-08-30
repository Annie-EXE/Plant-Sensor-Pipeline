"""Test Script: Testing functions from transform.py"""
from unittest.mock import MagicMock, patch
import pandas as pd

from transform import (
    flatten_data,
    transform_email_column_using_regex
)


def test_flatten_data_returns_correct_data(mock_nested_data, mock_flattened_data):
    """"""
    result = flatten_data([mock_nested_data])
    assert result == mock_flattened_data


def test_transform_email_column_using_regex():
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
