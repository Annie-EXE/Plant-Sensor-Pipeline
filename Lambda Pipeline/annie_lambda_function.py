import json
from os import environ
from dotenv import load_dotenv
import requests


from extract import (
    get_plant_data_from_api,
    process_plant_data_from_api,
    get_all_plants_data,
    clean_unicode_from_plant_data,
    create_json_file
)

