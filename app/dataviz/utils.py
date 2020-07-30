import pandas as pd
import numpy as np
import datetime
import base64
import io

import dash_table
import dash_html_components as html

column_names = [
    "Time",
    "Pressure",
    "Filter Status",
    "Gas flow speed",
    "Gas pump power",
    "Oxygen top",
    "Oxygen 2",
    "Gas Temp",
    "Platform",
    "Build Chamber",
    "Optical Bench",
    "Collimator",
    "T_U",
    "T_LL",
    "T_LR",
    "R_LL",
    "R_LR",
    "B_F",
    "B_R",
    "Pump",
    "Cabinet",
    "Cabinet 2",
    "Ambiance",
    "MemTotal",
    "MemProcess",
    "Laser Emission Flags",
    "Laser On Flags",
    "Galvo X0",
    "Galvo Y0",
    "Servo X0",
    "Servo Y0",
    "Optic1 Home-in X1",
    "Optic1 Home-in Y1",
    "Optic1 Home-in X2",
    "Optic1 Home-in Y2",
]


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""

    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=10,
    )

    return table


def parse_data_sheet(content, filename):
    _, content_string = content.split(",")
    decoded_data = base64.b64decode(content_string)

    try:
        if "csv" in filename[-3:]:
            # improved from 56s to 12.6s to 0.8s :D
            df = pd.read_csv(
                io.StringIO(decoded_data.decode("utf-8")),
                delimiter=";",
                parse_dates=["Time"],
                date_parser=lambda dt: pd.to_datetime(
                    dt, format="%a %b %d %H:%M:%S %Y"
                ),
                cache_dates=False,
            )
            if all(df.columns == column_names):
                print("File loaded successfully")
                return df

    except Exception as e:
        print(e)

    return None


def create_placeholder_df():
    return pd.read_csv("data/sensordata.csv")
