"""Handles using the streamlit library to visualise data"""

from os import environ, _Environ
from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame
import streamlit as st
import matplotlib.pyplot as plt
import psycopg2
from psycopg2 import connect
from psycopg2.extensions import connection


def get_db_connection(config_file: _Environ) -> connection:
    try:
        return connect(
            database=config_file["DB_NAME"],
            user=config_file["DB_USER"],
            password=config_file["DB_PASSWORD"],
            port=config_file["DB_PORT"],
            host=config_file["DB_HOST"]
        )
    except Exception as err:
        print("Error connecting to database.")
        raise err


def dashboard_header(header_title: str, sub_title: str = None) -> None:
    """Displays the dashboard header"""
    st.markdown(f"## {header_title.title()}")
    if sub_title:
        st.markdown(
            "A dashboard representing _**relevant data**_ for the trucks selling produce. 🍦")


def create_chart_title(chart_title: str) -> None:
    """Creates chart chart_title"""

    st.markdown(f"### {chart_title.title()}")


def get_df_from_sql(conn: connection, table_name: str) -> DataFrame:
    """Returns df from SQL query"""
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table_name}")
        data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=column_names)

    conn.commit()

    return df


def bar_chart_to_show_water_frequency(water_df: DataFrame):
    """Makes a bar chart that shows how often
    each plant has been watered"""

    counts = water_df['plant_id'].value_counts()

    plt.figure(figsize=(60, 30))
    plt.bar(counts.index, counts.values, width=0.5, color='#44d4eb')
    plt.xticks(counts.index, counts.index, rotation=90, fontsize=50)
    plt.xlabel("\nPlant ID", fontsize=100)
    plt.ylabel("Times Watered", fontsize=100)
    plt.title("Watering Frequency\n", fontsize=200)

    st.pyplot(plt)


def plot_average_temperatures(reading_df: DataFrame):
    """Plots the average temperature of each plant"""

    average_temperatures = reading_df.groupby('plant_id')['temperature'].mean()

    plt.bar(average_temperatures.index,
            average_temperatures.values, color='#fa9196')

    plt.xlabel('\nPlant ID')
    plt.ylabel('Average Temperature')
    plt.title('\nAverage Temperature for Each Plant ID\n', fontsize=200)

    st.pyplot(plt)


def plot_average_soil_moisture(reading_df: DataFrame):
    """Plots the average soil moisture for each plant"""

    avg_soil_moisture = reading_df.groupby('plant_id')['soil_moisture'].mean()

    plt.bar(avg_soil_moisture.index, avg_soil_moisture.values, color='#7d4807')

    plt.xlabel('\nPlant ID')
    plt.ylabel('Average Soil Moisture')
    plt.title('\nAverage Soil Moisture for Each Plant ID\n', fontsize=200)

    st.pyplot(plt)


if __name__ == "__main__":

    load_dotenv()
    config = environ

    conn = get_db_connection(config)

    # config["DB_PASSWORD"] = environ.get("DB_PASSWORD")
    # config["DB_NAME"] = environ.get("DB_NAME")
    # config["DB_USER"] = environ.get("DB_USER")
    # config["DB_HOST"] = environ.get("DB_HOST")
    # config["DB_PORT"] = environ.get("DEB_PORT")

    # conn = connect(database=config["DB_NAME"],
    #                user=config["DB_USER"],
    #                password=config["DB_PASSWORD"],
    #                host=config["DB_HOST"],
    #                port=config["DB_PORT"])

    # dashboard_header('plants', 'p l a n t s')

    water_df = get_df_from_sql(conn, 'water_history')
    reading_df = get_df_from_sql(conn, 'reading_information')
    plants_df = get_df_from_sql(conn, 'plant')
    reading_df = pd.merge(
        reading_df, plants_df[['plant_id', 'plant_name']], on='plant_id', how='left')
    print(reading_df[['plant_id', 'plant_name']])

    bar_chart_to_show_water_frequency(water_df)
    print(reading_df['soil_moisture'])

    plot_average_temperatures(reading_df)
    plot_average_soil_moisture(reading_df)

    print(plants_df)
