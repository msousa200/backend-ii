import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.crew_service import CrewAIService


@pytest.fixture
def crew_service():
    """Create a CrewAIService instance for testing."""
    return CrewAIService()


class TestCrewAIService:
    pass
