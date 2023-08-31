import json
from os import environ
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame
import numpy as np
import re
from psycopg2 import connect
from psycopg2.extensions import connection

from extract import (
    get_all_plants_data,
    clean_unicode_from_plant_data,
)

from transform import (
    flatten_data,
    build_plant_dataframe
)

from load import (
    get_db_connection,
    insert_into_plant_origin_table,
    insert_into_plant_table,
    insert_into_botanist_table,
    insert_into_water_history_table,
    insert_into_reading_information_table,
    delete_old_rows
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

    delete_old_rows(conn)

    conn.close()

    return {
        'statusCode': 200,
        'body': 'Data uploaded to database successfully'
    }


lambda_handler(None, None)
