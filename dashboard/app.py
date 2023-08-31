"""Handles using the streamlit library to visualise data"""

from os import environ
from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame
import streamlit as st
import matplotlib.pyplot as plt
import psycopg2
from psycopg2 import connect
from psycopg2.extensions import connection

def dashboard_header(header_title: str, sub_title: str = None) -> None:
    """Displays the dashboard header"""
    st.markdown(f"## {header_title.title()}")
    if sub_title:
        st.markdown(
            "A dashboard representing _**relevant data**_ for the trucks selling produce. 🍦")


def create_chart_title(chart_title: str) -> None:
    """Creates chart chart_title"""

    st.markdown(f"### {chart_title.title()}")


def get_water_df_from_sql(conn: connection) -> DataFrame:
    """Returns df from SQL query"""
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM water_history")
        water_data = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        water_df = pd.DataFrame(water_data, columns=column_names)


    conn.commit()

    return water_df


if __name__ == "__main__":

    load_dotenv()

    config = {}

    config["DB_PASSWORD"] = environ.get("DB_PASSWORD")
    config["DB_NAME"] = environ.get("DB_NAME")
    config["DB_USER"] = environ.get("DB_USER")
    config["DB_HOST"] = environ.get("DB_HOST")
    config["DB_PORT"] = environ.get("DEB_PORT")

    conn = connect(database=config["DB_NAME"],
                   user=config["DB_USER"],
                   password=config["DB_PASSWORD"],
                   host=config["DB_HOST"],
                   port=config["DB_PORT"])

    # dashboard_header('plants', 'p l a n t s')

    print(get_water_df_from_sql(conn))

