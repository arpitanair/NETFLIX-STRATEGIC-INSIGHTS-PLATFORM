import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    df = pd.read_csv("data/raw/netflix_titles.csv")

    # Clean date column
    df["date_added"] = pd.to_datetime(
        df["date_added"].str.strip(),
        errors="coerce"
    )

    # Create year column
    df["year_added"] = df["date_added"].dt.year

    return df