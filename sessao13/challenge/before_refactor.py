"""
Example of a basic FastAPI application without best practices.
This will be refactored to incorporate best practices.
"""

from fastapi import FastAPI, HTTPException
import sqlite3
import time
import random

app = FastAPI()

def get_db():
    return sqlite3.connect("products.db")


@app.get("/products/")
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return {"products": products}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        raise HTTPException(status_code=404, content={"message": "Product not found"})
    

    time.sleep(random.uniform(0.5, 2.0))
    
    return {"product": product}

@app.post("/products/")
def create_product(name: str, price: float, category: str):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
            (name, price, category)
        )
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        

        return {"id": product_id, "name": name, "price": price, "category": category}
    except Exception as e:

        return {"error": str(e)}


@app.on_event("startup")
def init_db():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, category TEXT)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
