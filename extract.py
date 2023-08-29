"""Pipeline Script: Extracting pipeline data from the API endpoint"""

import requests

def get_plant_data(plant_id: int) -> dict:
    """
    Retrieves the data for a given
    plant and stores it as a dict
    """
    response = requests.get(f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}")
    plant_data = response.json()

    plant_data_id = plant_data["plant_id"]
    name = plant_data["name"] # string
    scientific_name = plant_data["scientific_name"] # list of strings
    cycle = plant_data["cycle"] # string
    last_watered = plant_data["last_watered"] # string

    recording_time = plant_data["recording_taken"] # string

    origin_latitude = plant_data["origin_location"][0] # string
    origin_longitude = plant_data["origin_location"][1] # string
    origin_country = plant_data["origin_location"][-1] # string

    botanist_details = plant_data["botanist"] # dict
    


get_plant_data(8)