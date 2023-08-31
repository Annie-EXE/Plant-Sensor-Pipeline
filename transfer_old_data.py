"""Transfers old data from the short term db to the long term db"""

from os import environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection, cursor


def get_db_connection_lt(config: dict) -> connection:
    """Returns connection to long term database"""

    return connect(dbname=config["DB_NAME"],
                   user=config["DB_USER"],
                   password=config["DB_PASSWORD"],
                   host=config["DB_HOST"],
                   port=config["DB_PORT"])


def commit_and_close_cursor(conn: connection, cur: cursor) -> None:
    """Commits changes and closes cursor"""

    conn.commit()

    cur.close()


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

    commit_and_close_cursor(conn, cur)


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

    commit_and_close_cursor(conn, cur)


def transfer_reading_information_table(conn: connection) -> None:
    """
    Transfers data in reading_information from short_term to long_term schema
    Will only transfer data that does not already exist in the long_term schema
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.reading_information
                    (plant_id, plant_reading_time, botanist_id, soil_moisture, sun_condition_id, shade_condition_id, temperature)
                    SELECT plant_id, plant_reading_time, botanist_id, soil_moisture, sun_condition_id, shade_condition_id, temperature 
                    FROM reading_information
                    WHERE NOT EXISTS
                    (SELECT plant_id, plant_reading_time, botanist_id, soil_moisture, sun_condition_id, shade_condition_id, temperature
                    FROM long_term.reading_information 
                    WHERE long_term.reading_information.plant_reading_time = reading_information.plant_reading_time);""")

    commit_and_close_cursor(conn, cur)


def delete_data_from_over_24_hours_reading_information_table(conn: connection) -> None:
    """Deletes all data from reading_information that is older than 24 hours"""

    cur = conn.cursor()

    cur.execute("""DELETE from reading_information
                WHERE 
                plant_reading_time < now() - interval '24 hours';""")

    commit_and_close_cursor(conn, cur)


def delete_data_from_over_24_hours_water_history_table(conn: connection) -> None:
    """Deletes all data from water_history that is older than 24 hours"""

    cur = conn.cursor()

    cur.execute("""DELETE from water_history
                WHERE 
                time_watered < now() - interval '24 hours';""")

    commit_and_close_cursor(conn, cur)


def transfer_shade_condition_table(conn: connection) -> None:
    """
    Transfers data in shade_condition from short_term to long_term schema
    Will only transfer data that does not already exist in the long_term schema
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.shade_condition
                    (shade_condition_type)
                    SELECT shade_condition_type 
                    FROM shade_condition
                    WHERE NOT EXISTS
                    (SELECT shade_condition_type
                    FROM long_term.shade_condition 
                    WHERE long_term.shade_condition.shade_condition_type = shade_condition.shade_condition_type);""")

    commit_and_close_cursor(conn, cur)


def transfer_sun_condition_table(conn: connection) -> None:
    """
    Transfers data in sun_condition from short_term to long_term schema
    Will only transfer data that does not already exist in the long_term schema
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.sun_condition
                    (sun_condition_type)
                    SELECT sun_condition_type 
                    FROM sun_condition
                    WHERE NOT EXISTS
                    (SELECT sun_condition_type
                    FROM long_term.sun_condition 
                    WHERE long_term.sun_condition.sun_condition_type = sun_condition.sun_condition_type);""")

    data = cur.fetchall()

    print(data)


def transfer_plant_origin_table(conn: connection) -> None:
    """
    Transfers data in plant_origin from short_term to long_term schema
    Will only transfer data that does not already exist in the long_term schema
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.plant_origin
                    (latitude, longitude, country)
                    SELECT latitude, longitude, country 
                    FROM plant_origin
                    WHERE NOT EXISTS
                    (SELECT latitude, longitude, country
                    FROM long_term.plant_origin 
                    WHERE long_term.plant_origin.latitude = plant_origin.latitude
                    AND long_term.plant_origin.longitude = plant_origin.longitude
                    AND long_term.plant_origin.country = plant_origin.country);""")

    commit_and_close_cursor(conn, cur)


if __name__ == "__main__":

    pass
