"""Pipeline Script: Transforming pipeline data"""

from datetime import datetime
import json
import pandas as pd
from pandas import DataFrame


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
        plant["botanist_name"] = data.get("botanist_details").get("name")
        plant["botanist_email"] = data.get("botanist_details").get("email")
        plant["botanist_phone_number"] = data.get(
            "botanist_details").get("phone")
        plant["plant_id"] = data.get("plant_id")
        plant["scientific_name"] = data.get("scientific_name")
        plant["plant_name"] = data.get("name")
        plant["plant_cycle"] = data.get("cycle")
        plant["last_watered"] = data.get("last_watered")
        plant["plant_origin"] = data.get("origin_location")
        plant["recording_time"] = data.get("recording_time")
        plant["soil_moisture"] = data.get("soil_moisture")
        plant["conditions"] = data.get("sunlight_details")
        plant["temperature"] = data.get("temperature")

        flattened_data.append(plant)

    return flattened_data


def transform_email_column_using_regex(df: DataFrame) -> DataFrame:
    """
    Extract email from affiliation column and add to existing 'botanist_email' column.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data

    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """
    try:
        email_pattern = r"([\w.-]+@[\w.-]+)"
        df["botanist_email"] = df["botanist_email"].str.extract(
            email_pattern)
        df["botanist_email"] = df["botanist_email"].fillna("N/A")
        return df
    except:
        "N/A"


def transform_phone_column_using_regex(df: DataFrame) -> DataFrame:
    """
    Extract phone number from "botanist_phone_number" column and add to existing column.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """
    try:
        email_pattern = r"(\+[\d-]+)"
        df["botanist_phone_number"] = df["botanist_phone_number"].str.extract(
            email_pattern)
        df["botanist_phone_number"] = df["botanist_phone_number"].fillna("N/A")
        return df
    except:
        "N/A"


def get_scientific_name(scientific_name: list[str]) -> str:
    """
    Extract scientific names from a list and normalize into a string

    Args:
        scientific_name (list[str]): A list containing strings related to the scientific name of a plant

    Returns:
        str: A string containing one of more of the scientific names for a plant
    """
    try:
        if len(scientific_name) == 1:
            return scientific_name[0]
        else:
            return ", ".join(scientific_name)
    except:
        return "N/A"


def transform_scientific_name_column(df: DataFrame) -> DataFrame:
    """
    Extract scientific name from "scientific_name" column and add to existing column.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """
    df["scientific_name"] = df.apply(
        lambda row: get_scientific_name(row["scientific_name"]), axis=1)
    return df


def get_last_watered_date_time(datetime_string: str) -> datetime | str:
    """
    Convert date string from "last_watered" column to a datetime object

    Args: 
        datetime_string (str): A string containing date time information
    Returns:
        datetime: A date time object
    """
    try:
        date_object = datetime.strptime(
            datetime_string, "%a, %d %b %Y %H:%M:%S %Z")
        return date_object
    except:
        return "N/A"


def transform_last_watered_column(df: DataFrame) -> DataFrame:
    """
    Extract date string from "last_watered" column and add to existing column
    in date time corrected format.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """

    df["last_watered"] = df.apply(
        lambda row: get_last_watered_date_time(row["last_watered"]), axis=1)

    return df


def get_recording_taken_date_time(datetime_string: str) -> datetime | str:
    """
    Convert date string from "recording_taken" column to a datetime object

    Args: 
        datetime_string (str): A string containing date time information
    Returns:
        datetime: A date time object relating to when the recording was taken
    """
    try:
        date_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        return date_object
    except:
        return "N/A"


def transform_recording_taken_column(df: DataFrame) -> DataFrame:
    """
    Extract date string from "recording_taken" column and add to existing column
    in date time corrected format.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """

    df["recording_time"] = df.apply(
        lambda row: get_recording_taken_date_time(row["recording_time"]), axis=1)
    return df


def get_latitude(origin_string: list[str]) -> float | str:
    """
    Return information related to the latitude of the plant

    Args:
        origin_string (list[str]): A list containing information related to the latitude,
        longitude and country of origin for the plant

    Returns:
        float: A float relating to the latitude of the plant 

    """
    try:
        return origin_string[0]
    except Exception as e:
        print(f"Error retrieving latitude: {e}")
        return "N/A"


