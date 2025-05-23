"""
Performance utilities for the application.
"""

import time
import functools
from typing import Callable

from app.core.logging_config import get_logger

logger = get_logger(__name__)

def measure_execution_time(func: Callable) -> Callable:
    """
    Decorator to measure and log the execution time of a function.
    
    Args:
        func: The function to measure.
        
    Returns:
        A wrapped function that logs execution time.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):

        start_time = time.time()
        

        result = await func(*args, **kwargs)
        

        execution_time = time.time() - start_time
        logger.debug(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    
    return wrapper
