from flask import Flask
from flask_assets import Environment


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        from . import routes
        from .dashboards.data_visualization.main import create_dashboard

        app = create_dashboard(app)
        return app
