from flask import render_template, make_response, send_file
from flask import current_app as app
import os
from urllib.parse import unquote


@app.route("/")
def index():
    return render_template("index.jinja2")


@app.route("/ml-dashboard")
def ml_dashboard():
    return render_template("wip.jinja2", title="Image Recognition Dashboard")


@app.route("/ref")
def data_report():
    return render_template("reference.jinja2", title="Consumer Reference")


@app.route("/reports")
def ml_report():
    return render_template("reports.jinja2", title="Team Reports")


@app.route("/download/report/<path:path>")
def download_reports(path):
    path = unquote(path)
    full_path = os.path.join("media", "reports", path)

    return send_file(full_path, as_attachment=True)


# /data-dashboard was implicitly routed in main.py
