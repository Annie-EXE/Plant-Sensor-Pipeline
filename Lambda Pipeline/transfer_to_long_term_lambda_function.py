"""Lambda function file to transfer data from short term to long term schema"""

from os import environ

from dotenv import load_dotenv

from transfer_old_data import (get_db_connection,
                               transfer_botanist_table,
                               transfer_sun_condition_table,
                               transfer_shade_condition_table,
                               transfer_water_history_table,
                               transfer_plant_origin_table,
                               transfer_reading_information_table,
                               transfer_plant_table)


def lambda_handler(event=None, function=None):
    """Lambda function that transfers data from short term to long term schema"""

    load_dotenv()

    config = environ

    try:
        conn = get_db_connection(config)
    except (ConnectionError, ConnectionAbortedError, ConnectionAbortedError) as err:
        err("Error: Unable to establish connection with the database1")

    try:
        transfer_sun_condition_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'sun_condition' table is of incorrect value or type!")

    try:
        transfer_shade_condition_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'shade_condition' table is of incorrect value or type!")

    try:
        transfer_botanist_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'botanist' table is of incorrect value or type!")

    try:
        transfer_plant_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'plant' table is of incorrect value or type!")

    try:
        transfer_plant_origin_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'plant_origin' table is of incorrect value or type!")

    try:
        transfer_water_history_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'water_history' table is of incorrect value or type!")

    try:
        transfer_reading_information_table(conn)
    except (ValueError, TypeError) as err:
        err("Error: Information in 'reading_information' table is of incorrect value or type!")
