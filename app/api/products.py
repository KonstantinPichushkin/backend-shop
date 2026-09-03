from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from app.models.product import Product
from app.db.database import SessionLocal
from app.schemas.product import ProductRead, ProductCreate

app = FastAPI()

@app.get("/products", response_model=list[ProductRead])
def get_products():
    with SessionLocal() as session:
        query = select(Product)
        result = session.execute(query)
        products = result.scalars().all()

        return products

@app.get("/product/{product_id}", response_model=ProductRead)
def get_product(product_id : int):
    with SessionLocal() as session:
        query = select(Product).where(Product.id == product_id)
        result = session.execute(query)
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(
                status_code=404, 
                detail="Product not found"
            )    

        return product
            
         
