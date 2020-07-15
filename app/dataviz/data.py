"""Prepare data for Plotly Dash."""
import pandas as pd
import numpy as np
import datetime

import dash_html_components as html

from .utils import create_data_table

def parse_data_sheet(data, filename, date):
    try: 
        if 'csv' in filename:
            df = pd.read_csv(data)
        elif 'xls' in filename:
            df = pd.read_excel(data)
        else:
            return html.Div(['Please upload a .csv or .xls file.'])
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    # TEMPORARY
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        create_data_table(df[:10]),
    ])



# @app.callback()
def update_page(data_list, filename_list, date_list):
    if data_list:
        children = [
            parse_data_sheet(data, filename, date) 
            for data, filename, date 
            in zip(data_list, filename_list, date_list)
        ]
        return children
