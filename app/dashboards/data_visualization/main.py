import numpy as np
import pandas as pd
import datetime

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from .layout import html_layout
from . import graphs
from .utils import parse_data_sheet
from . import constants


def create_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/data-dashboard/",
        external_stylesheets=[
            "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css",
            "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        ],
    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = create_layout()

    init_callbacks(dash_app)

    return dash_app.server


def create_layout():
    return html.Div(
        children=[
            dcc.Upload(
                id="upload-component",
                children=html.Div(
                    [
                        "Drag and Drop or ",
                        html.A("Select File", style={"textDecoration": "underline"},),
                    ]
                ),
                className="mx-auto w-50 text-center rounded",
                style={
                    "lineHeight": "36px",
                    "border": "1px dashed",
                    "cursor": "pointer",
                },
            ),
            dcc.Dropdown(
                id="filter-component",
                options=constants.dropdown_options,
                multi=True,
                clearable=False,
                value=["Pressure"],
                className="mx-auto pt-3 w-50",
            ),
            # html.Div(id="info-component", className="text-center pt-2"),
            html.Div(id="dashboard-component", className="text-center")
            # html.Div(id="dashboard-body", className="text-center py-4"),
        ],
        className="container-fluid",
    )


def init_callbacks(app):
    # @app.callback(
    #     Output("info-component", "children"),
    #     [
    #         Input("graphs-component", "children")
    #         # Input("upload-component", "contents"),
    #         # Input("upload-component", "filename"),
    #         # Input("filter-component", "value"),
    #     ],
    #     [State('upload-component', 'filename')]
    # )
    # def update_info(graph_component):
    #     print("info...")
    #     if graph_component:
    #         return html.P(
    #                     f"Successfully uploaded: {csv_filename} ♦ Machine Type: {data['machine_type']}",
    #                     className="text-success",
    #                 )
    #     else:
    #         return html.P("The file you uploaded was either not a CSV file or does not have the expected column names of a SLM280 or SLM500 machine.", className="text-danger")

    @app.callback(
        Output("dashboard-component", "children"),
        [
            Input("upload-component", "contents"),
            Input("upload-component", "filename"),
            Input("filter-component", "value")
        ],
        # [State("filter-component", "value")],
    )
    def update(csv_contents, csv_filename, column_filters):
        print("Updating...")
        if csv_filename:
            data = parse_data_sheet(csv_contents, csv_filename)
            column_filters += ["Time"]
            df = data["cleaned_df"][column_filters]
            if data is not None:
                return [
                        html.P(
                        f"Successfully uploaded: {csv_filename} ♦ Machine Type: {data['machine_type']}",
                        className="text-success pt-3",
                    ),
                        dcc.Graph(id="main-graph", figure=graphs.main_graph(df), className="h-50")
                    ]
            else:
                return html.P(
                    children="The file you uploaded was either not a CSV file or does not have the expected column names of a SLM280 or SLM500 machine.",
                    className="text-danger",
                )


# def create_graphs(df, column_filters):
#     column_filters += ["Time"]
#     df = df[column_filters]
#     return html.Div(
#         children=[dcc.Graph(id="main-graph", figure=graphs.main_graph(df), className="col"),],
#         className="row",
#     )
