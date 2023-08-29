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


def transform_email_column_using_regex(df: DataFrame) -> DataFrame:
    """
    Extract email from affiliation column and add to existing 'botanist_email' column.

    Args: 
        df (DataFrame): A pandas DataFrame 

    Returns:
        DataFrame: A pandas DataFrame 
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
    Extract phone number from affiliation column and add to existing 'botanist_phone_number' column.

    Args: 
        df (DataFrame): A pandas DataFrame 
    Returns:
        DataFrame: A pandas DataFrame 
    """
    try:
        email_pattern = r"(\+[\d-]+)"
        df["botanist_phone_number"] = df["botanist_phone_number"].str.extract(
            email_pattern)
        df["botanist_phone_number"] = df["botanist_phone_number"].fillna("N/A")
        return df
    except:
        "N/A"


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
        df (DataFrame): A pandas DataFrame 
    Returns:
        DataFrame: A pandas DataFrame 
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
        datetime: A date time object
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
        df (DataFrame): A pandas DataFrame 
    Returns:
        DataFrame: A pandas DataFrame 
    """

    df["recording_taken"] = df.apply(
        lambda row: get_recording_taken_date_time(row["recording_taken"]), axis=1)
    return df


def build_plant_dataframe(plant_data: list[dict]) -> DataFrame:
    """
    Build a DataFrame from a a list of dictionaries.

    Args:
        plant_data (list[dict]): A Python list of dictionaries containing the parsed JSON data without nested dictionaries.
    Returns:
        DataFrame: A pandas DataFrame 
    """
    df = pd.DataFrame(plant_data)

    df = transform_email_column_using_regex(df)
    df = transform_phone_column_using_regex(df)
    df = transform_last_watered_column(df)
    df = transform_recording_taken_column(df)
    df = built_location_columns(df)

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
    json_file_path = 'mock_transform_data.json'

    loaded_data_from_file = load_data(json_file_path)

    flatted_plant_data = flatten_data(loaded_data_from_file)

    plant_df = build_plant_dataframe(flatted_plant_data)

    # text = "Bird of paraDise"
    # normalised_text = normalise_text(text)
    # print(normalised_text)

    print(plant_df)
