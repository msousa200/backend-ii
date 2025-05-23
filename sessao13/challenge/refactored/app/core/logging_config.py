"""
Logging configuration.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path

from app.core.config import settings

def setup_logging():
    """Configure and set up logging for the application."""

    log_dir = Path("logs")
    os.makedirs(log_dir, exist_ok=True)
    

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName(settings.LOG_LEVEL))
    

    if root_logger.handlers:
        root_logger.handlers.clear()
    

    formatter = logging.Formatter(settings.LOG_FORMAT)
    

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    

    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / settings.LOG_FILE,
        maxBytes=10485760,  
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    

    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging configured with level {settings.LOG_LEVEL} in {settings.ENVIRONMENT} environment"
    )
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)
