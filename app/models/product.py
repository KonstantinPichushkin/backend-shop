from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))