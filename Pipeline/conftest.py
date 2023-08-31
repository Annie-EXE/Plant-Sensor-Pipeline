"""Conftest File: Store commonly accessed resources for testing purposes"""
import pytest
import pandas as pd

from transform import build_plant_dataframe


@pytest.fixture
def mock_api_data():
    """
    A dictionary representing data retrieved from an API request

    Returns:
        dict: Mock data from API request
    """
    data = {
        "botanist": {"email": "mock@example.com", "name": "Mock Botanist", "phone": "+000-000-000.000x000mock"},
        "cycle": "Mock Cycle",
        "last_watered": "Mon, 1 Jan 2023 00:00:00 GMT",
        "name": "Mock Name",
        "origin_location": ["0.000", "0.000", "Mock", "Mock", "Mock Country"],
        "plant_id": 0,
        "recording_taken": "2023-01-01 00:00:00",
        "scientific_name": ["Mock Scientific Name"],
        "soil_moisture": 0,
        "sunlight": ["Mock Sun detail", "Mock Shade detail"],
        "temperature": 0,
    }
    return data


@pytest.fixture
def mock_nested_data():
    """
    A dictionary representing processed data retrieved from an API request. This is mock_api_data passed through
    the `process_plant_data_from_api` function

    Returns:
        dict: A Python dictionary representing mock processed data from API request
    """
    data = {
        "plant_id": 0,
        "name": "Mock Name",
        "scientific_name": [
                "Mock Scientific Name"
        ],
        "cycle": "Mock Cycle",
        "last_watered": "Mon, 1 Jan 2023 00:00:00 GMT",
        "recording_time": "2023-01-01 00:00:00",
        "temperature": 0,
        "soil_moisture": 0,
        "sunlight_details": [
            "Mock Sun detail",
            "Mock Shade detail"
        ],
        "origin_location": {
            "origin_latitude": "0.000",
            "origin_longitude": "0.000",
            "origin_country": "Mock Country"
        },
        "botanist_details": {
            "email": "mock@example.com",
            "name": "Mock Botanist",
            "phone": "+000-000-000.000x000mock"
        }
    }
    return data


@pytest.fixture
def mock_flattened_data():
    """
    A list of dictionaries representing flatted data retrieved from an API request. This is mock_nested_data passed through
    the `flatten_data` function

    Returns:
        dict: A Python list of dictionaries representing mock flattened data from API request
    """
    data = [
        {
            'botanist_name': 'Mock Botanist',
            'botanist_email': 'mock@example.com',
            'botanist_phone_number': '+000-000-000.000x000mock',
            'plant_id': 0,
            'scientific_name': [
                'Mock Scientific Name'
            ],
            'plant_name': 'Mock Name',
            'plant_cycle': 'Mock Cycle',
            'last_watered': "Mon, 1 Jan 2023 00:00:00 GMT",
            'plant_origin': {
                'origin_latitude': '0.000',
                'origin_longitude': '0.000',
                'origin_country': 'Mock Country'
            },
            'recording_time': "2023-01-01 00:00:00",
            'soil_moisture': 0,
            'sun_condition': "Mock Sun detail",
            'shade_condition': "Mock Shade detail",
            'temperature': 0
        }
    ]
    return data


@pytest.fixture
def mock_database(mock_flattened_data):
    """
    A DataFrame built from flattened data with no transformational processing applied

    Args:
        mock_flattened_data (dict): A Python list of dictionaries representing mock flattened data from API request

    Returns:
        DataFrame: A Pandas DataFrame of flattened data with no DataFrame processing
    """
    return pd.DataFrame(mock_flattened_data)


@pytest.fixture
def mock_transformed_database(mock_flattened_data):
    """
    A DataFrame built from flattened data with transformational processing applied

    Args:
        mock_flattened_data (dict): A Python list of dictionaries representing mock flattened data from API request

    Returns:
        DataFrame: A Pandas DataFrame of flattened data with DataFrame processing
    """
    return build_plant_dataframe(mock_flattened_data)
