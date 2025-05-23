"""
Main application file for FastAPI Hello World example.
"""
import time
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .logging_config import configure_logging


logger = logging.getLogger(__name__)
configure_logging()


app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI application demonstrating best practices",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request details and timing."""
    start_time = time.time()
    

    logger.info(f"Request: {request.method} {request.url.path} from {request.client.host}")
    
    try:
    
        response = await call_next(request)
        
  
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} in {process_time:.3f}s")
        
        return response
    except Exception as e:
     
        process_time = time.time() - start_time
        logger.error(f"Error: {str(e)} in {process_time:.3f}s")
        

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

@app.get("/")
async def index():
    """Simple Hello World endpoint."""
    logger.info("Hello World endpoint called")
    return {"message": "Hello from FastAPI"}

@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized Hello endpoint."""
    logger.info(f"Hello name endpoint called with name: {name}")
    

    if not name or len(name) > 50:
        logger.warning(f"Invalid name provided: {name}")
        raise HTTPException(
            status_code=400, 
            detail="Name must be between 1 and 50 characters"
        )
    
    return {"message": f"Hello, {name}, from FastAPI!"}
