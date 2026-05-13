import pytest
from app import create_app
from app import models


@pytest.fixture()
def app():
    app = create_app("testing")
    yield app
    models._store.clear()


@pytest.fixture()
def client(app):
    return app.test_client()
