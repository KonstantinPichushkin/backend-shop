from decimal import Decimal
from sqlalchemy import select, func

from app.models.product import Product


def test_get_products_empty(client):
    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()
    assert data == []


def test_get_products_one_product(client, session):
    product = Product(
        name="test name",
        description="test description",
        price=Decimal("12.94")    
    )
    
    session.add(product)
    session.commit()
    
    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    actual = data[0]

    assert actual["name"] == product.name
    assert actual["description"] == product.description
    assert actual["price"] == str(product.price)


def test_get_products_multiple_products(client, session):
    products =[
        Product(
            name=f"test name{i}",
            description=f"test description{i}",
            price=Decimal("0.95") + i
        )
        for i in range(10)
    ]

    session.add_all(products)
    session.commit()

    response = client.get("/products/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(products)

    data_by_id = {item["id"] : item for item in data}

    for expected in products:  
        actual = data_by_id[expected.id]
        assert actual["name"] == expected.name
        assert actual["description"] == expected.description
        assert actual["price"] == str(expected.price)


def test_post_product_with_description(client, session):
    request_data = {
            "name": "test_name",
            "description": "test_description",
            "price": "19.25"
    }
    response = client.post(
        "/products/",
        json=request_data
    )

    assert response.status_code == 201
    
    response_product = response.json()
    
    assert response_product["name"] == request_data["name"]
    assert response_product["description"] == request_data["description"]
    assert Decimal(response_product["price"]) == Decimal(request_data["price"])

    query = select(Product).where(Product.id == response_product["id"])
    db_product = session.scalar(query)

    assert db_product.name == request_data["name"]
    assert db_product.description == request_data["description"]
    assert db_product.price == Decimal(request_data["price"])


def test_post_product_without_description(client, session):
    request_data = {
            "name": "test_name",
            "price": "19.250"
    }
    response = client.post(
        "/products/",
        json=request_data
    )

    assert response.status_code == 201

    response_product = response.json()

    assert response_product["name"] == request_data["name"]
    assert response_product["description"] is None
    assert Decimal(response_product["price"]) == Decimal(request_data["price"])

    query = select(Product).where(Product.id == response_product["id"])
    db_product = session.scalar(query)

    assert db_product.name == request_data["name"]
    assert db_product.description is None
    assert db_product.price == Decimal(request_data["price"])


def test_post_product_too_many_digits(client, session):
    request_data = {
        "name": "test_name",
        "price": "9999999999999"
    }
    response = client.post(
        "/products/",
        json=request_data
    )

    assert response.status_code == 422

    errors = response.json()["detail"]

    assert any(error["loc"][-1] == "price" for error in errors)
    
    query = select(func.count()).select_from(Product)
    db_product_count = session.scalar(query)

    assert db_product_count == 0


def test_post_product_negative_price(client, session):
    request_data = {
        "name": "test_name",
        "price": "-23"
    }
    response = client.post(
        "/products/",
        json=request_data
    )

    assert response.status_code == 422    

    errors = response.json()["detail"]

    assert any(error["loc"][-1] == "price" for error in errors)
    
    query = select(func.count()).select_from(Product)
    db_product_count = session.scalar(query)

    assert db_product_count == 0


def test_post_product_too_many_decimal_places(client, session):
    request_data = {
        "name": "test_name",
        "price": "123.123"
    }
    response = client.post(
        "/products/",
        json=request_data
    )

    assert response.status_code == 422    

    errors = response.json()["detail"]

    assert any(error["loc"][-1] == "price" for error in errors)
    
    query = select(func.count()).select_from(Product)
    db_product_count = session.scalar(query)

    assert db_product_count == 0

