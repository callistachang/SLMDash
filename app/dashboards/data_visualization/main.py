import numpy as np
import pandas as pd
import os
import datetime
import flask
import pdfkit

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

import plotly

from .layout import html_layout
from . import graphs
from .utils import parse_data_sheet
from . import constants as c
from .report_generator import Checker
from .anomaly_detection import detect_anomalies


PDFKIT_CONFIG = pdfkit.configuration(
    wkhtmltopdf=os.path.join(os.getcwd(), "app", "static", "wkhtmltopdf.exe")
)


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
                id="filter-dropdown",
                options=c.DROPDOWN_OPTIONS,
                multi=True,
                value=["Pressure", "Oxygen1"],
                className="mx-auto pt-2 w-50",
            ),
            dcc.Checklist(
                id="anomaly-checkbox",
                options=[
                    {"label": " Show Anomalies (1 Column)", "value": "ShowAnomalies",}
                ],
                className="text-center",
            ),
            html.A(
                dcc.Loading(
                    html.Button(
                        "Initialize Report Download",
                        id="download-btn",
                        className="btn btn-primary",
                    ),
                    type="dot",
                ),
                id="download-link",
                href=None,
                className="d-none",
            ),
            html.Div(id="dashboard-component", className="text-center"),
            dcc.Store(id="store"),
        ]
    )


def upload_history():
    try:
        upload_history_options = [
            {"label": file[:-4], "value": file} for file in os.listdir(c.MEDIA_DF_PATH)
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
    except:
        pass


def init_callbacks(app):
    @app.callback(
        [
            Output("download-link", "href"),
            Output("download-btn", "children"),
            Output("download-btn", "className"),
        ],
        [Input("download-btn", "n_clicks")],
        [State("store", "data"), State("download-link", "href"),],
    )
    def make_image(n_clicks, data, download_href):
        print("make_image()")
        if download_href:
            return (None, "Initialize Report Download", "btn btn-primary")
        else:
            # run the report generator by passing in the df
            df = pd.read_feather(data["filepath"])
            df = df.set_index("Time")
            checker = Checker(df)
            r = checker.generateReport()

            # put the report data into the template
            template = flask.render_template(
                "report_template.jinja2",
                filename=data["filename"],
                pressure=r["Pressure"],
                filter_status=r["FilterStatus"],
                gas_flow_speed=r["GasFlowSpeed"],
                oxygen_1=r["Oxygen1"],
                oxygen_2=r["Oxygen2"],
                gas_temp=r["GasTemp"],
                build_chamber=r["BuildChamber"],
                optical_bench=r["OpticalBench"],
                collimator=r["Collimator"],
                num_alerts=r["NumAlerts"],
                alert_level=r["AlertLevel"],
            )
            pdfkit.from_string(
                template,
                f"{c.MEDIA_REPORT_PATH}/{data['filename']}.pdf",
                configuration=PDFKIT_CONFIG,
            )
            return (
                f"/download/report/{data['filename']}.pdf",
                "Download Now",
                "btn btn-success",
            )

    @app.callback(
        Output("store", "data"),
        [
            Input("upload-component", "contents"),
            Input("upload-component", "filename"),
            Input("history-component", "value"),
        ],
    )
    def upload(csv_contents, csv_filename, history_filename):
        try:
            fired_input = dash.callback_context.triggered[0]["prop_id"]
            if "history-component" in fired_input:
                print("Looking through past uploads...")
                return {
                    "filename": history_filename[:-4],
                    "filepath": f"{c.MEDIA_DF_PATH}/{history_filename}",
                    "valid_upload": True,
                }
            elif "upload-component" in fired_input:
                print("Uploading...")
                if csv_filename:
                    if csv_filename[-4:] == ".csv":
                        filename = csv_filename[:-4]
                        filepath = f"{c.MEDIA_DF_PATH}/{filename}.ftr"
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
        except:
            pass

    @app.callback(
        [
            Output("dashboard-component", "children"),
            Output("download-link", "className"),
        ],
        [Input("store", "data"), Input("filter-dropdown", "value")],
    )
    def update_dashboard(data, column_filters):
        print(f"update_dashboard, data: {data}, column_filters: {column_filters}")
        try:
            download_btn_class = "row justify-content-center pt-3"
            if data["valid_upload"]:
                column_filters += c.TEMP_COLUMNS
                df = pd.read_feather(data["filepath"])[column_filters]
                print("Success!")
                return (
                    [
                        html.P(
                            f"Successfully uploaded: {data['filename']} ♦ Machine Type: {df.loc[0, 'MachineType']} ♦ Number of Data Points: {df.loc[0, 'NumDataPoints']}",
                            className="text-success pt-2",
                        ),
                        dcc.Loading(
                            dcc.Graph(
                                id="main-graph",
                                figure=graphs.main_graph(df),
                                style={"height": "80%"},
                            ),
                            type="dot",
                        ),
                    ],
                    download_btn_class,
                )
            else:
                return (
                    html.P(
                        children="The file you uploaded was either not a CSV file or does not have the expected column names of a SLM280 or SLM500 machine.",
                        className="text-danger pt-2",
                    ),
                    f"{download_btn_class} d-none",
                )
        except:
            pass
        return (
            None,
            f"{download_btn_class} d-none",
        )

    @app.callback(
        Output("main-graph", "figure"),
        [Input("anomaly-checkbox", "value")],
        [State("main-graph", "figure"), State("filter-dropdown", "value")],
    )
    def show_anomalies(value, figure, column_filters):
        print(f"show_anomalies(), checkbox value: {value}")
        if len(column_filters) == 1:
            input_df = pd.DataFrame()
            input_df["Time"] = figure["data"][0]["x"]
            input_df[column_filters[0]] = figure["data"][0]["y"]
            detect_anomalies(
                input_df, column_filters[0], 11.5, 11.9,
            )
            # detect_anomalies()
            if value:
                figure["layout"]["shapes"] = [
                    anomaly_region(
                        "2020-3-23T06:00:00", "2020-3-23T12:00:00", "#e41a1c"
                    )
                ]
            elif not value and "shapes" in figure["layout"]:
                del figure["layout"]["shapes"]
        return figure


def anomaly_region(start, end, color):
    return {
        "type": "rect",
        "xref": "Time",
        "yref": "paper",  # y-reference is assigned to the plot paper [0, 1]
        "x0": start,
        "y0": 0,
        "x1": end,
        "y1": 1,
        "fillcolor": color,
        "opacity": 0.3,
        "layer": "below",
        "line": {"width": 0},
    }
