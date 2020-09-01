"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


class Config:
    """Flask configuration variables."""

    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")

    STATIC_FOLDER = "static"
    MEDIA_FOLDER = "media"
    TEMPLATES_FOLDER = "templates"
