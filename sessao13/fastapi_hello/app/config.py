"""
Configuration settings for the FastAPI application.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
  
    APP_NAME: str = "FastAPI Hello World"
    ENVIRONMENT: str = "development"

    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:8000"]

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
