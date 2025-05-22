"""
Logging utility for the application
This module provides a centralized logging configuration for the entire application.
"""
import logging
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

LOG_DIR = os.getenv("LOG_DIR", "/tmp/logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logging.getLogger('performance').setLevel(logging.INFO)
logging.getLogger('crew').setLevel(logging.INFO)
logging.getLogger('app.services.language_service').setLevel(logging.INFO)

def get_logger(name):
    """Get a logger with the given name"""
    return logging.getLogger(name)

class PerformanceTimer:
    """
    Timer for measuring execution time of operations
    Example usage:
    
    with PerformanceTimer("task_processing") as timer:
        # Do some work
        result = process_text(text)
        timer.add_info("task_id", task_id)
    """
    def __init__(self, operation_name: str, log_level: int = logging.INFO):
        self.logger = logging.getLogger("performance")
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.additional_info = {}
        self.log_level = log_level

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        
        log_data = {
            "operation": self.operation_name,
            "duration_seconds": self.duration,
            "timestamp": datetime.now().isoformat()
        }
        
        for key, value in self.additional_info.items():
            log_data[key] = value
            
        if exc_type:
            log_data["error"] = str(exc_val)
            log_data["error_type"] = exc_type.__name__
        
        self.logger.log(self.log_level, f"Performance: {json.dumps(log_data, cls=DateTimeEncoder)}")
        return False 

    def add_info(self, key: str, value: Any) -> None:
        """Add additional information to the log"""
        self.additional_info[key] = value


class RequestLogger:
    """
    Logger for API requests and responses
    """
    def __init__(self, name: str = "api"):
        self.logger = logging.getLogger(name)
    
    def log_request(self, 
                   endpoint: str, 
                   method: str, 
                   request_data: Optional[Dict[str, Any]] = None,
                   request_id: Optional[str] = None) -> str:
        """
        Log an API request
        
        Args:
            endpoint: The API endpoint
            method: HTTP method (GET, POST, etc.)
            request_data: Request data (optional)
            request_id: Request ID (optional, will be generated if not provided)
            
        Returns:
            The request ID
        """
        if not request_id:
            import uuid
            request_id = str(uuid.uuid4())
        
        log_data = {
            "request_id": request_id,
            "endpoint": endpoint,
            "method": method,
            "timestamp": datetime.now().isoformat()
        }
        
        if request_data:
            if isinstance(request_data, dict) and "text" in request_data and isinstance(request_data["text"], str):
                if len(request_data["text"]) > 100:
                    log_data["text_length"] = len(request_data["text"])
                    request_data = request_data.copy()  
                    request_data["text"] = request_data["text"][:100] + "..."
            
            log_data["request_data"] = request_data
        
        self.logger.info(f"API Request: {json.dumps(log_data, cls=DateTimeEncoder)}")
        return request_id
    
    def log_response(self,
                    endpoint: str,
                    request_id: str,
                    status_code: int,
                    response_data: Optional[Dict[str, Any]] = None,
                    duration_ms: Optional[float] = None):
        """
        Log an API response
        
        Args:
            endpoint: The API endpoint
            request_id: Request ID linking to the request
            status_code: HTTP status code
            response_data: Response data (optional)
            duration_ms: Request duration in milliseconds (optional)
        """
        log_data = {
            "request_id": request_id,
            "endpoint": endpoint,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        }
        
        if duration_ms is not None:
            log_data["duration_ms"] = duration_ms
        
        if response_data:
            if isinstance(response_data, dict) and "processed_text" in response_data and isinstance(response_data["processed_text"], str):
                if len(response_data["processed_text"]) > 100:
                    log_data["processed_text_length"] = len(response_data["processed_text"])
                    response_data = response_data.copy()  
                    response_data["processed_text"] = response_data["processed_text"][:100] + "..."
            
            log_data["response_data"] = response_data
        
        self.logger.info(f"API Response: {json.dumps(log_data, cls=DateTimeEncoder)}")


def log_agent_result(agent_type: str, input_text: str, output_text: str, duration: float) -> None:
    """
    Log agent processing result with detailed information
    
    Args:
        agent_type: Type of agent (summarization, translation, etc.)
        input_text: Input text
        output_text: Processed output text
        duration: Processing time in seconds
    """
    logger = logging.getLogger("agent_results")
    
    truncated_input = (input_text[:100] + "...") if len(input_text) > 100 else input_text
    truncated_output = (output_text[:100] + "...") if len(output_text) > 100 else output_text
    
    log_data = {
        "agent_type": agent_type,
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration,
        "input_length": len(input_text),
        "output_length": len(output_text),
        "input_text": truncated_input,
        "output_text": truncated_output
    }
    
    logger.info(f"Agent Result: {json.dumps(log_data, cls=DateTimeEncoder)}")

logger = get_logger("app")
api_logger = RequestLogger("api")
crew_logger = get_logger("crew")
db_logger = get_logger("db")
agent_logger = get_logger("agent_results")
