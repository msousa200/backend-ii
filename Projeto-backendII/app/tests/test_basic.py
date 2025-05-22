"""
Testes simples para validar as funcionalidades básicas do sistema.
"""
import pytest
import os
from app.services.crew_service import CrewAIService
from app.models.pydantic_models import ProcessingType

def test_crew_service_initialization():
    """Test if CrewAIService can be initialized."""
    service = CrewAIService()
    assert service is not None

def test_environment_variables():
    """Test if essential environment variables are set."""
    assert "OLLAMA_MODEL" in os.environ or os.getenv("OLLAMA_MODEL") is not None
    
    assert "OLLAMA_BASE_URL" in os.environ or os.getenv("OLLAMA_BASE_URL") is not None

def test_processing_types():
    """Test ProcessingType enumeration."""
    assert ProcessingType.TRANSLATION.value == "translation"
    assert ProcessingType.SUMMARIZATION.value == "summarization"
