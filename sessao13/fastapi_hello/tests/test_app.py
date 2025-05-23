"""
Tests for the FastAPI Hello World application.

Run with: pytest test_app.py -v
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_hello_endpoint(client):
    """Test the /hello/ endpoint returns correct response."""
    response = client.get("/hello/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Hello, World!"


def test_hello_with_name_endpoint(client):
    """Test the /hello/{name} endpoint with a name parameter."""
    test_name = "TestUser"
    response = client.get(f"/hello/{test_name}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == f"Hello, {test_name}!"


def test_health_check_endpoint(client):
    """Test the /health/ endpoint returns status UP."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "UP"


def test_invalid_endpoint_returns_404(client):
    """Test that accessing an invalid endpoint returns a 404 error."""
    response = client.get("/invalid-endpoint/")
    assert response.status_code == 404
    assert "detail" in response.json()
