"""Pipeline Script: Extracting pipeline data from the API endpoint"""

import json
from os import environ
from dotenv import load_dotenv
import requests


def get_plant_data_from_api(plant_id: int, api_path: str) -> dict:
    """
    Retrieves the data for a given
    plant and stores it as a dict
    """
    response = requests.get(f"{api_path}/plants/{plant_id}")
    data = response.json()

    return data


def process_plant_data_from_api(plant_data: dict) -> dict:
    """
    Process API data and extract relevant information into a new dict
    """
    origin_location = plant_data.get("origin_location", [])

    plant_data_dict = {
        "plant_id": plant_data.get("plant_id"),
        "name": plant_data.get("name"),
        "scientific_name": plant_data.get("scientific_name"),
        "cycle": plant_data.get("cycle"),
        "last_watered": plant_data.get("last_watered"),
        "recording_time": plant_data.get("recording_taken"),
        "temperature": plant_data.get("temperature"),
        "soil_moisture": plant_data.get("soil_moisture"),
        "sunlight_details": plant_data.get("sunlight"),
        "origin_location": {
            "origin_latitude": origin_location[0] if len(origin_location) > 0 else None,
            "origin_longitude": origin_location[1] if len(origin_location) > 1 else None,
            "origin_country": origin_location[-1] if len(origin_location) > 2 else None
        },
        "botanist_details":  plant_data.get("botanist", {})
    }

    return plant_data_dict


def get_all_plants_data(api_path: str) -> list[dict]:
    """
    Extracts the data for all 50
    plants, into a list of dicts
    """
    all_plants_data = []

    for i in range(51):
        raw_plant_data = get_plant_data_from_api(i, api_path)
        processed_plant_data = process_plant_data_from_api(raw_plant_data)
        all_plants_data.append(processed_plant_data)

    return all_plants_data


def clean_unicode_from_plant_data(plants_data: list[dict]) -> list[dict]:
    """
    Remove unicode characters which appear in the plant `name` data
    """
    for plant in plants_data:

        if plant["name"]:

            plant["name"] = plant["name"].replace(
                u"\u2018", "'").replace(u"\u2019", "'")

    return plants_data


def create_json_file(data: list[dict], file_path: str) -> str:
    """
    Creates a .json file and 
    uploads data to it
    """
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    return "Data processed!"


if __name__ == "__main__":

    load_dotenv()

    api_path = environ.get("API_PATH")

    plant_data_file_path = "recent_plant_data.json"

    all_plants_data = get_all_plants_data(api_path)

    cleaned_plants_data = clean_unicode_from_plant_data(all_plants_data)

    create_json_file(all_plants_data, plant_data_file_path)
