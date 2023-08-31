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


def merge_botanist_table(conn: connection) -> None:
    """Merges the botanist table from the short_term schema to the long_term schema"""

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.botanist
                    SELECT * FROM botanist AS stb
                    WHERE NOT EXISTS
                    (SELECT * FROM long_term.botanist
                     WHERE long_term.botanist.botanist_id = botanist.botanist_id);""")
    cur.commit()


def merge_plant_table(conn: connection) -> None:
    """
    Merges the plant table from the short_term schema to the long_term schema
    Will only merge for plant entries that do not already exist in both tables
    """

    cur = conn.cursor()

    cur.execute(f"""INSERT INTO long_term.plant AS ltp
                    SELECT * FROM plant AS stp
                    WHERE NOT EXISTS
                    (SELECT * FROM long_term.plant 
                     WHERE long_term.plant.plant_name = stp.plant_name);""")

    cur.commit()


def merge_readings_table(conn: connection) -> None:
    """Merges the readings table from the short_term schema to the long_term schema"""

    cur = conn.cursor()

    cur.execute(f"""SELECT * FROM reading_information""")

    data = cur.fetchall()

    print(data)


def merge_plant_origin_table(conn: connection) -> None:
    """Merges the plant origin from the short_term schema to the long_term schema"""

    cur = conn.cursor()

    cur.execute(f"""SELECT * FROM plant_origin;""")

    data = cur.fetchall()

    print(data)


if __name__ == "__main__":

    load_dotenv()

    config = environ

    conn = get_db_connection_lt(config)

    # merge_readings_table(conn)
    merge_plant_origin_table(conn)

    conn.close()
