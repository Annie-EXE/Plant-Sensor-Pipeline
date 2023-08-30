"""Test Script: Tests extract.py"""

import os
import tempfile
import json
from os import environ
from dotenv import load_dotenv
from dateutil.parser import parse

from unittest.mock import MagicMock, patch

from extract import (
    get_plant_data,
    get_all_plants_data,
    create_json_file
)

load_dotenv()

api_path = environ.get("API_PATH")

all_plants_data = get_all_plants_data(api_path)


def is_valid_timestamp(timestamp_str: str) -> bool:
    """
    Verifies whether a given
    string is a valid timestamp
    """
    try:
        parse(timestamp_str)
        return True
    except ValueError:
        return False


def test_get_plant_data_produces_dict():
    """
    Verifies that get_plant_data()
    produces a dictionary per plant
    """
    plant_data_1 = get_plant_data(1, api_path)
    assert isinstance(plant_data_1, dict)

    for plant in all_plants_data:
        assert isinstance(plant, dict)


@patch("requests.get")
def test_get_plant_data_calls_api(mock_get, mock_api_data, mock_nested_data):
    """
    Test `get_plant_data` to see if the `requests.get` function is called correctly
    """
    mock_response = MagicMock()
    mock_response.json.return_value = mock_api_data

    expected_result = mock_nested_data

    mock_get.return_value = mock_response
    mock_id = 1
    mock_api = 'mock_api_path'
    result = get_plant_data(mock_id, mock_api)

    assert mock_get.call_count == 1
    assert mock_response.json.call_count == 1
    assert result == expected_result


def test_get_plant_data_has_correct_information():
    """
    Tests that get_plant_data()
    is assigning the correct values
    to the correct keys
    """
    plant_data_1 = get_plant_data(1, api_path)
    assert plant_data_1["name"].lower() == "venus flytrap"

    plant_data_17 = get_plant_data(17, api_path)
    assert plant_data_17["name"].lower() == "ipomoea batatas"

    for plant in all_plants_data:
        if plant.get("recording_taken"):
            validate_timestamp = is_valid_timestamp(plant["recording_taken"])
            assert validate_timestamp == True


def test_data_is_retrieved_for_all_plants():
    """
    Tests that get_all_plants_data()
    is a list that contains information
    on each plant in the exhibit
    """
    assert isinstance(all_plants_data, list)
    assert len(all_plants_data) == 51


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
