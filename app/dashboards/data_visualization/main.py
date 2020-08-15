import numpy as np
import pandas as pd
import os
import datetime

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from .layout import html_layout
from . import graphs
from .utils import parse_data_sheet
from . import constants as c


def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/data-dashboard/",
        external_stylesheets=[
            "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css",
            "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        ],
    )
    dash_app.index_string = html_layout
    dash_app.layout = create_layout()
    init_callbacks(dash_app)

    return dash_app.server


def create_layout():
    return html.Div(
        [
            html.Div(
                [
                    dcc.Upload(
                        "Upload New File",
                        id="upload-component",
                        className="px-5 text-center rounded",
                        style={
                            "lineHeight": "36px",
                            "border": "1px dashed",
                            "cursor": "pointer",
                        },
                    ),
                    html.Span("OR", className="mx-3 pt-2 font-weight-bold"),
                    upload_history(),
                ],
                className="d-flex justify-content-center",
            ),
            dcc.Dropdown(
                id="filter-component",
                options=c.DROPDOWN_OPTIONS,
                multi=True,
                value=["Pressure"],
                className="mx-auto pt-3 w-50",
            ),
            html.Div(id="dashboard-component", className="text-center"),
            dcc.Store(id="store"),
        ]
    )


def upload_history():
    upload_history_options = [
        {"label": file[:-4], "value": file} for file in os.listdir(c.MEDIA_PATH)
    ]

    return html.Div(
        children=[
            dcc.Dropdown(
                id="history-component",
                options=upload_history_options,
                placeholder="Use Past Uploads",
            )
        ],
        className="w-25 text-center",
    )


def init_callbacks(app):
    @app.callback(
        Output("store", "data"),
        [
            Input("upload-component", "contents"),
            Input("upload-component", "filename"),
            Input("history-component", "value"),
        ],
    )
    def upload(csv_contents, csv_filename, history_filename):
        fired_input = dash.callback_context.triggered[0]["prop_id"]

        if "history-component" in fired_input:
            print("Looking through past uploads...")
            return {
                "filename": history_filename[:-4],
                "filepath": f"{c.MEDIA_PATH}/{history_filename}",
                "valid_upload": True,
            }
        elif "upload-component" in fired_input:
            print("Uploading...")
            if csv_filename:
                if csv_filename[-4:] == ".csv":
                    filename = csv_filename[:-4]
                    filepath = f"{c.MEDIA_PATH}/{filename}.ftr"
                    if os.path.exists(filepath):
                        print("Cache hit!")
                    else:
                        df = parse_data_sheet(csv_contents, csv_filename)
                        df.to_feather(filepath)
                    return {
                        "filename": filename,
                        "filepath": filepath,
                        "valid_upload": True,
                    }
            return {"valid_upload": False}

    @app.callback(
        Output("dashboard-component", "children"),
        [Input("store", "data"), Input("filter-component", "value")],
    )
    def update(data, column_filters):
        print("Updating...")
        try:
            if data["valid_upload"]:
                column_filters += c.TEMP_COLUMNS
                df = pd.read_feather(data["filepath"])[column_filters]
                print("Success!")
                return [
                    html.P(
                        f"Successfully uploaded: {data['filename']} ♦ Machine Type: {df.loc[0, 'MachineType']} ♦ Number of Data Points: {df.loc[0, 'NumDataPoints']}",
                        className="text-success pt-3",
                    ),
                    dcc.Graph(
                        id="main-graph",
                        figure=graphs.main_graph(df),
                        style={"height": "80%"},
                    ),
                ]
            else:
                return html.P(
                    children="The file you uploaded was either not a CSV file or does not have the expected column names of a SLM280 or SLM500 machine.",
                    className="text-danger pt-3",
                )
        except:
            pass
