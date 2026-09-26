from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.settings import settings


class Base(DeclarativeBase):
    pass


def get_session():
    with session_factory() as session:
        yield session

engine = create_engine(url=settings.database_url)
session_factory = sessionmaker(bind=engine)
