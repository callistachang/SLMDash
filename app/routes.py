"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route("/")
def home():
    return render_template(
        "index.jinja2", title="WIP Dashboard", template="home-template",
    )
