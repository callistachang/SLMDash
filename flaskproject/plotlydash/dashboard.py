"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe
from .layout import html_layout

def pressure_and_oxygen_over_time(df):
    color1 = '#9467BD'
    color2 = '#F08B00'

    data = [
        {
            'x': df['Time'],
            'y': df['Pressure'],
            'name': 'pressure',
            'line': {
                'color': color1
            },
            'type': 'scatter'
        },
        {
            'x': df['Time'],
            'y': df['Oxygen top'],
            'name': 'oxygen',
            'yaxis': 'y2',
            'type': 'scatter'
        }
    ]

    layout = {
        'title': 'Pressure and Oxygen Over Time',
        'yaxis': {
            'title': 'pressure',
            'titlefont': {
                'color': color1
            },
            'tickfont': {
                'color': color1
            }
        },
        'yaxis2': {
            'title': 'oxygen',
            'overlaying': 'y',
            'side': 'right',
            'titlefont': {
                'color': color2
            },
            'tickfont': {
                'color': color2
            }
        },
        'height': 500,
        'width': 1000,
        'padding': 100,
    }

    return {'data': data, 'layout': layout}

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    # Load DataFrame
    df = create_dataframe()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure=pressure_and_oxygen_over_time(df)
        ),
        create_data_table(df)
    ])

    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""

    table = dash_table.DataTable(
        id='example-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        sort_action='native',
        sort_mode='native',
        page_size=20
    )

    return table