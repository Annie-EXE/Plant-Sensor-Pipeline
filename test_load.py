"""Test Script: Testing functions from load.py"""
from unittest.mock import MagicMock
from load import (
    insert_into_plant_origin_table,
    insert_into_plant_table,
    insert_into_botanist_table,
    insert_into_water_history_table,
    insert_into_reading_information_table
)


def test_insert_into_plant_origin_table(mock_transformed_database):
    """
    Test `insert_into_plant_origin_table` calls with correct statement functions
    """
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value

    insert_into_plant_origin_table(mock_connection, mock_transformed_database)

    mock_executemany = mock_cursor.executemany

    mock_origin_info = mock_transformed_database[['plant_latitude',
                                                  'plant_longitude', 'plant_location']].values.tolist()

    assert mock_executemany.called_with(
        """INSERT INTO plant_origin
            (latitude, longitude, country)
            VALUES
            (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, mock_origin_info
    )


def test_insert_into_plant_table(mock_transformed_database):
    """
    Test `insert_into_plant_table` calls with correct statement functions
    """
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value

    insert_into_plant_table(mock_connection, mock_transformed_database)

    mock_executemany = mock_cursor.executemany

    mock_plant_info = mock_transformed_database[['plant_id', 'plant_name', 'scientific_name',
                                                 'plant_latitude', 'plant_longitude']].values.tolist()

    assert mock_executemany.called_with("""INSERT INTO plant
                    (plant_id,
                    plant_name,
                    plant_scientific_name,
                    plant_origin_id)
                    VALUES
                    (%s, %s, %s,
                        (SELECT plant_origin_id FROM plant_origin 
                        WHERE latitude = %s and longitude = %s))
                    ON CONFLICT DO NOTHING;
                    """, mock_plant_info)


def test_insert_into_botanist_table(mock_transformed_database):
    """
    Test `insert_into_botanist_table` calls with correct statement functions
    """
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value

    insert_into_botanist_table(mock_connection, mock_transformed_database)

    mock_executemany = mock_cursor.executemany

    mock_botanist_info = mock_transformed_database[['botanist_name', 'botanist_email',
                                                    'botanist_phone_number']].values.tolist()

    assert mock_executemany.called_with("""INSERT INTO botanist
                    (botanist_name, botanist_email, botanist_phone_number)
                    VALUES
                    (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """, mock_botanist_info)


def test_insert_into_water_history_table(mock_transformed_database):
    """
    Test `insert_into_water_history_table` calls with correct statement functions
    """
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value

    insert_into_water_history_table(mock_connection, mock_transformed_database)

    mock_executemany = mock_cursor.executemany

    mock_watering_info = mock_transformed_database[[
        'last_watered', 'plant_id']].values.tolist()

    assert mock_executemany.called_with("""INSERT INTO water_history
                    (time_watered, plant_id)
                    VALUES
                    (%s, %s)
                    ON CONFLICT DO NOTHING;
                    """, mock_watering_info)


def test_insert_into_reading_information_table(mock_transformed_database):
    """
    Test `insert_into_reading_information_table` calls with correct statement functions
    """
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value

    insert_into_reading_information_table(
        mock_connection, mock_transformed_database)

    mock_executemany = mock_cursor.executemany

    mock_reading_info = mock_transformed_database[['plant_id', 'recording_time', 'botanist_name',
                                                   'temperature', 'soil_moisture', 'sun_condition',
                                                   'shade_condition']].values.tolist()

    assert mock_executemany.called_with("""INSERT INTO reading_information
                    (plant_id, plant_reading_time, botanist_id,
                    temperature, soil_moisture, 
                    sun_condition_id, shade_condition_id)
                    VALUES
                    (%s, %s, 
                    (SELECT botanist_id FROM botanist WHERE botanist_name = %s),
                    %s, %s,
                    (SELECT sun_condition_id FROM sun_condition WHERE sun_condition_type = %s), 
                    (SELECT shade_condition_id FROM shade_condition WHERE shade_condition_type = %s))
                    ON CONFLICT DO NOTHING;
                    """, mock_reading_info)
