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


# def get_database_longterm(conn_postgres: connection, schema: str) -> DataFrame:
#     """Returns redshift database transaction table as a DataFrame Object"""
#     with conn.cursor() as curr:
#         curr.execute(f"SELECT \
#                     truck_id, transaction_time, transaction_date, payment_type AS type, total_value AS total\
#                     FROM {schema}.transaction_fact AS transaction \
#                     LEFT JOIN {schema}.date_dim AS date ON \
#                     transaction.date_id=date.date_id \
#                     LEFT JOIN {schema}.type_dim AS type ON \
#                     transaction.type_id=type.type_id;")

#         transaction_df = curr.fetch_dataframe()

#     # transaction_df["timestamp"] = transaction_df.apply(lambda row: datetime.combine(
#     #     row["transaction_date"], row["transaction_time"]), axis=1)

#     return transaction_df


# def get_database_shortterm(conn_postgres: connection) -> DataFrame:
#     """Returns redshift database transaction table as a DataFrame Object"""
#     query = f"SELECT \
#             reading_information_id, plant_reading_time AS reading_time, soil_moisture, temperature\
#             FROM reading_information as reading\
#             LEFT JOIN sun_condition AS sun ON \
#             reading.shade_condition_id=sun.shade_condition_id \
#             LEFT JOIN shade_condition AS shade ON \
#             reading.shade_condition_id=shade.shade_condition_id;"

#     df = pd.read_sql_query(query, conn_postgres)

#     print(df)

#     return df


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

    # plant_df = get_database_shortterm(conn)

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
