"""Conftest File: Store commonly accessed resources for testing purposes"""
import pytest
import pandas as pd

from transform import build_plant_dataframe


@pytest.fixture
def mock_api_data():
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
    return pd.DataFrame(mock_flattened_data)


@pytest.fixture
def mock_transformed_database(mock_flattened_data):
    return build_plant_dataframe(mock_flattened_data)
