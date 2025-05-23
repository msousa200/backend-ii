"""
API routes definition.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
import time
from typing import List, Optional

from app.core.logging_config import get_logger
from app.db.database import get_db
from app.models.product import Product, ProductCreate, ProductResponse
from app.utils.performance import measure_execution_time

logger = get_logger(__name__)

router = APIRouter(tags=["products"])

@router.get("/health/", status_code=200)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    Used for monitoring and container health checks.
    """
    return {"status": "UP", "timestamp": time.time()}

@router.get("/products/", response_model=List[ProductResponse])
@measure_execution_time
async def get_products(
    skip: int = Query(0, ge=0, description="Skip the first N items"),
    limit: int = Query(100, ge=1, le=100, description="Limit the number of items returned"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db=Depends(get_db),
):
    """
    Retrieve all products with pagination and optional filtering.
    """
    try:
        logger.info(f"Retrieving products (skip={skip}, limit={limit}, category={category})")
        
        query = "SELECT id, name, price, category FROM products"
        params = []
        
        if category:
            query += " WHERE category = ?"
            params.append(category)
        
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        cursor = db.execute(query, params)
        rows = cursor.fetchall()
        
        products = [
            ProductResponse(
                id=row[0],
                name=row[1],
                price=row[2],
                category=row[3]
            )
            for row in rows
        ]
        
        logger.debug(f"Retrieved {len(products)} products")
        return products
    
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve products"
        )

@router.get("/products/{product_id}", response_model=ProductResponse)
@measure_execution_time
async def get_product(product_id: int, db=Depends(get_db)):
    """
    Retrieve a product by its ID.
    """
    try:
        logger.info(f"Retrieving product with ID {product_id}")
        
        cursor = db.execute(
            "SELECT id, name, price, category FROM products WHERE id = ?",
            (product_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"Product with ID {product_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID {product_id} not found"
            )
        
        product = ProductResponse(
            id=row[0],
            name=row[1],
            price=row[2],
            category=row[3]
        )
        
        logger.debug(f"Retrieved product: {product}")
        return product
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve product with ID {product_id}"
        )

@router.post("/products/", response_model=ProductResponse, status_code=201)
@measure_execution_time
async def create_product(product: ProductCreate, db=Depends(get_db)):
    """
    Create a new product.
    """
    try:
        logger.info(f"Creating new product: {product.name}")
        
        cursor = db.execute(
            "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
            (product.name, product.price, product.category)
        )
        db.commit()
        
        product_id = cursor.lastrowid
        
        new_product = ProductResponse(
            id=product_id,
            name=product.name,
            price=product.price,
            category=product.category
        )
        
        logger.info(f"Created product with ID {product_id}")
        return new_product
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create product"
        )
