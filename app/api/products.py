from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.product import Product
from app.db.database import get_session
from app.schemas.product import ProductRead, ProductCreate, ProductUpdate


app = FastAPI()

@app.get(
    "/products", 
    response_model=list[ProductRead]
)
def get_products(
    session: Session = Depends(get_session)
):
    query = select(Product)
    result = session.execute(query)
    products = result.scalars().all()

    return products


@app.get(
    "/products/{product_id}", 
    response_model=ProductRead
)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    query = select(Product).where(Product.id == product_id)
    product = session.scalar(query)

    if product is None:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )    

    return product
            

@app.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session)
):   
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    query = delete(Product).where(Product.id == product_id)
    result = session.execute(query)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
            
    session.commit()

@app.put(
    "/products/{product_id}",
    response_model=ProductRead
)
def replace_product(
    product_id: int,
    product_data: ProductCreate,
    session: Session = Depends(get_session)
):
    query = select(Product).where(Product.id == product_id)
    product = session.scalar(query)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price

    session.commit()
    session.refresh(product)

    return product


@app.patch(
    "/products/{product_id}",
    response_model=ProductRead
)
def update_product(
    product_id: int, 
    product_data: ProductUpdate,
    session: Session = Depends(get_session)
):
    query = select(Product).where(Product.id == product_id)
    product = session.scalar(query)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    updates = product_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)

    session.commit()
    session.refresh(product)

    return product
        
