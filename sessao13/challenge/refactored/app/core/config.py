"""
Application configuration settings.
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings using Pydantic for validation."""
    
    APP_TITLE: str = "Product API"
    APP_DESCRIPTION: str = "API for product management with best practices"
    APP_VERSION: str = "1.0.0"
    SHOW_DOCS: bool = True
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    

    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000"]
    

    DATABASE_URL: str = "sqlite:///./products.db"
    

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    

    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
