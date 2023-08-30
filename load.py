"""File that handles loading data into the postgres database"""

from os import environ

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection


def get_db_connection(config: dict) -> connection:
    """Returns connection to the database"""

    return connect(user=config["DB_USER"],
                   password=config["DB_PASSWORD"],
                #    dbname=config["DB_NAME"],
                   host=config["DB_HOST"],
                   port=config["DB_PORT"])


# TODO Typehint for data?
def insert_into_plant_table(conn: connection, data) -> None:
    """Inserts information into plant table"""

    cur = conn.cursor()

    cur.execute("""INSERT INTO plant
                (plant_name,
                plant_scientific_name,
                plant_origin,
                water_history_id)
                Values
                (%s, %s, %s, %s);
                """([data]))

    cur.commit()


def insert_into_plant_origin_table(conn: connection, data) -> None:
    """Inserts information into plant_origin table"""

    cur = conn.cursor()

    cur.execute("""INSERT INTO plant_origin
                (latitude, longitude, country)
                Values
                (%s, %s, %s);
                """([data]))

    cur.commit()


def insert_into_botanist_table(conn: connection, data) -> None:
    """Inserts information into botanist table"""

    cur = conn.cursor()

    cur.execute("""INSERT INTO botanist
                (botanist_name, botanist_email, botanist_phone_number)
                Values
                (%s, %s, %s);
                """([data]))

    cur.commit()


def insert_into_water_history_table(conn: connection, data) -> None:
    """Inserts information into water_history table"""

    cur = conn.cursor()

    cur.execute("""INSERT INTO water_history
                (water_history_id, time_watered, plant_id)
                Values
                (%s, %s, %s);
                """([data]))

    cur.commit()


def insert_into_reading_information_table(conn: connection, data) -> None:
    """Inserts information into reading_information table"""

    cur = conn.cursor()

    cur.execute("""INSERT INTO reading_information
                (plant_id, plant_reading_time, botanist_id,
                temperature, soil_moisture, sunlight_id)
                Values
                (%s, %s, %s, %s, %s, %s);
                """([data]))

    cur.commit()


if __name__ == "__main__":

    load_dotenv()

    config = environ

    get_db_connection(config)
