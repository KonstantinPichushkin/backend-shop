from decimal import Decimal

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

