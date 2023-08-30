"""Pipeline Script: Main pipeline for running ETL scripts"""

from os import environ
from dotenv import load_dotenv


from extract import (
    get_all_plants_data,
    clean_unicode_from_plant_data,
    create_json_file
)

from transform import (
    load_data,
    flatten_data,
    build_plant_dataframe
)

if __name__ == "__main__":

    load_dotenv()

    api_path = environ.get("API_PATH")

    plant_data_file_path = "recent_plant_data.json"

    all_plants_data = get_all_plants_data(api_path)

    cleaned_plants_data = clean_unicode_from_plant_data(all_plants_data)

    create_json_file(all_plants_data, plant_data_file_path)

    loaded_data_from_file = load_data(plant_data_file_path)

    flatted_plant_data = flatten_data(loaded_data_from_file)

    plant_df = build_plant_dataframe(flatted_plant_data)

    print(plant_df)
