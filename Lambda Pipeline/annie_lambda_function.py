import json
from os import environ
from dotenv import load_dotenv
import requests
from datetime import datetime
import pandas as pd
from pandas import DataFrame
import numpy as np
import re
from psycopg2 import connect
from psycopg2.extensions import connection

from extract import (
    get_plant_data_from_api,
    process_plant_data_from_api,
    get_all_plants_data,
    clean_unicode_from_plant_data,
    create_json_file
)

from transform import (
    load_data,
    check_duplicates,
    get_conditions_sun,
    get_conditions_shade,
    flatten_data,
    transform_email_column_using_regex,
    normalize_phone_number,
    transform_phone_column_using_regex,
    get_scientific_name,
    transform_scientific_name_column,
    get_last_watered_date_time,
    transform_last_watered_column,
    get_recording_taken_date_time,
    transform_recording_taken_column,
    get_latitude,
    get_longitude,
    get_location,
    build_location_columns,
    get_valid_temperature,
    transform_temperature_column,
    normalize_text_in_list,
    normalize_column_text,
    build_plant_dataframe
)

from load import (
    get_db_connection,
    insert_into_plant_origin_table,
    insert_into_plant_table,
    insert_into_botanist_table,
    insert_into_water_history_table,
    insert_into_reading_information_table
)


def lambda_handler(event, context) -> dict:
    """
    This section of code is the 'Lambda function',
    to be used by AWS Lambda to execute the 
    data processing pipeline
    """

    load_dotenv()

    api_path = environ.get("API_PATH")

    all_plants_data = get_all_plants_data(api_path)

    unicode_free_plants_data = clean_unicode_from_plant_data(all_plants_data)

    flatted_plant_data = flatten_data(unicode_free_plants_data)

    plant_df = build_plant_dataframe(flatted_plant_data)

    plant_df = plant_df.dropna(subset=['last_watered', 'recording_time'])

    config = environ

    conn = get_db_connection(config)

    insert_into_plant_origin_table(conn, plant_df)

    insert_into_plant_table(conn, plant_df)

    insert_into_botanist_table(conn, plant_df)

    insert_into_water_history_table(conn, plant_df)

    insert_into_reading_information_table(conn, plant_df)

    conn.close()

    return {
        'statusCode': 200,
        'body': 'Data uploaded to database successfully'
    }
