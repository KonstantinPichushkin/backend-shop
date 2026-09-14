from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_products(
    session: Session
) -> list[Product]:
    query = select(Product)
    result = session.execute(query)
    products = result.scalars().all()

    return products


def get_product(
        session: Session,
        product_id: int
) -> Product | None:
    query = select(Product).where(Product.id == product_id)
    return session.scalar(query)


def create_product(
    session: Session,
    product_data: ProductCreate
) -> Product:   
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product


def delete_product(
    session: Session,
    product_id: int
) -> bool:
    query = delete(Product).where(Product.id == product_id)
    result = session.execute(query)
    
    if result.rowcount == 0:
        return False

    session.commit()
    return True


def replace_product(
    session: Session,
    product_id: int,
    product_data: ProductCreate
) -> Product | None:
    query = select(Product).where(Product.id == product_id)
    product = session.scalar(query)

    if product is None:
        return None

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price

    session.commit()
    session.refresh(product)

    return product


def update_product(
    session: Session,
    product_id: int,
    product_data: ProductUpdate
) -> Product | None:
    query = select(Product).where(Product.id == product_id)
    product = session.scalar(query)

    if product is None:
        return None

    updates = product_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)

    session.commit()
    session.refresh(product)

    return product