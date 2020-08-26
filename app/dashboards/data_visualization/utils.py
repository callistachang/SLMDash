import pandas as pd
import numpy as np
import datetime
import base64
import io

import dash_table
import dash_html_components as html

from . import constants as c


def read_log(content, filename):
    sep = "---------------------------------------------"
    start, end = None, None
    _, content_string = content.split(",")
    decoded_data = base64.b64decode(content_string)
    i = 0
    for line in io.StringIO(decoded_data.decode("utf-8")):
        if not line:
            break
        elif start is None and sep in line:
            start = pd.to_datetime(line.split(",")[0])
        elif sep in line:
            end = pd.to_datetime(line.split(",")[0])
    return start, end


def parse_data_sheet(content, filename):
    """Convert the CSV file uploaded from the data dashboard to a Pandas DataFrame.

    Args:
        content (string): Base64-encoded, comma-separated string of values from the CSV file.
        filename (string): Name of the CSV file uploaded.
    """
    _, content_string = content.split(",")
    decoded_data = base64.b64decode(content_string)

    df_columns = pd.read_csv(
        io.StringIO(decoded_data.decode("utf-8")), nrows=1, delimiter=";"
    ).columns
    machine_type = check_machine_type(df_columns)

    if machine_type:
        if machine_type == "SLM280":
            datetime_format = "%m/%d/%y %H:%M:%S"
        elif machine_type == "SLM500":
            datetime_format = "%a %b %d %H:%M:%S %Y"

        # Read the CSV into a DataFrame and parse the Time column
        df = pd.read_csv(
            io.StringIO(decoded_data.decode("utf-8")),
            delimiter=";",
            parse_dates=["Time"],
            date_parser=lambda dt: pd.to_datetime(
                dt, format=datetime_format, errors="coerce"
            ),
            cache_dates=False,
        )

        df = clean_dataframe(df)
        df["MachineType"] = machine_type
        df["NumDataPoints"] = len(df)

        # Cut the number of data points by a factor of 25k
        step = len(df) // 25000
        df = df.iloc[::step].reset_index()
        return df

    return None


def check_machine_type(df_columns):
    machine_type = None
    if len(df_columns) == len(c.SLM280_COLUMNS) and all(df_columns == c.SLM280_COLUMNS):
        machine_type = "SLM280"
    elif len(df_columns) == len(c.SLM500_COLUMNS) and all(
        df_columns == c.SLM500_COLUMNS
    ):
        machine_type = "SLM500"
    return machine_type


def clean_dataframe(df):
    df = df.rename(columns=c.COLUMN_MAPPER)
    df = df[c.COLUMNS_TO_KEEP]
    return df
