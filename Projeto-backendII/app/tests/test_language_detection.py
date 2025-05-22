"""
Test cases for the language detection endpoint
"""
import pytest
from fastapi.testclient import TestClient
import json

from main import app

client = TestClient(app)

def test_detect_english_language():
    response = client.post(
        "/api/detect-language",
        json={"text": "This is a sample text in English that should be correctly identified."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "English"
    assert data["confidence"] > 0.5
    assert data["text_length"] > 0

def test_detect_portuguese_language():
    response = client.post(
        "/api/detect-language",
        json={"text": "Este é um texto em português que deve ser corretamente identificado pelo sistema."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "Portuguese"
    assert data["confidence"] > 0.5
    assert data["text_length"] > 0

def test_detect_mixed_text_more_english():
    response = client.post(
        "/api/detect-language",
        json={"text": "This is a mixed text with some Portuguese words like 'olá' and 'obrigado', but mostly English."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "English"

def test_detect_language_short_text():
    response = client.post(
        "/api/detect-language",
        json={"text": "Hello!"}
    )
    assert response.status_code == 200

def test_detect_language_empty_text():
    response = client.post(
        "/api/detect-language",
        json={"text": ""}
    )
    assert response.status_code == 422  
