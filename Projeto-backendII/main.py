import uvicorn
import os
import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Gauge, Histogram

from app.api.routes import api_router
from app.models.database import TextTask
from app.utils.logging_util import logger
from app.utils.metrics import TASKS_TOTAL, TASK_QUEUE_SIZE, PROCESSING_TIME
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func
from app.db.database import engine, create_tables

VERSION = "1.1.0"
BUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
API_DESCRIPTION = """
## Text Processing AI Agents API

This API provides text processing capabilities using AI agents, powered by the CrewAI framework.

### Features

* **Summarization**: Create concise summaries of longer texts
* **Translation**: Translate text between English and Portuguese with automatic language detection
* **Language Detection**: Detect whether text is in English or Portuguese

### More Information

* The API processes text asynchronously through background tasks.
* Tasks can be monitored through the /api/tasks endpoints.
* All tasks are logged for performance monitoring and debugging.
* Metrics are available through Prometheus endpoints.
"""

app = FastAPI(
    title="Text Processing AI Agents API",
    description=API_DESCRIPTION,
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

instrumentator = Instrumentator()
instrumentator.instrument(app)
instrumentator.expose(app, include_in_schema=True, should_gzip=True)

metrics.request_size(metric_namespace="fastapi", metric_subsystem="http")
metrics.response_size(metric_namespace="fastapi", metric_subsystem="http")
metrics.latency(metric_namespace="fastapi", metric_subsystem="http")

@asynccontextmanager
async def lifespan(app):
    """Lifespan handler for application startup and shutdown"""
    logger.info(f"Starting application version {VERSION}")
    
    try:
        create_tables()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {str(e)}")
        logger.info("Falling back to SQLite database")
        os.environ["DATABASE_URL"] = "sqlite:///./app.db"
        create_tables()
        logger.info("SQLite database initialized")
    

    logger.info(f"OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")
    logger.info(f"OLLAMA_MODEL: {os.getenv('OLLAMA_MODEL', 'tinyllama')}")
    

    with Session(engine) as session:
        for status in ["pending", "processing", "completed", "failed"]:
            count = session.scalar(
                select(func.count())
                .select_from(TextTask)
                .where(TextTask.status == status)
            )
            TASKS_TOTAL.labels(status=status).set(count)
    
    yield  
    
    logger.info("Application shutting down")

app.router.lifespan_context = lifespan

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.utils.errors import AppError, error_to_dict

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle application-specific errors"""
    return JSONResponse(
        status_code=400,  
        content=error_to_dict(exc)
    )

@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": {"type": str(type(exc).__name__)}
            }
        }
    )

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {
        "message": "Welcome to the Text Processing AI Agents API",
        "version": VERSION,
        "build_date": BUILD_DATE,
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": VERSION
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)