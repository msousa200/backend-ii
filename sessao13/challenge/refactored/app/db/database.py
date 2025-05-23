"""
Database configuration and connections.
"""

import aiosqlite
import sqlite3
from fastapi import Depends
from functools import lru_cache
from urllib.parse import urlparse

from app.core.config import settings
from app.core.logging_config import get_logger


logger = get_logger(__name__)

async def init_db():
    """Initialize the database with required tables."""
    logger.info("Initializing database")

    parsed_url = urlparse(settings.DATABASE_URL)
    db_path = parsed_url.path.lstrip("/")
    

    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
            """
        )
        await db.commit()
    
    logger.info("Database initialized successfully")

class DatabaseSession:
    """
    Context manager for database connections.
    This ensures connections are properly closed after use.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()

@lru_cache()
def get_db_path():
    """Get the database path from the URL."""
    parsed_url = urlparse(settings.DATABASE_URL)
    return parsed_url.path.lstrip("/")

def get_db():
    """
    Dependency for getting a database connection.
    This ensures the connection is properly closed after the request.
    """
    with DatabaseSession(get_db_path()) as conn:
        yield conn
