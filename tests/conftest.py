import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture que fornece um TestClient para os endpoints da API."""
    with TestClient(app) as test_client:
        yield test_client
