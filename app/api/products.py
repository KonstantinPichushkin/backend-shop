from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.services import product as product_service

app = FastAPI()

@app.get(
    "/products", 
    response_model=list[ProductRead]
)
def get_products(
    session: Session = Depends(get_session)
):
    return product_service.get_products(session)


@app.get(
    "/products/{product_id}", 
    response_model=ProductRead
)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = product_service.get_product(session, product_id)

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
    product_data: ProductCreate,
    session: Session = Depends(get_session)
):   
    return product_service.create_product(
        session,
        product_data
    )


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    deleted = product_service.delete_product(session, product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return None        
    

@app.put(
    "/products/{product_id}",
    response_model=ProductRead
)
def replace_product(
    product_id: int,
    product_data: ProductCreate,
    session: Session = Depends(get_session)
):
    product = product_service.replace_product(
        session=session,
        product_id=product_id,
        product_data=product_data
    )
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
   
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
    product = product_service.update_product(
            session=session,
            product_id=product_id,
            product_data=product_data
    )
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product
        
