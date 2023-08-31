"""Transfers old data from the short term db to the long term db"""

from os import environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection


def get_db_connection_lt(config: dict) -> connection:
    """Returns connection to long term database"""

    return connect(dbname=config["DB_NAME"],
                   user=config["DB_USER"],
                   password=config["DB_PASSWORD"],
                   host=config["DB_HOST"],
                   port=config["DB_PORT"])


# TODO Delete data or not??
def transfer_botanist_table(conn: connection) -> None:
    """
    Transfers data in botanist from short_term to long_term schema
    Will only transfer data that does not exist already in the long term
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.botanist
                    SELECT * FROM botanist AS stb
                    WHERE NOT EXISTS
                    (SELECT * FROM long_term.botanist
                    WHERE long_term.botanist.botanist_phone_number = stb.botanist_phone_number);""")

    cur.commit()


# TODO Delete data or not??
def transfer_plant_table(conn: connection) -> None:
    """
    Transfers data in plant from the short_term schema to the long_term schema
    Will only transfer for plant entries that do not already exist in both tables
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.plant
                    SELECT * FROM plant AS stp
                    WHERE NOT EXISTS
                    (SELECT * FROM long_term.plant 
                     WHERE long_term.plant.plant_name = stp.plant_name);""")

    cur.commit()


# TODO Select and delete data in the past hour
def transfer_water_history_table(conn: connection) -> None:
    """
    Transfers data in water_history from the short_term schema to the long_term schema
    Will only transfer for plant entries that do not already exist in both tables
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.water_history (time_watered, plant_id)
                    SELECT time_watered, plant_id FROM water_history
                    WHERE NOT EXISTS
                    (SELECT time_watered, plant_id FROM long_term.water_history 
                     WHERE long_term.water_history.time_watered = water_history.time_watered);""")

    cur.commit()


# TODO Select and delete data in the past hour??
def transfer_reading_information_table(conn: connection) -> None:
    """
    Transfers data in reading_information from short_term to long_term schema
    Will only transfer data that does not already exist in the long_term schema
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.reading_information
                    (plant_id, plant_reading_time, botanist_id, soil_moisture, conditions, temperature)
                    SELECT plant_id, plant_reading_time, botanist_id, soil_moisture, conditions, temperature 
                    FROM reading_information
                    WHERE NOT EXISTS
                    (SELECT plant_id, plant_reading_time, botanist_id, soil_moisture, conditions, temperature
                    FROM long_term.reading_information 
                    WHERE long_term.reading_information.plant_reading_time = reading_information.plant_reading_time);""")

    data = cur.fetchall()

    print(data)


# TODO COMPLETE
def merge_plant_origin_table(conn: connection) -> None:
    """
    Transfers data in plant_origin from short_term to long_term schema
    Will only transfer data that does not already exist in the long_term schema
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.plant_origin
                    CASE 
                    WHEN latitude IS NaN THEN null
                    WHEN longitude IS NAN THEN null
                    SELECT * FROM plant_origin AS stpo
                    WHERE NOT EXISTS
                    (SELECT * FROM long_term.plant_origin 
                    WHERE long_term.plant_origin.plant_origin_id = plant_origin.plant_origin_id);""")

    data = cur.fetchall()

    print(data)


if __name__ == "__main__":

    load_dotenv()

    config = environ

    conn = get_db_connection_lt(config)

    # merge_readings_table(conn)
    merge_plant_origin_table(conn)

    conn.close()
