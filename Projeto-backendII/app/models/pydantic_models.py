from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ProcessingStatus(str, Enum):
    """Enum for task processing statuses"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingType(str, Enum):
    """Enum for different text processing types"""
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    DETECTION = "detection"  


class Language(str, Enum):
    """Supported languages for translation"""
    ENGLISH = "English"
    PORTUGUESE = "Portuguese"


class TaskMetadata(BaseModel):
    """Model for task metadata validation"""
    request_id: str = Field(..., description="Unique request ID for tracking")
    client_ip: str = Field(..., description="Client IP address")
    target_language: Optional[Language] = Field(None, description="Target language for translation")
    error_details: Optional[str] = Field(None, description="Error details if task failed")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    model_used: str = Field(default="ollama/tinyllama", description="AI model used for processing")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "client_ip": "127.0.0.1",
                "target_language": "Portuguese",
                "processing_time": 1.23,
                "model_used": "ollama/tinyllama"
            }
        }
    )


class TextProcessingRequest(BaseModel):
    """Model for text processing request"""
    text: str = Field(
        ..., 
        description="Text to process",
        min_length=1,
        max_length=50000  
    )
    processing_type: ProcessingType = Field(
        ..., 
        description="Type of processing to perform"
    )
    target_language: Optional[Language] = Field(
        None, 
        description="Target language for translation (if not provided, will detect automatically)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Sample text for processing",
                "processing_type": "summarization",
                "target_language": None
            }
        }
    )


class TextProcessingResponse(BaseModel):
    """Model for text processing response"""
    id: int
    original_text: str
    processed_text: Optional[str] = None
    processing_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TextProcessingStatusResponse(BaseModel):
    """Model for text processing status response"""
    id: int
    status: str
    processing_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LanguageDetectionRequest(BaseModel):
    """Model for language detection request"""
    text: str = Field(
        ..., 
        description="Text to analyze for language detection",
        min_length=1,
        max_length=50000
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Sample text for language detection"
            }
        }
    )


class LanguageDetectionResponse(BaseModel):
    """Model for language detection response"""
    language: str = Field(..., description="Detected language (English, Portuguese, or Unknown)")
    confidence: float = Field(..., description="Confidence level of language detection (0-1)")
    text_length: int = Field(..., description="Length of the original text")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "language": "English",
                "confidence": 0.95,
                "text_length": 30
            }
        }
    )