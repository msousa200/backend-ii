"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db.database import init_db


logger = setup_logging()

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url=settings.DOCS_URL if settings.SHOW_DOCS else None,
        redoc_url=settings.REDOC_URL if settings.SHOW_DOCS else None,
    )
    

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )
    
    application.add_middleware(GZipMiddleware, minimum_size=1000)
    

    application.include_router(api_router, prefix="/api")
    
    @application.on_event("startup")
    async def startup_event():
        """Actions to perform on application startup."""
        logger.info("Starting up application")
        await init_db()
    
    @application.on_event("shutdown")
    async def shutdown_event():
        """Actions to perform on application shutdown."""
        logger.info("Shutting down application")
    
    return application

app = create_application()
