from flask import render_template
from flask import current_app as app


@app.route("/")
def index():
    return render_template("index.jinja2")


@app.route("/ml-dashboard")
def ml_dashboard():
    return render_template("wip.jinja2", title="Image Recognition Dashboard")


@app.route("/data-report")
def data_report():
    return render_template("data_report.jinja2", title="Data Analysis Report")


@app.route("/ml-report")
def ml_report():
    return render_template("ml_report.jinja2", title="Machine Learning Report")


# /data-dashboard was implicitly routed in main.py