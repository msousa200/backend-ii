"""
Logging configuration for the FastAPI application.
"""
import logging
import logging.handlers
import os
from pathlib import Path

from .config import settings

def configure_logging():
    """Configure logging for the application."""

    log_dir = Path(__file__).parent.parent / "logs"
    os.makedirs(log_dir, exist_ok=True)
    
  
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
   
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "fastapi_hello.log",
        maxBytes=10485760,  
        backupCount=5,
    )
    file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
 
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
 
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []  
    uvicorn_logger.addHandler(file_handler)
    
   
    return root_logger
