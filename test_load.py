"""Test Script: Testing functions from load.py"""
from unittest.mock import MagicMock
from load import (
    insert_into_plant_origin_table
)


def test_insert_into_plant_origin_table(mock_transformed_database):
    """
    Test `insert_into_plant_origin_table` calls correct functions
    """
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor().return_value
    print(mock_transformed_database)

    mock_executemany = mock_cursor.executemany

    insert_into_plant_origin_table(mock_connection, mock_transformed_database)
    assert mock_cursor.call_count == 1
