"""
Custom middleware for logging requests.
"""

import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware for logging request details and timing."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
  
        start_time = time.time()
        
     
        logger.info(f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
        
    
        response = self.get_response(request)
        
   
        duration = time.time() - start_time
        logger.info(f"Response: {response.status_code} in {duration:.3f}s")
        
        return response
