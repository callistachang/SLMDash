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

<<<<<<< HEAD
<<<<<<< Updated upstream
    try:
        if "csv" in filename[-3:]:
            df_columns = pd.read_csv(
                io.StringIO(decoded_data.decode("utf-8")), nrows=1, delimiter=";"
            ).columns
            print(df_columns)
            datetime_format = ""
            machine_type = ""

            if len(df_columns) == len(constants.slm280_columns) and all(
                df_columns == constants.slm280_columns
            ):
                machine_type = "SLM280"
                datetime_format = "%m/%d/%y %H:%M:%S"
            elif len(df_columns) == len(constants.slm500_columns) and all(
                df_columns == constants.slm500_columns
            ):
                machine_type = "SLM500"
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

            return {"cleaned_df": clean_dataframe(df), "machine_type": machine_type}

    except Exception as e:
        print(e)
=======
=======
>>>>>>> 6c992c1ea6b0a2a76a6eef51f0bc39914c07efa6
    df_columns = pd.read_csv(
        io.StringIO(decoded_data.decode("utf-8")), nrows=1, delimiter=";"
    ).columns
    machine_type = check_machine_type(df_columns)

    if machine_type:
        if machine_type == "SLM280":
            datetime_format = "%m/%d/%y %H:%M:%S"
        elif machine_type == "SLM500":
            datetime_format = "%a %b %d %H:%M:%S %Y"

<<<<<<< HEAD
=======
        # improved from 56s to 12.6s to 0.8s :D
>>>>>>> 6c992c1ea6b0a2a76a6eef51f0bc39914c07efa6
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
<<<<<<< HEAD

        step = len(df) // 40000
        df = df.iloc[::step].reset_index()

        return df
>>>>>>> Stashed changes
=======
        return df
>>>>>>> 6c992c1ea6b0a2a76a6eef51f0bc39914c07efa6

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
    return df
