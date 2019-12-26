import pytest
from app import app

@pytest.fixture
def app():
    app1 = app()
    return app1