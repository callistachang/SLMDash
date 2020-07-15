"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc

from .data import parse_data_sheet
from .layout import html_layout
from . import graphs
from .utils import create_placeholder_df

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = create_layout()

    return dash_app.server

def create_layout():
    """Create the dashboard layout."""
    
    df = create_placeholder_df()

    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
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
            },
        ),
        dcc.Graph(
            id='example-graph',
            figure=graphs.pressure_and_oxygen_over_time(df)
        )
    ])


