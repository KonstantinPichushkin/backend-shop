from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(url=settings.database_url)
session_factory = sessionmaker(bind=engine)


def get_session():
    with session_factory() as session:
        yield session


