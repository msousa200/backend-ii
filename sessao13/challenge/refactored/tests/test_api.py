"""
Tests for the refactored product API.

Run with: pytest
"""
import pytest
from fastapi.testclient import TestClient
import sqlite3
import os
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""

    test_db = "test_products.db"
    

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)
    

    cursor.execute("""
    INSERT INTO products (name, description, price, stock)
    VALUES ('Test Product', 'This is a test product', 29.99, 10)
    """)
    conn.commit()
    conn.close()
    

    app.dependency_overrides = {}
    

    yield TestClient(app)
    

    if os.path.exists(test_db):
        os.remove(test_db)


def test_get_products(client):
    """Test retrieving products endpoint."""
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)


def test_get_product_by_id(client):
    """Test retrieving a single product by ID."""
    product_id = 1 
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert "product" in data
    assert data["product"]["id"] == product_id


def test_get_nonexistent_product(client):
    """Test retrieving a product that doesn't exist."""
    response = client.get("/products/999")  
    assert response.status_code == 404


def test_create_product(client):
    """Test creating a new product."""
    new_product = {
        "name": "New Test Product",
        "description": "This is a new test product",
        "price": 19.99,
        "stock": 5
    }
    response = client.post("/products/", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert "product" in data
    assert data["product"]["name"] == new_product["name"]
    assert "id" in data["product"]


def test_create_product_with_invalid_data(client):
    """Test creating a product with invalid data."""
    invalid_product = {
        "name": "", 
        "price": -10,  
        "stock": "not_a_number"  
    }
    response = client.post("/products/", json=invalid_product)
    assert response.status_code == 422  
