"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import datetime

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from .layout import html_layout
from . import graphs
from .utils import create_placeholder_df, parse_data_sheet

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dataviz/',
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = create_layout()

    init_callbacks(dash_app)

    return dash_app.server

def create_layout():
    """Create the dashboard layout."""
    
    df = create_placeholder_df()

    return html.Div([
        dcc.Upload(
            id='upload-input',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '80%',
                'height': '60px',
                'lineHeight': '60px',
                'border': '1px dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'alignItems': 'center',
            }
        ),
        dcc.Graph(
            id='example-graph',
            figure=graphs.pressure_and_oxygen_over_time(df)
        ),
        html.Div(id='upload-output')
    ])

def init_callbacks(app):
    @app.callback(
        Output('upload-output', 'children'),
        [Input('upload-input', 'contents'),
         Input('upload-input', 'filename')]
    )
    def update_output(list_of_contents, list_of_names):
        print("Updating...")
        if list_of_names is not None:
            print(list_of_names)
            df = parse_data_sheet(list_of_contents, list_of_names)
            print(df.head())
