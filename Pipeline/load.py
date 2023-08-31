"""File that handles loading data into the postgres database"""

from os import environ, _Environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection

import pandas as pd
from pandas import DataFrame


def get_db_connection(config: _Environ) -> connection:
    """
    Returns connection to the database

    Args:
        config (_Environ): A file containing sensitive values

    Returns:
        connection: A connection to a Postgres database
    """

    return connect(dbname='practice',
                   #    dbname=config["DB_NAME"],
                   user=config["DB_USER"],
                   password=config["DB_PASSWORD"],
                   #    dbname=config["DB_NAME"],
                   host=config["DB_HOST"],
                   port=config["DB_PORT"])


def insert_into_plant_origin_table(conn: connection, data: DataFrame) -> None:
    """
    Inserts information into plant_origin table

    Args:
        conn (connection): A connection to a Postgres database

        data (DataFrame): A DataFrame containing transformed data for all plants

    Returns:
        None
    """

    origin_info = data[['plant_latitude', 'plant_longitude',
                        'plant_location']].values.tolist()

    with conn.cursor() as cur:

        cur.executemany("""INSERT INTO plant_origin
                    (latitude, longitude, country)
                    VALUES
                    (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """, origin_info)

    conn.commit()


def insert_into_plant_table(conn: connection, data: DataFrame) -> None:
    """
    Inserts information into plant table

    Args:
        conn (connection): A connection to a Postgres database

        data (DataFrame): A DataFrame containing transformed data for all plants

    Returns:
        None
    """

    plant_info = data[['plant_id', 'plant_name', 'scientific_name',
                       'plant_latitude', 'plant_longitude']].values.tolist()

    with conn.cursor() as cur:

        cur.executemany("""INSERT INTO plant
                    (plant_id,
                    plant_name,
                    plant_scientific_name,
                    plant_origin_id)
                    VALUES
                    (%s, %s, %s,
                        (SELECT plant_origin_id FROM plant_origin 
                        WHERE latitude = %s and longitude = %s))
                    ON CONFLICT DO NOTHING;
                    """, plant_info)

    conn.commit()


def insert_into_botanist_table(conn: connection, data: DataFrame) -> None:
    """
    Inserts information into botanist table

    Args:
        conn (connection): A connection to a Postgres database

        data (DataFrame): A DataFrame containing transformed data for all plants

    Returns:
        None
    """

    botanist_info = data[['botanist_name', 'botanist_email',
                          'botanist_phone_number']].values.tolist()

    with conn.cursor() as cur:

        cur.executemany("""INSERT INTO botanist
                    (botanist_name, botanist_email, botanist_phone_number)
                    VALUES
                    (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """, botanist_info)

    conn.commit()


def insert_into_water_history_table(conn: connection, data: DataFrame) -> None:
    """
    Inserts information into water_history table

    Args:
        conn (connection): A connection to a Postgres database

        data (DataFrame): A DataFrame containing transformed data for all plants

    Returns:
        None
    """

    watering_info = data[['last_watered', 'plant_id']].values.tolist()

    with conn.cursor() as cur:

        cur.executemany("""INSERT INTO water_history
                    (time_watered, plant_id)
                    VALUES
                    (%s, %s)
                    ON CONFLICT DO NOTHING;
                    """, watering_info)

    conn.commit()


def insert_into_reading_information_table(conn: connection, data: DataFrame) -> None:
    """
    Inserts information into reading_information table

    Args:
        conn (connection): A connection to a Postgres database

        data (DataFrame): A DataFrame containing transformed data for all plants

    Returns:
        None
    """

    reading_info = data[['plant_id', 'recording_time', 'botanist_name',
                         'temperature', 'soil_moisture', 'sun_condition',
                         'shade_condition']].values.tolist()

    with conn.cursor() as cur:

        print(reading_info)

        cur.executemany("""INSERT INTO reading_information
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
                    """, reading_info)

    conn.commit()


if __name__ == "__main__":

    load_dotenv()

    config = environ

    conn = get_db_connection(config)

    data = pd.read_csv('transformed_plant_data.csv')

    insert_into_plant_origin_table(conn, data)

    insert_into_plant_table(conn, data)

    insert_into_botanist_table(conn, data)

    insert_into_water_history_table(conn, data)

    insert_into_reading_information_table(conn, data)

    conn.close()
