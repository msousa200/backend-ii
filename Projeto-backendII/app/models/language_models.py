from pydantic import BaseModel, Field
from typing import Optional


class LanguageDetectionRequest(BaseModel):
    """Model for language detection request"""
    text: str = Field(
        ..., 
        description="Text to detect language",
        min_length=1,
        max_length=50000  
    )

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a sample text for language detection."
            }
        }


class LanguageDetectionResponse(BaseModel):
    """Model for language detection response"""
    language: str = Field(..., description="Detected language (English, Portuguese, or Unknown)")
    confidence: float = Field(..., description="Confidence score (0-1) for language detection")
    text_length: int = Field(..., description="Length of the analyzed text")

    class Config:
        json_schema_extra = {
            "example": {
                "language": "English",
                "confidence": 0.95,
                "text_length": 42
            }
        }
