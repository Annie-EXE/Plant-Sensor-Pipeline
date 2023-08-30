"""File that handles loading data into the postgres database"""

from os import environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection

import pandas as pd
from pandas import DataFrame


def get_db_connection(config: dict) -> connection:
    """Returns connection to the database"""

    return connect(user=config["DB_USER"],
                   password=config["DB_PASSWORD"],
                   dbname=config["DB_NAME"],
                   host=config["DB_HOST"],
                   port=config["DB_PORT"])


def insert_into_plant_origin_table(conn: connection, data: DataFrame) -> None:
    """Inserts information into plant_origin table"""

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
    """Inserts information into plant table"""

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
    """Inserts information into botanist table"""

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
    """Inserts information into water_history table"""

    watering_info = data[['last_watered', 'plant_id']].values.tolist()

    with conn.cursor() as cur:

        cur.executemany("""INSERT INTO water_history
                    (time_watered, plant_id)
                    VALUES
                    (%s, %s)
                    ON CONFLICT DO NOTHING;
                    """, watering_info)

    conn.commit()


# TODO: grab sunlight id
def insert_into_reading_information_table(conn: connection, data: DataFrame) -> None:
    """Inserts information into reading_information table"""

    reading_info = data[['plant_id', 'recording_time', 'botanist_name',
                         'temperature', 'soil_moisture', 'conditions']].values.tolist()

    with conn.cursor() as cur:

        cur.executemany("""INSERT INTO reading_information
                    (plant_id, plant_reading_time, botanist_id,
                    temperature, soil_moisture, conditions)
                    VALUES
                    (%s, %s, 
                    (SELECT botanist_id FROM botanist WHERE botanist_name = %s),
                    %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """, reading_info)

    conn.commit()


# def insert_into_shade_condition_table(conn: connection, data: DataFrame) -> None:

#     all_conditions_values = [value.lower() for sublist in data['conditions']
#                              if sublist is not None for value in sublist]
    
#     with conn.cursor() as cur:

#         cur.executemany("""INSERT INTO condition
#                         (condition_type)
#                         VALUES (%s)
#                         ON CONFLICT DO NOTHING;""",
#                         all_conditions_values)


# def insert_into_shade_condition_table(conn: connection, data: DataFrame) -> None:

#     all_conditions_values = [value.lower() for sublist in data['conditions']
#                              if sublist is not None for value in sublist]
    
#     with conn.cursor() as cur:

#         cur.executemany("""INSERT INTO condition
#                         (condition_type)
#                         VALUES (%s)
#                         ON CONFLICT DO NOTHING;""",
#                         all_conditions_values)


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
