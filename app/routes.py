from flask import render_template
from flask import current_app as app


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


# /data-dashboard was implicitly routed in main.py
