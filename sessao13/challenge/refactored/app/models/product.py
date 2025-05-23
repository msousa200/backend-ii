"""
Data models for the application.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class ProductBase(BaseModel):
    """Base product model with common attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: float = Field(..., gt=0, description="Product price")
    category: str = Field(..., min_length=1, max_length=50, description="Product category")
    
    @validator("price")
    def validate_price(cls, v):
        """Validate price is reasonable."""
        if v > 1_000_000:
            raise ValueError("Price is unreasonably high")
        return round(v, 2) 

class ProductCreate(ProductBase):
    """Model for creating a new product."""
    pass

class ProductResponse(ProductBase):
    """Model for product responses including ID."""
    id: int = Field(..., description="Product unique identifier")

class Product(ProductBase):
    """Full product model including optional fields."""
    id: Optional[int] = None
    description: Optional[str] = None
    
    class Config:
        orm_mode = True
