"""Pipeline Script: Extracting pipeline data from the API endpoint"""

import requests

def get_plant_data(plant_id: int, api_path: str) -> dict:
    """
    Retrieves the data for a given
    plant and stores it as a dict
    """
    response = requests.get(f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}")
    plant_data = response.json()

    plant_data_id = plant_data.get("plant_id")
    name = plant_data.get("name") # string
    scientific_name = plant_data.get("scientific_name") # list of strings
    cycle = plant_data.get("cycle") # string
    last_watered = plant_data.get("last_watered") # string

    recording_time = plant_data.get("recording_taken") # string
    temperature = plant_data.get("temperature") # float
    soil_moisture = plant_data.get("soil_moisture") # float
    sunlight_details = plant_data.get("sunlight") # list of strings

    origin_location = plant_data.get("origin_location", []) # list with latitude, longitude, and country
    origin_latitude = origin_location[0] if len(origin_location) > 0 else None
    origin_longitude = origin_location[1] if len(origin_location) > 1 else None
    origin_country = origin_location[-1] if len(origin_location) > 2 else None

    botanist_details = plant_data.get("botanist", {}) # dict
    
    plant_data_dict = {
        "plant_id": plant_data_id,
        "name": name,
        "scientific_name": scientific_name,
        "cycle": cycle,
        "last_watered": last_watered,
        "recording_time": recording_time,
        "temperature": temperature,
        "soil_moisture": soil_moisture,
        "sunlight_details": sunlight_details,
        "origin_location": {
            "origin_latitude": origin_latitude,
            "origin_longitude": origin_longitude,
            "origin_country": origin_country
        },
        "botanist_details": botanist_details
    }

    return plant_data_dict


def get_all_plants_data()