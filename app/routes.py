from flask import render_template, send_file, request
from flask import current_app as app
import os
from urllib.parse import unquote
from werkzeug.utils import secure_filename


@app.route("/")
def index():
    return render_template("index_page.jinja2")


@app.route("/ml-dashboard")
def ml_dashboard():
    return render_template(
        "image_recognition_page.jinja2", title="Image Recognition Dashboard"
    )


@app.route("/ref")
def data_report():
    return render_template("reference_page.jinja2", title="Consumer Reference")


@app.route("/research")
def ml_report():
    return render_template("research_page.jinja2", title="Team Reports")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("app", "media", "images", filename))

    return """lol"""
    # return render_template("upload.html", data=a)


@app.route("/download/report/<path:path>")
def download_reports(path):
    path = unquote(path)
    full_path = os.path.join("media", "reports", path)
    return send_file(full_path, as_attachment=True)


# /data-dashboard was implicitly routed in main.py
