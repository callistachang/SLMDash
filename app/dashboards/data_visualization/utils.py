import pandas as pd
import numpy as np
import datetime
import base64
import io

import dash_table
import dash_html_components as html

from .constants import slm280_columns, slm500_columns


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
    """[summary]

    Args:
        content (string): [description]
        filename (string): Name of the CSV file uploaded on the dataviz dashboard

    Returns:
        DataFrame: Clean pandas DF.
    """
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
            if all(df.columns == slm500_columns) or all(df.columns == slm500_columns):
                print("File loaded successfully!")
                return df

    except Exception as e:
        print(e)

    return None


def clean_slm280_data(df):
    pass


def clean_slm500_data(df):
    pass
