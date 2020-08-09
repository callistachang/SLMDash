import pandas as pd
import numpy as np
import datetime
import base64
import io

import dash_table
import dash_html_components as html

from . import constants as c


def parse_data_sheet(content, filename):
    """Convert the CSV file uploaded from the data dashboard to a Pandas DataFrame.

    Args:
        content (string): Base64-encoded, comma-separated string of values from the CSV file.
        filename (string): Name of the CSV file uploaded.

    Returns:
        Dictionary: Contains the cleaned Pandas DataFrame as JSON dictionary, and the machine type derived from the CSV file.
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

        # improved from 56s to 12.6s to 0.8s :D
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
    """Cleans the DataFrame in a format that can be used to create graphs.

    Args:
        df (DataFrame): The DataFrame gotten immediately after reading

    Returns:
        [type]: [description]
    """
    df = df.rename(columns=c.COLUMN_MAPPER)
    df = df[c.COLUMNS_TO_KEEP]
    # return df.to_json(date_format="iso")
    return df


# def create_data_table(df):
#     table = dash_table.DataTable(
#         columns=[{"name": col, "id": col} for col in df.columns],
#         data=df.to_dict("records"),
#         sort_action="native",
#         sort_mode="native",
#         page_size=10,
#     )

#     return table
