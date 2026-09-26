import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.db.database import Base
from app.main import app
from app.db.database import get_session


test_engine = create_engine(url=settings.test_database_url)


@pytest.fixture
def session():
    with test_engine.connect() as connection:
        transaction = connection.begin()
        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint"
        )

        yield session

        session.close()
        transaction.rollback()
        

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(test_engine)
    yield
    
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()