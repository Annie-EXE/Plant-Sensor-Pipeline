"""Handles using the streamlit library to visualise data"""

import streamlit as st

from pandas import DataFrame


def dashboard_header(header_title: str, sub_title: str = None) -> None:
    """Displays the dashboard header"""
    st.markdown(f"## {header_title.title()}")
    if sub_title:
        st.markdown(
            "A dashboard representing _**relevant data**_ for the trucks selling produce. 🍦")


def create_chart_title(chart_title: str) -> None:
    """Creates chart chart_title"""

    st.markdown(f"### {chart_title.title()}")


def get_df_from_sql() -> DataFrame:
    """Returns df from SQL query"""
    pass


if __name__ == "__main__":

    pass
