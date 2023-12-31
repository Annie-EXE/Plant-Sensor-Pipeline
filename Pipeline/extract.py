"""Pipeline Script: Extracting pipeline data from the API endpoint"""

import json
from os import environ
from dotenv import load_dotenv
import requests


def get_plant_data_from_api(plant_id: int, api_path: str) -> dict:
    """
    Retrieves the data for a given plant and stores it as a dict

    Args:
        plant_id (int): A number representing the id value of the plant for which
        data will be accessed.

        api_path (str): A string containing the api path

    Returns:
        dict: A python dictionary containing retrieved data from the API
    """
    response = requests.get(f"{api_path}/plants/{plant_id}")
    data = response.json()

    return data


def process_plant_data_from_api(plant_data: dict) -> dict:
    """
    Process API data and extract relevant information into a new dict

    Args:
        plant_data (dict): Raw JSON response data from the API 

    Results: 
        dict: A python dictionary containing relevant data from the API
    """
    if 'error' not in plant_data:

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
    Extracts the data for all plants, into a list of dicts

    Args:
        api_path (str): A string containing the api path

    Returns:
        list[dict]: A Python list containing all data from API for each plant
    """
    all_plants_data = []

    for i in range(51):
        raw_plant_data = get_plant_data_from_api(i, api_path)
        processed_plant_data = process_plant_data_from_api(raw_plant_data)
        if processed_plant_data:
            all_plants_data.append(processed_plant_data)

    return all_plants_data


def clean_unicode_from_plant_data(plants_data: list[dict]) -> list[dict]:
    """
    Remove unicode characters which appear in the plant `name` data

    Args:
        plants_data (list[dict]): A list containing dictionaries of processed plant data
        with uncleaned name data

    Returns:
        list[dict]: A list containing dictionaries of processed plant data
        with unicode removed from `name` data
    """
    for plant in plants_data:

        if plant["name"]:

            plant["name"] = plant["name"].replace(
                u"\u2018", "").replace(u"\u2019", "")

    return plants_data


def create_json_file(data: list[dict], file_path: str) -> str:
    """
    Creates a .json file and uploads data to it

    Args:
        data (list[dict]): A list containing dictionaries of processed plant data
        with unicode removed from `name` data

        file_path (str): A string assigned as a file name

    Results:
        str: A string to show successful writing of data
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
