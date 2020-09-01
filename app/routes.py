from flask import render_template, send_file, request
from flask import current_app as app
import os
from urllib.parse import unquote
from werkzeug.utils import secure_filename
from app.dashboards.image_recognition import find_defects


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
    path = ""
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            dirname = os.path.join("app", "media", "images")
            filepath = os.path.join(dirname, filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            file.save(filepath)
            path = find_defects(filename)
            path = f"images/{path}"
    return render_template("image_recognition_page.jinja2", path=path)


@app.route("/download/report/<path:path>")
def download_reports(path):
    path = unquote(path)
    full_path = os.path.join("media", "reports", path)
    return send_file(full_path, as_attachment=True)


# /data-dashboard was implicitly routed in main.py
