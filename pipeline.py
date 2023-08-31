"""Pipeline Script: Main pipeline for running ETL scripts"""

from os import environ
from dotenv import load_dotenv


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
    insert_into_reading_information_table
)

if __name__ == "__main__":

    load_dotenv()

    config = environ

    api_path = environ.get("API_PATH")


    all_plants_data = get_all_plants_data(api_path)

    cleaned_plants_data = clean_unicode_from_plant_data(all_plants_data)

    flatted_plant_data = flatten_data(cleaned_plants_data)

    plant_df = build_plant_dataframe(flatted_plant_data)

    conn = get_db_connection(config)

    insert_into_plant_origin_table(conn, plant_df)

    insert_into_plant_table(conn, plant_df)

    insert_into_botanist_table(conn, plant_df)

    insert_into_water_history_table(conn, plant_df)

    insert_into_reading_information_table(conn, plant_df)

    conn.close()