def get_longitude(origin_string: list[str]) -> float | str:
    """
    Return information related to the longitude of the plant

    Args:
        origin_string (list[str]): A list containing information related to the latitude,
        longitude and country of origin for the plant

    Returns:
        float: A float relating to the longitude of the plant 

    """
    try:
        return origin_string[1]
    except Exception as e:
        print(f"Error retrieving longitude: {e}")
        return "N/A"


def get_location(origin_string: list[str]) -> str:
    """
    Return information related to the location of the plant

    Args:
        origin_string (list[str]): A list containing information related to the latitude,
        longitude and country of origin for the plant

    Returns:
        float: A float relating to the location of the plant 

    """
    try:
        return ", ".join(origin_string[2:])
    except Exception as e:
        print(f"Error retrieving location: {e}")
        return "N/A"


def build_location_columns(df: DataFrame) -> DataFrame:
    """
    Extract locational information from "plant_origin" column and built three columns
    for: plant_latitude, plant_longitude, plant_location.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """

    df["plant_latitude"] = df.apply(
        lambda row: get_latitude(row["plant_origin"]), axis=1)
    df["plant_longitude"] = df.apply(
        lambda row: get_longitude(row["plant_origin"]), axis=1)
    df["plant_location"] = df.apply(
        lambda row: get_location(row["plant_origin"]), axis=1)
    df["plant_latitude"] = df["plant_latitude"].astype(float)
    df["plant_longitude"] = df["plant_longitude"].astype(float)
    return df


def get_valid_temperature(temperature_data: float) -> float | str:
    """
    Return temperature value if it meets the following criteria: -40 < temperature_data < 75
    Else return "N/A"

    Args:
        temperature_data (float): A float value representing temperature in the data

    Returns: float | str: A float value representing the temperature else return "N/A" for outliers
    """
    if temperature_data < -40 or temperature_data > 75:
        return "N/A"
    return temperature_data


def transform_temperature_column(df: DataFrame) -> DataFrame:
    """
    Remove outliers from "temperature" data.

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """
    df["temperature"] = df.apply(
        lambda row: get_valid_temperature(row["temperature"]), axis=1)
    return df


def normalize_column_text(df: DataFrame) -> DataFrame:
    """
    Normalize text within column entries to be lowercase

    Args: 
        df (DataFrame): A pandas DataFrame containing all plant data
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """
    df["botanist_name"] = df["botanist_name"].apply(lambda x: x.lower())
    df["plant_name"] = df["plant_name"].apply(lambda x: x.lower())
    df["plant_cycle"] = df["plant_cycle"].apply(lambda x: x.lower())
    df["plant_location"] = df["plant_location"].apply(lambda x: x.lower())

    return df


def build_plant_dataframe(plant_data: list[dict]) -> DataFrame:
    """
    Build a DataFrame from a a list of dictionaries.

    Args:
        plant_data (list[dict]): A Python list of dictionaries containing the parsed JSON data without nested dictionaries.
    Returns:
        DataFrame: A pandas DataFrame containing all plant data
    """
    df = pd.DataFrame(plant_data)

    df = transform_email_column_using_regex(df)
    df = transform_phone_column_using_regex(df)
    # df = transform_scientific_name_column(df)
    df = transform_last_watered_column(df)
    df = transform_recording_taken_column(df)
    df = build_location_columns(df)
    df = transform_temperature_column(df)
    df = normalize_column_text(df)

    return df


def normalise_text(text: str) -> str:
    """
    Convert all characters in a string to lowercase characters

    Args:
        text (str): A string of characters with unknown character case

    Returns:
        str: A string of characters with all characters are lower case
    """
    return text.lower()


def normalise(text):
    return "".join([x.upper() if i % 2 else x.lower() for i, x in enumerate(text)])


if __name__ == "__main__":

    json_file_path = "recent_plant_data.json"

    loaded_data_from_file = load_data(json_file_path)

    flatted_plant_data = flatten_data(loaded_data_from_file)

    plant_df = build_plant_dataframe(flatted_plant_data)

    # # text = "Bird of paraDise"
    # # normalised_text = normalise_text(text)
    # # print(normalised_text)

    # print(plant_df)
