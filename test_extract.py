"""Test Script: Tests extract.py"""

import os
import tempfile
import json
from unittest.mock import MagicMock, patch


from extract import (
    get_plant_data_from_api,
    process_plant_data_from_api,
    get_all_plants_data,
    clean_unicode_from_plant_data,
    create_json_file
)


@patch("requests.get")
def test_get_plant_data_from_api_calls_correct_functions(mock_get, mock_api_data, mock_nested_data):
    """
    Test `get_plant_data` to see if the `requests.get` function is called correctly
    """
    mock_response = MagicMock()
    mock_response.json.return_value = mock_api_data
    mock_get.return_value = mock_response

    mock_id = "mock_id"
    mock_api = 'mock_api_path'
    get_plant_data_from_api(mock_id, mock_api)

    assert mock_get.call_count == 1
    assert mock_response.json.call_count == 1


def test_process_plant_data_from_api(mock_api_data, mock_nested_data):
    """
    Test `process_plant_data_from_api` to check if API data is being processed as expected
    """
    result = process_plant_data_from_api(mock_api_data)
    assert result == mock_nested_data


@patch("extract.get_plant_data_from_api")
def test_get_all_plants_data(mock_get_plant_data_from_api, mock_api_data, mock_nested_data):
    """
    Test `get_all_plants_data` to ensure a list of dictionaries 
    with the expected processed API data is returned
    """
    mock_get_plant_data_from_api.return_value = mock_api_data
    expected_result = [mock_nested_data] * 51

    mock_api_path = "mock_path"
    result = get_all_plants_data(mock_api_path)

    assert result == expected_result
    assert mock_get_plant_data_from_api.call_count == 51


def test_clean_unicode_from_plant_data():
    """
    Test `clean_unicode_from_plant_data` is removing the specified unicode characters
    from data
    """
    mock_data = [{"name": "\u2018Mock Name One"},
                 {"name": "Mock Name Two\u2019"}]
    expected_result = [{"name": "Mock Name One"},
                       {"name": "Mock Name Two"}]
    result = clean_unicode_from_plant_data(mock_data)
    assert result == expected_result


def test_create_json_file():

    test_data = [
        {"id": 1, "name": "daisy"},
        {"id": 2, "name": "marigold"}
    ]

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    result = create_json_file(test_data, temp_file_path)

    assert result == "Data processed!"

    with open(temp_file_path, "r") as json_file:
        file_content = json_file.read()
        actual_data = json.loads(file_content)
        expected_data = [
            {"id": 1, "name": "daisy"},
            {"id": 2, "name": "marigold"}
        ]
        assert actual_data == expected_data

    os.remove(temp_file_path)
