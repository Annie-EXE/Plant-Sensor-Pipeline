"""File that handles loading data into the postgres database"""

from os import environ

from dotenv import load_dotenv
from psycopg2 import connect, connection


def get_db_connection() -> connection:
    """Returns connection to the database"""

    load_dotenv()

    config = environ()

    return connect(dbname=config["db_name"],
                   user=config["db_user"],
                   password=config["db_password"],
                   host=config["db_host"],
                   port=config["db_port"])


if __name__ == "__main__":
    pass
