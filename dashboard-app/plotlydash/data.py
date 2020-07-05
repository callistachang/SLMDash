"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np

# TODO: TEMPORARY
def create_dataframe():
    """Create Pandas DataFrame from local CSV."""
    df = pd.read_csv("data/sensordata.csv")
    return df