from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(url=settings.database_url)

