"""Test Script: Testing functions from transform.py"""
from unittest.mock import MagicMock, patch
import pandas as pd

from transform import (
    get_conditions_sun,
    get_conditions_shade,
    flatten_data,
    transform_email_column_using_regex,
    transform_phone_column_using_regex
)


def test_get_conditions_sun():
    conditions = ["part sun", "part shade"]
    result = get_conditions_sun(conditions)
    assert isinstance(result, str)
    assert result == "part sun"


def test_get_conditions_shade():
    conditions = ["part sun", "part shade"]
    result = get_conditions_shade(conditions)
    assert isinstance(result, str)
    assert result == "part shade"


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
    """"""
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


# def test_transform_phone_column_using_regex():
#     """"""
#     mock_phone_data = [{"botanist_phone_number": "001.251-701-7428x7358", },
#                        {
#         "botanist_phone_number": [
#             "001.251-701-7428x7358",
#             "001-197/304-0701x96926",
#             "531)160(8892x4734",
#             "9766126198",
#             "+1-233-531-2626x72126"
#         ]
#     }
#     ]

#     mock_database = pd.DataFrame(mock_phone_data)
#     result_df = transform_phone_column_using_regex(mock_phone_data)

#     expected_result = [
#         "251-701-7428",
#         "197-304-0701",
#         "531-160-8892",
#         "976-612-6198",
#         "233-531-2626"
#     ]

#     assert result_df["botanist_phone_number"].tolist() == expected_result
