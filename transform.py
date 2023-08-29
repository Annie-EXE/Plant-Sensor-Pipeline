"""Pipeline Script: Transforming pipeline data"""


import json
import pandas as pd


def load_data(json_path: str) -> list[dict]:
    """
    Load JSON data from a file or JSON-formatted string.

    Args:
        json_data (str): Either a JSON-formatted string or a path to a JSON file.

    Returns:
        list[dict]: A Python list of dictionaries containing the parsed JSON data.
    """
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError) as e:
        print(f"Error loading JSON data: {e}")
        return None


def flatten_data(loaded_plant_data: list[dict]) -> list[dict]:
    """
    Build a flattened dictionary from extracted a Python list of dictionaries containing the parsed JSON data.

    Args:
        loaded_json_data: (list[dict]): A Python list of dictionaries containing the parsed JSON data.

    Returns:
        list[dict]: A Python list of dictionaries containing the parsed JSON data without nested dictionaries.
    """
    flattened_data = []
    for data in loaded_plant_data:
        plant = {}
        plant["botanist_name"] = data["botanist"]["name"]
        plant["botanist_email"] = data["botanist"]["email"]
        plant["botanist_phone_number"] = data["botanist"]["phone"]
        plant["plant_id"] = data["plant_id"]
        plant["scientific_name"] = data["scientific_name"]
        plant["plant_name"] = data["name"]
        plant["plant_cycle"] = data["cycle"]
        plant["last_watered"] = data["last_watered"]
        plant["plant_origin"] = data["origin_location"]
        plant["recording_taken"] = data["recording_taken"]
        plant["soil_moisture"] = data["soil_moisture"]
        plant["conditions"] = data["sunlight"]
        plant["temperature"] = data["temperature"]

        flattened_data.append(plant)

    return flattened_data


def built_plant_dataframe(plant_data: list[dict]):
    """
    Build a DataFrame from a a list of dictionaries.

    Args:
        plant_data (list[dict])
    """
    df = pd.DataFrame(plant_data)


if __name__ == "__main__":
    json_file_path = 'mock_transform_data.json'

    loaded_data_from_file = load_data(json_file_path)

    flatted_plant_data = flatten_data(loaded_data_from_file)
    print(flatted_plant_data)
