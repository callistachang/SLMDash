import pytest

from app import create_app


@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client
